"""Scratch (round 8): what a capture's compiles are, by the boundary gate's own reader and classification, run
with the gate modules of the tree the capture was made in (that tree's ROOT).

usage: popcmp.py <tree> <capture> <out.json> [builder ...]
Writes the judged facts: for every compiled source of the firmware or the stack (Places.kind), the files of a
checkout root its dependency list names (by kind and name) and the kinds of the rest; every include edge whose
includer lies in a root; and, per builder named, the kinds of the sources its invocations compile.
"""
import collections
import json
import re
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(tree / "sw/firmware/ctrl/test"), str(tree / "sw/firmware/gtest")]
import ctrl_boundary as cb  # noqa: E402
import ctrl_capture  # noqa: E402

cap = ctrl_capture.load(Path(sys.argv[2]).resolve())
out = Path(sys.argv[3])
watch = sys.argv[4:]
root = cb.ROOT.resolve()
places = cb.Places((root,), cb.targets(cap, (cb.ROOT,)))
TMP = re.compile(r"/(?:ctrl-fw-|fw-coverage\.|ctrl-nvm\.|fw-rv32-|ctrl-boundary-|tmp)[^/]*")


def norm(path: str) -> str:
    return TMP.sub("/<tmp>", path)


facts, edges = set(), set()
per = {b: collections.Counter() for b in watch}
samples = {b: collections.defaultdict(set) for b in watch}
judged = collections.Counter()
for inv in cap.invocations:
    impl = cb.implementation(inv)
    for src in inv.sources:
        if src.lang not in cb.COMPILED:
            continue
        side = places.kind(src.path, impl)
        for b in watch:
            if b in inv.builders:
                per[b][side] += 1
                if side not in (cb.OUTSIDE,):
                    samples[b][side].add(places.name(src.path))
        if src.deps is None:
            continue
        judged[side] += 1
        if side in (cb.FIRMWARE, cb.PUBLIC, cb.STACK_FILE):
            name = places.name(src.path)
            for f in src.deps.files:
                k = places.kind(f, impl)
                facts.add((name, k, places.name(f) if k not in (cb.OUTSIDE, cb.IMPLEMENTATION) else k))
        for inc, path in src.deps.edges(src.path):
            ki, kp = places.kind(inc, impl), places.kind(path, impl)
            if ki == cb.OUTSIDE:
                continue
            edges.add((ki, places.name(inc), kp, places.name(path) if kp not in (cb.OUTSIDE, cb.IMPLEMENTATION) else kp))
result = {"invocations": len(cap.invocations), "judged": dict(judged), "facts": sorted(facts), "edges": sorted(edges),
          "builders": {b: dict(per[b]) for b in watch},
          "samples": {b: {k: sorted(v)[:40] for k, v in samples[b].items()} for b in watch},
          "builder_counts": collections.Counter(b for inv in cap.invocations for b in inv.builders).most_common()}
out.write_text(json.dumps(result, indent=1), encoding="utf-8")
print(json.dumps({k: result[k] for k in ("invocations", "judged", "builders")}, indent=1))
print("facts", len(facts), "edges", len(edges))
