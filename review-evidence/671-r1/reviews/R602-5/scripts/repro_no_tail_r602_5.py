#!/usr/bin/env python3
"""R602-5 single-case reproduction for #671 / PR #715 round 5.

Usage: repro_no_tail_r602_5.py TREE WORK

Slot A holds a valid container at 0x5A5A5 and slot B is blank. The first two
judgement reads of A answer with the first CRC-trailer byte XORed by a
different value each (VD_CRC, the bytes before the trailer identical), the
third is clean; then a change, its commit and a clean reboot. Graded by the
tree's own check-13 case grader, on the firmware as it is and with the
trailer dropped from the refused-read comparison (`no_tail`), on both
product shapes, on a cold boot and on a writer restart. Every finding is
printed whole.
"""
import sys
from dataclasses import replace
from pathlib import Path

OLD = ("\treturn a.vd == b.vd && a.bytes == b.bytes && a.digest == b.digest &&\n"
       "\t       a.tail == b.tail;")
NEW = "\treturn a.vd == b.vd && a.bytes == b.bytes && a.digest == b.digest;"


def main() -> int:
    tree, work = Path(sys.argv[1]), Path(sys.argv[2])
    sys.path.insert(0, str(tree / "sw/firmware/nvm_hosttest"))
    import test_nvm_firmware as t
    import read_fault_cases as rfc
    text = (tree / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text()
    assert text.count(OLD) == 1
    for shape in ("endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8"):
        w = work / "base" / shape
        w.mkdir(parents=True, exist_ok=True)
        bench = replace(t.make_bench(tree / "configs" / f"{shape}.yaml", w, text), jobs=1)
        for label in ("head", "no_tail"):
            b = bench if label == "head" else t.replant(bench, work / label / shape, text.replace(OLD, NEW))
            fr = t.fault_run(b)
            for restart in (False, True):
                skip = 0 if restart else 1
                case = rfc.FaultCase("a", False, 0x5A5A5,
                                     ("--read-fault", f"a:{b.img_len - 4}:{skip}:2:8"), skip, 2, restart)
                e = rfc.expect(case)
                cw = work / "cases" / label / shape / ("restart" if restart else "cold")
                cw.mkdir(parents=True, exist_ok=True)
                got = t.grade_fault_case(b, fr, case, cw)
                print(f"{label} {shape} {'restart' if restart else 'cold'}: {case.name}; model "
                      f"reads={e.reads} judgement={e.judgement} unread={e.unread!r}; "
                      f"findings={len(got)}")
                for x in got:
                    print(f"    {x}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
