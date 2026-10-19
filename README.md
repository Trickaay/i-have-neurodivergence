# i-have-neurodivergence

Skills and a needs picker for choosing how an assistant presents information and works with you. Choose supports such as shorter sections, explicit wording, fewer choices, written steps, or help getting back to an interrupted task. You can change or stop them at any time.

The collection has **19 authored skills**, **89 supports** across **12 areas**, and **31 skills per platform** for Claude Code, Codex and Hermes Agent. It also exports plain instructions for other assistants.

## Start with the picker

1. Download this repository from [GitHub](https://github.com/Trickaay/i-have-neurodivergence) using **Code → Download ZIP**, then extract it.
2. Open `needs-picker.html` in your browser.
3. Choose what would make the exchange easier, then choose what helps. Everything is optional.
4. Copy the **Plain instructions** output into your assistant's custom instructions or the start of a conversation.

The picker also exports an `AGENTS.md` section, a `SKILL.md`, YAML and JSON. To keep an editable profile, export YAML and save it as `needs.yaml` wherever you choose. The browser page does not require a Python installation or a build step.

## Install skills

For Claude Code, add this repository as a marketplace and install the plugin:

```text
/plugin marketplace add Trickaay/i-have-neurodivergence
/plugin install i-have-neurodivergence@i-have-neurodivergence
```

Restart the host if needed, then invoke `needs-picker` using its skill menu or command; in Claude Code it is listed as `/i-have-neurodivergence:needs-picker`. The root plugin contains the 19 authored skills. The generated Claude platform plugin also includes the 12 area skills; see the [platform installation guide](platforms/README.md#claude-code-and-cowork).

For **Codex**, follow the [Codex installation steps](platforms/README.md#openai-codex) to copy all 31 complete folders from `platforms/codex/skills/` into your project's `.agents/skills/` or your personal `~/.agents/skills/`. Open that project in Codex and select `needs-picker` from the skill picker; in the CLI or IDE extension, type `$needs-picker`.

For **Hermes Agent**, use the skill folders and bundles under `platforms/hermes/`. For any other assistant, use the picker output or a block from `platforms/universal/`.

See the [platform installation guide](platforms/README.md) for paths, commands and format details. Copy complete skill folders, including the picker's bundled references and compiler.

## Choose a skill directly

The authored skills include the picker, two task-focused skills, and 16 condition or trait presets:

| Purpose | Skills |
| --- | --- |
| Choose your own supports | `needs-picker` |
| Learning and communication | `help-me-learn-this`, `help-me-with-words` |
| Wording and information | `i-have-autism`, `i-have-dyslexia`, `i-have-dyscalculia`, `i-have-apd` |
| Action and input | `i-have-dyspraxia`, `i-have-dysgraphia`, `i-have-tics` |
| Memory, starting and pacing | `i-have-working-memory-differences`, `i-have-inertia`, `i-have-limited-energy`, `i-need-low-demand` |
| Internal references | `i-have-alexithymia`, `i-have-aphantasia` |
| Sensory and assistive technology | `i-have-sensory-sensitivity`, `i-use-a-screen-reader`, `i-have-colour-vision-deficiency` |

The generated `easier-<area>` skills offer supports without a condition label: understanding, information load, attention, planning, memory, learning, communication, sensory access, choice, transitions, motor interaction and pacing.

Skills can be combined. Each support skill documents its stop phrase; the picker produces a profile and then stops. When preferences conflict, follow safety and host constraints, then what the reader can perceive, act on and understand. Ask the reader to resolve conflicts between their own settings. Presentation preferences never grant permission or replace a required confirmation.

## Profiles and evidence

No diagnosis is required. The picker stores chosen supports, contexts, reported difficulties and optional notes; it does not infer a condition or retain a preset label. Notes contain whatever you choose to write, including any personal information you include. Keep, edit or delete your exported profile yourself.

Each support includes an evidence record separating the underlying difficulty, the presentation or teaching method, and the exact rule. **Evidence for a difficulty is not proof that a prompt rule helps. The exact rules have not been validated for effectiveness in an agent.** The picker's “Why is this offered?” view explains these distinctions. Defaults are starting points you can change.

## Command-line use

The compiler uses Python's standard library:

```bash
python3 needs/compile.py needs.yaml
python3 needs/compile.py needs.yaml --format agents
python3 needs/compile.py needs.yaml --format skill
python3 needs/compile.py needs.yaml --format codex
python3 needs/compile.py needs.yaml --format hermes
```

Run these from the repository root, with the path to your own profile. The [needs model](needs/NEEDS_MODEL.md) describes the data and exports.

## Development and validation

Edit the authored skills, `needs/needs-vocabulary.json`, `needs/picker.template.html` or `platforms/adaptations.json`, then regenerate derived files:

```bash
python3 needs/build.py
python3 platforms/build_platform_skills.py
```

Available checks:

```bash
python3 needs/build.py --check
python3 needs/parity_check.py
python3 needs/compile.py --self-test
python3 needs/rule_checks.py
python3 needs/conformance_test.py
python3 platforms/build_platform_skills.py --check
python3 platforms/validate_platforms.py
```

Browser conformance needs Playwright and Chromium; missing Playwright reports a skip, while a missing browser executable must be installed or selected with `CHROMIUM_PATH`. Platform validation needs PyYAML, and uses `skills-ref` when installed.

### Validation status

These are smoke checks of files, the browser page and live sessions. **They do not show that any support is effective, that responses are identical between sessions, or that every assistive technology is covered.**

**Supplied browser review.** The returned picker passed 88 browser checks in Chromium, including focus, controls, notes, copying and downloads, reflow, light/dark contrast and automated accessibility checks. The repository conformance suite passed 44 export comparisons and six UI assertions. These results are bound to the returned HTML, before the additional post-review changes. GitHub ZIP downloads were blocked in that environment, so its downloaded-copy test used a byte-verified archive produced from the pinned Git commit instead.

**Supplied Claude Code 2.1.303 review.** The root marketplace plugin installed from GitHub and listed 19 skills; the generated plugin listed 31 from a path containing spaces. The baseline had 31 fresh three-turn sessions, with 85 of 93 turns meeting review criteria. Retesting the repaired picker and dyspraxia skill gave a candidate-equivalent result of 87 of 93, reusing results for 29 byte-identical skills; this was not a new full-candidate run. The remaining failures concerned default handling, section length, action splitting, numeric presentation and reduced output. One communication session also used imperative follow-up wording. The two targeted dyspraxia walkthroughs passed once each after their examples were clarified.

**Post-review repairs and independent checks.** The preset selector now transfers focus to the visible area tab, with a regression assertion added to browser conformance. Default handling, section limits, action splitting, numeric echoes, reduced-output replies and descriptive answer keys were clarified in canonical sources and regenerated. Software integration checks using Node/jsdom passed 56 checks, including 44 JavaScript/Python export comparisons; the same checks reproduced eight failures on the published baseline. Both theme token contrasts were recalculated, and all six compiler formats matched an installed copy with exact free-text preservation. Fresh Codex smoke checks passed 33 turns across 11 sessions for nine affected skills, including activation, topic persistence, stop phrases, motor walkthroughs and quotation/permission boundaries. Every discovery check found all 31 skills. Service-capacity interruptions and an intermediate example revision were retained outside the pass counts. This DOM check does not establish browser layout, real clipboard permissions or assistive-technology behavior.

**Reported from earlier Codex checks.** On earlier revisions, Codex discovered all 31 skills, each received a three-turn check, the revised descriptive-language rule passed four fresh sessions, and a fresh ZIP installation on macOS passed nine live turns. These results were not rerun for this release.

**Not established.** A fresh Claude Code run after the post-review clarifications, live behavior in Cowork and Hermes Agent, screen-reader and other assistive-technology use by people, and whether any support improves a reader's experience. The review host blocked local-file browser URLs, so the post-review pass did not repeat the direct-file GUI check.

## Inspiration and license

Inspired by [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd), whose skill format provided the starting point for this collection.

Released under the [MIT License](LICENSE). See [third-party notices](THIRD_PARTY_NOTICES.md) for upstream attribution.
