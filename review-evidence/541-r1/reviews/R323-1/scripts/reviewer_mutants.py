#!/usr/bin/env python3
"""Reviewer mutation probes for KL_crf_rx (disposable; never edits a checkout).

Usage: reviewer_mutants.py <extracted-head-root> <work-dir> [mutant ...]
Needs VERILATOR in the environment (the capped pinned wrapper). For each
mutant it writes a mutated KL_crf_rx.sv, builds the crf_rx unit,
discontinuity and talker_step harnesses against it in a private copy of
the harness directory, runs each, and records rc plus the failing check
names. A mutant is DETECTED when any harness exits non-zero after a
successful build; a build failure is reported separately, never as a kill.
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

MUTANTS = (
    ("clean", None, None),
    # the new header/row claim "does not refresh the timeout"
    ("uf_refreshes_timeout", "      if (w_acc_run_w) begin",
     "      if (w_acc_run_w || w_ev_uf_w) begin"),
    # the new header/row claim "breaks settling"
    ("uf_keeps_settle", "          settle_r  <= '0;\n        end else begin",
     "        end else begin"),
    # delayed unlock at the UNSUPPORTED_FORMAT interval commit
    ("uf_unlock_at_commit",
     "        if (iv_uf_r || w_ev_uf_w)\n          fmt_err_o <= fmt_err_o + 32'd1;",
     "        if (iv_uf_r || w_ev_uf_w) begin\n          fmt_err_o <= fmt_err_o + 32'd1;"
     "\n          locked_o <= 1'b0;\n        end"),
    # immediate unlock that also scores MEDIA_UNLOCKED
    ("uf_unlock_counted", "        if (!w_fmt_ok) begin",
     "        if (!w_fmt_ok) begin\n          if (locked_o) begin locked_o <= 1'b0;"
     " cnt_unlocked_o <= cnt_unlocked_o + 32'd1; end"),
    # the locked sink stops counting UNSUPPORTED_FORMAT
    ("uf_uncounted_when_locked",
     "        if (iv_uf_r || w_ev_uf_w)\n          fmt_err_o <= fmt_err_o + 32'd1;",
     "        if ((iv_uf_r || w_ev_uf_w) && !locked_o)\n          fmt_err_o <= fmt_err_o + 32'd1;"),
    # a locked sink's reject is also scored as an accepted PDU
    ("uf_counts_frames_rx", "        if (iv_frx_r || w_acc)",
     "        if (iv_frx_r || w_acc || (w_ev_uf_w && locked_o))"),
    # corrected form of the above: the reject raises the FRAMES_RX interval
    # flag (the tick-cycle term alone is a near-equivalent mutant)
    ("uf_flags_frames_rx", "        iv_frx_r <= iv_frx_r | w_acc;",
     "        iv_frx_r <= iv_frx_r | w_acc | (w_ev_uf_w & locked_o);"),
    # a locked sink's reject scores a phantom lock event
    ("uf_scores_lock_event", "        if (!w_fmt_ok) begin",
     "        if (!w_fmt_ok) begin\n          if (locked_o) cnt_locked_o <= cnt_locked_o + 32'd1;"),
)
TARGETS = (("unit", "obj_dir/Vcrf_rx_sim"), ("discontinuity", "obj_discontinuity/Vdiscontinuity"),
           ("talker_step", "obj_talker/Vtalker_step"))


def fails(output: str) -> list[str]:
    names = re.findall(r"\[(?:FAIL|FAIL )\]\s*([^\n]*)", output)
    names += re.findall(r"^\s*FAIL[: ]+([^\n]*)", output, flags=re.M)
    return names[:6]


def main() -> int:
    head, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    rtl = (head / "hdl/ieee1722/crf/KL_crf_rx.sv").read_text()
    verdicts = []
    only = set(sys.argv[3:])
    for name, anchor, repl in MUTANTS:
        if only and name not in only:
            continue
        root = work / name
        shutil.rmtree(root, ignore_errors=True)
        (root / "tb/verilator").mkdir(parents=True)
        os.symlink(head / "hdl", root / "hdl")
        os.symlink(head / "tb/common", root / "tb/common")
        os.symlink(head / "tb/verilator/mmcm_servo", root / "tb/verilator/mmcm_servo")
        # never inherit build outputs: an executable exists only if this
        # invocation built it
        shutil.copytree(head / "tb/verilator/crf_rx", root / "tb/verilator/crf_rx",
                        ignore=shutil.ignore_patterns("obj_*", "__pycache__"))
        src = rtl
        if anchor is not None:
            if rtl.count(anchor) != 1:
                print(f"{name}: anchor count {rtl.count(anchor)}, SKIPPED")
                verdicts.append((name, "ANCHOR"))
                continue
            src = rtl.replace(anchor, repl)
        mut = root / f"{name}.sv"
        mut.write_text(src)
        hdir = root / "tb/verilator/crf_rx"
        detected, built = [], True
        for target, exe in TARGETS:
            log = root / f"{target}.log"
            r = subprocess.run(["make", "-C", str(hdir), target, f"RX_RTL={mut}",
                                f"VERILATOR={os.environ['VERILATOR']}"],
                               capture_output=True, text=True, check=False)
            log.write_text(r.stdout + r.stderr)
            if r.returncode and not (hdir / exe).exists():
                built = False
                print(f"{name} {target}: BUILD FAILED rc={r.returncode}")
                continue
            names = fails(r.stdout + r.stderr) if r.returncode else []
            print(f"{name} {target}: rc={r.returncode}" + (f" first failures: {names}" if names else ""))
            if r.returncode:
                detected.append(target)
        verdict = ("BUILD-FAIL" if not built else
                   ("DETECTED by " + ",".join(detected)) if detected else "SURVIVED")
        if name == "clean":
            verdict = "CONTROL PASS" if built and not detected else "CONTROL FAIL"
        print(f"== {name}: {verdict}")
        verdicts.append((name, verdict))
    print("\nSUMMARY")
    for name, verdict in verdicts:
        print(f"{name:28s} {verdict}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
