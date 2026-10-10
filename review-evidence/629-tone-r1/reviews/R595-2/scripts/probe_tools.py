#!/usr/bin/env python3
"""Disposable probes of the lane's tap decode and alignment tools (copies with placeholder IDs).
usage: probe_tools.py <probe-dir containing tools/>   (writes <probe-dir>/probe-*.pcap/.raw, prints JSON lines)"""
import json, os, struct, subprocess, sys
import numpy as np
P = sys.argv[1]
sys.path.insert(0, os.path.join(P, 'tools'))
import tone_points_b15 as TP
import align_b15 as AL
SID = '0205aabbccdd0000'
rng = np.random.default_rng(629)
N = 1_152_000  # 24 s at 48 kHz
# A floor like the lane's: values -2..+1, mostly -1/0, independent per channel
floor = rng.choice([-2, -1, 0, 1], size=(N, 4), p=[0.02, 0.5, 0.46, 0.02]).astype(np.int64)

def write_pcap(path, x, port=2, cpf=4):
    words = (x << 8) & 0xFFFFFFFF
    out = bytearray(struct.pack('<IHHiIII', 0xA1B2C3D4, 2, 4, 0, 0, 262144, 1))
    for pdu in range(len(x) // 6):
        pay = words[pdu * 6:(pdu + 1) * 6].reshape(-1).astype('>u4').tobytes()
        avtp = bytes([0x02, 0x81, pdu & 0xFF, 0]) + bytes.fromhex(SID) + struct.pack('>I', pdu * 125000 & 0xFFFFFFFF) + \
            bytes([0x02, 0x50, cpf, 32]) + struct.pack('>H', len(pay)) + b'\x10\x00' + pay
        eth = bytes.fromhex('91e0f000fe00') + bytes.fromhex('0205aabbccdd') + b'\x81\x00\x60\x02\x22\xf0' + avtp
        rec = struct.pack('<IIIIII', 6, 0x110, port, 0, 0, len(eth)) + struct.pack('<I', len(eth)) + eth
        out += struct.pack('<IIII', pdu // 8000, (pdu % 8000) * 125, len(rec), len(rec)) + rec
    open(path, 'wb').write(out)

def mcasp_from(m4):
    w = np.zeros((len(m4), 8), dtype=np.int64); w[:, :4] = m4
    return ((w << 8) & 0xFFFFFFFF).astype('<u4')

pc = os.path.join(P, 'probe-floor.pcap'); write_pcap(pc, floor)
s, info = AL.load(pc, SID, 2, 4)
print(json.dumps(dict(probe='decode floor exact', ok=bool(np.array_equal(s, floor)), seq_gaps=info['seq_gaps'])))
base = floor[300000:780000]
def plus(m, idx, v):
    m = m.copy(); m[idx] += v; return m
cases = {
    'P1 exact 10 s recording': (base.copy(), 'SAMPLE-EXACT'),
    'P2 channels 2 and 3 swapped': (base[:, [0, 1, 3, 2]].copy(), 'NOT SAMPLE-EXACT'),
    'P3 one sample +256 (outside the 8-bit key)': (plus(base, (200000, 1), 256), 'NOT SAMPLE-EXACT'),
    'P4 every sample of channel 0 +256': (plus(base, (slice(None), 0), 256), 'NOT SAMPLE-EXACT'),
    'P5 one frame dropped': (np.delete(floor[300000:780001], 123456, axis=0), 'NOT SAMPLE-EXACT'),
}
for label, (m, want) in cases.items():
    raw = os.path.join(P, 'probe-mcasp.raw'); mcasp_from(m).tofile(raw)
    w = np.fromfile(raw, dtype='<i4'); mm = (w.reshape(-1, 8)[:, :4].astype(np.int64) >> 8)
    r = AL.compare(s, mm, 4, info['seq_gaps'])
    ok = (r.get('verdict') == 'SAMPLE-EXACT') == (want == 'SAMPLE-EXACT')
    print(json.dumps(dict(probe=label, want=want, verdict=r.get('verdict'), slips=r.get('slips'), differing=r.get('frames_differing'),
                          matches=r.get('matches_of_first_window'), tool_detects=ok)))
# The lane's own alignment controls, on this synthetic floor stream
cj = os.path.join(P, 'probe-align-controls.json')
rc = AL.controls(pc, SID, 2, cj)
print(json.dumps(dict(probe='align_b15 controls on a synthetic floor', rc=rc, all_pass=json.load(open(cj))['all_pass'])))
# Decode: floor-only stream verdict; and a -38.5 dBFS tone pair on channels 0/1 over the floor
r = TP.cmd_tap(pc, SID, os.path.join(P, 'probe-floor.json'), 2)
print(json.dumps(dict(probe='floor verdict', verdict=r['verdict'], rms=[c['rms_dbfs'] for c in r['channels']])))
k = np.arange(N)
for lvl in (-38.5, -41.5):
    a = 10 ** (lvl / 20) * 2 ** 23 * np.sqrt(2)  # RMS level lvl
    t = floor.copy(); t[:, 0] += np.round(a * np.sin(2 * np.pi * 997 * k / 48000)).astype(np.int64)
    t[:, 1] += np.round(a * np.sin(2 * np.pi * 9973 * k / 48000)).astype(np.int64)
    pt = os.path.join(P, 'probe-tone.pcap'); write_pcap(pt, t)
    r = TP.cmd_tap(pt, SID, os.path.join(P, 'probe-tone.json'), 2)
    print(json.dumps(dict(probe=f'tone pair at {lvl} dBFS RMS over the floor', verdict=r['verdict'], tone_channels=r['tone_channels'],
                          rms=[c['rms_dbfs'] for c in r['channels'][:2]], share=[r['channels'][0]['share_997'], r['channels'][1]['share_9973']])))
