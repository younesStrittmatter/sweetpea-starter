#!/usr/bin/env python3
"""Count what a trial sequence actually contains.

    python check_design.py trials.csv --balance color congruency --runs congruency

Reads a CSV file with one row per trial and one column per factor, and prints

  * how often each level of each column occurs,
  * how often each combination of the --balance columns occurs, and whether
    those combinations are equally frequent,
  * the longest run of each level of the --runs columns.

Empty cells (the first trial of a transition factor has none) are ignored.
Exits with status 1 if the --balance combinations are not equally frequent.
Needs only the Python standard library.
"""
import argparse
import csv
import sys
from collections import Counter
from itertools import groupby, product


def read_columns(path):
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        sys.exit(f"{path}: no trials found")
    return {name: [row[name] for row in rows] for name in rows[0]}


def level_counts(values):
    return Counter(value for value in values if value != "")


def combination_counts(columns, names):
    """Counts of every possible combination of the named columns (zeros included)."""
    levels = [sorted(level_counts(columns[name])) for name in names]
    seen = Counter(
        combination
        for combination in zip(*(columns[name] for name in names))
        if "" not in combination
    )
    return {combination: seen[combination] for combination in product(*levels)}


def longest_runs(values):
    runs = Counter()
    for value, group in groupby(values):
        if value != "":
            runs[value] = max(runs[value], len(list(group)))
    return runs


def report(columns, balance=(), runs=()):
    """Print the report; return True if the --balance combinations are equally frequent."""
    for name in list(balance) + list(runs):
        if name not in columns:
            sys.exit(f"no column named '{name}'; columns are: {', '.join(columns)}")

    total = len(next(iter(columns.values())))
    print(f"{total} trials, columns: {', '.join(columns)}")

    print("\nLevel counts")
    for name, values in columns.items():
        counts = level_counts(values)
        if len(counts) > 12:
            print(f"  {name}: {len(counts)} distinct values (not tabulated)")
            continue
        print(f"  {name}: " + ", ".join(f"{level}={count}" for level, count in sorted(counts.items())))

    balanced = True
    if balance:
        counts = combination_counts(columns, balance)
        balanced = len(set(counts.values())) == 1
        print(f"\nCombinations of {' x '.join(balance)}")
        for combination, count in counts.items():
            print(f"  {' / '.join(combination)}: {count}")
        print("  -> BALANCED: every combination occurs equally often" if balanced
              else "  -> NOT BALANCED: combinations differ in frequency")

    for name in runs:
        print(f"\nLongest run in {name}")
        for level, length in sorted(longest_runs(columns[name]).items()):
            print(f"  {level}: {length}")

    return balanced


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("csv_file")
    parser.add_argument("--balance", nargs="+", default=[], metavar="COLUMN",
                        help="columns whose combinations should be equally frequent")
    parser.add_argument("--runs", nargs="+", default=[], metavar="COLUMN",
                        help="columns for which to report the longest run of each level")
    arguments = parser.parse_args()
    balanced = report(read_columns(arguments.csv_file), arguments.balance, arguments.runs)
    sys.exit(0 if balanced else 1)


if __name__ == "__main__":
    main()
