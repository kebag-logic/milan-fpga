#!/usr/bin/env python3
"""Reviewer probes on the #148 fix in KL_aecp_notify, beyond the PR's named controls.

Each probe copies hdl/, tb/common, tb/aecp_notify and tb/pp_top from a head
extraction into its own tree, plants one exact edit (refused unless the old
text occurs once), builds and runs:
  tb/aecp_notify  make run                 (sections TS, TW, ...)
  tb/pp_top       --spacing-only, --notify-only, --counters-only
and records every FAIL line per run with return codes.

Usage: probe_mutants.py --head TREE --work DIR --output DIR --verilator V
                        [--jobs N] [--only NAME ...]
"""
import argparse
import concurrent.futures
import json
import shutil
import subprocess
from pathlib import Path

NTFY = "hdl/aecp/KL_aecp_notify.sv"
STAMP = "          if (em_kind_r == PP_UNS_CTRS_C) ctr_last_r[em_ctr_ix_r] <= now_ms_i;\n"
SEL = "                  ctr_last_r[pick_ctr_ix_w] <= now_ms_i;\n"

PROBES = {
    # the follow writes for every kind's job, not only GET_COUNTERS
    "kind_guard_dropped": [(NTFY, STAMP,
                            "          ctr_last_r[em_ctr_ix_r] <= now_ms_i;\n")],
    # the follow writes the descriptor the pick would choose now, not the round's
    "slot_from_live_pick": [(NTFY, STAMP, STAMP.replace("ctr_last_r[em_ctr_ix_r]",
                                                         "ctr_last_r[pick_ctr_ix_w]"))],
    # the follow writes slot 0 always (the latch removed)
    "slot_zero": [(NTFY, STAMP, STAMP.replace("ctr_last_r[em_ctr_ix_r]", "ctr_last_r[0]"))],
    # the selection stamp removed; only the follow remains
    "selection_stamp_dropped": [(NTFY, SEL, "")],
    # the unmutated head, the probes' golden
    "golden": [],
}

RUNS = (
    ("aecp_notify", "tb/aecp_notify", ["make", "run"]),
    ("spacing", "tb/pp_top", ["./obj_dir/Vpp_top_sim", "--spacing-only"]),
    ("notify", "tb/pp_top", ["./obj_dir/Vpp_top_sim", "--notify-only"]),
    ("counters", "tb/pp_top", ["./obj_dir/Vpp_top_sim", "--counters-only"]),
)


def probe(name, head, work, output, verilator):
    tree = work / name
    if tree.exists():
        shutil.rmtree(tree)
    skip = shutil.ignore_patterns("obj*", "__pycache__")
    for d in ("hdl", "tb/common", "tb/aecp_notify", "tb/pp_top"):
        shutil.copytree(head / d, tree / d, ignore=skip)
    for rel, old, new in PROBES[name]:
        p = tree / rel
        text = p.read_text()
        if text.count(old) != 1:
            return {"probe": name, "verdict": "REFUSED", "count": text.count(old)}
        p.write_text(text.replace(old, new, 1))
    rec = {"probe": name, "runs": {}}
    blog = output / f"{name}-pp_top-build.log"
    with blog.open("w") as s:
        brc = subprocess.run(["make", "gsi-build", "VERILATOR=" + verilator],
                             cwd=tree / "tb/pp_top", stdout=s, stderr=subprocess.STDOUT).returncode
    rec["pp_top_build_rc"] = brc
    for tag, d, argv in RUNS:
        log = output / f"{name}-{tag}.log"
        if d == "tb/pp_top" and brc != 0:
            rec["runs"][tag] = {"rc": None}
            continue
        cmd = argv + (["VERILATOR=" + verilator] if argv[0] == "make" else [])
        with log.open("w") as s:
            rc = subprocess.run(cmd, cwd=tree / d, stdout=s, stderr=subprocess.STDOUT).returncode
        text = log.read_text(errors="replace")
        fails = [l[6:] for l in text.splitlines() if l.startswith("FAIL: ")]
        tallies = [l for l in text.splitlines()
                   if "checks, " in l and "failures" in l or "PASS," in l]
        rec["runs"][tag] = {"rc": rc, "fails": fails, "tallies": tallies}
    shutil.rmtree(tree, ignore_errors=True)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--head", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    a.work.mkdir(parents=True, exist_ok=True)
    names = a.only or list(PROBES)
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:
        recs = list(pool.map(lambda n: probe(n, a.head.resolve(), a.work.resolve(),
                                             a.output.resolve(), a.verilator), names))
    (a.output / "results.json").write_text(json.dumps(recs, indent=1) + "\n")
    for r in recs:
        print(r["probe"], json.dumps({k: (v["rc"], len(v.get("fails", [])))
                                      for k, v in r.get("runs", {}).items()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
