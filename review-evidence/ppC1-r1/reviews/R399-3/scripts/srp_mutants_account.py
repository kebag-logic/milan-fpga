#!/usr/bin/env python3
"""Map each shard's verdict lines back to (label, suite, group, expected) MUTANTS entries."""
import importlib.util, re, sys
from pathlib import Path
tree, out = Path(sys.argv[1]), Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("m", tree / "tb/srp_top/mutants.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
verdict = {}
covered = set()
for log in sorted(out.glob("shard*.log")):
    txt = log.read_text()
    # the --only set of this shard is recoverable from the arms it printed
    lines = re.findall(r'^(\S+): rc=(\d+) failures=(\d+) (KILLED|UNPROVEN) tags=(.*)$', txt, re.M)
    only = {l[0] for l in lines}
    selected = [e for e in m.MUTANTS if e[0] in only]
    assert len(selected) == len(lines), (log, len(selected), len(lines))
    for e, l in zip(selected, lines):
        assert e[0] == l[0]
        verdict.setdefault(e, set()).add(l[3])
        if l[3] == "KILLED":
            covered.update(t for t in l[4].split(",") if t)
entries = list(m.MUTANTS)
missing_entries = [e for e in entries if e not in verdict]
bad = [e for e in entries if verdict.get(e) != {"KILLED"}]
expected = {f"{g}{i}" for g, c in [("K",12),("L",4),("M",12),("N",13),("O",8),("P",8),("Q",4),("R",4)] for i in range(1, c+1)}
print(f"MUTANTS entries: {len(entries)}; run: {len(entries)-len(missing_entries)}; every run KILLED: {len(bad)==0}")
print(f"assertion coverage (union of killed tags): {len(expected & covered)}/{len(expected)} missing={sorted(expected-covered)}")
for e in bad: print("NOT KILLED:", e, verdict.get(e))
sys.exit(1 if bad or missing_entries or (expected - covered) else 0)
