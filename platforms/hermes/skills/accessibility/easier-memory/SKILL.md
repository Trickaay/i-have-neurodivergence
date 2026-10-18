---
name: easier-memory
description: 'Presentation settings for memory: not having to hold things in your head between turns. Starting set: Repeat the current goal; Help me pick up where I was; Keep a running state block; Repeat important things. For a reader who says "I need important information repeated" / "I forget where I was after interruptions". Chosen by the reader, not inferred, and not a diagnosis. Use only when the reader invokes /easier-memory or asks for these settings; stays on until "stop easier memory".'
version: 0.4.0
author: 'Accessibility skill pack contributors'
license: MIT
metadata:
  hermes:
    tags:
      - 'Accessibility'
      - 'Presentation'
      - 'Memory'
      - 'What Would Make This Easier'
    category: accessibility
    related_skills:
      - 'needs-picker'
---

# easier-memory

Memory: not having to hold things in your head between turns.

These are settings the reader chose from the What Would Make This Easier picker, for this one area. They say nothing about the reader. Nothing here is a diagnosis and nothing is inferred.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop easier memory" or "normal mode". Confirm in one line, then return to your default style.

If another output-shaping skill is also active, apply both. Where two rules conflict, follow the order at the end of the settings: what the reader can perceive, then what they can act on, then what they can understand, then the rest; sensory overload the reader reports is an access barrier, and where two of the reader's own settings conflict, ask rather than rank.

## The reader said

- I need important information repeated
- I forget where I was after interruptions

Any one of these is enough. The reader may also have picked this area directly.

## The settings

The starting set below is the picker's suggested starting points for this area, not everything it offers. Apply all of it unless the reader removes a line by naming it.

These are presentation settings I chose for myself. They describe how I would like information laid out, not anything about me. Do not infer a condition, a diagnosis or a capability from them, and do not mention them back to me unless I ask.

Limits of these preferences: they change only how you present information and work with me. They operate within my explicit instructions, the project instructions and the permission rules, and they never grant permission, approve an action or count as a confirmation. Never leave out errors, failures, warnings, decisions I need to make, approval requests or irreversible effects to satisfy a brevity or deferral preference. Keep code, commands, paths, numbers, links, citations and meaning exact.

ATTENTION
- Restate the current goal at the start of every response.
- After any gap, open with location, last action, next action, on one line.

MEMORY
- Maintain a `State:` block with done, now, next, open — same place, every turn.
- Restate a fact rather than referring back to it. Outside a practice I opted into, repetition over retrieval.

If two of these ever pull against each other, prefer in this order: what I can perceive, then what I can act on, then what I can understand, then the rest. Sensory overload I report is an access barrier, not comfort. Where two of my own settings conflict, ask me which to follow rather than ranking them.

I can change any of this at any time. Ask me before assuming a setting is wrong; do not quietly drop one.

## Also available in this area

Not on by default. The reader turns one on by saying its label; say in one line that it is on.

- **Recap where we are.** One-line recap at the start of any response following a gap.
- **Never make me remember a value.** Restate every path, identifier, number and command at the point of use.
- **Mark checkpoints.** Mark a resumable checkpoint after each step, naming the exact state.
- **Hold my unfinished thread.** Park unfinished work with its exact resumption state and trigger.

## When it applies

Everything above applies always unless the reader says otherwise. The reader may declare a context in their own words: "work mode", "learning mode", "brainstorming", "I am stuck", "I am overloaded". A context is declared by the reader, never inferred from typing, message length, errors or the time of day. If the reader has set some of these to apply only in a context, follow what they said; if they have not, apply all of them.

## Pre-send check

Before sending, confirm each line of the starting set is honoured, that no error, failure, decision or approval request was dropped to satisfy one, and that nothing in the response names a condition or comments on the reader.

## On Hermes Agent

Invoke with `/easier-memory`. Up to five skills stack in one message, for example `/easier-memory /i-have-working-memory-differences`. The bundles in `skill-bundles/` load a set under one command. Each skill stays on until its own stop phrase.
