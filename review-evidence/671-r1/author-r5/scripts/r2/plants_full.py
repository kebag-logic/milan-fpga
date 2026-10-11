"""Scratch: grade each #671 plant on the FULL check-13/14 matrix (no early stop)
on one shape, and print the named and total finding counts.

usage: plants_full.py REPO CONFIG WORK JOBS [LABEL...]
"""
import dataclasses
import sys
import time
from pathlib import Path

repo, cfg, work, jobs = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4])
labels = sys.argv[5:]
sys.path.insert(0, str(repo / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as t  # noqa: E402

work.mkdir(parents=True, exist_ok=True)
fw = t.FIRMWARE.read_text()
base = dataclasses.replace(t.make_bench(cfg, work / "base", fw), jobs=jobs)
for label, (pairs, words) in t.READ_FAULT_MUTATIONS.items():
    if labels and label not in labels:
        continue
    text = fw
    for old, new in pairs:
        assert text.count(old) == 1, label
        text = text.replace(old, new)
    t0 = time.time()
    pb = t.replant(base, work / label, text)
    got = t.grade_refused_generation(pb) + t.grade_read_faults(pb)
    named = [x for x in got if words in x]
    print(f"PLANT {cfg.stem} {label}: {'CAUGHT' if named else 'NOT CAUGHT'} named={len(named)} "
          f"total={len(got)} words={words!r} {time.time() - t0:.1f}s", flush=True)
    if named:
        print(f"PLANT   first named: {named[0][:400]}", flush=True)
    kinds = {}
    for x in got:
        k = x.split(": ", 1)[1][:60] if ": " in x else x[:60]
        kinds[k] = kinds.get(k, 0) + 1
    for k, n in sorted(kinds.items(), key=lambda kv: -kv[1])[:6]:
        print(f"PLANT   {n:4d} x {k}", flush=True)
