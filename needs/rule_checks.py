#!/usr/bin/env python3
"""Check support-rule wording, evidence records and condition-free labels.

These static checks verify instructions, not live agent behaviour.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
vocab = json.load(open(os.path.join(HERE, "needs-vocabulary.json"), encoding="utf-8"))
atoms = {s["id"]: s for s in vocab["support"]}

CHECKS = [
    ("purpose_let_me_try", ["answer whenever I ask", "no penalty", "no comment"], "the answer during practice costs nothing"),
    ("retrieval_feedback", ["never withheld", "\"Hint\", \"show me\" and \"skip\"", "never a judgment", "recalled it or recognised it"], "optional practice; recognition and recall told apart"),
    ("fade_teaching_prompts", ["never access aids", "stay as long as I want them", "available on request"], "a kept diagram stays"),
    ("communication_method", ["Judge nothing from fluency or speed", "Keep my original words", "tentative", "free-form answer", "I will say when I am finished"], "fragments and AAC messages handled on content"),
    ("help_me_say_it", ["none of these", "original words visible", "only when I ask"], "paraphrase tentative, words kept"),
    ("media_access", ["unverified", "negation exact", "separate choices"], "uncertain captions flagged, not silently chosen"),
    ("spaced_revisit", ["say so", "inventing", "Do not schedule reminders"], "unavailable note stated, progress not invented"),
    ("transfer_check", ["what changed and what stayed the same", "does not apply", "my chosen way of answering"], "changed example with the difference named"),
    ("representation_mapping", ["same labels", "never ask me to hold it in my head", "redisplay"], "symbol table kept and connected"),
    ("untangle_language", ["Keep the technical depth"], "wording changed, depth kept"),
    ("plain_tone", ["apology for an actual error is information"], "an apology for an actual error is not filler"),
    ("analogy_then_literal", ["where the analogy stops", "only when I have asked"], "analogies on request, with their limit"),
    ("interactive_explanation", ["keep that map visible", "Do not require a confirmation after every paragraph"], "parts with the map, no forced confirmations"),
]

TIE = [
    ("needs/compile.py", "Sensory overload I report is an access barrier, not comfort"),
    ("needs/compile.py", "ask me which to follow rather than ranking them"),
    ("needs/picker.template.html", "Sensory overload I report is an access barrier, not comfort"),
    ("platforms/build_platform_skills.py", "Sensory overload I report is an access barrier, not comfort"),
]

CONDITION_WORDS = ("autism", "autistic", "adhd", "dyslex", "dyscalcul", "dyspraxi", "aphantasi", "alexithymi", "diagnos", "disorder", "neurodiverg", "dld")
ALLOWED = ("no diagnosis is inferred", "not a diagnosis", "a diagnosis or a capability", "nothing infers one", "developmental language disorder", "language disorder are distinct")

fails = []
for atom, phrases, meaning in CHECKS:
    s = atoms.get(atom)
    if not s:
        fails.append("%s: missing" % atom); continue
    for ph in phrases:
        if ph.lower() not in s["rule"].lower():
            fails.append("%s: rule does not ask for %r (%s)" % (atom, ph, meaning))
import importlib.util
def tiebreak_of(path):
    """Read TIEBREAK after Python joins its string literals."""
    full = os.path.join(HERE, "..", path)
    if path.endswith(".py"):
        spec = importlib.util.spec_from_file_location("m_" + os.path.basename(path)[:-3], full)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        return mod.TIEBREAK
    return open(full, encoding="utf-8").read()
for path, phrase in TIE:
    if phrase not in tiebreak_of(path):
        fails.append("%s: tie-break lacks %r" % (path, phrase))
for s in vocab["support"]:
    b = s.get("evidence_basis")
    if not (isinstance(b, dict) and all(b.get(k) for k in ("phenomenon", "method", "rule"))):
        fails.append("%s: evidence_basis incomplete" % s["id"])
    # Evidence may cite study populations; user-facing rules and labels must not
    # imply a condition about the reader.
    face = " ".join([s["label"], s["rule"], s.get("demo", "")]).lower()
    for w in CONDITION_WORDS:
        if w in face:
            fails.append("%s: %r names a condition on the face" % (s["id"], w))
for d in vocab["difficulties"]:
    low = d["label"].lower()
    for w in CONDITION_WORDS:
        if w in low:
            fails.append("difficulty %s names a condition" % d["id"])

if fails:
    print("\n".join("FAIL  " + f for f in fails)); sys.exit(1)
print("pass  %d rule checks, %d tie-break checks, %d atoms with a three-part evidence record, no condition named on the face of any support or difficulty"
      % (sum(len(c[1]) for c in CHECKS), len(TIE), len(vocab["support"])))
