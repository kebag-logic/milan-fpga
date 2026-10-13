#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Apply #726's notification gaps to the unchanged firmware mailbox path."""

import argparse
import os
import shutil
import tempfile
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "sw/firmware/ctrl/test"))
import aecp_arms  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
import fw_gtest  # noqa: E402


def mailbox_fixture(variant: str) -> str:
    """Stage the gap fixture, optionally restoring phase-sensitive bin grading."""
    fixture = (HERE / "stream_counter_f5.cpp").read_text()
    if variant == "fixed-grid":
        anchor = "result.refresh=result.count>=2 && result.max_ms<=1003 && result.tail_ms<=1003;"
        if fixture.count(anchor) != 1:
            raise RuntimeError("mailbox grid plant anchor moved")
        fixture = fixture.replace(anchor, """
    unsigned bins[5]{};
    for(const auto at:times) {
        if(at>=start_ms && at-start_ms<5000) ++bins[(at-start_ms)/1000];
    }
    result.refresh=std::all_of(std::begin(bins),std::end(bins),[](unsigned n){return n>=1;});""")
    return (ROOT / "sw/firmware/ctrl/test/test_aecp.cpp").read_text() + "\n" + fixture


def main() -> int:
    """Run mailbox gaps and, for a plant, require detection then omission escape."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path)
    parser.add_argument("--variant", choices=("clean", "late", "rate", "fixed-grid"), default="clean")
    parser.add_argument("--shape", type=int, choices=(1, 8), default=1)
    args = parser.parse_args()
    temporary = tempfile.TemporaryDirectory(prefix="stream-counter-f5-") if args.work is None else None
    work = args.work.resolve() if args.work else Path(temporary.name)
    work.mkdir(parents=True, exist_ok=True)
    # core_arm's test source seam selects this fixture extension; all firmware
    # inputs still come from CTRL and the existing arm builds the mailbox.
    (work / "test_aecp.cpp").write_text(mailbox_fixture(args.variant))
    aecp_arms.HERE = work
    source = CTRL
    if args.variant in ("late", "rate"):
        source = work / "firmware"
        shutil.copytree(CTRL, source, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        path = source / "aecp/aecp.c"
        text = path.read_text()
        anchor = "e->counter_at = departure_ms + 1000u;"
        if text.count(anchor) != 1:
            raise RuntimeError("counter deadline plant anchor moved")
        delay = 2000 if args.variant == "late" else 500
        path.write_text(text.replace(anchor, f"e->counter_at = departure_ms + {delay}u;"))
    tree = Tree(source, work / "build", work / "reuse", fw_gtest.Build(jobs=2))
    shape = "endstation_ax7101_1x1_tdm8" if args.shape == 1 else "endstation_ax7101_8x8"
    group = {"late": "CADENCE", "rate": "RATE", "fixed-grid": "PHASE"}.get(args.variant)
    for omitted in (None, group) if group else (None,):
        os.environ.pop("COUNTERS_OMIT_CHECK", None)
        if omitted:
            os.environ["COUNTERS_OMIT_CHECK"] = omitted
        result = aecp_arms.core_arm(tree, ROOT / "configs" / (shape + ".yaml"),
                                    mode="mailbox", selected="Mailbox.StreamCounterGaps")
        name = "escape.log" if omitted else "run.log"
        (work / name).write_text(result.log)
        if group and not omitted:
            failures = [line for line in result.log.splitlines() if "[FAIL] Mailbox." in line]
            if result.rc != 1 or not failures or any(f"[F5 {group}]" not in f for f in failures):
                raise RuntimeError(f"unattributable {args.variant}: {result.log}")
        elif result.rc:
            raise RuntimeError(result.log)
        print(f"F5 {args.shape}x{args.shape} {args.variant} {name}: rc={result.rc}")
    if temporary:
        temporary.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
