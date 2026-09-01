# Terminal AI Agents — A Complete Beginner's Guide

> Written so that you can follow along without being good with computers.
> Based on Windows 11. Work through it in order, start to finish.
> Estimated time: **30 minutes to install + 20 minutes for your first session**

---

## How to read this document

- **First time?** Start at Part 1 and read in order. Do not skip.
- **Already used a terminal?** Skip Part 2 and start at Part 3.
- **Text in grey boxes** is a command you type into the computer. Copy and paste it as is.
- Every step has a **"Check that it worked"** item. Confirm it before moving on.

---

# Part 1. Why run AI in a terminal

## 1.1 How this differs from the AI chatbot you already use

When you use ChatGPT or Claude in a web browser, the flow looks like this.

```
You: "Tell me how to clean up this Excel file"
AI:  (explains the method in words)
You: (read it -> open Excel -> do the work by hand)
```

The AI only **talks**. You do the actual work. You upload files one at a time, then copy the answer back out by hand.

A terminal AI agent works differently.

```
You: "Clean up the Excel files in this folder"
AI:  (opens the folder -> reads the files -> edits them -> reports back)
You: (just review it)
```

**There is one core difference: the AI can read and write files on your computer directly.**

| | Web chatbot | Terminal AI agent |
|---|---|---|
| Giving it files | Upload one by one | Reads a whole folder on its own |
| Getting results | Copy and paste out | Saved straight to a file |
| Working across many files | Effectively impossible | Hundreds at a time |
| Repeat work | Start over every time | Set it up once, it handles the rest |
| Memory of past work | Gone when you close the tab | Left behind as files in the folder |

## 1.2 What you can actually do with it

These are things you can do without being a programmer.

**Documents and reference material**
- Turn 100 scattered PDFs into a table of titles and summaries
- Rename files in bulk to a consistent convention
- Pull one specific section out of many Word files and merge them into one

**Data work**
- Find and fix errors in Excel/CSV files
- Merge several tables into one and compute statistics
- Plot data as a chart and save it as an image file

**Research and academic work**
- Rewrite a draft's sentences in an academic register
- Normalise references to a journal's required style
- Write and run a script that processes experimental data

**Everyday office work**
- Fill in a recurring report template automatically
- Gather material from the web and organise it
- Draft many emails at once

**Programming** (if you are interested)
- Build a program from scratch
- Understand and modify code someone else wrote

## 1.3 Answers to the usual worries

**"Do I need to know how to program?"**
No. You say "do this for me" in plain English. You do need to know how to open a terminal and a handful of commands, which Part 2 covers. Thirty minutes is enough.

**"What if it wrecks my files?"**
An AI agent **asks "may I make this change?" every single time** before it modifies a file. Nothing runs without your approval. On top of that, if you follow the safety rules in Part 7 (backups, a dedicated folder), the risk is close to zero.

**"Will my files leak?"**
File contents the AI reads are sent to a server so it can produce an answer. This is the same as uploading a file to a web chatbot. **Do not put personal data, unpublished research data, or company confidential material in your working folder.** Details in Part 7.

**"Does it cost money?"**
A paid subscription is generally required. If you already pay for ChatGPT Plus or Claude Pro, you can use it through that subscription at no extra cost. Google's Antigravity CLI gives you a free allowance when you sign in with a Google account (check the official documentation for the exact limits). Section 4.1 lays this out.

**"Do I need Linux? Do I need WSL?"**
No. **Use it on Windows as is.** Some tools did not support Windows in the past and required WSL (a Linux environment), and a lot of material from that era is still circulating. All three tools now ship a Windows-native installer. See **Appendix D** for how to decide.

**"The black screen scares me."**
That is the most common reaction. In practice you use about five commands; everything else is a plain-English conversation. Think of the black screen as just a window for talking to the AI.

---

# Part 2. Terminal basics — 30 minutes is enough

You are not trying to become a programmer. You learn just enough to give the AI work.

## 2.1 What a terminal is

**A terminal is a window where you give the computer instructions as text.**

Normally you open a folder by double-clicking it with the mouse. In a terminal you **type** `cd foldername` instead. The result is the same. Only the method differs.

The reason this matters is that **AI agents only work this way.** There is no screen to click.

### Open a terminal

1. Press the **`Windows key`** on your keyboard (the one with the window icon, usually next to the left Ctrl).
2. Type **`terminal`** into the search box that appears.
3. When the app named **`Terminal`** shows up, press **Enter**.

A black (or blue) window opens with text like this.

```
PS C:\Users\Jane>
```

This is normal. Here is what it means.

- `PS` = short for PowerShell. The name of the program taking your commands.
- `C:\Users\Jane` = **where you currently are (which folder)**. This is the important part.
- `>` = the signal that says "type a command here". You type after it.

> **Remember this**: a terminal always has a "current location". It is exactly like having a particular folder open in File Explorer. Every command runs relative to that location.

## 2.2 The shape of a command

Most commands look like this.

```
command target -option
```

Here is an example.

```
cd Documents
```

- `cd` = the command (means "move into this folder", short for change directory)
- `Documents` = the target (the folder to move into)

After typing a command you **must press Enter** for it to run. Nothing happens until you do, so if you make a typo, do not panic — just delete it.

## 2.3 Understanding folders and paths

Folders on a computer nest inside each other like a chest of drawers.

```
C:\                          <- the C: drive (outermost)
+-- Users\                   <- the users folder
    +-- Jane\                <- your folder
        +-- Documents\
        +-- Downloads\
        +-- Desktop\
```

Writing that out on one line gives you a **path**.

```
C:\Users\Jane\Documents
```

The backslash (`\`) is the separator between drawers. On some non-English keyboards it is displayed as a currency symbol (for example the won sign on Korean keyboards), but **it is the same character.** Do not worry about it.

### How to avoid typing paths by hand (important)

Typing paths by hand invites typos. There are much easier ways.

**Method 1 — copy it from File Explorer**
1. Open the folder you want in File Explorer.
2. **Click once on the address bar** at the top. The path turns into text.
3. Copy it with `Ctrl + C`.
4. In the terminal, type `cd ` (with **a space** after `cd`), then **click the right mouse button once** to paste.

**Method 2 — open a terminal straight from Explorer (easiest)**
1. Open the folder you want in File Explorer.
2. **Right-click on empty space** inside the folder.
3. Choose **"Open in Terminal"**.

The terminal opens already at that folder. **This is the method you will use most.**

> **Careful**: if the path **contains spaces, wrap it in double quotes.**
> Wrong: `cd C:\My Documents\Research Data`
> Right: `cd "C:\My Documents\Research Data"`

## 2.4 The five commands you must know

This is all you need.

### 1. `cd` — move into a folder

```
cd Documents
```

Moves into the Documents folder.

```
cd ..
```

Two dots means **go up one level (outwards)**.

```
cd \
```

Goes to the very top of the C: drive.

### 2. `ls` — see what is in the current folder

```
ls
```

Lists the files and folders where you are. The same as looking inside a folder in Explorer.

### 3. `pwd` — check where you are

```
pwd
```

Shows the full path of your current location. Use it when you get lost.

### 4. `mkdir` — make a new folder

```
mkdir myresearch
```

Creates a folder called `myresearch` where you are.

### 5. `cls` — clear the screen

```
cls
```

Tidies up a cluttered screen. It clears the display only — no files are deleted.

## 2.5 Handy things to know

| What you want | How |
|---|---|
| Paste | **Right-click** (Ctrl+V also works) |
| Copy | Select text by dragging, then `Ctrl + C` |
| Recall the command you just typed | **Up arrow key** |
| Force-stop a running job | `Ctrl + C` |
| Autocomplete a command | Type the first few letters and press **Tab** |
| Make the text bigger | `Ctrl` + mouse wheel |
| Close the terminal | Type `exit` and press Enter |

**Do learn the Tab key.** Type `cd Doc`, press Tab, and it completes to `cd Documents\` by itself. It prevents typos.

## 2.6 Practise right now

Open a terminal and type the following in order. Press Enter after each line.

```
pwd
```
-> shows where you are.

```
ls
```
-> shows a file list.

```
cd Documents
```
-> moves into the documents folder.

```
pwd
```
-> you can see the location has changed.

```
mkdir ai-practice
```
-> creates a new folder.

```
ls
```
-> the `ai-practice` folder you just made appears in the list.

```
cd ..
```
-> back out again.

**If you got this far, terminal basics are done.** That really is all of it.

### When something does not work

| What the screen says | What it means | Fix |
|---|---|---|
| `...cannot find path` | No such folder | Check the spelling; run `ls` to see the real names |
| `...is not recognized...` | No such command | Check the spelling of the command |
| `Access is denied` | A folder you lack permission for | Try somewhere else |

**No error will break your computer.** Try things freely.

---

# Part 3. Preparation — four supporting programs

Before installing an AI agent, install the programs it runs on.

## 3.0 What you are installing and why

| Order | Program | Why it is needed | Required? | Time |
|---|---|---|---|---|
| 1 | Windows Terminal | The window you talk to the AI in. The old console mangles non-English text | Required | 2 min |
| 2 | Node.js | The engine needed if you install via `npm` | Recommended | 5 min |
| 3 | Git | Used internally by the AI. With it, Claude Code uses Git Bash as its shell | Recommended | 5 min |
| 4 | Execution policy, encoding | Skip it and you get errors later | Required | 3 min |

**All of these are free, safe, official programs.**

> **Why Node.js is only "recommended"**
> AI agents used to be installable only through `npm` (the installer that ships with Node.js). Today Claude Code, Antigravity CLI and Codex CLI all provide **dedicated installers that work without Node.js**. It is still worth having: it gives you a fallback route when an install goes wrong, and a good share of the tools the AI writes for you will use it. **If you are short on time, skip section 3.2 and go to Part 4.**

## 3.1 Install Windows Terminal

Windows 11 nearly always has it already. If the terminal opened fine in section 2.1, **skip this step.**

If not, type this into a terminal (or Command Prompt).

```
winget install --id Microsoft.WindowsTerminal -e
```

## 3.2 Install Node.js (recommended)

Node.js is the underlying engine that runs and installs programs. It is used when you install an AI agent the `npm` way, and often needed to run the tools the AI builds for you.

### Method A — by command (recommended, fast)

Type this into the terminal and press Enter.

```
winget install --id OpenJS.NodeJS.LTS -e
```

It takes a few minutes. When you see `Successfully installed`, it is done.

### Method B — download from the website

Use this if the command does not work.

1. Go to **https://nodejs.org** in a browser.
2. Click the green button marked **"LTS"**. (LTS = the long-term support stable release. Do not pick Current.)
3. Double-click the downloaded file (`node-v24...msi`).
4. When the installer opens, **change nothing and keep pressing "Next"**.
5. If a checkbox reading `Automatically install the necessary tools...` appears, **leave it unchecked.** It is unnecessary and slow.
6. **"Install"** -> then **"Finish"**.

### Check that it worked (do not skip)

**Close the terminal window completely and open a new one.** (Skip this and it will look like the install failed.)

In the new terminal, type:

```
node --version
```

Success looks like this.

```
v24.9.0
```

The numbers can differ. Any version number starting with `v` is fine. (As of September 2026 the LTS line is 24.x, and 22.x is still supported.)

```
npm --version
```

Check this too. A number like `10.9.2` means you are fine.

> **What is `node` and what is `npm`?**
> `node` is the engine; `npm` is the tool that installs programs. Installing Node.js gives you both.

### When it does not work

If you see `'node' is not recognized...`:

1. Confirm you closed and reopened the terminal. (This is the most common cause.)
2. If that fails, **reboot** and check again.
3. Still failing? See section 8.1.

## 3.3 Install Git

Git is a tool programmers use to track file history, and AI agents use it internally. **You do not need to learn it — just have it installed.**

On Windows there is a second reason. Installing Git also installs **Git Bash**, which Claude Code detects automatically and uses as its command shell. The Linux-style commands that fill the internet then work as written, and errors drop noticeably. It is not mandatory, but you are better off with it.

```
winget install --id Git.Git -e
```

To get it from the website, download from **https://git-scm.com/download/win** and install. The installer asks a lot of questions; **leaving every default alone and pressing Next** is fine.

### Check

Open a new terminal and type:

```
git --version
```

```
git version 2.52.0.windows.1
```

Output like that means you are set.

## 3.4 Allow scripts to run (skip it and you get errors)

For security, Windows blocks external scripts by default. You have to lift that for AI agents to run.

Type this into the terminal.

```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

When it asks whether you want to change the execution policy, type **`Y`** and press Enter.

> **Is that dangerous?**
> `RemoteSigned` is the middle setting: "run scripts I wrote myself, and run downloaded ones only if they are signed." It is the standard developers use, and it does not disable security. Because of `-Scope CurrentUser` it applies to your account only, not the whole machine.

## 3.5 Text encoding (for non-English users)

If you work with file names or output in a language other than English, the console can show them as `???` or as garbled characters. This setting prevents that. **If you only ever handle English text, you can skip it.**

Type this into the terminal.

```
notepad $PROFILE
```

Notepad opens. If it asks **"Cannot find the file. Do you want to create a new file?"**, choose **Yes**.

Paste these three lines into Notepad.

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding  = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'
```

Save with `Ctrl + S` and close Notepad. **Close the terminal and open a new one.**

> This file (`$PROFILE`) runs automatically every time you start the terminal. Put it here once and you never touch it again.

## 3.6 Part 3 final check

Open a new terminal and type each of these, confirming that a version number comes back.

```
node --version
```
```
npm --version
```
```
git --version
```

**If all three return version numbers, you are ready.** If any one fails, see Part 8.

---

# Part 4. Installing an AI agent

## 4.1 Which one to choose

Pick one of three. **If this is your first time, install one and get comfortable before adding more.**

| | Claude Code | Codex CLI | Antigravity CLI |
|---|---|---|---|
| Made by | Anthropic | OpenAI | Google |
| Terminal command | `claude` | `codex` | `agy` |
| Cost | Included in Claude Pro (about $20/month) | Included in ChatGPT Plus (about $20/month) | Free allowance with a Google account |
| Writing and documents | Strong | Fair | Fair |
| Writing code | Strong | Strong | Good |
| Install difficulty | Easy | Easy | Easy |

**Recommendations**

- **I want to try it without paying** -> **Antigravity CLI** (section 4.4)
- **I already pay for ChatGPT Plus** -> **Codex CLI** (section 4.3)
- **I already pay for Claude Pro, or documents and research are my main use** -> **Claude Code** (section 4.2)

Installing all three causes no conflicts. Still, start with one.

> **If you came here looking for Gemini CLI**
> Google's `gemini` command (Gemini CLI) **stopped serving individual users on 18 June 2026**. Its successor is **Antigravity CLI (`agy`)**, covered in section 4.4. Older material online still tells you to run `npm install -g @google/gemini-cli`; install it that way today and you will be blocked at the login step. Section 4.4 has the details.

---

## 4.2 Install Claude Code

### Method A — dedicated installer (recommended)

Type this into the terminal.

```
irm https://claude.ai/install.ps1 | iex
```

It takes one to three minutes. No Node.js needed, and it keeps itself updated. **Use this if you are starting out.**

> `irm ... | iex` means "download an install script from the internet and run it immediately." Check that the address is `claude.ai` before you run it. Never use this pattern with an address you do not trust.

### Method B — via npm (if you already have Node.js)

```
npm install -g @anthropic-ai/claude-code
```

Lines of text scrolling past is normal. A few yellow `WARN` messages can be ignored. A red `ERR!` means you should look at Part 8. Requires Node.js 22 or later.

> `-g` means "install for the whole machine." You need it so the command works from any folder.
> Do not use `sudo npm install -g`. It creates permission problems.

**Do only one of the two.** If you already installed via npm, run `claude install` to migrate to the dedicated installer.

### Check that it worked

**Close the terminal completely, open a new one**, then type:

```
claude --version
```

A version number followed by `(Claude Code)` means success.

### Log in

Make a folder to work in and run it there.

```
mkdir C:\ai-work
```
```
cd C:\ai-work
```
```
claude
```

On first run it asks you the following, in order.

1. **Pick a theme (colours)** — choose with the arrow keys and press Enter. Any of them is fine.
2. **Pick a login method** — two options. (The wording shifts slightly between versions.)
   - Sign in with a subscription account -> for Claude Pro/Max subscribers. **Most people pick this.**
   - Sign in with a Console (API) account -> pay-as-you-go, for company or institutional accounts.
3. A browser opens automatically. Sign in to your Claude account and click **"Authorize"**.
4. A long string (a code) appears on screen. **Copy it, paste it into the terminal** and press Enter.
5. It asks whether you trust the folder. Choose **`Yes, proceed`**.

The chat window appears. **You only log in once; after this, typing `claude` starts you straight away.**

### Commands worth knowing

Inside the chat you can use special commands beginning with `/`.

| Command | What it does |
|---|---|
| `/help` | Show help |
| `/status` | Check login state and the model in use |
| `/init` | Analyse the current folder and draft a rules file |
| `/clear` | Reset the conversation (when starting a new topic) |
| `/doctor` | Diagnose installation problems |
| `exit` | Quit |

---

## 4.3 Install OpenAI Codex CLI

### Method A — dedicated installer (recommended)

```
irm https://chatgpt.com/codex/install.ps1 | iex
```

### Method B — via npm

```
npm install -g @openai/codex
```

### Method C — via winget

```
winget install --id OpenAI.Codex -e
```

> **Use only one of the three.** Installing more than one way leaves you with tangled versions that are hard to diagnose later.

### Check that it worked

Open a new terminal and type:

```
codex --version
```

### Log in

```
codex login
```

A browser opens. Sign in with your **ChatGPT account**. ChatGPT Plus/Pro subscribers use the allowance included in their subscription, with nothing extra to pay.

To confirm you are logged in:

```
codex login status
```

### Run it

Move into your working folder and type:

```
codex
```

---

## 4.4 Install Antigravity CLI (the successor to Gemini CLI)

### First, some background — Gemini CLI is finished

On 19 May 2026 Google announced the end of individual-user support for Gemini CLI and the Gemini Code Assist IDE extensions, and **service actually stopped on 18 June 2026**. The successor is **Antigravity CLI**, whose terminal command is `agy`.

| | Gemini CLI (retired) | Antigravity CLI (current) |
|---|---|---|
| Command | `gemini` | `agy` |
| Install | `npm install -g @google/gemini-cli` | Dedicated install script |
| Form | Open source (TypeScript), an npm package | A Google-distributed binary |
| Rules file | `GEMINI.md` | `AGENTS.md` |

**Who can still use Gemini CLI**: holders of a Gemini Code Assist Standard/Enterprise licence, users of Code Assist for GitHub through Google Cloud, and holders of a paid Gemini API key. Individual users outside those categories cannot even log in.

**If you already installed Gemini CLI**, remove it first.

```
npm uninstall -g @google/gemini-cli
```

### Install

Type this into **an ordinary (non-administrator) PowerShell**.

```
irm https://antigravity.google/cli/install.ps1 | iex
```

It installs to `C:\Users\yourname\AppData\Local\agy\bin`, and the install script registers it on your PATH for you.

> If you use Command Prompt (cmd), do this instead.
> `curl -fsSL https://antigravity.google/cli/install.cmd -o install.cmd && install.cmd && del install.cmd`

### Check that it worked

**Close the terminal completely, open a new one**, then type:

```
agy --version
```

A version number means success. If it says `agy` cannot be found, nine times out of ten you did not open a new terminal. If that is not it, see section 8.1.

### Log in

Move into your working folder and run:

```
agy
```

A browser opens automatically. Sign in with your Google account and grant permission; you return to the terminal with a chat window ready. Your credentials are stored in Windows Credential Manager, so **from now on typing `agy` starts you straight away.**

On first run it asks whether you trust the working folder (Workspace Trust). If you created the folder yourself, choose to trust it.

### Commands worth knowing

| Command | What it does |
|---|---|
| `/help` | Show commands and shortcuts |
| `/permissions` | Manage tool permissions |
| `/clear` (or `/new`) | Reset the conversation |
| `/resume` | Continue an earlier conversation |
| `/usage` | Check your remaining allowance |
| `/logout` | Log out (clears stored credentials) |
| `/exit` (or `/quit`) | Quit |

### Updating

Running the install script again upgrades you to the latest version.

```
irm https://antigravity.google/cli/install.ps1 | iex
```

---

# Part 5. Your first session — actually giving it work

## 5.1 Prepare a working folder

**An AI agent only handles files inside the folder you launched it from.** That is a safety feature as much as anything.

Do not launch it on your Desktop or in `C:\Users\yourname`. That would let the AI rummage through every file on the machine.

Make a practice folder.

```
mkdir C:\ai-practice
```
```
cd C:\ai-practice
```

## 5.2 Make a practice file

There is nothing to do in an empty folder, so create one file to work with.

```
notepad notes.txt
```

Notepad asks whether to create the file. Choose **Yes**, write a few lines, save with `Ctrl + S`, and close it.

Example:
```
January 2026 revenue: 12,000
February 2026 revenue: 14,500
March 2026 revenue: 9,800
```

## 5.3 Run the AI and talk to it

```
claude
```

(If you installed Codex, type `codex`; for Antigravity CLI, `agy`.)

When the chat window appears, **just talk to it in plain English.**

Try this as your first message.

```
Check what files are in this folder and summarise their contents
```

The AI will look through the folder, read `notes.txt`, and summarise it.

Next, try this.

```
Turn the revenue data in notes.txt into a table, calculate the average and
the month-on-month change, and save it as revenue-summary.md
```

## 5.4 Understanding approval prompts — the most important part

When the AI is about to **modify or create a file**, you see a screen like this.

```
About to create file: revenue-summary.md

  1. Yes                         (allow once)
  2. Yes, and don't ask again    (allow from now on)
  3. No, tell Claude what to do  (refuse and redirect)
```

Choose with the arrow keys and press Enter.

**Rules for beginners**

- **Read-only actions** -> allow freely with `1. Yes`
- **Creating a new file** -> `1. Yes`
- **Editing or deleting an existing file** -> **read it carefully** before deciding
- **Do not pick option 2 (allow from now on) at first.** Save it for when you are comfortable.
- If something looks off, pick **`3. No`** and say "don't do that, do X instead".

**To stop a job midway, press `Ctrl + C`.**

## 5.5 Quitting

Type this in the chat and you are done.

```
exit
```

Or press `Ctrl + C` twice.

## 5.6 Starting again next time

1. Open your working folder in File Explorer.
2. Right-click on empty space -> **"Open in Terminal"**.
3. Type `claude`. (Or `codex` / `agy`.)

You are already logged in, so it starts immediately.

---

# Part 6. Things worth trying

Instructions work better the **more specific** they are. Copy the examples below and adapt them.

## 6.1 File organisation

```
Rename every file in this folder to "date_title" format.
Use the file's creation date, formatted like 20260901.
Show me the planned list first, before renaming anything.
```

```
Look through the PDFs in this folder and build a table of
file name, title, page count and a one-line summary. Save it as index.md
```

## 6.2 Data work

```
Open data.csv, tell me how many rows have empty cells,
and suggest ways to handle them.
Do not modify the file yet.
```

```
Draw a bar chart of the monthly revenue in revenue.xlsx
and save it as a PNG. Put a title and axis labels on it.
```

## 6.3 Writing

```
Read draft.md and rewrite it in a dry, objective academic register.
Leave the original untouched and save the revision as draft-revised.md
Also summarise what you changed and why.
```

```
Write an email in three tones (formal / concise / friendly) covering the following.
Content: (describe the situation here)
```

## 6.4 Learning as you go

```
Explain what you just did in terms a beginner would understand.
```

```
Suggest five useful things I could do in this folder.
```

## 6.5 How to write good instructions

| Poor | Good |
|---|---|
| "Clean this up" | "Rename files to date_title order, and show me the list before renaming" |
| "Analyse this" | "Calculate the monthly average and month-on-month change, and put it in a table" |
| "Fix it" | "Fix only spelling and spacing; do not change sentence structure" |

**Four habits**

1. Say **what to do + how to do it + where to save the result**, together.
2. For risky work, add **"show me the plan first and run it only after I approve"**.
3. To protect the original, say explicitly **"do not touch the original, work on a copy"**.
4. If you dislike the result, do not say "do it again" — say **"change X to Y"**.

---

# Part 7. Using it safely — five rules

## 1. Only run it in a dedicated working folder

An AI agent treats the folder you launched it from, and everything below it, as its working scope.

- **Do not**: launch it on the Desktop, in `C:\Users\yourname`, or at the root of C:
- **Do**: create purpose-specific folders like `C:\ai-work\project1` and launch inside them

## 2. Copy the originals first

The AI can edit a file wrongly, and you can approve the wrong thing.

**Duplicate the whole folder before you start.** It is the simplest and most reliable safeguard there is.

## 3. Keep sensitive material out of the working folder

File contents the AI reads are sent to a server to produce an answer.

Do not put these in your working folder:
- Files containing national ID numbers, bank account numbers or passwords
- Unpublished research data, manuscripts under review
- Company confidential material, contracts
- Lists containing other people's personal data

> If your institution's rules forbid sending something outside, do not bring it into the folder in the first place.

## 4. Read the approval screen before you click

Hammering `Yes` to get through faster is a dangerous habit. **Read what it is about to do, at least once.**

Stop and check whenever you see these words in particular: **delete, rm, overwrite, all, force**.

## 5. Do not use auto-approve

Claude Code's `--dangerously-skip-permissions`, Codex CLI's `--full-auto`/`--yolo`, and Antigravity CLI's auto-approve setting all mean "stop asking and just do everything." **They are as dangerous as they sound. Beginners should never use them.**

Tip articles online sometimes recommend turning this on for convenience. That advice comes from people working in code repositories where a bad deletion is recoverable. Do not use it in a folder holding your original data.

---

# Part 8. When something goes wrong

## 8.1 "The term ... is not recognized"

```
'claude' is not recognized as the name of a cmdlet, function, script file...
```

**Try in this order**

1. **Close the terminal completely and open a new one.** (Nine times out of ten this fixes it.)
2. If that fails, **reboot**.
3. Still failing? Check where it installed.

```
npm config get prefix
```

You get a path like `C:\Users\yourname\AppData\Roaming\npm`. Register it with Windows.

- `Windows key` -> search `environment variables` -> run **"Edit environment variables for your account"**
- Select **`Path`** in the upper list -> **"Edit"**
- **"New"** -> paste the path -> press **"OK"** on every window to close them
- Open a new terminal and try again

## 8.2 "...cannot be loaded because running scripts is disabled"

You skipped the execution policy step in section 3.4.

```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Type `Y` and press Enter.

## 8.3 Non-English text shows as `???` or garbled characters

Temporary fix:

```
chcp 65001
```

Permanent fix: do the profile setup in section 3.5.

If that still fails, change a Windows setting.
- `Windows key` -> search `region` -> **"Date, time & regional formatting"** -> **"Additional date, time & regional settings"** -> **"Region"** -> **"Administrative"** tab -> **"Change system locale"**
- Tick **"Beta: Use Unicode UTF-8 for worldwide language support"** -> reboot

> This can cause side effects in some older non-Unicode programs. Use it only when nothing else works.

## 8.4 Red `ERR!` errors during installation

**If it is a permissions problem**: reopen the terminal **as administrator**.
`Windows key` -> search `Terminal` -> right-click the entry -> **"Run as administrator"**

**If it is a network problem**: corporate and university firewalls block these installs often. Try again on a personal connection (phone tethering, for instance).

## 8.5 Trouble caused by spaces or non-English characters in a path

Paths like `D:\My Research\2026 Data` occasionally cause problems.

**Fix**: build working folders using **letters, numbers and underscores only** where you can.

- Good: `C:\ai-work\project2026`
- Avoid: `C:\My Documents\2026 Research Data (final)`

When you must use an existing path, **wrap it in double quotes.**

```
cd "D:\My Research\2026 Data"
```

## 8.6 The AI answers oddly, or the conversation gets tangled

In a long conversation the AI can get dragged along by earlier context.

- Type `/clear` -> resets the conversation (the same command in all three tools)
- Or `exit` and start again

Getting into the habit of pressing `/clear` whenever the topic changes noticeably improves answer quality.

## 8.7 Updating to the latest version

**Update the same way you installed.**

| Tool | If you used the dedicated installer | If you used npm |
|---|---|---|
| Claude Code | Updates itself (`claude update` to check now) | `npm install -g @anthropic-ai/claude-code@latest` |
| Codex CLI | `irm https://chatgpt.com/codex/install.ps1 \| iex` | `npm install -g @openai/codex@latest` |
| Antigravity CLI | `irm https://antigravity.google/cli/install.ps1 \| iex` | (not applicable) |

> **Do not use `npm update -g`.** It only moves within the version range recorded at first install, so it often fails to reach the latest release. Use `npm install` with `@latest`.

If you installed Codex through winget, use `winget upgrade --id OpenAI.Codex -e`.

## 8.8 Removing them

```
npm uninstall -g @anthropic-ai/claude-code
```
```
npm uninstall -g @openai/codex
```
```
winget uninstall --id OpenAI.Codex -e
```

For dedicated installers, follow the uninstall instructions in each tool's official documentation.

If a retired Gemini CLI is still lying around, remove it like this.

```
npm uninstall -g @google/gemini-cli
```

---

# Appendix A. Glossary

| Term | Plain explanation |
|---|---|
| Terminal | A window for giving the computer text instructions |
| PowerShell | The program on Windows that receives and runs those commands |
| CLI | Command Line Interface. Working with text only, no mouse |
| Path | The address of a file or folder, e.g. `C:\Users\Jane\Documents` |
| Directory | Another word for folder. Same thing |
| Node.js | The engine program some AI agents need in order to run |
| npm | The tool that installs and manages programs. Ships with Node.js |
| Git | A tool for tracking file history |
| Global install (`-g`) | Installing machine-wide so it works from any folder |
| Execution policy | The Windows security setting that decides whether scripts may run |
| Agent | An AI that uses tools on its own to get work done |
| Token | The unit an AI counts text in. Used to measure usage |
| MCP | The standard for connecting an AI to outside services such as Google Drive |
| WSL | The feature that runs Linux inside Windows. Not needed any more (Appendix D) |
| Git Bash | The Linux-style command window installed with Git. Claude Code uses it as its shell |
| `CLAUDE.md` / `AGENTS.md` | The file holding your working folder's rules. The AI reads it every time |
| Context | How much conversation and file content the AI holds at once. When it overflows, the earliest parts are forgotten |

---

# Appendix B. One-page command summary

## Terminal basics

| Command | What it does |
|---|---|
| `pwd` | Show where you are |
| `ls` | List files in the current folder |
| `cd foldername` | Move into that folder |
| `cd ..` | Move up one level |
| `mkdir foldername` | Create a new folder |
| `cls` | Clear the screen |
| `exit` | Close the terminal |

## Installation (once)

```
winget install --id OpenJS.NodeJS.LTS -e
```
```
winget install --id Git.Git -e
```
```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

For AI agents, install **only the one you need** of the three.

```
irm https://claude.ai/install.ps1 | iex
```
```
irm https://chatgpt.com/codex/install.ps1 | iex
```
```
irm https://antigravity.google/cli/install.ps1 | iex
```

## Verification

```
node --version
```
```
npm --version
```
```
git --version
```
```
claude --version
```

## The everyday flow

1. Open your working folder in Explorer
2. Right-click empty space -> **"Open in Terminal"**
3. Type `claude` (or `codex` / `agy`)
4. Give instructions in plain English
5. Read the approval screen and choose
6. `exit` to quit

## Keyboard shortcuts

| Key | What it does |
|---|---|
| Up arrow | Recall the previous command |
| `Tab` | Autocomplete folder and file names |
| Right-click | Paste |
| `Ctrl + C` | Stop a running job |
| `Ctrl` + mouse wheel | Change text size |

---

# Appendix C. Summary for Mac users

This document is written for Windows. On a Mac, only these things differ; everything else is the same.

| Item | Windows | Mac |
|---|---|---|
| Open a terminal | Windows key -> "Terminal" | `Cmd + Space` -> "Terminal" |
| Install tool | winget | Homebrew (`brew`) |
| Install Node.js | `winget install OpenJS.NodeJS.LTS` | `brew install node` |
| Path separator | `\` (backslash) | `/` (slash) |
| Execution policy setup | Needed | Not needed |
| Text encoding setup | Needed | Not needed |

If you do not have Homebrew, install it first following the instructions at **https://brew.sh**.

For AI agents, use `curl` instead of `irm ... | iex`. Everything else is identical.

```
curl -fsSL https://claude.ai/install.sh | bash
```
```
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

Install Codex CLI through Homebrew.

```
brew install --cask codex
```

The `npm install -g ...` route is exactly the same as on Windows.

---

# Appendix D. Do you need WSL (Linux)?

**Short answer: if you are the audience for this guide, just use Windows.**

You will find articles online saying "Claude Code requires WSL". Most of them were written in 2024–2025, when it genuinely did not support Windows and WSL (Windows Subsystem for Linux, a feature that runs Linux inside Windows) was the only route. **All three tools now ship Windows-native installers, and WSL is not needed.**

## Why plain Windows is the better choice

| | Windows as is | WSL |
|---|---|---|
| Setup | One command | Install Linux, then install everything again inside it |
| Reaching Windows files | `D:\research` directly | Via `/mnt/d/research`, and **slow** |
| Non-English file names and paths | Fine | Sometimes mangled |
| Working with office documents | Natural | Awkward |
| Extra things to learn | None | One more set of Linux concepts |

**WSL is a net loss when your work is documents and data sitting in Windows folders.** Reading and writing Windows drives (`/mnt/c`, `/mnt/d`) from WSL is measurably slow, and it becomes obvious once you are working across hundreds of files.

## Do this instead

The way to reduce friction on Windows is not WSL — it is **installing Git for Windows** (section 3.3). When Claude Code detects Git Bash it uses that as its shell instead of PowerShell, and since most material online (and most of what the AI knows) is written in Linux-style commands, errors drop.

## When WSL is the better option

Consider WSL if one of these applies to you. Most readers of this guide will not be in that position.

- You need Linux-only development tools (Docker, particular Python packages, and so on)
- You are building something that will run on a server and want your environment to match it
- You want to give the AI risky work while keeping it isolated from Windows itself

> If you do go with WSL, keep your working files inside WSL (`~/projects/...`). Crossing back and forth to Windows drives is the slowest and most trouble-prone arrangement.

---

# Wrapping up — what comes next

If you got this far, you have the fundamentals. Once you are comfortable, try these.

1. **Put a rules file in your working folder** — create a rules file saying "in this folder, work according to these rules" and the AI follows it without being told each time. Claude Code reads `CLAUDE.md`; Codex CLI and Antigravity CLI read `AGENTS.md`. In Claude Code, `/init` drafts one for you.

2. **Save the instructions you reuse** — keep the prompts for recurring work in a text file and paste them in.

3. **Connect outside services (MCP)** — you can wire services like Google Drive or Notion directly into the AI. Attempt this once the basics feel routine.

4. **Compare the tools** — giving the same job to Claude, Codex and Antigravity teaches you their different characters.

## Official documentation

- Claude Code — https://code.claude.com/docs
- Codex CLI — https://developers.openai.com/codex/cli
- Antigravity CLI — https://antigravity.google/docs/cli/install

---

*This document is written for Windows 11. Screens shift a little as versions move on, but the overall flow stays the same.*
