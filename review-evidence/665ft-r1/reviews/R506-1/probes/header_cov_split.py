#!/usr/bin/env python3
"""Probe (R506-1): coverage of the firmware's measured headers (mbx_wire.h, wire.h),
split by the kind of object that ran them: a firmware C object, or a test
(C++) object. Usage: header_cov_split.py <fw_coverage --keep dir>"""
import gzip, json, subprocess, sys, tempfile
from collections import defaultdict
from pathlib import Path
keep = Path(sys.argv[1])
acc = {k: defaultdict(lambda: [0, []]) for k in ("firmware", "test")}
for gcda in sorted(keep.rglob("*.gcda")):
    kind = "test" if (gcda.with_suffix(".gcno").exists() and "-" in gcda.stem and "/tests" in str(gcda)) or "/tests/" in str(gcda) or "/harness/" in str(gcda) else "firmware"
    with tempfile.TemporaryDirectory() as t:
        subprocess.run(["gcov", "--json-format", "--branch-probabilities", "-o", str(gcda.parent), str(gcda)],
                       cwd=t, capture_output=True, check=False)
        for doc in Path(t).glob("*.gcov.json.gz"):
            for f in json.load(gzip.open(doc, "rt"))["files"]:
                if not f["file"].endswith(("mbx_wire.h", "wire/wire.h")):
                    continue
                for ln in f["lines"]:
                    key = (Path(f["file"]).name, ln["line_number"])
                    slot = acc[kind][key]
                    slot[0] += ln["count"]
                    arcs = [b["count"] for b in ln["branches"]]
                    if len(arcs) > len(slot[1]):
                        slot[1] = arcs[:] if not slot[1] else slot[1] + [0] * (len(arcs) - len(slot[1]))
                    slot[1] = [a + b for a, b in zip(slot[1] + [0] * (len(arcs) - len(slot[1])), arcs + [0] * (len(slot[1]) - len(arcs)))] if arcs else slot[1]
for name in ("mbx_wire.h", "wire.h"):
    keys = sorted({k for kind in acc for k in acc[kind] if k[0] == name})
    for kind in ("firmware", "test"):
        lines = [acc[kind][k] for k in keys if k in acc[kind]]
        arcs = [a for l in lines for a in l[1]]
        print(f"{name:12} by {kind:8} objects: lines run {sum(1 for l in lines if l[0] > 0)}/{len(keys)}"
              f"  arcs taken {sum(1 for a in arcs if a > 0)}/{len(arcs)}")
    for k in keys:
        fw = acc["firmware"].get(k, [0, []]); te = acc["test"].get(k, [0, []])
        if fw[1] or te[1] or fw[0] == 0:
            print(f"   line {k[1]:3}: firmware count {fw[0]} arcs {fw[1]}   test count {te[0]} arcs {te[1]}")
