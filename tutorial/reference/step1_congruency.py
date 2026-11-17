"""Step 1. Stroop: is naming the ink colour slower when the word names another colour?

The comparison is congruent against incongruent trials, so congruency is crossed
and half of the trials are congruent. With three colours, crossing colour x word
would give one third.

Run:  python tutorial/reference/step1_congruency.py
"""
import pandas as pd
from sweetpea import (Factor, DerivedLevel, WithinTrial, MinimumTrials,
                      CrossBlock, synthesize_trials, CMSGen)

colours = ["red", "green", "blue"]
colour = Factor("colour", colours)      # the ink
word = Factor("word", colours)          # what the word says


def same(colour, word):
    return colour == word


def different(colour, word):
    return colour != word


congruency = Factor("congruency", [
    DerivedLevel("congruent", WithinTrial(same, [colour, word])),
    DerivedLevel("incongruent", WithinTrial(different, [colour, word])),
])

block = CrossBlock(
    design=[colour, word, congruency],
    crossing=[colour, congruency],          # every ink colour equally often congruent and incongruent
    constraints=[MinimumTrials(24)],
)


def generate():
    return pd.DataFrame(synthesize_trials(block, 1, CMSGen)[0])


if __name__ == "__main__":
    trials = generate()
    print(len(trials), "trials")
    print(pd.crosstab(trials["colour"], trials["congruency"]))
    print(pd.crosstab(trials["word"], trials["congruency"]))    # the word is not crossed: is it even?
