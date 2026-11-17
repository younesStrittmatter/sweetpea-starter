"""The reference designs of the tutorial run and give the counts their pages talk about."""
import contextlib
import io
import runpy
from pathlib import Path

REFERENCE = Path(__file__).resolve().parents[1] / "tutorial" / "reference"


def run(name):
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(str(REFERENCE / name))


def test_step1_one_option_has_even_pairs_and_the_other_half_congruent():
    made = run("step1_congruency.py")
    even, half = made["trials_a"], made["trials_b"]
    assert len(even) == 18 and (even.groupby(["colour", "word"]).size() == 2).all()
    assert len(half) == 24 and (half.groupby(["colour", "congruency"]).size() == 4).all()


def test_step2_keeps_the_block_of_step1_and_crosses_it_with_the_trial_before():
    trials = run("step2_sequence.py")["trials"]
    rest = trials.iloc[1:]
    assert len(trials) == 25
    assert (rest.groupby(["trial_before", "congruency"]).size() == 6).all()
    assert (rest.groupby(["colour", "congruency", "trial_before"]).size() == 2).all()


def test_step3_blocks_have_the_proportions_asked_for_and_even_ink_colours():
    session = run("step3_adaptation.py")["session"]
    share = session.groupby("context")["congruency"].apply(lambda c: (c == "congruent").mean())
    assert share["mostly congruent"] == 0.75 and share["mostly incongruent"] == 0.25
    assert (session.groupby(["block", "colour"]).size() == 8).all()
    even = run("step3_adaptation.py")["trials_even"]
    assert all(n == (6 if colour == word else 1) for (colour, word), n in even.groupby(["colour", "word"]).size().items())


def test_step4_nests_the_mini_blocks_and_both_crossings_are_exact():
    made = run("step4_transfer.py")
    session, counted = made["session"], made["counted"]
    border = ["context_before", "context", "task", "task_transition"]
    assert len(session) == 204 and len(counted) == 192          # a first mini-block, then 16 of 12 trials
    # one kind of border per mini-block, and every kind of border once
    assert (counted.groupby("block")[border].nunique() == 1).all().all()
    assert counted.groupby(border).ngroups == 16
    assert (counted.groupby(border)["block"].nunique() == 1).all()
    # within a mini-block: the proportion of its context and every ink colour four times
    for (_, context), mini_block in counted.groupby(["block", "context"]):
        assert (mini_block["congruency"] == "congruent").sum() == (9 if context == "mostly congruent" else 3)
        assert (mini_block["colour"].value_counts() == 4).all()
