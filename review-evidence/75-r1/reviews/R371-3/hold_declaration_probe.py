"""Independent reviewer probe for PR #604 round 3 (issue #75).

Usage: python3 hold_declaration_probe.py EVIDENCE_ROOT PAGE INDEX [--mutate NAME]
  EVIDENCE_ROOT  the published review-evidence/75-r1 directory (author/, author-r2/, author-r3/)
  PAGE           docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md at the head under review
  INDEX          docs/findings/README.md at the head under review
  --mutate NAME  plant one fault in the loaded evidence and expect the probe to fail

Does not import or run the author's declarations.py or recompute.py for the
census.  It decodes nothing from raw captures (those are private); it works
from the retained per-cycle msrp.tsv/result.json records that are public
(talker cycles 1-5 from round 1, cycles 13, 24, 75 from round 3, and the setup),
the round-2 stop ledger, and the round-3 census tables, and checks:
  A. the three newly published cycle records are the originals (round-2 input
     hashes, round-1 raw index, per-directory manifests, publication ledger);
  B. the hold declaration census, re-derived from New/JoinIn/JoinMt events only;
  C. the talker cycle-1 exception chronology;
  D. the non-stop Listener chronology for cycles 13, 24 and 75;
  E. the page and index statements, and the #606/#608 links.
Exit status 0 only if every check passes.
"""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

DECLARE = {'New', 'JoinIn', 'JoinMt'}          # 802.1Q 10.7.5.1 declaration events
FAIL = []
NONSTOP = ('talker-013', 'talker-024', 'talker-075')
PUBLIC_T = [f'talker-{c:03d}' for c in range(1, 6)]


def check(ok, what):
    print(('PASS ' if ok else 'FAIL ') + what)
    if not ok:
        FAIL.append(what)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def tsv(p):
    with p.open() as f:
        return list(csv.DictReader(f, delimiter='\t'))


def jsonl(p):
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]


def dut_counter(p):
    r = next(x['response'] for x in jsonl(p) if x.get('role') == 'dut' and x.get('what') == 'counter-6-1')
    return int(r['counters']['0']), int(r['counters']['1'])


def s9(ns):
    return f'{ns / 1e9:.9f}'


def main():
    root, page, index = map(Path, sys.argv[1:4])
    mutate = sys.argv[5] if len(sys.argv) > 5 and sys.argv[4] == '--mutate' else None
    a1, a2, a3 = root / 'author', root / 'author-r2', root / 'author-r3'
    text = page.read_text()
    ledger = {(r['direction'], int(r['cycle'])): r for r in csv.DictReader((a2 / 'stop-checks.csv').open())}
    holds = [dict(r) for r in csv.DictReader((a3 / 'hold-declarations.csv').open())]
    events = [dict(r) for r in csv.DictReader((a3 / 'hold-events.csv').open())]
    summary = json.loads((a3 / 'declarations-summary.json').read_text())
    lev = [dict(r) for r in csv.DictReader((a3 / 'listener-events.csv').open())]
    records = {}
    for name in PUBLIC_T + ['talker-setup']:
        records[name] = (json.loads((a1 / name / 'result.json').read_text()), tsv(a1 / name / 'msrp.tsv'), a1 / name)
    for name in NONSTOP:
        records[name] = (json.loads((a3 / name / 'result.json').read_text()), tsv(a3 / name / 'msrp.tsv'), a3 / name)

    if mutate == 'declare-cycle-1':        # cycle 1's first Mt becomes a JoinMt in the census table
        next(e for e in events if e['cycle'] == '1' and e['event'] == 'Mt')['event'] = 'JoinMt'
    elif mutate == 'drop-declared-hold':   # every declaration of cycle 50 disappears from the census table
        events = [e for e in events if not (e['cycle'] == '50' and e['event'] in DECLARE)]
    elif mutate == 'redeclare-in-hold':    # a bridge Listener JoinIn appears in cycle 24's hold
        res, rows, d = records['talker-024']
        rows.append(dict(rows[-1], tap_ns=str(res['disconnect_response_ns'] + 1_000_000_000), sender='bridge',
                         type='Listener', event='JoinIn', stream_id=res['stream_id'], listener='2'))
        rows.sort(key=lambda r: int(r['tap_ns']))
    elif mutate == 'cycle1-declares':      # the public cycle-1 record gains a DUT Talker Advertise JoinIn in its hold
        res, rows, d = records['talker-001']
        rows.append(dict(tap_ns=str(res['disconnect_response_ns'] + 1_000_000_000), sender='DUT',
                         type='TalkerAdvertise', event='JoinIn', stream_id=res['stream_id'], listener='None',
                         first_value=''))
        rows.sort(key=lambda r: int(r['tap_ns']))

    print('== A. provenance of the published non-stop records (talker 13, 24, 75)')
    r2hash = {r['identifier']: r['sha256'] for r in csv.DictReader((a2 / 'input-hashes.csv').open())}
    pub = {r['identifier']: r for r in csv.DictReader((a3 / 'published-records.csv').open())}
    raw_index = {r['identifier']: r for r in json.loads((a1 / 'RAW-ARTIFACTS.json').read_text())}
    check(len(pub) == 48 and all(k.split('/')[0] in NONSTOP for k in pub),
          f'publication ledger lists {len(pub)} records, all in the three non-stop directories')
    for name in NONSTOP:
        d = a3 / name
        files = sorted(p.name for p in d.iterdir() if p.is_file() and p.name != 'MANIFEST.sha256')
        man = {l.split()[1]: l.split()[0] for l in (d / 'MANIFEST.sha256').read_text().splitlines() if l.strip()}
        check(sorted(man) == files and all(sha(d / f) == man[f] for f in files),
              f'{name}: local MANIFEST covers exactly the {len(files)} published files and verifies')
        check(all(f'{name}/{f}' in pub and pub[f'{name}/{f}']['published_sha256'] == sha(d / f) for f in files),
              f'{name}: every published file matches its publication-ledger hash')
        changed = sorted(k for k, r in pub.items() if k.startswith(name + '/') and r['source_sha256'] != r['published_sha256'])
        check(changed == [f'{name}/raw-artifacts.json'] and
              all((r['transform'] == 'unchanged') == (r['source_sha256'] == r['published_sha256'])
                  for k, r in pub.items() if k.startswith(name + '/')),
              f'{name}: only raw-artifacts.json is transformed ({changed})')
        r2 = {f: r2hash[f'{name}/{f}'] for f in ('result.json', 'analysis.json', 'snapshot-before.jsonl',
                                                  'snapshot-after.jsonl', 'cycle.jsonl')}
        check(all(sha(d / f) == h for f, h in r2.items()),
              f'{name}: result/analysis/snapshots/cycle equal the round-2 input-hash ledger (published before round 3)')
        ra = json.loads((d / 'raw-artifacts.json').read_text())
        led = ledger[('talker', int(name[-3:]))]
        check(len(ra) == 1 and ra[0]['identifier'] == f'{name}/tap.pcap'
              and ra[0]['sha256'] == raw_index[f'{name}/tap.pcap']['sha256'] == led['sha256']
              and ra[0]['size'] == raw_index[f'{name}/tap.pcap']['size'] == int(led['capture_bytes']),
              f'{name}: raw-artifacts.json is relative and agrees with the round-1 raw index and round-2 ledger')
        res = records[name][0]
        check(all(res[k] == int(led[k]) for k in ('disconnect_response_ns', 'connect_command_ns', 'response_ns')),
              f'{name}: result.json anchors equal the round-2 stop ledger')
        b, a = dut_counter(d / 'snapshot-before.jsonl'), dut_counter(d / 'snapshot-after.jsonl')
        check(((a[0] - b[0]) % 2**32, (a[1] - b[1]) % 2**32) == (0, 0) and
              (led['dut_start_delta'], led['dut_stop_delta'], led['classification']) == ('0', '0', 'NOT_RESTART'),
              f'{name}: DUT STREAM_START/STOP unchanged in the published snapshots {b}->{a}; ledger NOT_RESTART')

    print('== B. hold declaration census (New/JoinIn/JoinMt only; window [disconnect response, connect command))')
    by_cycle = {}
    for e in events:
        by_cycle.setdefault(int(e['cycle']), []).append(e)
    bad_window, bad_rows, bad_flag = [], [], []
    for h in holds:
        c = int(h['cycle'])
        led = ledger[('talker', c)]
        dr, cc = int(h['disconnect_response_ns']), int(h['connect_command_ns'])
        if (dr, cc, int(h['response_ns'])) != (int(led['disconnect_response_ns']), int(led['connect_command_ns']),
                                               int(led['response_ns'])):
            bad_window.append(c)
        ev = by_cycle.get(c, [])
        if any(not (dr <= int(e['tap_ns']) < cc) or abs(float(e['after_disconnect_s']) - (int(e['tap_ns']) - dr) / 1e9) > 5e-10
               for e in ev):
            bad_window.append(c)
        if any((e['is_declaration'] == 'True') != (e['event'] in DECLARE) for e in ev):
            bad_flag.append(c)
        mine = (sum(e['event'] in DECLARE for e in ev), sum(e['event'] == 'Lv' for e in ev),
                sum(e['event'] == 'Mt' for e in ev))
        if mine != (int(h['declaration_count']), int(h['withdrawal_count']), int(h['empty_count'])):
            bad_rows.append((c, mine))
    check(sorted(int(h['cycle']) for h in holds) == list(range(1, 101)), 'census has talker holds 1..100, each once')
    check(set(by_cycle) <= set(range(1, 101)), 'every hold event belongs to a census hold')
    check(not bad_window, f'hold windows equal the stop ledger and every event lies inside [dr, cc) {bad_window[:5]}')
    check(not bad_flag, f'is_declaration column agrees with the New/JoinIn/JoinMt predicate {bad_flag[:5]}')
    check(not bad_rows, f'per-hold declaration/Lv/Mt counts re-derived from events equal the census rows {bad_rows[:5]}')
    declared = sorted(c for c in range(1, 101) if any(e['event'] in DECLARE for e in by_cycle.get(c, [])))
    undeclared = sorted(set(range(1, 101)) - set(declared))
    kinds = sorted({e['event'] for e in events})
    print(f'INFO event kinds present in DUT Talker Advertise hold events: {kinds}; '
          f'holds with a non-declaration event: {sorted({int(e["cycle"]) for e in events if e["event"] not in DECLARE})}')
    print(f'INFO my census: {len(declared)}/100 holds carry a DUT Talker Advertise declaration; without: {undeclared}')
    check(summary['holds_with_dut_declaration'] == len(declared) and summary['holds_without_dut_declaration'] == undeclared
          and summary['inspected_holds'] == 100 and sorted(summary['declaration_events']) == sorted(DECLARE),
          'declarations-summary.json census equals my derivation')
    check(f'{len(declared)}/100 holds' in text and f'Talker cycle {undeclared[0]} withdraws' in text
          if undeclared else False,
          f'page states the derived census ({len(declared)}/100) and names the exception cycle {undeclared}')
    for name in PUBLIC_T + list(NONSTOP):
        res, rows, _ = records[name]
        c, dr, cc = int(name[-3:]), res['disconnect_response_ns'], res['connect_command_ns']
        mine = sorted((int(r['tap_ns']), r['event']) for r in rows if r['sender'] == 'DUT' and r['type'] == 'TalkerAdvertise'
                      and r['stream_id'] == res['stream_id'] and dr <= int(r['tap_ns']) < cc)
        theirs = sorted((int(e['tap_ns']), e['event']) for e in by_cycle.get(c, []))
        check(mine == theirs, f'{name}: hold events from the public msrp.tsv equal hold-events.csv '
                              f'({len(mine)} events, {sum(e in DECLARE for _, e in mine)} declarations)')

    print('== C. talker cycle 1 exception, from the public cycle-1 record')
    res, rows, _ = records['talker-001']
    dr, cc, ack, first = (res[k] for k in ('disconnect_response_ns', 'connect_command_ns', 'response_ns', 'first_avtp_ns'))
    ta = [r for r in rows if r['sender'] == 'DUT' and r['type'] == 'TalkerAdvertise' and r['stream_id'] == res['stream_id']]
    hold = [(int(r['tap_ns']) - dr, r['event']) for r in ta if dr <= int(r['tap_ns']) < cc]
    decl_to_resp = [r for r in ta if dr <= int(r['tap_ns']) < ack and r['event'] in DECLARE]
    first_decl = min(int(r['tap_ns']) for r in ta if int(r['tap_ns']) >= ack and r['event'] in DECLARE)
    ready = min(int(r['tap_ns']) for r in rows if r['sender'] == 'bridge' and r['type'] == 'Listener'
                and r['stream_id'] == res['stream_id'] and r['listener'] == '2' and r['event'] in DECLARE
                and int(r['tap_ns']) >= ack)
    print(f'INFO cycle-1 hold events (s after disconnect response): {[(s9(t), e) for t, e in hold]}')
    check(not decl_to_resp and [e for _, e in hold] == ['Lv', 'Mt', 'Mt'],
          'cycle 1: DUT withdraws (Lv) then sends only Mt; no declaration from disconnect response to reconnect response')
    for label, value in [('Lv', s9(hold[0][0])), ('Mt', s9(hold[1][0])), ('Mt', s9(hold[2][0])),
                         ('first declaration after response', s9(first_decl - ack)),
                         ('Ready after that declaration', s9(ready - first_decl)),
                         ('CRF after Ready', s9(first - ready)), ('latency', s9(first - ack))]:
        check(value in text, f'cycle 1: {label} {value} s appears on the page')
    check(first - ack == int(round(float(ledger[('talker', 1)]['latency_s']) * 1e9)) ==
          max(int(round(float(r['latency_s']) * 1e9)) for (d, c), r in ledger.items()
              if d == 'talker' and r['classification'] == 'RESTART'),
          f'cycle 1 latency {s9(first - ack)} s equals the ledger and is the talker restart maximum')
    sres, srows, _ = records['talker-setup']
    sdecl = [int(r['tap_ns']) for r in srows if r['sender'] == 'DUT' and r['type'] == 'TalkerAdvertise'
             and r['stream_id'] == sres['stream_id'] and r['event'] in DECLARE]
    check(not [t for t in sdecl if t < sres['response_ns']] and
          abs((min(sdecl) - sres['response_ns']) / 1e9 - summary['initial_bind']['first_advert_after_response_s']) < 1e-9,
          'initial bind: no DUT declaration before its response; first at +0.079237250 s (summary agrees)')
    for phrase in ('That shared absence alone cannot explain the initial-bind delay.',
                   'causal attribution remains open',
                   '[#606](https://github.com/kebag-logic/milan-fpga/issues/606) must consider cycle 1'):
        check(phrase in text, f'page qualifies the inference: "{phrase}"')
    for stale in ('Numbered reconnects instead retain DUT Talker Advertise through the hold',
                  'The initial bind therefore differs in DUT-side state'):
        check(stale not in text, f'withdrawn universal claim absent: "{stale}"')

    print('== D. non-stop Listener chronology (talker 13, 24, 75), from the published records')
    table_rows = [l for l in text.splitlines() if re.match(r'\| (13|24|75) \| (Lv|New|JoinIn|JoinMt|In|Mt) \|', l)]
    summary_rows = [l for l in text.splitlines() if re.match(r'\| (13|24|75) \| 0\.0', l)]
    mine_lev = []
    for name in NONSTOP:
        res, rows, d = records[name]
        c, dr, cc, ack = int(name[-3:]), res['disconnect_response_ns'], res['connect_command_ns'], res['response_ns']
        led = ledger[('talker', c)]
        lis = [r for r in rows if r['sender'] == 'bridge' and r['type'] == 'Listener'
               and r['stream_id'] == res['stream_id'] and int(r['tap_ns']) >= dr]
        lv = [int(r['tap_ns']) for r in lis if r['event'] == 'Lv']
        decl = [int(r['tap_ns']) for r in lis if r['event'] in DECLARE]
        la = sorted({int(r['tap_ns']) for r in rows if r['sender'] == 'bridge' and r['event'] == 'LeaveAll'
                     and dr <= int(r['tap_ns']) < ack})
        dut_ta = [r['event'] for r in rows if r['sender'] == 'DUT' and r['type'] == 'TalkerAdvertise'
                  and r['stream_id'] == res['stream_id'] and dr <= int(r['tap_ns']) < ack]
        acmp = json.loads((d / 'analysis.json').read_text())['acmp_wire_counts']
        print(f'INFO {name}: bridge Listener events after disconnect: '
              f'{[(r["event"], r["listener"], s9(int(r["tap_ns"]) - dr), s9(int(r["tap_ns"]) - ack)) for r in lis]}')
        print(f'INFO {name}: bridge LeaveAll between disconnect and reconnect response: {len(la)}; '
              f'DUT Talker Advertise events in that span: {dut_ta}; ACMP wire counts {acmp}')
        check(len(lv) == 1 and decl and min(decl) > ack and not [t for t in decl if lv[0] < t < ack],
              f'{name}: exactly one bridge Listener Lv, no Listener declaration until after the reconnect response')
        check(all(r['listener'] == '2' for r in lis), f'{name}: every bridge Listener event carries value 2 (Ready)')
        check(not any(str(k) == '2' for s in acmp.values() for k in s),
              f'{name}: no ACMP DISCONNECT_TX_COMMAND (message type 2) on the tap')
        check(float(led['maximum_hold_gap_s']) <= 0.002000053 and int(led['disconnect_to_command_pdus']) == 1000,
              f'{name}: ledger shows 1000 hold PDUs and max gap {led["maximum_hold_gap_s"]} s')
        for r in lis:
            t = int(r['tap_ns'])
            mine_lev.append((c, t, r['event']))
            want = f'| {c} | {r["event"]} | +{s9(t - dr)} | {"+" if t >= ack else "-"}{s9(abs(t - ack))} |'
            check(want in table_rows, f'{name}: page event row {want}')
        want = f'| {c} | {s9(lv[0] - dr)} | {s9(ack - dr)} | {s9(min(decl) - dr)} | {s9(min(decl) - ack)} |'
        check(any(l.startswith(want) for l in summary_rows), f'{name}: page summary row starts {want}')
        n = next(x for x in summary['nonstops'] if x['cycle'] == c)
        span = (min(decl) - lv[0]) / 2_000_000
        check(int(span) - 1 <= n['pdus_lv_to_redeclaration'] <= int(span) + 1 and
              f'| {n["pdus_lv_to_redeclaration"]} |' in next(l for l in summary_rows if l.startswith(f'| {c} |')),
              f'{name}: {n["pdus_lv_to_redeclaration"]} CRF PDUs from Lv to re-declaration is consistent with the '
              f'2 ms cadence over {span * 0.002:.6f} s and with the page')
    check(len(table_rows) == len(mine_lev) == 12, f'page event table has {len(table_rows)} rows; the records give {len(mine_lev)}')
    theirs = sorted((int(r['cycle']), int(r['tap_ns']), r['event']) for r in lev)
    check(theirs == sorted(mine_lev), 'listener-events.csv equals the events decoded from the published msrp.tsv')
    check(all(int(r['previous_crf_ns']) < int(r['tap_ns']) <= int(r['next_crf_ns']) and
              abs(float(r['bracketing_crf_gap_s']) - (int(r['next_crf_ns']) - int(r['previous_crf_ns'])) / 1e9) < 5e-10 and
              float(r['bracketing_crf_gap_s']) <= 0.002000053 for r in lev),
          'every Listener event is bracketed by CRF PDUs no more than 0.002000053 s apart')

    print('== E. owners and links')
    sec = text.split('## Stop checks', 1)[1].split('\n## ', 1)[0]
    link608 = '[#608](https://github.com/kebag-logic/milan-fpga/issues/608)'
    check(link608 in sec.split('| Direction | Cycle |')[0], 'Stop checks section links #608 before its table')
    acc = next(l for l in text.splitlines() if l.startswith('| At least 100 physical restarts'))
    check(link608 in acc and '13, 24, and 75' in acc, 'acceptance row links #608 and names cycles 13, 24, 75')
    idx = next(l for l in index.read_text().splitlines() if '75_RECONNECT_RESTART_MEASUREMENT.md' in l)
    check(link608 in idx and '#606' in idx, 'findings index row links #608 and names #606')
    check('This supports DUT-side non-stop behavior at the tapped boundary.' in sec and
          'It does not prove the DUT internally accepted that withdrawal.' in sec,
          'stop-check section states the supported attribution and its limit')

    print(f'== RESULT {"PASS" if not FAIL else "FAIL"} ({len(FAIL)} failing checks)')
    return 1 if FAIL else 0


if __name__ == '__main__':
    sys.exit(main())
