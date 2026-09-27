"""Exercise the addendum's stop assertion, fit and distribution functions.

Usage: python3 addendum_function_probe.py EVIDENCE_DIR
Imports author-r2/recompute.py without running its main (the raw captures
are private), then checks that its stop assertion rejects every non-stop
shape and that its statistics reproduce the published summary from the
published per-attempt rows.
"""
import csv
import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stop_check_probe import t_quantile  # noqa: E402

fails = []


def check(ok, what):
    print(('PASS ' if ok else 'FAIL ') + what)
    if not ok:
        fails.append(what)


def raises(fn, *args):
    try:
        fn(*args)
    except AssertionError:
        return True
    return False


def main():
    ev = Path(sys.argv[1])
    spec = importlib.util.spec_from_file_location('recompute', ev / 'author-r2' / 'recompute.py')
    rc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rc)
    ack = 5_000_000_000
    check(not raises(rc.assert_stop, 0, ack, ack), 'assert_stop accepts zero settled PDUs with first PDU at the response')
    check(not raises(rc.assert_stop, 0, ack + 19_000_000, ack), 'assert_stop accepts zero settled PDUs with first PDU after the response')
    check(raises(rc.assert_stop, 1, ack + 1, ack), 'assert_stop rejects one settled PDU')
    check(raises(rc.assert_stop, 750, ack + 300_000, ack), 'assert_stop rejects continuous hold traffic (750 settled PDUs)')
    check(raises(rc.assert_stop, 0, ack - 1, ack), 'assert_stop rejects a zero count whose first post-settle PDU precedes the response')
    rows = list(csv.DictReader((ev / 'author-r2' / 'stop-checks.csv').open()))
    summ = json.loads((ev / 'author-r2' / 'recomputed-summary.json').read_text())
    for d in ('listener', 'talker'):
        acc = [dict(cycle=int(r['cycle']), latency_s=float(r['latency_s'])) for r in rows if r['direction'] == d and r['classification'] == 'RESTART']
        dist, fit = rc.distribution(acc), rc.fit(acc)
        check(dist == summ[d]['demonstrated'], f'{d}: addendum distribution() on published rows reproduces summary {dist}')
        check(all(abs(fit[k] - summ[d]['fit'][k]) < 1e-15 for k in ('slope_s_per_cycle', 'ci95_low', 'ci95_high')), f'{d}: addendum fit() reproduces summary')
        exact = t_quantile(0.975, fit['degrees_of_freedom'])
        check(abs(fit['t_975'] - exact) < 5e-7, f"{d}: series-expanded t {fit['t_975']:.9f} vs exact {exact:.9f} (df {fit['degrees_of_freedom']})")
    print('RESULT', 'PASS' if not fails else f'FAIL ({len(fails)})')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
