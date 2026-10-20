#!/usr/bin/env python3
"""Reviewer fault probes for #637 round 2, run through the suite's own
dynmap_mutants.py machinery (plant, build, run, verdict) so each probe is
judged exactly as a committed control is.

Usage: python3 r669_probes.py SUITE_DIR [--jobs J] [NAME ...]
SUITE_DIR is tb/verilator/milan_dp of a disposable copy of the reviewed head.
Each probe names the checks it is EXPECTED to fail; 'expect' says whether the
reviewer predicts a catch ("caught") or a survival ("survives"). The script
prints each probe's verdict and exits 0; the reviewer reads the verdicts.
"""
import concurrent.futures
import sys
import tempfile
from pathlib import Path

suite = Path(sys.argv[1]).resolve()
argv = sys.argv[2:]
jobs = 1
if argv[:1] == ["--jobs"]:
    jobs = int(argv[1])
    argv = argv[2:]
sys.path.insert(0, str(suite))
import dynmap_mutants as dm  # noqa: E402

VALID = "          if (amr_hframe_r && amr_hid_r && (amr_hcrc_r == amr_crc_r))\n"

PROBES = {
    # the composed blank's validated-record test, one component at a time
    "valid-no-crc": ("dynmap", "validated test ignores the crc16",
                     [(VALID, "          if (amr_hframe_r && amr_hid_r)\n")],
                     "[MAPREC]", "survives"),
    "valid-no-id": ("dynmap", "validated test ignores layout and id",
                    [(VALID, "          if (amr_hframe_r && (amr_hcrc_r == amr_crc_r))\n")],
                    "[MAPREC]", "survives"),
    "valid-no-frame": ("dynmap", "validated test ignores magic and length",
                       [(VALID, "          if (amr_hid_r && (amr_hcrc_r == amr_crc_r))\n")],
                       "[MAPREC]", "survives"),
    # stages 0 and 2 do not wait for the post-terminal sweep
    "no-sweep-wait": ("dynmap", "stage 0/2 transactions do not wait for the sweep",
                      [("            if (!amap_sweep_busy_w) begin\n"
                        "              amr_step_r <= (amr_stage_r == 2'd0) ? 2'd0 : 2'd2;",
                        "            if (1'b1) begin\n"
                        "              amr_step_r <= (amr_stage_r == 2'd0) ? 2'd0 : 2'd2;")],
                      "[MAPREC]", "unknown"),
    # a refused stage-0 take-down continues instead of rolling back
    "takedown-no-rb": ("dynmap", "a refused take-down does not roll back",
                       [("          if (amr_ok_r || (amr_step_r == 2'd1)) begin",
                         "          if (amr_ok_r || (amr_step_r != 2'd2)) begin")],
                       "[MAPREC]", "survives"),
    "takedown-no-rb-8": ("maprec8", "a refused take-down does not roll back, 8x8",
                         [("          if (amr_ok_r || (amr_step_r == 2'd1)) begin",
                           "          if (amr_ok_r || (amr_step_r != 2'd2)) begin")],
                         "[MAPREC]", "survives"),
    # stage 2 puts every dynamic port back, marked or not
    "pb-all-8": ("maprec8", "stage 2 puts back every port, marked or not",
                 [("|| ((amr_stage_r == 2'd2) && !(|(amr_pb_r & amr_rmask_w)))) begin",
                   "|| ((amr_stage_r == 2'd2) && 1'b0)) begin")],
                 "[MAPREC]", "caught"),
}


def run(key):
    leg, name, edits, must, expect = PROBES[key]
    work = Path(tempfile.mkdtemp(prefix=f"r669_{key}_", dir=WORK))
    log = []
    planted = dm.plant(name, edits, work, key.replace("-", "_"), dm.DP_RTL, log)
    if planted is None:
        return key, expect, "pattern did not match once", log
    exe = dm.build(leg, planted, work / f"obj_{key}", None, log)
    if exe is None:
        return key, expect, "did not compile", log
    rc, out = dm.run_leg(leg, exe)
    (OUT / f"probe-{key}.log").write_text(out)
    reason, failed = dm.log_reports_failure(out)
    fails = [ln.strip() for ln in out.splitlines() if ln.strip().startswith("[FAIL]")]
    verdict = "caught" if (failed and rc != 0) else ("survives" if rc == 0 and not failed
                                                      else f"rc {rc}, {reason}")
    return key, expect, verdict, fails[:12]


if __name__ == "__main__":
    OUT = Path(__file__).resolve().parent.parent / "receipts"
    OUT.mkdir(exist_ok=True)
    WORK = Path(tempfile.mkdtemp(prefix="r669w_"))
    keys = argv or list(PROBES)
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        for key, expect, verdict, lines in pool.map(run, keys):
            print(f"PROBE {key}: expected {expect}, observed {verdict}", flush=True)
            for ln in lines:
                print(f"    {ln}")
    sys.exit(0)
