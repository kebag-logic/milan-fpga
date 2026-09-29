"""Build the per-cycle and per-step tables from bench/*/analysis.json.

Writes summary/cycles.json, summary/steps.json and summary/tables.md. No bench
access. Times are seconds relative to the OUT4 off command (cycles) or to the
software-GM start (steps), as in each analysis.
"""
import json
from pathlib import Path

P = Path(__file__).resolve().parent.parent
out = P / "summary"
out.mkdir(exist_ok=True)
A = lambda n: json.loads((P / "bench" / n / "analysis.json").read_text())


def tr(a, key):
    return a["counter_transitions"].get(key, [])


def first_after(rows, t, pred):
    for r in rows:
        if r[0] is not None and r[0] >= t and pred(r[1]):
            return r[0]
    return None


def count_changes(rows, lo, hi):
    vals = [v for t, v in rows if lo <= t <= hi]
    return sum(1 for a, b in zip(vals, vals[1:]) if a != b)


cycles = []
for name in ["bmsr-proof"] + ["cycle%02d" % i for i in range(1, 11)]:
    a = A(name)
    lk = a["link_counters"]["dut:counter-9-0"]
    d = {k: v["delta"] for k, v in a["counter_endpoints"].items()}
    md, mu = a.get("mac_link_down") or {}, a.get("mac_link_up") or {}
    w = a["wire"]
    carrier = a["carrier"]
    down = next((t for t, v in carrier if v == 0 and t > 0), None)
    up = next((t for t, v in carrier if v == 1 and down is not None and t > down), None)
    lic = a["crf_ctrl"]
    lic_drop = next((t for t, v in lic if t > 0 and v == "0x3"), None)
    lic_back = next((t for t, v in lic if lic_drop is not None and t > lic_drop and v == "0x3002e3"), None)
    c = dict(name=name, off_s=round(a["off_hold_s"], 2),
             link_down_bracket=[md.get("last_up_before"), md.get("first_down")],
             link_up_bracket=[mu.get("last_down_before"), mu.get("first_up")],
             linkg=[x for x in a["linkg_stat"]],
             link_counters=[lk["LINK_UP"], lk["LINK_DOWN"], lk["end_LINK_UP"], lk["end_LINK_DOWN"]],
             link_delta=[lk["end_LINK_DOWN"] - lk["LINK_DOWN"], lk["end_LINK_UP"] - lk["LINK_UP"]],
             gm_changed_delta=lk["GM_CHANGED"][1] - lk["GM_CHANGED"][0],
             mac_values=a["mac_status_values"], carrier_down_up=[down, up],
             last_far=a["last_far_frame_before_on"], far_frames_off=a["far_frames_during_off_after_5s"],
             wire_return=a["first_wire_return"], first_gm=a["first_gm"], first_gm_kind=a["first_gm_kind"],
             recovery_s=a["gptp_recovery_s"], steady_from=a["gptp_steady_from"],
             phc_steps=[s["phc_minus_wall_delta_s"] for s in a["phc_discontinuities"] if abs(s["phc_minus_wall_delta_s"]) > 0.1],
             first_pdu=[w["dut"].get("first_valid_after_on"), w["peer"].get("first_valid_after_on")],
             first_pdu_after_wire_return=[w["dut"].get("first_valid_after_wire_return_s"),
                                          w["peer"].get("first_valid_after_wire_return_s")],
             first_pdu_after_link_up=[round(x - mu["first_up"], 3) if x is not None and mu.get("first_up") else None
                                      for x in (w["dut"].get("first_valid_after_on"), w["peer"].get("first_valid_after_on"))],
             media_locked_at=a.get("media_locked_at"), servo_locked_at=a.get("servo_locked_at"),
             licence_drop_back=[lic_drop, lic_back],
             dut_mr_changes=len(w["dut"]["mr"]) - 1 if w["dut"]["mr"] else 0,
             peer_mr_changes=len(w["peer"]["mr"]) - 1 if w["peer"]["mr"] else 0,
             dut_in=d.get("dut:counter-5-1"), dut_out=d.get("dut:counter-6-1"), dut_cd=d.get("dut:counter-36-0"),
             peer_in_unlocked_seen=any(v.get("1", 0) > 0 for t, v in tr(a, "peer:counter-5-8")),
             dut_out_media_reset_seq=[v.get("2") for t, v in tr(a, "dut:counter-6-1")],
             bindings=a["bindings"], console_gap=round(a["max_console_gap_s"], 3), epochs=a["reset_epochs"],
             peer_adp=a["peer_available_index"])
    cycles.append(c)
(out / "cycles.json").write_text(json.dumps(cycles, indent=1) + "\n")

steps = []
runs = []
for i in range(1, 6):
    name = "gm%02d" % i
    a = A(name)
    d = {k: v["delta"] for k, v in a["counter_endpoints"].items()}
    real = [s for s in a["phc_discontinuities"] if abs(s["phc_minus_wall_delta_s"]) > 0.005]
    wj, fj = a["dut_phc_wire_jumps"], a["far_time_jumps"]
    health = a["health"]
    runs.append(dict(name=name, prep=a["events"], announce=a["announce_gm"], gm=a["gm"], deltas=d,
                     tucnt=a["clkv_tucnt_first_last"], discards=[a["servo"][0][1]["discards"], a["servo"][-1][1]["discards"]],
                     servo_states=sorted({s[1]["state"] for s in a["servo"]}), bindings=a["bindings"],
                     wire_mr=[a["wire"]["dut"]["mr"], a["wire"]["peer"]["mr"]],
                     wire_tu_counts=[a["wire"]["dut"]["tu_counts"], a["wire"]["peer"]["tu_counts"]],
                     wire_max_gap=[a["wire"]["dut"]["max_gap_s"], a["wire"]["peer"]["max_gap_s"]],
                     console_gap=round(a["max_console_gap_s"], 3), epochs=a["reset_epochs"],
                     other_console_flags=[s for s in a["phc_discontinuities"] if abs(s["phc_minus_wall_delta_s"]) <= 0.005]))
    for k, st in enumerate(real):
        lo = st["bracket"][0] - 1.0
        hi = (real[k + 1]["bracket"][0] - 1.0) if k + 1 < len(real) else 1e9
        p = next(x for x in a["per_step"] if x["step"]["bracket"] == st["bracket"])
        tu_wire = [x for x in a["wire"]["dut"]["tu"] if lo <= x[0] <= min(hi, st["bracket"][1] + 15)]
        episodes = sum(1 for t, v in tu_wire if v == 1)
        asc0 = next((t for t, v in health if t >= st["bracket"][0] and "asc0" in v and t < st["bracket"][1] + 10), None)
        asc1 = next((t for t, v in health if asc0 is not None and t > asc0 and "asc1" in v), None)
        hold = [x for x in a["holdover"] if lo <= x[0] <= min(hi, st["bracket"][1] + 15) and x[1] == 1]
        disc = [x[1]["discards"] for x in a["servo"] if lo <= x[0] <= min(hi, st["bracket"][1] + 15)]
        pre_disc = [x[1]["discards"] for x in a["servo"] if x[0] < lo]
        base_disc = pre_disc[-1] if pre_disc else (disc[0] if disc else None)

        def cdelta(key, idx):
            rows = [v for t, v in tr(a, key) if t <= min(hi, st["bracket"][1] + 15)]
            before = [v for t, v in tr(a, key) if t < lo]
            if not rows:
                return None
            b = (before[-1] if before else rows[0]).get(idx)
            return rows[-1].get(idx) - b
        steps.append(dict(run=name, edge="takeover" if k == 0 else "release", console_bracket=st["bracket"],
                          console_step_ms=round(st["phc_minus_wall_delta_s"] * 1e3, 3),
                          wire_step_ms=round(wj[k]["delta_s"] * 1e3, 3) if k < len(wj) else None,
                          gm_time_jump_ms=round(fj[k]["delta_s"] * 1e3, 3) if k < len(fj) else None,
                          tu_first=p["tu_first_set"], tu_steady_clear=p["tu_steady_clear"],
                          step_to_steady=[round(p["tu_steady_clear"] - st["bracket"][1], 3),
                                          round(p["tu_steady_clear"] - st["bracket"][0], 3)] if p["tu_steady_clear"] else None,
                          tu_wire_episodes=episodes, dut_wire_tu1=p["crf"]["dut"]["tu1"], peer_wire_tu1=p["crf"]["peer"]["tu1"],
                          holdover_episodes=len(hold), ascapable_drop=[asc0, asc1],
                          ascapable_drop_s=round(asc1 - asc0, 3) if asc0 is not None and asc1 is not None else None,
                          dut_mr_changes=count_changes([(t, v) for t, v in a["wire"]["dut"]["mr"]], lo, hi) if False else
                          sum(1 for t, v in a["wire"]["dut"]["mr"][1:] if lo <= t <= hi),
                          peer_mr_changes=sum(1 for t, v in a["wire"]["peer"]["mr"][1:] if lo <= t <= hi),
                          servo_discards=[base_disc, disc[-1] if disc else None],
                          dut_talker_media_reset=cdelta("dut:counter-6-1", "2"),
                          dut_talker_ts_uncertain=cdelta("dut:counter-6-1", "3"),
                          dut_listener=dict(locked=cdelta("dut:counter-5-1", "0"), unlocked=cdelta("dut:counter-5-1", "1"),
                                            media_reset=cdelta("dut:counter-5-1", "4"), ts_uncertain=cdelta("dut:counter-5-1", "5"),
                                            late=cdelta("dut:counter-5-1", "9"), early=cdelta("dut:counter-5-1", "10")),
                          peer_listener=dict(locked=cdelta("peer:counter-5-8", "0"), unlocked=cdelta("peer:counter-5-8", "1"),
                                             media_reset=cdelta("peer:counter-5-8", "4")),
                          dut_gm_changed=cdelta("dut:counter-9-0", "5"), peer_gm_changed=cdelta("peer:counter-9-0", "5"),
                          clock_domain=[cdelta("dut:counter-36-0", "0"), cdelta("dut:counter-36-0", "1")],
                          crf_max_gap_s=[p["crf"]["dut"]["max_gap_s"], p["crf"]["peer"]["max_gap_s"]]))
(out / "steps.json").write_text(json.dumps(dict(runs=runs, steps=steps), indent=1) + "\n")

L = []
L.append("| Cycle | OFF (s) | MAC_STATUS down / up | LINK_DOWN / LINK_UP | Controller down / up | GM return | gPTP recovery | First DUT / peer PDU | Link-up to first DUT / peer PDU | DUT MEDIA_LOCKED / UNLOCKED | Bindings |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|")
for c in cycles:
    L.append("| %s | %.2f | %s-%s / %s-%s | +%d / +%d | %.2f / %.2f | %.2f | %.3f | %s / %s | %s / %s | +%s / +%s | %s |" % (
        c["name"], c["off_s"], *c["link_down_bracket"], *c["link_up_bracket"], *c["link_delta"], *c["carrier_down_up"],
        c["first_gm"], c["recovery_s"], *c["first_pdu"], *c["first_pdu_after_link_up"],
        (c["dut_in"] or {}).get("0"), (c["dut_in"] or {}).get("1"), "held" if c["bindings"]["all_connected"] else "n/a"))
L.append("")
L.append("| Run | Edge | DUT PHC step (wire) | GM time jump | `tu` first / steady clear | Step to steady | `tu` episodes | asCapable drop | DUT / peer `mr` changes | DUT MEDIA_RESET talker / listener | DUT / peer MEDIA_UNLOCKED | Servo discards |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for s in steps:
    L.append("| %s | %s | %+.3f ms | %+.3f ms | %s / %s | %s-%s | %d | %s | %d / %d | +%s / +%s | +%s / +%s | %s -> %s |" % (
        s["run"], s["edge"], s["wire_step_ms"], s["gm_time_jump_ms"], s["tu_first"], s["tu_steady_clear"],
        *(s["step_to_steady"] or [None, None]), s["tu_wire_episodes"], s["ascapable_drop_s"], s["dut_mr_changes"],
        s["peer_mr_changes"], s["dut_talker_media_reset"], s["dut_listener"]["media_reset"],
        s["dut_listener"]["unlocked"], s["peer_listener"]["unlocked"], *s["servo_discards"]))
(out / "tables.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
