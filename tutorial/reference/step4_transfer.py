"""Step 4. Transfer: does the adjustment after a conflict carry over to another task?

Two tasks on the same stimuli: name the ink colour, or read the word. The
comparison is the sequential effect of step 2 (the congruency effect after a
congruent against after an incongruent trial) when the task repeats, against the
same effect when the task switches. So congruency, the congruency of the trial
before and the task transition are crossed, with the task.

Run:  python tutorial/reference/step4_transfer.py
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


def after_congruent(congruency):
    return congruency[-1] == "congruent"


def after_incongruent(congruency):
    return congruency[-1] == "incongruent"


trial_before = Factor("trial_before", [
    DerivedLevel("congruent", Transition(after_congruent, [congruency])),
    DerivedLevel("incongruent", Transition(after_incongruent, [congruency])),
])


def task_repeats(task):
    return task[0] == task[-1]


def task_switches(task):
    return task[0] != task[-1]


transition = Factor("transition", [
    DerivedLevel("repeat", Transition(task_repeats, [task])),
    DerivedLevel("switch", Transition(task_switches, [task])),
])

block = CrossBlock(
    design=[colour, word, task, congruency, trial_before, transition],
    crossing=[task, transition, congruency, trial_before],    # 2 x 2 x 2 x 2 = 16 combinations
    constraints=[MinimumTrials(33)],                          # twice, plus a first trial
)


def generate():
    return pd.DataFrame(synthesize_trials(block, 1, CMSGen)[0])


if __name__ == "__main__":
    trials = generate()
    rest = trials.iloc[1:]
    print(len(trials), "trials")
    print(pd.crosstab([rest["transition"], rest["trial_before"]], [rest["task"], rest["congruency"]]))
    print(pd.crosstab(rest["congruency"], rest["colour"]))      # not crossed: is the ink colour even?
