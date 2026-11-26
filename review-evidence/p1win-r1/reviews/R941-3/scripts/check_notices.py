"""Recompute the notice arms' worst rows from the published results.json and rc files (independent of notices_r3.py).
usage: python3 -I check_notices.py <r3 author/notice-arms dir>"""
import json, sys
from pathlib import Path
d = Path(sys.argv[1])
for pt in ('1x1', '8x8-1if'):
    for arm in ('answering-later', 'answering-every-port', 'talker-notices'):
        r = json.loads((d / f'{pt}-{arm}-results.json').read_text())
        rc = (d / f'{pt}-{arm}-rc.txt').read_text().split()[-1]
        idn = (d / f'{pt}-{arm}-identity.txt').read_text()
        rows = r['notices']
        paths = {}
        for n in rows:
            paths.setdefault(n['path'][0], []).append(n)
        s = ', '.join(f"{p}: n={len(v)} worst={max(x['ms'] for x in v):.3f} bound={sorted({x['budget_ms'] for x in v})} "
                      f"over={sum(x['ms'] > x['budget_ms'] for x in v)}/{sum(not x['within_budget'] for x in v)}"
                      for p, v in sorted(paths.items()))
        q = paths.get('notice.queued', [])
        firsts = {}
        for n in q:
            firsts[n['group']] = min(firsts.get(n['group'], 1e9), n['ms'])
        f = f'; first-of-queue worst {max(firsts.values()):.3f}' if firsts else ''
        point_ok = r['point'] if isinstance(r['point'], str) else json.dumps(r['point'])
        print(f"{pt} {arm}: rc {rc}, head ok {'079c4fa1514be460949ddc28ae3277ea1873cb48' in idn}, groups {len(r['results'])}, "
              f"refusals {len(r['refusals'])}, misses {len(r['misses'])}, notice_misses {len(r['notice_misses'])}, point {point_ok[:40]}; {s}{f}")
