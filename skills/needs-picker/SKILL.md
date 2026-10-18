---
name: needs-picker
description: 'The quick start for the collection. Ask the reader what would make this easier, in terms of the exchange rather than of themselves, then ask what helps for each thing they picked, and build a working setup from their answers. Never infers, stores or displays a diagnosis. Invoke with /needs-picker; run it again any time by saying "settings".'
disable-model-invocation: true
license: MIT
metadata:
  tags: "Onboarding, Accessibility, Personalisation, Needs Assessment, Neurodiversity"
  category: "productivity"
---

# needs-picker

Two questions, in this order: what would make this easier, and what helps. The answers build the setup. Nothing asks what the reader has.

Source of truth for every option below: `references/needs-vocabulary.json`. Read it before running this skill; do not work from memory of it.

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
- Every screen states how many screens remain.
- Every screen has a default and an exit. "Enter" means the default. "skip" means move on. "stop" means keep what has been chosen so far and finish.
- No question about how anything feels, seems, or sits.
- No praise, no encouragement, no progress celebration.
- Nothing is required. A reader who answers nothing at all still gets a working setup: the base layer.

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

List the difficulties from `references/needs-vocabulary.json`, grouped under their area labels, numbered continuously. Areas in this order: Understanding, Information load, Attention, Planning, Memory, Learning, Communication, Sensory and interface, Choice and decision, Transitions, Motor and interaction, Pacing.

```
1 of 2.  Tick anything you recognise. Numbers, separated by spaces.

UNDERSTANDING
 1  I prefer exact / literal wording
 2  I miss implied meaning or sarcasm
 3  I need to see the overall structure first
...
33  Something else — type it in your own words

Enter for none of these. "stop" to finish here.
```

Accept: numbers in any order, duplicates ignored, out-of-range ignored with one line saying which were ignored. Accept free text at any point and record it under `notes` without interpretation — line endings normalised, nothing else changed. Never rewrite it into a category, never summarise it, and never map it to a difficulty id on the reader's behalf. If the reader withdraws the difficulty the note was given for, drop the note with it and say so in one line; a note the reader can no longer see is one they cannot correct or withdraw. If free text clearly matches an existing difficulty, offer it as a question with a default of yes — do not assume.

## Screen 2 — what helps, one difficulty at a time

For each ticked difficulty, in the order ticked, show its `offers` with three fixed extras:

```
2 of 3.  "I forget where I was after interruptions"  (1 of 3)

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
Optional.  Do any of these only apply sometimes?

 1  Visual examples — always / learning only / when I am stuck
 2  Two options and a default — always / except when brainstorming

Enter to apply everything always.
```

Only offer this for supports where context genuinely changes the answer: the examples, disclosure and choice atoms. Never offer it for the sensory or assistive-technology atoms, which are always-on by nature. Contexts are `always`, `work`, `learning`, `brainstorming`, `stuck`, `overloaded`.

Never detect a context. The reader declares it by saying so, and `overloaded` may be offered — "say 'less' any time and I will switch to it" — but never entered on the agent's judgement.

## Screen 4 — the summary, in the reader's own terms

```
YOUR SETUP

You said:
  you forget where you were after interruptions
  too many choices are hard

You asked for:
  a recap when you come back
  a running state block
  never having to remember a value between turns
  at most two options, always with a default

Applies: always, except visual examples which are learning only.

Saved to needs.yaml at the location you chose.
Change it any time by saying "settings". Delete it with "forget my setup".
```

Show what was chosen, phrased as what was chosen, with its context only where it is not `Always`. Never show atom ids, never show evidence tiers on a selection or summary screen, never show rule text unless asked, never show a count of matched conditions, never show a label. If the reader asks why a rule is behaving a certain way, name the support they picked and offer to remove it.

To save the profile, use a location the reader chooses and report the actual path only after a successful write. If file access is unavailable, provide the profile for them to save. Free-text notes are preserved as written and may include sensitive information.

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

1. Reader asks to skip everything. Give them the base layer, say what it does in one line, stop.
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
