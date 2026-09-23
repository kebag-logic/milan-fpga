#!/usr/bin/env python3
"""Independent re-derivation of the issue 117 step 2 cadence/turnaround table
and the Run B CRF facts from the published tap captures of the A200 packet.

usage: rederive_step2.py A200_BENCH_DIR
"""
import sys, os, struct, statistics

bench = sys.argv[1]
RUNS = [('A', 'runA/tap-runA.pcap'), ('B', 'runB/tap-runB.pcap'), ('C', 'runC/tap-runC.pcap'),
        ('final', 'final/tap-final.pcap')]


def recs(path):
    raw = open(path, 'rb').read()
    nano = struct.unpack('<I', raw[:4])[0] == 0xA1B23C4D
    off, first, host_only = 24, None, 0
    out = []
    while off + 16 <= len(raw):
        s, f, incl, _o = struct.unpack('<IIII', raw[off:off + 16])
        pkt = raw[off + 16:off + 16 + incl]
        off += 16 + incl
        host = s * 10**9 + (f if nano else f * 1000)
        if len(pkt) < 42 or struct.unpack('<I', pkt[:4])[0] != 6 or struct.unpack('<I', pkt[8:12])[0] not in (2, 3):
            host_only += 1
            continue
        port = struct.unpack('<I', pkt[8:12])[0]
        lo = struct.unpack('<I', pkt[16:20])[0]
        if first is None:
            first = (host, lo)
        k = round(((host - first[0]) - (lo - first[1])) / 2**32)
        out.append((lo - first[1] + k * 2**32, port, pkt[28:], host))
    return out, host_only


def ts10(b):
    return int.from_bytes(b[0:6], 'big') * 10**9 + int.from_bytes(b[6:10], 'big')


tot = {}
agg = {k: [] for k in ('sync_far', 'ann_far', 'preq_far', 'preq_dut')}
logi = {}
ex_dut, ex_sw = [], []
ann_gm = {}
crf = []
for name, rel in RUNS:
    R, host_only = recs(os.path.join(bench, rel))
    by = {}
    ptp = []
    for tn, port, fr, host in R:
        et = fr[12:14]
        p = fr[14:]
        if et == b'\x81\x00':
            et, p = fr[16:18], fr[18:]
        if et == b'\x88\xf7' and len(p) >= 44:
            mt = p[0] & 15
            ptp.append(dict(t=tn, port=port, mt=mt, seq=struct.unpack('>H', p[30:32])[0],
                            li=struct.unpack('b', p[33:34])[0], src=p[20:30].hex(),
                            corr=int.from_bytes(p[8:16], 'big', signed=True) / 65536.0,
                            ts=ts10(p[34:44]), req=p[44:54].hex() if mt in (3, 10) else None,
                            gm=p[53:61].hex() if mt == 11 and len(p) >= 61 else None))
        elif et == b'\x22\xf0' and p and p[0] == 0x04:
            crf.append((name, tn, port, p[1] & 1, p[2], host))
    for key, port, mt in (('sync_far', 2, 0), ('ann_far', 2, 11), ('preq_far', 2, 2), ('preq_dut', 3, 2)):
        ts = [x['t'] for x in ptp if x['port'] == port and x['mt'] == mt]
        iv = [(b - a) / 1e6 for a, b in zip(ts, ts[1:])]
        agg[key].append((name, iv))
        logi.setdefault(key, set()).update(x['li'] for x in ptp if x['port'] == port and x['mt'] == mt)
        if key == 'preq_dut':
            logi.setdefault('preq_dut_src', set()).update(x['src'] for x in ptp if x['port'] == port and x['mt'] == mt)
    for x in ptp:
        if x['mt'] == 11 and x['port'] == 2:
            ann_gm[x['gm']] = ann_gm.get(x['gm'], 0) + 1
    # Pdelay exchanges: requester port rp; response on the other port with same seq
    for rp, lst in ((2, ex_dut), (3, ex_sw)):
        reqs = [x for x in ptp if x['port'] == rp and x['mt'] == 2]
        resp = {x['seq']: x for x in ptp if x['port'] != rp and x['mt'] == 3}
        rfu = {x['seq']: x for x in ptp if x['port'] != rp and x['mt'] == 10}
        for q in reqs:
            r, f = resp.get(q['seq']), rfu.get(q['seq'])
            if r and f and 0 < r['t'] - q['t'] < 1e9:
                # two-step: t2 in Resp body, t3 in Resp_Follow_Up body, corrections included
                claimed = (f['ts'] + f['corr']) - (r['ts'] - r['corr'])
                lst.append(dict(run=name, tap=r['t'] - q['t'], fu=f['t'] - r['t'], claimed=claimed,
                                diff=(r['t'] - q['t']) - claimed))
            else:
                lst.append(dict(run=name, tap=None))
    print('run %s: %d tap records, %d records without envelope, span %.1f s' % (
        name, len(R), host_only, (R[-1][0] - R[0][0]) / 1e9))

for key, runs in agg.items():
    allv = [v for _n, iv in runs for v in iv]
    means = ['%s %.2f' % (n, statistics.mean(iv)) for n, iv in runs if iv]
    nom = 125.0 if key == 'sync_far' else 1000.0
    within = sum(1 for v in allv if abs(v - nom) <= 0.3 * nom)
    print('%-9s intervals %d, min %.3f max %.3f ms, per-run mean [%s], within 30%% %d, logMessageInterval %s' % (
        key, len(allv), min(allv), max(allv), ', '.join(means), within, sorted(logi[key])))
print('DUT Pdelay_Req source port ids:', sorted(logi['preq_dut_src']))
print('Announce grandmasterIdentity counts (switch side):', ann_gm)
for label, lst in (('switch requests, DUT responds', ex_dut), ('DUT requests, switch responds', ex_sw)):
    ok = [x for x in lst if x['tap'] is not None]
    print(label, ': %d of %d complete' % (len(ok), len(lst)))
    tapv = sorted(x['tap'] for x in ok)
    print('   tap req->resp min %.0f ns max %.0f ns; resp->FU %.0f..%.0f ns; claimed t3-t2 %.0f..%.0f ns' % (
        tapv[0], tapv[-1], min(x['fu'] for x in ok), max(x['fu'] for x in ok),
        min(x['claimed'] for x in ok), max(x['claimed'] for x in ok)))
    print('   largest three tap turnarounds (ms):', [round(v / 1e6, 3) for v in tapv[-3:]])
    for run in ('A', 'B', 'C', 'final'):
        rr = [x for x in ok if x['run'] == run]
        if rr:
            print('   run %s: median tap %.0f ns, median tap-minus-claimed %.0f ns (min %.0f max %.0f)' % (
                run, statistics.median(x['tap'] for x in rr), statistics.median(x['diff'] for x in rr),
                min(x['diff'] for x in rr), max(x['diff'] for x in rr)))
# CRF (Run B)
b = [x for x in crf if x[0] == 'B']
print('CRF PDUs: Run B %d (DUT-sent %d), other runs %d; tu=1 count %d' % (
    len(b), sum(1 for x in b if x[2] == 3), len(crf) - len(b), sum(x[3] for x in b)))
seqgap = sum(1 for a, c in zip(b, b[1:]) if (c[4] - a[4]) % 256 != 1)
print('CRF sequence discontinuities (mod 256): %d' % seqgap)
bursts, start = [], b[0][1] if b else None
for a, c in zip(b, b[1:]):
    if c[1] - a[1] > 50e6:
        bursts.append(((a[1] - start) / 1e9, (c[1] - a[1]) / 1e6))
        start = c[1]
if b:
    bursts.append(((b[-1][1] - start) / 1e9, None))
print('CRF bursts (duration s, following pause ms):', [(round(d, 2), None if p is None else round(p)) for d, p in bursts])
