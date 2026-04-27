---
name: wrap
description: End of session. Reflects wins, updates Command Center, moves done tasks, writes to session log and memory.
user_invocable: true
---

End of session. Two phases.

---

## Phase 1 — Deterministic file work

Do these first, in order. Don't narrate them.

### 1. Bump the Command Center

Read `Command Center.md` from the vault (path is in `CLAUDE.md`). Find the line `**Last updated:** ...` near the top and replace the date with today's date (`YYYY-MM-DD`). Don't change anything else in the file unless the user has asked you to.

### 2. Move checked tasks to Done

In `To-Do.md`, scan the four quadrants (Do Now, Schedule, Defer, Later) for any tasks marked `- [x]`. Move each one into the `## Done` section at the bottom. Preserve the original wording. Add a date prefix in `YYYY-MM-DD` format if the task doesn't already carry one.

If no tasks were checked, skip this step silently.

### 3. Append a session log entry

Read `_system/last_session.md` to get the current session number from its frontmatter, then increment by 1 (the new value).

Append a block like this to `_system/Session Log.md`:

```
## Session N — YYYY-MM-DD

[Two to four sentences on what actually shipped this session. What changed in the world, not what was discussed.]

**Open threads:** [bullet list, or "none" if everything closed]
```

Use the new session number.

### 4. Overwrite hot context

Overwrite `_system/hot.md` with one paragraph (3-6 sentences) describing the current state at session close. This is deliberately low-fidelity. The next `/start` reads it to recover in-progress context quickly.

### 5. Overwrite last_session.md

Overwrite `_system/last_session.md`. Set the `date:` frontmatter to today and the `session:` frontmatter to the new session number. Body holds the recap paragraph and open-threads list. Same content as the Session Log entry, but as a standalone file the next `/start` reads first.

### 6. Append memory firings (if any fired)

If any memory file in `.claude/memory/` actually shaped a response during this session, append one line per firing to `_system/memory_firings.log`:

```
YYYY-MM-DD | session_N | filename.md | one-line note about how it fired
```

If no memories fired (rare), skip this step.

### 7. Audit counter

If the new session number is divisible by 7, flag at the end of the wrap output: "🔍 Audit due — run /audit when convenient."

---

## Phase 2 — Reflect and save

### Reflect wins

Name what was accomplished this session in a sentence or two. Don't let the user brush past progress. Use the moved-to-Done tasks as evidence if they exist.

### Save to memory

Update existing files in `.claude/memory/` rather than creating new ones. The four core files are `user_profile.md`, `preferences.md`, `projects.md`, and `session_context.md`. As the system grows, additional files follow the type-prefix convention (`user_*.md`, `feedback_*.md`, `project_*.md`, `reference_*.md`); see `docs/memory.md` for the full pattern.

For `session_context.md` specifically: prepend the new entry at the top with today's date. Then scan the file and remove any entries older than 7 days. Keep the file from growing unboundedly.

### Check Waiting For

Did anything get sent, handed off, or committed to this session? If so, propose adding a row to the Waiting For table in `To-Do.md`. Ask before adding.

### Suggest what to pick up next

One or two sentences. Frame as "queued up for next time," not "what you didn't finish."

Keep the whole Phase 2 section short. Prose, not bullet lists.
