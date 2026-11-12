"""Each leg's least row margin: over every measured probe within its budget, the smallest budget less its time, with
the probe; and the misses (over their budget). usage: least_margin.py RESULTS_JSON..."""
import json, sys
for path in sys.argv[1:]:
    d = json.load(open(path))
    best, misses = None, 0
    for g in d['results']:
        for r in g['probes']:
            if r.get('status') != 'measured' or r.get('budget_ms') is None or r.get('ms') is None:
                continue
            m = r['budget_ms'] - r['ms']
            if m < 0:
                misses += 1
                continue
            if best is None or m < best[0]:
                best = (m, r['ms'], r['budget_ms'], r['probe'], g['group'])
    print(f"{path.split('/builds/')[-1].split('/')[0]}: least margin {best[0]:.3f} ms ({best[3]} in {best[4]}: {best[1]:.3f} "
          f"of {best[2]} ms); {misses} over")
