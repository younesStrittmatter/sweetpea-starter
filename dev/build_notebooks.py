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
from sweetpea import (Factor, DerivedLevel, WithinTrial, Transition, MinimumTrials,
                      CrossBlock, synthesize_trials, tabulate_experiments, CMSGen)

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
experiments_a = synthesize_trials(block_a, 1, CMSGen)
tabulate_experiments(block_a, experiments_a, [colour, word])
tabulate_experiments(block_a, experiments_a, [congruency])'''),
("md", "`tabulate_experiments` is SweetPea's own count: how often each combination of the factors you name occurs, and its share.\n\n### Option B: half of the trials congruent\n\nCross the ink colour with congruency. Each ink colour is then congruent on half of its trials: 6 combinations, four rounds."),
("code", '''block_b = CrossBlock(design=[colour, word, congruency], crossing=[colour, congruency],
                     constraints=[MinimumTrials(24)])
experiments_b = synthesize_trials(block_b, 1, CMSGen)
tabulate_experiments(block_b, experiments_b, [colour, congruency])
tabulate_experiments(block_b, experiments_b, [colour, word])'''),
("md", "The first table is what was crossed: it is even. The second shows what was not: which word goes with an incongruent ink is left open, so those pairs can come out uneven. Run the cell again and compare.\n\n### What does each option cost?\n\nA congruent trial is a word in its own colour. In option A that is one third of the trials: the word tells nothing about the ink. In option B it is half: the word tells something.\n\n### The sequence as a table\n\nOne row per trial, for your experiment software."),
("code", '''trials_a = pd.DataFrame(experiments_a[0])
trials_b = pd.DataFrame(experiments_b[0])
display(trials_b.head(8))'''),
("md", "**Check.** In which option could a participant guess the ink from the word? In which are there fewer congruent trials? Neither is free: which cost is acceptable depends on what you compare.\n\n**Try.** Add a fourth colour to `colours` and run again. What happens to the share of congruent trials in option A?\n\n**Next.** Step 2 keeps option B and asks what happened on the trial before."),
]),
("2_sequence", "Step 2. The trial before", "trials", "Now I want to test whether the congruency effect depends on the trial before: is it smaller right after an incongruent trial? What is the hypothesis behind that, and what does the design need?", [
("md", '''**So far.** Step 1 gave a block with half of the trials congruent: the ink colour crossed with congruency. This step keeps that block and adds one factor.

**The question.** Does a conflict change how the next trial is handled?

**Prediction (conflict adaptation).** The congruency effect is smaller after an incongruent trial than after a congruent one.

**The alternative to rule out.** Nothing is adjusted; trials that repeat a colour or a word from the trial before are simply faster, and such repeats are spread unevenly.

**The analysis.** The congruency effect after a congruent trial against the congruency effect after an incongruent trial.'''),
("md", "### As in step 1"),
("code", BASE), ("code", CONGRUENCY),
("md", "### New: the trial before as a factor\n\nA transition factor follows from the trial before: `[0]` is this trial, `[-1]` the one before."),
("code", '''def after_congruent(colour, word):
    return colour[-1] == word[-1]


def after_incongruent(colour, word):
    return colour[-1] != word[-1]


trial_before = Factor("trial_before", [
    DerivedLevel("congruent", Transition(after_congruent, [colour, word])),
    DerivedLevel("incongruent", Transition(after_incongruent, [colour, word])),
])'''),
("md", "### The block\n\nThe crossing of step 1 with the trial before added: 12 combinations, two rounds, plus a first trial, which has no trial before."),
("code", '''block = CrossBlock(design=[colour, word, congruency, trial_before],
                   crossing=[colour, congruency, trial_before],
                   constraints=[MinimumTrials(25)])
experiments = synthesize_trials(block, 1, CMSGen)
after_first = list(range(1, 25))        # the trials that have a trial before
tabulate_experiments(block, experiments, [trial_before, congruency], trials=after_first)'''),
("md", "The four combinations are equal, and that is by design: run the cell again and they stay equal.\n\n### What else repeats?\n\nDoes the ink colour, and so the response, repeat from the trial before? That is a transition factor too. Put it in the design but not in the crossing: SweetPea then records it and leaves it free. Count it in each of the four combinations."),
("code", '''def response_repeats(colour):
    return colour[0] == colour[-1]


def response_changes(colour):
    return colour[0] != colour[-1]


response = Factor("response", [
    DerivedLevel("repeats", Transition(response_repeats, [colour])),
    DerivedLevel("changes", Transition(response_changes, [colour])),
])

block = CrossBlock(design=[colour, word, congruency, trial_before, response],
                   crossing=[colour, congruency, trial_before],
                   constraints=[MinimumTrials(25)])
experiments = synthesize_trials(block, 1, CMSGen)
tabulate_experiments(block, experiments, [trial_before, congruency, response], trials=after_first)
trials = pd.DataFrame(experiments[0])'''),
("md", "**Check.** Is the response repeat equal across the four combinations? If not, the alternative explanation is still open. Whatever is not in the crossing is left to chance: run the block cell again and see which counts change.\n\n**Try.** Ask what it would take to forbid all repeats (`Exclude` on a transition factor for the colour), and what that does to the four combinations.\n\n**Next.** Step 3 goes from the trial before to the whole block: mostly congruent and mostly incongruent blocks."),
]),
("3_adaptation", "Step 3. Adaptation", "session", "Now I want to test whether people adapt to the context. I want blocks in which most trials are congruent and blocks in which most are incongruent, and compare the congruency effect between them. What is the hypothesis, and what should I watch out for?", [
("md", '''**So far.** Step 1 crossed the ink colour with congruency: half of the trials congruent. This step changes that share, and the share becomes the manipulation.

**The question.** Do people adjust to how frequent conflict is?

**Prediction.** The congruency effect is smaller in mostly incongruent blocks than in mostly congruent blocks.

**The alternative to rule out.** In a mostly congruent block the word predicts the ink, so people can simply learn to follow the word.

**The analysis.** The congruency effect in mostly congruent blocks against the congruency effect in mostly incongruent blocks.'''),
("md", "### As in step 1"),
("code", BASE),
("code", '''def same(colour, word):
    return colour == word


def different(colour, word):
    return colour != word
'''.rstrip()),
("md", "### New: a weight\n\nA level can have a weight: the third argument of `DerivedLevel`. 3 to 1 makes the first level three times as frequent as the second. Crossed with the ink colour that is 12 combinations, two rounds: 18 of 24 trials."),
("code", '''mostly_congruent = Factor("congruency", [
    DerivedLevel("congruent", WithinTrial(same, [colour, word]), 3),
    DerivedLevel("incongruent", WithinTrial(different, [colour, word]), 1),
])
mostly_incongruent = Factor("congruency", [
    DerivedLevel("congruent", WithinTrial(same, [colour, word]), 1),
    DerivedLevel("incongruent", WithinTrial(different, [colour, word]), 3),
])

block_mc = CrossBlock(design=[colour, word, mostly_congruent], crossing=[colour, mostly_congruent],
                      constraints=[MinimumTrials(24)])
block_mi = CrossBlock(design=[colour, word, mostly_incongruent], crossing=[colour, mostly_incongruent],
                      constraints=[MinimumTrials(24)])'''),
("md", "### Two blocks of each kind\n\nEach kind of block is generated on its own. The second argument of `synthesize_trials` is the number of sequences."),
("code", '''experiments_mc = synthesize_trials(block_mc, 2, CMSGen)
experiments_mi = synthesize_trials(block_mi, 2, CMSGen)
tabulate_experiments(block_mc, experiments_mc, [mostly_congruent])
tabulate_experiments(block_mi, experiments_mi, [mostly_incongruent])'''),
("md", "### How well does the word tell the ink?\n\nFor each word, how often it is shown in its own colour (congruent). That number is the alternative explanation. First a mostly congruent block, then a mostly incongruent one."),
("code", '''tabulate_experiments(block_mc, experiments_mc[:1], [word, mostly_congruent])
tabulate_experiments(block_mi, experiments_mi[:1], [word, mostly_incongruent])'''),
("md", "### A session\n\nFour blocks one after the other, each with its context as a column."),
("code", '''order = [("mostly congruent", experiments_mc[0]), ("mostly incongruent", experiments_mi[0]),
         ("mostly incongruent", experiments_mi[1]), ("mostly congruent", experiments_mc[1])]
session = pd.concat([pd.DataFrame(trials).assign(block=number, context=context)
                     for number, (context, trials) in enumerate(order, start=1)], ignore_index=True)
display(session.head(4))'''),
("md", "**Check.** Are the proportions what was asked for? How many incongruent trials does a mostly congruent block have: is that enough to measure the effect there? A word is in its own colour far more often in one context than in the other: how could learning and control be told apart?\n\n**Try.** Change the weights to `(2, 1)` and `(1, 2)`. What are the proportions and the block lengths now?\n\n**Next.** Step 4 asks whether this adjustment has a price when the task changes. There the weight meets a limit: it cannot depend on another factor."),
]),
("4_transfer", "Step 4. Transfer", "session", "Last question: does the adaptation transfer to another task? I want mini-blocks that are mostly congruent or mostly incongruent, and each mini-block is either colour naming or word reading. I want the switch cost between mini-blocks: word reading after colour naming against word reading after word reading, compared between the two contexts. I take word reading because it has almost no congruency effect. What is the hypothesis, and can nested blocks keep everything counterbalanced, also at the border between two mini-blocks: which context and which task came before?", [
("md", '''**So far.** Step 2 made the trial before a factor. Step 3 made blocks that are mostly congruent or mostly incongruent with a weight, generated one by one. This step uses both ideas one level up: the mini-block is the unit, and the whole session is one design.

**The question.** Does adapting to frequent conflict make it harder to change the task?

**Prediction if it is one control setting.** Where conflict is frequent the current task is shielded more, so a change of task costs more: the switch cost is larger in the mostly incongruent context.

**Why word reading.** The switch cost is taken on word-reading mini-blocks. Word reading has almost no congruency effect, so the proportion itself hardly touches the trials the cost is measured on.

**The analysis.** Switch cost = response time in word-reading mini-blocks that follow colour naming (switch) minus response time in word-reading mini-blocks that follow word reading (repeat). Compare it between the two contexts.'''),
("md", "### As before, plus the task and the context\n\nBoth are regular factors. Neither changes from trial to trial: each is held for a whole mini-block."),
("code", BASE + '''
from sweetpea import Nest, IterateGen

context = Factor("context", ["mostly congruent", "mostly incongruent"])  # new: held for a whole mini-block
task = Factor("task", ["name the colour", "read the word"])              # new: held for a whole mini-block'''),
("code", CONGRUENCY),
("md", "### New: what happens at the border between two mini-blocks?\n\nTwo transition factors, as in step 2. Here they will look back one mini-block, not one trial: does the task change, and which context came before?"),
("code", '''def task_repeats(task):
    return task[0] == task[-1]


def task_switches(task):
    return task[0] != task[-1]


task_transition = Factor("task_transition", [
    DerivedLevel("repeat", Transition(task_repeats, [task])),
    DerivedLevel("switch", Transition(task_switches, [task])),
])


def after_mostly_congruent(context):
    return context[-1] == "mostly congruent"


def after_mostly_incongruent(context):
    return context[-1] == "mostly incongruent"


context_before = Factor("context_before", [
    DerivedLevel("mostly congruent", Transition(after_mostly_congruent, [context])),
    DerivedLevel("mostly incongruent", Transition(after_mostly_incongruent, [context])),
])'''),
("md", "### New: what the context makes frequent\n\nIn step 3 a weight on congruency set the proportion of a block. But a level has one weight, and here the proportion depends on the context, which changes from mini-block to mini-block. SweetPea has no weight that depends on another factor. So the weight sits on a helper factor that says whether a trial is the kind its context makes frequent: congruent in a mostly congruent mini-block, incongruent in a mostly incongruent one. A derived factor can follow from another derived factor: this one follows from congruency and the context."),
("code", '''def frequent_here(congruency, context):
    return (congruency == "congruent") == (context == "mostly congruent")


def rare_here(congruency, context):
    return not frequent_here(congruency, context)


frequency = Factor("frequency", [
    DerivedLevel("frequent", WithinTrial(frequent_here, [congruency, context]), 3),
    DerivedLevel("rare", WithinTrial(rare_here, [congruency, context]), 1),
])'''),
("md", "### New: a block inside a block\n\nTwo blocks, each with its own crossing:\n\n- **within a mini-block**: the frequency crossed with the ink colour, 12 trials;\n- **between mini-blocks**: the context, the context before, the task and the task transition. That is every kind of border, 16 mini-blocks, plus a first one that has no mini-block before it.\n\n`Nest` puts the first inside the second: every combination of the outer block is held for one whole mini-block."),
("code", '''mini_block = CrossBlock(design=[colour, word, congruency, frequency, context],
                        crossing=[frequency, colour],
                        constraints=[])
between_mini_blocks = CrossBlock(design=[context, context_before, task, task_transition],
                                 crossing=[context, context_before, task, task_transition],
                                 constraints=[])
block = Nest(outer_block=between_mini_blocks, inner_block=mini_block, alignment="post preamble")
experiments = synthesize_trials(block, 1, IterateGen)       # 204 trials: too long for CMSGen
after_start = list(range(12, 204))                           # without the first mini-block
tabulate_experiments(block, experiments, [context_before, context, task, task_transition], trials=after_start)'''),
("md", "Every kind of border has 12 trials: one mini-block each. The first mini-block has nothing before it; it is the start and is left out of the counts.\n\n### Within a mini-block\n\nThe proportion in each context, and the ink colours. Then one mini-block on its own: the second one."),
("code", '''tabulate_experiments(block, experiments, [context, congruency], trials=after_start)
tabulate_experiments(block, experiments, [context, colour], trials=after_start)
tabulate_experiments(block, experiments, [context, task, congruency, colour], trials=list(range(12, 24)))'''),
("md", "### The sequence as a table\n\nOne row per trial, with the mini-blocks numbered."),
("code", '''session = pd.DataFrame(experiments[0])
session.insert(0, "block", session.index // 12 + 1)
counted = session[session["block"] > 1]
display(session.iloc[10:14])'''),
("md", "### What is not in the design?\n\nThe two trials at the border themselves: the last trial of one mini-block and the first trial of the next. They are left to chance."),
("md", "**Check.** Both crossings are exact, and every kind of border occurs once. What is thin? Each kind of border is one mini-block of 12 trials; more need several sequences. The two trials at the border are left to chance: is that acceptable, or should the first trial of a mini-block be pinned?\n\n**The sampler.** `CMSGen` did not finish this design in five minutes. `IterateGen` takes a few seconds, but it does not draw at random among all possible sequences: it returns the solutions in the order the solver finds them. Look at the order of the trials before you use it.\n\n**Try.** Take `context_before` out of the outer block. How many mini-blocks are left, and does `CMSGen` work again?\n\n**The idea.** Each question added a factor, and each factor multiplies the design. Nesting keeps both levels counterbalanced at once. What it leaves open is still a choice, and which choice is acceptable depends on what you compare."),
]),
]


NOISE = ("Sampling ", "Encoding ", "Running ", "WARNING", " '", "Generating ", "Counting ")


def run(cells):
    """Runs the code cells in order; returns what each displayed, and the namespace."""
    shown, namespace = [], {}

    def display(value):
        shown[-1].append(value)

    namespace["display"] = display
    for kind, text in cells:
        shown.append([])
        if kind == "code":
            printed = io.StringIO()
            with contextlib.redirect_stdout(printed), contextlib.redirect_stderr(io.StringIO()):
                exec(compile(text, "cell", "exec"), namespace)
            text_out = "\n".join(line.rstrip() for line in printed.getvalue().split("\n") if not line.startswith(NOISE)).strip()
            if text_out:
                shown[-1].insert(0, text_out)
    return shown, namespace


def table(value):
    if isinstance(value, pd.DataFrame):
        return value.to_html(border=0, classes="nb-table").replace("\n\n", "\n")
    return f"<pre>{value}</pre>"


def source(text):
    lines = text.split("\n")
    return [line + "\n" for line in lines[:-1]] + [lines[-1]]


DEMO_COLUMNS = ["block", "context", "task", "colour", "word", "congruency", "trial_before", "task_transition", "context_before"]
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
         "| [3. Adaptation](3_adaptation.md) | Do people adjust to how frequent conflict is? | A weight; blocks that differ in proportion |",
         "| [4. Transfer](4_transfer.md) | Does adapting to conflict carry over to the next task? | A second task, mini-blocks nested in one design |", "",
         "## With an assistant", "",
         f"Open the [repository](https://github.com/{REPO}) in a Codespace, start your assistant (`claude`, `codex` or `gemini`),",
         "and say the line under \"With your assistant\" on each page, in your own words. Stuck? Say **\"Run the guided tutorial.\"**", "",
         "## Without one", "",
         "Every page has an \"Open in Colab\" button. The notebooks build on each other: step 2 keeps the block of step 1,",
         "step 3 turns its proportion into the manipulation with a weight, step 4 adds a task and nests the mini-blocks in one design.", ""]
(root / "docs" / "tutorial" / "index.md").write_text("\n".join(index))
