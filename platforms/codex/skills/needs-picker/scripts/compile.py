#!/usr/bin/env python3
"""Compile a support profile into something you can paste into any agent.

Uses only the Python standard library. See --help for output formats and options.
Run --self-test to check parsing and all output formats.
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.join(HERE, "needs-vocabulary.json")
if not os.path.isfile(VOCAB):
    VOCAB = os.path.join(HERE, "..", "references", "needs-vocabulary.json")

FORMATS = ("rules", "skill", "agents", "json", "hermes", "codex")


def parse_profile(text):
    """Parse the restricted YAML the picker emits. Not a general YAML parser.

    Accepts exactly:
        version: 1
        contexts:
          <context>:
            difficulties: [- item]
            support:      [- item]
            suppress:     [- item]
            presets:      [- item]
            notes: |
              free text
    Notes also accept a JSON-quoted string, preserving whitespace and line endings.
    Anything else raises, with the line number, rather than being silently ignored.
    """
    profile = {"version": None, "contexts": {}}
    ctx = None
    key = None
    notes_indent = None
    notes = []

    for n, raw in enumerate(text.replace("\r\n", "\n").replace("\r", "\n").split("\n"), 1):
        line = raw.rstrip()

        if notes_indent is not None:
            if line.strip() == "" or (len(line) - len(line.lstrip())) >= notes_indent:
                notes.append(raw[notes_indent:] if len(raw) >= notes_indent else "")
                continue
            profile["contexts"][ctx]["notes"] = "\n".join(notes).rstrip("\n")
            notes_indent, notes = None, []

        if not line.strip() or line.lstrip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())
        body = line.strip()

        if indent == 0:
            key = None
            if body.startswith("version:"):
                profile["version"] = body.split(":", 1)[1].strip()
            elif body in ("contexts:",):
                ctx = None
            else:
                raise ValueError("line %d: unexpected top-level key %r" % (n, body))
        elif indent == 2:
            if not body.endswith(":"):
                raise ValueError("line %d: expected a context name, got %r" % (n, body))
            ctx = body[:-1].strip()
            profile["contexts"].setdefault(ctx, {})
            key = None
        elif indent == 4:
            if ctx is None:
                raise ValueError("line %d: %r appears before any context" % (n, body))
            # `support: []   # base layer only` — structural lines may carry a comment.
            if not body.startswith("notes:") and " #" in body:
                body = body.split(" #", 1)[0].strip()
            if body.startswith("notes:"):
                rest = body.split(":", 1)[1].strip()
                if rest in ("|", "|-", ">"):
                    notes_indent, notes = 6, []
                elif rest.startswith('"'):
                    profile["contexts"][ctx]["notes"] = json.loads(rest)
                else:
                    profile["contexts"][ctx]["notes"] = rest
                key = None
            elif body.endswith(":") or body.endswith(": []"):
                key = body.split(":", 1)[0].strip()
                profile["contexts"][ctx].setdefault(key, [])
            else:
                raise ValueError("line %d: expected a list name, got %r" % (n, body))
        elif indent == 6 and body.startswith("- "):
            if key is None:
                raise ValueError("line %d: list item with no list: %r" % (n, body))
            profile["contexts"][ctx][key].append(body[2:].strip())
        else:
            raise ValueError("line %d: unexpected indentation: %r" % (n, raw))

    if notes_indent is not None:
        profile["contexts"][ctx]["notes"] = "\n".join(notes).rstrip("\n")
    return profile


def resolve(profile, vocab):
    """The composer, exactly as NEEDS_MODEL.md specifies it.

    1. Expand presets to atoms.  2. Union each context's support.
    3. Apply that context's suppressions.  4. Deduplicate.
    Order is the vocabulary's own area order, so the same profile always
    compiles to the same text.
    """
    atoms = {s["id"]: s for s in vocab["support"]}
    area_rank = {a["id"]: i for i, a in enumerate(vocab["areas"])}
    atom_rank = {s["id"]: i for i, s in enumerate(vocab["support"])}
    presets = vocab["presets"]

    unknown = []
    out = {}
    for name, block in profile["contexts"].items():
        chosen = []
        for p in block.get("presets", []):
            if p not in presets:
                unknown.append("preset %r" % p)
                continue
            chosen.extend(presets[p])
        chosen.extend(block.get("support", []))

        suppressed = set(block.get("suppress", []))
        seen, keep = set(), []
        for a in chosen:
            if a not in atoms:
                unknown.append("support %r" % a)
                continue
            if a in suppressed or a in seen:
                continue
            seen.add(a)
            keep.append(a)
        keep.sort(key=lambda a: (area_rank.get(atoms[a]["area"], 99), atom_rank[a]))
        out[name] = keep

    return out, unknown


def applicable_resolutions(active, vocab):
    """Return resolutions whose two supports are active."""
    return [r for r in vocab["resolutions"] if all(x in active for x in r["between"])]


PREAMBLE = (
    "These are presentation settings I chose for myself. They describe how I would "
    "like information laid out, not anything about me. Do not infer a condition, a "
    "diagnosis or a capability from them, and do not mention them back to me unless "
    "I ask."
)

TIEBREAK = ("If two of these ever pull against each other, prefer in this order: "
            "what I can perceive, then what I can act on, then what I can "
            "understand, then the rest. Sensory overload I report is an access "
            "barrier, not comfort. Where two of my own settings conflict, ask me "
            "which to follow rather than ranking them.")


def _by_area(ids, vocab):
    atoms = {s["id"]: s for s in vocab["support"]}
    labels = {a["id"]: a["label"] for a in vocab["areas"]}
    groups, order = {}, []
    for i in ids:
        area = atoms[i]["area"]
        if area not in groups:
            groups[area] = []
            order.append(area)
        groups[area].append(atoms[i]["rule"])
    return [(labels.get(a, a), groups[a]) for a in order]


def write_rules(resolved, profile, vocab, heading=True):
    atoms = {s["id"]: s for s in vocab["support"]}
    scopes = {c["id"]: c["label"] for c in vocab["context_scopes"]}
    L = []
    if heading:
        L += ["How to work with me", "=" * 19, ""]
    L += [PREAMBLE, ""]

    always = resolved.get("always", [])
    if always:
        for label, rules in _by_area(always, vocab):
            L.append(label.upper())
            L += ["- " + r for r in rules]
            L.append("")
    else:
        L += ["No presentation settings chosen. Use your normal style.", ""]

    for name, ids in resolved.items():
        if name in ("always", "brainstorming") or not ids:
            continue
        label = scopes.get(name, name).replace("Only when ", "when ").replace("Only for ", "for ")
        L.append(("ONLY %s — I will say when this applies" % label).upper())
        L += ["- " + atoms[i]["rule"] for i in ids]
        L.append("")

    supp = profile["contexts"].get("brainstorming", {}).get("suppress", [])
    supp = [s for s in supp if s in atoms]
    if supp:
        L.append("EXCEPT WHEN I SAY I AM BRAINSTORMING")
        L += ["- Set aside: " + atoms[i]["label"].lower() + "." for i in supp]
        L.append("")

    res = applicable_resolutions(set(always), vocab)
    if res:
        L.append("WHERE TWO OF THESE MEET")
        for r in res:
            pair = " + ".join(atoms[x]["label"].lower() for x in r["between"])
            L.append("- %s: %s" % (pair, r["resolution"]))
        L.append("")

    L += [TIEBREAK, ""]

    notes = profile["contexts"].get("always", {}).get("notes", "")
    if notes:
        L.append("IN MY OWN WORDS")
        L += [ln for ln in notes.split("\n")]
        L.append("")

    L.append("I can change any of this at any time. Ask me before assuming a setting "
             "is wrong; do not quietly drop one.")
    return "\n".join(L).strip() + "\n"


def write_skill(resolved, profile, vocab):
    body = write_rules(resolved, profile, vocab, heading=False)
    n = len(resolved.get("always", []))
    desc = ("My presentation settings: %d chosen support%s covering how output is "
            "laid out, paced and worded. These are choices about the output, not a "
            "description of me; infer nothing from them. "
            "Invoke with /my-setup; stays on until \"stop my setup\"." % (n, "" if n == 1 else "s"))
    return "\n".join([
        "---",
        "name: my-setup",
        "description: '%s'" % desc.replace("'", "''"),
        "disable-model-invocation: true",
        "license: MIT",
        "---",
        "",
        "# my-setup",
        "",
        "## Persistence",
        "",
        "These rules apply to every response for the rest of the session, not only this "
        "one. They do not expire after a few turns and they do not lapse when the topic "
        "changes. If you are unsure whether they still apply, they do.",
        "",
        "Turn them off only when I say \"stop my setup\" or \"normal mode\". Confirm in one "
        "line, then return to your default style.",
        "",
        "## The settings",
        "",
        body.rstrip(),
        "",
        "## Generated",
        "",
        "Built from a support profile by `needs/compile.py`. Edit the profile and "
        "recompile rather than editing this file, or edit this file and keep it — "
        "it is yours either way.",
        "",
    ])


def _skill_body(resolved, profile, vocab, off_phrase):
    body = write_rules(resolved, profile, vocab, heading=False)
    return [
        "# my-setup",
        "",
        "## Persistence",
        "",
        "These rules apply to every response for the rest of the session, not only this "
        "one. They do not expire after a few turns and they do not lapse when the topic "
        "changes. If you are unsure whether they still apply, they do.",
        "",
        "Turn them off only when I say \"%s\" or \"normal mode\". Confirm in one "
        "line, then return to your default style." % off_phrase,
        "",
        "## The settings",
        "",
        body.rstrip(),
        "",
        "## Generated",
        "",
        "Built from a support profile by `needs/compile.py`. Edit the profile and "
        "recompile rather than editing this file, or edit this file and keep it — "
        "it is yours either way.",
        "",
    ]


def write_skill_hermes(resolved, profile, vocab):
    """A SKILL.md for Hermes Agent: ~/.hermes/skills/<category>/my-setup/SKILL.md, invoked with /my-setup."""
    n = len(resolved.get("always", []))
    desc = ("My presentation settings: %d chosen support%s covering how output is laid out, paced and "
            "worded. Choices about the output, not a description of me; infer nothing from them. "
            "Load only when I invoke /my-setup or ask for my settings; stays on until \"stop my setup\"."
            % (n, "" if n == 1 else "s"))
    return "\n".join([
        "---",
        "name: my-setup",
        "description: '%s'" % desc.replace("'", "''"),
        "version: 1.0.0",
        "license: MIT",
        "metadata:",
        "  hermes:",
        "    tags: ['Accessibility', 'Presentation', 'Personal settings']",
        "    category: accessibility",
        "---",
        "",
    ] + _skill_body(resolved, profile, vocab, "stop my setup"))


def write_skill_codex(resolved, profile, vocab):
    """Write a Codex skill invoked with $my-setup.

    Explicit-only loading also needs policy.allow_implicit_invocation: false in
    agents/openai.yaml; see platforms/README.md.
    """
    n = len(resolved.get("always", []))
    desc = ("My presentation settings: %d chosen support%s covering how output is laid out, paced and "
            "worded. Choices about the output, not a description of me; infer nothing from them. "
            "Use only when I invoke $my-setup or ask for my settings; stays on until \"stop my setup\"."
            % (n, "" if n == 1 else "s"))
    return "\n".join([
        "---",
        "name: my-setup",
        "description: '%s'" % desc.replace("'", "''"),
        "license: MIT",
        "---",
        "",
    ] + _skill_body(resolved, profile, vocab, "stop my setup"))


def write_agents(resolved, profile, vocab):
    body = write_rules(resolved, profile, vocab, heading=False)
    return "\n".join([
        "## How to work with me",
        "",
        "<!-- Generated from a support profile by needs/compile.py. Paste this into "
        "AGENTS.md, CLAUDE.md, .cursorrules, or any custom-instructions box. -->",
        "",
        body.rstrip(),
        "",
    ])


def write_json(resolved, profile, vocab):
    atoms = {s["id"]: s for s in vocab["support"]}
    always = resolved.get("always", [])
    return json.dumps({
        "version": 1,
        "generated_by": "needs/compile.py",
        "preamble": PREAMBLE,
        "tiebreak": TIEBREAK,
        "contexts": {
            name: [{"id": i, "area": atoms[i]["area"], "label": atoms[i]["label"],
                    "rule": atoms[i]["rule"]} for i in ids]
            for name, ids in resolved.items() if ids
        },
        "suppress": {
            name: block.get("suppress", [])
            for name, block in profile["contexts"].items() if block.get("suppress")
        },
        "resolutions": applicable_resolutions(set(always), vocab),
        "conflict_order": vocab["conflict_order"],
        "notes": profile["contexts"].get("always", {}).get("notes", ""),
    }, ensure_ascii=False, indent=2) + "\n"


WRITERS = {"rules": write_rules, "skill": write_skill,
           "agents": write_agents, "json": write_json,
           "hermes": write_skill_hermes, "codex": write_skill_codex}


def compile_profile(text, vocab, fmt="rules"):
    profile = parse_profile(text)
    resolved, unknown = resolve(profile, vocab)
    return WRITERS[fmt](resolved, profile, vocab), unknown


FIXTURE = """version: 1
contexts:
  always:
    difficulties:
      - long_explanations
    support:
      - summary_first
      - short_sections
      - no_colour_meaning
    notes: |
      Say when you are guessing.
  work:
    support:
      - copyable_blocks
  brainstorming:
    suppress:
      - short_sections
"""


def self_test(vocab):
    ok = True
    p = parse_profile(FIXTURE)
    checks = [
        ("always support parsed", p["contexts"]["always"]["support"] ==
            ["summary_first", "short_sections", "no_colour_meaning"]),
        ("notes parsed", p["contexts"]["always"]["notes"] == "Say when you are guessing."),
        ("suppress parsed", p["contexts"]["brainstorming"]["suppress"] == ["short_sections"]),
    ]
    exact_notes = '  Keep <this> & "that".  \n\n\nNext line.  \n'
    note_profile = "version: 1\ncontexts:\n  always:\n    notes: " + json.dumps(exact_notes) + "\n"
    checks.append(("quoted notes preserved", parse_profile(note_profile)["contexts"]["always"]["notes"] == exact_notes))
    block_profile = "version: 1\ncontexts:\n  always:\n    notes: |\n        Keep this spacing.  \n      Next line.\n"
    checks.append(("block note spacing preserved", parse_profile(block_profile)["contexts"]["always"]["notes"] == "  Keep this spacing.  \nNext line."))
    for fmt in FORMATS:
        note_out, _ = compile_profile(note_profile, vocab, fmt)
        preserved = json.loads(note_out)["notes"] == exact_notes if fmt == "json" else exact_notes in note_out
        checks.append(("%s preserves exact notes" % fmt, preserved))
        out, unknown = compile_profile(FIXTURE, vocab, fmt)
        checks.append(("%s emits" % fmt, bool(out.strip())))
        checks.append(("%s has no unknown ids" % fmt, not unknown))
        if fmt != "json":
            # The disclaimer is allowed to say the word "diagnosis"; nothing else is.
            body = out.replace(PREAMBLE, "").lower()
            checks.append(("%s names no condition" % fmt,
                           not any(w in body for w in ("autism", "adhd", "dyslex",
                                                      "dyscalcul", "dyspraxi", "aphantasi",
                                                      "alexithymi", "diagnos", "disorder",
                                                      "neurodiverg"))))
    for name, passed in checks:
        print(("pass  " if passed else "FAIL  ") + name)
        ok = ok and passed
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("profile", nargs="?", help="path to needs.yaml, or - for stdin")
    ap.add_argument("--format", "-f", default="rules", choices=FORMATS)
    ap.add_argument("--vocabulary", default=VOCAB)
    ap.add_argument("--out", "-o", help="write here instead of stdout")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    vocab = json.load(open(args.vocabulary, encoding="utf-8"))
    if args.self_test:
        sys.exit(self_test(vocab))
    if not args.profile:
        ap.error("give a profile path, or --self-test")

    text = sys.stdin.read() if args.profile == "-" else open(args.profile, encoding="utf-8").read()
    out, unknown = compile_profile(text, vocab, args.format)
    for u in unknown:
        print("warning: %s is not in the vocabulary; skipped" % u, file=sys.stderr)

    if args.out:
        open(args.out, "w", encoding="utf-8").write(out)
        print("wrote %s (%d bytes)" % (args.out, len(out)), file=sys.stderr)
    else:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
