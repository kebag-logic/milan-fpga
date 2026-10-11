#!/usr/bin/env python3
# R603-3 disposable probe: plant one writer defect into a COPY of the shipping
# firmware text and grade it with the head's own checks 13 and 14 (and, with
# --all, checks 1 to 14). Never edits the checkout; builds under WORK.
#
# usage: probe_plants.py ROOT WORK LABEL CONFIG [--jobs N] [--all]
#   ROOT    the review checkout (exact head)
#   WORK    an empty scratch directory
#   LABEL   one key of PLANTS below, or "none" for the unplanted control
#   CONFIG  a configs/endstation_*.yaml path
from __future__ import annotations

import argparse
import sys
from dataclasses import replace
from pathlib import Path

#: label -> ((text that must occur exactly once, replacement), ...), why
PLANTS = {
    "none": ((), "unplanted control: the head must grade clean"),
    # the re-stage retries once more than the stated three
    "p_restage_four_tries": (
        (("\tfor (n = 0; n < NVM_READ_TRIES; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
          "\t\tif (rd.vd == VD_OK && rd.seq == seq)",
          "\tfor (n = 0; n < NVM_READ_TRIES + 1u; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
          "\t\tif (rd.vd == VD_OK && rd.seq == seq)"),),
        "re-stage bound 3 -> 4"),
    # the re-stage has no bound at all
    "p_restage_unbounded": (
        (("\tfor (n = 0; n < NVM_READ_TRIES; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
          "\t\tif (rd.vd == VD_OK && rd.seq == seq)",
          "\tfor (n = 0; n < 0xFFFFFFFFu; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
          "\t\tif (rd.vd == VD_OK && rd.seq == seq)"),),
        "re-stage bound removed"),
    # a judgement with no standing verdict is not marked UNREAD
    "p_judge_no_unread": (
        (("\tnvm_unread |= (slot == NVM_SLOT_A) ? 1u : 2u;\n\trd.vd = VD_LEN;",
          "\trd.vd = VD_LEN;"),),
        "judge: no unread bit"),
    # the hold stops commits but keeps answering the liveness deadline
    "p_held_heartbeats": (
        (("\tnvm_retired = 1;\n\tnvm_held = 1;", "\tnvm_held = 1;"),),
        "held writer keeps heartbeating"),
    # the sequence re-read from flash after the judgement (pre-#671 shape)
    "p_seq_from_flash": (
        (("\t\trd.seq = nvm_seq_of(NVM_STG);", "\t\trd.seq = nvm_seq_of(nvm_slot(slot));"),),
        "sequence from a fresh flash read"),
    # the third read compared with the first only
    "p_judge_ignores_second": (
        (("(n >= 1u && nvm_reads_agree(first, rd)) ||\n\t\t    (n >= 2u && nvm_reads_agree(second, rd)))",
          "(n >= 1u && nvm_reads_agree(first, rd)) ||\n\t\t    (n >= 2u && second.vd == 0xFFFFu))"),),
        "judge: third read never compared with the second"),
    # the hold applies only when both slots are unread
    "p_hold_only_both": (
        (("\tif (!nvm_unread) {\n\t\tnvm_ready = 1;", "\tif (nvm_unread != 3u) {\n\t\tnvm_ready = 1;"),),
        "hold only when both slots unread"),
    # the re-stage gives up one try early
    "p_restage_two_tries": (
        (("\tfor (n = 0; n < NVM_READ_TRIES; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
          "\t\tif (rd.vd == VD_OK && rd.seq == seq)",
          "\tfor (n = 0; n < NVM_READ_TRIES - 1u; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
          "\t\tif (rd.vd == VD_OK && rd.seq == seq)"),),
        "re-stage bound 3 -> 2"),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("label")
    ap.add_argument("config", type=Path)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    sys.path.insert(0, str(a.root / "sw/firmware/nvm_hosttest"))
    import test_nvm_firmware as t  # noqa: E402  (the head's own checks)

    text = (a.root / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text()
    pairs, why = PLANTS[a.label]
    for old, new in pairs:
        n = text.count(old)
        if n != 1:
            print(f"PLANT-MISMATCH {a.label}: anchor occurs {n} times")
            return 3
        text = text.replace(old, new)
    a.work.mkdir(parents=True, exist_ok=False)
    bench = replace(t.make_bench(a.config, a.work, text), jobs=max(1, a.jobs))
    grades = t.GRADES if a.all else t.READ_FAULT_GRADES
    got = t.grade(bench, grades)
    print(f"PROBE {a.label} ({why}) on {a.config.stem}: {len(got)} finding(s)")
    for x in got[:12]:
        print(f"  FINDING: {x}")
    print("VERDICT", "CAUGHT" if got else "NOT-CAUGHT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
