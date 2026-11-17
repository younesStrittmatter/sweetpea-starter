"""The checker's --compare finds what differs between compared conditions, also when nobody named it."""
import csv
import random
import subprocess
import sys
from pathlib import Path

CHECKER = Path(__file__).resolve().parents[1] / "skills" / "sweetpea" / "scripts" / "check_design.py"


def run(tmp_path, blocks, compare):
    files = []
    for number, rows in enumerate(blocks):
        path = tmp_path / f"block_{number}.csv"
        with open(path, "w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        files.append(str(path))
    return subprocess.run([sys.executable, str(CHECKER), *files, "--compare", compare],
                          capture_output=True, text=True).stdout.split("What differs")[1]


def test_a_relation_between_two_columns_that_nobody_named(tmp_path):
    """Prime and target from the same numbers, every pair once: only congruent pairs can be equal."""
    numbers = ["1", "4", "6", "9"]
    rng = random.Random(1)
    blocks = []
    for _ in range(6):
        rows = [{"prime": p, "target": t, "congruency": "congruent" if (int(p) < 5) == (int(t) < 5) else "incongruent"}
                for p in numbers for t in numbers] * 2
        rng.shuffle(rows)
        blocks.append(rows)
    out = run(tmp_path, blocks, "congruency")
    assert "prime equals target on this trial = same" in out
    assert "never in one condition" in out


def test_the_trial_before_in_shuffled_sets(tmp_path):
    """Sets of four, shuffled: a trial follows its own type less often than the other type."""
    rng = random.Random(2)
    blocks = []
    for _ in range(40):
        rows = []
        for _ in range(8):
            rows += [{"congruency": c} for c in rng.sample(["congruent", "congruent", "incongruent", "incongruent"], 4)]
        blocks.append(rows)
    out = run(tmp_path, blocks, "congruency")
    assert "congruency on the trial before" in out


def test_nothing_is_reported_for_independent_draws(tmp_path):
    rng = random.Random(3)
    blocks = [[{"congruency": rng.choice(["congruent", "incongruent"]), "side": rng.choice(["left", "right"])}
               for _ in range(200)] for _ in range(10)]
    out = run(tmp_path, blocks, "congruency")
    assert "nothing differs by more than chance" in out
