# SweetPea Starter

Design experiments with [SweetPea](https://sweetpea-org.github.io) together
with an AI assistant that actually knows SweetPea.

SweetPea turns a description of an experiment (factors, what must be
balanced, what must not happen) into randomised trial sequences that satisfy
it. This repository gives you a working environment, two skills that teach
any coding assistant the current SweetPea API, a tutorial, and a place for
your own designs.

> Unofficial and experimental. Not (yet) part of the SweetPea project.

## Start

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/younesStrittmatter/sweetpea-starter)
[![Open in Dev Container](https://img.shields.io/static/v1?label=Dev%20Container&message=Open%20locally&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/younesStrittmatter/sweetpea-starter)

| Way in | What you need |
|---|---|
| **Codespaces** (button above) | A GitHub account. Everything runs in the browser. |
| **Dev Container** (button above) | VS Code and Docker on your computer. |
| **Your own editor** | Python 3.9 or later; see below. |

### Your own editor

```
git clone https://github.com/younesStrittmatter/sweetpea-starter
cd sweetpea-starter
pip install -r requirements.txt
```

Then open the folder in VS Code, Cursor, PyCharm or JupyterLab.

## Bring your AI

In a Codespace, open a terminal and start the assistant you have an account
for. Each asks you to log in through the browser the first time.

| Command | Account |
|---|---|
| `claude` | Claude Pro or Max |
| `codex` | ChatGPT Plus or higher |
| `gemini` | Google account (has a free tier) |

Then just say what you want:

- *"Teach me SweetPea."* starts the tutor.
- *"I need a task-switching experiment with two tasks, balanced switches and
  repeats, and never more than three repeats in a row."* gets you a design,
  and a count showing that it does what you asked.

Using a chat window instead (ChatGPT, Claude, Gemini in the browser)? Upload
[`skills/sweetpea/SKILL.md`](skills/sweetpea/SKILL.md), and
[`skills/sweetpea-tutor/SKILL.md`](skills/sweetpea-tutor/SKILL.md) if you
want to be taught, and copy the code it writes into a notebook.

## What is in here

| Path | Purpose |
|---|---|
| `skills/sweetpea/` | The SweetPea reference and working method for assistants, plus `scripts/check_design.py`, which counts what a sequence really contains. |
| `skills/sweetpea-tutor/` | Turns the assistant into a teacher: explains, gives hints before answers, makes you count. |
| `tutorial/` | Notebooks to learn SweetPea step by step. |
| `experiments/` | Your own designs. |
| `AGENTS.md` | Points assistants that do not load skills at the files above. |
| `tests/` | Runs every code example in the skill against the released SweetPea, so the assistant is never taught something that does not work. |

## Use the skills in a project you already have

Copy the two folders in `skills/` into the place your assistant reads skills
from (for example `.claude/skills/` for Claude Code or `.agents/skills/` for
Codex), or copy `skills/sweetpea/SKILL.md` into your project and mention it
in your `AGENTS.md`.
