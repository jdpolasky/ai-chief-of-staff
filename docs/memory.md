# Memory

"Persistent memory" is the line most personal-LLM repos put in their README. The field in April 2026 is crowded: Karpathy's LLM Wiki gist, Caleb Peavy's `unmutable/ai-chief-of-staff`, `kbanc85/claudia`, ADAM, MemPalace, Hermes. Each handles memory differently. Some mean conversation history. Some mean a single long scratch file. Some mean a folder of notes the model can grep.

After running this system for 116 sessions against 125 active memory files (plus a handful of session logs and self-notes, and an archive of retired files), persistent memory here looks like something more specific. It is a directory of short markdown files with frontmatter, indexed at the top by a file called `MEMORY.md`, that the model reads at the start of every session before it sees the conversation. Functionally this is a narrow, structured application of retrieval-augmented generation (RAG): the index points, the model decides which files are relevant, the pulled files ground the response. The pattern is not novel. YAML frontmatter on markdown has been standard Obsidian-vault convention for years. What's worth writing up is which disciplines make the pattern load-bearing and which break it.

This doc covers what the directory holds, how it is laid out, what goes in, what stays out, and how memory stays honest over time.

## The floor

The template ships with four named files in `.claude/memory/`: `user_profile.md`, `preferences.md`, `projects.md`, and `session_context.md`, plus the `MEMORY.md` index. That's the floor. On day one those four files cover everything a fresh user needs the model to remember. Updates land in the right file. The index points at four entries.

Most users will outgrow the floor within a few weeks. When they do, the rest of this doc describes the convention they grow into.

## The index pattern

`.claude/memory/` holds the memory files. `MEMORY.md` sits at the root of that folder. It is an index. One line per file. Under 150 characters each.

```
- [Role and tools](user_profile.md) — JP, non-coder, Obsidian + Claude Code
- [No em-dashes](feedback_communication_style.md) — plain speech, no marketing verbs
- [Pony Parties Express](project_pony_party_web_stack.md) — Astro + Keystatic, live at pnyparty.netlify.app
```

That's the shape. `MEMORY.md` gets loaded every session because `CLAUDE.md` references it (see [`laws.md`](laws.md) for what `CLAUDE.md` is and how it loads). The referenced memory files get loaded on demand: the model reads `MEMORY.md` at session start, sees the descriptions, and pulls the specific files it decides are relevant to the current work. The index is a map to the terrain.

Writing paragraphs directly into `MEMORY.md` breaks the pattern. The index is not a memory. Paragraphs bloat it past useful, which makes the model scan past the pointers it needs.

## Four types

Every memory file declares a type in its frontmatter. There are four.

**user.** Background facts about the person. Role, preferences, knowledge, constraints. Eight files in this vault. These change slowly. They exist so a fresh session doesn't start by re-explaining who you are.

**feedback.** Guidance about how to work. "Never use em-dashes." "Don't line-edit my prose without asking." "Execute when the instruction is clear, don't narrate your thinking." Seventy-six files in this vault. This is the largest category because the model is always making small decisions that can be tuned.

**project.** Active work. Clients, deadlines, the current plan for the thing that's shipping. Thirty files. These decay fastest. A project memory from three months ago is usually wrong.

**reference.** Pointers to where information lives outside the vault. A Linear project for bug tracking. A Grafana dashboard for latency. The API docs for a tool. Eleven files. Smallest category, most stable.

Other type taxonomies exist. Four is enough for this one.

## Frontmatter

Every memory file opens with the same block.

```
---
name: Writing craft in JP's voice
description: Reach for the shortest accurate word. Plain language is evidence the thinking is done. No em-dashes, no marketing verbs, no rhythm pastiche.
type: feedback
---
```

Three fields. Each earns its keep.

`name` is the human-readable title. It appears in the `MEMORY.md` line.

`description` is how the model decides whether the file is relevant to the task at hand. The full description gets loaded when `MEMORY.md` loads. Generic descriptions like "writing rules" fail here because the model can't route. Specific descriptions let the model pull the right file without loading all of them.

`type` is one of the four above. Later filters (audit, decay) treat categories differently.

Files are named `{type}_{slug}.md`: `feedback_communication_style.md`, `project_pony_party_web_stack.md`, `user_profile.md`. The type prefix is convention, not enforced by tooling, and makes the directory scannable at a glance.

Optional fields include `decay: exempt` for memories the system should never prune, and `originSessionId` for tracing a memory back to the specific Claude Code session that produced it (the session UUID is available from Claude Code's session state when the memory is written). Add fields when you need them. Don't ship schema you aren't using.

## What to save and what not to

The hard part is discipline about what belongs.

**Save:** patterns that will still be true next month. Preferences the model can't derive from the current state of the code. Project decisions and the reasoning behind them. Rules that emerged from real failures.

**Don't save:** file paths, code structure, function signatures, architecture details. The repo is the authoritative source for those. A memory that duplicates what the code says is a future contradiction waiting to happen, because the code will change and the memory will not.

Also don't save: recent-chat summaries, today's task list, in-flight decisions. Those live in the Command Center or the To-Do List, which are designed to be rewritten. Memory is for what survives rewrites.

The rule I use: if I can grep the repo and answer the same question, the memory shouldn't exist.

## Decay and provenance

Memories go stale. A feedback rule can stop holding. A project can close. A reference can rot.

This system ships two mechanisms to keep memory honest. Both are simple.

**The firings log.** At `/wrap` time, for every memory that actually shaped a response during the session, the model appends one line to `_system/memory_firings.log`:

```
2026-04-22 | session_116 | feedback_verify_before_done.md | two full review passes before declaring code done
```

Date, session number, memory file, one-line note. Append-only. The log exists so audits can see which memories are load-bearing and which have gone quiet.

**Decay analysis.** The `/audit` skill runs every seven sessions (or whenever the briefing surfaces the audit-due flag). It reads the firings log over the most recent window and surfaces memories that haven't fired in a long time for review. The human decides whether to keep them, tighten them, or cut them.

The analysis has a bootstrap gate. It stays dormant until the firings log holds ten distinct sessions of data. Without that history the tool can't tell the difference between a dormant memory and one that hasn't had a chance to fire yet. The gate check lives inside `/audit`: the skill counts distinct session values in the log and skips decay analysis if the count is under ten. The gate lifts automatically once the log fills in.

The firings-log instrumentation is part of `/wrap` and starts producing data on the first session.

A small set of memories carry `decay: exempt` in their frontmatter. User-type memories are exempt by default (biographical baseline). A few foundational feedback memories are exempt because they are load-bearing even when they don't visibly fire. The prose-samples corpus is exempt for the same reason.

## What it does over time

The first week I installed this, memory was a handful of files. The model felt slightly less generic than a fresh session would have. That was it.

Six weeks in, the memory directory is running the personality of the system. Rules have accumulated. "Don't summarize at the end of every response." "Verify before denying a claim." "Ideas go to the capture inbox, not the to-do list." "Match response length to the task." Each one came from a friction point that cost me a few minutes the first time. Each one stopped costing minutes the second time.

That compound return is what other repos are describing when they say persistent memory. They are pointing at the end state. Getting there is a matter of writing it down every time something goes wrong and every time something surprising goes right. Start with two or three memories about how you like to work. Add one every time the model does something you want different next time. A month in you'll have something that behaves like it knows you. That's the whole mechanism. Nothing about it is clever.
