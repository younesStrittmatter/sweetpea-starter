"""Keeps the skill honest: every Python example in SKILL.md must run against
the installed SweetPea release, and the checker script must count correctly."""
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SKILL = (ROOT / "skills" / "sweetpea" / "SKILL.md").read_text(encoding="utf-8")
BLOCKS = re.findall(r"^```python\n(.*?)^```", SKILL, flags=re.M | re.S)
CHECKER = ROOT / "skills" / "sweetpea" / "scripts" / "check_design.py"


def test_skill_has_examples():
    assert len(BLOCKS) >= 6


@pytest.mark.parametrize("index", range(len(BLOCKS)))
def test_example_runs(index, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # one example writes CSV files
    exec(compile(BLOCKS[index], f"SKILL.md example {index}", "exec"), {"__name__": "__main__"})


def run_checker(tmp_path, text, *arguments):
    path = tmp_path / "trials.csv"
    path.write_text(text, encoding="utf-8")
    return subprocess.run([sys.executable, str(CHECKER), str(path), *arguments],
                          capture_output=True, text=True)


def test_checker_reports_balance_and_runs(tmp_path):
    result = run_checker(tmp_path, "color,size\nred,big\nred,small\nblue,big\nblue,small\n",
                         "--balance", "color", "size", "--runs", "color")
    assert result.returncode == 0
    assert "BALANCED" in result.stdout and "NOT BALANCED" not in result.stdout
    assert "red: 2" in result.stdout


def test_checker_flags_imbalance_and_missing_combinations(tmp_path):
    result = run_checker(tmp_path, "color,size\nred,big\nred,big\nblue,small\n",
                         "--balance", "color", "size")
    assert result.returncode == 1
    assert "NOT BALANCED" in result.stdout
    assert "red / small: 0" in result.stdout


def test_checker_ignores_empty_first_transition(tmp_path):
    result = run_checker(tmp_path, "task,transition\na,\na,repeat\nb,switch\n",
                         "--balance", "transition")
    assert result.returncode == 0
