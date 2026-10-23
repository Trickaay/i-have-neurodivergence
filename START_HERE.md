# Start here — 0.4.6 source revision

Choose how an assistant presents information. No diagnosis is required. You can change or stop the settings at any time.

## Use the picker without installing skills

1. Extract the whole ZIP first.
2. Open [needs-picker.html](needs-picker.html) in your usual web browser.
3. Choose what helps, then copy **Plain instructions** into your assistant's custom instructions or a conversation.

The page needs no build step or Python. If Copy is blocked, use Download. Save **YAML** if you want to edit your profile later. JSON is compiled instructions, not the editable difficulty selections. Keep personal notes private.

## Have an agent help you install

Open the extracted folder in a local coding agent, or give it access to that folder. Copy this message:

> Please read INSTALL_WITH_AGENT.md in this extracted pack and help me install it. First establish which assistant I use and where the files should go if I have not already said. Preserve my existing skills and settings. For copied skills, save a durable local installation record outside the skills folder, including which folders were newly added and their complete file inventories and hashes. Verify the installation and tell me where the record is, how to use the pack and how to check for custom changes before removing it.

A chat attachment alone may not give an agent access to your computer. If it cannot write files, it should guide you through [INSTALL.md](INSTALL.md).

## Install it yourself

| Your assistant | Route |
| --- | --- |
| Codex | Copy 31 complete skill folders; see [Codex installation](INSTALL.md#codex) |
| Claude Code | Load the bundled 31-skill plugin, or install the separate 19-skill marketplace plugin; see [Claude installation](INSTALL.md#claude-code) |
| Any assistant with custom instructions | Use the browser picker above |
| Cowork or Hermes | See [platform guidance](platforms/README.md); these host integrations remain unverified |

The browser picker and agent installation guide are separate ways to get started. You do not need to use both.

## What early access means

The current source includes repairs from the 0.4.5 retest. Check the README validation status for completed checks and remaining gaps; fresh Claude qualification of these repairs and human screen-reader testing remain outstanding. These settings are preferences, not proven treatments or guarantees of model behavior. See [release notes](RELEASE_NOTES.md) for the exact limits.

Inspired by [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd). [License](LICENSE) · [Attribution](THIRD_PARTY_NOTICES.md).
