#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""dma_mutants.py - planted defects the record mover's bench must catch (#665).

Each arm copies the mover and the package it imports to a scratch directory,
writes ONE defect into the copy (a substitution that must occur exactly once),
builds dma_main.cpp against the copy with the Makefile's own recipe (read
through `make print-dma-vflags`, never restated here), runs it, and requires
the run to exit 1 with a `[FAIL]` line naming the arm's check. The unmodified
mover is the positive control (`make run-dma`, which `make dma-mutants`
runs first). The tree is never written.

Usage:
    python3 tb/verilator/mbx/dma_mutants.py [--jobs N] [--keep DIR]

Exit 0 = every arm caught by its named check; 1 = an arm escaped or did not
build; 2 = a fixture did not apply.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE.parents[2] / "hdl" / "milan" / "mailbox"
RTL_FILES = ("KL_mbx_pkg.sv", "KL_mbx_dma.sv")


@dataclass(frozen=True)
class Arm:
    """One planted defect in KL_mbx_dma.sv and the check that must fail."""

    name: str
    old: str
    new: str
    needle: str


ARMS = (
    Arm("tail-strobe-full", "assign axi_wstrb_o   = last_word_w ? tail_be_r : 4'hF;", "assign axi_wstrb_o   = 4'hF;",
        "D1 no byte outside [addr, addr + len) is written"),
    Arm("tx-lanes-unmasked", "assign beat_data_w = last_word_w ? (axi_rdata_i & lanes_w) : axi_rdata_i;",
        "assign beat_data_w = axi_rdata_i;", "D2 the ring holds the record's words, the lanes past len zero"),
    Arm("ring-index-unwrapped", "base_r + MBX_ADDR_W_C'(index_r & mask_r);", "base_r + MBX_ADDR_W_C'(index_r);",
        "D1 memory holds the record's bytes in ring order"),
    Arm("burst-crosses-line", "return (words < 11'(room)) ? words[4:0] : room;",
        "return (words < 11'(BEATS_C)) ? words[4:0] : 5'(BEATS_C);", "D3 a burst stays inside one 64-byte line"),
    Arm("wlast-early", "assign axi_wlast_o   = (count_r + 5'd1 == chunk_r);",
        "assign axi_wlast_o   = (count_r + 5'd2 == chunk_r);", "D3 WLAST marks a burst's last beat only"),
    Arm("cpu-request-dropped", "      if (own_w && cpu_req_i) begin\n", "      if (1'b0) begin\n",
        "D4 a CPU access is answered"),
    Arm("ack-misrouted", "assign cpu_ack_o   = host_ack_i && ack_cpu_r;", "assign cpu_ack_o   = host_ack_i;",
        "D4 a CPU access held for a transfer completes after it"),
    Arm("misaligned-accepted", "if (mem_addr_i[1:0] != 2'b00) begin", "if (1'b0) begin",
        "D5 a start off a word sets ERR"),
    Arm("busy-start-accepted", "      if (start_p_i && own_w) err_r <= 1'b1;\n", "",
        "D5 a start while a transfer runs sets ERR"),
    Arm("bresp-ignored", "            if (axi_bresp_i[1]) begin\n", "            if (1'b0) begin\n",
        "D6 a write error response sets ERR"),
    Arm("rresp-error-written", "assign ring_wr_w   = beat_w && !rerr_r && (axi_rresp_i[1] == 1'b0);",
        "assign ring_wr_w   = beat_w;", "D6 no ring word is written from an errored beat or after it"),
    Arm("err-not-cleared", "              err_r       <= 1'b0;\n", "",
        "D6 the next accepted start clears ERR"),
    Arm("zero-length-runs", "              if (len_bytes_i != 12'd0) begin\n", "              if (1'b1) begin\n",
        "D7 a length of 0 runs no transfer"),
    Arm("reset-keeps-state", "      state_r      <= IDLE_S;\n      base_r       <= '0;\n",
        "      base_r       <= '0;\n", "D8 a reset leaves the mover idle"),
    Arm("hold-address-moves", "          if (hold_r) index_r <= index_r + 16'd1;\n",
        "          if (ring_wr_w) index_r <= index_r + 16'd1;\n", "D9 a request's address holds through its answer"),
    Arm("hold-data-moves", "host_wdata_o = hold_r ? hold_wdata_r : beat_data_w;", "host_wdata_o = beat_data_w;",
        "D9 a write's data holds through its answer"),
    Arm("single-beat-bursts", "return (words < 11'(room)) ? words[4:0] : room;", "return 5'd1;",
        "D9 a line's sixteen ring reads end within 32 cycles"),
)


def vflags() -> list[str]:
    """The Makefile's recipe for the mover's bench, one argument a line."""
    out = subprocess.run(["make", "-s", "-C", str(HERE), "print-dma-vflags"], check=True, capture_output=True,
                         text=True).stdout
    return [line for line in out.splitlines() if line]


def run_arm(arm: Arm, root: Path, flags: list[str]) -> tuple[str, str]:
    """Plant, build and run one arm; returns (verdict, detail)."""
    work = root / arm.name
    rtl = work / "rtl"
    rtl.mkdir(parents=True)
    for name in RTL_FILES:
        shutil.copy(RTL / name, rtl / name)
    target = rtl / "KL_mbx_dma.sv"
    text = target.read_text()
    if text.count(arm.old) != 1:
        return "FIXTURE", f"the substitution occurs {text.count(arm.old)} times"
    target.write_text(text.replace(arm.old, arm.new))
    build = subprocess.run([*flags, "--Mdir", str(work / "obj"), str(rtl / "KL_mbx_pkg.sv"), str(target),
                            str(HERE / "dma_main.cpp"), "-o", "Vmbx_dma"], cwd=HERE, capture_output=True, text=True)
    if build.returncode != 0:
        return "BUILD", build.stderr[-400:]
    run = subprocess.run([str(work / "obj" / "Vmbx_dma")], capture_output=True, text=True)
    failed = [line for line in run.stdout.splitlines() if "[FAIL]" in line]
    if run.returncode == 1 and any(arm.needle in line for line in failed):
        return "caught", arm.needle
    return "ESCAPED", f"rc {run.returncode}; {failed[:2]}"


def main() -> int:
    """Every arm, in parallel; one line each, then the tally."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--keep", type=Path, help="keep the scratch builds here")
    args = parser.parse_args()
    flags = vflags()
    with tempfile.TemporaryDirectory(prefix="mbx-dma-mutants-") as tmp:
        root = args.keep or Path(tmp)
        root.mkdir(parents=True, exist_ok=True)
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            results = list(pool.map(lambda arm: (arm, *run_arm(arm, root, flags)), ARMS))
    fixture = any(verdict == "FIXTURE" for _, verdict, _ in results)
    for arm, verdict, detail in results:
        print(f"  [{'ok' if verdict == 'caught' else verdict}] {arm.name}: {detail}")
    caught = sum(verdict == "caught" for _, verdict, _ in results)
    print(f"mbx record mover mutants: {caught} of {len(ARMS)} caught")
    if fixture:
        return 2
    return 0 if caught == len(ARMS) else 1


if __name__ == "__main__":
    sys.exit(main())
