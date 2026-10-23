---
name: i-have-apd
description: 'Shape output for a reader with auditory processing differences who chose it: written form is the primary channel unless the reader says otherwise, every spoken exchange gets a written copy, sequences are chunked and numbered, proper nouns and commands are spelled out, phonetically confusable terms are disambiguated, speech-to-text input is echoed back only when the reader says they use it, and nothing relies on an audio-only cue. Invoke with /i-have-apd; stays on until "stop apd mode".'
version: 0.4.6
author: 'Accessibility skill pack contributors'
license: MIT
metadata:
  hermes:
    tags:
      - 'APD'
      - 'Auditory Processing'
      - 'Output Style'
      - 'Accessibility'
      - 'Voice'
      - 'Formatting'
    category: accessibility
    related_skills:
      - 'needs-picker'
---

# i-have-apd

The reader has auditory processing differences (APD). Output is not just written. It is shaped so that nothing important ever exists only as sound, sequential information never arrives as an unbroken stream, and words that sound alike are never left to be told apart by ear.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop apd mode" or "normal mode". Confirm in one line, then return to your default style.

If another output-shaping skill is also active, apply both. Where two rules conflict, the rule that puts information into written, chunked form wins over the rule that shortens the response.

## What APD changes about reading and listening

Six facts drive every rule below:

1. Hearing is normal. Processing what is heard is not. Rapid speech, complex instructions, and speech in noise are the documented difficulties. (Alanazi 2023; Majak et al. 2023.)
2. Verbal working memory is weaker on both simple and complex tasks, so a long spoken sequence is lost before it ends. (Spandita et al. 2026.)
3. Temporal-order processing is tied to working memory: the order of items in a spoken list is the first thing to go. (Davidson et al. 2023.)
4. Phonological awareness is often weak, so words that sound alike (`fifteen` / `fifty`, `except` / `accept`, `.sh` / `.h`) are confused, and unfamiliar names cannot be reconstructed from sound. (Pires et al. 2015.)
5. The profile may overlap with reading, language and attention differences, and the diagnostic validity of APD itself is disputed in recent literature. None of that is to be assumed for any one reader: a co-occurring hearing, reading or language need is known only when the reader says so. (van Dijk et al. 2017.)
6. Written form is one accommodation, the default of this skill, not the only one. Confirm the reader's preferred input and output channels rather than inferring them; a deaf or hard-of-hearing reader may prefer a signed language or captions, and text does not resolve every language or reading barrier.

## Rules

### 1. Written form is the primary channel

Every piece of information the reader needs exists in text. If the session has a voice channel, everything said aloud is also written. If the harness can only speak, the response is shaped by rules 2 to 8 and the reader is told a written copy is available on request.

Bad: (voice only) "Okay so first you'll want to open the config and then..."
Good: (voice) "I have written the three steps in the chat." (chat) `1. ... 2. ... 3. ...`

### 2. Chunk everything sequential

Any sequence of more than 2 items is a numbered vertical list, one item per line, 12 words or fewer per item. Never a spoken or written run-on ("first do X then Y then Z and after that W").

Bad: "Install it, then set the env var, restart, and check the logs."
Good:
```
1. Install: (block below)
2. Set `PORT=3001` in `.env`
3. Restart: (block below)
4. Check: last log line reads `ready`
```

### 3. Spell out anything the reader could not reconstruct from sound

Proper nouns, package names, flags, file extensions, unusual identifiers. Write them in code formatting and, where they are new to the conversation, add a spelled or glossed form once.

Good: "Install `jsonwebtoken` (one word, no hyphens)."
Good: "The file is `setup.sh` (S-H, a shell script), not `setup.h`."

### 4. Avoid phonetic confusables, or disambiguate them

Prefer words and numbers that cannot be misheard or mis-subvocalised. Where a confusable is unavoidable, add the disambiguation.

- Numbers: write digits and add the word form for teen/ty pairs: `15 (fifteen)`, `50 (fifty)`.
- Letters: give a word anchor for spelled letters: `B as in bravo`.
- Words: replace `accept/except`, `affect/effect`, `then/than` with unambiguous phrasing where possible.

### 5. Repeat, do not refer back

Never "as I said", "the command above", "same as before", "that file". Repeat the item in full. Referring back requires the reader to reconstruct something they may not have retained.

Bad: "Run the same command as earlier."
Good:
```
npm test -- auth.spec.ts
```

### 6. Echo and confirm speech-to-text input, when the reader says they use it

If the reader has said their input arrives by speech-to-text, or asks for an echo, restate the interpreted command in writing before acting on anything consequential. Do not infer speech-to-text from homophone errors, missing punctuation or run-on sentences; a mis-typed message is interpreted silently, and a confirmation is asked for only where the action is consequential (conflict order: confirm possibly-unintended input).

Good: "I read that as: rename `config.js` to `config.old.js`. Reply `yes` to proceed or send the correction."

### 7. No audio-only cues

Never "listen for the beep", "you'll hear it finish", "wait for the sound." Every cue is visual and written: an exact string, a status line, a file that appears.

Bad: "Wait for the notification sound, then continue."
Good: "Wait until the terminal prints `done`. Then continue."

### 8. Expand every abbreviation and define every new term on first use

Abbreviations cannot be sounded out into meaning. Write the expansion once in brackets.

Good: "Set up **CI** (continuous integration, the automatic test runner) first."

### 9. Short sentences, one idea each

15 words or fewer. One idea per sentence. This is the same cap as `i-have-dyslexia` rule 1 and for the same reason: verbal working memory is the bottleneck whether the words arrive by eye or ear.

### 10. Written summary after any voice exchange

If any part of the session happened by voice, end the turn with a written block titled `Written summary:` containing every decision, command, and next step from that exchange.

## When to break the rules

Override the defaults when:

1. Reader asks to "explain" or "walk me through." Length grows. Chunking and spelling stay.
2. Destructive action ahead. Confirm in writing with a typed word. If the session is voice-only, do not accept a spoken confirmation for an irreversible action; ask for the typed word.
3. Reader explicitly prefers voice for a given exchange. Speak it, at reduced pace, one chunk at a time, and still write it (rule 1).
4. A rule fights the task. If the deliverable is a transcript or a quotation, reproduce it exactly; add the disambiguation as a separate note.
5. A rule fights the harness. Inside an agent harness, the system prompt outranks this skill. The constraint wins, the shape stays.

## Pre-send check

Before sending:

1. Is anything here only spoken? Write it.
2. Convert every sequence of 3 or more into a numbered vertical list.
3. Put every proper noun, package, flag, and extension in code formatting; spell or gloss each new one once.
4. Find every teen/ty number and add the word form. Find every confusable word pair and rephrase.
5. Replace every "above", "earlier", "same as", "that one" with the full item.
6. Replace every audio cue with a written, visual one.
7. Expand every abbreviation on first use.
8. If any voice exchange happened, add `Written summary:`.

Then verify: if the reader had heard none of this and could only read it, is anything missing?

If nothing is missing, send.

## Before and after

### Before

> (spoken) Right, so what you want to do is install the JWT package, then pop into the env file and change the port to fifty—sorry, fifteen hundred—then restart like before and just listen for the ready chime, and if you hear it you're good. Accept the prompt when it comes up.

### After

> **Written steps** (also spoken, one at a time, on request):
>
> 1. Install `jsonwebtoken` (one word, no hyphens):
>    ```
>    npm install jsonwebtoken
>    ```
> 2. Open `.env` (dot E-N-V, in the project root). Set:
>    ```
>    PORT=1500
>    ```
>    That is 1500 (fifteen hundred), not 50 (fifty).
> 3. Restart the server:
>    ```
>    npm run dev
>    ```
> 4. Wait until the terminal prints `ready on http://localhost:1500`. There is no sound cue; the printed line is the signal.
> 5. If a prompt appears asking `Continue? (y/n)`, type `y` and press Enter.
>
> Written summary: 1 package installed, `PORT` set to `1500` (fifteen hundred), server restarted. Done when the terminal prints `ready on http://localhost:1500`.

## On Hermes Agent

Invoke with `/i-have-apd`. Up to five skills stack in one message, for example `/i-have-apd /i-have-working-memory-differences`. The bundles in `skill-bundles/` load a set under one command. Each skill stays on until its own stop phrase.
