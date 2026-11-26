"""notices_r3.py RUNS_DIR UNITS_DIR: the notice arms' rows at both points, from each run's results.json: per arm and
point the rc, groups, refusals, notice_misses, and the worst row of each notice path against its bound."""
import json, sys
from pathlib import Path
runs, units = Path(sys.argv[1]), Path(sys.argv[2])
bad = 0
for arm in ('answering-later', 'answering-every-port', 'talker-notices'):
    for pt in ('1x1', '8x8-1if'):
        r = runs / f'r3-{arm}-{pt}'
        d = json.loads((r / 'results.json').read_text())
        rc = (units / f'r3-{arm}-{pt}.rc').read_text().strip()
        rows = d['notices']
        print(f"== {arm} at {pt}: rc {rc}, {len(d['results'])} groups, refusals {len(d['refusals'])}, "
              f"notice rows {len(rows)}, notice_misses {len(d['notice_misses'])}, misses {len(d['misses'])}")
        for m in d['notice_misses']:
            print('  MISS', m)
        bad += rc != '0' or bool(d['notice_misses']) or not rows
        for path in sorted({n['path'][0] for n in rows}):
            sel = [n for n in rows if n['path'][0] == path]
            w = max(sel, key=lambda n: n['ms'])
            over = sum(not n['within_budget'] for n in sel)
            print(f"  {path}: {len(sel)} rows, worst {w['ms']:.3f} ms ({w.get('probe') or w['group']}), "
                  f"best {min(n['ms'] for n in sel):.3f} ms, bound {w['budget_ms']:g} ms, over {over}")
            if path.endswith('queued'):
                for g in sorted({n['group'] for n in sel}):
                    q = [n['ms'] for n in sel if n['group'] == g]
                    print(f"    {g}: first {min(q):.3f} ms, last {max(q):.3f} ms, {len(q)} notices")
print('ALL ARMS: ' + ('PASS' if not bad else f'{bad} arm(s) not clean'))
