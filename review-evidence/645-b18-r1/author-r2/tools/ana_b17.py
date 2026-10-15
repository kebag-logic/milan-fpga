#!/usr/bin/env python3
"""Lane B17: grade one bind cycle (offline, read-only; nothing here touches the bench).

usage: ana_b17.py cycle   <cycle_dir> <capture.pcap> <out.json>
       ana_b17.py control <out.json>

The poll (cycle_dir/poll.jsonl, console_poll_b8.py rows) and the events (cycle_dir/events.jsonl, cyc_b17.py):
  * every change of SLIP_LB (0x8D4: [15:0] dups, [31:16] skips) and SLIP_TDM (0x8D8) between two polls, with
    its interval relative to the bind: from the earlier poll's start to the later poll's end (the word is read
    inside each poll), on this host's clock;
  * RENDER_STAT (0x8DC: [7:0] fill, [8] prefill, [9] converged, [31:16] rails), MCSRV_STAT (0x8F8 [2:0]) and
    AAFM_STAT (0x8E0) as read; the poll's coverage before and after the bind.
The capture (the DUT's link tap; each frame behind the tap's 28-byte record header: little-endian words,
[0] tag 6, [2] port, 2 = switch to DUT, 3 = DUT to switch, [4] the tap's nanosecond counter, low 32 bits,
unwrapped against the pcap time as lane B14's tapdec_b14.py does):
  * per AVTP stream (IEEE 1722-2016): AAF (subtype 0x02, clause 7) sequence_num and avtp_timestamp; CRF
    (subtype 0x04, clause 10) sequence_num and its first timestamp;
  * each stream's media clock against gPTP time from its presentation timestamps: a least-squares line of the
    unwrapped timestamp against the PDU index (sequence_num unwrapped, so a lost PDU keeps its index), rate
    = slope / nominal step - 1 (AAF: 6 events of 48 kHz, 125,000 ns; CRF: timestamps per PDU x
    timestamp_interval / base_frequency);
  * delta_ppm = the peer's AAF stream (port 2) minus the DUT's AAF stream (port 3): the push rate of the
    DUT's loopback ring against its pop rate (the DUT's packet grid stamps its own talker's timestamps). The
    rate-offset slip interval is 1 / (48,000 x |delta_ppm| x 1e-6) s; a slower peer (delta < 0) empties the
    ring (dups), a faster one fills it (skips);
  * ACMP (subtype 0xFC, IEEE 1722.1 clause 8) frames naming the DUT's listener 0: the unbind's and the bind's
    commands and responses on the tap's clock, which places the bind on the capture;
  * the bind priming: the first peer PDU after the bind's CONNECT_RX_RESPONSE, its delay, and the arrival
    phase of the peer's PDUs against the DUT's own transmit grid (a line fitted to the DUT's AAF PDUs on the
    same tap clock), modulo one PDU (125 us) and one media tick (20.833 us), up to the DUT's fixed latencies;
  * arrival lateness: each peer PDU's arrival minus a line fitted to the arrivals after the bind; every PDU
    later than 10 us, with its time from the bind; for each slip, the largest lateness inside its interval,
    mapped to the tap clock through the bind's CONNECT_RX_COMMAND.
Classification per slip (the resume ruling): (a) between a settle recentre's arming and its firing; (b) a rate
offset, the slips periodic at 1 / (f_s x |delta_ppm|) within the poll resolution, in the direction delta's sign
gives, with at least one slip expected in the window; (c) neither. On this image no CSR exposes the recentre
count or the aligner's state, so (a) is graded only on what is observable: a CLOCK_SOURCE change in the cycle
(none is made) is the only observable arming term.
"""
import json
import math
import struct
import sys
from pathlib import Path

import numpy as np

FS = 48_000
AAF_STEP_NS = 125_000
TICK_NS = 1e9 / FS
LATE_US = 10.0
DUT_EID = bytes.fromhex("020000fffe000001")
ACMP_NAMES = {0: "CONNECT_TX_COMMAND", 1: "CONNECT_TX_RESPONSE", 2: "DISCONNECT_TX_COMMAND",
              3: "DISCONNECT_TX_RESPONSE", 6: "CONNECT_RX_COMMAND", 7: "CONNECT_RX_RESPONSE",
              8: "DISCONNECT_RX_COMMAND", 9: "DISCONNECT_RX_RESPONSE"}


def jl(path):
    return [json.loads(x) for x in open(path) if x.startswith("{")]


# ----------------------------------------------------------------------------------------------- poll
def w(row, off):
    v = row["words"].get(off)
    return None if v is None else int(v, 16)


def poll_analysis(rows, t_bind, t_unbind):
    rows = sorted(rows, key=lambda r: r["n"])
    rel = lambda x: round(x - t_bind, 3)
    out = dict(polls=len(rows), first_poll_s=rel(rows[0]["t0"]), last_poll_s=rel(rows[-1]["t1"]),
               unbind_s=rel(t_unbind), missing_reads=0)
    gaps = [b["t0"] - a["t0"] for a, b in zip(rows, rows[1:])]
    out["poll_spacing_s"] = dict(median=round(float(np.median(gaps)), 3), max=round(max(gaps), 3)) if gaps else None
    slips, tdm, render, servo, aafm = [], [], [], set(), set()
    prev = None
    for r in rows:
        lb, td, rs, ms, am = (w(r, k) for k in ("0x8d4", "0x8d8", "0x8dc", "0x8f8", "0x8e0"))
        if None in (lb, td, rs, ms, am):
            out["missing_reads"] += 1
            continue
        servo.add(ms & 7)
        aafm.add(f"{am:08x}")
        render.append(dict(s=rel(r["t1"]), fill=rs & 0xFF, prefill=rs >> 8 & 1, converged=rs >> 9 & 1, rails=rs >> 16))
        if prev is not None:
            plb, ptd, pt0 = prev
            for name, cur, old, dst in (("SLIP_LB", lb, plb, slips), ("SLIP_TDM", td, ptd, tdm)):
                dd, ds = (cur & 0xFFFF) - (old & 0xFFFF), (cur >> 16) - (old >> 16)
                if dd or ds:
                    lo, hi = rel(pt0), rel(r["t1"])
                    dst.append(dict(word=name, dups=dd, skips=ds, s_lo=lo, s_hi=hi, poll_n=r["n"],
                                    bound=not (rel(t_unbind) <= lo and hi <= 0.0),
                                    after=dict(dups=cur & 0xFFFF, skips=cur >> 16)))
        prev = (lb, td, r["t0"])
    first = next(w(r, "0x8d4") for r in rows if w(r, "0x8d4") is not None)
    last = next(w(r, "0x8d4") for r in reversed(rows) if w(r, "0x8d4") is not None)
    out.update(slip_lb_first=dict(dups=first & 0xFFFF, skips=first >> 16),
               slip_lb_last=dict(dups=last & 0xFFFF, skips=last >> 16), slips=slips, slip_tdm_changes=tdm,
               servo_states=sorted(servo), aafm_stat_values=sorted(aafm))
    pre = [x for x in render if x["s"] <= 0]
    post = [x for x in render if x["s"] > 0]
    out["render"] = dict(
        before_unbind=next((x for x in render if x["s"] < out["unbind_s"]), None),
        prefill_exit_s=next((x["s"] for x in post if not x["prefill"]), None),
        converged_first_s=next((x["s"] for x in post if x["converged"]), None),
        fill_after_prefill=dict(min=min((x["fill"] for x in post if not x["prefill"]), default=None),
                                max=max((x["fill"] for x in post if not x["prefill"]), default=None)),
        rails=sorted({x["rails"] for x in render}), unbound_prefill=all(x["prefill"] for x in pre if x["s"] > out["unbind_s"] + 1))
    return out


# ------------------------------------------------------------------------------------------------ tap
def read_pcap(path):
    f = open(path, "rb")
    head = f.read(24)
    nano = head[:4] == b"\x4d\x3c\xb2\xa1"
    first = None
    while True:
        h = f.read(16)
        if len(h) < 16:
            break
        sec, frac, incl, _ = struct.unpack("<4I", h)
        pkt = f.read(incl)
        if len(pkt) < incl:
            break
        if len(pkt) < 46:
            continue
        tag, _, port = struct.unpack("<3I", pkt[:12])
        if tag != 6:
            continue
        host = sec * 10**9 + frac * (1 if nano else 1000)
        lo = struct.unpack("<I", pkt[16:20])[0]
        if first is None:
            first = (host, lo)
        ns = lo - first[1] + round(((host - first[0]) - (lo - first[1])) / (1 << 32)) * (1 << 32)
        yield port, ns, pkt[28:]


def line_fit(x, y):
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    xm, ym = x.mean(), y.mean()
    b = float(((x - xm) * (y - ym)).sum() / ((x - xm) ** 2).sum())
    a = float(ym - b * xm)
    return a, b, y - (a + b * x)


def unwrap(vals, mod, step_hint):
    out, acc, prev = [], 0, None
    for v in vals:
        if prev is not None:
            d = (v - prev) % mod
            acc += d if step_hint is None or d < mod // 2 else d - mod
        out.append(acc)
        prev = v
    return out


def tap_analysis(path):
    streams, acmp = {}, []
    n = 0
    for port, ns, fr in read_pcap(path):
        n += 1
        et = int.from_bytes(fr[12:14], "big")
        o = 14
        if et == 0x8100:
            et = int.from_bytes(fr[16:18], "big")
            o = 18
        if et != 0x22F0:
            continue
        p = fr[o:]
        if len(p) < 24:
            continue
        sub = p[0]
        if sub == 0xFC and len(p) >= 44:
            mt = p[1] & 0x0F
            if mt in ACMP_NAMES and p[28:36] == DUT_EID and int.from_bytes(p[38:40], "big") == 0:
                acmp.append(dict(port=port, ns=ns, msg=ACMP_NAMES[mt], status=p[2] >> 3,
                                 talker_uid=int.from_bytes(p[36:38], "big"),
                                 connection_count=int.from_bytes(p[46:48], "big") if len(p) >= 48 else None))
            continue
        if sub not in (0x02, 0x04):
            continue
        key = (port, sub, p[4:12].hex())
        s = streams.setdefault(key, dict(seq=[], ts=[], ns=[], meta=None))
        s["seq"].append(p[2])
        s["ns"].append(ns)
        if sub == 0x02:
            s["ts"].append(int.from_bytes(p[12:16], "big"))
        else:
            if s["meta"] is None and len(p) >= 28:
                bf = int.from_bytes(p[12:16], "big")
                s["meta"] = dict(pull=bf >> 29, base_frequency=bf & 0x1FFFFFFF, crf_data_length=int.from_bytes(p[16:18], "big"),
                                 timestamp_interval=int.from_bytes(p[18:20], "big"))
            s["ts"].append(int.from_bytes(p[20:28], "big") if len(p) >= 28 else None)
    return n, streams, acmp


def segments(seq, ns, max_gap_ns=50_000_000):
    """Split a stream into runs without a pause longer than max_gap_ns (the unbind leaves a gap)."""
    cut = [0] + [i for i in range(1, len(ns)) if ns[i] - ns[i - 1] > max_gap_ns] + [len(ns)]
    return [(a, b) for a, b in zip(cut, cut[1:]) if b > a]


def stream_rate(s, sub, a, b):
    seq = s["seq"][a:b]
    k = np.array(unwrap(seq, 256, 1), dtype=np.float64)
    gaps = int(sum(1 for i in range(1, len(seq)) if (seq[i] - seq[i - 1]) % 256 != 1))
    ts = [t for t in s["ts"][a:b]]
    if sub == 0x02:
        nominal = AAF_STEP_NS
        tsu = np.array(unwrap(ts, 1 << 32, None), dtype=np.float64)
    else:
        m = s["meta"]
        mult = {0: 1.0, 1: 1 / 1.001, 2: 1.001, 3: 24 / 25, 4: 25 / 24, 5: 1 / 8}.get(m["pull"], 1.0)
        nominal = (m["crf_data_length"] // 8) * m["timestamp_interval"] / (m["base_frequency"] * mult) * 1e9
        tsu = np.array(unwrap([t & 0xFFFFFFFF for t in ts], 1 << 32, None), dtype=np.float64)
    _, slope, res = line_fit(k, tsu)
    _, aslope, _ = line_fit(k, np.array(s["ns"][a:b], dtype=np.float64))
    return dict(pdus=b - a, seq_gaps=gaps, span_s=round((s["ns"][b - 1] - s["ns"][a]) / 1e9, 3), nominal_step_ns=nominal,
                rate_ppm=round((slope / nominal - 1) * 1e6, 4), ts_residual_rms_ns=round(float(np.sqrt((res ** 2).mean())), 1),
                ts_residual_max_ns=round(float(np.abs(res).max()), 1),
                arrival_rate_tap_ppm=round((aslope / nominal - 1) * 1e6, 4))


def classify(slips, delta_ppm, windows):
    """windows: [(lo, hi)] of bound polling relative to the bind, s. Returns per-slip classes and the basis."""
    s_pred = math.inf if not delta_ppm else 1.0 / (FS * abs(delta_ppm) * 1e-6)
    expect_dups = delta_ppm is not None and delta_ppm < 0
    w_total = sum(hi - lo for lo, hi in windows)
    n_expected = w_total / s_pred
    out = []
    lb = [x for x in slips if x["word"] == "SLIP_LB" and x["bound"]]
    for i, x in enumerate(lb):
        right_dir = (x["dups"] > 0 and x["skips"] == 0) if expect_dups else (x["skips"] > 0 and x["dups"] == 0)
        basis = []
        periodic = False
        if s_pred <= w_total and right_dir:
            nb = [y for j, y in enumerate(lb) if j != i]
            mids = sorted([(y["s_lo"] + y["s_hi"]) / 2 for y in lb])
            if len(lb) == 1:
                periodic = n_expected <= 2.0
            else:
                tol = max((y["s_hi"] - y["s_lo"]) for y in lb)
                iv = [b - a for a, b in zip(mids, mids[1:])]
                periodic = all(abs(v / s_pred - round(v / s_pred)) * s_pred <= tol and round(v / s_pred) >= 1 for v in iv)
            basis.append(f"rate interval {s_pred:.3f} s within the bound window {w_total:.1f} s; periodic within the poll "
                         f"resolution: {periodic}")
        else:
            basis.append(f"rate interval {s_pred:.1f} s" + (" exceeds the bound window" if s_pred > w_total else "")
                         + ("" if right_dir else "; direction does not match delta's sign"))
        basis.append("(a) not shown: no CLOCK_SOURCE change in the cycle, and the aligner's state and the recentre "
                     "count are not exposed by any CSR on this image")
        cls = "b" if (s_pred <= w_total and right_dir and periodic) else "c"
        out.append(dict(s_lo=x["s_lo"], s_hi=x["s_hi"], dups=x["dups"], skips=x["skips"], cls=cls, basis=basis))
    return dict(rate_interval_s=None if math.isinf(s_pred) else round(s_pred, 3), bound_window_s=round(w_total, 3),
                rate_slips_expected=round(n_expected, 4), slips=out)


def cycle(cdir, pcap):
    ev = jl(Path(cdir) / "events.jsonl")
    get = lambda kind: [e for e in ev if e["kind"] == kind]
    t_bind = get("bind-time")[0]["t_bind_local"]
    ub, bd = get("unbind")[0], get("bind")[-1]
    t_unbind = ub["t_cmd_local"]
    pa = poll_analysis(jl(Path(cdir) / "poll.jsonl"), t_bind, t_unbind)
    res = dict(cycle=Path(cdir).name, bind_local=t_bind, unbind_local=t_unbind,
               bind_status=bd["status"], unbind_status=ub["status"],
               states={e["when"]: dict(clk_dut=e["clk_dut"], clk_peer=e["clk_peer"], rx_dut_0=e["rx_dut_0"]) for e in get("state")},
               format_check=get("format-check"), poll=pa)
    delta = None
    if pcap:
        n, streams, acmp = tap_analysis(pcap)
        res["tap"] = dict(frames=n)
        by = {}
        for (port, sub, sid), s in streams.items():
            name = {(2, 0x02): "peer-aaf", (3, 0x02): "dut-aaf", (3, 0x04): "dut-crf"}.get((port, sub), f"port{port}-{sub:#04x}")
            if name in by:
                name = f"{name}-{sid[-4:]}"
            by[name] = (s, sub)
        cmd = [x for x in acmp if x["msg"] == "CONNECT_RX_COMMAND" and x["port"] == 2]
        rsp = [x for x in acmp if x["msg"] == "CONNECT_RX_RESPONSE" and x["port"] == 3 and x["status"] == 0]
        dcmd = [x for x in acmp if x["msg"] == "DISCONNECT_RX_COMMAND" and x["port"] == 2]
        res["tap"]["acmp"] = [dict(msg=x["msg"], port=x["port"], status=x["status"], connection_count=x["connection_count"],
                                   s=round((x["ns"] - cmd[-1]["ns"]) / 1e9, 6) if cmd else None) for x in acmp]
        t_cmd = cmd[-1]["ns"] if cmd else None
        t_rsp = rsp[-1]["ns"] if rsp else None
        if t_cmd is not None and dcmd:
            # the unbind against the bind on both clocks: a check of the tap-to-host mapping
            res["tap"]["unbind_to_bind_tap_s"] = round((t_cmd - dcmd[-1]["ns"]) / 1e9, 4)
            res["tap"]["unbind_to_bind_host_s"] = round(t_bind - t_unbind, 4)
        rates = {}
        for name, (s, sub) in by.items():
            segs = segments(s["seq"], s["ns"])
            post = [(a, b) for a, b in segs if t_cmd is None or s["ns"][b - 1] > t_cmd]
            a, b = max(post or segs, key=lambda ab: ab[1] - ab[0])
            r = stream_rate(s, sub, a, b)
            r["segments"] = len(segs)
            r["first_s"] = round((s["ns"][a] - t_cmd) / 1e9, 6) if t_cmd is not None else None
            r["last_s"] = round((s["ns"][b - 1] - t_cmd) / 1e9, 6) if t_cmd is not None else None
            rates[name] = r
        res["tap"]["streams"] = rates
        if "peer-aaf" in rates and "dut-aaf" in rates:
            delta = round(rates["peer-aaf"]["rate_ppm"] - rates["dut-aaf"]["rate_ppm"], 4)
            res["tap"]["delta_ppm"] = delta
            res["tap"]["delta_basis"] = "the AAF presentation timestamps on the DUT's link: the peer's received stream minus the DUT's transmitted stream"
            if "dut-crf" in rates:
                res["tap"]["delta_vs_dut_crf_ppm"] = round(rates["peer-aaf"]["rate_ppm"] - rates["dut-crf"]["rate_ppm"], 4)
        # the priming: the peer's first PDU after the bind, and its arrival phase against the DUT's transmit grid
        if t_rsp is not None and "peer-aaf" in by and "dut-aaf" in by:
            ps, _ = by["peer-aaf"]
            ds, _ = by["dut-aaf"]
            i0 = next((i for i, t in enumerate(ps["ns"]) if t > t_rsp), None)
            if i0 is not None:
                pk = np.array(unwrap(ps["seq"][i0:], 256, 1), dtype=np.float64)
                pt = np.array(ps["ns"][i0:], dtype=np.float64)
                pa_, pb_, pres = line_fit(pk, pt)
                da, db, _ = line_fit(np.array(unwrap(ds["seq"], 256, 1), dtype=np.float64), np.array(ds["ns"], dtype=np.float64))
                ph = ((pt - da) / db) % 1.0
                ph_tick = (((pt - da) / db) * 6.0) % 1.0
                res["tap"]["priming"] = dict(
                    first_pdu_after_response_ms=round((ps["ns"][i0] - t_rsp) / 1e6, 3),
                    first_pdu_after_command_ms=round((ps["ns"][i0] - t_cmd) / 1e6, 3) if t_cmd is not None else None,
                    first_pdu_phase_us_mod_pdu=round(float(ph[0]) * 125.0, 3),
                    phase_us_mod_pdu=dict(p50=round(float(np.median(ph)) * 125.0, 3), p01=round(float(np.percentile(ph, 1)) * 125.0, 3),
                                          p99=round(float(np.percentile(ph, 99)) * 125.0, 3)),
                    first_pdu_phase_tick=round(float(ph_tick[0]), 4),
                    phase_tick=dict(p50=round(float(np.median(ph_tick)), 4), p01=round(float(np.percentile(ph_tick, 1)), 4),
                                    p99=round(float(np.percentile(ph_tick, 99)), 4)),
                    lateness_us=dict(p50=round(float(np.median(pres)) / 1e3, 3), p99=round(float(np.percentile(pres, 99)) / 1e3, 3),
                                     p999=round(float(np.percentile(pres, 99.9)) / 1e3, 3), max=round(float(pres.max()) / 1e3, 3),
                                     min=round(float(pres.min()) / 1e3, 3)))
                # every peer PDU later than LATE_US against the fit, in seconds from the bind's command
                late = np.nonzero(pres > LATE_US * 1e3)[0]
                res["tap"]["late_pdus"] = [dict(s=round((float(pt[i]) - t_cmd) / 1e9, 6), late_us=round(float(pres[i]) / 1e3, 3))
                                           for i in late] if t_cmd is not None else None
                # per slip: the largest lateness inside its interval, the bind's command as the common instant
                for x in pa["slips"]:
                    lo = t_cmd + x["s_lo"] * 1e9
                    hi = t_cmd + x["s_hi"] * 1e9
                    m = (pt >= lo) & (pt <= hi)
                    x["tap_lateness_max_us"] = round(float(pres[m].max()) / 1e3, 3) if m.any() else None
                    x["tap_pdus_in_interval"] = int(m.sum())
    windows = []
    if pa["first_poll_s"] < pa["unbind_s"]:
        windows.append((pa["first_poll_s"], pa["unbind_s"]))
    windows.append((0.0, pa["last_poll_s"]))
    res["classification"] = classify(pa["slips"], delta, windows)
    return res


# -------------------------------------------------------------------------------------------- control
def synth_pcap(path, t_cmd_s, peer_ppm, dut_ppm, late_at_s=None, late_us=30.0, drop_at_s=None, span_s=12.0):
    """A synthetic tap capture: the DUT's AAF and CRF talkers on port 3 throughout, the peer's AAF talker on port 2
    until an unbind 6 s before t_cmd_s and again from 2 ms after it, ACMP around both, jitter-free except one late PDU."""
    rng = np.random.default_rng(7)
    recs = []

    def add(t_ns, port, frame):
        recs.append((int(t_ns), port, frame))

    def eth(payload, vlan=True):
        h = bytes.fromhex("91e0f000fe01") + bytes.fromhex("020000000001")
        return h + (bytes.fromhex("8100600222f0") if vlan else bytes.fromhex("22f0")) + payload

    def aaf(sid, seq, ts):
        return eth(bytes([0x02, 0x81, seq & 0xFF, 0]) + sid + struct.pack(">I", ts & 0xFFFFFFFF) + bytes.fromhex("0205022001006000")[:4] + bytes(4 + 96))

    def crf(sid, seq, ts):
        return eth(bytes([0x04, 0x80, seq & 0xFF, 1]) + sid + struct.pack(">IHH", 48000, 48, 160) + struct.pack(">Q", ts) + bytes(40))

    def acmp(mt, cc=0):
        p = bytes([0xFC, mt, 0, 44]) + bytes(8) + bytes(8) + bytes.fromhex("0a0b0cfffe000000") + DUT_EID + bytes(4) + bytes(6) + struct.pack(">H", cc) + bytes(8)
        return eth(p, vlan=False)

    gptp0 = 1_000_000_000
    dur = int(span_s * FS / 6)
    sid_d, sid_c, sid_p = bytes.fromhex("0200000000010000"), bytes.fromhex("0200000000010001"), bytes.fromhex("0a0b0c0d0e0f0000")
    for k in range(dur):
        t = gptp0 + k * AAF_STEP_NS * (1 + dut_ppm * 1e-6)
        add(t + 3000, 3, aaf(sid_d, k, int(t + 2_000_000)))
    for k in range(int(span_s * 50)):
        t = gptp0 + k * 160 * 6 / 48000 * 1e9 * (1 + dut_ppm * 1e-6)
        add(t + 5000, 3, crf(sid_c, k, int(t + 2_000_000)))
    t_unb = gptp0 + (t_cmd_s - 6.0) * 1e9
    t_cmd = gptp0 + t_cmd_s * 1e9
    add(t_unb, 2, acmp(8))
    add(t_unb + 1e5, 3, acmp(9))
    add(t_cmd, 2, acmp(6))
    add(t_cmd + 5e5, 3, acmp(0))
    add(t_cmd + 1e6, 2, acmp(1, 1))
    add(t_cmd + 1.5e6, 3, acmp(7, 1))
    ph0 = 37_000.0
    for k in range(dur):
        t = gptp0 + ph0 + k * AAF_STEP_NS * (1 + peer_ppm * 1e-6)
        if t_unb < t < t_cmd + 2e6:
            continue
        if drop_at_s is not None and abs(t - (gptp0 + drop_at_s * 1e9)) < AAF_STEP_NS / 2:
            continue
        jit = rng.uniform(0, 200)
        if late_at_s is not None and abs(t - (gptp0 + late_at_s * 1e9)) < AAF_STEP_NS / 2:
            jit = late_us * 1e3
        add(t + jit, 2, aaf(sid_p, k, int(t + 2_000_000)))
    recs.sort()
    with open(path, "wb") as f:
        f.write(struct.pack("<IHHiIII", 0xA1B23C4D, 2, 4, 0, 0, 262144, 1))
        for t, port, frame in recs:
            pkt = struct.pack("<7I", 6, 0, port, 0, t & 0xFFFFFFFF, 0, 0) + frame
            f.write(struct.pack("<4I", t // 10**9 + 1_700_000_000, t % 10**9, len(pkt), len(pkt)) + pkt)
    return gptp0


def synth_cycle(cdir, t_bind, slips, missing_at=None, n_polls=84):
    cdir.mkdir(parents=True, exist_ok=True)
    t0 = t_bind - 8.0
    ev = [dict(kind="unbind", t_cmd_local=t_bind - 6.0, status=0), dict(kind="bind", t_cmd_local=t_bind, status=0),
          dict(kind="bind-time", t_bind_local=t_bind)]
    with open(cdir / "events.jsonl", "w") as f:
        for e in ev:
            f.write(json.dumps(e) + "\n")
    dups = 208
    with open(cdir / "poll.jsonl", "w") as f:
        for n in range(n_polls):
            a = t0 + 0.5 * n
            for s_at, d, sk in slips:
                if a - 0.5 < t_bind + s_at <= a:
                    dups += d
            words = {"0x8e0": "00000000", "0x8e4": "00000000", "0x8f8": "00000020", "0x8d4": f"{dups:08x}",
                     "0x8d8": "00000000", "0x8dc": f"{(0x100 if t_bind - 6.0 < a < t_bind + 0.3 else 0x20b):08x}",
                     "0x738": "00000000", "0x73c": "00000000", "0x748": "00000000"}
            if missing_at is not None and n == missing_at:
                words["0x8d4"] = None
            f.write(json.dumps(dict(n=n, t0=a, t1=a + 0.35, words=words, servo_state=0)) + "\n")


def control(out_path):
    import tempfile
    d = Path(tempfile.mkdtemp(prefix="b17ctl-"))
    results = []

    def check(name, cond, detail):
        results.append(dict(control=name, result="PASS" if cond else "FAIL", detail=detail))

    # 1. the poll: two planted slips and one unreadable poll
    synth_cycle(d / "c1", 1000.0, [(1.2, 2, 0), (3.1, 2, 0)], missing_at=50)
    pa = poll_analysis(jl(d / "c1" / "poll.jsonl"), 1000.0, 994.0)
    got = [(x["dups"], x["s_lo"] <= 1.2 <= x["s_hi"] or x["s_lo"] <= 3.1 <= x["s_hi"]) for x in pa["slips"]]
    check("poll: two planted dups found, each inside its interval", got == [(2, True), (2, True)], pa["slips"])
    check("poll: an unreadable SLIP_LB read is counted, not graded", pa["missing_reads"] == 1, pa["missing_reads"])
    check("poll: prefill exit after the bind", pa["render"]["prefill_exit_s"] is not None and 0 < pa["render"]["prefill_exit_s"] < 1.0,
          pa["render"]["prefill_exit_s"])
    # 2. the tap: a planted +5.92 ppm peer against a 0 ppm DUT, one lost PDU, one 30 us late PDU
    pc = d / "c2.pcap"
    synth_pcap(pc, 8.0, -5.92, 0.0, late_at_s=9.2, drop_at_s=10.0)
    synth_cycle(d / "c2", 2000.0, [(1.21, 2, 0)])
    r = cycle(d / "c2", str(pc))
    t = r["tap"]
    check("tap: peer rate recovered", abs(t["streams"]["peer-aaf"]["rate_ppm"] + 5.92) < 0.01, t["streams"]["peer-aaf"])
    check("tap: DUT AAF and CRF rates recovered", abs(t["streams"]["dut-aaf"]["rate_ppm"]) < 0.01 and abs(t["streams"]["dut-crf"]["rate_ppm"]) < 0.01,
          [t["streams"]["dut-aaf"]["rate_ppm"], t["streams"]["dut-crf"]["rate_ppm"]])
    check("tap: delta_ppm recovered", abs(t["delta_ppm"] + 5.92) < 0.01, t["delta_ppm"])
    check("tap: the lost PDU is a sequence gap, not a rate change", t["streams"]["peer-aaf"]["seq_gaps"] == 1, t["streams"]["peer-aaf"]["seq_gaps"])
    check("tap: first PDU after the bind's response", abs(t["priming"]["first_pdu_after_response_ms"] - 0.5) < 0.13, t["priming"])
    check("tap: the bind found on the tap clock, unbind to bind 6 s", abs(t["unbind_to_bind_tap_s"] - 6.0) < 1e-3, t.get("unbind_to_bind_tap_s"))
    sl = r["poll"]["slips"][0]
    lp = t.get("late_pdus") or []
    check("tap: the planted 30 us late PDU is the only PDU later than 10 us, at 1.2 s", len(lp) == 1 and abs(lp[0]["s"] - 1.2) < 1e-3 and lp[0]["late_us"] > 29.0, lp)
    check("tap: the planted 30 us late PDU found inside the slip's interval", sl.get("tap_lateness_max_us") is not None and sl["tap_lateness_max_us"] > 29.0,
          sl.get("tap_lateness_max_us"))
    # the phase, on a peer at the DUT's rate: arrivals 34 us after the DUT's transmit grid (37 us less its 3 us), plus 0 to 0.2 us
    pc0 = d / "c2b.pcap"
    synth_pcap(pc0, 8.0, 0.0, 0.0)
    synth_cycle(d / "c2b", 2500.0, [])
    t0 = cycle(d / "c2b", str(pc0))["tap"]
    check("tap: arrival phase against the DUT's grid, 34 us planted", abs(t0["priming"]["phase_us_mod_pdu"]["p50"] - 34.1) < 0.2,
          t0["priming"]["phase_us_mod_pdu"])
    check("tap: delta 0 at equal rates", abs(t0["delta_ppm"]) < 0.01, t0["delta_ppm"])
    # 3. classification: periodic dups at the rate interval with a slow peer -> (b); a lone dup with no offset -> (c)
    s_pred = 1 / (FS * 5.92e-6)
    synth_cycle(d / "c3", 3000.0, [(1.0 + s_pred * i, 2, 0) for i in range(9)])
    pa3 = poll_analysis(jl(d / "c3" / "poll.jsonl"), 3000.0, 2994.0)
    c3 = classify(pa3["slips"], -5.92, [(-8.0, -6.0), (0.0, 33.5)])
    check("classify: periodic dups at 1/(f_s x 5.92 ppm) with a slower peer are (b)", [x["cls"] for x in c3["slips"]] == ["b"] * 9,
          [x["cls"] for x in c3["slips"]])
    c3s = classify(pa3["slips"], +5.92, [(-8.0, -6.0), (0.0, 33.5)])
    check("classify: the same dups with a faster peer are (c)", all(x["cls"] == "c" for x in c3s["slips"]), [x["cls"] for x in c3s["slips"]])
    synth_cycle(d / "c4", 4000.0, [(0.8, 2, 0)])
    pa4 = poll_analysis(jl(d / "c4" / "poll.jsonl"), 4000.0, 3994.0)
    c4 = classify(pa4["slips"], 0.002, [(-8.0, -6.0), (0.0, 33.5)])
    check("classify: a lone dup at 0.002 ppm is (c)", [x["cls"] for x in c4["slips"]] == ["c"], c4)
    c5 = classify(pa4["slips"], -5.92, [(-8.0, -6.0), (0.0, 33.5)])
    check("classify: a lone dup where about 10 are expected is (c)", [x["cls"] for x in c5["slips"]] == ["c"], c5)
    out = dict(controls=results, passed=sum(1 for x in results if x["result"] == "PASS"), total=len(results))
    Path(out_path).write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(dict(passed=out["passed"], total=out["total"])))
    return 0 if out["passed"] == out["total"] else 1


if __name__ == "__main__":
    if sys.argv[1] == "control":
        sys.exit(control(sys.argv[2]))
    res = cycle(sys.argv[2], None if sys.argv[3] == "-" else sys.argv[3])
    Path(sys.argv[4]).write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps(dict(cycle=res["cycle"], slips=len(res["poll"]["slips"]), delta_ppm=res.get("tap", {}).get("delta_ppm"),
                          classes=[x["cls"] for x in res["classification"]["slips"]])))
