---
name: chief-of-staff
description: Personal Chief of Staff system for ADHD-ish operators. Vault-based, loop-driven, nervous-system-aware. Built and lived-in across daily sessions on real consulting, content, and long-running personal work.
tags: [chief-of-staff, productivity, adhd, memory, obsidian, claude-code, vault, loop]
---

# Chief of Staff

**Executive function as a service. For the brain that builds everything and remembers nothing.**

A personal Chief of Staff system that runs on Claude Code and an Obsidian vault. Four commands, one loop, persistent memory. Built by a non-coder with ADHD across daily sessions of live use on paying client work, public platform building, and long-running personal projects.

## What It Solves

- **Session amnesia.** Every new Claude session forgets who you are, what you're working on, and where you left off. You waste the first ten minutes re-priming. The vault and memory layer fix this at boot.
- **Task pile-up without executive function.** Lists grow, nothing moves, shame compounds. The loop forces a small win first and flags what matters now, not everything.
- **Nervous system collapse under pressure.** Financial stress triggers freeze, freeze prevents action, inaction deepens shame. The system leads with what's working, shrinks the task when stuck, and never uses guilt.
- **Drift between sessions.** What you decided Tuesday is gone by Friday. `/wrap` writes it down. `/start` reads it back.

## The Loop

| Command | When | What It Does |
|---------|------|--------------|
| `/setup` | Once | Conversational wizard. Generates `CLAUDE.md`, seeds `.claude/memory/`, copies vault templates. |
| `/start` | Opens every session | Reads Command Center + To-Do List. Delivers Must/Should/Could briefing. Flags overdue Waiting For items. Ends with "what do you want to work on?" |
| `/sync` | Mid-session (optional) | Checkpoint. Saves anything worth keeping to memory. Updates Command Center or To-Do if needed. |
| `/wrap` | Closes every session | Reflects wins. Updates Command Center date. Queues open threads. Rotates stale memory entries out. |

## The Key Insight

> **The loop is the thing. The commands are cheap. The state they read and write is where the value lives.**

Your Claude does not need to be smarter. It needs to be oriented. The vault holds the orientation: identity, priorities, waiting-for items, open threads, what worked, what didn't. Every session boots with that context loaded and ends with it updated. The AI becomes a Chief of Staff, not a task executor.

## Setup

See [Quickstart in the README](README.md#quickstart). Four questions get you a working system; the rest is optional.

## Prerequisites

- Claude Code installed (`claude.ai/code`)
- Obsidian (free, `obsidian.md`) with a vault set up
- A Claude subscription (any tier; Pro works)
- Optional but recommended: Gmail, Google Calendar, Google Drive MCP connectors for briefing enrichment

## What You Get Out of It

- A Claude that wakes up knowing who you are, what's on your plate, and what's overdue
- A morning briefing that starts with a small win, not a guilt list
- A single source of truth for tasks, waiting-for items, and open threads
- Memory stored as plain Markdown on your disk. Survives model swaps, session resets, and vendor changes.
- A system that gets *more* useful over time as the vault grows, not less

## What This Is Not

- Not a task manager. It is an *operating shell* for a task manager.
- Not a life coach. It is a structural prosthetic for executive function.
- Not a productivity cult. No streaks, no guilt, no shame. You skip a day, you pick back up.

## Links

- **Repo:** https://github.com/jdpolasky/ai-chief-of-staff
- **Architecture deep-dive:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Obsidian setup guide:** [docs/obsidian-setup.md](docs/obsidian-setup.md)
- **Notion vs Obsidian (why vault-based):** [docs/notion-vs-obsidian.md](docs/notion-vs-obsidian.md)
