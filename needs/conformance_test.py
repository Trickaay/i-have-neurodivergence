#!/usr/bin/env python3
"""Compare browser exports with the Python compiler.

Run with Playwright and Chromium installed. CHROMIUM_PATH can select a browser.
Missing Playwright reports a skip; browser launch failures fail the test.
"""
import difflib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PAGE = os.path.join(ROOT, "needs-picker.html")

sys.path.insert(0, HERE)
import compile as C

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
    ("note spacing", {"diff": ["other"], "notes": '  Keep <this> & "that".  \nNext line.'}),
    ("note blank lines", {"diff": ["other"], "notes": "Line one.\n\n\nLine four.  \n"}),
    ("note Unicode separators", {"diff": ["other"], "notes": "Keep \u007f\u0085\u009f\u2028\u2029 exactly."}),
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


def check_export_contract(got, fixture):
    profile = C.parse_profile(got["yaml"])
    selected = profile["contexts"].get("always", {}).get("difficulties", [])
    assert selected == fixture.get("diff", []), "YAML profile lost difficulty selections"
    compiled = json.loads(got["json"])
    assert "difficulties" not in compiled and all(
        isinstance(supports, list) and all(
            isinstance(s, dict) and "id" in s and "rule" in s and "difficulties" not in s
            for s in supports)
        for supports in compiled["contexts"].values()
    ), "JSON must contain compiled supports, not profile difficulty fields"
    return 2


def check_ui(page):
    page.reload()
    page.locator("#d-long_explanations").check()
    page.get_by_role("button", name="Try these", exact=True).click()
    page.locator("#d-long_explanations").uncheck()
    assert page.locator("#count").text_content() == "nothing chosen · plain default"

    page.get_by_role("tab", name="By area", exact=True).click()
    page.locator("#s-a-summary_first").check()
    page.get_by_role("tab", name="What’s hard", exact=True).click()
    page.locator("#d-long_explanations").check()
    page.get_by_role("button", name="Try these", exact=True).click()
    page.locator("#d-long_explanations").uncheck()
    page.get_by_role("tab", name="Copy for your agent", exact=True).click()
    page.locator("#fmt").select_option("json")
    exported = json.loads(page.locator("#yaml").text_content())
    assert [s["id"] for s in exported["contexts"]["always"]] == ["summary_first"]

    page.locator("#d-other").check()
    notes = '  Keep <this> & "that".  \n\n\nNext line.  \n'
    page.locator("#notes").fill(notes)
    assert json.loads(page.locator("#yaml").text_content())["notes"] == notes
    page.locator("#d-other").uncheck()
    assert json.loads(page.locator("#yaml").text_content())["notes"] == ""

    # Rebuilt controls keep keyboard focus (support toggle and "Try these").
    page.get_by_role("tab", name="What’s hard", exact=True).click()
    page.locator("#d-long_explanations").check()
    box = page.locator("#helps input[data-sup]").first
    box_id = box.get_attribute("id")
    box.focus()
    page.keyboard.press("Space")
    assert page.evaluate("()=>document.activeElement.id") == box_id
    page.locator("#try-long_explanations").focus()
    page.keyboard.press("Enter")
    assert page.evaluate("()=>document.activeElement.id") == "try-long_explanations"

    page.get_by_role("tab", name="From a label", exact=True).click()
    page.locator("#pane-p button").first.focus()
    page.keyboard.press("Enter")
    assert page.locator("#tab-a").get_attribute("aria-selected") == "true"
    assert page.evaluate("()=>document.activeElement.id") == "tab-a"
    return 7


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
    contract_checked = 0

    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()
        page = browser.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto("file://" + PAGE)
        page.wait_for_timeout(400)

        for name, fixture in FIXTURES:
            got = page.evaluate("(" + APPLY + ")", fixture)
            contract_checked += check_export_contract(got, fixture)
            expected_notes = fixture.get("notes", "").replace("\r\n", "\n").replace("\r", "\n")
            if json.loads(got["json"])["notes"] != expected_notes:
                failures += 1
                print("FAIL  %s / notes changed" % name)
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
        ui_checked = check_ui(page)
        browser.close()

    if errors:
        print("FAIL  the page raised: %s" % "; ".join(errors))
        failures += len(errors)
    if failures:
        print("\n%d of %d comparisons differ. The two compilers have drifted." % (failures, checked))
        return 1
    print("conformance: %d comparisons, the page and compile.py agree exactly" % checked)
    print("  %d fixtures x 4 formats" % len(FIXTURES))
    print("  %d UI regression checks" % ui_checked)
    print("  %d profile/compiled-export contract checks" % contract_checked)
    return 0


if __name__ == "__main__":
    sys.exit(main())
