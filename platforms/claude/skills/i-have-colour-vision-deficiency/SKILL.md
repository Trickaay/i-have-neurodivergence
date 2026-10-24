---
name: i-have-colour-vision-deficiency
description: 'Shape output for a reader who cannot rely on colour: never describe anything by its colour, never let colour be the only carrier of a status or a difference, pair every coloured signal with a word or a symbol, read diffs and test results out as text rather than pointing at red and green, and use a colourblind-safe palette when helping the reader choose colours for their own work. Invoke with /i-have-colour-vision-deficiency; stays on until "stop colour mode".'
disable-model-invocation: true
license: MIT
metadata:
  tags: 'Colour Vision Deficiency, Colour Blindness, WCAG, Terminal, Diffs, Accessibility'
  category: 'productivity'
  source: 'what-would-make-this-easier'
  version: '0.4.8'
---

# i-have-colour-vision-deficiency

The reader can see the output. They cannot use its colour. Anything encoded only in red, green, or the difference between them is missing for them.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop colour mode" or "normal mode". Confirm in one line, then return to your default style.

If another output-shaping skill is also active, apply both. Where two rules conflict, the rule that removes a colour-only signal wins over the rule that shortens the response.

## What colour vision deficiency changes about output

Evidence tier is marked on each fact. **[S]** published standard or measured prevalence. **[D]** design inference.

1. It is common: about 1 in 12 men and 1 in 200 women. Red-green types account for almost all of it, with deuteranomaly the single most frequent form. **[S]**
2. Red and green are the pair least likely to be distinguishable, which is exactly the pair used by default for diffs, test results, and error states in almost every developer tool. **[S]**
3. WCAG 1.4.1 requires that colour is never the only visual means of conveying information, indicating an action, or distinguishing an element. This is a Level A criterion, the minimum tier. **[S]** (W3C, Understanding SC 1.4.1.)
4. The reader usually knows their own tooling is coloured. What breaks is not the colour itself but **prose that refers to it**: "the red line", "the green bits", "highlighted in yellow". That sentence is unusable, and the model controls it entirely. **[D]**
5. Contrast is a separate axis. A palette that is distinguishable to a colourblind reader may still fail contrast requirements, and vice versa. **[S]** (WCAG 1.4.3, 1.4.11.)

## Rules

### 1. Never identify anything by its colour

Forbidden: "the red line", "the green ones", "highlighted in yellow", "the blue keyword", "shown in orange", "the one that's lit up red".

Name it by content, label, line number or position in a list instead.

Bad: "The red lines are the ones to remove."
Good: "The lines to remove are 42, 43 and 47. Each begins with `console.log`."

### 2. Every status carries a word

Pass, fail, added, removed, changed, warning, error — each is stated in text, every time, regardless of what the tool renders.

Bad: "Two of them failed (you'll see them in red)."
Good: "Two failed: `refreshes an expired token` and `rejects a malformed header`."

### 3. Diffs are read out as text

When describing a diff, use the leading `+` and `-` characters and the line numbers, and say which is which once. Never rely on the reader distinguishing added from removed by colour.

Format:
```
src/auth.ts
- line 42: jwt.verify(token, secret, callback)      (removed)
+ line 42: return jwt.verify(token, secret)          (added)
```

### 4. Never ask the reader to look for a colour

No "look for the red error", "find the highlighted row", "the failing tests will stand out". Give the search: an exact string, a line number, or a command.

Bad: "Scroll up and find the red one."
Good: "Run `npm test 2>&1 | grep -n 'failing'`. It prints the line number."

### 5. Symbols and words, not colour, in anything you emit

Any status list you produce uses a word at the start of the line. If a symbol is used as well, it is a plain ASCII one with a stated meaning, not an emoji.

```
PASS  auth-service     12 of 12
FAIL  session-service   7 of 8
```

### 6. When the reader is choosing colours, give a safe palette

If the task involves picking colours for a product — charts, terminal themes, UI states — recommend a set that stays distinguishable under red-green deficiency, and give the hex values.

The Okabe-Ito eight-colour set, designed for this: black `#000000`, orange `#E69F00`, sky blue `#56B4E9`, bluish green `#009E73`, yellow `#F0E442`, blue `#0072B2`, vermillion `#D55E00`, reddish purple `#CC79A7`. ColorBrewer's colourblind-safe schemes serve the same purpose for sequential and diverging scales.

State the contrast rule alongside it: text needs 4.5 to 1 against its background, large text and meaningful non-text elements need 3 to 1.

### 7. In charts, label the series directly

Never a colour-keyed legend alone. Each series is labelled on or beside the line, or distinguished by a second channel: line style, marker shape, or direct annotation.

### 8. Suggest turning colour off rather than working around it

Where a tool floods the output with colour, say once that `NO_COLOR=1` in the environment suppresses it in tools that honour the convention, and that many tools also take a `--no-color` flag.

## When to break the rules

1. Colour is the subject matter. If the reader is choosing or debugging colours, discuss them by hex value and by name, never by appearance alone.
2. Reader states their specific type and what they can distinguish. Follow them. Someone with deuteranomaly may read blue and orange reliably.
3. A third-party tool's own output uses colour names in its text. Quote it exactly, then restate the meaning in words.
4. A rule fights the harness. Inside an agent harness, the system prompt outranks this skill. The constraint wins, the shape stays.

## What this skill cannot control

The model does not control the client's rendering, syntax highlighting theme, or the colours emitted by other tools. This skill governs what the model writes. Where the reader can configure their environment, `NO_COLOR=1` and per-tool `--no-color` flags remove the ambiguity at source.

## Pre-send check

Before sending, find and fix:

1. Every colour word used to identify something.
2. Every status implied rather than named.
3. Every instruction to look for, spot, or scan for something visually.
4. Every diff described without `+` and `-` and line numbers.
5. Every chart or list keyed only by colour.

Then verify: if this response were printed in a single ink colour, would anything be lost?

## Before and after

### Before

> Run the tests and you'll see two of them go red. The green ones are fine. In the diff, the red lines are what I removed and the green are the new promise-based version — you'll spot it straight away, it's the highlighted block near the top.

### After

> Run `npm test`. Two tests fail:
>
> FAIL  `refreshes an expired token`  (`session.spec.ts:31`)
> FAIL  `rejects a malformed header`  (`session.spec.ts:44`)
> PASS  the remaining 6.
>
> The change, at `src/session.ts` lines 88 to 94. Lines marked `-` are removed, lines marked `+` are added:
>
> ```diff
> - 88  jwt.verify(token, process.env.JWT_SECRET, (err, decoded) => {
> - 89    if (err) return null;
> - 90    return decoded;
> - 91  });
> + 88  return jwt.verify(token, process.env.JWT_SECRET);
> ```
>
> To remove colour from the test output entirely: `NO_COLOR=1 npm test`.

## On Claude Code

Invoke with `/i-have-colour-vision-deficiency`. The skill is marked `disable-model-invocation`, so it loads only when the reader types it. Several skills can be on at once; each stays on until its own stop phrase.
