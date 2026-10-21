# Install and remove the 0.4.5 pack

Extract the entire ZIP before starting. These instructions apply to macOS, Linux and Windows; a local host application must already be installed. The copy-based routes do not need Python, Git or a build step. See [START_HERE.md](START_HERE.md) for the browser-only option.

## Codex

### Choose where the skills apply

- **One project (recommended):** the `.agents/skills/` folder inside the project you will open in Codex.
- **Across projects:** `.agents/skills/` inside your home folder. On Windows, that means your Windows user profile folder. If Codex runs inside WSL or on another computer, use that environment's home or project folder instead.

In Finder, Command-Shift-period shows hidden folders. In Windows File Explorer, enable **View → Show → Hidden items**. In Linux file managers, Control-H commonly shows hidden folders. Create `.agents` and its `skills` subfolder if they do not exist. Keep the leading dot.

### Copy and check

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

Keep a local installation record with the destination and the names of the folders you added (a saved folder listing is enough). Note any identical folders that were already there; they were not newly installed. The skill files are self-contained after copying, so the extracted download is no longer needed for this route once you have that record. Python 3 is optional, only for running the profile compiler yourself. File copying alone does not prove the host loaded the skills: if the menu is unavailable, report that check as not run.

### Update or remove

For an update, compare the new complete folders with your installed copies first. Back up customised folders outside `.agents/skills/`, then replace only folders you explicitly choose. Keep unrelated skills and profiles. Check the menu again in a new chat. Avoid installing the same names in both project and personal locations unless you intend to manage both.

To remove the pack, close the active chats using it and remove only the folders recorded as newly installed by this pack. If you did not keep a record, compare against the original download and check ownership before removing anything. Do not delete the entire `.agents/skills/` directory. Keep customised work and saved profiles unless you explicitly want to remove them. Start a new chat afterward.

## Claude Code

Choose one route. The bundled route has **31 skills**; the marketplace route has **19 authored skills**. They use different command namespaces. Loading both can produce duplicate choices.

### All 31 skills from this download

Keep the extracted folder in a location you intend to retain. Open a terminal in its root folder and run:

```text
claude --plugin-dir platforms/claude
```

From another location, replace the example below with the full path to the extracted pack's `platforms/claude` folder. Keep quotes around paths containing spaces:

```text
claude --plugin-dir "FULL PATH TO THE EXTRACTED PACK/platforms/claude"
```

Use `/what-would-make-this-easier-skills:needs-picker` in that Claude Code session. The plugin is loaded for sessions launched with this flag; this command does not make a permanent marketplace installation. Start future sessions with the same flag. Moving or deleting the folder breaks that path. To stop loading it, exit the session and launch Claude Code without the flag.

For an update, extract the new release into a separate retained folder and launch with its path. Preserve any custom edits before changing versions.

### Marketplace installation: 19 authored skills

In Claude Code:

```text
/plugin marketplace add Trickaay/i-have-neurodivergence
/plugin install i-have-neurodivergence@i-have-neurodivergence
```

Choose your intended installation scope in the host. Restart if needed and invoke `/i-have-neurodivergence:needs-picker`. This installs the current marketplace version from GitHub, which may be newer than this ZIP; it is not a frozen 0.4.5 installation route.

To update:

```text
/plugin marketplace update i-have-neurodivergence
/plugin update i-have-neurodivergence@i-have-neurodivergence
```

Restart afterward. To disable or uninstall, use Claude Code's `/plugin` installed-plugin controls, selecting this plugin and its original scope. Do not remove other plugins or account configuration.

## Other hosts

For ordinary chat assistants, use the picker's Plain instructions export. An uploaded ZIP does not automatically install skills or give an assistant filesystem access. Cowork and Hermes instructions are in [platforms/README.md](platforms/README.md); their live integrations have not been qualified for this release.

## Integrity and help

The release includes a `.zip.sha256` checksum beside the ZIP. Compare it with your download if you want to check transport integrity; this is not a publisher signature. Inside the curated bundle, `BUNDLE_MANIFEST.json` records the source commit and the SHA-256 of every other file. GitHub's automatic source-code archives do not include that generated manifest.

If a host cannot open local HTML, use your normal browser where permitted; do not override organization or browser restrictions. Downloaded exports avoid the known manual-copy final-newline limitation. See [release notes](RELEASE_NOTES.md) and the [repository](https://github.com/Trickaay/i-have-neurodivergence) when reporting an issue; omit personal profiles and account details.
