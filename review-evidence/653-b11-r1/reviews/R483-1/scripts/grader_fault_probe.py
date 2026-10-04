#!/usr/bin/env python3
"""Fault probe for the published lane grader (o653_grade.py) and the provided decoder.
Builds synthetic captures in the tap's record format (28-byte header: port at 8..11, the 64-bit
ns timestamp as two LE 32-bit words high first at 12..19) and runs grade_capture() unchanged.
usage: grader_fault_probe.py <dir holding tools/o653_grade.py and tap_order_decode.py> <workdir>"""
import hashlib, importlib.util, json, struct, sys
from pathlib import Path
src, work = Path(sys.argv[1]), Path(sys.argv[2]); work.mkdir(parents=True, exist_ok=True)
DUT = bytes.fromhex('020000fffe000001'); CTL = bytes.fromhex('90e0f0fffe000b11'); TALK = bytes.fromhex('001b92fffe010000')
def acmp(mt, status=0, luid=0):
    a = bytes([0xFC, mt]) + struct.pack('>H', (status << 11) | 44) + bytes(8) + CTL + TALK + DUT + struct.pack('>HH', 0, luid) + bytes(6) + struct.pack('>HHHH', 0, 1, 0, 0)
    assert len(a) == 54; return a
def push(cmd, ml, mu, si=0, idx=0, seq=1):
    ct = 0x8000 | cmd
    a = bytes([0xFB, 1]) + struct.pack('>H', 0) + DUT + CTL + struct.pack('>HH', seq, ct)
    if cmd == 0x29:
        a += struct.pack('>HHI', 5, idx, 0xfff) + struct.pack('>32I', ml, mu, si, *([0] * 29))
    else:
        a += struct.pack('>HHI', 5, idx, 0)
    return a
def aaf(): return bytes([0x02, 0x81]) + bytes(30)
def frame(avtp): return bytes.fromhex('91e0f000fe00') + bytes.fromhex('020000000001') + b'\x22\xf0' + avtp
def pcap(path, recs):
    out = struct.pack('<IHHiIII', 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1)
    for port, tns, avtp in recs:
        f = frame(avtp)
        hdr = bytes(8) + struct.pack('<III', port, tns >> 32, tns & 0xffffffff) + struct.pack('<I', len(f)) + bytes(4)
        p = hdr + f
        out += struct.pack('<IIII', 0, 0, len(p), len(p)) + p
    path.write_bytes(out)
spec = importlib.util.spec_from_file_location('g', src / 'tools' / 'o653_grade.py')
sys.argv = ['o653_grade.py', str(work), str(work / 'out'), 'x']
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
T0 = (7 << 32) + (2 ** 32 - 3000)      # the low word wraps 3 us after the command
def base(order):
    r = [(2, T0 - 2_000_000_000, aaf()), (3, T0 - 1_900_000_000, push(0x29, 1, 0, seq=1))]
    r += [(2, T0 - 125_000 * k, aaf()) for k in range(5, 0, -1)]
    cmd = (2, T0, acmp(8)); rsp = (3, T0 + 7_500, acmp(9))
    gsi = (3, T0 + 60_000, push(0x0F, 0, 0, seq=2)); pu = (3, T0 + 123_000, push(0x29, 1, 1, seq=3))
    tail = [(2, T0 + 125_000 * k, aaf()) for k in range(1, 4)]
    if order == 'response_first': body = [cmd, rsp, gsi, pu]
    elif order == 'counters_first': body = [cmd, (3, T0 + 3_000, push(0x29, 1, 1, seq=3)), (3, T0 + 7_500, acmp(9)), gsi]
    elif order == 'push_before_cmd': body = [(3, T0 - 50_000, push(0x29, 1, 1, seq=3)), cmd, rsp, gsi]
    elif order == 'other_index_first': body = [cmd, (3, T0 + 3_000, push(0x29, 1, 1, idx=1, seq=3)), rsp, gsi, pu]
    elif order == 'unbind_other_input_first': body = [(2, T0 - 9_000, acmp(8, luid=1)), (3, T0 - 1_500, acmp(9, luid=1)), cmd, (3, T0 + 3_000, push(0x29, 1, 1, seq=3)), rsp, gsi]
    recs = sorted(r + body + tail, key=lambda x: x[1])
    return recs
expect = {'response_first': ('RESPONSE_FIRST', 'RESPONSE_FIRST'), 'counters_first': ('COUNTERS_FIRST', 'COUNTERS_FIRST'),
          'push_before_cmd': ('NO_UNLOCK_PUSH', 'NO_LINES'), 'other_index_first': ('RESPONSE_FIRST', 'RESPONSE_FIRST'),
          'unbind_other_input_first': ('COUNTERS_FIRST', None)}
fails = 0
for case, (eg, ed) in expect.items():
    p = work / f'probe-{case}.pcap'; pcap(p, base(case))
    r = g.grade_capture(p, 0)
    ok = r['order'] == eg and (ed is None or r['decoder_order'] == ed)
    fails += not ok
    print(('OK  ' if ok else 'FAIL'), case, 'grader=', r['order'], 'decoder=', r['decoder_order'], 'cmd_to_rsp_us=', r.get('cmd_to_rsp_us'),
          'rsp_to_push_us=', r.get('rsp_to_push_us'), 'monotonic=', r['tap_time_monotonic_in_file_order'], 'expected=', (eg, ed))
print('FAILS', fails)
print('grader sha256', hashlib.sha256((src / 'tools' / 'o653_grade.py').read_bytes()).hexdigest())
print('decoder sha256', hashlib.sha256((src / 'tap_order_decode.py').read_bytes()).hexdigest())
sys.exit(1 if fails else 0)
