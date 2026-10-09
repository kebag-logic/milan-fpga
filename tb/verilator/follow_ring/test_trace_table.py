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

    def table(self, events: str, complete: bool = True, *,
              options: tuple[str, ...] = (), pdus: str | None = None,
              servo: str | None = None) -> list[dict[str, str]]:
        """Run the actual CLI over a margin step and supplied event records."""
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            log = "info: t=1.000000 s  CLOCK_SOURCE <- 1\n" + events
            if complete:
                log += "RING-EVENTS: complete through 2.000000000 s\n"
            (work / "run.log").write_text(log)
            (work / "pdu.csv").write_text(
                "arrive_s,ring_margin_ticks,render_fill,render_delay_ticks\n" +
                (pdus if pdus is not None else
                 "1.000,1.3,14,8.5\n1.599,1.3,14,8.5\n"
                 "1.600,5.3,14,8.5\n1.900,5.3,14,8.5\n"))
            (work / "servo.csv").write_text(
                "t_s,state,pi_run,ew_ns,trim_ppm,meter_valid\n" +
                (servo if servo is not None else "1.0,4,1,0,0.0,1\n"))
            argv = [sys.executable, "-B", str(Path(__file__).with_name("trace_table.py")),
                    str(work / "run.log"), str(work / "pdu.csv"), str(work / "servo.csv"),
                    "--from-s", "0", "--to-s", "1", "--step-s", "0.25",
                    "--csv", str(work / "table.csv"), *options]
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


    def test_decimal_boundaries_for_events_and_pdus(self) -> None:
        """Both inputs include the start, exclude the end, and own each edge."""
        cases = (
            ("interior", "1", "0", ".4",
             ("1.199999999", "1.2", "1.200000001"),
             (1, 2, 2), ("+0.10", "+0.20", "+0.30", "+0.40")),
            ("start", ".1", ".2", ".4",
             (".299999999", ".3", ".300000001"),
             (None, 0, 0), ("+0.30", "+0.40")),
            ("end", ".1", "0", ".2",
             (".299999999", ".3", ".300000001"),
             (1, None, None), ("+0.10", "+0.20")),
        )
        for name, origin, start, end, times, owners, labels in cases:
            for kind in ("dup", "skip", "recentre"):
                for instant, owner in zip(times, owners):
                    with self.subTest(case=name, kind=kind, instant=instant):
                        rows = self.table(
                            f"RING-EVENT: {kind} {instant}\n",
                            options=("--origin-s", origin, "--from-s", start,
                                     "--to-s", end, "--step-s", ".1"),
                            pdus=f"{instant},5.3,14,8.5\n")
                        self.assertEqual(tuple(r["t_s"] for r in rows), labels)
                        for i, row in enumerate(rows):
                            present = i == owner
                            for column, counted in (("slips", kind != "recentre"),
                                                    ("skips", kind == "skip"),
                                                    ("recentres", kind == "recentre")):
                                self.assertEqual(row[column], str(int(present and counted)))
                            for column, value in (("ring_margin_ticks", "+5.300..+5.300"),
                                                  ("render_fill", "14..14"),
                                                  ("render_delay_ticks", "8.500..8.500")):
                                self.assertEqual(row[column], value if present else "-")
                            self.assertEqual(row["event_trace"], "complete")

    def test_subnanosecond_sides_remain_distinct(self) -> None:
        """No grace interval or decimal precision rounding absorbs neighbours."""
        for kind in ("dup", "skip", "recentre"):
            for instant, owner in (("1.199999999999999999999999999999", 1),
                                   ("1.2", 2),
                                   ("1.200000000000000000000000000001", 2)):
                with self.subTest(kind=kind, instant=instant):
                    rows = self.table(
                        f"RING-EVENT: {kind} {instant}\n",
                        options=("--from-s", "0", "--to-s", ".4", "--step-s", ".1"),
                        pdus=f"{instant},5.3,14,8.5\n")
                    key = "recentres" if kind == "recentre" else "slips"
                    self.assertEqual([r[key] for r in rows],
                                     [str(int(i == owner)) for i in range(4)])
                    self.assertEqual([r["render_fill"] for r in rows],
                                     ["14..14" if i == owner else "-" for i in range(4)])

    def test_partial_last_bin_and_servo_timestamp(self) -> None:
        """A short final bin clips at the exact end; servo snapshots stay exact."""
        rows = self.table(
            "RING-EVENT: dup .299999999\nRING-EVENT: skip .3\n",
            options=("--origin-s", ".1", "--from-s", "0", "--to-s", ".2",
                     "--step-s", ".07"),
            pdus=".299999999,5.3,14,8.5\n.3,99,99,99\n",
            servo=".1,1,0,10,0.0,0\n.24,4,1,20,0.0,1\n"
                  ".240000000000000000000000000001,5,0,30,0.0,0\n"
                  ".3,2,0,40,0.0,0\n.300000001,6,0,50,0.0,0\n")
        self.assertEqual([r["t_s"] for r in rows], ["+0.07", "+0.14", "+0.20"])
        self.assertEqual([r["slips"] for r in rows], ["0", "0", "1"])
        self.assertEqual([r["skips"] for r in rows], ["0", "0", "0"])
        self.assertEqual(rows[2]["ring_margin_ticks"], "+5.300..+5.300")
        self.assertEqual([r["e_ns"] for r in rows], ["10", "20", "40"])


if __name__ == "__main__":
    unittest.main()
