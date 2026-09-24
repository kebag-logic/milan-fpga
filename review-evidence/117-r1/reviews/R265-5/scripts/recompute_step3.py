#!/usr/bin/env python3
"""Independently recompute the issue 117 step 3 per-cycle table from raw files.

Usage: recompute_step3.py <bench-a202/bench directory>

Reads only raw artifacts of each cycle: powerstrip.txt (outlet command
times on the power-strip host clock), clock-before/after.jsonl (measured
remote-minus-build-box offsets), console.txt (the build-box console
transcript) and tap-c<N>.pcap (the DUT-link tap). It does not read the
packet's analysis files or tools. Times are seconds after the outlet-off
command on the build-box clock, as on the findings page.

Tap time is placed on the capture server clock by a least-squares line
through the per-5 s minima of (pcap host time - unwrapped tap time), refit
once without minima more than 2 ms from the first line; then the server
offset moves it to the build-box clock.
"""
import json
import re
import struct
import sys
from pathlib import Path

SWITCH = "3cc0c6fffefe0210"
DUT = "020000fffe000001"
WRAP = 1 << 32


def offsets(cdir):
    acc = {}
    for name in ("clock-before.jsonl", "clock-after.jsonl"):
        for ln in (cdir / name).read_text().splitlines():
            r = json.loads(ln)
            role = r["host"].split(">")[-1]
            acc.setdefault(role, []).append(r["offset_s"])
    return {k: sum(v) / len(v) for k, v in acc.items()}


def iso(ts):
    from datetime import datetime
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()


def console(cdir):
    text = (cdir / "console.txt").read_text(errors="replace")
    out = []
    for block in text.split("### ")[1:]:
        m = re.match(r"(\S+) cmd='milan_status'", block)
        if not m:
            continue
        kv = dict(re.findall(r"(\w+)=(\S+)", block))
        if "GPTP_GM" not in kv:
            continue
        out.append(dict(t=iso(m.group(1)), gm=kv["GPTP_GM"], sync=kv["SYNC"],
                        asc=kv["ASCAPABLE"], tu=kv["TU"], clkv=kv["CLKV_STAT"]))
    return out


def tap(cdir, n):
    raw = (cdir / f"tap-c{n}.pcap").read_bytes()
    off, first, recs = 24, None, []
    while off + 16 <= len(raw):
        s, us, incl, _o = struct.unpack("<IIII", raw[off:off + 16])
        off += 16
        pkt = raw[off:off + incl]
        off += incl
        if len(pkt) < 42:
            continue
        tag, _l, port = struct.unpack("<III", pkt[:12])
        w5, w6 = struct.unpack("<II", pkt[20:28])
        if tag != 6 or port not in (2, 3) or w5 != incl - 28:
            continue
        host_ns = s * 10**9 + us * 1000
        lo = struct.unpack("<I", pkt[16:20])[0]
        if first is None:
            first = (host_ns, lo)
        k = round(((host_ns - first[0]) - (lo - first[1])) / WRAP)
        tap_ns = lo - first[1] + k * WRAP
        recs.append((tap_ns, host_ns, port, pkt[28:]))
    # per-5 s minima of host - tap, then a line, refit without outliers
    wins = {}
    for tap_ns, host_ns, _p, _f in recs:
        w = tap_ns // 5_000_000_000
        d = host_ns - tap_ns
        if w not in wins or d < wins[w][1]:
            wins[w] = (tap_ns, d)
    pts = list(wins.values())

    def fit(pp):
        n_ = len(pp)
        mx = sum(x for x, _ in pp) / n_
        my = sum(y for _, y in pp) / n_
        sxx = sum((x - mx) ** 2 for x, _ in pp) or 1
        b = sum((x - mx) * (y - my) for x, y in pp) / sxx
        return my - b * mx, b

    # Theil-Sen start (median pairwise slope), robust to the few windows
    # whose minimum is queue-delayed, then least squares on the inliers.
    slopes = sorted((y2 - y1) / (x2 - x1) for i, (x1, y1) in enumerate(pts)
                    for x2, y2 in pts[i + 1:] if x2 != x1)
    b = slopes[len(slopes) // 2]
    a = sorted(y - b * x for x, y in pts)[len(pts) // 2]
    kept = [(x, y) for x, y in pts if abs(y - (a + b * x)) <= 2e6]
    a, b = fit(kept)
    resid = max(abs(y - (a + b * x)) for x, y in kept) / 1e6
    out = []
    for tap_ns, _h, port, fr in recs:
        server_s = (tap_ns + a + b * tap_ns) / 1e9
        et = struct.unpack(">H", fr[12:14])[0]
        body = fr[14:]
        if et == 0x8100:
            et = struct.unpack(">H", fr[16:18])[0]
            body = fr[18:]
        kind = None
        if et == 0x88F7:
            kind = {0: "Sync", 0xB: "Announce", 2: "PdelayReq", 3: "PdelayResp",
                    8: "FollowUp", 0xA: "PdelayRespFU"}.get(body[0] & 0x0F, "ptp")
            if kind in ("PdelayReq", "PdelayResp", "PdelayRespFU"):
                kind += ":%d" % struct.unpack(">H", body[30:32])[0]
            if kind == "Announce":
                kind += ":" + body[53:61].hex()
        out.append((server_s, port, kind))
    return out, dict(windows=len(pts), kept=len(kept), max_resid_ms=round(resid, 3))


def main():
    base = Path(sys.argv[1])
    print("cycle | off_for | sync0 | gm_own | asc0 | sw_first_frame | sw_first_ann | "
          "asc1 | gm_sw | all_good | recovery | recovery_from_sync | last_sw_frame | fit")
    for n in range(1, 7):
        cdir = base / f"cycle{n}"
        off = offsets(cdir)
        ps = (cdir / "powerstrip.txt").read_text()
        t_off = float(re.search(r"T_OFF_CMD (\S+)", ps).group(1)) - off["pi"]
        t_on = float(re.search(r"T_ON_CMD (\S+)", ps).group(1)) - off["pi"]
        cs = console(cdir)
        rel = lambda t: t - t_off
        after = [c for c in cs if rel(c["t"]) > 0]
        sync0 = next(rel(c["t"]) for c in after if c["sync"] == "0")
        gm_own = next(rel(c["t"]) for c in after if c["gm"] == DUT)
        asc0 = next(rel(c["t"]) for c in after if c["asc"] == "0")
        own_i = next(i for i, c in enumerate(cs) if rel(c["t"]) > 0 and c["gm"] == DUT)
        asc0_i = next(i for i, c in enumerate(cs) if rel(c["t"]) > 0 and c["asc"] == "0")
        asc1 = next(rel(c["t"]) for c in cs[asc0_i:] if c["asc"] == "1")
        gm_sw = next(rel(c["t"]) for c in cs[own_i:] if c["gm"] == SWITCH)

        def ok(c):
            return c["gm"] == SWITCH and c["sync"] == "1" and c["asc"] == "1" and c["tu"] == "0"

        good_i = len(cs)
        while good_i > 0 and ok(cs[good_i - 1]):
            good_i -= 1
        good = rel(cs[good_i]["t"])
        recs, fitinfo = tap(cdir, n)
        bb = [(s - off["ubuntu-server"] - t_off, p, k) for s, p, k in recs]
        sw = [(t, k) for t, p, k in bb if p == 2]
        last_sw = max(t for t, _ in sw if t < 10)
        first_sw = min(t for t, _ in sw if t > 10)
        first_ann = min(t for t, k in sw if t > 10 and k is not None and k.startswith("Announce"))
        first_sync = min(t for t, k in sw if t > 10 and k == "Sync")
        k0 = lambda k, pre: k is not None and k.startswith(pre)
        last_sync = max(t for t, k in sw if t < 10 and k == "Sync")
        last_ann = max(t for t, k in sw if t < 10 and k0(k, "Announce"))
        # last Pdelay response the DUT received (switch answers a DUT request)
        last_resp = max(t for t, k in sw if t < 10 and k0(k, "PdelayResp:"))
        dut = [(t, k) for t, p, k in bb if p == 3]
        # DUT requests after the return and the switch's responses: completed exchanges
        reqs = {k.split(":")[1]: t for t, k in dut if t > 10 and k0(k, "PdelayReq")}
        fus = sorted(t for t, k in sw if t > 10 and k0(k, "PdelayRespFU") and k.split(":")[1] in reqs)
        master_sync = sum(1 for t, k in dut if first_sw < t < gm_sw + 0.05 and k == "Sync")
        master_ann = [k.split(":")[1] for t, k in dut if first_sw < t < gm_sw + 0.05 and k0(k, "Announce")]
        anns_after = sorted(t for t, k in sw if t > 10 and k0(k, "Announce"))
        adopted = min(a for a in anns_after if a <= gm_sw + 0.001) if any(a <= gm_sw + 0.001 for a in anns_after) else None
        adopted = max(a for a in anns_after if a <= gm_sw + 0.001)
        print(f"   loss: sync0-lastSync {sync0 - last_sync:.2f}  gmOwn-lastAnn {gm_own - last_ann:.2f}  "
              f"asc0-lastPdelayResp {asc0 - last_resp:.2f}  |  return: 2nd completed DUT exchange {fus[1]:.2f} "
              f"(asc1 {asc1:.2f}, diff {asc1 - fus[1]:+.2f})  master Syncs {master_sync} master Announce GMs {master_ann}  "
              f"adopted Announce {adopted:.3f} -> CSR {gm_sw:.3f} ({(gm_sw - adopted) * 1000:.0f} ms); "
              f"announces after return {[round(a, 3) for a in anns_after[:3]]}")
        print(f"{n} | {t_on - t_off:.2f} | {sync0:.2f} | {gm_own:.2f} | {asc0:.2f} | "
              f"{first_sw:.2f} | {first_ann:.2f} | {asc1:.2f} | {gm_sw:.2f} | {good:.2f} | "
              f"{good - first_ann:.2f} | {good - min(first_ann, first_sync):.2f} vs sync {good - first_sync:.2f} | "
              f"{last_sw:.2f} | {fitinfo}")


if __name__ == "__main__":
    main()
