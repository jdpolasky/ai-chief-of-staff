# Operating laws

Give an LLM access to your file system, a terminal, and your email, and the failure modes stop being textual. They become permanent. A model that rewrites the wrong file doesn't unwrite it. A model that confidently states a fake date puts that date into an email you later have to correct. The cost of an unprincipled tool-using assistant is measured in undo operations that aren't available to you.

Four rules do most of the work to keep that from happening. Two ship with this template in `CLAUDE.md`, which Claude Code loads at the start of every session. Two more I added over time as feedback memories after real frictions surfaced. They are short. They compound with the rest of memory. Together they are the difference between a helpful assistant and one that creates extra work.

This doc covers the four and why each exists. There are plenty of preference-level rules in any working setup. These four are the ones that matter if you want tool access to be an asset rather than a liability.

## The Operating Constraint

When you flag a problem, the model stops. It diagnoses the root cause. It proposes a plan. It waits for you to say go. Only then does it act.

This is the rule that closes the gap between "I think I understand" and "I am going to act on that." That gap is where most of the damage happens. A model that thinks it knows what you want and takes action is sometimes right and sometimes expensive. The expensive cases include files rewritten in ways that can't be reverted, messages sent to people who weren't supposed to see them, and hours of work lost to an enthusiastic undo.

Closing the gap with a pause is free. The model gets one extra round trip to confirm it read the situation correctly. You get a say before anything changes. It isn't sophisticated and it doesn't need to be.

## The Verification Protocol

Before stating a fact about your life, your work, or your history, the model reads the relevant memory file. If the fact isn't on file, the model says so and asks, rather than inventing.

The rule has a clean test. If the model can't name the source of a claim, the claim doesn't go in the response. "Per your professional profile, you have a JD and an MBA." "I don't have that on file." Those are the two acceptable outputs. There is no third one where the model takes a confident guess.

This rule exists because the whole value of a persistent-memory system depends on the memory being trustworthy. One fabrication and you have to double-check every claim after it. At that point you don't have a memory system, you have a second source of facts that you verify against the first one. The rule costs nothing to follow and keeps the system usable.

## Scope Discipline

Take the stated scope literally. Do not bundle nearby work. Do not substitute a better idea for the one that was asked for. Do not inflate a quick task into a full production. Do not leap from "explain this" to "build this."

The failure mode this rule prevents is the one where you ask for a bug fix and the model also refactors the module nearby, adds a test suite, and updates the README while it's in there. Any of those might be worth doing on its own. All of them attached to a fix you wanted in two minutes is a different kind of mess.

The rule has a corollary. If the model notices scope-adjacent work that looks worth doing, it says so and asks. The user keeps the say on what the session actually covers.

## Execute, Don't Meta-Talk

When the instruction is clear and approved, the first output is the work. Not "on it." Not "I'll start by..." Not a plan the model is about to execute anyway.

This one cost me forty minutes once. I gave a clear instruction, got back a paragraph announcing the work, asked what was happening, got back another paragraph confirming the work was starting, and so on. The rule went into memory the same day.

The principle: announcing is not doing. If the model has what it needs, it produces output. If it doesn't have what it needs, it asks the question. There is no third gear where the model narrates its own process while waiting to begin.

## Where the rules live

Home is `CLAUDE.md` at the project root or in the user's home directory. Claude Code loads this file at the start of every session. New rules take effect on the next session they apply to.

The template ships with two of these four already in `CLAUDE.md`: Operating Constraint and Verification Protocol. They belong at the top layer because the damage they prevent is irreversible, so the rule has to fire before a single keystroke. Scope Discipline and Execute, Don't Meta-Talk live as feedback memories in my own setup. Either home works. Memory files are easier to tune after a near-miss; `CLAUDE.md` rules carry more weight per session. Promote from memory to `CLAUDE.md` once a rule has survived a few rounds of edits and you're sure about the shape.

A copyable version of all four, written as instruction text. Paste what fits your working style into `CLAUDE.md` or into a feedback memory:

```markdown
# Operating Constraint

When I flag a problem, correction, or ask a question about how the system works: stop. Do not execute a fix, move a file, or start building in the same turn. Diagnose the root cause. Propose a plan. Wait for my explicit go ("yes," "do it," "go ahead," or equivalent). Only then execute.

# Verification Protocol

Before stating a fact about my life, career, history, or work, check the relevant memory file first. If the information isn't on file, say so and ask. Never invent names, dates, numbers, or biographical details. When referencing my facts, name the source ("per your professional profile," "from the Command Center").

# Scope Discipline

Take stated scope literally. Do not bundle nearby work. Do not substitute a better idea for what was asked. Do not inflate a quick task into a full production. Do not leap from "explain this" to "build this." If you notice scope-adjacent work worth doing, surface it and ask before acting.

# Execute, Don't Meta-Talk

When an instruction is clear and approved, the first output is the work. No "on it." No "I'll start by..." No plan you're about to execute anyway. If you have what you need, produce the output. If you don't, ask the question. There is no third gear where you narrate your process while waiting to begin.
```

Treat `CLAUDE.md` as an instruction set, not documentation. If the model keeps doing something you don't want, write a rule. If the rule holds for a week, it stays. If it doesn't, cut it. The file is the shortest path from a moment of friction to a durable change in behavior.

Four is a floor, not a ceiling. Once these are in place you will find others. Add them as they show up.
