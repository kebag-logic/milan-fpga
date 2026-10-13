"""Scratch: read a capture back; count invocations, expansions, reuse, refusals, modes, files read first."""
import collections, json, sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve(); caps = [Path(a).resolve() for a in sys.argv[2:]]
sys.path[:0] = [str(tree / "sw/firmware/ctrl/test"), str(tree / "sw/firmware/gtest")]
import ctrl_capture, ctrl_configs
c = sum((ctrl_capture.load(p) for p in caps[1:]), ctrl_capture.load(caps[0]))
for p in caps:
    entries = [e for e in (p / "expand").iterdir() if e.is_file() and not e.name.startswith("base-")]
    print(f"{p.name}: entries {len(entries)}")
invs = c.invocations
print("invocations", len(invs), "expanded", sum(1 for i in invs if i.expansion is not None),
      "distinct expansions", len({i.expansion.digest for i in invs if i.expansion is not None}),
      "not expanded (no input)", sum(1 for i in invs if i.expansion is None and not i.failed))
reasons = []
for leaf in c.leaves:
    reasons += ctrl_configs.expanded(leaf, ctrl_configs.places((ctrl_configs.CTRL, ctrl_configs.STACK)))
print("expansion refusals", len(reasons))
for r in list(dict.fromkeys(reasons))[:15]:
    print("  ", r[:400])
first = collections.Counter()
for i in invs:
    if i.expansion is not None and not i.expansion.error:
        for where, what in ctrl_configs.read_first(i):
            if what != ctrl_configs.IMPLEMENTATION:
                first[(Path(where).name, what)] += 1
print("files read first (not the implementation's):", first.most_common(20))
print("read-first units:", ctrl_configs.read_first_units(c, (ctrl_configs.CTRL, ctrl_configs.STACK)))
try:
    modes = {}
    for leaf in c.leaves:
        for k, v in ctrl_configs.modes_of(leaf).items():
            modes.setdefault(k, set()).update(v)
    print("modes:", len(modes))
    for k, v in sorted(modes.items()):
        print("  ", k, sorted(v))
except Exception as exc:
    print("modes refused:", exc)
langs = collections.Counter(l for i in invs for _, l, _ in i.sources)
print("source languages:", langs)
