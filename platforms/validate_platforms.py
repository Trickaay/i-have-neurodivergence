#!/usr/bin/env python3
"""Validate the generated platform trees against each platform's published rules.

Development-only dependencies (the generator itself needs none):
    pip install pyyaml skills-ref

Checks, per SKILL.md:
  * agentskills.io reference validator (skills-ref): name/description constraints, name == folder
  * Claude: `disable-model-invocation: true` present
  * Codex: only name, description, license, metadata, allowed-tools in the frontmatter (the set Codex's
    own quick_validate.py allows); agents/openai.yaml parses, short_description is 25-64 characters,
    default_prompt names `$<skill>`, policy.allow_implicit_invocation is false
  * Hermes: name, description, version present; metadata.hermes.tags is a list; category set
  * generated files (easier-*, universal/) name no condition
Then: every file listed in index.json exists with the recorded sha256.
"""
import hashlib, json, os, re, sys

import yaml

try:
    from skills_ref import validate as ref_validate
except ImportError:  # pragma: no cover
    ref_validate = None

HERE = os.path.dirname(os.path.abspath(__file__))
CONDITION_WORDS = ("autism", "adhd", "dyslex", "dyscalcul", "dyspraxi", "aphantasi",
                   "alexithymi", "diagnos", "disorder", "neurodiverg")
ALLOWED = {"nothing here is a diagnosis", "not a diagnosis",
           "do not infer a condition, a diagnosis or a capability"}
CODEX_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}

problems = []
counts = {"claude": 0, "codex": 0, "hermes": 0}


def fail(path, msg):
    problems.append("%s: %s" % (os.path.relpath(path, HERE), msg))


def frontmatter(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        fail(path, "no frontmatter"); return None, text
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        fail(path, "frontmatter YAML: %s" % e); return None, text
    return fm, text


def check_skill(platform, skill_dir):
    path = os.path.join(skill_dir, "SKILL.md")
    fm, text = frontmatter(path)
    if fm is None:
        return
    counts[platform] += 1
    name = os.path.basename(skill_dir)
    if fm.get("name") != name:
        fail(path, "name %r != folder %r" % (fm.get("name"), name))
    if not (1 <= len(fm.get("description", "")) <= 1024):
        fail(path, "description length %d" % len(fm.get("description", "")))
    if text.count("\n") > 500:
        fail(path, "body over 500 lines (%d); the spec recommends splitting" % text.count("\n"))
    if ref_validate is not None:
        try:
            errs = ref_validate(skill_dir)
            for e in errs or []:
                # Each host's own keys sit outside the open spec: Claude's disable-model-invocation,
                # Hermes's top-level version and author (its contributor template requires them).
                # Everything else is a real finding.
                msg = str(e)
                if platform == "claude" and "disable-model-invocation" in msg:
                    continue
                if platform == "hermes" and msg.startswith("Unexpected fields in frontmatter: author, version."):
                    continue
                fail(path, "skills-ref: %s" % e)
        except Exception as e:  # pragma: no cover
            fail(path, "skills-ref raised: %s" % e)
    if platform == "claude":
        if fm.get("disable-model-invocation") is not True:
            fail(path, "missing disable-model-invocation: true")
    if platform == "codex":
        extra = set(fm) - CODEX_KEYS
        if extra:
            fail(path, "frontmatter keys Codex rejects: %s" % sorted(extra))
        ypath = os.path.join(skill_dir, "agents", "openai.yaml")
        if not os.path.isfile(ypath):
            fail(path, "agents/openai.yaml missing")
        else:
            y = yaml.safe_load(open(ypath, encoding="utf-8"))
            sd = y.get("interface", {}).get("short_description", "")
            if not (25 <= len(sd) <= 64):
                fail(ypath, "short_description is %d characters, not 25-64: %r" % (len(sd), sd))
            if "$" + name not in y.get("interface", {}).get("default_prompt", ""):
                fail(ypath, "default_prompt does not name $%s" % name)
            if y.get("policy", {}).get("allow_implicit_invocation") is not False:
                fail(ypath, "policy.allow_implicit_invocation is not false")
        if "$" + name not in fm["description"]:
            fail(path, "description does not say how to invoke ($%s)" % name)
    if platform == "hermes":
        for k in ("name", "description", "version"):
            if k not in fm:
                fail(path, "missing %s" % k)
        h = (fm.get("metadata") or {}).get("hermes") or {}
        if not isinstance(h.get("tags"), list) or not h["tags"]:
            fail(path, "metadata.hermes.tags is not a non-empty list")
        if not h.get("category"):
            fail(path, "metadata.hermes.category missing")
        if "/" + name not in fm["description"]:
            fail(path, "description does not say how to invoke (/%s)" % name)
    if name.startswith("easier-"):
        low = text.lower()
        for a in ALLOWED:
            low = low.replace(a, "")
        hit = [w for w in CONDITION_WORDS if w in low]
        if hit:
            fail(path, "generated skill names a condition: %s" % hit)


def main():
    for platform in ("claude", "codex", "hermes"):
        root = os.path.join(HERE, platform, "skills")
        for dirpath, dirnames, filenames in os.walk(root):
            if "SKILL.md" in filenames:
                check_skill(platform, dirpath)
                dirnames[:] = []
    for fn in os.listdir(os.path.join(HERE, "universal")):
        p = os.path.join(HERE, "universal", fn)
        low = open(p, encoding="utf-8").read().lower()
        for a in ALLOWED:
            low = low.replace(a, "")
        hit = [w for w in CONDITION_WORDS if w in low]
        if hit:
            fail(p, "names a condition: %s" % hit)
    for slug in os.listdir(os.path.join(HERE, "hermes", "skill-bundles")):
        p = os.path.join(HERE, "hermes", "skill-bundles", slug)
        b = yaml.safe_load(open(p, encoding="utf-8"))
        if not b.get("skills"):
            fail(p, "bundle lists no skills")
    index = json.load(open(os.path.join(HERE, "index.json"), encoding="utf-8"))
    for rel, digest in index["files"].items():
        p = os.path.join(HERE, rel)
        if not os.path.isfile(p):
            fail(p, "listed in index.json but missing"); continue
        actual = hashlib.sha256(open(p, "rb").read()).hexdigest()
        if actual != digest:
            fail(p, "sha256 differs from index.json")
    print("checked %s skills; skills-ref %s" % (counts, "used" if ref_validate else "NOT installed"))
    if problems:
        print("\n".join("FAIL  " + p for p in problems))
        sys.exit(1)
    print("all platform trees valid")


if __name__ == "__main__":
    main()
