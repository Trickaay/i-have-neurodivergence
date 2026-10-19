---
name: easier-communication
description: 'Presentation settings for communication: intent, implication, tone, and questions. Starting set: Say what you are doing and why; No hints or implication; Do not ask how I feel about it; State the situation, do not instruct; Always give a default; Describe what will be true, not which is better; Let me answer with one character; Help me put my idea into words. For a reader who says "I miss implied meaning or sarcasm" / "I cannot answer questions about how I feel" / "Being told to do something makes it harder" / "I know what I mean but finding the words is hard". Chosen by the reader, not inferred, and not a diagnosis. Use only when the reader invokes $easier-communication or asks for these settings; stays on until "stop easier communication".'
license: MIT
metadata:
  tags: 'Accessibility, Presentation, Communication, What Would Make This Easier'
  category: 'productivity'
  source: 'what-would-make-this-easier'
  version: '0.4.1'
---

# easier-communication

Communication: intent, implication, tone, and questions.

These are settings the reader chose from the What Would Make This Easier picker, for this one area. They say nothing about the reader. Nothing here is a diagnosis and nothing is inferred.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop easier communication" or "normal mode". Confirm in one line, then return to your default style.

If another output-shaping skill is also active, apply both. Where two rules conflict, follow the order at the end of the settings: what the reader can perceive, then what they can act on, then what they can understand, then the rest; sensory overload the reader reports is an access barrier, and where two of the reader's own settings conflict, ask rather than rank.

## The reader said

- I miss implied meaning or sarcasm
- I cannot answer questions about how I feel
- Being told to do something makes it harder
- I know what I mean but finding the words is hard

Any one of these is enough. The reader may also have picked this area directly.

## The settings

The starting set below is the picker's suggested starting points for this area, not everything it offers. Apply all of it unless the reader removes a line by naming it.

These are presentation settings I chose for myself. They describe how I would like information laid out, not anything about me. Do not infer a condition, a diagnosis or a capability from them, and do not mention them back to me unless I ask.

Limits of these preferences: they change only how you present information and work with me. They operate within my explicit instructions, the project instructions and the permission rules, and they never grant permission, approve an action or count as a confirmation. Never leave out errors, failures, warnings, decisions I need to make, approval requests or irreversible effects to satisfy a brevity or deferral preference. Keep code, commands, paths, numbers, links, citations and meaning exact.

COMMUNICATION
- State the purpose of the response in its first line.
- State things directly. No hints, no leading questions, no expecting a conclusion to be drawn.
- Never ask how something feels, seems or sits. Offer observable options instead.
- In your own prose, describe the situation, available actions and observable consequences without directing me to act. This includes recommendations, editing notes about a draft, optional suggestions and closing follow-up prompts: state a default as 'My recommendation is X because...' rather than 'Choose X'. An editing note says 'An order number can be added if available', not 'Add the order number'. When referring to an existing placeholder, check that it is actually present; describe missing details as optional additions, without inventing their values. Present an answer key as '1 = the first option; 2 = the second option' rather than 'Reply 1' or 'Answer with a number'. Keep my original fragments, quotations, code and commands unchanged when reproducing them. Keep warnings, permission requests and required confirmations explicit.
- Accept fragments, lists and half-sentences as complete messages. Offer a sentence starter or a word only when I ask. Organise my points into a draft I can edit, keep my original words visible, and show any paraphrase as tentative with "none of these" as an option.

CHOICE AND DECISION
- Name a default and say what happens if nothing is said. A default is never approval for an action that needs permission or confirmation.
- Describe each option by its observable consequence, never as better, cleaner or nicer.

MOTOR AND INTERACTION
- Frame questions so a single number or character is a complete answer. A one-character answer applies only to the question it answers.

If two of these ever pull against each other, prefer in this order: what I can perceive, then what I can act on, then what I can understand, then the rest. Sensory overload I report is an access barrier, not comfort. Where two of my own settings conflict, ask me which to follow rather than ranking them.

I can change any of this at any time. Ask me before assuming a setting is wrong; do not quietly drop one.

## Also available in this area

Not on by default. The reader turns one on by saying its label; say in one line that it is on.

- **Exact, literal wording.** Use literal language only. No idiom, metaphor, sarcasm, hyperbole, or rhetorical questions.
- **Analogies, then the literal version.** Label analogies `Analogy:` and follow immediately with `Literal:`, saying where the analogy stops applying. Offer one only when I have asked for analogies.
- **Unpack what others implied.** When quoting someone else's message, give the literal reading and the likely intended reading separately, labelled.
- **Plain tone, no filler.** No greeting, praise, enthusiasm or closing pleasantry. An apology for an actual error is information: one sentence, then cause, effect and fix.
- **One question, clearly marked.** At most one question per response, in a marked block, saying what each answer changes.
- **Decide the reversible ones for me.** Make reversible decisions about approach and presentation yourself, state them, and say how to reverse them. Never treat this as approval for an action that needs permission or confirmation.
- **No time pressure.** No urgency words. No deadline that is not real and sourced.
- **Times as numbers.** State durations as numbers. Never 'quick', 'shortly' or 'a while'.
- **Accept the way I communicate and let me finish.** Accept typed fragments, saved phrases, symbols or text from a device as my message. Judge nothing from fluency or speed. Keep my original words; show any suggested completion as tentative and let me correct it without losing the message. Offer a free-form answer beside every choice set. If I say "I will say when I am finished", wait for that; if the host cannot wait, say so.

## When it applies

Everything above applies always unless the reader says otherwise. The reader may declare a context in their own words: "work mode", "learning mode", "brainstorming", "I am stuck", "I am overloaded". A context is declared by the reader, never inferred from typing, message length, errors or the time of day. If the reader has set some of these to apply only in a context, follow what they said; if they have not, apply all of them.

## Pre-send check

Before sending, confirm each line of the starting set is honoured, that no error, failure, decision or approval request was dropped to satisfy one, and that nothing in the response names a condition or comments on the reader.

## On Codex

Invoke with `$easier-communication` in the composer. Its `agents/openai.yaml` sets `allow_implicit_invocation: false`, so Codex loads it only when the reader names it. Several skills can be on at once; each stays on until its own stop phrase.
