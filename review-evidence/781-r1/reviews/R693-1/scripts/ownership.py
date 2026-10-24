"""Check that --ci-pieces --shard k/N listings own every --ci-pieces unit exactly once.
usage: python3 -I ownership.py <gates-dir> <N>"""
import collections, pathlib, sys
d, n = pathlib.Path(sys.argv[1]), int(sys.argv[2])
def units(p): return [w for w in p.read_text().split() if w]
allu = units(d / "list-ci-pieces.txt")
owners = collections.defaultdict(list)
for k in range(n):
    for u in units(d / f"shard-{k}-of-{n}.txt"): owners[u].append(k)
dup = {u: o for u, o in owners.items() if len(o) != 1}
missing = sorted(set(allu) - set(owners)); extra = sorted(set(owners) - set(allu))
print(f"ci-pieces units={len(allu)} distinct={len(set(allu))} owned={len(owners)} dup={dup} missing={missing} extra={extra}")
for k in range(n): print(k, " ".join(units(d / f"shard-{k}-of-{n}.txt")))
print("media_phase owner:", owners.get("media_phase"), " milan_dp_mclk__0 owner:", owners.get("milan_dp_mclk__0"))
ok = not dup and not missing and not extra and len(allu) == len(set(allu))
print("OWNERSHIP:", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
