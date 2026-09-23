#!/usr/bin/env python3
"""Derive a 50 MHz variant of the disposable probe (30_make_probe.py output).

Why: the shipping 1x1 TDM8 shape and the Arty shapes set milan_clk_hz to
50 MHz (configs/*.yaml), so there DIV_C = 1041 and the default keep-off is
1041/128 = 8 cycles, while every raced-lock arm runs the 100 MHz shape
(keep-off 16). This variant runs the same loop, capture and arms with the
datapath clock at 50 MHz and the physical grid unchanged at the plan's
47,999.4893 Hz (100 MHz * 391/1591 / 512 from the audio clock, which does not
follow the datapath clock). Only clock-derived constants move:
  kClkHz 100e6 -> 50e6; PLAN_A pinned to its physical value; phase aims and
  range bounds scaled from DIV_C 2083 to 1041; G1/G4/G5 tick expectations
  from 4800 to 9600 per 10M cycles. The clearance floor stays 12 cycles, so
  a 50 MHz lock is expected to FAIL that grade (keep-off 8 < 12); what the
  variant measures is the clearance it does keep and the junction counts.
Usage: 32_make_probe50.py <export-root>
"""
import pathlib
import shutil
import sys

root = pathlib.Path(sys.argv[1])
src = root / "tb/verilator/media_grid_align_probe"
dst = root / "tb/verilator/media_grid_align_probe50"
if dst.exists():
    shutil.rmtree(dst)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("obj_*", "*.log"))


def sub(text, old, new, count):
    n = text.count(old)
    if n != count:
        raise SystemExit(f"anchor {old!r}: found {n}, expected {count}")
    return text.replace(old, new)


cpp = (dst / "sim_main.cpp").read_text()
cpp = sub(cpp, "constexpr double kClkHz     = 100e6;", "constexpr double kClkHz     = 50e6;", 1)
cpp = sub(cpp, "constexpr double PLAN_A = kClkHz * (391.0 / 1591.0) / 512.0;",
          "constexpr double PLAN_A = 100e6 * (391.0 / 1591.0) / 512.0;", 1)
cpp = sub(cpp, "engage_at_phase(2082);", "engage_at_phase(1040);", 1)
cpp = sub(cpp, "last_phase, 2081, 2083);", "last_phase, 1039, 1042);", 1)
cpp = sub(cpp, "clear_min, kLockClearMin, 2083);", "clear_min, kLockClearMin, 1041);", 2)
cpp = sub(cpp, "anchor_grid(kPlanPeriod, 2063);", "anchor_grid(kPlanPeriod, 1021);", 1)
cpp = sub(cpp, "dir > 0 ? 2063 : 20);", "dir > 0 ? 1021 : 20);", 1)
cpp = sub(cpp, "tick_count, 4800);", "tick_count, 9600);", 3)
(dst / "sim_main.cpp").write_text(cpp)

wrap = (dst / "media_grid_align_wrap.sv").read_text()
wrap = sub(wrap, ".CLK_FREQ_HZ_P (100_000_000),", ".CLK_FREQ_HZ_P (50_000_000),", 2)
(dst / "media_grid_align_wrap.sv").write_text(wrap)
print(f"50 MHz probe written to {dst}")
