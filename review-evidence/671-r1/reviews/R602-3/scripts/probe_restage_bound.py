#!/usr/bin/env python3
"""R602-3 demonstrator: is the re-stage retry bound pinned by check 13?

Usage: probe_restage_bound.py TREE OUTDIR CFG_STEM

Builds the head firmware and two plants of nvm_restage()'s loop bound
(four tries; no practical bound) into the head's host harness, then:
  1. counts check 13's own cases in which the picked slot's re-stage meets
     more than NVM_READ_TRIES consecutive faulty reads (the only cases that
     could see the re-stage bound);
  2. grades, with the head's own grade_fault_case(), extra cases that are
     NOT in check 13: a fault starting after the judgement reads and lasting
     past the bound, on the picked slot, cold boot and writer restart.
Prints one line per (firmware, case) with the findings.
"""
import sys
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
STEM = sys.argv[3]
sys.path.insert(0, str(TREE / "sw/firmware/nvm_hosttest"))

import tempfile                                   # noqa: E402

import read_fault_cases as RF                     # noqa: E402
import test_nvm_firmware as T                     # noqa: E402

LOOP = ("\tfor (n = 0; n < NVM_READ_TRIES; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
        "\t\tif (rd.vd == VD_OK && rd.seq == seq)")
PLANTS = {
    "head": None,
    "restage_four_tries": LOOP.replace("n < NVM_READ_TRIES;", "n < NVM_READ_TRIES + 1u;"),
    "restage_unbounded": LOOP.replace("n < NVM_READ_TRIES;", "n != 0xffffffffu;"),
}
EXTRA = [
    # both valid, A newer: A's judgement read (read 1) clean, every later A read faulty
    RF.FaultCase("a", True, 0x5A5A5, ("--read-fault", "a:0:3:64"), 3, 64),
    RF.FaultCase("b", True, 0x5A5A5, ("--read-fault", "b:0:3:64"), 3, 64),
    # A valid, B blank: A judged at read 1, B at reads 2-3, A's re-stage from read 4
    RF.FaultCase("a", False, 0x5A5A5, ("--read-fault", "a:0:4:64"), 4, 64),
    # the writer restart (reads counted from the restart): A newer, judged at
    # read 0, B at read 1, A's re-stage from read 2
    RF.FaultCase("a", True, 0x5A5A5, ("--read-fault", "a:0:2:64"), 2, 64, True),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    head = T.FIRMWARE.read_text()
    assert head.count(LOOP) == 1
    cfg = TREE / "configs" / f"{STEM}.yaml"
    cases = RF.fault_cases(0)
    long_restage = [c for c in cases if c.count > RF.READ_TRIES and (c.skip, c.count) != RF.WHOLE]
    print(f"check 13 cases: {len(cases)}; cases faulting more than {RF.READ_TRIES} consecutive "
          f"reads that do not also fault the judgement (skip>0): {len(long_restage)}")
    with tempfile.TemporaryDirectory(prefix="r602bound.", dir=str(OUT)) as tmp:
        for label, loop in PLANTS.items():
            text = head if loop is None else head.replace(LOOP, loop)
            work = Path(tmp) / label
            work.mkdir()
            bench = T.make_bench(cfg, work, text)
            fr = T.fault_run(bench)
            for i, case in enumerate(EXTRA):
                w = work / f"c{i}"
                w.mkdir()
                got = T.grade_fault_case(bench, fr, case, w)
                print(f"{label:<20} {STEM:<26} {case.name}: findings={len(got)}"
                      + "".join(f"\n    - {g[:260]}" for g in got[:3]), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
