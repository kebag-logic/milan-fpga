#!/usr/bin/env python3
"""Reviewer probe: does a reject-only stream on a LOCKED sink still unlock at 100 ms?

Usage: probe_reject_stream.py <extracted-head-root> <work-dir>
Needs VERILATOR in the environment. Builds a private copy of the crf_rx
discontinuity harness with one extra reviewer check appended, against the
head RTL and against a mutant in which a validation error refreshes the
lock timeout. Expected: head passes, mutant fails the named probe check.
No checkout is edited.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

PROBE = r'''
    void reviewer_reject_stream_times_out() {
        // Reviewer probe: the last accepted PDU is followed only by
        // format rejects. They must neither hold lock past 100 ms nor
        // count as silence-breaking activity.
        reset(); fill(200, false);
        check.that("probe precondition: sink is locked", dut->locked_o);
        unsigned elapsed = 2;           // send() left two idle clocks
        dut->type_i = 0;
        bool held = true;
        while (elapsed < 19900) {
            fields(); dut->frame_p_i = 1; tick(); dut->frame_p_i = 0; ++elapsed;
            for (int k = 0; k < 99; ++k) { tick(); ++elapsed; }
            held &= dut->locked_o;
        }
        check.that("probe: rejects alone retain lock before 100 ms", held);
        while (elapsed < 20012) {
            fields(); dut->frame_p_i = 1; tick(); dut->frame_p_i = 0; ++elapsed;
        }
        check.that("probe: reject-only stream still unlocks at 100 ms", !dut->locked_o);
        check.dec("probe: that unlock is one MEDIA_UNLOCKED event", dut->cnt_unlocked_o, 1);
        dut->type_i = 1;
    }
'''
CASES = (("head", None, None),
         ("uf_refreshes_timeout", "      if (w_acc_run_w) begin",
          "      if (w_acc_run_w || w_ev_uf_w) begin"))


def main() -> int:
    head, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    rtl = (head / "hdl/ieee1722/crf/KL_crf_rx.sv").read_text()
    for name, anchor, repl in CASES:
        root = work / name
        shutil.rmtree(root, ignore_errors=True)
        (root / "tb/verilator").mkdir(parents=True)
        os.symlink(head / "hdl", root / "hdl")
        os.symlink(head / "tb/common", root / "tb/common")
        hdir = root / "tb/verilator/crf_rx"
        shutil.copytree(head / "tb/verilator/crf_rx", hdir,
                        ignore=shutil.ignore_patterns("obj_*", "__pycache__"))
        cpp = hdir / "sim_discontinuity.cpp"
        text = cpp.read_text()
        call, hook = "        locked_validation_error();\n", "    void locked_validation_error() {"
        assert text.count(call) == 1 and text.count(hook) == 1
        text = text.replace(call, call + "        reviewer_reject_stream_times_out();\n")
        text = text.replace(hook, PROBE + hook)
        cpp.write_text(text)
        src = rtl if anchor is None else rtl.replace(anchor, repl)
        assert anchor is None or rtl.count(anchor) == 1
        mut = root / f"{name}.sv"
        mut.write_text(src)
        r = subprocess.run(["make", "-C", str(hdir), "discontinuity", f"RX_RTL={mut}",
                            f"VERILATOR={os.environ['VERILATOR']}"],
                           capture_output=True, text=True, check=False)
        out = r.stdout + r.stderr
        (root / "discontinuity.log").write_text(out)
        built = (hdir / "obj_discontinuity/Vdiscontinuity").exists()
        print(f"== {name}: built={built} rc={r.returncode}")
        for line in out.splitlines():
            if "probe" in line or "== crf_rx discontinuity" in line or "RESULT" in line:
                print("   " + line.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
