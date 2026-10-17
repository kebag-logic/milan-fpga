#!/usr/bin/env python3
"""Lane B21: offline grading of the direction runs (read-only on its inputs).

PR round 2 version. The mcasp grade now accepts an alignment and every continuing run only on equal
slot words; the 64-bit frame keys only propose candidate wire positions. The first alignment's offset
is kept when it is found, so a record whose first event is a foreign frame completes its grade.
The other subcommands are unchanged from the as-run round 3 version.

usage:
  b21_grade.py wire <dut_pcap> <peer_pcap> <stream_id> <dut_port> <peer_port> <nch> <out_prefix> [pattern]
      Every AAF packet of one stream on both taps (b21_aaf.py's decode): sequence numbers, avtp_timestamp
      steps, tv, stream_data_length, inter-arrival on the tap clock; packet-by-packet equality across the
      two taps (matched by position after the first common packet: sequence number, timestamp and
      payload must all be equal); with "pattern", the first-light rule per TDM frame (slot c carries
      ((c + 1) << 16 | n) << 8, the same n in every slot; steps of n between consecutive valid frames).
      Writes <out_prefix>-wire.json and, per tap, <out_prefix>-<tap>.pkts/.samples (b21_aaf.py extract).
  b21_grade.py ext <ext_raw_dir> <out_prefix>
      The external capture's AES pair (cap-lr.raw, S24_3LE) under lane B5's rule (channel 0 word
      (1 << 16) | n, channel 1 (2 << 16) | n): repeats, skips, zero and invalid frames, each discontinuity
      placed on the read-time record (cap-ts.bin) against stalls (read interval over 15 ms) within two reads.
  b21_grade.py mcasp <board_raw_dir> <name> <wire_samples> <nch> <out_prefix>
      Direction B: the McASP capture (<name>.pcm, TDM slots 0..nch-1, S32_LE) aligned frame by frame to the
      frames the DUT received on the wire (<wire_samples>, uint32 per channel): every McASP frame either
      continues the current alignment bit-exactly or starts a new one (found by a 32-frame exact match
      within +-4800 wire frames); offset changes are skips (+d) or repeats/insertions (-d); frames
      matching no wire frame are counted as foreign (zero or otherwise). "Exact" compares all nch
      32-bit words of every frame; the per-frame keys and window hashes only index candidates.
      A final pass compares every matched frame's words with the wire frame at its assigned offset.
  b21_grade.py csr <dut_poll.txt> <out_prefix>
      The DUT CSR poll: AAF_FRAMES, AAF_PAIRS, AVTPRX_STAT/ERR, SLIP_LB, SLIP_TDM, RENDER_STAT, the AAF
      clock meter, first/last and every change.
"""
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

import numpy as np

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import b21_aaf  # noqa: E402

PKT = np.dtype([("tap_ns", "<i8"), ("seq", "<u2"), ("ts", "<u4"), ("tv", "u1"), ("mr", "u1"), ("sdl", "<u2")])


def load(prefix, nch):
    pk = np.fromfile(prefix + ".pkts", dtype=PKT)
    sm = np.fromfile(prefix + ".samples", dtype="<u4")
    per = int(pk["sdl"][0]) // 4 // nch if len(pk) else 0
    return pk, sm.reshape(-1, nch), per


def pattern_frames(S, nch):
    tags = (S >> 24) & 0xFF
    n = (S >> 8) & 0xFFFF
    low = S & 0xFF
    tag_ok = np.all(tags == np.arange(1, nch + 1, dtype=np.uint32)[None, :], axis=1) & np.all(low == 0, axis=1)
    same_n = np.all(n == n[:, :1], axis=1)
    valid = tag_ok & same_n
    torn = tag_ok & ~same_n
    return valid, torn, n[:, 0].astype(np.int64)


def steps(valid, n):
    idx = np.flatnonzero(valid)
    if len(idx) < 2:
        return dict(valid=int(len(idx))), idx, np.array([], dtype=np.int64)
    d = (np.diff(n[idx]) % 65536)
    gap = np.diff(idx)
    out = dict(valid=int(len(idx)), first_valid=int(idx[0]), last_valid=int(idx[-1]),
               region_frames=int(idx[-1] - idx[0] + 1), invalid_inside_region=int(idx[-1] - idx[0] + 1 - len(idx)),
               in_order=int(((d == 1) & (gap == 1)).sum()), repeats=int((d == 0).sum()),
               skips=int(((d > 1) & (d < 32768)).sum()), skipped_frames=int((d[(d > 1) & (d < 32768)] - 1).sum()),
               backward=int((d >= 32768).sum()))
    return out, idx, d


def grade_tap(prefix, nch, pattern):
    pk, S, per = load(prefix, nch)
    r = dict(packets=int(len(pk)))
    if not len(pk):
        return r, pk, S
    sq = np.diff(pk["seq"].astype(np.int64)) % 256
    tsd = np.diff(pk["ts"].astype(np.int64)) % (1 << 32)
    ia = np.diff(pk["tap_ns"]) / 1e3
    r.update(frames_per_packet=per, seconds_tap=round(float(pk["tap_ns"][-1] - pk["tap_ns"][0]) / 1e9, 3),
             rate_pps=round((len(pk) - 1) / ((pk["tap_ns"][-1] - pk["tap_ns"][0]) / 1e9), 3),
             seq_step_not_1=int((sq != 1).sum()), seq_steps=sorted(set(sq.tolist()))[:10],
             ts_step_ns=dict(zip(*[x.tolist() for x in np.unique(tsd, return_counts=True)])) if len(np.unique(tsd)) < 12 else
             dict(min=int(tsd.min()), median=int(np.median(tsd)), max=int(tsd.max()), not_125000=int((tsd != 125000).sum())),
             tv_zero=int((pk["tv"] == 0).sum()), sdl=sorted(set(pk["sdl"].tolist())),
             interarrival_us=dict(min=round(float(ia.min()), 2), p50=round(float(np.median(ia)), 2),
                                  p99_99=round(float(np.percentile(ia, 99.99)), 2), max=round(float(ia.max()), 2)))
    gaps = np.flatnonzero(sq != 1)
    r["seq_breaks"] = [dict(packet=int(i), seq=[int(pk["seq"][i]), int(pk["seq"][i + 1])],
                            tap_t_s=round(float(pk["tap_ns"][i] - pk["tap_ns"][0]) / 1e9, 6)) for i in gaps[:20]]
    if pattern:
        valid, torn, n = pattern_frames(S, nch)
        st, idx, d = steps(valid, n)
        idle = np.all(S == S[0:1, :], axis=1)
        st.update(torn=int(torn.sum()), torn_inside_region=int(torn[idx[0]:idx[-1] + 1].sum()) if len(idx) else 0,
                  first_frame_word=hex(int(S[0, 0])))
        ev = np.flatnonzero(d != 1)
        st["events"] = [dict(frame=int(idx[k + 1]), step=int(d[k]), packet=int(idx[k + 1] // per),
                             tap_t_s=round(float(pk["tap_ns"][idx[k + 1] // per] - pk["tap_ns"][0]) / 1e9, 6)) for k in ev[:200]]
        if len(ev) > 1:
            fr = np.array([idx[k + 1] for k in ev])
            st["event_spacing_frames"] = dict(min=int(np.diff(fr).min()), median=float(np.median(np.diff(fr))), max=int(np.diff(fr).max()))
        r["pattern"] = st
    return r, pk, S


def wire(dut_pcap, peer_pcap, sid, dport, pport, nch, outp, pattern=False):
    nch = int(nch)
    res = dict(stream=sid)
    taps = {}
    for tap, pc, port in (("dutlink", dut_pcap, dport), ("peerlink", peer_pcap, pport)):
        pre = f"{outp}-{tap}"
        subprocess.run([sys.executable, "-B", str(TOOLS / "b21_aaf.py"), "extract", pc, sid, str(port), pre], check=True,
                       stdout=subprocess.DEVNULL)
        r, pk, S = grade_tap(pre, nch, pattern)
        res[tap] = r
        taps[tap] = (pk, S)
    (pa, Sa), (pb, Sb) = taps["dutlink"], taps["peerlink"]
    per = res["dutlink"].get("frames_per_packet", 6)
    # align: first packet of the peer link inside the DUT link record by (seq, ts) and payload
    key_a = {}
    for i, (s, t) in enumerate(zip(pa["seq"][:200000].tolist(), pa["ts"][:200000].tolist())):
        key_a.setdefault((s, t), i)
    j0 = next((j for j in range(min(len(pb), 50000)) if (int(pb["seq"][j]), int(pb["ts"][j])) in key_a), None)
    x = dict()
    if j0 is not None:
        i0 = key_a[(int(pb["seq"][j0]), int(pb["ts"][j0]))]
        m = min(len(pa) - i0, len(pb) - j0)
        sa, sb = pa[i0:i0 + m], pb[j0:j0 + m]
        hdr_eq = (sa["seq"] == sb["seq"]) & (sa["ts"] == sb["ts"])
        pay_eq = np.all(Sa[i0 * per:(i0 + m) * per].reshape(m, -1) == Sb[j0 * per:(j0 + m) * per].reshape(m, -1), axis=1)
        dt = (sb["tap_ns"] - sa["tap_ns"]).astype(np.float64)
        dtc = dt - np.median(dt)
        x = dict(common_packets=int(m), dut_first_common=int(i0), peer_first_common=int(j0),
                 header_equal=int(hdr_eq.sum()), payload_equal=int(pay_eq.sum()),
                 first_unequal=int(np.flatnonzero(~(hdr_eq & pay_eq))[0]) if not np.all(hdr_eq & pay_eq) else None,
                 dut_only_before=int(i0), dut_only_after=int(len(pa) - i0 - m), peer_only_before=int(j0), peer_only_after=int(len(pb) - j0 - m),
                 transit_minus_median_us=dict(min=round(float(dtc.min()) / 1e3, 3), p50=0.0, max=round(float(dtc.max()) / 1e3, 3),
                                              note="tap clocks of the two links are not common; drift included"))
    res["cross_link"] = x
    json.dump(res, open(outp + "-wire.json", "w"), indent=1)
    print(json.dumps(res, indent=1))


def ext(rawdir, outp):
    raw = Path(rawdir)
    b = np.fromfile(raw / "cap-lr.raw", dtype=np.uint8)
    n = len(b) // 6
    w = b[:n * 6].reshape(n, 2, 3).astype(np.int64)
    w = w[:, :, 0] | (w[:, :, 1] << 8) | (w[:, :, 2] << 16)
    ts = np.fromfile(raw / "cap-ts.bin", dtype=np.dtype([("f", "<i8"), ("rt", "<f8"), ("mono", "<i8")]))
    F, MONO = ts["f"], ts["mono"]
    valid = ((w[:, 0] >> 16) == 1) & ((w[:, 1] >> 16) == 2) & ((w[:, 0] & 0xFFFF) == (w[:, 1] & 0xFFFF))
    nn = w[:, 0] & 0xFFFF
    zero = (w[:, 0] == 0) & (w[:, 1] == 0)
    torn = ((w[:, 0] >> 16) == 1) & ((w[:, 1] >> 16) == 2) & ~valid
    st, idx, d = steps(valid, nn)
    lo, hi = (idx[0], idx[-1]) if len(idx) else (0, 0)
    gi = np.diff(MONO) / 1e6
    stall_reads = np.flatnonzero(gi > 15.0) + 1
    cls = dict(repeat=0, skip1=0, skip2_59=0, skip60=0)
    placed = dict(stall_aligned=0, not_stall_aligned=0)
    evs = []
    for k in np.flatnonzero(d != 1):
        f = int(idx[k + 1])
        rd = int(np.searchsorted(F, f + 1))       # the read that delivered frame f
        near = bool(len(stall_reads) and np.min(np.abs(stall_reads - rd)) <= 2)
        dk = int(d[k])
        c = "repeat" if dk == 0 else "skip1" if dk == 2 else "skip2_59" if dk <= 60 else "skip60" if dk < 32768 else "backward"
        cls[c] = cls.get(c, 0) + 1
        if dk != 0:
            placed["stall_aligned" if near else "not_stall_aligned"] += 1
        if len(evs) < 400:
            evs.append(dict(frame=f, step=dk, read=rd, stall_within_2_reads=near))
    st.update(frames=int(n), zero_inside_region=int(zero[lo:hi + 1].sum()), torn=int(torn.sum()),
              invalid_nonzero_inside=int((~valid & ~zero)[lo:hi + 1].sum()), classes=cls, skip_placement=placed,
              stalls=int(len(stall_reads)), reads=int(len(ts)), events=evs)
    json.dump(st, open(outp + "-ext.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in st.items() if k != "events"}, indent=1))


def mcasp(rawdir, name, wire_samples, nch, outp):
    nch = int(nch)
    M = np.fromfile(Path(rawdir) / f"{name}.pcm", dtype="<u4").reshape(-1, nch)
    Wd = np.fromfile(wire_samples, dtype="<u4").reshape(-1, nch)
    return mcasp_grade(M, Wd, outp)


def mcasp_grade(M, Wd, outp=None):
    # one 64-bit key per frame: an index for candidate positions only, never a proof of equality
    def keys(A):
        k = np.zeros(len(A), dtype=np.uint64)
        for c in range(A.shape[1]):
            k = k * np.uint64(1000003) ^ A[:, c].astype(np.uint64)
        return k
    km, kw = keys(M), keys(Wd)
    L = 32
    # rolling window hash of L frames (polynomial over the frame keys)
    def wins(k):
        h = np.zeros(len(k) - L + 1, dtype=np.uint64)
        for i in range(L):
            h = h * np.uint64(0x100000001B3) ^ k[i:len(k) - L + 1 + i]
        return h
    hw = wins(kw)
    order = np.argsort(hw, kind="stable")
    hws = hw[order]

    def find(j, around=None, span=4800):
        if j + L > len(km):
            return None
        h = wins(km[j:j + L])[0]
        a, b = np.searchsorted(hws, h, "left"), np.searchsorted(hws, h, "right")
        cand = order[a:b]
        if around is not None:
            cand = cand[np.abs(cand - around) <= span]
        for i in sorted(cand, key=lambda c: abs(c - (around if around is not None else c))):
            if np.array_equal(Wd[i:i + L], M[j:j + L]):
                return int(i)
        return None

    j = 0
    off = None
    while j < len(km) and off is None:
        i = find(j)
        if i is not None:
            off = i - j
        else:
            j += 1
    first = j
    off0 = off
    ev = []
    foreign = foreign_zero = 0
    matched = 0
    nz = np.all(M == 0, axis=1)
    assigned = np.full(len(M), -1, dtype=np.int64)
    while off is not None and j < len(km):
        i = j + off
        if 0 <= i < len(kw) and np.array_equal(M[j], Wd[i]):
            # the longest run that continues the alignment with equal words, in blocks
            n = min(65536, len(km) - j, len(kw) - i)
            eq = np.all(M[j:j + n] == Wd[i:i + n], axis=1)
            run = n if eq.all() else int(np.argmin(eq))
            assigned[j:j + run] = np.arange(i, i + run)
            matched += run
            j += run
            continue
        i2 = find(j, around=j + off)
        if i2 is not None:
            ev.append(dict(mcasp_frame=int(j), wire_frame=int(i2), offset_change=int(i2 - j - off)))
            off = i2 - j
            continue
        # this frame matches no nearby wire window: foreign; move on one frame
        foreign += 1
        foreign_zero += int(nz[j])
        if len(ev) < 2000:
            ev.append(dict(mcasp_frame=int(j), foreign=True, zero=bool(nz[j])))
        j += 1
    ch = [e for e in ev if "offset_change" in e]
    # independent of the run logic: every matched frame against the wire frame it was assigned
    a = np.flatnonzero(assigned >= 0)
    unequal = int(np.count_nonzero(~np.all(M[a] == Wd[assigned[a]], axis=1))) if len(a) else 0
    res = dict(mcasp_frames=int(len(M)), wire_frames=int(len(Wd)),
               first_aligned_mcasp_frame=int(first) if off0 is not None else None,
               first_wire_frame=int(first + off0) if off0 is not None else None,
               matched=int(matched), matched_word_check=dict(frames=int(len(a)), unequal=unequal),
               unaligned_leading_frames=int(first) if off0 is not None else int(len(M)),
               foreign_frames=int(foreign), foreign_zero=int(foreign_zero),
               offset_changes=len(ch), skips=sum(1 for e in ch if e["offset_change"] > 0),
               skipped_wire_frames=sum(e["offset_change"] for e in ch if e["offset_change"] > 0),
               repeats_or_inserts=sum(1 for e in ch if e["offset_change"] < 0),
               inserted_frames=-sum(e["offset_change"] for e in ch if e["offset_change"] < 0),
               final_offset=int(off) if off is not None else None)
    # clean: every captured frame equal, word for word, to the received frame at one constant offset
    res["clean"] = bool(matched == len(M) and unequal == 0 and not ch and foreign == 0)
    res["events"] = ev[:400]
    if outp is not None:
        json.dump(res, open(outp + "-mcasp.json", "w"), indent=1)
        print(json.dumps({k: v for k, v in res.items() if k != "events"}, indent=1))
        print("events (first 40):", json.dumps(ev[:40]))
    return res


def csr(path, outp):
    txt = open(path, errors="replace").read()
    blocks = re.split(r"^### ", txt, flags=re.M)[1:]
    rows = []
    for b in blocks:
        m = re.match(r"(\S+) cmd='mem_read (0x[0-9a-f]+) (\d+)'", b)
        if not m:
            continue
        base = int(m.group(2), 16)
        data = bytearray()
        for ln in b.splitlines():
            mm = re.match(r"^0x([0-9a-f]{8})\s+((?:[0-9a-f]{2} )+)", ln)
            if mm:
                data += bytes.fromhex(mm.group(2).replace(" ", ""))
        for k in range(len(data) // 4):
            rows.append((m.group(1), base + 4 * k, struct.unpack("<I", data[4 * k:4 * k + 4])[0]))
    names = {0x90000660: "AAF_FRAMES", 0x90000664: "AAF_PAIRS", 0x900006b8: "AVTPRX_STAT", 0x900006bc: "0x6BC",
             0x900006c0: "AVTPRX_ERR", 0x900008d4: "SLIP_LB", 0x900008d8: "SLIP_TDM", 0x900008dc: "RENDER_STAT",
             0x900008e0: "CLKM_0x8E0", 0x900008e4: "CLKM_0x8E4"}
    by = {}
    for t, a, v in rows:
        by.setdefault(a, []).append((t, v))
    out = {}
    for a, vs in sorted(by.items()):
        nm = names.get(a, hex(a))
        ch = [(vs[i][0], hex(vs[i - 1][1]), hex(vs[i][1])) for i in range(1, len(vs)) if vs[i][1] != vs[i - 1][1]]
        out[nm] = dict(samples=len(vs), first=[vs[0][0], hex(vs[0][1])], last=[vs[-1][0], hex(vs[-1][1])],
                       changes=len(ch), change_list=ch[:12] if nm not in ("AAF_FRAMES", "AAF_PAIRS") else [],
                       delta=(vs[-1][1] - vs[0][1]) % (1 << 32))
    json.dump(out, open(outp + "-csr.json", "w"), indent=1)
    print(json.dumps(out, indent=1))


SI_NAMES = ["MEDIA_LOCKED", "MEDIA_UNLOCKED", "STREAM_INTERRUPTED", "SEQ_NUM_MISMATCH", "MEDIA_RESET",
            "TIMESTAMP_UNCERTAIN", "TIMESTAMP_VALID", "TIMESTAMP_NOT_VALID", "UNSUPPORTED_FORMAT",
            "LATE_TIMESTAMP", "EARLY_TIMESTAMP", "FRAMES_RX"]
SO_NAMES = ["STREAM_START", "STREAM_STOP", "MEDIA_RESET", "TIMESTAMP_UNCERTAIN", "FRAMES_TX"]


def counters(outp, *files):
    """GET_COUNTERS payloads (descriptor type, index, counters_valid, 32 words): every valid word per
    read and its change from the first read. counters_valid bit k marks word k. STREAM_INPUT words 0-11
    are named in the twelve-counter order both entities report (counters_valid 0xfff: the ten
    IEEE 1722.1-2021 Table 7-157 counters with TIMESTAMP_VALID and TIMESTAMP_NOT_VALID at words 6 and 7),
    STREAM_OUTPUT words 0-4 by Milan v1.2 Table 5.7."""
    reads = []
    for f in files:
        rows = {}
        for ln in open(f):
            if not ln.startswith("{"):
                continue
            r = json.loads(ln)
            if r.get("cmd") != "GET_COUNTERS" or r.get("status") != "SUCCESS":
                continue
            b = bytes.fromhex(r["payload"])
            dt, di, valid = struct.unpack(">HHI", b[:8])
            words = struct.unpack(">32I", b[8:8 + 128])
            rows[(r["role"], dt, di)] = (valid, words, r.get("t_rx"))
        reads.append((Path(f).name, rows))
    out = {}
    for key in reads[0][1]:
        role, dt, di = key
        nm = SI_NAMES if dt == 5 else SO_NAMES if dt == 6 else []
        first = reads[0][1][key]
        ent = {}
        for k in range(32):
            if not (first[0] >> (31 - k)) & 1 and not (first[0] >> k) & 1:
                continue
            label = nm[k] if k < len(nm) else f"word{k}"
            series = [rd[1][key][1][k] if key in rd[1] else None for rd in reads]
            ent[label] = dict(values=series, change=(series[-1] - series[0]) if None not in series else None)
        out[f"{role} {'STREAM_INPUT' if dt == 5 else 'STREAM_OUTPUT' if dt == 6 else hex(dt)} {di}"] = dict(valid=hex(first[0]), words=ent)
    res = dict(reads=[r[0] for r in reads], counters=out)
    json.dump(res, open(outp + "-counters.json", "w"), indent=1)
    for k, v in out.items():
        moved = {a: b["values"] for a, b in v["words"].items() if b["change"]}
        print(k, v["valid"], "moved:", moved)


if __name__ == "__main__":
    cmd, a = sys.argv[1], sys.argv[2:]
    if cmd == "counters":
        counters(*a)
        sys.exit(0)
    if cmd == "wire":
        wire(*a[:7], pattern=(len(a) > 7 and a[7] == "pattern"))
    elif cmd == "ext":
        ext(*a)
    elif cmd == "mcasp":
        mcasp(*a)
    elif cmd == "csr":
        csr(*a)
    else:
        raise SystemExit(__doc__)
