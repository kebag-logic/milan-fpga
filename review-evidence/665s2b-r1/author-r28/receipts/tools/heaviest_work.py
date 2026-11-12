"""The heaviest work pass of each leg's results.json, its group, and the share's margin; and every class's heaviest
over its stated limit (whole passes). usage: heaviest_work.py RESULTS_JSON..."""
import json, sys
for path in sys.argv[1:]:
    d = json.load(open(path))
    best = max(((g['passes']['worst']['cycles'], g['group']) for g in d['results'] if g['passes'].get('worst')), default=None)
    over = sum(g['passes']['share']['over'] for g in d['results'])
    passes = sum(g['passes']['share']['passes'] for g in d['results'])
    print(f"{path.split('/builds/')[-1].split('/')[0]}: heaviest work pass {best[0]:,} cycles ({best[1]}), "
          f"{200000 - best[0]:,} under the share; {over} of {passes:,} over it")
