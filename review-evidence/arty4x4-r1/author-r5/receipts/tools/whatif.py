"""Desk what-ifs for the Arty split points by the unchanged rule (round 2): the rule's row search (derive4.py's, the
r9 derive-own.py at arty-4x4) for N AAF streams each way on one interface, at a control CPU clock, from measured
cycles: N = 1 and N = 4 measured (round 9's 1x1 census and this lane's 4x4 census, both at aa53840d9, both with
#969's disposition), N = 2 and 3 interpolated linearly in N between them, cycle by cycle. The clock scales time
only: cycles unchanged, each cost by the rule (cycles / MHz x 1.05, rounded up to 5 us) at that clock.

The harness's arty-4x4 point is the vehicle: its counts (sources, sinks, counter descriptors, notices) and every
cost table the model reads are replaced by the what-if's; no other point enters.

usage: whatif.py N MHZ [--scale k=f ...] [--json OUT]     (cwd = checkout root)
"""
import argparse, json, math, sys
from pathlib import Path
from unittest.mock import patch
root = Path.cwd()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import arty_grade, edit_rows, load_grade, paced_rows, poll_grade, queued_bound, rows_grade as rg, rows_tiers as rt
import shape_costs as sc
import os
ONE = Path(os.environ.get('WHATIF_ONE', '$VALIDATION_STORAGE/artysplit-a829/r9/final-census/merged-census.json'))
FOUR = Path('$VALIDATION_STORAGE/arty4x4-a863/model/census1-969.json')
POINT = 'arty-4x4'
SHARE_US = 2000


def retry_raw(raw):
    """derive-own.py's retry fit in cycles: the cold start, the refused attempt and the notice."""
    rounds = {tuple(map(int, k.split(':'))): v['cycles'] for k, v in raw['rounds'].items()}
    k = max(k for n, k in rounds if n == 0)
    full = rounds[(0, k)]
    cold = max([rounds.get((0, 0), 0)] + [(cost * k - full * j) / (k - j) for (n, j), cost in rounds.items()
                                           if n == 0 and j < k])
    attempt = (full - cold) / k
    notice = max((cost - cold - j * attempt) / n for (n, j), cost in rounds.items() if n)
    return dict(cold=cold, attempt=attempt, notice=notice), rounds


def cycles_at(n):
    """Each cost's cycles and the retry fit's at N streams: measured at 1 and 4, linear in N between."""
    one, four = json.loads(ONE.read_text()), json.loads(FOUR.read_text())
    c1 = {k: v['cycles'] for k, v in one['costs'].items()}
    c4 = {k: v['cycles'] for k, v in four['costs'].items()}
    r1, r4 = retry_raw(one)[0], retry_raw(four)[0]
    mode = os.environ.get('WHATIF_COSTS', 'linear')
    f = {'linear': (n - 1) / 3, 'one': 0.0, 'four': 1.0}[mode]
    lin = lambda a, b: a + (b - a) * f  # noqa: E731
    basis = {1: 'measured (round 9, arty-1x1)', 4: 'measured (this lane, arty-4x4)'}.get(n, f'interpolated {f:.3f}')
    if mode != 'linear':
        basis = f'bound: every cost at the {"1x1" if mode == "one" else "4x4"} measurement, the counts at {n}x{n}'
    return {k: lin(c1[k], c4[k]) for k in c4}, {k: lin(r1[k], r4[k]) for k in r4}, basis


def rule(cycles, mhz):
    return math.ceil(cycles / mhz * 1.05 / 5 - 1e-9) * 5


def counts(n):
    """The shape's counts: N AAF each way and the CRF input; the CRF output from two AAF inputs (Milan 7.2.3)."""
    sources = n + (1 if n >= 2 else 0)
    sinks = n + 1
    text = sc.aecp_text(root)
    notices = sc.evaluated(text, 'AECP_NOTICES_MOST', {'CTRL_AEM_STREAM_INPUTS': sinks, 'CTRL_AEM_STREAM_OUTPUTS': sources,
                                                      'CTRL_AEM_AVB_INTERFACES': 1, 'CTRL_AEM_CLOCK_DOMAINS': 1,
                                                      'MBX_N_IF': 1})
    return dict(n_if=1, sources=sources, sinks_per_if=sinks, registrations=16,
                counter_descriptors=sources + sinks + 2, notices=notices)


POLL = {'base': 'base', 'withdraw': 'item.withdraw', 'rebuild': 'item.rebuild', 'walk': 'item.walk',
        'reclaim': 'item.reclaim', 'acmp': 'item.acmp', 'aecp': 'item.aecp', 'aecp_long': 'item.aecp_long',
        'acmp_declined': 'item.acmp_declined'}


def costs_us(cyc, retry, mhz, scale=None):
    """The rule's statements at the clock, each optionally scaled (a what-if cut, applied to cycles)."""
    scale = scale or {}
    cyc = {k: v * scale.get(k, 1.0) for k, v in cyc.items()}
    c = {k: rule(v, mhz) for k, v in cyc.items()}
    for slot, name in enumerate(('ADP', 'ACMP', 'MAAP', 'AECP')):
        c['event.' + name] = c['event.TIMER#' + str(slot)]
    c.update({'record.aecp': c['record.aecp.other'], 'item.retained': c['record.srp'], 'item.mrpdu': c['build_one'],
              'item.aecp.long': c['item.aecp_long'], 'item.aecp.notice': c['tx.aecp.notice'],
              'item.aecp.response': c['tx.aecp.response'], 'item.aecp.probe': c.get('tx.aecp.probe',
                                                                                   c['tx.aecp.response'])})
    r = {k: v * scale.get('retry.' + k, 1.0) for k, v in retry.items()}
    retry_us = {k: rule(v, mhz) for k, v in r.items()}
    return c, retry_us, cyc


def search(n, mhz, scale=None, quick=False):
    cyc, retry, basis = cycles_at(n)
    c, retry_us, cyc = costs_us(cyc, retry, mhz, scale)
    s = counts(n)
    h = rg.header(root, sc.Shape(1, 5, 5))
    h.update(CTRL_LOOP_STEP_PASS_US=c['step'], CTRL_LOOP_TICK_US=c['centisecond'], CTRL_LOOP_BUILD_PASS_US=c['build'],
             CTRL_LOOP_BUILD_ONE_PASS_US=c['build_one'], AECP_ROUND_COLD_US=retry_us['cold'],
             AECP_ATTEMPT_US=retry_us['attempt'], AECP_NOTICE_US=retry_us['notice'], AECP_NOTICES_MOST=s['notices'])
    rate, tick = rg.contract(root)
    built = rt.built_constants(root, POINT)
    i = rt.Inputs(h, c, s, rate, tick, 8, 1300, built[1], built[2], built[3], built[4], 9)
    paced = {'a one-row edit': max(c['paced.44'], c['paced.45']), 'an accepted SET_CONFIGURATION': c['paced.6']}
    poll = {**poll_grade.STATED_US[sc.Shape(1, 5, 5)], **{k: c[v] for k, v in POLL.items()},
            'retained': c['record.srp'], 'mrpdu': 0}
    load_h = {**load_grade.macros(root, sc.Shape(1, 5, 5)), **h}
    with patch.dict(edit_rows.PACED, {POINT: paced}), patch.dict(edit_rows.EDIT_RECORD_US, {POINT: max(paced.values())}), \
            patch.dict(load_grade.POINTS, {POINT: s}), patch.dict(load_grade.STATED_US, {POINT: c}), \
            patch.dict(poll_grade.STATED_US, {sc.Shape(1, 5, 5): poll}), \
            patch.dict(rt.DATAPATH_US, {POINT: {k: c['event.' + k] for k in rt.DATAPATH}}), \
            patch.dict(rt.LONG_RECORD_US, {POINT: c['record.aecp.long']}), \
            patch.dict(rt.LONG_NOTICE_US, {POINT: c['item.aecp_long']}), \
            patch.dict(rg.ROW_COSTS, {POINT: {'event.LINK': c['event.LINK']}}), \
            patch.object(load_grade, 'macros', lambda *a: load_h):
        terms = load_grade.load(root, POINT, load_grade.STATED_US)
        load = sum(terms.values())
        out = []
        for queued in ((140,) if quick else (125, 130, 135, 140)):
            for pace in range(1, paced_rows.PACE_MOST_MS + 1):
                base = i._replace(h={**h, 'AECP_QUEUED_MS': queued}, pace_ms=pace)
                with patch.object(rt, 'point_inputs', lambda *a: base):
                    sl, margin = rt.slice_choice(root, POINT)
                at = base._replace(slice_us=sl)
                with patch.object(rt, 'point_inputs', lambda *a: at):
                    taken = paced_rows.choice(root, POINT)
                full = rt.rows(root, POINT, rt.BUILT, at)
                rows = {k: v for k, (v, _) in full.items()}
                owner = arty_grade.owner_findings(load, rows)
                ok = taken == pace and queued_bound.ruled(rows['last']) == queued and sl >= c['build_one'] and not owner
                out.append(dict(queued_ms=queued, pace_ms=pace, slice_us=sl, pace_rule=taken,
                                queued_rule=queued_bound.ruled(rows['last']), rows_ms=rows, owner=owner, qualifies=ok,
                                terms={k: full[k][1] for k in ('ACMP', 'txL', 'last')}))
    share_us = cyc['share'] / mhz
    return dict(n=n, mhz=mhz, basis=basis, counts=s, load=load, load_terms=terms, share_us=share_us,
                share_ok=share_us <= SHARE_US, costs_us=c, retry_us=retry_us, candidates=out)


def excess(r):
    """How far a candidate is from every owner bound: the worst ratio of row to bound (load and THE SHARE apart)."""
    b = dict(arty_grade.OWNER_MS)
    return max((r['rows_ms'][k] or 1e9) / v for k, v in b.items())


def summary(res):
    c = res['candidates']
    q = [r for r in c if r['qualifies']]
    best = min(q, key=lambda r: (r['pace_ms'], r['queued_ms'], r['slice_us'])) if q else min(c, key=excess)
    least = {k: min(r['rows_ms'][k] or 1e9 for r in c) for k in ('ACMP', 'txL', 'last')}
    return dict(n=res['n'], mhz=res['mhz'], basis=res['basis'], counts=res['counts'], load=round(res['load'], 4),
                share_ms=round(res['share_us'] / 1000, 3), qualifying=len(q), best=dict(
                    queued_ms=best['queued_ms'], pace_ms=best['pace_ms'], slice_us=best['slice_us'],
                    rows_ms=best['rows_ms'], owner=best['owner'], qualifies=best['qualifies']), least=least,
                status=('ROW' if q and res['load'] <= 0.70 and res['share_ok'] else 'NO ROW'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int)
    ap.add_argument('mhz', type=int)
    ap.add_argument('--scale', nargs='*', default=[])
    ap.add_argument('--json')
    a = ap.parse_args()
    scale = {k: float(v) for k, v in (x.split('=') for x in a.scale)}
    res = search(a.n, a.mhz, scale)
    s = summary(res)
    print(json.dumps(s, indent=1))
    if a.json:
        Path(a.json).write_text(json.dumps(dict(summary=s, scale=scale, **res), indent=1) + '\n')
