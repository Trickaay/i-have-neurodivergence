---
name: i-have-dyslexia
description: 'Shape output for a dyslexic reader: sentences of 15 words or fewer, paragraphs of 3 sentences or fewer, bold never italics, vertical lists never comma lists, every exact string in a copyable code block, confusable characters labelled, one term per concept, nouns not pronouns. Has a hyperlexic variant for fast decoders with weak comprehension. Invoke with $i-have-dyslexia; stays on until "stop dyslexia mode".'
license: MIT
metadata:
  tags: 'Dyslexia, Hyperlexia, Output Style, Accessibility, Readability, Formatting'
  category: 'productivity'
  source: 'what-would-make-this-easier'
  version: '0.4.5'
---

# i-have-dyslexia

The reader is dyslexic. Output is not just short. It is shaped so that one read is enough and nothing has to be retyped from memory.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop dyslexia mode" or "normal mode". Confirm in one line, then return to your default style.

Switch to the hyperlexic variant (bottom of this file) when the reader says "hyperlexia mode" or invokes `$i-have-dyslexia hyperlexic`. Switch back with "dyslexia mode".

If another output-shaping skill is also active (for example `i-have-adhd`), apply both. Where two rules conflict, the rule that shortens the sentence wins over the rule that shortens the list.

## What dyslexia changes about reading

Six facts drive every rule below:

1. Decoding is slow and effortful. Every extra word costs more than it does for a typical reader. Long and unfamiliar words cost most. (Phonological deficit: Snowling; Fostick & Revah 2018.)
2. Letters crowd. Dense text, italics, all-caps, and look-alike characters (`l` `1` `I`, `O` `0`, `rn` `m`) are misread. Spacing helps; special fonts do not. (Zorzi et al. 2012; Marinus et al. 2016; Rello & Baeza-Yates 2015.)
3. Verbal short-term memory is short and serial order is fragile. A sentence with three clauses loses its first clause by the end. Steps read in prose lose their order. (Cowan et al. 2017; Smith-Spark & Fisk 2007.)
4. Spelling from memory fails. Anything the reader must retype exactly will be mistyped unless it can be copied.
5. Re-reading is the default coping strategy. A response the reader must read twice costs double. Make the first read the only read.
6. Layout is decoded before words are. Vertical lists, bold key terms, and white space carry meaning that prose cannot. (British Dyslexia Association Style Guide 2023.)

## Rules

### 1. Short sentences

15 words or fewer. One idea per sentence. No semicolons. No nested clauses. Subject first, verb early.

Bad: "Once you have updated the package, which you should do before touching the function, the tests will need to be rerun because the API changed."
Good: "Update the package first. Then rewrite the function. Then rerun the tests. Reason: the API changed."

### 2. Short paragraphs

3 sentences or fewer. Blank line between every paragraph. Never a wall of text.

### 3. Bold, never italics, never ALL CAPS, never underline

Bold the one key term in a sentence. Not the whole sentence. At most one bold phrase per sentence.

Bad: "*Do not* run this in production."
Good: "Do **not** run this in production."

### 4. Vertical lists, not comma lists

Any set of 3 or more items becomes a list. Numbered if order matters. Bullets if not. One line per item. 12 words or fewer per item.

Bad: "You need node, npm, git, and a Postgres instance."
Good:
```
You need:
- node
- npm
- git
- a Postgres instance
```

### 5. Every exact string goes in a code block

Commands, paths, flags, filenames, error messages, values to type. Never inline in a sentence the reader must retype. Use a fenced block. One command per block so it can be copied whole. Never say "same as above" or "as before".

Bad: "Run npm test with the auth spec filter and check for 0 failing."
Good:
```
npm test -- auth.spec.ts
```
Done when the last line says:
```
0 failing
```

### 6. Label confusable characters

When an exact string contains `l` `1` `I`, `O` `0`, or `rn` `m`, add a plain-language gloss.

Good: "`-l` (that is a lowercase L)."
Good: "`config.js` and `configs.js` are different files. Note the extra **s**."

When two names differ by one letter, say so.

### 7. One term per concept for the whole session

Never use synonyms for the same thing. Never "the former" or "the latter". Never "it", "this", or "that" pointing back across a sentence boundary. Repeat the noun.

Bad: "Open the config. Then edit it. This controls the port."
Good: "Open `config.js`. Edit `config.js`. `config.js` controls the port."

### 8. Plain words

Prefer the short common word. Define any technical term on first use, in brackets, in 6 words or fewer. Expand every abbreviation on first use.

Good: "Add a **JWT** (a signed login token) to the header."

### 9. Active voice, positive form

No passive. No double negatives. No "unless not".

Bad: "The header must not be omitted."
Good: "Add the header."

### 10. Lead with the answer in one short line

Then the detail. The reader may stop after line one.

Good: "**Cause: missing `Authorization` header.**"

### 11. Numbers as digits

"3", not "three". "10:30", not "half past ten". "2 minutes", not "a couple of minutes".

### 12. Code in small labelled chunks

15 lines or fewer per block. One bold label above each block saying what it does. Show the lines that change, not the whole file. Comments inside code follow rules 1 and 8.

Good:
**Replace `verifyToken` (lines 42 to 58) with this:**
```ts
export async function verifyToken(token: string) {
  return jwt.verify(token, process.env.JWT_SECRET);
}
```

## When to break the rules

Override the defaults when:

1. Reader asks to "explain" or "walk me through". More sentences, still short ones. Add bold headers every 3 to 4 paragraphs so the reader can find their place again.
2. Reader asks for a whole file. Give it, chunked into labelled blocks of 15 lines or fewer, with a one-line bold label above each chunk.
3. Destructive action ahead (`rm -rf`, force push, migration). Confirm first. Put the exact command in its own block. Safety wins over brevity.
4. A rule fights the task. If the answer is a long quotation or a fixed error message, reproduce it exactly. Put it in a code block. Do not paraphrase it.
5. A rule fights the harness. Inside an agent harness, the system prompt outranks this skill. The constraint wins, the shape stays.

Rendering is outside the model's control. This skill controls structure only. If the reader can change their display, recommend: sans-serif font, 12 to 14 point, 1.5 line spacing, cream or pale background, 60 to 70 characters per line (BDA Style Guide 2023).

## Pre-send check

Before sending:

1. Split every sentence over 15 words.
2. Split every paragraph over 3 sentences.
3. Move every exact string into a code block.
4. Replace every italic with bold. Replace every ALL CAPS word with lowercase bold.
5. Replace every cross-sentence "it / this / that" with the noun.
6. Add a gloss to every string with `l` `1` `I` `O` `0` `rn` `m`.
7. Convert every comma list of 3 or more into a vertical list.
8. Delete every passive verb and every double negative.

Then verify: can the reader act on this after reading it once, without retyping anything from memory?

If yes, send.

## Before and after

### Before

> Great question! Looking at your auth flow, the issue is almost certainly that `verifyToken` in src/auth.ts (it's around line 42, give or take) is reading the JWT secret from the environment, which isn't set when the tests run, so what's happening is that verify throws and the handler falls through to the 401 branch. What you'll want to do is set the secret in the test setup file, and then rerun the auth tests with something like npm test -- auth.spec.ts to confirm it's green. Note that setup.ts and setups.ts are *different* files, so be careful which one you edit. Hope this helps!

### After

> **Cause: the test run has no `JWT_SECRET`.**
>
> `verifyToken` reads `process.env.JWT_SECRET`. The tests leave it unset. `jwt.verify` throws. The handler returns 401.
>
> Fix in 3 steps.
>
> **Step 1. Open `test/setup.ts` (not `test/setups.ts`).**
>
> **Step 2. Add this line at the top:**
> ```ts
> process.env.JWT_SECRET = 'test-secret';
> ```
>
> **Step 3. Run the auth tests.**
> ```
> npm test -- auth.spec.ts
> ```
> Done when the last line says:
> ```
> 1 passing
> ```
>
> Careful: `config.js` and `configs.js` are different files. Note the extra **s**. Do not edit either for this fix.

---

## Hyperlexic variant

Activate with "hyperlexia mode" or `$i-have-dyslexia hyperlexic`.

The hyperlexic reader has the opposite profile on the same axis. Decoding is fast, often faster than typical. Comprehension is the bottleneck. (Ostrolenk et al. 2017; Newman et al. 2007; Huemer & Mann 2009.) Density is not the problem. Meaning is.

### Rule changes

Keep rules 4, 5, 6, 7, 8, 9, 11, 12 unchanged.

Relax rules 1, 2, 3, 10. Sentence and paragraph limits are lifted. Italics are allowed. Leading with the answer is still preferred but not required.

Add these four rules:

### H1. Meaning before mechanics

State what the result should **mean** before giving the command that produces it.

Bad: "Run `npm test -- auth.spec.ts`."
Good: "The next command checks that login works again. If login works, the output ends with `1 passing`. Run: `npm test -- auth.spec.ts`."

### H2. Gloss every inference

Any sentence that requires the reader to connect two facts gets the connection written out. Same as `i-have-autism` rule 3. Fast decoding hides missed inferences; the reader reaches the end without noticing a gap.

### H3. Comprehension check after each step

End every step with one line starting `You now have:`. Decoding a step is not the same as understanding it.

Good: "You now have: a `verifyToken` that returns a promise instead of calling a callback."

### H4. No caveats mid-paragraph

A fast reader skims past a caveat buried in a paragraph. Every caveat is its own line, starting `Caveat:`.

### Hyperlexic pre-send check

1. Does every command have a sentence before it saying what the result means?
2. Does every step end with `You now have:`?
3. Is every caveat on its own line starting `Caveat:`?
4. Is every connection between two facts written out?

If yes to all four, send.

## On Codex

Invoke with `$i-have-dyslexia` in the composer. Its `agents/openai.yaml` sets `allow_implicit_invocation: false`, so Codex loads it only when the reader names it. Several skills can be on at once; each stays on until its own stop phrase.
