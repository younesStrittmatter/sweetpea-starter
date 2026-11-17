---
name: sweetpea
description: Design trial sequences for factorial experiments with the SweetPea Python library (counterbalancing, derived factors such as congruency, transition factors such as task switch/repeat, run-length and exclusion constraints). Use whenever the user wants to create, randomise, counterbalance, check or export a trial sequence for a behavioural or psychology experiment, or mentions SweetPea. Also use when the user asks for mini-blocks, sets, or balance within every few trials: that changes what follows what, and the skill says what to tell them.
---

# Designing experiments with SweetPea

SweetPea turns a description of an experiment (factors, what must be balanced,
what must not happen) into randomised trial sequences that provably satisfy it.

Your training data most likely contains an outdated SweetPea API. Use only the
names shown in this file. In particular, `fully_cross_block`,
`multiple_cross_block`, `derived_level`, `within_trial`, `transition`,
`at_most_k_in_a_row`, `exclude` and `synthesize_trials_non_uniform` no longer
exist.

## How to work

A design is right or wrong only for an analysis. The method is the same for
every experiment, whatever the task:

1. **Start from the question, then ask what will be compared.** When the user
   names a goal ("test the congruency effect", "see whether people adapt"),
   say in two or three sentences what it is about: the construct, the
   hypothesis and what it predicts, and the best-known alternative
   explanation, because that is what the design has to rule out. Say it as
   your understanding and let the user correct it. If they have not chosen a
   task, suggest two or three from `paradigms.md` (next to this file) with what
   each is good for. Then ask which conditions are compared, on which measure, and
   restate the design: the factors and their levels, what is crossed, the
   constraints.
2. **Write the design and generate sequences.** Use the API below, the
   experiment's own factors, and constraints for what must not occur. Generate
   several sequences, not one, and save them as CSV.
   **Keep each generated block short.** Generation time grows steeply with the
   number of trials: a plain 2 x 2 x 2 crossing took 0.6 s at 40 trials, 2.6 s
   at 80, and more than 100 s at 160 (CMSGen). Build a long session from
   several short blocks, each generated on its own, and always run generation
   with a time limit: `python scripts/limit.py 60 your_design.py` stops it
   after 60 seconds. Never wait on a generation without a limit. When it is
   stopped, the design is too large as written: make it smaller and tell the
   user what you changed and what that costs. If a design is only
   "every combination equally often, in random order", with no derived or
   transition factor in the crossing and no constraint, you do not need the
   solver for the check: write the list in plain Python and shuffle it.
3. **Count everything else.** Run

   ```
   python scripts/check_design.py sequence_*.csv --compare <the compared columns>
   ```

   It lists every property that differs between the compared conditions: the
   other columns on this trial, every column on the trial before, what repeats,
   and whether two columns with the same levels are equal. It looks one
   trial back; add `--back 2` or more when the order of trials is itself part
   of the task (sequences, n-back, task order). Do this even when
   the design looks fine; the point is to find what nobody asked about. Put
   into the CSV any property of a trial that could matter (the response, a
   position, an identity), also when it is not a factor of the design.
4. **For each difference, find out why, then tell the user.**
   - It was left out of the crossing: that can be fixed. Fix it before you
     compare options; it is not a cost of the design.
   - It is forced by another choice: that is a trade-off. Lay out the options
     with what each keeps and gives up, say which fits the planned comparison
     and why, and let the user decide. Do not decide silently.
   - Ask whether it plausibly affects the measure. If not, say so and move on.
   - Keep "differs by design" apart from "varies by chance". If a share is
     even in expectation and only wobbles from one sequence to the next, it is
     not a difference of the design. Say that it varies, offer a constraint if
     the user wants it fixed, and do not call it a problem.

Verify by counting, never by reading the code, and report the counts,
including what is not balanced. If zero sequences come back, the design is
impossible as written: find the conflicting requirement and let the user
decide what to give up. Do not silently drop a constraint.

## Where differences come from

Three mechanisms produce most differences that nobody chose. They are not tied
to a task; look for the mechanism, not for the example.

| Mechanism | What happens | Typical sign |
|---|---|---|
| **A combination that cannot occur.** Two things cannot share a level (a place, an item, a key), or a relation is true by definition in one condition only. | The condition that lacks the combination differs from the others in a property nobody named. | `--compare` reports "never in one condition" |
| **Balance within a short stretch of trials.** Sets, mini-blocks, a shuffled list that is repeated, "every condition once every n trials". | Whatever was just shown is scarcer among the trials that are left, so a trial follows its own level less often than half of the time. It does not even out over a block. | `--compare` reports the level "on the trial before" |
| **A share that the stimuli do not give by themselves.** Half matching trials when most combinations do not match; a cue that is valid on most trials. | Reaching the share means showing some combinations more often, so one stimulus predicts another. | Count each combination: some are several times as frequent |

A fourth source is not a mechanism but an omission: a factor that is in the
design and not in the crossing is left to the solver and comes out uneven.

`examples/` shows each mechanism once, in a published experiment. Read an
example for how the reasoning goes and what the options cost, not as a
pattern to match: the next experiment will look different and work the same
way.

## The API

Install with `pip install sweetpea`. Everything is imported from `sweetpea`.

### Factors, crossing, sequences

```python
import pandas as pd
from sweetpea import Factor, CrossBlock, synthesize_trials, CMSGen

color = Factor("color", ["red", "blue", "green"])
word = Factor("word", ["red", "blue", "green"])

design = [color, word]      # every factor that appears in a trial
crossing = [color, word]    # the factors whose combinations are balanced
block = CrossBlock(design, crossing, constraints=[])

# 2 independent sequences; each is a dict: factor name -> list of level names
experiments = synthesize_trials(block, 2, CMSGen)
trials = pd.DataFrame(experiments[0])
assert len(trials) == 9     # 3 x 3 combinations, each exactly once
```

- A sequence has one trial per combination of the crossed factors. Use
  `MinimumTrials(n)` in the constraints for more. The sequence then has
  exactly `n` trials, so make `n` a multiple of the crossing size (6
  combinations: 12, 18, 24, ...). Any other `n` gives an unbalanced sequence
  in which some combinations can be missing.
- A factor in `design` but not in `crossing` is chosen freely by the solver
  and is not balanced.
- Use `CMSGen` (or omit the argument). `RandomGen` and `UniformGen` can run
  for a very long time on designs with constraints.

### Derived factors (computed from other factors in the same trial)

```python
from sweetpea import Factor, DerivedLevel, WithinTrial, CrossBlock, synthesize_trials, CMSGen

color = Factor("color", ["red", "blue", "green"])
word = Factor("word", ["red", "blue", "green"])

def is_congruent(color, word):
    return color == word

def is_incongruent(color, word):
    return color != word

congruency = Factor("congruency", [
    DerivedLevel("congruent", WithinTrial(is_congruent, [color, word])),
    DerivedLevel("incongruent", WithinTrial(is_incongruent, [color, word])),
])

# Crossing color x congruency gives 50% congruent trials.
# Crossing color x word would give 33%, because 3 of 9 combinations match.
block = CrossBlock([color, word, congruency], [color, congruency], [])
experiments = synthesize_trials(block, 1, CMSGen)
assert experiments[0]["congruency"].count("congruent") == 3
```

The levels of a derived factor must cover every case exactly once: for any
combination of inputs, exactly one level's function returns `True`. SweetPea
prints a warning that dependencies "may make the crossing unsatisfiable" when
a crossed factor is derived from another crossed factor; that is only a
warning.

### Transition factors (depend on the previous trial)

```python
from sweetpea import (Factor, DerivedLevel, Transition, AtMostKInARow,
                      CrossBlock, synthesize_trials, CMSGen)

task = Factor("task", ["color", "motion"])

# The function receives one indexable value per factor:
# [0] is the current trial, [-1] is the previous trial.
def is_repeat(task):
    return task[0] == task[-1]

def is_switch(task):
    return task[0] != task[-1]

task_transition = Factor("task_transition", [
    DerivedLevel("repeat", Transition(is_repeat, [task])),
    DerivedLevel("switch", Transition(is_switch, [task])),
])

block = CrossBlock([task, task_transition], [task, task_transition],
                   [AtMostKInARow(2, (task_transition, "repeat"))])
experiments = synthesize_trials(block, 1, CMSGen)

# The first trial has no previous trial: its transition is "" and the
# sequence is one trial longer than the crossing (4 + 1).
assert experiments[0]["task_transition"][0] == ""
assert len(experiments[0]["task"]) == 5
```

With a crossed transition factor, count that extra first trial when using
`MinimumTrials`: for 4 repetitions of this 4-combination crossing ask for
`MinimumTrials(17)`, not 16. With 16, one combination occurs only 3 times.

For longer histories use `Window(function, [factors], width, 1)`; with width 3
the function can read `[0]`, `[-1]` and `[-2]` (for example a 2-back target).

### Constraints

```python
from sweetpea import (Factor, Level, DerivedLevel, WithinTrial, CrossBlock,
                      AtMostKInARow, Exclude, MinimumTrials, synthesize_trials, CMSGen)

color = Factor("color", ["red", "blue", "green"])
word = Factor("word", ["red", "blue", "green"])
congruency = Factor("congruency", [
    DerivedLevel("congruent", WithinTrial(lambda c, w: c == w, [color, word])),
    DerivedLevel("incongruent", WithinTrial(lambda c, w: c != w, [color, word])),
])

# At most 2 trials in a row with the same congruency, at least 24 trials.
block = CrossBlock([color, word, congruency], [color, congruency],
                   [AtMostKInARow(2, congruency), MinimumTrials(24)])
experiments = synthesize_trials(block, 1, CMSGen)
assert len(experiments[0]["color"]) == 24

# Excluding a level removes combinations from the crossing, so the block
# must be told that an incomplete crossing is intended.
block = CrossBlock([color, word, congruency], [color, word],
                   [Exclude((congruency, "congruent"))],
                   require_complete_crossing=False)
experiments = synthesize_trials(block, 1, CMSGen)
assert len(experiments[0]["color"]) == 6

# Unequal frequencies: weights on the levels of a crossed factor.
validity = Factor("validity", [Level("valid", 4), Level("invalid", 1)])
side = Factor("side", ["left", "right"])
block = CrossBlock([validity, side], [validity, side], [])
experiments = synthesize_trials(block, 1, CMSGen)
assert experiments[0]["validity"].count("valid") == 8
```

- `AtMostKInARow(k, factor)` applies to every level; `AtMostKInARow(k, (factor, "level"))` to one.
- Also available: `AtLeastKInARow`, `ExactlyKInARow`, `ExactlyK(k, (factor, "level"))`,
  `Pin(trial_index, (factor, "level"))`.
- Constraints hold within one sequence, not across sequences.
- An impossible design returns an empty list, not an error:

```python
from sweetpea import Factor, AtMostKInARow, CrossBlock, synthesize_trials, CMSGen

color = Factor("color", ["red", "blue"])
size = Factor("size", ["big", "small"])
# Colour and size must both alternate on every trial, so only 2 of the 4
# combinations could ever occur, but the crossing requires all 4.
block = CrossBlock([color, size], [color, size],
                   [AtMostKInARow(1, (color, "red")), AtMostKInARow(1, (color, "blue")),
                    AtMostKInARow(1, size)])
experiments = synthesize_trials(block, 1, CMSGen)
assert experiments == []
```

### Sets (mini-blocks) and the trial before

When trials are shuffled in sets, with every combination once per set, each
combination is exactly equally frequent and evenly spread. It also changes
what follows what: inside a set, whatever was just shown is scarcer among the
trials that are left. A trial then follows its own level less often than the
other levels, and this does not even out over a block. With two levels and
sets of 4 the same level follows in 37.5% of cases, with sets of 12 in 45.8%.

So when a user asks for balance within short stretches of trials (sets,
mini-blocks, "each condition once every n trials"), tell them this, ask
whether their measure depends on the trial before (it usually does in
conflict, switching and priming tasks), and offer to make what repeats part
of the design:

```python
from sweetpea import (Factor, DerivedLevel, Transition, MinimumTrials, ExactlyK,
                      CrossBlock, Repeat, synthesize_trials, CMSGen)

side = Factor("side", ["left", "right"])
colour = Factor("colour", ["red", "green"])

# What repeats from the trial before? One level for each of the four cases.
cases = {"side and colour": (True, True), "side only": (True, False),
         "colour only": (False, True), "neither": (False, False)}
what_repeats = Factor("what_repeats", [
    DerivedLevel(name, Transition(lambda s, c, want=want: (s[0] == s[-1], c[0] == c[-1]) == want, [side, colour]))
    for name, want in cases.items()])

# Repeat keeps the sets: each of the 4 combinations once in every 4 trials.
one_set = CrossBlock([side, colour, what_repeats], [side, colour], [])
block = Repeat(one_set, [MinimumTrials(33)] + [ExactlyK(8, (what_repeats, name)) for name in cases])
trials = synthesize_trials(block, 1, CMSGen)[0]

squares = list(zip(trials["side"], trials["colour"]))
assert all(len(set(squares[i:i + 4])) == 4 for i in range(0, 32, 4))          # the sets are intact
assert sum(a[0] == b[0] for a, b in zip(squares, squares[1:])) == 16           # the side repeats on half
assert sum(a == b for a, b in zip(squares, squares[1:])) == 8                  # the same square on a quarter
```

- Ask for one more trial than the sets need: the first trial has no trial
  before.
- Balance everything that can repeat, not one property. Evening out only one
  (say congruency) pushes the others further from one half.
- Small sets leave little freedom. With sets of 4 as above, every set has to
  start with the combination that ended the last one. Tell the user, and
  suggest larger sets when that matters.
- With several crossings in a `MultiCrossBlock`, `mode=RepeatMode.REPEAT`
  applies to every crossing, not only to the smallest.
- A worked case with the numbers is in `examples/simon_previous_trial/`.

### Continuous values (jittered intervals and similar)

```python
from sweetpea import (Factor, ContinuousFactor, UniformDistribution, MinimumTrials,
                      CrossBlock, synthesize_trials, CMSGen)

color = Factor("color", ["red", "blue"])
iti = ContinuousFactor("iti", distribution=UniformDistribution(0.5, 1.5))
block = CrossBlock([color, iti], [color], [MinimumTrials(8)])
experiments = synthesize_trials(block, 1, CMSGen)
assert all(0.5 <= value <= 1.5 for value in experiments[0]["iti"])
```

A continuous factor can be in the design but not in the crossing.

### Exporting and checking

```python
import pandas as pd
from sweetpea import Factor, CrossBlock, synthesize_trials, CMSGen

color = Factor("color", ["red", "blue"])
size = Factor("size", ["big", "small"])
block = CrossBlock([color, size], [color, size], [])
experiments = synthesize_trials(block, 3, CMSGen)

for index, experiment in enumerate(experiments):
    pd.DataFrame(experiment).to_csv(f"sequence_{index}.csv", index=False)
```

Write CSV files through pandas as above. `save_experiments_csv` leaves out
continuous factors.

Then check the result (the script needs only the Python standard library):

```
python scripts/check_design.py sequence_0.csv --balance color size --runs color
```

It prints how often each level and each combination of the `--balance`
columns occurs, whether those combinations are equally frequent, and the
longest run of each level of the `--runs` columns.

## Tasks and paradigms

When a user has a question and no task yet ("I want to study mental effort"):

- `paradigms.md`: paradigms by research topic, from 782 published studies with
  open data (the psyche database): how many studies used each paradigm and
  which factors they manipulated. Start here.
- `paradigms/<topic>.md`: the studies themselves: the construct, what was
  compared with what on which measure, the factors, the reference. A construct
  without a topic of its own is found by searching the folder.
- `tasks.md`: 65 experiments in more detail, with the factors of each design,
  including those that depend on the trial before.

Offer two or three paradigms, say in a sentence what each compares, and say
which you would take for the user's question and why. Then use the
comparisons listed for that paradigm to ask the user which one is theirs.
The entries were read off abstracts by an assistant and are a sample, not a
survey: a count is not a recommendation, a missing paradigm is not a poor
choice, and a reference should be checked before it is cited. Say so.

## Examples

`examples/` holds published experiments in one fixed format: the research
question, the comparison, the design as published, what it leaves unequal, the
options with their costs, and a design to propose. Read the takeaway of each
when a user describes an experiment, and open the one that fits:

- `examples/masked_number_priming/`: two stimuli from the same set, completely
  crossed; the pairs with the same item twice can only be congruent.
- `examples/simon_previous_trial/`: trials shuffled in small sets; what
  follows what is no longer even.
- `examples/distractor_location_learning/`: two things that cannot be in the
  same place; no design without a cost, only a choice between costs.

In an example, the published design is shown to explain a problem. Propose the
design marked `propose` in its `meta.yaml`, name the alternatives with their
costs, and let the user decide. Where every design is marked `option`, there
is nothing to propose: present them all with their trade-offs.
