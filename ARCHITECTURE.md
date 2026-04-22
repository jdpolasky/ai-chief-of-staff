# Architecture

Every new conversation with a model starts from zero. It doesn't know who you are, what you're working on, or what you decided yesterday. Minutes are spent at the top of every session re-priming a model on a conversation you already had.

This repo is a personal operating system to end that. A vault of markdown files, a handful of slash commands, and a memory layer that persists between sessions. It runs on your own machine against your own notes. The model reads the vault at session start and hands you back an assistant that already knows who and where you are.

Chief of Staff is the role the model plays once the OS is live. It triages, tracks, briefs, learns, and catches things before they fall.

## What this document is

The short version is the [README](README.md). This is the longer version for readers who want to see the bones before or after they run `/setup`. It covers the loop, the memory model, the operating rules, and the design choices. It's not a user guide. It won't tell you which button to click. It will tell you what's happening when you do.

The template files described below aren't in this repo yet. See the README for what's live today.

## Who this is for

Built by a non-coder with ADHD, for a non-coder with ADHD. The distraction pattern is familiar, discouraging, and drains your life. You lose focus, you forget things, time-blindness degrades your ability to function efficiently. Re-calibration takes longer than it should. The small failures add up and turn into shame. Every operating rule here responds to that, none are theoretical.

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

The minutes at the top of every session you used to lose re-priming a fresh model are draining your precious executive function. A good briefing ends that, and you know where you are before you've written a word.

### `/sync`

Mid-session checkpoint. Optional. Saves to memory, updates the Command Center or the To-Do List, and keeps the system honest halfway through. Most sessions don't need it. Long ones do. What you decided two hours ago can fall out of context before `/wrap` comes around.

### `/wrap`

Closes every session. Reflects back what got done. Saves to memory. Updates the Command Center date. Queues open threads for next time. Rotates stale memory entries out so the next `/start` isn't reading yesterday.

`/wrap` is the command that pays the future version of you.

## Memory architecture

Three tiers, sorted by how often the model reads them. Some it loads every session. Some it touches rarely. Some it ignores until you point at them.

### Tier one: vault source files

The working docs. Command Center. To-Do List. Optionally, source files for each lane of your life you want to track separately: career, research, health, whatever. These are short, factual, current-state. Claude reads them on demand, not every session. You can read them too. They're the single source of truth for what's happening now.

### Tier two: session logs

The narrative record. Append-only. Written during `/wrap`. Rarely loaded back into Claude. They exist so you can reread your own history when you want to, and so future-you can audit past-you when the story has drifted. They're also good for feeding back into your model for research and pattern analysis.

### Tier three: `.claude/memory/`

Claude's persistent memory across sessions. A handful of short markdown files: who you are, what you prefer, what you're working on, what happened recently. Claude reads these at the start of every session. Without them the model meets you new every time. That's how every LLM session works by default. This tier is what breaks the pattern. A file called `MEMORY.md` sits at the top as an index, pointing at the rest.

## `CLAUDE.md`: the operating instructions

Claude Code loads `CLAUDE.md` at the start of every session. This is where your preferences, your verification rules, your operating constraints live. `/setup` writes the first version. You edit it over time as rules surface from real work.

Treat `CLAUDE.md` as a running instruction set, not documentation. Rules go in, they take effect on the next session, they compound. If the model keeps doing something you don't want, write a rule. If the rule holds for a week, it stays. If it doesn't, cut it. The file is the shortest path from a moment of friction to a durable change in behavior.

## Operating principles

Three rules do most of the work.

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

The template ships an empty `scripts/hooks/` directory. Hooks are optional. The base system runs without them. They are where the system bends to your work. Inject today's date at session start. Remind yourself to `/wrap` before closing the terminal. Flag memory files nobody has touched in a month. Scrub private strings before anything goes public. The template ships none of these. Write the ones you need.

Hooks can be any executable. Python is common.

## MCP integration

One MCP is required. [Obsidian MCP](obsidian-setup), because without it the system cannot reach the vault and `/start` has nothing to read.

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

Any event Claude Code exposes is a hook point. Add a script to `scripts/hooks/`. Register it in `settings.json`. The hook fires.

## Lineage

Fall 2025. My first attempt at this was ChatGPT, Obsidian, and n8n. I got close enough to see the shape, but was way over my head using n8n and couldn't attach ChatGPT to Obsidian.

Early March 2026. I started again. I'm not a coder at all but now I had Claude Code (desktop). I made rapid progress.

April 3, 2026. Andrej Karpathy posted a gist titled "LLM Wiki." A hundred articles, four hundred thousand words, maintained by a model inside a markdown folder. It went viral on X. My quest was validated!

Second brain literature goes back a decade. Roam Research and Obsidian proved plain text plus bidirectional links could hold a lifetime of thought. My own IFS therapy produced the language the operating principles borrow from. Every ADHD-having professional I have ever met has been building a private system out of sticky notes and calendar apps and prayer, because the off-the-shelf tools never fit.

Between Karpathy's post and this document, at least ten open-source implementations of the same basic pattern have shipped. That's a good sign. Markdown + a language model is now a serious substrate for personal operating systems. It's becoming popular because it's badly needed and so damn helpful.

This repo is one of those implementations. A non-coder with ADHD built it for non-coders with ADHD. It's been lived in for over a hundred sessions against real paying client work and a public platform build. The code can be copied. The rest cannot. The rules in this document were learned. None of them are theoretical.

Yours should be different. Start with this one. Keep what works. Cut what does not.

## Where to go next

Back to the [README](README.md) for the short version.

Into [`obsidian-setup`](obsidian-setup) for the practical wiring guide.
