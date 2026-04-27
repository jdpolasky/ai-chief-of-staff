# Architecture

Every new conversation with a model starts from zero. It doesn't know who you are, what you're working on, or what you decided yesterday. Time and focus are spent at the top of every session re-priming a model on a conversation you already had.

This repo is a personal operating system to end that. A vault of markdown files, a handful of slash commands, and a memory layer that persists between sessions. The underlying pattern is retrieval-augmented generation (RAG) over a local vault. It runs on your own machine against your own notes. The model reads the vault at session start and hands you back an assistant that already knows who and where you are.

Chief of Staff is the role the model plays once the OS is live. It triages, tracks, briefs, learns, and catches things before they fall.

## What this document is

The short version is the [README](README.md). This is the longer version for readers who want to see the bones before or after they run `/setup`. It covers the loop, the memory model, the operating rules, and the design choices. It's not a user guide. It won't tell you which button to click. It will tell you what's happening when you do.

For current repo contents and install status, see the [README](README.md).

## Who this is for

Built by a non-coder with ADHD, for a non-coder with ADHD. The distraction pattern is familiar, discouraging, and drains your life. You lose focus, you forget things, and time-blindness degrades your ability to function efficiently. Re-calibration takes longer than it should. The small failures add up and turn into shame. Every operating rule here responds to that, none are theoretical.

If you don't have ADHD, this scaffolding will still work great. It was just designed for harder cases than you.

## The loop

A session starts with `/start`. You work. Optionally you `/sync` in the middle. You close with `/wrap`. Between sessions the vault sits on disk and holds state. Next session `/start` reads the state and hands it back to the model.

That's the whole system.

The commands are small. The state they read and write is where the value lives. Each command is a short set of plain instructions that tells the model what to load, what to ask, and what to save. The work is keeping the vault honest.

## The four commands

### `/setup`

Runs once. It's closer to an intake interview than an installer. Asks about you, your work, your goals, your psyche, and what's actually helped you before. The answers become your `CLAUDE.md`, your memory files, and your Command Center. Skip anything you want and come back later to fill the gaps. The system runs on partial information. The first session after setup is the first time a model meets you already knowing who you are.

### `/start`

Opens every session. Reads the Command Center and the To-Do List, and if Gmail and Calendar are wired in it reads those too. Hands you a Must / Should / Could briefing and flags anything you are waiting on that has gone stale. Ends with an invitation, not an assignment.

You used to lose minutes at the top of every session re-priming a fresh model. Those minutes drain executive function you can't afford. A good briefing ends that, and you know where you are before you've written a word.

### `/sync`

Mid-session checkpoint. Optional. Saves to memory, updates the Command Center or the To-Do List, and keeps the system honest halfway through. Most sessions don't need it. Long ones do. What you decided two hours ago can fall out of context before `/wrap` comes around.

### `/wrap`

Closes every session. Reflects back what got done. Saves to memory. Updates the Command Center date. Queues open threads for next time.

`/wrap` is the command that pays the future version of you.

For each command's wiring, see [`docs/protocols.md`](docs/protocols.md). That doc covers what each command reads and writes, failure modes, and the state files behind them.

## Memory architecture

Three tiers, sorted by how often the model reads them. Some it loads every session. Some it touches rarely. Some it ignores until you point at them.

### Tier one: vault source files

The working docs. Command Center. To-Do List. Optionally, source files for each lane of your life you want to track separately: career, research, health, whatever. These are short, factual, current-state. Claude reads them on demand, not every session. You can read them too. They're the single source of truth for what's happening now.

### Tier two: session logs

The narrative record. Append-only. Written during `/wrap`. Rarely loaded back into Claude. They exist so you can reread your own history when you want to, and so future-you can audit past-you when the story has drifted. They're also good for feeding back into your model for research and pattern analysis.

### Tier three: `.claude/memory/`

Claude's persistent memory across sessions. A handful of short markdown files: who you are, what you prefer, what you're working on, what happened recently. Claude reads these at the start of every session. Without them the model meets you new every time. That's how every LLM session works by default. This tier is what breaks the pattern. A file called `MEMORY.md` sits at the top as an index, pointing at the rest.

For the full memory model, see [`docs/memory.md`](docs/memory.md). That doc covers the four types, frontmatter schema, decay and provenance, and the firings log.

## `CLAUDE.md`: the operating instructions

Claude Code loads `CLAUDE.md` at the start of every session. This is where your preferences, your verification rules, your operating constraints live. `/setup` writes the first version. You edit it over time as rules surface from real work.

Treat `CLAUDE.md` as a running instruction set, not documentation. Rules go in, they take effect on the next session, they compound. If the model keeps doing something you don't want, write a rule. If the rule holds for a week, it stays. If it doesn't, cut it. The file is the shortest path from a moment of friction to a durable change in behavior.

The mechanism that turns those frictions into durable behavior is covered in [`docs/feedback-loop.md`](docs/feedback-loop.md).

## Operating principles

A handful of rules do most of the work. Three stand out here. For the `CLAUDE.md`-layer Laws and how each one emerged, see [`docs/laws.md`](docs/laws.md).

### The Operating Constraint

When you flag a problem or a correction, Claude stops, diagnoses the root cause, proposes a plan, and waits for you to say go. Only then does it act.

This is the rule that keeps a model from making your day worse. The damage AI assistants do comes from the gap between "I think I understand" and "I'm going to act on that." A model that closes the gap with action destroys work, rewrites files, sends things it shouldn't. Closing the gap with a pause instead is free.

### Verification Protocol

Before stating a fact about your life, your work, your history, Claude reads the relevant memory file. If the fact isn't on file, Claude says so rather than inventing.

The whole point of this system is to have something you can trust about yourself. A model that makes up a date, a dollar amount, or a person's name and states it with confidence breaks that trust for good. Verification is the rule that keeps it intact.

### Shame-aware framing

No "should have" language. No guilt. No streaks to maintain. When work isn't moving, the system shrinks the task. When you skip a day you pick back up.

An ADHD prosthetic has to work this way to be useful. Financial pressure triggers shame. Shame triggers freeze. Freeze prevents action. Inaction deepens the shame. A system that leads with guilt feeds the loop that broke you in the first place. This one does not.

## The hook layer

Claude Code exposes the seams of the session. Session start, before a tool call, after a tool call, on stop, before compaction. You hang scripts on those seams. That's the hook layer.

Hooks are optional. The base system runs without them. They are where the system bends to your work. Inject today's date at session start. Remind yourself to `/wrap` before closing the terminal. Flag memory files nobody has touched in a month. Scrub private strings before anything goes public. The template ships none of these. Write the ones you need.

Hooks can be any executable. Python is common.

## MCP integration

One MCP is required. [Obsidian MCP](docs/obsidian-setup.md), because without it the system cannot reach the vault and `/start` has nothing to read.

The rest are optional. Gmail surfaces unread threads during `/start`. Google Calendar surfaces today's meetings. Google Drive pulls linked docs into sessions. Wire in whatever else you want.

The system is MCP-agnostic. The vault is the source of truth. MCPs are tentacles that reach out from it. Swap them. Add them. Drop them. The vault survives.

## Design choices

### Why markdown

Plain text outlives the tool. Readable by humans, parseable by machines, version-controllable in git. Notes written today will still open in twenty years. No vendor lock-in. No schema migration. No "the database got corrupted." Worst-case recovery is: open the folder in any text editor.

### Why Obsidian

Best markdown editor shipping. Local-first. Plugins extend the vault without giving up the plain-text substrate. Not strictly required. Any markdown folder would work. Obsidian makes graph and search usable, and setup costs an hour you recover in a week.

### Why Claude Code

Three features. Persistent file-system access. Tool use. Configurable instructions via `CLAUDE.md`. Other clients will reach parity. The template ports when they do. Today Claude Code is the shortest path.

### Why a vault and not a database

Legibility. Every file in this system should be readable by eye. No opaque storage. No "what does that table even contain." If Claude disappears tomorrow the vault is still there and still makes sense to whoever opens it. That property is cheap to preserve and expensive to recover.

## What is not included

No web UI. No mobile app. No hosted service. The system runs on your machine against your vault.

No multi-user support. This is a personal operating system.

No built-in scheduling. If you want reminders at specific times, wire in a hook or a cron job.

## Extension points

### Custom slash commands

Drop a new skill folder into `.claude/skills/` with a `SKILL.md`. Claude Code picks it up. `/review` for code review. `/journal` for daily notes. `/brief` for meeting prep. Whatever your life actually contains.

### Additional memory files

The default set is a floor, not a ceiling. Add files as needs expand. Update `MEMORY.md` so the new ones load when they should. Organize by topic, not date.

### New hooks

Any event Claude Code exposes is a hook point. Add a script to `scripts/hooks/`. Register it in `.claude/settings.json`. The hook fires.

The template ships `settings.json` empty (`{}`). A minimal example that runs a Python script at session start:

```json
{
  "hooks": {
    "SessionStart": [
      { "type": "command", "command": "python scripts/hooks/inject_date.py" }
    ]
  }
}
```

See [`docs/obsidian-setup.md`](docs/obsidian-setup.md) Layer 5 for more examples and the events Claude Code exposes.

## Technical: the `_system/` folder

The user-visible files in your vault — `Command Center.md` and `To-Do.md` — are deliberately clean. Plain markdown, no YAML frontmatter, no embedded query blocks. You read them every day; they have to be readable.

State the system needs lives behind that, in `_system/` at the vault root. You can ignore this folder until you want to know how the machinery works.

Four files ship there:

- **`last_session.md`.** Frontmatter holds the session counter (`session: N`) and the date of the last `/wrap`. Body holds the recap and open-threads list. `/start` reads this for re-entry detection. `/wrap` overwrites it.
- **`hot.md`.** One paragraph of in-progress context overwritten by every `/wrap`. Deliberately low-fidelity. `/start` reads it to recover where you left off.
- **`Session Log.md`.** Append-only narrative. One block per `/wrap`. Rarely loaded back into the model. Exists for pattern analysis and so future-you can audit past-you.
- **`memory_firings.log`.** One line per memory that actually shaped a response in a session. `/wrap` appends. `/audit` reads, once enough sessions accumulate. See [`docs/memory.md`](docs/memory.md) for the bootstrap-gate detail.

The split is the design. Anything you read every day is in the user-facing files. Anything the machinery needs is in `_system/`. Swap the slash commands for different ones, or extract `/wrap` Phase 1 into a Python script — the shape doesn't change as long as the two layers stay separate.

If you want to grow the user-facing side toward the elaborated patterns described in [`docs/protocols.md`](docs/protocols.md) — frontmatter on Command Center, inline `#waiting` tags with a Dataview aggregation, custom skills like `/audit` extended with your own checks — that's the path. None of it is required. The simple shipped state runs the loop.

## Lineage

This started in early 2024 with me building and using custom GPTs. They were a step forward from the standard chat, but for any serious use they were weak and drifted easily. They needed more memory and more readily available context. I wanted a "2nd Brain," a functional assistant that remembered everything. My research uncovered Obsidian, which I liked because it could all stay on my machine, no cloud. The local-only constraint came first and never moved. Every architectural choice since has filtered through it.

By late summer 2025 I had a name for the pattern I was reaching for: RAG. RAG, Retrieval-Augmented Generation, is the canonical name for what this whole system does. Store knowledge locally and let the model query it on demand. Ground every answer in your own notes instead of the model's general training. By September 2025 I'd evolved a playbook: save chats to Obsidian then cut/paste them into ChatGPT to provide context. This worked but was clunky. The problem was tooling, I couldn't bring it all together. I tried using n8n to connect ChatGPT to Obsidian, but was way over my head and ChatGPT couldn't walk me through it. Node names changed under me, webhooks failed, and file paths broke, I was just flailing around. So, I stayed in custom GPTs and kept pasting in markdown files for context. 

One of my GPTs was a therapist and it exceeded my expectations. I made it Internal Family Systems (IFS) and somatics flavored, ADHD-aware. It uncovered patterns and insights human therapists hadn't. It was the first time any of this technology felt like it was actually in the room with me.

In early 2026 I came back to the 2nd Brain problem, this time in Claude Code. I have zero coding background, but with Claude that didn't matter. I was able to attach Obsidian and make it function smoothly as extended memory. I moved the therapist over from GPT and with the vault attached it worked even better. Everything else evolved out of that: the Command Center, the Chief of Staff role, the memory tier, and the Laws. The nervous-system-aware framing in the operating principles comes from a skill that was already running against my actual life.

In early April 2026 Andrej Karpathy posted a gist titled "LLM Wiki", a markdown folder maintained by a model, framed as a personal knowledge base written for an LLM reader. It went viral on X. My quest had been validated.

Between Karpathy's post and this document, multiple open-source implementations of the same basic pattern have shipped. A partial list: Jereme Strange's [ADAM Framework](https://github.com/ajsupplycollc/Adam) (MIT-licensed, five layers, closest architectural cousin to this one, and the source of two adapted scripts in my local setup; full credit in [CREDITS.md](CREDITS.md)), Caleb Peavy's [`unmutable/ai-chief-of-staff`](https://github.com/unmutable/ai-chief-of-staff) (which shares this repo's name and deserves the namespace nod), [`kbanc85/claudia`](https://github.com/kbanc85/claudia), MemPalace, and the earlier Hermes Agent work from Nous Research. That's a good sign. Markdown plus a language model is now a serious substrate for personal operating systems. The pattern is becoming popular because it's badly needed and so damn helpful.

This repo is one of those implementations, built by a non-coder with ADHD for non-coders with ADHD. It's been lived in for over a hundred sessions against real paying client work and a public platform build. Every rule in this document came out of that work. Nothing here is theoretical.

Your Chief of Staff should be different. Start with this one. Keep what works and cut what doesn't. The code can be copied but the rest cannot, it must grow toward your specific psyche. 

## Where to go next

Back to the [README](README.md) for the short version.

Into [`docs/obsidian-setup.md`](docs/obsidian-setup.md) for the practical wiring guide.
