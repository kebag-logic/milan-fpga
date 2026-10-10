#!/usr/bin/env python3
"""Reviewer probe for PR #715 (issue #671).

Grades a firmware text (the head firmware, the base firmware, or the head
with one planted defect) with the head's host read-fault checks, one shape,
and prints every finding. It never edits the checkout: plants are applied to
an in-memory copy of the firmware text, and benches are built under WORK.

usage: probe_read_fault.py REPO CONFIG WORK [--base-fw FILE] [--plant NAME]
                            [--all-grades] [--jobs N]
       with no --plant / --base-fw: every plant below plus the base firmware.
"""
import argparse
import concurrent.futures as cf
import sys
from pathlib import Path

# Each plant: every (text, replacement) pair, each text occurring exactly once
# in the head firmware.
PLANTS = {
    # restores the base go-live: an unread slot no longer holds the writer
    "r_restart_at_zero": [
        ("\t\t\tnvm_publish(verdict);\n\t\t\tnvm_go_live();\n",
         "\t\t\tnvm_publish(verdict);\n\t\t\tnvm_ready = 1;\n"),
    ],
    # judgement retries far over the bound (bounded, so the run ends)
    "r_retry_over_bound": [
        ("\tfor (n = 0; n < NVM_READ_TRIES; ++n) {\n\t\trd = nvm_read_slot(slot);\n\t\tif (rd.vd == VD_OK ||",
         "\tfor (n = 0; n < 40u * NVM_READ_TRIES; ++n) {\n\t\trd = nvm_read_slot(slot);\n\t\tif (rd.vd == VD_OK ||"),
    ],
    # the generation after no accepted slot is read straight from slot A
    "r_generation_from_flash": [
        ("\t\tnvm_seq = 0;\n\t\tverdict = (nvm_verdict_a != VD_BLANK)",
         "\t\tnvm_seq = nvm_rd32(nvm_slot(NVM_SLOT_A) + 8);\n\t\tverdict = (nvm_verdict_a != VD_BLANK)"),
    ],
    # two refusals agree by verdict and length, not by their bytes
    "r_agree_without_digest": [
        ("\treturn a.vd == b.vd && a.digest == b.digest && a.bytes == b.bytes;",
         "\treturn a.vd == b.vd && a.bytes == b.bytes;"),
    ],
    # the third read may only agree with the first
    "r_no_second_agreement": [
        ("(n >= 2u && nvm_reads_agree(second, rd))", "(n >= 2u && 0 && nvm_reads_agree(second, rd))"),
    ],
    # bound of two reads: a single faulty read can no longer be outvoted
    "r_two_tries": [
        ("#define NVM_READ_TRIES         3u", "#define NVM_READ_TRIES         2u"),
    ],
    # the held writer keeps answering the liveness deadline
    "r_held_heartbeats": [
        ("\tnvm_retired = 1;\n\tprintf(\"Milan NVM: slot %s gave no standing verdict",
         "\tprintf(\"Milan NVM: slot %s gave no standing verdict"),
    ],
    # the console commit goes through while held
    "r_console_commit_while_held": [
        ("\t\tif (!nvm_ready && nvm_unread)\n\t\t\tprintf(",
         "\t\tif (!nvm_ready && nvm_unread && !nvm_commit(\"console\"))\n\t\t\tprintf("),
    ],
    # an unread pick no longer offers the other slot: blank is offered
    "r_restage_fail_offers_none": [
        ("\t\tchosen = nvm_pick_slot(nvm_verdict_a, seq_a, nvm_verdict_b, seq_b);\n\t}\n",
         "\t\tchosen = NVM_SLOT_NONE;\n\t}\n"),
    ],
    # the re-stage accepts any OK read, whatever sequence it names
    "r_restage_any_seq": [
        ("\t\tif (rd.vd == VD_OK && rd.seq == seq)\n\t\t\treturn 1;",
         "\t\tif (rd.vd == VD_OK && (rd.seq == seq || 1))\n\t\t\treturn 1;"),
    ],
    # the window is filled by a fresh read of the slot, as before #671
    "r_fill_from_flash": [
        ("\tif (chosen == NVM_SLOT_NONE)\n\t\tnvm_stage_blank_image();\n"
         "\tfor (i = 0; i < NVM_IMG_LEN; ++i)\n\t\tNVM_IMG[i] = NVM_STG[i];\n",
         "\tif (chosen != NVM_SLOT_NONE) {\n"
         "\t\tconst volatile uint8_t *src = nvm_slot(chosen);\n\n"
         "\t\tfor (i = 0; i < NVM_IMG_LEN; ++i)\n\t\t\tNVM_IMG[i] = src[i];\n"
         "\t} else {\n\t\tnvm_stage_blank_image();\n"
         "\t\tfor (i = 0; i < NVM_IMG_LEN; ++i)\n\t\t\tNVM_IMG[i] = NVM_STG[i];\n\t}\n"),
    ],
    # a refusal's digest covers the 40 header bytes only, not every byte read
    "r_digest_header_only": [
        ("\t\trd.digest = nvm_crc32(NVM_STG, rd.bytes);",
         "\t\trd.digest = nvm_crc32(NVM_STG, KLJ2_HDR);"),
    ],
    # no re-stage at all: the stage still holds whichever slot was judged last
    "r_no_restage": [
        ("\twhile (chosen != NVM_SLOT_NONE &&\n\t       !nvm_restage(",
         "\twhile (0 && chosen != NVM_SLOT_NONE &&\n\t       !nvm_restage("),
    ],
}


def grade_one(repo: Path, cfg: Path, work: Path, label: str, text: str, all_grades: bool,
              body_off=None):
    sys.path.insert(0, str(repo / "sw/firmware/nvm_hosttest"))
    import test_nvm_firmware as t  # noqa: E402  (the head's harness)
    work.mkdir(parents=True, exist_ok=True)
    if body_off is not None:
        orig = t.fault_cases

        def body_cases(bench):
            """The head's check-13 cases, with every valid-slot XOR fault moved
            to one byte of the record area (a body fault), BASE 8."""
            out = []
            for valid, target, seq, fault, count, skip in orig(bench):
                if fault[0] == "--read-fault" and target == valid:
                    sl, _b, sk, co = fault[1].split(":")[:4]
                    fault = ("--read-fault", f"{sl}:{body_off}:{sk}:{co}:8")
                out.append((valid, target, seq, fault, count, skip))
            return out
        t.fault_cases = body_cases
    try:
        bench = t.make_bench(cfg, work, text)
    except SystemExit as e:
        return label, [f"BUILD EXIT: {str(e)[:400]}"]
    grades = t.GRADES if all_grades else t.READ_FAULT_GRADES
    out = []
    for g in grades:
        try:
            got = g(bench)
        except SystemExit as e:  # a harness crash is itself a finding
            got = [f"HARNESS EXIT: {str(e)[:300]}"]
        out += [f"{g.__name__}: {x}" for x in got]
    return label, out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", type=Path)
    ap.add_argument("config", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("--base-fw", type=Path)
    ap.add_argument("--plant", action="append")
    ap.add_argument("--all-grades", action="store_true")
    ap.add_argument("--head", action="store_true", help="also grade the unplanted head")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--body-fault", type=lambda v: int(v, 0),
                    help="move every valid-slot XOR fault to this byte offset in the slot")
    a = ap.parse_args()
    head = (a.repo / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text()
    jobs = []
    if a.head:
        jobs.append(("head", head))
    if a.base_fw:
        jobs.append(("base", a.base_fw.read_text()))
    for name in a.plant or []:
        text = head
        for old, new in PLANTS[name]:
            n = text.count(old)
            if n != 1:
                print(f"PLANT {name}: text occurs {n} times, not applied")
                return 2
            text = text.replace(old, new)
        jobs.append((name, text))
    rc = 0
    with cf.ProcessPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(grade_one, a.repo, a.config, a.work / lab, lab, txt, a.all_grades,
                          a.body_fault)
                for lab, txt in jobs]
        for f in cf.as_completed(futs):
            lab, out = f.result()
            print(f"=== {lab}: {len(out)} finding(s)")
            for x in out:
                print(f"  {x}")
            sys.stdout.flush()
    return rc


if __name__ == "__main__":
    sys.exit(main())
