# Chief of Staff

A Chief of Staff built on Claude Code and an Obsidian vault. Designed as an ADHD prosthetic.

Every new conversation with a model starts from zero. It doesn't know who you are, what you're working on, or what you decided yesterday. This repo is a personal operating system to end that. A vault of markdown files, a handful of slash commands, and a memory layer that persists between sessions. The model reads the vault at session start and hands you back an assistant that already knows who and where you are.

It's one of at least ten open-source implementations of the same pattern all posted in the last month. The code can be copied from any of them. What can't be copied is what's around it: a non-coder with ADHD built this one for non-coders with ADHD, and lived in it for over a hundred sessions against real paying client work and a public platform build. The rules in this system were learned. None of them are theoretical.

## The loop

Four commands. One runs once. The other three cycle every session.

- **`/setup`**. Conversational wizard. Asks about you, your lanes, how you stall, what has actually helped you before. Generates `CLAUDE.md`, vault files, and memory.
- **`/start`**. Morning briefing. Reads the Command Center and the To-Do List. Delivers Must / Should / Could. Flags overdue follow-ups.
- **`/sync`**. Mid-session checkpoint. Saves what matters to memory. Optional.
- **`/wrap`**. End of session. Reflects wins. Updates the Command Center. Queues what is open for next time.

## What's here now

This repo currently ships the docs and the architecture writeup. The full template is staged locally and will push next, once a clean-install test has actually been run. Shipping a broken install is worse than waiting a week. That gate has not closed yet.

Today you can read:

- [`ARCHITECTURE.md`](ARCHITECTURE.md). The longer writeup. The loop, the memory model, the operating rules, the design choices. Start here if you want the system explained before you build your own.
- [`obsidian-setup`](obsidian-setup). Step by step wiring guide for Obsidian, MCP servers, plugins, the hook layer. Plain English. No coding background assumed. Paste it into Claude and say do this.
- [`notion-vs-obsidian`](notion-vs-obsidian). Short editorial on why the vault is Obsidian and not Notion. Two paragraphs.
- [`notion-vs-obsidian-deep`](notion-vs-obsidian-deep). The long version. Specifications, pricing, lock-in analysis, recovery stories.

## Who this is for

If you have ADHD, this operating system was built for you. If you don't, it still works just fine. 

## License

MIT.
