# What Would Make This Easier — Claude skills

Version 0.4.8. This plugin contains 31 skills: 19 authored skills and
12 area skills generated from the needs vocabulary. They change presentation
only when invoked; they do not infer a diagnosis or authorize actions.

From this directory, start Claude Code with:

```bash
claude --plugin-dir .
```

From the repository root, use `claude --plugin-dir platforms/claude`.
For an absolute path containing spaces, quote the complete path after
`--plugin-dir`. Keep the entire directory, including bundled picker resources.

Invoke `/what-would-make-this-easier-skills:needs-picker` to choose settings,
or select an individual skill from the command menu. Support skills persist
until their documented stop phrase; the picker ends after producing a profile.
The root marketplace plugin is a separate 19-skill installation route.

See the [installation guide](https://github.com/Trickaay/i-have-neurodivergence/blob/main/platforms/README.md)
and [validation limits](https://github.com/Trickaay/i-have-neurodivergence/blob/main/README.md#validation-status).
These are presentation preferences, not evidence that the support is effective.

Inspired by [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd).
Licensed under MIT; see the repository license.
