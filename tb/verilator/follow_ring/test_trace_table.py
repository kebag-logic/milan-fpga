#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Exercise the diagnostic CLI with independent counter/pulse event fixtures.

Run with python3 -B tb/verilator/follow_ring/test_trace_table.py.
The four-tick step is the review's passing recentre counterexample. A real
slip at that same instant must remain visible, even with no margin change.
"""

import csv
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class TraceTableTests(unittest.TestCase):
    """Grade the printed CSV contract, not implementation helper functions."""

    def table(self, events: str, complete: bool = True) -> list[dict[str, str]]:
        """Run the actual CLI over a margin step and supplied event records."""
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            log = "info: t=1.000000 s  CLOCK_SOURCE <- 1\n" + events
            if complete:
                log += "RING-EVENTS: complete through 2.000000000 s\n"
            (work / "run.log").write_text(log)
            (work / "pdu.csv").write_text(
                "arrive_s,ring_margin_ticks,render_fill,render_delay_ticks\n"
                "1.000,1.3,14,8.5\n1.599,1.3,14,8.5\n"
                "1.600,5.3,14,8.5\n1.900,5.3,14,8.5\n")
            (work / "servo.csv").write_text(
                "t_s,state,pi_run,ew_ns,trim_ppm,meter_valid\n"
                "1.0,4,1,0,0.0,1\n")
            argv = [sys.executable, "-B", str(Path(__file__).with_name("trace_table.py")),
                    str(work / "run.log"), str(work / "pdu.csv"), str(work / "servo.csv"),
                    "--from-s", "0", "--to-s", "1", "--step-s", "0.25",
                    "--csv", str(work / "table.csv")]
            result = subprocess.run(argv, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            with (work / "table.csv").open() as fh:
                return list(csv.DictReader(fh))

    def test_declared_action_is_not_a_slip(self) -> None:
        """A four-tick recentre changes margins without moving slip counters."""
        rows = self.table("RING-EVENT: recentre 1.600000000\n")
        self.assertEqual([r["slips"] for r in rows], ["0"] * 4)
        self.assertEqual([r["recentres"] for r in rows], ["0", "0", "1", "0"])
        self.assertEqual(rows[2]["ring_margin_ticks"], "+1.300..+5.300")
        self.assertTrue(all(r["event_trace"] == "complete" for r in rows))

    def test_duplicate_during_recentre_is_counted(self) -> None:
        """The declared pulse grants no exclusion window to a true duplicate."""
        rows = self.table("RING-EVENT: recentre 1.600000000\n"
                          "RING-EVENT: dup 1.600000000\n")
        self.assertEqual(rows[2]["slips"], "1")
        self.assertEqual(rows[2]["skips"], "0")
        self.assertEqual(rows[2]["recentres"], "1")

    def test_skip_with_flat_margin_is_counted(self) -> None:
        """A genuine skip is observable without a positive margin jump."""
        rows = self.table("RING-EVENT: skip 1.800000000\n")
        self.assertEqual(rows[3]["slips"], "1")
        self.assertEqual(rows[3]["skips"], "1")
        self.assertEqual(rows[3]["recentres"], "0")

    def test_bins_count_all_events_and_exclude_end(self) -> None:
        """Counter events use half-open bins, even without a PDU in that bin."""
        rows = self.table("RING-EVENT: dup 0.999000000\n"
                          "RING-EVENT: dup 1.250000000\n"
                          "RING-EVENT: skip 1.250000000\n"
                          "RING-EVENT: recentre 1.250000000\n"
                          "RING-EVENT: dup 2.000000000\n")
        self.assertEqual([r["slips"] for r in rows], ["0", "2", "0", "0"])
        self.assertEqual(rows[1]["skips"], "1")
        self.assertEqual(rows[1]["recentres"], "1")

    def test_legacy_probe_does_not_infer_slips(self) -> None:
        """Old margin-only traces cannot establish a measured slip count."""
        rows = self.table("", complete=False)
        self.assertEqual([r["slips"] for r in rows], ["0"] * 4)
        self.assertTrue(all(r["event_trace"] == "unavailable" for r in rows))


if __name__ == "__main__":
    unittest.main()
