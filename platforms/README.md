# Platform installation guide

The Claude, Codex and Hermes trees each contain **31 skills**: the **19 authored skills** from `skills/` and **12 `easier-<area>` skills** generated from the vocabulary's **89 supports**. `universal/` contains one plain Markdown instruction block per area.

All paths below are relative to the repository root unless stated otherwise. Copy entire skill folders. Each `needs-picker` folder includes `references/needs-vocabulary.json` and `scripts/compile.py` so its resources travel with the skill.

## Claude Code and Cowork

The root marketplace installs the 19 authored skills. Follow the [root installation instructions](../README.md#install-skills) for that route.

To use the generated Claude plugin with all 31 skills, launch Claude Code from the repository root with:

```bash
claude --plugin-dir platforms/claude
```

Choose `needs-picker`, an authored skill such as `i-have-autism`, or an area skill such as `easier-memory` from the host's skill menu. Command names may include a plugin namespace; use the names shown by the host. The plugin layout also targets Cowork, but its loading flow depends on the host.

Claude skills set `disable-model-invocation: true` to require explicit invocation.

## OpenAI Codex

Download the ZIP from GitHub and extract it. The extracted folder is normally named `i-have-neurodivergence-main`. Open a terminal in that folder, which contains this pack's root `README.md` and `platforms/` directory. No build step is needed.

For one project, run the following commands on macOS or Linux. Replace the example path with the project folder you will open in Codex:

```bash
TARGET_PROJECT="/absolute/path/to/your-project"
mkdir -p "$TARGET_PROJECT/.agents/skills"
cp -R platforms/codex/skills/. "$TARGET_PROJECT/.agents/skills/"
```

For personal use across projects, use this destination instead:

```bash
mkdir -p "$HOME/.agents/skills"
cp -R platforms/codex/skills/. "$HOME/.agents/skills/"
```

Both commands copy all 31 complete skill folders, including metadata and the picker's bundled vocabulary and compiler. If you have edited an existing copy, preserve those edits before replacing it. These locations follow the [OpenAI skill discovery guide](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

Open the target project in Codex and select `needs-picker` from the skill picker. In the CLI or IDE extension, type `$needs-picker`. The picker displays “WHAT WOULD MAKE THIS EASIER?” and offers `skip` for the plain default. The picker stops after producing your setup. An authored skill such as `i-have-dyslexia` or an area skill such as `easier-communication` can also be selected directly.

To check the installation, the destination should contain `needs-picker/SKILL.md`, `needs-picker/references/needs-vocabulary.json` and `needs-picker/scripts/compile.py`, alongside the other skill folders. If the skills do not appear, start a new chat or restart Codex, and check that you opened the project containing `.agents/skills/`. You can keep or remove the extracted download after copying; the installed folders contain their own resources. Python 3 is needed only when running the optional profile compiler.

Each folder contains `agents/openai.yaml` with `allow_implicit_invocation: false`, requesting explicit invocation. `platforms/codex/.codex-plugin/plugin.json` also provides a plugin manifest for hosts that support that installation route; the commands above use direct skill installation.

## Hermes Agent

Copy `platforms/hermes/skills/accessibility/` into `~/.hermes/skills/`, or configure that folder through `skills.external_dirs` in your Hermes configuration.

Invoke `/needs-picker`, `/i-have-autism`, `/easier-memory`, or another skill by name. Copy `platforms/hermes/skill-bundles/*.yaml` into `~/.hermes/skill-bundles/` to use bundles such as `/reading-stack` or `/learning-layer`.

Some bundles list the separately distributed [i-have-adhd](https://github.com/ayghri/i-have-adhd) skill. Install that upstream skill if you want its rules included; it is not included in this collection.

## Other assistants

Paste a block from `platforms/universal/` into a custom-instructions box or an instructions file your tool reads. For a custom combination, use the browser picker or compile a saved profile:

```bash
python3 needs/compile.py needs.yaml
```

Within an installed `needs-picker` folder, its bundled compiler supports the same formats:

```bash
python3 scripts/compile.py /path/to/needs.yaml --format codex
```

Replace the example path with your profile location. Use `--format rules`, `agents`, `skill`, `hermes`, `codex` or `json` as needed.

## How the trees are built

`build_platform_skills.py` reads the authored skills, `needs/needs-vocabulary.json` and `adaptations.json`. It adjusts invocation syntax, adds platform metadata, bundles picker resources, and generates the area skills. Edit those sources; manual edits to generated files will be overwritten.

Area skills offer the recommended supports for that area, plus additional supports the reader can choose. The recommendations are starting points, not effectiveness rankings. `adaptations.json` supplies action and consent wording so a presentation preference does not grant permission or count as approval.

The picker's profile persists only when the reader saves or applies it. The picker itself stops after setup; each support skill describes its own persistence and stop phrase.

## Rebuild and validate

```bash
python3 platforms/build_platform_skills.py
python3 platforms/build_platform_skills.py --check
python3 platforms/validate_platforms.py
python3 needs/compile.py --self-test
```

The generator uses Python's standard library. The validator requires PyYAML; installing `skills-ref` also enables the Agent Skills reference checks. The validator checks metadata, invocation settings and the file hashes in `index.json`.

See the [root validation notes](../README.md#development-and-validation) for the browser and live Codex checks completed for this release. Live installation, invocation and behavior inside Claude Code, Cowork and Hermes have not been verified. Passing file validation does not establish host integration or the effectiveness of the exact rules.
