---
name: sync
description: Mid-session checkpoint. Saves to memory, flags Command Center or To-Do drift, rotates session context.
user_invocable: true
---

Mid-session checkpoint. Optional. Most short sessions don't need it. Long sessions (2+ hours) usually do.

## Save to memory

Update existing files in `.claude/memory/` rather than creating new ones. The four core files are `user_profile.md`, `preferences.md`, `projects.md`, `session_context.md`. As the system grows, additional files follow the type-prefix convention (`user_*.md`, `feedback_*.md`, `project_*.md`, `reference_*.md`); see `docs/memory.md`.

For `session_context.md`: prepend the new entry at the top with today's date. Scan the file and remove any entries older than 7 days. Keep it current.

## Check Command Center and To-Do drift

If something we worked on this session has shifted lane status, priorities, or the state check, propose specific edits and ask before making them. Don't edit silently.

If new tasks emerged or new waiting-for items came up, propose adding them to `To-Do.md` (rows in the Waiting For table for the latter) and ask before adding.

Keep it short. The point is to save the one or two real decisions from the last hour, not to rewrite everything.
