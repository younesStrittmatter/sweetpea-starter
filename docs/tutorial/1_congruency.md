# Step 1. Congruency

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/younesStrittmatter/sweetpea-starter/blob/main/tutorial/notebooks/1_congruency.ipynb){ target=_blank } · [notebook](https://github.com/younesStrittmatter/sweetpea-starter/blob/main/tutorial/notebooks/1_congruency.ipynb) · [script](https://github.com/younesStrittmatter/sweetpea-starter/blob/main/tutorial/reference/step1_congruency.py)

## The experiment

A block from the design built on this page. Press play, or step through it.

<div class="stroop-demo" data-trials='[{"colour": "green", "word": "blue", "congruency": "incongruent"}, {"colour": "blue", "word": "red", "congruency": "incongruent"}, {"colour": "red", "word": "blue", "congruency": "incongruent"}, {"colour": "green", "word": "red", "congruency": "incongruent"}, {"colour": "red", "word": "green", "congruency": "incongruent"}, {"colour": "blue", "word": "green", "congruency": "incongruent"}, {"colour": "green", "word": "green", "congruency": "congruent"}, {"colour": "blue", "word": "blue", "congruency": "congruent"}, {"colour": "green", "word": "red", "congruency": "incongruent"}, {"colour": "red", "word": "blue", "congruency": "incongruent"}, {"colour": "blue", "word": "blue", "congruency": "congruent"}, {"colour": "red", "word": "red", "congruency": "congruent"}, {"colour": "green", "word": "blue", "congruency": "incongruent"}, {"colour": "blue", "word": "red", "congruency": "incongruent"}, {"colour": "red", "word": "red", "congruency": "congruent"}, {"colour": "blue", "word": "blue", "congruency": "congruent"}, {"colour": "red", "word": "red", "congruency": "congruent"}, {"colour": "blue", "word": "green", "congruency": "incongruent"}, {"colour": "green", "word": "green", "congruency": "congruent"}, {"colour": "green", "word": "green", "congruency": "congruent"}, {"colour": "red", "word": "green", "congruency": "incongruent"}, {"colour": "blue", "word": "blue", "congruency": "congruent"}, {"colour": "red", "word": "red", "congruency": "congruent"}, {"colour": "green", "word": "green", "congruency": "congruent"}]'></div>

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
from sweetpea import (Factor, DerivedLevel, WithinTrial, Transition, Exclude, MinimumTrials,
                      CrossBlock, synthesize_trials, CMSGen)

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
trials_a = pd.DataFrame(synthesize_trials(block_a, 1, CMSGen)[0])
display(pd.crosstab(trials_a["colour"], trials_a["word"]))
display(trials_a["congruency"].value_counts().to_frame("trials"))
```

<div class="nb-out">
<table class="dataframe nb-table">
  <thead>
    <tr style="text-align: right;">
      <th>word</th>
      <th>blue</th>
      <th>green</th>
      <th>red</th>
    </tr>
    <tr>
      <th>colour</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>blue</th>
      <td>2</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>green</th>
      <td>2</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>red</th>
      <td>2</td>
      <td>2</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>

<div class="nb-out">
<table class="dataframe nb-table">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>trials</th>
    </tr>
    <tr>
      <th>congruency</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>incongruent</th>
      <td>12</td>
    </tr>
    <tr>
      <th>congruent</th>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>

### Option B: half of the trials congruent

Every pair once, and the congruent pairs a second time. Two helper factors do that: `copy` numbers the copies, and the copies that are too many are excluded. The helper is written once here and used again in steps 2 and 3.

```python
def pairs_with_copies(congruent_copies, incongruent_copies):
    """Two helper factors that make every congruent pair occur `congruent_copies` times
    and every incongruent pair `incongruent_copies` times."""
    copy = Factor("copy", [str(n) for n in range(1, max(congruent_copies, incongruent_copies) + 1)])

    def too_many(copy, colour, word):
        return int(copy) > (congruent_copies if colour == word else incongruent_copies)

    def wanted(copy, colour, word):
        return not too_many(copy, colour, word)

    extra_copy = Factor("extra_copy", [
        DerivedLevel("too many", WithinTrial(too_many, [copy, colour, word])),
        DerivedLevel("wanted", WithinTrial(wanted, [copy, colour, word])),
    ])
    return copy, extra_copy
```

```python
copy, extra_copy = pairs_with_copies(congruent_copies=2, incongruent_copies=1)
block_b = CrossBlock(design=[colour, word, congruency, copy, extra_copy],
                     crossing=[colour, word, copy],
                     constraints=[Exclude((extra_copy, "too many")), MinimumTrials(24)],
                     require_complete_crossing=False)
trials_b = pd.DataFrame(synthesize_trials(block_b, 1, CMSGen)[0])
display(pd.crosstab(trials_b["colour"], trials_b["word"]))
display(trials_b["congruency"].value_counts().to_frame("trials"))
```

<div class="nb-out">
<table class="dataframe nb-table">
  <thead>
    <tr style="text-align: right;">
      <th>word</th>
      <th>blue</th>
      <th>green</th>
      <th>red</th>
    </tr>
    <tr>
      <th>colour</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>blue</th>
      <td>4</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>green</th>
      <td>2</td>
      <td>4</td>
      <td>2</td>
    </tr>
    <tr>
      <th>red</th>
      <td>2</td>
      <td>2</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>

<div class="nb-out">
<table class="dataframe nb-table">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>trials</th>
    </tr>
    <tr>
      <th>congruency</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>incongruent</th>
      <td>12</td>
    </tr>
    <tr>
      <th>congruent</th>
      <td>12</td>
    </tr>
  </tbody>
</table>
</div>

### What does each option cost?

How often is a word shown in its own colour? One third means the word tells nothing about the ink.

```python
cost = pd.DataFrame({
    "congruent trials (%)": [round((t["congruency"] == "congruent").mean() * 100) for t in (trials_a, trials_b)],
    "word is in its own colour (%)": [round((t["word"] == t["colour"]).mean() * 100) for t in (trials_a, trials_b)],
}, index=["A: every pair equally often", "B: half congruent"])
display(cost)
```

<div class="nb-out">
<table class="dataframe nb-table">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>congruent trials (%)</th>
      <th>word is in its own colour (%)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>A: every pair equally often</th>
      <td>33</td>
      <td>33</td>
    </tr>
    <tr>
      <th>B: half congruent</th>
      <td>50</td>
      <td>50</td>
    </tr>
  </tbody>
</table>
</div>

**Check.** In which option could a participant guess the ink from the word? In which are there fewer congruent trials? Neither is free: which cost is acceptable depends on what you compare.

**Try.** Add a fourth colour to `colours` and run again. What happens to the share of congruent trials in option A?

**Next.** Step 2 keeps option B and asks what happened on the trial before.
