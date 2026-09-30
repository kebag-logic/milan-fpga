#!/usr/bin/env python3
"""Per-channel and per-pair analysis of the DUT talker's AAF stream (offline).

usage: decode_din_pairs.py <pcap> <stream_id_hex> [<json_out>]

Same framing and pattern rule as decode_din_pcap.py: stream channel c is
expected to carry tag c + 1 in bits 31:24, a 16-bit ordinal in bits 23:8 and
a zero low byte. That decoder calls a frame torn when its eight channels
disagree on the ordinal, and skips torn frames in its step statistics. This
one looks inside them:

- the playback region: first to last frame in which all eight channels carry
  their own tag (outside it the SoC is not playing);
- inside the region, every word is classified (own tag, other tag, zero,
  non-pattern);
- channels 2p and 2p+1 form TDM pair p; the left/right ordinals of each pair
  are compared, and each pair's ordinal is compared with pair 0's (signed,
  modulo 2^16), giving a histogram of per-frame offset vectors;
- per channel, the ordinal step between consecutive frames is classified
  (+1, 0 repeat, +2 skip, other), with the frame indices of non-+1 steps,
  so channel continuity is measured without dropping any frame.
"""
import collections
import hashlib
import json
import struct
import sys


def frames_of(path, sid):
    raw = open(path, "rb").read()
    magic = raw[:4]
    endian = "<" if magic in (b"\xd4\xc3\xb2\xa1", b"\x4d\x3c\xb2\xa1") else ">"
    nano = magic in (b"\x4d\x3c\xb2\xa1", b"\xa1\xb2\x3c\x4d")
    pos = 24
    out = []
    meta = dict(pdus=0, seq_gaps=0, hdr_err=0, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    prev_seq = None
    while pos + 16 <= len(raw):
        sec, frac, incl, _ = struct.unpack(endian + "4I", raw[pos:pos + 16])
        fr = raw[pos + 16:pos + 16 + incl]
        pos += 16 + incl
        off = 12
        et = struct.unpack(">H", fr[off:off + 2])[0]
        if et == 0x8100:
            off += 4
            et = struct.unpack(">H", fr[off:off + 2])[0]
        p = fr[off + 2:]
        if et != 0x22F0 or len(p) < 24 or p[0] != 0x02 or p[4:12] != sid:
            continue
        meta["pdus"] += 1
        if prev_seq is not None and ((p[2] - prev_seq) & 0xFF) != 1:
            meta["seq_gaps"] += 1
        prev_seq = p[2]
        if p[16] != 0x02 or (p[17] >> 4) != 5 or (((p[17] & 3) << 8) | p[18]) != 8 or p[19] != 32 \
                or struct.unpack(">H", p[20:22])[0] != 192:
            meta["hdr_err"] += 1
            continue
        t = sec + frac / (1e9 if nano else 1e6)
        words = struct.unpack(">48I", p[24:216])
        for k in range(6):
            out.append((t, words[k * 8:(k + 1) * 8]))
    return out, meta


def own(v, c):
    return v != 0 and (v & 0xFF) == 0 and (v >> 24) == c + 1


def sgn(d):
    d &= 0xFFFF
    return d - 0x10000 if d >= 0x8000 else d


def runs_of(region):
    """Run-length summary of the per-frame pair-offset state (frames with an
    invalid word are skipped): how often the state changes, the transitions,
    and the state that follows each maximal all-equal run."""
    trans = collections.Counter()
    lengths = collections.defaultdict(list)
    cur, n = None, 0
    for _, w in region:
        if not all(own(w[c], c) for c in range(8)):
            continue
        o0 = (w[0] >> 8) & 0xFFFF
        st = tuple(sgn(((w[2 * p] >> 8) & 0xFFFF) - o0) for p in range(1, 4))
        if st == cur:
            n += 1
            continue
        if cur is not None:
            trans[(cur, st)] += 1
            lengths[cur].append(n)
        cur, n = st, 1
    if cur is not None:
        lengths[cur].append(n)
    return dict(changes=sum(trans.values()),
                transitions={f"{list(a)}->{list(b)}": v for (a, b), v in trans.most_common(12)},
                runs={json.dumps(list(k)): dict(count=len(v), min=min(v), max=max(v),
                                                mean=round(sum(v) / len(v), 1))
                      for k, v in lengths.items()})


def main():
    path, sid = sys.argv[1], bytes.fromhex(sys.argv[2])
    frames, meta = frames_of(path, sid)
    full = [i for i, (_, w) in enumerate(frames) if all(own(w[c], c) for c in range(8))]
    res = dict(file=path.split("/")[-1], bytes=meta["bytes"], sha256=meta["sha256"], stream_id=sid.hex(),
               pdus=meta["pdus"], frames=len(frames), sequence_gaps=meta["seq_gaps"],
               header_mismatch=meta["hdr_err"])
    if not full:
        res["region"] = None
        print(json.dumps(res, indent=1))
        return
    a, b = full[0], full[-1]
    region = frames[a:b + 1]
    res["region"] = dict(first_frame=a, last_frame=b, frames=len(region),
                         seconds_at_48k=round(len(region) / 48000, 3),
                         wall_span_s=round(region[-1][0] - region[0][0], 6))
    cls = [collections.Counter() for _ in range(8)]
    lr_mismatch = [0] * 4
    offsets = collections.Counter()
    steps = [collections.Counter() for _ in range(8)]
    step_at = [[] for _ in range(8)]
    prev = [None] * 8
    incomplete = 0
    for i, (_, w) in enumerate(region):
        ok = True
        ords = [None] * 8
        for c in range(8):
            v = w[c]
            if own(v, c):
                cls[c]["own_tag"] += 1
                ords[c] = (v >> 8) & 0xFFFF
            elif v == 0:
                cls[c]["zero"] += 1
                ok = False
            elif (v & 0xFF) == 0 and 1 <= (v >> 24) <= 8:
                cls[c]["other_tag"] += 1
                ok = False
            else:
                cls[c]["non_pattern"] += 1
                ok = False
        for c in range(8):
            if ords[c] is None:
                prev[c] = None
                continue
            if prev[c] is not None:
                d = sgn(ords[c] - prev[c])
                key = "+1" if d == 1 else "0" if d == 0 else "+2" if d == 2 else "other"
                steps[c][key] += 1
                if d != 1 and len(step_at[c]) < 5000:
                    step_at[c].append((a + i, d))
            prev[c] = ords[c]
        if not ok:
            incomplete += 1
            continue
        for p in range(4):
            if ords[2 * p] != ords[2 * p + 1]:
                lr_mismatch[p] += 1
        offsets[tuple(sgn(ords[2 * p] - ords[0]) for p in range(1, 4))] += 1
    res["incomplete_frames_in_region"] = incomplete
    res["per_channel"] = [dict(stream_channel=c, expected_tag=c + 1, words=dict(cls[c]),
                               steps=dict(steps[c])) for c in range(8)]
    res["left_right_mismatch_per_pair"] = lr_mismatch
    res["pair_offset_vs_pair0"] = {json.dumps(list(k)): v for k, v in offsets.most_common()}
    res["offset_state_runs"] = runs_of(region)
    # group each channel's non-+1 steps closer than 50 ms (2,400 frames) into
    # clusters, as the capture decoder does, to compare with the beat
    ev = []
    for c in range(8):
        cl = []
        for f, d in step_at[c]:
            if cl and f - cl[-1]["last_frame"] <= 2400:
                k = cl[-1]
            else:
                k = dict(first_frame=f, last_frame=f, repeats=0, skips=0, other=0)
                cl.append(k)
            k["last_frame"] = f
            k["repeats" if d == 0 else "skips" if d == 2 else "other"] += 1
        starts = [k["first_frame"] for k in cl]
        gaps = [q - p for p, q in zip(starts, starts[1:])]
        net = collections.Counter(k["skips"] - k["repeats"] for k in cl)
        ev.append(dict(stream_channel=c, events=len(step_at[c]), clusters=len(cl),
                       cluster_gap_min=min(gaps) if gaps else None, cluster_gap_max=max(gaps) if gaps else None,
                       net_skips_minus_repeats_per_cluster=dict(sorted(net.items())),
                       other_steps=sum(k["other"] for k in cl), first_clusters=cl[:3]))
    res["step_clusters"] = ev
    s = json.dumps(res, indent=1)
    print(s)
    if len(sys.argv) > 3:
        open(sys.argv[3], "w").write(s + "\n")


if __name__ == "__main__":
    main()
