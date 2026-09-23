#!/usr/bin/env python3
"""Second independent pass over the A202 (and A200) packets: console command
census, CLKV_TUCNT and path-generation deltas, CRF/licence edges and ACMP
CONNECT_TX probes in cycles 4 to 6, and controller counters.

usage: rederive_step3_extra.py EVIDENCE_ROOT
"""
import sys, os, re, json, struct, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location('s3', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rederive_step3.py'))
src = open(spec.origin).read().split('\npage_rows = {')[0]
ns = {'__name__': 's3', 'sys': sys}
sys_argv = sys.argv
sys.argv = ['x', 'unused']
exec(compile(src, spec.origin, 'exec'), ns)
sys.argv = sys_argv
root = sys.argv[1]
A202 = os.path.join(root, 'bench-a202', 'bench')

# 1. console command census over every console transcript in both packets
cmds = collections.Counter()
files = []
for p in sorted(glob.glob(os.path.join(root, '**', '*'), recursive=True)):
    if os.path.isfile(p) and re.search(r'console', os.path.basename(p)) and p.endswith('.txt'):
        t = open(p, encoding='latin-1').read()
        c = re.findall(r"^### \S+ cmd='([^']*)'", t, flags=re.M)
        if c:
            files.append(os.path.relpath(p, root))
            for x in c:
                cmds[x.split()[0]] += 1
print('console transcripts with commands: %d' % len(files))
for f in files:
    print('   ', f)
print('command verbs:', dict(cmds), 'total', sum(cmds.values()))

# 2. per cycle console counters and CRF edges
for c in range(1, 7):
    cdir = os.path.join(A202, 'cycle%d' % c)
    ofs = ns['offsets'](cdir)
    pw = ns['power'](cdir)
    t_off = pw['T_OFF_CMD'] - ofs['strip']
    S = ns['console'](cdir)
    for s in S:
        s['r'] = s['t'] - t_off
    tu = [s.get(0x90000780) for s in S if s.get(0x90000780) is not None]
    pg = [s['pgen'] for s in S]
    tu1 = [s['r'] for s in S if s['tu'] == '1']
    line = 'cycle %d: CLKV_TUCNT %s->%s (+%d); tu=1 samples span %.2f..%.2f s (%.1f s); AS_PATH_GEN %s->%s; path counts %s' % (
        c, tu[0], tu[-1], tu[-1] - tu[0], tu1[0], tu1[-1], tu1[-1] - tu1[0], pg[0], pg[-1], sorted(set(s['pcount'] for s in S)))
    print(line)
    if c >= 4:
        ctrl = [(s['r'], s.get(0x90000750)) for s in S]
        cnt = [(s['r'], s.get(0x90000764)) for s in S]
        drop = next(r for r, v in ctrl if r > 0 and v == 0x3)
        relic = next(r for r, v in ctrl if r > drop and v not in (0x3, None))
        print('   CRFT_CTRL values %s; licence dropped %.2f s; relicensed %.2f s' % (
            sorted('%#x' % v for v in set(v for _r, v in ctrl if v is not None)), drop, relic))
        fr, _resid, _n = ns['tap'](os.path.join(cdir, 'tap-c%d.pcap' % c))
        fr = [(t - ofs['capture'] - t_off, port, k, i) for t, port, k, i in fr]
        crf = [x for x in fr if x[2] == 'CRF']
        loss_tu1 = [x for x in crf if x[3]['tu'] == 1]
        pre = [x for x in crf if x[0] < 0]
        after = [x for x in crf if x[0] > 30]
        print('   CRF PDUs: %d total; tu=1 %d, first tu=1 at %.3f, last PDU before return %.3f; first PDU after return %.3f, tu=1 after return %d; pre-off tu=1 %d' % (
            len(crf), len(loss_tu1), loss_tu1[0][0] if loss_tu1 else float('nan'),
            max(x[0] for x in crf if x[0] < 30), after[0][0] if after else float('nan'),
            sum(x[3]['tu'] for x in after), sum(x[3]['tu'] for x in pre)))
        # console interval where CLKV_STAT bit 0 rose
        rise = next(i for i, s in enumerate(S) if s['r'] > 0 and int(s['clkv'], 16) & 1)
        print('   CLKV_STAT[0] rose between %.2f and %.2f s' % (S[rise - 1]['r'], S[rise]['r']))
        # ACMP CONNECT_TX_COMMAND (message type 0) reaching the DUT (port 2 = switch side)
        raw_acmp = []
        raw = open(os.path.join(cdir, 'tap-c%d.pcap' % c), 'rb').read()
        # reuse tap() output: need message type; decode again quickly
        fr2 = []
        off = 24
        first = None
        recs = []
        while off + 16 <= len(raw):
            s_, f_, incl, _o = struct.unpack('<IIII', raw[off:off + 16])
            pkt = raw[off + 16:off + 16 + incl]
            off += 16 + incl
            if len(pkt) < 42 or struct.unpack('<I', pkt[:4])[0] != 6:
                continue
            recs.append(pkt)
        # map ACMP frames by order to the decoded list (same filter order)
        decoded = [x for x in fr]
        k = 0
        acmp_times = []
        for pkt in recs:
            port = struct.unpack('<I', pkt[8:12])[0]
            if port not in (2, 3):
                continue
            t = decoded[k][0]
            k += 1
            fr_ = pkt[28:]
            et, p = fr_[12:14], fr_[14:]
            if et == b'\x81\x00':
                et, p = fr_[16:18], fr_[18:]
            if et == b'\x22\xf0' and p and p[0] == 0xFC and (p[1] & 15) == 0 and port == 2:
                acmp_times.append(t)
        good = None
        ok = [s['gm'] == '3cc0c6fffefe0210' and s['sync'] == '1' and s['asc'] == '1' and s['tu'] == '0' for s in S]
        for i in range(len(S) - 1, -1, -1):
            if not ok[i]:
                good = S[i + 1]['r']
                break
        between = [t for t in acmp_times if 0.5 < t < good]
        firstafter = [t for t in acmp_times if t >= good]
        print('   ACMP CONNECT_TX to the DUT: %d total; between loss and all-good (%.2f) %d; first after return %.2f; last before off %.2f' % (
            len(acmp_times), good, len(between), firstafter[0] if firstafter else float('nan'),
            max([t for t in acmp_times if t < 0.5] or [float('nan')])))
