# Validation history and limits

These are bounded checks of instructions, files and software behavior. They do not establish clinical benefit, effectiveness for everyone, or identical replies across models.

## 0.4.9: reviewed return and current checks

The returned Claude retest used 0.4.8 at `2cbd45e`. Its archive checksum and all 1,573 manifest entries were verified, and the tested source matched all 208 baseline files. Review confirmed the reported wording/guidance findings. The fixed behavior sample was **62 PASS / 4 FAIL out of 66**; the original 33 agent cases were **27 PASS / 6 FAIL**, and all 48 agent cases including supplemental controls were **39 PASS / 9 FAIL**. These are separate denominators. Returned public plugin-upgrade and browser checks are supplied evidence, not fresh 0.4.9 execution.

The 0.4.9 changes address factual additions in planning drafts, presentation defaults, decision counts, numeric back-check columns, picker closing offers and installation guidance. The recorded installer/remover mechanism is unchanged.

Fresh checks on the candidate:

- Seven documented non-browser checks plus `git diff --check` passed, including **45 helper tests**. **83 software-DOM checks** passed. The documented Playwright browser-conformance command was not run here.
- Native Codex: **19 PASS / 4 UNKNOWN across 23 valid turns**. All final task/screen-content targets passed. Four turns included skill/preparation announcements; whether the host required those notices could not be independently established. Those turns are not counted as full passes.
- Eight earlier picker turns had an invalid invocation in the test harness and are retained separately as invalid setup. The corrected eight-turn journey loaded the skill and complete menu, preserved selected contexts, and did not write a file when save was skipped.
- Live-site UI smoke checks verified selection, comparison, preview and export controls and supplied the README screenshot. Copy showed success feedback, but the browser automation's clipboard read returned empty; clipboard round-trip remains UNKNOWN. This live-site check preceded publication of 0.4.9 and is not final-candidate browser conformance.

Agent guidance remains a limitation. Fresh Codex trials still searched before asking for an exact removal record. Other trials accurately reported real helper refusals and no-op removals, but some violated procedural reading/stop instructions. Scenario-only missing-Python tests and restricted-capability tests do not qualify genuinely unavailable-Python or truly tool-less hosts. Later wording clarifies report-only reads without retroactively changing earlier scores. Prefer the exact recorded helper command for removal; do not ask an agent to discover the latest record or bypass a refusal.

No fresh Claude model, native Windows, Cowork, Hermes, human screen-reader or native mod-host qualification is claimed. Manual selection can omit the final export newline; use Download for exact bytes. An installer source identity supplied by a caller is not authentication—verify the source independently.

See [development commands](DEVELOPMENT.md), [installation instructions](INSTALL.md) and [release notes](RELEASE_NOTES.md).

---

# Earlier 0.4.8 verification

These are smoke checks of files, the browser page and live sessions. **They do not establish support effectiveness, identical responses between sessions, or complete assistive-technology coverage.**

**Returned Claude retest of 0.4.7.** Independent review supports 65 PASS / 1 FAIL across the fixed 66 behavior turns, with 33 separate positive, save, supplemental and picker turns passing. The reported agent-installation result was 29 PASS / 4 FAIL; review identified an additional retry after explicit permission denial, giving 28 PASS / 5 FAIL after that targeted correction. Unsafe-removal cases stopped, quarantine maps preserved owned bytes, and both public upgrades from 0.4.6 and 0.4.5 passed in the returned evidence. These are bounded samples, not reliability rates or fresh 0.4.8 results.

**Current repairs (0.4.8).** Installation instructions check real tool capability before planning, preserve exact path components, require an exact record before searching, restrict manual fallback to user-performed steps, and stop operations on explicit permission denial. They exclude installation through symlinks. Dyscalculia separates explicitly requested teaching examples from the calculation's Working table, labels conversion factors with compound units, and retains a separate explanation column. The deterministic helper's ownership, refusal and retained-quarantine behavior is unchanged.

**Verification.** Seven documented non-browser checks and `git diff --check` passed, including 45 helper tests; 83 separate software-DOM checks passed. The documented browser-conformance command was not run in this review. An isolated Claude CLI upgrade from 0.4.7 to the candidate 0.4.8 used local Git transport and matched all installed files; public update transport still needs Claude's retest. Initial native Codex numeric checks scored 7/9 against the full contract, followed by a 3/3 retest after repairing missing explanation columns. Those small, separate samples are not a full-pack or Claude qualification.

**Agent limits.** Fresh Codex trials exposed searches before missing-record/symlink refusals; the guide now gives terminal stop conditions. Original failures and subsequent targeted checks are retained for independent retesting. A restricted-capability session still announced file access before admitting it could not perform it, so this response behavior is not repaired or qualified. With no filesystem tools, use the manual guide yourself. Genuine tool-less and genuinely unavailable-Python host tests remain outstanding; a scenario assertion does not establish either condition. The deterministic helper passed its tests, but prose cannot enforce agent behavior. Verify source provenance independently: the helper only records the caller's asserted identity. Native Windows, Cowork, Hermes, screen-reader and native mod-host qualification remain outstanding.

**Browser limits.** The browser page, its logic, layout, styling and embedded support wording are unchanged in this revision. Software-DOM checks do not establish native clipboard or accessibility behavior. Manual selection may omit the final newline; use Download when exact bytes matter. The nonblocking missing-icon directory warning remains.

