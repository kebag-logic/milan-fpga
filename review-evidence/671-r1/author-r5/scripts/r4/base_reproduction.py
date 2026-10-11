#!/usr/bin/env python3
"""The base firmware graded by this head's checks 13 and 14 (#671 round 4, R602-3-F2).

Usage: base_reproduction.py <tree> <work> <jobs> <base-commit> <cfg-stem>...

The base firmware is `git show <base-commit>:sw/firmware/milan_baremetal/milan_baremetal.c`.
This head's harness appends the writer-restart model, which refuses a firmware
whose file-scope statics differ from writer_restart.WRITER_STATICS; the base
writer has none of the four #671 statics (nvm_unread, nvm_unstaged, nvm_held,
nvm_read_faults). The model is therefore narrowed to exactly the statics the
same regex finds in the base text, which must equal WRITER_STATICS without
those four, and nothing else changes. Checks 13 and 14 then run in full, no
early stop, and the findings are counted by kind.
"""
import re
import subprocess
import sys
import time
from collections import Counter
from dataclasses import replace
from pathlib import Path

tree, work, jobs, base = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
sys.path.insert(0, str(tree / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as T  # noqa: E402
import writer_restart as W  # noqa: E402

text = subprocess.run(["git", "-C", str(tree), "show", f"{base}:sw/firmware/milan_baremetal/milan_baremetal.c"],
                      check=True, capture_output=True, text=True).stdout
import hashlib  # noqa: E402
print(f"base firmware {base}: sha256 {hashlib.sha256(text.encode()).hexdigest()}")
found = set(re.findall(r"^static (?:int|uint32_t|uint64_t|unsigned int) (nvm_\w+)(?: = [^;(]+)?;$", text, re.M))
narrowed = {k: v for k, v in W.WRITER_STATICS.items() if k in found}
assert found == set(narrowed), sorted(found ^ set(narrowed))
print(f"restart model narrowed by {sorted(set(W.WRITER_STATICS) - found)}; {len(narrowed)} statics kept")
W.WRITER_STATICS = narrowed
work.mkdir(parents=True, exist_ok=False)
for stem in sys.argv[5:]:
    t0 = time.time()
    bench = replace(T.make_bench(tree / "configs" / f"{stem}.yaml", work / stem, text), jobs=jobs)
    got = T.grade(bench, T.READ_FAULT_GRADES)
    keys = ("was lost on the clean reboot", "did not survive", "want exactly", "over the bound",
            "did not hold the writer", "re-attached live", "neither committed nor refused",
            "generation was taken", "printed no boot line", "but holds", "on reads that returned different bytes",
            "does not name it unread", "yet the boot offered", "another valid container",
            "is not the container it judged")
    kinds = Counter(k for g in got for k in keys if k in g)
    lost = sorted({g.split(": ", 2)[1] for g in got if "was lost on the clean reboot" in g})
    print(f"{stem}: {len(got)} findings in {time.time() - t0:.0f}s; {dict(kinds)}")
    print(f"  cases whose committed change was lost on the clean reboot: {len(lost)}")
    for name in lost[:3]:
        print(f"    e.g. {name}")
