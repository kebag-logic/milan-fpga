#!/usr/bin/env python3
"""Round-2 reviewer delta probes for KL_crf_rx (disposable; never edits a checkout).

Usage: reviewer_mutants_r2.py <extracted-head-root> <work-dir> [mutant ...]
Needs VERILATOR in the environment (the capped pinned wrapper). Same method
as the round-1 script: each mutant is a private copy of the crf_rx harness
directory built against a mutated KL_crf_rx.sv. Only the unit and
discontinuity harnesses are built (the talker_step leg does not exercise
the lock timeout under rejects). For every run it prints rc and ALL named
failing checks, and marks which of the round-2 reject-stream checks fired.
A build failure is reported separately, never as a kill.
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REFRESH = "      if (w_acc_run_w) begin"
TIMEOUT = "      end else if (tout_r == TOUT_CYC_C[$clog2(TOUT_CYC_C+1)-1:0]) begin"
UNLOCK = "        if (locked_o) begin\n          locked_o       <= 1'b0;"
MUTANTS = (
    ("clean", None, None),
    # a reject refreshes the timeout only while the sink is locked
    ("r2_refresh_when_locked", REFRESH,
     "      if (w_acc_run_w || (w_ev_uf_w && locked_o)) begin"),
    # a reject refreshes the timeout only in the second half of the window
    ("r2_refresh_late_window", REFRESH,
     "      if (w_acc_run_w || (w_ev_uf_w && tout_r[14])) begin"),
    # the timeout expires 200 clocks (1 ms at 200 kHz) late
    ("r2_timeout_late_1ms", TIMEOUT,
     "      end else if (tout_r == TOUT_CYC_C[$clog2(TOUT_CYC_C+1)-1:0] + 15'd200) begin"),
    # the timeout expires 40 clocks (0.2 ms at 200 kHz) early
    ("r2_timeout_early_200us", TIMEOUT,
     "      end else if (tout_r == TOUT_CYC_C[$clog2(TOUT_CYC_C+1)-1:0] - 15'd40) begin"),
    # an expired timeout keeps scoring MEDIA_UNLOCKED while silent
    ("r2_unlock_recounts", UNLOCK,
     "        if (1'b1) begin\n          locked_o       <= 1'b0;"),
    # a reject on an unlocked sink relocks it and scores MEDIA_LOCKED
    ("r2_reject_relocks", "        if (!w_fmt_ok) begin",
     "        if (!w_fmt_ok) begin\n          if (!locked_o) begin locked_o <= 1'b1;"
     " cnt_locked_o <= cnt_locked_o + 32'd1; end"),
)
TARGETS = (("unit", "obj_dir/Vcrf_rx_sim"), ("discontinuity", "obj_discontinuity/Vdiscontinuity"))
NEW = ("reject stream",)


def fails(output: str) -> list[str]:
    return [n.strip() for n in re.findall(r"\[FAIL\]\s*([^\n]*)", output)]


def main() -> int:
    head, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    rtl = (head / "hdl/ieee1722/crf/KL_crf_rx.sv").read_text()
    only = set(sys.argv[3:])
    verdicts = []
    for name, anchor, repl in MUTANTS:
        if only and name not in only:
            continue
        root = work / name
        shutil.rmtree(root, ignore_errors=True)
        (root / "tb/verilator").mkdir(parents=True)
        os.symlink(head / "hdl", root / "hdl")
        os.symlink(head / "tb/common", root / "tb/common")
        shutil.copytree(head / "tb/verilator/crf_rx", root / "tb/verilator/crf_rx",
                        ignore=shutil.ignore_patterns("obj_*", "__pycache__"))
        src = rtl
        if anchor is not None:
            if rtl.count(anchor) != 1:
                print(f"{name}: anchor count {rtl.count(anchor)}, SKIPPED", flush=True)
                verdicts.append((name, "ANCHOR"))
                continue
            src = rtl.replace(anchor, repl)
        mut = root / f"{name}.sv"
        mut.write_text(src)
        hdir = root / "tb/verilator/crf_rx"
        detected, built, new_hit = [], True, False
        for target, exe in TARGETS:
            r = subprocess.run(["make", "-C", str(hdir), target, f"RX_RTL={mut}",
                                f"VERILATOR={os.environ['VERILATOR']}"],
                               capture_output=True, text=True, check=False)
            (root / f"{target}.log").write_text(r.stdout + r.stderr)
            if r.returncode and not (hdir / exe).exists():
                built = False
                print(f"{name} {target}: BUILD FAILED rc={r.returncode}", flush=True)
                continue
            names = fails(r.stdout + r.stderr) if r.returncode else []
            summary = [l for l in (r.stdout + r.stderr).splitlines()
                       if "checks:" in l and "failures" in l]
            print(f"{name} {target}: rc={r.returncode} {summary[-1] if summary else ''}",
                  flush=True)
            shown = names if target == "discontinuity" else names[:6]
            for n in shown:
                print(f"    [FAIL] {n}", flush=True)
            if target == "discontinuity" and any(n.startswith(NEW) for n in names):
                new_hit = True
            if r.returncode:
                detected.append(target)
        if not built:
            verdict = "BUILD-FAIL"
        elif name == "clean":
            verdict = "CONTROL PASS" if not detected else "CONTROL FAIL"
        elif detected:
            verdict = ("DETECTED by " + ",".join(detected)
                       + ("; round-2 reject-stream check fired" if new_hit
                          else "; round-2 reject-stream check did NOT fire"))
        else:
            verdict = "SURVIVED"
        print(f"== {name}: {verdict}", flush=True)
        verdicts.append((name, verdict))
    print("\nSUMMARY")
    for name, verdict in verdicts:
        print(f"{name:26s} {verdict}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
