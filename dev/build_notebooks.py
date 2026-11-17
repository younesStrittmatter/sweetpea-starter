"""Builds tutorial/notebooks/*.ipynb: the four tutorial steps as notebooks that run on Colab without an assistant.

Run:  python dev/build_notebooks.py
A cell that starts with '# ' on a line of its own after '%%md' is text; everything else is code.
"""
import json
from pathlib import Path

REPO = "younesStrittmatter/sweetpea-starter"
out = Path(__file__).resolve().parents[1] / "tutorial" / "notebooks"
out.mkdir(exist_ok=True)

SETUP = '''%pip install -q sweetpea pandas'''

BASE = '''import pandas as pd
from sweetpea import (Factor, DerivedLevel, WithinTrial, Transition, Exclude, MinimumTrials,
                      CrossBlock, synthesize_trials, CMSGen)

colours = ["red", "green", "blue"]

# regular factors: set freely on every trial
colour = Factor("colour", colours)      # the ink
word = Factor("word", colours)          # what the word says'''

CONGRUENCY = '''# a derived factor: it follows from colour and word on the same trial
def same(colour, word):
    return colour == word


def different(colour, word):
    return colour != word


congruency = Factor("congruency", [
    DerivedLevel("congruent", WithinTrial(same, [colour, word])),
    DerivedLevel("incongruent", WithinTrial(different, [colour, word])),
])'''

NOTEBOOKS = {
"1_congruency": ["Step 1. Congruency", [
("md", '''**The question.** Does an irrelevant word interfere with naming a colour?

**Prediction.** Naming the ink is slower when the word names another colour (incongruent) than when it names the same one (congruent).

**The analysis.** Response time on congruent trials against incongruent trials.

**The decision.** With three colours there are 3 congruent and 6 incongruent pairs of ink and word. Two wishes pull apart: *every pair equally often* (then one third of the trials is congruent) or *half of the trials congruent* (then the word tells something about the ink). Below are both.'''),
("code", BASE), ("code", CONGRUENCY),
("md", "### Option A: every pair equally often\n\nColour and word are crossed: each of the 9 pairs occurs equally often. `MinimumTrials(18)` asks for two rounds."),
("code", '''block_a = CrossBlock(design=[colour, word, congruency], crossing=[colour, word],
                     constraints=[MinimumTrials(18)])
trials_a = pd.DataFrame(synthesize_trials(block_a, 1, CMSGen)[0])
print(pd.crosstab(trials_a["colour"], trials_a["word"]))
print(trials_a["congruency"].value_counts())'''),
("md", "### Option B: half of the trials congruent\n\nEvery pair once, and a second copy of the congruent pairs only. `copy` is a helper factor; the unwanted second copies are excluded."),
("code", '''copy = Factor("copy", ["first", "second"])


def unwanted(copy, colour, word):       # a second copy of an incongruent pair
    return copy == "second" and colour != word


def wanted(copy, colour, word):
    return not unwanted(copy, colour, word)


second_copy = Factor("second_copy", [
    DerivedLevel("unwanted", WithinTrial(unwanted, [copy, colour, word])),
    DerivedLevel("wanted", WithinTrial(wanted, [copy, colour, word])),
])
block_b = CrossBlock(design=[colour, word, congruency, copy, second_copy],
                     crossing=[colour, word, copy],
                     constraints=[Exclude((second_copy, "unwanted")), MinimumTrials(24)],
                     require_complete_crossing=False)
trials_b = pd.DataFrame(synthesize_trials(block_b, 1, CMSGen)[0])
print(pd.crosstab(trials_b["colour"], trials_b["word"]))
print(trials_b["congruency"].value_counts())'''),
("md", "### What does each option cost?\n\nHow often is a word shown in its own colour? One third means the word tells nothing about the ink."),
("code", '''for name, trials in [("every pair equally often", trials_a), ("half congruent", trials_b)]:
    print(name, "-> a word is in its own colour on", round((trials["word"] == trials["colour"]).mean() * 100), "% of trials")'''),
("md", "**Check.** In which option could a participant guess the ink from the word? In which are there fewer congruent trials? Neither is free: which cost is acceptable depends on what you compare.\n\n**Try.** Add a fourth colour to `colours` and run again. What happens to the share of congruent trials in option A?"),
]],
"2_sequence": ["Step 2. The trial before", [
("md", '''**The question.** Does a conflict change how the next trial is handled?

**Prediction (conflict adaptation).** The congruency effect is smaller after an incongruent trial than after a congruent one.

**The alternative to rule out.** Nothing is adjusted; trials that repeat a colour or a word from the trial before are simply faster, and such repeats are spread unevenly.

**The analysis.** The congruency effect after a congruent trial against the congruency effect after an incongruent trial.'''),
("code", BASE), ("code", CONGRUENCY),
("md", "### The trial before as a factor\n\nA transition factor follows from the trial before: `[0]` is this trial, `[-1]` the one before."),
("code", '''def after_congruent(congruency):
    return congruency[-1] == "congruent"


def after_incongruent(congruency):
    return congruency[-1] == "incongruent"


trial_before = Factor("trial_before", [
    DerivedLevel("congruent", Transition(after_congruent, [congruency])),
    DerivedLevel("incongruent", Transition(after_incongruent, [congruency])),
])'''),
("md", "### The block\n\nColour, congruency and the trial before are crossed: 3 x 2 x 2 = 12 combinations. Twice is 24 trials, plus a first trial that has no trial before."),
("code", '''block = CrossBlock(design=[colour, word, congruency, trial_before],
                   crossing=[colour, congruency, trial_before],
                   constraints=[MinimumTrials(25)])
trials = pd.DataFrame(synthesize_trials(block, 1, CMSGen)[0])
rest = trials.iloc[1:]                  # without the first trial
print(len(trials), "trials")
print(pd.crosstab(rest["trial_before"], rest["congruency"]))'''),
("md", "### What else repeats?\n\nNot in the design: does the ink colour, and so the response, repeat? Count it in each of the four combinations."),
("code", '''trials["response_repeats"] = trials["colour"].eq(trials["colour"].shift())
rest = trials.iloc[1:]
print(pd.crosstab([rest["trial_before"], rest["congruency"]], rest["response_repeats"]))'''),
("md", "**Check.** Are the four combinations equal? Is the response repeat equal across them? If not, the alternative explanation is still open: whatever is not in the crossing is left to chance.\n\n**Try.** Run the block cell again a few times. Which counts stay the same, which change?"),
]],
"3_adaptation": ["Step 3. Adaptation", [
("md", '''**The question.** Do people adjust to how frequent conflict is?

**Prediction.** The congruency effect is smaller in mostly incongruent blocks than in mostly congruent blocks.

**The alternative to rule out.** In a mostly congruent block the word predicts the ink, so people can simply learn to follow the word.

**The analysis.** The congruency effect in mostly congruent blocks against the congruency effect in mostly incongruent blocks.'''),
("code", BASE),
("md", "### The proportion is a weight\n\nThe third argument of a level is its weight: 3 to 1 gives three quarters."),
("code", '''WEIGHTS = {"mostly congruent": (3, 1), "mostly incongruent": (1, 3)}     # (congruent, incongruent)


def same(colour, word):
    return colour == word


def different(colour, word):
    return colour != word


def block(context):
    congruent_weight, incongruent_weight = WEIGHTS[context]
    congruency = Factor("congruency", [
        DerivedLevel("congruent", WithinTrial(same, [colour, word]), congruent_weight),
        DerivedLevel("incongruent", WithinTrial(different, [colour, word]), incongruent_weight),
    ])
    return CrossBlock(design=[colour, word, congruency], crossing=[colour, congruency],
                      constraints=[MinimumTrials(24)])'''),
("md", "### A session of four blocks\n\nEach block is generated on its own."),
("code", '''blocks = []
for number, context in enumerate(["mostly congruent", "mostly incongruent", "mostly incongruent", "mostly congruent"], start=1):
    trials = pd.DataFrame(synthesize_trials(block(context), 1, CMSGen)[0])
    trials.insert(0, "context", context)
    trials.insert(0, "block", number)
    blocks.append(trials)
session = pd.concat(blocks, ignore_index=True)
print(pd.crosstab(session["context"], session["congruency"]))'''),
("md", "### How well does the word tell the ink?\n\nFor each word, the share of trials on which it is shown in its own colour. That number is the alternative explanation."),
("code", '''session["word_is_ink"] = session["word"] == session["colour"]
print(session.groupby(["context", "word"])["word_is_ink"].mean().round(2).unstack())'''),
("md", "**Check.** Are the proportions what was asked for? How many incongruent trials does a mostly congruent block have: is that enough? The word was left out of the crossing: does every word predict its ink equally well?\n\n**Try.** Change the weights to `(4, 1)` and `(1, 4)`. What happens to the rare trials?"),
]],
"4_transfer": ["Step 4. Transfer", [
("md", '''**The question.** Does adapting to frequent conflict make it harder to switch to another task?

**Prediction if shielding and switching are one control setting.** The switch cost is larger in a mostly incongruent context than in a mostly congruent one.

**The alternative to rule out.** A mostly incongruent context is simply harder, so everything is slower there.

**The analysis.** The switch cost (switch against repeat trials) in mostly incongruent mini-blocks against mostly congruent mini-blocks.'''),
("code", BASE + '''
task = Factor("task", ["name the colour", "read the word"])        # new: a second task, with a cue'''),
("md", "### The task transition\n\nA transition factor: does the task repeat or switch from the trial before? Without repeat trials in the same context there is no switch cost to measure."),
("code", '''def task_repeats(task):
    return task[0] == task[-1]


def task_switches(task):
    return task[0] != task[-1]


transition = Factor("transition", [
    DerivedLevel("repeat", Transition(task_repeats, [task])),
    DerivedLevel("switch", Transition(task_switches, [task])),
])'''),
("md", "### One mini-block\n\nCongruency (weighted as in step 3), the task and the transition are crossed: 16 combinations, plus a first trial. The ink colour is left out of the crossing: with it a mini-block would be three times as long."),
("code", '''WEIGHTS = {"mostly congruent": (3, 1), "mostly incongruent": (1, 3)}


def same(colour, word):
    return colour == word


def different(colour, word):
    return colour != word


def mini_block(context):
    congruent_weight, incongruent_weight = WEIGHTS[context]
    congruency = Factor("congruency", [
        DerivedLevel("congruent", WithinTrial(same, [colour, word]), congruent_weight),
        DerivedLevel("incongruent", WithinTrial(different, [colour, word]), incongruent_weight),
    ])
    return CrossBlock(design=[colour, word, task, congruency, transition],
                      crossing=[congruency, task, transition],
                      constraints=[MinimumTrials(17)])'''),
("md", "### A session of four mini-blocks"),
("code", '''blocks = []
for number, context in enumerate(["mostly congruent", "mostly incongruent", "mostly incongruent", "mostly congruent"], start=1):
    trials = pd.DataFrame(synthesize_trials(mini_block(context), 1, CMSGen)[0])
    trials.insert(0, "context", context)
    trials.insert(0, "block", number)
    blocks.append(trials)
session = pd.concat(blocks, ignore_index=True)
counted = session[session["transition"] != ""]       # the first trial of a mini-block has no transition
print(len(session), "trials")
print(pd.crosstab(counted["context"], [counted["transition"], counted["congruency"]]))'''),
("md", "### What gave way?"),
("code", '''print(pd.crosstab(counted["context"], counted["colour"]))       # not crossed: is the ink colour even?'''),
("md", "**Check.** Is there a repeat baseline in each context? How many incongruent switch trials does a mostly congruent mini-block have? Is the ink colour even?\n\nEach question added a factor, and each factor multiplies the design. At some point not everything fits, and the design becomes a choice about what to leave open."),
]],
}


def cell(kind, text):
    lines = text.split("\n")
    source = [line + "\n" for line in lines[:-1]] + [lines[-1]]
    if kind == "md":
        return {"cell_type": "markdown", "metadata": {}, "source": source}
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": source}


for name, (title, cells) in NOTEBOOKS.items():
    badge = (f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]"
             f"(https://colab.research.google.com/github/{REPO}/blob/main/tutorial/notebooks/{name}.ipynb)")
    head = [("md", f"# {title}\n\n{badge}\n\nA backup for the tutorial: the same step without an assistant. Run the cells from top to bottom."),
            ("code", SETUP)]
    notebook = {"cells": [cell(k, t) for k, t in head + cells],
                "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                             "language_info": {"name": "python"}, "colab": {"provenance": []}},
                "nbformat": 4, "nbformat_minor": 5}
    (out / f"{name}.ipynb").write_text(json.dumps(notebook, indent=1) + "\n")
print(sorted(p.name for p in out.glob("*.ipynb")))
