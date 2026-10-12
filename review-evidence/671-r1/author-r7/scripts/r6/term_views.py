#!/usr/bin/env python3
"""What each comparison term's class actually hands the writer (#671 round 6).

Usage: term_views.py TREE WORK [--shapes a,b,...]

Compiles a probe copy of the firmware (never the tree's) whose
nvm_read_slot prints every read's slot and the four terms nvm_reads_agree
compares: verdict, byte count, prefix CRC (digest) and trailer (tail). Runs
the faulty boot or writer restart of every term-class case check 13
generates and requires, for the faulted slot's judgement: three reads, the
first two refused and differing from each other in their own term and in no
other, the third VD_OK. Exit 1 on any other shape of read.
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("tree", type=Path)
ap.add_argument("work", type=Path)
ap.add_argument("--shapes", default="endstation_arty_4x4,endstation_ax7101_1x1_tdm8,endstation_ax7101_8x8")
a = ap.parse_args()
tree = a.tree.resolve()
sys.path.insert(0, str(tree / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as t  # noqa: E402
import read_fault_cases as c  # noqa: E402

ANCHOR = "\t\trd.tail = nvm_rd32(NVM_STG + rd.bytes - KLJ2_TRAILER);\n\t}\n\treturn rd;\n"
PROBE = ANCHOR.replace("\treturn rd;\n", '\tprintf("PROBE read slot=%u vd=%u bytes=%u digest=%08x tail=%08x\\n",\n'
                       "\t       (unsigned int)slot, rd.vd, (unsigned int)rd.bytes, (unsigned int)rd.digest,\n"
                       "\t       (unsigned int)rd.tail);\n\treturn rd;\n")
READ_RE = re.compile(r"PROBE read slot=(\d+) vd=(\d+) bytes=(\d+) digest=([0-9a-f]+) tail=([0-9a-f]+)")
FIELD = {"verdict": 1, "byte count": 2, "prefix CRC": 3, "trailer": 4}
text = t.FIRMWARE.read_text()
assert text.count(ANCHOR) == 1
probe_text = text.replace(ANCHOR, PROBE)
rc = 0
for shape in a.shapes.split(","):
    work = a.work.resolve() / shape
    bench = t.make_bench(tree / "configs" / f"{shape}.yaml", work / "base", text)
    pb = t.replant(bench, work / "probe", probe_text)
    fr = t.fault_run(pb)
    cases = [x for x in c.fault_cases(t.KLJ2_HDR + (pb.img_len - t.KLJ2_HDR - t.KLJ2_TRAILER) // 2) if c.term_of(x)]
    slots_seen = Counter()
    tally = Counter()
    for case in cases:
        newer = fr.containers[(case.seq, False)]
        other = fr.containers[(case.seq, True)] if case.older else b"\xff" * t.SLOT
        slots = {case.valid.upper(): newer, case.other.upper(): other}
        (work / "a.bin").write_bytes(slots["A"])
        (work / "b.bin").write_bytes(slots["B"])
        lead = ("--slot-a", str(work / "a.bin"), "--slot-b", str(work / "b.bin"))
        if case.restart:
            out = t.run(pb, *lead, "--boot", "--idle-ms", "100", *case.fault, "--restart")[0]
            out = out.split("HOST restarting\n", 1)[1]
        else:
            out = t.run(pb, *lead, *case.fault, "--boot")[0]
        reads = [m.groups() for m in READ_RE.finditer(out)]
        slots_seen.update(r[0] for r in reads)
        # the slot ids the firmware passes: the first read of a boot judges A
        a_id = reads[0][0]
        faulted = [r for r in reads if (r[0] == a_id) == (case.fault[1][0] == "a")]
        term = c.term_of(case)
        f1, f2, ok = faulted[0], faulted[1], faulted[2]
        differ = [name for name, i in FIELD.items() if f1[i] != f2[i]]
        good = f1[1] != "0" and f2[1] != "0" and ok[1] == "0" and differ == [term]
        tally[(term, good)] += 1
        if not good:
            rc = 1
            print(f"BAD {shape} {case.name}: {faulted[:3]} differ in {differ}", flush=True)
    for term in FIELD:
        print(f"{shape} {term:<10}: {tally[(term, True)]} of {tally[(term, True)] + tally[(term, False)]} cases "
              f"hand the judgement two refusals differing in the {term} alone, then VD_OK", flush=True)
    sample = {}
    for case in cases:
        sample.setdefault(c.term_of(case), case)
    for term, case in sample.items():
        newer = fr.containers[(case.seq, False)]
        other = fr.containers[(case.seq, True)] if case.older else b"\xff" * t.SLOT
        slots = {case.valid.upper(): newer, case.other.upper(): other}
        (work / "a.bin").write_bytes(slots["A"])
        (work / "b.bin").write_bytes(slots["B"])
        out = t.run(pb, "--slot-a", str(work / "a.bin"), "--slot-b", str(work / "b.bin"),
                    "--boot", "--idle-ms", "100", *case.fault, "--restart")[0].split("HOST restarting\n", 1)[1]
        print(f"  e.g. {case.name}:", flush=True)
        for m in READ_RE.finditer(out):
            print(f"    {m.group(0)}", flush=True)
print("term views:", "OK" if not rc else "FAILED")
sys.exit(rc)
