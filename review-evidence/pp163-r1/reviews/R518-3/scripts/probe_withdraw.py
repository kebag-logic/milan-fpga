#!/usr/bin/env python3
"""Reviewer fault probes against tb/pp_top section WD (issue #163), run in disposable copies.

Usage: probe_withdraw.py --tree CLEAN_EXPORT --work DIR --out DIR --verilator PATH [--jobs N]
Each probe is a set of exact text edits (each old text must occur exactly once) to
hdl/top/protocol_processor_top.sv in a private copy of CLEAN_EXPORT. The copy is built with
`make gsi-build` and run with `--withdraw-only`. A probe is KILLED when the build succeeds, the
run prints the suite tally and exits non-zero; SURVIVED when it prints the tally and exits 0;
anything else is reported as such. The golden (no edit) must PASS. Writes one log per probe
and results.json under --out.
"""
import argparse
import json
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

TOP = "hdl/top/protocol_processor_top.sv"
ABORT = "  assign arb_start_abort_w = org_withdraw_mask_r[ser_slot_w]\n"
HEAD = ("  assign laneq_org_withdraw_head_w = (laneq_org_cnt_r != 4'd0)\n"
        "                                   && org_withdraw_mask_r[laneq_org_r[0]];\n")
COMPACT = "          && !org_withdraw_mask_r[laneq_org_r[i]]) begin\n"
STAGE = "    else        org_withdraw_mask_r <= org_withdraw_slot_mask_w;\n"

PROBES = {
    "golden": [],
    # the arbiter's pre-start abort loses the registered mask; both lane readers keep it
    "rp-abort-mask-dropped": [(ABORT, "  assign arb_start_abort_w = 1'b0\n")],
    # the lane head's withdraw drop loses the mask; compaction and the abort keep it
    "rp-head-mask-dropped": [(HEAD, "  assign laneq_org_withdraw_head_w = 1'b0;\n")],
    # the lane compaction loses the mask; the head drop and the abort keep it
    "rp-compact-mask-dropped": [(COMPACT, "          && 1'b1) begin\n")],
    # both lane readers lose the mask; only the abort keeps it
    "rp-lane-mask-dropped": [(HEAD, "  assign laneq_org_withdraw_head_w = 1'b0;\n"),
                             (COMPACT, "          && 1'b1) begin\n")],
    # the stage holds only the lowest set slot of the mask: a mask of several slots loses all but one
    "rp-mask-lowest-only": [(STAGE, "    else        org_withdraw_mask_r <= org_withdraw_slot_mask_w"
                                    " & (~org_withdraw_slot_mask_w + 8'd1);\n")],
    # the stage keeps the mask a second clock (OR with its previous value)
    "rp-mask-held-two": [(STAGE, "    else        org_withdraw_mask_r <= org_withdraw_slot_mask_w"
                                 " | (org_withdraw_mask_r & {8{|org_withdraw_slot_mask_w}});\n")],
}


def run_probe(name, edits, a):
    work = Path(a.work) / name
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(a.tree, work, symlinks=True)
    top = work / TOP
    text = top.read_text()
    for old, new in edits:
        if text.count(old) != 1:
            return name, {"status": "REFUSED", "reason": f"old text occurs {text.count(old)} times"}
        text = text.replace(old, new)
    top.write_text(text)
    log = Path(a.out) / f"{name}.log"
    suite = work / "tb/pp_top"
    with log.open("w") as fh:
        b = subprocess.run(["make", "gsi-build", f"VERILATOR={a.verilator}"], cwd=suite,
                           stdout=fh, stderr=subprocess.STDOUT)
        if b.returncode:
            return name, {"status": "BUILD-FAILED", "rc": b.returncode}
        fh.write("==== RUN ./obj_dir/Vpp_top_sim --withdraw-only\n")
        fh.flush()
        r = subprocess.run(["./obj_dir/Vpp_top_sim", "--withdraw-only"], cwd=suite,
                           stdout=fh, stderr=subprocess.STDOUT, timeout=3000)
    out = log.read_text()
    tally = re.search(r"WD: (\d+) checks, (\d+) failures", out)
    failing = sorted(set(re.findall(r"FAIL[^\n]*?(WD\d)", out)))
    if not tally:
        return name, {"status": "NO-TALLY", "rc": r.returncode}
    status = "PASS" if r.returncode == 0 and tally.group(2) == "0" else "KILLED" if r.returncode else "INCONSISTENT"
    if name != "golden" and status == "PASS":
        status = "SURVIVED"
    return name, {"status": status, "rc": r.returncode, "tally": tally.group(0), "failing": failing,
                  "edits": len(edits)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    Path(a.out).mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(a.jobs) as pool:
        results = dict(pool.map(lambda kv: run_probe(kv[0], kv[1], a), PROBES.items()))
    for name, edits in PROBES.items():
        results[name]["edit_text"] = [{"old": o, "new": n} for o, n in edits]
    (Path(a.out) / "results.json").write_text(json.dumps(results, indent=1) + "\n")
    print(json.dumps({k: {x: v[x] for x in v if x != "edit_text"} for k, v in results.items()}, indent=1))
    return 0 if results["golden"]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
