#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Negative controls for the #387 gmstep leg: prove each of its checks can fail.

sim_gmstep.cpp grades a grandmaster change that steps the PHC by 1.5 s under
CRF selection: tu on the commit edge and a holdover after the step, the stream
kept streaming, one counted render re-base, one mr toggle and one MEDIA_RESET.
Each control below plants one defect into a private copy of the source that
carries the property - the clock-validity block, the render setpoint stage or
the datapath - and rebuilds the SAME leg through the Makefile's own recipe
(`make gmstep` with CLKV_SRC, RSP_SRC or DP_SRC and GMSTEP_MDIR overridden).
The leg must FAIL by its own verdict, with the named check among the
failures; a crash or an abort is not a catch.

The base datapath is an argument, because the one the leg passes on is the
#387 edit: until it lands in the tree the controls run against a copy of the
tree with that edit applied. The leg is cycle-bounded by construction (every
AXI and AECP wait gives up after a fixed cycle count, every window is a fixed
count), so this driver sets no host-time deadline.

Usage: python3 gmstep_mutants.py --datapath <edited milan_datapath.sv>
       (run from tb/verilator/milan_dp; VERILATOR and VERILATOR_JOBS pass through)
Exit 0 = every control was caught and the clean leg passes.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path.cwd()
CLKV_RTL = HERE / "../../../hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv"
STAGE_RTL = HERE / "../../../hdl/ieee1722/aaf/KL_render_setpoint.sv"

#: (name, source, anchor, replacement, the check this defect must break)
MUTATIONS = [
    ("tu reaches the talkers four cycles late", "clkv",
     "  assign ts_uncertain_o = (~sync_ok_w) | hold_w | disc_p_w;\n",
     "  logic [3:0] tu_late_r;\n"
     "  always_ff @(posedge clk_i) begin : p_tu_late\n"
     "    tu_late_r <= {tu_late_r[2:0], (~sync_ok_w) | hold_w | disc_p_w};\n"
     "  end : p_tu_late\n"
     "  assign ts_uncertain_o = tu_late_r[3];\n",
     "tu: set in the first cycle the bank names GM B"),
    ("the plane's step does not re-arm the holdover", "datapath",
     "                   ? gptp_step_we_w : cfg_ptp_cmd_adjust),",
     "                   ? 1'b0 : cfg_ptp_cmd_adjust),",
     "tu: held at least the 0.25 s holdover after the step"),
    ("tu stops the talker", "datapath",
     "assign aaf_stream_en_w = aaf_stream_en_raw_w & ~amap_edit_out_resv_r;",
     "assign aaf_stream_en_w = aaf_stream_en_raw_w & ~amap_edit_out_resv_r & ~clkv_tu_w;",
     "licence: the talker never pauses beyond four of its intervals"),
    ("the step does not re-centre the render stage", "datapath",
     "       media_rebase_p_w | src_recentre_p_r;",
     "       src_recentre_p_r;",
     "render: the GM change is one counted re-base event"),
    ("the identity change re-centres as well as the step", "datapath",
     "       media_rebase_p_w | src_recentre_p_r;",
     "       gm_recentre_p_r | media_rebase_p_w | src_recentre_p_r;",
     "render: the GM change is one counted re-base event"),
    ("the step's recentre snaps one event off the setpoint", "stage",
     "                rptr_r[s]    <= snap_rptr_w;\n"
     "                prefill_r[s] <= 1'b0;\n",
     "                rptr_r[s]    <= prefill_r[s] ? snap_rptr_w : snap_rptr_w - 1'b1;\n"
     "                prefill_r[s] <= 1'b0;\n",
     "render: the fill at accept holds its constant across the event"),
    ("the step does not restart the media clock", "datapath",
     "                       | media_rebase_p_w;\n",
     "                       ;\n",
     "restart: the outgoing mr toggles exactly once"),
]


def run_leg(sources: dict[str, Path], mdir: str) -> tuple[int, str]:
    """Build and run the gmstep leg against `sources`; return (status, log)."""
    command = ["make", "gmstep", f"GMSTEP_MDIR={mdir}",
               f"DP_SRC={sources['datapath']}", f"CLKV_SRC={sources['clkv']}",
               f"RSP_SRC={sources['stage']}"]
    for name in ("VERILATOR", "VERILATOR_JOBS"):
        if name in os.environ:
            command.append(f"{name}={os.environ[name]}")
    done = subprocess.run(command, cwd=HERE, capture_output=True, text=True, check=False)
    return done.returncode, done.stdout + done.stderr


def failed_checks(log: str) -> list[str]:
    """The names of the checks the leg printed as failed."""
    return [line.split("[FAIL]", 1)[1].split(" got=")[0].strip()
            for line in log.splitlines() if "[FAIL]" in line]


def plant(base: Path, destination: Path, anchor: str, replacement: str) -> bool:
    """Copy `base` to `destination` with one defect; False if the anchor is gone."""
    text = base.read_text(encoding="utf-8")
    if text.count(anchor) != 1:
        return False
    destination.write_text(text.replace(anchor, replacement, 1), encoding="utf-8")
    return True


def campaign(datapath: Path, scratch: Path) -> int:
    """Run the clean leg, then every control; return the number of escapes."""
    clean = {"datapath": datapath, "clkv": CLKV_RTL.resolve(), "stage": STAGE_RTL.resolve()}
    status, log = run_leg(clean, "obj_gmstep_clean")
    escapes = 0 if status == 0 else 1
    print(f"[{'ok' if status == 0 else 'FAIL'}] clean leg passes (make exit {status})")
    for index, (name, source, anchor, replacement, expect) in enumerate(MUTATIONS):
        planted = scratch / f"m{index}_{clean[source].name}"
        if not plant(clean[source], planted, anchor, replacement):
            print(f"[FAIL] {name}: its anchor is not in {clean[source]}")
            escapes += 1
            continue
        status, log = run_leg({**clean, source: planted}, f"obj_gmstep_m{index}")
        broke = failed_checks(log)
        caught = status != 0 and "== gmstep: checks:" in log and expect in broke
        print(f"[{'ok' if caught else 'FAIL'}] {name}: "
              f"{'caught by' if caught else 'NOT caught by'} \"{expect}\"; broke {broke}")
        escapes += 0 if caught else 1
    return escapes


def main() -> int:
    """Parse the base datapath and run the campaign in a private directory."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--datapath", type=Path, required=True,
                        help="the milan_datapath.sv the leg passes on")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="gmstep-mutants-") as directory:
        escapes = campaign(args.datapath.resolve(), Path(directory))
    for index in range(len(MUTATIONS)):
        shutil.rmtree(HERE / f"obj_gmstep_m{index}", ignore_errors=True)
    print(f"controls: {len(MUTATIONS)}   escapes: {escapes}")
    print(f"RESULT: {'PASS' if escapes == 0 else 'FAIL'}")
    return 1 if escapes else 0


if __name__ == "__main__":
    sys.exit(main())
