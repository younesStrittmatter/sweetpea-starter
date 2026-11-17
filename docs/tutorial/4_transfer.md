# Step 4. Transfer

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/younesStrittmatter/sweetpea-starter/blob/main/tutorial/notebooks/4_transfer.ipynb){ target=_blank } · [notebook](https://github.com/younesStrittmatter/sweetpea-starter/blob/main/tutorial/notebooks/4_transfer.ipynb) · [script](https://github.com/younesStrittmatter/sweetpea-starter/blob/main/tutorial/reference/step4_transfer.py)

## The experiment

A block from the design built on this page. Press play, or step through it.

<div class="stroop-demo" data-trials='[{"block": 1, "context": "mostly incongruent", "task": "name the colour", "colour": "red", "word": "blue", "congruency": "incongruent", "task_transition": ""}, {"block": 1, "context": "mostly incongruent", "task": "name the colour", "colour": "green", "word": "green", "congruency": "congruent", "task_transition": ""}, {"block": 1, "context": "mostly incongruent", "task": "name the colour", "colour": "blue", "word": "green", "congruency": "incongruent", "task_transition": ""}, {"block": 1, "context": "mostly incongruent", "task": "name the colour", "colour": "red", "word": "blue", "congruency": "incongruent", "task_transition": ""}, {"block": 1, "context": "mostly incongruent", "task": "name the colour", "colour": "green", "word": "green", "congruency": "congruent", "task_transition": ""}, {"block": 1, "context": "mostly incongruent", "task": "name the colour", "colour": "blue", "word": "blue", "congruency": "congruent", "task_transition": ""}, {"block": 1, "context": "mostly incongruent", "task": "name the colour", "colour": "red", "word": "red", "congruency": "congruent", "task_transition": ""}, {"block": 1, "context": "mostly incongruent", "task": "name the colour", "colour": "blue", "word": "red", "congruency": "incongruent", "task_transition": ""}, {"block": 1, "context": "mostly incongruent", "task": "name the colour", "colour": "red", "word": "red", "congruency": "congruent", "task_transition": ""}, {"block": 1, "context": "mostly incongruent", "task": "name the colour", "colour": "green", "word": "blue", "congruency": "incongruent", "task_transition": ""}, {"block": 1, "context": "mostly incongruent", "task": "name the colour", "colour": "blue", "word": "green", "congruency": "incongruent", "task_transition": ""}, {"block": 1, "context": "mostly incongruent", "task": "name the colour", "colour": "green", "word": "green", "congruency": "congruent", "task_transition": ""}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "red", "word": "green", "congruency": "incongruent", "task_transition": "repeat"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "blue", "word": "green", "congruency": "incongruent", "task_transition": "repeat"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "green", "word": "blue", "congruency": "incongruent", "task_transition": "repeat"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "green", "word": "green", "congruency": "congruent", "task_transition": "repeat"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "blue", "word": "green", "congruency": "incongruent", "task_transition": "repeat"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "red", "word": "red", "congruency": "congruent", "task_transition": "repeat"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "red", "word": "green", "congruency": "incongruent", "task_transition": "repeat"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "blue", "word": "red", "congruency": "incongruent", "task_transition": "repeat"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "red", "word": "green", "congruency": "incongruent", "task_transition": "repeat"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "green", "word": "blue", "congruency": "incongruent", "task_transition": "repeat"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "green", "word": "red", "congruency": "incongruent", "task_transition": "repeat"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "blue", "word": "blue", "congruency": "congruent", "task_transition": "repeat"}, {"block": 3, "context": "mostly congruent", "task": "name the colour", "colour": "blue", "word": "blue", "congruency": "congruent", "task_transition": "repeat"}, {"block": 3, "context": "mostly congruent", "task": "name the colour", "colour": "green", "word": "green", "congruency": "congruent", "task_transition": "repeat"}, {"block": 3, "context": "mostly congruent", "task": "name the colour", "colour": "green", "word": "green", "congruency": "congruent", "task_transition": "repeat"}, {"block": 3, "context": "mostly congruent", "task": "name the colour", "colour": "red", "word": "red", "congruency": "congruent", "task_transition": "repeat"}, {"block": 3, "context": "mostly congruent", "task": "name the colour", "colour": "blue", "word": "blue", "congruency": "congruent", "task_transition": "repeat"}, {"block": 3, "context": "mostly congruent", "task": "name the colour", "colour": "blue", "word": "green", "congruency": "incongruent", "task_transition": "repeat"}, {"block": 3, "context": "mostly congruent", "task": "name the colour", "colour": "blue", "word": "blue", "congruency": "congruent", "task_transition": "repeat"}, {"block": 3, "context": "mostly congruent", "task": "name the colour", "colour": "green", "word": "blue", "congruency": "incongruent", "task_transition": "repeat"}, {"block": 3, "context": "mostly congruent", "task": "name the colour", "colour": "green", "word": "green", "congruency": "congruent", "task_transition": "repeat"}, {"block": 3, "context": "mostly congruent", "task": "name the colour", "colour": "red", "word": "red", "congruency": "congruent", "task_transition": "repeat"}, {"block": 3, "context": "mostly congruent", "task": "name the colour", "colour": "red", "word": "red", "congruency": "congruent", "task_transition": "repeat"}, {"block": 3, "context": "mostly congruent", "task": "name the colour", "colour": "red", "word": "blue", "congruency": "incongruent", "task_transition": "repeat"}, {"block": 4, "context": "mostly incongruent", "task": "read the word", "colour": "blue", "word": "red", "congruency": "incongruent", "task_transition": "switch"}, {"block": 4, "context": "mostly incongruent", "task": "read the word", "colour": "blue", "word": "green", "congruency": "incongruent", "task_transition": "switch"}, {"block": 4, "context": "mostly incongruent", "task": "read the word", "colour": "red", "word": "green", "congruency": "incongruent", "task_transition": "switch"}, {"block": 4, "context": "mostly incongruent", "task": "read the word", "colour": "red", "word": "green", "congruency": "incongruent", "task_transition": "switch"}, {"block": 4, "context": "mostly incongruent", "task": "read the word", "colour": "green", "word": "red", "congruency": "incongruent", "task_transition": "switch"}, {"block": 4, "context": "mostly incongruent", "task": "read the word", "colour": "blue", "word": "red", "congruency": "incongruent", "task_transition": "switch"}, {"block": 4, "context": "mostly incongruent", "task": "read the word", "colour": "blue", "word": "blue", "congruency": "congruent", "task_transition": "switch"}, {"block": 4, "context": "mostly incongruent", "task": "read the word", "colour": "red", "word": "green", "congruency": "incongruent", "task_transition": "switch"}, {"block": 4, "context": "mostly incongruent", "task": "read the word", "colour": "green", "word": "blue", "congruency": "incongruent", "task_transition": "switch"}, {"block": 4, "context": "mostly incongruent", "task": "read the word", "colour": "red", "word": "red", "congruency": "congruent", "task_transition": "switch"}, {"block": 4, "context": "mostly incongruent", "task": "read the word", "colour": "green", "word": "blue", "congruency": "incongruent", "task_transition": "switch"}, {"block": 4, "context": "mostly incongruent", "task": "read the word", "colour": "green", "word": "green", "congruency": "congruent", "task_transition": "switch"}]'></div>

## With your assistant

> Last question: does the adaptation transfer to another task? I want mini-blocks that are mostly congruent or mostly incongruent, and each mini-block is either colour naming or word reading. I want the switch cost between mini-blocks: word reading after colour naming against word reading after word reading, compared between the two contexts. I take word reading because it has almost no congruency effect. What is the hypothesis, and can nested blocks keep all of that counterbalanced?

## Step by step

**So far.** Step 2 made the trial before a factor. Step 3 made blocks that are mostly congruent or mostly incongruent, generated one by one. This step uses both ideas one level up: the mini-block is the unit, and the whole session is one design.

**The question.** Does adapting to frequent conflict make it harder to change the task?

**Prediction if it is one control setting.** Where conflict is frequent the current task is shielded more, so a change of task costs more: the switch cost is larger in the mostly incongruent context.

**Why word reading.** The switch cost is taken on word-reading mini-blocks. Word reading has almost no congruency effect, so the proportion itself hardly touches the trials the cost is measured on.

**The analysis.** Switch cost = response time in word-reading mini-blocks that follow colour naming (switch) minus response time in word-reading mini-blocks that follow word reading (repeat). Compare it between the two contexts.

### As before, plus the task and the context

Both are regular factors. Neither changes from trial to trial: each is held for a whole mini-block.

```python
import pandas as pd
from sweetpea import (Factor, DerivedLevel, WithinTrial, Transition, Exclude, MinimumTrials,
                      CrossBlock, synthesize_trials, CMSGen)

colours = ["red", "green", "blue"]

# regular factors: set freely on every trial
colour = Factor("colour", colours)      # the ink
word = Factor("word", colours)          # what the word says
from sweetpea import Nest

context = Factor("context", ["mostly congruent", "mostly incongruent"])  # new: held for a whole mini-block
task = Factor("task", ["name the colour", "read the word"])              # new: held for a whole mini-block
```

### New: does the task change from one mini-block to the next?

A transition factor, as in step 2. Here it will look back one mini-block, not one trial.

```python
def task_repeats(task):
    return task[0] == task[-1]


def task_switches(task):
    return task[0] != task[-1]


task_transition = Factor("task_transition", [
    DerivedLevel("repeat", Transition(task_repeats, [task])),
    DerivedLevel("switch", Transition(task_switches, [task])),
])
```

### New: what the context makes frequent

In a mostly congruent mini-block the congruent trials are the frequent ones, in a mostly incongruent mini-block the incongruent ones. One derived factor says that for both: it follows from the colour, the word and the context. The third argument of a level is its weight: 3 to 1 is three quarters.

```python
def frequent_here(colour, word, context):
    congruent = colour == word
    return congruent == (context == "mostly congruent")


def rare_here(colour, word, context):
    return not frequent_here(colour, word, context)


frequency = Factor("frequency", [
    DerivedLevel("frequent", WithinTrial(frequent_here, [colour, word, context]), 3),
    DerivedLevel("rare", WithinTrial(rare_here, [colour, word, context]), 1),
])
```

### New: a block inside a block

Two blocks, each with its own crossing:

- **within a mini-block**: the frequency crossed with the ink colour, 12 trials;
- **between mini-blocks**: the context, the task and the task transition, 8 mini-blocks, plus a first one that has no mini-block before it.

`Nest` puts the first inside the second: every combination of the outer block is held for one whole mini-block.

```python
mini_block = CrossBlock(design=[colour, word, frequency, context],
                        crossing=[frequency, colour],
                        constraints=[])
between_mini_blocks = CrossBlock(design=[context, task, task_transition],
                                 crossing=[context, task, task_transition],
                                 constraints=[])
block = Nest(outer_block=between_mini_blocks, inner_block=mini_block, alignment="post preamble")
session = pd.DataFrame(synthesize_trials(block, 1, CMSGen)[0])

# columns for counting
session["congruency"] = ["congruent" if colour == word else "incongruent"
                         for colour, word in zip(session["colour"], session["word"])]
session.insert(0, "block", session.index // 12 + 1)
overview = session.groupby("block")[["context", "task", "task_transition"]].first()
overview["congruent trials"] = session.groupby("block")["congruency"].apply(lambda c: (c == "congruent").sum())
display(overview)
```

<div class="nb-out">
<table class="dataframe nb-table">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>context</th>
      <th>task</th>
      <th>task_transition</th>
      <th>congruent trials</th>
    </tr>
    <tr>
      <th>block</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>mostly incongruent</td>
      <td>name the colour</td>
      <td></td>
      <td>6</td>
    </tr>
    <tr>
      <th>2</th>
      <td>mostly incongruent</td>
      <td>name the colour</td>
      <td>repeat</td>
      <td>3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>mostly congruent</td>
      <td>name the colour</td>
      <td>repeat</td>
      <td>9</td>
    </tr>
    <tr>
      <th>4</th>
      <td>mostly incongruent</td>
      <td>read the word</td>
      <td>switch</td>
      <td>3</td>
    </tr>
    <tr>
      <th>5</th>
      <td>mostly congruent</td>
      <td>read the word</td>
      <td>repeat</td>
      <td>9</td>
    </tr>
    <tr>
      <th>6</th>
      <td>mostly incongruent</td>
      <td>name the colour</td>
      <td>switch</td>
      <td>3</td>
    </tr>
    <tr>
      <th>7</th>
      <td>mostly congruent</td>
      <td>read the word</td>
      <td>switch</td>
      <td>9</td>
    </tr>
    <tr>
      <th>8</th>
      <td>mostly incongruent</td>
      <td>read the word</td>
      <td>repeat</td>
      <td>3</td>
    </tr>
    <tr>
      <th>9</th>
      <td>mostly congruent</td>
      <td>name the colour</td>
      <td>switch</td>
      <td>9</td>
    </tr>
  </tbody>
</table>
</div>

One row per mini-block. The first has no task transition; it is the start. After it, every combination of context, task and transition comes once, and every mini-block has the proportion of its context: 9 or 3 of 12.

### Between mini-blocks: is everything crossed?

```python
counted = session[session["task_transition"] != ""]          # without the first mini-block
mini_blocks = counted.groupby("block")[["context", "task", "task_transition"]].first()
display(pd.crosstab([mini_blocks["context"], mini_blocks["task"]], mini_blocks["task_transition"]))
```

<div class="nb-out">
<table class="dataframe nb-table">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>task_transition</th>
      <th>repeat</th>
      <th>switch</th>
    </tr>
    <tr>
      <th>context</th>
      <th>task</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="2" valign="top">mostly congruent</th>
      <th>name the colour</th>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>read the word</th>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">mostly incongruent</th>
      <th>name the colour</th>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>read the word</th>
      <td>1</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>

### Within a mini-block: is the ink colour even?

```python
display(pd.crosstab([counted["block"], counted["context"]], [counted["congruency"], counted["colour"]]))
```

<div class="nb-out">
<table class="dataframe nb-table">
  <thead>
    <tr>
      <th></th>
      <th>congruency</th>
      <th colspan="3" halign="left">congruent</th>
      <th colspan="3" halign="left">incongruent</th>
    </tr>
    <tr>
      <th></th>
      <th>colour</th>
      <th>blue</th>
      <th>green</th>
      <th>red</th>
      <th>blue</th>
      <th>green</th>
      <th>red</th>
    </tr>
    <tr>
      <th>block</th>
      <th>context</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2</th>
      <th>mostly incongruent</th>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>3</td>
      <td>3</td>
    </tr>
    <tr>
      <th>3</th>
      <th>mostly congruent</th>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <th>mostly incongruent</th>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>3</td>
      <td>3</td>
    </tr>
    <tr>
      <th>5</th>
      <th>mostly congruent</th>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>6</th>
      <th>mostly incongruent</th>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>3</td>
      <td>3</td>
    </tr>
    <tr>
      <th>7</th>
      <th>mostly congruent</th>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>8</th>
      <th>mostly incongruent</th>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>3</td>
      <td>3</td>
    </tr>
    <tr>
      <th>9</th>
      <th>mostly congruent</th>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>

### What is not in the design?

The adaptation that is supposed to carry over was built up in the mini-block before. Its context is not in the crossing. Count it for the mini-blocks the switch cost is taken from.

```python
mini_blocks["context_before"] = session.groupby("block")["context"].first().shift()
reading = mini_blocks[mini_blocks["task"] == "read the word"]
display(reading[["context", "task_transition", "context_before"]])
```

<div class="nb-out">
<table class="dataframe nb-table">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>context</th>
      <th>task_transition</th>
      <th>context_before</th>
    </tr>
    <tr>
      <th>block</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4</th>
      <td>mostly incongruent</td>
      <td>switch</td>
      <td>mostly congruent</td>
    </tr>
    <tr>
      <th>5</th>
      <td>mostly congruent</td>
      <td>repeat</td>
      <td>mostly incongruent</td>
    </tr>
    <tr>
      <th>7</th>
      <td>mostly congruent</td>
      <td>switch</td>
      <td>mostly incongruent</td>
    </tr>
    <tr>
      <th>8</th>
      <td>mostly incongruent</td>
      <td>repeat</td>
      <td>mostly congruent</td>
    </tr>
  </tbody>
</table>
</div>

**Check.** Both crossings are exact. What is thin? Each cell of the comparison is one mini-block of 12 trials; more need a longer session or several sequences. Is the context of the mini-block before the same for switch and repeat? It is left to chance: run the block cell again and look. Should it be a factor too, and how many mini-blocks would that take?

**Try.** Add `MinimumTrials(17)` to the outer block: it counts mini-blocks, so that is two rounds plus the start.

**The idea.** Each question added a factor, and each factor multiplies the design. Nesting keeps both levels counterbalanced at once. What it leaves open is still a choice, and which choice is acceptable depends on what you compare.
