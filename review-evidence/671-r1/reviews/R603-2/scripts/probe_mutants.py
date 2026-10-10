#!/usr/bin/env python3
"""Reviewer probe (R603-2): independent writer defects planted into a copy of
the shipping firmware, graded by the PR's own checks 13 and 14 (and, with
--all-grades, checks 1 to 14). Nothing in the source tree is modified: the
planted text is compiled into a temporary bench.

Usage: probe_mutants.py REPO_ROOT [--shapes a,b] [--jobs N] [--all-grades] [--only m1,m2]
Prints one line per (mutant, shape): CAUGHT with the first finding, or SURVIVED.
Exit 0 always when the probe ran; 2 when a plant text no longer matches.
"""
from __future__ import annotations

import argparse
import sys
import tempfile
from dataclasses import replace
from pathlib import Path

PROBES = {
    # the CPU-only restart (re-attach) path goes live with a slot unread
    "p_reattach_goes_live": (
        "\t\tnvm_publish(verdict);\n\t\tnvm_go_live();\n\t\tprintf(\"Milan NVM: writer restarted",
        "\t\tnvm_publish(verdict);\n\t\tnvm_ready = 1;\n\t\tprintf(\"Milan NVM: writer restarted"),
    # the cold-boot path goes live with a slot unread (sanity, like restart_at_zero)
    "p_cold_goes_live": (
        "\t\t\tnvm_publish(verdict);\n\t\t\tnvm_go_live();",
        "\t\t\tnvm_publish(verdict);\n\t\t\tnvm_ready = 1;"),
    # a third read may only agree with the first
    "p_no_second_agreement": (
        "(n >= 1u && nvm_reads_agree(first, rd)) ||\n\t\t    (n >= 2u && nvm_reads_agree(second, rd)))",
        "(n >= 1u && nvm_reads_agree(first, rd)) ||\n\t\t    (0 && nvm_reads_agree(second, rd)))"),
    # the re-stage is tried once, not three times
    "p_restage_one_try": (
        "\tfor (n = 0; n < NVM_READ_TRIES; ++n) {\n\t\trd = nvm_read_slot(slot);\n\t\tif (rd.vd == VD_OK && rd.seq == seq)",
        "\tfor (n = 0; n < 1u; ++n) {\n\t\trd = nvm_read_slot(slot);\n\t\tif (rd.vd == VD_OK && rd.seq == seq)"),
    # a held writer keeps heartbeating, so nvm_backed stays 1
    "p_held_heartbeats": (
        "\tnvm_retired = 1;\n\tnvm_held = 1;",
        "\tnvm_held = 1;"),
    # BLANK stands on one read
    "p_blank_on_one_read": (
        "if (rd.vd == VD_OK || (n >= 1u",
        "if (rd.vd == VD_OK || rd.vd == VD_BLANK || (n >= 1u"),
    # any refusal stands on one read (the base rule over the stage)
    "p_refusal_on_one_read": (
        "if (rd.vd == VD_OK || (n >= 1u",
        "if (1 || (n >= 1u"),
    # the writer holds only when both slots are unread
    "p_hold_only_both": (
        "\tif (!nvm_unread) {\n\t\tnvm_ready = 1;",
        "\tif (nvm_unread != 3u) {\n\t\tnvm_ready = 1;"),
    # a judgement takes four reads, over the stated bound of three
    "p_judge_four_tries": (
        "\tfor (n = 0; n < NVM_READ_TRIES; ++n) {\n\t\trd = nvm_read_slot(slot);\n\t\tif (rd.vd == VD_OK ||",
        "\tfor (n = 0; n < NVM_READ_TRIES + 1u; ++n) {\n\t\trd = nvm_read_slot(slot);\n\t\tif (rd.vd == VD_OK ||"),
    # agreement ignores the byte count (informative: likely equivalent)
    "p_agree_ignores_count": (
        "a.digest == b.digest && a.bytes == b.bytes;",
        "a.digest == b.digest;"),
    # the pick is never re-staged: the window gets whatever the stage last held
    "p_restage_skipped": (
        "while (chosen != NVM_SLOT_NONE &&\n\t       !nvm_restage(",
        "while (0 && chosen != NVM_SLOT_NONE &&\n\t       !nvm_restage("),
    # a judgement that gives no standing verdict does not mark the slot UNREAD
    "p_judge_not_unread": (
        "\tnvm_unread |= (slot == NVM_SLOT_A) ? 1u : 2u;\n\trd.vd = VD_LEN;",
        "\trd.vd = VD_LEN;"),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--shapes", default="endstation_ax7101_1x1_tdm8")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--all-grades", action="store_true")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    sys.path.insert(0, str(root / "sw/firmware/nvm_hosttest"))
    import test_nvm_firmware as t  # noqa: E402

    text = t.FIRMWARE.read_text()
    assert t.FIRMWARE.resolve().is_relative_to(root), t.FIRMWARE
    labels = [x for x in a.only.split(",") if x] or list(PROBES)
    for label in labels:
        old, new = PROBES[label]
        if text.count(old) != 1:
            print(f"PLANT-MISMATCH {label}: {text.count(old)} occurrences")
            return 2
    with tempfile.TemporaryDirectory(prefix="r603probe.") as tmp:
        for shape in a.shapes.split(","):
            cfg = root / "configs" / f"{shape}.yaml"
            for label in labels:
                old, new = PROBES[label]
                work = Path(tmp) / shape / label
                work.mkdir(parents=True)
                bench = replace(t.make_bench(cfg, work, text.replace(old, new)), jobs=a.jobs)
                if a.all_grades:
                    got = t.grade(bench)
                else:
                    got = t.grade_refused_generation(bench)
                    if not got:
                        got = t.grade_read_faults(bench, until=":")
                verdict = f"CAUGHT ({len(got)} finding(s)); first: {got[0]}" if got else "SURVIVED"
                print(f"{label:<24} {shape:<28} {verdict}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
