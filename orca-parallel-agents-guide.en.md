# Orca — A Beginner's Guide to Running AI Agents in Parallel

> Based on Windows 11. Written as the next step for people who have already used an AI CLI such as Claude Code.
> If you have never used an AI CLI, read **[Terminal AI Agents — A Complete Beginner's Guide](en.html)** first.
> Estimated time: **10 minutes to install + 20 minutes for your first parallel session**

---

## How to read this document

- **Parts 1–6 are all you need to start using it.** Follow them in order.
- **Open the appendices only when you need them.** They cover Mac/Linux installation, how git worktrees actually behave, script automation, and remote execution.
- **Text in grey boxes** is a command you type into the computer.

---

# Part 1. What Orca is

## 1.1 Definition

**Orca is a program for running several AI coding agents at the same time.**

It does **not** replace Claude Code or Codex CLI. It is a shell that launches several of them and manages them in one window. It is less like changing your car and more like building a car park.

It is made by Stably AI, and it calls itself an **ADE (Agent Development Environment)**.

## 1.2 What changes

Here is how you work today.

```
one terminal -> run claude -> instruct -> wait -> check result -> instruct again
```

One thing at a time. While the agent works for five minutes, you wait. If you open two terminals and run two agents in the same folder, **they edit the same files and tangle with each other.**

Here is how Orca works.

```
Task A -> folder copy A -> Claude Code     ┐
Task B -> folder copy B -> Codex           ├─ all in one window
Task C -> folder copy C -> Antigravity     ┘
```

**There is one core idea: every task gets its own copy of the folder.** Different copies means no shared files to fight over, so nothing collides. Those copies are made using Git's `worktree` feature (see **Appendix B** for how it actually behaves).

## 1.3 Basic facts

| Item | Detail |
|---|---|
| Made by | Stably AI |
| Official site | https://www.onorca.dev |
| Licence | MIT (open source) |
| Form | Desktop application (Windows, Mac, Linux) |
| Latest version | v1.4.195 (as of 2 September 2026) |
| Cost | **The app is free.** It uses your existing subscription (Claude Pro and so on) |
| Traffic path | Nothing goes through Orca's servers. Each CLI talks to its own provider directly |

**What is included**

- Task tabs — one task = one folder copy
- Agent terminals — split the window however you like
- A diff view — comment directly on the changed lines and hand it back to the agent
- A built-in browser — point at a page element and say "fix this"
- GitHub, Linear and Jira integration
- Mobile apps (iOS/Android) — check progress while away
- An `orca` command — drive it from a shell as a script (**Appendix C**)

## 1.4 A name collision to watch for

There are at least three AI agent tools on GitHub called `orca`.

| Repository | What it is |
|---|---|
| **stablyai/orca** | **onorca.dev. The subject of this document** |
| orca-cli/orca | A different project with a similar idea (a Go binary) |
| fmfsaisai/orca | A tmux-based orchestrator |

When searching, include **`orca stablyai`** or **`onorca.dev`**. Without that you will get install instructions for a different project mixed into your results.

---

# Part 2. Installing on Windows

## 2.1 What you need first

Orca **does not install agents for you.** The AI CLI you intend to use must already be installed and logged in.

| Requirement | How to check | If missing |
|---|---|---|
| **Git** | `git --version` | [Beginner's guide, section 3.3](en.html#33-install-git) |
| **At least one AI CLI** | `claude --version`, etc. | [Beginner's guide, Part 4](en.html#part-4-installing-an-ai-agent) |

Orca itself does not require Node.js.

> **Why log in beforehand?**
> Orca reuses the credentials each CLI has already stored. You do not enter any API key into Orca. A CLI you have not logged into will simply show its login screen when Orca launches it.

## 2.2 Download from the official site

1. Go to **https://www.onorca.dev** in a browser.
2. Click **`Download`**.
3. Download the Windows installer (`orca-windows-setup.exe`).
4. Double-click the downloaded file.
5. When the installer opens, **keep the defaults and continue**.

> Windows may warn about an unrecognised publisher. Click **`More info` → `Run anyway`** to continue. Make sure the file came from `onorca.dev` or the [official GitHub Releases page](https://github.com/stablyai/orca/releases).

If you use Mac or Linux, or prefer installing from a terminal, see **Appendix A**.

## 2.3 First launch

The first time you open Orca it asks the following, in order.

1. **Access to your home directory** — so it can find repositories. Allow it.
2. **Whether to import existing settings** — it offers to import `~/.claude`, `~/.codex` and your terminal settings. **Import them.** Your credentials and preferences carry over, which removes most of the setup.
3. **An empty screen** — nothing is there until you add a repository. That is normal.

### Check your shell

On Windows, `Settings → Terminal` lets you choose PowerShell or CMD as the default shell. Leave it on **PowerShell** unless you have a reason not to.

## 2.4 Updates

**It auto-updates by default** on the stable channel.

To check immediately, use **"Check for Updates"** in the app menu. The release cadence is extremely fast (effectively daily). Screens may already differ slightly from this document, so look for things by position and role rather than by exact label.

---

# Part 3. Connecting your AI CLIs

## 3.1 How it works

**Orca detects CLIs that are already installed and logged in, and launches them for you.**

Open `Settings → Agents` to see the detected list. Turn them on or off there and pick a default agent. Over 40 come preconfigured.

## 3.2 Integration depth differs by tool

"Supported" does not mean the same thing for every tool.

| Level | Tools | What you get |
|---|---|---|
| **Deep integration** | **Claude Code**, **Antigravity CLI**, Cursor CLI | Usage and rate-limit display, model hot-swap, hooks, account switching |
| **Auto-setup + status** | Prime Agent, Pi, OMP, Droid, Command Code | Status display, hooks |
| **Auto-setup only** | **Codex**, Grok, GitHub Copilot, Aider, Cline and 20+ others | One-click launch |
| **Register manually** | Any CLI | Type the command into the dropdown yourself |

## 3.3 Claude Code

**No extra configuration.** Install Claude Code, log in once, and Orca reads `~/.claude` automatically.

What you get:

- **Usage and rate-limit proximity in the status bar** — this matters when running in parallel
- **One-click switching between multiple accounts** — it prevents overlapping credential refreshes
- Per-repository hooks and memory files
- The working directory is set to that task's folder when it launches

**Claude Agent Teams** (an agent directing sub-agents) is **off by default.** Turning it on shows sub-agents as expandable child rows in the task list. Leave it off at first; it makes it hard to tell what is doing what.

## 3.4 Codex CLI

It imports `~/.codex`. One-click launch works, but there is **no usage display.** You have to check how much of your ChatGPT allowance you have used outside Orca.

## 3.5 Antigravity CLI (`agy`)

Install and log into `agy` first ([Beginner's guide, section 4.4](en.html#44-install-antigravity-cli-the-successor-to-gemini-cli)) and Orca detects it. **It is at the deep-integration level, including usage display.**

> **Where the documentation and reality disagree**
> Orca's official supported-agent list still shows only the old name "Gemini". The repository source, however, contains Antigravity-specific usage mirroring, hook injection and session-history parsers. The documentation appears not to have been updated.
> **Check the `Settings → Agents` list yourself after installing to be sure.**

## 3.6 The setting you must change — permission bypass is on by default

**Orca attaches a permission-skipping flag by default when it launches an agent.** For Claude Code that is `--dangerously-skip-permissions`.

`Settings → Agents → Agent Permissions` offers two choices.

| Setting | Meaning |
|---|---|
| `Yolo` | Run everything without asking (**the default**) |
| `Manual` | Ask for approval each time |

The reasoning is clear enough. A task folder is a disposable copy, so if something goes wrong you delete the whole thing.

**But that reasoning depends on working inside a Git repository.** Point it at a folder holding original data, or a cloud-sync folder, and the premise breaks. Only files Git tracks come back when you delete and start over.

> **Set it to `Manual` at first.** Move to `Yolo` once you have watched what the agents actually do. Doing it the other way round means an accident before you have had the chance to learn.

---

# Part 4. Creating a project and working in parallel

This is the actual usage. No difficult concepts appear here.

## 4.1 Add a project — point it at a folder

1. Click **`Add Repo`** in the left sidebar.
2. **Choose the folder you want to work in.**
3. Done. Orca reads that folder's git state and takes its default branch as the base reference.

> **The folder has to be a Git repository.** Orca's whole approach leans on git features. If it is not one yet, open a terminal there and run `git init` once.
>
> **Avoid cloud-sync folders.** Sync clients can corrupt a repository by syncing files inside `.git`. Use a plain local path such as `C:\projects\my-project`.

To base tasks on a different branch, adjust it in the repository settings.

## 4.2 Create one task and launch an agent

1. Click **`+`** next to the repository name.
2. **Type a task name.** (Leave it blank and one is generated for you.)
3. Choose the starting reference. **Usually leave it on the default branch.**
4. A launcher appears with your default agent preselected. Pick the agent you want from the terminal's **dropdown** — Claude Code, Codex, Antigravity CLI and so on.
5. The agent starts. **Instruct it in plain English as usual.**

At this point Orca has created **a dedicated folder copy for that task** in the background. You never create or manage those folders yourself.

## 4.3 Add a second and third task — that is the parallelism

**Just repeat 4.2.**

Press `+` again for a second task and launch an agent. Same for the third. Each task has a different folder copy, so **none of them affect each other.**

While the first agent works you can already be instructing the second and third. The waiting disappears.

## 4.4 Split the window to watch them at once

**Drag a task tab to the right or bottom edge of the window.** The window splits so you can see several tasks side by side.

To watch three, drag one to the right and another to the bottom for a three-way split.

## 4.5 Review the results and ship

1. Open each task's **diff view**.
2. If something needs changing, use **`Annotate AI Diff`** to comment on that line. The agent reads it and revises.
3. When you are happy, **commit and push directly from Orca**.

## 4.6 Clean up

Delete a task you no longer need with **one click**. The folder copy and the branch go together.

If unmerged changes remain, Orca shows a review step first. Even on a forced delete it keeps the problematic branch for inspection.

## 4.7 Two ways to use it

**Pattern A — race: the same job across several agents**

Create three tasks and **give the same instruction to three different agents**. The official reasoning goes like this.

> Different agents make different mistakes. Running the same task in parallel is cheaper than sequential retries, and disagreement is itself a signal.

If all three agree, the answer is probably right; if they diverge, that is the spot a human needs to judge. **This is useful for validating analysis scripts** — have three write the same processing and look at where the results fail to match.

**Pattern B — division of labour: different jobs at once**

Assign a different job to each task. Files are isolated, so nothing collides. This is the pattern that actually increases throughput.

## 4.8 Do this once, up front — share dependencies

A new task folder is **a clean copy**. Anything Git does not track — `node_modules`, `.venv`, `.env` — is missing. Reinstalling every time cancels out the benefit of parallelism.

**Fix**: set the paths to share under **`Worktree Shared Paths`** in the repository settings. Do it once, and every task folder from then on shares them.

Managing this through config files (`orca.yaml`, `.worktreeinclude`) is covered in **Appendix B**.

---

# Part 5. Where it runs — local desktop

**This is the default, and it is what most people should use.**

Agents, terminals and the browser all run on your PC. Nothing extra to configure. Installing as in Part 2 leaves you here.

**When it fits**: iterating quickly on a machine with enough capacity. In other words, ordinary daily work.

**Watch out for**: memory. Running many tasks uses a lot of it — this is an Electron app, and each task carries its own folder copy and terminal. **Start with two or three** and find where your machine tops out.

Running on a remote server, checking in from a phone, or spinning up a disposable cloud machine per task are covered in **Appendix D**. Read it when you need it.

---

# Part 6. Things to be careful about

## 1. Your allowance drains in parallel too

Running three agents at once **burns your subscription allowance three times as fast.** Claude Code shows rate-limit proximity in the status bar; watch it and pace yourself.

## 2. The permission bypass default

Re-read section 3.6. Start on `Manual`.

## 3. Only use it inside a Git repository

Orca's safety net is "it is only a folder copy, so delete it." That holds only in a Git repository. **Point it at a folder of original data or documents and you have the permission bypass switched on with no safety net underneath.**

## 4. This is still a young project

The repository was created in March 2026 and ships releases effectively every day. The official documentation and the actual behaviour already disagree in places (the Antigravity listing in section 3.5). If a screen does not match this document, the document is usually the outdated one.

## 5. When not to use it

| Situation | Verdict |
|---|---|
| Code or scripts in a Git repository | **Good fit.** Clear gain |
| Cross-checking the same analysis with several agents | **Good fit.** Pattern A |
| Tidying documents and spreadsheets in a data folder | **Poor fit.** No benefit, added risk |
| You have not yet got comfortable with an AI CLI | **Poor fit.** Learn one CLI first |

---

# Appendix A. Mac and Linux installation, and installing from a terminal

## Windows — from a terminal

```
winget install --id StablyAI.Orca
```

## macOS

Homebrew:

```
brew install --cask stablyai/orca/orca
```

Update:

```
brew upgrade --cask orca
```

To download directly, use `orca-macos-arm64.dmg` for Apple Silicon and `orca-macos-x64.dmg` for Intel. The builds are signed and notarised, though macOS may still ask for confirmation on first launch.

## Linux

Pick a format from the Releases page.

| Format | File |
|---|---|
| AppImage | `orca-linux.AppImage`, `orca-linux-arm64.AppImage` |
| Debian/Ubuntu | `orca-ide_<version>_amd64.deb`, `_arm64.deb` |
| Fedora/RHEL | `orca-ide-<version>.x86_64.rpm`, `.aarch64.rpm` |
| Arch | AUR package |

> **Linux note**: use `orca-ide` in a shell. A bare `orca` may invoke a screen reader program.

## Older and prerelease builds

They are all on [GitHub Releases](https://github.com/stablyai/orca/releases). To pull a release candidate, hold a modifier key while clicking "Check for Updates".

| Action | Target |
|---|---|
| `Shift` + click | Latest RC prerelease |
| `Ctrl` (`Cmd` on Mac) + click | Latest performance-tagged prerelease |
| `Option` + click (macOS only) | Validated local builds |

---

# Appendix B. How task folders (worktrees) actually behave

What Part 4 calls a "folder copy" is a **Git `worktree`**.

## Where they live, and what they are

- **They are real `git worktree` checkouts**, created in a directory Orca manages
- You can `cd` into that path from a terminal and **use plain `git` as normal.** It is not an Orca-specific format
- Each task has its own file space, its own branch and its own terminal session. That is why parallel execution is safe

## Base reference and branch names

- The base ref is usually `origin/main`
- You can also branch from a local branch, **a specific commit SHA**, or a remote branch
- Branch names are derived from the task name. Link a GitHub PR, a Linear/Jira issue or a GitLab MR and the name comes from there instead
- To set it yourself, open **Advanced** in the `Create Worktree` dialog

## Sharing dependencies — three ways

A new worktree is a clean checkout, so anything Git does not track is absent.

| Method | Where | Use for |
|---|---|---|
| **Worktree Shared Paths** | Per-repository settings (GUI) | Simplest. Working alone |
| **`worktree.sharedDirectories`** | `orca.yaml` in the repository | `node_modules` and similar. **Commit it to share with a team** |
| **`.worktreeinclude`** | A file at the repository root | Copying individual files such as `.env` |

macOS uses APFS clone-copying where it can, and symlinks otherwise. Windows and Linux use the symlink route.

## Deletion

- Deleting removes **both the directory and the branch**
- If unmerged commits exist, Orca shows a review step first
- Even on a forced delete, the problematic branch is preserved for inspection

## How many at once

The documentation states no hard limit. The practical constraints are your machine's memory and your subscription allowance.

---

# Appendix C. Automating parallel runs with the `orca` command

Instead of driving the app by hand, you can script it from a shell. Use this to make repetitive parallel work unattended.

## Registering and checking

The `orca` CLI ships with the app but **must be registered under `Settings → General → Orca CLI`** before it works.

```
orca status --json
```
```
orca worktree current --json
```

## Main commands

| Command | What it does |
|---|---|
| `orca worktree create --name <name> --agent <agent> --prompt "<instruction>" --json` | Create a task, launch the agent and send the instruction in one go |
| `orca worktree ps --json` | List active tasks |
| `orca worktree set` | Edit task metadata |
| `orca worktree rm` | Delete a task |
| `orca terminal list --json` | List terminals |
| `orca terminal create` / `split` | Create or split a terminal |
| `orca terminal send` | Send input to a terminal (line break added automatically) |
| `orca terminal wait --for tui-idle --timeout-ms <ms>` | Wait until the agent goes idle |
| `orca terminal read --json` | Read terminal output |
| `orca automations ...` | Create, run and remove scheduled tasks |

Chain `create` → `send` → `wait` → `read` and a whole parallel run becomes a script.

## Gotchas

- **Terminal handles are scoped to the running app.** After an Orca restart, reacquire them with `terminal list`
- **Always pass `--timeout-ms` to `terminal wait --for tui-idle`.** Without it you can hang indefinitely
- For structured coordination between several agents, the documentation says to use Orca's orchestration feature rather than bare `terminal send`
- The executable name varies by environment. If `ORCA_CLI_COMMAND` is set, use that value; in a dev checkout use `orca-dev`; **in a Linux shell outside Orca use `orca-ide`**; otherwise `orca`

## MCP

Orca exposes an MCP server. You can let an agent drive Orca, or let Orca drive agents. Configure it under `Settings → Integrations`.

---

# Appendix D. Running somewhere other than your desktop

Besides the local desktop (Part 5) there are three more modes. You can mix them within one installation.

| Mode | Structure | When it fits |
|---|---|---|
| **SSH targets** | Agents and task folders on a remote machine; editor, diff and UI on your laptop | You already have a VPS or GPU box with the repo and tools set up |
| **Remote Orca servers** | Orca runs continuously on a separate machine; laptop, browser, mobile and automation all connect to the same runtime | Keeping sessions alive. Mobile access |
| **Cloud VMs** | A disposable virtual machine per task, created and destroyed by recipes committed to your repo | When you need full isolation |

Where to configure:

- SSH — `Settings → SSH` (supports jump hosts and Kerberos authentication)
- Remote servers — `Settings → Remote Orca Servers` (pair with another machine, or advertise this one as a server)
- Cloud VMs — `Settings → Experimental`

> **Cloud VM costs are yours.** Orca only runs your create/suspend/resume/destroy scripts; you manage the provider and the billing.

---

# Appendix E. Limits of this document, and sources

## Not verified

- What name `agy` actually shows under in the agent dropdown (the source code indicates support; the documentation still says "Gemini")
- A practical ceiling on concurrent tasks (machine-dependent, and no official figure exists)
- Real-world performance of dependency sharing on Windows, where it falls back to symlinks
- Minimum system requirements (not stated in the official documentation)

## Sources

- [stablyai/orca (GitHub)](https://github.com/stablyai/orca) — repository, licence, releases, source inspection
- [Orca official site](https://www.onorca.dev)
- [Orca Docs](https://www.onorca.dev/docs) / [Install](https://www.onorca.dev/docs/install) / [First 3-agent session](https://www.onorca.dev/docs/first-session)
- [Worktrees](https://www.onorca.dev/docs/model/worktrees) / [Supported agents](https://www.onorca.dev/docs/agents/supported) / [Claude Code in Orca](https://www.onorca.dev/docs/agents/claude-code)
- [Recipe: parallel agents](https://www.onorca.dev/docs/recipes/parallel-agents) / [Orca CLI overview](https://www.onorca.dev/docs/cli/overview) / [Ways to run](https://www.onorca.dev/docs/ways-to-run) / [Settings](https://www.onorca.dev/docs/settings)
- [orca-cli skill guide](https://github.com/stablyai/orca/blob/main/skill-guides/orca-cli.md)

---

*Verified as of 2 September 2026. Orca's release cadence is extremely fast. If the screens differ, this document is the outdated one.*
