# To do

## Ask the SweetPea developers: a crossing within the levels of another factor

**What we want to say:** "cross colour and word within incongruent trials" (every ink-word pair equally
often among the incongruent trials), next to "half of the trials congruent". More generally: a crossing,
or a weight, that holds within each level of another factor.

**Why:** it cannot be declared in SweetPea 0.2.14 (checked 2026-11-17 against the PyPI release, the guide,
the example programs and the API list). A crossing gives every combination the same frequency over all
trials of the block.

What was tried:

| Attempt | Result |
|---|---|
| colour x congruency, plus colour x word x congruency as a second crossing | no sequence: nine equal pairs means one third congruent |
| two factors "ink / word of an incongruent trial" with a level "not applicable", crossed, next to colour x congruency | no sequence: "not applicable" must be as frequent as each pair |
| colour x congruency and word x congruency | works and is declared; the pairs are tied but not fixed (2 each in about half of the sequences, else 1 and 3, once 0 and 4) |
| colour x word x congruency with a weight on congruency | exact, but the weight counts pairs and has to be recalculated when colours or share change |
| colour x congruency, plus `ExactlyK` on each incongruent pair (a derived factor names the pairs) | exact and readable; this is what the skill uses now. The count still has to be written |

**The same gap elsewhere:** tutorial step 4 needs the helper factor `frequency` because a weight cannot
depend on another factor (the proportion flips with the context of the mini-block).

**Also for the developers** (found the same day):

- `Nest` fails with "... is not in list" on a derived factor that is in the design but in no crossing,
  no constraint, and that no other derived factor follows from (`Sustain.apply` loops over `block.design`).
- `tabulate_experiments` only prints; a version that returns a table would replace the pandas crosstabs.
- A 204-trial `Nest` does not finish with `CMSGen`; `IterateGen` does, but every sequence has the same
  order of mini-blocks.
