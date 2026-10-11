"""Every #671 control (or a reviewer plant file's plants, parsed as data) graded by checks 13 and 14
in full, no early stop: python plants_full.py TREE WORK JOBS CFG_STEM [LABEL...]"""
import sys, time
from collections import Counter
from dataclasses import replace
from pathlib import Path
tree, work, jobs, stem = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
sys.path.insert(0, str(tree / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as T
import read_fault_cases as RF
labels = sys.argv[5:] or list(RF.READ_FAULT_MUTATIONS)
KEYS = ("want exactly", "over the bound", "names another cause", "held the writer; the bound",
        "did not hold the writer", "re-attached live", "was lost on the clean reboot", "did not survive",
        "neither committed nor refused", "does not name it unread", "on reads that returned different bytes",
        "yet the boot offered", "is not the container it judged", "another valid container",
        "printed no boot line", "persisted something", "but holds", "generation was taken",
        "printed that it re-attached", "reloaded the window", "did not name the unread slot",
        "which differ only in their")
text = T.FIRMWARE.read_text()
work.mkdir(parents=True, exist_ok=False)
bench = replace(T.make_bench(tree / "configs" / f"{stem}.yaml", work / "base", text), jobs=jobs)
for label in labels:
    pairs, words = RF.READ_FAULT_MUTATIONS[label]
    planted = text
    for old, new in pairs:
        assert planted.count(old) == 1, label
        planted = planted.replace(old, new)
    t0 = time.time()
    pb = T.replant(bench, work / label, planted)
    got = T.grade(pb, T.READ_FAULT_GRADES)
    kinds = Counter(k for g in got for k in KEYS if k in g)
    named = [g for g in got if words in g]
    rs = sum(1 for g in named if "on a writer restart" in g)
    print(f"{label:<28} {stem}: named {len(named)} ({rs} restart / {len(named) - rs} cold) of {len(got)} "
          f"in {time.time() - t0:.0f}s; {dict(kinds)}", flush=True)
    print(f"    first: {named[0][:300] if named else 'NOT CAUGHT'}", flush=True)
