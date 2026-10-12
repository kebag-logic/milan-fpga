#!/usr/bin/env python3
"""Lane B15 (new): is the known tone present at each observation point? (offline, read-only)

The four points of the B15 assignment, each reduced to per-channel tone figures:

  tap     an AAF stream decoded from a tap capture (pcap, link type Ethernet, each record carrying
          the tap's 28-byte record header before the Ethernet frame: the direction port at header
          bytes 8-11, little-endian). The stream is selected by its stream_id and, optionally, the
          tap port. Each AVTPDU (IEEE 1722-2016 clause 7, AAF, subtype 0x02) is checked: format
          INT_32BIT (0x02), channels_per_frame, bit_depth, stream_data_length; its samples are the
          big-endian 32-bit words, channel-interleaved per frame (7.3.4). The 24-bit audio sample is
          bits 31:8, as the tone tools use; bits 7:0 are counted separately. Sequence-number gaps,
          tv, mr and the timestamp step are counted.
  mcasp   McASP0's capture of the DUT's TDM output (8 channels, S32_LE, the sample in bits 31:8).
  extcap  the external capture (packed 3-byte little-endian, <nch> channels).

Per channel: RMS level in dBFS (24-bit full scale), minimum and maximum, the share of the
channel's power within +-5 Hz of 997 Hz and of 9,973 Hz (lane B8's b8_proof.py rule: a channel
carries a tone when that share exceeds 0.9 at a level above -40 dBFS), and, for a channel that
carries a tone, lane B6's b6_thdn.block_metrics on every whole one-second block (fitted level,
frequency and its offset in ppm of the capture's own clock, THD+N and SNR), summarised as the
median and the worst block. The tone tools' sample values are not assumed: the tone at these points
is the reference peer's own conversion of an analog signal.

usage: tone_points_b15.py tap <pcap> <stream_id_hex> <out.json> [port] [samples.npy]
       tone_points_b15.py mcasp <raw> <out.json>
       tone_points_b15.py extcap <raw> <nch> <out.json> [ch ...]     (default: every channel)
       tone_points_b15.py control <out.json>                         synthetic controls of the tap decode
"""
import hashlib
import json
import os
import struct
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import b6_thdn as A  # noqa: E402

FS = 48000
TONES = (997, 9973)
TAPHDR = 28


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def pcap_records(d):
    magic = struct.unpack("<I", d[:4])[0]
    if magic not in (0xA1B2C3D4, 0xA1B23C4D):
        raise SystemExit(f"not a little-endian pcap: {magic:#x}")
    lt = struct.unpack("<I", d[20:24])[0]
    if lt != 1:
        raise SystemExit(f"link type {lt}, not Ethernet")
    off = 24
    while off + 16 <= len(d):
        ts, tu, incl, orig = struct.unpack("<IIII", d[off:off + 16])
        yield ts + tu * (1e-9 if magic == 0xA1B23C4D else 1e-6), d[off + 16:off + 16 + incl], orig
        off += 16 + incl


def aaf_decode(pcap, stream_id, port=None):
    """(samples (N, cpf) int64 of the 32-bit words, info dict)."""
    d = open(pcap, "rb").read()
    sid = bytes.fromhex(stream_id)
    words, info = [], dict(pdus=0, other_avtp=0, ports={}, seq_gaps=0, seq_gap_list=[], tv0=0, mr_toggles=0,
                            formats={}, bad_length=0, ts_steps={}, first_t=None, last_t=None)
    last_seq = last_mr = last_ts = None
    for t, p, orig in pcap_records(d):
        if len(p) < TAPHDR + 18:
            continue
        prt = struct.unpack("<I", p[8:12])[0]
        f = p[TAPHDR:]
        et, b = f[12:14], 14
        if et == b"\x81\x00":
            et, b = f[16:18], 18
        if et != b"\x22\xf0":
            continue
        a = f[b:]
        if len(a) < 24 or a[0] != 0x02 or a[4:12] != sid:
            info["other_avtp"] += 1
            continue
        if port is not None and prt != port:
            continue
        info["ports"][prt] = info["ports"].get(prt, 0) + 1
        sv_mr_tv = a[1]
        mr, tv = (sv_mr_tv >> 3) & 1, sv_mr_tv & 1
        seq = a[2]
        ts = struct.unpack(">I", a[12:16])[0]
        fmt = a[16]
        nsr = a[17] >> 4
        cpf = ((a[17] & 0x03) << 8) | a[18]
        depth = a[19]
        sdl = struct.unpack(">H", a[20:22])[0]
        key = f"fmt={fmt:#04x} nsr={nsr} cpf={cpf} depth={depth} sdl={sdl}"
        info["formats"][key] = info["formats"].get(key, 0) + 1
        if fmt != 0x02 or depth != 32 or cpf == 0 or sdl % (4 * cpf) or len(a) < 24 + sdl:
            info["bad_length"] += 1
            continue
        if last_seq is not None and seq != (last_seq + 1) & 0xFF:
            info["seq_gaps"] += 1
            if len(info["seq_gap_list"]) < 50:
                info["seq_gap_list"].append([info["pdus"], last_seq, seq])
        if last_mr is not None and mr != last_mr:
            info["mr_toggles"] += 1
        if not tv:
            info["tv0"] += 1
        if last_ts is not None:
            st = (ts - last_ts) & 0xFFFFFFFF
            info["ts_steps"][st] = info["ts_steps"].get(st, 0) + 1
        last_seq, last_mr, last_ts = seq, mr, ts
        w = np.frombuffer(a[24:24 + sdl], dtype=">i4").astype(np.int64).reshape(-1, cpf)
        words.append(w)
        info["pdus"] += 1
        info["first_t"] = t if info["first_t"] is None else info["first_t"]
        info["last_t"] = t
    top = sorted(info["ts_steps"].items(), key=lambda kv: -kv[1])[:6]
    info["ts_steps"] = {str(k): v for k, v in top}
    info["ports"] = {str(k): v for k, v in info["ports"].items()}
    x = np.concatenate(words) if words else np.zeros((0, 1), dtype=np.int64)
    return x, info


def channel_rows(x24, low=None):
    """x24: (N, ch) float64 24-bit samples."""
    rows = []
    n = len(x24)
    for c in range(x24.shape[1]):
        v = x24[:, c]
        p = float(np.mean(v * v)) if n else 0.0
        lvl = 10 * np.log10(p / (2 ** 23) ** 2) if p > 0 else None
        row = dict(channel=c, frames=int(n), rms_dbfs=None if lvl is None else round(lvl, 2),
                   min=int(v.min()) if n else None, max=int(v.max()) if n else None,
                   nonzero=int(np.count_nonzero(v)))
        if low is not None:
            lw = low[:, c]
            row["low_byte_nonzero"] = int(np.count_nonzero(lw))
            row["low_byte_values"] = sorted(int(u) for u in np.unique(lw)[:8])
        if p > 0 and n >= FS:
            S = np.abs(np.fft.rfft(v - v.mean())) ** 2
            fr = np.fft.rfftfreq(len(v), 1 / FS)
            tot = S.sum()
            for t in TONES:
                share = float(S[(fr > t - 5) & (fr < t + 5)].sum() / tot) if tot > 0 else 0.0
                row[f"share_{t}"] = round(share, 6)
                if share > 0.9 and lvl > -40:
                    bl = [A.block_metrics(v[i * FS:(i + 1) * FS], t) for i in range(n // FS)]
                    keys = ("level_dbfs", "f_hz", "ppm", "thdn_db", "snr_db")
                    row[f"tone_{t}"] = dict(
                        blocks=len(bl),
                        median={k: round(float(np.median([b[k] for b in bl])), 4 if k != "ppm" else 3) for k in keys},
                        worst_thdn_db=round(float(max(b["thdn_db"] for b in bl)), 3),
                        worst_snr_db=round(float(min(b["snr_db"] for b in bl)), 3),
                        per_block=[{k: round(float(b[k]), 4 if k != "ppm" else 3) for k in keys} for b in bl])
        rows.append(row)
    return rows


def verdict(rows):
    found = {}
    for r in rows:
        for t in TONES:
            if f"tone_{t}" in r:
                found.setdefault(str(t), []).append(r["channel"])
    return found, ("TONE PRESENT" if found.get(str(TONES[0])) and found.get(str(TONES[1])) else
                   "ONE TONE PRESENT" if found else "TONE ABSENT")


def cmd_tap(pcap, sid, out, port=None, npy=None):
    x, info = aaf_decode(pcap, sid, port)
    x24 = (x >> 8).astype(np.float64)
    rows = channel_rows(x24, low=(x & 0xFF))
    found, v = verdict(rows)
    res = dict(point="tap", file=os.path.basename(pcap), bytes=os.path.getsize(pcap), sha256=sha(pcap),
               stream_id=sid, port=port, frames=int(len(x)), seconds=round(len(x) / FS, 3), info=info,
               channels=rows, tone_channels=found, verdict=v)
    if npy:
        np.save(npy, x.astype(np.int32))
    json.dump(res, open(out, "w"), indent=1)
    return res


def cmd_mcasp(raw, out):
    w = np.fromfile(raw, dtype="<i4")
    n = len(w) // 8
    w = w[:n * 8].reshape(n, 8).astype(np.int64)
    rows = channel_rows((w >> 8).astype(np.float64), low=(w & 0xFF))
    found, v = verdict(rows)
    res = dict(point="mcasp", file=os.path.basename(raw), bytes=os.path.getsize(raw), sha256=sha(raw),
               frames=int(n), seconds=round(n / FS, 3), channels=rows, tone_channels=found, verdict=v)
    json.dump(res, open(out, "w"), indent=1)
    return res


def cmd_extcap(raw, nch, out, chans=None):
    b = np.fromfile(raw, dtype=np.uint8)
    n = len(b) // (3 * nch)
    a = b[:n * 3 * nch].reshape(n, nch, 3).astype(np.int64)
    v = a[..., 0] | (a[..., 1] << 8) | (a[..., 2] << 16)
    v = np.where(v >= 1 << 23, v - (1 << 24), v)
    sel = list(range(nch)) if not chans else chans
    rows = channel_rows(v[:, sel].astype(np.float64))
    for r, c in zip(rows, sel):
        r["channel"] = c
    found, vd = verdict(rows)
    res = dict(point="extcap", file=os.path.basename(raw), bytes=os.path.getsize(raw), sha256=sha(raw),
               frames=int(n), seconds=round(n / FS, 3), channels=rows, tone_channels=found, verdict=vd)
    json.dump(res, open(out, "w"), indent=1)
    return res


def synth_pcap(path, sid, cpf, frames, tone_ch, gap_at=None, hdr_port=3, other=True):
    """A synthetic tap capture: AAF INT_32BIT, 6 frames per PDU, the tone pair on tone_ch at -20 dBFS
    (b9_tone's samples, 24-bit in bits 31:8, low byte 0x5A to show the byte lanes), the other channels
    a known +-1 LSB pattern; one PDU dropped at gap_at; foreign AVTP frames interleaved."""
    import b9_tone as T9
    k = np.arange(frames)
    s0 = T9.tone(997, 0.7, n=frames)
    s1 = T9.tone(9973, 2.1, n=frames)
    x = np.zeros((frames, cpf), dtype=np.int64)
    for c in range(cpf):
        x[:, c] = (k + c) % 3 - 1
    x[:, tone_ch[0]], x[:, tone_ch[1]] = s0, s1
    words = ((x << 8) | 0x5A) & 0xFFFFFFFF
    out = bytearray(struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 262144, 1))
    seq, ts, kept = 0, 1000, []
    for pdu in range(frames // 6):
        seq_now, seq = seq, (seq + 1) & 0xFF
        ts_now, ts = ts, (ts + 125000) & 0xFFFFFFFF
        if gap_at is not None and pdu == gap_at:
            continue
        kept.append(pdu)
        pay = b"".join(struct.pack(">I", int(v)) for v in words[pdu * 6:(pdu + 1) * 6].reshape(-1))
        avtp = bytes([0x02, 0x81, seq_now, 0]) + bytes.fromhex(sid) + struct.pack(">I", ts_now) + \
            bytes([0x02, 0x50 | (cpf >> 8), cpf & 0xFF, 32]) + struct.pack(">H", len(pay)) + b"\x10\x00" + pay
        eth = bytes.fromhex("91e0f000fe00") + bytes.fromhex("<peer-id>") + b"\x81\x00\x60\x02\x22\xf0" + avtp
        rec = struct.pack("<IIIIII", 6, 0x110, hdr_port, 0, 0, len(eth)) + struct.pack("<I", len(eth)) + eth
        out += struct.pack("<IIII", pdu // 8000, (pdu % 8000) * 125, len(rec), len(rec)) + rec
        if other and pdu % 7 == 0:
            o = avtp[:4] + bytes.fromhex("0200000000010000") + avtp[12:]
            eth2 = bytes.fromhex("91e0f000dd85") + bytes.fromhex("020000000001") + b"\x81\x00\x60\x02\x22\xf0" + o
            rec2 = struct.pack("<IIIIII", 6, 0x110, 2, 0, 0, len(eth2)) + struct.pack("<I", len(eth2)) + eth2
            out += struct.pack("<IIII", pdu // 8000, (pdu % 8000) * 125, len(rec2), len(rec2)) + rec2
    open(path, "wb").write(out)
    return x, kept


def cmd_control(out):
    import tempfile
    res, ok = [], True
    sid = "<peer-eid>"
    with tempfile.TemporaryDirectory() as td:
        # 1: clean, 4 channels, tone on 0/1: exact sample recovery, both tones found, no gap
        p = os.path.join(td, "c1.pcap")
        x, kept = synth_pcap(p, sid, 4, 3 * FS, (0, 1))
        r = cmd_tap(p, sid, os.path.join(td, "c1.json"), port=3)
        got, info = aaf_decode(p, sid, 3)
        exact = bool(np.array_equal(got >> 8, x)) and bool(np.all((got & 0xFF) == 0x5A))
        t0 = r["channels"][0].get("tone_997", {}).get("median", {})
        t1 = r["channels"][1].get("tone_9973", {}).get("median", {})
        good = (exact and r["verdict"] == "TONE PRESENT" and r["tone_channels"] == {"997": [0], "9973": [1]}
                and info["seq_gaps"] == 0 and abs(t0.get("level_dbfs", 0) + 20) < 0.01 and abs(t1.get("level_dbfs", 0) + 20) < 0.01
                and abs(t0.get("ppm", 9)) < 0.01 and abs(t1.get("ppm", 9)) < 0.01 and info["other_avtp"] > 0)
        res.append(dict(control="clean, tone on 0/1, foreign stream interleaved", exact_samples=exact, verdict=r["verdict"],
                        tone_channels=r["tone_channels"], seq_gaps=info["seq_gaps"], other_avtp=info["other_avtp"],
                        level_997=t0.get("level_dbfs"), level_9973=t1.get("level_dbfs"), ppm=[t0.get("ppm"), t1.get("ppm")],
                        thdn=[t0.get("thdn_db"), t1.get("thdn_db")], result="PASS" if good else "FAIL"))
        ok &= good
        # 2: the tone on channels 2/3 instead: found there, not on 0/1
        p = os.path.join(td, "c2.pcap")
        synth_pcap(p, sid, 4, 2 * FS, (2, 3))
        r = cmd_tap(p, sid, os.path.join(td, "c2.json"), port=3)
        good = r["tone_channels"] == {"997": [2], "9973": [3]}
        res.append(dict(control="tone on 2/3", tone_channels=r["tone_channels"], result="PASS" if good else "FAIL"))
        ok &= good
        # 3: one PDU dropped: one sequence gap at its place
        p = os.path.join(td, "c3.pcap")
        synth_pcap(p, sid, 4, 2 * FS, (0, 1), gap_at=5000)
        got, info = aaf_decode(p, sid, 3)
        good = info["seq_gaps"] == 1 and info["seq_gap_list"][0][0] == 5000 and len(got) == 2 * FS - 6
        res.append(dict(control="one PDU dropped at 5,000", seq_gaps=info["seq_gaps"], at=info["seq_gap_list"],
                        frames=int(len(got)), result="PASS" if good else "FAIL"))
        ok &= good
        # 4: the port filter: the stream on port 2 is not taken for port 3
        p = os.path.join(td, "c4.pcap")
        synth_pcap(p, sid, 4, FS, (0, 1), hdr_port=2)
        got, info = aaf_decode(p, sid, 3)
        good = len(got) == 0
        res.append(dict(control="stream on the other port", frames=int(len(got)), result="PASS" if good else "FAIL"))
        ok &= good
        # 5: silence of +-1 LSB only: TONE ABSENT
        p = os.path.join(td, "c5.pcap")
        x, _ = synth_pcap(p, sid, 4, FS, (0, 1))
        res5 = channel_rows(np.stack([((np.arange(FS) + c) % 3 - 1) for c in range(4)], axis=1).astype(np.float64))
        good = verdict(res5)[1] == "TONE ABSENT"
        res.append(dict(control="+-1 LSB only", verdict=verdict(res5)[1], result="PASS" if good else "FAIL"))
        ok &= good
    out_d = dict(controls=res, all_pass=bool(ok))
    json.dump(out_d, open(out, "w"), indent=1)
    print(json.dumps(out_d))
    return 0 if ok else 1


def short(res):
    keep = ("channel", "rms_dbfs", "min", "max", "share_997", "share_9973", "low_byte_values")
    for r in res["channels"]:
        line = {k: r.get(k) for k in keep if k in r}
        for t in TONES:
            if f"tone_{t}" in r:
                line[f"tone_{t}"] = r[f"tone_{t}"]["median"]
        print(json.dumps(line))
    print(res.get("verdict"), res.get("tone_channels"), res.get("frames"), res.get("sha256"))


if __name__ == "__main__":
    m = sys.argv[1]
    if m == "tap":
        short(cmd_tap(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5] != "-" else None,
                      sys.argv[6] if len(sys.argv) > 6 else None))
    elif m == "mcasp":
        short(cmd_mcasp(sys.argv[2], sys.argv[3]))
    elif m == "extcap":
        short(cmd_extcap(sys.argv[2], int(sys.argv[3]), sys.argv[4], [int(c) for c in sys.argv[5:]] or None))
    elif m == "control":
        sys.exit(cmd_control(sys.argv[2]))
    else:
        raise SystemExit(__doc__)
