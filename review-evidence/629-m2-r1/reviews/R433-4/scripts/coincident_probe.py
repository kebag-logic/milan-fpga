#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe (R433-4) of F-A512-1 through gmstep_mutants.py's own run_control.

Usage: coincident_probe.py <disposable checkout of the head>

Plants, each in its own work directory and in parallel, three reviewer-written
variants of "a PHC step suppresses a coincident CRF restart" on the gmstep leg:
  V1  the veto on the whole selected-CRF group (a different text from the
      campaign's control, the same defect): must be CAUGHT by the named check;
  V2  round 4's published form (the veto ANDed onto the request's last line,
      binding to the AAF toggle alone): expected to SURVIVE, the disarming;
  V3  the veto on the received-toggle term only (informational: which CRF
      restart cause the coincident check exercises).
Nothing is written to the checkout's tracked files; build products go to a
temporary directory.
"""
import multiprocessing
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve() / "tb/verilator/milan_dp"))
import gmstep_mutants as g  # noqa: E402

NAMED = "coincident: a PHC step does not suppress the CRF restart"
VARIANTS = [
    ("V1 whole selected-CRF group vetoed", "       (crf_clk_selected_r\n",
     "       (crf_clk_selected_r & ~media_rebase_p_w\n", "caught"),
    ("V2 round-4 form: veto ANDed onto the last line", g.RESTART_TRIGGER,
     g.RESTART_TRIGGER[:-1] + " & ~media_rebase_p_w;", "survives"),
    ("V3 veto on the received-toggle term only", "| crf_mr_toggle_p_w))",
     "| (crf_mr_toggle_p_w & ~media_rebase_p_w)))", "informational"),
]


def one(tag: int, root: Path) -> tuple[str, bool, str]:
    """Plant variant `tag` in its own process (stdout capture is per process)."""
    name, anchor, rep, expect = VARIANTS[tag]
    control = g.Control(name, "datapath", anchor, rep, NAMED, False)
    work = root / f"v{tag}"
    work.mkdir()
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        caught = g.run_control(control, work, 100 + tag)
    return name, caught, expect + "\n" + buf.getvalue()


def main() -> int:
    """Plant the variants in parallel; 1 if any result is unexpected."""
    with tempfile.TemporaryDirectory(prefix="r433-4-coincident-") as td:
        with ProcessPoolExecutor(max_workers=3, mp_context=multiprocessing.get_context("fork")) as pool:
            results = list(pool.map(one, range(len(VARIANTS)), [Path(td)] * len(VARIANTS)))
    bad = 0
    for name, caught, text in results:
        expect, _, log = text.partition("\n")
        ok = (expect == "caught" and caught) or (expect == "survives" and not caught) or expect == "informational"
        bad += 0 if ok else 1
        print(f"== {name}: {'CAUGHT' if caught else 'NOT CAUGHT'} (expected {expect}) -> {'OK' if ok else 'UNEXPECTED'}")
        print(log.rstrip())
    print(f"probe: {len(results) - bad}/{len(results)} as expected")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
