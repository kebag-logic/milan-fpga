#!/usr/bin/env python3
"""Tabulate the disconnect runs: one row per control, one column per run.

P = refused on its recorded pin, O = refused for another reason, A = accepted.
Usage: tabulate_disconnect.py <receipts/disconnect> > table.txt"""
import json
import sys
from pathlib import Path

RUNS = ("connected-sdk", "connected-absent", "sel-sdk", "sel-absent", "e-sdk",
        "h-sdk", "res-sdk", "eres-sdk")


def code(record):
    if record["verdict"] == "ACCEPTED":
        return "A"
    return "P" if record.get("pin_ok") else "O"


def main() -> int:
    where = Path(sys.argv[1])
    table = {run: {r["label"]: code(r) for r in
                   json.loads((where / f"{run}.json").read_text())["results"]}
             for run in RUNS}
    labels = list(table["connected-sdk"])
    print(" ".join(f"{run[:10]:>10}" for run in RUNS) + "  control")
    for label in labels:
        print(" ".join(f"{table[run].get(label, '-'):>10}" for run in RUNS)
              + "  " + label)
    print()
    for run in RUNS:
        codes = list(table[run].values())
        print(f"{run}: {len(codes)} controls, P={codes.count('P')} "
              f"O={codes.count('O')} A={codes.count('A')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
