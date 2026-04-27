---
name: audit
description: Periodic integrity check. Reads memory, skills, vault state. Reports redundant rules, stale memories, broken links, drifted skills.
user_invocable: true
---

Periodic integrity check. Run roughly every 7 sessions, or whenever the briefing surfaces an audit-due flag.

This is a read-mostly skill. Its job is to surface findings as a report. The user picks which fixes to make.

## Read

In parallel:

1. `.claude/memory/MEMORY.md` and every file it points at.
2. Every `SKILL.md` under `.claude/skills/`.
3. `Command Center.md` and `To-Do.md` from the vault.
4. `_system/memory_firings.log`.

## Checklist

Walk through these in order. For each, return findings with concrete file paths and line references where applicable.

### 1. Redundant or contradictory memory

Are any two memory files saying the same thing? Are any two saying contradictory things? List candidates for merging or reconciliation.

### 2. Stale memory

Read each memory file's `description` frontmatter against the actual contents. Does the description still describe what's in the file? Flag mismatches.

For project-type memories: do the projects still exist and look active? Closed-project memories should be moved or marked.

### 3. Index drift

Does `MEMORY.md` list every file in `.claude/memory/`? Is every file in the index actually present? Flag both directions of drift.

### 4. Broken links

Scan memory files and skills for wikilinks (`[[...]]`) and markdown links (`[...](...)`) pointing at vault files. Flag any whose target doesn't exist.

### 5. Skill drift

For each `SKILL.md`, does the skill's described behavior match what `CLAUDE.md`, the docs, and the vault templates actually support? A common drift: a skill references a file or pattern that has since been renamed or removed.

### 6. Decay analysis (gated)

Read `_system/memory_firings.log`. Count distinct session numbers. If under 10, **skip this section** with a short note: "Decay analysis is gated until the firings log holds 10 distinct sessions. Currently at N. Skipping."

If 10 or more, surface memory files that have not fired in the most recent 5 sessions. Don't recommend deletion. Surface for the user to review.

## Report format

Return findings as a numbered list grouped by checklist section. For each finding: what's wrong, where it lives, a one-line proposed fix. Don't make any of the fixes. The user picks.

End the report with a one-line state summary: total memory files, total skills, last audit-counter value, decay-analysis status (gated or live).
