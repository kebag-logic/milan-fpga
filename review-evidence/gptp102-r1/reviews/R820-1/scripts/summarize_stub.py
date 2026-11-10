#!/usr/bin/env python3
"""Summarise the fake-toolchain probe receipts written by stub_probes.sh.
usage: summarize_stub.py <receipts/stub>"""
import collections, hashlib, json, re, sys
from pathlib import Path
d = Path(sys.argv[1])
rd = lambda n: (d / n).read_text().strip()
print("1. jobs comparison test vs planted faults (rc 0 = test PASSES, 1 = test FAILS)")
for v in ("none", "order", "print", "droplast", "abort", "short", "shared"):
    log = rd(f"test-{v}.log")
    fails = [l[5:] for l in log.splitlines() if l.startswith("FAIL ")]
    tally = re.findall(r"^\d+ checks: .*$", log, re.M)[-1]
    left = re.search(r"leftover-in-TMPDIR: (\d+)", log).group(1)
    print(f"  {v:9s} rc {rd(f'test-{v}.rc')}  {tally}  leftover {left}  failed: {fails}")
print("2. direct runs, full list, fake toolchain")
for n in ("head-j1", "head-j4", "head-j8", "head-j16", "base-serial"):
    b = (d / f"{n}.stdout").read_bytes()
    print(f"  {n:11s} rc {rd(n + '.rc')} {len(b)} bytes sha256 {hashlib.sha256(b).hexdigest()} "
          f"tally {b.decode().strip().splitlines()[-1]!r}")
for j in (1, 4, 8, 16):
    recs = [json.loads(l) for l in open(d / f"dirs-j{j}.jsonl")]
    runs = [p for k, p, _ in recs if k == "run"]
    builds = [p for k, p, _ in recs if k == "build"]
    owners = collections.Counter(p.split("/mutant-")[1].split("/")[0]
                                 for p in runs if "/mutant-" in p)
    print(f"  --jobs {j:2d}: run dirs {len(runs)} unique {len(set(runs))}; build dirs "
          f"{len(builds)} unique {len(set(builds))}; per-mutant dirs {len(owners)}, "
          f"max runs per dir {max(owners.values())}; threads {len({t for *_, t in recs})}")
print("3. a task raising OSError at mutant index 5")
a, b = (d / "raise-j1.stdout").read_bytes(), (d / "raise-j4.stdout").read_bytes()
for j in (1, 4):
    print(f"  --jobs {j}: rc {rd(f'raise-j{j}.rc')}, last stderr line "
          f"{rd(f'raise-j{j}.stderr').splitlines()[-1]!r}, "
          f"{re.search(r'leftover-in-TMPDIR: (\d+)', rd(f'raise-j{j}.log')).group(0)}")
print(f"  stdout identical across --jobs 1 and 4: {a == b} ({len(a.splitlines())} lines)")
print("4. SIGINT 5 s into a run (fake harness runs up to 2 s each)")
for j in (1, 4):
    print(f"  --jobs {j}: rc {rd(f'sigint{j}.rc')}; " + "; ".join(rd(f"sigint{j}.log").splitlines()))
print("5. --jobs argument and default")
for a_ in ("0", "-1", "2.5", "x"):
    print(f"  --jobs {a_}: rc {rd(f'arg-{a_}.rc')}: {rd(f'arg-{a_}.log').splitlines()[-1]}")
for c in ("112", "112-114", "112-127"):
    usable, dflt = rd(f"default-{c}.log").split()
    print(f"  affinity {c}: usable CPUs {usable}, default_jobs {dflt}")
