#!/usr/bin/env python3
"""Round 2 receipts for lane B11 (#653), docs only, from files already in the packet.

Writes three receipts next to this script:
  library-check.txt   the controller library's STREAM_INPUT counter-value check at tag v4.3.1.1,
                      quoted from the public source archive (kept outside the packet, hash recorded),
                      tied to the bench's source tree by its describe line and the copied header's hash;
  control-interval.txt  the control C0's two intervals from the provided decoder's text and the grade;
  library-updates.txt   every STREAM_INPUT counters update the library delivered in s0b and s1, with
                      the input's connection state, and each CRF cycle's updates around the unbind.
Usage: r2_receipts.py <packet dir> <unpacked library source dir> <library archive>
"""
import hashlib, json, os, re, sys

pkt, src, archive = sys.argv[1:4]
out = os.path.dirname(os.path.abspath(__file__))
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()

# 1. The library check
cpp = os.path.join(src, 'src/controller/avdeccControllerImpl.cpp')
lines = open(cpp, encoding='utf-8').read().split('\n')
hits = []
for root in ('src', 'include'):
    for dp, _, fs in os.walk(os.path.join(src, root)):
        for f in sorted(fs):
            p = os.path.join(dp, f)
            for i, l in enumerate(open(p, encoding='utf-8', errors='replace').read().split('\n'), 1):
                if 'MediaUnlocked' in l or 'MEDIA_UNLOCKED' in l:
                    hits.append(f'{os.path.relpath(p, src)}:{i}: {l.strip()[:160]}')
hdr = os.path.join(src, 'include/la/avdecc/controller/internals/avdeccVirtualControlledEntityInterface.hpp')
b3 = open(os.path.join(pkt, 'runs/build/build-3.txt'), encoding='utf-8').read().split('\n')
b3hdr = next(l.split()[0] for l in b3 if l.endswith('avdeccVirtualControlledEntityInterface.hpp') and len(l.split()[0]) == 64)
with open(os.path.join(out, 'library-check.txt'), 'w') as o:
    o.write('Controller library STREAM_INPUT counter-value check, public source at tag v4.3.1.1\n')
    o.write('tag object 080ab851ba558e8502c5d44522a3012bee007440 -> commit 6d61a92e7f264c69f23cdc38f50d31114e567aa0\n')
    o.write(f'source archive (outside the packet) sha256 {sha(archive)} bytes {os.path.getsize(archive)}\n')
    o.write(f'src/controller/avdeccControllerImpl.cpp sha256 {sha(cpp)} bytes {os.path.getsize(cpp)}\n\n')
    o.write('Function holding the check (called on every STREAM_INPUT counters update):\n')
    o.write(f'1590: {lines[1589].strip()[:120]} ...\n\n')
    for n in range(1605, 1616):
        o.write(f'{n}: {lines[n - 1]}\n')
    o.write('\nEvery MediaUnlocked / MEDIA_UNLOCKED line in src/ and include/ at the tag:\n')
    o.write('\n'.join(hits) + '\n')
    o.write('\nThe bench source tree (runs/build/build-3.txt line 2, git describe --tags --always): '
            f'{b3[1].strip()}\n')
    o.write(f'Header copied from the bench tree (build-3.txt): {b3hdr}\n')
    o.write(f'Same header at the public tag:                 {sha(hdr)}\n')
    o.write(f'EQUAL: {b3hdr == sha(hdr)}\n')
    o.write('\nCondition: the Milan flag is removed only when MEDIA_LOCKED != MEDIA_UNLOCKED and\n'
            'MEDIA_LOCKED != MEDIA_UNLOCKED + 1. The connection state is not an input.\n')

# 2. The control interval
dec = open(os.path.join(pkt, 'summary/decode/b11-a535-s0b-C0.decode.txt'), encoding='utf-8').read().split('\n')
ms = lambda pat: float(next(l for l in dec if re.search(pat, l)).split()[0])
own = ms(r'DUT->sw\s+AECP RSP GET_COUNTERS .*seq=2 ')
cmd = ms(r'UNBIND_RX_CMD'); rsp = ms(r'UNBIND_RX_RESP')
us = lambda a, b: (b - a) * 1e6 / 2**32 / 1e3   # decoder column = LE64 of the swapped words, in ms
g = json.load(open(os.path.join(pkt, 'summary/o653-grade.json')))
ctl = next(v for k, v in g.items() if k.endswith('C0') or (isinstance(v, dict) and 'C0' in v))
ctl = ctl['C0'] if 'C0' in ctl else ctl
with open(os.path.join(out, 'control-interval.txt'), 'w') as o:
    o.write('Control C0, from summary/decode/b11-a535-s0b-C0.decode.txt (the provided decoder, unchanged).\n')
    o.write('Its time column is (S - S0)/1e6 with S the LE64 read of the tap record\'s two words; the\n'
            'true interval in ns is dS/2^32 while the low word does not wrap.\n')
    o.write(f'probe GET_COUNTERS answer -> UNBIND_RX command : {us(own, cmd):.3f} us\n')
    o.write(f'probe GET_COUNTERS answer -> UNBIND_RX response: {us(own, rsp):.3f} us\n')
    o.write(f'UNBIND_RX command -> response                  : {us(cmd, rsp):.3f} us\n')
    o.write(f'grade own_rsp_to_cmd_us (cmd - own)            : {ctl["wire"]["control"]["own_rsp_to_cmd_us"]}\n')

# 3. Library updates
with open(os.path.join(out, 'library-updates.txt'), 'w') as o:
    pairs = {}
    for s in ('s0b', 's1'):
        cyc = None
        for l in open(os.path.join(pkt, f'runs/{s}/{s}-probe.jsonl'), encoding='utf-8'):
            e = json.loads(l)
            if e['ev'] == 'cycle_begin':
                cyc, t0 = e['tag'], e['t']
            if e['ev'] == 'si_counters' and e.get('who') == 'dut':
                c = e['counters']
                k = (c['ML'], c['MU'], e['lib_conn'])
                pairs[k] = pairs.get(k, 0) + 1
            if cyc in ('R01', 'R02') and e['ev'] in ('bind', 'unbind', 'si_connection', 'si_counters') \
                    and e.get('idx', 1) == 1 and e.get('who', 'dut') == 'dut':
                c = e.get('counters')
                o.write(f'{s} {cyc} +{(e["t"] - t0) / 1e3:9.3f} ms {e["ev"]:13} '
                        + (f'{e["state"]}' if e['ev'] == 'si_connection' else '')
                        + (f'ML={c["ML"]} MU={c["MU"]} lib_conn={e["lib_conn"]}' if c else '')
                        + (f'status={e["status"]}' if e['ev'] in ('bind', 'unbind') else '') + '\n')
    o.write('\nEvery DUT STREAM_INPUT counters update the library delivered (s0b and s1), by\n'
            'MEDIA_LOCKED, MEDIA_UNLOCKED and the library\'s connection state at that update:\n')
    for k in sorted(pairs, key=str):
        ok = k[0] == k[1] or k[0] == k[1] + 1
        o.write(f'  {k[0]}/{k[1]} {k[2]:13} x{pairs[k]:3}  accepted by the check: {ok}\n')
print('ok')
