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

A set is one congruent and one incongruent square. What repeats from the trial before is one more factor, with its four cases equally often.

```python
from sweetpea import (Factor, DerivedLevel, WithinTrial, Transition, MinimumTrials, ExactlyK,
                      CrossBlock, Repeat, synthesize_trials, CMSGen)

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

# What repeats from the trial before?  [0] is this trial, [-1] the one before.
def side_and_colour(side, colour):
    return side[0] == side[-1] and colour[0] == colour[-1]

def side_only(side, colour):
    return side[0] == side[-1] and colour[0] != colour[-1]

def colour_only(side, colour):
    return side[0] != side[-1] and colour[0] == colour[-1]

def neither(side, colour):
    return side[0] != side[-1] and colour[0] != colour[-1]

what_repeats = Factor("what_repeats", [
    DerivedLevel("side and colour", Transition(side_and_colour, [side, colour])),
    DerivedLevel("side only", Transition(side_only, [side, colour])),
    DerivedLevel("colour only", Transition(colour_only, [side, colour])),
    DerivedLevel("neither", Transition(neither, [side, colour])),
])

# One set: one congruent and one incongruent square.
one_set = CrossBlock(design=[side, colour, congruency, what_repeats], crossing=[congruency], constraints=[])

# 16 sets and a first trial that has no trial before; each of the four cases 8 times.
block = Repeat(one_set, [
    MinimumTrials(33),
    ExactlyK(8, (what_repeats, "side and colour")),
    ExactlyK(8, (what_repeats, "side only")),
    ExactlyK(8, (what_repeats, "colour only")),
    ExactlyK(8, (what_repeats, "neither")),
])
trials = synthesize_trials(block, 1, CMSGen)[0]
```

The generated block: 33 trials, every set intact; trial type, side and response each repeat on half of the trials, the same square on a quarter.

</div>

<div class="sm-variant" data-v="4" markdown="1">

A set is each of the four squares once. What repeats from the trial before is one more factor, with its four cases equally often.

```python
from sweetpea import (Factor, DerivedLevel, Transition, MinimumTrials, ExactlyK,
                      CrossBlock, Repeat, synthesize_trials, CMSGen)

side = Factor("side", ["left", "right"])
colour = Factor("colour", ["red", "green"])

# What repeats from the trial before?  [0] is this trial, [-1] the one before.
def side_and_colour(side, colour):
    return side[0] == side[-1] and colour[0] == colour[-1]

def side_only(side, colour):
    return side[0] == side[-1] and colour[0] != colour[-1]

def colour_only(side, colour):
    return side[0] != side[-1] and colour[0] == colour[-1]

def neither(side, colour):
    return side[0] != side[-1] and colour[0] != colour[-1]

what_repeats = Factor("what_repeats", [
    DerivedLevel("side and colour", Transition(side_and_colour, [side, colour])),
    DerivedLevel("side only", Transition(side_only, [side, colour])),
    DerivedLevel("colour only", Transition(colour_only, [side, colour])),
    DerivedLevel("neither", Transition(neither, [side, colour])),
])

# One set: each of the four squares once.
one_set = CrossBlock(design=[side, colour, what_repeats], crossing=[side, colour], constraints=[])

# 8 sets and a first trial that has no trial before; each of the four cases 8 times.
block = Repeat(one_set, [
    MinimumTrials(33),
    ExactlyK(8, (what_repeats, "side and colour")),
    ExactlyK(8, (what_repeats, "side only")),
    ExactlyK(8, (what_repeats, "colour only")),
    ExactlyK(8, (what_repeats, "neither")),
])
trials = synthesize_trials(block, 1, CMSGen)[0]
```

The generated block: 33 trials, every set intact; trial type, side and response each repeat on half of the trials, the same square on a quarter.

</div>

<div class="sm-variant" data-v="12" markdown="1">

Two crossings in one block: the twelve combinations, repeated set by set, and whether the side repeats crossed with whether the colour repeats.

```python
from sweetpea import (Factor, DerivedLevel, Transition, MinimumTrials,
                      MultiCrossBlock, RepeatMode, AlignmentMode, synthesize_trials, CMSGen)

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

block = MultiCrossBlock(
    design=[word, side, colour, side_repeats, colour_repeats],
    crossings=[
        [word, side, colour],               # the twelve combinations ...
        [side_repeats, colour_repeats],     # ... and the four cases of what repeats
    ],
    constraints=[MinimumTrials(109)],       # 9 sets, plus a first trial that has no trial before
    mode=RepeatMode.REPEAT,                 # every combination once in every set of twelve
    alignment=AlignmentMode.PARALLEL_START,
)
trials = synthesize_trials(block, 1, CMSGen)[0]
```

The generated block: 109 trials, every set intact; trial type, side and response each repeat on half of the trials, the same square on a quarter. The repeat mode applies to both crossings, so this version also balances within every four trials, which is stricter than needed.

</div>

## The point

- Making things even within a short stretch of trials changes what follows
  what, and it does not even out over a block.
- What repeats from the trial before can be a factor of the design like any
  other. The sets can stay.
- Every rule costs freedom. The smaller the sets, the less is left.
