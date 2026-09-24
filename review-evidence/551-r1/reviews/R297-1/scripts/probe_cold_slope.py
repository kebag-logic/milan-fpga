#!/usr/bin/env python3
"""R297-1 disposable probe: the #551 licence leg with a COLD TSpec slope pipeline.

The shipped fixture (sim_crf_licence.cpp grant_case) warms the processor's
TSpec slope pipeline with the SAME MaxFrameSize it then re-declares, so the
first admission rounds after the graded declaration already evaluate the
correct slope. This probe changes only the warm-up TSpec:

  cold-refuse : warm/withdraw with 224 B, graded re-declaration 20000 B
                (the pipeline still holds the admissible slope when the
                refused declaration is first evaluated)
  cold-admit  : warm/withdraw with 20000 B, graded re-declaration 224 B
                (latency of an admitted start whose slope must first update)
  no-warm     : no warm-up declaration at all (withdraw only); the pipeline
                keeps the source's previous declaration's TSpec

Nothing in hdl/ is modified. Usage (from a git checkout of the exact head
with its submodules, Verilator on PATH):

  probe_cold_slope.py <tree> <cold-refuse|cold-admit|no-warm>

Writes the leg log to stdout; restores the harness bytes afterwards.
"""
import pathlib
import subprocess
import sys

ORIG = ("    const uint16_t max_frame = refuse ? 20000 : 224;\n"
        "    stage_declaration(uid, max_frame, true);\n"
        "    run_until(cyc + 128);\n"
        "    stage_declaration(uid, max_frame, false);\n")

WARM = {"cold-refuse": "refuse ? 224 : max_frame",
        "cold-admit": "refuse ? max_frame : 20000"}


def main() -> int:
    tree = pathlib.Path(sys.argv[1]).resolve()
    mode = sys.argv[2]
    leg = tree / "tb/verilator/milan_dp"
    src = leg / "sim_crf_licence.cpp"
    orig = src.read_bytes()
    text = orig.decode()
    if text.count(ORIG) != 1:
        print("PROBE-ERROR: anchor not found exactly once", flush=True)
        return 3
    if mode == "no-warm":
        new = ("    const uint16_t max_frame = refuse ? 20000 : 224; // R297 probe\n"
               "    stage_declaration(uid, max_frame, false);\n")
    else:
      new = ("    const uint16_t max_frame = refuse ? 20000 : 224;\n"
             f"    const uint16_t warm_frame = {WARM[mode]}; // R297 probe\n"
             "    stage_declaration(uid, warm_frame, true);\n"
             "    run_until(cyc + 128);\n"
             "    stage_declaration(uid, warm_frame, false);\n")
    try:
        src.write_text(text.replace(ORIG, new))
        mdir = f"obj_r297_{mode.replace('-', '_')}"
        rc = subprocess.run(["make", "crflic", "VERILATOR_JOBS=8",
                             f"CRFLIC_MDIR={mdir}"], cwd=leg).returncode
        print(f"PROBE {mode} make rc={rc}", flush=True)
        return 0
    finally:
        src.write_bytes(orig)


if __name__ == "__main__":
    sys.exit(main())
