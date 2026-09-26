#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Rank every reported wrapper and processor child, including own logic.

Input is report_utilization -hierarchical at depth 10 or deeper, with
-hierarchical_min_primitive_count 0. The explicit reconciliation row records
cross-child LUT sharing in the vendor report.
"""

import argparse
import csv
from pathlib import Path
import sys


FIELDS = ("LUT", "logic_LUT", "LUTRAM", "SRL", "FF", "RAMB36", "RAMB18", "DSP")


def hierarchy(path: Path) -> dict[str, dict[str, int]]:
    """Read indentation as ancestry, retaining each parenthesized own row."""
    rows = {}
    ancestors = []
    for line in path.read_text().splitlines():
        fields = line.split("|")[1:-1]
        if len(fields) != 10 or not fields[2].strip().isdigit():
            continue
        indent = len(fields[0]) - len(fields[0].lstrip())
        depth = (indent - 1) // 2
        name = fields[0].strip()
        if name.startswith("("):
            name = "@own"
        else:
            ancestors = ancestors[:depth] + [name]
        key = "/".join(ancestors[:depth] + [name])
        if key in rows:
            raise ValueError(f"duplicate hierarchy row: {key}")
        rows[key] = dict(zip(FIELDS, (int(value.strip()) for value in fields[2:]), strict=True))
    if not rows:
        raise ValueError("no hierarchical utilization rows")
    return rows


def ranking(rows: dict[str, dict[str, int]], root: str) -> list[dict]:
    """Return all live direct children; threshold is zero, without omission."""
    result = []
    for relative in ("", "u_pp"):
        parent = root + ("/" + relative if relative else "")
        children = {key.removeprefix(parent + "/"): counts
                    for key, counts in rows.items()
                    if key.startswith(parent + "/") and key.count("/") == parent.count("/") + 1}
        if not children or parent not in rows:
            raise ValueError(f"missing complete hierarchy: {parent}")
        ff_order = sorted(children, key=lambda key: (-children[key]["FF"], key))
        lut_order = sorted(children, key=lambda key: (-children[key]["LUT"], key))
        for position, key in enumerate(lut_order, 1):
            result.append(dict(scope=relative or "wrapper", instance=key,
                               LUT_rank=position, FF_rank=ff_order.index(key) + 1,
                               **children[key]))
        adjustment = {field: rows[parent][field] - sum(row[field] for row in children.values())
                      for field in FIELDS}
        # Hierarchical reports can count shared LUTs at both child scopes.
        # Storage and arithmetic primitives must still add exactly.
        if any(adjustment[field] for field in ("FF", "RAMB36", "RAMB18", "DSP")):
            raise ValueError(f"non-additive storage counts: {parent}: {adjustment}")
        result.append(dict(scope=relative or "wrapper", instance="@reconciliation",
                           LUT_rank="", FF_rank="", **adjustment))
        result.append(dict(scope=relative or "wrapper", instance="@total",
                           LUT_rank="", FF_rank="", **rows[parent]))
    return result



def main() -> None:
    """Emit a compact complete ranking from one hierarchical report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--root", required=True, help="full instance path, including report top")
    args = parser.parse_args()
    rows = ranking(hierarchy(args.report), args.root)
    writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)


if __name__ == "__main__":
    main()
