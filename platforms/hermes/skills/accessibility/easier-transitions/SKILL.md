---
name: easier-transitions
description: 'Presentation settings for transitions: changing topic or task without losing the thread. Starting set: Warn me before changing topic; Hold my unfinished thread. For a reader who says "I struggle switching between tasks". Chosen by the reader, not inferred, and not a diagnosis. Use only when the reader invokes /easier-transitions or asks for these settings; stays on until "stop easier transitions".'
version: 0.4.5
author: 'Accessibility skill pack contributors'
license: MIT
metadata:
  hermes:
    tags:
      - 'Accessibility'
      - 'Presentation'
      - 'Transitions'
      - 'What Would Make This Easier'
    category: accessibility
    related_skills:
      - 'needs-picker'
---

# easier-transitions

Transitions: changing topic or task without losing the thread.

These are settings the reader chose from the What Would Make This Easier picker, for this one area. They say nothing about the reader. Nothing here is a diagnosis and nothing is inferred.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop easier transitions" or "normal mode". Confirm in one line, then return to your default style.

If another output-shaping skill is also active, apply both. Where two rules conflict, follow the order at the end of the settings: what the reader can perceive, then what they can act on, then what they can understand, then the rest; sensory overload the reader reports is an access barrier, and where two of the reader's own settings conflict, ask rather than rank.

## The reader said

- I struggle switching between tasks

Any one of these is enough. The reader may also have picked this area directly.

## The settings

The starting set below is the picker's suggested starting points for this area, not everything it offers. Apply all of it unless the reader removes a line by naming it.

These are presentation settings I chose for myself. They describe how I would like information laid out, not anything about me. Do not infer a condition, a diagnosis or a capability from them, and do not mention them back to me unless I ask.

Limits of these preferences: they change only how you present information and work with me. They operate within my explicit instructions, the project instructions and the permission rules, and they never grant permission, approve an action or count as a confirmation. Never leave out errors, failures, warnings, decisions I need to make, approval requests or irreversible effects to satisfy a brevity or deferral preference. Keep code, commands, paths, numbers, links, citations and meaning exact.

TRANSITIONS
- Say before changing topic, and name what is being left.
- Park unfinished work with its exact resumption state and trigger.

If two of these ever pull against each other, prefer in this order: what I can perceive, then what I can act on, then what I can understand, then the rest. Sensory overload I report is an access barrier, not comfort. Where two of my own settings conflict, ask me which to follow rather than ranking them.

I can change any of this at any time. Ask me before assuming a setting is wrong; do not quietly drop one.

## Also available in this area

Not on by default. The reader turns one on by saying its label; say in one line that it is on.

- **One goal at a time.** One current goal, named at the top. Everything else is parked explicitly. Holds back: Parks anything that is not the current goal.
- **Offer a clean stopping point.** Name a clean stop point before long work begins, and what will be true there.
- **Never two things at once.** Never leave two items in progress at the same time.

## When it applies

Everything above applies always unless the reader says otherwise. The reader may declare a context in their own words: "work mode", "learning mode", "brainstorming", "I am stuck", "I am overloaded". A context is declared by the reader, never inferred from typing, message length, errors or the time of day. If the reader has set some of these to apply only in a context, follow what they said; if they have not, apply all of them.

## Pre-send check

Before sending, confirm each line of the starting set is honoured, that no error, failure, decision or approval request was dropped to satisfy one, and that nothing in the response names a condition or comments on the reader.

## On Hermes Agent

Invoke with `/easier-transitions`. Up to five skills stack in one message, for example `/easier-transitions /i-have-working-memory-differences`. The bundles in `skill-bundles/` load a set under one command. Each skill stays on until its own stop phrase.
