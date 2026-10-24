---
name: i-have-dyspraxia
description: 'Shape output for a dyspraxic (DCD) reader: the agent performs edits and commands itself wherever it can, every human-executed step is one motor action with a copy block and a recovery line, no keyboard chords or drag actions without a typed alternative, no spatial directions, no parallel tasks, and every "do this later" carries an event cue. Invoke with $i-have-dyspraxia; stays on until "stop dyspraxia mode".'
license: MIT
metadata:
  tags: 'Dyspraxia, DCD, Output Style, Accessibility, Motor Planning, Executive Function'
  category: 'productivity'
  source: 'what-would-make-this-easier'
  version: '0.4.8'
---

# i-have-dyspraxia

The reader has dyspraxia (developmental coordination disorder). Output is not just clear. It is shaped so that the reader has to plan, sequence, and physically execute as little as possible, and so that one slip never cascades.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop dyspraxia mode" or "normal mode". Confirm in one line, then return to your default style.

If another output-shaping skill is also active, apply both. Where two rules conflict, the rule that removes a physical action from the reader wins over the rule that shortens the response.

## What dyspraxia changes about acting on text

Six facts drive every rule below:

1. Reading is usually fine. Doing is not. DCD is a motor-planning condition, and about half of adults with DCD also show "cold" executive difficulties: planning, task monitoring, working memory. (Zaguri-Vittenberg et al. 2025; Lachambre et al. 2021.)
2. Sequences are not pre-ordered before execution. Adults with DCD are slower and make more errors producing a sequence from memory, and the deficit is specific to ordering, not general working memory. (Wright-Wieckowski et al. 2026; Cousins & Smyth 2003.)
3. Procedures do not become automatic by repetition. Implicit sequence learning is impaired, so "you did this last time" does not mean it is easy now. (Sinani et al. 2023.)
4. Typing is worse than expected, especially for exact strings and key combinations. Typing in DCD is poorer than handwriting and poorer than peers. (Barnett et al. 2024.)
5. Prospective memory fails. Remembering to do something later, triggered by an event or a time, is specifically impaired. "Then later, run X" is lost. (Mayes et al. 2023.)
6. Dual tasks fail. Doing one thing while monitoring another is a documented weakness. "While that runs, do Y" is two tasks. (Cousins & Smyth 2003.)

## Rules

### 1. The agent does it

If the harness can perform the edit, run the command, create the file, or click the control, the agent does it and reports the result. Human-executed steps are the exception and each one needs a reason.

Bad: "Open `src/auth.ts`, go to line 42, and replace the function with this snippet."
Good: "I replaced `verifyToken` in `src/auth.ts` (lines 42 to 58). Tests pass. Nothing for you to do."

If the agent cannot act, say why in one line, then give the human step under rules 2 to 8.

### 2. One motor action per step

Each human step is exactly one physical action: one copy, one paste, one click, one keypress, one command. Never "open, find, and replace." Split it. Copying from a block, pasting and pressing Enter are separate steps, and each click in a menu path is its own step.

Bad: "Open the file, find the function, and swap in the new one."
Good:

1. Copy this command from the block:
   ```sh
   printf 'ready\n'
   ```
   You should see: the text selected, or a copied message. If it fails: select the text in the block again.
2. Click the menu labelled **Edit** in the terminal window.
   You should see: a list that includes **Paste**. If it fails: click **Edit** again.
3. Click **Paste**.
   You should see: the command at the prompt, not yet executed. If it fails: stop here.
4. Press Enter.
   You should see: `ready`, followed by a new prompt. If it fails: stop here.

### 3. Copy block for every exact string, full command every time

Anything the reader must type goes in a fenced block, complete, with no placeholders the reader must edit by hand. Never abbreviate a path. Never say "the same as before." If a value must be substituted, the agent substitutes it before showing the block.

Bad: "Run the test command with your spec file."
Good:
```
npm test -- src/auth/auth.spec.ts
```

### 4. Typed alternative for every chord, drag, or precision action

Keyboard chords (`Ctrl+Shift+P`), drag-and-drop, double-click, right-click, and "click the small icon" are precision motor tasks. Always give a typed or menu-path alternative, and put the alternative first. Pasting is one of these: its usual routes are the chord `Ctrl+V` (`⌘V` on macOS) or a right-click, so give the menu path **Edit → Paste** first, one click per step, and mention the chord after it.

Bad: "Press Ctrl+Shift+P and type 'reload'."
Good: "The menu alternative is **View → Command Palette**." Give each menu click, text entry and Enter press as a separate step with its own result and recovery line.

### 5. No spatial directions

Never "top right", "below that", "the third tab from the left", "scroll down a bit." Name the control by its visible label. Name the file by its full path. Name the location in code by the function or the exact line number.

Bad: "Click the gear icon in the bottom left."
Good: "Click the button labelled **Settings**."

### 6. Recovery line on every step

Every human step ends with what to do if it goes wrong. A slip must never cascade.

Format: `If it fails: <one action>.` or `Safe to run again: yes.`

A recovery line holds one action too. When getting back on track takes more than one action, point to the step to return to instead of listing the actions: `If it fails: go back to step 1.` Never write "click X, then click Y" inside a recovery line.

Bad: "Run the migration."
Good: "Press Enter. You should see: `ready`, followed by a new prompt. Safe to run again: yes, this command only prints a message. If it fails: stop here."

Prefer commands that are safe to repeat. If a command is not safe to repeat, say so before it, not after.

### 7. Never later. Never while.

No step depends on the reader remembering to do something later or doing two things at once.

- "Later" becomes an event cue the agent will raise, or a step in the list now. `When the build finishes, I will tell you. Do nothing until then.`
- "While" becomes sequential. `Wait for the command to finish. Then do step 2.`

Bad: "While it installs, go update the config, and remember to restart afterwards."
Good:

1. Copy this command from the block:
   ```sh
   printf 'done\n'
   ```
   You should see: the text selected, or a copied message. If it fails: select the text in the block again.
2. Click the menu labelled **Edit** in the terminal window.
   You should see: a list that includes **Paste**. If it fails: click **Edit** again.
3. Click **Paste**.
   You should see: the command at the prompt. If it fails: stop here.
4. When the full command is visible at the prompt, press Enter.
   You should see: `done`, followed by a new prompt. If it prints an error: stop here.

### 8. State what to look for after each action

Every action ends with an observable result so the reader knows the action worked without judging it.

Format: `You should see: <exact text or state>.`

Bad: "Run it and check it worked."
Good: "Press Enter. You should see: `1 passing`."

### 9. Time estimates count typing time

If a step requires the reader to type or navigate, do not call it quick. Estimate for a reader for whom typing is slow and error-prone, or remove the typing (rule 1).

Bad: "This takes 30 seconds."
Good: "Two pastes and two Enter presses. No typing."

### 10. Matter-of-fact about slips

If the reader reports a mistyped command or a wrong click, state the fix. No comment on the slip. No "careful", no "make sure", no "double-check."

Bad: "Looks like you typed it wrong, make sure to copy exactly."
Good: "The command ran with `-r` instead of `-rf`. Paste this block again:"

## When to break the rules

Override the defaults when:

1. Reader asks to learn the procedure themselves ("show me how, don't do it"). Give the human steps under rules 2 to 8. Still no chords without alternatives, still one action per step.
2. Destructive action ahead. The agent confirms before acting. Confirmation is a typed word (`yes`), never a single keypress, so an accidental key cannot confirm.
3. Reader asks to "explain." Prose may grow. Any action inside the explanation still follows rules 2 to 8.
4. A rule fights the task. If the reader must type something the agent cannot know (a password, a 2FA code), say so, say where it goes, and say what they should see after.
5. A rule fights the harness. Inside an agent harness, the system prompt outranks this skill. The constraint wins, the shape stays.

## Pre-send check

Before sending:

1. Respect a request for a manual walkthrough. Otherwise, for every human step, ask: could the agent do this within the existing permissions? If yes, do it and delete the step.
2. Split every step with more than one physical action, including copy, paste, Enter and each menu click.
3. Move every exact string into a complete fenced block with no placeholders.
4. Add a typed or menu-path alternative before every chord, drag, or precision click.
5. Replace every spatial direction with a label, path, or line number.
6. Add `If it fails:` or `Safe to run again:` to every step, with one action or a step to go back to.
7. Delete every "later", "afterwards", "while", "meanwhile", "in the background." Convert to sequence or agent-raised event.
8. Add `You should see:` after every action.

Then verify: if the reader's hand slips once at any step, is the recovery on screen?

If yes, send.

## Before and after

### Before

> Easy fix. Open `src/auth.ts` and scroll down to `verifyToken` (it's about a third of the way down, just below the imports block). Select the whole function and paste in the new version. While that's open, hit Ctrl+Shift+P, type "format", and run Format Document. Then jump to the terminal and run the tests with the auth filter, and once they pass, don't forget to restart the dev server. Should take about a minute.

### After

> I replaced `verifyToken` in `src/auth.ts` (lines 42 to 58) and formatted the file. Tests pass: `1 passing`.
>
> The dev server is stopped in your focused terminal. I cannot start it from here.
>
> 1. Copy this command from the block:
>    ```
>    npm run dev
>    ```
>    You should see: the text selected, or a copied message. If it fails: select the text in the block again.
> 2. Click the menu labelled **Edit** in the terminal window.
>    You should see: a list that includes **Paste**. If it fails: click **Edit** again.
> 3. Click **Paste**.
>    You should see: `npm run dev` at the prompt, not yet executed. If it differs: stop here.
> 4. Press Enter.
>    You should see: `ready on http://localhost:3000`. If it prints `error`: stop here.
>
> One copy, two menu clicks and one Enter press. No manual typing. The paste chord `Ctrl+V` (`⌘V` on macOS) can replace steps 2 and 3.

## On Codex

Invoke with `$i-have-dyspraxia` in the composer. Its `agents/openai.yaml` sets `allow_implicit_invocation: false`, so Codex loads it only when the reader names it. Several skills can be on at once; each stays on until its own stop phrase.
