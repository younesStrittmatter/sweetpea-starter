"""Step 2. Task switching: is a response slower after a switch of task, and does that depend on congruency?

Two tasks on the same stimulus: name the ink colour, or read the word. The
comparisons are switch against repeat, and that difference for congruent and
incongruent trials. So task, congruency and the task transition are crossed.

Run:  python tutorial/reference/step2_task_switching.py
"""
import pandas as pd
from sweetpea import (Factor, DerivedLevel, WithinTrial, Transition, MinimumTrials,
                      CrossBlock, synthesize_trials, CMSGen)

colours = ["red", "green", "blue"]
colour = Factor("colour", colours)
word = Factor("word", colours)
task = Factor("task", ["name the colour", "read the word"])


def same(colour, word):
    return colour == word


def different(colour, word):
    return colour != word


congruency = Factor("congruency", [
    DerivedLevel("congruent", WithinTrial(same, [colour, word])),
    DerivedLevel("incongruent", WithinTrial(different, [colour, word])),
])


# The task transition: [0] is this trial, [-1] the one before.
def task_repeats(task):
    return task[0] == task[-1]


def task_switches(task):
    return task[0] != task[-1]


transition = Factor("transition", [
    DerivedLevel("repeat", Transition(task_repeats, [task])),
    DerivedLevel("switch", Transition(task_switches, [task])),
])

block = CrossBlock(
    design=[colour, word, task, congruency, transition],
    crossing=[colour, congruency, task, transition],     # 3 x 2 x 2 x 2 = 24 combinations
    constraints=[MinimumTrials(49)],                     # twice, plus a first trial that has no trial before
)


def response(row):
    return row["colour"] if row["task"] == "name the colour" else row["word"]


def generate():
    trials = pd.DataFrame(synthesize_trials(block, 1, CMSGen)[0])
    trials["response"] = trials.apply(response, axis=1)
    # not part of the design: does the response repeat? counted, to see what the design leaves open
    trials["response_repeats"] = trials["response"].eq(trials["response"].shift())
    return trials


if __name__ == "__main__":
    trials = generate()
    rest = trials.iloc[1:]
    print(len(trials), "trials")
    print(pd.crosstab([rest["task"], rest["transition"]], rest["congruency"]))
    print(pd.crosstab(rest["transition"], rest["response_repeats"]))
