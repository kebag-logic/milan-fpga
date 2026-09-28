#!/usr/bin/env python3
"""Order of DIN pair-offset states inside the playback region: collapses runs
shorter than 1000 frames (the dither at each change) and reports the sequence
of long states plus the transition census. Usage:
din_state_order.py <recording.pcap> <stream_id_hex> <first_frame> <last_frame>"""
import collections, json, struct, sys
import numpy as np
path, sid = sys.argv[1], bytes.fromhex(sys.argv[2]); a, b = int(sys.argv[3]), int(sys.argv[4])
data = open(path, "rb").read(); off = 24; pl = []
while off + 16 <= len(data):
    incl = struct.unpack_from("<I", data, off + 8)[0]; off += 16; pkt = data[off:off + incl]; off += incl
    p = 18 if pkt[12:14] == b"\x81\x00" else 14
    if pkt[p - 2:p] != b"\x22\xf0" or pkt[p] != 2 or pkt[p + 4:p + 12] != sid: continue
    sdl = struct.unpack_from(">H", pkt, p + 20)[0]; pl.append(pkt[p + 24:p + 24 + sdl])
w = np.frombuffer(b"".join(pl), dtype=">u4").reshape(-1, 8)[a:b + 1]
o = ((w >> 8) & 0xFFFF).astype(np.int64)[:, 0::2]
offs = ((o[:, 1:] - o[:, :1] + 32768) % 65536) - 32768
code = offs[:, 0] * 100 + offs[:, 1] * 10 + offs[:, 2]
names = {0: "0,0,0", -1: "0,0,-1", -11: "0,-1,-1", -111: "-1,-1,-1"}
chg = np.nonzero(np.diff(code))[0]
st = np.concatenate([[0], chg + 1]); en = np.concatenate([chg, [len(code) - 1]])
runs = [(int(code[s]), int(e - s + 1), int(s)) for s, e in zip(st, en)]
long_seq = []
for c, n, s in runs:
    if n >= 1000:
        if long_seq and long_seq[-1][0] == c: long_seq[-1][1] += n
        else: long_seq.append([c, n, s])
tr = collections.Counter((names.get(x[0], str(x[0])), names.get(y[0], str(y[0]))) for x, y in zip(long_seq, long_seq[1:]))
short = collections.Counter(n for c, n, s in runs if n < 1000)
print(json.dumps({"runs_total": len(runs), "long_states": len(long_seq),
                  "first_long_states": [[names.get(c, str(c)), n, s + a] for c, n, s in long_seq[:10]],
                  "long_state_transitions": [[f"{k[0]} -> {k[1]}", v] for k, v in tr.most_common()],
                  "short_runs": sum(short.values()), "short_run_max_len": max(short) if short else 0}, indent=1))
