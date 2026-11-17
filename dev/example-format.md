# How an example is written

An example is one published or realistic experiment, described from the
science down to the design. Each lives in `skills/sweetpea/examples/<task_name>/`, inside the skill so that
it travels with the skill when someone installs only the skill:

- `index.md`: the text, with the same headings in every example.
- `meta.yaml`: the same content as fixed fields, for checking and searching.
- `design.py`: the SweetPea designs, runnable.

The folder is named after the task, not the paper. Read the paper before
writing; do not write from a summary.

Keep every section short. The examples are read by assistants as context while
they work with a user, and by people on a web page; neither is helped by extra
words. State each fact once, in the section it belongs to.

Status: only the sections below are agreed. Add a section here when it has
been agreed, before writing it for further examples.

## Research question

Three short paragraphs, each starting with its bold label. About 90 words in
all.

**What, and why.** The area of research and the construct or
question behind it, at the level of the science, and why it matters. No design
terms. It follows the authors' own aim. It need not be a cognitive construct:
a methods paper asks a question about a method.

**How.** The paradigm, what a participant does, and the logic of
the inference ("if X was processed, responses should be faster when ..."). Say
what a response is a response to ("classify the target as smaller or larger
than five", not "classify the target"). No counts, no statistics; those belong
to Task and Analysis.

**Part used.** One sentence naming the comparison of the
paper that the rest of the example is about. Papers ask more than one thing;
this line says which piece the design discussion refers to.

In `meta.yaml` the matching fields are `construct` and `paradigm`.

## Takeaway (top of the file, and `takeaway` in `meta.yaml`)

One or two sentences with the rule a reader should carry to another
experiment, not a summary of this one. It is what the index shows.

## Design as published

A table of the decisions: what was chosen, the reason the paper gives (or
"None"), and what follows from it. There is no separate Task section: what the
participant does is in "How". A stimulus set or a pairing is a decision, not
part of the task.

## Options

List all of them, with the cost of each: changes to the design, and ways to
handle the property in the analysis with the published design (leaving trials
out, adding the property as a condition). Name what stays unequal in every
option. Wording is neutral: "leaves X unequal", never "flaw" or "fix"; say
that none of the options is the correct one.

## Design to propose

Every design in `design.py` has a role in `meta.yaml`: `propose`,
`do_not_propose` (the published design of a `kind: unequal_property` example)
or `alternative`. An assistant raises the property, shows the design with role
`propose`, and names the alternatives with their costs. The user decides.

The counts in `meta.yaml` must equal the counts of a generated block.

## Rules learned from the first example (masked number priming, 2026-11-16)

- **Say how the published design assigned trials:** counterbalanced (a
  complete crossing) or randomised. A property left unequal by a complete
  crossing is a consequence of the design, not sampling noise; say so.
- **Check every option for what it newly makes unequal.** Removing or
  repeating trials changes how often each stimulus pair occurs. For each
  option, count how expected the second stimulus is given the first, per
  compared condition.
- **Be exact about what is predicted.** State separately whether the trial
  type, the response and the specific stimulus are predictable. "The prime
  predicts the target" is not enough: the stimulus can be predictable while
  the trial type and the response are at one half.
- **Write `design.py` with the experiment's own factors** (prime, target) and
  express restrictions as constraints (`Exclude` on a derived factor). Do not
  fold several stimuli into one combined factor to get the counts; it hides
  the design. The alternatives may use a helper, the proposed design may not.
- **The option the author of the paradigm finds may be better than the
  obvious one.** List the obvious one too, with what it leaves unequal.

## Rules learned from the second example (Simon task, 2026-11-16)

- **Quote the reason the paper gives for the choice that causes the
  imbalance** ("Reason given" column), from the paper itself. It tells the
  reader, and an assistant, when the situation applies: here, whenever someone
  shuffles small sets to keep frequencies equal.
- **A choice made to avoid one confound can create another.** Say what the
  choice was for before saying what it costs.
- **Give the size of the imbalance as an exact long-run rate** where one
  exists (11/24), and say how it changes with the design parameter (set
  size). A count from one generated block is not that rate.
- **SweetPea's samplers do not draw orders like a shuffle.** A SweetPea
  version of "shuffled sets" is a valid block but does not reproduce the
  rates of shuffling; do not report its counts as the published design's.
- **Prefer a proposed design that keeps what the original choice was for**
  (here the sets) and adds the missing rule.

- **Check the other properties after a fix.** A design that evens out one
  property can push others further away (trial type at 50% moved side and
  response repetition from 38% to 33%). Count everything that can repeat.
- **A general lesson belongs in `SKILL.md`, not only in the example.** If the
  example teaches something a user could ask for in other words (here: "make
  it balanced every n trials"), add a short section with tested code there
  and point to the example.
- **Teaching pages may offer a smaller version of the design** when it shows
  the mechanism more clearly (sets of four or two instead of twelve). It must
  be labelled as not part of the original, and the original must be
  selectable on the same page.
- **Use one word per thing** on a page and in the conversation about it
  (here: set, block, the trial before, what repeats).

- **Some examples have no design to propose** (`kind: trade_off`). Every
  design then has the role `option`; the text lists what each keeps and gives
  up in neutral words and does not rank them. The lesson of such an example is
  that writing the design down makes the choice explicit.

Not yet agreed in detail: Analysis, What to balance.
