# The needs model

The picker asks what would make an exchange easier and which supports the reader wants. It does not infer a condition. Its source is `needs-vocabulary.json`: **12 areas, 33 difficulties, 89 supports, 6 context scopes and 17 presets**.

## From difficulty to support

An area groups related choices, such as memory or communication. A difficulty describes something the reader notices. A support is a choice about how the assistant should work. Each support has a rule the compiler can turn into instructions.

For example, “I forget where I was after interruptions” can lead to a recap, a running state block or help restarting. The reader chooses which supports to use. The same difficulty can lead different readers to different choices.

The profile records difficulties, chosen supports, contexts and optional notes. The chat picker and browser use the same schema: explicitly selected difficulty IDs are retained under `contexts.always.difficulties`, without inferring difficulties from a preset. There is no structured diagnosis field. A preset expands into supports; the preset label is not retained in the picker's exported profile. Free-text notes can contain anything the reader chooses to write and must not be treated as a source for diagnostic inference.

## Picking supports

1. Choose difficulties, choose supports directly by area, or start from a preset. Every selection is optional.
2. Choose what helps. “Try these” adds a difficulty's authored recommended set. “Show me the difference” compares authored examples. “Not now” dismisses that difficulty's selection.
3. Optionally choose when each support applies. Every support defaults to “Always”.

Recommendations are suggested starting points, not evidence of comparative effectiveness. Some supports deliberately shorten, defer or narrow information. Their `defers_note` explains this before selection.

Supports can have several selection origins: a difficulty, a direct choice or a preset. Dismissing one difficulty removes only its origin; a support chosen elsewhere remains. Explicitly unticking a support removes it entirely. Origins are picker state and are not exported into the profile.

“Something else” accepts a free-text note without classifying it. The picker's quoted serialization converts CRLF and CR line endings to LF and otherwise keeps the note exactly, including leading and trailing spaces, blank lines, quotes and Unicode separators. Deselecting that entry clears its note.

## Contexts

The exported profile can apply supports always or only in a declared context:

```yaml
version: 1
contexts:
  always:
    support:
      - summary_first
      - fewer_options
  learning:
    support:
      - worked_examples
  brainstorming:
    suppress:
      - fewer_options
```

An active context adds to `always` and can suppress a support from that base. The picker exposes six scopes: always, work, learning, stuck, overloaded, and always except brainstorming. The last scope becomes an `always` support plus a brainstorming suppression.

The reader declares contexts. Typing speed, message length, errors or time of day do not establish a context. Access settings remain in place when the reader chooses a learning purpose such as “show me” or “let me try”; practice is never a condition for receiving a requested answer.

## Compilation and exports

`compile.py` parses the restricted profile YAML, resolves support sets, deduplicates choices and emits rules with the applicable conflict guidance. The browser picker implements matching export logic in JavaScript.

| Format | Use |
| --- | --- |
| `rules` | Plain instructions for a conversation or custom-instructions box |
| `agents` | A Markdown section for an instructions file |
| `skill` | A Claude-style `SKILL.md` |
| `codex` | A Codex-style `SKILL.md` |
| `hermes` | A Hermes-style `SKILL.md` |
| `json` | Compiled supports and resolved rules for tooling, not an editable profile |
| YAML from the browser picker | The editable profile itself; save as `needs.yaml` |

YAML retains explicitly selected difficulty IDs in the editable profile. Compiled JSON omits structured difficulty and preset selections: it contains resolved support rules, suppressions, conflict guidance and exact notes. Notes can still contain personal information supplied by the reader. JSON is not a profile backup; keep YAML to reopen or edit the selections.

The browser offers `rules`, `agents`, `skill`, YAML and `json`; the command-line compiler also provides the Codex and Hermes formats. The authored skills supply explanations, examples and edge cases for the rules.

## Conflicts and permissions

Safety and host constraints take priority. The general preference order is what the reader can perceive, then act on, then understand. Sensory overload reported by the reader is an access barrier. Where the reader's own settings conflict, ask which to follow.

The vocabulary defines 18 pair-specific resolutions. Rules that shorten or defer information must still preserve errors, failures, necessary decisions, approval requests and irreversible effects. Presentation settings do not grant permission or substitute for confirmation.

## Evidence and limits

Each support has an `evidence_basis` with three parts: the underlying phenomenon, what is known about the method, and the exact rule. Evidence for a difficulty does not establish the effectiveness of a particular prompt. **The exact rules have not been validated for effectiveness in an agent.**

The picker keeps this explanation under “Why is this offered?” instead of presenting evidence letters as a score beside every choice. Defaults and comparisons are design choices the reader can change.

## Storage

Save an exported profile as `needs.yaml` in a location you choose. In chat, showing the profile is the default; Enter or skip never requests a file write. A save request supplies an explicit destination, and the host must permit the write before a success is reported. It is plain text and can be edited or deleted. There is no required application-specific storage directory.

The browser offers copying and downloading; it does not install a profile into an assistant. Apply the exported instructions through the host's settings or skill mechanism. Optional notes may contain personal information the reader supplied, so the reader controls where the profile is saved and shared.

## Generated files and checks

`needs-vocabulary.json` is the data source. `picker.template.html` contains the page structure and JavaScript. `build.py` validates their references and combines them into the root `needs-picker.html` and `vocab.embed.json`. The embedded projection includes the support and context data needed by the page, along with conflict resolutions; repository-only provenance is excluded.

From the repository root:

```bash
python3 needs/build.py
python3 needs/build.py --check
python3 needs/parity_check.py
python3 needs/compile.py --self-test
python3 needs/rule_checks.py
python3 needs/conformance_test.py
```

The build and parity checks cover generated-file consistency. The compiler self-test and rule checks cover data and instruction properties. Browser conformance compares JavaScript and Python exports; it requires Playwright and Chromium and reports a skip if unavailable. A skipped check is not a pass.

These commands describe the validation workflow. On their own they do not establish live host integration, accessibility for people using assistive technology, or whether a support improves a reader's experience. The [validation status](../README.md#validation-status) lists the browser and live host checks performed for this release and what remains unverified.

The picker exports notes as a quoted YAML string so spaces, blank lines and Unicode characters survive export and compilation. The compiler also accepts the existing indented `notes: |` form.
