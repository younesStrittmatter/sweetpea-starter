# Step 2. The trial before

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/younesStrittmatter/sweetpea-starter/blob/main/tutorial/notebooks/2_sequence.ipynb){ target=_blank } · [notebook](https://github.com/younesStrittmatter/sweetpea-starter/blob/main/tutorial/notebooks/2_sequence.ipynb) · [script](https://github.com/younesStrittmatter/sweetpea-starter/blob/main/tutorial/reference/step2_sequence.py)

## The experiment

A block from the design built on this page. Press play, or step through it.

<div class="stroop-demo" data-trials='[{"colour": "green", "word": "blue", "congruency": "incongruent", "trial_before": ""}, {"colour": "green", "word": "green", "congruency": "congruent", "trial_before": "incongruent"}, {"colour": "blue", "word": "blue", "congruency": "congruent", "trial_before": "congruent"}, {"colour": "blue", "word": "blue", "congruency": "congruent", "trial_before": "congruent"}, {"colour": "green", "word": "green", "congruency": "congruent", "trial_before": "congruent"}, {"colour": "red", "word": "blue", "congruency": "incongruent", "trial_before": "congruent"}, {"colour": "red", "word": "red", "congruency": "congruent", "trial_before": "incongruent"}, {"colour": "blue", "word": "red", "congruency": "incongruent", "trial_before": "congruent"}, {"colour": "red", "word": "blue", "congruency": "incongruent", "trial_before": "incongruent"}, {"colour": "green", "word": "blue", "congruency": "incongruent", "trial_before": "incongruent"}, {"colour": "green", "word": "green", "congruency": "congruent", "trial_before": "incongruent"}, {"colour": "red", "word": "red", "congruency": "congruent", "trial_before": "congruent"}, {"colour": "red", "word": "red", "congruency": "congruent", "trial_before": "congruent"}, {"colour": "green", "word": "red", "congruency": "incongruent", "trial_before": "congruent"}, {"colour": "red", "word": "green", "congruency": "incongruent", "trial_before": "incongruent"}, {"colour": "blue", "word": "green", "congruency": "incongruent", "trial_before": "incongruent"}, {"colour": "blue", "word": "red", "congruency": "incongruent", "trial_before": "incongruent"}, {"colour": "green", "word": "red", "congruency": "incongruent", "trial_before": "incongruent"}, {"colour": "blue", "word": "blue", "congruency": "congruent", "trial_before": "incongruent"}, {"colour": "green", "word": "blue", "congruency": "incongruent", "trial_before": "congruent"}, {"colour": "red", "word": "red", "congruency": "congruent", "trial_before": "incongruent"}, {"colour": "green", "word": "green", "congruency": "congruent", "trial_before": "congruent"}, {"colour": "blue", "word": "green", "congruency": "incongruent", "trial_before": "congruent"}, {"colour": "blue", "word": "blue", "congruency": "congruent", "trial_before": "incongruent"}, {"colour": "red", "word": "green", "congruency": "incongruent", "trial_before": "congruent"}]'></div>

## With your assistant

> Now I want to test whether the congruency effect depends on the trial before: is it smaller right after an incongruent trial? What is the hypothesis behind that, and what does the design need?

## Step by step

**So far.** Step 1 gave a block with half of the trials congruent and every pair of a kind equally often. This step keeps that block and adds one factor.

**The question.** Does a conflict change how the next trial is handled?

**Prediction (conflict adaptation).** The congruency effect is smaller after an incongruent trial than after a congruent one.

**The alternative to rule out.** Nothing is adjusted; trials that repeat a colour or a word from the trial before are simply faster, and such repeats are spread unevenly.

**The analysis.** The congruency effect after a congruent trial against the congruency effect after an incongruent trial.

### As in step 1

```python
import pandas as pd
from sweetpea import (Factor, DerivedLevel, WithinTrial, Transition, Exclude, MinimumTrials,
                      CrossBlock, synthesize_trials, CMSGen)

colours = ["red", "green", "blue"]

# regular factors: set freely on every trial
colour = Factor("colour", colours)      # the ink
word = Factor("word", colours)          # what the word says
```

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

### New: the trial before as a factor

A transition factor follows from the trial before: `[0]` is this trial, `[-1]` the one before.

```python
def after_congruent(colour, word):
    return colour[-1] == word[-1]


def after_incongruent(colour, word):
    return colour[-1] != word[-1]


trial_before = Factor("trial_before", [
    DerivedLevel("congruent", Transition(after_congruent, [colour, word])),
    DerivedLevel("incongruent", Transition(after_incongruent, [colour, word])),
])
```

### The block

The block of step 1, crossed with the trial before: 12 trials times 2 is 24, plus a first trial, which has no trial before.

```python
copy, extra_copy = pairs_with_copies(congruent_copies=2, incongruent_copies=1)
block = CrossBlock(design=[colour, word, congruency, copy, extra_copy, trial_before],
                   crossing=[colour, word, copy, trial_before],
                   constraints=[Exclude((extra_copy, "too many")), MinimumTrials(25)],
                   require_complete_crossing=False)
trials = pd.DataFrame(synthesize_trials(block, 1, CMSGen)[0])
rest = trials.iloc[1:]                  # without the first trial
display(pd.crosstab(rest["trial_before"], rest["congruency"]))
```

<div class="nb-out">
<table class="dataframe nb-table">
  <thead>
    <tr style="text-align: right;">
      <th>congruency</th>
      <th>congruent</th>
      <th>incongruent</th>
    </tr>
    <tr>
      <th>trial_before</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>congruent</th>
      <td>6</td>
      <td>6</td>
    </tr>
    <tr>
      <th>incongruent</th>
      <td>6</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>

The four combinations are equal, and that is by design: run the cell again and they stay equal.

### What else repeats?

Not in the design: does the ink colour, and so the response, repeat from the trial before? Count it in each of the four combinations.

```python
trials["response_repeats"] = trials["colour"].eq(trials["colour"].shift())
rest = trials.iloc[1:]
display(pd.crosstab([rest["trial_before"], rest["congruency"]], rest["response_repeats"]))
```

<div class="nb-out">
<table class="dataframe nb-table">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>response_repeats</th>
      <th>False</th>
      <th>True</th>
    </tr>
    <tr>
      <th>trial_before</th>
      <th>congruency</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="2" valign="top">congruent</th>
      <th>congruent</th>
      <td>4</td>
      <td>2</td>
    </tr>
    <tr>
      <th>incongruent</th>
      <td>6</td>
      <td>0</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">incongruent</th>
      <th>congruent</th>
      <td>2</td>
      <td>4</td>
    </tr>
    <tr>
      <th>incongruent</th>
      <td>5</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>

**Check.** Is the response repeat equal across the four combinations? If not, the alternative explanation is still open. Whatever is not in the crossing is left to chance: run the block cell again and see which counts change.

**Try.** Ask what it would take to forbid all repeats (`Exclude` on a transition factor for the colour), and what that does to the four combinations.

**Next.** Step 3 goes from the trial before to the whole block: mostly congruent and mostly incongruent blocks.
