"""Summarize lane B2: per-bind and per-cycle results, distributions, growth, stop classes.

Reads every analysis.json and msrp.tsv in the packet and re-hashes every raw
capture. Writes summary/summary.json and RAW-ARTIFACTS.json. Derives every
printed count from the rows; nothing is pinned.

usage: b2_summary.py
"""
import hashlib, json, math, statistics as st, sys
from pathlib import Path

if sys.flags.optimize:
    raise SystemExit("refused: run without -O")
p = Path(__file__).resolve().parent.parent
RAW = Path("/tmp/b2-a440/raw")
SID = "0200000000010001"
DECL = ("New", "JoinIn", "JoinMt")


def betacf(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / d
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d
        c = 1 + aa / c
        d = 1 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d
        c = 1 + aa / c
        d = 1 / d
        de = d * c
        h *= de
        if abs(de - 1) < 1e-15:
            break
    return h


def ibeta(a, b, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lb = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    if x < (a + 1) / (a + b + 2):
        return math.exp(lb) * betacf(a, b, x) / a
    return 1 - math.exp(lb) * betacf(b, a, 1 - x) / b


def t_cdf(t, df):
    x = df / (df + t * t)
    tail = 0.5 * ibeta(df / 2, 0.5, x)
    return 1 - tail if t > 0 else tail


def t_crit(df, q=0.975):
    lo, hi = 0.0, 50.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if t_cdf(mid, df) < q:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def nearest_rank(v, q):
    v = sorted(v)
    return v[max(0, math.ceil(q * len(v)) - 1)]


def ols(xs, ys):
    n = len(xs)
    mx, my = st.fmean(xs), st.fmean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    a0 = my - b * mx
    rss = sum((y - a0 - b * x) ** 2 for x, y in zip(xs, ys))
    se = math.sqrt(rss / (n - 2) / sxx)
    tc = t_crit(n - 2)
    return dict(n=n, slope=b, se=se, df=n - 2, t_crit=tc, ci=[b - tc * se, b + tc * se])


def load_tsv(path):
    rows = []
    lines = path.read_text().splitlines()
    for line in lines[1:]:
        t, sender, typ, ev, sid, lst = line.split("\t")
        rows.append(dict(t=float(t), sender=sender, type=typ, event=ev, sid=sid, listener=lst))
    return rows


binds = []
for k in range(1, 100):
    f = p / "bind" / f"bind-{k}" / "analysis.json"
    if not f.exists():
        break
    a = json.loads(f.read_text())
    u = p / "bind" / f"unbind-{k}" / "analysis.json"
    b = json.loads(u.read_text()) if u.exists() else None
    binds.append(dict(bind=k, fresh=a["fresh"], pre_window_s=a["pre_window_s"], pre_dut_leaveall_pdus=a["pre_dut_leaveall_pdus"],
                      pre_target_ta_declarations=a["pre_dut_target_ta_declarations"], pre_target_ta_events=a["pre_dut_target_ta_events"],
                      probe_status=a["first_probe_response_status"], probe_after_response_s=a["first_probe_response_after_response_s"],
                      first_dut_ta_s=a["first_dut_ta"]["after_response_s"], first_dut_ta_event=a["first_dut_ta"]["event"],
                      first_bridge_mrpdu_s=a["first_bridge_mrpdu"]["after_response_s"], first_bridge_mrpdu_leaveall=a["first_bridge_mrpdu"]["leaveall"],
                      first_bridge_mrpdu_content=a["first_bridge_mrpdu"]["content"], first_bridge_ready_s=a["first_bridge_ready"]["after_response_s"],
                      bridge_leaveall_before_ready=a["bridge_leaveall_between_response_and_ready"], latency_s=a["latency_s"],
                      ready_to_first_pdu_s=a["ready_to_first_pdu_s"], checks=[a["first_pair_progresses"], a["first_pdu_dmac_ok"], a["first_pdu_src_ok"]],
                      start_stop_delta=a["dut_out1_start_stop_delta"], result=a["result"],
                      unbind=None if b is None else dict(lv_s=b["bridge_listener_lv_after_response_s"], last_pdu_s=b["last_valid_pdu_after_response_s"],
                                                         pdus_after_lv_plus_period=b["pdus_after_lv_plus_period"], dut_ta_lv_s=b["dut_ta_lv_after_response_s"],
                                                         settle_s=b["settle_after_ta_lv_s"], start_stop_delta=b["dut_out1_start_stop_delta"], result=b["result"])))

cycles = []
redecl = []
for f in sorted((p / "cycles").glob("cycle-[0-9]*/analysis.json")):
    a = json.loads(f.read_text())
    n = int(f.parent.name.split("-")[1])
    ev = load_tsv(f.parent / "msrp.tsv")
    D, R = a["disconnect_response_s"], a["response_s"]
    ready_back = a["response_s"] + (a["bridge_ready_after_response_s"] or 0)
    # Every Listener-type LeaveAll while the stream is registered (before the disconnect
    # response, or after the bridge's post-reconnect Ready): delay to the bridge's next
    # declaration of the stream, same-PDU declarations included.
    for i, e in enumerate(ev):
        if e["event"] == "LeaveAll" and e["type"] == "Listener" and (e["t"] < D or e["t"] > ready_back):
            nxt = next((x for x in ev[i + 1:] if x["sender"] == "bridge" and x["type"] == "Listener" and x["sid"] == SID and x["event"] in DECL), None)
            redecl.append(dict(cycle=n, sender=e["sender"], delay_s=(nxt["t"] - e["t"]) if nxt else None))
    lv_t = D + a["bridge_lv_after_disconnect_s"] if a.get("bridge_lv_after_disconnect_s") is not None else None
    cls = a.get("registrar_at_lv")
    cycles.append(dict(cycle=n, hold_s=a["hold_s"], lv_s=a.get("bridge_lv_after_disconnect_s"), registrar=cls,
                       window_before_lv_s=lv_t, last_la_before_lv=a.get("last_listener_leaveall_before_lv"),
                       nearest_own_la_minus_lv_s=a.get("nearest_own_leaveall_minus_lv_s"),
                       last_pdu_after_lv_s=a.get("last_pdu_after_lv_s"), last_pdu_after_disconnect_s=a.get("last_pdu_after_disconnect_s"),
                       pdus_after_lv_plus_period=a.get("pdus_after_lv_plus_period"), hold_pdus=a["hold_pdus"], settled_pdus=a["settled_pdus"],
                       last_half_second_pdus=a["last_half_second_pdus"], stopped=a["stopped"], start_stop_delta=a["dut_out1_start_stop_delta"],
                       counted=a["counted_stop_start"], ta_in_hold=a["dut_ta_declarations_in_hold"] > 0, ta_lv_in_hold=a["dut_ta_lv_in_hold"],
                       restart_s=a["restart_s"], bridge_ready_s=a["bridge_ready_after_response_s"], progresses=a.get("first_pair_progresses"),
                       demonstrated=a["demonstrated_restart"], restart_75=a["restart_75"], stop_608=a["stop_608"],
                       msrp=a["msrp_pdus_by_sender"], span_s=a["capture_span_s"], reversals=a["reversals"], anchor_spread_s=a["anchor_spread_s"],
                       malformed=len(a["msrp_malformed"])))

max_redecl = max(r["delay_s"] for r in redecl if r["delay_s"] is not None)
missing_redecl = [r for r in redecl if r["delay_s"] is None]
min_window = min(c["window_before_lv_s"] for c in cycles if c["window_before_lv_s"] is not None)
for c in cycles:
    if c["registrar"] == "UNDETERMINED":
        # No Listener LeaveAll in the capture before the Lv: the last one came more than
        # window_before_lv_s earlier, and the bridge re-declared within max_redecl of
        # every one observed while registered. Inferred IN only when that bound holds.
        c["registrar_class"] = "IN (inferred)" if max_redecl < c["window_before_lv_s"] and not missing_redecl else "UNDETERMINED"
    else:
        c["registrar_class"] = c["registrar"] + (" (observed)" if c["registrar"] == "IN" else "")
    stop_in = c["pdus_after_lv_plus_period"] == 0
    c["stop_class"] = ("stop within one PDU" if stop_in else ("non-stop hold" if not c["stopped"] else "late stop"))

demo = [c for c in cycles if c["demonstrated"]]
lat = [c["restart_s"] for c in demo]
fit = ols([c["cycle"] for c in demo], lat)
blocks = []
for b0 in range(1, 101, 10):
    rows = [c for c in cycles if b0 <= c["cycle"] < b0 + 10]
    dl = [c["restart_s"] for c in rows if c["demonstrated"]]
    pdus = sum(sum(c["msrp"].values()) for c in rows)
    span = sum(c["span_s"] for c in rows)
    blocks.append(dict(block=f"{b0}-{b0 + 9}", demonstrated=len(dl), median=st.median(dl) if dl else None, max=max(dl) if dl else None,
                       msrp_pdus_per_s=pdus / span if span else None))
by_ta = {}
for key, sel in (("held", True), ("withdrawn", False)):
    v = [c["restart_s"] for c in demo if c["ta_in_hold"] == sel]
    by_ta[key] = dict(n=len(v), median=st.median(v) if v else None, min=min(v) if v else None, max=max(v) if v else None)
near_own = [dict(cycle=c["cycle"], own_la_minus_lv_s=c["nearest_own_la_minus_lv_s"], stop=c["stop_class"], registrar=c["registrar_class"])
            for c in cycles if c["nearest_own_la_minus_lv_s"] is not None and abs(c["nearest_own_la_minus_lv_s"]) <= 0.25]
stopped = [c for c in cycles if c["stopped"]]
summary = dict(
    binds=binds,
    bind_latency=dict(n=len(binds), below_1s=sum(b["latency_s"] < 1 for b in binds), min=min(b["latency_s"] for b in binds),
                      median=st.median(b["latency_s"] for b in binds), max=max(b["latency_s"] for b in binds),
                      fresh=sum(b["fresh"] for b in binds), probe_success=sum(b["probe_status"] == 0 for b in binds),
                      bridge_first_mrpdu_leaveall=sum(b["first_bridge_mrpdu_leaveall"] for b in binds)),
    cycles_n=len(cycles),
    restart=dict(demonstrated=len(demo), below_1s=sum(v < 1 for v in lat), min=min(lat), median=st.median(lat), p95=nearest_rank(lat, 0.95), max=max(lat),
                 first_ten_median=st.median([c["restart_s"] for c in demo if c["cycle"] <= 10]),
                 last_ten_median=st.median([c["restart_s"] for c in demo if c["cycle"] > 90]), fit=fit, by_ta_in_hold=by_ta),
    not_restart=[c["cycle"] for c in cycles if not c["demonstrated"]],
    blocks=blocks,
    stop=dict(within_one_pdu=sum(c["stop_class"] == "stop within one PDU" for c in cycles), non_stop_holds=[c["cycle"] for c in cycles if c["stop_class"] == "non-stop hold"],
              late_stops=[c["cycle"] for c in cycles if c["stop_class"] == "late stop"],
              registrar_classes={k: sum(c["registrar_class"] == k for c in cycles) for k in sorted({c["registrar_class"] for c in cycles})},
              in_withdrawals_stopped=sum(c["registrar_class"].startswith("IN") and c["stop_class"] == "stop within one PDU" for c in cycles),
              in_withdrawals=sum(c["registrar_class"].startswith("IN") for c in cycles),
              lv_after_disconnect=[min(c["lv_s"] for c in cycles), max(c["lv_s"] for c in cycles)],
              last_pdu_after_lv_stopped=[min(c["last_pdu_after_lv_s"] for c in stopped), max(c["last_pdu_after_lv_s"] for c in stopped)],
              last_pdu_after_disconnect_stopped=[min(c["last_pdu_after_disconnect_s"] for c in stopped), st.median(c["last_pdu_after_disconnect_s"] for c in stopped),
                                                 max(c["last_pdu_after_disconnect_s"] for c in stopped)],
              counted=sum(c["counted"] for c in cycles), start_stop_sum=[sum(c["start_stop_delta"][0] for c in cycles), sum(c["start_stop_delta"][1] for c in cycles)],
              redeclaration_after_leaveall=dict(observed=len(redecl), max_delay_s=max_redecl, missing=len(missing_redecl),
                                                by_sender={s: sum(r["sender"] == s for r in redecl) for s in ("DUT", "bridge")}),
              min_window_before_lv_s=min_window, near_own_leaveall=near_own),
    ta_in_hold=dict(held=sum(c["ta_in_hold"] for c in cycles), withdrawn=sum(not c["ta_in_hold"] for c in cycles)),
    integrity=dict(reversals=sum(c["reversals"] for c in cycles), max_anchor_spread_s=max(c["anchor_spread_s"] for c in cycles),
                   malformed_msrp=sum(c["malformed"] for c in cycles), progress_fail=[c["cycle"] for c in cycles if c["progresses"] is False]),
    cycles=cycles)
(p / "summary" / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
raw = []
for f in sorted(RAW.glob("*/tap.pcap")):
    b = f.read_bytes()
    h = hashlib.sha256(b).hexdigest()
    rec = None
    for d in ("bind", "cycles"):
        q = p / d / f.parent.name / "raw-artifacts.json"
        if q.exists():
            rec = json.loads(q.read_text())[0]
    assert rec and rec["sha256"] == h and rec["size"] == len(b), ("raw mismatch", f)
    raw.append(dict(path=f.parent.name + "/tap.pcap", size=len(b), sha256=h))
(p / "RAW-ARTIFACTS.json").write_text(json.dumps(dict(location="outside the packet, on the build box scratch area (/tmp/b2-a440/raw)", files=raw,
                                                      total_bytes=sum(r["size"] for r in raw)), indent=1) + "\n")
print(json.dumps({k: v for k, v in summary.items() if k not in ("cycles", "binds")}, indent=1))
print("raw artifacts:", len(raw), sum(r["size"] for r in raw))
