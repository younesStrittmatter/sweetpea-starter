# Step 4. Transfer

Without an assistant: [notebook](notebooks/4_transfer.ipynb) · [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/younesStrittmatter/sweetpea-starter/blob/main/tutorial/notebooks/4_transfer.ipynb)

## The question

Does adapting to frequent conflict make it harder to switch to another task?

**What it is about.** Whether shielding a task and switching between tasks
are the same control setting. Stability (keeping the word out) and
flexibility (moving to another task) may pull against each other.
**Prediction if they are one setting:** in a mostly incongruent context,
where the task is shielded more, the switch cost is larger than in a mostly
congruent context. **If they are separate:** the switch cost is the same in
both. **The alternative to rule out:** a mostly incongruent context is simply
harder, so everything is slower there, switches included.

## The analysis

The switch cost (switch trials against repeat trials) in mostly incongruent
mini-blocks against the switch cost in mostly congruent mini-blocks.

## Ask your assistant

> Last question. I want to know whether this control setting has a price: if
> people shield the task more in a mostly incongruent context, are they then
> worse at switching to another task? I add a second task: on some trials
> people read the word instead of naming the ink, and a cue says which. I want
> mini-blocks that are mostly congruent or mostly incongruent, and to compare
> the switch cost between them. What is the hypothesis, and what does the
> design need?

## What to check

- **Is there a repeat baseline?** A switch cost needs switch trials and repeat
  trials in the same context. Count both, in each kind of mini-block.
- **The thin cells.** How many incongruent switch trials does a mostly
  congruent mini-block have? Is that enough?
- **What gave way?** Count the ink colour. Is it still even? Did the assistant
  say what it left out of the crossing, and why?
- **One design or blocks put one after the other?** With `Nest` the context is
  a factor of the design and SweetPea draws its order. Where does the crossing
  sit then: does it line up with the mini-blocks, or is it off by a trial?
- **The first trial of a mini-block.** It is a switch or a repeat relative to
  a trial from the other context. Keep it or drop it?

## The idea

Each question added a factor, and each factor multiplies the design. At some
point not everything fits, and the design becomes a choice about what to
leave open. The assistant should make that choice with you, not for you.
