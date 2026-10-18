#!/usr/bin/env python3
"""The picker compiles in JavaScript; needs/compile.py compiles in Python.
Two implementations of one spec drift unless something checks. This does.

For each fixture selection it drives the real page in a headless browser, takes
the YAML the page emits, compiles that YAML with compile.py, and compares the
result against what the page produced for the same format. Any difference at all
is a failure, printed as a unified diff.

    python3 needs/conformance_test.py

Needs playwright and a chromium. Skips with exit 0 and a clear message when
neither is available, so it never blocks a machine that only wants build.py.
"""
import difflib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PAGE = os.path.join(ROOT, "needs-picker.html")

sys.path.insert(0, HERE)
import compile as C

# Each fixture: difficulties to tick, supports to add, and contexts to scope them to.
FIXTURES = [
    ("empty", {}),
    ("one support", {"sup": ["summary_first"]}),
    ("across areas", {"sup": ["summary_first", "short_sections", "no_colour_meaning",
                              "copyable_blocks", "clock_not_feeling"]}),
    ("with contexts", {"sup": ["summary_first", "copyable_blocks", "one_goal"],
                       "ctx": {"copyable_blocks": "work", "one_goal": "stuck"}}),
    ("brainstorming suppression", {"sup": ["fewer_options", "next_step_only"],
                                   "ctx": {"fewer_options": "always_not_brainstorming"}}),
    ("resolution pair active", {"sup": ["summary_first", "explicit_intent",
                                        "fewer_options", "comparison_table"]}),
    ("difficulties and notes", {"diff": ["long_explanations", "other"],
                                "sup": ["summary_first"],
                                "notes": "Say when you are guessing.\nDo not apologise."}),
    ("a whole preset", {"preset": "i-use-a-screen-reader"}),
]

APPLY = """(f)=>{
  const P=window.__needsPicker, s=P.state;
  s.diff.clear(); s.sup.clear(); s.ctx={}; s.origin={}; s.notes="";
  (f.diff||[]).forEach(d=>s.diff.add(d));
  if(f.preset) (P.V.presets[f.preset]||[]).forEach(a=>P.addSup(a,"preset:"+f.preset));
  (f.sup||[]).forEach(a=>P.addSup(a,"direct"));
  Object.keys(f.ctx||{}).forEach(k=>{s.ctx[k]=f.ctx[k];});
  s.notes=f.notes||"";
  P.render();
  return {yaml:P.yaml(), rules:P.writeRules(), agents:P.writeAgents(),
          skill:P.writeSkill(), json:P.writeJson()};
}"""


def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("skip: playwright is not installed; the page and compile.py were not compared")
        return 0

    exe = None
    for cand in (os.environ.get("CHROMIUM_PATH", ""),):
        if cand and os.path.exists(cand):
            exe = cand
            break

    vocab = json.load(open(C.VOCAB, encoding="utf-8"))
    failures = 0
    checked = 0

    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()
        page = browser.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto("file://" + PAGE)
        page.wait_for_timeout(400)

        # The page keeps its compiler inside a closure; expose it once for testing.
        for name, fixture in FIXTURES:
            got = page.evaluate("(" + APPLY + ")", fixture)
            for fmt in ("rules", "agents", "skill", "json"):
                mine, _ = C.compile_profile(got["yaml"], vocab, fmt)
                checked += 1
                if mine != got[fmt]:
                    failures += 1
                    print("FAIL  %s / %s" % (name, fmt))
                    for line in list(difflib.unified_diff(
                            mine.splitlines(), got[fmt].splitlines(),
                            "compile.py", "picker", lineterm=""))[:24]:
                        print("      " + line)
        browser.close()

    if errors:
        print("FAIL  the page raised: %s" % "; ".join(errors))
        failures += len(errors)
    if failures:
        print("\n%d of %d comparisons differ. The two compilers have drifted." % (failures, checked))
        return 1
    print("conformance: %d comparisons, the page and compile.py agree exactly" % checked)
    print("  %d fixtures x 4 formats" % len(FIXTURES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
