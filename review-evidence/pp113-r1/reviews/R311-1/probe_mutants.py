#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer mutation probes for processor issue #113 / PR #115.

Each variant is exported from the exact head with `git archive`, edited at an
exact-count site, built with the processor's own `gsi-build` target and run
with `--gsi-internal-only`. The verdict of every variant is recorded; a probe
may be expected to be KILLED (named check fails) or is recorded as SURVIVED
(all checks pass), which is itself the observation.

Usage:
  probe_mutants.py --repo CLONE --rev SHA --verilator PATH --scratch DIR \
                   --out DIR [--workers 2 --jobs 4] [--only name,...]
workers * jobs is the total parallel compile budget (8 in this review).
"""

import argparse
import concurrent.futures as cf
import json
import os
import re
import shutil
import subprocess
import tarfile
import io
from pathlib import Path

TOP = "hdl/top/protocol_processor_top.sv"
SRP = "hdl/srp/KL_srp_listener_fsm.sv"
CMP = "evt_tk_latency_chg_o[s] <= (lat_r[s] != evt_acc_latency_i);"

# name, [(file, old, new, count)], required failing check prefix or None
VARIANTS = [
    ("golden", [], None),
    # the author's retained mutant, reproduced independently
    ("r-trigger-removed",
     [(TOP, " || srp_evt_tk_latency_chg_w[k]", "", 1)],
     "GI LATENCY-CHANGE: exactly one unsolicited response"),
    # comparator width probes
    ("r-cmp-low16",
     [(SRP, CMP, "evt_tk_latency_chg_o[s] <= (lat_r[s][15:0] != evt_acc_latency_i[15:0]);", 1)],
     None),
    ("r-cmp-no-bit31",
     [(SRP, CMP, "evt_tk_latency_chg_o[s] <= (lat_r[s][30:0] != evt_acc_latency_i[30:0]);", 1)],
     None),
    ("r-cmp-low8",
     [(SRP, CMP, "evt_tk_latency_chg_o[s] <= (lat_r[s][7:0] != evt_acc_latency_i[7:0]);", 1)],
     None),
    ("r-cmp-high16",
     [(SRP, CMP, "evt_tk_latency_chg_o[s] <= (lat_r[s][31:16] != evt_acc_latency_i[31:16]);", 1)],
     None),
    # behavioural probes
    ("r-always-pulse",
     [(SRP, CMP, "evt_tk_latency_chg_o[s] <= 1'b1;", 1)],
     "GI LATENCY-SAME"),
    ("r-advertise-only",
     [(SRP, CMP, "evt_tk_latency_chg_o[s] <= (lat_r[s] != evt_acc_latency_i) && !rx_is_failed_w;", 1)],
     "GI LATENCY-CHANGE: exactly one unsolicited response for sink 1"),
    ("r-all-sinks",
     [(TOP, " || srp_evt_tk_latency_chg_w[k]", " || (|srp_evt_tk_latency_chg_w)", 1)],
     "GI LATENCY-OTHER"),
    # a latency strobe delayed by 4096 cycles: no longer coalesced with the
    # registration pulse of the same write
    ("r-delayed-strobe",
     [(TOP, " || srp_evt_tk_latency_chg_w[k]", " || lat_dly_r[4095][k]", 1),
      (TOP, "  logic [N_STREAM_IN_P-1:0]  srp_evt_tk_latency_chg_w;\n",
       "  logic [N_STREAM_IN_P-1:0]  srp_evt_tk_latency_chg_w;\n"
       "  logic [4095:0][N_STREAM_IN_P-1:0] lat_dly_r;\n"
       "  always_ff @(posedge clk_i) lat_dly_r <= {lat_dly_r[4094:0], srp_evt_tk_latency_chg_w};\n", 1)],
     None),
    # the strobe reaching the ACMP event path (TK_ATTR_REGISTERED)
    ("r-strobe-to-acmp",
     [(SRP, "if (ind_reg_w[s])  evt_tk_registered_o[s] <= 1'b1;",
       "if (ind_reg_w[s] || (lat_r[s] != evt_acc_latency_i))  evt_tk_registered_o[s] <= 1'b1;", 1)],
     None),
    # the strobe re-driving the applicant (Listener New re-declaration)
    ("r-strobe-to-applicant",
     [(SRP, "&& ((reg_r[s] == R_MT_C) || (rtype_r[s] != rx_is_failed_w));",
       "&& ((reg_r[s] == R_MT_C) || (rtype_r[s] != rx_is_failed_w)"
       " || (lat_r[s] != evt_acc_latency_i));", 1)],
     None),
]

# Feasibility of the required test outcome: two extra single-bit refreshes
# (only bit 31 differs, then only bit 0 differs) appended to the head's own
# latency sequence, alone and with each comparator-width mutant.
GI = "tb/pp_top/gsi_internal.hpp"
T_OLD = "    latency_refresh(1, 0xFFFFFFFF, 0, true);\n"
T_NEW = (T_OLD + "    latency_refresh(1, 0x7FFFFFFF, 0, true);\n"
         "    latency_refresh(1, 0x7FFFFFFE, 0, true);\n")
T_EDIT = (GI, T_OLD, T_NEW, 1)
for _n in ("r-cmp-low16", "r-cmp-no-bit31", "r-cmp-low8", "r-cmp-high16"):
    _e = [v for v in VARIANTS if v[0] == _n][0]
    VARIANTS.append(("t-" + _n[2:], _e[1] + [T_EDIT], "GI LATENCY-CHANGE: exactly one unsolicited response"))
VARIANTS.append(("t-golden", [T_EDIT], None))


def export(repo: Path, rev: str, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    data = subprocess.run(["git", "-C", str(repo), "archive", rev, "hdl",
                           "tb/common", "tb/pp_top"], check=True,
                          stdout=subprocess.PIPE).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        tar.extractall(dest)


def run_variant(args, name, edits, expected):
    tree = Path(args.scratch) / name
    export(Path(args.repo), args.rev, tree)
    for fname, old, new, count in edits:
        p = tree / fname
        text = p.read_text()
        if text.count(old) != count:
            return {"variant": name, "error": f"edit site count {text.count(old)} != {count} in {fname}"}
        p.write_text(text.replace(old, new))
    mk = tree / "tb/pp_top/Makefile"
    mk.write_text(mk.read_text().replace("--build -j 0", f"--build -j {args.jobs}", 1))
    out = Path(args.out)
    blog = out / f"{name}-build.log"
    rlog = out / f"{name}-run.log"
    bench = tree / "tb/pp_top"
    with blog.open("w") as s:
        brc = subprocess.run(["make", "gsi-build", "VERILATOR=" + args.verilator],
                             cwd=bench, stdout=s, stderr=subprocess.STDOUT,
                             timeout=3600).returncode
    if brc != 0:
        return {"variant": name, "build_rc": brc, "verdict": "BUILD-FAILED"}
    with rlog.open("w") as s:
        rrc = subprocess.run(["./obj_dir/Vpp_top_sim", "--gsi-internal-only"],
                             cwd=bench, stdout=s, stderr=subprocess.STDOUT,
                             timeout=3600).returncode
    text = rlog.read_text()
    fails = [l for l in text.splitlines() if l.startswith("FAIL: ")]
    tally = [l for l in text.splitlines() if re.search(r"\d+ checks", l)]
    complete = "[build default," in text
    if expected is None:
        verdict = ("SURVIVED" if (rrc == 0 and not fails and complete)
                   else "KILLED")
    else:
        named = [l for l in fails if l.startswith("FAIL: " + expected)]
        verdict = "KILLED-BY-NAMED-CHECK" if (rrc != 0 and named and complete) else "NOT-KILLED-AS-REQUIRED"
    if name == "golden":
        verdict = "PASS" if (rrc == 0 and not fails and complete) else "GOLDEN-FAILED"
    shutil.rmtree(bench / "obj_dir", ignore_errors=True)
    return {"variant": name, "build_rc": brc, "run_rc": rrc,
            "expected_named_check": expected, "verdict": verdict,
            "fail_lines": fails[:12], "fail_count": len(fails),
            "tally": tally[-2:]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    assert args.workers * args.jobs <= 8
    Path(args.out).mkdir(parents=True, exist_ok=True)
    sel = [v for v in VARIANTS if not args.only or v[0] in args.only.split(",")]
    results = []
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_variant, args, *v): v[0] for v in sel}
        for f in cf.as_completed(futs):
            r = f.result()
            print(json.dumps(r), flush=True)
            results.append(r)
    results.sort(key=lambda r: [v[0] for v in VARIANTS].index(r["variant"]))
    (Path(args.out) / "results.json").write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
