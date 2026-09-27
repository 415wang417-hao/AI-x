# Peeking Under the Hood of Claude Code: Architecture and Internals

# Peeking Under the Hood of Claude Code: Architecture and Internals

## 1. Overview: De-mystifying Claude Code

Anthropic's Claude Code has set a new benchmark for autonomous command-line coding agents. Rather than relying on hidden proprietary magic, Claude Code achieves state-of-the-art results through rigorous software engineering, meticulous context management, and hierarchical prompting strategies. By proxying Claude Code's network traffic with LiteLLM, Outsight AI extracted and analyzed the exact mechanics powering the agent.

## 2. The Dynamic Prompt Assembly Pipeline

Unlike simple agents that submit a static 10,000-token system prompt on every call, Claude Code dynamically constructs its instructions from modular components based on current project state:

- Core Agent Persona: Defines terminal interaction guidelines, bash execution safety, and conciseness rules.
- Project Memory (CLAUDE.md): Automatically discovers and parses CLAUDE.md in the repository root to ingest build commands, test patterns, and code styles.
- Ephemeral Tool Descriptions: Only tools relevant to the active sub-task (grep, glob, bash, file edit) are exposed in the JSON schema.

## 3. The Secret Weapon: <system-reminder> Tags

One of the most consequential findings is Claude Code's extensive use of <system-reminder> tags injected at the tail of user turns. As conversations grow and approach context limits, LLMs tend to suffer from "recency bias" and "context rot". Claude Code counteracts this by injecting real-time reminders:

```
<system-reminder>
CRITICAL: Do not write test commands with infinite loops.
Always inspect the file before applying edits.
Keep your response concise and focused on tool calls.
</system-reminder>
```

## 4. Sub-Agent Task Decomposition

When handling broad requests (e.g., "Refactor the authentication middleware and write unit tests"), Claude Code spawns ephemeral sub-agents. Each sub-agent runs in an isolated context window with dedicated tools, returning only the synthesized diff and test results back to the primary supervisor agent, preventing context pollution.

## 5. Command Execution Guardrails & Sandboxing

To prevent catastrophic filesystem modification or remote command injection, Claude Code evaluates bash commands through a multi-tier risk scoring matrix before prompting the user for approval or executing in a protected sandbox.