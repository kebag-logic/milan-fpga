#!/usr/bin/env python3
"""Round-3 figures of the lane B5 continuity page (docs only, no bench access).

usage:
  b5_round3.py figures  <a472_packet_dir> <record_dir>
  b5_round3.py ordinals <raw_a-long_dir> <a472_packet_dir>

figures needs only published inputs: the round-1 packet's summary/a-long/summary.json,
summary/a-long/continuity-events.csv and restore/peer-descs-2.jsonl, and the round-2
derived read record (a-long-reads.json and a-long-reads.u16; the published packet
carries the record as a-long-reads.u16.gz, restored with gunzip -kf). It uses the
round-2 definitions of b5_attrib.py unchanged: a stall is a read interval over 15 ms,
the floor step compares the minimum of the delivery deficit over 11 reads on each side
with guards of 3 reads before and 2 after, skips of two frames or more closer than 16
reads form one cluster, and a step matches within 4 frames.

  A. which skips of 60 frames or more the stall alignment covers, and the other ones;
  B. how often the floor steps by 1 ms at the off-stall clusters and at clear positions;
  C. that the planted-loss control is linear in the plant;
  D. which descriptor reads the second survey actually sent.

ordinals (needs the raw graded pair, which stays local) prints the pattern ordinals
around each zero frame of the window, and the window's transition count.
"""
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

FS = 48000
PER = 480
STALL_MS = 15.0
W, GB, GA = 10, 3, 2           # b5_attrib.py defaults: floor over W + 1 = 11 reads
JOIN = GB + GA + W + 1         # 16 reads: one floor test's span, and the cluster join
TOL = 4.0
MS1 = FS // 1000
RECORD_SHA = "2183d57f0646cf94405b95aea5547b83f5ff0b9190ac0bd1bdcc87760c919961"
CAP_LR_SHA = "2ac666fb5ff6284cc665887758ad6f2754918e5b7932258a06ea7efeeec99bdf"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 22), b""):
            h.update(blk)
    return h.hexdigest()


def pct(x, q=(0, 5, 25, 50, 75, 95, 100)):
    return "[" + ", ".join(f"{v:+.1f}" for v in np.percentile(np.asarray(x, float), q)) + "]"


def figures(packet, rdir):
    packet, rdir = Path(packet), Path(rdir)
    meta = json.load(open(rdir / "a-long-reads.json"))
    rec = rdir / meta["record"]["file"]
    got = sha256(rec)
    assert got == RECORD_SHA == meta["record"]["sha256"], f"record sha256 {got} is not the page's {RECORD_SHA}"
    gap_us = np.fromfile(rec, dtype="<u2").astype(np.int64)
    R = len(gap_us)
    assert int(gap_us.sum()) == meta["elapsed_us_record"]
    t = np.concatenate(([0], np.cumsum(gap_us))) / 1e6
    D = t * FS - PER * np.arange(R + 1)
    g = np.concatenate(([np.nan], gap_us / 1e3))
    s = json.load(open(packet / "summary/a-long/summary.json"))["continuity"]
    c0, c1 = s["window"]
    assert [c0, c1] == meta["window_frames"] and c1 - c0 == PER * R
    ev = [dict(frame=int(e["frame"]), kind=e["kind"], frames=int(e["frames"]))
          for e in csv.DictReader(open(packet / "summary/a-long/continuity-events.csv"))]
    for e in ev:
        e["r"] = (e["frame"] - c0) // PER + 1
    skips = [e for e in ev if e["kind"] == "skip"]
    multi = sorted((e for e in skips if e["frames"] >= 2), key=lambda e: e["r"])
    out = []
    p = out.append
    p("== inputs")
    p(f"derived read record {rec.name} {rec.stat().st_size} B sha256 {got}; {R} reads; window frames {c0} .. {c1}")
    p(f"events {len(ev)}; skips {len(skips)}; skips of 2 or more {len(multi)}")

    p("== A. skips of 60 frames or more against the stalls (read interval over 15 ms)")
    st = np.flatnonzero(g[1:] > STALL_MS) + 1
    sset = set(int(x) for x in st)
    ex = float(((g[st] - 10.0) * FS / 1000).sum())
    g60 = [e for e in skips if e["frames"] >= 60]
    lag = {id(e): next((o for o in (0, 1, 2) if e["r"] - o in sset), None) for e in g60}
    al = [e for e in g60 if lag[id(e)] is not None]
    na = [e for e in g60 if lag[id(e)] is None]
    p(f"stalls {len(st)}; excess over the 10 ms period {ex:.1f} frames")
    p(f"skips of 60 or more: {len(g60)}, {sum(e['frames'] for e in g60)} frames")
    p(f"  stall-aligned, a stall 0 to 2 reads before: {len(al)}, {sum(e['frames'] for e in al)} frames; "
      f"reads before {dict(sorted(Counter(lag[id(e)] for e in al).items()))}")
    p(f"  not stall-aligned: {len(na)}, {sum(e['frames'] for e in na)} frames")
    for e in na:
        iv = g[max(1, e["r"] - 2):e["r"] + 1]
        near = min(abs(e["r"] - int(x)) for x in st)
        p(f"    {e['frames']} frames at window frame {e['frame'] - c0} ({(e['frame'] - c0) / FS:.2f} s of captured audio), "
          f"read {e['r']} at {t[e['r']]:.2f} s on the host clock; longest read interval of the 3 up to it "
          f"{iv.max():.2f} ms ({iv.max() - 10.0:.2f} ms over the period, {e['frames'] / 48:.2f} ms of audio skipped); "
          f"nearest stall {near} reads away")
    p(f"stall excess {ex:.1f} frames against {sum(e['frames'] for e in al)} in the {len(al)} stall-aligned skips "
      f"and {sum(e['frames'] for e in g60)} in all {len(g60)}")
    content = (c1 - c0) + sum(e["frames"] for e in multi)
    for name, grp in (("skips of 2 or more", multi), ("skips of 60 or more", g60), ("stall-aligned skips", al)):
        f = sum(e["frames"] for e in grp)
        p(f"share of captured plus skipped frames ({content}) in the {len(grp)} {name}: {f} frames, {100 * f / content:.3f}%")

    p("== B. 1 ms floor steps: off-stall clusters against clear positions")

    def step(a, b):
        lo, hi = a - GB - W, b + GA + W
        if lo < 0 or hi > R:
            return None
        return float(D[b + GA:hi + 1].min() - D[lo:a - GB + 1].min())

    cl = []
    for e in multi:
        if cl and e["r"] - cl[-1][-1]["r"] < JOIN:
            cl[-1].append(e)
        else:
            cl.append([e])
    B = [c for c in cl if not any(e["frames"] >= 60 for e in c)]
    assert not any(np.any(g[max(1, c[0]["r"] - 2):c[-1]["r"] + 1] > STALL_MS) for c in B)
    bsteps = [step(c[0]["r"], c[-1]["r"]) for c in B]
    assert None not in bsteps
    k1 = sum(1 for c, v in zip(B, bsteps) if abs(v - MS1) <= TOL and abs(v - sum(e["frames"] for e in c)) > TOL)
    p(f"off-stall clusters (skips of 2 to 59 only, no stall): {len(B)}; floor steps by 1 ms (48 +- {TOL:.0f} frames): {k1}")
    mr = np.array([e["r"] for e in multi])

    def free(a, b, margin):
        i, j = np.searchsorted(mr, a - margin), np.searchsorted(mr, b + margin, side="right")
        return j == i
    pos = [r for r in range(GB + W, R - GA - W) if free(r, r, JOIN + 4)]
    x = np.array([step(r, r) for r in pos])
    big = np.flatnonzero(np.abs(x) > TOL)
    grp = []
    for i in big:
        if grp and pos[i] - grp[-1][-1] <= 2 * JOIN:
            grp[-1].append(pos[i])
        else:
            grp.append([pos[i]])
    gmax = [max((x[pos.index(r)] for r in gg), key=abs) for gg in grp]
    n1 = sum(1 for v in gmax if abs(v - MS1) <= TOL)
    windows = len(pos) / JOIN
    rate = n1 / windows
    p(f"clear read positions: {len(pos)}; groups with |step| > {TOL:.0f}: {len(grp)}, {n1} of them a 1 ms step")
    p(f"one floor test spans {JOIN} reads, so the clear positions hold {len(pos)} / {JOIN} = {windows:.2f} windows")
    p(f"1 ms steps per window at clear positions: {n1} / {windows:.2f} = {rate:.5f}")
    p(f"expected among {len(B)} clusters at that rate: {len(B) * rate:.2f}; observed {k1} "
      f"({100 * k1 / len(B):.1f}% of the clusters against {100 * rate:.2f}% of the windows)")

    p("== C. the planted-loss control is linear in the plant")
    rng = np.random.default_rng(117)
    pick = rng.choice(np.array(pos), size=300, replace=False)
    base = np.array([step(int(r), int(r)) for r in pick])
    for m in (6, 12, 24):
        rec_ = []
        for r in pick:
            Ds = D.copy()
            D[r - 1:] += m
            rec_.append(step(int(r), int(r)))
            D[:] = Ds
        d = np.array(rec_) - m - base
        p(f"planted {m} frames at the same 300 positions as b5_attrib.py: recovered less planted less the unplanted "
          f"step there, largest |difference| {np.abs(d).max():.2e} frames; recovered less planted {pct(np.array(rec_) - m)}")
    p("so a planted loss reads back as the unplanted step plus the plant: the control locates the floor windows, "
      "it does not measure detection power")

    p("== D. what the second descriptor survey sent (restore/peer-descs-2.jsonl)")
    rows = []
    for line in open(packet / "restore/peer-descs-2.jsonl"):
        line = line.strip()
        if line.startswith("{"):
            r = json.loads(line)
            rows.append(r.get("line", r))
    ex_ = [r for r in rows if "cmd" in r]
    tally = Counter()
    for r in ex_:
        m = re.match(r"(?:desc|map)-peer-(?:\d+-)?(0x[0-9a-f]{4})-", r.get("what", ""))
        tally[(r["cmd"], m.group(1) if m else "", r.get("status"))] += 1
    p(f"exchanges {len(ex_)}")
    for (kind, typ, stt), n in sorted(tally.items()):
        p(f"  {kind:16s} {typ} {stt}: {n}")
    sent = Counter(typ for (kind, typ, _), n in tally.items() for _ in range(n) if kind == "READ_DESCRIPTOR")
    for typ, role in (("0x0010", "the walk's cluster reads (0x0010 is EXTERNAL_PORT_INPUT)"),
                      ("0x0011", "the walk's external input port reads"), ("0x0012", "the walk's external output port reads"),
                      ("0x0014", "the walk's map reads (0x0014 is AUDIO_CLUSTER)"), ("0x0017", "AUDIO_MAP")):
        p(f"READ_DESCRIPTOR of type {typ}, {role}: {sent.get(typ, 0)}")
    idx = sorted(int(r["what"].rsplit("-", 1)[1]) for r in ex_ if re.match(r"desc-peer-(?:\d+-)?0x0010-", r.get("what", "")))
    p(f"  type 0x0010 indices {idx[0]} .. {idx[-1]}, {len(idx)} reads")
    for t_, name in ((0x000E, "STREAM_PORT_INPUT"), (0x000F, "STREAM_PORT_OUTPUT")):
        d = [r for r in ex_ if r.get("what") == f"desc-peer-1-{t_:#06x}-0" and r["status"] == "SUCCESS"][0]
        pb = bytes.fromhex(d["payload"])[4:]
        ncl, bcl, nmp, bmp = (int(v) for v in np.frombuffer(pb[12:20], dtype=">u2"))
        p(f"{name} 0: clusters {ncl} from index {bcl}; static maps (number_of_maps) {nmp}")
    au = [r for r in ex_ if r.get("what") == "desc-peer-1-0x0002-0" and r["status"] == "SUCCESS"][-1]
    ab = bytes.fromhex(au["payload"])[4:]
    nein, _, neout, _ = (int(v) for v in np.frombuffer(ab[80:88], dtype=">u2"))
    p(f"AUDIO_UNIT 0: external input ports {nein}, external output ports {neout}")
    p("so no AUDIO_CLUSTER and no AUDIO_MAP descriptor was read; the dynamic maps came from GET_AUDIO_MAP")
    print("\n".join(out))


def ordinals(raw, packet):
    raw, packet = Path(raw), Path(packet)
    src = raw / "cap-lr.raw"
    assert sha256(src) == CAP_LR_SHA, "cap-lr.raw is not the a-long graded pair"
    b = np.memmap(src, dtype=np.uint8, mode="r")
    s = json.load(open(packet / "summary/a-long/summary.json"))["continuity"]
    c0, c1 = s["window"]

    def word(k):
        x = b[6 * k:6 * k + 6].astype(np.int64)
        return int(x[0] | (x[1] << 8) | (x[2] << 16)), int(x[3] | (x[4] << 8) | (x[5] << 16))

    def ordn(k):
        L, R = word(k)
        if L == 0 and R == 0:
            return None
        assert L >> 16 == 1 and R >> 16 == 2 and (L & 0xFFFF) == (R & 0xFFFF), f"frame {k} is not valid"
        return L & 0xFFFF
    out = []
    p = out.append
    p(f"== ordinals around the window's zero frames (a-long/cap-lr.raw, {src.stat().st_size} B, sha256 {CAP_LR_SHA})")
    p("frame offset -8 .. +8 from the zero frame; Z is the zero frame")
    for z in s["silent_stretches"]:
        k, n = z["start"], z["frames"]
        assert n == 1
        seq = [ordn(j) for j in range(k - 8, k + 9)]
        d = [(seq[i + 1] - seq[i]) % 65536 for i in range(len(seq) - 1) if seq[i] is not None and seq[i + 1] is not None]
        before, after = ordn(k - 1), ordn(k + 1)
        sk = [j - k for j in range(k - 8, k + 9) if j - 1 >= k - 8 and ordn(j) is not None and ordn(j - 1) is not None
              and (ordn(j) - ordn(j - 1)) % 65536 == 2]
        p(f"window frame {k - c0}: " + " ".join("Z" if v is None else str(v) for v in seq))
        p(f"  across the zero frame {before} -> {after}: {'consecutive, the zero frame replaces no pattern frame' if (after - before) % 65536 == 1 else 'NOT consecutive'}; "
          f"one-frame skips at offsets {sk}; other steps {sorted(set(d) - {1, 2})}")
    trans = (c1 - c0) - 1
    ungraded = 2 * len(s["silent_stretches"])
    p(f"window transitions {trans} = in order {s['in_order_steps']} + repeats {s['repeats']} + skips {s['skip_events']} "
      f"+ backward {s['backward']} + next to a zero frame {ungraded}: "
      f"{s['in_order_steps'] + s['repeats'] + s['skip_events'] + s['backward'] + ungraded == trans}")
    print("\n".join(out))


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "figures":
        figures(*sys.argv[2:4])
    elif len(sys.argv) == 4 and sys.argv[1] == "ordinals":
        ordinals(*sys.argv[2:4])
    else:
        raise SystemExit(__doc__)
