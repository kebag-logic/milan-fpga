"""table7.py: the attribution experiment's figures from analyse7.sh's surveys, per image and repeat.

usage: python3 -I table7.py R7ATTR IMG...
For each image: srp-talker-held's record.srp, item.reclaim, item.record and the polls' base (the ordinary view's
costs.json), its run's SUMMARY (instructions, ROM fetches, CPU cycles), and the notice leg's AECP notice item (ordinary
view, aecp-fanout) and long notice (long view, aecp-largest-notice), each in cycles and by the rule."""
import gzip
import json
import math
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
rule = lambda c: int(math.ceil(c * 1.05 / 100 / 5 - 1e-9) * 5)  # noqa: E731


def costs(view: Path) -> dict:
    f = view / 'costs.json'
    return json.loads(f.read_text())['_most_cycles'] if f.is_file() else {}


def summary(results: Path, group: str) -> dict:
    for name in (f'{group}.log', f'{group}.log.gz'):
        f = results / name
        if f.is_file():
            opener = gzip.open if name.endswith('.gz') else open
            with opener(f, 'rt') as h:
                for line in h:
                    if line.startswith('SUMMARY '):
                        return dict(kv.split('=', 1) for kv in line.split()[1:] if '=' in kv)
    return {}


rows = []
for img in sys.argv[2:]:
    for k in (1, 2, 3):
        s = costs(root / f'out/{img}-rep{k}/survey/ordinary-costs')
        o = costs(root / f'out/notice-{img}-rep{k}/survey/ordinary-costs')
        lg = costs(root / f'out/notice-{img}-rep{k}/survey/long-costs')
        m = summary(root / f'{img}/rep{k}/results', 'srp-talker-held')
        rc = (root / f'{img}/rep{k}.rc').read_text().strip() if (root / f'{img}/rep{k}.rc').is_file() else '-'
        nrc = (root / f'notice-{img}/rep{k}.rc').read_text().strip() if (root / f'notice-{img}/rep{k}.rc').is_file() else '-'
        rows.append(dict(img=img, rep=k, rc=rc, nrc=nrc, srp=s.get('record.srp'), reclaim=s.get('item.reclaim'),
                         record=s.get('item.record'), base=s.get('base'), aecp=o.get('item.aecp'),
                         long=lg.get('item.aecp_long'), instr=m.get('instr'), cpu=m.get('cpu'),
                         fetch=m.get('fetch_rom', '').split('/')[0]))


def f(v):
    return '-' if v is None or v == '' else f'{int(v):,}'


def u(v):
    return '-' if v is None else str(rule(int(v)))


print('| Image | Rep | rc | record.srp | rule | item.reclaim | rule | item.record | polls base | AECP notice item | rule '
      '| long notice | rule | instructions | ROM fetches | CPU cycles |')
print('|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
for r in rows:
    print(f"| {r['img']} | {r['rep']} | {r['rc']}/{r['nrc']} | {f(r['srp'])} | {u(r['srp'])} | {f(r['reclaim'])} | "
          f"{u(r['reclaim'])} | {f(r['record'])} | {f(r['base'])} | {f(r['aecp'])} | {u(r['aecp'])} | {f(r['long'])} | "
          f"{u(r['long'])} | {f(r['instr'])} | {f(r['fetch'])} | {f(r['cpu'])} |")
json.dump(rows, open(root / 'out/table7.json', 'w'), indent=1)
