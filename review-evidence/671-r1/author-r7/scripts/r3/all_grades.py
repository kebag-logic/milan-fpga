"""Round 3 scratch: grade the shipping writer's checks 1 to 14 (the gate's
own `grade`) on a planted copy of the firmware, per shape, as the reviewers'
--all-grades probe does, and print CAUGHT with the first finding or SURVIVED.

usage: all_grades.py REPO WORK JOBS LABEL SHAPE...
LABEL is a READ_FAULT_MUTATIONS label, or "head" for the unplanted firmware.
"""
import dataclasses
import sys
from pathlib import Path

repo, work, jobs, label = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
sys.path.insert(0, str(repo / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as t  # noqa: E402

text = t.FIRMWARE.read_text()
if label != "head":
    for old, new in t.READ_FAULT_MUTATIONS[label][0]:
        assert text.count(old) == 1, label
        text = text.replace(old, new)
for shape in sys.argv[5:]:
    w = work / label / shape
    w.mkdir(parents=True, exist_ok=True)
    bench = dataclasses.replace(t.make_bench(repo / "configs" / f"{shape}.yaml", w, text), jobs=jobs)
    got = t.grade(bench)
    print(f"{label:<22} {shape:<28} " + (f"CAUGHT ({len(got)} finding(s)); first: {got[0]}" if got else "SURVIVED"),
          flush=True)
