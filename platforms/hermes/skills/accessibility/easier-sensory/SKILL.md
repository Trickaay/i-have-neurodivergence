---
name: easier-sensory
description: 'Presentation settings for sensory and interface: visual density, motion, colour, sound. Starting set: Summary first, detail underneath; No motion; Less on screen; No sound or pop-ups; Space it out; Never rely on colour; Readable as a flat stream; Captions, a transcript or another usable format. For a reader who says "I am sensitive to visual clutter" / "I am sensitive to sound / interruptions" / "I hear the output rather than see it" / "I cannot rely on the colours" / "Audio or video is hard to follow". Chosen by the reader, not inferred, and not a diagnosis. Use only when the reader invokes /easier-sensory or asks for these settings; stays on until "stop easier sensory".'
version: 0.4.8
author: 'Accessibility skill pack contributors'
license: MIT
metadata:
  hermes:
    tags:
      - 'Accessibility'
      - 'Presentation'
      - 'Sensory and interface'
      - 'What Would Make This Easier'
    category: accessibility
    related_skills:
      - 'needs-picker'
---

# easier-sensory

Sensory and interface: visual density, motion, colour, sound.

These are settings the reader chose from the What Would Make This Easier picker, for this one area. They say nothing about the reader. Nothing here is a diagnosis and nothing is inferred.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop easier sensory" or "normal mode". Confirm in one line, then return to your default style.

If another output-shaping skill is also active, apply both. Where two rules conflict, follow the order at the end of the settings: what the reader can perceive, then what they can act on, then what they can understand, then the rest; sensory overload the reader reports is an access barrier, and where two of the reader's own settings conflict, ask rather than rank.

## The reader said

- I am sensitive to visual clutter
- I am sensitive to sound / interruptions
- I hear the output rather than see it
- I cannot rely on the colours
- Audio or video is hard to follow

Any one of these is enough. The reader may also have picked this area directly.

## The settings

The starting set below is the picker's suggested starting points for this area, not everything it offers. Apply all of it unless the reader removes a line by naming it.

These are presentation settings I chose for myself. They describe how I would like information laid out, not anything about me. Do not infer a condition, a diagnosis or a capability from them, and do not mention them back to me unless I ask.

Limits of these preferences: they change only how you present information and work with me. They operate within my explicit instructions, the project instructions and the permission rules, and they never grant permission, approve an action or count as a confirmation. Never leave out errors, failures, warnings, decisions I need to make, approval requests or irreversible effects to satisfy a brevity or deferral preference. Keep code, commands, paths, numbers, links, citations and meaning exact.

INFORMATION LOAD
- Answer or summary in the first line. Detail after. Never the reverse. Compose the overview from the finished answer: any count, range or named stage must match the actual parts below. If two stages share one numbered part, count that part once; do not announce a missing part. Before sending, count the actual members of every group named by a count in a heading or overview. For example, book, member and loan are three records, even if lending and returns share them. Use a count-free heading such as "Records" when a count adds no information.

SENSORY AND INTERFACE
- No animation, spinners, progress bars, or redrawn lines.
- No emoji, exclamation marks, ALL CAPS, ASCII art, box drawing, or decorative rules.
- No terminal bell, notification, or window focus change.
- One idea per line. No dense or multi-column tables.
- Never identify anything by its colour. Every status carries a word.
- No meaning carried by alignment, indentation or layout. Tables become labelled lists.
- For any audio or video, offer captions, a complete transcript, a summary and a text-first version as separate choices; I pick. Keep technical terms, numbers and negation exact. Mark an unverified transcript as unverified. Where the host allows, let me replay or change the speed.

If two of these ever pull against each other, prefer in this order: what I can perceive, then what I can act on, then what I can understand, then the rest. Sensory overload I report is an access barrier, not comfort. Where two of my own settings conflict, ask me which to follow rather than ranking them.

I can change any of this at any time. Ask me before assuming a setting is wrong; do not quietly drop one.

## Also available in this area

Not on by default. The reader turns one on by saying its label; say in one line that it is on.

- **Short labelled sections.** Use labelled sections with at most five nonblank content lines each; aim for four to leave room for necessary notes. Count every prose line, bullet, numbered item and table row from one heading to the next; headings and blank lines do not count. An introduction plus five bullets is six lines and must be split. Closing offers count in the section they follow: give them their own heading or omit an unrequested offer. Before sending, count each whole section and move any sixth line under another heading. Keep the complete requested explanation; split its presentation rather than omitting content.
- **Say how long it is first.** State what is coming and how long before anything longer than ten lines.
- **Nothing that pulls attention away.** No asides, no 'by the way', no unrequested suggestions, no notifications.
- **Repeat important things.** Restate a fact rather than referring back to it. Outside a practice I opted into, repetition over retrieval.
- **Same shape every time.** Same structure and labels each turn. Announce any change of shape before it happens.
- **Warn me before changing topic.** Say before changing topic, and name what is being left.
- **Everything copy-ready.** Every exact string in its own copyable block, never inside a sentence.

## When it applies

The starting set and any optional settings the reader has explicitly enabled apply unless the reader says otherwise. Items under Also available remain off until enabled; persistence does not turn them on. The reader may declare a context in their own words: "work mode", "learning mode", "brainstorming", "I am stuck", "I am overloaded". A context is declared by the reader, never inferred from typing, message length, errors or the time of day. If the reader has set some of these to apply only in a context, follow what they said; if they have not, apply the active settings in every context.

## Pre-send check

Before sending, confirm each line of the starting set is honoured, that no error, failure, decision or approval request was dropped to satisfy one, and that nothing in the response names a condition or comments on the reader.

## On Hermes Agent

Invoke with `/easier-sensory`. Up to five skills stack in one message, for example `/easier-sensory /i-have-working-memory-differences`. The bundles in `skill-bundles/` load a set under one command. Each skill stays on until its own stop phrase.
