#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Round R302-2 driver for the unchanged round-1 probe campaign.

Usage: VERILATOR=<verilator 5.050> python3 run_probes_r2.py <clone> <packet>

probes/run_probes.py, probes/probe_loop.cpp and probes/probe_jitter.cpp are
byte-identical to the round-1 packet (hashes in REPORT.md). This driver only:
  * points the campaign at the round-2 head (the head guard is kept);
  * promotes the connected talker_step harness expectation from INFO to FAIL
    for rx_no_detection, jump_removed, lower_bound_removed (the round-2
    assignment) and servo_ignores_valid (the harness's held-update check);
  * adds accept_edge_late and refill_short as recorded (INFO) talker rows.
Every round-1 expectation is otherwise unchanged.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "probes"))
import run_probes as rp  # noqa: E402

rp.HEAD = "d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1"
PROMOTE = {"rx_no_detection", "jump_removed", "lower_bound_removed",
           "servo_ignores_valid"}
for _name, _file, _anchor, _repl, expects in rp.MUTANTS:
    if _name in PROMOTE:
        assert expects.get("talker") == "INFO", _name
        expects["talker"] = "FAIL"
rp.MUTANTS += [
    ("accept_edge_late", rp.RX, "!w_bind_rise_w && !rate_break_w;",
     "!w_bind_rise_w;", {"disc": "FAIL", "talker": "INFO"}),
    ("refill_short", rp.RX, "hfill_r <= 9'd1;", "hfill_r <= 9'd2;",
     {"disc": "FAIL", "talker": "INFO"}),
]

if __name__ == "__main__":
    raise SystemExit(rp.main())
