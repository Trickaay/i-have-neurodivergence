# Install and remove the pack

Extract the entire ZIP before starting. These instructions apply to macOS, Linux and Windows; a local host application must already be installed. Manual copying needs no Python, Git or build step. The recorded installer/remover needs Python 3.10 or later. See [START_HERE.md](START_HERE.md) for the browser-only option.

## Codex

### Choose where the skills apply

- **One project (recommended):** the `.agents/skills/` folder inside the project you will open in Codex.
- **Across projects:** `.agents/skills/` inside your home folder. On Windows, that means your Windows user profile folder. If Codex runs inside WSL or on another computer, use that environment's home or project folder instead.

In Finder, Command-Shift-period shows hidden folders. In Windows File Explorer, enable **View → Show → Hidden items**. In Linux file managers, Control-H commonly shows hidden folders. Create `.agents` and its `skills` subfolder if they do not exist. Keep the leading dot.

### Recorded installation and removal (recommended)

Create the chosen destination parent first: for a project, create `.agents` inside that project. Keep the extracted pack in a retained folder. The helper requires Python 3.10+, supplied by your environment; it does not install dependencies or contact the network.

From the extracted pack root, preview the installation. Replace the example paths and source identity with your actual verified download or commit:

```text
python3 scripts/install_pack.py install --source "." --destination "FULL PROJECT PATH/.agents/skills" --host codex --scope project --source-id "VERIFIED SOURCE IDENTITY"
```

The preview makes no changes. If it matches your intended installation, repeat with `--apply` at the end. On Windows use `py -3` if that is how Python is installed. For personal scope choose the skills path in your home environment and `--scope personal`. Do not copy a placeholder identity without verifying it: the helper records this value but cannot authenticate a repository or release for you.

Use the exact retained path spelling. Parent-traversal (`..`) components, links and destinations inside the record store are refused; `--source "."` is supported.

Every applied run gets a durable record beside `skills`, under `.i-have-neurodivergence-records/RUN_ID/record.json`. Even an all-identical reinstall gets its own record and owns no pre-existing skills. Keep the exact path printed by the helper, including for later removal; keep these private records out of version control. Conflicting skills stop installation before any skill is copied. All 31 folders and their nested files are checked. Open a fresh Codex chat and invoke `$needs-picker` to verify the host loads them.

To remove one run, close chats using its skills and preview:

```text
python3 scripts/install_pack.py remove --record "EXACT RECORD PATH"
```

If the preview succeeds, append `--apply`. Only that run's unchanged newly added skills move into its retained **quarantine**, outside the host's skills directory. The record and all original bytes remain available for recovery. This is removal from host discovery, not permanent deletion. No-op reinstall records cannot remove earlier skills. If the record or a skill is missing, moved, incomplete, edited or contains extra entries or links, the helper stops. Do not bypass the error with a shell deletion or a source-name/hash comparison.

Keep the record and quarantine in place. Recovery after an interrupted operation or restoration into an occupied path needs explicit review; there is no automatic overwrite, permanent-delete or record-recovery command. The helper refuses older record schemas and cannot adopt or remove manually installed trees. Byte-identical manual trees may remain as pre-existing, unowned skills. Stop other writers during an operation: cooperative locking and integrity checks are not protection against a malicious local process modifying records or racing filesystem changes.

### Manual copy and check

1. Open this pack's `platforms/codex/skills/` folder. It contains 31 skill folders.
2. Check the destination for folders with the same names before copying. If any exist, stop the copy and preserve them. An agent can compare them; identical copies need no update, while different files need your decision and a backup. Do not choose Replace or merge different versions blindly.
3. Copy the 31 complete folders **inside** the source `skills` folder into the destination `skills` folder. Do not nest a second `skills` folder inside it. Keep all subfolders, including `agents`, `references` and `scripts`.
4. Confirm these paths exist beneath the chosen destination:

   - `needs-picker/SKILL.md`
   - `needs-picker/agents/openai.yaml`
   - `needs-picker/references/needs-vocabulary.json`
   - `needs-picker/references/picker-menu.json`
   - `needs-picker/scripts/compile.py`

5. Open the target project and start a new Codex chat. Choose `needs-picker` from the skill menu; in the CLI or IDE extension, type `$needs-picker`. The first screen should say **WHAT WOULD MAKE THIS EASIER?**. `skip` selects the plain default. You can also invoke an individual skill.

For manual copying, retain the original download and a separate durable list of newly added folders. These manual records are not accepted by the deterministic remover. For automatic ownership tracking use the recorded route above. The skill files are self-contained after copying; Python is optional for manual copying and compiling profiles. If host discovery cannot run, report it as not checked.

### Update or remove

For a helper-managed update, preview removal using the exact old run record. If its owned trees are unchanged and you want the update, apply that removal, retaining the quarantine and record; then install the verified new source as a new run. A no-op record owns nothing and cannot remove an earlier run. Changed or pre-existing unowned trees need an explicit preservation/ownership review before updating; the helper never overwrites them. Do not manually replace a managed tree and expect its old record to remain valid. For a manual installation, compare and back up customised folders outside the skills root before replacing only folders you explicitly choose. Keep unrelated skills and profiles. Check discovery in a new chat. Avoid duplicate project/personal copies unless intended.

For helper-managed installations, use the exact recorded-removal command above. For older/manual installations, automatic removal is unavailable: inspect ownership and custom work before deciding what to keep or back up. A matching name or source hash is not proof of ownership. Do not ask an agent to reconstruct a removal list or delete the entire skills directory. Keep unrelated skills, profiles and records.

## Claude Code

Choose one route. The bundled route has **31 skills**; the marketplace route has **19 authored skills**. They use different command namespaces. Loading both can produce duplicate choices.

### All 31 skills from this download

Keep the extracted folder in a location you intend to retain. Open a terminal in its root folder and run:

```text
claude --plugin-dir "platforms/claude"
```

From another location, replace the example below with the full path to the extracted pack's `platforms/claude` folder. Keep quotes around paths containing spaces:

```text
claude --plugin-dir "FULL PATH TO THE EXTRACTED PACK/platforms/claude"
```

Use `/what-would-make-this-easier-skills:needs-picker` in that Claude Code session. The plugin is loaded for sessions launched with this flag; this command does not make a permanent marketplace installation. Start future sessions with the same flag. Moving or deleting the folder breaks that path. To stop loading it, exit the session and launch Claude Code without the flag.

For an update, extract the new release into a separate retained folder and launch with its path. Preserve any custom edits before changing versions.

### Marketplace installation: 19 authored skills

Inside an **interactive Claude Code session**:

```text
/plugin marketplace add Trickaay/i-have-neurodivergence
/plugin install i-have-neurodivergence@i-have-neurodivergence
```

Choose your intended installation scope in the host. For a terminal or coding agent, use the shell commands instead; slash commands are not available in non-interactive `claude -p` sessions. This example uses project scope, so run it from the target project. Use `user` or `local` instead only if that is your chosen scope:

```text
claude plugin marketplace add Trickaay/i-have-neurodivergence --scope project
claude plugin install i-have-neurodivergence@i-have-neurodivergence --scope project
```

Restart if needed and invoke `/i-have-neurodivergence:needs-picker`. This installs the current marketplace version from GitHub, which may be newer than this ZIP; it is not a frozen release-ZIP installation route.

To update inside an interactive session:

```text
/plugin marketplace update i-have-neurodivergence
/plugin update i-have-neurodivergence@i-have-neurodivergence
```

Or update from a terminal, using the installed plugin's scope:

```text
claude plugin marketplace update i-have-neurodivergence
claude plugin update i-have-neurodivergence@i-have-neurodivergence --scope project
```

Restart afterward. See the [Claude Code command reference](https://code.claude.com/docs/en/plugins/cli-reference) for your host version. To disable or uninstall, use Claude Code's `/plugin` installed-plugin controls, selecting this plugin and its original scope. Do not remove other plugins or account configuration.

## Other hosts

For ordinary chat assistants, use the picker's Plain instructions export. An uploaded ZIP does not automatically install skills or give an assistant filesystem access. Cowork and Hermes instructions are in [platforms/README.md](platforms/README.md); their live integrations have not been qualified for this release.

## Integrity and help

The release includes a `.zip.sha256` checksum beside the ZIP. Compare it with your download if you want to check transport integrity; this is not a publisher signature. Inside the curated bundle, `BUNDLE_MANIFEST.json` records the source commit and the SHA-256 of every other file. GitHub's automatic source-code archives do not include that generated manifest.

If a host cannot open local HTML, use your normal browser where permitted; do not override organization or browser restrictions. Downloaded exports avoid the known manual-copy final-newline limitation. See [release notes](RELEASE_NOTES.md) and the [repository](https://github.com/Trickaay/i-have-neurodivergence) when reporting an issue; omit personal profiles and account details.
