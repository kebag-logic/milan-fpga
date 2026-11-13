"""Reviewer probe: the last record of a non-AECP tier-1 channel's burst (ACMP, ADP, MAAP) by every source under the
built design (rows_tiers.BUILT), the analogue of R4 for a channel that AECP-first now serves after AECP.
usage: python3 -I tier1_other_rows.py <repo-root> [--lean]
--lean: the fewest passes (every tier-1 record past its cap, no pass lost to a centisecond), optimistic for the row.
The model reuses rows_tiers.tiered's per-pass terms for row R4 and replaces its tier-1 terms:
  own     the channel's own burst, each at its stated cost (its refills come after its last record of the burst);
  aecp    every AECP record arriving in the window (AECP-first: none of the channel's is taken while one waits);
  others  each remaining tier-1 channel's arrivals, at most its cap in each pass (in turn);
and the passes: AECP's (its arrivals' cost over CTRL_LOOP_DRAIN_US, past its cap), the channel's burst at its cap a
pass, a pass per centisecond (THE TICK's cap), and the pass running at arrival."""
import math, sys
from pathlib import Path
root = Path([a for a in sys.argv[1:] if not a.startswith('--')][0]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import rows_tiers as rt  # noqa: E402

LEAN = '--lean' in sys.argv

def row_terms(ch, i, w_ms, d):
    h, c, s, rate, tick_ms = i[:5]
    cap = h['CTRL_LOOP_RX_PER_PASS']
    arrive = lambda o: rate[o][0] + math.floor(w_ms / rate[o][1])
    ticks = math.floor(w_ms / tick_ms) + 1
    aecp_us = arrive('aecp') * c['record.aecp']
    passes = math.ceil((aecp_us + h['AECP_ROUND_COLD_US'] + h['AECP_NOTICE_US']) / h['CTRL_LOOP_DRAIN_US']) + \
        math.ceil(rate[ch][0] / cap) + ticks + 1
    if LEAN:
        # the fewest passes: every tier-1 record in the window taken past its cap to CTRL_LOOP_DRAIN_US, no pass lost
        # to a centisecond or to a pass's own work (optimistic for the row)
        t1 = aecp_us + rate[ch][0] * c[f'record.{ch}'] + sum(arrive(o) * c[f'record.{o}'] for o in rt.TIER1
                                                            if o not in ('aecp', ch))
        passes = math.ceil(t1 / h['CTRL_LOOP_DRAIN_US']) + 1
    base = rt.tiered('R4', i, w_ms, d)
    # recompute the per-pass terms at this row's passes by re-running tiered's pass-dependent terms
    out = {k: v for k, v in base.items() if k not in ('aecp', 'others')}
    import load_grade, rows_grade
    out['timers'] = rows_grade.timer_us(s, c, w_ms, passes, rate)
    gm = sum(math.floor(w_ms / ms) + 1 for ms in load_grade.GM_INTERVALS_MS)
    out['gm'] = s['n_if'] * min(passes, gm) * c['event.GM']
    out['item.walk'] = min(passes * s['n_if'], s['n_if'] * ticks) * c['item.walk']
    per_slice = max(1, math.floor((d.slice_us - c['events_none']) / c['record.srp']))
    out['item.reclaim'] = min(2 * s['n_if'] * passes, 2 * per_slice) * c['item.reclaim']
    out['item.acmp'] = min(passes, arrive('acmp') + arrive('adp') + s['n_if'] * s['sinks_per_if']) * c['item.acmp']
    out['item.aecp'] = min(passes, arrive('aecp') + s['n_if'] * s['registrations']) * c['item.aecp']
    out['passes'] = passes * (c['events_none'] + c['base'])
    out['datapath'] = passes * rt.datapath_pass_us(c, s)
    out['own'] = rate[ch][0] * c[f'record.{ch}']
    out['aecp'] = aecp_us
    out['others'] = sum(min(arrive(o), passes * cap) * c[f'record.{o}'] for o in rt.TIER1 if o not in ('aecp', ch))
    return out, passes

def solve(ch, i, d):
    w = 0.01
    while w < 2000:
        t, n = row_terms(ch, i, w, d)
        total = sum(t.values()) / 1000
        if total <= w:
            return w, t, n
        w = max(w + 0.01, math.ceil(total * 100) / 100)
    return None, t, n

for point in ('1x1/1if', '8x8/2if'):
    i = rt.point_inputs(root, point)
    d = rt.at_point(rt.BUILT, i)
    r4 = rt.rows(root, point, rt.BUILT, i)['R4'][0]
    print(f'{point}: slice {d.slice_us} us; rows_tiers R4 (AECP) {r4:.2f} ms; bursts', {o: i.rate[o] for o in rt.TIER1},
          'costs', {o: i.c[f"record.{o}"] for o in rt.TIER1})
    for ch in ('acmp', 'adp', 'maap'):
        w, t, n = solve(ch, i, d)
        top = ', '.join(f'{k} {v/1000:.3f}' for k, v in sorted(t.items(), key=lambda kv: -kv[1]))
        print(f'  {ch} last record of its burst: W {w:.2f} ms against 20 ms ({"OVER" if w > 20 else "fits"}), passes {n}: {top}')
