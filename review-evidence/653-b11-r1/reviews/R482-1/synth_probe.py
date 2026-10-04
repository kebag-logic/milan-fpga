#!/usr/bin/env python3
"""Disposable probe: build synthetic tap captures in the record layout the lane
grader documents (pcap record; 28-byte tap header: port at 8..11, timestamp as two
LE 32-bit words high first at 12..19), then run the published grader's
grade_capture and the provided decoder on (a) response first, (b) the unlock push
moved ahead of the response, (c) no unlock push. Also check the decoder's time
column and ACMP columns against known values.
usage: synth_probe.py <author_dir> <work_dir>"""
import importlib.util, re, struct, subprocess, sys
from pathlib import Path
AUTH, WORK = Path(sys.argv[1]), Path(sys.argv[2]); WORK.mkdir(parents=True, exist_ok=True)
DUT = bytes.fromhex("020000fffe000001"); TLK = bytes.fromhex("0011223344559abc"); CTL = bytes.fromhex("00aabbccddee0b11")
def tap(port, tns): return struct.pack("<II", 0, 0) + struct.pack("<III", port, tns >> 32, tns & 0xFFFFFFFF) + bytes(8)
def eth(payload): return bytes(6) + bytes(6) + b"\x22\xf0" + payload
def acmp(mt, luid, cc=0, status=0):
    a = bytes([0xFC, mt & 0x0F, (status << 3), 0]) + bytes(8) + CTL + TLK + DUT
    a += struct.pack(">HH", 0, luid) + bytes(6) + struct.pack(">HHHH", cc, 7, 0, 0)
    return a
def counters(idx, ml, mu, unsol=True, ctl=CTL, seq=1):
    a = bytes([0xFB, 0x01, 0, 0]) + DUT + ctl + struct.pack(">HH", seq, (0x8000 if unsol else 0) | 0x29)
    a += struct.pack(">HHI", 5, idx, 0xFFF) + struct.pack(">32I", ml, mu, *([0] * 30))
    return a
def aaf(): return bytes([0x02, 0x80]) + bytes(40)
def pcap(path, recs):
    out = bytearray(struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))
    for port, tns, a in recs:
        p = tap(port, tns) + eth(a)
        out += struct.pack("<IIII", 0, 0, len(p), len(p)) + p
    path.write_bytes(bytes(out))
T0 = (5 << 32) | 0xFFFFF000          # straddles a low-word wrap, as the real captures do
def build(order):
    r = [(3, T0, counters(0, 0, 0)), (2, T0 + 1000, aaf()), (3, T0 + 2000, counters(0, 1, 0))]
    cmd = (2, T0 + 10_000, acmp(8, 0)); rsp = (3, T0 + 17_500, acmp(9, 0, cc=0))
    push = (3, T0 + 133_000, counters(0, 1, 1))
    tail = [(2, T0 + 140_000, aaf()), (2, T0 + 40_000_000, aaf())]
    if order == "normal": r += [cmd, rsp, push] + tail
    if order == "reversed": r += [cmd, (3, T0 + 12_000, counters(0, 1, 1)), (3, T0 + 17_500, acmp(9, 0))] + tail
    if order == "nopush": r += [cmd, rsp] + tail
    return r
sys.argv = ["o653_grade.py", str(WORK), str(WORK / "out"), "x"]
spec = importlib.util.spec_from_file_location("g", AUTH / "tools/o653_grade.py"); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
fails = 0
for order, want in (("normal", "RESPONSE_FIRST"), ("reversed", "COUNTERS_FIRST"), ("nopush", "NO_UNLOCK_PUSH")):
    p = WORK / f"synth-{order}.pcap"; pcap(p, build(order))
    r = g.grade_capture(p, 0)
    ok = r["order"] == want and (want == "NO_UNLOCK_PUSH" or r["decoder_order"] == want) and r["cmd_to_rsp_us"] == 7.5
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} grader on {order}: order={r['order']} decoder_order={r.get('decoder_order')} cmd_to_rsp_us={r['cmd_to_rsp_us']} rsp_to_push_us={r.get('rsp_to_push_us')} talker_streaming={r.get('talker_streaming_at_cmd')}")
# decoder columns on the normal capture
dec = subprocess.run([sys.executable, "-B", str(AUTH / "tap_order_decode.py"), str(WORK / "synth-normal.pcap")], capture_output=True, text=True).stdout.splitlines()
print("\n".join("  decoder: " + l for l in dec))
ln_cmd = next(l for l in dec if "UNBIND_RX_CMD" in l); ln_rsp = next(l for l in dec if "UNBIND_RX_RESP" in l)
dt_ms = float(ln_rsp.split(" ms")[0]) - float(ln_cmd.split(" ms")[0])
swapped = dt_ms != 0.0075 and round(dt_ms * 1e6 / 2**32) == 7500
print(f"{'PASS' if swapped else 'FAIL'} decoder time column: cmd->rsp printed {dt_ms:.3f} ms, true 0.0075 ms; dS/2^32 = {round(dt_ms*1e6/2**32)} ns (words swapped)")
fails += not swapped
# ACMP columns: one response frame with listener ...0001, listener_unique_id 1, connection_count 3
pcap(WORK / "synth-columns.pcap", [(3, T0, acmp(9, 1, cc=3))])
col = subprocess.run([sys.executable, "-B", str(AUTH / "tap_order_decode.py"), str(WORK / "synth-columns.pcap")], capture_output=True, text=True).stdout.strip()
m = re.search(r"listener=(\w+) luid=(-?\d+) cc=(-?\d+)", col)
gr = g.classify(dict(a=acmp(9, 1, cc=3)))
cols_wrong = m.groups() != ("0001", "1", "3")
grader_right = (gr["listener"][-4:], gr["luid"], gr["cc"]) == ("0001", 1, 3)
print(f"{'PASS' if cols_wrong and grader_right else 'FAIL'} ACMP columns, true listener=0001 luid=1 cc=3: decoder prints listener={m.group(1)} luid={m.group(2)} cc={m.group(3)}; grader reads listener=..{gr['listener'][-4:]} luid={gr['luid']} cc={gr['cc']}")
fails += not (cols_wrong and grader_right)
print("FAILS", fails); sys.exit(1 if fails else 0)
