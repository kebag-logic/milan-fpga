#!/usr/bin/env python3
"""Reviewer R300-2 probe of the connected gmstep release-tail oracle (#545).

Run from a copy of the exact-head tree whose sim_gmstep.cpp carries
gmstep_oracle_print.patch (prints the oracle's counters and the samples
around release; no check changed). Each case plants one datapath edit into
a private copy, builds the gmstep leg through the suite's own recipe
(make gmstep-build DP_SRC=... GMSTEP_MDIR=...), runs it and prints the
slew-path verdicts and probe lines.

Usage: gmstep_oracle_probe.py <tree> <work> <case>...
"""
import subprocess
import sys
from pathlib import Path

PORT = """    .adj_i                (phc_adj_ts_w),"""
CASES = {
    "clean": [],
    # the published control: one extra register on the counter's addend
    "addend_delay_1": [("  timestamp_counter #(\n    .COUNTER_WIDTH (64),",
        "  logic [31:0] probe_adj_r;\n"
        "  always_ff @(posedge gtx_clk) probe_adj_r <= phc_adj_ts_w;\n"
        "  timestamp_counter #(\n    .COUNTER_WIDTH (64),"),
        (PORT, "    .adj_i                (probe_adj_r),")],
    # two extra registers
    "addend_delay_2": [("  timestamp_counter #(\n    .COUNTER_WIDTH (64),",
        "  logic [31:0] probe_adj_r, probe_adj2_r;\n"
        "  always_ff @(posedge gtx_clk) begin probe_adj_r <= phc_adj_ts_w; "
        "probe_adj2_r <= probe_adj_r; end\n"
        "  timestamp_counter #(\n    .COUNTER_WIDTH (64),"),
        (PORT, "    .adj_i                (probe_adj2_r),")],
    # a three-cycle tail
    "tail_3": [("gptp_slew_active_w || (|gptp_slew_tail_r)",
                "gptp_slew_active_w || (|gptp_slew_tail_r[2:0])")],
    # a five-cycle tail: conservative, must still pass
    "tail_5": [("  logic [3:0] gptp_slew_tail_r;", "  logic [4:0] gptp_slew_tail_r;"),
               ("gptp_slew_tail_r <= {gptp_slew_tail_r[2:0], gptp_slew_active_w};",
                "gptp_slew_tail_r <= {gptp_slew_tail_r[3:0], gptp_slew_active_w};")],
    # the level never releases at the servo
    "level_stuck_high": [(".phc_slew_active_i (gptp_slew_eff_w)", ".phc_slew_active_i (1'b1)")],
}


def main() -> int:
    tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    work.mkdir(parents=True, exist_ok=True)
    here = tree / "tb/verilator/milan_dp"
    base = (tree / "hdl/milan/milan_datapath.sv").read_text()
    for case in sys.argv[3:]:
        text = base
        for anchor, repl in CASES[case]:
            n = text.count(anchor)
            if n != 1:
                print(f"CASE {case}: ANCHOR-COUNT {n} for {anchor[:40]!r}")
                return 1
            text = text.replace(anchor, repl)
        dp = work / f"{case}_milan_datapath.sv"
        dp.write_text(text)
        mdir = work / f"obj_{case}"
        b = subprocess.run(["make", "-s", "-C", str(here), "gmstep-build",
                            f"GMSTEP_MDIR={mdir}", f"DP_SRC={dp}"],
                           capture_output=True, text=True, check=False)
        exe = mdir / "Vmilan_dp_gmstep"
        if b.returncode or not exe.is_file():
            print(b.stdout[-1500:] + b.stderr[-1500:])
            print(f"CASE {case}: BUILD-FAIL")
            continue
        r = subprocess.run([str(exe), str(mdir / "aemi.bin")], cwd=str(here),
                           capture_output=True, text=True, check=False)
        out = r.stdout + r.stderr
        (work / f"{case}.run.log").write_text(out)
        for ln in out.splitlines():
            if "slew path" in ln or "probe" in ln or "== gmstep" in ln or ln.startswith("RESULT"):
                print("  " + ln.strip())
        print(f"CASE {case}: rc={r.returncode}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
