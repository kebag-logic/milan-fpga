#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Check verbatim settle control at every shipping and diagnostic axis rate.

This is a controller test with one media tick per stimulus edge, not a
physical-clock simulation. It checks quiet noise, action count, interrupted
recovery dwell, a new pull after recovery, reset, source-change priority,
disengaged INTERNAL dwell, the LOCKED dwell and the independent ceiling.
The physical follow_ring campaigns separately establish the measured band.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess

RATES = (6250000, 25000000, 50000000, 100000000)
HEADER = """module settle_control;
logic axis_clk=0, axis_resetn=0;
logic [15:0] media_clk_src_r=0;
logic follow_sel_r=0, mga_engaged_w=0, mcsrv_locked_w=0;
logic signed [15:0] mga_err_w=0;
logic media_tick_p=1;
logic settle_recentre_p_r;
localparam int unsigned MILAN_CLK_FREQ_HZ=AXIS_RATE;
localparam int unsigned MCSRV_WIN_LOG2_C=9;
"""
DRIVER = """
integer actions=0;
task tick;
  #1; axis_clk=1; #1;
  if (settle_recentre_p_r) actions++;
  axis_clk=0; #1;
endtask
task reset_control;
  axis_resetn=0; tick(); axis_resetn=1;
  if (settle_pend_r || settle_recover_r || settle_recentre_p_r)
    $fatal(1, "reset did not clear control");
endtask
task wait_action(input integer limit);
  integer before_count;
  before_count=actions;
  for (integer i=0; i<limit && actions==before_count; i++) tick();
  if (actions!=before_count+1) $fatal(1, "missing one bounded action");
endtask
initial begin
  reset_control();
  mga_engaged_w=1; tick(); wait_action(2050);
  repeat (2050) tick();
  if (settle_recover_r) $fatal(1, "quiet did not re-arm");
  // Quantisation noise must never arm, not merely avoid a pulse.
  for (integer i=0; i<8192; i++) begin
    mga_err_w=(i % 2) ? 16'sd1 : -16'sd1; tick();
    if (settle_pend_r) $fatal(1, "quiet noise armed");
  end
  // Three cycles exceeds the same two-cycle quiet band at every rate.
  mga_err_w=3; tick();
  if (!settle_pend_r) $fatal(1, "excursion did not arm");
  mga_err_w=0; wait_action(2050);
  begin
    integer before_count;
    before_count=actions;
    mga_err_w=-9; repeat (4096) tick();
    if (!settle_recover_r || settle_pend_r || actions!=before_count)
      $fatal(1, "own recovery armed a second action");
    mga_err_w=0; repeat (2047) tick();
    if (!settle_recover_r) $fatal(1, "re-armed before quiet dwell");
    mga_err_w=3; tick();
    mga_err_w=0; repeat (2047) tick();
    if (!settle_recover_r) $fatal(1, "excursion failed to restart recovery dwell");
    repeat (3) tick();
    if (settle_recover_r || actions!=before_count) $fatal(1, "quiet dwell failed");
  end
  mga_err_w=-9; tick();
  if (!settle_pend_r) $fatal(1, "pull outside recovery did not arm");
  mga_err_w=0; wait_action(2050);
  // A new source selection overrides recovery; following still waits 8 windows.
  media_clk_src_r=1; follow_sel_r=1; mcsrv_locked_w=1; tick();
  begin
    integer before_count;
    before_count=actions;
    repeat (196607) tick();
    if (actions!=before_count) $fatal(1, "following acted before eight windows");
    wait_action(3);
  end
  // Reset during recovery and while pending both clear the new state.
  reset_control();
  media_clk_src_r=2; mcsrv_locked_w=0; tick(); reset_control();
  tick(); wait_action(1048578);
  // INTERNAL without an engaged aligner still owes its 2048-tick dwell.
  media_clk_src_r=0; follow_sel_r=0; mga_engaged_w=0; tick();
  begin
    integer before_count;
    before_count=actions;
    repeat (2047) tick();
    if (actions!=before_count) $fatal(1, "disengaged INTERNAL acted without dwell");
    wait_action(3);
  end
  $display("SETTLE CONTROL PASS: axis_hz=%0d actions=%0d", MILAN_CLK_FREQ_HZ, actions);
  $finish;
end
endmodule
"""


def run(rate: int, source: str, out: Path, simulator: str) -> int:
    """Compile and run one exact controller with independent expected values."""
    work = out / str(rate)
    work.mkdir(parents=True, exist_ok=True)
    (work / "settle_control.sv").write_text(HEADER.replace("AXIS_RATE", str(rate)) + source + DRIVER)
    commands = [
        [simulator, "--binary", "--timing", "-j", "16", "-Wno-fatal", "--top-module",
         "settle_control", "settle_control.sv"],
        [str(work / "obj_dir/Vsettle_control")],
    ]
    for name, argv in zip(("build", "run"), commands):
        (work / f"{name}.command.json").write_text(json.dumps(argv) + "\n")
        with (work / f"{name}.log").open("w") as log:
            rc = subprocess.run(argv, cwd=work, stdout=log, stderr=subprocess.STDOUT, check=False).returncode
        (work / f"{name}.rc").write_text(f"{rc}\n")
        if rc:
            return rc
    print(f"settle control {rate} Hz: PASS", flush=True)
    return 0


def main() -> int:
    """Extract the live controller and exercise the four axis-clock units."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sim", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=2)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    text = (root / "hdl/milan/milan_datapath.sv").read_text()
    begin = text.index("  localparam int unsigned SRC_SETTLE_ERR_C")
    end = text.index("  end : g_settle_recentre", begin) + len("  end : g_settle_recentre")
    source = text[begin:end]
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda rate: run(rate, source, args.out.resolve(), args.sim), RATES))
    return int(any(results))


if __name__ == "__main__":
    raise SystemExit(main())
