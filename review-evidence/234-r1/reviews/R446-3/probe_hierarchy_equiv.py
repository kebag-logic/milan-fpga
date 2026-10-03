#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe: the round-3 hierarchy parser against the round-2 one on real reports.

Loads `hierarchy()` from the head's syn/ooc/pp_baseline_rank.py and from a copy
of the round-2 file, parses each real report with both and compares the parsed
tables and the ranking command's full TSV output byte for byte. Also counts the
10-field rows each version skips, and plants a non-count row to confirm the new
parser refuses it.

Usage: probe_hierarchy_equiv.py <checkout> <old-rank-py> <report>...; exit 0 when all equal.
"""

import contextlib
import hashlib
import importlib.util
import io
from pathlib import Path
import sys
import tempfile


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ranking_tsv(module, report: Path, root: str) -> bytes:
    out = io.StringIO()
    argv = sys.argv
    sys.argv = ["pp_baseline_rank.py", str(report), "--root", root]
    try:
        with contextlib.redirect_stdout(out):
            module.main()
    finally:
        sys.argv = argv
    return out.getvalue().encode()


def main() -> int:
    repo, old_path, reports = Path(sys.argv[1]), Path(sys.argv[2]), [Path(p) for p in sys.argv[3:]]
    new = load(repo / "syn/ooc/pp_baseline_rank.py", "rank_new")
    old = load(old_path, "rank_old")
    bad = 0
    for report in reports:
        a, b = old.hierarchy(report), new.hierarchy(report)
        skipped = sum(1 for line in report.read_text().splitlines() if len(line.split("|")[1:-1]) == 10
                      and not line.split("|")[3].strip().isdigit())
        root = "alinx_ax7101/milan_datapath/pp_shadow" if "gateware" in str(report) else "KL_pp_shadow"
        ta, tb = ranking_tsv(old, report, root), ranking_tsv(new, report, root)
        same = a == b and ta == tb
        bad += not same
        print(f"{'OK ' if same else 'BAD'} {report.relative_to(report.parents[3])}: {len(a)} rows, "
              f"tables {'equal' if a == b else 'DIFFER'}, ranking TSV sha256 old {hashlib.sha256(ta).hexdigest()[:16]} "
              f"new {hashlib.sha256(tb).hexdigest()[:16]} ({len(tb)} bytes), 10-field non-count rows {skipped}")
    text = reports[0].read_text().splitlines()
    index = next(i for i, line in enumerate(text) if len(line.split("|")[1:-1]) == 10
                 and line.split("|")[3].strip().isdigit())
    cells = text[index].split("|")
    cells[3] = " n/a "
    planted = text[:index] + ["|".join(cells)] + text[index + 1:]
    with tempfile.NamedTemporaryFile("w", suffix=".rpt", delete=False) as handle:
        handle.write("\n".join(planted) + "\n")
    try:
        new.hierarchy(Path(handle.name))
        print("BAD planted non-count row: accepted")
        bad += 1
    except ValueError as error:
        print(f"OK  planted non-count row refused: {str(error)[:90]}")
    rows_old = old.hierarchy(Path(handle.name))
    print(f"INFO round-2 parser on the planted report: {len(rows_old)} rows (the row and its subtree position skipped)")
    Path(handle.name).unlink()
    print(f"hierarchy equivalence: {bad} mismatch(es)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
