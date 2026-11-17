# Step 4. Transfer

Without an assistant: [notebook](notebooks/4_transfer.ipynb) · [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/younesStrittmatter/sweetpea-starter/blob/main/tutorial/notebooks/4_transfer.ipynb)

## The question

Does adapting to frequent conflict make it harder to change the task?

**What it is about.** Whether shielding a task and switching between tasks
are the same control setting. **Prediction if they are one setting:** where
conflict is frequent the current task is shielded more, so a change of task
costs more: the switch cost is larger in the mostly incongruent context.
**If they are separate:** the switch cost is the same in both.
**Why word reading:** it has almost no congruency effect, so the proportion
itself hardly touches the trials the switch cost is measured on.

## The analysis

Mini-blocks are mostly congruent or mostly incongruent, and each is either
colour naming or word reading. Switch cost = response time in word-reading
mini-blocks that follow colour naming (switch) minus response time in
word-reading mini-blocks that follow word reading (repeat). Compare it
between the two contexts.

## Ask your assistant

> Last question: does the adaptation transfer to another task? I want
> mini-blocks that are mostly congruent or mostly incongruent, and each
> mini-block is either colour naming or word reading. I want the switch cost
> between mini-blocks: word reading after colour naming against word reading
> after word reading, compared between the two contexts. I take word reading
> because it has almost no congruency effect. What is the hypothesis, and can
> nested blocks keep all of that counterbalanced?

## What to check

- **Two crossings.** Within a mini-block: is the proportion right and the ink
  colour even? Between mini-blocks: does every combination of context, task
  and switch or repeat occur equally often?
- **The first mini-block.** It has no mini-block before it. Is it left out of
  the counts?
- **How much data per cell?** Each combination is one mini-block. How many
  trials does the switch cost in one context rest on?
- **What is in neither crossing?** The adaptation that should carry over was
  built up in the mini-block before. Is its context the same for switch and
  repeat? Did the assistant say so without being asked?

## The idea

Each question added a factor, and each factor multiplies the design. Nesting
keeps both levels counterbalanced at once. What it leaves open is still a
choice, and the assistant should make that choice with you, not for you.
