#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Write the gptp_tables README's one-valued column table from its list.

WHY THIS EXISTS. The suite's lockstep cannot see a column stuck at the only
value its stimulus gives it, so every such column is declared in
`one_valued.tsv`, with that value, the reason the stimulus gives no other,
and the suite that does see a defect in it, if any. The harness reads the
list to grade its value census; this script writes the README's limits table
from the same rows, so the README cannot state other limits than the run
grades. `--check` is part of the suite's default make target.

Usage:
    python3 one_valued.py           # rewrite the table in README.md
    python3 one_valued.py --check   # change nothing; fail if it is stale

Exit 0 = the table is current (or was written); 1 = stale under --check;
2 = the list or the README's markers cannot be read.
"""

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIST = HERE / "one_valued.tsv"
README = HERE / "README.md"
#: the list's header row; the harness requires the same five fields
HEADER = ["table", "column", "value", "covered_by", "reason"]
VALUE = re.compile(r"0x[0-9a-f]+")
START = "<!-- one-valued-columns:start -->"
END = "<!-- one-valued-columns:end -->"


class Malformed(Exception):
    """The list or the README is not in the shape this script writes."""


def read_rows(text: str) -> list[list[str]]:
    """The list's rows after its header, comment and blank lines skipped."""
    lines = [line for line in text.splitlines() if line and not line.startswith("#")]
    if not lines or lines[0].split("\t") != HEADER:
        raise Malformed(f"{LIST.name}: the first row is not {HEADER}")
    rows = []
    for number, line in enumerate(lines[1:], start=1):
        fields = line.split("\t")
        if len(fields) != len(HEADER) or not all(fields):
            raise Malformed(f"{LIST.name}: row {number} has not {len(HEADER)} non-empty fields")
        if not VALUE.fullmatch(fields[2]):
            raise Malformed(f"{LIST.name}: row {number} value {fields[2]!r} is not lower-case hex")
        if any("|" in field for field in fields):
            raise Malformed(f"{LIST.name}: row {number} has a '|', which ends a table cell")
        rows.append(fields)
    return rows


def render(rows: list[list[str]]) -> str:
    """The table, between and including the README's markers."""
    out = [START,
           "| Column | Value | Why this stimulus gives no other | Covered by |",
           "|---|---|---|---|"]
    for table, column, value, covered, reason in rows:
        suite = "none" if covered == "none" else f"[`{covered}`](../{covered})"
        out.append(f"| `{table}` `{column}` | `{value}` | {reason} | {suite} |")
    out.append(END)
    return "\n".join(out)


def splice(readme: str, table: str) -> str:
    """The README with the text between its markers replaced by `table`."""
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise Malformed(f"{README.name}: each marker must appear exactly once")
    head, rest = readme.split(START, 1)
    _stale, tail = rest.split(END, 1)
    return head + table + tail


def main() -> int:
    """Write the table, or check that it is current."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="change nothing; exit 1 if the table is stale")
    args = parser.parse_args()
    try:
        current = README.read_text(encoding="utf-8")
        wanted = splice(current, render(read_rows(LIST.read_text(encoding="utf-8"))))
    except (Malformed, OSError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    if wanted == current:
        print(f"{README.name}: the one-valued table is current")
        return 0
    if args.check:
        print(f"{README.name}: the one-valued table is stale; run python3 one_valued.py",
              file=sys.stderr)
        return 1
    README.write_text(wanted, encoding="utf-8")
    print(f"{README.name}: the one-valued table was written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
