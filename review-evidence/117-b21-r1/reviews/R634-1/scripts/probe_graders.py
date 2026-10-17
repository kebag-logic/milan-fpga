#!/usr/bin/env python3
"""Fault probes of the packet's round 3 graders on synthetic inputs.

usage: python3 -I probe_graders.py <tools_copy_dir> <work_dir>

<tools_copy_dir> holds unmodified copies of b21_grade.py and b21_aaf.py from the evidence packet
(their hashes are printed and must equal the page's tool table). Each probe builds a clean input and
one mutant per fault, runs the packet's own grading function and prints what it reports. A probe
"detects" a fault when the mutant's report differs from the clean report in the field that grades it.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import struct
import sys
from pathlib import Path

import numpy as np


def load(tools, name):
    spec = importlib.util.spec_from_file_location(name, tools / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **k)


# ---------- synthetic tap capture (the envelope b21_aaf.records reads) ----------
def pcap(path, pkts):
    """pkts: list of (port, tap_ns, seq, ts, payload_words(uint32 array), sid bytes)."""
    with open(path, "wb") as f:
        f.write(struct.pack("<IHHiIII", 0xA1B23C4D, 2, 4, 0, 0, 262144, 1))
        for port, tns, seq, ts, words, sid in pkts:
            body = np.asarray(words, dtype=">u4").tobytes()
            avtp = bytes([0x02, 0x81, seq & 0xFF, 0]) + sid + struct.pack(">I", ts & 0xFFFFFFFF) + \
                bytes([0x02, 0x05, 0x02, 0x20]) + struct.pack(">H", len(body)) + bytes([0, 0]) + body
            eth = b"\x91\xe0\xf0\x00\x00\x01" + b"\x02\x00\x00\x00\x00\x01" + struct.pack(">H", 0x22F0) + avtp
            env = struct.pack("<III", 6, 28, port) + b"\0" * 4 + struct.pack("<I", tns & 0xFFFFFFFF) + b"\0" * 8
            rec = env + eth
            hns = 1_000_000_000 + tns
            f.write(struct.pack("<IIII", hns // 10**9, hns % 10**9, len(rec), len(rec)) + rec)


def pattern_words(n0, nframes, nch=8):
    n = (np.arange(n0, n0 + nframes) % 65536).astype(np.uint32)
    tags = np.arange(1, nch + 1, dtype=np.uint32)
    return (((tags[None, :] << 16) | n[:, None]) << 8).astype(np.uint32)


def wire_probe(g, work):
    sid = bytes.fromhex("0200000000010000")
    NP = 3000
    frames = pattern_words(100, NP * 6)

    def build(mut):
        F = frames.copy()
        seqs = list(range(NP))
        keep = list(range(NP))
        if mut == "frame-repeat":
            F[600 * 6 + 3] = F[600 * 6 + 2]
        if mut == "frame-skip-in-content":
            F[600 * 6:] = pattern_words(100 + 600 * 6 + 6, (NP - 600) * 6)
        if mut == "torn":
            F[700 * 6 + 1, 5] ^= 1 << 8
        if mut == "low-byte":
            F[700 * 6 + 1, 2] |= 0x01
        dut = [(3, 125000 * i, s, 1000 + 125000 * i, F[i * 6:(i + 1) * 6].ravel(), sid) for i, s in zip(keep, seqs)]
        peer_F = F.copy()
        if mut == "peer-payload-bitflip":
            peer_F[1000 * 6 + 2, 1] ^= 1 << 12
        peer = [(2, 125000 * i + 5000, s, 1000 + 125000 * i, peer_F[i * 6:(i + 1) * 6].ravel(), sid) for i, s in zip(keep, seqs)]
        if mut == "peer-packet-lost":
            del peer[1500]
        if mut == "dut-packet-lost":
            del dut[1500]
        if mut == "peer-ts-changed":
            p = peer[1200]
            peer[1200] = (p[0], p[1], p[2], p[3] + 8, p[4], p[5])
        return dut, peer

    res = {}
    for mut in ("clean", "frame-repeat", "frame-skip-in-content", "torn", "low-byte", "dut-packet-lost",
                "peer-packet-lost", "peer-payload-bitflip", "peer-ts-changed"):
        dut, peer = build(mut)
        pa, pb = work / f"w-{mut}-dut.pcap", work / f"w-{mut}-peer.pcap"
        pcap(pa, dut)
        pcap(pb, peer)
        out = str(work / f"w-{mut}")
        quiet(g.wire, str(pa), str(pb), "0200000000010000", 3, 2, 8, out, pattern=True)
        r = json.load(open(out + "-wire.json"))
        d, x = r["dutlink"], r["cross_link"]
        p = d["pattern"]
        res[mut] = dict(dut_seq_breaks=d["seq_step_not_1"], peer_seq_breaks=r["peerlink"]["seq_step_not_1"],
                        dut_repeats=p["repeats"], dut_skips=p["skips"], dut_torn=p["torn"],
                        dut_invalid_inside=p["invalid_inside_region"], peer_skips=r["peerlink"]["pattern"]["skips"],
                        common=x.get("common_packets"), header_equal=x.get("header_equal"), payload_equal=x.get("payload_equal"))
    return res


def mcasp_probe(g, work, rng):
    N = 200_000
    vals = np.array([0x00000000, 0xFFFFFF00, 0xFFFFFE00], dtype=np.uint32)
    W = vals[rng.choice(3, size=(N, 4), p=[0.81, 0.14, 0.05])]
    eq_prev = float(np.mean(np.all(W[1:] == W[:-1], axis=1)))
    wire = work / "m-wire.samples"
    W.astype("<u4").tofile(wire)
    off = 12345
    base = W[off:off + 150_000].copy()

    def mutant(mut):
        M = base.copy()
        if mut == "skip6":
            M = np.concatenate([M[:50_000], M[50_006:]])
        if mut == "repeat1":
            M = np.concatenate([M[:60_000], M[59_999:60_000], M[60_000:]])
        if mut == "insert3zero":
            M = np.concatenate([M[:70_000], np.zeros((3, 4), np.uint32), M[70_000:]])
        if mut == "bitflip":
            M[80_000, 2] ^= 1 << 31
        if mut == "replace1zero":
            # in place, on the first non-zero frame from 90,000 (a zero frame replacing a zero frame
            # is bit-exact and not a fault)
            k = 90_000 + int(np.flatnonzero(np.any(M[90_000:] != 0, axis=1))[0])
            M[k] = 0
        return M

    res = {"fraction_equal_to_previous": round(eq_prev, 3)}
    for mut in ("clean", "skip6", "repeat1", "insert3zero", "bitflip", "replace1zero"):
        d = work / f"m-{mut}"
        d.mkdir(exist_ok=True)
        mutant(mut).astype("<u4").tofile(d / "x.pcm")
        quiet(g.mcasp, str(d), "x", str(wire), 4, str(d / "out"))
        r = json.load(open(d / "out-mcasp.json"))
        res[mut] = {k: r[k] for k in ("matched", "offset_changes", "skips", "skipped_wire_frames", "repeats_or_inserts",
                                      "inserted_frames", "foreign_frames", "foreign_zero")}
    return res


def ext_probe(g, work):
    N = 100_000
    n = np.arange(500, 500 + N) % 65536

    def build(mut):
        L = (1 << 16) | n
        R = (2 << 16) | n
        L, R = L.copy(), R.copy()
        if mut == "skip1":
            L, R = np.delete(L, 40_000), np.delete(R, 40_000)
        if mut == "repeat1":
            L, R = np.insert(L, 40_000, L[39_999]), np.insert(R, 40_000, R[39_999])
        if mut == "zero1":
            L[40_000] = R[40_000] = 0
        if mut == "torn":
            R[40_000] = (2 << 16) | ((n[40_000] + 3) % 65536)
        w = np.stack([L, R], axis=1).astype(np.uint32)
        b = np.stack([w & 0xFF, (w >> 8) & 0xFF, (w >> 16) & 0xFF], axis=2).astype(np.uint8)
        return b.reshape(-1)

    res = {}
    for mut in ("clean", "skip1", "repeat1", "zero1", "torn"):
        d = work / f"e-{mut}"
        d.mkdir(exist_ok=True)
        b = build(mut)
        b.tofile(d / "cap-lr.raw")
        nf = len(b) // 6
        F = np.arange(480, nf + 1, 480, dtype=np.int64)
        ts = np.zeros(len(F), dtype=np.dtype([("f", "<i8"), ("rt", "<f8"), ("mono", "<i8")]))
        ts["f"], ts["mono"] = F, np.arange(len(F)) * 10_000_000
        ts.tofile(d / "cap-ts.bin")
        quiet(g.ext, str(d), str(d / "out"))
        r = json.load(open(d / "out-ext.json"))
        res[mut] = {k: r[k] for k in ("valid", "repeats", "skips", "skipped_frames", "zero_inside_region", "torn", "invalid_nonzero_inside")}
    return res


def main(tools, work):
    tools, work = Path(tools), Path(work)
    work.mkdir(parents=True, exist_ok=True)
    for t in ("b21_grade.py", "b21_aaf.py"):
        print(f"[tool] {t} sha256 {hashlib.sha256((tools / t).read_bytes()).hexdigest()}")
    load(tools, "b21_aaf")
    g = load(tools, "b21_grade")
    rng = np.random.default_rng(117)
    print("[wire probe]")
    for k, v in wire_probe(g, work).items():
        print(f"  {k:24s} {v}")
    print("[mcasp probe]")
    for k, v in mcasp_probe(g, work, rng).items():
        print(f"  {k:24s} {v}")
    print("[ext probe]")
    for k, v in ext_probe(g, work).items():
        print(f"  {k:24s} {v}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
