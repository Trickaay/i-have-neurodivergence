# 0.4.5 — first early-access bundle

A downloadable needs picker and optional skills for choosing how an assistant presents information. Start with [START_HERE.md](START_HERE.md), or give [INSTALL_WITH_AGENT.md](INSTALL_WITH_AGENT.md) to a local coding agent when asking it to help install.

This release packages the tested 0.4.5 skill content from commit `11b3a2c9ec793623887e324822854871eb8d1358`. Added onboarding documents do not change skill behavior or plugin versions. The final packaging commit is recorded in the curated ZIP's `BUNDLE_MANIFEST.json` and GitHub's `v0.4.5` release tag.

## Included

- Standalone browser picker: 89 supports across 12 areas; no build or Python needed.
- 19 authored skills and 12 area skills, with 31 complete skills in each generated platform tree.
- Separate Claude marketplace route containing 19 authored skills.
- Start guide, installation/removal guide, agent-install recipe, licence and upstream attribution.
- Source and existing checks for reproducibility. Private research, review transcripts, accounts, machine configuration and Git history are not packaged.

## Repairs already in 0.4.5

Planning removes discarded instructions and unrequested greetings while preserving supplied wording. Numeric rules check unused calculation fragments and misleading glosses. Communication and choice rules require a concrete default and descriptive editing notes. The generated Claude plugin includes its own README.

## Validation and limits

The preceding 0.4.5 source review recorded 62 Codex turns: 60 PASS, no FAIL and two UNKNOWN concerning host-announcement provenance; both final picker screens were exact. It also checked 83 software-DOM groups, generated files and all 93 platform skills. A local Claude Code 2.1.306 upgrade simulation compared all 199 then-current source files. These are prior source checks, not new Claude or browser qualification of this ZIP.

Bundle-specific checks are listed in the GitHub release notes. A file-copy test, host discovery and live conversation behavior are separate results. Windows instructions are provided, but native Windows execution has not been verified. Fresh Claude behavior, native-browser and human screen-reader checks remain outstanding. Cowork and Hermes integrations remain unverified.

Manual clipboard fallback may omit the final newline; use Download when exact export bytes matter. The missing-icon directory warning is nonblocking. Models can still fail to follow a rule. These smoke checks do not establish support effectiveness, clinical benefit or consistent behavior across models.

Inspired by [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd); see [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
