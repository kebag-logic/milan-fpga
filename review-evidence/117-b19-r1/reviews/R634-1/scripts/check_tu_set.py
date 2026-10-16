#!/usr/bin/env python3
"""Compare the published 'tu set' and 'steady clear' times (per_step in
bench/gmNN/analysis.json, used by the 387 page) with the console health history
in the same file. Matches gm_summary.py's step selection. Usage: check_tu_set.py <author-dir>"""
import json, os, sys
auth = sys.argv[1]
SPLIT = 27.0
for r in range(1, 6):
    a = json.load(open(os.path.join(auth, 'bench', 'gm%02d' % r, 'analysis.json')))
    h = a['health']
    for k in (0, 1):
        lo, hi = (-9.0, SPLIT) if k == 0 else (SPLIT, 200.0)
        # the step entry the grader uses: the first whose bracket ends in the window
        ps = next(p for p in a['per_step'] if lo <= p['step']['bracket'][1] < hi)
        first_tu1 = next(t for t, v in h if lo <= t < hi and v.endswith('tu1'))
        clear = next(t for t, v in h if lo <= t < hi and t > first_tu1 and v == 'sync1 asc1 tu0')
        print('run %d %-8s first tu1 in health %.3f, published tu set %.3f (%+.3f s); health clear %.3f, published steady clear %.3f (%+.3f s); step bracket %s' % (
            r, ('takeover', 'release')[k], first_tu1, ps['tu_first_set'], ps['tu_first_set'] - first_tu1,
            clear, ps['tu_steady_clear'], ps['tu_steady_clear'] - clear, ps['step']['bracket']))
