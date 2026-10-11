#!/usr/bin/env python3
"""R602-5 reviewer probe for #671 / PR #715 (round 5).

Usage: probe_r602_5.py TREE WORK [--jobs N] [--mutants a,b,...] [--standing]

TREE is a checkout of the head under review; WORK is a scratch directory.
The probe imports the tree's own host harness (sw/firmware/nvm_hosttest) and
grades, on endstation_arty_4x4 and both product shapes:

  trailer   a byte fault on the container's CRC trailer only (first and
            last trailer byte: VD_CRC refusals whose bytes before the trailer
            are identical) and on the last byte before the trailer, two or
            three faulty reads then clean reads, at every start of the boot and
            restart bound, both orientations, one slot valid and the other
            blank or older, every FAULT_SEQS / BOTH_VALID_SEQS value;
  sealedalt the harness's --read-sealed fault at offsets the standing suite
            does not use: the model ID (VD_SHAPE) and the record-layout word
            (VD_REC);
  standing  (with --standing) the tree's check 13 and 14 in full count.

Each set runs on the firmware as it is ("head") and on each planted mutant:

  no_tail       the trailer is dropped from the refused-read comparison;
  digest_short  the refusal CRC stops eight bytes short of the end, so the
                four bytes before the trailer are compared by nothing;
  trailer_in    the round-4 whole-read CRC with the trailer compare kept
                (expected equivalent: the tail and the whole-read CRC
                together determine the prefix CRC).

A finding line is printed per case; a summary line per (mutant, shape, set).
Exit 0 always; the receipts are the printed counts.
"""
import argparse
import sys
from dataclasses import replace
from pathlib import Path

MUTANTS = {
    "no_tail": (("\treturn a.vd == b.vd && a.bytes == b.bytes && a.digest == b.digest &&\n"
                 "\t       a.tail == b.tail;",
                 "\treturn a.vd == b.vd && a.bytes == b.bytes && a.digest == b.digest;"),),
    "digest_short": (("\t\trd.digest = nvm_crc32(NVM_STG, rd.bytes - KLJ2_TRAILER);",
                      "\t\trd.digest = nvm_crc32(NVM_STG, rd.bytes - 2u * KLJ2_TRAILER);"),),
    "trailer_in": (("\t\trd.digest = nvm_crc32(NVM_STG, rd.bytes - KLJ2_TRAILER);",
                    "\t\trd.digest = nvm_crc32(NVM_STG, rd.bytes);"),),
}
SHAPES = ("endstation_arty_4x4", "endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tree", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--mutants", default="head," + ",".join(MUTANTS))
    ap.add_argument("--standing", action="store_true")
    ap.add_argument("--sets", default="trailer,sealedalt")
    a = ap.parse_args()
    sys.path.insert(0, str(a.tree / "sw/firmware/nvm_hosttest"))
    import test_nvm_firmware as t
    import read_fault_cases as rfc
    from concurrent.futures import ThreadPoolExecutor

    firmware = (a.tree / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text()
    a.work.mkdir(parents=True, exist_ok=True)
    base = {}
    for shape in SHAPES:
        w = a.work / "base" / shape
        w.mkdir(parents=True, exist_ok=True)
        base[shape] = t.make_bench(a.tree / "configs" / f"{shape}.yaml", w, firmware)

    def cases(bench, which):
        body = t.KLJ2_HDR + (bench.img_len - t.KLJ2_HDR - t.KLJ2_TRAILER) // 2
        out = []
        for restart in (False, True):
            bound = rfc.BOOT_READ_BOUND - int(restart)
            for older, seqs in ((False, rfc.FAULT_SEQS), (True, rfc.BOTH_VALID_SEQS)):
                for valid in "ab":
                    other = "b" if valid == "a" else "a"
                    targets = [valid] + ([other] if older else [])
                    for slot in targets:
                        for seq in seqs:
                            if which == "trailer":
                                faults = [("--read-fault", f"{slot}:{bench.img_len + k}")
                                          for k in (-5, -4, -1)]
                            else:
                                faults = [("--read-sealed", f"{slot}:{off}")
                                          for off in (28, 36)]
                            for opt, head in faults:
                                for skip in range(bound):
                                    for count in (2, 3):
                                        c = rfc.FaultCase(valid, older, seq,
                                                          (opt, f"{head}:{skip}:{count}:8"),
                                                          skip, count, restart)
                                        if rfc.expect(c).within:
                                            out.append(c)
        return out

    def grade_set(bench, which):
        fr = t.fault_run(bench)
        cs = cases(bench, which)

        def one(k):
            w = bench.work / f"{which}{k}"
            w.mkdir(parents=True, exist_ok=True)
            got = []
            for i in range(k, len(cs), a.jobs):
                got += t.grade_fault_case(bench, fr, cs[i], w)
            return got
        with ThreadPoolExecutor(a.jobs) as ex:
            found = [x for r in ex.map(one, range(a.jobs)) for x in r]
        return len(cs), found

    for label in a.mutants.split(","):
        text = firmware
        if label != "head":
            for old, new in MUTANTS[label]:
                assert text.count(old) == 1, f"{label}: anchor not unique"
                text = text.replace(old, new)
        for shape in SHAPES:
            bench = base[shape]
            if label != "head":
                bench = t.replant(bench, a.work / label / shape, text)
            bench = replace(bench, jobs=a.jobs)
            for which in [x for x in a.sets.split(",") if x in ("trailer", "sealedalt")]:
                n, found = grade_set(bench, which)
                lost = sum("was lost on the clean reboot" in x for x in found)
                for x in found[:3]:
                    print(f"  {label} {shape} {which}: {x}")
                print(f"SUMMARY {label} {shape} {which}: cases={n} findings={len(found)} lost={lost}",
                      flush=True)
            if a.standing and label != "head":
                got = t.grade_refused_generation(bench) + t.grade_read_faults(bench)
                lost = sum("was lost on the clean reboot" in x for x in got)
                for x in got[:3]:
                    print(f"  {label} {shape} standing: {x}")
                print(f"SUMMARY {label} {shape} standing: findings={len(got)} lost={lost}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
