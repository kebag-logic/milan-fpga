#!/usr/bin/env python3
"""Re-derive the issue 117 step 2 cadence/turnaround table and the Run B CRF facts.

usage: step2_rederive.py <archive-root: .../review-evidence/117-r1>
Reads the A200 tap captures of Runs A, B, C and final; intervals and turnarounds come from
the tap clock only (unwrapped against pcap host time). Independent of the packet's scripts.
"""
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tapdec  # noqa: E402

root = sys.argv[1]
B = os.path.join(root, 'bench-a200', 'bench')
RUNS = [('A', 'runA/tap-runA.pcap'), ('B', 'runB/tap-runB.pcap'), ('C', 'runC/tap-runC.pcap'), ('final', 'final/tap-final.pcap')]
DUT_SPI = '020000fffe000001:0001'
SW = '3cc0c6fffefe0210'
agg = {}
dur_total = 0
print('run  records  envelope-less  span_s')
for name, rel in RUNS:
    recs, noenv = tapdec.tap_records(os.path.join(B, rel))
    ev = [(r['tap_ns'], r['port'], tapdec.decode(r['frame'])) for r in recs]
    ev.sort(key=lambda e: e[0])
    span = (ev[-1][0] - ev[0][0]) / 1e9
    dur_total += span
    print(name, len(recs), noenv, round(span, 1))
    def times(port, kind, pred=lambda d: True):
        return [e[0] for e in ev if e[1] == port and e[2].get('kind') == kind and pred(e[2])]
    for key, port, kind, pred in [('sync_sw', 2, 'gPTP Sync', lambda d: True),
                                  ('ann_sw', 2, 'gPTP Announce', lambda d: True),
                                  ('preq_sw', 2, 'gPTP Pdelay_Req', lambda d: True),
                                  ('preq_dut', 3, 'gPTP Pdelay_Req', lambda d: True)]:
        t = times(port, kind, pred)
        iv = [(b - a) / 1e6 for a, b in zip(t, t[1:])]
        agg.setdefault(key, []).append((name, iv))
    lmi = {}
    for e in ev:
        if e[2].get('kind') in ('gPTP Sync', 'gPTP Announce', 'gPTP Pdelay_Req'):
            lmi.setdefault((e[1], e[2]['kind']), set()).add(e[2]['lmi'])
    agg.setdefault('lmi', []).append((name, lmi))
    anns = [e[2] for e in ev if e[1] == 2 and e[2].get('kind') == 'gPTP Announce']
    agg.setdefault('ann_fields', []).append((name, len(anns), {(a['gm'], a['prio1'], a['cclass'], a['cacc'], a['cvar'], a['prio2'], a['tsrc'], a['steps'], tuple(a['path'])) for a in anns}))
    agg.setdefault('dut_sync_ann', []).append((name, sum(1 for e in ev if e[1] == 3 and e[2].get('kind') in ('gPTP Sync', 'gPTP Announce'))))
    agg.setdefault('dut_spi', []).append((name, {e[2]['spi'] for e in ev if e[1] == 3 and e[2].get('kind', '').startswith('gPTP')}))
    agg.setdefault('domain', []).append((name, {e[2]['domain'] for e in ev if e[2].get('kind', '').startswith('gPTP')}))
    # Pdelay exchanges: switch requests, DUT responds (port 2 req -> port 3 resp/fu) and the reverse
    for key, rq_port, rs_port, spi_filter in [('sw_req_dut_resp', 2, 3, None), ('dut_req_sw_resp', 3, 2, DUT_SPI)]:
        reqs = [e for e in ev if e[1] == rq_port and e[2].get('kind') == 'gPTP Pdelay_Req']
        resp = {}
        fu = {}
        for e in ev:
            if e[1] == rs_port and e[2].get('kind') == 'gPTP Pdelay_Resp':
                resp[(e[2]['seq'], e[2]['req_spi'])] = e
            if e[1] == rs_port and e[2].get('kind') == 'gPTP Pdelay_Resp_Follow_Up':
                fu[(e[2]['seq'], e[2]['req_spi'])] = e
        rows = []
        for rq in reqs:
            k = (rq[2]['seq'], rq[2]['spi'])
            if k in resp and k in fu:
                rs, f = resp[k], fu[k]
                tap_turn = rs[0] - rq[0]
                claimed = f[2]['t'] - rs[2]['t'] + (f[2]['corr_ns'] - rs[2]['corr_ns'])
                rows.append((tap_turn, f[0] - rs[0], claimed, tap_turn - claimed))
        agg.setdefault(key, []).append((name, len(reqs), rows))
    if name == 'B':
        crf = [e for e in ev if e[1] == 3 and e[2].get('kind') == 'CRF']
        seqs = [e[2]['seqnum'] for e in crf]
        gaps = sum(1 for a, b in zip(seqs, seqs[1:]) if (a + 1) % 256 != b)
        tus = {e[2]['tu'] for e in crf}
        bursts = []
        cur = [crf[0][0], crf[0][0]]
        pauses = []
        for a, b in zip(crf, crf[1:]):
            if b[0] - a[0] > 50e6:
                bursts.append(cur)
                pauses.append((b[0] - a[0]) / 1e6)
                cur = [b[0], b[0]]
            else:
                cur[1] = b[0]
        bursts.append(cur)
        print('RunB CRF PDUs', len(crf), 'tu values', tus, 'sequence gaps', gaps, 'streams', {e[2]['stream_id'] for e in crf},
              'vlan', {e[2]['vlan'] for e in crf})
        print('RunB bursts (s)', [round((b - a) / 1e9, 2) for a, b in bursts], 'pauses (ms)', [round(p) for p in pauses])
        rate = len(crf) / sum((b - a) / 1e9 for a, b in bursts)
        print('RunB PDU rate per s within bursts', round(rate, 1))
print('tapped span total (s)', round(dur_total, 1))
for key in ('sync_sw', 'ann_sw', 'preq_sw', 'preq_dut'):
    ivs = [x for _, iv in agg[key] for x in iv]
    means = [round(st.mean(iv), 2) for _, iv in agg[key] if iv]
    nom = 125.0 if key == 'sync_sw' else 1000.0
    print(key, 'intervals', len(ivs), 'mean per run', means, 'min', round(min(ivs), 3), 'max', round(max(ivs), 3),
          'outside 30%', sum(1 for x in ivs if abs(x - nom) > 0.3 * nom))
print('lmi', agg['lmi'])
print('announce', [(n, c, f) for n, c, f in agg['ann_fields']])
print('DUT Sync/Announce sent', agg['dut_sync_ann'])
print('DUT source port ids', agg['dut_spi'])
print('domains', agg['domain'])
for key in ('sw_req_dut_resp', 'dut_req_sw_resp'):
    tot_req = sum(n for _, n, _ in agg[key])
    rows = [r for _, _, rs in agg[key] for r in rs]
    med = [round(st.median([r[3] for r in rs])) for _, _, rs in agg[key] if rs]
    print(key, 'requests', tot_req, 'complete', len(rows),
          'tap turnaround ns min/max', round(min(r[0] for r in rows)), round(max(r[0] for r in rows)),
          'resp->fu ns min/max', round(min(r[1] for r in rows)), round(max(r[1] for r in rows)),
          'claimed ns min/max', round(min(r[2] for r in rows)), round(max(r[2] for r in rows)),
          'tap-claimed median per run', med, 'min/max', round(min(r[3] for r in rows)), round(max(r[3] for r in rows)))
    big = sorted(r[0] for r in rows)[-3:]
    print('   largest three tap turnarounds (ms)', [round(x / 1e6, 3) for x in big])
