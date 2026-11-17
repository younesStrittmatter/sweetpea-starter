# Step 2. The trial before

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/younesStrittmatter/sweetpea-starter/blob/main/tutorial/notebooks/2_sequence.ipynb){ target=_blank } · [notebook](https://github.com/younesStrittmatter/sweetpea-starter/blob/main/tutorial/notebooks/2_sequence.ipynb) · [script](https://github.com/younesStrittmatter/sweetpea-starter/blob/main/tutorial/reference/step2_sequence.py)

## The experiment

A block from the design built on this page. Press play, or step through it.

<div class="stroop-demo" data-trials='[{"colour": "green", "word": "green", "congruency": "congruent", "trial_before": ""}, {"colour": "blue", "word": "blue", "congruency": "congruent", "trial_before": "congruent"}, {"colour": "green", "word": "green", "congruency": "congruent", "trial_before": "congruent"}, {"colour": "green", "word": "green", "congruency": "congruent", "trial_before": "congruent"}, {"colour": "blue", "word": "green", "congruency": "incongruent", "trial_before": "congruent"}, {"colour": "blue", "word": "blue", "congruency": "congruent", "trial_before": "incongruent"}, {"colour": "red", "word": "red", "congruency": "congruent", "trial_before": "congruent"}, {"colour": "blue", "word": "blue", "congruency": "congruent", "trial_before": "congruent"}, {"colour": "green", "word": "blue", "congruency": "incongruent", "trial_before": "congruent"}, {"colour": "red", "word": "green", "congruency": "incongruent", "trial_before": "incongruent"}, {"colour": "red", "word": "red", "congruency": "congruent", "trial_before": "incongruent"}, {"colour": "green", "word": "blue", "congruency": "incongruent", "trial_before": "congruent"}, {"colour": "green", "word": "blue", "congruency": "incongruent", "trial_before": "incongruent"}, {"colour": "red", "word": "red", "congruency": "congruent", "trial_before": "incongruent"}, {"colour": "red", "word": "red", "congruency": "congruent", "trial_before": "congruent"}, {"colour": "red", "word": "green", "congruency": "incongruent", "trial_before": "congruent"}, {"colour": "green", "word": "green", "congruency": "congruent", "trial_before": "incongruent"}, {"colour": "blue", "word": "green", "congruency": "incongruent", "trial_before": "congruent"}, {"colour": "red", "word": "green", "congruency": "incongruent", "trial_before": "incongruent"}, {"colour": "green", "word": "red", "congruency": "incongruent", "trial_before": "incongruent"}, {"colour": "green", "word": "green", "congruency": "congruent", "trial_before": "incongruent"}, {"colour": "red", "word": "blue", "congruency": "incongruent", "trial_before": "congruent"}, {"colour": "blue", "word": "green", "congruency": "incongruent", "trial_before": "incongruent"}, {"colour": "blue", "word": "green", "congruency": "incongruent", "trial_before": "incongruent"}, {"colour": "blue", "word": "blue", "congruency": "congruent", "trial_before": "incongruent"}]'></div>

## With your assistant

> Now I want to test whether the congruency effect depends on the trial before: is it smaller right after an incongruent trial? What is the hypothesis behind that, and what does the design need?

## Step by step

**So far.** Step 1 gave a block with half of the trials congruent: the ink colour crossed with congruency. This step keeps that block and adds one factor.

**The question.** Does a conflict change how the next trial is handled?

**Prediction (conflict adaptation).** The congruency effect is smaller after an incongruent trial than after a congruent one.

**The alternative to rule out.** Nothing is adjusted; trials that repeat a colour or a word from the trial before are simply faster, and such repeats are spread unevenly.

**The analysis.** The congruency effect after a congruent trial against the congruency effect after an incongruent trial.

### As in step 1

```python
import pandas as pd
from sweetpea import (Factor, DerivedLevel, WithinTrial, Transition, MinimumTrials,
                      CrossBlock, synthesize_trials, tabulate_experiments, CMSGen)

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

The crossing of step 1 with the trial before added: 12 combinations, two rounds, plus a first trial, which has no trial before.

```python
block = CrossBlock(design=[colour, word, congruency, trial_before],
                   crossing=[colour, congruency, trial_before],
                   constraints=[MinimumTrials(25)])
experiments = synthesize_trials(block, 1, CMSGen)
after_first = list(range(1, 25))        # the trials that have a trial before
tabulate_experiments(block, experiments, [trial_before, congruency], trials=after_first)
```

<div class="nb-out">
<pre>Experiment 0:
trial_before congruent   | congruency congruent   | frequency 6 | proportion 25.0%
trial_before congruent   | congruency incongruent | frequency 6 | proportion 25.0%
trial_before incongruent | congruency congruent   | frequency 6 | proportion 25.0%
trial_before incongruent | congruency incongruent | frequency 6 | proportion 25.0%</pre>
</div>

The four combinations are equal, and that is by design: run the cell again and they stay equal.

### What else repeats?

Does the ink colour, and so the response, repeat from the trial before? That is a transition factor too. Put it in the design but not in the crossing: SweetPea then records it and leaves it free. Count it in each of the four combinations.

```python
def response_repeats(colour):
    return colour[0] == colour[-1]


def response_changes(colour):
    return colour[0] != colour[-1]


response = Factor("response", [
    DerivedLevel("repeats", Transition(response_repeats, [colour])),
    DerivedLevel("changes", Transition(response_changes, [colour])),
])

block = CrossBlock(design=[colour, word, congruency, trial_before, response],
                   crossing=[colour, congruency, trial_before],
                   constraints=[MinimumTrials(25)])
experiments = synthesize_trials(block, 1, CMSGen)
tabulate_experiments(block, experiments, [trial_before, congruency, response], trials=after_first)
trials = pd.DataFrame(experiments[0])
```

<div class="nb-out">
<pre>Experiment 0:
trial_before congruent   | congruency congruent   | response repeats | frequency 2 | proportion 8.333333333333332%
trial_before congruent   | congruency congruent   | response changes | frequency 4 | proportion 16.666666666666664%
trial_before congruent   | congruency incongruent | response repeats | frequency 1 | proportion 4.166666666666666%
trial_before congruent   | congruency incongruent | response changes | frequency 5 | proportion 20.833333333333336%
trial_before incongruent | congruency congruent   | response repeats | frequency 4 | proportion 16.666666666666664%
trial_before incongruent | congruency congruent   | response changes | frequency 2 | proportion 8.333333333333332%
trial_before incongruent | congruency incongruent | response repeats | frequency 2 | proportion 8.333333333333332%
trial_before incongruent | congruency incongruent | response changes | frequency 4 | proportion 16.666666666666664%</pre>
</div>

**Check.** Is the response repeat equal across the four combinations? If not, the alternative explanation is still open. Whatever is not in the crossing is left to chance: run the block cell again and see which counts change.

**Try.** Ask what it would take to forbid all repeats (`Exclude` on a transition factor for the colour), and what that does to the four combinations.

**Next.** Step 3 goes from the trial before to the whole block: mostly congruent and mostly incongruent blocks.
