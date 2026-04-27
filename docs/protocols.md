# Protocols

Three commands, two files, one loop. Everything else in this system is support.

The three commands are `/start`, `/sync`, and `/wrap`. The two files are `Command Center.md` and the to-do list. The loop runs every day you work. At session start the model reads the current state of the files. During the session it might check in with `/sync`. At session end it writes back. The files hold the state between sessions.

This doc covers each command in operating detail. What files it reads. What it writes. What its failure modes look like. It also covers the state files and what belongs in them. `ARCHITECTURE.md` describes each command in a paragraph. This one goes down to the wiring.

## The loop

State in this system lives in four places.

1. `Command Center.md`. Current priorities, week ahead, state check.
2. `To-Do List.md`. Tasks by quadrant, with a waiting-for table auto-aggregated from tags.
3. `.claude/memory/`. Persistent memory files. Covered in [`memory.md`](memory.md).
4. Session logs. Append-only narrative record. One entry per `/wrap`.

`/start` reads the first three. `/sync` and `/wrap` write to them. Session logs grow monotonically and are rarely loaded back into the model.

That's the whole cycle. The commands are short. The state files carry the value.

## `/start`

Opens every session.

**Reads.** Four files in parallel. `Command Center.md` for current priorities. A session pointer (`_system/last_session.md` in my setup) that records when the last session was and what threads were open. A hot-context snapshot written by the previous `/wrap`, deliberately low-fidelity, used to recover in-progress state quickly. The to-do list.

If MCP servers are wired in: Gmail gets queried for unread human senders in the last two days, filtered to exclude promotional categories. Calendar gets queried for today's meetings. An optional semantic-search helper surfaces cross-domain vault connections that would otherwise get missed.

**Writes.** Nothing at the file layer. `/start` is read-only by design.

**Produces.** A Must / Should / Could briefing, then flags for anything overdue in the waiting-for table. My setup prefixes the briefing with a short motivational opening, because the person reading it has ADHD and benefits from a little energy at the top. Skip that layer if it isn't useful to you; the briefing stands on its own.

**Re-entry case.** If the last session was three or more days ago, the briefing shortens. No guilt about the gap. Lead with what's still in place. Offer one easy entry point. The loop assumes skipped days and recovers gracefully.

**Failure mode.** The main one is a stale Command Center. If `/wrap` didn't run at the end of the last session, `/start` is briefing against out-of-date state. The audit is the safety net.

## `/sync`

Mid-session checkpoint. Optional. Reads whatever's already in context, pulls any relevant memory files, and writes updates to memory, the Command Center, or the to-do list if priorities shifted since session start.

Most sessions don't need it. Long ones do. What you decided two hours ago can fall out of context before `/wrap` comes around, and on a four-hour session `/wrap` will end up reconstructing decisions the model can no longer see clearly.

The failure mode is being too casual about what goes to memory. A `/sync` that writes every passing thought to disk is noise. A `/sync` that catches the one real decision from the last hour is a save.

## `/wrap`

Closes every session. Two phases.

**Phase one: the deterministic work.** Checked tasks (`- [x]`) in the four to-do quadrants move into the `## Done` section at the bottom of the file. The Command Center's in-body `**Last updated:**` line gets set to today's date. The session counter in `_system/last_session.md` frontmatter gets incremented. One block gets appended to `_system/Session Log.md`. `_system/hot.md` and `_system/last_session.md` get overwritten with the current state. If the new session number is divisible by seven, the wrap output flags audit-due.

User-facing files (`Command Center.md`, `To-Do.md`) stay clean — no YAML frontmatter, no machinery markup. State the system needs (session counter, hot context, session log, firings log) lives in `_system/` so the user's daily-read files stay readable.

None of phase one needs the model's judgment. It's file shuffling, and it should be fast. The template ships these as instructions inside the `/wrap` skill; you can extract them into a small Python script that runs first if the shuffling gets old.

**Phase two: the thinking.** The model reflects on what actually shipped this session. Saves the right things to memory, updating existing files where possible and creating new ones where a new topic emerged. Checks whether any part of the session belongs in the waiting-for table. Suggests what to pick up next time.

**Firings log.** If any memory actually fired during the session, `/wrap` appends one line per firing to `_system/memory_firings.log`. This is the instrumentation that makes decay analysis possible. Described in [`memory.md`](memory.md).

**Failure mode.** Skipping the automation phase and going straight to the thinking. The tasks don't move, the Command Center date doesn't update, and `/start` next session operates on stale state. The automation phase runs first for exactly this reason.

## `/audit`

Periodic integrity check. Run roughly every seven sessions, or whenever the briefing surfaces an audit-due flag. Reads `MEMORY.md` and every file it points to, every skill file in `.claude/skills/`, the Command Center, and the to-do list.

The checklist covers redundant rules, stale memories, dead-weight files, broken wikilinks between memory and vault source files, and skill instructions that have drifted from what the system actually does. Findings come back as a report. The human picks which fixes to make.

The audit also reads the firings log and surfaces memories that haven't fired recently. This analysis stays dormant until the log holds ten distinct sessions of data, because before that the tool can't distinguish a dormant memory from one that hasn't had a chance to fire. See [`memory.md`](memory.md) for the bootstrap-gate detail.

Letting the audit backlog grow is the failure mode. If the counter passes seven and the audit isn't run, the rules file keeps accumulating and the system starts contradicting itself. The audit-due flag in the `/start` briefing is the nudge.

## Command Center

One markdown file at the vault root. The single source of truth for priorities.

The skeleton:

```markdown
# Command Center

**Last updated:** 2026-04-22

## Your Lanes

### Lane 1: [name]
[One paragraph. Current status, active work, next action.]

### Lane 2: [name]
...

## This Week
**Top priority:** ...

## State Check
- Energy: ...
- Biggest blocker: ...
- Next action: ...
```

No YAML frontmatter. The user reads this file in Obsidian; the simple in-body `**Last updated:**` line is what `/wrap` bumps. Current lanes of work with status. A weekly focus section listing what actually matters right now. A state check covering energy, blockers, and the very next action.

What doesn't go here: long histories, deep strategy documents, anything that would make the file long enough that `/start` can't scan it in one read. Those belong in dedicated docs that the Command Center links to.

One file, because a system with five different "where are my priorities" files has no priorities. The Command Center is the forcing function that makes the human pick.

## The quadrant system

The to-do list is a single markdown file organized into four quadrants.

- **Do Now.** Urgent and important.
- **Schedule.** Important, not urgent.
- **Defer.** Urgent, not important.
- **Later.** Not urgent, not important.

The quadrants are Eisenhower-derived but intentionally drift-tolerant. Do Now in practice holds what the human wants front-of-mind today, which isn't always strict urgent-plus-important. The system respects that. The quadrants are a priority shape, not a logic puzzle.

**Waiting For is its own table** at the bottom of the file. Add a row whenever you hand something off or start waiting on someone: what, who, started, follow-up date, status. `/start` reads the table and flags rows where the follow-up date has passed.

The simple table is the floor. As the system grows, you can move to inline `#waiting` tags with a Dataview aggregation block — see the Technical section in `ARCHITECTURE.md`. The tag pattern is more flexible; the table is more readable on day one.

## Session logs

Append-only narrative. One entry per `/wrap`. Never loaded back into the model during a normal session.

**What they're for.** Pattern analysis over time. Recovery when the story has drifted. Something to feed back into the model when you want it to look at your own history from a distance and tell you what's changed.

**What they're not.** Daily context. `/start` doesn't read session logs. They're not part of the working memory tier. The hot-context snapshot written by `/wrap` carries the "where did we leave off" signal in one paragraph. The session log carries the full narrative for later use.

Keep them long if you want. Nothing is loading them on the hot path.

## The whole shape

Three commands. Two active state files. A memory directory. A log of audits and firings.

The commands are intentionally small. Each one is a short set of plain-English instructions that tells the model what to read, what to ask, and what to save. Most of the engineering is in the state files and the memory directory. The skills themselves are almost nothing.

The pattern is portable to any markdown-reading model. A different model next year reads markdown the same way this one does; the skills are short enough to rewrite in an afternoon. What's not portable is the months of memory a particular user accumulates. The rest of the system mostly exists to protect that.
