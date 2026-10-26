"""Recompute each arm's composed-maximum record and table lines with the head's run.py from
published per-arm results.json 'results' lists (or per-group grade json files when results.json
is absent), and compare with the author's published head-regrade records and tables.
Usage: python3 -I recompute_composed.py <harness dir> <runs dir> <head-regrade dir>"""
import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1]); sys.dont_write_bytecode = True
import run
runs, regrade = Path(sys.argv[2]), Path(sys.argv[3])
published = json.loads((regrade / 'composed_maximum_records.json').read_text())
bad = 0
for arm in sorted(published):
    rj = runs / arm / 'results.json'
    if rj.exists():
        results = json.loads(rj.read_text())['results']; src = 'results.json'
    else:
        order = [l.split('|')[1].strip() for l in (runs / arm / 'table.md').read_text().splitlines()
                 if l.startswith('| ') and l.count('|') == 7 and (runs / arm / (l.split('|')[1].strip() + '.json')).exists()]
        rest = [p.stem for p in sorted((runs / arm).glob('*.json')) if p.stem not in order]
        results = [json.loads((runs / arm / f'{g}.json').read_text()) for g in order + rest]
        src = 'group json, run order from table.md'
    mine = run.composed_maximum(results)
    point = '8x8' if arm.endswith('8') else '1x1'
    lines = [l for l in run.table(results, point).splitlines() if l.startswith(('Composed maximum', 'Over the windows'))]
    tab = regrade / arm / 'table.md'
    theirs = [l for l in tab.read_text().splitlines() if l.startswith(('Composed maximum', 'Over the windows'))] if tab.exists() else None
    ok = mine == published[arm] and (theirs is None or theirs == lines)
    bad += not ok
    print(f'{arm} ({src}, {len(results)} groups): record {"==" if mine == published[arm] else "!="} published; '
          f'table lines {"==" if theirs == lines else "!=" if theirs is not None else "(no table)"}')
    for l in lines: print('   ', l)
print('arms differing:', bad); sys.exit(1 if bad else 0)
