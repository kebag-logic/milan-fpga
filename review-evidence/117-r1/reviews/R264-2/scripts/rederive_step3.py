#!/usr/bin/env python3
"""Independent re-derivation of the issue 117 step 3 per-cycle table from the
published raw artifacts (console transcript, power-strip log, clock-offset
exchanges, tap capture), without using the packet's own analysis tools.

usage: rederive_step3.py A202_BENCH_DIR
Times are seconds after the outlet-off command on the build-box clock.
"""
import sys, os, re, json, struct, statistics, datetime

bench = sys.argv[1]
SWITCH = '3cc0c6fffefe0210'
DUT = '020000fffe000001'


def iso(s):
    return datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ').replace(
        tzinfo=datetime.timezone.utc).timestamp()


def offsets(cdir):
    per = {}
    for fn in ('clock-before.jsonl', 'clock-after.jsonl'):
        for ln in open(os.path.join(cdir, fn)):
            o = json.loads(ln)
            per.setdefault(o['host'].split('>')[-1], []).append(o['offset_s_median_best5'])
    # role labels: the power-strip host, the controller host, the capture server
    out = {}
    for h, v in per.items():
        role = 'strip' if h.endswith('pi') else ('controller' if h.endswith('pw1') else 'capture')
        out[role] = statistics.mean(v)
    return out


def power(cdir):
    t = {}
    for ln in open(os.path.join(cdir, 'powerstrip.txt')):
        m = re.search(r'(T_OFF_CMD|T_ON_CMD|T_OFF_DONE|T_ON_DONE) ([0-9.]+)', ln)
        if m:
            t[m.group(1)] = float(m.group(2))
    return t


def console(cdir):
    txt = open(os.path.join(cdir, 'console.txt'), encoding='latin-1').read()
    blocks = re.split(r'^### ', txt, flags=re.M)[1:]
    samples = []
    cur = None
    for b in blocks:
        head, _, body = b.partition('\n')
        m = re.match(r"(\S+) cmd='([^']*)'", head)
        ts, cmd = iso(m.group(1)), m.group(2)
        if cmd == 'milan_status':
            kv = dict(re.findall(r'(\w+)=([0-9a-fA-Fx]+)', body))
            cur = dict(t=ts, gm=kv.get('GPTP_GM'), parent=kv.get('GPTP_PARENT'), sync=kv.get('SYNC'),
                       asc=kv.get('ASCAPABLE'), tu=kv.get('TU'), clkv=kv.get('CLKV_STAT'),
                       pgen=kv.get('AS_PATH_GEN'), pcount=kv.get('AS_PATH_COUNT'), pdelay=kv.get('PDELAY_NS'))
            samples.append(cur)
        elif cmd.startswith('mem_read') and cur is not None:
            addr = int(cmd.split()[1], 16)
            mm = re.search(r'0x%08x\s+((?:[0-9a-f]{2} ){4})' % addr, body)
            if mm:
                cur[addr] = int.from_bytes(bytes.fromhex(mm.group(1).replace(' ', '')), 'little')
    return samples


def tap(path):
    raw = open(path, 'rb').read()
    nano = struct.unpack('<I', raw[:4])[0] == 0xA1B23C4D
    off, recs, first = 24, [], None
    while off + 16 <= len(raw):
        s, f, incl, _o = struct.unpack('<IIII', raw[off:off + 16])
        pkt = raw[off + 16:off + 16 + incl]
        off += 16 + incl
        host = s + (f * 1e-9 if nano else f * 1e-6)
        if len(pkt) < 42 or struct.unpack('<I', pkt[:4])[0] != 6:
            continue
        port = struct.unpack('<I', pkt[8:12])[0]
        if port not in (2, 3):
            continue
        lo = struct.unpack('<I', pkt[16:20])[0]
        if first is None:
            first = (host, lo)
        k = round(((host - first[0]) * 1e9 - (lo - first[1])) / 2**32)
        tapns = lo - first[1] + k * 2**32
        recs.append((host, tapns, port, pkt[28:]))
    # clock fit: lower envelope of host - tap per 5 s of tap time, dense windows only
    wins = {}
    for host, tn, _p, _f in recs:
        w = int(tn // 5e9)
        wins.setdefault(w, []).append((host - tn * 1e-9, tn))
    pts = [(min(v)[1], min(v)[0]) for w, v in wins.items() if len(v) >= 30]
    for _ in range(3):
        n = len(pts)
        mx = sum(x for x, _ in pts) / n
        my = sum(y for _, y in pts) / n
        sxx = sum((x - mx) ** 2 for x, _ in pts)
        b = sum((x - mx) * (y - my) for x, y in pts) / sxx if sxx else 0.0
        a = my - b * mx
        keep = [(x, y) for x, y in pts if abs(y - (a + b * x)) <= 0.002]
        if len(keep) == len(pts) or len(keep) < 3:
            break
        pts = keep
    resid = max(abs(y - (a + b * x)) for x, y in pts)
    out = []
    for host, tn, port, fr in recs:
        t = tn * 1e-9 + a + b * tn
        et = fr[12:14]
        p = fr[14:]
        if et == b'\x81\x00':
            et, p = fr[16:18], fr[18:]
        kind, info = None, {}
        if et == b'\x88\xf7' and len(p) >= 34:
            mt = p[0] & 15
            kind = {0: 'Sync', 8: 'FU', 2: 'PReq', 3: 'PResp', 10: 'PRFU', 11: 'Ann'}.get(mt, 'ptp%d' % mt)
            if mt == 11 and len(p) >= 61:
                info = dict(prio1=p[47], gm=p[53:61].hex())
        elif et == b'\x22\xf0' and p:
            kind = {0xFA: 'ADP', 0xFB: 'AECP', 0xFC: 'ACMP', 0x04: 'CRF'}.get(p[0], 'avtp')
            if p[0] == 0x04:
                info = dict(tu=p[1] & 1, seq=p[2])
        else:
            kind = 'other'
        out.append((t, port, kind, info))
    return out, resid, len(pts)


page_rows = {
    1: (20.29, 1.16, 3.56, 5.66, 38.24, 39.95, 39.66, 39.96, 40.46, 0.51),
    2: (20.40, 1.08, 3.48, 4.78, 37.75, 39.06, 38.78, 39.08, 39.58, 0.52),
    3: (20.39, 1.08, 2.88, 5.48, 38.07, 39.07, 39.48, 40.08, 40.58, 1.51),
    4: (20.29, 1.17, 3.66, 4.91, 38.57, 40.00, 39.91, 40.01, 40.42, 0.43),
    5: (20.40, 1.09, 2.96, 5.75, 38.07, 39.07, 39.71, 40.12, 40.54, 1.46),
    6: (20.40, 1.06, 3.24, 5.62, 38.12, 39.12, 39.68, 40.20, 40.72, 1.60),
}
cols = ('off_for', 'sync0', 'gm_own', 'asc0', 'sw_first', 'sw_ann1', 'asc1', 'gm_sw', 'good', 'recovery')
worst = 0.0
mism = []
for c in range(1, 7):
    cdir = os.path.join(bench, 'cycle%d' % c)
    ofs = offsets(cdir)
    pw = power(cdir)
    t_off = pw['T_OFF_CMD'] - ofs['strip']
    hold = pw['T_ON_CMD'] - pw['T_OFF_CMD']
    S = console(cdir)
    for s in S:
        s['r'] = s['t'] - t_off
    after = [s for s in S if s['r'] > 0]
    gaps = max(b['t'] - a['t'] for a, b in zip(S, S[1:]))
    epochs = sorted(set(s.get(0x90000720) for s in S))
    sync0 = next(s['r'] for s in after if s['sync'] == '0')
    gm_own = next(s['r'] for s in after if s['gm'] == DUT)
    asc0 = next(s['r'] for s in after if s['asc'] == '0')
    asc1 = next(s['r'] for s in after if s['r'] > asc0 and s['asc'] == '1')
    gm_sw = next(s['r'] for s in after if s['r'] > gm_own and s['gm'] == SWITCH)
    ok = [s['gm'] == SWITCH and s['sync'] == '1' and s['asc'] == '1' and s['tu'] == '0' for s in S]
    gi = None
    for i in range(len(S) - 1, -1, -1):
        if not ok[i]:
            gi = i + 1
            break
    good = S[gi]['r']
    hold_bits = [s for s in after if s['r'] < gm_own and int(s['clkv'], 16) & 8]
    fr, resid, nwin = tap(os.path.join(cdir, 'tap-c%d.pcap' % c))
    fr = [(t - ofs['capture'] - t_off, port, k, i) for t, port, k, i in fr]
    far = [x for x in fr if x[1] == 2]
    # the gap: largest interval between consecutive far-end frames
    gi2 = max(range(1, len(far)), key=lambda i: far[i][0] - far[i - 1][0])
    sw_last, sw_first = far[gi2 - 1][0], far[gi2][0]
    last_sync = max(x[0] for x in far if x[2] == 'Sync' and x[0] < sw_first)
    last_ann = max(x[0] for x in far if x[2] == 'Ann' and x[0] < sw_first)
    ann1 = next(x for x in far if x[2] == 'Ann' and x[0] >= sw_first)
    sync1 = next(x[0] for x in far if x[2] == 'Sync' and x[0] >= sw_first)
    ret = min(ann1[0], sync1)
    rec = good - ret
    worst = max(worst, rec)
    dut_master_sync = [x for x in fr if x[1] == 3 and x[2] == 'Sync' and sw_first <= x[0] <= gm_sw + 0.1]
    dut_own_ann = [x for x in fr if x[1] == 3 and x[2] == 'Ann' and x[3].get('gm') == DUT and x[0] > sw_first]
    silent_from = max(x[0] for x in fr if x[0] < sw_first)
    mine = (hold, sync0, gm_own, asc0, sw_first, ann1[0], asc1, gm_sw, good, rec)
    print('cycle %d: tap fit windows %d resid_max %.2f ms; console samples %d max gap %.3f s RST_EPOCH %s' % (
        c, nwin, resid * 1e3, len(S), gaps, epochs))
    print('   derived : ' + ' '.join('%s=%.3f' % (k, v) for k, v in zip(cols, mine)))
    print('   page    : ' + ' '.join('%s=%.2f' % (k, v) for k, v in zip(cols, page_rows[c])))
    d = [(k, round(v - p, 3)) for k, v, p in zip(cols, mine, page_rows[c]) if abs(round(v, 2) - p) > 0.011]
    print('   rounding-level agreement' if not d else '   DIFFERENCES %s' % d)
    if d:
        mism.append((c, d))
    print('   switch last frame %.3f, last Sync %.3f, last Announce %.3f; tap silent from %.3f to %.3f' % (
        sw_last, last_sync, last_ann, silent_from, sw_first))
    print('   sync0 - last Sync %.3f; gm_own - last Announce %.3f; ann1 prio1 %s gm %s; first Sync - ann1 %.3f' % (
        sync0 - last_sync, gm_own - last_ann, ann1[3].get('prio1'), ann1[3].get('gm'), sync1 - ann1[0]))
    print('   holdover-set samples during loss %d; DUT Sync as master %d; DUT own-GM Announce %d (prio1 %s)' % (
        len(hold_bits), len(dut_master_sync), len(dut_own_ann), sorted(set(x[3].get('prio1') for x in dut_own_ann))))
    print('   all-good minus on-command %.2f; minus switch first frame %.2f; asc1 - sw_first %.2f' % (
        good - hold, good - sw_first, asc1 - sw_first))
print('worst recovery %.3f s; bound 5 s; %s' % (worst, 'PASS' if worst < 5 else 'FAIL'))
print('cycles with differences beyond rounding:', mism if mism else 'none')
