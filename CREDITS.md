# Credits

This file documents the lineage of code and concepts that shaped this repo. It is maintained alongside the source so anyone reading can trace where ideas came from and who deserves credit. Attribution here supplements, and does not replace, the per-file notices that live inside derived source files.

## ADAM Framework

**Repository:** https://github.com/ajsupplycollc/Adam
**Author:** Jereme Strange (Strange Advanced Marketing, Miami FL)
**License:** MIT
**Copyright line:** `Copyright (c) 2026 Jereme Strange / Strange Advanced Marketing`

ADAM is an open-source 5-layer persistent AI memory and identity framework. It is the closest architectural cousin to this repo's pattern. Two scripts in my local setup trace to ADAM:

1. `coherence_monitor.py`. **Code-adapted** from ADAM's `tools/coherence_monitor.py`. This is a derivative work. Modifications include: reading Claude Code JSONL session files instead of OpenClaw, removing the SENTINEL daemon architecture, writing alerts to `coherence_alert.json` instead of `reanchor_pending.json`, and adding compaction-event detection. The file-level docstring names ADAM and lists the differences.

2. `nightly_reconciliation.py`. **Concept-adapted** from ADAM's Layer 4 nightly reconciliation. No source code was shared; the conceptual structure (end-of-day automated maintenance that produces a morning brief) was the inspiration.

**Neither script ships in this repo as of the initial public release.** When either ships publicly, the file must also carry the full ADAM MIT copyright line and permission notice, per MIT's attribution requirement for redistributed code. The `coherence_monitor.py` docstring currently cites the historical URL `github.com/strangeadvancedmarketing/Adam`, which has since migrated to `github.com/ajsupplycollc/Adam` (same author). That URL reference will be updated at the same time the script is prepared for public release.

Thanks to Jereme for shipping ADAM openly. Studying it shortened my build significantly.

## Andrej Karpathy, LLM Wiki

**Source:** Gist published early April 2026.

Andrej's public posting of a markdown-plus-model personal wiki validated the broader direction this project was already pursuing. The timing (his post in early April 2026; my build began March 2026) produced a public category that made it possible to write about what I'd been building without explaining the shape from scratch. No code is shared between projects. Influence is framing-level.

## Adjacent implementations

The following open-source projects occupy adjacent space in the same April 2026 wave. None of their code ships here. They are listed so readers can compare approaches, and so the field is named rather than strawmanned.

- [`unmutable/ai-chief-of-staff`](https://github.com/unmutable/ai-chief-of-staff) by Caleb Peavy. Same repo name as this one; different project. Noted here to acknowledge the namespace overlap.
- [`kbanc85/claudia`](https://github.com/kbanc85/claudia). Claude Code session management and skill layer.
- **MemPalace** by Milla Jovovich and Ben Sigman, April 2026. Wings, halls, and rooms memory architecture.
- **Hermes Agent** by Nous Research. Self-improving agent with persistent memory (earlier than the April 2026 wave but in the same lineage).

## Prior intellectual debts

Retrieval-Augmented Generation (RAG) is the canonical name for the architectural pattern this repo implements. The term entered widespread use around 2020 (Facebook AI Research, Lewis et al.). This system applies it to a personal-knowledge-base setting rather than a general-corpus setting, but the pattern is not original. My own first pass at a RAG project used n8n and ChatGPT in September 2025 and stalled on tooling. The 2026 Claude Code version is the same idea running on better infrastructure. See the Lineage section of [ARCHITECTURE.md](ARCHITECTURE.md) for the full sequence.

The operating principles borrow language from Internal Family Systems (IFS) therapy, which predates this project and is not owned by me. Any "part," "Self," "firefighter," or related vocabulary in memory files or skills can be traced to Richard Schwartz's IFS work.

The nervous-system-aware framing came into this project through a custom GPT therapist I built in 2024 and later ported into Claude Code. That skill was the first working piece, and the rest of the system grew outward from it. See the Lineage section of [ARCHITECTURE.md](ARCHITECTURE.md) for the full sequence.

The Eisenhower Matrix (four quadrants of urgent × important) is public domain and used here as a common reference, not a claimed contribution.

## How this file is maintained

When a new script, skill, or concept is adapted from another open-source project, a new section goes here before the code ships publicly. When a script that traces to an external source is prepared for public release, its per-file docstring must include the source repo URL, the source file path, and (if MIT or similar) the original copyright line and permission notice. This file is the checklist, not the substitute for those notices.
