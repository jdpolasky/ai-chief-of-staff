# The feedback loop

The model does not get smarter. Weights don't update between sessions. What does change is the set of rules, preferences, and facts the model reads before every conversation. When the model does something I don't want, I tell it. The correction gets written down. The correction loads at the start of the next session. Next session the model doesn't make the same mistake, because it walked into the session carrying a rule that wasn't there before.

That loop is the part of a personal operating system nobody sells you on, because on day one nothing has been saved and the model is behaving generically. A few weeks in, it is the reason the whole thing works.

This doc covers the loop. What the moment of friction looks like. How a correction turns into a memory file. What one of those files actually contains. And what compounds over time.

## The moment of friction

A correction starts with the model doing something I don't want. Small example: I ask for a quick scan and get back a ranked top-ten production. Bigger example: I mention an unrelated project in passing, the model spins off and builds something I didn't ask for, and we both lose an hour.

Most assistants stop here. You correct the model in the current conversation, it course-corrects, and next session it makes the same mistake again because the correction existed only in the chat history. The model starts fresh. Whatever you taught it last time is gone.

The loop starts when the correction goes somewhere that survives the session.

## Capturing the correction

Every correction likely to come up again gets a file in `.claude/memory/` with `type: feedback`. Seventy-six of those exist in my vault right now.

In practice I don't write these files by hand. When the model does something I want to change, I tell it "save that as a feedback memory" and the model writes the file itself: it picks the filename, drafts the rule, the why, and the how-to-apply, and adds a line to `MEMORY.md`. I review the draft and tighten anything that's wrong. Writing them by hand is possible but slower.

The review is the load-bearing step, and it's worth naming what's at stake. The same model that just made the mistake is drafting the rule meant to prevent the mistake. If you rubber-stamp the draft, the rule reflects the model's interpretation of its own failure, which can be wrong in subtle ways. Too narrow. Too broad. Quietly self-exculpating ("the user didn't specify clearly enough..."). Read each draft like an intern wrote it, because that is closer to the truth than treating it as durable policy. Reject anything that sounds like the model letting itself off the hook. Tighten rules that try to cover more ground than the actual moment justified.

A common shape is rule, why, how-to-apply:

```
---
name: Don't inflate quick tasks
description: Quick scans stay quick. Don't turn a lookup into a ranked top-N deliverable.
type: feedback
---
Rule: When I ask for a quick check, produce a quick check. Don't inflate it into a ranked production.

**Why:** Logged after I spent fifteen minutes on what was supposed to be a two-minute scan. The ranking was more effort than the task.

**How to apply:** Before producing output, check whether the original ask was a scan or a full analysis. When in doubt, ask.
```

Three pieces. The rule. The why. The how-to-apply. None of them are ceremony. Some of my feedback files use this literal structure. Others use ordinary section headings to organize more complex corrections. The shape matters less than the three pieces being present somewhere in the file.

The rule is what the model needs to change. The why is what lets the model handle edge cases later, because a rule without context is brittle. The how-to-apply is what makes the rule fire at the right moment.

A feedback memory without the why is the most common failure. The model follows the rule mechanically, runs into a situation the rule's author didn't anticipate, and either misapplies the rule or ignores it. The why gives the model something to judge with.

## How it loads

`MEMORY.md` is the index. Every feedback file gets one line:

```
- [Don't inflate quick tasks](feedback_quick_task_inflation.md) — scans stay quick, don't ranked-produce
```

At session start the model loads `MEMORY.md` in full. The descriptions tell it which files are relevant to the current work. A writing session pulls writing-related feedback. An email session pulls email-related feedback. The rest stays on disk.

The important part is that the descriptions are specific. "Writing rules" is useless. "No em-dashes, no marketing verbs, no rhythm pastiche" is specific enough that the model knows when to pull the file.

## Pruning

Corrections stop holding. A rule that made sense during one phase of work stops making sense during the next. The system has to clear dead weight or it drowns in rules that contradict each other.

This happens two ways. The first is ambient: during a session, if a feedback memory fires and the human disagrees with its application, the rule gets revisited. Tightened. Broadened. Cut.

The second is scheduled. Every seven sessions, `/audit` runs a decay analysis against the firings log described in [`memory.md`](memory.md). Memories that haven't fired in a long time get surfaced for review. Most survive. A few get cut because the friction that caused them stopped being a real friction.

Neither mechanism is perfect. Both beat letting the rules file grow until nobody reads it.

## What compounds

The first feedback memory I wrote saved me one round trip. The most recent ones I can't separate from the model's default behavior anymore. The accumulation is what the system actually is, a few weeks in.

My rules are calibrated against hundreds of small moments that only happened in my work. If you installed my `.claude/memory/` folder on your machine, the model would carry the wrong rules into your sessions. The code ships. The calibration doesn't. Anyone using this pattern has to grow their own rules over their own sessions.
