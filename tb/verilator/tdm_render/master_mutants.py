#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects for KL_tdm_render_master's lane width (#584): `make master-mutants`.

Each defect is planted in a copy of KL_tdm_render_master.sv, elaborated through
this suite's own recipe (RM_SRC), and must fail the named leg with its own
words; the tracked source is never touched. An unplanted control runs first.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE.parents[2] / "hdl/ieee1722/aaf/KL_tdm_render_master.sv"

NARROW = ("    assign bit_smp_w = (32'(bit_slot_w) < SLOTS_P)\n"
          "                     ? frame_sel_w[24*32'(bit_slot_w) % FRAME_BITS_C +: 24]\n"
          "                     : 24'd0;")

#: (name, leg, original text, planted text, words the failing leg prints)
MUTANTS = (
    ("narrow-lane-unmasked", "lane1of32", NARROW,
     "    assign bit_smp_w = frame_sel_w[24*32'(bit_slot_w) % FRAME_BITS_C +: 24];",
     "past the lane: zero"),
    ("narrow-lane-one-slot-wide", "lane2of8", NARROW,
     NARROW.replace("< SLOTS_P", "<= SLOTS_P"),
     "past the lane: zero"),
    ("bank-slot-off-by-one", "lane8of8",
     "      if (smp_wr_en_i) bank_r[smp_wr_slot_i] <= smp_wr_data_i;",
     "      if (smp_wr_en_i) bank_r[smp_wr_slot_i + 1'b1] <= smp_wr_data_i;",
     "rendered: sample"),
    ("narrow-lane-unmasked-on-the-capture-master", "bus1of32", NARROW,
     "    assign bit_smp_w = frame_sel_w[24*32'(bit_slot_w) % FRAME_BITS_C +: 24];",
     "past the lane carry zero"),
    ("narrow-lane-frames-its-own-slots", "lane1of32",
     "  if (BUS_SLOTS_P == SLOTS_P) begin : g_full_lane",
     "  if (1) begin : g_full_lane",
     "past the lane: zero"),
)


def run(leg: str, src: Path | None) -> tuple[int, str]:
    """One leg through the suite's recipe, with RM_SRC planted when given."""
    cmd = ["make", "--no-print-directory", leg]
    if src is not None:
        cmd += [f"RM_SRC={src}"]
    p = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True, timeout=900)
    return p.returncode, p.stdout + p.stderr


def main() -> int:
    caught = 0
    rc, out = run("lane1of32", None)
    if rc != 0 or "RESULT: PASS" not in out:
        print("CONTROL FAILED: the unplanted lane1of32 leg does not pass")
        return 1
    print("control: lane1of32 unplanted PASS")
    text = RTL.read_text()
    work = HERE / "obj_mut"
    work.mkdir(exist_ok=True)
    for name, leg, old, new, words in MUTANTS:
        if text.count(old) != 1:
            print(f"{name}: NOT PLANTED (the original text is not unique in the source)")
            continue
        src = work / f"{name}.sv"
        src.write_text(text.replace(old, new))
        rc, out = run(leg, src)
        fails = [ln for ln in out.splitlines() if "[FAIL]" in ln and words in ln]
        ok = rc != 0 and bool(fails)
        caught += ok
        print(f"{name} ({leg}): {'CAUGHT' if ok else 'MISSED'}"
              + (f" - {fails[0].strip()}" if fails else ""))
    print(f"RESULT: {caught} of {len(MUTANTS)} caught")
    return 0 if caught == len(MUTANTS) else 1


if __name__ == "__main__":
    sys.exit(main())
