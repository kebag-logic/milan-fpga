"""Scratch: grade a firmware text from a file (the base firmware) with the
head's checks 13 and 14 on one shape and summarise the findings by kind.

usage: base_repro.py REPO CONFIG WORK JOBS FIRMWARE_FILE
"""
import dataclasses
import sys
from pathlib import Path

repo, cfg, work, jobs, fw = (Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]),
                             int(sys.argv[4]), Path(sys.argv[5]))
sys.path.insert(0, str(repo / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as t  # noqa: E402

work.mkdir(parents=True, exist_ok=True)
b = dataclasses.replace(t.make_bench(cfg, work, fw.read_text()), jobs=jobs)
got = t.grade_read_faults(b) + t.grade_refused_generation(b)
lost = [x for x in got if "was lost on the clean reboot" in x]
others = [x for x in got if "did not survive" in x]
print(f"BASE {cfg.stem}: {len(got)} finding(s); {len(lost)} 'was lost on the clean reboot'; "
      f"{len(others)} 'other saved record(s) did not survive'")
kinds = {}
for x in got:
    k = x.split(": ", 1)[1][:70] if ": " in x else x[:70]
    kinds[k] = kinds.get(k, 0) + 1
for k, n in sorted(kinds.items(), key=lambda kv: -kv[1])[:12]:
    print(f"BASE   {n:4d} x {k}")
for x in lost[:3]:
    print(f"BASE   e.g. {x[:300]}")
