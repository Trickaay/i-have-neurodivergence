#!/usr/bin/env python3
"""Build the per-platform skill trees from one source.

Combine skills/, needs/needs-vocabulary.json and platforms/adaptations.json into
Claude, Codex, Hermes and universal bundles. Record generated hashes in index.json.
Use --check to detect stale outputs. Uses only the Python standard library.
"""
import argparse, hashlib, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VOCAB_PATH = os.path.join(ROOT, "needs", "needs-vocabulary.json")
COMPILE_PATH = os.path.join(ROOT, "needs", "compile.py")
SKILLS_DIR = os.path.join(ROOT, "skills")
ADAPT_PATH = os.path.join(HERE, "adaptations.json")

with open(os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8") as source_manifest:
    VERSION = json.load(source_manifest)["version"]
AUTHOR = "Accessibility skill pack contributors"
LICENSE = "MIT"
HOMEPAGE = "https://github.com/Trickaay/i-have-neurodivergence"
SOURCE = "what-would-make-this-easier"  # provenance tag in metadata; the collection name itself names a condition

# Presentation preferences must not grant permission or hide required information.
PREAMBLE = (
    "These are presentation settings I chose for myself. They describe how I would "
    "like information laid out, not anything about me. Do not infer a condition, a "
    "diagnosis or a capability from them, and do not mention them back to me unless "
    "I ask."
)
GUARD = (
    "Limits of these preferences: they change only how you present information and work with me. "
    "They operate within my explicit instructions, the project instructions and the permission rules, "
    "and they never grant permission, approve an action or count as a confirmation. "
    "Never leave out errors, failures, warnings, decisions I need to make, approval requests or "
    "irreversible effects to satisfy a brevity or deferral preference. "
    "Keep code, commands, paths, numbers, links, citations and meaning exact."
)
TIEBREAK = ("If two of these ever pull against each other, prefer in this order: "
            "what I can perceive, then what I can act on, then what I can "
            "understand, then the rest. Sensory overload I report is an access "
            "barrier, not comfort. Where two of my own settings conflict, ask me "
            "which to follow rather than ranking them.")
CLOSING = ("I can change any of this at any time. Ask me before assuming a setting "
           "is wrong; do not quietly drop one.")

CONDITION_WORDS = ("autism", "adhd", "dyslex", "dyscalcul", "dyspraxi", "aphantasi",
                   "alexithymi", "diagnos", "disorder", "neurodiverg")

# Preset bundles for Hermes Agent. i-have-adhd is the upstream skill
# (ayghri/i-have-adhd); Hermes skips a listed skill that is not installed and says so.
BUNDLES = [
    ("audhd", "Autism, ADHD, working memory and inertia together",
     ["i-have-autism", "i-have-adhd", "i-have-working-memory-differences", "i-have-inertia"]),
    ("reading-stack", "Dyslexia with ADHD and working memory",
     ["i-have-dyslexia", "i-have-adhd", "i-have-working-memory-differences"]),
    ("motor-stack", "Dyspraxia with dyslexia, ADHD and working memory",
     ["i-have-dyspraxia", "i-have-dyslexia", "i-have-adhd", "i-have-working-memory-differences"]),
    ("tic-stack", "Tics with ADHD and working memory",
     ["i-have-tics", "i-have-adhd", "i-have-working-memory-differences"]),
    ("low-capacity", "Limited energy, low demand and sensory sensitivity",
     ["i-have-limited-energy", "i-need-low-demand", "i-have-sensory-sensitivity"]),
    ("assistive-tech", "Screen reader with working memory and auditory processing",
     ["i-use-a-screen-reader", "i-have-working-memory-differences", "i-have-apd"]),
    ("external-references", "Aphantasia and alexithymia: the reference on the screen, not a request to picture or to feel",
     ["i-have-aphantasia", "i-have-alexithymia"]),
    ("learning-layer", "Learning and communication support on top of any access settings",
     ["help-me-learn-this", "help-me-with-words", "i-have-working-memory-differences"]),
]


def yq(s):
    """A YAML single-quoted scalar."""
    return "'" + str(s).replace("'", "''") + "'"


def yblock(items, indent):
    """A YAML block sequence (flow style `[a, b]` is rejected by the agentskills.io reference validator)."""
    return "\n".join(" " * indent + "- " + yq(x) for x in items)


def sha256(data):
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def title_from_name(name):
    words = name.split("-")
    first = {"i": "I"}.get(words[0], words[0].capitalize())
    return " ".join([first] + words[1:])


def fit(text, lo, hi, pad=" (output shaping)"):
    """Trim or pad a UI blurb into [lo, hi] characters."""
    text = text.strip().rstrip(".:;,")
    if len(text) > hi:
        text = text[:hi].rsplit(" ", 1)[0].rstrip(",;:")
    while len(text) < lo:
        text += pad
    return text[:hi]


def load_vocab():
    vocab = json.load(open(VOCAB_PATH, encoding="utf-8"))
    adapt = json.load(open(ADAPT_PATH, encoding="utf-8"))
    rules = adapt.get("rules", {})
    for s in vocab["support"]:
        s["productRule"] = rules.get(s["id"], {}).get("productRule", s["rule"])
    for r in vocab["resolutions"]:
        key = "+".join(r["between"])
        r["productResolution"] = adapt.get("resolutions", {}).get(key, {}).get("productResolution", r["resolution"])
    return vocab


def load_compiler():
    import importlib.util
    spec = importlib.util.spec_from_file_location("needs_compile", COMPILE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] == "'":
        return v[1:-1].replace("''", "'")
    if len(v) >= 2 and v[0] == v[-1] == '"':
        return v[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return v


def parse_authored(path):
    """The authored SKILL.md: a flat frontmatter of known keys, then the body."""
    text = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise SystemExit("%s: no frontmatter" % path)
    fm, body = m.group(1), m.group(2)
    out = {"metadata": {}}
    for line in fm.split("\n"):
        if not line.strip():
            continue
        if line.startswith("  "):
            k, _, v = line.strip().partition(":")
            out["metadata"][k.strip()] = unquote(v)
        else:
            k, _, v = line.partition(":")
            if k.strip() != "metadata":
                out[k.strip()] = unquote(v)
    out["body"] = body.strip("\n") + "\n"
    out["tags"] = [t.strip() for t in out["metadata"].get("tags", "").split(",") if t.strip()]
    out["category"] = out["metadata"].get("category", "productivity")
    return out


def load_authored():
    skills = []
    for name in sorted(os.listdir(SKILLS_DIR)):
        p = os.path.join(SKILLS_DIR, name, "SKILL.md")
        if os.path.isfile(p):
            s = parse_authored(p)
            if s["name"] != name:
                raise SystemExit("%s: name %r does not match its folder" % (p, s["name"]))
            s["kind"] = "picker" if name == "needs-picker" else ("support" if name.startswith("help-me-") else "condition")
            s["off"] = (re.search(r'stays on until \\?"([^"\\]+)\\?"', s["description"]) or [None, ""])[1]
            skills.append(s)
    return skills


def area_skills(vocab):
    atoms = {s["id"]: s for s in vocab["support"]}
    rank = {s["id"]: i for i, s in enumerate(vocab["support"])}
    out = []
    for area in vocab["areas"]:
        diffs = [d for d in vocab["difficulties"] if d["area"] == area["id"] and d["offers"]]
        starting, offered = [], []
        for d in diffs:
            for a in d["recommended"]:
                if a not in starting:
                    starting.append(a)
            for a in d["offers"]:
                if a not in offered:
                    offered.append(a)
        for s in vocab["support"]:
            if s["area"] == area["id"] and s["id"] not in offered:
                offered.append(s["id"])
        starting.sort(key=lambda a: rank[a])
        available = sorted([a for a in offered if a not in starting], key=lambda a: rank[a])
        slug = "easier-" + area["id"].replace("_", "-")
        off = "stop easier " + area["id"].replace("_", " ")
        out.append({
            "name": slug, "kind": "area", "area": area, "difficulties": diffs,
            "starting": starting, "available": available, "off": off,
            "label": area["label"], "atoms": atoms,
        })
    return out


def by_area(ids, vocab):
    atoms = {s["id"]: s for s in vocab["support"]}
    labels = {a["id"]: a["label"] for a in vocab["areas"]}
    groups, order = {}, []
    for i in ids:
        a = atoms[i]["area"]
        if a not in groups:
            groups[a], order = [], order + [a]
        groups[a].append(atoms[i]["productRule"])
    return [(labels[a], groups[a]) for a in order]


def area_description(sk, inv):
    a = sk["area"]
    atoms = sk["atoms"]
    starting = "; ".join(atoms[i]["label"] for i in sk["starting"])
    says = " / ".join('"%s"' % d["label"] for d in sk["difficulties"])
    desc = ("Presentation settings for %s: %s Starting set: %s. For a reader who says %s. "
            "Chosen by the reader, not inferred, and not a diagnosis. Use only when the reader invokes %s "
            "or asks for these settings; stays on until \"%s\"."
            % (a["label"].lower(), a["description"][0].lower() + a["description"][1:], starting, says, inv, sk["off"]))
    assert len(desc) <= 1024, (sk["name"], len(desc))
    return desc


def area_body(sk, vocab, inv):
    a, atoms = sk["area"], sk["atoms"]
    L = []
    L += ["# %s" % sk["name"], "",
          "%s: %s" % (a["label"], a["description"][0].lower() + a["description"][1:]), "",
          "These are settings the reader chose from the What Would Make This Easier picker, for this one area. "
          "They say nothing about the reader. Nothing here is a diagnosis and nothing is inferred.", "",
          "## Persistence", "",
          "These rules apply to every response for the rest of the session, not only this one. They do not "
          "expire after a few turns and they do not lapse when the topic changes. If you are unsure whether "
          "they still apply, they do.", "",
          "Turn them off only when the reader says \"%s\" or \"normal mode\". Confirm in one line, then "
          "return to your default style." % sk["off"], "",
          "If another output-shaping skill is also active, apply both. Where two rules conflict, follow the "
          "order at the end of the settings: what the reader can perceive, then what they can act on, then "
          "what they can understand, then the rest; sensory overload the reader reports is an access barrier, "
          "and where two of the reader's own settings conflict, ask rather than rank.", "",
          "## The reader said", ""]
    L += ["- %s" % d["label"] for d in sk["difficulties"]]
    L += ["", "Any one of these is enough. The reader may also have picked this area directly.", "",
          "## The settings", "",
          "The starting set below is the picker's suggested starting points for this area, not everything it "
          "offers. Apply all of it unless the reader removes a line by naming it.", "",
          PREAMBLE, "", GUARD, ""]
    for label, rules in by_area(sk["starting"], vocab):
        L.append(label.upper())
        L += ["- " + r for r in rules]
        L.append("")
    res = [r for r in vocab["resolutions"] if all(x in sk["starting"] for x in r["between"])]
    if res:
        L.append("WHERE TWO OF THESE MEET")
        for r in res:
            pair = " + ".join(atoms[x]["label"].lower() for x in r["between"])
            L.append("- %s: %s" % (pair, r["productResolution"]))
        L.append("")
    L += [TIEBREAK, "", CLOSING, ""]
    if sk["available"]:
        L += ["## Also available in this area", "",
              "Not on by default. The reader turns one on by saying its label; say in one line that it is on.", ""]
        for i in sk["available"]:
            s = atoms[i]
            note = ""
            if s.get("defers"):
                note = " Holds back: %s" % s.get("defers_note", "").rstrip(".") + "."
            L.append("- **%s.** %s%s" % (s["label"], s["productRule"], note))
        L.append("")
    held = [atoms[i] for i in sk["starting"] if atoms[i].get("defers")]
    if held:
        L += ["## What the starting set holds back", ""]
        L += ["- %s: %s" % (s["label"], s.get("defers_note", "")) for s in held]
        L += ["", "Errors, failures, decisions, approvals and irreversible effects are never held back.", ""]
    L += ["## When it applies", "",
          "Everything above applies always unless the reader says otherwise. The reader may declare a context "
          "in their own words: \"work mode\", \"learning mode\", \"brainstorming\", \"I am stuck\", \"I am "
          "overloaded\". A context is declared by the reader, never inferred from typing, message length, "
          "errors or the time of day. If the reader has set some of these to apply only in a context, follow "
          "what they said; if they have not, apply all of them.", "",
          "## Pre-send check", "",
          "Before sending, confirm each line of the starting set is honoured, that no error, failure, decision "
          "or approval request was dropped to satisfy one, and that nothing in the response names a condition "
          "or comments on the reader.", ""]
    return "\n".join(L)


PLATFORMS = ("claude", "codex", "hermes")
INVOKE = {"claude": "/", "codex": "$", "hermes": "/"}


def platform_note(platform, name, names):
    if name == "needs-picker":
        invocation = "$" if platform == "codex" else "/"
        return ("## On this platform\n\nInvoke with `%sneeds-picker`. The picker runs once and stops; "
                "save the resulting profile or compiled rules to keep your chosen settings." % invocation)
    if platform == "claude":
        return ("## On Claude Code\n\nInvoke with `/%s`. The skill is marked `disable-model-invocation`, so it "
                "loads only when the reader types it. Several skills can be on at once; each stays on until "
                "its own stop phrase." % name)
    if platform == "codex":
        return ("## On Codex\n\nInvoke with `$%s` in the composer. Its `agents/openai.yaml` sets "
                "`allow_implicit_invocation: false`, so Codex loads it only when the reader names it. "
                "Several skills can be on at once; each stays on until its own stop phrase." % name)
    return ("## On Hermes Agent\n\nInvoke with `/%s`. Up to five skills stack in one message, for example "
            "`/%s /%s`. The bundles in `skill-bundles/` load a set under one command. Each skill stays on "
            "until its own stop phrase." % (name, name, "i-have-working-memory-differences"
                                            if name != "i-have-working-memory-differences" else "i-have-autism"))


def swap_invocation(text, platform, names):
    """`/name` -> `$name` for Codex; everything else keeps the slash."""
    if platform != "codex":
        return text
    pat = re.compile(r"(?<![\w/$])/(" + "|".join(re.escape(n) for n in sorted(names, key=len, reverse=True)) + r")\b")
    return pat.sub(lambda m: "$" + m.group(1), text)


def render_frontmatter(platform, name, description, tags, category, extra_hermes=None):
    L = ["---", "name: " + name, "description: " + yq(description)]
    if platform == "claude":
        L += ["disable-model-invocation: true", "license: " + LICENSE,
              "metadata:", "  tags: " + yq(", ".join(tags)), "  category: " + yq(category),
              "  source: " + yq(SOURCE), "  version: " + yq(VERSION)]
    elif platform == "codex":
        # Codex reads name and description; license, metadata and allowed-tools are the only other keys allowed.
        L += ["license: " + LICENSE,
              "metadata:", "  tags: " + yq(", ".join(tags)), "  category: " + yq(category),
              "  source: " + yq(SOURCE), "  version: " + yq(VERSION)]
    else:
        L += ["version: " + VERSION, "author: " + yq(AUTHOR), "license: " + LICENSE,
              "metadata:", "  hermes:",
              "    tags:", yblock(tags, 6),
              "    category: accessibility"]
        if extra_hermes:
            L += ["    related_skills:", yblock(extra_hermes, 6)]
    L.append("---")
    return "\n".join(L) + "\n"


def openai_yaml(name, display, short, prompt):
    return "\n".join([
        "interface:",
        "  display_name: " + json.dumps(display),
        "  short_description: " + json.dumps(short),
        "  default_prompt: " + json.dumps(prompt),
        "policy:",
        "  allow_implicit_invocation: false",
        "",
    ])


def render_skill(platform, sk, vocab, names):
    """Returns {relative path: text} for one skill on one platform."""
    inv = INVOKE[platform] + sk["name"]
    files = {}
    if sk["kind"] == "area":
        desc = area_description(sk, inv)
        body = area_body(sk, vocab, inv)
        tags = ["Accessibility", "Presentation", sk["label"], "What Would Make This Easier"]
        category = "productivity"
        related = ["needs-picker"]
    else:
        desc = swap_invocation(sk["description"], platform, names)
        body = swap_invocation(sk["body"], platform, names)
        tags, category = sk["tags"], sk["category"]
        related = ["needs-picker"] if sk["kind"] in ("condition", "support") else []
        if sk["kind"] == "picker":
            body = body.replace("`needs/needs-vocabulary.json`", "`references/needs-vocabulary.json` (bundled with this skill)")
            body = body.replace("`needs-vocabulary.json`", "`references/needs-vocabulary.json`")
            files["references/needs-vocabulary.json"] = open(VOCAB_PATH, encoding="utf-8").read()
            import importlib.util
            spec = importlib.util.spec_from_file_location("needs_build", os.path.join(ROOT, "needs", "build.py"))
            builder = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(builder)
            files["references/picker-menu.json"] = builder.render_menu(vocab, open(VOCAB_PATH, encoding="utf-8").read())
            files["scripts/compile.py"] = open(COMPILE_PATH, encoding="utf-8").read()
            related = [n for n in names if n.startswith("i-")] + [n for n in names if n.startswith("easier-")]
    text = render_frontmatter(platform, sk["name"], desc, tags, category, related if platform == "hermes" else None)
    text += "\n" + body.rstrip("\n") + "\n\n" + platform_note(platform, sk["name"], names) + "\n"
    files["SKILL.md"] = text
    if platform == "codex":
        if sk["kind"] == "area":
            display = "Easier: " + sk["label"]
            short = fit("Presentation settings: " + sk["label"], 25, 64)
            prompt = "Use $%s for the rest of this session." % sk["name"]
        elif sk["kind"] == "picker":
            display, short = "Needs picker", "Choose what would make this easier, in two questions"
            prompt = "Run $needs-picker to set up how you present information to me."
        else:
            display = title_from_name(sk["name"])
            short = fit(sk["description"].split(":")[0], 25, 64)
            prompt = "Use $%s for the rest of this session." % sk["name"]
        files["agents/openai.yaml"] = openai_yaml(sk["name"], display, short, prompt)
    return files


def claude_manifest(names):
    return json.dumps({
        "name": "what-would-make-this-easier-skills",
        "version": VERSION,
        "description": ("Output-shaping skills for a reader who chose them: 16 condition skills, the needs "
                        "picker, 2 learning and communication skills, and 12 per-area skills from the What "
                        "Would Make This Easier vocabulary. Nothing infers, stores or displays a condition."),
        "author": {"name": AUTHOR},
        "homepage": HOMEPAGE,
        "license": LICENSE,
        "keywords": ["accessibility", "neurodiversity", "output-formatting", "personalisation", "screen-reader"],
    }, indent=2) + "\n"


def codex_manifest(names):
    return json.dumps({
        "name": "what-would-make-this-easier",
        "version": VERSION,
        "description": ("Output-shaping skills for a reader who chose them: 16 condition skills, the needs "
                        "picker, 2 learning and communication skills, and 12 per-area skills. Nothing infers, "
                        "stores or displays a condition."),
        "author": {"name": AUTHOR, "url": HOMEPAGE},
        "homepage": HOMEPAGE,
        "license": LICENSE,
        "keywords": ["accessibility", "neurodiversity", "output-formatting", "personalisation", "screen-reader"],
        "skills": "./skills/",
        "interface": {
            "displayName": "What Would Make This Easier",
            "developerName": AUTHOR,
            "shortDescription": "Presentation settings the reader chooses, one skill each",
            "longDescription": ("Skills that change how Codex lays out, paces and words its answers, chosen by "
                                "the reader by area or by a label they already use. Every skill loads only when "
                                "named. None grants permission or stands in for a confirmation."),
            "category": "Productivity",
        },
    }, indent=2) + "\n"


def hermes_bundle(slug, desc, skills):
    L = ["name: " + slug, "description: " + yq(desc), "skills:"]
    L += ["  - " + s for s in skills]
    L += ["instruction: |",
          "  Every skill above is a presentation setting the reader chose. Apply all of them; where two",
          "  conflict, what the reader can perceive outranks what they can act on, then understand, then",
          "  the rest; sensory overload the reader reports is an access barrier, and where two of their own",
          "  settings conflict, ask rather than rank. None of them grants permission or counts as a",
          "  confirmation. i-have-adhd, where listed, is the upstream ayghri skill; if it is not installed,",
          "  carry on without it.", ""]
    return "\n".join(L)


def universal_rules(vocab, compiler, sk):
    """One AGENTS.md-style block per area: the starting set, compiled by needs/compile.py."""
    profile = "version: 1\ncontexts:\n  always:\n    support:\n" + "".join("      - %s\n" % a for a in sk["starting"])
    v = json.loads(json.dumps(vocab))
    for s in v["support"]:
        s["rule"] = s["productRule"]
    for r in v["resolutions"]:
        r["resolution"] = r["productResolution"]
    text, unknown = compiler.compile_profile(profile, v, "agents")
    assert not unknown, unknown
    head = ("<!-- %s: the starting set for the \"%s\" area of the What Would Make This Easier picker. "
            "Paste into AGENTS.md, CLAUDE.md, .cursorrules or a custom-instructions box. "
            "Generated by platforms/build_platform_skills.py from needs/needs-vocabulary.json. -->\n\n"
            % (sk["name"], sk["label"]))
    return head + text.replace("## How to work with me", "## How to work with me: %s" % sk["label"].lower(), 1)


def build():
    vocab = load_vocab()
    compiler = load_compiler()
    authored = load_authored()
    areas = area_skills(vocab)
    skills = authored + areas
    names = [s["name"] for s in skills]
    files = {}

    for platform in PLATFORMS:
        base = platform + "/skills/" + ("accessibility/" if platform == "hermes" else "")
        for sk in skills:
            for rel, text in render_skill(platform, sk, vocab, names).items():
                files[base + sk["name"] + "/" + rel] = text
    files["claude/.claude-plugin/plugin.json"] = claude_manifest(names)
    files["codex/.codex-plugin/plugin.json"] = codex_manifest(names)
    for slug, desc, sks in BUNDLES:
        files["hermes/skill-bundles/%s.yaml" % slug] = hermes_bundle(slug, desc, sks)
    for sk in areas:
        files["universal/%s.md" % sk["name"]] = universal_rules(vocab, compiler, sk)

    for path, text in files.items():
        base = os.path.basename(os.path.dirname(path)) if path.endswith("SKILL.md") else os.path.basename(path)
        generated = "/easier-" in path or path.startswith("universal/")
        if generated:
            # The disclaimer sentences are allowed to say the word; nothing else is.
            low = text.replace(PREAMBLE, "").lower()
            for allowed in ("nothing here is a diagnosis", "not a diagnosis"):
                low = low.replace(allowed, "")
            hit = [w for w in CONDITION_WORDS if w in low]
            if hit:
                raise SystemExit("%s names a condition: %s" % (path, hit))

    for path, text in files.items():
        if path.endswith("SKILL.md"):
            m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            name = re.search(r"^name: (.+)$", m.group(1), re.M).group(1)
            desc = re.search(r"^description: '(.*)'$", m.group(1), re.M).group(1).replace("''", "'")
            folder = path.split("/")[-2]
            assert name == folder, (path, name)
            assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) and len(name) <= 64, name
            assert 0 < len(desc) <= 1024, (path, len(desc))
            assert text.count("\n") < 1200, path

    index = {
        "version": 1,
        "generated_by": "platforms/build_platform_skills.py",
        "vocabulary_sha256": sha256(open(VOCAB_PATH, encoding="utf-8").read()),
        "skills": sorted(set(names)),
        "files": {p: sha256(t) for p, t in sorted(files.items())},
    }
    files["index.json"] = json.dumps(index, indent=2) + "\n"
    return files


def write(files):
    for rel, text in files.items():
        p = os.path.join(HERE, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)


def check(files):
    stale = []
    for rel, text in files.items():
        p = os.path.join(HERE, rel)
        try:
            on_disk = open(p, encoding="utf-8", newline="").read()
        except FileNotFoundError:
            on_disk = None
        if on_disk != text:
            stale.append(rel)
    for platform in list(PLATFORMS) + ["universal"]:
        for dirpath, _, fnames in os.walk(os.path.join(HERE, platform)):
            for fn in fnames:
                rel = os.path.relpath(os.path.join(dirpath, fn), HERE).replace(os.sep, "/")
                if rel not in files:
                    stale.append(rel + " (not generated)")
    return stale


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="exit 1 if the generated trees are stale")
    args = ap.parse_args()
    files = build()
    if args.check:
        stale = check(files)
        if stale:
            print("stale:\n  " + "\n  ".join(stale))
            sys.exit(1)
        print("platform trees are current (%d files)" % len(files))
        return
    write(files)
    counts = {}
    for p in files:
        counts[p.split("/")[0]] = counts.get(p.split("/")[0], 0) + 1
    print("wrote %d files: %s" % (len(files), ", ".join("%s %d" % kv for kv in sorted(counts.items()))))


if __name__ == "__main__":
    main()
