#!/usr/bin/env python3
"""Lane B17: the lane's per-cycle table and summary from the graded cycles (offline, read-only).

usage: summ_b17.py <packet_dir>
Reads cycles/cNN/events.jsonl and summary/cNN.json (ana_b17.py), writes summary/cycles.json, summary/table.md
and summary/counter-logs.sha256 (the SHA-256 of each cycle's raw counter log, cycles/cNN/poll.jsonl).
Late bursts: the peer PDUs later than 20 us against the post-bind fit (ana_b17.py's late_pdus), grouped into one
burst while consecutive PDUs are less than 1 ms apart; a burst's time is its first PDU's, its peak its largest
lateness.
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

P = Path(sys.argv[1])
BURST_US, BURST_GAP_S = 20.0, 1e-3


def jl(path):
    return [json.loads(x) for x in open(path) if x.startswith("{")]


def bursts(late):
    out = []
    for x in late:
        if x["late_us"] <= BURST_US:
            continue
        if out and x["s"] - out[-1]["last_s"] < BURST_GAP_S:
            out[-1]["last_s"] = x["s"]
            out[-1]["peak_us"] = max(out[-1]["peak_us"], x["late_us"])
            out[-1]["pdus"] += 1
        else:
            out.append(dict(s=x["s"], last_s=x["s"], peak_us=x["late_us"], pdus=1))
    return out


rows, logs = [], []
for cdir in sorted((P / "cycles").glob("c[0-9][0-9]")):
    c = cdir.name
    ev = jl(cdir / "events.jsonl")
    r = json.load(open(P / "summary" / f"{c}.json"))
    k = {e["kind"]: e for e in ev}
    po, tap, cl = r["poll"], r["tap"], r["classification"]
    log_sha = hashlib.sha256((cdir / "poll.jsonl").read_bytes()).hexdigest()
    logs.append(f"{log_sha}  cycles/{c}/poll.jsonl")
    b = bursts(tap.get("late_pdus") or [])
    slips = []
    for x, y in zip(po["slips"], cl["slips"]):
        inside = [z for z in b if x["s_lo"] <= z["s"] <= x["s_hi"]]
        before = [z for z in (tap.get("late_pdus") or []) if z["s"] < x["s_lo"]]
        after = [z for z in b if z["s"] > x["s_hi"]]
        slips.append(dict(word=x["word"], s_lo=x["s_lo"], s_hi=x["s_hi"], dups=x["dups"], skips=x["skips"], frames=x["dups"] // 2 if not x["skips"] else None,
                          after=x["after"], cls=y["cls"], basis=y["basis"], lateness_max_in_interval_us=x.get("tap_lateness_max_us"),
                          first_burst_in_interval=bool(b) and b[0] in inside,
                          lateness_max_before_interval_us=max((z["late_us"] for z in before), default=None),
                          bursts_after_interval=len(after), burst_peak_after_interval_us=max((z["peak_us"] for z in after), default=None)))
    cap = k["capture-end"]
    pr = tap.get("priming", {})
    rows.append(dict(
        cycle=c, tool_sha256=k["start"]["tool_sha256"], poller_sha256=k["start"]["poller_sha256"],
        bind_utc=datetime.fromtimestamp(r["bind_local"], timezone.utc).strftime("%H:%M:%S.%f")[:-3],
        unbind_to_bind_s=round(r["bind_local"] - r["unbind_local"], 3), unbind_status=r["unbind_status"], bind_status=r["bind_status"],
        format_check=[dict(talker_fmt=f["talker_fmt"], listener_fmt=f["listener_fmt"], set=f["set"]) for f in r["format_check"]],
        states=r["states"], polls=po["polls"], first_poll_s=po["first_poll_s"], last_poll_s=po["last_poll_s"],
        poll_spacing_s=po["poll_spacing_s"], missing_reads=po["missing_reads"],
        slip_lb_start=po["slip_lb_first"], slip_lb_end=po["slip_lb_last"], slip_tdm_changes=len(po["slip_tdm_changes"]),
        servo_states=po["servo_states"], aafm_stat_values=po["aafm_stat_values"],
        settle_boundary="undefined: no poll read LOCKED (MCSRV_STAT state IDLE throughout)" if po["servo_states"] == [0] else "check",
        render=po["render"], slips=slips, rates_ppm={n: v["rate_ppm"] for n, v in tap["streams"].items()},
        seq_gaps={n: v["seq_gaps"] for n, v in tap["streams"].items()}, delta_ppm=tap.get("delta_ppm"),
        delta_vs_dut_crf_ppm=tap.get("delta_vs_dut_crf_ppm"), rate_interval_s=cl["rate_interval_s"], bound_window_s=cl["bound_window_s"],
        first_pdu_after_bind_ms=pr.get("first_pdu_after_command_ms"), phase_us_mod_pdu=pr.get("phase_us_mod_pdu"),
        phase_tick=pr.get("phase_tick"), lateness_us=pr.get("lateness_us"), late_bursts=len(b),
        late_burst_times_s=[round(z["s"], 3) for z in b], capture=dict(file=cap["file"], bytes=cap["bytes"], sha256=cap["sha256"],
                                                                         summary=cap["summary"], removed_from_tap=cap["removed_from_tap"]),
        ended_bound_as_found=k["cycle-check"]["bound_as_found"], clk_dut_end=k["cycle-check"]["clk_dut_end"]))

(P / "summary" / "counter-logs.sha256").write_text("\n".join(logs) + "\n")
digest = hashlib.sha256((P / "summary" / "counter-logs.sha256").read_bytes()).hexdigest()
all_slips = [s for r in rows for s in r["slips"]]
lane = dict(cycles=len(rows), slips=len(all_slips), classes={k: sum(1 for s in all_slips if s["cls"] == k) for k in ("a", "b", "c")},
            slip_lb=[rows[0]["slip_lb_start"], rows[-1]["slip_lb_end"]],
            delta_ppm_range=[min(r["delta_ppm"] for r in rows), max(r["delta_ppm"] for r in rows)],
            dut_aaf_vs_gptp_ppm_range=[min(r["rates_ppm"]["dut-aaf"] for r in rows), max(r["rates_ppm"]["dut-aaf"] for r in rows)],
            slip_interval_range_s=[min(s["s_lo"] for s in all_slips), max(s["s_hi"] for s in all_slips)] if all_slips else None,
            first_burst_in_slip_interval=sum(1 for s in all_slips if s["first_burst_in_interval"]),
            counter_logs_manifest_sha256=digest, poller_sha256=sorted({r["poller_sha256"] for r in rows}),
            tool_sha256=sorted({r["tool_sha256"] for r in rows}))
(P / "summary" / "cycles.json").write_text(json.dumps(dict(lane=lane, cycles=rows), indent=1) + "\n")

md = ["| Cycle | Bind, UTC | Settle boundary | Polls, s from the bind | `SLIP_LB` dups | Slip: s from the bind, count | Before or after | Class | delta_ppm, rate interval | Largest lateness in the slip's interval |",
      "|---|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    for s in r["slips"] or [None]:
        md.append("| {c} | {b} | Undefined (servo IDLE) | {n}, {f:+.2f} to {l:+.2f} | {a} to {e} | {sl} | {ba} | {cl} | {d:+.4f}, {ri:,.0f} s | {lt} |".format(
            c=r["cycle"], b=r["bind_utc"], n=r["polls"], f=r["first_poll_s"], l=r["last_poll_s"], a=r["slip_lb_start"]["dups"],
            e=r["slip_lb_end"]["dups"], sl=f"{s['s_lo']:.2f} to {s['s_hi']:.2f}, +{s['dups']} dups, {s['skips']} skips" if s else "none",
            ba="No boundary" if s else "-", cl=f"({s['cls']})" if s else "-", d=r["delta_ppm"], ri=r["rate_interval_s"],
            lt=f"{s['lateness_max_in_interval_us']:.1f} us" if s else "-"))
(P / "summary" / "table.md").write_text("\n".join(md) + "\n")
print(json.dumps(lane, indent=1))
