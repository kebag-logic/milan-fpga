#!/usr/bin/env python3
"""Compare each d3 mutant's failing-check count (FAIL: lines in its per-mutant
log, as d3_mutants.py counts them) with the last-cell number of its README
record row. usage: d3_counts.py REPO OUTDIR..."""
import pathlib, re, sys
repo = pathlib.Path(sys.argv[1])
rec = {}
for readme in sorted(repo.glob("tb/*/README.md")):
    for line in readme.read_text().splitlines():
        m = re.match(r"^\| `([A-Za-z0-9_]+)` \|", line)
        if m:
            last = line.strip().strip("|").split("|")[-1].strip()
            n = re.match(r"(\d[\d,]*)", last)
            if n:
                rec.setdefault(m.group(1), []).append((int(n.group(1).replace(",", "")), readme.parent.name))
got = {}
for d in sys.argv[2:]:
    for log in pathlib.Path(d).glob("*.log"):
        if log.stem.startswith("golden"):
            continue
        text = log.read_text(errors="replace")
        got[log.stem] = sum(1 for l in text.splitlines() if l.startswith("FAIL: "))
diff = norec = 0
for name, n in sorted(got.items()):
    r = rec.get(name)
    if not r:
        norec += 1
        print(f"NOREC {name}: failing {n}")
        continue
    ok = any(v == n for v, _ in r)
    diff += not ok
    print(f"{'OK ' if ok else 'DIFF'} {name}: failing {n}, README {r}")
print(f"{len(got)} mutants; {len(got) - norec} with a record row; {diff} count differences; {norec} without a numeric record")
