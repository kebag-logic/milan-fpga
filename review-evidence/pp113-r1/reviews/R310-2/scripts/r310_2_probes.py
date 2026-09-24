#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Round-2 reviewer comparator probes for processor PR #115 (issue #113).

Same mechanics as the round-1 probe script: each variant is extracted fresh
from the exact reviewed commit with `git archive`, edited once in a
disposable tree, built with `make gsi-build` and run with
`--gsi-internal-only`. The source checkout is never modified. A variant is
KILLED-BY-NAMED only if the build passes, the run completes with a tally,
and at least one FAIL line starts with the expected check name.

Usage:
  r310_2_probes.py --repo <clone> --commit <sha> --work <scratch> --out <dir>
                   --verilator <path> [--cpus 0-1] VARIANT [VARIANT ...]
"""

import argparse
import json
import shutil
import subprocess
from pathlib import Path

SRP = "hdl/srp/KL_srp_listener_fsm.sv"
CMP = "evt_tk_latency_chg_o[s] <= (lat_r[s] != evt_acc_latency_i);"


def cmp(expr):
    return [(SRP, CMP, f"evt_tk_latency_chg_o[s] <= {expr};", 1)]


VARIANTS = {
    "golden": ([], ""),
    # only 0->1 bit changes notify: every walking-one return must fail
    "rising-only": (cmp("(|(evt_acc_latency_i & ~lat_r[s]))"),
                    "GI LATENCY-WALK-ONE bit 0 return: exactly one unsolicited response"),
    # only 1->0 bit changes notify: every walking-one step must fail
    "falling-only": (cmp("(|(lat_r[s] & ~evt_acc_latency_i))"),
                     "GI LATENCY-WALK-ONE bit 0 step: exactly one unsolicited response"),
    # odd Hamming distance only: single-bit walks pass, the original
    # distinct-value case (distance 10) must fail
    "parity": (cmp("(^(lat_r[s] ^ evt_acc_latency_i))"),
               "GI LATENCY-CHANGE: exactly one unsolicited response"),
    # sink 1 alone truncated to [15:0]: only the walking zero on the Failed
    # sink can see it
    "sink1-low16": (cmp("((s == 0) ? (lat_r[s] != evt_acc_latency_i)"
                        " : (lat_r[s][15:0] != evt_acc_latency_i[15:0]))"),
                    "GI LATENCY-WALK-ZERO bit 16 step: exactly one unsolicited response"),
    # sink 0 alone loses bit 31
    "sink0-no-bit31": (cmp("((s == 0) ? (lat_r[s][30:0] != evt_acc_latency_i[30:0])"
                           " : (lat_r[s] != evt_acc_latency_i))"),
                       "GI LATENCY-WALK-ONE bit 31 step: exactly one unsolicited response"),
    # sink 1 alone loses bit 0
    "sink1-no-bit0": (cmp("((s == 0) ? (lat_r[s] != evt_acc_latency_i)"
                          " : (lat_r[s][31:1] != evt_acc_latency_i[31:1]))"),
                      "GI LATENCY-WALK-ZERO bit 0 step: exactly one unsolicited response"),
}


def sh(cmd, cwd, log, cpus):
    with open(log, "w") as stream:
        return subprocess.run(["taskset", "-c", cpus] + cmd, cwd=cwd, stdout=stream,
                              stderr=subprocess.STDOUT, check=False).returncode


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--commit", required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--cpus", default="0-1")
    ap.add_argument("variants", nargs="+")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    head = subprocess.run(["git", "-C", str(a.repo), "rev-parse", a.commit + "^{commit}"],
                          capture_output=True, text=True, check=True).stdout.strip()
    for name in a.variants:
        edits, expected = VARIANTS[name]
        tree = a.work / name
        if tree.exists():
            shutil.rmtree(tree)
        tree.mkdir(parents=True)
        arc = subprocess.run(["git", "-C", str(a.repo), "archive", head, "hdl",
                              "tb/common", "tb/pp_top"], capture_output=True, check=True)
        subprocess.run(["tar", "-x", "-C", str(tree)], input=arc.stdout, check=True)
        for fname, old, new, count in edits:
            p = tree / fname
            text = p.read_text()
            if text.count(old) != count:
                raise SystemExit(f"{name}: {fname} has {text.count(old)} sites, want {count}")
            p.write_text(text.replace(old, new))
        bench = tree / "tb/pp_top"
        brc = sh(["make", "gsi-build", "VERILATOR=" + a.verilator], bench,
                 a.out / f"{name}-build.log", a.cpus)
        rrc, fails, tally = None, [], ""
        if brc == 0:
            rlog = a.out / f"{name}-run.log"
            rrc = sh(["./obj_dir/Vpp_top_sim", "--gsi-internal-only"], bench, rlog, a.cpus)
            lines = rlog.read_text(errors="replace").splitlines()
            fails = [l for l in lines if l.startswith("FAIL: ")]
            tally = next((l for l in lines if l.startswith("[build default,")), "")
        if expected == "":
            verdict = "PASS" if (rrc == 0 and not fails and tally) else "UNEXPECTED"
        else:
            named = [l for l in fails if l.startswith("FAIL: " + expected)]
            verdict = "KILLED-BY-NAMED" if (brc == 0 and tally and named) else "UNEXPECTED"
        rec = {"variant": name, "commit": head, "edits": [e[:3] for e in edits],
               "build_rc": brc, "run_rc": rrc, "tally": tally,
               "n_fail_lines": len(fails), "first_fails": fails[:6],
               "expected": expected, "verdict": verdict}
        with open(a.out / "probes.jsonl", "a") as f:
            f.write(json.dumps(rec) + "\n")
        print(json.dumps(rec), flush=True)
        shutil.rmtree(tree / "tb/pp_top/obj_dir", ignore_errors=True)


if __name__ == "__main__":
    main()
