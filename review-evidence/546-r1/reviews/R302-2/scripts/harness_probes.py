#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Round R302-2 harness-integrity probes for tb/verilator/crf_rx/sim_talker_step.cpp.

Usage: VERILATOR=<verilator 5.050> python3 harness_probes.py <clone> <packet>

Extracts the reviewed commit with `git archive` (the clone is never edited),
then plants one defect in the HARNESS (not the RTL) per case and requires a
named check to fail. A compile error never counts. At most 2 builds (x4 compile jobs) at once.
  post_edge_sampling: observe the combinational validity after the accepting
      edge (the round-1 observation) -> the quiet withhold check must fail.
  boundary_never: the boundary predicate never matches -> the talker-only and
      600 ms cases must fail "crossing history reaches a servo boundary".
  boundary_ignores_valid: the invalid-boundary tally never increments -> the
      discriminating cases must fail "servo samples invalid history".
"""

import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HEAD = "d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1"
VER = os.environ.get("VERILATOR", "verilator")
CASES = [
    ("clean", None, None, None),
    ("post_edge_sampling",
     "observe(sampled_valid, boundary, writeback, old_integ);",
     "observe(dut->rate_valid_o, boundary, writeback, old_integ);",
     "quiet: sampled validity never satisfies withhold check"),
    ("boundary_never",
     "tick_cnt_r == 511;", "tick_cnt_r == 1023;",
     "crossing history reaches a servo boundary"),
    ("boundary_ignores_valid",
     "                ++invalid_boundaries;\n", "",
     "servo samples invalid history at a boundary"),
]


def main():
    clone, packet = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    head = subprocess.run(["git", "-C", str(clone), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()
    if head != HEAD:
        print(f"refusing: clone HEAD {head} is not {HEAD}")
        return 2
    root = packet / "scratch" / "harness-run"
    shutil.rmtree(root, ignore_errors=True)
    root.mkdir(parents=True)
    arch = subprocess.run(["git", "-C", str(clone), "archive", HEAD, "hdl", "tb"],
                          capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(root)], input=arch, check=True)
    out = packet / "receipts" / "harness"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    src_dir = root / "tb/verilator/crf_rx"
    src = (src_dir / "sim_talker_step.cpp").read_text()

    def job(case):
        name, anchor, repl, failure = case
        d = root / "tb/verilator" / f"crf_rx_h_{name}"
        d.mkdir()
        for f in ("Makefile", "crf_talker_wrap.sv"):
            shutil.copy(src_dir / f, d / f)
        if anchor is not None:
            if src.count(anchor) != 1:
                return name, f"ANCHOR({src.count(anchor)})", failure
            text = src.replace(anchor, repl, 1)
        else:
            text = src
        (d / "sim_talker_step.cpp").write_text(text)
        r = subprocess.run(["make", "talker_step", f"VERILATOR={VER}"], cwd=d,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           text=True, timeout=3000)
        (out / f"{name}.log").write_text(r.stdout + f"\nexit status {r.returncode}\n")
        built = (d / "obj_talker" / "Vtalker_step").exists()
        if not built:
            return name, "COMPILE_ERROR", failure
        if failure is None:
            got = "PASS" if r.returncode == 0 and "RESULT: PASS" in r.stdout else "BAD"
        else:
            got = "KILLED" if (r.returncode != 0 and f"[FAIL] {failure}" in r.stdout) \
                else "SURVIVED"
        return name, got, failure

    with ThreadPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(job, CASES))
    ok = True
    with open(out / "SUMMARY.txt", "w") as s:
        s.write(f"head {HEAD}\n")
        for name, got, failure in rows:
            good = got == ("PASS" if failure is None else "KILLED")
            ok &= good
            line = f"{'OK ' if good else 'BAD'} {name:24s} got={got} named={failure}"
            print(line)
            s.write(line + "\n")
        s.write(f"campaign {'PASS' if ok else 'FAIL'}\n")
    print("campaign", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
