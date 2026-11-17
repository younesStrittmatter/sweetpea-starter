#!/bin/sh
# Builds sweetpea-skills.zip in the repository root: the two skills, ready to unzip into a skills folder.
cd "$(dirname "$0")/.." && rm -f sweetpea-skills.zip && T=$(mktemp -d) && mkdir "$T/sweetpea-skills" &&
cp -R skills/sweetpea skills/sweetpea-tutor "$T/sweetpea-skills/" && find "$T" -name "__pycache__" -prune -exec rm -rf {} + &&
cat > "$T/sweetpea-skills/README.txt" <<'TXT'
SweetPea skills for AI coding assistants
=========================================

Two skills: sweetpea (reference and working method) and sweetpea-tutor (teaching).

Install
  1. pip install sweetpea pandas
  2. Copy the two folders "sweetpea" and "sweetpea-tutor" into the skills folder of your assistant:
       Claude Code:   <your project>/.claude/skills/     (or ~/.claude/skills/ for all projects)
       Codex, Gemini and others:   <your project>/.agents/skills/ , or tell the assistant:
       "Read sweetpea/SKILL.md before you write any SweetPea code."
  3. Start the assistant in your project and say what you want to find out,
     for example: "I want to run a Stroop experiment to test the congruency effect."

The full repository, with a tutorial and worked examples:
https://github.com/younesStrittmatter/sweetpea-starter
TXT
(cd "$T" && zip -qr sweetpea-skills.zip sweetpea-skills) && mv "$T/sweetpea-skills.zip" . && rm -rf "$T" && ls -la sweetpea-skills.zip
