#!/usr/bin/env python3
"""Reviewer-owned KL_crf_rx mutants against the crf_rx discontinuity harness.

Usage: probe_mutants.py <exported-tree> <verilator> <workdir> [names...]
Builds each mutant with the tree's own Makefile target (discontinuity-build),
runs it, and prints rc plus every failing check name. A build error or a
signal is reported as such, never as a kill. At most 8 parallel builds.
"""
import concurrent.futures
import re
import subprocess
import sys
from pathlib import Path

tree, verilator, work = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve()
want = set(sys.argv[4:])
HERE = tree / "tb/verilator/crf_rx"
SRC = (tree / "hdl/ieee1722/crf/KL_crf_rx.sv").read_text()
T0 = "      if (w_acc_run_w) begin\n        tout_r <= '0;\n"
TMAX = "TOUT_CYC_C[$clog2(TOUT_CYC_C+1)-1:0]"
REJ = "        if (!w_fmt_ok) begin\n"
MUTANTS = {
    # a reject is treated like a consumed accept for the timeout
    "uf_refreshes": (T0, "      if (w_acc_run_w || w_ev_uf_w) begin\n        tout_r <= '0;\n"),
    # any matched started frame refreshes (format verdict ignored)
    "hit_refreshes": (T0, "      if (w_hit && !stop_i) begin\n        tout_r <= '0;\n"),
    # a reject halves the elapsed silence
    "uf_halves": (T0, T0 + "      end else if (w_ev_uf_w) begin\n        tout_r <= tout_r >> 1;\n"),
    # a reject pauses the silence counter for one clock
    "uf_pauses": (T0, T0 + "      end else if (w_ev_uf_w) begin\n"),
    # a reject re-arms lock once the timeout has dropped it
    "uf_relocks": (REJ, REJ + "          locked_o <= 1'b1;\n"),
    # timeout 20 clocks (100 us) late / early
    "tout_late20": (f"tout_r == {TMAX}", f"tout_r == {TMAX} + 20"),
    "tout_early20": (f"tout_r == {TMAX}", f"tout_r == {TMAX} - 20"),
    # a reject unlocks the sink (the round-1 validation-error mutant shape)
    "uf_unlocks": (REJ, REJ + "          locked_o <= 1'b0;\n"),
}


def run(name: str) -> str:
    if name == "clean":
        source = SRC
    else:
        anchor, repl = MUTANTS[name]
        if SRC.count(anchor) != 1:
            return f"{name}: ANCHOR count={SRC.count(anchor)} (not run)"
        source = SRC.replace(anchor, repl)
    rtl = work / f"{name}.sv"
    rtl.write_text(source)
    mdir = work / f"obj_{name}"
    b = subprocess.run(["make", "-s", "-C", str(HERE), "discontinuity-build",
                        f"RX_RTL={rtl}", f"DISC_MDIR={mdir}", f"VERILATOR={verilator}"],
                       capture_output=True, text=True, timeout=1200)
    if b.returncode:
        return f"{name}: BUILD FAILED rc={b.returncode}\n{b.stderr[-800:]}"
    r = subprocess.run([str(mdir / "Vdiscontinuity")], capture_output=True, text=True,
                       timeout=1200)
    out = r.stdout + r.stderr
    (work / f"{name}.log").write_text(out)
    fails = sorted(set(re.findall(r"\[FAIL\] (.*?)(?:\s+got=.*)?$", out, re.M)))
    summ = re.findall(r"== crf_rx discontinuity: .*==", out)
    verdict = ("SURVIVED" if r.returncode == 0 else
               "KILLED" if r.returncode == 1 and "RESULT: FAIL" in out else
               f"ABNORMAL rc={r.returncode}")
    lines = [f"{name}: rc={r.returncode} {verdict} {summ[-1] if summ else ''}"]
    lines += [f"    [FAIL] {f.rstrip()}" for f in fails]
    return "\n".join(lines)


work.mkdir(parents=True, exist_ok=True)
names = ["clean"] + [n for n in MUTANTS if not want or n in want]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    for text in pool.map(run, names):
        print(text, flush=True)
