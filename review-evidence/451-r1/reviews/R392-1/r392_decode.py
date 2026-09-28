#!/usr/bin/env python3
"""Independent reviewer decoder for the #451 TDM8 first-light raw captures.

Written from the page's stated pattern rule only (docs/findings/451_TDM8_FIRST_LIGHT.md,
"Method"): word = ((t << 16) | (n & 0xffff)) << 8, tag t = channel + 1, low byte zero.

  r392_decode.py raw     <S32_LE 8ch capture>          DOUT capture decode
  r392_decode.py pattern <S32_LE 8ch pattern>          pattern-source check
  r392_decode.py pcap    <pcap> <stream_id_hex>        DIN talker-stream decode

Prints one JSON object. Needs numpy. No bench access.
"""
import json
import struct
import sys

import numpy as np

CH = 8
CLUSTER_GAP = 2400  # 50 ms at 48 kHz, the page's clustering rule


def words_to_fields(w):
    w = w.astype(np.uint32)
    low = w & 0xFF
    tag = (w >> 24) & 0xFF
    ordv = (w >> 8) & 0xFFFF
    return low, tag, ordv


def valid_mask(w):
    low, tag, _ = words_to_fields(w)
    return (low == 0) & (tag >= 1) & (tag <= 8)


def own_tag_mask(w):
    low, tag, _ = words_to_fields(w)
    own = np.arange(1, CH + 1, dtype=np.uint32)[None, :]
    return (low == 0) & (tag == own)


def continuity(ordv):
    """Per-sequence ordinal step classification (mod 2^16)."""
    d = (ordv[1:].astype(np.int64) - ordv[:-1].astype(np.int64)) % 65536
    rep_idx = np.nonzero(d == 0)[0]
    drop_idx = np.nonzero((d != 0) & (d != 1))[0]
    drops = int(np.sum(d[drop_idx] - 1)) if drop_idx.size else 0
    # a step backwards (d large) would show as a huge "drop"; report separately
    back_idx = np.nonzero(d > 32768)[0]
    events = np.sort(np.concatenate([rep_idx, drop_idx]))
    clusters = []
    if events.size:
        start = events[0]
        prev = events[0]
        members = [events[0]]
        for e in events[1:]:
            if e - prev <= CLUSTER_GAP:
                members.append(e)
            else:
                clusters.append(members)
                members = [e]
            prev = e
        clusters.append(members)
    cl = []
    for m in clusters:
        m = np.array(m)
        r = int(np.sum(d[m] == 0))
        dr = int(np.sum(d[m][d[m] != 0] - 1))
        cl.append({"first": int(m[0]), "repeated": r, "dropped": dr})
    return {
        "repeated": int(rep_idx.size),
        "dropped": drops,
        "backward_steps": int(back_idx.size),
        "clusters": cl,
    }


def cluster_summary(cl):
    firsts = [c["first"] for c in cl]
    sp = np.diff(firsts) if len(firsts) > 1 else np.array([])
    nets = {}
    for c in cl:
        k = c["repeated"] - c["dropped"]
        nets[k] = nets.get(k, 0) + 1
    return {
        "count": len(cl),
        "repeated": sum(c["repeated"] for c in cl),
        "dropped": sum(c["dropped"] for c in cl),
        "net_repeat_minus_drop_hist": {str(k): v for k, v in sorted(nets.items())},
        "first_at": firsts[0] if firsts else None,
        "spacing_min": int(sp.min()) if sp.size else None,
        "spacing_max": int(sp.max()) if sp.size else None,
    }


def decode_frames(w, region=None):
    """w: (N, 8) uint32 words."""
    n = w.shape[0]
    out = {"frames": int(n)}
    zero_frames = np.all(w == 0, axis=1)
    out["all_zero_frames"] = int(zero_frames.sum())
    out["zero_words"] = int((w == 0).sum())
    nz = np.nonzero(~zero_frames)[0]
    out["first_nonzero_frame"] = int(nz[0]) if nz.size else None
    out["last_nonzero_frame"] = int(nz[-1]) if nz.size else None
    own = own_tag_mask(w)
    all_own = np.all(own, axis=1)
    idx = np.nonzero(all_own)[0]
    if region is None:
        region = (int(idx[0]), int(idx[-1])) if idx.size else None
    out["own_tag_region"] = region
    if region is None:
        vals, cnts = np.unique(w, return_counts=True)
        top = sorted(zip(cnts.tolist(), vals.tolist()), reverse=True)[:5]
        out["top_word_values"] = [[f"{v:08x}", c] for c, v in top]
        return out
    a, b = region
    r = w[a : b + 1]
    out["region_frames"] = int(r.shape[0])
    low, tag, ordv = words_to_fields(r)
    vm = valid_mask(r)
    out["region_invalid_words"] = int((~vm).sum())
    out["region_zero_words"] = int((r == 0).sum())
    per = []
    for c in range(CH):
        tags, cnts = np.unique(tag[:, c], return_counts=True)
        per.append(
            {
                "channel": c,
                "tag_hist": {str(int(t)): int(k) for t, k in zip(tags, cnts)},
                "valid_words": int(vm[:, c].sum()),
                "own_tag_words": int(own[a : b + 1, c].sum()),
            }
        )
    out["per_channel"] = per
    torn = np.any(ordv != ordv[:, :1], axis=1)
    out["region_torn_frames"] = int(torn.sum())
    # outside region
    outside = np.concatenate([w[:a], w[b + 1 :]])
    if outside.size:
        vals, cnts = np.unique(outside, return_counts=True)
        top = sorted(zip(cnts.tolist(), vals.tolist()), reverse=True)[:5]
        out["outside_region_top_words"] = [[f"{v:08x}", c] for c, v in top]
    # frame continuity on channel 0 ordinal (whole-frame when not torn)
    out["frame_continuity_ch0"] = cluster_summary(continuity(ordv[:, 0])["clusters"])
    cc = continuity(ordv[:, 0])
    out["frame_continuity_ch0"]["total_repeated"] = cc["repeated"]
    out["frame_continuity_ch0"]["total_dropped"] = cc["dropped"]
    out["frame_continuity_ch0"]["backward_steps"] = cc["backward_steps"]
    # per pair continuity and pair offsets
    pairs = []
    for p in range(4):
        c0, c1 = 2 * p, 2 * p + 1
        disagree = int(np.sum(ordv[:, c0] != ordv[:, c1]))
        cc = continuity(ordv[:, c0])
        s = cluster_summary(cc["clusters"])
        s.update(
            {
                "pair": p,
                "within_pair_disagree": disagree,
                "total_repeated": cc["repeated"],
                "total_skipped": cc["dropped"],
                "backward_steps": cc["backward_steps"],
                "first_at_recording_frame": (a + 1 + s["first_at"]) if s["first_at"] is not None else None,
            }
        )
        pairs.append(s)
    out["pairs"] = pairs
    off = np.stack(
        [((ordv[:, 2 * p].astype(np.int64) - ordv[:, 0].astype(np.int64) + 32768) % 65536) - 32768 for p in (1, 2, 3)],
        axis=1,
    )
    keys, cnts = np.unique(off, axis=0, return_counts=True)
    out["pair_offset_hist"] = {",".join(str(int(x)) for x in k): int(c) for k, c in zip(keys, cnts)}
    # run lengths of each offset state
    code = off[:, 0] * 9 + off[:, 1] * 3 + off[:, 2]
    change = np.nonzero(np.diff(code))[0]
    starts = np.concatenate([[0], change + 1])
    ends = np.concatenate([change + 1, [len(code)]])
    runs = {}
    for s0, e0 in zip(starts, ends):
        k = ",".join(str(int(x)) for x in off[s0])
        runs[k] = max(runs.get(k, 0), int(e0 - s0))
    out["pair_offset_longest_run"] = runs
    return out


def cmd_raw(path):
    data = np.fromfile(path, dtype="<u4")
    w = data.reshape(-1, CH)
    return {"file_bytes": int(data.size * 4), **decode_frames(w)}


def cmd_pattern(path):
    data = np.fromfile(path, dtype="<u4")
    w = data.reshape(-1, CH)
    n = np.arange(w.shape[0], dtype=np.uint32)
    exp = (((np.arange(1, CH + 1, dtype=np.uint32)[None, :] << 16) | (n[:, None] & 0xFFFF)) << 8)
    return {
        "frames": int(w.shape[0]),
        "mismatch_words": int((w != exp).sum()),
        "first_period_bytes_65536_frames": int(min(w.shape[0], 65536) * CH * 4),
    }


def pcap_records(path):
    with open(path, "rb") as f:
        gh = f.read(24)
        magic = struct.unpack("<I", gh[:4])[0]
        if magic in (0xA1B2C3D4, 0xA1B23C4D):
            e = "<"
        elif magic in (0xD4C3B2A1, 0x4D3CB2A1):
            e = ">"
        else:
            raise SystemExit(f"not a classic pcap: {magic:08x}")
        linktype = struct.unpack(e + "I", gh[20:24])[0]
        if linktype != 1:
            raise SystemExit(f"linktype {linktype} not Ethernet")
        while True:
            h = f.read(16)
            if len(h) < 16:
                return
            _, _, incl, _ = struct.unpack(e + "IIII", h)
            yield f.read(incl)


def cmd_pcap(path, sid_hex):
    sid = bytes.fromhex(sid_hex)
    pdus = 0
    other = 0
    gaps = 0
    gap_frames = 0
    prev_seq = None
    hdr = None
    chunks = []
    for pkt in pcap_records(path):
        off = 12
        et = struct.unpack(">H", pkt[off : off + 2])[0]
        while et in (0x8100, 0x88A8):
            off += 4
            et = struct.unpack(">H", pkt[off : off + 2])[0]
        off += 2
        if et != 0x22F0:
            other += 1
            continue
        a = pkt[off:]
        if len(a) < 24 or a[0] != 0x02 or a[4:12] != sid:
            other += 1
            continue
        seq = a[2]
        fmt = a[16]
        cpf = ((a[17] & 0x03) << 8) | a[18]
        depth = a[19]
        sdl = struct.unpack(">H", a[20:22])[0]
        h = (fmt, (a[17] >> 4) & 0xF, cpf, depth, sdl)
        if hdr is None:
            hdr = h
        elif h != hdr:
            raise SystemExit(f"AAF header changed: {hdr} -> {h}")
        if prev_seq is not None:
            d = (seq - prev_seq) % 256
            if d != 1:
                gaps += 1
                gap_frames += (d - 1) % 256
        prev_seq = seq
        pdus += 1
        chunks.append(a[24 : 24 + sdl])
    fmt, nsr, cpf, depth, sdl = hdr
    if fmt != 0x02 or cpf != CH:
        raise SystemExit(f"unexpected AAF format {fmt:#x} cpf {cpf}")
    buf = b"".join(chunks)
    w = np.frombuffer(buf, dtype=">u4").reshape(-1, CH)
    return {
        "stream_id": sid_hex,
        "aaf_pdus": pdus,
        "non_matching_packets": other,
        "aaf_format": f"{fmt:#04x}",
        "nsr": nsr,
        "channels_per_frame": cpf,
        "bit_depth": depth,
        "stream_data_length": sdl,
        "frames_per_pdu": sdl // (CH * 4),
        "sequence_gaps": gaps,
        "sequence_missing_pdus": gap_frames,
        **decode_frames(w),
    }


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    cmd = sys.argv[1]
    if cmd == "raw":
        r = cmd_raw(sys.argv[2])
    elif cmd == "pattern":
        r = cmd_pattern(sys.argv[2])
    elif cmd == "pcap":
        r = cmd_pcap(sys.argv[2], sys.argv[3])
    else:
        raise SystemExit(__doc__)
    json.dump(r, sys.stdout, indent=1, sort_keys=True)
    print()


if __name__ == "__main__":
    main()
