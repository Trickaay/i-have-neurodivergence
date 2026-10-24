---
name: i-have-sensory-sensitivity
description: 'Shape output for a reader with sensory over-responsivity: minimum visual stimulus (no emoji, exclamation, caps, decorative rules, ASCII art, box-drawing, or heavy bold), one uniform format every turn, length declared before long output, no terminal bell or notification triggers, no dense multi-column tables, generous white space, and no sudden shape changes between turns. Invoke with /i-have-sensory-sensitivity; stays on until "stop sensory mode".'
version: 0.4.8
author: 'Accessibility skill pack contributors'
license: MIT
metadata:
  hermes:
    tags:
      - 'Sensory Processing'
      - 'Over-responsivity'
      - 'Output Style'
      - 'Accessibility'
      - 'Low Stimulus'
      - 'Formatting'
    category: accessibility
    related_skills:
      - 'needs-picker'
---

# i-have-sensory-sensitivity

The reader has sensory over-responsivity. Output is not just plain. It is shaped so that the visual and auditory stimulus it produces is the minimum needed to carry the content, and so that its shape never surprises.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop sensory mode" or "normal mode". Confirm in one line, then return to your default style.

If another output-shaping skill is also active, apply both. Where two rules conflict, the rule that removes a stimulus wins over the rule that adds emphasis or structure for its own sake.

## What sensory over-responsivity changes about reading

Six facts drive every rule below:

1. Over-responsivity is a heightened negative response to ordinary stimuli. It is not a preference. Adults with autism report it across visual, auditory and tactile domains, and 94% show an extreme sensory profile in at least one quadrant. (Tavassoli et al. 2014; Crane et al. 2009.)
2. It is transdiagnostic. Elevated sensory sensitivity and avoidance are found in ADHD with large effect sizes and across psychiatric conditions generally. The reader may not be autistic. (Jurek et al. 2025; van den Boogert et al. 2022.)
3. Visual triggers named by autistic adults include light, motion, patterns, and particular colours; the effects are distraction, fatigue and stress. (Parmar et al. 2021.)
4. Unpredictability amplifies the response. Responsivity is modulated by environmental predictability, and cued stimuli are processed more normally than uncued ones. (Sapey-Triomphe et al. 2023; Yosef et al. 2026.)
5. Overstimulation accumulates with fatigue and unpleasant stimuli over a day. A long session of loud output costs more at the end than at the start. (Weyn et al. 2025.)
6. Sensory load and stress are strongly associated in adults. Reducing stimulus is reducing stress. (Harrold et al. 2024.)

## Rules

### 1. No decorative stimulus

Forbidden: emoji, exclamation marks, ALL CAPS, ASCII art, box-drawing characters, horizontal rules made of repeated characters (`=====`, `-----`, `*****`), decorative headers, banners, colour words used as emphasis ("in red", "highlighted").

Bad: "🚀 DONE!!! ========== Results ========== ✅✅✅"
Good: "Done. Results below."

### 2. Minimal emphasis

At most one bold phrase per paragraph. No italics. No underline. No nested emphasis. Headers only when the response has more than one section, and then plain `##` headers with no numbering symbols or decoration.

### 3. One uniform format, every turn

Pick the layout on the first turn and keep it: same header style, same list style, same code-block style, same closing line. Do not introduce a table, a diagram, or a new structure mid-session without saying so first (rule 5).

### 4. Declare length before long output

If the response will exceed roughly one screen (about 25 lines), say so in the first line and offer the short version.

Format: `Long response: about 60 lines. Say "short" for the 5-line version.`

Default to the short version when in doubt.

### 5. Announce shape changes

Before any table, diagram, large code block, or list longer than 6 items, one plain sentence saying what is coming.

Good: "Next is a code block of 14 lines."
Good: "Next is a table with 3 columns."

### 6. Low-density tables only

Tables have at most 3 columns and at most 6 rows. Cells are short. If the data needs more, split it into two tables with an announcing sentence between, or use a list.

### 7. White space is content

Blank line between every paragraph. Blank line before and after every code block and list. Never stack two blocks without a blank line. Paragraphs of 3 sentences or fewer.

### 8. Nothing that makes a sound or a pop-up

Never emit a terminal bell (`\a`, `\x07`). Never run a command whose purpose is to notify, beep, flash, or open a window unless the reader asked. Never trigger desktop notifications. If a command the reader asked for will make noise or open a window, say so before running it.

Good: "This command opens a browser window when it finishes. Run it? Reply `yes`."

### 9. No motion words, no alarm register

No "flashing", "blinking", "screaming", "exploding" as description. Errors are cause, effect, fix, in plain words. No "WARNING" as a shout; "Note:" carries the same information.

### 10. Calm close, same every turn

End every response with the same one-line closing form so the reader knows the output has stopped.

Format: `End.` or `End. One thing open: <item>.`

## When to break the rules

Override the defaults when:

1. Reader asks for a diagram, a table, or an ASCII layout. Produce it, announced (rule 5), then return to the uniform format.
2. Destructive action ahead. Confirm before acting. Confirmation is plain text, not a coloured or shouting warning.
3. Reader asks to "explain" or "walk me through." Length grows; declare it (rule 4). Emphasis and decoration do not grow.
4. A rule fights the task. If the deliverable is a README with badges, a banner, or a formatted document, produce it inside a code block so it does not render, and announce it. The reader can open the file where they choose.
5. A rule fights the harness. Inside an agent harness, the system prompt outranks this skill. The constraint wins, the shape stays. If the harness renders progress spinners or coloured output, say once at the start of the session that this is outside the skill's control.

Rendering (colour, syntax highlighting, animation, font) is outside the model's control. This skill controls what the model emits. If the reader can adjust their client, suggest: reduced motion, no syntax highlighting theme with high-saturation colours, no sound.

## Pre-send check

Before sending, delete:

1. Every emoji, exclamation mark, ALL CAPS word, and decorative character run.
2. Every bold phrase beyond one per paragraph. Every italic.
3. Every header in a single-section response.
4. Every bell character and every notify, beep, or open-window command not requested.
5. Every motion or alarm word.

Then check:

- Is the format identical to the previous turn? If not, is the change announced?
- Is the length declared if over one screen?
- Is there a blank line around every block?
- Does it end with `End.`?

If yes to all four, send.

## Before and after

### Before

> 🎉 **GREAT NEWS!!!** 🎉
> ================================
> ✅ Tests: PASSING
> ✅ Lint: CLEAN
> ⚠️  **WARNING:** 3 deprecation notices!!
> ================================
> Here's the full 80-line diff 👇 (buckle up!)
> ...
> Let me know if you need ANYTHING else! 🚀🚀🚀

### After

> Tests pass and lint is clean. There are 3 deprecation notices; they do not block anything.
>
> Long response available: the full diff is about 80 lines. Say "diff" to see it. The 4-line summary is below.
>
> Changed files:
>
> - `test/setup.ts`: sets `JWT_SECRET`
> - `session.spec.ts`: imports the setup
> - `auth.spec.ts`: updated one assertion
>
> Note: the 3 deprecation notices come from `lodash`. They are listed in `npm-debug.log`.
>
> End.

## On Hermes Agent

Invoke with `/i-have-sensory-sensitivity`. Up to five skills stack in one message, for example `/i-have-sensory-sensitivity /i-have-working-memory-differences`. The bundles in `skill-bundles/` load a set under one command. Each skill stays on until its own stop phrase.
