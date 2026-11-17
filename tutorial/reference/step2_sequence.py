"""Step 2. The trial before: is the congruency effect smaller right after an incongruent trial?

The comparison is the congruency effect after a congruent trial against the
congruency effect after an incongruent trial. So congruency and the congruency
of the trial before are crossed, with the ink colour.

Run:  python tutorial/reference/step2_sequence.py
"""
import pandas as pd
from sweetpea import (Factor, DerivedLevel, WithinTrial, Transition, MinimumTrials,
                      CrossBlock, synthesize_trials, CMSGen)

colours = ["red", "green", "blue"]
colour = Factor("colour", colours)      # the ink
word = Factor("word", colours)


def same(colour, word):
    return colour == word


def different(colour, word):
    return colour != word


congruency = Factor("congruency", [
    DerivedLevel("congruent", WithinTrial(same, [colour, word])),
    DerivedLevel("incongruent", WithinTrial(different, [colour, word])),
])


# The trial before: [0] is this trial, [-1] the one before.
def after_congruent(congruency):
    return congruency[-1] == "congruent"


def after_incongruent(congruency):
    return congruency[-1] == "incongruent"


trial_before = Factor("trial_before", [
    DerivedLevel("congruent", Transition(after_congruent, [congruency])),
    DerivedLevel("incongruent", Transition(after_incongruent, [congruency])),
])

block = CrossBlock(
    design=[colour, word, congruency, trial_before],
    crossing=[colour, congruency, trial_before],    # 3 x 2 x 2 = 12 combinations
    constraints=[MinimumTrials(25)],                # twice, plus a first trial that has no trial before
)


def generate():
    trials = pd.DataFrame(synthesize_trials(block, 1, CMSGen)[0])
    # not part of the design: does the ink colour, and so the response, repeat? counted, to see what is left open
    trials["response_repeats"] = trials["colour"].eq(trials["colour"].shift())
    return trials


if __name__ == "__main__":
    trials = generate()
    rest = trials.iloc[1:]
    print(len(trials), "trials")
    print(pd.crosstab(rest["trial_before"], rest["congruency"]))
    print(pd.crosstab([rest["trial_before"], rest["congruency"]], rest["response_repeats"]))
