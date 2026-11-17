# Masked number priming

Is the meaning of a number processed when the number cannot be seen?

Based on Zerweck et al. (2021), *Attention, Perception, & Psychophysics*,
Experiment 3. [doi:10.3758/s13414-021-02312-2](https://doi.org/10.3758/s13414-021-02312-2)

## The task and the question

Scroll, or use the buttons under each block.

<div class="mp-intro" data-trials="4>1, 9>4, 6>6, 1>9, 9>6"></div>

## From the published design to a better one

<div class="mp-story" data-numbers="1,4,6,9" data-mapping="1>6,4>9,6>1,9>4"></div>

Nobody decided that half of the congruent trials repeat the number. It follows
from two choices: the same four numbers for primes and targets, and every pair
equally often.

## What it costs

- A participant never sees half of the incongruent pairs. A second mapping for
  the other half of the participants covers them.
- Congruent pairs stay 3 apart and incongruent pairs 5. These four numbers
  allow nothing else.

## In SweetPea

Prime and target are the factors. Two constraints say what must not occur.

```python
from sweetpea import (Factor, DerivedLevel, WithinTrial, Exclude, MinimumTrials,
                      CrossBlock, synthesize_trials, CMSGen)

numbers = ["1", "4", "6", "9"]
prime = Factor("prime", numbers)
target = Factor("target", numbers)

# Congruency: are prime and target on the same side of five?
def same_side(prime, target):
    return (int(prime) < 5) == (int(target) < 5)

def opposite_sides(prime, target):
    return not same_side(prime, target)

congruency = Factor("congruency", [
    DerivedLevel("congruent", WithinTrial(same_side, [prime, target])),
    DerivedLevel("incongruent", WithinTrial(opposite_sides, [prime, target])),
])

# Repetition: is the prime the same number as the target?
def same_number(prime, target):
    return prime == target

def different_number(prime, target):
    return prime != target

repetition = Factor("repetition", [
    DerivedLevel("repeated", WithinTrial(same_number, [prime, target])),
    DerivedLevel("different", WithinTrial(different_number, [prime, target])),
])

# Every prime has one fixed incongruent target; the other incongruent pair is left out.
partner = {"1": "6", "4": "9", "6": "1", "9": "4"}

def left_out(prime, target):
    return opposite_sides(prime, target) and partner[prime] != target

def kept(prime, target):
    return not left_out(prime, target)

pairing = Factor("pairing", [
    DerivedLevel("left out", WithinTrial(left_out, [prime, target])),
    DerivedLevel("kept", WithinTrial(kept, [prime, target])),
])

block = CrossBlock(
    design=[prime, target, congruency, repetition, pairing],
    crossing=[prime, congruency],          # every prime equally often congruent and incongruent
    constraints=[
        Exclude((repetition, "repeated")),  # no trial shows the same number twice
        Exclude((pairing, "left out")),     # one incongruent target per prime
        MinimumTrials(64),
    ],
)
trials = synthesize_trials(block, 1, CMSGen)[0]
```

The generated block: 64 trials, 32 congruent, each of the eight pairs 8 times.
The original also showed each number as a digit or a word; that is left out.

## The point

- A few explicit choices specified the design. What mattered was a consequence
  nobody stated.
- Written as a specification and counted, such consequences show before any
  data are collected.
