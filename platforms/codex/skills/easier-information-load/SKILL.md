---
name: easier-information-load
description: 'Presentation settings for information load: how much arrives at once: length, density, layers. Starting set: Summary first, detail underneath; Short labelled sections; The complete explanation first. For a reader who says "I lose track of long explanations" / "I need to choose between the whole explanation and one part at a time". Chosen by the reader, not inferred, and not a diagnosis. Use only when the reader invokes $easier-information-load or asks for these settings; stays on until "stop easier information load".'
license: MIT
metadata:
  tags: 'Accessibility, Presentation, Information load, What Would Make This Easier'
  category: 'productivity'
  source: 'what-would-make-this-easier'
  version: '0.4.7'
---

# easier-information-load

Information load: how much arrives at once: length, density, layers.

These are settings the reader chose from the What Would Make This Easier picker, for this one area. They say nothing about the reader. Nothing here is a diagnosis and nothing is inferred.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop easier information load" or "normal mode". Confirm in one line, then return to your default style.

If another output-shaping skill is also active, apply both. Where two rules conflict, follow the order at the end of the settings: what the reader can perceive, then what they can act on, then what they can understand, then the rest; sensory overload the reader reports is an access barrier, and where two of the reader's own settings conflict, ask rather than rank.

## The reader said

- I lose track of long explanations
- I need to choose between the whole explanation and one part at a time

Any one of these is enough. The reader may also have picked this area directly.

## The settings

The starting set below is the picker's suggested starting points for this area, not everything it offers. Apply all of it unless the reader removes a line by naming it.

These are presentation settings I chose for myself. They describe how I would like information laid out, not anything about me. Do not infer a condition, a diagnosis or a capability from them, and do not mention them back to me unless I ask.

Limits of these preferences: they change only how you present information and work with me. They operate within my explicit instructions, the project instructions and the permission rules, and they never grant permission, approve an action or count as a confirmation. Never leave out errors, failures, warnings, decisions I need to make, approval requests or irreversible effects to satisfy a brevity or deferral preference. Keep code, commands, paths, numbers, links, citations and meaning exact.

INFORMATION LOAD
- Answer or summary in the first line. Detail after. Never the reverse. Compose the overview from the finished answer: any count, range or named stage must match the actual parts below. If two stages share one numbered part, count that part once; do not announce a missing part. Before sending, count the actual members of every group named by a count in a heading or overview. For example, book, member and loan are three records, even if lending and returns share them. Use a count-free heading such as "Records" when a count adds no information.
- Use labelled sections with at most five nonblank content lines each; aim for four to leave room for necessary notes. Count every prose line, bullet, numbered item and table row from one heading to the next; headings and blank lines do not count. An introduction plus five bullets is six lines and must be split. Closing offers count in the section they follow: give them their own heading or omit an unrequested offer. Before sending, count each whole section and move any sixth line under another heading. Keep the complete requested explanation; split its presentation rather than omitting content.

LEARNING
- Give the complete explanation in one piece: a short overview, then every part, then where each part belongs. Do not stop for a confirmation between parts unless I ask.

If two of these ever pull against each other, prefer in this order: what I can perceive, then what I can act on, then what I can understand, then the rest. Sensory overload I report is an access barrier, not comfort. Where two of my own settings conflict, ask me which to follow rather than ranking them.

I can change any of this at any time. Ask me before assuming a setting is wrong; do not quietly drop one.

## Also available in this area

Not on by default. The reader turns one on by saying its label; say in one line that it is on.

- **Least first, more on request.** Give the minimum that answers it. Offer depth as a named next step, do not include it. Holds back: Holds detail back until you ask for it.
- **Short sentences.** Sentences of 15 words or fewer. Paragraphs of 3 sentences or fewer.
- **Say how long it is first.** State what is coming and how long before anything longer than ten lines.
- **Keep tangents out.** Anything outside the current scope goes in a `Deferred:` list at the end, one line each.
- **Repeat the current goal.** Restate the current goal at the start of every response.
- **One instruction at a time.** Give one instruction, then stop and wait for it to be done. Holds back: Holds the next instruction back until this one is done.
- **Progress markers.** Show step N of M on every step.
- **One part at a time, with the map.** Explain one part, then show where it belongs in the whole and keep that map visible. Wait for me before the next part. Do not require a confirmation after every paragraph if I say interruptions make it harder.

## When it applies

The starting set and any optional settings the reader has explicitly enabled apply unless the reader says otherwise. Items under Also available remain off until enabled; persistence does not turn them on. The reader may declare a context in their own words: "work mode", "learning mode", "brainstorming", "I am stuck", "I am overloaded". A context is declared by the reader, never inferred from typing, message length, errors or the time of day. If the reader has set some of these to apply only in a context, follow what they said; if they have not, apply the active settings in every context.

## Pre-send check

Before sending, confirm each line of the starting set is honoured, that no error, failure, decision or approval request was dropped to satisfy one, and that nothing in the response names a condition or comments on the reader.

## On Codex

Invoke with `$easier-information-load` in the composer. Its `agents/openai.yaml` sets `allow_implicit_invocation: false`, so Codex loads it only when the reader names it. Several skills can be on at once; each stays on until its own stop phrase.
