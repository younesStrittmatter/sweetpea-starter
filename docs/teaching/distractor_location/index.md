# Two things in one place

Does a distractor still disturb us at a place where we have learned to expect
it?

Based on Gong & Theeuwes (2021), *Attention, Perception, & Psychophysics*,
Experiment 3. [doi:10.3758/s13414-020-02142-8](https://doi.org/10.3758/s13414-020-02142-8)

## The task and the question

Scroll, or use the buttons under each block.

<div class="dl-intro"></div>

## Three designs

<div class="dl-story"></div>

Each design keeps one of the three and gives up two. None is the right one.

## What is simplified

The original has two kinds of distractor and two groups, and its distractor is
at the usual place on 65% of the trials that have one. Here there is one kind,
four times as often at its usual place as at any other single place.

## In SweetPea

One design, with the choice as its argument.

```python
import pandas as pd
from sweetpea import (Factor, Level, DerivedLevel, WithinTrial, Exclude,
                      CrossBlock, synthesize_trials, CMSGen)

places = ["1", "2", "3", "4", "5", "6", "7", "8"]
usual = "1"                                  # the place where the distractor usually is


def design(target_at_usual_place):
    """One block. `target_at_usual_place` is "as often", "never" or "more often":
    how often the target is at the distractor's usual place, compared with any other free place."""
    target = Factor("target", places)

    # The distractor: absent, or at a place; four times as often at its usual place as at any other.
    distractor = Factor("distractor", [Level("none", 1), Level(usual, 4)]
                                      + [Level(p, 1) for p in places if p != usual])

    # Two things cannot be in the same place.
    def same_place(target, distractor):
        return target == distractor

    def different_places(target, distractor):
        return target != distractor

    overlap = Factor("overlap", [
        DerivedLevel("same place", WithinTrial(same_place, [target, distractor])),
        DerivedLevel("different places", WithinTrial(different_places, [target, distractor])),
    ])

    # Where the target is, by name, so that it can be counted and kept apart.
    def at_usual_place(target):
        return target == usual

    def elsewhere(target):
        return target != usual

    target_place = Factor("target_place", [
        DerivedLevel("usual place", WithinTrial(at_usual_place, [target])),
        DerivedLevel("elsewhere", WithinTrial(elsewhere, [target])),
    ])

    factors = [target, distractor, overlap, target_place]
    crossing = [target, distractor]
    constraints = [Exclude((overlap, "same place"))]

    if target_at_usual_place == "never":
        constraints.append(Exclude((target_place, "usual place")))

    if target_at_usual_place == "more often":
        # A second copy of some trials: those with the target at the usual place while the distractor
        # is at another place. Trials without a distractor are the baseline and get no second copy.
        copy = Factor("copy", ["first", "second"])

        def unwanted(copy, target, distractor):
            doubled = target == usual and distractor not in ("none", usual)
            return copy == "second" and not doubled

        def wanted(copy, target, distractor):
            return not unwanted(copy, target, distractor)

        second_copy = Factor("second_copy", [
            DerivedLevel("unwanted", WithinTrial(unwanted, [copy, target, distractor])),
            DerivedLevel("wanted", WithinTrial(wanted, [copy, target, distractor])),
        ])
        factors += [copy, second_copy]
        crossing = [target, distractor, copy]
        constraints.append(Exclude((second_copy, "unwanted")))

    return CrossBlock(design=factors, crossing=crossing, constraints=constraints,
                      require_complete_crossing=False)


for choice in ["as often", "never", "more often"]:
    trials = pd.DataFrame(synthesize_trials(design(choice), 1, CMSGen)[0])
    kind = trials["distractor"].map(lambda d: "none" if d == "none" else "usual place" if d == usual else "another place")
    print(choice, len(trials), "trials")
    print(pd.crosstab(kind, trials["target_place"]))
```

Trials per block, as target elsewhere / target at the usual place:

| distractor | as often (85 trials) | never (77) | more often (92) |
|---|---|---|---|
| none | 7 / 1 | 7 / 0 | 7 / 1 |
| at its usual place | 28 / 0 | 28 / 0 | 28 / 0 |
| at another place | 42 / 7 | 42 / 0 | 42 / 14 |

In the code, "more often" is twice as often, which keeps the block short. The
picture uses 10 to 7, which spreads the target evenly over all places.

## The point

- Often there is no design without a cost, only a choice between costs.
- A design that is not written down still makes that choice, unseen.
- Written as a specification, the choice is explicit and can be counted, and
  the analysis can be made to agree with it.
