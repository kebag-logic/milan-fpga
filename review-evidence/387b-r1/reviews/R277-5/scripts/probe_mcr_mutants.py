#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R277-4 reviewer probe: prove probe_mcr_property.cpp can fail.

Builds the property probe against the base engine (dev 57456af9) and against
reviewer-planted engine defects, and requires each to FAIL the probe on at
least one seed. usage: probe_mcr_mutants.py <repo-root> <work-dir>
VERILATOR in the environment selects the tool.
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
HERE = Path(__file__).resolve().parent
ENGINE = ROOT / "hdl/ieee1722/avtp/KL_media_clock_restart.sv"
BASE = "57456af96b3127b9d309a995bbbd35a6113ce52d"
MERGE = "      if (restart_p_i | src_change_w) tgt_r <= ~mr_o;"
WIRE = ("        if ((restart_p_i | src_change_w) && streaming_i[t]"
        " && (hold_r[t] == '0))")
MUTANTS = [
    ("window extends one PDU past the first at the adopted level", WIRE,
     "        if ((restart_p_i | src_change_w) && streaming_i[t]"
     " && (hold_r[t] <= HOLDW_C'(1)))"),
    ("no wire-boundary term (window ends at adoption)", WIRE, "        if (1'b0)"),
    ("flip per request (cancels)", MERGE,
     "      if (restart_p_i | src_change_w) tgt_r <= ~tgt_r;"),
    ("source change no longer a request", MERGE,
     "      if (restart_p_i) tgt_r <= ~mr_o;"),
    ("hold of 7 PDUs", "hold_r[t] == HOLDW_C'(HOLD_PDU_P))) begin : g_adopt",
     "hold_r[t] >= HOLDW_C'(HOLD_PDU_P - 1))) begin : g_adopt"),
]


def run(engine: Path, tag: str) -> tuple[int, str]:
    build = WORK / f"b_{tag}"
    out = subprocess.run(["sh", str(HERE / "run_probe_mcr_property.sh"), str(ROOT),
                          str(build), str(engine)], capture_output=True, text=True,
                         check=False)
    return out.returncode, out.stdout + out.stderr


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    src = ENGINE.read_text()
    bad = 0
    base = WORK / "KL_media_clock_restart_base.sv"
    base.write_text(subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{BASE}:hdl/ieee1722/avtp/KL_media_clock_restart.sv"],
        capture_output=True, text=True, check=True).stdout)
    cases = [("base dev engine", base)]
    for i, (name, pat, rep) in enumerate(MUTANTS):
        if src.count(pat) != 1:
            print(f"[FAIL] {name}: anchor count {src.count(pat)}")
            bad += 1
            continue
        p = WORK / f"KL_media_clock_restart_m{i}.sv"
        p.write_text(src.replace(pat, rep))
        cases.append((name, p))
    for i, (name, path) in enumerate(cases):
        rc, out = run(path, f"c{i}")
        fails = [l for l in out.splitlines() if l.startswith("PROBE FAIL")]
        verdict = "KILLED" if rc != 0 and fails else "SURVIVED"
        if verdict == "SURVIVED":
            bad += 1
        print(f"[{verdict}] {name}: {len(fails)}/36 runs fail the probe")
    print(f"probe mutants: {'ALL KILLED' if not bad else f'{bad} problem(s)'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
