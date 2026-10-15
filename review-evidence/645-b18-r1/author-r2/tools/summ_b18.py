#!/usr/bin/env python3
"""Lane B18 (#645 acceptance after PR #742): the per-cycle grade, the comparison with lane B17 and the summary
(offline, read-only).

usage: summ_b18.py <packet_dir> <b17_packet_dir>
Reads, in the B18 packet: cycles/cNN/events.jsonl (cyc_b18.py), the raw counter logs cycles/cNN/poll.jsonl
(console_poll_b8.py), summary/cNN.json (ana_b17.py, unchanged) and restore/dut-{start,end}.txt. Reads, in the
B17 packet: summary/cNN.json and cycles/cNN/events.jsonl. Writes summary/cycles.json, summary/table.md,
summary/compare.md, summary/counters.md and summary/counter-logs.sha256. Exits 1 on any failed consistency check.

Rules (lane B17's summ_b17.py, round 3, where they apply):
  * Every poll figure is computed here from the raw counter log and the bind's instant and rounded once when
    printed. A change of a word is timed from the start of the poll before it to the end of the poll that saw it.
    A time of day is a clock reading, truncated to the millisecond.
  * A tap figure the grade already rounded is printed at fewer decimals only where no rounding tie makes it
    depend on the dropped digits; a tie stops the tool.
  * Late bursts: B17's rule, unchanged. Peer PDUs more than 20 us late against the post-bind fit (ana_b17.py's
    late_pdus), grouped while successive qualifying PDUs are less than 1 ms apart; a burst's time is its first
    PDU's, its peak its largest lateness. "To the last poll" counts bursts that start no later than the end of
    the cycle's last poll; the counter is read only to there, and later bursts rest on the cumulative counter
    (each cycle's first SLIP_LB read equals the previous cycle's last; c01's first equals the start baseline,
    c10's last the end baseline).
Grade per cycle, against #742's stated behaviour (the B18 assignment, item 3):
  * held: SLIP_LB does not change across the cycle's polls;
  * #743 residual: one +1 dup, no skip, whose poll interval contains the first peer PDU after the bind and
    ends no later than the first PDU more than 20 us late (the poll cannot resolve the 3 ms the assignment names;
    stated in TAKEN);
  * B17's class (c): one +2 dup slip, no skip, whose interval holds a late burst; recorded with its time and
    the largest lateness inside the interval;
  * anything else: not held, reported as read.
The arm's firing time is the design's figure (2,048 ticks, 42.7 ms after the first PDU); no CSR on this image
exposes the recentre count, so it is printed as the design's, not as observed.
"""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path

P, B17 = Path(sys.argv[1]), Path(sys.argv[2])
BURST_US, BURST_GAP_S, FS = 20.0, 1e-3, 48_000
ARM_MS = 2048 / FS * 1e3
CYCLES = [f"c{i:02d}" for i in range(1, 11)]
ROUNDING, FAIL = [], []
SI_NAMES = {0: "MEDIA_LOCKED", 1: "MEDIA_UNLOCKED", 2: "STREAM_INTERRUPTED", 3: "SEQ_NUM_MISMATCH", 4: "MEDIA_RESET",
            5: "TIMESTAMP_UNCERTAIN", 6: "TIMESTAMP_VALID", 7: "TIMESTAMP_NOT_VALID", 8: "UNSUPPORTED_FORMAT",
            9: "LATE_TIMESTAMP", 10: "EARLY_TIMESTAMP", 11: "FRAMES_RX"}
NAMES = {0x0005: SI_NAMES, 0x0006: {0: "STREAM_START", 1: "STREAM_STOP", 2: "MEDIA_RESET", 3: "TIMESTAMP_UNCERTAIN",
                                    4: "FRAMES_TX"},
         0x0009: {0: "LINK_UP", 1: "LINK_DOWN", 5: "GPTP_GM_CHANGED"}}
LABEL = {"dut-0x0005-0": "DUT STREAM_INPUT 0", "dut-0x0009-0": "DUT AVB_INTERFACE 0",
         "peer-0x0006-0": "peer STREAM_OUTPUT 0"}
POLL_WORDS = {"0x8d4": "SLIP_LB", "0x8d8": "SLIP_TDM", "0x8dc": "RENDER_STAT", "0x8f8": "MCSRV_STAT",
              "0x8e0": "AAFM_STAT", "0x8e4": "AAFM_RATE", "0x738": "CRF_CTRL", "0x748": "CRF_RATE"}


def jl(path):
    return [json.loads(x) for x in open(path) if x.startswith("{")]


def check(name, ok, detail=None):
    if not ok:
        FAIL.append(dict(check=name, detail=detail))


def r1(v, dp, sign=False):
    return f"{v:+.{dp}f}" if sign else f"{v:.{dp}f}"


def once(v, src_dp, dp, what, sign=False):
    d = Decimal(repr(v)).quantize(Decimal(1).scaleb(-src_dp))
    q = Decimal(1).scaleb(-dp)
    tie = abs(d) % q == q / 2 and dp < src_dp
    ROUNDING.append(dict(figure=what, grade_value=str(d), grade_decimals=src_dp, printed_decimals=dp, tie=tie))
    if tie:
        sys.exit(f"rounding tie: {what} = {d} cannot be printed at {dp} decimals from the grade")
    out = d.quantize(q, rounding=ROUND_HALF_EVEN)
    return f"{out:+}" if sign and out > 0 else f"{abs(out) if out == 0 else out}"


def baseline(path):
    m = re.search(r"^0x900008d4\s+((?:[0-9a-f]{2} ){4})", Path(path).read_text(), re.M)
    v = int.from_bytes(bytes.fromhex(m.group(1).replace(" ", "")), "little")
    return dict(dups=v & 0xFFFF, skips=v >> 16)


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


def counters_block(payload):
    dt, valid = int(payload[0:4], 16), int(payload[8:16], 16)
    vals = [int(payload[16 + 8 * k:24 + 8 * k], 16) for k in range(32)]
    names = NAMES.get(dt, {})
    return {names.get(k, f"k{k}"): vals[k] for k in range(32) if valid >> k & 1}


def cycle(tag):
    ev = jl(P / "cycles" / tag / "events.jsonl")
    rows = sorted(jl(P / "cycles" / tag / "poll.jsonl"), key=lambda r: r["n"])
    g = json.loads((P / "summary" / f"{tag}.json").read_text())
    kinds = {}
    for e in ev:
        kinds.setdefault(e["kind"], []).append(e)
    tb = kinds["bind-time"][0]["t_bind_local"]
    tu = next(e for e in kinds["unbind"])["t_cmd_local"]
    rel = lambda t: t - tb
    out = dict(cycle=tag, bind_utc=datetime.fromtimestamp(tb, timezone.utc).strftime("%H:%M:%S.%f")[:12],
               unbind_s=rel(tu), polls=len(rows), first_poll_s=rel(rows[0]["t0"]), last_poll_s=rel(rows[-1]["t1"]))
    out["unbind_status"] = [e["status"] for e in kinds["unbind"]]
    out["bind_status"] = [e["status"] for e in kinds["bind"]]
    out["bind_retry"] = "bind-retry" in kinds
    out["formats"] = [dict(talker=e["talker_fmt"], listener=e["listener_fmt"], set=e["set"]) for e in kinds["format-check"]]
    st = {e["when"]: e for e in kinds["state"]}
    out["clock_source"] = dict(dut_start=st["start"]["clk_dut"], dut_end=st["end"]["clk_dut"],
                               peer_start=st["start"]["clk_peer"], peer_end=st["end"]["clk_peer"])
    out["bound_as_found_end"] = kinds["cycle-check"][0]["bound_as_found"]
    # every polled word: the set of values and every change, timed by its poll interval
    missing = 0
    changes = {name: [] for name in POLL_WORDS.values()}
    values = {name: set() for name in POLL_WORDS.values()}
    prev = None
    for r in rows:
        w = r["words"]
        if any(w.get(k) is None for k in POLL_WORDS):
            missing += 1
            continue
        for k, name in POLL_WORDS.items():
            values[name].add(w[k])
            if prev is not None and prev["words"][k] != w[k]:
                changes[name].append(dict(s_lo=rel(prev["t0"]), s_hi=rel(r["t1"]), before=prev["words"][k], after=w[k]))
        prev = r
    out["missing_reads"] = missing
    out["values"] = {k: sorted(v) for k, v in values.items()}
    lb = lambda v: dict(dups=int(v, 16) & 0xFFFF, skips=int(v, 16) >> 16)
    out["slip_lb_first"], out["slip_lb_last"] = lb(rows[0]["words"]["0x8d4"]), lb(rows[-1]["words"]["0x8d4"])
    out["slip_lb_changes"] = [dict(c, d_dups=lb(c["after"])["dups"] - lb(c["before"])["dups"],
                                   d_skips=lb(c["after"])["skips"] - lb(c["before"])["skips"]) for c in changes["SLIP_LB"]]
    out["word_changes"] = {k: len(v) for k, v in changes.items()}
    # RENDER_STAT after the bind: prefill exit bracket, converged by, fill range, rails
    post = [r for r in rows if r["t1"] > tb]
    rs = [(r, int(r["words"]["0x8dc"], 16)) for r in post if r["words"].get("0x8dc")]
    first0 = next((i for i, (r, v) in enumerate(rs) if not v >> 8 & 1), None)
    conv = next((r for r, v in rs[first0:] if v >> 9 & 1), None) if first0 is not None else None
    fills = [v & 0xFF for r, v in rs[first0:]] if first0 is not None else []
    out["render"] = dict(prefill_exit_by_s=rel(rs[first0][0]["t1"]) if first0 is not None else None,
                         converged_by_s=rel(conv["t1"]) if conv else None,
                         fill_min=min(fills) if fills else None, fill_max=max(fills) if fills else None,
                         rails=sorted({v >> 16 for r, v in rs}),
                         stays_converged=all(v >> 9 & 1 for r, v in rs[first0:]) if first0 is not None else None)
    out["servo_states"] = sorted({int(r["words"]["0x8f8"], 16) & 7 for r in rows})
    # tap
    t = g["tap"]
    pr = t["priming"]
    out["first_pdu_ms"] = pr["first_pdu_after_command_ms"]
    out["arm_fires_ms_design"] = pr["first_pdu_after_command_ms"] + ARM_MS
    out["delta_ppm"] = t["delta_ppm"]
    out["peer_rate_ppm"], out["dut_rate_ppm"] = t["streams"]["peer-aaf"]["rate_ppm"], t["streams"]["dut-aaf"]["rate_ppm"]
    out["lateness_p999_us"], out["lateness_max_us"] = pr["lateness_us"]["p999"], pr["lateness_us"]["max"]
    out["phase_p50_us"] = pr["phase_us_mod_pdu"]["p50"]
    late = [x for x in t["late_pdus"] if x["s"] > 0]
    b = bursts(late)
    last = out["last_poll_s"]
    to_last = [x for x in b if x["s"] <= last]
    out["bursts_to_last_poll"] = len(to_last)
    out["bursts_to_capture"] = len(b)
    out["first_burst"] = dict(s=b[0]["s"], peak_us=b[0]["peak_us"], pdus=b[0]["pdus"]) if b else None
    out["peak_to_last_poll_us"] = max((x["peak_us"] for x in to_last), default=None)
    out["peak_to_capture_us"] = max((x["peak_us"] for x in b), default=None)
    first10 = next((x for x in late if x["late_us"] > 10.0), None)
    out["first_over_10us"] = first10
    out["over_10us_before_arm"] = [x for x in late if x["late_us"] > 10.0 and x["s"] * 1e3 <= out["arm_fires_ms_design"]]
    out["pdus_seq_gaps"] = {k: v["seq_gaps"] for k, v in t["streams"].items()}
    # GET_COUNTERS, start and end
    cs = {e["when"]: e["payloads"] for e in kinds["counters"]}
    moved = {}
    for key in cs["start"]:
        a, z = counters_block(cs["start"][key]), counters_block(cs["end"][key])
        moved[LABEL[key]] = {n: [a[n], z[n]] for n in a if a[n] != z[n]}
    out["counters_moved"] = moved
    # grade
    first_late20 = next((x["s"] for x in late if x["late_us"] > BURST_US), None)
    grades = []
    for c in out["slip_lb_changes"]:
        lat = max((x["late_us"] for x in late if c["s_lo"] <= x["s"] <= c["s_hi"]), default=None)
        in_burst = any(c["s_lo"] <= x["s"] <= c["s_hi"] for x in b)
        fp = out["first_pdu_ms"] / 1e3
        if (c["d_dups"], c["d_skips"]) == (1, 0) and c["s_lo"] <= fp <= c["s_hi"] and (first_late20 is None or c["s_hi"] <= first_late20):
            cls = "#743 residual"
        elif (c["d_dups"], c["d_skips"]) == (2, 0) and in_burst:
            cls = "B17 class (c)"
        else:
            cls = "other"
        grades.append(dict(c, cls=cls, largest_lateness_us=lat))
    out["slip_grades"] = grades
    out["grade"] = "held" if not grades else ("#743 residual" if all(x["cls"] == "#743 residual" for x in grades) else "not held")
    # consistency with the grade's own poll reading
    check(f"{tag} polls", g["poll"]["polls"] == len(rows))
    check(f"{tag} slips", len(g["poll"]["slips"]) == len(grades))
    check(f"{tag} first/last", abs(g["poll"]["first_poll_s"] - out["first_poll_s"]) < 5e-4 and abs(g["poll"]["last_poll_s"] - out["last_poll_s"]) < 5e-4)
    return out


def b17_cycle(tag):
    g = json.loads((B17 / "summary" / f"{tag}.json").read_text())
    ev = jl(B17 / "cycles" / tag / "events.jsonl")
    tb = next(e for e in ev if e["kind"] == "bind-time")["t_bind_local"]
    late = [x for x in g["tap"]["late_pdus"] if x["s"] > 0]
    b = bursts(late)
    # B17's slip intervals from its raw counter log, rounded once when printed (B17 round 2's rule)
    rows = sorted(jl(B17 / "cycles" / tag / "poll.jsonl"), key=lambda r: r["n"])
    sl = []
    for a, z in zip(rows, rows[1:]):
        va, vz = a["words"].get("0x8d4"), z["words"].get("0x8d4")
        if va and vz and va != vz:
            sl.append(dict(s_lo=a["t0"] - tb, s_hi=z["t1"] - tb, dups=(int(vz, 16) & 0xFFFF) - (int(va, 16) & 0xFFFF),
                           skips=(int(vz, 16) >> 16) - (int(va, 16) >> 16)))
    check(f"B17 {tag} slips", len(sl) == len(g["poll"]["slips"]) and all(
        abs(x["s_lo"] - y["s_lo"]) < 5e-4 and abs(x["s_hi"] - y["s_hi"]) < 5e-4 for x, y in zip(sl, g["poll"]["slips"])))
    return dict(cycle=tag, bind_utc=datetime.fromtimestamp(tb, timezone.utc).strftime("%H:%M:%S.%f")[:12],
                slips=sl,
                first_pdu_ms=g["tap"]["priming"]["first_pdu_after_command_ms"],
                first_burst=dict(s=b[0]["s"], peak_us=b[0]["peak_us"]) if b else None,
                slip_lb=[g["poll"]["slip_lb_first"]["dups"], g["poll"]["slip_lb_last"]["dups"]])


def main():
    cyc = [cycle(t) for t in CYCLES]
    b17 = [b17_cycle(t) for t in CYCLES]
    start, end = baseline(P / "restore" / "dut-start.txt"), baseline(P / "restore" / "dut-end.txt")
    joins = [start == cyc[0]["slip_lb_first"]] + [a["slip_lb_last"] == b["slip_lb_first"] for a, b in zip(cyc, cyc[1:])] + \
            [cyc[-1]["slip_lb_last"] == end]
    check("counter continuity", all(joins), joins)
    digest_lines = []
    for t in CYCLES:
        f = P / "cycles" / t / "poll.jsonl"
        digest_lines.append(f"{hashlib.sha256(f.read_bytes()).hexdigest()}  cycles/{t}/poll.jsonl")
    (P / "summary" / "counter-logs.sha256").write_text("\n".join(digest_lines) + "\n")
    tools = {f: hashlib.sha256((P / "tools" / f).read_bytes()).hexdigest()
             for f in ("cyc_b18.py", "console_poll_b8.py", "ana_b17.py", "summ_b18.py")}
    as_run = {e["tool_sha256"] for t in CYCLES for e in jl(P / "cycles" / t / "events.jsonl") if e["kind"] == "start"}
    poll_run = {e["poller_sha256"] for t in CYCLES for e in jl(P / "cycles" / t / "events.jsonl") if e["kind"] == "start"}
    check("cycle runner as run", as_run == {tools["cyc_b18.py"]}, sorted(as_run))
    check("poller as run", poll_run == {tools["console_poll_b8.py"]}, sorted(poll_run))

    # per-cycle table
    hdr = ("| Cycle | Bind, UTC | Polls, s from the bind | `SLIP_LB` dups, skips | Change | Grade | First peer PDU, ms "
           "| First burst over 20 us: s, peak | Bursts to the last poll, peak | CLOCK_SOURCE DUT, peer | delta_ppm |\n"
           "|---|---|---|---|---|---|---|---|---|---|---|\n")
    lines = []
    for c in cyc:
        fb = c["first_burst"]
        chg = "None" if not c["slip_grades"] else "; ".join(
            f"{r1(x['s_lo'], 2)} to {r1(x['s_hi'], 2)}, {x['d_dups']:+d} dups, {x['d_skips']:+d} skips" for x in c["slip_grades"])
        cls = c["clock_source"]
        lines.append(
            f"| {c['cycle']} | {c['bind_utc']} | {c['polls']}, {r1(c['first_poll_s'], 2)} to {r1(c['last_poll_s'], 2, True)} "
            f"| {c['slip_lb_first']['dups']}, {c['slip_lb_first']['skips']} to {c['slip_lb_last']['dups']}, {c['slip_lb_last']['skips']} "
            f"| {chg} | {c['grade'].capitalize() if c['grade'] == 'held' else c['grade']} "
            f"| {once(c['first_pdu_ms'], 3, 3, c['cycle'] + ' first PDU')} "
            f"| {once(fb['s'], 6, 2, c['cycle'] + ' first burst s')}, {once(fb['peak_us'], 3, 1, c['cycle'] + ' first burst peak')} us "
            f"| {c['bursts_to_last_poll']}, {once(c['peak_to_last_poll_us'], 3, 1, c['cycle'] + ' peak to last poll')} us "
            f"| {cls['dut_start']} to {cls['dut_end']}, {cls['peer_start']} to {cls['peer_end']} "
            f"| {once(c['delta_ppm'], 4, 4, c['cycle'] + ' delta', True)} |")
    table = hdr + "\n".join(lines) + "\n"
    (P / "summary" / "table.md").write_text(table)

    # comparison with B17
    hdr = ("| Cycle | B17 bind, UTC | B17 first peer PDU, ms | B17 slip: s from the bind, count | B17 first burst: s, peak "
           "| B18 first peer PDU, ms | B18 `SLIP_LB` change | B18 first burst: s, peak |\n|---|---|---|---|---|---|---|---|\n")
    cl = []
    for a, c in zip(b17, cyc):
        sl = "; ".join(f"{r1(x['s_lo'], 2)} to {r1(x['s_hi'], 2)}, +{x['dups']} dups" for x in a["slips"]) or "None"
        cl.append(f"| {c['cycle']} | {a['bind_utc']} | {once(a['first_pdu_ms'], 3, 3, 'B17 ' + c['cycle'] + ' first PDU')} | {sl} "
                  f"| {once(a['first_burst']['s'], 6, 2, 'B17 ' + c['cycle'] + ' burst s')}, "
                  f"{once(a['first_burst']['peak_us'], 3, 1, 'B17 ' + c['cycle'] + ' burst peak')} us "
                  f"| {once(c['first_pdu_ms'], 3, 3, c['cycle'] + ' first PDU')} "
                  f"| {'None' if not c['slip_grades'] else 'see table'} "
                  f"| {once(c['first_burst']['s'], 6, 2, c['cycle'] + ' first burst s')}, "
                  f"{once(c['first_burst']['peak_us'], 3, 1, c['cycle'] + ' first burst peak')} us |")
    compare = hdr + "\n".join(cl) + "\n"
    (P / "summary" / "compare.md").write_text(compare)

    # counters that moved, per cycle
    cm = ["| Cycle | Counter | Start | End |", "|---|---|---|---|"]
    for c in cyc:
        for who, d in c["counters_moved"].items():
            for n, (a, z) in d.items():
                cm.append(f"| {c['cycle']} | {who} {n} | {a:,} | {z:,} |")
    (P / "summary" / "counters.md").write_text("\n".join(cm) + "\n")

    rng = lambda vals, dp: f"{r1(min(vals), dp)} to {r1(max(vals), dp)}"
    lane = dict(
        cycles=len(cyc), held=sum(c["grade"] == "held" for c in cyc),
        residual_743=sum(x["cls"] == "#743 residual" for c in cyc for x in c["slip_grades"]),
        class_c=sum(x["cls"] == "B17 class (c)" for c in cyc for x in c["slip_grades"]),
        other=sum(x["cls"] == "other" for c in cyc for x in c["slip_grades"]),
        slip_lb=[start, end], counter_joins=joins,
        clock_source_changes=sum(c["clock_source"]["dut_start"] != c["clock_source"]["dut_end"] or
                                 c["clock_source"]["peer_start"] != c["clock_source"]["peer_end"] for c in cyc),
        polls=sorted({c["polls"] for c in cyc}), missing_reads=sum(c["missing_reads"] for c in cyc),
        first_poll_s=rng([c["first_poll_s"] for c in cyc], 2), last_poll_s=rng([c["last_poll_s"] for c in cyc], 2),
        poll_word_changes={k: sum(c["word_changes"][k] for c in cyc) for k in POLL_WORDS.values()},
        poll_word_values={k: sorted({v for c in cyc for v in c["values"][k]}) for k in POLL_WORDS.values() if k != "RENDER_STAT"},
        servo_states=sorted({s for c in cyc for s in c["servo_states"]}),
        first_pdu_ms=[min(c["first_pdu_ms"] for c in cyc), max(c["first_pdu_ms"] for c in cyc)],
        arm_fires_ms_design=[min(c["arm_fires_ms_design"] for c in cyc), max(c["arm_fires_ms_design"] for c in cyc)],
        first_burst_s=[min(c["first_burst"]["s"] for c in cyc), max(c["first_burst"]["s"] for c in cyc)],
        first_burst_peak_us=[min(c["first_burst"]["peak_us"] for c in cyc), max(c["first_burst"]["peak_us"] for c in cyc)],
        bursts_to_last_poll=[min(c["bursts_to_last_poll"] for c in cyc), max(c["bursts_to_last_poll"] for c in cyc)],
        bursts_to_capture=[min(c["bursts_to_capture"] for c in cyc), max(c["bursts_to_capture"] for c in cyc)],
        peak_to_last_poll_us=[min(c["peak_to_last_poll_us"] for c in cyc), max(c["peak_to_last_poll_us"] for c in cyc)],
        peak_to_capture_us=[min(c["peak_to_capture_us"] for c in cyc), max(c["peak_to_capture_us"] for c in cyc)],
        over_10us_before_arm=sum(len(c["over_10us_before_arm"]) for c in cyc),
        first_over_10us_s=[min(c["first_over_10us"]["s"] for c in cyc), max(c["first_over_10us"]["s"] for c in cyc)],
        lateness_p999_us=[min(c["lateness_p999_us"] for c in cyc), max(c["lateness_p999_us"] for c in cyc)],
        delta_ppm=[min(c["delta_ppm"] for c in cyc), max(c["delta_ppm"] for c in cyc)],
        peer_rate_ppm=[min(c["peer_rate_ppm"] for c in cyc), max(c["peer_rate_ppm"] for c in cyc)],
        dut_rate_ppm=[min(c["dut_rate_ppm"] for c in cyc), max(c["dut_rate_ppm"] for c in cyc)],
        phase_p50_us=[min(c["phase_p50_us"] for c in cyc), max(c["phase_p50_us"] for c in cyc)],
        prefill_exit_by_s=[min(c["render"]["prefill_exit_by_s"] for c in cyc), max(c["render"]["prefill_exit_by_s"] for c in cyc)],
        converged_by_s=[min(c["render"]["converged_by_s"] for c in cyc), max(c["render"]["converged_by_s"] for c in cyc)],
        fill=[min(c["render"]["fill_min"] for c in cyc), max(c["render"]["fill_max"] for c in cyc)],
        rails=sorted({r for c in cyc for r in c["render"]["rails"]}),
        seq_gaps=sum(v for c in cyc for v in c["pdus_seq_gaps"].values()),
        b17_slips=sum(len(a["slips"]) for a in b17),
        b17_first_pdu_ms=[min(a["first_pdu_ms"] for a in b17), max(a["first_pdu_ms"] for a in b17)],
        tools=tools, failed_checks=FAIL)
    (P / "summary" / "cycles.json").write_text(json.dumps(dict(lane=lane, cycles=cyc, b17=b17, rounding=ROUNDING),
                                                          indent=1, default=str) + "\n")
    print(json.dumps(lane, indent=1, default=str))
    print(table)
    print(compare)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
