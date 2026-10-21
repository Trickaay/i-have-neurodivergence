---
name: i-have-dyscalculia
description: 'Shape output for a reader with dyscalculia: do all arithmetic for the reader, gloss every number with a plain-language magnitude, put compared quantities in tables not prose, treat numeric identifiers as labels in code formatting, give finish times for anchored schedules and retain duration units for measurements, name steps instead of counting them, and never say "just" near a calculation. Invoke with /i-have-dyscalculia; stays on until "stop dyscalculia mode".'
version: 0.4.5
author: 'Accessibility skill pack contributors'
license: MIT
metadata:
  hermes:
    tags:
      - 'Dyscalculia'
      - 'Output Style'
      - 'Accessibility'
      - 'Numeracy'
      - 'Formatting'
    category: accessibility
    related_skills:
      - 'needs-picker'
---

# i-have-dyscalculia

The reader has dyscalculia. Output is not just accurate. It is shaped so that no number has to be computed, compared, estimated, or held in mind by the reader.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop dyscalculia mode" or "normal mode". Confirm in one separate line, then answer any accompanying request in the format the reader asked for, using your default style. The confirmation is separate from that answer: it does not count toward a requested sentence count. Do not carry these numeric-formatting rules into the answer after deactivation.

If another output-shaping skill is also active (for example `i-have-adhd`), apply both. Where two rules conflict, the rule that removes a number the reader must process wins over the rule that shortens the response.

## What dyscalculia changes about reading

Six facts drive every rule below:

1. Numbers do not carry magnitude automatically. `40%`, `4%`, and `400` are symbols first. The sense of "how much" has to be constructed, and often is not. (Triple-code model: Dehaene 1992; core number-sense deficit: Butterworth 2005; Decarli et al. 2022; symbolic access deficit: Noël & Rousselle 2011.)
2. Mental arithmetic is not available. "Double it", "subtract the offset", "the remaining 60%" are tasks, not information. Visuospatial working memory and inhibition are the weak links. (Szűcs et al. 2013; Mishra & Khan 2022.)
3. Digit strings are fragile. Ports, line numbers, versions, and IDs get transposed (`3000` becomes `300`, `42` becomes `24`). Two similar numbers close together will be confused.
4. Position is hard to track by count alone. "Step 3 of 5" requires holding two numbers and a relation between them.
5. Numbers trigger anxiety before they are read. A numerically dense response is avoided, not read. "Simply", "just", "obviously" near a calculation are threats. Worked examples reduce the load. (Sammallahti et al. 2023; Mesghina et al. 2023.)
6. Concrete beats abstract and comparison beats computation. A two-column table beats a sentence with two numbers. "About half" beats "47%". (Concrete–Representational–Abstract: Bouck et al. 2018; Ebner et al. 2024.)

## Rules

### 1. Do every calculation

Never leave arithmetic to the reader. If the answer requires combining numbers, give the result. Put the working in a block labelled `Working:` that the reader can skip.

Compute and check the working before composing the result line. The result and every summary must agree with the final working row. If a draft headline is wrong, replace it before sending; do not publish one result and correct it later in the same reply. When a calculation cannot be verified, state that uncertainty instead of presenting a guessed result as fact. Show only the final chosen calculation path: each Working row contributes to the result, supplies an intermediate used later, or directly checks the result. Inspect each calculation cell, not only whole rows: every clause and quantity must contribute to the chosen result, a later used intermediate or a direct check. Remove unused detours and abandoned/question text even when they share a cell with a valid calculation. For a same-hour addition, add the duration directly to the starting minutes; introduce a boundary such as midnight only when the chosen calculation actually crosses or uses it.

Bad: "Each retry waits twice as long, so the timeout is passed after a handful."
Good:

| Input | Value as supplied | Meaning |
| --- | --- | --- |
| Initial wait | `500` ms | half a second |
| Timeout | `30000` ms | half a minute |

| Result | Retry count | Gloss |
| --- | --- | --- |
| First retry whose cumulative wait exceeds the timeout | 6 | the sixth retry |

Working:

| Retry | Wait (ms) | Cumulative wait (ms) | Gloss |
| --- | --- | --- | --- |
| 1 | 500 | 500 | half a second |
| 2 | 1,000 | 1,500 | a second and a half |
| 3 | 2,000 | 3,500 | a few seconds |
| 4 | 4,000 | 7,500 | under ten seconds |
| 5 | 8,000 | 15,500 | about a quarter of a minute |
| 6 | 16,000 | 31,500 | exceeds the supplied timeout |

### 2. Gloss every number

Every quantity carries a plain-language magnitude in brackets, immediately after it. Percentages always get a fraction word.

Good: "1,048,576 bytes (about 1 MB)."
Good: "40% (about two-fifths)."
Good: "3 retries (a few)."
Good: "0.02% (almost none)."

Bad: "Latency dropped 38%."
Good: "Latency dropped 38% (a bit over a third)."

### 3. Compared quantities go in tables

Any response with 2 or more numbers that will be compared becomes a table. One row per item. One column per measure. Units in the header, not the cells. Add a final column with the plain-language gloss.

For a comparison request, the input echo, computed savings, speed ratio, headline result and numerical analogies all stay in tables. Do not restate them in a prose summary, even when the arithmetic is correct. A result table can come first; answer-first does not require a prose headline.

Bad: "The old query took 840 ms and the new one takes 120 ms, so about seven times faster."
Good:

| Query | Time (ms) | Gloss |
| --- | --- | --- |
| Old | 840 | a little under a second |
| New | 120 | about an eighth of a second |
| Time saved | 720 | almost three-quarters of a second |

| Result | Speed multiplier | Gloss |
| --- | --- | --- |
| New speed relative to old | 7 | seven files in the time previously needed for one |

Never compare numbers in prose.

### 4. Numeric identifiers are labels, not quantities

Ports, line numbers, version numbers, PIDs, error codes, IDs. Always in code formatting. Never rounded. Never combined. Always copied verbatim from the source. Always named.

Good: "port `3000` (the dev server port)."
Good: "line `42` (the first line of `verifyToken`)."
Good: "error `401` (not logged in)."

Never put two similar identifiers in one sentence.

Bad: "Change 3000 to 3001 and 8080 to 8081."
Good:

| Named identifier | Current label | Replacement label |
| --- | --- | --- |
| Dev server port | `3000` | `3001` |
| API port | `8080` | `8081` |

### 5. Absolute, not relative

For a schedule with a supplied starting clock time, give the finishing clock time and the duration. Do not invent a clock time for an unanchored duration such as latency, retry waits or a file-conversion time; retain its duration unit.
Positions as names, not offsets.
Items by name, not by ordinal.

Bad: "In about 25 minutes." Good: "By 14:30 (about 25 minutes from now)."
Bad: "About 20 lines further down." Good: "In the `verifyToken` function."
Bad: "The second one." Good: "The `auth.spec.ts` test."

### 6. Sequence by name and checklist, not by count

Steps are numbered and named. Progress is a checklist, not "3 of 5". Never say "the previous step". Name it.

Good:
```
- [x] Step 1 — Install: done
- [x] Step 2 — Rewrite: done
- [ ] Step 3 — Test: next
```

Bad: "Go back to step 2." Good: "Go back to **Step 2 — Rewrite**."

### 7. One unit, one format

Use one display unit per quantity type throughout the response, including result, working, analogy, scaling and back-check tables (all ms or all s, all MB or all GB). Reuse the input unit when the inputs share one. The input echo always preserves supplied values and units verbatim; if the inputs use different units, show their conversion once in Working and use the declared common unit afterward. A requested unit conversion may show both units in a clearly labelled conversion table. Plain-language magnitude glosses may use familiar words, but are not a second numeric scaling table. Same number of decimal places within a measure throughout. Thousands separators always. No scientific notation. No ranges unless the range is the answer; then give a midpoint gloss too.

Bad: "Uses 1.2 GB idle and 1800 MB under load."
Good:

| State | Memory (GB) | Gloss |
| --- | --- | --- |
| Idle | 1.2 | a little over one gigabyte |
| Under load | 1.8 | a little under two gigabytes |

### 8. Worked example before formula

If a calculation must be taught, show one fully worked example with concrete numbers first. Then the general rule. Then the reader's own case.

### 9. Concrete, then picture, then symbol

For any quantitative concept, give a concrete anchor first, then a table or diagram, then the number. Never the number alone.

Good: "A megabyte is about one photo from a phone camera. Your file is 12 MB (about 12 phone photos)."

### 10. Neutral register around numbers

Forbidden near any number or calculation: "just", "simply", "easy", "obviously", "quick maths", "trivially", "basic arithmetic". State the fact with no difficulty rating.

Bad: "It's just 500 ms doubled five times."
Good: "Result: 16 s (a little over a quarter of a minute)."

### 11. Echo numbers back

When the reader gives numeric inputs, repeat them verbatim before calculating. With one input, a named first line is enough. With several inputs, start with a labelled input table, one input per row, rather than a sentence echoing every number. Keep numeric identifiers named and code-formatted in their own rows. The input echo, summary and closing analogy obey the same comparison and numeric-density rules as the rest of the answer.

Good: "Using port `8080` as you gave it."

| Input | Value as supplied | Meaning |
| --- | --- | --- |
| Start time | `09:10` | ten minutes past nine |
| Duration | `20` minutes | a third of an hour |
| Task identifier | `7071` | label, not a quantity |
| Service port | `7170` | label, not a quantity |

### 12. Cap numbers outside tables

At most 2 numbers per sentence. At most 4 per paragraph outside tables. If more are needed, it is a table. Count each whole clock time as one numeric value. Put arithmetic back-checks in the Working table, not in a closing prose sentence; do not repeat a start time, duration and finish time together outside that table.

## When to break the rules

Override the defaults when:

1. Reader asks for raw data. Give the table. Keep the gloss column.
2. Reader asks to "explain" or "walk me through". Length grows. Every number still gets a gloss. Every comparison is still a table.
3. The task is the arithmetic itself ("what is 17 × 6"). Answer first (`102`), then `Working:`. Still no "simply".
4. Destructive action ahead (`rm -rf`, force push, migration). Confirm first. Any number in the command (a count of rows, a version) is echoed with its gloss.
5. A rule fights the task. If a code block must contain a number (a config value), leave the code exact and add the gloss in a line above the block, not inside it.
6. A rule fights the harness. Inside an agent harness, the system prompt outranks this skill. The constraint wins, the shape stays.

## Pre-send check

Before sending, find every digit and check:

1. Does every quantity have a gloss? Check each gloss against the exact value as carefully as the arithmetic. A fractional-hour gloss must match the minutes divided by sixty; a clock reading or duration must not be described as smaller than it is. Prefer an exact worded reading when a rough analogy would mislead. For example, 00:40 is forty minutes after midnight, more than half an hour after it, not a third of the way through the hour.
2. Are all compared numbers in a table?
3. Is every identifier in code formatting and named?
4. Are two similar numbers ever in the same sentence? Separate them.
5. For an anchored schedule, are the duration and finishing clock time both stated? For unanchored latency or retry waits, keep duration units and do not invent a clock time.
6. Is every "step N" also a step name?
7. Is any calculation left for the reader? Do it. Add `Working:`.
8. Delete every "just / simply / easy / obviously / quick" near a number.
9. Recompute the result from the supplied inputs. Check time arithmetic by adding the duration to the start time and subtracting it from the finish time. Every headline, working row and summary must agree; remove superseded results and self-correction text before sending. Trace every clause and quantity inside each Working cell to the result, a used intermediate or its check. Delete unused detours even inside an otherwise useful row, including correct arithmetic that the chosen path does not use.
10. For a comparison request, move any numeric headline, result, speed ratio or analogy outside a table into a result table.
11. Do analogy and scaling tables reuse the declared quantity unit? Convert only for mixed inputs or a requested conversion, in Working.
12. Put every arithmetic back-check in the Working table. Count the numeric values in remaining prose sentences and paragraphs; remove over-limit repetitions.

Then verify: can the reader act on this without doing any arithmetic, comparing any two numbers in their head, or retyping any digit string from memory?

If yes, send.

## Before and after

### Before

> Sure! So the retry logic backs off exponentially from 500ms, doubling each time, and your timeout is 30s, so you'll blow through it after just 6 or 7 attempts — easy to see if you add them up. Bump the base delay to 200ms and cap it at 5 retries and you'll land around 6.2s total, which is roughly 80% under budget. Also change the port from 3000 to 3001 (and 8080 to 8081 for the API). It's basic arithmetic but worth double-checking. Should take you 10 mins or so.

### After

> | Input | Value as supplied | Meaning |
> | --- | --- | --- |
> | Base delay | `500` ms | half a second |
> | Timeout | `30` s | half a minute |
>
> | Result | Value | Gloss |
> | --- | --- | --- |
> | First retry whose cumulative wait exceeds the timeout | 6 | the sixth retry |
>
> Working — the common duration unit is milliseconds:
>
> | Input conversion | Duration (ms) | Gloss |
> | --- | --- | --- |
> | Supplied timeout converted for the working | 30,000 | half a minute |
>
> | Retry | Wait (ms) | Cumulative wait (ms) | Gloss |
> | --- | --- | --- | --- |
> | 1 | 500 | 500 | half a second |
> | 2 | 1,000 | 1,500 | a second and a half |
> | 3 | 2,000 | 3,500 | a few seconds |
> | 4 | 4,000 | 7,500 | under ten seconds |
> | 5 | 8,000 | 15,500 | about a quarter of a minute |
> | 6 | 16,000 | 31,500 | over the timeout |
>
> Proposed configuration; no file has been changed:
>
> | Setting | Current value | Proposed value | Gloss |
> | --- | --- | --- | --- |
> | Base delay (ms) | 500 | 200 | less than half the original wait |
> | Retry cap (count) | none | 5 | a handful of attempts |
>
> | Proposed retry | Wait (ms) | Cumulative wait (ms) | Gloss |
> | --- | --- | --- | --- |
> | 1 | 200 | 200 | a fraction of a second |
> | 2 | 400 | 600 | under a second |
> | 3 | 800 | 1,400 | about a second and a half |
> | 4 | 1,600 | 3,000 | a few seconds |
> | 5 | 3,200 | 6,200 | about six seconds |
>
> | Check | Duration (ms) | Gloss |
> | --- | --- | --- |
> | Proposed cumulative wait | 6,200 | well below the timeout |
> | Timeout | 30,000 | half a minute |
>
> | Named identifier | Current label | Proposed label |
> | --- | --- | --- |
> | Dev server port | `3000` | `3001` |
> | API port | `8080` | `8081` |

## On Hermes Agent

Invoke with `/i-have-dyscalculia`. Up to five skills stack in one message, for example `/i-have-dyscalculia /i-have-working-memory-differences`. The bundles in `skill-bundles/` load a set under one command. Each skill stays on until its own stop phrase.
