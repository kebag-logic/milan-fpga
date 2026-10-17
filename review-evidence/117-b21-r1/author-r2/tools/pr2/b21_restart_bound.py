#!/usr/bin/env python3
"""Lane B21 PR round 2: rebind to first valid output sample, per restart cycle (offline, read-only).

usage: b21_restart_bound.py <cycles.jsonl> <peer_link_pcap> <cap_lr_raw> <cap_ts_bin> <out_json>

Criterion: from the rebind (the CONNECT_RX command) to the first valid sample at the peer's output,
under 1 s, for every cycle.

Upper bound, on one clock: the bench host's CLOCK_REALTIME, which stamps both records below.
  start  restart_b21.py logs its "binding-rule" event after the format reads and before it writes the
         CONNECT_RX request to the controller agent, so the command leaves the controller after it.
  end    the external capture's reader stamps every read after it returns (cap-ts.bin: frames
         delivered after the read, realtime, monotonic). The first valid frame of a cycle's run was
         output by the peer before the read that delivered it returned.
  So rebind to first valid output sample < t(read delivering that frame) - t(binding-rule event).
  This holds for any output latency: the latency is inside the interval, not added to it. Host-side
  delays (the controller session, the capture's USB transfer and buffering, read stalls) can only
  make the bound larger.
Time base check: realtime minus monotonic over every read of the capture must stay within 1 ms, or
the tool refuses (a realtime step inside the run would break the single-clock argument).
Pairing: each cycle's binding-rule event must fall inside one captured silence, after the read that
delivered the silence's last valid frame and before the read that delivered the next first valid
frame; every first valid frame must start 480 valid frames in order.

Lower bound, on the peer-link tap's clock: the peer's received CONNECT_RX_COMMAND (ACMP message_type
6, tap port 2) to the tap time of the AAF packet (DUT STREAM_OUTPUT 0, port 2) that carries the frame
counter n of the cycle's first valid output frame (channel 0 word (1 << 16) | n), the first such packet
after the command. The tap is inline in front of the peer, and no frame is output before the peer
receives it. Also on the tap: command to response, command to the first AAF packet, and how many
frames the wire carried after the last frame the output played before the silence.

Verdict: PASS when all 20 cycles pair, every upper bound is under 1 s, every first valid frame starts
480 valid frames in order and every lower bound is at most its upper bound; FAIL otherwise (exit 1).
The true rebind-to-output time of a cycle lies between its two bounds.
"""
import json
import struct
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b21_aaf  # noqa: E402

SID = bytes.fromhex("0200000000010000")
FS, LIMIT_S, RT_MONO_TOL_S = 48000, 1.0, 1e-3


def tap(pcap):
    acmp, aaf, n0 = [], [], []
    for tap_ns, port, fr, _h in b21_aaf.records(pcap):
        a = b21_aaf.avtp(fr)
        if a is None or len(a) < 24:
            continue
        if a[0] == 0xFC and len(a) >= 56:
            acmp.append(dict(t=tap_ns, port=port, mt=a[1] & 0x0F, status=a[2] >> 3, seq=struct.unpack(">H", a[48:50])[0],
                             talker=a[20:28].hex(), listener=a[28:36].hex()))
        elif a[0] == 0x02 and a[4:12] == SID and port == 2:
            aaf.append(tap_ns)
            s0 = np.frombuffer(a[24:24 + 192], dtype=">u4").reshape(6, 8)[:, 0].astype(np.int64)
            n0.append(np.where((s0 >> 24) == 1, (s0 >> 8) & 0xFFFF, -1))
    return acmp, np.array(aaf, dtype=np.int64), np.array(n0, dtype=np.int64).reshape(-1, 6)


def main(cycles, pcap, cap_lr, cap_ts, out):
    ev = [json.loads(ln) for ln in open(cycles) if ln.startswith("{")]
    pre = {int(e["tag"].split("-")[1]): e["t"] for e in ev if e["kind"] == "binding-rule" and e["tag"].count("-") == 1}
    binds = [e for e in ev if e["kind"] == "bind"]
    retries = [e for e in ev if e["kind"] in ("bind-failed", "bind-retry")]
    # external capture
    b = np.fromfile(cap_lr, dtype=np.uint8)
    n = len(b) // 6
    w = b[:n * 6].reshape(n, 2, 3).astype(np.int64)
    w = w[:, :, 0] | (w[:, :, 1] << 8) | (w[:, :, 2] << 16)
    valid = ((w[:, 0] >> 16) == 1) & ((w[:, 1] >> 16) == 2) & ((w[:, 0] & 0xFFFF) == (w[:, 1] & 0xFFFF))
    nn = w[:, 0] & 0xFFFF
    idx = np.flatnonzero(valid)
    gaps = np.flatnonzero(np.diff(idx) > 2400)
    ts = np.fromfile(cap_ts, dtype=np.dtype([("f", "<i8"), ("rt", "<f8"), ("mono", "<i8")]))
    F, RT = ts["f"], ts["rt"]
    rm = RT - ts["mono"] / 1e9
    tb = dict(clock="bench host CLOCK_REALTIME", reads=int(len(ts)), realtime_minus_monotonic_range_s=float(rm.max() - rm.min()),
              tolerance_s=RT_MONO_TOL_S, capture_realtime=[float(RT[0]), float(RT[-1])])
    if rm.max() - rm.min() > RT_MONO_TOL_S:
        raise SystemExit(f"refused: realtime moved against monotonic by {rm.max() - rm.min():.6f} s inside the capture")

    def read_of(frame):
        r = int(np.searchsorted(F, frame + 1))
        return r if r < len(F) else None

    sil = []
    for g in gaps:
        a, b_ = int(idx[g]), int(idx[g + 1])
        run = valid[b_:b_ + 480].all() and bool(np.all(np.diff(nn[b_:b_ + 480]) % 65536 == 1))
        ra, rb = read_of(a), read_of(b_)
        sil.append(dict(last_valid=a, first_valid=b_, silence_frames=b_ - a - 1, first_480_valid_in_order=bool(run),
                        n_last=int(nn[a]), n_first=int(nn[b_]),
                        t_read_last_valid=float(RT[ra]) if ra is not None else None,
                        t_read_first_valid=float(RT[rb]) if rb is not None else None))
    # peer-link tap
    acmp, t_aaf, n_aaf = tap(pcap)
    cmd = [m for m in acmp if m["mt"] == 6 and m["port"] == 2]
    rsp = [m for m in acmp if m["mt"] == 7 and m["port"] == 3]
    dsc = [m for m in acmp if m["mt"] == 9 and m["port"] == 3]
    rows, ok = [], True
    for c in sorted(pre):
        t0 = pre[c]
        s = [x for x in sil if x["t_read_last_valid"] is not None and x["t_read_last_valid"] < t0
             and x["t_read_first_valid"] is not None and t0 < x["t_read_first_valid"]]
        row = dict(cycle=c, t_binding_rule=t0)
        if len(s) != 1:
            row.update(paired=False, upper_s=None, pass_=False)
            ok = False
            rows.append(row)
            continue
        s = s[0]
        up = s["t_read_first_valid"] - t0
        row.update(paired=True, silence_frames=s["silence_frames"], first_480_valid_in_order=s["first_480_valid_in_order"],
                   upper_s=round(up, 6))
        # the tap: the cycle's command is the first received CONNECT_RX_COMMAND after the cycle's
        # DISCONNECT_RX_RESPONSE (cycle order on the tap)
        if c - 1 < len(dsc):
            d = dsc[c - 1]["t"]
            cc = [m for m in cmd if m["t"] > d]
            rr = [m for m in rsp if m["t"] > d]
            if cc and rr:
                tc, tr = cc[0]["t"], rr[0]["t"]
                j = int(np.searchsorted(t_aaf, tr))
                k0 = int(np.searchsorted(t_aaf, tc))
                # the packet carrying the first output frame: first after the command, within 1 s
                win = np.flatnonzero((t_aaf[k0:] - tc) < int(1e9))[-1] + 1 if k0 < len(t_aaf) else 0
                hit = np.flatnonzero(np.any(n_aaf[k0:k0 + win] == s["n_first"], axis=1))
                # the wire after the last output frame: frames carried after it before the stop
                last = int(np.searchsorted(t_aaf, d + int(0.5e9))) - 1
                prior = n_aaf[max(0, last - 400):last + 1].ravel()
                prior = prior[prior >= 0]
                if j < len(t_aaf):
                    row.update(tap_command_to_response_s=round((tr - tc) / 1e9, 6),
                               tap_command_to_first_aaf_s=round((int(t_aaf[j]) - tc) / 1e9, 6))
                if len(hit):
                    kk = k0 + int(hit[0])
                    row.update(first_output_frame_packet_after_first_aaf=int(kk - j),
                               lower_s=round((int(t_aaf[kk]) - tc) / 1e9, 6))
                if len(prior):
                    row["wire_frames_after_last_output_frame"] = int((int(prior[-1]) - s["n_last"]) % 65536)
        # the two bounds come from different clocks; a lower bound above the upper one means a premise
        # failed, so such a cycle cannot pass
        row["bounds_consistent"] = bool(row.get("lower_s") is not None and row["lower_s"] <= up)
        row["pass_"] = bool(up < LIMIT_S and s["first_480_valid_in_order"] and row["bounds_consistent"])
        ok &= row["pass_"]
        rows.append(row)
    up = np.array([r["upper_s"] for r in rows if r.get("upper_s") is not None])
    lo = np.array([r["lower_s"] for r in rows if r.get("lower_s") is not None])
    res = dict(time_base=tb, cycles_logged=len(pre), binds_logged=len(binds), bind_retries=len(retries),
               captured_silences=len(sil), tap_connect_commands=len(cmd), tap_connect_responses=len(rsp),
               tap_disconnect_responses=len(dsc), limit_s=LIMIT_S,
               upper_s=dict(n=int(len(up)), min=float(up.min()), median=float(np.median(up)), max=float(up.max()),
                            under_limit=int((up < LIMIT_S).sum())) if len(up) else None,
               lower_s=dict(n=int(len(lo)), min=float(lo.min()), median=float(np.median(lo)), max=float(lo.max())) if len(lo) else None,
               verdict="PASS" if ok and len(rows) == 20 else "FAIL", cycles=rows)
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "cycles"}, indent=1))
    print("cycle  lower_ms  upper_ms  pass")
    for r in rows:
        lo_ = r.get("lower_s")
        print(f"{r['cycle']:5d}  {lo_ * 1e3 if lo_ is not None else float('nan'):8.1f}  "
              f"{r['upper_s'] * 1e3 if r.get('upper_s') is not None else float('nan'):8.1f}  {r['pass_']}")
    return 0 if res["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:6]))
