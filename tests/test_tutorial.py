"""The reference designs of the tutorial run and give the counts their pages talk about."""
import runpy
from pathlib import Path

REFERENCE = Path(__file__).resolve().parents[1] / "tutorial" / "reference"


def test_step1_both_designs_have_every_incongruent_pair_equally_often():
    generate = runpy.run_path(str(REFERENCE / "step1_congruency.py"))["generate"]
    half = generate("half congruent")
    assert len(half) == 24 and (half["congruency"] == "congruent").sum() == 12
    pairs = half.groupby(["colour", "word"]).size()
    assert all(n == (4 if colour == word else 2) for (colour, word), n in pairs.items())
    even = generate("every pair equally often")
    assert len(even) == 18 and (even.groupby(["colour", "word"]).size() == 2).all()


def test_step2_task_congruency_and_transition_are_crossed():
    trials = runpy.run_path(str(REFERENCE / "step2_task_switching.py"))["generate"]()
    assert len(trials) == 49
    assert (trials.iloc[1:].groupby(["task", "transition", "congruency"]).size() == 6).all()


def test_step3_both_ways_have_the_proportions_asked_for():
    module = runpy.run_path(str(REFERENCE / "step3_stability_flexibility.py"))
    for vary, column, frequent in (("congruency", "congruency", {"mostly congruent": "congruent", "mostly incongruent": "incongruent"}),
                                   ("switches", "transition", {"switches rare": "repeat", "switches frequent": "switch"})):
        session = module["generate"](vary)
        assert len(session) == 4 * 17
        counted = session[session["transition"] != ""]
        for context, level in frequent.items():
            block = counted[counted["context"] == context]
            assert (block[column] == level).mean() == 0.75
