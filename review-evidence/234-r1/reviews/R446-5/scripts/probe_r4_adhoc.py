#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe (round 4): this reviewer's round-3 ad hoc checks, rerun at the head.

1. WNS of `1` followed by 400 zeros `.063` in a mirror of A's real route (round 3 found rc 0, RESULT: PASS):
   the head must give rc 2 with no traceback.
2. The hierarchy parser's ranking of each of the six real reports equals the published ranking TSV.
3. The armq_r census (FD* cells whose path holds `armq_r`, and `armq_cnt_r`) of each real cell census,
   with the census sha256, equals the round-4 packet's armq-census.tsv row.

Usage: probe_r4_adhoc.py <checkout> <run-root> <published-evidence-dir> <armq-census.tsv> <scratch-dir>
"""

import csv
import hashlib
import io
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

REPO, RUN, EV, CENSUS, SCRATCH = (Path(arg).resolve() for arg in sys.argv[1:6])
sys.path.insert(0, str(REPO / "syn/ooc"))
import pp_baseline_rank  # noqa: E402

DIRS = {("A", "route-1x1"): "A/work/ax7101/gateware", ("B", "route-1x1"): "B/work/ax7101/gateware",
        ("A", "ooc-1x1"): "A/work/ax7101-ooc", ("B", "ooc-1x1"): "B/work/ax7101-ooc",
        ("A", "ooc-8x8"): "A/work/ax8x8-ooc", ("B", "ooc-8x8"): "B/work/ax8x8-ooc"}
RANKED = {"route-1x1": ("route", "alinx_ax7101/milan_datapath/pp_shadow"), "ooc-1x1": ("ax7101-ooc", "KL_pp_shadow"),
          "ooc-8x8": ("ax8x8-ooc", "KL_pp_shadow")}


def wns_overflow() -> int:
    real = RUN / DIRS[("A", "route-1x1")]
    folder = SCRATCH / "wns"
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    for entry in real.iterdir():
        if entry.name != "baseline_timing.rpt":
            (folder / entry.name).symlink_to(entry)
    text = (real / "baseline_timing.rpt").read_text()
    head, _, tail = text.partition("| Design Timing Summary")
    lines = tail.splitlines(keepends=True)
    heads = next(i for i, line in enumerate(lines) if "WNS(ns)" in line)
    row = heads + 2
    token = next(re.finditer(r"\S+", lines[row]))
    lines[row] = lines[row][:token.start()] + "1" + "0" * 400 + ".063" + lines[row][token.end():]
    (folder / "baseline_timing.rpt").write_text(head + "| Design Timing Summary" + "".join(lines))
    base = SCRATCH / "baseline.json"
    data = (REPO / "syn/ooc/pp_resource_baseline.json").read_text()
    digest = re.search(r'"inputs_sha256": "([0-9a-f]{64})"', data)[1]
    base.write_text(data.replace(digest, "0" * 64))
    result = subprocess.run([sys.executable, "-B", str(REPO / "syn/ooc/pp_resource_gate.py"), "check", str(folder),
                             "--endpoint", "route-1x1", "--baseline", str(base)], capture_output=True, text=True,
                            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    last = (result.stdout + result.stderr).strip().splitlines()[-1][:160]
    ok = result.returncode == 2 and "Traceback" not in result.stderr
    print(f"{'OK ' if ok else 'BAD'} WNS 1e400-digit slack in A's real route: rc={result.returncode} want=2 | {last}")
    return not ok


def rankings() -> int:
    bad = 0
    for (combo, endpoint), relative in DIRS.items():
        name, root = RANKED[endpoint]
        rows = pp_baseline_rank.ranking(pp_baseline_rank.hierarchy(RUN / relative / "baseline_hierarchy.rpt"), root)
        out = io.StringIO()
        writer = csv.DictWriter(out, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        published = (EV / f"{combo}-{name}-ranking.tsv").read_text()
        equal = out.getvalue() == published
        bad += not equal
        print(f"{'EQUAL' if equal else 'DIFFER'} {combo}-{name}-ranking.tsv")
    return bad


def censuses() -> int:
    bad = 0
    rows = {(row["combination"], row["endpoint"]): row for row in csv.DictReader(CENSUS.open(), delimiter="\t")}
    for key, relative in DIRS.items():
        path = RUN / relative / "baseline_cells.tsv"
        data = path.read_bytes()
        armq = cnt = 0
        for line in data.decode().splitlines()[1:]:
            cell, _, primitive = line.partition("\t")
            if primitive.startswith("FD") and "armq_cnt_r" in cell:
                cnt += 1
            elif primitive.startswith("FD") and "armq_r" in cell:
                armq += 1
        got = (hashlib.sha256(data).hexdigest(), str(len(data)), str(armq), str(cnt))
        row = rows[key]
        want = (row["census_sha256"], row["census_bytes"], row["armq_r_FD_cells"], row["armq_cnt_r_FD_cells"])
        bad += got != want
        print(f"{'EQUAL' if got == want else 'DIFFER'} {key[0]} {key[1]} armq_r {armq} armq_cnt_r {cnt} "
              f"sha256 {got[0][:16]} (packet {want[2]} {want[3]} {want[0][:16]})")
    return bad


def main() -> None:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    bad = wns_overflow() + rankings() + censuses()
    print(f"probe_r4_adhoc: {bad} not as expected")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
