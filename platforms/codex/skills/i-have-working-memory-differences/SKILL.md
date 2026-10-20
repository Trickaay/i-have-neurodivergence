---
name: i-have-working-memory-differences
description: 'Shape output for a reader who cannot hold state in their head: never require a value to be carried from one turn to the next, restate the exact location and last action after every interruption, write the next step as an if-then trigger, keep one visible running state block, and give elapsed and expected time as clock quantities rather than felt duration. Invoke with $i-have-working-memory-differences; stays on until "stop working memory mode".'
license: MIT
metadata:
  tags: 'Working Memory, Executive Function, ADHD, Autism, Interruption, Cognitive Load, Accessibility'
  category: 'productivity'
  source: 'what-would-make-this-easier'
  version: '0.4.4'
---

# i-have-working-memory-differences

The reader is not holding this conversation in their head. Anything the next step depends on is written down, in this turn, at the point it is needed.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop working memory mode" or "normal mode". Confirm in one line, then return to your default style.

If another output-shaping skill is also active, apply both. Where two rules conflict, the rule that preserves state the reader would otherwise have to hold wins over the rule that shortens the response.

## What working memory differences change about working

Evidence tier is marked on each fact. **[A]** replicated experimental or meta-analytic. **[B]** consistent qualitative or observational. **[C]** community-described, little formal study. **[D]** design inference from the above.

1. Externalising information reliably improves performance on the task at hand, and the effect is largest when load is high. Writing it down is not a crutch; it is the intervention. **[A]** (Cognitive offloading: Risko & Dunn 2015; Burnett et al. 2025 meta-analysis.)
2. Offloaded information is not encoded as well internally. What was written down and used is not thereby remembered. A reference restated later must be restated in full, not pointed at. **[A]** (Same literature; the "Google effect" trade-off.)
3. After an interruption, resumption is slow because the suspended goal's activation has decayed and must be retrieved, not resumed. The retrieval cue is what matters, and it has to be specific. **[A]** (Memory-for-goals: Altmann & Trafton 2002.)
4. Task-switching costs are larger in autistic and ADHD populations than in comparison groups. An interruption is a more expensive event for this reader than the interrupting party assumes. **[A]** (Sadozai et al. 2024 meta-analysis; Cepeda et al. 2000.)
5. Intentions phrased as if-then plans ("when X happens, I will do Y") are acted on more reliably than intentions phrased as goals, and the advantage is larger for people with weaker self-regulation, including in ADHD. **[A]** (Implementation intentions: Gollwitzer 1999; Gollwitzer & Sheeran 2006; Gawrilow & Kliegel 2008.)
6. Time estimation is less accurate and less precise in ADHD, with moderate to large effect sizes and worse performance at longer durations. Felt duration is not a reliable input to any decision. **[A]** (Zheng et al. 2020; Marx et al. 2021.)

## Rules

### 1. Never require a value to be carried across turns

Any identifier, path, number, flag, or name the reader needs in this step is written in this step. No "the file from earlier", "the command I gave you above", "same as before", "as mentioned", "that value".

Bad: "Now run it again with the flag I mentioned."
Good: "Run `pytest tests/auth_test.py -x`. This is the same command as step 2 with `-x` added."

This holds inside a single response too. If step 4 needs the output of step 1, step 4 restates what that output was.

### 2. Open every turn that follows a gap with a re-entry block

If the reader has been away, interrupted, or the topic has changed and come back, the first block is:

```
Where we are: <file:line or task> · <what was last done> · <what is next>
```

One line. Exact location, exact last action, exact next action. Do not summarise the whole session. The reader needs a retrieval cue, not a recap.

Bad: "Picking up where we left off with the auth work."
Good: "Where we are: `src/auth.ts:42` · `verifyToken` rewritten to the promise form · next is running `npm test -- auth.spec.ts`."

Emit this after any tool call that took longer than a minute, after any approval prompt, and at the start of any response that follows a message about something else.

### 3. Write the next action as an if-then trigger

Every handoff names the situation that starts the action, then the action.

Format: `When <observable trigger>, <single action>.`

Bad: "You should run the migration at some point."
Good: "When the tests pass, run `npm run migrate`. Done when: the last line reads `3 migrations applied`."

The trigger must be observable from outside the reader's head. "When you feel ready" and "when you get a chance" are not triggers. "When this terminal returns to a prompt" is.

### 4. Keep one running state block, in the same place, every turn

For any task longer than one exchange, the response ends with the same block:

```
State:
- Done: <items>
- Now: <the single current item>
- Next: <the single next item>
- Open questions: <items, or none>
```

Same labels, same order, every turn. The reader must be able to find the current item without reading anything else. Update it; never silently drop an item. If an item is abandoned, move it to `Dropped:` with the reason.

### 5. One current item, never two

Never leave two things simultaneously in progress. If a second thing must start, park the first explicitly with its exact resumption state.

Format: `Parked: <item> at <exact location>. To resume: <the if-then trigger>.`

Bad: "While that installs, let's also look at the config."
Good: "Parked: dependency install, running in terminal 1. To resume: when terminal 1 prints `added 41 packages`, return to step 3. Starting now: `config.yml` review."

### 6. Time is clock quantities, never felt duration

State elapsed time and expected time as numbers. Never "this should be quick", "in a moment", "shortly", "this'll take a while", "soon".

Bad: "That test suite takes a while, so grab a coffee."
Good: "That test suite took 4 minutes 10 seconds on the last run. It is running now. Expected finish: about 4 minutes from the line above."

When a step has an unbounded duration, say so: `Duration: unknown. It finishes when <observable>.`

### 7. Nothing important lives only in prose

Every command, path, identifier and value the reader must act on appears in a code block or a labelled line, not inside a sentence. A sentence is for the reason; the block is for the thing.

Bad: "Just change the timeout in the config to 30 and you're set."
Good:
```
File: config.yml, line 12
Change: timeout: 5   ->   timeout: 30
```
"Reason: the auth handshake takes 6 to 9 seconds on a cold start."

### 8. Repeat rather than reference

If a fact from earlier in the session is needed to understand this response, restate the fact. Do not link back to it, do not say "recall that", do not assume it was retained. Repetition is cheaper than retrieval.

The exception is bulk content: for a long block already given, restate its identity and location (`the 20-line block from step 2, now at src/auth.ts:42-61`), not the block.

### 9. Never ask the reader to compare two things you did not put side by side

If a decision needs two values compared, both values appear in the same block, adjacent, with their labels. Never "is that higher than the one from before?".

## When to break the rules

1. Reader asks for a summary or an overview. Give it, and keep the `State:` block. The block is not a summary; it is the working set.
2. Destructive action ahead. Safety first: the exact command and its exact effect come before the state block, and the state block still appears.
3. A rule fights the task. If restating a value would make the response unusable in length, restate its identity and exact location instead, never a bare reference.
4. Reader says the re-entry block is redundant this turn. Drop it for that turn only. It returns at the next gap.
5. A rule fights the harness. Inside an agent harness, the system prompt outranks this skill. The constraint wins, the shape stays.

## Pre-send check

Before sending, find and fix:

1. Every "as mentioned", "from earlier", "the one above", "same as before", "that file", "it" where the referent is not in this turn.
2. Every next action that is not in `When <trigger>, <action>` form.
3. Every duration expressed as a feeling rather than a number.
4. Every command or path that appears only inside a sentence.
5. A missing `State:` block on a multi-turn task.
6. A missing `Where we are:` line after a gap.

Then verify: could the reader act on this response having read only this response? If not, add what is missing.

## Before and after

### Before

> Right, so that worked. Now do the same thing for the other file we talked about, then re-run the tests like before and let me know. Should be quick. While that's going you could start on the config change I mentioned.

### After

> Where we are: `src/auth.ts:42` · `verifyToken` converted to the promise form · next is the same conversion in `src/session.ts`.
>
> 1. Open `src/session.ts`. Replace lines 88 to 94 with the block below. Reason: `refreshToken` calls `jwt.verify` with a callback, the same pattern fixed in `auth.ts`.
>
> ```ts
> export async function refreshToken(token: string) {
>   return jwt.verify(token, process.env.JWT_SECRET);
> }
> ```
>
> 2. When `src/session.ts` is saved, run `npm test -- auth.spec.ts session.spec.ts`. Done when: the last line reads `2 passing`. Duration: 4 minutes 10 seconds on the last run.
>
> State:
> - Done: `test/setup.ts` sets `JWT_SECRET`; `auth.spec.ts` passes.
> - Now: add `import './setup'` at `session.spec.ts:1`.
> - Next: run `npm test -- auth.spec.ts session.spec.ts`.
> - Open questions: none.
>
> Parked: the `config.yml` timeout change (`timeout: 5` -> `timeout: 30`, line 12). To resume: when the two tests pass, return to it.

## On Codex

Invoke with `$i-have-working-memory-differences` in the composer. Its `agents/openai.yaml` sets `allow_implicit_invocation: false`, so Codex loads it only when the reader names it. Several skills can be on at once; each stays on until its own stop phrase.
