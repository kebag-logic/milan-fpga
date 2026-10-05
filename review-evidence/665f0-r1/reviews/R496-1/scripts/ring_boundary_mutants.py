#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ring_boundary_mutants.py - reviewer probe for PR #668 (#665 F0).

Plants ring and doorbell boundary defects (off-by-one free space, removed
occupancy guards) into disposable copies of the tree and runs the mailbox
suite's own Wishbone build (make run-wb, the 120 checks) on each. A defect the
suite passes is reported as SURVIVED: a ring/doorbell semantic the suite does
not pin at its boundary.

usage: ring_boundary_mutants.py <clean-tree> <workdir> [--jobs N]
"""
import argparse
import os
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

V = os.environ.get("VERILATOR", "verilator")   # the pinned Verilator 5.050
MUTANTS = (
    ("rx-free-space-off-by-one", "KL_mbx_rx.sv", "+ 32'd2 < 32'(free_w))", "+ 32'd2 <= 32'(free_w))",
     "a record one word longer than the free space is stored over the oldest unread word"),
    ("rx-bogus-tail-unguarded", "KL_mbx_rx.sv",
     "free_w       = (used_w > ring_words_w) ? 16'd0 : ring_words_w - used_w;",
     "free_w       = ring_words_w - used_w;", "an RX_TAIL past RX_HEAD makes the free space huge"),
    ("tx-occupancy-unguarded", "KL_mbx_tx.sv", "&& occ_w <= ring_words_w && rec_words_w <= occ_w;",
     "&& rec_words_w <= occ_w;", "a TX_HEAD more than a ring ahead of TX_TAIL is served"),
    ("evt-posts-into-last-record", "KL_mbx_evt.sv", "free_w >= 16'(MBX_EV_WORDS_C);",
     "free_w + 16'd4 >= 16'(MBX_EV_WORDS_C);", "the poster writes when the ring is full"),
    ("evt-ring-holds-one-less", "KL_mbx_evt.sv", "free_w >= 16'(MBX_EV_WORDS_C);",
     "free_w > 16'(MBX_EV_WORDS_C);", "the ring never fills its last record"),
    ("tx-tail-early", "KL_mbx_tx.sv", "            left_r <= len_w;\n",
     "            left_r <= len_w;\n            tail_r[ch_r] <= tail_r[ch_r] + rec_words_w;\n",
     "TX_TAIL moves past the record before its bytes leave (and again at DONE)"),
    ("rx-head-before-header", "KL_mbx_rx.sv", "        if (commit_w && ch_r == MBX_CH_W_C'(c)) begin\n          head_r",
     "        if (st_r == HDR0_S && ch_r == MBX_CH_W_C'(c)) begin\n          head_r",
     "RX_HEAD advances in HDR0, a cycle before header word 1 is written"),
)


def run(src: Path, work: Path, m: tuple) -> str:
    name, fname, old, new, what = m
    t = work / name
    if t.exists():
        shutil.rmtree(t)
    shutil.copytree(src, t, symlinks=True)
    f = t / "hdl/milan/mailbox" / fname
    text = f.read_text()
    if text.count(old) != 1:
        return f"{name}: PROBE-BROKEN ({text.count(old)} matches)"
    f.write_text(text.replace(old, new))
    mk = t / "tb/verilator/mbx/Makefile"
    mk.write_text(mk.read_text().replace("--build -j 0", "--build -j 4"))
    log = work / f"{name}.log"
    with log.open("w") as h:
        subprocess.run(["make", "run-wb", f"VERILATOR={V}"], cwd=t / "tb/verilator/mbx", stdout=h,
                       stderr=subprocess.STDOUT, timeout=1200, check=False)
    out = log.read_text(errors="replace")
    tally = re.findall(r"checks: (\d+)\s+failures: (\d+)", out)
    if not tally:
        return f"{name}: NO TALLY (build failed?) - {what}"
    checks, fails = tally[-1]
    first = next((ln for ln in out.splitlines() if ln.startswith("[FAIL]")), "")
    verdict = "caught" if int(fails) else "SURVIVED"
    return f"{name}: {verdict} ({fails} of {checks} failed) - {what}" + (f"\n    first: {first[:160]}" if first else "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    a.work.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(a.jobs) as pool:
        for line in pool.map(lambda m: run(a.src.resolve(), a.work.resolve(), m), MUTANTS):
            print(line, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
