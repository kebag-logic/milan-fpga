#!/usr/bin/env python3
"""Does `git merge-file` honor diff.algorithm from configuration?

Finds a (current, base, other) triple whose merge-file output differs between
explicit --diff-algorithm=myers and =histogram/patience, then runs merge-file
with no option but -c diff.algorithm=<alg>.  Usage: mergefile_algo_probe.py <dir>
"""
import json, random, subprocess, sys
from pathlib import Path

d = Path(sys.argv[1]); d.mkdir(parents=True, exist_ok=True)
rng = random.Random(423)
def mf(extra, files):
    r = subprocess.run(("git", *extra, "merge-file", "-p", "-q", *map(str, files)), capture_output=True)
    return r.returncode, r.stdout
def rand_lines(n):
    return [rng.choice("abcxy{}") for _ in range(n)]
found = None
for trial in range(20000):
    base = rand_lines(rng.randint(4, 12))
    cur = list(base); oth = list(base)
    for lst in (cur, oth):
        for _ in range(rng.randint(1, 3)):
            i = rng.randrange(len(lst) + 1)
            op = rng.random()
            if op < 0.4 and lst: del lst[min(i, len(lst) - 1)]
            elif op < 0.8: lst.insert(i, rng.choice("abcxy{}"))
            elif lst: lst[min(i, len(lst) - 1)] = rng.choice("abcxy{}")
    files = [d / "cur", d / "base", d / "oth"]
    for f, lines in zip(files, (cur, base, oth)):
        f.write_text("".join(x + "\n" for x in lines))
    outs = {alg: mf((), ["--diff-algorithm=" + alg, *files]) for alg in ("myers", "histogram", "patience")}
    for alg in ("histogram", "patience"):
        if outs[alg] != outs["myers"]:
            found = (alg, outs)
            break
    if found:
        break
if not found:
    print(json.dumps({"found": False, "trials": trial + 1})); sys.exit(0)
alg, outs = found
cfg = mf(("-c", "diff.algorithm=" + alg), files)
default = mf((), files)
print(json.dumps({"found": True, "trial": trial, "alg": alg,
                  "default_equals_myers": default == outs["myers"],
                  "config_equals_myers": cfg == outs["myers"],
                  "config_equals_alg": cfg == outs[alg],
                  "rc": {"myers": outs["myers"][0], alg: outs[alg][0], "config": cfg[0]}}))
