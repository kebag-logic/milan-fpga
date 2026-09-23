#!/usr/bin/env python3
"""Independent re-derivation of the step 3 console and tap edges per cycle.

Usage: step3_recheck.py ARCHIVE_ROOT
  ARCHIVE_ROOT is review-evidence/117-r1 at the pinned commit.

Times are seconds after the outlet-off command on the build-box clock:
  t_off = T_OFF_CMD (power-strip host clock) - offset(power-strip host),
where the offset is the mean of the before/after best-5 medians in
clock-before.jsonl / clock-after.jsonl (the host whose name ends in 'pi').
Console samples carry the '### <ts>' send time (build-box clock).
Tap records: the 32-bit ns word is unwrapped against pcap host time; tap time
is mapped to the capture-server clock by a least-squares line through the
per-5 s minima of (host - tap), then to the build box by subtracting the
capture server's offset (host whose name ends in 'ubuntu-server').
Nothing here reuses the packet's analysis scripts.
"""
import datetime as dt, json, os, re, struct, sys

WRAP = 1 << 32


def offsets(cdir):
    acc = {}
    for f in ("clock-before.jsonl", "clock-after.jsonl"):
        for ln in open(os.path.join(cdir, f)):
            d = json.loads(ln)
            acc.setdefault(d["host"], []).append(d["offset_s_median_best5"])
    return {h: sum(v) / len(v) for h, v in acc.items()}


def host(offs, suffix):
    return next(v for h, v in offs.items() if h.endswith(suffix))


def t_off(cdir, offs):
    t = open(os.path.join(cdir, "powerstrip.txt")).read()
    return float(re.search(r"T_OFF_CMD (\S+)", t).group(1)) - host(offs, "pi"), \
        float(re.search(r"T_ON_CMD (\S+)", t).group(1)) - host(offs, "pi")


def console(cdir, t0):
    txt = open(os.path.join(cdir, "console.txt"), encoding="utf-8", errors="replace").read()
    out = []
    for blk in re.split(r"^### ", txt, flags=re.M)[1:]:
        m = re.match(r"(\S+) cmd='milan_status'", blk)
        if not m:
            continue
        ts = dt.datetime.fromisoformat(m.group(1).replace("Z", "+00:00")).timestamp() - t0
        f = dict(re.findall(r"(\w+)=([0-9a-fx]+)", blk))
        if "CLKV_STAT" not in f:
            continue
        out.append(dict(t=ts, clkv=int(f["CLKV_STAT"], 16), gm=f.get("GPTP_GM"),
                        pdelay=int(f["PDELAY_NS"]) if "PDELAY_NS" in f else None))
    return out


def tap(path):
    raw = open(path, "rb").read()
    nano = struct.unpack("<I", raw[:4])[0] == 0xA1B23C4D
    off, first, recs = 24, None, []
    while off + 16 <= len(raw):
        s, f, incl, _o = struct.unpack("<IIII", raw[off:off + 16])
        off += 16
        pkt = raw[off:off + incl]
        off += incl
        if len(pkt) < 42:
            continue
        tag, _l, port = struct.unpack("<III", pkt[:12])
        if tag != 6 or port not in (2, 3):
            continue
        hns = s * 10**9 + (f if nano else f * 1000)
        lo = struct.unpack("<I", pkt[16:20])[0]
        if first is None:
            first = (hns, lo)
        k = round(((hns - first[0]) - (lo - first[1])) / WRAP)
        recs.append(dict(h=hns, tap=lo - first[1] + k * WRAP, port=port, fr=pkt[28:]))
    # per-5 s minima of host - tap, least-squares line in tap time
    win = {}
    for r in recs:
        w = r["h"] // (5 * 10**9)
        d = r["h"] - r["tap"]
        if w not in win or d < win[w][1]:
            win[w] = (r["tap"], d)
    xs = [v[0] / 1e9 for v in win.values()]
    ys = [v[1] / 1e9 for v in win.values()]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx if sxx else 0.0
    a = my - b * mx
    resid = max(abs(y - (a + b * x)) for x, y in zip(xs, ys))
    for r in recs:
        x = r["tap"] / 1e9
        r["srv"] = x + a + b * x
    return recs, resid


def ptp(fr):
    et = struct.unpack(">H", fr[12:14])[0]
    p = fr[14:]
    if et == 0x8100:
        et = struct.unpack(">H", fr[16:18])[0]
        p = fr[18:]
    if et != 0x88F7 or len(p) < 34:
        return None
    mt = p[0] & 0xF
    d = dict(mt=mt, seq=struct.unpack(">H", p[30:32])[0], src=p[20:30].hex())
    if mt in (0x3, 0xA) and len(p) >= 54:
        d["req"] = p[44:54].hex()
    return d


def main():
    root = sys.argv[1]
    dut_port = "020000fffe0000010001"
    for c in range(1, 7):
        cdir = os.path.join(root, "bench-a202", "bench", f"cycle{c}")
        offs = offsets(cdir)
        t0, ton = t_off(cdir, offs)
        srv_off = host(offs, "ubuntu-server")
        cs = console(cdir, t0)
        # holdover run at the loss edge
        i = next(k for k, s in enumerate(cs) if s["t"] > 0 and s["clkv"] & 0x8)
        j = i
        while j < len(cs) and cs[j]["clkv"] & 0x8:
            j += 1
        hold_n, hold_span = j - i, cs[j]["t"] - cs[i]["t"]
        sync0 = next(s["t"] for s in cs if s["t"] > 0 and not s["clkv"] & 0x2)
        # asCapable return: first 0 -> 1 on bit 16 after t > 20
        k = next(k for k in range(1, len(cs)) if cs[k]["t"] > 20 and cs[k]["clkv"] & 0x10000
                 and not cs[k - 1]["clkv"] & 0x10000)
        asc_t, asc_prev, asc_pd = cs[k]["t"], cs[k - 1]["t"], cs[k]["pdelay"]
        # all-good: first sample from which every later sample is good
        good = [s["gm"] == "3cc0c6fffefe0210" and (s["clkv"] & 0x10003) == 0x10002 for s in cs]
        ag = None
        for q in range(len(cs) - 1, -1, -1):
            if not good[q]:
                break
            ag = cs[q]["t"]
        recs, resid = tap(os.path.join(cdir, f"tap-c{c}.pcap"))
        for r in recs:
            r["t"] = r["srv"] - srv_off - t0
        far = [r for r in recs if r["port"] == 2]
        last_before = max(r["t"] for r in far if r["t"] < 10)
        ff = min(r["t"] for r in far if r["t"] > 10)
        ann = min(r["t"] for r in far if r["t"] > 10 and (ptp(r["fr"]) or {}).get("mt") == 0xB)
        syn = min(r["t"] for r in far if r["t"] > 10 and (ptp(r["fr"]) or {}).get("mt") == 0x0)
        # DUT-requested exchanges completed after the return (Resp + Resp_FU from the switch)
        reqs, resp, rfu = {}, {}, {}
        for r in recs:
            if r["t"] <= 10:
                continue
            d = ptp(r["fr"])
            if not d:
                continue
            if r["port"] == 3 and d["mt"] == 0x2 and d["src"] == dut_port:
                reqs.setdefault(d["seq"], r["t"])
            elif r["port"] == 2 and d["mt"] == 0x3 and d.get("req") == dut_port:
                resp.setdefault(d["seq"], r["t"])
            elif r["port"] == 2 and d["mt"] == 0xA and d.get("req") == dut_port:
                rfu.setdefault(d["seq"], r["t"])
        done = sorted(rfu[s] for s in rfu if s in reqs and s in resp)
        ex2 = done[1] if len(done) > 1 else None
        silent_from = max(r["t"] for r in recs if r["t"] < 10)
        silent_to = min(r["t"] for r in recs if r["t"] > 10)
        rec = ann if ann < syn else syn
        print(f"CYCLE {c} off_for={ton - t0:.2f} tap_fit_resid_ms={resid*1e3:.2f} "
              f"sync0={sync0:.2f} holdover_samples={hold_n} holdover_first_set_to_first_clear={hold_span:.2f} "
              f"switch_last_frame={last_before:.2f} tap_silent={silent_from:.2f}..{silent_to:.2f} "
              f"switch_first_frame={ff:.2f} first_announce={ann:.2f} first_sync={syn:.2f} "
              f"ascap1_sample={asc_t:.2f} prev_sample={asc_prev:.2f} pdelay_at_ascap={asc_pd} "
              f"dut_ex2_complete={ex2:.2f} ascap_minus_first_frame={asc_t - ff:.2f} "
              f"all_good={ag:.2f} recovery={ag - rec:.2f}")


if __name__ == "__main__":
    main()
