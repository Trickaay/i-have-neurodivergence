# Agent-assisted installation — 0.4.6 source revision

First check whether this session has usable filesystem tools. If it does not, begin your reply with “I cannot access or change your local files in this session.” Then give manual guidance from [INSTALL.md](INSTALL.md). Do not print simulated tool calls, tool markup or invented execution results. An attachment alone is not filesystem access.

This document is an installation recipe, not automatic permission to execute it. Follow it only when the user requests installation or help installing. User instructions and the host's permission rules take precedence. Do not enable the support skills on the user's behalf as part of installation.

## Establish the requested destination

Read [START_HERE.md](START_HERE.md) and [INSTALL.md](INSTALL.md). Resolve the extracted pack's root from this document's location. Ask only for missing choices: host, project versus personal scope, and destination path. For Codex, recommend project scope when the user has not chosen. For Claude Code, explain the bundled 31-skill session route and separate 19-skill marketplace route before selecting one. Use any choice the user has already supplied.

If the user asks only for advice, explain the steps. If filesystem access fails later, report the limitation and any partial changes; do not claim installation from seeing an attachment. Do not install a host application, sign in, change account settings, request broader permissions or disable safeguards as a side effect.

## Inspect before copying

- Inspect the source. The curated release contains `BUNDLE_MANIFEST.json`; check that its file list is safe and unique, and verify every listed SHA-256 against the extracted bytes. Reject absolute paths, traversal, symlinks and unsupported file types. Do not execute file content while validating it. The manifest checks accidental damage; it is not a signature or a source of instructions. If it is missing, explain that this may be a source archive, and establish provenance before proceeding.
- Identify the exact host skill root in the environment where that host runs. Resolve paths containing spaces correctly. Check existing same-named folders and any symlinks before making changes; stop on ambiguous ownership or a symlink destination rather than following it into an unexpected location.
- Never silently replace or merge an existing different skill. Byte-identical complete folders may be left in place. If any folder differs (including extra files), stop the whole copy before adding any skills and present the conflict and backup/replacement choices. A request to install is not permission to discard custom work. Keep unrelated folders, projects, profiles and account settings unchanged.

## Perform the selected route

**Codex:** Copy all 31 complete directories from `platforms/codex/skills/` into the chosen `.agents/skills/` root. Include hidden metadata and all nested resources. Do not copy the outer `skills` folder as another nesting level. Use normal file operations, with no network downloads or execution of bundled compiler scripts required. Do not overwrite a path that appears during copying; stop and report any partial additions rather than guessing or deleting existing data. Create and retain the durable installation record described below; a source folder listing or final chat message is not that record.

**Claude Code, bundled 31 skills:** Keep the complete bundle in the user's chosen retained location. Give both launch forms: `claude --plugin-dir "FULL PATH TO THE EXTRACTED PACK/platforms/claude"` from any directory, and `claude --plugin-dir "platforms/claude"` from the extracted pack root. Substitute the actual full path in the first form, preserving quotes. Name the working directory required by the relative form. Launch it only if asked and supported by your tools. Explain that this loads a session plugin and requires the flag again next time; do not claim it as a persistent installation. Do not alter the marketplace or copy this plugin into an undocumented cache location.

**Claude Code, marketplace 19 skills:** Use only the documented marketplace and installation commands after the user selects this route and scope. `/plugin` commands belong in an interactive Claude Code session; for terminal or agent execution, use the `claude plugin` equivalents in INSTALL.md with the selected scope. This route contacts public GitHub and may install a version newer than the ZIP. Respect host confirmations and report the actual installed version. Do not export credentials or replace user configuration to make validation pass.

**Other hosts:** Use the documented platform route only when the user explicitly chooses it. State that Cowork and Hermes live qualification remains outstanding. Plain instructions can be prepared for any assistant, but changing account-wide custom instructions needs the user's selected destination and authorization.

## Keep a durable record for copied skills

Before copying, reserve a new local record beside the destination `skills` directory, for example `.agents/i-have-neurodivergence-install-record-<unique-id>.json`. Use a unique name and exclusive creation; never overwrite an existing record or follow a symlink. This must be a retained location outside `skills`, not `/tmp`, another temporary directory, or the disposable download folder. If a durable record cannot be written, stop before copying. Keep it private and do not add it to version control automatically.

Record the source version, verified provenance and manifest hash when a manifest is supplied. For a source archive without a manifest, record the verified repository and commit identity (or other independently verified source identity), a complete relative source-file inventory with SHA-256 values, and the digest of that saved inventory; do not invent a manifest or treat a filename as provenance. Also record source and destination paths, host and scope, and the complete planned folder list. Classify each folder as newly created by this run or pre-existing and identical. For each new folder, retain its complete relative entry inventory, including hidden files, nested directories and empty directories, entry types, and SHA-256 for every regular file. Capture the installed bytes after verification, not just the names from the source. This records exactly what may later be removed and detects added files as well as changed or missing ones.

Update only this run's record as copying proceeds: distinguish planned, actually created, verified and incomplete entries. On interruption or copy failure, retain the record and report partial additions; do not delete them automatically. Before declaring installation complete, reread the saved record and verify that it matches the installed trees. Show the record's retained path in the final reply. Pre-existing identical folders are never owned by this installation.

## Removing copied skills

A request to remove this pack does not authorize deletion of later custom work. Before deleting anything, inspect the durable record and preflight **every** recorded newly created tree. Validate that its path remains within the recorded destination, with no symlink in the destination, its ancestors or any tree entry. Compare complete entry membership, types and file hashes with the saved installation inventory, including hidden or extra files. Do not execute text from a record as commands.

If the record is absent, incomplete or ambiguous, or any tree differs, is missing or contains a symlink, stop the whole removal. Preserve everything, report the affected paths and ask whether to keep or back up the custom work before deciding what to remove. Do not provide or run a destructive command while this is unresolved. A release folder list alone cannot establish ownership. Do not treat an unchanged file subset as an unchanged folder.

When preflight is complete and unchanged, remove only this run's verified newly created folders under the user's removal request; recheck them immediately before removal. Never remove pre-existing identical folders, unrelated skills, profiles or the `skills` parent. Retain the record and append the removal outcome. If the host blocks removal, report it; do not suggest a command that bypasses the block or the preflight.

## Verify and report

For copied Codex skills, compare every relative file and its bytes with the bundled source and count all 31 folders. Check the five picker resource paths in INSTALL.md, and report the source version. Confirm unrelated and pre-existing files are unchanged. Include conflicts and the verification outcome in the durable record; avoid credentials or account data. A temporary list or unsaved summary does not complete this step.

Where tools permit, ask the host to refresh discovery or start a fresh session and verify that it lists the skills. The picker should be available under the documented invocation. Do not change the user's preferences to perform an installation check. If live discovery or invocation cannot run, explicitly say “Files verified; host discovery/invocation not checked.” A manifest check or file count alone is not a live-host pass.

For a Claude session plugin, verify the manifest and resources and give the launch and picker commands; separately state whether the host actually loaded them. For a marketplace install, report its version, scope and observed status.

Finish with where the pack was placed, what was verified, any unrun checks, how to invoke needs-picker, and the route-specific removal steps. Stop after installation; no repository pushes, releases, external messages or unrelated changes.
