#!/usr/bin/env python3
"""Check the picker against its template and projected vocabulary; exit 1 on drift."""
import json, os, re, sys

import build

def extract(html):
    m = re.search(r'<script id="vocab" type="application/json">(.*?)</script>', html, re.S)
    if not m:
        sys.exit("no <script id=\"vocab\"> block in needs-picker.html")
    return json.loads(m.group(1).replace("<\\/", "</"))


def main():
    vocab = json.load(open(build.SOURCE, encoding="utf-8"))
    expected = build.project(vocab)
    html = open(build.OUTPUT, encoding="utf-8").read()
    embedded = extract(html)

    failures = []

    if embedded != expected:
        for key in sorted(set(expected) | set(embedded)):
            if key not in embedded:
                failures.append("embedded vocabulary is missing '%s'" % key)
            elif key not in expected:
                failures.append("embedded vocabulary has extra key '%s'" % key)
            elif embedded[key] != expected[key]:
                failures.append("'%s' differs from the projection of the source" % key)

    for key in ("resolutions", "conflict_order"):
        if key not in embedded:
            failures.append("the page cannot compile: '%s' is missing" % key)

    # No field the projection excludes may appear in the page's vocabulary.
    for row in embedded.get("support", []):
        extra = set(row) - (set(build.SUPPORT_FIELDS) | {"defers", "defers_note"})
        if extra:
            failures.append("support %s carries unprojected fields: %s"
                            % (row.get("id"), ", ".join(sorted(extra))))
    for row in embedded.get("difficulties", []):
        extra = set(row) - set(build.DIFF_FIELDS)
        if extra:
            failures.append("difficulty %s carries unprojected fields: %s"
                            % (row.get("id"), ", ".join(sorted(extra))))

    template = open(build.TEMPLATE, encoding="utf-8").read()
    if build.render(template, expected) != html:
        failures.append("needs-picker.html is not the current build of "
                        "picker.template.html + needs-vocabulary.json")

    if not failures:
        print("parity: needs-picker.html matches needs-vocabulary.json")
        print("  areas %d · difficulties %d · supports %d · scopes %d · presets %d"
              % (len(expected["areas"]), len(expected["difficulties"]),
                 len(expected["support"]), len(expected["contexts"]),
                 len(expected["presets"])))
        pairs = sum(len(d["compare_pairs"]) for d in expected["difficulties"])
        defers = sum(1 for s in expected["support"] if s["defers"])
        print("  comparison pairs %d · atoms that defer %d" % (pairs, defers))
        return 0

    for f in failures:
        print("FAIL: " + f, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
