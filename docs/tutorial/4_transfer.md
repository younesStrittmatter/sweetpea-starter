# Step 4. Transfer

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/younesStrittmatter/sweetpea-starter/blob/main/tutorial/notebooks/4_transfer.ipynb){ target=_blank } · [notebook](https://github.com/younesStrittmatter/sweetpea-starter/blob/main/tutorial/notebooks/4_transfer.ipynb) · [script](https://github.com/younesStrittmatter/sweetpea-starter/blob/main/tutorial/reference/step4_transfer.py)

## The experiment

A block from the design built on this page. Press play, or step through it.

<div class="stroop-demo" data-trials='[{"block": 1, "context": "mostly congruent", "task": "name the colour", "colour": "green", "word": "red", "congruency": "incongruent", "transition": ""}, {"block": 1, "context": "mostly congruent", "task": "name the colour", "colour": "green", "word": "green", "congruency": "congruent", "transition": "repeat"}, {"block": 1, "context": "mostly congruent", "task": "name the colour", "colour": "blue", "word": "blue", "congruency": "congruent", "transition": "repeat"}, {"block": 1, "context": "mostly congruent", "task": "read the word", "colour": "blue", "word": "blue", "congruency": "congruent", "transition": "switch"}, {"block": 1, "context": "mostly congruent", "task": "read the word", "colour": "blue", "word": "blue", "congruency": "congruent", "transition": "repeat"}, {"block": 1, "context": "mostly congruent", "task": "name the colour", "colour": "blue", "word": "blue", "congruency": "congruent", "transition": "switch"}, {"block": 1, "context": "mostly congruent", "task": "read the word", "colour": "green", "word": "green", "congruency": "congruent", "transition": "switch"}, {"block": 1, "context": "mostly congruent", "task": "read the word", "colour": "green", "word": "blue", "congruency": "incongruent", "transition": "repeat"}, {"block": 1, "context": "mostly congruent", "task": "name the colour", "colour": "blue", "word": "blue", "congruency": "congruent", "transition": "switch"}, {"block": 1, "context": "mostly congruent", "task": "name the colour", "colour": "red", "word": "red", "congruency": "congruent", "transition": "repeat"}, {"block": 1, "context": "mostly congruent", "task": "name the colour", "colour": "blue", "word": "red", "congruency": "incongruent", "transition": "repeat"}, {"block": 1, "context": "mostly congruent", "task": "read the word", "colour": "red", "word": "red", "congruency": "congruent", "transition": "switch"}, {"block": 1, "context": "mostly congruent", "task": "read the word", "colour": "red", "word": "red", "congruency": "congruent", "transition": "repeat"}, {"block": 1, "context": "mostly congruent", "task": "read the word", "colour": "blue", "word": "blue", "congruency": "congruent", "transition": "repeat"}, {"block": 1, "context": "mostly congruent", "task": "name the colour", "colour": "red", "word": "green", "congruency": "incongruent", "transition": "switch"}, {"block": 1, "context": "mostly congruent", "task": "read the word", "colour": "green", "word": "red", "congruency": "incongruent", "transition": "switch"}, {"block": 1, "context": "mostly congruent", "task": "name the colour", "colour": "green", "word": "green", "congruency": "congruent", "transition": "switch"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "blue", "word": "blue", "congruency": "congruent", "transition": ""}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "green", "word": "blue", "congruency": "incongruent", "transition": "repeat"}, {"block": 2, "context": "mostly incongruent", "task": "read the word", "colour": "blue", "word": "green", "congruency": "incongruent", "transition": "switch"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "red", "word": "blue", "congruency": "incongruent", "transition": "switch"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "green", "word": "red", "congruency": "incongruent", "transition": "repeat"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "green", "word": "green", "congruency": "congruent", "transition": "repeat"}, {"block": 2, "context": "mostly incongruent", "task": "read the word", "colour": "red", "word": "blue", "congruency": "incongruent", "transition": "switch"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "red", "word": "blue", "congruency": "incongruent", "transition": "switch"}, {"block": 2, "context": "mostly incongruent", "task": "read the word", "colour": "red", "word": "green", "congruency": "incongruent", "transition": "switch"}, {"block": 2, "context": "mostly incongruent", "task": "read the word", "colour": "red", "word": "blue", "congruency": "incongruent", "transition": "repeat"}, {"block": 2, "context": "mostly incongruent", "task": "read the word", "colour": "blue", "word": "blue", "congruency": "congruent", "transition": "repeat"}, {"block": 2, "context": "mostly incongruent", "task": "read the word", "colour": "blue", "word": "green", "congruency": "incongruent", "transition": "repeat"}, {"block": 2, "context": "mostly incongruent", "task": "read the word", "colour": "blue", "word": "red", "congruency": "incongruent", "transition": "repeat"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "red", "word": "red", "congruency": "congruent", "transition": "switch"}, {"block": 2, "context": "mostly incongruent", "task": "read the word", "colour": "blue", "word": "blue", "congruency": "congruent", "transition": "switch"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "green", "word": "red", "congruency": "incongruent", "transition": "switch"}, {"block": 2, "context": "mostly incongruent", "task": "name the colour", "colour": "green", "word": "blue", "congruency": "incongruent", "transition": "repeat"}, {"block": 3, "context": "mostly incongruent", "task": "name the colour", "colour": "blue", "word": "green", "congruency": "incongruent", "transition": ""}, {"block": 3, "context": "mostly incongruent", "task": "name the colour", "colour": "red", "word": "green", "congruency": "incongruent", "transition": "repeat"}, {"block": 3, "context": "mostly incongruent", "task": "read the word", "colour": "red", "word": "green", "congruency": "incongruent", "transition": "switch"}, {"block": 3, "context": "mostly incongruent", "task": "read the word", "colour": "green", "word": "red", "congruency": "incongruent", "transition": "repeat"}, {"block": 3, "context": "mostly incongruent", "task": "name the colour", "colour": "green", "word": "red", "congruency": "incongruent", "transition": "switch"}, {"block": 3, "context": "mostly incongruent", "task": "name the colour", "colour": "red", "word": "green", "congruency": "incongruent", "transition": "repeat"}, {"block": 3, "context": "mostly incongruent", "task": "read the word", "colour": "blue", "word": "blue", "congruency": "congruent", "transition": "switch"}, {"block": 3, "context": "mostly incongruent", "task": "name the colour", "colour": "green", "word": "green", "congruency": "congruent", "transition": "switch"}, {"block": 3, "context": "mostly incongruent", "task": "read the word", "colour": "green", "word": "red", "congruency": "incongruent", "transition": "switch"}, {"block": 3, "context": "mostly incongruent", "task": "read the word", "colour": "green", "word": "green", "congruency": "congruent", "transition": "repeat"}, {"block": 3, "context": "mostly incongruent", "task": "read the word", "colour": "blue", "word": "red", "congruency": "incongruent", "transition": "repeat"}, {"block": 3, "context": "mostly incongruent", "task": "read the word", "colour": "green", "word": "blue", "congruency": "incongruent", "transition": "repeat"}, {"block": 3, "context": "mostly incongruent", "task": "name the colour", "colour": "green", "word": "red", "congruency": "incongruent", "transition": "switch"}, {"block": 3, "context": "mostly incongruent", "task": "name the colour", "colour": "green", "word": "green", "congruency": "congruent", "transition": "repeat"}]'></div>

## With your assistant

> Last question. I want to know whether this control setting has a price: if people shield the task more in a mostly incongruent context, are they then worse at switching to another task? I add a second task: on some trials people read the word instead of naming the ink, and a cue says which. I want mini-blocks that are mostly congruent or mostly incongruent, and to compare the switch cost between them. What is the hypothesis, and what does the design need?

## Step by step

**So far.** Step 2 made the trial before a factor, and step 3 made blocks that are mostly congruent or mostly incongruent. This step puts both ideas together and adds a second task.

**The question.** Does adapting to frequent conflict make it harder to switch to another task?

**Prediction if shielding and switching are one control setting.** The switch cost is larger in a mostly incongruent context than in a mostly congruent one.

**The alternative to rule out.** A mostly incongruent context is simply harder, so everything is slower there.

**The analysis.** The switch cost (switch against repeat trials) in mostly incongruent mini-blocks against mostly congruent mini-blocks.

### As before, plus a second task

A cue says on each trial whether to name the ink or read the word. The task is a regular factor.

```python
import pandas as pd
from sweetpea import (Factor, DerivedLevel, WithinTrial, Transition, Exclude, MinimumTrials,
                      CrossBlock, synthesize_trials, CMSGen)

colours = ["red", "green", "blue"]

# regular factors: set freely on every trial
colour = Factor("colour", colours)      # the ink
word = Factor("word", colours)          # what the word says
task = Factor("task", ["name the colour", "read the word"])        # new: a second task, with a cue
```

### New: the task transition

A transition factor, as in step 2, but on the task: does it repeat or switch? Without repeat trials in the same context there is no switch cost to measure.

```python
def task_repeats(task):
    return task[0] == task[-1]


def task_switches(task):
    return task[0] != task[-1]


transition = Factor("transition", [
    DerivedLevel("repeat", Transition(task_repeats, [task])),
    DerivedLevel("switch", Transition(task_switches, [task])),
])
```

### Something has to give

The blocks of step 3 hold 24 trials. Crossed with 2 tasks and 2 transitions that is 96 trials per mini-block: too long for a context that should change often.

So this design crosses what the analysis compares, congruency, the task and the transition, and gives up the even pairs. Congruency gets a weight instead of copies: the third argument of a level. 3 to 1 is three quarters. That is 16 combinations, plus a first trial.

```python
WEIGHTS = {"mostly congruent": (3, 1), "mostly incongruent": (1, 3)}     # (congruent, incongruent)


def same(colour, word):
    return colour == word


def different(colour, word):
    return colour != word


def mini_block(context):
    congruent_weight, incongruent_weight = WEIGHTS[context]
    congruency = Factor("congruency", [
        DerivedLevel("congruent", WithinTrial(same, [colour, word]), congruent_weight),
        DerivedLevel("incongruent", WithinTrial(different, [colour, word]), incongruent_weight),
    ])
    return CrossBlock(design=[colour, word, task, congruency, transition],
                      crossing=[congruency, task, transition],
                      constraints=[MinimumTrials(17)])
```

### A session of four mini-blocks

```python
blocks = []
for number, context in enumerate(["mostly congruent", "mostly incongruent", "mostly incongruent", "mostly congruent"], start=1):
    trials = pd.DataFrame(synthesize_trials(mini_block(context), 1, CMSGen)[0])
    trials.insert(0, "context", context)
    trials.insert(0, "block", number)
    blocks.append(trials)
session = pd.concat(blocks, ignore_index=True)
counted = session[session["transition"] != ""]       # the first trial of a mini-block has no transition
display(pd.crosstab(counted["context"], [counted["transition"], counted["congruency"]]))
```

<div class="nb-out">
<table class="dataframe nb-table">
  <thead>
    <tr>
      <th>transition</th>
      <th colspan="2" halign="left">repeat</th>
      <th colspan="2" halign="left">switch</th>
    </tr>
    <tr>
      <th>congruency</th>
      <th>congruent</th>
      <th>incongruent</th>
      <th>congruent</th>
      <th>incongruent</th>
    </tr>
    <tr>
      <th>context</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>mostly congruent</th>
      <td>12</td>
      <td>4</td>
      <td>12</td>
      <td>4</td>
    </tr>
    <tr>
      <th>mostly incongruent</th>
      <td>4</td>
      <td>12</td>
      <td>4</td>
      <td>12</td>
    </tr>
  </tbody>
</table>
</div>

### What gave way?

The ink colour and the pairs are no longer in the crossing. Count them.

```python
display(pd.crosstab(counted["context"], counted["colour"]))
display(pd.crosstab([counted["context"], counted["colour"]], counted["word"]))
```

<div class="nb-out">
<table class="dataframe nb-table">
  <thead>
    <tr style="text-align: right;">
      <th>colour</th>
      <th>blue</th>
      <th>green</th>
      <th>red</th>
    </tr>
    <tr>
      <th>context</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>mostly congruent</th>
      <td>12</td>
      <td>9</td>
      <td>11</td>
    </tr>
    <tr>
      <th>mostly incongruent</th>
      <td>7</td>
      <td>13</td>
      <td>12</td>
    </tr>
  </tbody>
</table>
</div>

<div class="nb-out">
<table class="dataframe nb-table">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>word</th>
      <th>blue</th>
      <th>green</th>
      <th>red</th>
    </tr>
    <tr>
      <th>context</th>
      <th>colour</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="3" valign="top">mostly congruent</th>
      <th>blue</th>
      <td>10</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>green</th>
      <td>2</td>
      <td>6</td>
      <td>1</td>
    </tr>
    <tr>
      <th>red</th>
      <td>1</td>
      <td>2</td>
      <td>8</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">mostly incongruent</th>
      <th>blue</th>
      <td>3</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>green</th>
      <td>3</td>
      <td>4</td>
      <td>6</td>
    </tr>
    <tr>
      <th>red</th>
      <td>5</td>
      <td>6</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>

**Check.** Is there a repeat baseline in each context? How many incongruent switch trials does a mostly congruent mini-block have? Are the ink colours and the pairs still even, and does that matter for the switch cost?

**The idea.** Each question added a factor, and each factor multiplies the design. At some point not everything fits, and the design becomes a choice about what to leave open. Which choice is acceptable depends on what you compare.
