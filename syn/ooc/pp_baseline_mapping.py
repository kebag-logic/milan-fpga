#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reconcile flattened logic LUTs through an equivalent hierarchical mapping.

Partition both standalone netlists into disjoint direct processor children,
processor own logic, other wrapper children and wrapper own logic. Explicitly
retain the flattened-minus-hierarchical residual; never attribute it by name.
"""

import argparse
from collections import Counter, defaultdict
import csv
from functools import cache
import json
from pathlib import Path
import re
import sys


def logic_luts(counts: Counter) -> int:
    """Count raw logic primitives, excluding RAM, SRL and dedicated inverters."""
    return sum(count for primitive, count in counts.items()
               if re.fullmatch(r"LUT[1-6]", primitive))


def hierarchical_counts(path: Path) -> dict[str, Counter]:
    """Expand mapped module instances, preserving instance multiplicity."""
    modules = json.loads(path.read_text())["modules"]

    def children(name: str) -> dict:
        """Library blackboxes may retain simulation cells; count the primitive."""
        module = modules.get(name, {})
        if any(int(module.get("attributes", {}).get(flag, "0"), 2)
               for flag in ("blackbox", "whitebox")):
            return {}
        return module.get("cells", {})

    @cache
    def total(name: str) -> Counter:
        """Count one mapped module, recursively, without changing cached data."""
        cells = children(name)
        if not cells:
            return Counter({name: 1})
        result = Counter()
        for cell in cells.values():
            result.update(total(cell["type"]))
        return result

    rows = defaultdict(Counter)
    top = modules["KL_pp_shadow"]["cells"]
    processor = modules[top["u_pp"]["type"]]["cells"]
    for prefix, cells in (("", top), ("u_pp/", processor)):
        for name, cell in cells.items():
            if not prefix and name == "u_pp":
                continue
            nested = children(cell["type"])
            key = prefix + (name if nested else "@own")
            rows[key].update(total(cell["type"]))
    return dict(rows)


def vivado_counts(path: Path) -> dict[str, Counter]:
    """Partition the standalone primitive census at the same source scopes."""
    rows = defaultdict(Counter)
    with path.open() as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            parts = row["cell"].split("/")
            if parts[0] == "u_pp":
                key = "u_pp/" + (parts[1] if len(parts) > 2 else "@own")
            else:
                key = parts[0] if len(parts) > 1 else "@own"
            rows[key][row["primitive"]] += 1
    return dict(rows)


def reconciliation(hierarchical: Path, flattened: Path, census: Path) -> list[dict]:
    """Make disjoint contributions sum exactly to the original raw gap."""
    mapped = hierarchical_counts(hierarchical)
    vendor = vivado_counts(census)
    rows = []
    for name in sorted(set(mapped) | set(vendor)):
        left = logic_luts(mapped.get(name, Counter()))
        right = logic_luts(vendor.get(name, Counter()))
        rows.append(dict(instance=name, hierarchical_Yosys=left,
                         raw_Vivado=right, difference=left - right))
    rows.sort(key=lambda row: (-abs(row["difference"]), row["instance"]))
    flat_cells = json.loads(flattened.read_text())["modules"]["KL_pp_shadow"]["cells"]
    flat = logic_luts(Counter(cell["type"] for cell in flat_cells.values()))
    hierarchical_total = sum(row["hierarchical_Yosys"] for row in rows)
    vendor_total = sum(row["raw_Vivado"] for row in rows)
    rows.append(dict(instance="@flattening_residual", hierarchical_Yosys=flat - hierarchical_total,
                     raw_Vivado=0, difference=flat - hierarchical_total))
    if sum(row["difference"] for row in rows) != flat - vendor_total:
        raise AssertionError("raw logic reconciliation does not balance")
    rows.append(dict(instance="@flat_total", hierarchical_Yosys=flat,
                     raw_Vivado=vendor_total, difference=flat - vendor_total))
    return rows


def main() -> None:
    """Emit the complete logic-LUT reconciliation as a compact TSV."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hierarchical", type=Path)
    parser.add_argument("flattened", type=Path)
    parser.add_argument("census", type=Path)
    args = parser.parse_args()
    rows = reconciliation(args.hierarchical, args.flattened, args.census)
    writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)


if __name__ == "__main__":
    main()
