"""Independent stop-check and statistics probe for the #75 round-2 page.

Usage: python3 stop_check_probe.py EVIDENCE_DIR PAGE
EVIDENCE_DIR is the published review-evidence/75-r1 directory (it holds
author/ and author-r2/). PAGE is the findings page at the head under review.
Reads only; prints a receipt and exits non-zero on the first failed check.
"""
import csv
import hashlib
import json
import math
import re
import statistics as st
import sys
from pathlib import Path

PERIOD_S = 0.002
SETTLE_NS = 500_000_000
HOLD_NS = 2_000_000_000
fails = []


def check(ok, what):
    print(('PASS ' if ok else 'FAIL ') + what)
    if not ok:
        fails.append(what)


# Student-t quantile from the regularised incomplete beta function.
def betacf(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / d
    h = d
    for m in range(1, 400):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 / (1 + aa * d); c = 1 + aa / c; h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 / (1 + aa * d); c = 1 + aa / c; de = d * c; h *= de
        if abs(de - 1) < 1e-15:
            break
    return h


def ibeta(a, b, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lb = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    if x < (a + 1) / (a + b + 2):
        return math.exp(lb) * betacf(a, b, x) / a
    return 1 - math.exp(lb) * betacf(b, a, 1 - x) / b


def t_cdf(t, df):
    p = 0.5 * ibeta(df / 2, 0.5, df / (df + t * t))
    return 1 - p if t > 0 else p


def t_quantile(q, df):
    lo, hi = 0.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if t_cdf(mid, df) < q else (lo, mid)
    return (lo + hi) / 2


def ols(points):
    x = [p[0] for p in points]; y = [p[1] for p in points]; n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x)
    slope = sum((a - mx) * (b - my) for a, b in zip(x, y)) / sxx
    icpt = my - slope * mx
    se = math.sqrt(sum((b - icpt - slope * a) ** 2 for a, b in zip(x, y)) / (n - 2) / sxx)
    t = t_quantile(0.975, n - 2)
    return n, slope, slope - t * se, slope + t * se, t


def dist(values):
    y = sorted(values)
    return len(y), min(y), st.median(y), y[math.ceil(0.95 * len(y)) - 1], max(y)


def table_rows(text, header_prefix):
    lines = text.splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith(header_prefix))
    rows = []
    for l in lines[start + 2:]:
        if not l.startswith('|'):
            break
        rows.append([c.strip() for c in l.strip('|').split('|')])
    return rows


def main():
    ev, page_path = Path(sys.argv[1]), Path(sys.argv[2])
    page = page_path.read_text()
    a1, a2 = ev / 'author', ev / 'author-r2'
    rows = list(csv.DictReader((a2 / 'stop-checks.csv').open()))
    check(len(rows) == 200, f'stop-checks.csv has 200 attempt rows ({len(rows)})')
    I = lambda r, k: int(r[k])
    F = lambda r, k: float(r[k])

    # A. My own stop predicate from the recorded window counts and timestamps.
    mine, window_bad = {}, 0
    for r in rows:
        key = (r['direction'], I(r, 'cycle'))
        dr, sb, cc, ack = (I(r, k) for k in ('disconnect_response_ns', 'settle_begin_ns', 'connect_command_ns', 'response_ns'))
        check_ok = (sb == dr + SETTLE_NS and cc - dr >= HOLD_NS and ack > cc
                    and I(r, 'settled_to_response_pdus') == I(r, 'settled_to_command_pdus') + I(r, 'command_to_response_pdus')
                    and I(r, 'last_before_settle_ns') < sb <= I(r, 'first_after_settle_ns')
                    and abs((I(r, 'first_post_response_ns') - ack) / 1e9 - F(r, 'latency_s')) < 1e-12)
        if not check_ok:
            window_bad += 1
            print(f'FAIL {key} window arithmetic')
        stopped = (I(r, 'settled_to_response_pdus') == 0 and I(r, 'last_half_second_pdus') == 0
                   and I(r, 'first_after_settle_ns') >= ack
                   and I(r, 'first_after_settle_ns') == I(r, 'first_post_response_ns'))
        mine[key] = 'RESTART' if stopped else 'NOT_RESTART'
    check(window_bad == 0, f'window arithmetic (settle = response + 0.5 s, hold >= 2 s, count sums, latency) on 200 rows; {window_bad} bad')
    agree = [k for k in mine if mine[k] == next(r['classification'] for r in rows if (r['direction'], int(r['cycle'])) == k)]
    check(len(agree) == 200, f'independent stop predicate agrees with published classification on {len(agree)}/200')
    nr = sorted(k for k, v in mine.items() if v != 'RESTART')
    print('INFO independent NOT_RESTART set:', nr)
    check(nr == [('talker', 13), ('talker', 24), ('talker', 75)], 'non-restarts are exactly talker 13, 24, 75')
    sub = sorted((r['direction'], I(r, 'cycle'), F(r, 'latency_s')) for r in rows if F(r, 'latency_s') < PERIOD_S)
    print('INFO sub-PDU-period intervals:', sub)
    check(all(mine[(d, c)] == 'NOT_RESTART' for d, c, _ in sub), 'every sub-PDU-period interval is a NOT_RESTART')
    check(all(r['stop_check'] in ('PASS', 'FAIL') for r in rows), 'every attempt carries a recorded stop check')
    for d in ('listener', 'talker'):
        acc = [r for r in rows if r['direction'] == d and mine[(d, I(r, 'cycle'))] == 'RESTART']
        gaps = [F(r, 'silence_gap_s') for r in acc]
        print(f'INFO {d} restart silence gap min/max s: {min(gaps):.6f} / {max(gaps):.6f}')
        check(min(gaps) > 1.5, f'{d}: every accepted restart shows > 1.5 s recorded silence spanning the settled hold')
        check(min(F(r, 'latency_s') for r in acc) > PERIOD_S, f'{d}: no accepted restart interval is below one PDU period')
    for r in rows:
        if mine[(r['direction'], I(r, 'cycle'))] == 'NOT_RESTART':
            check(I(r, 'disconnect_to_command_pdus') == 1000 and I(r, 'last_half_second_pdus') == 250
                  and F(r, 'maximum_hold_gap_s') < 2 * PERIOD_S,
                  f"talker {r['cycle']}: 1000 hold PDUs, 250 final-half PDUs, max gap {r['maximum_hold_gap_s']} s")

    # Counters: wire classification versus retained start/stop deltas.
    for d in ('listener', 'talker'):
        ser = [r for r in rows if r['direction'] == d]
        ok = all((I(r, 'active_start_delta'), I(r, 'active_stop_delta')) == ((1, 1) if mine[(d, I(r, 'cycle'))] == 'RESTART' else (0, 0)) for r in ser)
        check(ok, f'{d}: active-talker start/stop delta is 1/1 for each restart and 0/0 for each non-restart')
        tot = (sum(I(r, 'active_start_delta') for r in ser), sum(I(r, 'active_stop_delta') for r in ser))
        print(f'INFO {d} summed active deltas {tot}')
        if d == 'listener':
            check(all(I(r, 'dut_start_delta') == 0 == I(r, 'dut_stop_delta') for r in ser), 'listener: inactive DUT output deltas all zero')
    summ = json.loads((a2 / 'recomputed-summary.json').read_text())
    check(summ['talker']['active_counter_before'] == [18, 17] and summ['talker']['active_counter_after'] == [115, 114], 'talker counters 18/17 -> 115/114 in summary')
    check(summ['listener']['active_counter_before'] == [12, 11] and summ['listener']['active_counter_after'] == [112, 111], 'listener counters 12/11 -> 112/111 in summary')
    check(115 - 18 == 97 == sum(I(r, 'active_start_delta') for r in rows if r['direction'] == 'talker'), 'talker +97 start increments equal the 97 demonstrated restarts')

    # Setup and restore snapshots in the public operator packet.
    def ctr(path, role, what):
        for line in path.read_text().splitlines():
            j = json.loads(line)
            if j.get('role') == role and j.get('what') == what:
                return [j['response']['counters'][str(i)] for i in (0, 1)]
    for d, role, what, pair in (('talker', 'dut', 'counter-6-1', ([18, 17], [115, 114])), ('listener', 'peer', 'counter-6-2', ([12, 11], [112, 111]))):
        s = ctr(a1 / f'{d}-setup' / 'snapshot-after.jsonl', role, what)
        e = ctr(a1 / f'{d}-restore' / 'snapshot-before.jsonl', role, what)
        check([s, e] == list(pair), f'{d}: public setup-after {s} and restore-before {e} snapshots')

    # Public cycles 1-5: raw records versus the addendum rows.
    ih = {r['identifier']: r['sha256'] for r in csv.DictReader((a2 / 'input-hashes.csv').open())}
    for d, role, what in (('listener', 'peer', 'counter-6-2'), ('talker', 'dut', 'counter-6-1')):
        prev = ctr(a1 / f'{d}-setup' / 'snapshot-after.jsonl', role, what)
        for c in range(1, 6):
            f = a1 / f'{d}-{c:03d}'
            res = json.loads((f / 'result.json').read_text())
            r = next(x for x in rows if x['direction'] == d and int(x['cycle']) == c)
            b, e = ctr(f / 'snapshot-before.jsonl', role, what), ctr(f / 'snapshot-after.jsonl', role, what)
            ok = (res['response_ns'] == I(r, 'response_ns') and res['disconnect_response_ns'] == I(r, 'disconnect_response_ns')
                  and res['connect_command_ns'] == I(r, 'connect_command_ns') and res['first_avtp_ns'] == I(r, 'first_post_response_ns')
                  and res['latency_s'] == F(r, 'latency_s') and res['frames_last_half_second_disconnected'] == I(r, 'last_half_second_pdus')
                  and b == prev and [e[0] - b[0], e[1] - b[1]] == [I(r, 'active_start_delta'), I(r, 'active_stop_delta')])
            hashes = all(hashlib.sha256((f / s).read_bytes()).hexdigest() == ih[f'{d}-{c:03d}/{s}']
                         for s in ('result.json', 'analysis.json', 'snapshot-before.jsonl', 'snapshot-after.jsonl', 'cycle.jsonl'))
            check(ok and hashes, f'{d}-{c:03d}: public record timings, counters {b}->{e}, continuity and input hashes match addendum')
            prev = e
    check(len(ih) == 1000, f'input-hashes.csv lists 1000 per-attempt source records ({len(ih)})')

    # Raw-capture index: addendum, operator index and page Artifacts table.
    raw = {x['identifier']: x for x in json.loads((a1 / 'RAW-ARTIFACTS.json').read_text())}
    pg = {m.group(1): (int(m.group(2)), m.group(3)) for m in re.finditer(r'^\| `([a-z]+-[0-9a-z]+/tap\.pcap)` \| (\d+) \| `([0-9a-f]{64})` \|$', page, re.M)}
    ok = all(raw[r['capture']]['sha256'] == r['sha256'] == pg[r['capture']][1] and raw[r['capture']]['size'] == I(r, 'capture_bytes') == pg[r['capture']][0] for r in rows)
    check(ok, f'200 capture sizes/SHA-256 agree across addendum, operator index and page ({len(pg)} page capture rows)')

    # Page tables against the addendum.
    cyc = table_rows(page, '| Direction | Cycle | Interval, seconds |')
    stp = table_rows(page, '| Direction | Cycle | Settled PDUs |')
    check(len(cyc) == 200 and len(stp) == 200, f'page cycle table {len(cyc)} rows, stop table {len(stp)} rows')
    bad = []
    for r in rows:
        k = (f"DUT {r['direction']}", r['cycle'])
        c = next(x for x in cyc if (x[0], x[1]) == k)
        s = next(x for x in stp if (x[0], x[1]) == k)
        want_res = 'PASS' if mine[(r['direction'], I(r, 'cycle'))] == 'RESTART' else 'NOT RESTART'
        if c[2] != f"{F(r, 'latency_s'):.6f}" or c[8] != want_res:
            bad.append(('cycle', k, c))
        if s[2:] != [r['settled_to_response_pdus'], r['command_to_response_pdus'], f"{r['dut_start_delta']} / {r['dut_stop_delta']}",
                     f"{r['active_start_delta']} / {r['active_stop_delta']}", r['stop_check']]:
            bad.append(('stop', k, s))
    check(not bad, f'page cycle and stop tables match addendum rows ({bad[:3]})')

    # Distributions and growth, recomputed from accepted rows only.
    dt = {x[0]: x for x in table_rows(page, '| Direction | Demonstrated restarts |')}
    gt = {x[0]: x for x in table_rows(page, '| Direction | First ten median |')}
    bt = table_rows(page, '| Direction | Cycles | Median, seconds |')
    for d in ('listener', 'talker'):
        acc = sorted(((I(r, 'cycle'), F(r, 'latency_s')) for r in rows if r['direction'] == d and mine[(d, I(r, 'cycle'))] == 'RESTART'))
        n, mn, md, p95, mx = dist(v for _, v in acc)
        print(f'INFO {d} demonstrated n={n} min={mn:.9f} median={md:.10f} p95={p95:.9f} max={mx:.9f}')
        row = dt[f'DUT {d}']
        check(row[1] == str(n) == row[2] and row[3:7] == [f'{v:.6f}' for v in (mn, md, p95, mx)], f'{d}: page distribution row {row[1:7]}')
        on, omn, omd, op95, omx = dist(F(r, 'latency_s') for r in rows if r['direction'] == d)
        print(f'INFO {d} original (all 100) min={omn:.9f} median={omd:.9f} p95={op95:.9f} max={omx:.9f}')
        nn, slope, lo, hi, t = ols(acc)
        print(f'INFO {d} OLS n={nn} slope={slope:.12f} ci=[{lo:.12f}, {hi:.12f}] t975={t:.9f} df={nn-2}')
        g = gt[f'DUT {d}']
        check(g[3] == f'{slope:.9f}', f'{d}: page slope {g[3]}')
        check(g[4] == f'[{lo:+.9f}, {hi:+.9f}]', f'{d}: page 95% slope interval {g[4]} (exact t)')
        f10 = st.median(v for c, v in acc if c <= 10); l10 = st.median(v for c, v in acc if c > 90)
        check(g[1] == f'{f10:.6f}' and g[2] == f'{l10:.6f}', f'{d}: first/last ten medians {g[1]} {g[2]}')
        for b0 in range(1, 101, 10):
            blk = [v for c, v in acc if b0 <= c <= b0 + 9]
            prow = next(x for x in bt if x[0] == f'DUT {d}' and x[1] == f'{b0}-{b0+9}')
            if prow[2] != f'{st.median(blk):.6f}' or prow[3] != f'{max(blk):.6f}':
                check(False, f'{d} block {b0}: page {prow[2:4]} vs {st.median(blk):.6f}/{max(blk):.6f}')
        check(True, f'{d}: ten-cycle block medians and maxima checked against page')
        n1, s1, _, _, _ = ols([p for p in acc if p[0] != 1])
        print(f'INFO {d} slope without cycle 1: {s1:.9f}')

    # Addendum artifact hashes quoted by the page.
    for name in ('recompute.py', 'stop-checks.csv', 'recomputed-summary.json', 'input-hashes.csv'):
        b = (a2 / name).read_bytes()
        m = re.search(r'^\| `' + re.escape(name) + r'` \| (\d+) \| `([0-9a-f]{64})` \|$', page, re.M)
        check(m and int(m.group(1)) == len(b) and m.group(2) == hashlib.sha256(b).hexdigest(), f'page addendum row for {name}')

    print('RESULT', 'PASS' if not fails else f'FAIL ({len(fails)})')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
