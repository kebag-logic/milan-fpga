"""Independent round-3 probe for the #75 findings page (PR #604).

Usage: python3 -B r3_probe.py EVIDENCE_DIR PAGE INDEX
EVIDENCE_DIR is the published review-evidence/75-r1 directory (author/,
author-r2/, author-r3/). PAGE is the findings page and INDEX the findings
README at the head under review. Reads only. Prints one PASS/FAIL/INFO line
per check and exits 1 if any check fails. Uses only published files.

A declaration is an MRP New, JoinIn or JoinMt event (IEEE 802.1Q 10.7.6,
Table 10-3). In, Mt, Lv and LeaveAll carry no declaration.
"""
import ast
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

DECL = ('New', 'JoinIn', 'JoinMt')
fails = []


def check(ok, what):
    print(('PASS ' if ok else 'FAIL ') + what)
    if not ok:
        fails.append(what)


def info(what):
    print('INFO ' + what)


def tsv(path):
    with path.open() as f:
        return list(csv.DictReader(f, delimiter='\t'))


def rows(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def s(ns):
    return f'{ns / 1e9:.9f}'


def main():
    ev, page_path, index_path = map(Path, sys.argv[1:])
    a1, a2, a3 = ev / 'author', ev / 'author-r2', ev / 'author-r3'
    page = page_path.read_text()
    index = index_path.read_text()
    summary = json.loads((a3 / 'declarations-summary.json').read_text())
    hold_rows = {int(r['cycle']): r for r in rows(a3 / 'hold-declarations.csv')}
    hold_events = rows(a3 / 'hold-events.csv')
    stops = {int(r['cycle']): r for r in rows(a3 / 'stop-checks.csv') if r['direction'] == 'talker'}

    # ---- Item 1: declaration census, derived from event names only ----
    check(sorted(hold_rows) == list(range(1, 101)), 'hold-declarations.csv has exactly talker holds 1..100')
    derived = {c: 0 for c in range(1, 101)}
    for e in hold_events:
        if e['event'] in DECL:
            derived[int(e['cycle'])] += 1
    check(all(e['is_declaration'] == str(e['event'] in DECL) for e in hold_events),
          f'hold-events.csv is_declaration flag agrees with the event name on all {len(hold_events)} rows')
    check(all(derived[c] == int(hold_rows[c]['declaration_count']) for c in derived),
          'per-hold declaration counts re-derived from hold-events.csv event names equal hold-declarations.csv')
    declared = [c for c in derived if derived[c] > 0]
    undeclared = [c for c in derived if derived[c] == 0]
    info(f'derived census: {len(declared)}/{len(derived)} holds carry a DUT Talker Advertise declaration; without: {undeclared}')
    check(summary['holds_with_dut_declaration'] == len(declared) and summary['holds_without_dut_declaration'] == undeclared,
          'declarations-summary.json census equals the re-derived census')
    check(f'DUT Talker Advertise in {len(declared)}/{len(derived)} holds' in page,
          f'page states the derived census ({len(declared)}/{len(derived)})')
    check(summary['hold_window'] == '[disconnect response, connect command)' and 'It includes its start and excludes its end.' in page,
          'page and summary state the same half-open hold window')

    # Cross-check the census input against every published talker TSV.
    published = {c: a1 / f'talker-{c:03d}' for c in range(1, 6)}
    published.update({c: a3 / f'talker-{c:03d}' for c in (13, 24, 75)})
    hashes = {r['identifier']: r['sha256'] for r in rows(a3 / 'declaration-input-hashes.csv')}
    for c, d in published.items():
        r = json.loads((d / 'result.json').read_text())
        dr, cc, ack = r['disconnect_response_ns'], r['connect_command_ns'], r['response_ns']
        check((dr, cc, ack) == tuple(int(hold_rows[c][k]) for k in ('disconnect_response_ns', 'connect_command_ns', 'response_ns')),
              f'talker-{c:03d}: hold anchors equal result.json')
        ta = [e for e in tsv(d / 'msrp.tsv') if e['sender'] == 'DUT' and e['type'] == 'TalkerAdvertise'
              and e['stream_id'] == r['stream_id'] and dr <= int(e['tap_ns']) < cc]
        mine = [(int(e['tap_ns']), e['event']) for e in ta]
        theirs = [(int(e['tap_ns']), e['event']) for e in hold_events if int(e['cycle']) == c]
        check(mine == theirs, f'talker-{c:03d}: hold-events.csv rows equal the published msrp.tsv ({len(mine)} events)')
        check(sum(ev_ in DECL for _, ev_ in mine) == int(hold_rows[c]['declaration_count'])
              and sum(ev_ == 'Lv' for _, ev_ in mine) == int(hold_rows[c]['withdrawal_count'])
              and sum(ev_ == 'Mt' for _, ev_ in mine) == int(hold_rows[c]['empty_count']),
              f'talker-{c:03d}: declaration/withdrawal/empty counts equal the published msrp.tsv')
        for src in ('result.json', 'msrp.tsv'):
            check(hashes.get(f'talker-{c:03d}/{src}') == sha(d / src),
                  f'talker-{c:03d}/{src}: census input hash equals the published file')
    # Initial bind.
    su = a1 / 'talker-setup'
    r = json.loads((su / 'result.json').read_text())
    ta = [e for e in tsv(su / 'msrp.tsv') if e['sender'] == 'DUT' and e['type'] == 'TalkerAdvertise'
          and e['stream_id'] == r['stream_id'] and e['event'] in DECL]
    before = sum(int(e['tap_ns']) < r['response_ns'] for e in ta)
    first = min(int(e['tap_ns']) for e in ta) - r['response_ns']
    check(before == 0 == summary['initial_bind']['declarations_before_response'], 'initial bind: 0 DUT declarations before its response')
    check(s(first) == '0.079237250' and 'first declaration follows the response by 0.079 seconds' in page,
          f'initial bind: first DUT declaration +{s(first)} s after response, as the page states')

    # Cycle 1 chronology, every number on the page.
    d = published[1]
    r = json.loads((d / 'result.json').read_text())
    dr, cc, ack = r['disconnect_response_ns'], r['connect_command_ns'], r['response_ns']
    ev1 = tsv(d / 'msrp.tsv')
    ta = [e for e in ev1 if e['sender'] == 'DUT' and e['type'] == 'TalkerAdvertise' and e['stream_id'] == r['stream_id']]
    hold = [(int(e['tap_ns']) - dr, e['event']) for e in ta if dr <= int(e['tap_ns']) < cc]
    info('cycle 1 hold DUT TA events: ' + ', '.join(f'+{s(t)} {n}' for t, n in hold))
    check([n for _, n in hold] == ['Lv', 'Mt', 'Mt'], 'cycle 1: hold carries Lv then Mt only (no declaration)')
    check(f'`Lv` at +{s(hold[0][0])} seconds' in page and f'+{s(hold[1][0])} and +{s(hold[2][0])} seconds' in page,
          'cycle 1: page Lv/Mt offsets equal the published msrp.tsv')
    check(not [e for e in ta if dr <= int(e['tap_ns']) < ack and e['event'] in DECL],
          'cycle 1: no DUT declaration from disconnect response to reconnect response ("undeclared until after reconnect success")')
    fa = min(int(e['tap_ns']) for e in ta if int(e['tap_ns']) >= ack and e['event'] in DECL)
    ready = min(int(e['tap_ns']) for e in ev1 if e['sender'] == 'bridge' and e['type'] == 'Listener'
                and e['stream_id'] == r['stream_id'] and e['listener'] == '2' and e['event'] in DECL
                and int(e['tap_ns']) >= ack)
    trip = (s(fa - ack), s(ready - fa), s(r['first_avtp_ns'] - ready))
    info(f'cycle 1: first declaration +{trip[0]} s after response; Ready +{trip[1]}; CRF +{trip[2]}; latency {r["latency_s"]}')
    check(f'reconnect success by {trip[0]} seconds' in page and f'that declaration by {trip[1]} seconds' in page
          and f'another {trip[2]} seconds later' in page and f'restarts in {r["latency_s"]:.9f} seconds' in page,
          'cycle 1: page chronology equals the published records')
    check('therefore differs in DUT-side state' not in page and 'retain DUT Talker Advertise through the hold' not in page,
          'old universal claim and its unqualified inference are gone from the page')
    check('[#606](https://github.com/kebag-logic/milan-fpga/issues/606) must consider cycle 1' in page,
          'page points #606 at cycle 1')
    dsrc = (a3 / 'declarations.py').read_text()
    check("holds_with_dut_declaration=sum(r['declaration_count'] > 0 for r in holds)" in dsrc
          and "DECLARATIONS = {'New', 'JoinIn', 'JoinMt'}" in dsrc,
          'declarations.py derives the census count from data with the declaration-only event set')

    # ---- Item 2: non-stop chronology ----
    le = rows(a3 / 'listener-events.csv')
    for c in (13, 24, 75):
        d = published[c]
        r = json.loads((d / 'result.json').read_text())
        dr, cc, ack = r['disconnect_response_ns'], r['connect_command_ns'], r['response_ns']
        ev_ = tsv(d / 'msrp.tsv')
        bl = [e for e in ev_ if e['sender'] == 'bridge' and e['type'] == 'Listener'
              and e['stream_id'] == r['stream_id'] and int(e['tap_ns']) >= dr]
        mine = [(int(e['tap_ns']), e['event'], e['listener']) for e in bl]
        theirs = [(int(x['tap_ns']), x['event'], x['listener']) for x in le if int(x['cycle']) == c]
        check(mine == theirs, f'talker-{c:03d}: listener-events.csv equals every target bridge Listener event after disconnect in msrp.tsv ({len(mine)})')
        lv = [t for t, n, _ in mine if n == 'Lv']
        dec = [t for t, n, _ in mine if n in DECL]
        check(len(lv) == 1 and all(t > ack for t in dec) and dec and lv[0] < min(dec),
              f'talker-{c:03d}: one Lv, then no Listener declaration until after reconnect response')
        row = f'| {c} | {s(lv[0] - dr)} | {s(ack - dr)} | {s(min(dec) - dr)} | {s(min(dec) - ack)} |'
        check(row in page, f'talker-{c:03d}: page chronology row {row!r} equals the published records')
        for t, n, _ in mine:
            srow = f'| {c} | {n} | +{s(t - dr)} | {"+" if t >= ack else "-"}{s(abs(t - ack))} |'
            check(srow in page, f'talker-{c:03d}: page event row {srow!r} present')
        for x in le:
            if int(x['cycle']) == c:
                p, t, n = int(x['previous_crf_ns']), int(x['tap_ns']), int(x['next_crf_ns'])
                check(p < t <= n and abs((n - p) / 1e9 - float(x['bracketing_crf_gap_s'])) < 1e-12 and n - p <= 2_000_053,
                      f'talker-{c:03d} {x["event"]} @{t}: bracketed by CRF {p}..{n}, gap <= 0.002000053 s')
        ns = next(x for x in summary['nonstops'] if x['cycle'] == c)
        sc = stops[c]
        check(sc['classification'] == 'NOT_RESTART' and int(sc['dut_start_delta']) == 0 == int(sc['dut_stop_delta'])
              and ns['dut_start_delta'] == 0 == ns['dut_stop_delta'] and int(sc['disconnect_to_command_pdus']) == 1000,
              f'talker-{c:03d}: NOT_RESTART, DUT start/stop +0/+0, 1000 PDUs in the hold (stop-checks.csv)')
        span_lv = min(dec) - lv[0]
        check(abs(ns['pdus_lv_to_redeclaration'] - span_lv / 2e6) <= 1 and abs(ns['pdus_lv_to_response'] - (ack - lv[0]) / 2e6) <= 1,
              f'talker-{c:03d}: PDU counts consistent with 2 ms period ({ns["pdus_lv_to_redeclaration"]} vs {span_lv / 2e6:.2f})')
        check(f'| {c} | {s(lv[0] - dr)} | {s(ack - dr)} | {s(min(dec) - dr)} | {s(min(dec) - ack)} | {ns["pdus_lv_to_redeclaration"]} |' in page,
              f'talker-{c:03d}: page PDU count equals declarations-summary.json')
        la = [(int(e['tap_ns']) - lv[0]) for e in ev_ if e['sender'] == 'DUT' and e['event'] == 'LeaveAll'
              and dr <= int(e['tap_ns']) < cc]
        info(f'talker-{c:03d}: DUT LeaveAll during hold at +{", +".join(sorted({s(x) for x in la}))} s after the bridge Lv')
    for c in range(1, 6):
        d = published[c]
        r = json.loads((d / 'result.json').read_text())
        dr, cc = r['disconnect_response_ns'], r['connect_command_ns']
        ev_ = tsv(d / 'msrp.tsv')
        lv = min(int(e['tap_ns']) for e in ev_ if e['sender'] == 'bridge' and e['type'] == 'Listener'
                 and e['event'] == 'Lv' and e['stream_id'] == r['stream_id'] and int(e['tap_ns']) >= dr)
        la = sorted({int(e['tap_ns']) - lv for e in ev_ if e['sender'] == 'DUT' and e['event'] == 'LeaveAll' and dr <= int(e['tap_ns']) < cc})
        info(f'talker-{c:03d} (restart): bridge Lv +{s(lv - dr)} s; DUT LeaveAll during hold at ' +
             (', '.join('+' + s(x) for x in la) or 'none') + ' s after the Lv')
    for anchor, what in [('owns the non-stop behavior in these three cycles', 'stop-check section'),
                         ('three talker non-restarts excluded, tracked by [#608]', 'acceptance row'),
                         ('behavior owned by [#608]', 'acceptance restarts row')]:
        check(anchor in page, f'page links #608 from the {what}')
    check('three non-restarts tracked by [#608](https://github.com/kebag-logic/milan-fpga/issues/608)' in index,
          'findings index row links #608')

    # ---- Item 3/4: replay classification, optimisation refusal, derived outcome ----
    for name in ('recompute.py', 'declarations.py'):
        t = ast.parse((a3 / name).read_text())
        check(not any(isinstance(n, ast.Assert) for n in ast.walk(t)), f'{name}: no assert statements')
        check(not any(isinstance(n, ast.ExceptHandler) for n in ast.walk(t)), f'{name}: no exception-based classification')
    for name in ('recompute.py', 'declarations.py'):
        for label, opt, env in [('-O', ['-O'], dict(os.environ)), ('-OO', ['-OO'], dict(os.environ)),
                                ('PYTHONOPTIMIZE=1', [], dict(os.environ, PYTHONOPTIMIZE='1'))]:
            p = subprocess.run([sys.executable, '-B', *opt, str(a3 / name), 'x', 'y', 'z'], env=env,
                               capture_output=True, text=True, timeout=120, cwd=str(a3))
            check(p.returncode != 0 and 'REFUSED: optimized execution' in p.stderr and 'Traceback' not in p.stderr,
                  f'{name} {label}: refused before reading inputs, rc {p.returncode}')
    sys.path.insert(0, str(a3))
    import recompute
    truth = [((0, 100, 100), 'RESTART'), ((1, 101, 100), 'NOT_RESTART'), ((0, 99, 100), 'NOT_RESTART'),
             ((754, 50, 100), 'NOT_RESTART'), ((0, 100, 99), 'RESTART')]
    check(all(recompute.classify_stop(*a) == v for a, v in truth), 'classify_stop truth table (count, early resumption, silence)')
    real = [dict(direction=r['direction'], cycle=int(r['cycle']), stop_check=r['stop_check'],
                 classification=r['classification']) for r in rows(a3 / 'stop-checks.csv')]
    lines = recompute.outcome_lines(real)
    info('derived outcome: ' + ' | '.join(lines))
    rej = [f"{r['direction']}-{r['cycle']:03d}" for r in real if r['classification'] != 'RESTART']
    check(f'{len(real)} raw hashes' in lines[0] and f"{sum(r['stop_check'] == 'PASS' for r in real)} PASS; {len(rej)} FAIL" in lines[1]
          and ', '.join(rej) in lines[1], 'outcome lines equal counts computed independently from stop-checks.csv')
    mut = [dict(x) for x in real]
    mut[0]['classification'], mut[0]['stop_check'] = 'NOT_RESTART', 'FAIL'
    ml = recompute.outcome_lines(mut)
    check(ml != lines and 'listener-001' in ml[1] and f'{len(rej) + 1} FAIL' in ml[1], 'outcome lines change with a mutated row')
    osrc = ast.get_source_segment((a3 / 'recompute.py').read_text(),
                                  next(n for n in ast.parse((a3 / 'recompute.py').read_text()).body
                                       if isinstance(n, ast.FunctionDef) and n.name == 'outcome_lines'))
    check(not re.search(r'\b(197|013|024|075)\b', osrc), 'outcome_lines source pins no count or cycle literal')
    for n in ('stop-checks.csv', 'recomputed-summary.json', 'input-hashes.csv'):
        check((a3 / n).read_bytes() == (a2 / n).read_bytes(), f'{n}: round-3 bytes equal round-2 (stop results and quantiles unchanged)')

    # ---- Addendum integrity ----
    check(all(sha(a3 / l.split(None, 1)[1].lstrip('*')) == l.split()[0] for l in (a3 / 'MANIFEST.sha256').read_text().splitlines()),
          'author-r3 MANIFEST.sha256: every listed file verifies')
    pr = rows(a3 / 'published-records.csv')
    changed = sorted(x['identifier'] for x in pr if x['transform'] != 'unchanged')
    check(len(pr) == 48 and changed == [f'talker-{c:03d}/raw-artifacts.json' for c in (13, 24, 75)]
          and all(sha(a3 / x['identifier']) == x['published_sha256'] for x in pr)
          and all(x['source_sha256'] == x['published_sha256'] for x in pr if x['transform'] == 'unchanged'),
          'published-records.csv: 48 records, only raw-artifacts.json transformed, published hashes verify')
    for c in (13, 24, 75):
        ra = json.loads((a3 / f'talker-{c:03d}' / 'raw-artifacts.json').read_text())
        check(ra == [dict(identifier=f'talker-{c:03d}/tap.pcap', size=ra[0]['size'], sha256=ra[0]['sha256'])]
              and ra[0]['sha256'] == stops[c]['sha256'] and ra[0]['size'] == int(stops[c]['capture_bytes']),
              f'talker-{c:03d}: relative capture identifier; size and sha256 equal stop-checks.csv')
        files = sorted(p.name for p in (a3 / f'talker-{c:03d}').iterdir())
        check(files == sorted(p.name for p in published[1].iterdir()), f'talker-{c:03d}: same record set as published cycle 1')

    print('RESULT ' + ('PASS' if not fails else f'FAIL ({len(fails)})'))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
