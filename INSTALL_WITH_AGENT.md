# Agent-assisted installation and removal — 0.4.7

If this session has no usable filesystem tools, begin: **“I cannot access or change your local files in this session.”** Give manual steps from [INSTALL.md](INSTALL.md). Never print simulated tool calls or claim execution. An attachment alone does not grant filesystem access.

Follow this document only when the user asks for installation or removal. Establish any missing host, project/personal scope and exact destination. Use choices already supplied. Installing does not activate support settings. Do not install host applications or dependencies, sign in, broaden permissions or change account settings as a side effect.

## Copied Codex or Hermes skills

Use the supplied **Python 3.10+ helper**, `scripts/install_pack.py`. Do not implement copying, inventory recovery or removal yourself. If Python or the helper is unavailable, stop automatic installation/removal and give manual installation guidance. Do not substitute shell deletion, a source inventory or a filesystem search. Older recipe records are not accepted. Identical manually copied trees may remain as pre-existing and unowned; the helper cannot adopt or remove them.

Read [INSTALL.md](INSTALL.md) for the host's destination. Codex's destination is the exact `.agents/skills` directory. Hermes uses the exact `skills/accessibility` directory inside the chosen Hermes environment; live Hermes qualification is still outstanding. Resolve the extracted source location and verify its provenance independently. A supplied source identity is recorded as an assertion, not authenticated by the helper. For a curated release verify its published checksum and manifest; for a GitHub source archive compare its full file inventory with the chosen verified commit. The helper checks manifest hashes when present, but a manifest is not a signature.

Run a preview, with quoted actual paths and the verified identity:

```text
python3 "PACK/scripts/install_pack.py" install --source "PACK" --destination "PROJECT/.agents/skills" --host codex --scope project --source-id "VERIFIED SOURCE IDENTITY"
```

Inspect the JSON result. A successful preview changes no files. If the user requested installation and the preview matches that request, repeat the same command with `--apply`. Existing identical complete skills remain unowned; any conflicting tree stops the whole operation. Do not overwrite or merge customised skills. Use the user's chosen skills destination and its authorized retained parent for the sibling record store; the parent must already exist. If the write authorization covers only the skills directory, establish permission for the sibling store before applying. Never create unrelated helper directories.

The helper creates a unique durable record at `DESTINATION_PARENT/.i-have-neurodivergence-records/RUN_ID/record.json`, including for a no-op reinstall. It saves complete source provenance/inventory, installed inventories, new versus pre-existing ownership and outcomes. Retain that directory privately; it may contain local paths. Do not commit it, move it or replace an earlier record. Keep the exact new record path in the installation reply. Read the result and verify successful completion, all 31 skill folders and picker resources. A failed/incomplete run needs diagnosis; never clean it up by guessing.

Where available, start a fresh host session and check discovery and `needs-picker` invocation. Otherwise say **“Files verified; host discovery/invocation not checked.”** File equality does not prove loading. Finish with installed version, destination, record path, observed checks and limits.

## Remove a recorded installation

Use this section in a fresh removal session as well. Ask for the **exact record for the run to remove** if it is missing; do not infer “latest” from filenames or search for records. A no-op run owns nothing and must never take over an earlier installation. A request to remove does not authorize destroying custom work.

Preview using the selected record:

```text
python3 "PACK/scripts/install_pack.py" remove --record "EXACT RETAINED RECORD PATH"
```

Only when the preview succeeds and the user requested removal, repeat with `--apply`. The helper validates record structure and location, ownership and complete installed trees. Missing, extra, edited or symlinked entries, malformed/missing/moved records and unresolved transactions stop removal. **Do not bypass a refusal**, even if files match the original download. Report the exact error and preserve everything.

Removal moves only unchanged trees owned by that run out of the host's skills folder into that record's **quarantine**. It does not permanently delete them. Pre-existing skills, unrelated content, profiles, the parent skills folder and every record remain. The result gives quarantine and retained record paths. Keep them for recovery; do not automatically erase quarantine or restore over an existing skill. Partial/interrupted operations remain recorded and need review. Close chats using these skills and start a fresh chat after removal.

The helper is an accidental-loss safeguard for a trusted local account, not a security boundary against a malicious process modifying records or racing filesystem operations. Stop other writers while it operates. A host blocking an operation is a failure to execute, not permission to use another route.

## Claude Code

**Bundled 31-skill session plugin:** retain the extracted pack and give both launch forms:

```text
claude --plugin-dir "FULL PATH TO THE EXTRACTED PACK/platforms/claude"
claude --plugin-dir "platforms/claude"
```

The first works from any directory; the second requires the pack root as the working directory. Substitute the actual quoted full path. Launch only if requested. This is a session plugin, not a persistent install; omit the flag next time to stop loading it. Do not copy it into a cache or use the copied-skills remover on it.

**Marketplace 19-skill plugin:** after the user selects this route and scope, use the documented `claude plugin` commands in [INSTALL.md](INSTALL.md) for terminal/agent execution. `/plugin` commands are for an interactive Claude Code session. Respect host confirmations; report actual version and scope. Use the host's plugin update/uninstall controls for this route, not the copied-skills helper.

**Other hosts or plain instructions:** follow their documented route only when selected. Cowork/Hermes live support remains unqualified. Preparing an export does not authorize changing account-wide custom instructions.

Stop after the requested install/removal and verification. No unrelated writes, repository pushes, releases or external messages.
