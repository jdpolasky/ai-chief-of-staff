---
name: start
description: Morning briefing. Reads vault state, delivers Must/Should/Could briefing, flags overdue waiting-for items.
user_invocable: true
---

Morning briefing.

## Read the state (in parallel where possible)

1. `Command Center.md` from the vault (path is in `CLAUDE.md`).
2. `To-Do.md` from the vault.
3. `_system/last_session.md` — what shipped last time, what's open. Frontmatter has the last session number and date.
4. `_system/hot.md` — low-fidelity in-progress snapshot from last `/wrap`.

If MCP servers are connected: check Gmail for unread human senders in the last 24 hours, and check today's Calendar.

## Re-entry check

Look at the `date:` field in `_system/last_session.md` frontmatter (or the `**Last updated:**` line in Command Center if last_session.md hasn't been written yet).

- If today's date: this is a continuation of an active stretch. Brief normally.
- If 1-2 days ago: brief normally, mention the gap in passing only.
- If 3+ days ago: shorten the briefing. Lead with what's still in place from `last_session.md`. Offer one easy entry point. No guilt about the gap.

## Wins

If `To-Do.md` has tasks marked `- [x]` that haven't been moved to Done yet, acknowledge them as wins and offer to move them. (`/wrap` normally handles this; if `/wrap` didn't run last session, the items will still be in their quadrants.)

## Briefing

Deliver a Must / Should / Could briefing per the structure in `CLAUDE.md`:

🔴 **Must** — the one thing that matters most today
🟡 **Should** — 1-2 items worth attention if momentum is good
🟢 **Could** — a quick win under 15 minutes to build early momentum

Pull from the Command Center's `Top priority` and the `Do Now` quadrant.

## Flags

- **Waiting For:** scan the Waiting For table in `To-Do.md` for any rows where `Follow Up By` has passed. Flag each one.
- **Audit due:** if the session number from `_system/last_session.md` is divisible by 7 and the audit hasn't run recently, mention it.

End with: **"What do you want to work on?"**
