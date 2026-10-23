#!/usr/bin/env python3
"""Build the picker from the vocabulary.

Generate the HTML, browser projection and standalone skill resources.
Use --check to verify that generated files are current.
"""
import hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SOURCE   = os.path.join(HERE, "needs-vocabulary.json")
TEMPLATE = os.path.join(HERE, "picker.template.html")
EMBED    = os.path.join(HERE, "vocab.embed.json")
OUTPUT   = os.path.join(ROOT, "needs-picker.html")

PLACEHOLDER = "__VOCAB__"

# Per-record fields copied to the browser; project() also includes presets,
# resolutions and conflict_order for the in-page compiler.
AREA_FIELDS = ("id", "label", "description")
DIFF_FIELDS = ("id", "label", "area", "offers", "recommended", "compare_pairs")
SUPPORT_FIELDS = ("id", "area", "label", "rule", "evidence", "evidence_basis", "demo")
SCOPE_FIELDS = ("id", "label", "yaml")


def project(vocab):
    """Return exactly the structure the picker's JavaScript reads."""
    def pick(obj, fields, defaults=None):
        out = {}
        for f in fields:
            if f in obj:
                out[f] = obj[f]
            elif defaults and f in defaults:
                out[f] = defaults[f]
        return out

    support = []
    for s in vocab["support"]:
        row = pick(s, SUPPORT_FIELDS)
        row["defers"] = bool(s.get("defers", False))
        row["defers_note"] = s.get("defers_note", "")
        support.append(row)

    return {
        "areas":        [pick(a, AREA_FIELDS) for a in vocab["areas"]],
        "difficulties": [pick(d, DIFF_FIELDS, {"recommended": [], "compare_pairs": []})
                         for d in vocab["difficulties"]],
        "support":      support,
        # The picker's context selector offers scopes, not raw contexts:
        # `always_not_brainstorming` is a scope that compiles to two contexts.
        "contexts":     [pick(c, SCOPE_FIELDS) for c in vocab["context_scopes"]],
        "presets":      vocab["presets"],
        "resolutions":  vocab["resolutions"],
        "conflict_order": vocab["conflict_order"],
    }


def validate(vocab, proj):
    """Validate references and evidence records before rendering."""
    errors = []
    atoms = {s["id"] for s in proj["support"]}
    areas = {a["id"] for a in proj["areas"]}
    for d in proj["difficulties"]:
        if d["area"] not in areas:
            errors.append("difficulty %s: unknown area %s" % (d["id"], d["area"]))
        for o in d["offers"]:
            if o not in atoms:
                errors.append("difficulty %s offers unknown atom %s" % (d["id"], o))
        for r in d["recommended"]:
            if r not in d["offers"]:
                errors.append("difficulty %s recommends %s, which it does not offer" % (d["id"], r))
        seen = []
        for pair in d["compare_pairs"]:
            if not 1 <= len(pair) <= 2:
                errors.append("difficulty %s: pair of %d atoms" % (d["id"], len(pair)))
            for a in pair:
                if a not in d["offers"]:
                    errors.append("difficulty %s pairs %s, which it does not offer" % (d["id"], a))
                seen.append(a)
        if sorted(seen) != sorted(d["offers"]):
            errors.append("difficulty %s: pairs cover %d of %d offers, or repeat one"
                          % (d["id"], len(set(seen)), len(d["offers"])))
    for s in proj["support"]:
        b = s.get("evidence_basis")
        if not (isinstance(b, dict) and all(isinstance(b.get(k), str) and b.get(k) for k in ("phenomenon", "method", "rule"))):
            errors.append("support %s: evidence_basis must record phenomenon, method and rule" % s["id"])
        if s["area"] not in areas:
            errors.append("support %s: unknown area %s" % (s["id"], s["area"]))
        if s["defers"] and not s["defers_note"]:
            errors.append("support %s defers but carries no note" % s["id"])
    for r in proj["resolutions"]:
        if len(r["between"]) != 2:
            errors.append("resolution %r does not name two atoms" % r["between"])
        for a in r["between"]:
            if a not in atoms:
                errors.append("resolution names unknown atom %s" % a)
    for name, expansion in proj["presets"].items():
        for a in expansion:
            if a not in atoms:
                errors.append("preset %s expands to unknown atom %s" % (name, a))
    reachable = {o for d in proj["difficulties"] for o in d["offers"]}
    reachable |= {a for e in proj["presets"].values() for a in e}
    # every atom is also reachable from the by-area tab, so this is advisory
    for a in sorted(atoms - reachable):
        print("note: %s is offered only under 'By area'" % a, file=sys.stderr)
    return errors


def render(template, proj):
    payload = json.dumps(proj, ensure_ascii=False, separators=(",", ":"))
    # A literal </script> inside a JSON island would close the block early.
    payload = payload.replace("</", "<\\/")
    return template.replace(PLACEHOLDER, payload)


def render_menu(vocab, source_text):
    """Compact complete menu data; detailed rules/evidence stay in the vocabulary."""
    ordered = [d for a in vocab["areas"] for d in vocab["difficulties"]
               if d["area"] == a["id"] and d["id"] != "other"]
    ordered += [d for d in vocab["difficulties"] if d["id"] == "other"]
    data = {
        "source": "needs-vocabulary.json",
        "source_sha256": hashlib.sha256(source_text.encode("utf-8")).hexdigest(),
        "areas": [{k: a[k] for k in ("id", "label")} for a in vocab["areas"]],
        "screen1": [{"number": n, "id": d["id"], "area": d["area"], "label": d["label"]}
                    for n, d in enumerate(ordered, 1)],
        "difficulties": vocab["difficulties"],
        "support": [{k: s[k] for k in ("id", "area", "label", "demo", "defers", "defers_note") if k in s}
                    for s in vocab["support"]],
        "contexts": vocab["contexts"],
        "context_scopes": vocab["context_scopes"],
        "presets": vocab["presets"],
    }
    lines = []
    for key, value in data.items():
        prefix = " " + json.dumps(key) + ": "
        if isinstance(value, list):
            text = "[\n" + ",\n".join("  " + json.dumps(v, ensure_ascii=False, separators=(",", ":")) for v in value) + "\n ]"
        else:
            text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        lines.append(prefix + text)
    text = "{\n" + ",\n".join(lines) + "\n}\n"
    if len(text.encode("utf-8")) > 40000:
        raise ValueError("Picker menu exceeds its read budget; split it before adding more data")
    return text


def main():
    check = "--check" in sys.argv
    vocab = json.load(open(SOURCE, encoding="utf-8"))
    template = open(TEMPLATE, encoding="utf-8").read()
    if template.count(PLACEHOLDER) != 1:
        sys.exit("template must contain %s exactly once" % PLACEHOLDER)

    proj = project(vocab)
    errors = validate(vocab, proj)
    if errors:
        for e in errors:
            print("error: " + e, file=sys.stderr)
        sys.exit("%d validation errors; nothing written" % len(errors))

    html = render(template, proj)

    skill = os.path.join(ROOT, "skills", "needs-picker")
    outputs = {
        OUTPUT: html,
        os.path.join(ROOT, "docs", "index.html"): html,
        EMBED: json.dumps(proj, ensure_ascii=False, indent=1) + "\n",
        os.path.join(skill, "references", "needs-vocabulary.json"):
            open(SOURCE, encoding="utf-8").read(),
        os.path.join(skill, "references", "picker-menu.json"):
            render_menu(vocab, open(SOURCE, encoding="utf-8").read()),
        os.path.join(skill, "scripts", "compile.py"):
            open(os.path.join(HERE, "compile.py"), encoding="utf-8").read(),
    }
    if check:
        stale = [os.path.relpath(path, ROOT) for path, expected in outputs.items()
                 if not os.path.isfile(path) or open(path, encoding="utf-8").read() != expected]
        if stale:
            sys.exit("Generated files missing or stale: %s; run: python3 needs/build.py" % ", ".join(stale))
        print("picker HTML, embedded vocabulary and standalone skill resources are current")
        return

    for path, content in outputs.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write(content)
    print("built %s (%d bytes) from %d areas, %d difficulties, %d supports, %d scopes, %d presets"
          % (os.path.basename(OUTPUT), len(html), len(proj["areas"]),
             len(proj["difficulties"]), len(proj["support"]),
             len(proj["contexts"]), len(proj["presets"])))


if __name__ == "__main__":
    main()
