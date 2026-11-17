"""Step 3. Adaptation: is the congruency effect smaller in blocks where most trials are incongruent?

Two kinds of block: mostly congruent (3 in 4) and mostly incongruent (1 in 4).
The comparison is the congruency effect in one kind of block against the other.
The share of congruent trials is the manipulation: a weight on a level.

Run:  python tutorial/reference/step3_adaptation.py
"""
import pandas as pd
from sweetpea import (Factor, DerivedLevel, WithinTrial, MinimumTrials,
                      CrossBlock, synthesize_trials, CMSGen)

colours = ["red", "green", "blue"]
WEIGHTS = {"mostly congruent": (3, 1), "mostly incongruent": (1, 3)}     # (congruent, incongruent)


def block(context):
    colour = Factor("colour", colours)
    word = Factor("word", colours)

    def same(colour, word):
        return colour == word

    def different(colour, word):
        return colour != word

    congruent_weight, incongruent_weight = WEIGHTS[context]
    congruency = Factor("congruency", [
        DerivedLevel("congruent", WithinTrial(same, [colour, word]), congruent_weight),      # the third argument is the weight
        DerivedLevel("incongruent", WithinTrial(different, [colour, word]), incongruent_weight),
    ])
    return CrossBlock(
        design=[colour, word, congruency],
        crossing=[colour, congruency],              # 3 x 4 = 12 combinations with the weights
        constraints=[MinimumTrials(24)],
    )


def generate(order=("mostly congruent", "mostly incongruent", "mostly incongruent", "mostly congruent")):
    blocks = []
    for number, context in enumerate(order, start=1):
        trials = pd.DataFrame(synthesize_trials(block(context), 1, CMSGen)[0])
        trials.insert(0, "context", context)
        trials.insert(0, "block", number)
        blocks.append(trials)
    return pd.concat(blocks, ignore_index=True)


if __name__ == "__main__":
    session = generate()
    print(len(session), "trials in", session["block"].nunique(), "blocks")
    print(pd.crosstab(session["context"], session["congruency"]))
    # how well does the word tell the ink? the share of trials on which they are the same, per word
    session["word_is_ink"] = session["word"] == session["colour"]
    print(session.groupby(["context", "word"])["word_is_ink"].mean().round(2).unstack())
