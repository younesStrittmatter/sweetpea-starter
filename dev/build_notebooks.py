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
("4_transfer", "Step 4. Transfer", "session", "Last question: does the adaptation transfer to another task? I want mini-blocks that are mostly congruent or mostly incongruent, and each mini-block is either colour naming or word reading. I want the switch cost between mini-blocks: word reading after colour naming against word reading after word reading, compared between the two contexts. I take word reading because it has almost no congruency effect. What is the hypothesis, and can nested blocks keep all of that counterbalanced?", [
("md", '''**So far.** Step 2 made the trial before a factor. Step 3 made blocks that are mostly congruent or mostly incongruent, generated one by one. This step uses both ideas one level up: the mini-block is the unit, and the whole session is one design.

**The question.** Does adapting to frequent conflict make it harder to change the task?

**Prediction if it is one control setting.** Where conflict is frequent the current task is shielded more, so a change of task costs more: the switch cost is larger in the mostly incongruent context.

**Why word reading.** The switch cost is taken on word-reading mini-blocks. Word reading has almost no congruency effect, so the proportion itself hardly touches the trials the cost is measured on.

**The analysis.** Switch cost = response time in word-reading mini-blocks that follow colour naming (switch) minus response time in word-reading mini-blocks that follow word reading (repeat). Compare it between the two contexts.'''),
("md", "### As before, plus the task and the context\n\nBoth are regular factors. Neither changes from trial to trial: each is held for a whole mini-block."),
("code", BASE + '''
from sweetpea import Nest

context = Factor("context", ["mostly congruent", "mostly incongruent"])  # new: held for a whole mini-block
task = Factor("task", ["name the colour", "read the word"])              # new: held for a whole mini-block'''),
("md", "### New: does the task change from one mini-block to the next?\n\nA transition factor, as in step 2. Here it will look back one mini-block, not one trial."),
("code", '''def task_repeats(task):
    return task[0] == task[-1]


def task_switches(task):
    return task[0] != task[-1]


task_transition = Factor("task_transition", [
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
("md", "### New: a block inside a block\n\nTwo blocks, each with its own crossing:\n\n- **within a mini-block**: the frequency crossed with the ink colour, 12 trials;\n- **between mini-blocks**: the context, the task and the task transition, 8 mini-blocks, plus a first one that has no mini-block before it.\n\n`Nest` puts the first inside the second: every combination of the outer block is held for one whole mini-block."),
("code", '''mini_block = CrossBlock(design=[colour, word, frequency, context],
                        crossing=[frequency, colour],
                        constraints=[])
between_mini_blocks = CrossBlock(design=[context, task, task_transition],
                                 crossing=[context, task, task_transition],
                                 constraints=[])
block = Nest(outer_block=between_mini_blocks, inner_block=mini_block, alignment="post preamble")
session = pd.DataFrame(synthesize_trials(block, 1, CMSGen)[0])

# columns for counting
session["congruency"] = ["congruent" if colour == word else "incongruent"
                         for colour, word in zip(session["colour"], session["word"])]
session.insert(0, "block", session.index // 12 + 1)
overview = session.groupby("block")[["context", "task", "task_transition"]].first()
overview["congruent trials"] = session.groupby("block")["congruency"].apply(lambda c: (c == "congruent").sum())
display(overview)'''),
("md", "One row per mini-block. The first has no task transition; it is the start. After it, every combination of context, task and transition comes once, and every mini-block has the proportion of its context: 9 or 3 of 12.\n\n### Between mini-blocks: is everything crossed?"),
("code", '''counted = session[session["task_transition"] != ""]          # without the first mini-block
mini_blocks = counted.groupby("block")[["context", "task", "task_transition"]].first()
display(pd.crosstab([mini_blocks["context"], mini_blocks["task"]], mini_blocks["task_transition"]))'''),
("md", "### Within a mini-block: is the ink colour even?"),
("code", '''display(pd.crosstab([counted["block"], counted["context"]], [counted["congruency"], counted["colour"]]))'''),
("md", "### What is not in the design?\n\nThe adaptation that is supposed to carry over was built up in the mini-block before. Its context is not in the crossing. Count it for the mini-blocks the switch cost is taken from."),
("code", '''mini_blocks["context_before"] = session.groupby("block")["context"].first().shift()
reading = mini_blocks[mini_blocks["task"] == "read the word"]
display(reading[["context", "task_transition", "context_before"]])'''),
("md", "**Check.** Both crossings are exact. What is thin? Each cell of the comparison is one mini-block of 12 trials; more need a longer session or several sequences. Is the context of the mini-block before the same for switch and repeat? It is left to chance: run the block cell again and look. Should it be a factor too, and how many mini-blocks would that take?\n\n**Try.** Add `MinimumTrials(17)` to the outer block: it counts mini-blocks, so that is two rounds plus the start.\n\n**The idea.** Each question added a factor, and each factor multiplies the design. Nesting keeps both levels counterbalanced at once. What it leaves open is still a choice, and which choice is acceptable depends on what you compare."),
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


DEMO_COLUMNS = ["block", "context", "task", "colour", "word", "congruency", "trial_before", "task_transition"]
DEMO_LENGTH = 48
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
         "| [4. Transfer](4_transfer.md) | Does adapting to conflict carry over to the next task? | A second task, mini-blocks nested in one design |", "",
         "## With an assistant", "",
         f"Open the [repository](https://github.com/{REPO}) in a Codespace, start your assistant (`claude`, `codex` or `gemini`),",
         "and say the line under \"With your assistant\" on each page, in your own words. Stuck? Say **\"Run the guided tutorial.\"**", "",
         "## Without one", "",
         "Every page has an \"Open in Colab\" button. The notebooks build on each other: step 2 keeps the block of step 1,",
         "step 3 turns its proportion into the manipulation, step 4 adds a task and nests the mini-blocks in one design.", ""]
(root / "docs" / "tutorial" / "index.md").write_text("\n".join(index))
