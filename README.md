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

Restart the host if needed, then invoke `needs-picker` using its skill menu or command. The root plugin contains the 19 authored skills. The generated Claude platform plugin also includes the 12 area skills.

For **Codex**, copy the folders in `platforms/codex/skills/` into your user skills directory or a repository's `.agents/skills/`, then invoke `$needs-picker` or another skill by name.

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

Browser verification covered 11 selection and note scenarios, with all 44 exports matching the Python compiler, plus selection removal, comparison controls, clipboard copying and file downloads. Live Codex checks discovered all 31 skills and exercised the picker and every support skill. After the initial checks of `needs-picker`, `easier-choice` and `i-have-dyslexia`, the remaining 28 skills each received an isolated three-turn check: activation, a new topic without reinvocation, and the documented stop phrase. All 28 stop phrases worked. The revised dyspraxia skill also passed separate manual UI and terminal walkthrough retests.

An earlier `easier-communication` response used imperative recommendation wording. Its descriptive-language rule now explicitly covers recommendations and follow-up prompts while preserving quotations, commands, warnings and required confirmations. The revised skill passed four fresh Codex sessions (12 turns): two runs of the original scenario, new recommendation topics, and quotation and permission checks. Each session checked activation, persistence on a new topic and the stop phrase. These are behavioral smoke checks, not a guarantee of identical responses, effectiveness or complete assistive-technology coverage.

## Inspiration and license

Inspired by [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd), whose skill format provided the starting point for this collection.

Released under the [MIT License](LICENSE). See [third-party notices](THIRD_PARTY_NOTICES.md) for upstream attribution.
