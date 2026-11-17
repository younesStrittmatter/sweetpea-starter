"""Simon task with a prime word: shuffled sets of twelve, and a design that also balances the trial before.

Run:  python design.py            prints the counts of the fast designs (about 15 seconds)
      python design.py --slow     also runs the two slow ones (several minutes)

`proposed()` is the design to propose. `as_published()` is shown to explain
what it leaves unequal; do not propose it without raising that.
"""
import random
import sys
from collections import Counter

import pandas as pd
from sweetpea import (Factor, DerivedLevel, WithinTrial, Transition, MinimumTrials, ExactlyK, CrossBlock,
                      MultiCrossBlock, Repeat, RepeatMode, AlignmentMode, synthesize_trials, CMSGen)

WORDS = ["red", "green", "cross"]
SIDES = ["left", "right"]
COLOURS = ["red", "green"]
KEY = {"red": "right", "green": "left"}      # one of the two key mappings; the other swaps the labels
SET = 12                                     # 3 words x 2 sides x 2 colours
SETS_PER_BLOCK = 9


def prime_compatibility_of(word, colour):
    return "neutral" if word == "cross" else "compatible" if word == colour else "incompatible"


def simon_congruency_of(side, colour):
    return "congruent" if KEY[colour] == side else "incongruent"


def factors():
    word = Factor("prime_word", WORDS)
    side = Factor("target_location", SIDES)
    colour = Factor("target_colour", COLOURS)
    prime = Factor("prime_compatibility", [
        DerivedLevel(level, WithinTrial(lambda w, c, level=level: prime_compatibility_of(w, c) == level, [word, colour]))
        for level in ("compatible", "neutral", "incompatible")])
    simon = Factor("simon_congruency", [
        DerivedLevel(level, WithinTrial(lambda s, c, level=level: simon_congruency_of(s, c) == level, [side, colour]))
        for level in ("congruent", "incongruent")])
    return word, side, colour, prime, simon


def previous(factor, name):
    """The level of `factor` on the trial before, as a factor of its own."""
    return Factor(name, [DerivedLevel(level.name, Transition(lambda x, level=level.name: x[-1] == level, [factor]))
                         for level in factor.levels])


def repeats(factor, name):
    """Does `factor` have the same level as on the trial before?"""
    return Factor(name, [DerivedLevel("repeats", Transition(lambda x: x[0] == x[-1], [factor])),
                         DerivedLevel("changes", Transition(lambda x: x[0] != x[-1], [factor]))])


def proposed():
    """Sets of twelve kept, and everything that can repeat from the trial before balanced.

    Two crossings: the twelve combinations, repeated set by set; and "the side
    repeats" x "the colour repeats". Simon congruency, side and response then
    each repeat on half of the trials, and the same square on a quarter.
    The repeat mode applies to both crossings, so the four cases are also even
    within every four trials: stricter than needed, and fast (seconds).
    """
    word, side, colour, prime, simon = factors()
    side_repeats, colour_repeats = repeats(side, "side_repeats"), repeats(colour, "colour_repeats")
    return MultiCrossBlock([word, side, colour, prime, simon, side_repeats, colour_repeats],
                           [[word, side, colour], [side_repeats, colour_repeats]],
                           [MinimumTrials(SET * SETS_PER_BLOCK + 1)],
                           mode=RepeatMode.REPEAT, alignment=AlignmentMode.PARALLEL_START)


def proposed_block_level():
    """As proposed(), but even over the block only: the four cases 27 times each, anywhere.

    Looser, so the order is freer. Slow: about five minutes with CMSGen.
    """
    word, side, colour, prime, simon = factors()
    cases = {"side and colour": (True, True), "side only": (True, False), "colour only": (False, True), "neither": (False, False)}
    what = Factor("what_repeats", [
        DerivedLevel(name, Transition(lambda s, c, want=want: (s[0] == s[-1], c[0] == c[-1]) == want, [side, colour]))
        for name, want in cases.items()])
    one_set = CrossBlock([word, side, colour, prime, simon, what], [word, side, colour], [])
    n = SET * SETS_PER_BLOCK
    return Repeat(one_set, [MinimumTrials(n + 1)] + [ExactlyK(n // 4, (what, name)) for name in cases])


def trial_type_only():
    """Alternative: sets kept and only Simon congruency crossed with that of the trial before.

    Evens out trial type, and pushes side and response repetitions further from one half
    (in sets of four: from 38% to 33%), because the repeats of trial type are bought with
    trials on which side and colour both change.
    """
    word, side, colour, prime, simon = factors()
    before = previous(simon, "previous_simon_congruency")
    return MultiCrossBlock([word, side, colour, prime, simon, before],
                           [[word, side, colour], [simon, before]],
                           [MinimumTrials(SET * SETS_PER_BLOCK + 1)],
                           mode=RepeatMode.REPEAT, alignment=AlignmentMode.PARALLEL_START)


def conditions_crossed():
    """Alternative: each of the 6 conditions (prime compatibility x Simon congruency) follows each
    of the 6 conditions 3 times. About two minutes with CMSGen."""
    word, side, colour, prime, simon = factors()
    before_simon = previous(simon, "previous_simon_congruency")
    before_prime = previous(prime, "previous_prime_compatibility")
    return MultiCrossBlock([word, side, colour, prime, simon, before_simon, before_prime],
                           [[word, side, colour], [prime, simon, before_prime, before_simon]],
                           [MinimumTrials(SET * SETS_PER_BLOCK + 1)],
                           mode=RepeatMode.REPEAT, alignment=AlignmentMode.PARALLEL_START)


def as_published():
    """One block as the paper describes it: nine sets of the twelve combinations, each set in random order."""
    word, side, colour, prime, simon = factors()
    return Repeat(CrossBlock([word, side, colour, prime, simon], [word, side, colour], []),
                  [MinimumTrials(SET * SETS_PER_BLOCK)])


def expected_rate_in_shuffled_sets(set_size=SET):
    """How often a congruent trial follows a congruent one when sets are shuffled: exact, long run.

    Inside a set (set_size - 1 of every set_size transitions) the next trial is one of the
    set_size / 2 - 1 remaining congruent ones among set_size - 1; across a border it is one half.
    """
    half = set_size // 2
    return ((set_size - 1) * (half - 1) / (set_size - 1) + 0.5) / set_size


def one_block(block):
    return pd.DataFrame(synthesize_trials(block, 1, CMSGen)[0])


def summary(trials):
    """The counts that the example reports for a block."""
    squares = list(zip(trials["target_location"], trials["target_colour"]))
    combos = list(zip(trials["prime_word"], trials["target_location"], trials["target_colour"]))
    pairs = list(zip(squares[:-1], squares[1:]))
    share = lambda same: round(100 * sum(same(a, b) for a, b in pairs) / len(pairs))
    return {
        "trials": len(trials),
        "sets_of_twelve": all(len(set(combos[i * SET:(i + 1) * SET])) == SET for i in range(len(combos) // SET)),
        "repeats_percent": {
            "simon_congruency": share(lambda a, b: simon_congruency_of(*a) == simon_congruency_of(*b)),
            "side": share(lambda a, b: a[0] == b[0]),
            "response": share(lambda a, b: a[1] == b[1]),
            "same_square": share(lambda a, b: a == b),
        },
    }


if __name__ == "__main__":
    print("expected rate, shuffled sets of twelve:", round(expected_rate_in_shuffled_sets(), 4))
    print("proposed", summary(one_block(proposed())))
    print("trial_type_only", summary(one_block(trial_type_only())))
    print("as_published (one block; what repeats differs from block to block)", summary(one_block(as_published())))
    if "--slow" in sys.argv:
        print("proposed_block_level", summary(one_block(proposed_block_level())))
        print("conditions_crossed", summary(one_block(conditions_crossed())))
