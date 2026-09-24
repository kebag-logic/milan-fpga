#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Negative controls and start-phase sweep for the #387 gmstep leg.

sim_gmstep.cpp grades a grandmaster change that steps the PHC by 1.5 s under
CRF selection: tu on the commit edge and a holdover after the step, the talker
streaming to the end of the window, the listener locked, one counted render
re-base and one mr toggle landing right after the step, MEDIA_RESET unmoved
between the commit and the step and one after it, and the render law graded
where the stage states it (the fill right after every PDU push).

Two campaigns, both against a base datapath given as an argument (the one the
leg passes on is the #387 edit; until it lands in the tree the caller passes a
copy of the tree's datapath with that edit applied):

  --sweep A-B     build the clean leg once and run it at every feed delay A..B
                  (fabric cycles idled before the peer's media feed starts,
                  the leg's optional second argument). One media tick is
                  41.67 cycles at 2 MHz, so 0-41 covers every accept phase.
                  Every run must pass.
  --controls D,.. plant each defect below into a private copy of the source
                  that carries the property (the clock-validity block, the
                  render stage or the datapath), build the SAME leg through
                  the Makefile's own recipe (`make gmstep-build` with
                  CLKV_SRC, RSP_SRC or DP_SRC and GMSTEP_MDIR overridden) and
                  run it at every listed feed delay. Each run must FAIL by the
                  leg's own verdict with every named check among its
                  failures; a crash or an abort is not a catch.

The leg is cycle-bounded by construction, so this driver sets no host-time
deadline. Builds run one at a time with VERILATOR_JOBS; runs go --jobs at a
time. Run from tb/verilator/milan_dp. Exit 0 only when every run is as
required.
"""

import argparse
import concurrent.futures
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path.cwd()
CLKV_RTL = HERE / "../../../hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv"
STAGE_RTL = HERE / "../../../hdl/ieee1722/aaf/KL_render_setpoint.sv"

#: the AAF packetizer silenced for good once tu clears the second time since
#: reset (the first is acquisition, the second is after the change); the gate
#: register still reads open
TALKER_DIES = [
    ("assign aaf_stream_en_w = aaf_stream_en_raw_w & ~amap_edit_out_resv_r;\n",
     "assign aaf_stream_en_w = aaf_stream_en_raw_w & ~amap_edit_out_resv_r;\n"
     "  logic       probe_tu_q_r;\n"
     "  logic [1:0] probe_falls_r;\n"
     "  logic       probe_dead_r;\n"
     "  always_ff @(posedge axis_clk) begin : probe_dead\n"
     "    if (!axis_resetn) begin\n"
     "      probe_tu_q_r  <= 1'b1;\n"
     "      probe_falls_r <= 2'd0;\n"
     "      probe_dead_r  <= 1'b0;\n"
     "    end else begin\n"
     "      probe_tu_q_r <= clkv_tu_w;\n"
     "      if (probe_tu_q_r && !clkv_tu_w && probe_falls_r != 2'd3)\n"
     "        probe_falls_r <= probe_falls_r + 2'd1;\n"
     "      if (probe_falls_r == 2'd2) probe_dead_r <= 1'b1;\n"
     "    end\n"
     "  end : probe_dead\n"),
    ("    .stream_en_i (aaf_stream_en_w),\n",
     "    .stream_en_i (aaf_stream_en_w & ~{N_STREAMS{probe_dead_r}}),\n"),
]

#: (name, source, [(anchor, replacement)], the checks this defect must break)
MUTATIONS = [
    ("tu reaches the talkers four cycles late", "clkv",
     [("  assign ts_uncertain_o = (~sync_ok_w) | hold_w | disc_p_w;\n",
       "  logic [3:0] tu_late_r;\n"
       "  always_ff @(posedge clk_i) begin : p_tu_late\n"
       "    tu_late_r <= {tu_late_r[2:0], (~sync_ok_w) | hold_w | disc_p_w};\n"
       "  end : p_tu_late\n"
       "  assign ts_uncertain_o = tu_late_r[3];\n")],
     ["tu: set in the first cycle the bank names GM B"]),
    ("the plane's step does not re-arm the holdover", "datapath",
     [("                   ? gptp_step_we_w : cfg_ptp_cmd_adjust),",
       "                   ? 1'b0 : cfg_ptp_cmd_adjust),")],
     ["tu: held at least the 0.25 s holdover after the step"]),
    ("tu stops the talker", "datapath",
     [("assign aaf_stream_en_w = aaf_stream_en_raw_w & ~amap_edit_out_resv_r;",
       "assign aaf_stream_en_w = aaf_stream_en_raw_w & ~amap_edit_out_resv_r & ~clkv_tu_w;")],
     ["licence: the talker never pauses beyond four of its intervals"]),
    ("the talker falls silent for good once tu clears after the change", "datapath",
     TALKER_DIES,
     ["licence: the talker never pauses beyond four of its intervals",
      "licence: the talker keeps its baseline rate within 1%",
      "tu: talker PDUs graded after tu clears"]),
    ("the Stream Input counters answer nothing valid", "datapath",
     [("  wire ctr_sin_w = (ctrq_type_r == DESC_STREAM_INPUT_C)\n"
       "                && (ctrq_index_r < 16'(N_STREAMS));",
       "  wire ctr_sin_w = 1'b0;")],
     ["licence: both Stream Input answers carry MEDIA_UNLOCKED and FRAMES_RX"]),
    ("the step does not re-centre the render stage", "datapath",
     [("       media_rebase_p_w | src_recentre_p_r;", "       src_recentre_p_r;")],
     ["render: the GM change is one counted re-base event"]),
    ("the identity change re-centres as well as the step", "datapath",
     [("       media_rebase_p_w | src_recentre_p_r;",
       "       gm_recentre_p_r | media_rebase_p_w | src_recentre_p_r;")],
     ["render: the GM change is one counted re-base event",
      "render: every counted re-base lands at a PDU end right after the step"]),
    ("the re-base is keyed to the grandmaster identity, not the step", "datapath",
     [("  wire media_rebase_p_w = eff_ptp_adjust_w | cfg_ptp_cmd_load;",
       "  wire media_rebase_p_w = gm_recentre_p_r | cfg_ptp_cmd_load;")],
     ["render: every counted re-base lands at a PDU end right after the step",
      "restart: every mr toggle is first sent right after the step",
      "restart: MEDIA_RESET does not move between the commit and the step"]),
    ("the step's recentre snaps one event off the setpoint", "stage",
     [("                rptr_r[s]    <= snap_rptr_w;\n"
       "                prefill_r[s] <= 1'b0;\n",
       "                rptr_r[s]    <= prefill_r[s] ? snap_rptr_w : snap_rptr_w - 1'b1;\n"
       "                prefill_r[s] <= 1'b0;\n")],
     ["render: every PDU push leaves the target fill across the event"]),
    ("the step does not restart the media clock", "datapath",
     [("                       | media_rebase_p_w;\n", "                       ;\n")],
     ["restart: the outgoing mr toggles exactly once",
      "restart: the talker's MEDIA_RESET counts exactly one"]),
]


def build(sources: dict[str, Path], mdir: str) -> tuple[int, str]:
    """Build the gmstep leg against `sources` into `mdir`; return (status, log)."""
    command = ["make", "gmstep-build", f"GMSTEP_MDIR={mdir}",
               f"DP_SRC={sources['datapath']}", f"CLKV_SRC={sources['clkv']}",
               f"RSP_SRC={sources['stage']}"]
    for name in ("VERILATOR", "VERILATOR_JOBS"):
        if name in os.environ:
            command.append(f"{name}={os.environ[name]}")
    done = subprocess.run(command, cwd=HERE, capture_output=True, text=True, check=False,
                          env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    return done.returncode, done.stdout + done.stderr


def run_leg(mdir: str, delay: int) -> tuple[int, str]:
    """Run a built leg at one feed delay; return (status, log)."""
    done = subprocess.run([f"./{mdir}/Vmilan_dp_gmstep", f"{mdir}/aemi.bin", str(delay)],
                          cwd=HERE, capture_output=True, text=True, check=False)
    return done.returncode, done.stdout + done.stderr


def failed_checks(log: str) -> list[str]:
    """The names of the checks the leg printed as failed."""
    return [line.split("[FAIL]", 1)[1].split(" got=")[0].strip()
            for line in log.splitlines() if "[FAIL]" in line]


def tally(log: str) -> str:
    """The leg's own summary line, or a marker when it has none."""
    lines = [line for line in log.splitlines() if line.startswith("== gmstep: checks:")]
    return lines[0] if lines else "NO VERDICT"


def plant(base: Path, destination: Path, edits: list[tuple[str, str]]) -> bool:
    """Copy `base` to `destination` with every edit; False if an anchor is not unique."""
    text = base.read_text(encoding="utf-8")
    for anchor, replacement in edits:
        if text.count(anchor) != 1:
            return False
        text = text.replace(anchor, replacement, 1)
    destination.write_text(text, encoding="utf-8")
    return True


def sweep(clean: dict[str, Path], delays: list[int], jobs: int, logs: Path) -> int:
    """Run the clean leg at every delay; return the number of failing runs."""
    status, log = build(clean, "obj_gmstep_sweep")
    (logs / "sweep-build.log").write_text(log, encoding="utf-8")
    if status != 0:
        print(f"[FAIL] clean build (make exit {status})")
        return 1
    bad = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(lambda d: (d, *run_leg("obj_gmstep_sweep", d)), delays))
    for delay, status, log in results:
        (logs / f"sweep-{delay}.log").write_text(log, encoding="utf-8")
        ok = status == 0 and "RESULT: PASS" in log
        bad += 0 if ok else 1
        render = [line for line in log.splitlines() if line.startswith("RENDER: fill after")]
        print(f"[{'ok' if ok else 'FAIL'}] clean leg, feed delay {delay}: {tally(log)}; "
              f"failed {failed_checks(log)}; {render[0] if render else ''}")
    shutil.rmtree(HERE / "obj_gmstep_sweep", ignore_errors=True)
    print(f"sweep: {len(delays)} delays   failing: {bad}")
    return bad


def controls(clean: dict[str, Path], delays: list[int], jobs: int, logs: Path,
             scratch: Path) -> int:
    """Build every control once, run each at every delay; return the escapes."""
    escapes = 0
    built = []
    for index, (name, source, edits, expect) in enumerate(MUTATIONS):
        planted = scratch / f"m{index}_{clean[source].name}"
        if not plant(clean[source], planted, edits):
            print(f"[FAIL] {name}: an anchor is not unique in {clean[source]}")
            escapes += 1
            continue
        mdir = f"obj_gmstep_m{index}"
        status, log = build({**clean, source: planted}, mdir)
        (logs / f"control-{index}-build.log").write_text(log, encoding="utf-8")
        if status != 0:
            print(f"[FAIL] {name}: the control does not build (make exit {status})")
            escapes += 1
            continue
        built.append((index, name, expect, mdir))
    runs = [(entry, delay) for entry in built for delay in delays]
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(lambda job: (job, *run_leg(job[0][3], job[1])), runs))
    for ((index, name, expect, _), delay), status, log in results:
        (logs / f"control-{index}-delay-{delay}.log").write_text(log, encoding="utf-8")
        broke = failed_checks(log)
        missing = [check for check in expect if check not in broke]
        caught = status != 0 and "== gmstep: checks:" in log and not missing
        escapes += 0 if caught else 1
        print(f"[{'ok' if caught else 'FAIL'}] {name}, feed delay {delay}: "
              f"{'caught by' if caught else 'NOT caught by'} {expect}; {tally(log)}; "
              f"broke {broke}")
    for _, _, _, mdir in built:
        shutil.rmtree(HERE / mdir, ignore_errors=True)
    print(f"controls: {len(MUTATIONS)} x {len(delays)} delays   escapes: {escapes}")
    return escapes


def delay_list(text: str) -> list[int]:
    """Parse 'A-B' or 'A,B,C' into feed delays."""
    if "-" in text:
        first, last = (int(part) for part in text.split("-", 1))
        return list(range(first, last + 1))
    return [int(part) for part in text.split(",")]


def main() -> int:
    """Parse the base datapath and the campaigns, then run them."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--datapath", type=Path, required=True,
                        help="the milan_datapath.sv the leg passes on")
    parser.add_argument("--sweep", type=delay_list, help="feed delays for the clean leg")
    parser.add_argument("--controls", type=delay_list, help="feed delays for every control")
    parser.add_argument("--jobs", type=int, default=8, help="legs run at once (<= 8)")
    parser.add_argument("--logs", type=Path, required=True, help="directory for every log")
    args = parser.parse_args()
    if not 1 <= args.jobs <= 8:
        parser.error("--jobs must be 1..8")
    if not args.sweep and not args.controls:
        parser.error("name --sweep, --controls or both")
    args.logs.mkdir(parents=True, exist_ok=True)
    clean = {"datapath": args.datapath.resolve(), "clkv": CLKV_RTL.resolve(),
             "stage": STAGE_RTL.resolve()}
    bad = 0
    if args.sweep:
        bad += sweep(clean, args.sweep, args.jobs, args.logs.resolve())
    if args.controls:
        with tempfile.TemporaryDirectory(prefix="gmstep-mutants-") as directory:
            bad += controls(clean, args.controls, args.jobs, args.logs.resolve(),
                            Path(directory))
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
