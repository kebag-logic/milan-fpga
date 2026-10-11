#!/usr/bin/env python3
"""Grade the round-3 reviewers' firmware plants with this head's checks 13 and 14 (#671 round 4).

Usage: reviewer_plants.py <tree> <work> <jobs> <probe.py>... -- <cfg-stem>...

Each probe file is PARSED with ast and never executed: its module-level PLANTS
dict literal gives label -> (old, new) pairs (R602-3's form, a list of pairs;
R603-3's form, a (pairs, why) tuple). Each plant is applied to the head
firmware text (each old text must occur exactly once), compiled into the
head's host harness and graded by checks 13 and 14 in full, no early stop.
Prints, per plant and shape, the finding count and the counts of the words
the controls use.
"""
import ast
import sys
import time
from collections import Counter
from dataclasses import replace
from pathlib import Path

tree, work, jobs = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
split = sys.argv.index("--")
probes, stems = sys.argv[4:split], sys.argv[split + 1:]
sys.path.insert(0, str(tree / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as T  # noqa: E402

KEYS = ("want exactly", "over the bound", "names another cause", "held the writer; the bound",
        "did not hold the writer", "re-attached live", "was lost on the clean reboot", "did not survive",
        "neither committed nor refused", "does not name it unread", "on reads that returned different bytes",
        "yet the boot offered", "is not the container it judged", "another valid container",
        "printed no boot line", "persisted something", "but holds", "generation was taken",
        "printed that it re-attached", "reloaded the window", "did not refuse the console",
        "named the slot on the console", "did not erase both slots")


def plants(path: Path) -> dict:
    """The PLANTS literal of a probe file, by label, as lists of (old, new)."""
    mod = ast.parse(path.read_text())
    for node in mod.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "PLANTS" for t in node.targets):
            raw = ast.literal_eval(node.value)
            return {k: (list(v[0]) if isinstance(v, tuple) and len(v) == 2 and isinstance(v[1], str) else list(v))
                    for k, v in raw.items()}
    raise SystemExit(f"no PLANTS literal in {path}")


text = T.FIRMWARE.read_text()
work.mkdir(parents=True, exist_ok=False)
benches = {s: replace(T.make_bench(tree / "configs" / f"{s}.yaml", work / f"base-{s}", text), jobs=jobs)
           for s in stems}
#: R602-3's p_console_unnamed, re-spelled at this head: the console's commit
#: refusal while held is removed (R603-3-S1 rewrote the text it anchored on)
RESPELLED = {"p_console_unnamed@head": [(
    "\t\tif (nvm_held) {\n\t\t\tprintf(\"NVM: refused; \");\n\t\t\tnvm_print_unread();\n"
    "\t\t\tprintf(\" at boot, the writer is HELD until reset.\\n\");\n\t\t} else if (!nvm_ready) {",
    "\t\tif (!nvm_ready) {")]}
for probe in probes:
    table = RESPELLED if probe == "respelled" else plants(Path(probe))
    for label, pairs in table.items():
        planted, bad = text, []
        for old, new in pairs:
            if planted.count(old) != 1:
                bad.append(planted.count(old))
            else:
                planted = planted.replace(old, new)
        tag = f"{Path(probe).parent.parent.name or probe}:{label}"
        if bad:
            print(f"{tag:<44} anchor occurs {bad} times at this head: NOT APPLIED", flush=True)
            continue
        for stem, bench in benches.items():
            t0 = time.time()
            pb = T.replant(bench, work / (Path(probe).parent.parent.name or probe) / label / stem, planted)
            got = T.grade(pb, T.READ_FAULT_GRADES)
            kinds = Counter(k for g in got for k in KEYS if k in g)
            print(f"{tag:<44} {stem:<27} findings={len(got):4d} {time.time() - t0:5.0f}s {dict(kinds)}", flush=True)
