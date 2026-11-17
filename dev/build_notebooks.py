"""Builds the tutorial from one source: notebooks, website pages and reference scripts.

    tutorial/notebooks/N_name.ipynb      runs on Colab, with the tables of one run stored in it
    docs/tutorial/N_name.md              the same on the website, with a playable block of the experiment
    tutorial/reference/stepN_name.py     the code cells as one script (what the guided tutorial walks through)

Run:  python dev/build_notebooks.py     (runs every design once; takes a few seconds)
"""
import contextlib
import io
import json
from pathlib import Path

import pandas as pd

REPO = "younesStrittmatter/sweetpea-starter"
root = Path(__file__).resolve().parents[1]
COLAB = f"https://colab.research.google.com/github/{REPO}/blob/main/tutorial/notebooks/"

SETUP = "%pip install -q sweetpea pandas"

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

COPIES = '''def pairs_with_copies(congruent_copies, incongruent_copies):
    """Two helper factors that make every congruent pair occur `congruent_copies` times
    and every incongruent pair `incongruent_copies` times."""
    copy = Factor("copy", [str(n) for n in range(1, max(congruent_copies, incongruent_copies) + 1)])

    def too_many(copy, colour, word):
        return int(copy) > (congruent_copies if colour == word else incongruent_copies)

    def wanted(copy, colour, word):
        return not too_many(copy, colour, word)

    extra_copy = Factor("extra_copy", [
        DerivedLevel("too many", WithinTrial(too_many, [copy, colour, word])),
        DerivedLevel("wanted", WithinTrial(wanted, [copy, colour, word])),
    ])
    return copy, extra_copy'''

STEPS = [
("1_congruency", "Step 1. Congruency", "trials_b", "I want to run a Stroop experiment to test the congruency effect. What is it about, and what do I need to decide?", [
("md", '''**The question.** Does an irrelevant word interfere with naming a colour?

**Prediction.** Naming the ink is slower when the word names another colour (incongruent) than when it names the same one (congruent). The difference is the congruency effect.

**The analysis.** Response time on congruent trials against incongruent trials.

**The decision.** With three colours there are 3 congruent and 6 incongruent pairs of ink and word. Two wishes pull apart: *every pair equally often* (then one third of the trials is congruent) or *half of the trials congruent* (then the word tells something about the ink). This page builds both and counts them.'''),
("md", "### The factors\n\nA regular factor is set freely on every trial. The ink colour and the word are regular factors."),
("code", BASE),
("md", "Congruency is not set freely: it follows from the colour and the word. That is a derived factor."),
("code", CONGRUENCY),
("md", "### Option A: every pair equally often\n\nColour and word are crossed, so each of the 9 pairs occurs equally often. `MinimumTrials(18)` asks for two rounds of the crossing."),
("code", '''block_a = CrossBlock(design=[colour, word, congruency], crossing=[colour, word],
                     constraints=[MinimumTrials(18)])
trials_a = pd.DataFrame(synthesize_trials(block_a, 1, CMSGen)[0])
display(pd.crosstab(trials_a["colour"], trials_a["word"]))
display(trials_a["congruency"].value_counts().to_frame("trials"))'''),
("md", "### Option B: half of the trials congruent\n\nEvery pair once, and the congruent pairs a second time. Two helper factors do that: `copy` numbers the copies, and the copies that are too many are excluded. The helper is written once here and used again in steps 2 and 3."),
("code", COPIES),
("code", '''copy, extra_copy = pairs_with_copies(congruent_copies=2, incongruent_copies=1)
block_b = CrossBlock(design=[colour, word, congruency, copy, extra_copy],
                     crossing=[colour, word, copy],
                     constraints=[Exclude((extra_copy, "too many")), MinimumTrials(24)],
                     require_complete_crossing=False)
trials_b = pd.DataFrame(synthesize_trials(block_b, 1, CMSGen)[0])
display(pd.crosstab(trials_b["colour"], trials_b["word"]))
display(trials_b["congruency"].value_counts().to_frame("trials"))'''),
("md", "### What does each option cost?\n\nHow often is a word shown in its own colour? One third means the word tells nothing about the ink."),
("code", '''cost = pd.DataFrame({
    "congruent trials (%)": [round((t["congruency"] == "congruent").mean() * 100) for t in (trials_a, trials_b)],
    "word is in its own colour (%)": [round((t["word"] == t["colour"]).mean() * 100) for t in (trials_a, trials_b)],
}, index=["A: every pair equally often", "B: half congruent"])
display(cost)'''),
("md", "**Check.** In which option could a participant guess the ink from the word? In which are there fewer congruent trials? Neither is free: which cost is acceptable depends on what you compare.\n\n**Try.** Add a fourth colour to `colours` and run again. What happens to the share of congruent trials in option A?\n\n**Next.** Step 2 keeps option B and asks what happened on the trial before."),
]),
("2_sequence", "Step 2. The trial before", "trials", "Now I want to test whether the congruency effect depends on the trial before: is it smaller right after an incongruent trial? What is the hypothesis behind that, and what does the design need?", [
("md", '''**So far.** Step 1 gave a block with half of the trials congruent and every pair of a kind equally often. This step keeps that block and adds one factor.

**The question.** Does a conflict change how the next trial is handled?

**Prediction (conflict adaptation).** The congruency effect is smaller after an incongruent trial than after a congruent one.

**The alternative to rule out.** Nothing is adjusted; trials that repeat a colour or a word from the trial before are simply faster, and such repeats are spread unevenly.

**The analysis.** The congruency effect after a congruent trial against the congruency effect after an incongruent trial.'''),
("md", "### As in step 1"),
("code", BASE), ("code", CONGRUENCY), ("code", COPIES),
("md", "### New: the trial before as a factor\n\nA transition factor follows from the trial before: `[0]` is this trial, `[-1]` the one before."),
("code", '''def after_congruent(colour, word):
    return colour[-1] == word[-1]


def after_incongruent(colour, word):
    return colour[-1] != word[-1]


trial_before = Factor("trial_before", [
    DerivedLevel("congruent", Transition(after_congruent, [colour, word])),
    DerivedLevel("incongruent", Transition(after_incongruent, [colour, word])),
])'''),
("md", "### The block\n\nThe block of step 1, crossed with the trial before: 12 trials times 2 is 24, plus a first trial, which has no trial before."),
("code", '''copy, extra_copy = pairs_with_copies(congruent_copies=2, incongruent_copies=1)
block = CrossBlock(design=[colour, word, congruency, copy, extra_copy, trial_before],
                   crossing=[colour, word, copy, trial_before],
                   constraints=[Exclude((extra_copy, "too many")), MinimumTrials(25)],
                   require_complete_crossing=False)
trials = pd.DataFrame(synthesize_trials(block, 1, CMSGen)[0])
rest = trials.iloc[1:]                  # without the first trial
display(pd.crosstab(rest["trial_before"], rest["congruency"]))'''),
("md", "The four combinations are equal, and that is by design: run the cell again and they stay equal.\n\n### What else repeats?\n\nNot in the design: does the ink colour, and so the response, repeat from the trial before? Count it in each of the four combinations."),
("code", '''trials["response_repeats"] = trials["colour"].eq(trials["colour"].shift())
rest = trials.iloc[1:]
display(pd.crosstab([rest["trial_before"], rest["congruency"]], rest["response_repeats"]))'''),
("md", "**Check.** Is the response repeat equal across the four combinations? If not, the alternative explanation is still open. Whatever is not in the crossing is left to chance: run the block cell again and see which counts change.\n\n**Try.** Ask what it would take to forbid all repeats (`Exclude` on a transition factor for the colour), and what that does to the four combinations.\n\n**Next.** Step 3 goes from the trial before to the whole block: mostly congruent and mostly incongruent blocks."),
]),
("3_adaptation", "Step 3. Adaptation", "session", "Now I want to test whether people adapt to the context. I want blocks in which most trials are congruent and blocks in which most are incongruent, and compare the congruency effect between them. What is the hypothesis, and what should I watch out for?", [
("md", '''**So far.** Step 1 chose how many copies of each pair a block holds: 2 of each congruent pair, 1 of each incongruent pair. This step turns that choice into the manipulation.

**The question.** Do people adjust to how frequent conflict is?

**Prediction.** The congruency effect is smaller in mostly incongruent blocks than in mostly congruent blocks.

**The alternative to rule out.** In a mostly congruent block the word predicts the ink, so people can simply learn to follow the word.

**The analysis.** The congruency effect in mostly congruent blocks against the congruency effect in mostly incongruent blocks.'''),
("md", "### As in step 1"),
("code", BASE), ("code", CONGRUENCY), ("code", COPIES),
("md", "### New: two kinds of block\n\nThe number of copies sets the proportion. 6 copies of each congruent pair and 1 of each incongruent pair is 18 of 24 trials congruent; 2 and 3 copies is 6 of 24."),
("code", '''COPIES = {"mostly congruent": (6, 1), "mostly incongruent": (2, 3)}     # copies of each (congruent, incongruent) pair


def block(context):
    copy, extra_copy = pairs_with_copies(*COPIES[context])
    return CrossBlock(design=[colour, word, congruency, copy, extra_copy],
                      crossing=[colour, word, copy],
                      constraints=[Exclude((extra_copy, "too many"))],
                      require_complete_crossing=False)'''),
("md", "### A session of four blocks\n\nEach block is generated on its own and gets its context as a column."),
("code", '''blocks = []
for number, context in enumerate(["mostly congruent", "mostly incongruent", "mostly incongruent", "mostly congruent"], start=1):
    trials = pd.DataFrame(synthesize_trials(block(context), 1, CMSGen)[0])
    trials.insert(0, "context", context)
    trials.insert(0, "block", number)
    blocks.append(trials)
session = pd.concat(blocks, ignore_index=True)
display(pd.crosstab(session["context"], session["congruency"]))'''),
("md", "### How well does the word tell the ink?\n\nFor each word, the share of trials on which it is shown in its own colour. That number is the alternative explanation."),
("code", '''session["word_is_ink"] = session["word"] == session["colour"]
display(session.groupby(["context", "word"])["word_is_ink"].mean().round(2).unstack())'''),
("md", "**Check.** Are the proportions what was asked for? How many incongruent trials does a mostly congruent block have: is that enough to measure the effect there? A word is in its own colour on 75% of the trials in one context and 25% in the other: how could learning and control be told apart?\n\n**Try.** Change the copies to `(4, 1)` and `(1, 2)`. What are the proportions and the block lengths now?\n\n**Next.** Step 4 asks whether this adjustment has a price when the task changes."),
]),
("4_transfer", "Step 4. Transfer", "session", "Last question. I want to know whether this control setting has a price: if people shield the task more in a mostly incongruent context, are they then worse at switching to another task? I add a second task: on some trials people read the word instead of naming the ink, and a cue says which. I want mini-blocks that are mostly congruent or mostly incongruent, and to compare the switch cost between them. What is the hypothesis, and what does the design need?", [
("md", '''**So far.** Step 2 made the trial before a factor, and step 3 made blocks that are mostly congruent or mostly incongruent. This step puts both ideas together and adds a second task.

**The question.** Does adapting to frequent conflict make it harder to switch to another task?

**Prediction if shielding and switching are one control setting.** The switch cost is larger in a mostly incongruent context than in a mostly congruent one.

**The alternative to rule out.** A mostly incongruent context is simply harder, so everything is slower there.

**The analysis.** The switch cost (switch against repeat trials) in mostly incongruent mini-blocks against mostly congruent mini-blocks.'''),
("md", "### As before, plus a second task and the context\n\nA cue says on each trial whether to name the ink or read the word. The task is a regular factor. So is the context now: in step 3 it was a column added by hand, here it is part of the design."),
("code", BASE + '''
from sweetpea import Nest, Repeat

task = Factor("task", ["name the colour", "read the word"])              # new: a second task, with a cue
context = Factor("context", ["mostly congruent", "mostly incongruent"])  # new: held for a whole mini-block'''),
("md", "### New: the task transition\n\nA transition factor, as in step 2, but on the task: does it repeat or switch? Without repeat trials in the same context there is no switch cost to measure."),
("code", '''def task_repeats(task):
    return task[0] == task[-1]


def task_switches(task):
    return task[0] != task[-1]


transition = Factor("transition", [
    DerivedLevel("repeat", Transition(task_repeats, [task])),
    DerivedLevel("switch", Transition(task_switches, [task])),
])'''),
("md", "### New: what the context makes frequent\n\nIn a mostly congruent mini-block the congruent trials are the frequent ones, in a mostly incongruent mini-block the incongruent ones. One derived factor says that for both: it follows from the colour, the word and the context. The third argument of a level is its weight: 3 to 1 is three quarters."),
("code", '''def frequent_here(colour, word, context):
    congruent = colour == word
    return congruent == (context == "mostly congruent")


def rare_here(colour, word, context):
    return not frequent_here(colour, word, context)


frequency = Factor("frequency", [
    DerivedLevel("frequent", WithinTrial(frequent_here, [colour, word, context]), 3),
    DerivedLevel("rare", WithinTrial(rare_here, [colour, word, context]), 1),
])'''),
("md", "### Something has to give\n\nThe blocks of step 3 hold 24 trials. Crossed with 2 tasks and 2 transitions that is 96 trials per mini-block: too long for a context that should change often.\n\nSo a mini-block crosses what the analysis compares: the frequency (and with it congruency), the task and the transition. That is 16 trials. The even pairs of colour and word are given up.\n\n### New: a block inside a block\n\nStep 3 generated every block on its own and put them one after the other. `Nest` makes it one design. The outer block crosses the context; `Repeat` asks for it twice, so four mini-blocks. The inner block is the mini-block. `Nest` holds each context for the length of one mini-block and draws the order of the contexts."),
("code", '''contexts = Repeat(CrossBlock(design=[context], crossing=[context], constraints=[]),
                  constraints=[MinimumTrials(4)])            # four mini-blocks: each context twice
mini_block = CrossBlock(design=[colour, word, task, transition, frequency, context],
                        crossing=[frequency, task, transition],
                        constraints=[])
block = Nest(contexts, mini_block, alignment="parallel start")
session = pd.DataFrame(synthesize_trials(block, 1, CMSGen)[0])

# congruency as a column: inside a nested block, SweetPea 0.2.14 fails on a derived factor that is in no crossing
session["congruency"] = ["congruent" if colour == word else "incongruent"
                         for colour, word in zip(session["colour"], session["word"])]
session.insert(0, "block", session.index // 16 + 1)
display(pd.crosstab([session["block"], session["context"]], session["congruency"]))'''),
("md", "Every mini-block holds one context, and each context comes twice.\n\n### Where does the crossing sit?\n\nCount the eight combinations the switch cost is computed from, in every mini-block. The first trial of the session has no transition."),
("code", '''counted = session[session["transition"] != ""]
display(pd.crosstab([counted["block"], counted["context"]], [counted["transition"], counted["task"], counted["congruency"]]))'''),
("md", "Almost 3 to 1 in every mini-block, but not exactly. The reason: a transition needs a trial before, so the crossing starts at the second trial and runs one trial ahead of the context. Count again in stretches of 16 that start at the second trial:"),
("code", '''counted = counted.assign(stretch=(counted.index - 1) // 16 + 1)
display(pd.crosstab(counted["stretch"], [counted["transition"], counted["task"], counted["frequency"]]))'''),
("md", "There it is exact (the last stretch is one trial short). So a mini-block is the exact crossing except for one trial: its first trial, right after the context changed, belongs to the stretch before. Most analyses drop that trial anyway.\n\n### What gave way?\n\nThe ink colour and the pairs are not in the crossing. Count them."),
("code", '''display(pd.crosstab(session["context"], session["colour"]))
display(pd.crosstab([session["context"], session["colour"]], session["word"]))'''),
("md", "**Check.** Is there a repeat baseline in each context? How many incongruent switch trials does a mostly congruent mini-block have? Are the ink colours and the pairs still even, and does that matter for the switch cost? The first trial of a mini-block is a switch or a repeat relative to a trial from the other context: keep it or drop it?\n\n**Try.** Put `colour` into the crossing of the mini-block. How long is a mini-block now?\n\n**The idea.** Each question added a factor, and each factor multiplies the design. At some point not everything fits, and the design becomes a choice about what to leave open. Which choice is acceptable depends on what you compare."),
]),
]


def run(cells):
    """Runs the code cells in order; returns what each displayed, and the namespace."""
    shown, namespace = [], {}

    def display(value):
        shown[-1].append(value)

    namespace["display"] = display
    for kind, text in cells:
        shown.append([])
        if kind == "code":
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                exec(compile(text, "cell", "exec"), namespace)
    return shown, namespace


def table(value):
    if isinstance(value, pd.DataFrame):
        return value.to_html(border=0, classes="nb-table").replace("\n\n", "\n")
    return f"<pre>{value}</pre>"


def source(text):
    lines = text.split("\n")
    return [line + "\n" for line in lines[:-1]] + [lines[-1]]


DEMO_COLUMNS = ["block", "context", "task", "colour", "word", "congruency", "trial_before", "transition"]
for name, title, play, ask, cells in STEPS:
    shown, namespace = run(cells)
    number = name[0]

    # the notebook
    nb_cells = [{"cell_type": "markdown", "metadata": {}, "source": source(
                    f"# {title}\n\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB}{name}.ipynb)\n\n"
                    "The tutorial step without an assistant. Run the cells from top to bottom; the tables below are from one run, yours will differ where the design leaves things open.")},
                {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": source(SETUP)}]
    for (kind, text), out in zip(cells, shown):
        if kind == "md":
            nb_cells.append({"cell_type": "markdown", "metadata": {}, "source": source(text)})
        else:
            outputs = [{"output_type": "display_data", "metadata": {},
                        "data": {"text/html": source(table(v)), "text/plain": source(str(v))}} for v in out]
            nb_cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": outputs, "source": source(text)})
    notebook = {"cells": nb_cells, "nbformat": 4, "nbformat_minor": 5,
                "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                             "language_info": {"name": "python"}, "colab": {"provenance": []}}}
    (root / "tutorial" / "notebooks").mkdir(exist_ok=True)
    (root / "tutorial" / "notebooks" / f"{name}.ipynb").write_text(json.dumps(notebook, indent=1) + "\n")

    # the reference script
    code = "\n\n\n".join(text for kind, text in cells if kind == "code")
    script = (f'"""{title}. The code of the tutorial notebook as one script.\n\n'
              f"Generated by dev/build_notebooks.py from the same source as tutorial/notebooks/{name}.ipynb.\n"
              f'Run:  python tutorial/reference/step{name}.py\n"""\n'
              "try:\n    display\nexcept NameError:      # outside a notebook, show tables by printing them\n    display = print\n\n" + code + "\n")
    (root / "tutorial" / "reference" / f"step{name}.py").write_text(script)

    # the website page
    trials = namespace[play]
    demo = trials[[c for c in DEMO_COLUMNS if c in trials.columns]].head(48).to_dict("records")
    page = [f"# {title}", "",
            f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB}{name}.ipynb){{ target=_blank }} "
            f"· [notebook](https://github.com/{REPO}/blob/main/tutorial/notebooks/{name}.ipynb) "
            f"· [script](https://github.com/{REPO}/blob/main/tutorial/reference/step{name}.py)", "",
            "## The experiment", "",
            "A block from the design built on this page. Press play, or step through it.", "",
            f"<div class=\"stroop-demo\" data-trials='{json.dumps(demo)}'></div>", "",
            "## With your assistant", "", "> " + ask, "",
            "## Step by step", ""]
    for (kind, text), out in zip(cells, shown):
        if kind == "md":
            page += [text.replace("### ", "### "), ""]
        else:
            page += ["```python", text, "```", ""]
            for value in out:
                page += ['<div class="nb-out">', table(value), "</div>", ""]
    (root / "docs" / "tutorial").mkdir(exist_ok=True)
    (root / "docs" / "tutorial" / f"{name}.md").write_text("\n".join(page))
    print(name, "ok:", len(trials), "trials in the demo source")

index = ["# Tutorial: four questions about one task", "",
         "One Stroop experiment, grown in four steps. Each step is a research question. With an assistant, you say what",
         "you want to find out and it builds the design with you. Without one, each page is a notebook: the design in small",
         "pieces, a playable block of the experiment, and the count tables.", "",
         "| Step | The question | New in the design |", "|---|---|---|",
         "| [1. Congruency](1_congruency.md) | Does an irrelevant word interfere? | Regular factors, a derived factor, what is crossed |",
         "| [2. The trial before](2_sequence.md) | Does a conflict change how the next trial is handled? | A transition factor |",
         "| [3. Adaptation](3_adaptation.md) | Do people adjust to how frequent conflict is? | Blocks that differ in proportion |",
         "| [4. Transfer](4_transfer.md) | Does adapting to conflict make switching to another task harder? | A second task, a block nested in a block |", "",
         "## With an assistant", "",
         f"Open the [repository](https://github.com/{REPO}) in a Codespace, start your assistant (`claude`, `codex` or `gemini`),",
         "and say the line under \"With your assistant\" on each page, in your own words. Stuck? Say **\"Run the guided tutorial.\"**", "",
         "## Without one", "",
         "Every page has an \"Open in Colab\" button. The notebooks build on each other: step 2 keeps the block of step 1,",
         "step 3 turns its proportion into the manipulation, step 4 adds a task and nests the mini-blocks in one design.", ""]
(root / "docs" / "tutorial" / "index.md").write_text("\n".join(index))
