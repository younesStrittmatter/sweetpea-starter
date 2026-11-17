# The trial before

If every trial type is shown equally often, does it matter what came before?

Based on Dunaway & Weissman (2026), *Psychological Research*, Experiment 4.
[doi:10.1007/s00426-025-02216-y](https://doi.org/10.1007/s00426-025-02216-y)

## The task and the question

Scroll, or use the buttons under each block.

<script src="data.js"></script>
<div class="sm-intro"></div>

## From the original design to a better one

The original shuffles its trials in sets of twelve. Smaller sets show the same
thing more strongly.

<div class="sm-switch"></div>

<div class="sm-story"></div>

Nobody decided that a trial should follow its own type less often. It follows
from shuffling small sets. The side of the square, the response and the square
itself are affected in the same way, and the design balances those too.

## What is simplified

The original shows a word before the square, which gives twelve combinations
per set. The page leaves the word out. Sets of four and of two are not in the
original.

## In SweetPea

The code for the sets chosen above.

<div class="sm-variant" data-v="2" markdown="1">

A set is one congruent and one incongruent square. Two blocks, merged. Each says what is even within its own length: the first is one set, the second the whole block. `Merge` repeats the set until the block is full. So inside a set congruency is even and the transitions are free; over the block the transitions are even.

```python
from sweetpea import (Factor, DerivedLevel, WithinTrial, Transition, MinimumTrials,
                      MultiCrossBlock, Merge, RepeatMode, AlignmentMode, synthesize_trials, CMSGen)

side = Factor("side", ["left", "right"])
colour = Factor("colour", ["red", "green"])

# Congruency: does the square appear on the side of its key?
key = {"red": "left", "green": "right"}

def on_key_side(side, colour):
    return key[colour] == side

def on_other_side(side, colour):
    return key[colour] != side

congruency = Factor("congruency", [
    DerivedLevel("congruent", WithinTrial(on_key_side, [side, colour])),
    DerivedLevel("incongruent", WithinTrial(on_other_side, [side, colour])),
])

# Does the side repeat from the trial before? Does the colour?  [0] is this trial, [-1] the one before.
def repeats(factor):
    return factor[0] == factor[-1]

def changes(factor):
    return factor[0] != factor[-1]

side_repeats = Factor("side_repeats", [
    DerivedLevel("repeats", Transition(repeats, [side])),
    DerivedLevel("changes", Transition(changes, [side])),
])
colour_repeats = Factor("colour_repeats", [
    DerivedLevel("repeats", Transition(repeats, [colour])),
    DerivedLevel("changes", Transition(changes, [colour])),
])

# One set: 2 trials, one congruent and one incongruent square.
one_set = MultiCrossBlock(design=[side, colour, congruency], crossings=[[congruency]],
                          constraints=[MinimumTrials(2)],             # the set size
                          mode=RepeatMode.WEIGHT, alignment=AlignmentMode.PARALLEL_START)

# The whole block: 33 trials (16 sets, and a first trial that has no trial before).
# Side repeats or not, crossed with colour repeats or not, equally often anywhere in it.
transitions = MultiCrossBlock(design=[side, colour, side_repeats, colour_repeats],
                              crossings=[[side_repeats, colour_repeats]],
                              constraints=[MinimumTrials(33)],         # the block length
                              mode=RepeatMode.WEIGHT, alignment=AlignmentMode.PARALLEL_START)

# Both at once: the set is repeated until the block is full.
block = Merge([one_set, transitions], alignment=AlignmentMode.PARALLEL_START)
trials = synthesize_trials(block, 1, CMSGen)[0]
```

The generated block: 33 trials, every set intact; trial type, side and response each repeat on half of the trials, the same square on a quarter.

</div>

<div class="sm-variant" data-v="4" markdown="1">

A set is each of the four squares once. Two blocks, merged. Each says what is even within its own length: the first is one set, the second the whole block. `Merge` repeats the set until the block is full. So inside a set the squares are even and the transitions are free; over the block the transitions are even.

```python
from sweetpea import (Factor, DerivedLevel, Transition, MinimumTrials,
                      MultiCrossBlock, Merge, RepeatMode, AlignmentMode, synthesize_trials, CMSGen)

side = Factor("side", ["left", "right"])
colour = Factor("colour", ["red", "green"])

# Does the side repeat from the trial before? Does the colour?  [0] is this trial, [-1] the one before.
def repeats(factor):
    return factor[0] == factor[-1]

def changes(factor):
    return factor[0] != factor[-1]

side_repeats = Factor("side_repeats", [
    DerivedLevel("repeats", Transition(repeats, [side])),
    DerivedLevel("changes", Transition(changes, [side])),
])
colour_repeats = Factor("colour_repeats", [
    DerivedLevel("repeats", Transition(repeats, [colour])),
    DerivedLevel("changes", Transition(changes, [colour])),
])

# One set: 4 trials, each of the four squares once.
one_set = MultiCrossBlock(design=[side, colour], crossings=[[side, colour]],
                          constraints=[MinimumTrials(4)],             # the set size
                          mode=RepeatMode.WEIGHT, alignment=AlignmentMode.PARALLEL_START)

# The whole block: 33 trials (8 sets, and a first trial that has no trial before).
# Side repeats or not, crossed with colour repeats or not, equally often anywhere in it.
transitions = MultiCrossBlock(design=[side, colour, side_repeats, colour_repeats],
                              crossings=[[side_repeats, colour_repeats]],
                              constraints=[MinimumTrials(33)],         # the block length
                              mode=RepeatMode.WEIGHT, alignment=AlignmentMode.PARALLEL_START)

# Both at once: the set is repeated until the block is full.
block = Merge([one_set, transitions], alignment=AlignmentMode.PARALLEL_START)
trials = synthesize_trials(block, 1, CMSGen)[0]
```

The generated block: 33 trials, every set intact; trial type, side and response each repeat on half of the trials, the same square on a quarter.

</div>

<div class="sm-variant" data-v="12" markdown="1">

A set is the twelve combinations, each once. Two blocks, merged. Each says what is even within its own length: the first is one set, the second the whole block. `Merge` repeats the set until the block is full. So inside a set the combinations are even and the transitions are free; over the block the transitions are even.

```python
from sweetpea import (Factor, DerivedLevel, Transition, MinimumTrials,
                      MultiCrossBlock, Merge, RepeatMode, AlignmentMode, synthesize_trials, CMSGen)

word = Factor("word", ["red", "green", "cross"])    # the word shown before the square
side = Factor("side", ["left", "right"])
colour = Factor("colour", ["red", "green"])

# Does the side repeat from the trial before? Does the colour?  [0] is this trial, [-1] the one before.
def repeats(factor):
    return factor[0] == factor[-1]

def changes(factor):
    return factor[0] != factor[-1]

side_repeats = Factor("side_repeats", [
    DerivedLevel("repeats", Transition(repeats, [side])),
    DerivedLevel("changes", Transition(changes, [side])),
])
colour_repeats = Factor("colour_repeats", [
    DerivedLevel("repeats", Transition(repeats, [colour])),
    DerivedLevel("changes", Transition(changes, [colour])),
])

# One set: 12 trials, each of the twelve combinations once.
one_set = MultiCrossBlock(design=[word, side, colour], crossings=[[word, side, colour]],
                          constraints=[MinimumTrials(12)],             # the set size
                          mode=RepeatMode.WEIGHT, alignment=AlignmentMode.PARALLEL_START)

# The whole block: 49 trials (4 sets, and a first trial that has no trial before).
# Side repeats or not, crossed with colour repeats or not, equally often anywhere in it.
transitions = MultiCrossBlock(design=[side, colour, side_repeats, colour_repeats],
                              crossings=[[side_repeats, colour_repeats]],
                              constraints=[MinimumTrials(49)],         # the block length
                              mode=RepeatMode.WEIGHT, alignment=AlignmentMode.PARALLEL_START)

# Both at once: the set is repeated until the block is full.
block = Merge([one_set, transitions], alignment=AlignmentMode.PARALLEL_START)
trials = synthesize_trials(block, 1, CMSGen)[0]
```

The generated block: 49 trials, every set intact; trial type, side and response each repeat on half of the trials, the same square on a quarter. For sets of 24 with every combination twice, write `MinimumTrials(24)` in the set. The full block of 9 sets (109 trials) took about four minutes to generate.

</div>

## The point

- Making things even within a short stretch of trials changes what follows
  what, and it does not even out over a block.
- What repeats from the trial before can be a factor of the design like any
  other. The sets can stay: inside a set the combinations are even and the
  transitions are free; over the whole block the transitions are even.
- Every rule costs freedom. The smaller the sets, the less is left.
