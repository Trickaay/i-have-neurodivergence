# Start here — 0.4.8 source revision

Choose how an assistant presents information. No diagnosis is required. You can change or stop the settings at any time.

## Use the picker without installing skills

1. Extract the whole ZIP first.
2. Open [needs-picker.html](needs-picker.html) in your usual web browser.
3. Choose what helps, then copy **Plain instructions** into your assistant's custom instructions or a conversation.

The page needs no build step or Python. If Copy is blocked, use Download. Save **YAML** if you want to edit your profile later. JSON is compiled instructions, not the editable difficulty selections. Keep personal notes private.

## Have an agent help you install

Open the extracted folder in a local coding agent, or give it access to that folder. Copy this message:

> Help me install this pack using INSTALL_WITH_AGENT.md. First check whether you have real tools that can access my files. If not, say so and give steps for me to perform; do not simulate tool calls. Establish my assistant and exact destination if missing. Keep path components unchanged; ask about ambiguous paths. Use the supplied installer after verifying the source, preserve existing skills, and retain its exact run record. If a tool denies permission, stop that operation rather than retrying another way. If Python or the helper is unavailable, give manual instructions for me, without offering to do the copy. Report what you actually checked and how to preview removal using the exact record.

A chat attachment alone may not give an agent access to your computer. Without usable filesystem tools, use [INSTALL.md](INSTALL.md) yourself. That agent route is not qualified: tested agents can announce file access before admitting they cannot perform it. An announced action is not evidence of installation.

## Install it yourself

| Your assistant | Route |
| --- | --- |
| Codex | Use the recorded installer (Python 3.10+) or copy 31 complete skill folders; see [Codex installation](INSTALL.md#codex) |
| Claude Code | Load the bundled 31-skill plugin, or install the separate 19-skill marketplace plugin; see [Claude installation](INSTALL.md#claude-code) |
| Any assistant with custom instructions | Use the browser picker above |
| Cowork or Hermes | See [platform guidance](platforms/README.md); these host integrations remain unverified |

The browser picker and agent installation guide are separate ways to get started. You do not need to use both.

## What early access means

The current source includes repairs from the 0.4.7 retest. Check the README validation status for completed checks and remaining gaps. Agent instructions cannot enforce a host's capabilities or guarantee compliance; the tool-less agent route remains unqualified. Fresh Claude qualification of these repairs and human screen-reader testing remain outstanding. These settings are preferences, not proven treatments or guarantees of model behavior. See [release notes](RELEASE_NOTES.md) for the exact limits.

Inspired by [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd). [License](LICENSE) · [Attribution](THIRD_PARTY_NOTICES.md).
