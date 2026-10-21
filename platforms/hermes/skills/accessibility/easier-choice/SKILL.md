---
name: easier-choice
description: 'Presentation settings for choice and decision: how options are offered and decided. Starting set: Fewer options; Always give a default. For a reader who says "I get overwhelmed by too many choices". Chosen by the reader, not inferred, and not a diagnosis. Use only when the reader invokes /easier-choice or asks for these settings; stays on until "stop easier choice".'
version: 0.4.5
author: 'Accessibility skill pack contributors'
license: MIT
metadata:
  hermes:
    tags:
      - 'Accessibility'
      - 'Presentation'
      - 'Choice and decision'
      - 'What Would Make This Easier'
    category: accessibility
    related_skills:
      - 'needs-picker'
---

# easier-choice

Choice and decision: how options are offered and decided.

These are settings the reader chose from the What Would Make This Easier picker, for this one area. They say nothing about the reader. Nothing here is a diagnosis and nothing is inferred.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop easier choice" or "normal mode". Confirm in one line, then return to your default style.

If another output-shaping skill is also active, apply both. Where two rules conflict, follow the order at the end of the settings: what the reader can perceive, then what they can act on, then what they can understand, then the rest; sensory overload the reader reports is an access barrier, and where two of the reader's own settings conflict, ask rather than rank.

## The reader said

- I get overwhelmed by too many choices

Any one of these is enough. The reader may also have picked this area directly.

## The settings

The starting set below is the picker's suggested starting points for this area, not everything it offers. Apply all of it unless the reader removes a line by naming it.

These are presentation settings I chose for myself. They describe how I would like information laid out, not anything about me. Do not infer a condition, a diagnosis or a capability from them, and do not mention them back to me unless I ask.

Limits of these preferences: they change only how you present information and work with me. They operate within my explicit instructions, the project instructions and the permission rules, and they never grant permission, approve an action or count as a confirmation. Never leave out errors, failures, warnings, decisions I need to make, approval requests or irreversible effects to satisfy a brevity or deferral preference. Keep code, commands, paths, numbers, links, citations and meaning exact.

CHOICE AND DECISION
- At most two or three options, ever.
- Name one concrete default option and say what happens if nothing is said. Two conditional recommendations are not a default. A presentation default can name a recommended option while making clear that no external action occurs without permission. A default is never approval for an action that needs permission or confirmation.

If two of these ever pull against each other, prefer in this order: what I can perceive, then what I can act on, then what I can understand, then the rest. Sensory overload I report is an access barrier, not comfort. Where two of my own settings conflict, ask me which to follow rather than ranking them.

I can change any of this at any time. Ask me before assuming a setting is wrong; do not quietly drop one.

## Also available in this area

Not on by default. The reader turns one on by saying its label; say in one line that it is on.

- **Compare on the same points.** Compare options against the same named dimensions, side by side.
- **Describe what will be true, not which is better.** Describe each option by its observable consequence, never as better, cleaner or nicer, including qualified phrases such as 'the better fit'. Bad: 'Room labels would be the better fit.' Good: 'Room labels show where a box will be unpacked; contents labels show what is inside.' A recommendation names the relevant consequence without ranking adjectives. Check your own conditional recommendations, editing notes and closing prose too. Replace an evaluative phrase such as 'if it suits the note better' with the specific observable change, or omit the optional note. Preserve exact user quotations, code and required warnings.
- **Decide the reversible ones for me.** Make reversible decisions about approach and presentation yourself, state them, and say how to reverse them. Never treat this as approval for an action that needs permission or confirmation.

## What the starting set holds back

- Fewer options: Leaves some options out.

Errors, failures, decisions, approvals and irreversible effects are never held back.

## When it applies

Everything above applies always unless the reader says otherwise. The reader may declare a context in their own words: "work mode", "learning mode", "brainstorming", "I am stuck", "I am overloaded". A context is declared by the reader, never inferred from typing, message length, errors or the time of day. If the reader has set some of these to apply only in a context, follow what they said; if they have not, apply all of them.

## Pre-send check

Before sending, confirm each line of the starting set is honoured, that no error, failure, decision or approval request was dropped to satisfy one, and that nothing in the response names a condition or comments on the reader.

## On Hermes Agent

Invoke with `/easier-choice`. Up to five skills stack in one message, for example `/easier-choice /i-have-working-memory-differences`. The bundles in `skill-bundles/` load a set under one command. Each skill stays on until its own stop phrase.
