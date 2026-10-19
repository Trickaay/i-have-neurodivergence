# i-have-neurodivergence

Skills and a needs picker for choosing how an assistant presents information and works with you. Choose supports such as shorter sections, explicit wording, fewer choices, written steps, or help getting back to an interrupted task. You can change or stop them at any time.

The collection has **19 authored skills**, **89 supports** across **12 areas**, and **31 skills per platform** for Claude Code, Codex and Hermes Agent. It also exports plain instructions for other assistants.

## Start with the picker

1. Download this repository from [GitHub](https://github.com/Trickaay/i-have-neurodivergence) using **Code → Download ZIP**, then extract it.
2. Open `needs-picker.html` in your browser.
3. Choose what would make the exchange easier, then choose what helps. Everything is optional.
4. Copy the **Plain instructions** output into your assistant's custom instructions or the start of a conversation.

The picker also exports an `AGENTS.md` section, a `SKILL.md`, YAML and JSON. To keep an editable profile, export YAML and save it as `needs.yaml` wherever you choose. The browser page does not require a Python installation or a build step.

If clipboard access is blocked, Copy selects the displayed text for manual copying. Some browsers omit its final line break from that selection. Download preserves the complete export, including its final line break.

## Install skills

For Claude Code, add this repository as a marketplace and install the plugin:

```text
/plugin marketplace add Trickaay/i-have-neurodivergence
/plugin install i-have-neurodivergence@i-have-neurodivergence
```

Restart the host if needed, then invoke `needs-picker` using its skill menu or command; in Claude Code it is listed as `/i-have-neurodivergence:needs-picker`. The root plugin contains the 19 authored skills. The generated Claude platform plugin also includes the 12 area skills; see the [platform installation guide](platforms/README.md#claude-code-and-cowork).

For an existing Claude Code installation, refresh the marketplace and update the plugin, then restart the host:

```text
/plugin marketplace update i-have-neurodivergence
/plugin update i-have-neurodivergence@i-have-neurodivergence
```

This release is **0.4.1**. Earlier repaired files still used the `0.4.0` version, which caused existing installations to keep their cached copy. Updating the marketplace alone does not update the installed plugin.

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

Before publishing changed skills, increase the version in `.claude-plugin/plugin.json`. The platform generator reads that version for every generated bundle; keeping the old version prevents existing Claude installations from receiving the update.

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

These are smoke checks of files, the browser page and live sessions. **They do not establish support effectiveness, identical responses between sessions, or complete assistive-technology coverage.**

**Claude retest of `af0cd63`.** Claude Code 2.1.303 installed the root marketplace plugin with 19 skills and the generated plugin with 31 skills, including a path containing spaces. A fresh GitHub browser ZIP matched all 194 files. Sixteen fresh three-turn sessions completed: 42 of 48 turns passed review; six failed across planning, default handling, numeric results and communication wording. Existing installations also stayed on an older cached copy because both releases used version `0.4.0`. The real-browser conformance suite passed 44 export comparisons and seven UI checks. Separate direct-file checks recorded 56 PASS, one final-newline selection failure and one screen-reader check NOT_RUN. These supplied results belong to that revision, before the repairs below.

**Version 0.4.1 repairs and fresh checks.** The four remaining skill contracts now include more explicit examples and checks for external triggers, one-action steps, defaults without repeated menus, consistent arithmetic, tabled comparisons and descriptive editing notes. One root manifest supplies every generated release version; validation rejects mismatched versions. A real Claude Code 2.1.303 upgrade test reproduced the stale `0.4.0` cache, then updated to `0.4.1` and verified all 194 installed files through an isolated local Git remote. The public GitHub transport was not part of that upgrade test.

Fresh Codex checks passed 30 reviewed turns across 10 sessions for the four repaired skills, the picker and quotation/permission boundaries. Intermediate outputs, including an additional numeric-comparison formatting failure corrected before the final tests, remain outside the final-source pass counts. Node/jsdom passed 64 software-integration checks, including 52 browser-compiler/Python comparisons across 13 profiles. This is not a native-browser run. All six root/installed compiler formats match; build, parity, compiler self-test, rule checks and validation of 93 generated skills pass.

**Limits.** Fresh Claude conversations and a native-browser run after the 0.4.1 changes are NOT_RUN. The picker implementation and styling are unchanged; only embedded rule wording changed. Cowork, Hermes host behavior and screen-reader use by people remain unverified. The manual-copy final-line-break limitation is documented above; downloads retain the complete export. Narrow smoke checks do not establish that every rule holds in every response.

## Inspiration and license

Inspired by [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd), whose skill format provided the starting point for this collection.

Released under the [MIT License](LICENSE). See [third-party notices](THIRD_PARTY_NOTICES.md) for upstream attribution.
