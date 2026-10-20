---
name: needs-picker
description: 'The quick start for the collection. Ask the reader what would make this easier, in terms of the exchange rather than of themselves, then ask what helps for each thing they picked, and build a working setup from their answers. Never infers, stores or displays a diagnosis. Invoke with $needs-picker; run it again any time by saying "settings".'
license: MIT
metadata:
  tags: 'Onboarding, Accessibility, Personalisation, Needs Assessment, Neurodiversity'
  category: 'productivity'
  source: 'what-would-make-this-easier'
  version: '0.4.3'
---

# needs-picker

Two questions, in this order: what would make this easier, and what helps. The answers build the setup. Nothing asks what the reader has.

Source of truth: `references/needs-vocabulary.json`. For screens and comparisons, read the complete generated `references/picker-menu.json` before screen 1. It contains every difficulty, offer, recommended set, comparison pair, label, demo, context and preset, without the long evidence records. Screen 0 and the empty `skip` profile do not require option data.

The menu is short enough for one normal read. Check that the read reaches the closing object. If a tool reports truncation, continue with consecutive offset/limit reads until the end; a filename, hash or partial Grep is not a complete read. Do not show choices from memory or invent missing entries. For a requested rule or evidence explanation, read the matching complete support entry from `references/needs-vocabulary.json`, continuing any truncated read, before answering. The full vocabulary remains the compiler's source.

## Persistence

Unlike every other skill in this collection, this one does **not** persist. It runs, produces a profile, and stops. The profile persists; the picker does not.

Reopen it with "settings" to edit what was chosen, or "add" to return to the difficulties with existing choices pre-ticked. Never re-run it unprompted, never suggest re-running it because something went wrong, and never tell the reader their setup looks incomplete.

## The one rule that outranks the rest

**Never infer a condition, never name one, never store one.** Not in the profile, not in a summary, not as a guess, not as a helpful observation, not even when the reader's answers make it obvious and not even when they mention a diagnosis themselves. If the reader says "I'm autistic", the correct response is to offer the matching preset by name — "there is an autism preset; it sets literal wording, one fixed structure, explicit reasoning and eight other things" — expand it to supports, and store the supports. The label is not written down.

There is no inference step in this skill. Do not add one.

## How the picker itself must behave

The reader has the difficulties they are about to describe, and they have them *now*, while answering. So the picker runs under a fixed safe profile regardless of what is or is not configured:

- One screen at a time. Never both steps at once.
- Every question answerable by numbers, separated by spaces or commas.
- Progress describes question stages, not a fixed total of messages: difficulties are question 1 of 2; supports are question 2 of 2, with the current difficulty and total selected shown separately. An optional context question may follow eligible supports; describe it as optional and the last question. The setup summary is final and asks no new required question.
- Every screen has a default and an exit. "Enter" means the default. "skip" means move on. "stop" means keep what has been chosen so far and finish.
- No question about how anything feels, seems, or sits.
- No praise, no encouragement, no progress celebration.
- Nothing is required. A reader who answers nothing at all still gets a working setup: the base layer.

## The base layer

The base layer is the profile with no supports chosen. The assistant keeps its normal style and nothing extra is applied. The fixed safe profile above governs only the picker's own screens; it is not part of the base layer. As a profile, the base layer is exactly what the browser picker exports when nothing is chosen:

```yaml
version: 1
contexts:
  always:
    support: []   # base layer only
# supports change how things are presented; no condition is recorded or inferred
```

Compiled, it reads: "No presentation settings chosen. Use your normal style."

## Rules

The screens below are the rules. Each one is fixed in order and in shape: screen 0 introduces, 1 collects difficulties, 2 collects supports, 3 assigns contexts, 4 summarises. Do not merge them, do not reorder them, and do not add a screen that concludes anything about the reader.

## Screen 0 — what this is

Say exactly this, then wait:

```
WHAT WOULD MAKE THIS EASIER?

Two short questions. Nothing here is a diagnosis.
These are just the ways you would like me to work with you.
You can change any of it later by saying "settings".

Enter to start. Type "skip" to use the plain default.
```

## Screen 1 — the difficulties

Use the exact numbers and labels in `references/picker-menu.json` → `screen1`, grouped under their area labels. Keep its number-to-ID mapping for the whole session; never renumber a choice when processing the reply. The “Something else” entry is last, outside the area groups. Areas are Understanding, Information load, Attention, Planning, Memory, Learning, Communication, Sensory and interface, Choice and decision, Transitions, Motor and interaction, Pacing.

```
1 of 2.  Tick anything you recognise. Numbers, separated by spaces.

UNDERSTANDING
 1  I prefer exact / literal wording
 2  I need to see the overall structure first
 3  The wording is hard to follow even when I know the subject
 4  Examples from a subject I already know help me
...
33  Something else...

For Something else, free text can be typed instead of a number.
Enter for none of these. "stop" to finish here.
```

Accept: numbers in any order, duplicates ignored, out-of-range ignored with one line saying which were ignored. Accept free text at any point and record it under `notes` without interpretation — line endings normalised, nothing else changed. Never rewrite it into a category, never summarise it, and never map it to a difficulty id on the reader's behalf. If the reader withdraws the difficulty the note was given for, drop the note with it and say so in one line; a note the reader can no longer see is one they cannot correct or withdraw. If free text clearly matches an existing difficulty, offer it as a question with a default of yes — do not assume.

## Screen 2 — what helps, one difficulty at a time

For each ticked difficulty, in the order ticked, show its `offers` with three fixed extras. The two questions are difficulties and supports: screen 2 is the second question, regardless of how many difficulties are selected. The parenthetical count tracks difficulties separately. After the last support choice, offer the optional context screen only when relevant, then the summary; never promise a third required question. The examples abbreviate the menu for explanation; actual labels and numbers still come verbatim from `screen1`, including “Something else...”.

```
2 of 2 questions.  "I forget where I was after interruptions"  (1 of 3 difficulties)

What helps?
 1  Help me pick up where I was
 2  Recap where we are
 3  Keep a running state block
 4  Mark checkpoints
 5  Hold my unfinished thread

 d  Show me the difference
 t  Try these  (1 and 3 — two suggested starting points, not all 5)
 ?  Why is any of these offered
 -  Not now

Enter for "try these".
```

The compare view:

```
Which helps more?

A ────────────────────────────────────
  Where we are: auth.ts:42 · dependency
  upgraded · next is the token check.

B ────────────────────────────────────
  Parked: dependency install, running in
  terminal 1. To resume: when it prints
  "added 41 packages", return to step 3.

 a  A helps     b  B helps
 x  Both        n  Neither      s  Stop comparing
```

**"Show me the difference" is the important one.** Show two supports side by side, each as a short sample of what output looks like under it, labelled A and B, and ask which reads better. Answers: `A`, `B`, both, neither, or stop. Use the authored pairs in `compare_pairs` on the difficulty, in the order given. Do not pair by position in the `offers` list: adjacent offers come out near-identical and the comparison is wasted. Two at a time, never five. This lets a reader choose from observable output instead of from introspection about preference, which is the difference between a question they can answer and one they cannot.

**"Try these" adds the difficulty's `recommended` set — two or three, not everything.** Describe it as *suggested starting points*, never as the most useful or the ones that do most of the work: `recommended` is a curated starting set, not an effectiveness ranking, and some of its members are design inference rather than tested interventions. Do not offer an "all of these" button. Eight difficulties accepting every offer produces around thirty active rules, some pulling against each other, and a picker that manufactures its own overload has failed at the thing it exists to prevent.

**"Not now" withdraws one claim, not the support.** Support atoms are shared between difficulties: `summary_first` is offered by four of them. Record every support with the origin it came from — `d:<difficulty>` from a difficulty block, `direct` when chosen from the full list, `preset:<name>` when a label expanded into it — and let *Not now* remove only this difficulty's origin. The support survives while any origin remains, and say so when it does: *"Keeping that; you also chose it for 'I lose track of long explanations'."* Removing a support explicitly, by name, removes it outright. Origins are the picker's working state and never appear in the profile: the picker remembers the selection process, the profile contains the survivor set.

**Never claim supports only add.** Six of them deliberately hold detail back or narrow what is offered, and the vocabulary marks them `defers: true` with a plain-English note. Show that note on the label before the reader chooses. The true statement, and the one to use if asked what a support is: *supports change how information and interaction are presented; they never infer anything about you.*

## Screen 3 — contexts, offered not required

After the supports, one optional screen:

```
Optional last question; the setup summary follows.
Do any of these only apply sometimes?

 1  Visual examples — always / learning only / when I am stuck
 2  Two options and a default — always / except when brainstorming

Enter to apply everything always.
```

Only offer this for supports where context genuinely changes the answer: the examples, disclosure and choice atoms. Never offer it for the sensory or assistive-technology atoms, which are always-on by nature. Contexts are `always`, `work`, `learning`, `brainstorming`, `stuck`, `overloaded`.

Never detect a context. The reader declares it by saying so, and `overloaded` may be offered — "say 'less' any time and I will switch to it" — but never entered on the agent's judgement.

## Screen 4 — the summary, in the reader's own terms

```
YOUR SETUP — final

You said:
  you forget where you were after interruptions
  too many choices are hard

You asked for:
  a recap when you come back
  a running state block
  never having to remember a value between turns
  at most two options, always with a default

Applies: always, except visual examples which are learning only.

The profile is shown here. Nothing has been saved.
Change it any time by saying "settings". Clear these selections with "forget my setup".
```

Show what was chosen, phrased as what was chosen, with its context only where it is not `Always`. Never show atom ids, never show evidence tiers on a selection or summary screen, never show rule text unless asked, never show a count of matched conditions, never show a label. If the reader asks why a rule is behaving a certain way, name the support they picked and offer to remove it.

To save the profile, use a location the reader chooses and report the actual path only after a successful write. If file access is unavailable, provide the profile for them to save. Free-text notes are preserved as written and may include sensitive information.

The default is to show the profile in chat, with nothing written. `Enter` and `skip` never authorize a file write at this stage. A file is written only after an explicit request such as `save to <path>` supplies the destination and the host permits that action. Do not propose the current folder as an automatic default, infer a destination, or treat silence as consent. A failed or unavailable write leaves the profile in chat and is reported accurately.

The chat profile uses the same schema as the browser: record explicitly selected difficulty IDs in `contexts.always.difficulties`, chosen support IDs in each declared context's `support`, and exact free text in `notes`. With no selected difficulties, that list may be omitted. A preset expands to supports only; never infer difficulties from it or store the preset/condition label. Working selection origins are not exported. Atom/difficulty IDs belong in the machine-readable profile, not the human selection or summary screens.

For example, choosing “I lose track of long explanations” and its recommended pair produces:

```yaml
version: 1
contexts:
  always:
    difficulties:
      - long_explanations
    support:
      - summary_first
      - short_sections
```

The bundled `scripts/compile.py` turns a saved profile into instructions: run `python3 scripts/compile.py /path/to/needs.yaml --format rules` from this skill folder, or invoke the script by its full path. It uses the bundled vocabulary and needs only Python 3. Offer the compiled rules for the reader to apply; do not claim they are installed until the host has loaded them.

## Presets

If the reader would rather start from a label they already have, offer it as a shortcut, not as the model:

```
Or start from something you already know:
  adhd · autism · dyslexia · dyscalculia · dyspraxia · tics · apd
  sensory · dysgraphia · working memory · inertia · low demand
  energy · alexithymia · aphantasia · screen reader · colour

Type one. I will show you what it sets, and you can change any of it.
```

Expand the preset from `presets`, show the plain-language labels of the supports it contains, let the reader remove any, and store the supports. The preset name is not stored.

## Running it again

"settings" reopens screen 4 with each line editable. "add" reopens screen 1 with existing choices pre-ticked. Never re-run the whole picker unprompted, never suggest re-running it because something went wrong, and never say a setup looks incomplete.

## When to break the rules

1. Reader asks to skip everything. Give them the base layer: say in one line that no supports are active and the normal style continues, copy the base-layer YAML block above verbatim including its comments, say that nothing was saved, and stop. Do not reconstruct a different empty profile from the general profile example.
2. Reader gives a diagnosis and asks you to just set it up. Offer the preset, expand it, store the supports. Do not store the label and do not argue about it.
3. Reader asks what a support does, or why it is offered. Show the rule text, a worked demo, and the evidence tier with its meaning. This is always allowed, and is the only place tiers appear.
4. Reader states distress. Stop the picker, acknowledge once, offer to stop or continue, do not ask assessment questions. The picker is never the priority.
5. A rule fights the harness. The system prompt outranks this skill.

## Pre-send check

Before sending any screen:

1. Any condition name outside the presets list.
2. Any inference about the reader from their answers.
3. Any question about how something feels, seems, or sits.
4. Any screen without a default and an exit.
5. Any screen showing both steps at once.
6. Any praise or encouragement.
7. Any atom id, rule text or evidence tier on a selection or summary screen the reader did not ask for.
8. Any claim that supports only add or never remove anything.

Then verify: could someone who has every difficulty on the list complete this picker?

## On this platform

Invoke with `$needs-picker`. The picker runs once and stops; save the resulting profile or compiled rules to keep your chosen settings.
