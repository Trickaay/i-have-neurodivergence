---
name: easier-pacing
description: 'Presentation settings for pacing: time, speed, confirmation, and how much is asked at once. Starting set: One instruction at a time; No time pressure; Tell me what it will cost first; Smallest useful version first. For a reader who says "I need more time to process" / "I run out of energy before the task does". Chosen by the reader, not inferred, and not a diagnosis. Use only when the reader invokes /easier-pacing or asks for these settings; stays on until "stop easier pacing".'
disable-model-invocation: true
license: MIT
metadata:
  tags: 'Accessibility, Presentation, Pacing, What Would Make This Easier'
  category: 'productivity'
  source: 'what-would-make-this-easier'
  version: '0.4.6'
---

# easier-pacing

Pacing: time, speed, confirmation, and how much is asked at once.

These are settings the reader chose from the What Would Make This Easier picker, for this one area. They say nothing about the reader. Nothing here is a diagnosis and nothing is inferred.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop easier pacing" or "normal mode". Confirm in one line, then return to your default style.

If another output-shaping skill is also active, apply both. Where two rules conflict, follow the order at the end of the settings: what the reader can perceive, then what they can act on, then what they can understand, then the rest; sensory overload the reader reports is an access barrier, and where two of the reader's own settings conflict, ask rather than rank.

## The reader said

- I need more time to process
- I run out of energy before the task does

Any one of these is enough. The reader may also have picked this area directly.

## The settings

The starting set below is the picker's suggested starting points for this area, not everything it offers. Apply all of it unless the reader removes a line by naming it.

These are presentation settings I chose for myself. They describe how I would like information laid out, not anything about me. Do not infer a condition, a diagnosis or a capability from them, and do not mention them back to me unless I ask.

Limits of these preferences: they change only how you present information and work with me. They operate within my explicit instructions, the project instructions and the permission rules, and they never grant permission, approve an action or count as a confirmation. Never leave out errors, failures, warnings, decisions I need to make, approval requests or irreversible effects to satisfy a brevity or deferral preference. Keep code, commands, paths, numbers, links, citations and meaning exact.

ATTENTION
- Give one instruction, then stop and wait for it to be done.

PACING
- No urgency words. No deadline that is not real and sourced.
- State steps, decisions required, and minutes, before starting.
- Offer the smallest version that actually works before the full one.

If two of these ever pull against each other, prefer in this order: what I can perceive, then what I can act on, then what I can understand, then the rest. Sensory overload I report is an access barrier, not comfort. Where two of my own settings conflict, ask me which to follow rather than ranking them.

I can change any of this at any time. Ask me before assuming a setting is wrong; do not quietly drop one.

## Also available in this area

Not on by default. The reader turns one on by saying its label; say in one line that it is on.

- **Least first, more on request.** Give the minimum that answers it. Offer depth as a named next step, do not include it. Holds back: Holds detail back until you ask for it.
- **Fewer options.** At most two or three options, ever. Holds back: Leaves some options out.
- **Offer a clean stopping point.** Name a clean stop point before long work begins, and what will be true there.
- **Confirm before each step.** Wait for a typed confirmation before each irreversible step. A confirmation covers only the step it was given for; an earlier or remembered 'yes', a default, or this setting itself is not confirmation.
- **Times as numbers.** State durations as numbers. Never 'quick', 'shortly' or 'a while'.
- **One word to shorten everything.** Honour a single word that reduces any answer to its shortest form.

## What the starting set holds back

- One instruction at a time: Holds the next instruction back until this one is done.
- Smallest useful version first: Offers a smaller piece of work before the whole one.

Errors, failures, decisions, approvals and irreversible effects are never held back.

## When it applies

Everything above applies always unless the reader says otherwise. The reader may declare a context in their own words: "work mode", "learning mode", "brainstorming", "I am stuck", "I am overloaded". A context is declared by the reader, never inferred from typing, message length, errors or the time of day. If the reader has set some of these to apply only in a context, follow what they said; if they have not, apply all of them.

## Pre-send check

Before sending, confirm each line of the starting set is honoured, that no error, failure, decision or approval request was dropped to satisfy one, and that nothing in the response names a condition or comments on the reader.

## On Claude Code

Invoke with `/easier-pacing`. The skill is marked `disable-model-invocation`, so it loads only when the reader types it. Several skills can be on at once; each stays on until its own stop phrase.
