#!/usr/bin/env python3
"""Independent re-derivation of the Step 3 per-cycle table from the pinned raw files.

Usage: verify_step3_cycles.py <a202-packet-dir>

Per cycle N (bench/cycleN), own decoders only (the packet's analysis scripts
are not imported):
  * t0 = power-strip host T_OFF_CMD minus that host's offset to the build box
    (mean of clock-before and clock-after offset_s_median_best5), i.e. the
    outlet-off command on the build-box clock, the page's time origin;
  * console samples: `### <utc>` send times on the build-box clock, parsed
    from each milan_status block (GM, SYNC, ASCAPABLE, TU);
  * tap: tap ns unwrapped against pcap host time; a least-squares line through
    the per-5 s minima of (host - tap) maps tap time to the capture server's
    clock; minus that server's offset gives build-box time.
Prints each column of the page table recomputed, and the recovery
(all-good minus the earlier of the switch's first post-return Announce/Sync).
"""
import json
import os
import re
import struct
import sys
from datetime import datetime, timezone

WRAP = 1 << 32
SWITCH = "3cc0c6fffefe0210"
DUT = "020000fffe000001"


def offsets(cdir):
    off = {}
    for fn in ("clock-before.jsonl", "clock-after.jsonl"):
        for line in open(os.path.join(cdir, fn)):
            d = json.loads(line)
            off.setdefault(d["host"], []).append(d["offset_s_median_best5"])
    return {h: sum(v) / len(v) for h, v in off.items()}


def console(path):
    samples, cur = [], None
    for line in open(path, errors="replace"):
        m = re.match(r"### (\S+)Z cmd='([^']*)'", line)
        if m:
            t = datetime.fromisoformat(m.group(1)).replace(tzinfo=timezone.utc).timestamp()
            cur = {"t": t, "cmd": m.group(2)}
            if m.group(2) == "milan_status":
                samples.append(cur)
            continue
        if cur is not None and cur["cmd"] == "milan_status":
            for k, v in re.findall(r"(GPTP_GM|SYNC|ASCAPABLE|TU|CLKV_STAT)=(\S+)", line):
                cur[k] = v
    return [s for s in samples if "GPTP_GM" in s and "SYNC" in s]


def tap(path):
    raw = open(path, "rb").read()
    nano = struct.unpack("<I", raw[:4])[0] == 0xA1B23C4D
    off, first, recs = 24, None, []
    while off + 16 <= len(raw):
        s, f, incl, _ = struct.unpack("<IIII", raw[off:off + 16])
        off += 16
        pkt = raw[off:off + incl]
        off += incl
        hns = s * 10**9 + (f if nano else f * 1000)
        if len(pkt) >= 42 and struct.unpack("<I", pkt[:4])[0] == 6 and struct.unpack("<I", pkt[8:12])[0] in (2, 3):
            lo = struct.unpack("<I", pkt[16:20])[0]
            if first is None:
                first = (hns, lo)
            k = round(((hns - first[0]) - (lo - first[1])) / WRAP)
            recs.append((lo - first[1] + k * WRAP, hns, struct.unpack("<I", pkt[8:12])[0], pkt[28:]))
    # line through per-5 s minima of host - tap
    bins = {}
    for t, h, _, _ in recs:
        b = t // 5_000_000_000
        d = h - t
        if b not in bins or d < bins[b][1]:
            bins[b] = (t, d)
    xs = [v[0] for v in bins.values()]
    ys = [v[1] for v in bins.values()]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sl = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    ic = my - sl * mx
    resid = max(abs(y - (ic + sl * x)) for x, y in zip(xs, ys))
    out = []
    for t, _, port, fr in recs:
        et, o = struct.unpack(">H", fr[12:14])[0], 14
        while et == 0x8100:
            et, o = struct.unpack(">H", fr[o + 2:o + 4])[0], o + 4
        out.append(((t + ic + sl * t) / 1e9, port, et, fr[o:]))
    return out, resid / 1e6


def first_after(samples, t, pred):
    for s in samples:
        if s["t"] > t and pred(s):
            return s["t"]
    return None


def main():
    pk = sys.argv[1]
    print("cycle | off_for | sync0 | gm_self | ascap0 | sw_first_frame | sw_first_ann | sw_first_sync | ascap1 | gm_switch | all_good | recovery | fit_resid_ms | samples | max_gap_s")
    for c in range(1, 7):
        cdir = os.path.join(pk, f"bench/cycle{c}")
        offs = offsets(cdir)
        ps = open(os.path.join(cdir, "powerstrip.txt")).read()
        t_off_ps = float(re.search(r"T_OFF_CMD (\S+)", ps).group(1))
        t_on_ps = float(re.search(r"T_ON_CMD (\S+)", ps).group(1))
        ps_host = [h for h in offs if h.endswith("pi")][0]
        srv = [h for h in offs if h.endswith("ubuntu-server")][0]
        t0 = t_off_ps - offs[ps_host]
        smp = console(os.path.join(cdir, "console.txt"))
        gaps = max(b["t"] - a["t"] for a, b in zip(smp, smp[1:]))
        rel = lambda x: None if x is None else round(x - t0, 2)
        sync0 = first_after(smp, t0, lambda s: s["SYNC"] == "0")
        gm_self = first_after(smp, t0, lambda s: s["GPTP_GM"] == DUT)
        ascap0 = first_after(smp, t0, lambda s: s["ASCAPABLE"] == "0")
        recs, resid = tap(os.path.join(cdir, f"tap-c{c}.pcap"))
        recs = [(t - offs[srv], p, et, pl) for t, p, et, pl in recs]
        sw = [r for r in recs if r[1] == 2]
        last_sw = max(r[0] for r in sw if r[0] < t0 + 10)
        ret = [r for r in sw if r[0] > t0 + 10]
        ff = ret[0][0]
        fa = next(r[0] for r in ret if r[2] == 0x88F7 and r[3][0] & 0xF == 0xB)
        fs = next(r[0] for r in ret if r[2] == 0x88F7 and r[3][0] & 0xF == 0x0)
        ascap1 = first_after(smp, t0 + 10, lambda s: s["ASCAPABLE"] == "1")
        gm_sw = first_after(smp, t0 + 10, lambda s: s["GPTP_GM"] == SWITCH)
        good = lambda s: s["GPTP_GM"] == SWITCH and s["SYNC"] == "1" and s["ASCAPABLE"] == "1" and s["TU"] == "0"
        ag = None
        for i, s in enumerate(smp):
            if s["t"] > t0 + 10 and all(good(x) for x in smp[i:]) and not good(smp[i - 1]):
                ag = s["t"]
                break
        rec = ag - min(fa, fs)
        print(f"{c} | {t_on_ps - t_off_ps:.2f} | {rel(sync0)} | {rel(gm_self)} | {rel(ascap0)} | {rel(ff)} | {rel(fa)} | {rel(fs)} | {rel(ascap1)} | {rel(gm_sw)} | {rel(ag)} | {rec:.2f} | {resid:.2f} | {len(smp)} | {gaps:.3f}")
        print(f"   switch last frame {rel(last_sw)}; first frame->first Announce {fa - ff:.2f} s; on cmd->all-good {ag - (t_on_ps - offs[ps_host]):.2f} s; first frame->all-good {ag - ff:.2f} s")


if __name__ == "__main__":
    main()
