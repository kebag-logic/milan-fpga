#!/usr/bin/env python3
"""Independent re-derivation of the step 3 per-cycle table from the pinned archive.

Usage: step3_rederive.py <evidence-root: .../review-evidence/117-r1>

Clocks: the console transcript is on the build-box clock; the power-strip log on
the power-strip host; tap pcap host stamps on the capture server; the watcher on
the controller host. Each remote clock is moved to the build box with the median
of the best-5 bracketed offsets recorded before and after the cycle (mean of the
two). Tap hardware time is unwrapped and placed on the capture-server clock by a
least-squares line through the per-5 s minima of (host time - tap time).
All printed times are seconds after the outlet-off command, build-box clock.
"""
import datetime as dt
import json
import os
import re
import struct
import sys

GM_SELF = "020000fffe000001"
GM_SW = "3cc0c6fffefe0210"
WRAP = 1 << 32


def offsets(cdir):
    res = {}
    for fn in ("clock-before.jsonl", "clock-after.jsonl"):
        for line in open(os.path.join(cdir, fn)):
            if line.strip():
                r = json.loads(line)
                h = r["host"].split(">")[-1]
                res.setdefault(h, []).append(r["offset_s_median_best5"])
    return {h: sum(v) / len(v) for h, v in res.items()}


def strip_times(cdir):
    t = open(os.path.join(cdir, "powerstrip.txt")).read()
    off = float(re.search(r"T_OFF_CMD (\S+)", t).group(1))
    on = float(re.search(r"T_ON_CMD (\S+)", t).group(1))
    return off, on


def console(cdir):
    txt = open(os.path.join(cdir, "console.txt"), errors="replace").read()
    out = []
    for m in re.finditer(r"^### (\S+) cmd='milan_status'[^\n]*\n(.*?)(?=^### |\Z)", txt, re.M | re.S):
        ts = dt.datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=dt.timezone.utc).timestamp()
        body = m.group(2)
        f = dict(re.findall(r"(\w+)=(\S+)", body))
        if "GPTP_GM" not in f:
            continue
        out.append((ts, f))
    return out


def tap(cdir, name):
    raw = open(os.path.join(cdir, name), "rb").read()
    off = 24
    recs = []
    first = None
    while off + 16 <= len(raw):
        s, us, incl, _ = struct.unpack("<IIII", raw[off:off + 16])
        off += 16
        pkt = raw[off:off + incl]
        off += incl
        host_ns = s * 10**9 + us * 1000
        if len(pkt) < 42:
            continue
        tag, _, port = struct.unpack("<III", pkt[:12])
        if tag != 6 or port not in (2, 3):
            continue
        lo = struct.unpack("<I", pkt[16:20])[0]
        if first is None:
            first = (host_ns, lo)
        k = round(((host_ns - first[0]) - (lo - first[1])) / WRAP)
        recs.append([host_ns, lo - first[1] + k * WRAP, port, pkt[28:]])
    # line through per-5 s minima of host - tap
    bins = {}
    for h, t, _, _ in recs:
        b = t // (5 * 10**9)
        d = h - t
        if b not in bins or d < bins[b][1]:
            bins[b] = (t, d)
    xs = [v[0] / 1e9 for v in bins.values()]
    ys = [v[1] / 1e9 for v in bins.values()]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx if sxx else 0.0
    b0 = my - a * mx
    resid = max(abs(y - (a * x + b0)) for x, y in zip(xs, ys))
    out = []
    for h, t, port, fr in recs:
        server = t / 1e9 + a * (t / 1e9) + b0
        out.append((server, port, decode(fr)))
    return out, resid


def decode(fr):
    et = struct.unpack(">H", fr[12:14])[0]
    p = fr[14:]
    if et == 0x8100:
        et = struct.unpack(">H", fr[16:18])[0]
        p = fr[18:]
    d = {"et": et}
    if et == 0x88F7 and len(p) >= 34:
        d["mt"] = p[0] & 0xF
        d["seq"] = struct.unpack(">H", p[30:32])[0]
        d["src"] = p[20:28].hex()
        if d["mt"] == 0xB and len(p) >= 64:
            d["p1"] = p[47]
            d["gm"] = p[53:61].hex()
    elif et == 0x22F0 and len(p) >= 1:
        d["subtype"] = p[0]
        if p[0] == 0xFC and len(p) >= 2:  # ACMP
            d["acmp_msg"] = p[1] & 0x0F
    return d


def first(seq, pred, after=None):
    for t, *rest in seq:
        if (after is None or t > after) and pred(t, *rest):
            return t
    return None


def last(seq, pred, before=None):
    r = None
    for t, *rest in seq:
        if (before is None or t < before) and pred(t, *rest):
            r = t
    return r


def main():
    root = sys.argv[1]
    base = os.path.join(root, "bench-a202", "bench")
    for c in range(1, 7):
        cdir = os.path.join(base, f"cycle{c}")
        offs = offsets(cdir)
        off_pi = [v for h, v in offs.items() if h.endswith("pi")][0]
        off_srv = [v for h, v in offs.items() if "server" in h][0]
        t_off, t_on = strip_times(cdir)
        T0 = t_off - off_pi
        con = [(ts - T0, f) for ts, f in console(cdir)]
        taps, resid = tap(cdir, f"tap-c{c}.pcap")
        tp = [(s - off_srv - T0, port, d) for s, port, d in taps]
        on_rel = t_on - off_pi - T0

        def ok(f):
            return f["GPTP_GM"] == GM_SW and f["SYNC"] == "1" and f["ASCAPABLE"] == "1" and f["TU"] == "0"

        sync0 = first(con, lambda t, f: f["SYNC"] == "0")
        gmself = first(con, lambda t, f: f["GPTP_GM"] == GM_SELF)
        asc0 = first(con, lambda t, f: f["ASCAPABLE"] == "0")
        ret = on_rel
        asc1 = first(con, lambda t, f: f["ASCAPABLE"] == "1", after=ret)
        gmsw = first(con, lambda t, f: f["GPTP_GM"] == GM_SW, after=ret)
        allgood = None
        for i in range(len(con) - 1, -1, -1):
            if not ok(con[i][1]):
                allgood = con[i + 1][0] if i + 1 < len(con) else None
                break
        # holdover bit 3 at the loss
        hold = [t for t, f in con if t < ret and int(f["CLKV_STAT"], 16) & 0x8]
        # wire
        sw_last = last(tp, lambda t, port, d: port == 2, before=ret)
        sw_last_sync = last(tp, lambda t, port, d: port == 2 and d.get("mt") == 0, before=ret)
        sw_last_ann = last(tp, lambda t, port, d: port == 2 and d.get("mt") == 0xB, before=ret)
        sw_last_presp = last(tp, lambda t, port, d: port == 2 and d.get("mt") == 3, before=ret)
        sw_first = first(tp, lambda t, port, d: port == 2, after=ret)
        sw_first_ann = first(tp, lambda t, port, d: port == 2 and d.get("mt") == 0xB, after=ret)
        sw_first_sync = first(tp, lambda t, port, d: port == 2 and d.get("mt") == 0, after=ret)
        dut_last = last(tp, lambda t, port, d: port == 3, before=ret)
        dark_end = first(tp, lambda t, port, d: True, after=ret)
        # DUT Pdelay exchanges completed after return (DUT requester)
        reqs = {}
        done = []
        for t, port, d in tp:
            if t < ret:
                continue
            if port == 3 and d.get("mt") == 2:
                reqs[d["seq"]] = [t, False]
            elif port == 2 and d.get("mt") == 3 and d.get("seq") in reqs:
                reqs[d["seq"]][1] = True
            elif port == 2 and d.get("mt") == 0xA and d.get("seq") in reqs and reqs[d["seq"]][1]:
                done.append(t)
        second_pd = done[1] if len(done) > 1 else None
        master_syncs = sum(1 for t, port, d in tp if port == 3 and d.get("mt") == 0 and sw_first and sw_first < t < (gmsw or 1e9) + 0.2)
        master_anns = sum(1 for t, port, d in tp if port == 3 and d.get("mt") == 0xB and sw_first and sw_first < t < (gmsw or 1e9) + 0.2)
        pd_at_asc1 = [f["PDELAY_NS"] for t, f in con if t == asc1]
        start = min(x for x in (sw_first_ann, sw_first_sync) if x is not None)
        rec = allgood - start if allgood is not None else None

        def r2(x):
            return None if x is None else round(x, 2)
        print(f"cycle {c}: tap-line residual {resid*1e3:.2f} ms; off-for {r2(on_rel)}")
        print(f"   DUT sync0/tu1 {r2(sync0)}  GM=self {r2(gmself)}  asCapable0 {r2(asc0)}  | switch first frame {r2(sw_first)}  first Announce {r2(sw_first_ann)}  first Sync {r2(sw_first_sync)}")
        print(f"   DUT asCapable1 {r2(asc1)}  GM=switch {r2(gmsw)}  all-good {r2(allgood)}  recovery {r2(rec)}  (from first Sync: {r2(allgood - sw_first_sync) if allgood and sw_first_sync else None})")
        print(f"   loss: sync0 - last switch Sync {r2(sync0 - sw_last_sync) if sync0 and sw_last_sync else None}; GM=self - last Announce {r2(gmself - sw_last_ann) if gmself and sw_last_ann else None}; asCapable0 - last Pdelay_Resp {r2(asc0 - sw_last_presp) if asc0 and sw_last_presp else None}")
        print(f"   holdover-set samples before return {len(hold)} span {r2(hold[-1]-hold[0]) if hold else None}; switch last frame {r2(sw_last)}; DUT last frame {r2(dut_last)}; dark until {r2(dark_end)}")
        print(f"   asCapable1 - 2nd completed DUT Pdelay {r2(asc1 - second_pd) if asc1 and second_pd else None}; 2nd completed after switch first frame {r2(second_pd - sw_first) if second_pd and sw_first else None}; asCapable1 after switch first frame {r2(asc1 - sw_first) if asc1 and sw_first else None}; PDELAY at asCapable1 {pd_at_asc1}; DUT master Syncs {master_syncs}, Announces {master_anns}")
        print(f"   on->all-good {r2(allgood - on_rel) if allgood else None}; first frame->all-good {r2(allgood - sw_first) if allgood and sw_first else None}")


if __name__ == "__main__":
    main()
