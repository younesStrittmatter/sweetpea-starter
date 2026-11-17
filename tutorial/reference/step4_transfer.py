"""Step 4. Transfer: does adapting to frequent conflict make switching to another task harder?

Two kinds of mini-block, as in step 3: mostly congruent and mostly incongruent.
New: a second task (read the word) and a cue. The comparison is the switch cost
in mostly incongruent mini-blocks against the switch cost in mostly congruent
ones. So inside every mini-block congruency, the task and the task transition
are crossed, and congruency is weighted 3 to 1 or 1 to 3.

The ink colour is left to the solver: crossing it as well would make a
mini-block three times as long. That is a choice, and the counts show its cost.

Run:  python tutorial/reference/step4_transfer.py
"""
import pandas as pd
from sweetpea import (Factor, DerivedLevel, WithinTrial, Transition, MinimumTrials,
                      CrossBlock, synthesize_trials, CMSGen)

colours = ["red", "green", "blue"]
WEIGHTS = {"mostly congruent": (3, 1), "mostly incongruent": (1, 3)}     # (congruent, incongruent)


def mini_block(context):
    """The design of one mini-block of 17 trials."""
    # regular factors: set freely on every trial
    colour = Factor("colour", colours)      # the ink
    word = Factor("word", colours)
    task = Factor("task", ["name the colour", "read the word"])

    # derived factor: follows from colour and word on the same trial
    def same(colour, word):
        return colour == word

    def different(colour, word):
        return colour != word

    congruent_weight, incongruent_weight = WEIGHTS[context]
    congruency = Factor("congruency", [
        DerivedLevel("congruent", WithinTrial(same, [colour, word]), congruent_weight),      # the third argument is the weight
        DerivedLevel("incongruent", WithinTrial(different, [colour, word]), incongruent_weight),
    ])

    # transition factor: follows from the task on this trial [0] and the trial before [-1]
    def task_repeats(task):
        return task[0] == task[-1]

    def task_switches(task):
        return task[0] != task[-1]

    transition = Factor("transition", [
        DerivedLevel("repeat", Transition(task_repeats, [task])),
        DerivedLevel("switch", Transition(task_switches, [task])),
    ])

    return CrossBlock(
        design=[colour, word, task, congruency, transition],
        crossing=[congruency, task, transition],        # 4 x 2 x 2 = 16 combinations with the weights
        constraints=[MinimumTrials(17)],                # plus a first trial that has no trial before
    )


def generate(order=("mostly congruent", "mostly incongruent", "mostly incongruent", "mostly congruent")):
    """A session of mini-blocks, each generated on its own."""
    blocks = []
    for number, context in enumerate(order, start=1):
        trials = pd.DataFrame(synthesize_trials(mini_block(context), 1, CMSGen)[0])
        trials.insert(0, "context", context)
        trials.insert(0, "block", number)
        blocks.append(trials)
    return pd.concat(blocks, ignore_index=True)


if __name__ == "__main__":
    session = generate()
    counted = session[session["transition"] != ""]        # the first trial of a mini-block has no transition
    print(len(session), "trials in", session["block"].nunique(), "mini-blocks")
    print(pd.crosstab(counted["context"], [counted["transition"], counted["congruency"]]))
    print(pd.crosstab(counted["context"], counted["colour"]))      # not crossed: is the ink colour even?
