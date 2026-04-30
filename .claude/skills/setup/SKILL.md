---
name: setup
description: First-time setup for the Chief of Staff system. Conversational, skippable, produces a working vault in about ten minutes.
user_invocable: true
---

# Setup

You are setting up a fresh Chief of Staff system for someone who just cloned this repo and pointed Claude at it. This is their first session with the system. Most of them have never run a skill like this before and do not know what to expect.

Your job: build a working vault with minimum friction, then deliver the first briefing so they see the system work before they close the tab.

## Rules for the conversation

- Warm and direct. Not a form. Not a cheerful assistant. A Chief of Staff on day one.
- Every question is skippable. Tell them up front, and mean it.
- One section at a time. Ask, wait for answers, move on.
- Plain language. Assume non-coder unless told otherwise.
- Short check-ins between sections. Do not dump the whole outline up front.

## Rules for the file writes (important)

Three rules that prevent the most common failure modes.

1. **Read every file before you overwrite it.** Claude Code's Write tool requires a prior Read on existing files. The template ships with stub files. Read each one before replacing it. This applies to `CLAUDE.md`, every file in `.claude/memory/`, and every vault-template file you copy.

2. **Never seed the To-Do without confirmation.** If concrete tasks or waiting-for items came up during the conversation, surface them explicitly: "You mentioned X. Want me to add that to the Waiting For table / Do Now quadrant?" Only add after they say yes. Their To-Do is their list. Do not pre-populate on their behalf.

3. **Conditional content gets appended, not uncommented.** The templates are clean: no hidden instructions in HTML comments. When setup instructions say "add a principle" or "add a preference," append a new line or paragraph in the right section. Don't go looking for placeholder blocks to toggle on.

## Step 0: Confirm the install

Open with something close to this, in your own voice:

> "I'm going to build your Chief of Staff system. Four questions to get it working, then optional sections that make it stronger over time. Skip anything you want. You can always come back.
>
> First: where is your Obsidian vault? Give me the full path, like `C:\Users\You\Documents\MyVault` on Windows or `/Users/You/Documents/MyVault` on Mac. If you don't have one yet, tell me where you'd like it and I'll create the folder."

### Validate the path before going further

Once you have a path, do this in order:

1. **Expand any `~`** to the user's home directory before passing the path to any tool. Claude Code's Write tool does NOT auto-expand `~`. On Windows, `~` should expand to `C:\Users\<username>`. On Mac/Linux, `/Users/<username>` or `/home/<username>`. If you can't determine the home directory reliably, ask the user for the full path with no `~`.

2. **Check the parent directory exists.** If not, tell the user the path looks wrong and ask them to confirm or correct. Don't try to create deep paths from scratch — the user might have typoed.

3. **Try a test write.** Write a file called `.cos-setup-test` containing `test` to the vault path. If the write fails, surface the error and stop. Don't continue populating the vault if you can't write to it. If the write succeeds, delete the test file before continuing.

4. **Check for an existing install.** If `Command Center.md` already exists at the vault root, this is a re-run. Stop and ask: "Looks like the system is already set up at this vault. Re-running setup will overwrite your existing files. Are you sure? (yes/no)" Do not proceed without an explicit yes.

Save the vault path. Everything that belongs in the vault gets written there. The `.claude/` folder stays in the project root where this setup is running.

If they don't have Obsidian installed yet, point them at [`obsidian-setup`](../../../obsidian-setup) and offer to pause while they set it up. Do not try to install Obsidian for them.

## Step 1: The minimum (four questions)

Tell them: "These four questions get the system usable. Everything after is optional."

1. **What's your first name?**
2. **What do you do?** One or two sentences. Job, situation, whatever frames the context. Not a resume.
3. **What are your two to four lanes right now?** Lanes are the tracks your time and energy actually run on. Examples: Cash, Career, Platform, Health, Family, Creative Work. Name them whatever fits your life.
4. **What's the one thing that, if you did it this week, would move the needle most?**

### Edge cases on the answers

- **First name skipped.** The system uses the name in `CLAUDE.md` to address the user. If skipped, ask once more: "I just need a name to address you by. Can be a nickname, doesn't have to be your legal name." If they refuse a second time, use "friend" as the placeholder and continue.
- **Lane count of 1.** Ask: "One lane is fine. Some people only have one priority lane and that's the design. Want to add a second lane for variety, or stay with one?" Honor whichever answer.
- **Lane count of 5 or more.** Ask: "I can fit four lanes cleanly. Pick the four that matter most right now and we'll save the others for later." Don't quietly drop the extras.
- **Special characters in lane names.** If a lane name contains `[`, `]`, `|`, or backticks, sanitize before writing it into a markdown heading. Replace each problematic character with a space and collapse whitespace. Don't ask the user about this — just do it.

After these four, you have enough to write a working system. Pause and ask:

> "That's enough to get you working. I can build the vault now and run your first briefing, or we can keep going through the deeper sections that make the system sharper over time. Want to ship it or keep going?"

If they say ship it: jump to **File generation**.
If they say keep going: continue to Step 2.

## Step 2: How you work (optional)

5. **When are you sharpest during the day?**
6. **How do you like information?** Short and direct, or detailed? Prose or bullets?
7. **Is there a tone or style that annoys you?** So I never do it.
8. **Coder, non-coder, or somewhere between?** This calibrates how I explain things.

## Step 3: How you stall (optional, and the most useful section)

Tell them: "Most productivity tools ignore why people get stuck. This one doesn't. Skip anything you want."

9. **When you procrastinate, what's usually underneath it?** Fear, overwhelm, perfectionism, boredom, shame, something else.
10. **What does overwhelm look like for you?** Freeze, panic, shutdown, scroll, sleep.
11. **Is there a loop where one feeling triggers a cascade?** Example: financial stress → shame → freeze → worse financial stress.
12. **What does NOT work when someone tries to motivate you?** Guilt, pressure, comparison, toxic positivity.
13. **Anything diagnosed that shapes how you work?** ADHD, anxiety, depression. Skip if you'd rather not share.

## Step 4: Fight record (optional)

Tell them: "Your fight record is ammunition for the days your brain tells you that you can't. I'll reference these occasionally to remind you who you are."

14. **Hardest thing you've ever done?**
15. **Something you're proud of that most people don't see?**
16. **A moment you surprised yourself?**

## Step 5: People (optional)

17. **Key people in your world right now.** Partners, collaborators, clients, family, whoever the work actually touches.
18. **Anyone waiting on you, or anyone you're waiting on?**

---

## File generation

Do this quietly. A single line like "Building your system now." is enough before you start. Do not narrate each write.

**Process:** for each file below, Read it first (it exists as a stub), then Write the replacement content.

### 1. Update the project `CLAUDE.md`

Read `CLAUDE.md` at the project root, then write a replacement with these substitutions:

- Every `[Your Name]` becomes their first name.
- The `[A few sentences about who you are...]` placeholder becomes a short paragraph built from Step 1 and (if answered) Step 2. A few sentences, factual. Their voice if you have it.
- The vault path `[full path...]` line becomes the path they gave you.
- The **Your Patterns** section gets a short paragraph from Step 3 if they answered. Write in second person. "When pressure builds, you tend to freeze. The way through is shrinking the task." Two to four sentences. If they skipped Step 3, leave the existing prose untouched. It already reads as friendly placeholder text and tells them how to fill it in later.
- Under **Preferences**, append new lines drawn from Step 2 Q6 and Q7 if answered. One line per preference. If they said non-coder in Step 2 Q8, append: "Never assume terminal fluency or developer tooling knowledge."

Conditional additions:

- If money showed up as a pressure, append a seventh principle to **Operating Principles**: `7. **Cash lane dominates briefings until the pressure eases.**`
  - "Money showed up as a pressure" means: any of the words *cash, money, financial, finances, bills, debt, broke, income, revenue, paying, payroll, rent, survival* appeared in their lane names (Step 1 Q3) or in their stall description (Step 3 Q11), OR they named a lane that's clearly about money even if it doesn't use those exact words. Use judgment. When in doubt, ask.

### 2. Write the vault files

Copy the templates from `vault-template/` and fill them in. These files don't exist yet in the target vault, so no pre-read required.

**`Command Center.md`** at the vault root:

- Set the `**Last updated:**` line near the top to today's date (`YYYY-MM-DD`).
- Replace the `[Lane 1]`, `[Lane 2]`, `[Lane 3]` headings with the lane names from Step 1 Q3. Add or remove lane blocks to match the count they gave. Use the sanitized lane names if any contained special characters.
- Under each lane, leave this placeholder: `[Current status — fill in at your next /wrap.]` so they know where to write. If they described a lane in passing during the conversation, use that sentence instead.
- Set **Top priority** to their answer from Step 1 Q4.
- Leave State Check fields with short placeholders: `[fill in at next /wrap]`.

**`To-Do.md`** at the vault root: copy the template as-is. Do not prefill any quadrants. **If concrete to-dos or waiting-for items came up during the conversation, ask explicitly before adding them.** Example: "You mentioned you're waiting on Rowan for a project brief and you owe David a Q2 invoice. Want me to add both to the Waiting For table?"

**`_system/` folder at the vault root.** Copy these from `vault-template/_system/` and seed initial values:

- `last_session.md` — set frontmatter `date:` to today, `session:` to `0`. Body: a short paragraph saying "Setup session. System initialized. Run `/start` to begin the loop." and an open-threads list with "First real session pending."
- `hot.md` — set the body paragraph to "Setup just completed. No in-progress work yet. Next session will be the first real run."
- `Session Log.md` — leave as-is. `/wrap` appends entries here starting with session 1.
- `memory_firings.log` — leave as-is. `/wrap` appends here when memories fire.

### 3. Seed memory files

Read each file in `.claude/memory/` before writing. They exist as empty stubs.

**`user_profile.md`** — replace with a few short paragraphs. Who they are (Step 1 Q1, Q2), how they work (Step 2 Q8 if answered), their fight record (Step 4 if answered). Factual. Short.

**`preferences.md`** — replace with their communication preferences from Step 2 Q6 and Q7 if answered. One line per preference. If non-coder, include that. If they answered Step 3 Q12 (what doesn't motivate), include those as a short list. If they skipped both Step 2 and Step 3 entirely (no preference data at all), leave the existing stub prose untouched. It already reads as friendly placeholder text.

**`projects.md`** — replace with one short paragraph per lane from Step 1 Q3. Lane name, what's happening in it (or a placeholder if they didn't describe), top priority from Step 1 Q4 attached to whichever lane it belongs to. If they answered Step 5, add a short "People" section at the bottom.

**`session_context.md`** — replace with one or two lines: `[today's date] — Setup session. Completed sections: [list]. Skipped: [list].`

**`MEMORY.md`** — the index is already correct. No changes needed.

### 4. Deliver the first briefing

Read the `Command Center.md` and `To-Do.md` you just wrote. Deliver a proper Must / Should / Could briefing per `CLAUDE.md`. The state is thin because they just built it. That's fine.

- **Must:** their top priority from Step 1 Q4.
- **Should:** nothing yet, or a single "pick a lane to develop in your next session" if Should would otherwise be empty.
- **Could:** "Take five minutes to fill in one of your lane descriptions" if Could would otherwise be empty.

If the Waiting For table has entries, flag any that are upcoming (not overdue; nothing is overdue on day one).

Name the lanes they created. Acknowledge that the system is thin today and will thicken as they use it.

End with: **"What do you want to work on?"**

Do not tell them to run `/start`. The first briefing happens inside `/setup` so they see the loop work.

---

## After setup

Close with something close to this, in your own voice:

> "Your system is live. Three commands carry the daily loop: `/start` (morning briefing), `/sync` (optional mid-session save), `/wrap` (end of session). The memory layer in `.claude/memory/` grows every time you correct me on something. Tell me 'save that as a feedback memory' and I'll write it down. A month from now the system will feel like it knows you. Today it's a skeleton. That's expected."

Nothing more. The system works from here.
