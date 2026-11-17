"""The reference designs of the tutorial run and give the counts their pages talk about."""
import contextlib
import io
import runpy
from pathlib import Path

REFERENCE = Path(__file__).resolve().parents[1] / "tutorial" / "reference"


def run(name):
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(str(REFERENCE / name))


def test_step1_both_options_have_every_pair_of_a_kind_equally_often():
    made = run("step1_congruency.py")
    even, half = made["trials_a"], made["trials_b"]
    assert len(even) == 18 and (even.groupby(["colour", "word"]).size() == 2).all()
    assert len(half) == 24 and (half["congruency"] == "congruent").sum() == 12
    assert all(n == (4 if colour == word else 2) for (colour, word), n in half.groupby(["colour", "word"]).size().items())


def test_step2_keeps_the_block_of_step1_and_crosses_it_with_the_trial_before():
    trials = run("step2_sequence.py")["trials"]
    rest = trials.iloc[1:]
    assert len(trials) == 25
    assert (rest.groupby(["trial_before", "congruency"]).size() == 6).all()
    assert all(n == (2 if colour == word else 1) for (colour, word, _), n in rest.groupby(["colour", "word", "trial_before"]).size().items())


def test_step3_blocks_have_the_proportions_asked_for_and_even_pairs():
    session = run("step3_adaptation.py")["session"]
    share = session.groupby("context")["congruency"].apply(lambda c: (c == "congruent").mean())
    assert share["mostly congruent"] == 0.75 and share["mostly incongruent"] == 0.25
    assert (session.groupby(["block", "congruency", "colour", "word"]).size().groupby(["block", "congruency"]).nunique() == 1).all()


def test_step4_nests_the_mini_blocks_and_crosses_what_the_switch_cost_needs():
    made = run("step4_transfer.py")
    session, counted = made["session"], made["counted"]
    # four mini-blocks of 16, one context each, each context twice
    assert len(session) == 64
    assert (session.groupby("block")["context"].nunique() == 1).all()
    assert (session.groupby("context")["block"].nunique() == 2).all()
    # the crossing runs one trial ahead of the context: exact in stretches that start at the second trial
    full = counted[counted["stretch"] <= 3]
    cells = full.groupby(["stretch", "frequency", "task", "transition"]).size()
    assert all(n == (3 if frequency == "frequent" else 1) for (_, frequency, _, _), n in cells.items())
    # so every mini-block is within one trial of three quarters
    frequent = session.groupby("block")["frequency"].apply(lambda f: (f == "frequent").sum())
    assert frequent.between(11, 13).all()
