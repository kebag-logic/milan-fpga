#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check disjoint report accounting with independently counted small netlists."""

import json
from pathlib import Path
import tempfile

from pp_baseline_mapping import reconciliation
from pp_baseline_rank import hierarchy, ranking


def main() -> None:
    """Cover shared LUTs, omitted children, multiplicity and library internals."""
    with tempfile.TemporaryDirectory(prefix="pp-baseline-reports-") as tmp:
        root = Path(tmp)
        report = root / "hierarchy.rpt"
        report.write_text(
            "| top | (top) | 9 | 9 | 0 | 0 | 7 | 0 | 0 | 0 |\n"
            "|   (top) | (top) | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |\n"
            "|   u_pp | processor | 8 | 8 | 0 | 0 | 6 | 0 | 0 | 0 |\n"
            "|     (u_pp) | processor | 3 | 3 | 0 | 0 | 2 | 0 | 0 | 0 |\n"
            "|     child | engine | 6 | 6 | 0 | 0 | 4 | 0 | 0 | 0 |\n")
        parsed = hierarchy(report)
        ranked = ranking(parsed, "top")
        processor = {row["instance"]: row for row in ranked if row["scope"] == "u_pp"}
        if (processor["child"]["LUT_rank"], processor["child"]["FF_rank"],
                processor["@own"]["FF"], processor["@reconciliation"]["LUT"]) != (1, 1, 2, -1):
            raise AssertionError("hierarchy ancestry, own logic or shared LUTs miscounted")
        del parsed["top/u_pp/child"]
        try:
            ranking(parsed, "top")
        except ValueError:
            pass
        else:
            raise AssertionError("omitted child accepted as complete")
        modules = {
            "KL_pp_shadow": {"cells": {
                "u_pp": {"type": "processor"}, "u_nvm": {"type": "engine"},
                "own": {"type": "LUT1"}, "inverter": {"type": "INV"}}},
            "processor": {"cells": {
                "a": {"type": "engine"}, "b": {"type": "engine"},
                "own": {"type": "LUT2"}}},
            "engine": {"cells": {"lut": {"type": "LUT6"}, "ff": {"type": "FDRE"}}},
            # A blackbox's retained simulation cells are not physical cells.
            "LUT6": {"attributes": {"blackbox": "1"},
                     "cells": {"simulation": {"type": "LUT1"}, "extra": {"type": "LUT1"}}},
        }
        hierarchical = root / "hierarchical.json"
        hierarchical.write_text(json.dumps({"modules": modules}))
        flat = root / "flat.json"
        flat.write_text(json.dumps({"modules": {"KL_pp_shadow": {
            "cells": {str(index): {"type": "LUT6"} for index in range(4)}}}}))
        census = root / "cells.tsv"
        census.write_text("cell\tprimitive\nu_pp/a/lut\tLUT6\nu_pp/own\tLUT2\n"
                          "own\tLUT1\nu_pp/a/ff\tFDRE\n")
        rows = {row["instance"]: row for row in reconciliation(hierarchical, flat, census)}
        expected = {"u_pp/a": 1, "u_pp/b": 1, "u_pp/@own": 1, "u_nvm": 1, "@own": 1}
        if {key: rows[key]["hierarchical_Yosys"] for key in expected} != expected:
            raise AssertionError("module multiplicity or blackbox primitive accounting failed")
        if (rows["@flattening_residual"]["difference"], rows["@flat_total"]["difference"]) != (-1, 1):
            raise AssertionError("flattening residual or raw logic gap miscounted")
    print("baseline reports selftest: ancestry, sharing, omission, multiplicity, blackboxes, residual PASS")


if __name__ == "__main__":
    main()
