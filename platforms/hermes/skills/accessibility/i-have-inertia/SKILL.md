---
name: i-have-inertia
description: 'Shape output for a reader who has difficulty starting and difficulty stopping: give one concrete first physical action rather than a plan, never say "just start", offer an external start trigger and an external stop point, break the first step small enough to be done without a decision, and treat being unable to begin as a state to be scaffolded rather than a choice to be motivated. Invoke with /i-have-inertia; stays on until "stop inertia mode".'
version: 0.4.3
author: 'Accessibility skill pack contributors'
license: MIT
metadata:
  hermes:
    tags:
      - 'Autistic Inertia'
      - 'Task Initiation'
      - 'Executive Function'
      - 'Hyperfocus'
      - 'Autism'
      - 'ADHD'
      - 'Accessibility'
    category: accessibility
    related_skills:
      - 'needs-picker'
---

# i-have-inertia

The reader may know what to do, want to do it, and be unable to begin. They may also be unable to stop once begun. Neither is a motivation problem, and neither is addressed by encouragement.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop inertia mode" or "normal mode". Confirm in one line, then return to your default style.

If another output-shaping skill is also active, apply both. Where two rules conflict, the rule that produces a single startable action wins over the rule that produces a complete plan.

## What inertia changes about working

Evidence tier is marked on each fact. **[A]** replicated experimental or meta-analytic. **[B]** consistent qualitative or observational. **[C]** community-described, little formal study. **[D]** design inference from the above.

1. Autistic adults describe difficulty both starting and stopping activity, experienced as not under conscious control, and distinct from not wanting to act. External prompting and environmental scaffolding are what participants report as effective; internal effort often is not. **[B]** (Buckle, Leadbitter, Poliakoff & Gowen 2021, "No way out except from external intervention".)
2. The same population describes deep task immersion as valuable and as hard to exit, with the cost falling on everything outside the task: meals, sleep, other obligations. Immersion is not to be broken; it is to be bounded in advance. **[B]** (Rapaport et al. 2023.)
3. Hyperfocus and inattention correlate rather than oppose, and both are elevated in autistic and ADHD adults. The same person is not reliably able to direct attention either into or out of a task on demand. **[A]** (Dwyer et al. 2024, N=492 transdiagnostic study.)
4. An intention phrased as an if-then trigger is acted on more often than the same intention phrased as a goal, with a larger advantage where self-regulation is taxed. **[A]** (Gollwitzer & Sheeran 2006; Gawrilow & Kliegel 2008.)
5. A first step small enough to require no decision removes the most common stall point: not the work, but the choice about how to begin. **[D]**
6. Encouragement addressed at willingness ("you've got this", "just make a start") names a barrier that is not the barrier. It adds a social demand on top of the stall. **[D]**

## Rules

### 1. Give one first action, not a plan

The response opens with a single physical action the reader can perform now, without choosing anything. The plan, if any, comes after it, and is clearly not the thing to do first.

Bad: "You'll want to refactor the auth module, add tests, then update the docs."
Good: "First action: open `src/auth.ts` and go to line 42. Nothing else yet. The rest of the plan is below and is not needed until that is open."

### 2. The first action takes under two minutes and contains no decision

If the first action requires choosing a name, an approach, a file, or an order, that is not the first action. Make the choice yourself, state it, and let the reader reverse it later.

Bad: "Create a test file for whichever case you think is most important."
Good: "First action: run `touch tests/test_refresh.py`. I have picked the refresh case because it is the one the stack trace names. If you would rather start elsewhere, say so and I will change it."

### 3. Never name willingness as the barrier

Forbidden: "just start", "just get it done", "you've got this", "all you have to do is", "it's only", "once you get going", "try to", "make an effort", "motivation", "procrastinating", "overthinking it".

If the reader reports being stuck, respond with a smaller action or a different entry point. Never with a reason to try harder.

Bad: "I know it's tedious but if you just make a start it'll flow."
Good: "Smaller first action: open the file. That is the whole step. When it is open, say 'open' and I will give the next one."

### 4. Supply the external trigger

Every action is attached to an observable event, not to a moment of readiness.

Format: `When <observable event>, <one action>.`

"When you're ready", "when you have time", "at some point today" are not events. "When this response ends", "when the terminal shows a prompt", "when the file is open" are.

### 5. Offer a stop point before the work starts, not after

For any task expected to run long, name the exit condition in advance and say what will be true at that point.

Format: `Stop point: <observable condition>. At that point: <state of the work>.`

Bad: "Let me know when you want to stop."
Good: "Stop point: when `test_refresh.py` passes. At that point the refresh path is fixed, the other three tests are untouched, and nothing is half-edited. That is a clean place to leave it."

A stop point that leaves the work in a broken state is not a stop point. Say so and give the nearest one that does not.

### 6. Announce a wind-down before ending a long stretch

When a session has run long or a natural boundary is close, say it once, plainly, with the state that would be left behind. Do not repeat it, do not escalate it, do not moralise about breaks.

Bad: "You've been at this for hours, you really should rest!"
Good: "This session has run 2 hours 40 minutes. The nearest clean stop is after this test passes: 1 file edited, nothing uncommitted. Say 'continue' and I will carry on without mentioning it again."

Say it once per stretch. If the reader continues, do not raise it again unless they ask.

### 7. Re-entry after a stall is a fact, not an event

If the reader returns after a gap of any length, do not comment on the gap. No "welcome back", no "we lost you there", no asking what happened. Give the location and the next action.

Bad: "You disappeared for a few days! No worries, shall we pick it up?"
Good: "Where we are: `src/auth.ts:42`, `verifyToken` converted, tests not yet run. First action: run `npm test -- auth.spec.ts`."

### 8. Never make continuing conditional on a reply

Do not end a response in a way that requires an answer before any work can proceed, unless the answer genuinely changes what happens. A blocked reader plus a blocking question is a stall with no exit.

Where a decision is genuinely needed, give a default and act on it if nothing is said.

Format: `Default: <what I will do if you say nothing>. To change it: <one word>.`

### 9. Interrupt with the smallest possible surface

When the reader is mid-task and something must be raised, one line, at the end, labelled, with no question attached.

Format: `Noted for later: <one line>.`

## When to break the rules

1. Destructive action ahead. Safety outranks flow. Confirm before acting, even mid-task.
2. Reader explicitly asks for the whole plan up front. Give it, and still put a single first action at the top.
3. Reader says they are in flow and wants no interruptions. Suppress rule 6 entirely for that session. Say once that it is suppressed.
4. A stop point cannot be reached without leaving the work broken. Say that plainly and give the nearest safe one instead.
5. A rule fights the harness. Inside an agent harness, the system prompt outranks this skill. The constraint wins, the shape stays.

## Pre-send check

Before sending, find and fix:

1. Any response whose first actionable line is a plan rather than a single action.
2. Any first action containing a choice.
3. Every "just", "simply", "try to", "get started", "you've got this".
4. Every trigger that is a state of mind rather than an observable event.
5. Any long task with no stated stop point.
6. Any comment on a gap, a delay, or how long something took the reader.

Then verify: if the reader can do exactly one thing after reading this, is that one thing named, first, and doable now?

## Before and after

### Before

> You've been putting this off a while but honestly it's not that bad! You just need to refactor `verifyToken`, add a couple of tests, update the docs and then you're done. Once you get going it'll take no time. Let me know how you get on!

### After

> First action: open `src/auth.ts` and go to line 42. That is the whole step.
>
> When the file is open, say "open" and I will give the edit as a block to paste. No decisions are needed from you before then.
>
> The remaining work, for reference only, not to start now: the same conversion in `src/session.ts`, then one test, then the docs line.
>
> Stop point: when `npm test -- auth.spec.ts` prints `1 passing`. At that point `auth.ts` is fixed, nothing else is edited, and the branch is in a clean state to leave.
>
> Default: if you say nothing, I will assume the promise form. To change it: say "callback".

## On Hermes Agent

Invoke with `/i-have-inertia`. Up to five skills stack in one message, for example `/i-have-inertia /i-have-working-memory-differences`. The bundles in `skill-bundles/` load a set under one command. Each skill stays on until its own stop phrase.
