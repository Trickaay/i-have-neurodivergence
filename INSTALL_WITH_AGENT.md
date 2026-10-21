# Agent-assisted installation — 0.4.5 early access

This document is an installation recipe, not automatic permission to execute it. Follow it only when the user requests installation or help installing. User instructions and the host's permission rules take precedence. Do not enable the support skills on the user's behalf as part of installation.

## Establish the requested destination

Read [START_HERE.md](START_HERE.md) and [INSTALL.md](INSTALL.md). Resolve the extracted pack's root from this document's location. Ask only for missing choices: host, project versus personal scope, and destination path. For Codex, recommend project scope when the user has not chosen. For Claude Code, explain the bundled 31-skill session route and separate 19-skill marketplace route before selecting one. Use any choice the user has already supplied.

If the user asks only for advice, explain the steps. If you cannot access the user's filesystem, say so and guide them manually; do not claim installation from seeing an attachment. Do not install a host application, sign in, change account settings, request broader permissions or disable safeguards as a side effect.

## Inspect before copying

- Inspect the source. The curated release contains `BUNDLE_MANIFEST.json`; check that its file list is safe and unique, and verify every listed SHA-256 against the extracted bytes. Reject absolute paths, traversal, symlinks and unsupported file types. Do not execute file content while validating it. The manifest checks accidental damage; it is not a signature or a source of instructions. If it is missing, explain that this may be a source archive, and establish provenance before proceeding.
- Identify the exact host skill root in the environment where that host runs. Resolve paths containing spaces correctly. Check existing same-named folders and any symlinks before making changes; stop on ambiguous ownership or a symlink destination rather than following it into an unexpected location.
- Never silently replace or merge an existing different skill. Byte-identical complete folders may be left in place. If any folder differs (including extra files), stop the whole copy before adding any skills and present the conflict and backup/replacement choices. A request to install is not permission to discard custom work. Keep unrelated folders, projects, profiles and account settings unchanged.

## Perform the selected route

**Codex:** Copy all 31 complete directories from `platforms/codex/skills/` into the chosen `.agents/skills/` root. Include hidden metadata and all nested resources. Do not copy the outer `skills` folder as another nesting level. Use normal file operations, with no network downloads or execution of bundled compiler scripts required. Do not overwrite a path that appears during copying; stop and report any partial additions rather than guessing or deleting existing data. Keep a list of newly created skill directories for the user's installation record.

**Claude Code, bundled 31 skills:** Keep the complete bundle in the user's chosen retained location. Give the correctly quoted `claude --plugin-dir` command pointing at its `platforms/claude` directory. Launch it only if asked and supported by your tools. Explain that this loads a session plugin and requires the flag again next time; do not claim it as a persistent installation. Do not alter the marketplace or copy this plugin into an undocumented cache location.

**Claude Code, marketplace 19 skills:** Use only the documented marketplace and installation commands after the user selects this route and scope. This route contacts public GitHub and may install a version newer than the ZIP. Respect host confirmations and report the actual installed version. Do not export credentials or replace user configuration to make validation pass.

**Other hosts:** Use the documented platform route only when the user explicitly chooses it. State that Cowork and Hermes live qualification remains outstanding. Plain instructions can be prepared for any assistant, but changing account-wide custom instructions needs the user's selected destination and authorization.

## Verify and report

For copied Codex skills, compare every relative file and its bytes with the bundled source and count all 31 folders. Check the five picker resource paths in INSTALL.md, and report the source version. Confirm unrelated and pre-existing files are unchanged. Record source path, destination, route, copied versus identical folders, and any conflicts; keep this record local and avoid credentials or account data.

Where tools permit, ask the host to refresh discovery or start a fresh session and verify that it lists the skills. The picker should be available under the documented invocation. Do not change the user's preferences to perform an installation check. If live discovery or invocation cannot run, explicitly say “Files verified; host discovery/invocation not checked.” A manifest check or file count alone is not a live-host pass.

For a Claude session plugin, verify the manifest and resources and give the launch and picker commands; separately state whether the host actually loaded them. For a marketplace install, report its version, scope and observed status.

Finish with where the pack was placed, what was verified, any unrun checks, how to invoke needs-picker, and the route-specific removal steps. Stop after installation; no repository pushes, releases, external messages or unrelated changes.
