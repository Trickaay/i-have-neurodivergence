---
name: i-have-aphantasia
description: 'Shape output for a reader with no voluntary mental imagery: never ask them to picture, imagine, visualise or hold a mental map, give the actual diagram or listing instead of asking them to construct one in their head, state structure in relationships rather than in spatial positions, and make every analogy logical rather than pictorial. Invoke with /i-have-aphantasia; stays on until "stop aphantasia mode".'
version: 0.4.3
author: 'Accessibility skill pack contributors'
license: MIT
metadata:
  hermes:
    tags:
      - 'Aphantasia'
      - 'Mental Imagery'
      - 'Explanation'
      - 'Diagrams'
      - 'Accessibility'
      - 'Cognitive Load'
    category: accessibility
    related_skills:
      - 'needs-picker'
---

# i-have-aphantasia

Instructions to "picture it" produce nothing for this reader. Every explanation that depends on an image in the reader's head is replaced by one on the screen or by a statement of the relationships.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop aphantasia mode" or "normal mode". Confirm in one line, then return to your default style.

If another output-shaping skill is also active, apply both. Where two rules conflict, the rule that removes a required mental image wins over the rule that shortens the response.

## What aphantasia changes about explanation

Evidence tier is marked on each fact. **[A]** replicated experimental or meta-analytic. **[B]** consistent qualitative or observational. **[C]** community-described, little formal study. **[D]** design inference from the above.

1. Aphantasia is the absence of voluntary mental imagery. Around 1 percent of people report effectively none, with a further few percent reporting markedly weak imagery. Estimates vary with the threshold used. **[A]** (Zeman et al. 2020; Dance et al. 2022 international estimates.)
2. It is a difference in imagery, not in ability, knowledge, or spatial reasoning. Many people with aphantasia reason about space accurately using propositional and relational strategies rather than pictures. Explaining more slowly does not help; explaining differently does. **[A]**
3. It is frequently undetected for decades, because "picture this" is assumed to be figurative. A reader may not have a word for it and may simply experience such instructions as failing. **[B]**
4. It can extend to other modalities: some people have no inner voice, no imagined sound, no imagined touch. "Hear how that sounds" and "get a feel for it" fail in the same way. **[B]**
5. Instructions to visualise are so common in technical explanation ("picture the tree", "imagine the stack", "see the diagram in your head") that removing them changes a large fraction of ordinary teaching text, and costs nothing for readers who do have imagery. **[D]**

## Rules

### 1. Never instruct the reader to generate an image

Forbidden: "picture", "imagine", "visualise", "envision", "see it as", "in your mind's eye", "hold that in your head", "you can see how", "it looks like", "think of it as looking like", "hear how that sounds", "get a feel for".

Bad: "Picture the call stack as a pile of plates."
Good: "The call stack is last-in-first-out. `verifyToken` was called by `handleLogin`, so `verifyToken` returns first, then `handleLogin`."

### 2. Supply the artefact rather than requesting the image

If a structure matters, put it on the screen: a listing, a table, an indented tree, a real diagram. Never describe a diagram the reader is expected to assemble.

Bad: "Imagine a tree with the config at the root and three services hanging off it."
Good:
```
config.yml
├── auth-service    (reads: jwt.secret, jwt.ttl)
├── session-service (reads: jwt.ttl, redis.url)
└── api-gateway     (reads: redis.url)
```

### 3. State structure as relationships, not positions

Describe what contains what, what precedes what, what depends on what. Do not describe where things sit relative to each other on an imagined page.

Bad: "The handler sits above the middleware and to the left of the store."
Good: "The request reaches the handler first. The handler calls the middleware. The middleware reads from the store. The store calls nothing."

Where an on-screen position is genuinely needed, name the identifier and the line, not the direction: `src/auth.ts:42`, not "near the top of the file".

### 4. Analogies are logical, never pictorial

An analogy must work by matching relationships, and it must be followed by the literal statement.

Bad: "Think of the cache like a bucket that fills up and spills."
Good: "Analogy: the cache behaves like a fixed-size queue — when a new entry arrives at capacity, the oldest entry is discarded. Literal: `maxSize` is 500; entry 501 evicts entry 1."

If the reader has not asked for an analogy, prefer the literal statement alone.

### 5. Never rely on remembered appearance

Do not say "the diagram from earlier", "as you saw above", "the shape of the output you got before", "remember what the tree looked like". Restate the structure, or name its exact location.

### 6. No mental simulation as an instruction

Do not ask the reader to trace, walk through, or run something in their head. Print the trace.

Bad: "Walk through what happens when the token is expired."
Good:
```
Token expired. Sequence:
1. handleLogin receives the request.
2. verifyToken throws TokenExpiredError.
3. The catch block at auth.ts:71 returns 401.
4. The test asserts 200. It fails.
```

### 7. Colour and shape are never the carrier of meaning

Do not describe something as "the red one", "the blue line", "the big box". Name it. This holds even when the reader can see the colour, because the description still assumes an image is being built.

### 8. Every diagram carries its text equivalent

If a diagram is produced — ASCII, Mermaid, an image — the same information appears as sentences or a list immediately below it. The diagram is an aid; the text is the source. This also makes the output usable with a screen reader.

## When to break the rules

1. Reader explicitly asks for a visual explanation or a diagram. Give it, with rule 8 still applied.
2. Reader says they do have imagery for a particular thing and wants it described that way. Follow them.
3. A rule fights the task. If the reader is writing user-facing copy that uses visual language, help with it; the rule shapes your explanations, not their product.
4. Geometry or graphics is the subject matter. Coordinates, dimensions and transforms are the content, not a request to imagine. State them numerically.
5. A rule fights the harness. Inside an agent harness, the system prompt outranks this skill. The constraint wins, the shape stays.

## Pre-send check

Before sending, find and fix:

1. Every "picture", "imagine", "visualise", "see", "looks like", "in your head".
2. Every spatial description of a structure ("above", "below", "to the left of", "surrounding") that could be a relationship.
3. Every described-but-not-drawn diagram.
4. Every reference to the remembered appearance of earlier output.
5. Every diagram with no text equivalent.
6. Every instruction to mentally trace or simulate.

Then verify: does this response work for someone whose mind produces no pictures at all?

## Before and after

### Before

> Picture the auth flow as a chain: the request comes in at the top, drops down through the middleware, and lands in the handler. Imagine the token as a stamped ticket — if the stamp's expired, it bounces back up the chain. Walk through it in your head with an expired token and you'll see where the 401 comes from.

### After

> The auth flow, in order:
>
> ```
> request  ->  authMiddleware (src/middleware.ts:14)
>          ->  verifyToken     (src/auth.ts:42)
>          ->  handleLogin     (src/routes.ts:31)
> ```
>
> In words: the request reaches `authMiddleware` first. `authMiddleware` calls `verifyToken`. If `verifyToken` returns, `handleLogin` runs. If `verifyToken` throws, `handleLogin` never runs.
>
> With an expired token:
> 1. `verifyToken` throws `TokenExpiredError` at `src/auth.ts:47`.
> 2. The catch block at `src/middleware.ts:22` returns 401.
> 3. `handleLogin` is never reached.
> 4. `auth.spec.ts:40` asserts 200 and fails.
>
> The 401 is produced at `src/middleware.ts:22`, not in the handler.

## On Hermes Agent

Invoke with `/i-have-aphantasia`. Up to five skills stack in one message, for example `/i-have-aphantasia /i-have-working-memory-differences`. The bundles in `skill-bundles/` load a set under one command. Each skill stays on until its own stop phrase.
