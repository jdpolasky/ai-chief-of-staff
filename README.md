# Chief of Staff

> **Note:** This whole thing is designed for non-coders. The install guide below assumes you've never used a terminal or installed a code project before. If you've done that stuff, skip ahead. Nothing here will gatekeep you out.

> **Have Claude walk you through it.** If you already have Claude in any form (paid or free, browser or phone), paste this whole README into a Claude conversation and say "walk me through this." Claude reads it back to you in plain English, coaches you through the terminal, and helps when something breaks. The doc was written to work both ways.

A Chief of Staff built on Claude and an Obsidian vault. Designed as an ADHD prosthetic for non-coders.

Every new conversation with an AI starts from zero. It doesn't know who you are, what you're working on, or what you decided yesterday. This repo fixes that. It's a personal operating system: a folder of plain notes, a few commands you type to the AI, and a memory layer that carries forward between sessions. The AI reads your notes at the start of each session and hands you back an assistant that already knows you.

A non-coder with ADHD built this for non-coders with ADHD, and lived in it for over a hundred sessions against real client work and a public platform build. The rules in here were learned, not theorized.

## The loop

Four commands. One you run once. The other three cycle every session.

- **`/setup`**. A guided wizard. Asks about you, your priorities, how you stall, what has actually helped you before. Builds the system in about ten minutes.
- **`/start`**. Morning briefing. The AI reads your notes and hands you a Must / Should / Could plan. If you've connected your email and calendar, it surfaces today's events and unread messages too.
- **`/sync`**. Mid-session checkpoint. Saves what matters. Optional.
- **`/wrap`**. End of session. Reflects on wins, updates your notes, queues what's still open for next time.

## Before you start

This install needs a few free programs and one paid subscription. Don't worry if you've never installed anything like this before. Each one has a download link below and a one-line explanation. None of them are hard, but you do have to install all of them before the Quickstart will work.

**1. Claude Code.** This is the AI app you'll be talking to. Not the same as the Claude chatbot in your browser. Claude Code is a separate desktop app from the same company.
Download: https://claude.ai/code

**2. A paid Claude subscription.** Any paid tier works. Free accounts can't run Claude Code. If you already pay for Claude Pro or Max, you're set; the same login works.

**3. Obsidian.** This is the notes app where your Chief of Staff lives. Free.
Download: https://obsidian.md
After installing, open Obsidian and create a new vault. A vault is just a folder where Obsidian keeps your notes. Pick a name like `MyVault` and let Obsidian put it somewhere you'll remember (Documents folder is a fine default). You don't need to add any notes yet. The wizard will fill it in.

**4. Git.** This is a tool that lets you download code projects from the internet. Many computers don't have it installed by default.
Download: https://git-scm.com/downloads
Run the installer and accept all the defaults. You won't need to use Git directly. You'll just type three commands the wizard needs.

**What's a terminal?** A terminal is a window where you type commands instead of clicking buttons. It feels intimidating the first time. It's just an app.

- **On Windows:** press the Windows key, type `cmd`, press Enter. A black window opens. That's your terminal.
- **On Mac:** press Command+Space, type `Terminal`, press Enter. A window opens. That's your terminal.

You'll only need three commands. Copy and paste them.

## Quickstart

You've installed Claude Code, Obsidian (with a vault), Git, and you have a paid Claude subscription. Now:

**Step 1. Open a terminal** (instructions just above).

**Step 2. Download this project.** Copy and paste this line into the terminal, then press Enter:

    git clone https://github.com/jdpolasky/ai-chief-of-staff

You'll see lines of text scroll by. When the cursor stops, the download is done. The project is now in a folder called `ai-chief-of-staff` on your computer (usually in your home folder).

**Step 3. Move into that folder.** Type this and press Enter:

    cd ai-chief-of-staff

`cd` means "change directory." You're telling the terminal which folder to operate in. Nothing visible will happen. That's normal.

**Step 4. Launch Claude Code.** Type this and press Enter:

    claude

Claude Code starts up inside the terminal. You'll see a welcome message and a prompt where you can type. You're now talking to the AI.

> **Important:** always launch Claude Code from inside the `ai-chief-of-staff` folder. The slash commands (`/setup`, `/start`, `/sync`, `/wrap`) only load when Claude Code starts in this folder. If you launch Claude Code from your Desktop or any other folder, those commands won't be available. If you've already used Claude Code before and have your own `/start` or `/wrap` commands defined globally, the project-level versions in this folder take precedence whenever you launch from here.

**Step 5. Run the setup wizard.** Type this and press Enter:

    /setup

The slash at the front is intentional. It tells Claude this is a command, not a regular message. The wizard runs.

**Step 6. Answer the wizard.** It asks four questions to get the system working: your first name, what you do, what your two-to-four lanes are right now (lanes are the tracks your time runs on, like Cash, Career, Family, Creative Work), and the one thing this week that would matter most. After those four, it'll ask if you want to keep going through optional sections or "ship it." Either choice is fine. Optional sections sharpen the system, but you can always come back.

The wizard will also ask where your Obsidian vault is. Give it the full folder path. For example: `C:\Users\YourName\Documents\MyVault` on Windows or `/Users/YourName/Documents/MyVault` on Mac. If you don't know the exact path, open Obsidian, right-click your vault name in the sidebar, and choose "Show in folder." That's the path.

**Step 7. You'll see your first briefing.** The wizard finishes by writing a Must / Should / Could briefing right there in the terminal. That's the system working.

**To confirm it landed:** open Obsidian. You should see two new files in your vault, `Command Center.md` and `To-Do.md`, plus a `_system/` folder where the system keeps its session log and a few housekeeping files. If they're not visible right away, click on the vault name to refresh. The two files at the top are the spine of the system. You'll see them grow over time.

If something didn't work, scroll back through the terminal and look for red error messages. The most common cause is a wrong vault path. If so, run `/setup` again and try a different path.

## What to expect

On day one the system feels thin. The AI doesn't know much about you yet because you've only had one conversation with it. That's normal, it's not broken.

Give it two weeks of real use. Memory accumulates and rules get written down when you correct the AI. The briefings start sounding like they actually know you. The calibration is the system.

## Read more

- [`ARCHITECTURE.md`](ARCHITECTURE.md). The longer writeup. The loop, the memory model, the operating rules, the design choices. Read this if you want the system explained before you commit.
- [`docs/obsidian-setup.md`](docs/obsidian-setup.md). Step-by-step guide to wiring up Obsidian and the optional MCP servers (the connectors that let the AI read your email and calendar). Plain English. No coding background assumed. Once you have the system running, paste this file into Claude and say "do this."
- [`docs/notion-vs-obsidian.md`](docs/notion-vs-obsidian.md). Short editorial on why this uses Obsidian and not Notion.
- [`docs/notion-vs-obsidian-deep.md`](docs/notion-vs-obsidian-deep.md). The longer version of the same argument.

A note on jargon: a few technical words show up in the docs. Here's the short version, so they don't slow you down.

- **Vault**: the folder Obsidian uses to hold your notes.
- **MCP**: short for Model Context Protocol. A way for the AI to read other apps like Gmail and Calendar. Optional. Setup instructions are in `docs/obsidian-setup.md`.
- **Slash command**: a message you type to the AI that starts with `/`. The AI treats it as a command, not regular conversation. `/setup`, `/start`, `/sync`, `/wrap` are the four you'll use.
- **RAG**: short for retrieval-augmented generation. Just means the AI looks at your notes before it answers. That's how the memory works.

## Who this is for

If you have ADHD, this was built for you. If you don't, it still works fine.

## What it costs

This runs on Claude, which is a paid product from Anthropic. I built half of this with the $20/month version but frequently hit the limits. Then I upgraded to the $100/month Max tier and finished it with far fewer limit problems. A lighter user could run it on the cheaper Pro tier. Obsidian is free. The MCP servers are free. The model is the only paid part. No hosting, no database, no other subscriptions.

If you don't already pay for Claude, that's the only floor cost.

## Acknowledgments

This repo lives alongside several open-source personal-AI frameworks that emerged in early 2026. Two of the local support scripts I run draw on the [ADAM Framework](https://github.com/ajsupplycollc/Adam) by Jereme Strange (MIT-licensed). Neither ships in this repo. Full attribution details in [`CREDITS.md`](CREDITS.md).

Andrej Karpathy's April 2026 LLM Wiki gist validated the broader markdown-plus-AI direction and is worth reading. Other implementations in the same wave: Caleb Peavy's [`unmutable/ai-chief-of-staff`](https://github.com/unmutable/ai-chief-of-staff), [`kbanc85/claudia`](https://github.com/kbanc85/claudia), MemPalace, and the Hermes Agent work from Nous Research.

## License

MIT.
