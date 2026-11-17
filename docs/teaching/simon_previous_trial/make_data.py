"""Blocks and rates for the Simon page, for sets of two, four and twelve, written to data.js.

Run from the repository root:  python docs/teaching/simon_previous_trial/make_data.py
Nothing on the page is typed by hand: every block is generated here, the rates of the
shuffled sets are exact (and checked against a long simulation), and the rates of the designs are counted.
"""
import json
import random
from pathlib import Path

from sweetpea import (Factor, DerivedLevel, WithinTrial, Transition, MinimumTrials, ExactlyK, CrossBlock,
                      MultiCrossBlock, Repeat, RepeatMode, AlignmentMode, synthesize_trials, CMSGen)

KEY = {"red": "left", "green": "right"}          # the key of each colour (counterbalanced in the experiment)
SQUARES = [(side, colour) for side in ("left", "right") for colour in ("red", "green")]
CONGRUENT = [q for q in SQUARES if KEY[q[1]] == q[0]]
INCONGRUENT = [q for q in SQUARES if KEY[q[1]] != q[0]]
PROPERTIES = {
    "type": lambda a, b: (KEY[a[1]] == a[0]) == (KEY[b[1]] == b[0]),
    "side": lambda a, b: a[0] == b[0],
    "response": lambda a, b: a[1] == b[1],
    "square": lambda a, b: a == b,
}
SETS_SHOWN = {2: 16, 4: 8, 12: 4}                # how many sets a block on the page has


def one_set(size, rng):
    """One shuffled set. Two: a congruent and an incongruent square. Four: each square once. Twelve: each three times."""
    trials = [rng.choice(CONGRUENT), rng.choice(INCONGRUENT)] if size == 2 else SQUARES * (size // 4)
    return rng.sample(trials, len(trials))


def shuffled_sets(size, n_sets, rng):
    return [q for _ in range(n_sets) for q in one_set(size, rng)]


def rates(block):
    pairs = list(zip(block[:-1], block[1:]))
    return {name: sum(same(a, b) for a, b in pairs) / len(pairs) for name, same in PROPERTIES.items()}


def long_run_rates(size):
    """Exact rates under shuffled sets: (size - 1) of every `size` neighbour pairs lie inside a set, one across a border."""
    if size == 2:
        inside = [(c, i) for c in CONGRUENT for i in INCONGRUENT] + [(i, c) for c in CONGRUENT for i in INCONGRUENT]
        border = [(a, b) for a in SQUARES for b in SQUARES]
    else:
        items = SQUARES * (size // 4)
        inside = [(items[x], items[y]) for x in range(size) for y in range(size) if x != y]
        border = [(a, b) for a in items for b in items]
    share = lambda pairs, same: sum(same(a, b) for a, b in pairs) / len(pairs)
    total = {name: ((size - 1) * share(inside, same) + share(border, same)) / size for name, same in PROPERTIES.items()}
    # for the trial type also the two parts: inside a set, and across the border between two sets
    total["type_inside"], total["type_border"] = share(inside, PROPERTIES["type"]), share(border, PROPERTIES["type"])
    return total


def typical(size, long_run, seeds=range(3000)):
    """A shuffled block whose own rates are closest to the long-run rates."""
    def distance(seed):
        mine = rates(shuffled_sets(size, SETS_SHOWN[size], random.Random(seed)))
        return sum(abs(mine[k] - long_run[k]) for k in mine), seed
    return shuffled_sets(size, SETS_SHOWN[size], random.Random(min(seeds, key=distance)))


def repeats(factor, name):
    return Factor(name, [DerivedLevel("repeats", Transition(lambda x: x[0] == x[-1], [factor])),
                         DerivedLevel("changes", Transition(lambda x: x[0] != x[-1], [factor]))])


def designed(size):
    """Sets kept, and everything that can repeat from the trial before balanced."""
    side = Factor("side", ["left", "right"])
    colour = Factor("colour", ["red", "green"])
    n = size * SETS_SHOWN[size] + 1
    if size == 12:
        word = Factor("word", ["red", "green", "cross"])
        side_repeats, colour_repeats = repeats(side, "side_repeats"), repeats(colour, "colour_repeats")
        block = MultiCrossBlock([word, side, colour, side_repeats, colour_repeats],
                                [[word, side, colour], [side_repeats, colour_repeats]],
                                [MinimumTrials(n)], mode=RepeatMode.REPEAT, alignment=AlignmentMode.PARALLEL_START)
    else:
        cases = {"side and colour": (True, True), "side only": (True, False), "colour only": (False, True), "neither": (False, False)}
        what = Factor("what_repeats", [
            DerivedLevel(name, Transition(lambda s, c, want=want: (s[0] == s[-1], c[0] == c[-1]) == want, [side, colour]))
            for name, want in cases.items()])
        counts = [ExactlyK((n - 1) // 4, (what, name)) for name in cases]
        if size == 4:
            inner = CrossBlock([side, colour, what], [side, colour], [])
        else:
            congruency = Factor("congruency", [
                DerivedLevel("congruent", WithinTrial(lambda s, c: KEY[c] == s, [side, colour])),
                DerivedLevel("incongruent", WithinTrial(lambda s, c: KEY[c] != s, [side, colour]))])
            inner = CrossBlock([side, colour, congruency, what], [congruency], [])
        block = Repeat(inner, [MinimumTrials(n)] + counts)
    trials = synthesize_trials(block, 1, CMSGen)[0]
    return list(zip(trials["side"], trials["colour"]))


def sets_intact(block, size):
    def ok(part):
        if size == 2:
            return len(part) < 2 or {KEY[q[1]] == q[0] for q in part} == {True, False}
        return all(part.count(q) <= size // 4 for q in SQUARES)
    return all(ok(block[i:i + size]) for i in range(0, len(block) - 1, size))


if __name__ == "__main__":
    data = {"key": KEY, "variants": {}}
    for size in (2, 4, 12):
        long_run = long_run_rates(size)
        simulated = rates(shuffled_sets(size, 600000 // size, random.Random(size)))
        assert all(abs(long_run[k] - simulated[k]) < 0.005 for k in simulated), (size, long_run, simulated)
        design = designed(size)
        assert sets_intact(design, size), size
        # SweetPea puts the one extra trial at the end. Read backwards, the block has the same sets and
        # the same neighbours, and the extra trial comes first: the trial before the first set.
        design = design[::-1]
        borders = [i for i in range(1, len(design), size)]
        data["variants"][str(size)] = {
            "size": size, "original": typical(size, long_run), "design": design,
            "long_run": long_run, "design_rates": rates(design),
            "design_same_square_at_borders": sum(design[i] == design[i - 1] for i in borders) / len(borders),
            "design_same_type_at_borders": sum(PROPERTIES["type"](design[i - 1], design[i]) for i in borders) / len(borders),
            "design_same_type_inside": sum(PROPERTIES["type"](design[i - 1], design[i]) for i in range(1, len(design)) if i not in borders)
                                       / sum(1 for i in range(1, len(design)) if i not in borders),
        }
        v = data["variants"][str(size)]
        print(size, len(v["original"]), len(design), {k: round(x, 3) for k, x in long_run.items()},
              {k: round(x, 3) for k, x in v["design_rates"].items()},
              "borders: same square", round(v["design_same_square_at_borders"], 2), "same type", round(v["design_same_type_at_borders"], 2))
    Path(__file__).with_name("data.js").write_text("window.SIMON = " + json.dumps(data) + ";\n")
