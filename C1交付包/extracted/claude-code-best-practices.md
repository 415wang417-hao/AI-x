# Claude Code overview - Claude Code Docs

##### Getting started

- Overview
- Quickstart
- Changelog

##### Core concepts

- How Claude Code works
- Extend Claude Code
- Explore the .claude directory
- Explore the context window

##### Use Claude Code

- Store instructions and memories
- Permission modes
- Common workflows
- Best practices

##### Platforms and integrations

- Overview
- Remote Control
- Claude Code on the web
- Claude Code on desktop
- Chrome extension (beta)
- Computer use (preview)
- Visual Studio Code
- JetBrains IDEs
- Code review & CI/CD
- Claude Code in Slack

- Get started
- What you can do
- Use Claude Code everywhere
- Next steps

## ​Get started

- Terminal
- VS Code
- Desktop app
- Web
- JetBrains

- Native Install (Recommended)
- Homebrew
- WinGet

```
curl -fsSL https://claude.ai/install.sh | bash
```

```
irm https://claude.ai/install.ps1 | iex
```

```
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

```
brew install --cask claude-code
```

```
winget install Anthropic.ClaudeCode
```

```
cd your-project
claude
```

- Install for VS Code
- Install for Cursor

- macOS (Intel and Apple Silicon)
- Windows (x64)
- Windows ARM64 (remote sessions only)

## ​What you can do

Automate the work you keep putting off

```
claude "write tests for the auth module, run them, and fix any failures"
```

Build features and fix bugs

Create commits and pull requests

```
claude "commit my changes with a descriptive message"
```

Connect your tools with MCP

Customize with instructions, skills, and hooks

Run agent teams and build custom agents

Pipe, script, and automate with the CLI

```
# Analyze recent log output
tail -200 app.log | claude -p "Slack me if you see any anomalies"

# Automate translations in CI
claude -p "translate new strings into French and raise a PR for review"

# Bulk operations across files
git diff main --name-only | claude -p "review these changed files for security issues"
```

Schedule recurring tasks

- Cloud scheduled tasks run on Anthropic-managed infrastructure, so they keep running even when your computer is off. Create them from the web, the Desktop app, or by running /schedule in the CLI.
- Desktop scheduled tasks run on your machine, with direct access to your local files and tools
- /loop repeats a prompt within a CLI session for quick polling

Work from anywhere

- Step away from your desk and keep working from your phone or any browser with Remote Control
- Message Dispatch a task from your phone and open the Desktop session it creates
- Kick off a long-running task on the web or iOS app, then pull it into your terminal with claude --teleport
- Hand off a terminal session to the Desktop app with /desktop for visual diff review
- Route tasks from team chat: mention @Claude in Slack with a bug report and get a pull request back

## ​Use Claude Code everywhere

## ​Next steps

- Quickstart: walk through your first real task, from exploring a codebase to committing a fix
- Store instructions and memories: give Claude persistent instructions with CLAUDE.md files and auto memory
- Common workflows and best practices: patterns for getting the most out of Claude Code
- Settings: customize Claude Code for your workflow
- Troubleshooting: solutions for common issues
- code.claude.com: demos, pricing, and product details

Was this page helpful?