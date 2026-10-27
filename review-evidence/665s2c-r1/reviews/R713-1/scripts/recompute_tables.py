"""Recompute each archived arm's table.md with the checkout's run.table() from the archived
per-group graded JSONs, and compare with the archived head regrade; also compare the JSON hashes.
Group order is taken from the pre-rebase table's probe rows (order only).
usage: recompute_tables.py CHECKOUT RUNS_DIR REGRADE_ARMS_DIR"""
import hashlib
import json
import re
import sys
from pathlib import Path

checkout, runs, arms = map(Path, sys.argv[1:4])
sys.path.insert(0, str(checkout / 'tb/verilator/ctrl_service_budget'))
import run  # noqa: E402

bad = 0
for arm in sorted(p.name for p in runs.iterdir()):
    reg = arms / arm
    if not (reg / 'table.md').is_file():
        print(f'{arm}: no regrade table'); continue
    groups = {p.stem: json.loads(p.read_text()) for p in (runs / arm).glob('*.json')
              if p.stem not in ('results',)}
    hashes = dict(reversed(l.split()) for l in (reg / 'json_sha256.txt').read_text().splitlines() if l.strip())
    jmis = [g for g in groups if hashes.get(g + '.json') != hashlib.sha256((runs / arm / (g + '.json')).read_bytes()).hexdigest()]
    missing = sorted(set(k[:-5] for k in hashes if k.endswith('.json') and k != 'results.json') - set(groups))
    order, seen = [], set()
    probe_group = {r['probe']: g for g, d in groups.items() for r in d['probes']}
    for m in re.finditer(r'^\| [^|]+ \| `([^`]+)` \|', (runs / arm / 'table.md').read_text(), re.M):
        g = probe_group.get(m.group(1))
        if g and g not in seen:
            seen.add(g); order.append(g)
    order += [g for g in groups if g not in seen]
    point = '1x1' if arm[1] == '1' else '8x8'
    text = run.table([groups[g] for g in order], point)
    same = text == (reg / 'table.md').read_text()
    bad += (not same) + bool(jmis) + bool(missing)
    print(f'{arm}: groups {len(groups)}; json identical to head regrade: {not jmis} {jmis or ""} '
          f'missing {missing or "-"}; recomputed table == head regrade table: {same}')
print('mismatches', bad)
