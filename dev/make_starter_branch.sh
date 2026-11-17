#!/bin/sh
# Builds the branch "starter": what a participant needs and nothing else (the skills, the tutorial,
# an empty experiments folder, the environment). Development stays on main; run this after a change
# to publish it:   sh dev/make_starter_branch.sh          (add "push" to also push the branch)
set -e
cd "$(dirname "$0")/.."
ROOT=$(pwd); T=$(mktemp -d); REMOTE=$(git remote get-url origin)
git archive HEAD AGENTS.md CLAUDE.md .gitignore .devcontainer .claude .agents skills tutorial experiments | tar -x -C "$T"
printf 'sweetpea\npandas\nipykernel\n' > "$T/requirements.txt"
cat > "$T/README.md" <<'MD'
# SweetPea Starter

Design experiments with [SweetPea](https://sweetpea-org.github.io) together
with an AI assistant that knows SweetPea. You say what you want to find out;
the assistant states the hypothesis, writes the design, and counts whether it
does what you asked.

Website with the examples and the tutorial:
<https://younesstrittmatter.github.io/sweetpea-starter/>

> Unofficial and experimental. Not (yet) part of the SweetPea project.

## Start

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/younesStrittmatter/sweetpea-starter?ref=starter)

| Way in | What you need |
|---|---|
| **Codespaces** (button above) | A GitHub account. Everything runs in the browser. |
| **Your own computer** | Python 3.9 or later: `git clone -b starter https://github.com/younesStrittmatter/sweetpea-starter`, then `pip install -r requirements.txt`. |
| **Download** | [The folder as a zip](https://github.com/younesStrittmatter/sweetpea-starter/archive/refs/heads/starter.zip), then `pip install -r requirements.txt`. |

## Bring your AI

Open a terminal and start the assistant you have an account for. Each asks
you to log in through the browser the first time.

| Command | Account |
|---|---|
| `claude` | Claude Pro or Max |
| `codex` | ChatGPT Plus or higher |
| `gemini` | Google account (has a free tier) |

Then say what you want to find out, for example:

- *"I want to run a Stroop experiment to test the congruency effect. What is
  it about, and what do I need to decide?"*
- *"Run the guided tutorial."* The assistant then leads you through the four
  steps in `tutorial/`.

Using a chat window (ChatGPT, Claude, Gemini in the browser)? Upload
`skills/sweetpea/SKILL.md` and copy the code it writes into a notebook.

## What is in here

| Path | Purpose |
|---|---|
| `skills/` | What the assistant reads: the SweetPea reference and working method, worked examples, and how to teach. |
| `tutorial/` | One Stroop experiment in four questions: a page per step, notebooks, and the reference designs. |
| `experiments/` | Your own designs go here. |
| `AGENTS.md` | Tells the assistant where to look. |
MD
cd "$T" && git init -q -b starter && git add -A && git -c user.name="$(git -C "$ROOT" config user.name)" -c user.email="$(git -C "$ROOT" config user.email)" \
  commit -q -m "Starter: built from main $(git -C "$ROOT" rev-parse --short HEAD)"
echo "built in $T"; git ls-files | cut -d/ -f1 | sort | uniq -c
if [ "$1" = "push" ]; then git push -q --force "$REMOTE" starter:starter && echo "pushed branch starter"; fi
