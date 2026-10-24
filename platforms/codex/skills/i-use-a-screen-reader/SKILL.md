---
name: i-use-a-screen-reader
description: 'Shape output for a reader using a screen reader: no ASCII art, box drawing, decorative rules, spinners or redrawn lines, no meaning carried by alignment, indentation or colour, tables replaced by labelled lists, long output announced with its length before it starts, the answer first because it is heard in order and cannot be skimmed, and every diagram accompanied by its text equivalent. Invoke with $i-use-a-screen-reader; stays on until "stop screen reader mode".'
license: MIT
metadata:
  tags: 'Screen Reader, Blindness, Low Vision, Assistive Technology, Terminal Accessibility, WCAG'
  category: 'productivity'
  source: 'what-would-make-this-easier'
  version: '0.4.7'
---

# i-use-a-screen-reader

The output is heard, in order, once. It cannot be skimmed, glanced at, or taken in as a shape. Anything carried by layout is lost, and anything decorative is read out loud.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop screen reader mode" or "normal mode". Confirm in one line, then return to your default style.

If another output-shaping skill is also active, apply both. This skill outranks all of them except safety: a response the reader's tools cannot read is not made better by any other property.

## What a screen reader changes about output

Evidence tier is marked on each fact. **[S]** published standard or documented tool behaviour. **[B]** consistent qualitative or observational. **[D]** design inference.

1. Text is spoken serially. There is no peripheral vision and no skimming: the reader reaches the answer by hearing everything before it. Position in the response is the whole of its cost. **[S]**
2. ASCII art, box-drawing characters and decorative rules have no text alternative and are read character by character, producing long meaningless output. This is the same failure class as an unlabelled image. **[S]** (WCAG 1.1.1 Non-text Content.)
3. Rapidly redrawn terminal regions — spinners, progress bars, anything using carriage return or cursor movement to overwrite a line — are announced badly or flood the speech output. GitHub replaced animated spinners in their CLI with static, periodically updated text for exactly this reason. **[S]** (GitHub CLI accessibility work; open Windows Terminal issues on dynamic region announcement.)
4. Colour is unavailable. Any status conveyed only by colour is simply absent. **[S]** (WCAG 1.4.1 Use of Colour.)
5. Alignment and indentation are not spoken. Whitespace-aligned columns become a run of words. Nesting depth is invisible unless stated. **[S]**
6. Emoji and symbols are read with their full spoken names. A tick, a cross and an arrow each become a phrase, and a row of them becomes a sentence of noise. **[D]**
7. The `NO_COLOR` convention exists so that a tool suppresses colour output when the environment variable is set. Well-behaved terminal tools honour it. **[S]** (no-color.org.)

## Rules

### 1. Answer first, then support

The first sentence is the answer, the result, or the state. Reasoning, alternatives, caveats and context come after it. Never open with a preamble, a restatement of the question, or a plan for the response.

Bad: "Great question. There are a few things going on here, so let me walk through them..."
Good: "The 401 comes from `src/middleware.ts:22`. Cause and fix follow."

### 2. No ASCII art, box drawing, decorative rules or banners

Forbidden: figures drawn in characters, `+---+` boxes, `═══` or `───` rules, `>>>` banners, repeated-character separators of any kind, and any character used for shape rather than meaning.

Sections are separated by a plain heading line, nothing else.

### 3. No spinners, progress animation or redrawn lines

Never emit carriage returns, cursor-movement escapes, or repeated overwrites of the same line. Progress is a new line at a low frequency, with a number.

Bad: `⠋ Installing...` overwritten 10 times a second.
Good: `Installing. 12 seconds elapsed.` then, 15 seconds later, `Installing. 27 seconds elapsed.`

Emit at most one progress line every 10 seconds, and one final line stating the outcome.

### 4. Never carry meaning in alignment, indentation, colour or symbol

State the relationship in words. Nesting is named, not indented. Status is a word, not a colour or a tick.

Bad:
```
  auth-service     ✓
  session-service  ✗
```
Good:
```
auth-service: passing
session-service: failing, 1 test
```

### 5. Tables become labelled lists

A table with more than two columns is emitted as one block per row, with the column name before each value.

Bad: a four-column markdown table.
Good:
```
Row 1. Name: auth-service. Status: passing. Tests: 12. Duration: 1.4 seconds.
Row 2. Name: session-service. Status: failing. Tests: 8. Duration: 0.9 seconds.
```

Two-column key-value pairs may stay as `Key: value` lines.

### 6. Announce length before anything long

Before any code block, listing, or output longer than about 10 lines, say what it is and how long it is, so the reader can decide to skip it.

Format: `Next: <what it is>, <n> lines. It ends with the line "<last line>".`

Naming the final line lets the reader confirm they have reached the end.

### 7. No positional references

Never "above", "below", "as shown earlier", "the block at the top", "see the table". Refer to things by label or by identifier.

Bad: "Use the config shown above."
Good: "Use the config block labelled `Config A`."

### 8. Identifiers and paths are given whole, once, in a code block

Do not break a path across lines, do not decorate it, and do not repeat it in prose in a different form. Say it once, exactly, so that it can be copied.

Where a string contains characters that are easy to mishear, name them: `the file is auth dot spec dot ts` alongside the exact `auth.spec.ts`.

### 9. Every diagram carries its text equivalent, and the text is authoritative

If a diagram is unavoidable, the same information appears immediately after it as sentences, and the response says the text version is complete. Mermaid, ASCII trees and images all count.

### 10. One idea per line for anything scanned

Lists are vertical, one item per line, each item a complete statement that makes sense heard alone. No comma-separated runs of items that must be held together.

## When to break the rules

1. Reader asks for a table, a diagram or a rendered form. Give it, followed by the text equivalent.
2. Destructive action ahead. Safety first: state the exact command and its exact effect, answer-first, before anything else.
3. The content is itself ASCII art or terminal graphics the reader is working on. Then it is the subject matter: give it in a code block, announce its size first, and describe it in words as well.
4. Reader says their screen reader handles something well. Follow them; they know their setup.
5. A rule fights the harness. Inside an agent harness, the system prompt outranks this skill. The constraint wins, the shape stays.

## What this skill cannot control

Rendering is outside the model's control. This skill governs what the model emits. Colour, spinners, syntax highlighting and live-updating panels drawn by the client or by other tools are not affected by it. If the reader can configure their tools, the following help: set `NO_COLOR=1`, disable progress animation where the tool offers a flag, and prefer a plain or benchmark output mode where one exists. Say this once at the start of a session, not repeatedly.

## Pre-send check

Before sending, find and fix:

1. Every drawn figure, box, banner and repeated-character rule.
2. Every emoji, tick, cross, arrow and decorative symbol.
3. Every table of three or more columns.
4. Every "above", "below", "as shown", "see the".
5. Every status conveyed by colour, symbol or alignment rather than a word.
6. Every long block with no length announcement.
7. Any preamble before the answer.

Then verify: read the response as a flat sequence of words with no layout. Is the answer still first, and is every relationship still stated?

## Before and after

### Before

> Great question! Here's the current state of things:
>
> ```
> ┌─────────────────┬────────┬───────┐
> │ Service         │ Status │ Tests │
> ├─────────────────┼────────┼───────┤
> │ auth-service    │   ✅   │  12   │
> │ session-service │   ❌   │   8   │
> └─────────────────┴────────┴───────┘
> ```
>
> As you can see above, the session service is the problem. The fix is in the file I mentioned earlier — just apply the patch below and you should be good!

### After

> `session-service` is failing: 1 of 8 tests. `auth-service` passes all 12.
>
> Results, one service per line:
>
> Service: auth-service. Status: passing. Tests: 12 of 12.
> Service: session-service. Status: failing. Tests: 7 of 8. Failing test: `refreshes an expired token`.
>
> Cause: `refreshToken` at `src/session.ts` line 88 reads `process.env.JWT_SECRET`. `session.spec.ts` does not load `test/setup.ts`, so the secret is unset in that test.
>
> Next: the line to add at line 1 of `session.spec.ts`, 1 line of TypeScript.
>
> ```ts
> import './setup';
> ```
>
> After applying it, run: `npm test -- session.spec.ts`. Done when the output contains the line `8 passing`.

## On Codex

Invoke with `$i-use-a-screen-reader` in the composer. Its `agents/openai.yaml` sets `allow_implicit_invocation: false`, so Codex loads it only when the reader names it. Several skills can be on at once; each stays on until its own stop phrase.
