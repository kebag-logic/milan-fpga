"""Scratch (round 8): a capture's compiled sources grouped by the phase that compiled them, read from where the
compile wrote (its -o, else its directory): the arms' builds, each campaign, the coverage builds, the store; by
the gate's own classification (Places), run with the gate modules of the tree the capture was made in.

usage: phases.py <tree> <capture>
"""
import collections
import re
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(tree / "sw/firmware/ctrl/test"), str(tree / "sw/firmware/gtest")]
import ctrl_boundary as cb  # noqa: E402
import ctrl_capture  # noqa: E402

cap = ctrl_capture.load(Path(sys.argv[2]).resolve())
places = cb.Places((cb.ROOT.resolve(),), cb.targets(cap, (cb.ROOT,)))
PHASE = re.compile(r"/(ctrl-fw-[^/]+/[^/]+|fw-coverage\.[^/]+/[^/]+/[^/]+|ctrl-nvm\.[^/]+|fw-rv32-[^/]+|ctrl-boundary-[^/]+/[^/]+)")
groups = collections.defaultdict(collections.Counter)
names = collections.defaultdict(set)
for inv in cap.invocations:
    out = next((inv.args[i + 1] for i, a in enumerate(inv.args[:-1]) if a == "-o"), inv.cwd)
    m = PHASE.search(out)
    phase = re.sub(r"(ctrl-fw-|fw-coverage\.|ctrl-nvm\.|fw-rv32-)[^/]+", r"\1*", m.group(1)) if m else "other"
    impl = cb.implementation(inv)
    for src in inv.sources:
        if src.lang in cb.COMPILED:
            k = places.kind(src.path, impl)
            groups[phase][k] += 1
            if k in (cb.FIRMWARE, cb.STACK_FILE, cb.PUBLIC):
                names[(phase, k)].add(places.name(src.path))
for phase in sorted(groups):
    print(phase, dict(groups[phase]))
    for k in (cb.FIRMWARE, cb.STACK_FILE):
        if names[(phase, k)]:
            print("   ", k, len(names[(phase, k)]), sorted(names[(phase, k)])[:8])
