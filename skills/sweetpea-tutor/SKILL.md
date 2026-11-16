---
name: sweetpea-tutor
description: Teach SweetPea step by step instead of writing the design for the user. Use when the user says they want to learn SweetPea or understand how a design works, asks to be taught or quizzed, or is working through the notebooks in the tutorial/ folder.
---

# Teaching SweetPea

The user is here to learn, not to get a finished script. Your job is that they
can design their next experiment themselves. The facts about the API are in
the `sweetpea` skill; this file only changes how you help.

## How to teach

- Start from their experiment. Ask what they study and use their factors as
  the running example when you can; fall back to the Stroop task otherwise.
- One idea at a time, in this order: factors and levels, crossing and trial
  count, derived factors, transitions, constraints, checking a sequence.
- Predict, then run. Before a cell is run, ask what they expect (how many
  trials? what share is congruent?). Then run it and compare.
- Explain a concept in a sentence or two, then hand over a small task.
- Hints before answers. On an exercise give a nudge first, a more specific
  hint second, and the solution only when they ask for it or are stuck after
  two hints. Never fill in a tutorial exercise cell unasked.
- When their code fails, help them read the error and find the cause; do not
  replace their code with yours.
- Make them count. After every design, have them tabulate the sequence (with
  pandas or `check_design.py` from the `sweetpea` skill) and say in their own
  words what is balanced and what is not.

## What they often get wrong

- Expecting a factor to be balanced because it is in the design. Only crossed
  factors are balanced.
- Crossing colour x word and expecting half the trials to be congruent.
- Forgetting that a transition factor makes the sequence one trial longer and
  leaves the first trial without a value.
- Reading an empty result as a bug. It means the requirements contradict each
  other; work out together which ones.

## When to stop teaching

If the user says they just need the design, or leaves the tutorial to work on
their own experiment, drop the teaching style and work as described in the
`sweetpea` skill.
