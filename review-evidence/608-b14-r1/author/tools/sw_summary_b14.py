#!/usr/bin/env python3
"""Lane B14 item 2: per-switch summary from sw_b14.py's records (read-only; nothing here touches the bench).

usage: sw_summary_b14.py <packet_dir>
Reads item2/cyc*/events.jsonl in the packet, each invocation's console poll
(/tmp/608-b14/raw/item2/<run>/poll.jsonl) and the tap summaries (/tmp/608-b14/raw/item2/tapsum/).
Writes item2/summary/switches.json (one row per INTERNAL->AAF and AAF->CRF switch, and per
CRF->INTERNAL return) and item2/summary/switches.tsv.

Per switch, from the 0.5 s console poll (times in seconds after the set's SET_CLOCK_SOURCE answer,
on this host's CLOCK_MONOTONIC_RAW; a poll interval (lo, hi) runs from the end of the poll before
to the end of the poll that saw the change):
  * set to LOCKED: the first poll reading MCSRV_STAT state 4;
  * settle boundary: LOCKED (hi) + 4.096 s (8 servo windows, MEDIA_CLOCK_FOLLOWING.md
    "Settle recentre") + 0.5 s for the poll and the deciding PDU;
  * SLIP_LB and SLIP_TDM dups and skips before the set, at the boundary and at the hold's end:
    the transient delta (set to boundary, declared as part of the switch) and the after delta
    (boundary to hold end, which must be zero); every SLIP_LB step's time, and whether it falls
    within 0.5 s of the boundary (not separable at this poll period);
  * RENDER_STAT: rails (any change is a finding), converged-bit drops (polls reading 0) and their
    times; prefill;
  * AAF meter restarts; CRF sink lock bit.
From the GET_COUNTERS marks (before, locked, settled, mid, end): deltas from `before` to `end` and
from `locked` to `end` for every decoded counter (b7_decode.CTR_NAMES).
From the tap: per stream PDUs, sequence gaps, mr toggles, tv=0, tu=1, presentation-time steps off
the mode by more than 1 us.
"""
import json
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b7_decode as X  # noqa: E402

pk = Path(sys.argv[1])
RAW = Path("/tmp/608-b14/raw/item2")
SETTLE_S = 4.096
MARGIN_S = 0.5
NAMES = {"dut-0x0024-0": 0x0024, "dut-0x0006-0": 0x0006, "dut-0x0006-1": 0x0006, "peer-0x0005-0": 0x0005,
         "dut-0x0005-0": 0x0005, "dut-0x0005-1": 0x0005, "dut-0x0009-0": 0x0009, "peer-0x0006-0": 0x0006,
         "peer-0x0006-2": 0x0006}


def load(p):
    return [json.loads(l) for l in open(p) if l.startswith("{")]


def dec(w):
    try:
        sv = X.servo(w["0x8f8"])
        m = X.meter(w["0x8e0"], w["0x8e4"])
        lb, td, rs = int(w["0x8d4"], 16), int(w["0x8d8"], 16), int(w["0x8dc"], 16)
        return dict(servo=sv["state"], trim=sv["trim_ppm"], lb=(lb & 0xFFFF, lb >> 16), tdm=(td & 0xFFFF, td >> 16),
                    fill=rs & 0xFF, prefill=rs >> 8 & 1, conv=rs >> 9 & 1, rails=rs >> 16, mrst=m["restarts"],
                    mlock=m["locked"], crf=int(w["0x738"], 16) >> 31)
    except (KeyError, TypeError, ValueError):
        return None


def ctr(payload, dt):
    if not isinstance(payload, str):
        return None
    b = bytes.fromhex(payload)
    mask = int.from_bytes(b[4:8], "big")
    v = struct.unpack(">32I", b[8:136])
    return {X.CTR_NAMES.get(dt, {}).get(i, str(i)): v[i] for i in range(32) if mask >> i & 1}


def delta(a, b):
    if a is None or b is None:
        return None
    return {k: b[k] - a.get(k, 0) for k in b if b[k] != a.get(k, 0)}


rows = []
for run in sorted(pk.glob("item2/cyc*/events.jsonl")):
    name = run.parent.name
    ev = load(run)
    polls = load(RAW / name / "poll.jsonl")
    dp = [(p, dec(p["words"])) for p in polls]
    sw = [e for e in ev if e["kind"] == "switch"]
    marks = {e["tag"]: e for e in ev if e["kind"] == "counters"}
    sets = {e["tag"]: e for e in ev if e["kind"] == "set-clock"}
    locks = {e["tag"]: e for e in ev if e["kind"] == "servo-state"}
    ends = {e["tag"]: e for e in ev if e["kind"] == "phase-end"}
    caps = {e["file"]: e for e in ev if e["kind"] == "capture-end"}
    for e in sw:
        tag = e["tag"]
        t_set = sets[tag]["mono_raw_ns"]
        t_end = ends[tag]["mono_raw_ns"]
        lk = locks.get(tag, {})
        if e["src"]:
            bound = t_set + int(((lk.get("s_hi") or 0) + SETTLE_S + MARGIN_S) * 1e9)
        else:
            bound = t_set + int(MARGIN_S * 1e9)
        before = next((d for p, d in reversed(dp) if p["raw1"] <= e["mono_raw_ns"] and d), None)
        inside = [(p, d) for p, d in dp if d and t_set <= p["raw0"] and p["raw1"] <= t_end]
        at_b = next((d for p, d in reversed(inside) if p["raw1"] <= bound), before)
        at_e = inside[-1][1] if inside else None
        steps, prev = [], before
        bad = sum(1 for p, d in dp if d is None and t_set <= p["raw0"] and p["raw1"] <= t_end)
        conv0 = []
        for p, d in inside:
            if prev and d["lb"] != prev["lb"]:
                s = (p["raw1"] - t_set) / 1e9
                steps.append(dict(s_hi=round(s, 3), lb=list(d["lb"]), near_boundary=abs(p["raw1"] - bound) < MARGIN_S * 1e9,
                                  after_boundary=p["raw1"] > bound))
            if d["conv"] == 0:
                conv0.append(round((p["raw1"] - t_set) / 1e9, 3))
            prev = d
        c = lambda t: {k: ctr(v, NAMES[k]) for k, v in (marks.get(f"{tag}-{t}", {}).get("payloads") or {}).items()}
        cb, cl, ce = c("before"), c("locked"), c("end")
        tap = {}
        for f, ce_ in caps.items():
            if f == f"608-b14-sw-{tag}.pcap":
                tp = RAW / "tapsum" / f.replace(".pcap", ".json")
                if tp.exists():
                    d = json.load(open(tp))
                    for s in d["streams"]:
                        who = ("dut" if s["port"] == 3 else "peer") + ("-aaf" if s["subtype"] == "0x2" else "-crf")
                        tap[who] = dict(pdus=s["n"], seq_gaps=s["seq_gap_count"], mr_toggles_s=[x["t"] for x in s["mr_toggles"]],
                                        tv0=s["tv0"], tu1=s["tu1"], max_gap_ms=round(s["max_gap_s"] * 1e3, 3),
                                        ts_steps_off_mode_gt_1us=s["ts_steps_off_mode_gt_1us_total"], ts_step_range_ns=s["ts_step_min_max_ns"])
                tap["capture"] = dict(file=f, bytes=ce_.get("bytes"), sha256=ce_.get("sha256"), summary=ce_.get("summary"),
                                      removed_from_tap=ce_.get("removed_from_tap"))
        row = dict(run=name, tag=tag, to_source=e["src"], set_status=sets[tag]["status"], readback=sets[tag]["readback"],
                   locked_s=[lk.get("s_lo"), lk.get("s_hi")] if e["src"] else None,
                   idle_s=[lk.get("s_lo"), lk.get("s_hi")] if not e["src"] else None,
                   settle_boundary_s=round((bound - t_set) / 1e9, 3), hold_end_s=round((t_end - t_set) / 1e9, 3),
                   slip_lb_before=list(before["lb"]) if before else None, slip_lb_boundary=list(at_b["lb"]) if at_b else None,
                   slip_lb_end=list(at_e["lb"]) if at_e else None,
                   slip_lb_transient_dups=(at_b["lb"][0] - before["lb"][0]) if at_b and before else None,
                   slip_lb_after_dups=(at_e["lb"][0] - at_b["lb"][0]) if at_e and at_b else None,
                   slip_lb_after_skips=(at_e["lb"][1] - at_b["lb"][1]) if at_e and at_b else None,
                   slip_lb_steps=steps,
                   slip_tdm_before_end=[list(before["tdm"]) if before else None, list(at_e["tdm"]) if at_e else None],
                   rails_before_end=[before["rails"] if before else None, at_e["rails"] if at_e else None],
                   converged_zero_polls_s=conv0, meter_restarts_before_end=[before["mrst"] if before else None, at_e["mrst"] if at_e else None],
                   servo_end=at_e["servo"] if at_e else None, trim_end_ppm=at_e["trim"] if at_e else None,
                   polls=len(inside), bad_polls=bad,
                   counters_before_to_end=({k: delta(cb.get(k), ce.get(k)) for k in ce} if cb and ce else None),
                   counters_locked_to_end=({k: delta(cl.get(k), ce.get(k)) for k in ce} if cl and ce else None),
                   tap=tap)
        rows.append(row)
out = pk / "item2" / "summary"
out.mkdir(parents=True, exist_ok=True)
(out / "switches.json").write_text(json.dumps(rows, indent=1) + "\n")
with open(out / "switches.tsv", "w") as f:
    f.write("tag\tto\tlocked_s\tslip_lb_transient_dups\tslip_lb_after_dups\tslip_lb_after_skips\tsteps_s\tslip_tdm\trails\tconv0_s\tmeter_restarts\t"
            "dut_in0_MEDIA_UNLOCKED_locked_to_end\tdut_in1_MEDIA_UNLOCKED_locked_to_end\tdut_cd_LOCKED_UNLOCKED\tdut_out0_MEDIA_RESET\ttap_gaps\ttap_dut_mr\n")
    for r in rows:
        le = r["counters_locked_to_end"] or {}
        be = r["counters_before_to_end"] or {}
        g = sum(v.get("seq_gaps", 0) for k, v in r["tap"].items() if k != "capture")
        mr = [len(r["tap"].get(k, {}).get("mr_toggles_s", [])) for k in ("dut-aaf", "dut-crf")] if r["tap"] else None
        f.write("\t".join(str(x) for x in (
            r["tag"], r["to_source"], r["locked_s"], r["slip_lb_transient_dups"], r["slip_lb_after_dups"], r["slip_lb_after_skips"],
            [s["s_hi"] for s in r["slip_lb_steps"]], r["slip_tdm_before_end"], r["rails_before_end"], r["converged_zero_polls_s"],
            r["meter_restarts_before_end"],
            (le.get("dut-0x0005-0") or {}).get("MEDIA_UNLOCKED", 0), (le.get("dut-0x0005-1") or {}).get("MEDIA_UNLOCKED", 0),
            [(be.get("dut-0x0024-0") or {}).get("LOCKED", 0), (be.get("dut-0x0024-0") or {}).get("UNLOCKED", 0)],
            (be.get("dut-0x0006-0") or {}).get("MEDIA_RESET", 0), g if r["tap"] else None, mr)) + "\n")
print(json.dumps(dict(switches=len(rows)), indent=0))
