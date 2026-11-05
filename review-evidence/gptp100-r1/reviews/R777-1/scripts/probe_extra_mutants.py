#!/usr/bin/env python3
"""Reviewer probe: disposable extra mutants of the #100 TLV datapath, run
through the engine arm's own run_mutant() (stage, build, both passes,
verdict, named-check rule). Nothing here is added to the arm; the staged
trees live under WORK_DIR only.

Usage: probe_extra_mutants.py ENGINE_DIR WORK_DIR [--jobs N]
Prints each verdict; exit 0 always (the verdicts are the evidence).
"""
from __future__ import annotations

import argparse
import contextlib
import io
import multiprocessing as mp
import sys
from pathlib import Path

ENGINE = "top/KL_gptp_engine.sv"
FREQ = ("#100 TLV settled: scaledLastGmFreqChange is the kept trim less "
        "the estimate")
EXTRA = [
    ("PROBE frequency truncated toward zero, not floored", ENGINE,
     "      if (tlv_mul_r) tlv_freq_r <= 32'(tlv_prod_w >>> 16);\n",
     "      if (tlv_mul_r) tlv_freq_r <= 32'(tlv_prod_w / 64'sd65536);\n",
     FREQ),
    ("PROBE frequency multiply zero-extends the difference", ENGINE,
     "  wire signed [63:0] tlv_prod_w = 64'(tlv_dlt_r) *\n",
     "  wire signed [63:0] tlv_prod_w = $signed(64'($unsigned(tlv_dlt_r))) *\n",
     FREQ),
    ("PROBE lastGmPhaseChange not sign-extended", ENGINE,
     "  wire  [95:0] tlv_phase_w = {{16{tlv_off_w[63]}}, tlv_off_w, 16'd0};\n",
     "  wire  [95:0] tlv_phase_w = {16'd0, tlv_off_w, 16'd0};\n",
     "#100 TLV slewing: lastGmPhaseChange is the last offset"),
]

ARM = WORK = None


def _init(engine_dir, work):
    global ARM, WORK
    sys.path.insert(0, engine_dir)
    import mutants as arm
    v = arm.VFLAGS
    v[v.index("-j") + 1] = "2"
    ARM, WORK = arm, Path(work)


def _one(m):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ok = ARM.run_mutant(WORK, None, m)
    return m[0], ok, buf.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("engine_dir")
    ap.add_argument("work_dir")
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    ed = str(Path(a.engine_dir).resolve())
    Path(a.work_dir).mkdir(parents=True, exist_ok=True)
    with mp.get_context("fork").Pool(a.jobs, _init, (ed, a.work_dir)) as p:
        for name, ok, text in p.imap(_one, EXTRA):
            sys.stdout.write(text)
            print(f"VERDICT {name}: {'caught' if ok else 'NOT CAUGHT'}",
                  flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
