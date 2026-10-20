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

This release is **0.4.3**. Earlier repaired files still used the `0.4.0` version, which caused existing installations to keep their cached copy. Updating the marketplace alone does not update the installed plugin.

For **Codex**, follow the [Codex installation steps](platforms/README.md#openai-codex) to copy all 31 complete folders from `platforms/codex/skills/` into your project's `.agents/skills/` or your personal `~/.agents/skills/`. Open that project in Codex and select `needs-picker` from the skill picker; in the CLI or IDE extension, type `$needs-picker`.

For **Hermes Agent**, use the skill folders and bundles under `platforms/hermes/`. For any other assistant, use the picker output or a block from `platforms/universal/`.

See the [platform installation guide](platforms/README.md) for paths, commands and format details. Copy complete skill folders, including the picker's bundled references, compact menu and compiler.

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

**Supplied Claude retest of 0.4.2 (`bc7c068`).** The GitHub browser download matched all 198 files. Fresh root/generated-plugin installs passed, and public updates from 0.4.1 plus both older 0.4.0 revisions reached the pinned release with matching installed files and restarted skill discovery. The 54 fixed live turns were reported clean: 49 PASS and five FAIL, affecting planning and numeric formatting. Guided picker and save cases passed six turns each. Browser conformance passed 44 comparisons and seven UI checks; separate direct-file checks recorded 84 PASS, two known final-newline selection failures and one screen-reader check NOT_RUN. These are supplied results for 0.4.2, before the repairs below.

**Version 0.4.3 repairs.** Planning keeps every task action inside its steps, with one visible completion result and no redundant material setup, placeholder-editing choices or invented facts. Dyscalculia rules and positive examples now agree on computed units, tabulated arithmetic checks and anchored schedules versus measured durations. Deactivation keeps the remaining request's requested format. The chat picker uses the exact final menu label and separates its two question stages from individual difficulties and the optional context question. Every generated bundle uses the root release version.

**Fresh 0.4.3 checks.** Codex passed 38 reviewed turns across 10 sessions: planning, numeric formatting, mixed-unit and cross-midnight arithmetic, warning/permission boundaries, and picker journeys with and without optional contexts. Earlier numeric runs remain outside the final-source counts, including one stop reply that gave only one requested explanatory sentence before the transition guidance was clarified. These small repeated checks are not a reliability estimate. Node/jsdom passed 68 software-integration checks, including 56 JavaScript/Python export comparisons. All six compiler formats match across four compiler copies; build, parity, compiler self-test, rule checks and validation of 93 generated skills pass. Genuine Claude Code 2.1.303 validated both manifests and upgraded an isolated 0.4.2 installation to 0.4.3 with all 198 files matching the candidate. This upgrade used a local Git remote, not public GitHub transport.

**Limits.** Fresh Claude conversations and a native-browser run after these changes are NOT_RUN. Browser JavaScript, layout and styling are unchanged; embedded planning-rule wording changed. Node/jsdom does not qualify browser layout or assistive technology. Cowork, Hermes host behavior and screen-reader use by people remain unverified. Manual-copy selection can still omit the final line break; downloads preserve it. Narrow smoke checks do not establish that every rule holds in every response or that any support is effective.

## Inspiration and license

Inspired by [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd), whose skill format provided the starting point for this collection.

Released under the [MIT License](LICENSE). See [third-party notices](THIRD_PARTY_NOTICES.md) for upstream attribution.
