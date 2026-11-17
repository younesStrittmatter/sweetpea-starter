# Step 1. Congruency

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/younesStrittmatter/sweetpea-starter/blob/main/tutorial/notebooks/1_congruency.ipynb){ target=_blank } · [notebook](https://github.com/younesStrittmatter/sweetpea-starter/blob/main/tutorial/notebooks/1_congruency.ipynb) · [script](https://github.com/younesStrittmatter/sweetpea-starter/blob/main/tutorial/reference/step1_congruency.py)

## The experiment

A block from the design built on this page. Press play, or step through it.

<div class="stroop-demo" data-trials='[{"colour": "green", "word": "green", "congruency": "congruent"}, {"colour": "red", "word": "red", "congruency": "congruent"}, {"colour": "red", "word": "green", "congruency": "incongruent"}, {"colour": "green", "word": "red", "congruency": "incongruent"}, {"colour": "blue", "word": "red", "congruency": "incongruent"}, {"colour": "red", "word": "red", "congruency": "congruent"}, {"colour": "blue", "word": "blue", "congruency": "congruent"}, {"colour": "green", "word": "blue", "congruency": "incongruent"}, {"colour": "green", "word": "green", "congruency": "congruent"}, {"colour": "green", "word": "green", "congruency": "congruent"}, {"colour": "green", "word": "blue", "congruency": "incongruent"}, {"colour": "blue", "word": "blue", "congruency": "congruent"}, {"colour": "blue", "word": "blue", "congruency": "congruent"}, {"colour": "blue", "word": "green", "congruency": "incongruent"}, {"colour": "green", "word": "red", "congruency": "incongruent"}, {"colour": "blue", "word": "green", "congruency": "incongruent"}, {"colour": "red", "word": "red", "congruency": "congruent"}, {"colour": "blue", "word": "blue", "congruency": "congruent"}, {"colour": "red", "word": "blue", "congruency": "incongruent"}, {"colour": "red", "word": "red", "congruency": "congruent"}, {"colour": "blue", "word": "red", "congruency": "incongruent"}, {"colour": "green", "word": "green", "congruency": "congruent"}, {"colour": "red", "word": "green", "congruency": "incongruent"}, {"colour": "red", "word": "blue", "congruency": "incongruent"}]'></div>

## With your assistant

> I want to run a Stroop experiment to test the congruency effect. What is it about, and what do I need to decide?

## Step by step

**The question.** Does an irrelevant word interfere with naming a colour?

**Prediction.** Naming the ink is slower when the word names another colour (incongruent) than when it names the same one (congruent). The difference is the congruency effect.

**The analysis.** Response time on congruent trials against incongruent trials.

**The decision.** With three colours there are 3 congruent and 6 incongruent pairs of ink and word. Two wishes pull apart: *every pair equally often* (then one third of the trials is congruent) or *half of the trials congruent* (then the word tells something about the ink). This page builds both and counts them.

### The factors

A regular factor is set freely on every trial. The ink colour and the word are regular factors.

```python
import pandas as pd
from sweetpea import (Factor, DerivedLevel, WithinTrial, Transition, MinimumTrials,
                      CrossBlock, synthesize_trials, tabulate_experiments, CMSGen)

colours = ["red", "green", "blue"]

# regular factors: set freely on every trial
colour = Factor("colour", colours)      # the ink
word = Factor("word", colours)          # what the word says
```

Congruency is not set freely: it follows from the colour and the word. That is a derived factor.

```python
# a derived factor: it follows from colour and word on the same trial
def same(colour, word):
    return colour == word


def different(colour, word):
    return colour != word


congruency = Factor("congruency", [
    DerivedLevel("congruent", WithinTrial(same, [colour, word])),
    DerivedLevel("incongruent", WithinTrial(different, [colour, word])),
])
```

### Option A: every pair equally often

Colour and word are crossed, so each of the 9 pairs occurs equally often. `MinimumTrials(18)` asks for two rounds of the crossing.

```python
block_a = CrossBlock(design=[colour, word, congruency], crossing=[colour, word],
                     constraints=[MinimumTrials(18)])
experiments_a = synthesize_trials(block_a, 1, CMSGen)
tabulate_experiments(block_a, experiments_a, [colour, word])
tabulate_experiments(block_a, experiments_a, [congruency])
```

<div class="nb-out">
<pre>Experiment 0:
colour red   | word red   | frequency 2 | proportion 11.11111111111111%
colour red   | word green | frequency 2 | proportion 11.11111111111111%
colour red   | word blue  | frequency 2 | proportion 11.11111111111111%
colour green | word red   | frequency 2 | proportion 11.11111111111111%
colour green | word green | frequency 2 | proportion 11.11111111111111%
colour green | word blue  | frequency 2 | proportion 11.11111111111111%
colour blue  | word red   | frequency 2 | proportion 11.11111111111111%
colour blue  | word green | frequency 2 | proportion 11.11111111111111%
colour blue  | word blue  | frequency 2 | proportion 11.11111111111111%

Experiment 0:
congruency congruent   | frequency 6  | proportion 33.33333333333333%
congruency incongruent | frequency 12 | proportion 66.66666666666666%</pre>
</div>

`tabulate_experiments` is SweetPea's own count: how often each combination of the factors you name occurs, and its share.

### Option B: half of the trials congruent

Cross the ink colour with congruency. Each ink colour is then congruent on half of its trials: 6 combinations, four rounds.

```python
block_b = CrossBlock(design=[colour, word, congruency], crossing=[colour, congruency],
                     constraints=[MinimumTrials(24)])
experiments_b = synthesize_trials(block_b, 1, CMSGen)
tabulate_experiments(block_b, experiments_b, [colour, congruency])
tabulate_experiments(block_b, experiments_b, [colour, word])
```

<div class="nb-out">
<pre>Experiment 0:
colour red   | congruency congruent   | frequency 4 | proportion 16.666666666666664%
colour red   | congruency incongruent | frequency 4 | proportion 16.666666666666664%
colour green | congruency congruent   | frequency 4 | proportion 16.666666666666664%
colour green | congruency incongruent | frequency 4 | proportion 16.666666666666664%
colour blue  | congruency congruent   | frequency 4 | proportion 16.666666666666664%
colour blue  | congruency incongruent | frequency 4 | proportion 16.666666666666664%

Experiment 0:
colour red   | word red   | frequency 4 | proportion 16.666666666666664%
colour red   | word green | frequency 2 | proportion 8.333333333333332%
colour red   | word blue  | frequency 2 | proportion 8.333333333333332%
colour green | word red   | frequency 2 | proportion 8.333333333333332%
colour green | word green | frequency 4 | proportion 16.666666666666664%
colour green | word blue  | frequency 2 | proportion 8.333333333333332%
colour blue  | word red   | frequency 2 | proportion 8.333333333333332%
colour blue  | word green | frequency 2 | proportion 8.333333333333332%
colour blue  | word blue  | frequency 4 | proportion 16.666666666666664%</pre>
</div>

The first table is what was crossed: it is even. The second shows what was not: which word goes with an incongruent ink is left open, so those pairs can come out uneven. Run the cell again and compare.

### What does each option cost?

A congruent trial is a word in its own colour. In option A that is one third of the trials: the word tells nothing about the ink. In option B it is half: the word tells something.

### The sequence as a table

One row per trial, for your experiment software.

```python
trials_a = pd.DataFrame(experiments_a[0])
trials_b = pd.DataFrame(experiments_b[0])
display(trials_b.head(8))
```

<div class="nb-out">
<table class="dataframe nb-table">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>colour</th>
      <th>word</th>
      <th>congruency</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>green</td>
      <td>green</td>
      <td>congruent</td>
    </tr>
    <tr>
      <th>1</th>
      <td>red</td>
      <td>red</td>
      <td>congruent</td>
    </tr>
    <tr>
      <th>2</th>
      <td>red</td>
      <td>green</td>
      <td>incongruent</td>
    </tr>
    <tr>
      <th>3</th>
      <td>green</td>
      <td>red</td>
      <td>incongruent</td>
    </tr>
    <tr>
      <th>4</th>
      <td>blue</td>
      <td>red</td>
      <td>incongruent</td>
    </tr>
    <tr>
      <th>5</th>
      <td>red</td>
      <td>red</td>
      <td>congruent</td>
    </tr>
    <tr>
      <th>6</th>
      <td>blue</td>
      <td>blue</td>
      <td>congruent</td>
    </tr>
    <tr>
      <th>7</th>
      <td>green</td>
      <td>blue</td>
      <td>incongruent</td>
    </tr>
  </tbody>
</table>
</div>

**Check.** In which option could a participant guess the ink from the word? In which are there fewer congruent trials? Neither is free: which cost is acceptable depends on what you compare.

**Try.** Add a fourth colour to `colours` and run again. What happens to the share of congruent trials in option A?

**Next.** Step 2 keeps option B and asks what happened on the trial before.
