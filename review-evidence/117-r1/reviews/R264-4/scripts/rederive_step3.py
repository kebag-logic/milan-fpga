#!/usr/bin/env python3
"""Independent re-derivation of the #117 step 3 facts from the raw A202
console transcripts, power-strip logs, clock-offset records and tap captures.
It reuses none of the packet's analysis scripts.

usage: rederive_step3.py <bench-a202 root>

Clocks: console samples carry build-box UTC; power-strip, capture-server and
controller-host times are NTP. Build-box time = NTP time - offset, with the
offset taken from each cycle's clock-before.jsonl (median of best 5). Tap
records carry a 32-bit nanosecond word; it is unwrapped against the capture
host's pcap time and placed on that clock by a least-squares line through the
per-5 s minima of (host time - tap time).
"""
import json
import os
import re
import struct
import sys
from datetime import datetime, timezone

SWITCH_CLK = "3cc0c6fffefe0210"
DUT_CLK = "020000fffe000001"
GM_SELF = DUT_CLK


def ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc).timestamp()


def offsets(path):
    o = {}
    for line in open(path):
        j = json.loads(line)
        o[j["host"].split(">")[-1]] = j["offset_s_median_best5"]
    return o


def console(path):
    """Samples: dicts with t, status fields, and the mem_read words that follow."""
    txt = open(path, encoding="utf-8", errors="replace").read()
    blocks = re.split(r"^### ", txt, flags=re.M)[1:]
    samples, cmds = [], []
    cur = None
    for b in blocks:
        m = re.match(r"(\S+) cmd='([^']*)'", b)
        if not m:
            continue
        t, cmd = ts(m.group(1)), m.group(2)
        cmds.append(cmd.split()[0] if cmd else "")
        if cmd == "milan_status":
            f = dict(re.findall(r"(\w+)=(\S+)", b))
            if "CLKV_STAT" not in f:
                continue
            cur = {"t": t, **f}
            samples.append(cur)
        elif cmd.startswith("mem_read") and cur is not None:
            addr = int(cmd.split()[1], 16)
            mm = re.search(r"0x%08x\s+((?:[0-9a-f]{2} ){4})" % addr, b)
            if mm:
                cur[hex(addr & 0xFFF)] = int.from_bytes(bytes.fromhex(mm.group(1).replace(" ", "")), "little")
    return samples, cmds


def ptp_records(path):
    d = open(path, "rb").read()
    off = 24
    recs = []
    while off + 16 <= len(d):
        s, us, incl, _ = struct.unpack("<IIII", d[off:off + 16])
        off += 16
        pkt = d[off:off + incl]
        off += incl
        if len(pkt) < 28:
            continue
        typ, _blk, port, _hi, lo, cap, orig = struct.unpack("<7I", pkt[:28])
        if typ != 6 or cap != orig or 28 + cap > len(pkt):
            continue
        recs.append((s + us * 1e-6, lo, port, pkt[28:28 + cap]))
    # unwrap the tap nanosecond word against host time
    out = []
    k = None
    for host, lo, port, fr in recs:
        if k is None:
            k = round((host * 1e9 - lo) / 2**32)
        pred = None
        cand = lo + k * 2**32
        # choose the wrap count nearest to host time given the running offset
        if out:
            last_host, last_tap = out[-1][0], out[-1][1]
            exp = last_tap + (host - last_host) * 1e9
            k = round((exp - lo) / 2**32)
            cand = lo + k * 2**32
        out.append((host, cand, port, fr))
    # line through per-5 s minima of host - tap
    if not out:
        return []
    t0 = out[0][0]
    bins = {}
    for host, tap, _, _ in out:
        b = int((host - t0) // 5)
        v = host - tap * 1e-9
        if b not in bins or v < bins[b][1]:
            bins[b] = (tap * 1e-9, v)
    xs = [x for x, _ in bins.values()]
    ys = [y for _, y in bins.values()]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs) or 1.0
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    icpt = my - slope * mx
    res = []
    for host, tap, port, fr in out:
        ts_ = tap * 1e-9
        res.append((ts_ + icpt + slope * ts_, port, fr))
    return res


def ptp_msgs(recs):
    """(t_server, direction, msgtype, src clock, extra) for gPTP frames."""
    out = []
    for t, port, fr in recs:
        if len(fr) < 14:
            continue
        et = struct.unpack(">H", fr[12:14])[0]
        off = 14
        if et == 0x8100:
            et = struct.unpack(">H", fr[16:18])[0]
            off = 18
        if et != 0x88F7:
            out.append((t, port, "other", fr[6:12].hex(), None))
            continue
        p = fr[off:]
        mt = p[0] & 0xF
        src = p[20:28].hex()
        extra = None
        if mt == 0xB and len(p) >= 61:
            extra = {"prio1": p[47], "gm": p[53:61].hex()}
        out.append((t, port, mt, src, extra))
    return out


def main():
    root = sys.argv[1]
    summary = []
    allcmds = {}
    for c in range(1, 7):
        d = os.path.join(root, "bench", f"cycle{c}")
        off = offsets(os.path.join(d, "clock-before.jsonl"))
        ps = open(os.path.join(d, "powerstrip.txt")).read()
        t_off_ntp = float(re.search(r"T_OFF_CMD (\S+)", ps).group(1))
        t_on_ntp = float(re.search(r"T_ON_CMD (\S+)", ps).group(1))
        pi = [v for k, v in off.items() if k == "pi"][0]
        srv = [v for k, v in off.items() if k.startswith("ubuntu")][0]
        t0 = t_off_ntp - pi  # build-box time of the off command
        samples, cmds = console(os.path.join(d, "console.txt"))
        for x in cmds:
            allcmds[x] = allcmds.get(x, 0) + 1
        S = []
        for s in samples:
            st = int(s["CLKV_STAT"], 16)
            S.append({
                "t": s["t"] - t0, "gm": s["GPTP_GM"], "par": s["GPTP_PARENT"],
                "tu": st & 1, "sync": (st >> 1) & 1, "hold": (st >> 3) & 1, "asc": (st >> 16) & 1,
                "pd": int(s["PDELAY_NS"]), "gen": int(s["AS_PATH_GEN"]), "cnt": int(s["AS_PATH_COUNT"]),
                "tucnt": s.get("0x780"), "linkg": s.get("0x774"), "epoch": s.get("0x720"),
            })
        gaps = max(b["t"] - a["t"] for a, b in zip(S, S[1:]))
        first = lambda pred, after=0.0: next((x for x in S if x["t"] > after and pred(x)), None)
        s_sync0 = first(lambda x: x["sync"] == 0)
        s_gmself = first(lambda x: x["gm"] == GM_SELF)
        s_asc0 = first(lambda x: x["asc"] == 0)
        # holdover runs
        def run_from(i0):
            i = i0
            while i < len(S) and S[i]["hold"]:
                i += 1
            return i - i0, (S[i]["t"] - S[i0]["t"]) if i < len(S) else None
        idx = {id(x): i for i, x in enumerate(S)}
        i_h1 = next(i for i, x in enumerate(S) if x["t"] > 0 and x["hold"])
        h1 = run_from(i_h1)
        i_g = idx[id(s_gmself)]
        h2 = run_from(i_g) if S[i_g]["hold"] else (0, None)
        # return
        t_back = 30.0
        s_asc1 = first(lambda x: x["asc"] == 1, t_back)
        s_gmsw = first(lambda x: x["gm"] == SWITCH_CLK, t_back)
        i_gmsw = idx[id(s_gmsw)]
        h3 = run_from(i_gmsw) if S[i_gmsw]["hold"] else (0, None)
        good = lambda x: x["gm"] == SWITCH_CLK and x["sync"] and x["asc"] and not x["tu"]
        i_ag = len(S)
        while i_ag > 0 and good(S[i_ag - 1]):
            i_ag -= 1
        s_ag = S[i_ag]
        s_tu0 = first(lambda x: x["tu"] == 0, s_gmsw["t"] - 0.001)
        tucnt = [x["tucnt"] for x in S if x["tucnt"] is not None]
        epochs = sorted({x["epoch"] for x in S if x["epoch"] is not None})
        linkg = [(round(x["t"], 2), x["linkg"]) for x in S if x["linkg"] is not None]
        lg_drop = next((t for t, v in linkg if t > 0 and v == 0x03), None)
        lg_back = next((t for t, v in linkg if lg_drop and t > lg_drop and v == 0x83), None)
        pd_ret = [x["pd"] for x in S if x["t"] >= s_asc1["t"] and x["t"] < s_asc1["t"] + 0.05]
        # wire
        recs = ptp_records(os.path.join(d, f"tap-c{c}.pcap"))
        W = [(t - srv - t0, port, mt, src, ex) for t, port, mt, src, ex in ptp_msgs(recs)]
        sw = [w for w in W if w[1] == 2]
        dut = [w for w in W if w[1] == 3]
        last_sw = max(w[0] for w in sw if w[0] < 20)
        last_sync = max(w[0] for w in sw if w[0] < 20 and w[2] == 0)
        last_ann = max(w[0] for w in sw if w[0] < 20 and w[2] == 0xB)
        first_sw = min(w[0] for w in sw if w[0] > 20)
        first_ann = min(w[0] for w in sw if w[0] > 20 and w[2] == 0xB)
        first_syn = min(w[0] for w in sw if w[0] > 20 and w[2] == 0)
        last_dut = max(w[0] for w in dut if w[0] < 20)
        first_dut = min(w[0] for w in dut if w[0] > 20)
        ann_ok = [w for w in sw if w[0] > 20 and w[2] == 0xB][:1]
        dut_sync_master = [w for w in dut if w[0] > 20 and w[2] == 0 and w[0] < s_gmsw["t"] + 0.2]
        dut_ann = [w for w in dut if w[0] > 20 and w[2] == 0xB]
        silent = [w[0] for w in W if 1.0 < w[0] < 37.0]
        rec = s_ag["t"] - min(first_ann, first_syn)
        row = {
            "cycle": c,
            "off_for_s": round(t_on_ntp - t_off_ntp, 2),
            "console_samples": len(S), "max_gap_s": round(gaps, 3),
            "sync0": round(s_sync0["t"], 2), "sync0_minus_last_sync": round(s_sync0["t"] - last_sync, 2),
            "hold_loss_samples": h1[0], "hold_loss_first_set_to_first_clear_s": round(h1[1], 2) if h1[1] else None,
            "gm_self": round(s_gmself["t"], 2), "gm_self_minus_last_announce": round(s_gmself["t"] - last_ann, 2),
            "hold_at_identity_change_samples": h2[0], "hold_at_identity_change_s": round(h2[1], 2) if h2[1] else None,
            "par_follows": s_gmself["par"] == GM_SELF, "gen_step": s_gmself["gen"] - S[0]["gen"], "cnt": s_gmself["cnt"],
            "asc0": round(s_asc0["t"], 2),
            "switch_last_frame": round(last_sw, 2), "dut_last_frame": round(last_dut, 2),
            "wire_silent_frames_1_to_37s": len(silent),
            "switch_first_frame": round(first_sw, 2), "switch_first_announce": round(first_ann, 2),
            "first_announce_prio1": ann_ok[0][4]["prio1"] if ann_ok and ann_ok[0][4] else None,
            "switch_first_sync_minus_announce_ms": round((first_syn - first_ann) * 1e3, 1),
            "dut_first_frame": round(first_dut, 2),
            "asc1": round(s_asc1["t"], 2), "pdelay_at_asc1": pd_ret,
            "gm_switch": round(s_gmsw["t"], 2), "hold_at_adoption_samples": h3[0],
            "tu_clear": round(s_tu0["t"], 2), "tu_clear_minus_adoption": round(s_tu0["t"] - s_gmsw["t"], 2),
            "all_good": round(s_ag["t"], 2), "recovery_s": round(rec, 2),
            "dut_master_syncs_before_adoption": len(dut_sync_master),
            "dut_announces_after_return": [(round(w[0], 2), w[4]["prio1"] if w[4] else None, (w[4] or {}).get("gm") == DUT_CLK) for w in dut_ann],
            "tucnt_delta": (tucnt[-1] - tucnt[0]) if tucnt else None,
            "rst_epoch_values": epochs, "linkg_drop": lg_drop, "linkg_drop_minus_last_rx": round(lg_drop - max(last_sw, last_dut), 2) if lg_drop else None,
            "linkg_back": lg_back,
        }
        summary.append(row)
        print(json.dumps(row))
    print("console command census (A202 cycles only):", json.dumps(allcmds, sort_keys=True))


if __name__ == "__main__":
    main()
