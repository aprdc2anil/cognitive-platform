# Phase 1 — AI Accelerated Development Environment

## Goal

Establish a developer workstation capable of building the Cognitive Platform.
Covers OS/terminal setup, tools, language runtimes, and AI coding setup.
Docker and infrastructure setup is covered in Phase 2.

---

## Status

**Complete**

---

## Architecture

```
Developer Machine
│
└── Linux Shell (WSL / macOS Terminal / native Linux)
    │
    ├── Development Tools
    │   ├── VS Code (or any IDE)
    │   ├── Git + GitHub
    │   ├── GitHub Copilot
    │   └── Claude Code
    │
    └── Language Runtimes
        ├── Python + .venv
        └── Java 21
```

---

## Stages

### Stage 1 — Linux Shell Environment
Status: Complete

Get a working Linux shell. Method depends on your OS — see Onboarding below.

### Stage 2 — Development Workspace
Status: Complete

Create consistent directory structure:
```
~/dev/git/cognitive-platform
```

### Stage 3 — Git Repository
Status: Complete

Initialise monorepo, connect to GitHub remote.

### Stage 4 — IDE + AI Tools
Status: Complete

VS Code with required extensions. AI tools: GitHub Copilot, Claude Code.

### Stage 5 — Language Runtimes
Status: Complete

Python `.venv` created. Java 21 installed.

---

## Onboarding — Reproduce This Phase

---

### Step 1 — Linux Shell Setup

> This step depends on your OS. Pick your path.

#### Windows (this project's environment)

Install WSL with Ubuntu:

```powershell
wsl --install
```

Verify:
```powershell
wsl -l -v
```

Enter the Linux shell:
```bash
wsl
sudo apt update && sudo apt upgrade
```

VS Code with WSL — install the **Remote WSL** extension and open the project from inside WSL:
```bash
code .
```

#### macOS

macOS ships with a Unix shell. No additional setup needed.

Open Terminal or iTerm2.

```bash
xcode-select --install   # installs git and build tools
brew install git         # if using Homebrew
```

#### Native Linux

No additional setup. Open your terminal.

```bash
sudo apt update && sudo apt upgrade   # Debian/Ubuntu
```

---

### Step 2 — Development Workspace

Same across all platforms:

```bash
mkdir -p ~/dev/git
cd ~/dev/git
git clone <repo-url> cognitive-platform
cd cognitive-platform
```

---

### Step 3 — Python

Same across all platforms:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

> macOS: if `python3` is missing, install via `brew install python`.

---

### Step 4 — Java

#### Windows (WSL) / Linux

```bash
sudo apt install openjdk-21-jdk
java -version
```

#### macOS

```bash
brew install openjdk@21
java -version
```

---

### Step 5 — IDE + AI Tools

Install VS Code: https://code.visualstudio.com

Required extensions (all platforms):
- Python
- Java Extension Pack
- Docker
- GitLens
- Remote WSL *(Windows only — skip on Mac/Linux)*

AI tools:
- GitHub Copilot
- Claude Code (`npm install -g @anthropic-ai/claude-code`)

---

## Progress Tracking

- [x] Linux shell available and working
- [x] Development workspace created (`~/dev/git/cognitive-platform`)
- [x] Git repository initialised and pushed to GitHub
- [x] VS Code installed with required extensions
- [x] GitHub Copilot active
- [x] Claude Code active
- [x] Python `.venv` created
- [x] Java 21 installed

---

## Next Phase

Phase 2 — Platform Engineering: Docker, infrastructure containers, observability, Python runtime stack.
See [phase2-environment-runbook.md](phase2-environment-runbook.md)
