#!/usr/bin/env python3
"""Independent decode of a DUT talker AAF recording (classic pcap, Ethernet).

Selects AVTP (0x22f0, optional 802.1Q tag) AAF (subtype 0x02) PDUs of one
stream_id, checks sequence continuity, and unpacks big-endian 32-bit samples
into a (frames, channels) array. Pattern word as in decode_dout.py.
Prints JSON with header census, sequence gaps, zero/idle/valid counts, the
playback region (first..last frame where every channel carries its own tag),
per-channel tag table inside it, torn-frame and pair-offset census, and
per-channel continuity clusters.
Usage: decode_din.py <recording.pcap> <stream_id_hex> [cluster_gap_frames]
"""
import collections
import json
import struct
import sys

import numpy as np

path, sid_hex = sys.argv[1], sys.argv[2]
gap = int(sys.argv[3]) if len(sys.argv) > 3 else 2400
sid = bytes.fromhex(sid_hex)
data = open(path, "rb").read()
magic = struct.unpack_from("<I", data, 0)[0]
assert magic == 0xA1B2C3D4, hex(magic)
linktype = struct.unpack_from("<I", data, 20)[0]
assert linktype == 1
off = 24
records = 0
other = collections.Counter()
hdr = collections.Counter()
seqs = []
payloads = []
while off + 16 <= len(data):
    ts_s, ts_us, incl, orig = struct.unpack_from("<IIII", data, off)
    off += 16
    pkt = data[off:off + incl]
    off += incl
    records += 1
    et = struct.unpack_from(">H", pkt, 12)[0]
    p = 14
    vlan = None
    if et == 0x8100:
        vlan = struct.unpack_from(">H", pkt, 14)[0]
        et = struct.unpack_from(">H", pkt, 16)[0]
        p = 18
    if et != 0x22F0:
        other["ethertype_%04x" % et] += 1
        continue
    subtype = pkt[p]
    if subtype != 0x02 or pkt[p + 4:p + 12] != sid:
        other["avtp_subtype_%02x_other" % subtype] += 1
        continue
    b1 = pkt[p + 1]
    seq = pkt[p + 2]
    fmt = pkt[p + 16]
    nsr_cpf = struct.unpack_from(">H", pkt, p + 17)[0]
    nsr = nsr_cpf >> 12
    cpf = nsr_cpf & 0x3FF
    depth = pkt[p + 19]
    sdl = struct.unpack_from(">H", pkt, p + 20)[0]
    tv = b1 & 1
    hdr[(vlan >> 13 if vlan is not None else None, vlan & 0xFFF if vlan is not None else None,
         fmt, nsr, cpf, depth, sdl, tv, (b1 >> 7) & 1)] += 1
    seqs.append(seq)
    payloads.append(pkt[p + 24:p + 24 + sdl])
out = {"records": records, "non_stream_records": dict(other), "pdus": len(seqs),
       "header_census": [{"pcp": k[0], "vid": k[1], "format": k[2], "nsr": k[3], "channels_per_frame": k[4],
                          "bit_depth": k[5], "stream_data_length": k[6], "tv": k[7], "sv": k[8], "pdus": v}
                         for k, v in hdr.items()]}
s = np.array(seqs, dtype=np.int64)
ds = np.diff(s) % 256
out["seq_gaps"] = int(np.sum(ds != 1))
out["seq_missing_pdus"] = int(np.sum(np.where(ds != 1, (ds - 1) % 256, 0)))
cpf = out["header_census"][0]["channels_per_frame"]
assert all(h["channels_per_frame"] == cpf for h in out["header_census"])
raw = b"".join(payloads)
w = np.frombuffer(raw, dtype=">u4").astype(np.uint32).reshape(-1, cpf)
out["frames"] = int(w.shape[0])
out["all_zero_frames"] = int(np.sum(np.all(w == 0, axis=1)))
out["zero_words"] = int(np.sum(w == 0))
out["idle_ffffff00_words"] = int(np.sum(w == 0xFFFFFF00))
low = w & 0xFF
tag = (w >> 24).astype(np.int64)
ordv = ((w >> 8) & 0xFFFF).astype(np.int64)
own = (low == 0) & (tag == (np.arange(cpf) + 1)[None, :])
allown = np.all(own, axis=1)
idx = np.nonzero(allown)[0]
if idx.size == 0:
    out["playback_region"] = None
    vals, cnts = np.unique(w, return_counts=True)
    out["distinct_word_values"] = {("%08x" % v): int(c) for v, c in zip(vals[:16], cnts[:16])}
    out["distinct_word_value_count"] = int(vals.size)
    print(json.dumps(out, indent=1))
    sys.exit(0)
a, b = int(idx[0]), int(idx[-1])
R = slice(a, b + 1)
n = b - a + 1
out["playback_region"] = {"first_frame": a, "last_frame": b, "frames": n, "seconds_at_48k": n / 48000.0}
wr, tr, orr = w[R], tag[R], ordv[R]
validr = (wr & 0xFF == 0) & (tr >= 1) & (tr <= 8)
out["region_invalid_words"] = int((~validr).sum())
out["region_not_own_tag_words"] = int((~own[R]).sum())
out["channels"] = []
for c in range(cpf):
    t, k = np.unique(tr[:, c], return_counts=True)
    out["channels"].append({"stream_channel": c, "tag_histogram": {int(x): int(y) for x, y in zip(t, k)},
                            "valid_words": int(validr[:, c].sum())})
outside = np.concatenate([w[:a], w[b + 1:]])
ov, oc = np.unique(outside, return_counts=True)
out["outside_region_frames"] = int(outside.shape[0])
out["outside_region_word_values_top"] = {("%08x" % v): int(c) for v, c in sorted(zip(ov, oc), key=lambda x: -x[1])[:6]}
torn = np.any(orr != orr[:, :1], axis=1)
out["torn_frames"] = int(torn.sum())
pair_intra = np.any(orr[:, 0::2] != orr[:, 1::2], axis=1)
out["frames_with_pair_internal_disagreement"] = int(pair_intra.sum())
p = orr[:, 0::2]
offs = ((p[:, 1:] - p[:, :1] + 32768) % 65536) - 32768
shapes = collections.Counter(map(tuple, offs.tolist()))
out["pair_offset_shapes"] = [{"offsets_pairs_1_2_3": list(k), "frames": v, "share": round(v / n, 4)}
                             for k, v in shapes.most_common()]
# run lengths per shape
code = np.array([hash(tuple(r)) for r in offs.tolist()])
chg = np.nonzero(np.diff(code) != 0)[0]
bounds = np.concatenate([[-1], chg, [n - 1]])
runs = collections.defaultdict(int)
for i in range(len(bounds) - 1):
    s0, s1 = bounds[i] + 1, bounds[i + 1]
    key = tuple(offs[s0].tolist())
    runs[key] = max(runs[key], int(s1 - s0 + 1))
out["longest_run_per_shape"] = {str(list(k)): v for k, v in runs.items()}
# per-channel continuity
out["per_channel_continuity"] = []
for c in range(cpf):
    d = np.diff(orr[:, c]) % 65536
    st, sc = np.unique(d, return_counts=True)
    disc = np.nonzero(d != 1)[0]
    cl = []
    if disc.size:
        m = [disc[0]]
        for i in disc[1:]:
            if i - m[-1] < gap:
                m.append(i)
            else:
                cl.append(m)
                m = [i]
        cl.append(m)
    starts = [int(x[0]) for x in cl]
    nets = collections.Counter()
    for x in cl:
        x = np.array(x)
        nets[int(np.sum(d[x] == 0)) - int(np.sum(np.where((d[x] > 1) & (d[x] < 32768), d[x] - 1, 0)))] += 1
    sp = np.diff(starts)
    out["per_channel_continuity"].append({
        "stream_channel": c, "step_histogram": {int(x): int(y) for x, y in zip(st, sc)},
        "repeated": int(np.sum(d == 0)),
        "skipped": int(np.sum(np.where((d > 1) & (d < 32768), d - 1, 0))),
        "backward_or_large": int(np.sum(d >= 32768)),
        "clusters": len(cl), "cluster_net_repeat_histogram": {str(k): v for k, v in nets.items()},
        "first_cluster_recording_frame": (starts[0] + a) if starts else None,
        "cluster_spacing_min": int(sp.min()) if sp.size else None,
        "cluster_spacing_max": int(sp.max()) if sp.size else None,
    })
print(json.dumps(out, indent=1))
