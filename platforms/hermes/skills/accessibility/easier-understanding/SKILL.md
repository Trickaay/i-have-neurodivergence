---
name: easier-understanding
description: 'Presentation settings for understanding: making sense of what is said: wording, terms, examples, implied meaning. Starting set: Exact, literal wording; One name per thing; Summary first, detail underneath; Number and order the steps; Examples from a subject I name; Help me understand the wording. For a reader who says "I prefer exact / literal wording" / "I need to see the overall structure first" / "The wording is hard to follow even when I know the subject" / "Examples from a subject I already know help me". Chosen by the reader, not inferred, and not a diagnosis. Use only when the reader invokes /easier-understanding or asks for these settings; stays on until "stop easier understanding".'
version: 0.4.3
author: 'Accessibility skill pack contributors'
license: MIT
metadata:
  hermes:
    tags:
      - 'Accessibility'
      - 'Presentation'
      - 'Understanding'
      - 'What Would Make This Easier'
    category: accessibility
    related_skills:
      - 'needs-picker'
---

# easier-understanding

Understanding: making sense of what is said: wording, terms, examples, implied meaning.

These are settings the reader chose from the What Would Make This Easier picker, for this one area. They say nothing about the reader. Nothing here is a diagnosis and nothing is inferred.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop easier understanding" or "normal mode". Confirm in one line, then return to your default style.

If another output-shaping skill is also active, apply both. Where two rules conflict, follow the order at the end of the settings: what the reader can perceive, then what they can act on, then what they can understand, then the rest; sensory overload the reader reports is an access barrier, and where two of the reader's own settings conflict, ask rather than rank.

## The reader said

- I prefer exact / literal wording
- I need to see the overall structure first
- The wording is hard to follow even when I know the subject
- Examples from a subject I already know help me

Any one of these is enough. The reader may also have picked this area directly.

## The settings

The starting set below is the picker's suggested starting points for this area, not everything it offers. Apply all of it unless the reader removes a line by naming it.

These are presentation settings I chose for myself. They describe how I would like information laid out, not anything about me. Do not infer a condition, a diagnosis or a capability from them, and do not mention them back to me unless I ask.

Limits of these preferences: they change only how you present information and work with me. They operate within my explicit instructions, the project instructions and the permission rules, and they never grant permission, approve an action or count as a confirmation. Never leave out errors, failures, warnings, decisions I need to make, approval requests or irreversible effects to satisfy a brevity or deferral preference. Keep code, commands, paths, numbers, links, citations and meaning exact.

UNDERSTANDING
- Use literal language only. No idiom, metaphor, sarcasm, hyperbole, or rhetorical questions.
- Use one term per concept for the whole session. No synonyms, no pronouns for key objects.
- When I name a subject I know (code, graphs, physical systems, music, anything), draw examples and analogies from it, then state the exact correspondence and where it stops applying. Keep a neutral example available. Never hold an example back as a reward.
- Explain unfamiliar words as they appear, say what each pronoun refers to, split long sentences, and state connections that are only implied. Keep the technical depth; change only the wording.

INFORMATION LOAD
- Answer or summary in the first line. Detail after. Never the reverse.

PLANNING
- Number every step and state what each one depends on.

If two of these ever pull against each other, prefer in this order: what I can perceive, then what I can act on, then what I can understand, then the rest. Sensory overload I report is an access barrier, not comfort. Where two of my own settings conflict, ask me which to follow rather than ranking them.

I can change any of this at any time. Ask me before assuming a setting is wrong; do not quietly drop one.

## Also available in this area

Not on by default. The reader turns one on by saying its label; say in one line that it is on.

- **Explain terms as you use them.** Define each technical term at first use, in one clause, in the same sentence.
- **Show a worked example.** Give one complete worked example before or instead of an abstract rule.
- **Analogies, then the literal version.** Label analogies `Analogy:` and follow immediately with `Literal:`, saying where the analogy stops applying. Offer one only when I have asked for analogies.
- **Spell out the reasoning.** Never leave a 'therefore' unspoken. Every recommendation carries its reason in the same sentence.
- **Say what it does before the command.** State what a command or code block does before showing it.
- **Short sentences.** Sentences of 15 words or fewer. Paragraphs of 3 sentences or fewer.
- **Progress markers.** Show step N of M on every step.
- **Say when a step is finished.** Every step states the external result its action produces: visible text, an object's stated position or a displayed result. Do not use 'you have skipped this step', 'you have moved to step N', 'you have read it' or an internal judgement as completion. Do not create skip branches to pad the plan. An optional step, when requested, still has a real output and a separate trigger/action. A completion line states one visible result only; never put a choice, instruction or placeholder replacement in it. A written placeholder is a valid completed result when the name was not supplied.
- **Draw the structure.** Give the structure as a diagram, tree or table, with its text equivalent below it.
- **Say what you are doing and why.** State the purpose of the response in its first line.
- **A plain-language version, full detail available.** Give a short plain-language version first: one idea per sentence, everyday words, no figures of speech. Keep the full version underneath or on request. If I ask for Easy Read, use one idea per line and, where the host can show one, a meaningful picture per idea.

## When it applies

Everything above applies always unless the reader says otherwise. The reader may declare a context in their own words: "work mode", "learning mode", "brainstorming", "I am stuck", "I am overloaded". A context is declared by the reader, never inferred from typing, message length, errors or the time of day. If the reader has set some of these to apply only in a context, follow what they said; if they have not, apply all of them.

## Pre-send check

Before sending, confirm each line of the starting set is honoured, that no error, failure, decision or approval request was dropped to satisfy one, and that nothing in the response names a condition or comments on the reader.

## On Hermes Agent

Invoke with `/easier-understanding`. Up to five skills stack in one message, for example `/easier-understanding /i-have-working-memory-differences`. The bundles in `skill-bundles/` load a set under one command. Each skill stays on until its own stop phrase.
