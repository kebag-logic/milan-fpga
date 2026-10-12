#!/usr/bin/env python3
"""Each comparison term's class against each term's omission (#671 round 6).

Usage: term_matrix.py TREE WORK [--jobs N] [--shapes a,b,...]

For each shape, runs check 13's term-class cases (read_fault_cases.term_of
names a term) through the tree's own grade_fault_case, on the firmware as it
is and with each r_omit_ control planted. Prints, per plant and class, how
many cases have findings, how many carry the plant's own words, and how many
lose saved state on the clean reboot. Exit 1 unless the head is clean and
each plant is named by every case of its own class and by no other class.
"""
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("tree", type=Path)
ap.add_argument("work", type=Path)
ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--shapes", default="endstation_arty_4x4,endstation_ax7101_1x1_tdm8,endstation_ax7101_8x8")
a = ap.parse_args()
sys.path.insert(0, str(a.tree.resolve() / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as t  # noqa: E402
import read_fault_cases as c  # noqa: E402

firmware = t.FIRMWARE.read_text()
rc = 0
for shape in a.shapes.split(","):
    work = a.work.resolve() / shape
    base = replace(t.make_bench(a.tree.resolve() / "configs" / f"{shape}.yaml", work / "head", firmware), jobs=a.jobs)
    fr = t.fault_run(base)
    cases = [x for x in c.fault_cases(t.KLJ2_HDR + (base.img_len - t.KLJ2_HDR - t.KLJ2_TRAILER) // 2)
             if c.term_of(x)]
    for label in ["head"] + [c.control_of(term) for term, _, _ in c.COMPARISON]:
        bench = base
        if label != "head":
            (pairs, words) = c.READ_FAULT_MUTATIONS[label]
            text = firmware
            for old, new in pairs:
                assert text.count(old) == 1, label
                text = text.replace(old, new)
            bench = t.replant(base, work / label, text)

        def one(k, bench=bench):
            w = bench.work / f"tm{k}"
            w.mkdir(exist_ok=True)
            return [(i, t.grade_fault_case(bench, fr, cases[i], w)) for i in range(k, len(cases), a.jobs)]
        with ThreadPoolExecutor(a.jobs) as ex:
            got = dict(x for part in ex.map(one, range(a.jobs)) for x in part)
        for term, _, _ in c.COMPARISON:
            mine = [got[i] for i, x in enumerate(cases) if c.term_of(x) == term]
            failing = sum(bool(f) for f in mine)
            named = sum(any(c.alone_in(term) in y for y in f) for f in mine)
            lost = sum(any("was lost on the clean reboot" in y or "did not survive" in y for y in f) for f in mine)
            print(f"{shape} {label:<18} class {term:<10} cases={len(mine)} failing={failing} "
                  f"named={named} lost={lost}", flush=True)
            own = label == c.control_of(term)
            if label == "head" or not own:
                rc |= failing != 0
            else:
                rc |= named != len(mine)
        if label != "head":
            sample = next((y for i, f in sorted(got.items()) for y in f), "none")
            print(f"{shape} {label:<18} first finding: {sample}", flush=True)
print("term matrix:", "OK" if not rc else "FAILED")
sys.exit(rc)
