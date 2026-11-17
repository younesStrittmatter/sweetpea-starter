"""Step 3. Stability and flexibility, in mini-blocks. Two ways to ask the question:

  vary="congruency"   Blocks with mostly congruent or mostly incongruent trials.
                      When conflict is frequent, is the switch cost larger?
  vary="switches"     Blocks with rare or frequent task switches.
                      When switches are frequent, is the congruency effect larger?

In both, the comparisons are the switch cost and the congruency effect in each kind
of block. So inside every block congruency, task and the transition are crossed, and
the factor that is varied is weighted, 3 to 1 or 1 to 3. The ink colour is left to
the solver: crossing it as well would make a block three times as long. That is a
choice, and the counts show what it costs.

Run:  python tutorial/reference/step5_stability_flexibility.py
"""
import pandas as pd
from sweetpea import (Factor, DerivedLevel, WithinTrial, Transition, MinimumTrials,
                      CrossBlock, synthesize_trials, CMSGen)

colours = ["red", "green", "blue"]

# For each way of asking: the two kinds of block, as weights
# ((congruent, incongruent), (repeat, switch)).
CONTEXTS = {
    "congruency": {"mostly congruent": ((3, 1), (1, 1)), "mostly incongruent": ((1, 3), (1, 1))},
    "switches": {"switches rare": ((1, 1), (3, 1)), "switches frequent": ((1, 1), (1, 3))},
}


def mini_block(congruency_weights, transition_weights):
    """The design of one mini-block of 17 trials."""
    colour = Factor("colour", colours)
    word = Factor("word", colours)
    task = Factor("task", ["name the colour", "read the word"])

    def same(colour, word):
        return colour == word

    def different(colour, word):
        return colour != word

    # the third argument of a level is its weight
    congruency = Factor("congruency", [
        DerivedLevel("congruent", WithinTrial(same, [colour, word]), congruency_weights[0]),
        DerivedLevel("incongruent", WithinTrial(different, [colour, word]), congruency_weights[1]),
    ])

    def task_repeats(task):
        return task[0] == task[-1]

    def task_switches(task):
        return task[0] != task[-1]

    transition = Factor("transition", [
        DerivedLevel("repeat", Transition(task_repeats, [task]), transition_weights[0]),
        DerivedLevel("switch", Transition(task_switches, [task]), transition_weights[1]),
    ])

    return CrossBlock(
        design=[colour, word, task, congruency, transition],
        crossing=[congruency, task, transition],        # 16 combinations with the weights
        constraints=[MinimumTrials(17)],                # plus a first trial that has no trial before
    )


def generate(vary="congruency", order=(0, 1, 1, 0)):
    """A session of mini-blocks. `order` says which of the two kinds of block comes when."""
    kinds = list(CONTEXTS[vary].items())
    blocks = []
    for number, which in enumerate(order, start=1):
        context, (congruency_weights, transition_weights) = kinds[which]
        trials = pd.DataFrame(synthesize_trials(mini_block(congruency_weights, transition_weights), 1, CMSGen)[0])
        trials.insert(0, "context", context)
        trials.insert(0, "block", number)
        blocks.append(trials)
    return pd.concat(blocks, ignore_index=True)


if __name__ == "__main__":
    for vary in CONTEXTS:
        session = generate(vary)
        counted = session[session["transition"] != ""]        # the first trial of a block has no transition
        print(f"\nvary = {vary}: {len(session)} trials in {session['block'].nunique()} mini-blocks")
        print(pd.crosstab(counted["context"], [counted["transition"], counted["congruency"]]))
        print(pd.crosstab(counted["context"], counted["colour"]))   # not crossed: is the ink colour even?
