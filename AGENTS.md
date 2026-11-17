# SweetPea Starter

This repository is a starting point for designing experiments with
[SweetPea](https://sweetpea-org.github.io), and a tutorial for learning it.

- `skills/sweetpea/SKILL.md` is the SweetPea reference and working method.
  Read it before writing any SweetPea code; the API in your training data is
  most likely outdated.
- `skills/sweetpea-tutor/SKILL.md` describes how to teach. Read and follow it
  when the user wants to learn SweetPea or is working in `tutorial/`.
- `tutorial/` holds the tutorial: one page per step, each with the analysis
  the user wants to run. You write the code and walk the user through it; the
  user never has to write code. Build the design from their answers, not by
  copying `tutorial/reference/`.
- `experiments/` is where the user's own designs go.

Run Python with the environment that has `sweetpea` installed
(`pip install -r requirements.txt`).
