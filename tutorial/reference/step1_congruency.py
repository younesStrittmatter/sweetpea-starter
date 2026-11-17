"""Step 1. Stroop: is naming the ink colour slower when the word names another colour?

The comparison is congruent against incongruent trials. With three colours there
are 3 congruent and 6 incongruent pairs of ink and word, so two wishes pull apart:

  half of the trials congruent        each congruent pair twice as often as each incongruent pair
  every pair equally often            one third of the trials congruent

design("half congruent") keeps the first, design("every pair equally often") the second.
In both, every incongruent pair occurs equally often: that part costs nothing.

Run:  python tutorial/reference/step1_congruency.py
"""
import pandas as pd
from sweetpea import (Factor, DerivedLevel, WithinTrial, Exclude, MinimumTrials,
                      CrossBlock, synthesize_trials, CMSGen)

colours = ["red", "green", "blue"]


def design(choice="half congruent"):
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

    if choice == "every pair equally often":
        return CrossBlock(design=[colour, word, congruency], crossing=[colour, word],
                          constraints=[MinimumTrials(18)])

    # Half congruent: a second copy of the congruent trials, and of no others.
    copy = Factor("copy", ["first", "second"])

    def unwanted(copy, colour, word):
        return copy == "second" and colour != word

    def wanted(copy, colour, word):
        return not unwanted(copy, colour, word)

    second_copy = Factor("second_copy", [
        DerivedLevel("unwanted", WithinTrial(unwanted, [copy, colour, word])),
        DerivedLevel("wanted", WithinTrial(wanted, [copy, colour, word])),
    ])
    return CrossBlock(
        design=[colour, word, congruency, copy, second_copy],
        crossing=[colour, word, copy],
        constraints=[Exclude((second_copy, "unwanted")), MinimumTrials(24)],
        require_complete_crossing=False,
    )


def generate(choice="half congruent"):
    return pd.DataFrame(synthesize_trials(design(choice), 1, CMSGen)[0])


if __name__ == "__main__":
    for choice in ("half congruent", "every pair equally often"):
        trials = generate(choice)
        print(f"\n{choice}: {len(trials)} trials")
        print(pd.crosstab(trials["colour"], trials["word"]))            # every pair of ink and word
        print(trials["congruency"].value_counts().to_dict())
