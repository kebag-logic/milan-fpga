"""Independent reviewer probe for PR #604 (issue #75); the round-2 probe, reused in round 3.

Usage: python3 stop_probe.py EVIDENCE_ROOT PAGE [--addendum DIR] [--mutate NAME]
  --addendum DIR addendum holding stop-checks.csv (default author-r2; round 3 passes author-r3)
  EVIDENCE_ROOT  the published review-evidence/75-r1 directory (author/ and author-r2/)
  PAGE           docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md at the head under review
  --mutate NAME  apply one planted fault to the loaded ledger and expect the probe to fail

Recomputes, without the author's recompute.py, every round-2 claim that can be
derived from the recorded public data: the stop classification, the counter
reconciliation, the distributions, the slope intervals, the ordered blocks,
the capture-size identity and the page tables.  Exit status 0 only if every
check passes.  Raw captures are private, so the probe cannot re-derive the
per-PDU window counts; it cross-checks them against the public cycles 1-5 and
against the wire/counter redundancy instead.
"""
import csv
import hashlib
import json
import math
import re
import statistics as st
import sys
from pathlib import Path

FAIL = []


def check(ok, what):
    print(('PASS ' if ok else 'FAIL ') + what)
    if not ok:
        FAIL.append(what)


def rows_jsonl(p):
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]


def counter(p, role, what):
    r = next(x['response'] for x in rows_jsonl(p) if x.get('role') == role and x.get('what') == what)
    assert r['status'] == 'SUCCESS'
    return int(r['counters']['0']), int(r['counters']['1'])


def t975(df):
    # Two-sided 95% Student-t quantile by bisection on a Simpson-integrated CDF.
    c = math.exp(math.lgamma((df + 1) / 2) - math.lgamma(df / 2)) / math.sqrt(df * math.pi)

    def cdf(x, n=20000):
        h = x / n
        s = sum((1 if i in (0, n) else 4 if i % 2 else 2) * (1 + (i * h) ** 2 / df) ** (-(df + 1) / 2)
                for i in range(n + 1))
        return 0.5 + c * s * h / 3
    lo, hi = 1.9, 2.1
    for _ in range(50):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if cdf(mid) < 0.975 else (lo, mid)
    return (lo + hi) / 2


def ols(pts):
    x = [a for a, _ in pts]
    y = [b for _, b in pts]
    n, mx, my = len(x), st.mean(x), st.mean(y)
    sxx = sum((a - mx) ** 2 for a in x)
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sxx
    se = math.sqrt(sum((c - my - b * (a - mx)) ** 2 for a, c in zip(x, y)) / (n - 2) / sxx)
    t = t975(n - 2)
    return b, b - t * se, b + t * se, n - 2


def dist(v):
    v = sorted(v)
    return len(v), sum(x < 1 for x in v), v[0], st.median(v), v[math.ceil(0.95 * len(v)) - 1], v[-1]


def table(lines, header_prefix):
    """Return the data rows of the first Markdown table whose header starts with header_prefix."""
    for i, line in enumerate(lines):
        if line.startswith(header_prefix):
            out = []
            for row in lines[i + 2:]:
                if not row.startswith('|'):
                    break
                out.append([c.strip() for c in row.strip().strip('|').split('|')])
            return out
    raise SystemExit('table not found: ' + header_prefix)


def main():
    root, page = Path(sys.argv[1]), Path(sys.argv[2])
    opts = dict(zip(sys.argv[3::2], sys.argv[4::2]))
    mutate = opts.get('--mutate')
    a1, a2 = root / 'author', root / opts.get('--addendum', 'author-r2')
    print(f'INFO ledger: {a2.name}/stop-checks.csv')
    led = list(csv.DictReader((a2 / 'stop-checks.csv').open()))
    num = {'cycle', 'disconnect_response_ns', 'settle_begin_ns', 'connect_command_ns', 'response_ns',
           'last_half_second_pdus', 'settled_to_command_pdus', 'command_to_response_pdus',
           'settled_to_response_pdus', 'disconnect_to_command_pdus', 'last_before_settle_ns',
           'first_after_settle_ns', 'dut_start_delta', 'dut_stop_delta', 'active_start_delta',
           'active_stop_delta', 'first_post_response_ns', 'capture_bytes', 'target_pdus', 'mr_one_pdus',
           'fs_one_pdus', 'tu_one_pdus', 'target_stored_bytes', 'other_stored_bytes'}
    for r in led:
        for k in num:
            r[k] = int(r[k])
        for k in ('latency_s', 'silence_gap_s', 'maximum_hold_gap_s', 'capture_span_s', 'capture_tail_s',
                  'unwrap_spread_s'):
            r[k] = float(r[k])
    if mutate == 'one-pdu-in-hold':      # a restart row gains one PDU inside the settled window
        r = next(x for x in led if x['direction'] == 'talker' and x['cycle'] == 12)
        r['settled_to_command_pdus'] += 1
        r['settled_to_response_pdus'] += 1
    elif mutate == 'counter-on-nonrestart':  # a non-restart row reports a start/stop pair
        r = next(x for x in led if x['direction'] == 'talker' and x['cycle'] == 24)
        r['active_start_delta'] = r['active_stop_delta'] = 1
    elif mutate == 'latency-shift':      # one restart latency moves by 1 microsecond
        r = next(x for x in led if x['direction'] == 'talker' and x['cycle'] == 72)
        r['first_post_response_ns'] += 1000
        r['latency_s'] = (r['first_post_response_ns'] - r['response_ns']) / 1e9

    print('== 1. ledger shape')
    for d in ('listener', 'talker'):
        check(sorted(r['cycle'] for r in led if r['direction'] == d) == list(range(1, 101)),
              f'{d}: 100 attempts, cycles 1..100, each once')

    print('== 2. independent stop classification (window arithmetic, wire rule, counter redundancy)')
    bad_arith, bad_cls, bad_restart_shape, stop_after = [], [], [], {}
    mine = {}
    for r in led:
        k = (r['direction'], r['cycle'])
        if not (r['settle_begin_ns'] == r['disconnect_response_ns'] + 500_000_000
                and r['connect_command_ns'] - r['disconnect_response_ns'] >= 2_000_000_000
                and r['response_ns'] > r['connect_command_ns']
                and r['settled_to_response_pdus'] == r['settled_to_command_pdus'] + r['command_to_response_pdus']
                and r['latency_s'] == (r['first_post_response_ns'] - r['response_ns']) / 1e9):
            bad_arith.append(k)
        wire_stop = r['settled_to_response_pdus'] == 0 and r['first_after_settle_ns'] >= r['response_ns']
        counters = (r['active_start_delta'], r['active_stop_delta'])
        cls = 'RESTART' if wire_stop else 'NOT_RESTART'
        mine[k] = cls
        if cls != r['classification'] or (r['stop_check'] == 'PASS') != wire_stop \
                or counters != ((1, 1) if wire_stop else (0, 0)):
            bad_cls.append(k)
        if wire_stop:
            # stream observed stopped: last PDU before settling, then nothing until the restart PDU
            if not (r['last_before_settle_ns'] < r['settle_begin_ns']
                    and r['first_after_settle_ns'] == r['first_post_response_ns']
                    and r['last_half_second_pdus'] == 0
                    and r['silence_gap_s'] * 1e9 >= r['response_ns'] - r['settle_begin_ns']):
                bad_restart_shape.append(k)
            stop_after.setdefault(r['direction'], []).append(
                (r['last_before_settle_ns'] - r['disconnect_response_ns']) / 1e6)
    check(not bad_arith, f'window arithmetic and latency identity hold for all 200 rows {bad_arith}')
    check(not bad_cls, f'my wire rule and the counter redundancy agree with the published classification {bad_cls}')
    check(not bad_restart_shape, f'every accepted restart shows a silent gap spanning settle->response {bad_restart_shape}')
    nr = sorted(k for k, v in mine.items() if v == 'NOT_RESTART')
    check(nr == [('talker', 13), ('talker', 24), ('talker', 75)], f'non-restarts are exactly talker 13, 24, 75: {nr}')
    for d, v in stop_after.items():
        print(f'INFO {d}: last target PDU after the disconnect response, ms: min {min(v):.3f} '
              f'median {st.median(v):.3f} max {max(v):.3f} (n={len(v)})')
        check(max(v) < 500, f'{d}: every accepted restart stopped well inside the 0.5 s settling allowance')
    for c in (13, 24, 75):
        r = next(x for x in led if x['direction'] == 'talker' and x['cycle'] == c)
        exp_settled = (r['response_ns'] - r['settle_begin_ns']) / 2_000_000
        exp_hold = (r['connect_command_ns'] - r['disconnect_response_ns']) / 2_000_000
        ok = (abs(r['settled_to_response_pdus'] - exp_settled) <= 1.5 and abs(r['disconnect_to_command_pdus'] - exp_hold) <= 1.5
              and r['last_half_second_pdus'] == 250 and r['maximum_hold_gap_s'] < 0.004
              and r['first_after_settle_ns'] < r['response_ns'] and (r['dut_start_delta'], r['dut_stop_delta']) == (0, 0))
        check(ok, f'talker {c}: {r["settled_to_response_pdus"]} settled PDUs vs {exp_settled:.1f} expected at 500/s, '
                  f'{r["disconnect_to_command_pdus"]} hold PDUs vs {exp_hold:.1f}, max gap {r["maximum_hold_gap_s"]} s, '
                  f'DUT counters 0/0 -> continuous stream, no stop')

    print('== 3. flags and capture-size identity')
    check(all(r['mr_one_pdus'] == r['fs_one_pdus'] == r['tu_one_pdus'] == 0 for r in led), 'mr, fs, tu zero in every target PDU')
    check(all(r['capture_bytes'] == 24 + r['target_stored_bytes'] + r['other_stored_bytes']
              and r['target_stored_bytes'] == 108 * r['target_pdus'] for r in led),
          'bytes = 24 + 108 * CRF PDUs + other, all 200 captures')
    check(max(r['unwrap_spread_s'] for r in led) < 2.147483648, 'unwrap spread below half-wrap')

    print('== 4. raw identity cross-check (ledger vs private-artifact index vs page)')
    raw = {x['identifier']: x for x in json.loads((a1 / 'RAW-ARTIFACTS.json').read_text())}
    text = page.read_text()
    lines = text.splitlines()
    cap = {r[0].strip('`'): (int(r[1]), r[2].strip('`')) for r in table(lines, '| Capture identifier |')}
    check(all(raw[r['capture']]['sha256'] == r['sha256'] == cap[r['capture']][1]
              and raw[r['capture']]['size'] == r['capture_bytes'] == cap[r['capture']][0] for r in led),
          '200 capture sha256 and sizes agree across ledger, RAW-ARTIFACTS.json and the page index')

    print('== 5. public cycles 1-5: ledger vs retained per-cycle records, input hashes, counter continuity')
    ih = {x['identifier']: x['sha256'] for x in csv.DictReader((a2 / 'input-hashes.csv').open())}
    check(len(ih) == 1000, f'input-hashes.csv lists 1000 source records ({len(ih)})')
    for d, role, what in (('listener', 'peer', 'counter-6-2'), ('talker', 'dut', 'counter-6-1')):
        prev = counter(a1 / f'{d}-setup/snapshot-after.jsonl', role, what)
        for c in range(1, 6):
            f = a1 / f'{d}-{c:03d}'
            r = next(x for x in led if x['direction'] == d and x['cycle'] == c)
            res, an = json.loads((f / 'result.json').read_text()), json.loads((f / 'analysis.json').read_text())
            hashes_ok = all(ih[f'{d}-{c:03d}/{s}'] == hashlib.sha256((f / s).read_bytes()).hexdigest()
                            for s in ('result.json', 'analysis.json', 'snapshot-before.jsonl', 'snapshot-after.jsonl', 'cycle.jsonl'))
            b = counter(f / 'snapshot-before.jsonl', role, what)
            e = counter(f / 'snapshot-after.jsonl', role, what)
            db = counter(f / 'snapshot-before.jsonl', 'dut', 'counter-6-1')
            de = counter(f / 'snapshot-after.jsonl', 'dut', 'counter-6-1')
            ok = (hashes_ok and b == prev
                  and (e[0] - b[0], e[1] - b[1]) == (r['active_start_delta'], r['active_stop_delta'])
                  and (de[0] - db[0], de[1] - db[1]) == (r['dut_start_delta'], r['dut_stop_delta'])
                  and res['disconnect_response_ns'] == r['disconnect_response_ns']
                  and res['connect_command_ns'] == r['connect_command_ns'] and res['response_ns'] == r['response_ns']
                  and res['first_avtp_ns'] == r['first_post_response_ns'] and res['latency_s'] == r['latency_s']
                  and res['frames_last_half_second_disconnected'] == r['last_half_second_pdus']
                  and an['valid_avtp'] == r['target_pdus'])
            check(ok, f'{d}-{c:03d}: hashes, anchors, latency, last-half count, PDU total, counter deltas, continuity')
            prev = e
    for d, role, what, exp in (('listener', 'peer', 'counter-6-2', 100), ('talker', 'dut', 'counter-6-1', 97)):
        s = counter(a1 / f'{d}-setup/snapshot-after.jsonl', role, what)
        e = counter(a1 / f'{d}-restore/snapshot-before.jsonl', role, what)
        ds = sum(r['active_start_delta'] for r in led if r['direction'] == d)
        dp = sum(r['active_stop_delta'] for r in led if r['direction'] == d)
        nres = sum(1 for k, v in mine.items() if k[0] == d and v == 'RESTART')
        check((e[0] - s[0], e[1] - s[1]) == (ds, dp) == (exp, exp) == (nres, nres),
              f'{d}: retained counters {s} -> {e} = +{e[0]-s[0]}/+{e[1]-s[1]}; ledger sum +{ds}/+{dp}; '
              f'demonstrated restarts {nres}; claim {exp}')
    check(all((r['dut_start_delta'], r['dut_stop_delta']) == (0, 0) for r in led if r['direction'] == 'listener'),
          'listener series: inactive DUT output counters unchanged in all 100 cycles')

    print('== 6. distributions, blocks, slope intervals vs the page')
    lat = {d: [(r['cycle'], r['latency_s']) for r in led if r['direction'] == d and mine[(d, r['cycle'])] == 'RESTART']
           for d in ('listener', 'talker')}
    drows = {r[0]: r for r in table(lines, '| Direction | Demonstrated restarts |')}
    for d in lat:
        n, below, mn, med, p95, mx = dist([v for _, v in lat[d]])
        row = drows[f'DUT {d}']
        mine_row = [str(n), str(below)] + [f'{x:.6f}' for x in (mn, med, p95, mx)]
        check(row[1:7] == mine_row, f'{d}: distribution {mine_row} == page {row[1:7]}')
    orig = [r['latency_s'] for r in led if r['direction'] == 'talker']
    o = dist(orig)
    check(f'{o[2]:.6f}' == '0.000297' and f'{dist([v for _, v in lat["talker"]])[2]:.6f}' == '0.017427'
          and o[5] == dist([v for _, v in lat['talker']])[5],
          'stated effect: minimum 0.000297 -> 0.017427, maximum unchanged')
    grow = {r[0]: r for r in table(lines, '| Direction | First ten median |')}
    for d in lat:
        b, lo, hi, df = ols(lat[d])
        f10 = st.median(v for c, v in lat[d] if c <= 10)
        l10 = st.median(v for c, v in lat[d] if c > 90)
        row = grow[f'DUT {d}']
        mine_row = [f'{f10:.6f}', f'{l10:.6f}', f'{b:.9f}', f'[{lo:.9f}, {hi:+.9f}]']
        check(row[1] == mine_row[0] and row[2] == mine_row[1] and row[3] == mine_row[2]
              and row[4] == mine_row[3].replace('[-', '[-'),
              f'{d}: growth row mine {mine_row} (df {df}) vs page {row[1:5]}')
        print(f'INFO {d}: upper bound {hi*1e5:.3f} ms/100 cycles')
    b1 = ols([p for p in lat['talker'] if p[0] != 1])[0]
    check(f'{b1:+.9f}' == '+0.000040905', f'talker slope without cycle 1 {b1:+.9f}')
    blocks = table(lines, '| Direction | Cycles | Median, seconds |')
    bad = []
    for row in blocks:
        d = row[0].split()[1]
        lo_c, hi_c = map(int, row[1].split('-'))
        v = [x for c, x in lat[d] if lo_c <= c <= hi_c]
        if row[2] != f'{st.median(v):.6f}' or row[3] != f'{max(v):.6f}':
            bad.append(row[:4])
    check(not bad and len(blocks) == 20, f'20 ordered blocks: median and maximum over demonstrated restarts {bad}')

    print('== 7. page per-cycle tables vs ledger')
    cyc = table(lines, '| Direction | Cycle | Interval, seconds |')
    stp = table(lines, '| Direction | Cycle | Settled PDUs |')
    bad = []
    for row in cyc:
        r = next(x for x in led if f'DUT {x["direction"]}' == row[0] and x['cycle'] == int(row[1]))
        want = 'PASS' if mine[(r['direction'], r['cycle'])] == 'RESTART' and r['latency_s'] < 1 else 'NOT RESTART'
        if row[2] != f'{r["latency_s"]:.6f}' or row[8] != want:
            bad.append(row[:3] + row[8:])
    check(len(cyc) == 200 and not bad, f'cycle-evidence table: 200 intervals and results match {bad[:5]}')
    bad = []
    for row in stp:
        r = next(x for x in led if f'DUT {x["direction"]}' == row[0] and x['cycle'] == int(row[1]))
        want = [str(r['settled_to_response_pdus']), str(r['command_to_response_pdus']),
                f'{r["dut_start_delta"]} / {r["dut_stop_delta"]}', f'{r["active_start_delta"]} / {r["active_stop_delta"]}',
                'PASS' if mine[(r['direction'], r['cycle'])] == 'RESTART' else 'FAIL']
        if row[2:7] != want:
            bad.append(row)
    check(len(stp) == 200 and not bad, f'stop-check table: 200 rows match the ledger and my classification {bad[:5]}')
    size = table(lines, '| Talker cycle | Bytes |')
    tk = {r['cycle']: r for r in led if r['direction'] == 'talker'}
    top6 = sorted(tk.values(), key=lambda r: r['capture_bytes'], reverse=True)[:6]
    check([int(r[0]) for r in size] == [r['cycle'] for r in top6] and all(
        r[1:7] == [str(tk[int(r[0])]['capture_bytes']), f'{tk[int(r[0])]["capture_span_s"]:.6f}',
                   f'{tk[int(r[0])]["capture_tail_s"]:.6f}', str(tk[int(r[0])]['target_pdus']),
                   str(tk[int(r[0])]['target_stored_bytes']), str(tk[int(r[0])]['other_stored_bytes'])] for r in size),
          'six largest talker captures table matches the ledger')

    print('== 8. what the tapped MSRP record says about the three non-restarts')
    # Public cycles: one bridge Listener Lv per talker cycle, shortly after the disconnect response,
    # and the DUT's last PDU falls within one PDU period of it (the stop is Lv-driven).
    for c in range(1, 6):
        f = a1 / f'talker-{c:03d}'
        ev = [x.split('\t') for x in (f / 'msrp.tsv').read_text().splitlines()[1:]]
        lv = [int(e[0]) for e in ev if e[1] == 'bridge' and e[2] == 'Listener' and e[3] == 'Lv']
        r = tk[c]
        print(f'INFO talker-{c:03d}: bridge Listener Lv at disconnect+{(lv[0]-r["disconnect_response_ns"])/1e6:.3f} ms '
              f'(count {len(lv)}); last DUT PDU at disconnect+{(r["last_before_settle_ns"]-r["disconnect_response_ns"])/1e6:.3f} ms')
        check(len(lv) == 1 and 0 <= lv[0] - r['last_before_settle_ns'] < 2_000_100,
              f'talker-{c:03d}: exactly one bridge Listener Lv, and the stream stops within one PDU period before it reaches the DUT side')
    prof = {int(row[1]): tuple(row[3:8]) for row in cyc if row[0] == 'DUT talker'}
    for c in (13, 24, 75):
        twins = [k for k, v in prof.items() if v == prof[c] and k not in (13, 24, 75)]
        print(f'INFO talker {c}: MSRP profile {prof[c]} (PDUs, LeaveAll, TA, Listener, Ready) is identical to '
              f'restart cycles {twins}')
    attr = table(lines, '| Direction | Sender | Attribute |')
    lvrow = next(r for r in attr if r[0] == 'DUT talker' and r[1] == 'bridge' and r[2] == 'Listener')
    print(f'INFO page attribution table: bridge Listener Lv total over the 100 talker captures = {lvrow[8]}')
    print(f'INFO page text mentions Listener leave for the non-restarts: '
          f'{bool(re.search(r"(13, 24, and 75|non-restart)[^\n]*(Lv|leave|withdraw)", text, re.I))}')

    print('== RESULT', 'FAIL' if FAIL else 'PASS', f'({len(FAIL)} failing checks)')
    return 1 if FAIL else 0


if __name__ == '__main__':
    sys.exit(main())
