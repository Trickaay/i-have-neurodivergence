# Platform installation guide

The Claude, Codex and Hermes trees each contain **31 skills**: the **19 authored skills** from `skills/` and **12 `easier-<area>` skills** generated from the vocabulary's **89 supports**. `universal/` contains one plain Markdown instruction block per area.

All paths below are relative to the repository root unless stated otherwise. Copy entire skill folders. Each `needs-picker` folder includes `references/needs-vocabulary.json`, the compact `references/picker-menu.json`, and `scripts/compile.py` so its resources travel with the skill.

## Claude Code and Cowork

The root marketplace installs the 19 authored skills. Follow the [root installation instructions](../README.md#install-skills) for that route.

To use the generated Claude plugin with all 31 skills, launch Claude Code from the repository root with:

```bash
claude --plugin-dir platforms/claude
```

Choose `needs-picker`, an authored skill such as `i-have-autism`, or an area skill such as `easier-memory` from the host's skill menu. Command names may include a plugin namespace; use the names shown by the host. In Claude Code 2.1, the generated plugin listed its skills as `/what-would-make-this-easier-skills:<skill>`, for example `/what-would-make-this-easier-skills:needs-picker`, and the root plugin listed them as `/i-have-neurodivergence:<skill>`. The plugin layout also targets Cowork, but its loading flow depends on the host.

Claude skills set `disable-model-invocation: true` to require explicit invocation.

## OpenAI Codex

Follow the [Codex installation and removal guide](../INSTALL.md#codex). It covers project and personal locations on macOS, Linux and Windows, conflict checks before copying, and verification after installation. The [agent-install guide](../INSTALL_WITH_AGENT.md) uses a deterministic helper with retained ownership records and recoverable removal.

Copy all 31 complete folders from `platforms/codex/skills/` into the chosen `.agents/skills/` root. Do not nest the outer `skills` folder. Stop before copying if existing same-named folders differ; preserve customised files and unrelated skills. No build step is needed. Manual copying needs no Python; the recorded installer/remover requires Python 3.10+.

Open the target project in Codex and select `needs-picker` from the skill picker; in the CLI or IDE extension, type `$needs-picker`. The first screen should say “WHAT WOULD MAKE THIS EASIER?”. `skip` selects the plain default. The picker ends after setup; support skills have their own stop phrases.

Each folder contains `agents/openai.yaml` with `allow_implicit_invocation: false`, requesting explicit invocation. `platforms/codex/.codex-plugin/plugin.json` also provides a manifest for hosts supporting that route; the installation guide uses direct skill copying. These locations follow the [OpenAI skill discovery guide](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

## Hermes Agent

For recorded copying, use the helper in [INSTALL.md](../INSTALL.md#recorded-installation-and-removal-recommended) with `--host hermes --scope personal` and the exact destination `~/.hermes/skills/accessibility` (expand it to a full path); create its parent first. It records only the 31 skill folders, not bundles or host configuration. Alternatively, manually copy `platforms/hermes/skills/accessibility/` into `~/.hermes/skills/`, or configure that folder through `skills.external_dirs` in your Hermes configuration. Hermes live loading remains unverified.

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

See the [validation status](../README.md#validation-status) for the browser and live Claude Code checks performed for this release and the earlier Codex checks. Live installation, invocation and behavior inside Cowork and Hermes have not been verified. Passing file validation does not establish host integration or the effectiveness of the exact rules.
