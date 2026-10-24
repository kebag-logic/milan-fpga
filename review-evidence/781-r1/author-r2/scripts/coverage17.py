"""Check that the 17 --ci-pieces shard lists own every unit of the --ci-pieces inventory exactly once.
usage: python3 -I coverage17.py <coverage dir>"""
import collections, pathlib, sys
d = pathlib.Path(sys.argv[1])
full = d.joinpath("list-ci-pieces.txt").read_text().split()
owned = collections.Counter()
owner = {}
for k in range(17):
    for unit in d.joinpath(f"shard-{k}-of-17.txt").read_text().split():
        owned[unit] += 1
        owner[unit] = k
dup = sorted(u for u, n in owned.items() if n != 1)
missing = sorted(set(full) - set(owned))
extra = sorted(set(owned) - set(full))
print(f"inventory units {len(full)} (distinct {len(set(full))}), owned {sum(owned.values())} (distinct {len(owned)})")
print(f"owned more than once: {dup}")
print(f"missing from every shard: {missing}")
print(f"owned but not in inventory: {extra}")
print(f"media_phase owner: {owner.get('media_phase')}/17; milan_dp_mclk__0 owner: {owner.get('milan_dp_mclk__0')}/17 "
      f"(alone: {d.joinpath('shard-16-of-17.txt').read_text().split() == ['milan_dp_mclk__0']})")
ok = not dup and not missing and not extra and len(full) == len(set(full))
print("coverage:", "PASS every unit owned exactly once" if ok else "FAIL")
sys.exit(0 if ok else 1)
