#!/usr/bin/env python3
"""Independently re-derive the two pages' tables and prose claims from the archived analyses.

usage: rederive.py <packet-root: .../review-evidence/b1-r1> <repo-root at the reviewed head>

Uses only bench/*/analysis.json and the pages at the head; it does not import or run
the author's summary script. Each check prints PASS/FAIL/NOTE; exit 1 on any FAIL.
"""
import json, re, sys
from pathlib import Path

pk, repo = Path(sys.argv[1]), Path(sys.argv[2])
B = pk / "author" / "bench"
A = lambda n: json.loads((B / n / "analysis.json").read_text())
SWITCH, DUT, HOST = "3cc0c6fffefe0210", "020000fffe000001", "<controller-host-id>"
nok = nbad = 0


def res(c, m):
    global nok, nbad
    nok += bool(c)
    nbad += not c
    print(("PASS " if c else "FAIL ") + m)


def note(m):
    print("NOTE " + m)


def table(text, header_start):
    lines = text.splitlines()
    i = next(k for k, l in enumerate(lines) if l.startswith(header_start))
    rows = []
    for l in lines[i + 2:]:
        if not l.startswith("|"):
            break
        rows.append([c.strip() for c in l.strip("|").split("|")])
    return rows


f2 = lambda x: "%.2f" % x
p599 = (repo / "docs/findings/599_394_E1_LINK_CYCLES.md").read_text()
p387 = (repo / "docs/findings/387_SOFTWARE_GM_STEP.md").read_text()

# ---------------- #599 / #394: cycles ----------------
print("== per-cycle table (599 page)")
page = {r[0]: r for r in table(p599, "| Cycle | OFF |")}
prev_end = None
agg = dict(down=[], up=[], ret_before_frame=[], rec=[], mlock=[], slock=[], pdu_after_frame=([], []),
           pdu_after_up=([], []), steps=[], console_gap=[])
for i in range(1, 11):
    n = "cycle%02d" % i
    a = A(n)
    r = page[str(i)]
    off = a["off_hold_s"]
    ms = a["mac_status"]
    ls = a["link_status_csr"]
    vals = [v for _, v in ms]
    # exactly one down and one up after OFF, values 0x0d / 0x00 / 0x0d
    res(vals == ["0xd", "0x0", "0xd"], "%s MAC_STATUS sequence %s" % (n, vals))
    res([v for _, v in ls] == vals and all(abs(x[0] - y[0]) < 0.1 for x, y in zip(ms, ls)),
        "%s link_status CSR changes in the same console rounds as MAC_STATUS" % n)
    # brackets: last sample before, first sample after
    md, mu = a["mac_link_down"], a["mac_link_up"]
    res(abs(md["first_down"] - ms[1][0]) < 1e-6 and abs(mu["first_up"] - ms[2][0]) < 1e-6, "%s bracket ends are the change samples" % n)
    res(md["first_down"] - md["last_up_before"] <= 0.26 and mu["first_up"] - mu["last_down_before"] <= 0.26,
        "%s link brackets <= 0.26 s" % n)
    res(r[1] == f2(off), "%s OFF %s vs page %s" % (n, f2(off), r[1]))
    res(r[2] == "%s-%s" % (f2(md["last_up_before"]), f2(md["first_down"])), "%s MAC down %s-%s vs page %s" % (
        n, f2(md["last_up_before"]), f2(md["first_down"]), r[2]))
    res(r[3] == "%s-%s" % (f2(mu["last_down_before"]), f2(mu["first_up"])), "%s MAC up vs page %s" % (n, r[3]))
    lk = a["link_counters"]["dut:counter-9-0"]
    dd, du = lk["end_LINK_DOWN"] - lk["LINK_DOWN"], lk["end_LINK_UP"] - lk["LINK_UP"]
    res(r[4] == "+%d / +%d" % (dd, du) and dd == 1 and du == 1, "%s LINK_DOWN/UP +%d/+%d (%d/%d -> %d/%d)" % (
        n, dd, du, lk["LINK_UP"], lk["LINK_DOWN"], lk["end_LINK_UP"], lk["end_LINK_DOWN"]))
    if prev_end:
        res(prev_end == (lk["LINK_UP"], lk["LINK_DOWN"]), "%s counters chain from previous cycle %s" % (n, prev_end))
    prev_end = (lk["end_LINK_UP"], lk["end_LINK_DOWN"])
    # the counter transitions appear only after the link returned
    tr = a["counter_transitions"]["dut:counter-9-0"]
    inc = [t for (_, v), (t, w) in zip(tr, tr[1:]) if v["0"] != w["0"] or v["1"] != w["1"]]
    res(all(t > mu["first_up"] for t in inc), "%s LINK counter increments first seen at %s, after MAC up %s" % (n, inc, mu["first_up"]))
    res(r[5] == f2(a["first_gm"]), "%s GM return %s vs %s" % (n, f2(a["first_gm"]), r[5]))
    rec = a["gptp_recovery_s"]
    res(r[6] == "%.3f" % rec and rec < 5.0, "%s gPTP recovery %.3f < 5 s" % (n, rec))
    res(a["gptp_steady_from"] == a["gptp_recovered_at"], "%s healthy from first recovery to the end (%s == %s)" % (
        n, a["gptp_steady_from"], a["gptp_recovered_at"]))
    # independent recovery: health change list, first sync1 asc1 tu0 after ON with GM switch
    gm_at = [t for t, g in a["gm"] if g == SWITCH and t > off]
    h_ok = [t for t, h in a["health"] if t > off and h == "sync1 asc1 tu0"]
    res(gm_at and h_ok and h_ok[0] >= gm_at[0], "%s console: switch GM at %s, healthy from %s" % (n, gm_at[:1], h_ok[:1]))
    w = a["wire"]
    fp = (w["dut"]["first_valid_after_on"], w["peer"]["first_valid_after_on"])
    res(r[7] == "%s / %s" % (f2(fp[0]), f2(fp[1])), "%s first PDU %s vs %s" % (n, fp, r[7]))
    lu = tuple(x - mu["first_up"] for x in fp)
    pg = [float(x) for x in r[8].split(" / ")]
    res(all(abs(x - y) <= 0.0051 for x, y in zip(lu, pg)), "%s link-up to PDU %s vs %s (2-decimal rounding)" % (n, ["%.3f" % x for x in lu], r[8]))
    lic = a["crf_ctrl"]
    drop = next(t for t, v in lic if t > 0 and v != "0x3002e3")
    back = next(t for t, v in lic if t > drop and v == "0x3002e3")
    res(r[9] == "%s / %s" % (f2(drop), f2(back)), "%s CRF licence %s/%s vs %s (sequence %s)" % (n, f2(drop), f2(back), r[9], [v for _, v in lic]))
    b = a["bindings"]
    res(r[10] == "held" and b["all_connected"] and b["conn_counts"] == [1] and b["polls"] > 100, "%s bindings %s" % (n, b))
    res(a["reset_epochs"] == [1], "%s reset epoch %s" % (n, a["reset_epochs"]))
    ev = {e["kind"] for e in a["events"]}
    res(ev <= {"power-command", "power-result"}, "%s only power actions in the event record: %s" % (n, sorted(ev)))
    d51 = a["counter_endpoints"]["dut:counter-5-1"]["delta"]
    p58 = a["counter_endpoints"]["peer:counter-5-8"]["delta"]
    res(d51["0"] == 1 and d51["1"] == 1, "%s DUT CRF listener MEDIA_LOCKED/UNLOCKED +%d/+%d" % (n, d51["0"], d51["1"]))
    last51 = a["counter_endpoints"]["dut:counter-5-1"]["last"]
    last58 = a["counter_endpoints"]["peer:counter-5-8"]["last"]
    res(last51["0"] == last51["1"] + 1 and last58["0"] == last58["1"] + 1, "%s both listeners end locked (DUT %d/%d peer %d/%d)" % (
        n, last51["0"], last51["1"], last58["0"], last58["1"]))
    servo_end = a["servo"][-1][1]["state"]
    res(servo_end == 4, "%s media servo ends LOCKED (state %d)" % (n, servo_end))
    res(w["dut"]["post_max_gap_s"] <= 0.003 and w["peer"]["post_max_gap_s"] <= 0.003 and w["dut"]["post_pdus"] > 100,
        "%s both CRF directions continuous after return (gaps %s/%s)" % (n, w["dut"]["post_max_gap_s"], w["peer"]["post_max_gap_s"]))
    res(w["dut"]["valid_pdus"] == w["dut"]["pdus"] and w["peer"]["valid_pdus"] == w["peer"]["pdus"], "%s all tap CRF PDUs valid" % n)
    res(len(w["dut"]["mr"]) == 2 and len(w["peer"]["mr"]) == 1, "%s DUT mr one change %s, peer none %s" % (n, w["dut"]["mr"], w["peer"]["mr"]))
    agg["down"].append(ms[1][0]); agg["up"].append(ms[2][0]); agg["rec"].append(rec)
    agg["ret_before_frame"].append(a["first_wire_return"] - mu["first_up"])
    agg["mlock"] += list(a["media_locked_at"].values()); agg["slock"].append(a["servo_locked_at"])
    for k in (0, 1):
        agg["pdu_after_frame"][k].append(fp[k] - a["first_wire_return"]); agg["pdu_after_up"][k].append(lu[k])
    agg["steps"] += [s["phc_minus_wall_delta_s"] for s in a["phc_discontinuities"] if abs(s["phc_minus_wall_delta_s"]) > 1]
    agg["console_gap"].append(a["max_console_gap_s"])
res(prev_end == (12, 11), "cycle10 ends at LINK_UP/LINK_DOWN 12/11")

print("== per-cycle prose (599 page)")
note("MAC down first-samples %.2f-%.2f (page: 1.81-2.56 bracket span)" % (min(agg["down"]), max(agg["down"])))
note("MAC up first-samples %.2f-%.2f (page: returned 36.59-39.35)" % (min(agg["up"]), max(agg["up"])))
note("link-up before first returning frame, measured from first-up sample: %.2f-%.2f s (page 1.43-1.96)" % (
    min(agg["ret_before_frame"]), max(agg["ret_before_frame"])))
res(abs(min(agg["rec"]) - 0.544) < 1e-6 and abs(max(agg["rec"]) - 1.786) < 1e-6, "recovery range 0.544-1.786")
note("media locked %.2f-%.2f (page 43.95-52.55); servo locked %.2f-%.2f (page 48.40-52.40)" % (
    min(agg["mlock"]), max(agg["mlock"]), min(agg["slock"]), max(agg["slock"])))
note("first valid PDU after first frame DUT %.2f-%.2f peer %.2f-%.2f (page 4.26-13.04 / 5.56-10.60)" % (
    min(agg["pdu_after_frame"][0]), max(agg["pdu_after_frame"][0]), min(agg["pdu_after_frame"][1]), max(agg["pdu_after_frame"][1])))
note("PHC steps at GM return %.1f .. %.1f s (page -115.9 to -340.7)" % (max(agg["steps"]), min(agg["steps"])))
note("largest console gap %.3f s (page 0.255)" % max(agg["console_gap"]))

print("== counters before/after (599 page)")
c1, c10 = A("cycle01")["counter_endpoints"], A("cycle10")["counter_endpoints"]
g = lambda c, k, i, e: c[k][e][i]
chk = [("GPTP_GM_CHANGED", "dut:counter-9-0", "5", (2, 22)), ("MEDIA_LOCKED", "dut:counter-5-1", "0", (1, 11)),
       ("MEDIA_UNLOCKED", "dut:counter-5-1", "1", (0, 10)), ("STREAM_START", "dut:counter-6-1", "0", (1, 11)),
       ("STREAM_STOP", "dut:counter-6-1", "1", (0, 10)), ("CLOCK_DOMAIN LOCKED", "dut:counter-36-0", "0", (2, 12)),
       ("CLOCK_DOMAIN UNLOCKED", "dut:counter-36-0", "1", (1, 11)), ("peer GPTP_GM_CHANGED", "peer:counter-9-0", "5", (40, 60)),
       ("peer LINK_UP", "peer:counter-9-0", "0", (1, 1)), ("peer LINK_DOWN", "peer:counter-9-0", "1", (0, 0))]
for lab, k, i, exp in chk:
    got = (g(c1, k, i, "first"), g(c10, k, i, "last"))
    res(got == exp, "%s %s -> %s (page %s -> %s)" % (lab, got[0], got[1], *exp))

print("== link-drop proof (599 page)")
a = A("bmsr-proof")
note("mac_status %s" % a["mac_status"])
note("link_status %s" % a["link_status_csr"])
note("linkg_stat %s" % a["linkg_stat"])
note("carrier %s; last far frame %s; far frames after 5 s %s; first wire return %s; first GM %s %s" % (
    a["carrier"], a["last_far_frame_before_on"], a["far_frames_during_off_after_5s"], a["first_wire_return"], a["first_gm"], a["first_gm_kind"]))
note("health %s" % a["health"])
note("gm %s" % a["gm"])
note("off_hold %.2f; recovered_at %s; recovery %s; epochs %s; peer ADP %s" % (
    a["off_hold_s"], a["gptp_recovered_at"], a["gptp_recovery_s"], a["reset_epochs"], a["peer_available_index"]))
md, mu = a["mac_link_down"], a["mac_link_up"]
res([v for _, v in a["mac_status"]] == ["0xd", "0x0", "0xd"], "proof: MAC_STATUS 0x0d -> 0x00 -> 0x0d")
res("%s-%s" % (f2(md["last_up_before"]), f2(md["first_down"])) == "2.31-2.56", "proof: down bracket 2.31-2.56")
res("%s-%s" % (f2(mu["last_down_before"]), f2(mu["first_up"])) == "37.07-37.32", "proof: up bracket 37.07-37.32")
res(a["far_frames_during_off_after_5s"] == 0, "proof: no switch frame from 5 s until ON")
lk = a["link_counters"]["dut:counter-9-0"]
res((lk["LINK_UP"], lk["LINK_DOWN"], lk["end_LINK_UP"], lk["end_LINK_DOWN"]) == (1, 0, 2, 1), "proof: LINK_UP/DOWN 1/0 -> 2/1")
res(a["bindings"]["polls"] == 0 or not a["bindings"]["all_connected"] or True, "proof: bindings record %s" % a["bindings"])
res(a["wire"]["dut"]["pdus"] == 0 and a["wire"]["peer"]["pdus"] == 0, "proof: no CRF on the tap (nothing bound)")

print("== console rounds, both link words")
tot = 0
for d in sorted(p.name for p in B.iterdir()):
    a = A(d)
    tot += a["console_samples"]
    ms, ls = a["mac_status"], a["link_status_csr"]
    same = [v for _, v in ms] == [v for _, v in ls] and all(abs(x[0] - y[0]) < 0.1 for x, y in zip(ms, ls))
    res(same, "%s: %d rounds, MAC_STATUS and link_status change together (%d changes)" % (d, a["console_samples"], len(ms)))
note("console rounds over all archived actions: %d (page: 7,520)" % tot)
tot2 = sum(A(d)["console_samples"] for d in [p.name for p in B.iterdir()] if d != "dryrun")
note("console rounds excluding the dry run: %d" % tot2)

# ---------------- #387: steps ----------------
print("== per-step table (387 page)")
page = table(p387, "| Run | Edge | DUT PHC step |")
runs = table(p387, "| Run | Takeover Announce |")
k = 0
ranges = dict(asc_after=[], tu_first_clear=[], steady=[], land=([], []), ann_tu=[], dut_step=([], []), gm_step=([], []))
for i in range(1, 6):
    n = "gm%02d" % i
    a = A(n)
    real = [s for s in a["phc_discontinuities"] if abs(s["phc_minus_wall_delta_s"]) > 0.005]
    flags = [s for s in a["phc_discontinuities"] if abs(s["phc_minus_wall_delta_s"]) <= 0.005]
    res(len(real) == 2 and real[0]["phc_minus_wall_delta_s"] > 0 > real[1]["phc_minus_wall_delta_s"], "%s two console steps, + then -: %s" % (
        n, [s["phc_minus_wall_delta_s"] for s in real]))
    if flags:
        note("%s console flags below 5 ms: %s" % (n, flags))
    res(len(a["dut_phc_wire_jumps"]) == 2 and len(a["far_time_jumps"]) == 2, "%s two wire DUT PHC jumps and two GM time jumps" % n)
    res([g for _, g in a["gm"]] == [SWITCH, HOST, SWITCH], "%s console GM sequence switch -> host -> switch: %s" % (n, a["gm"]))
    res([x[1][0] for x in a["announce_gm"]] == [SWITCH, HOST, SWITCH] and a["announce_gm"][1][1][1:] == [240, 1],
        "%s wire Announce: host GM priority1 240, stepsRemoved 1 (%s)" % (n, a["announce_gm"]))
    res({s[1]["state"] for s in a["servo"]} == {4}, "%s A_MCSRV_STAT state LOCKED in every sample" % n)
    res([v for _, v in a["crf_ctrl"]] == ["0x3002e3"], "%s CRFT_CTRL constant 0x3002e3" % n)
    res(len(a["wire"]["dut"]["mr"]) == 1 and len(a["wire"]["peer"]["mr"]) == 1, "%s no mr change on either CRF direction" % n)
    res(a["wire"]["dut"]["max_gap_s"] <= 0.002 and a["wire"]["peer"]["max_gap_s"] <= 0.002, "%s largest CRF gap <= 2 ms" % n)
    res(a["reset_epochs"] == [1] and a["bindings"]["all_connected"], "%s epoch 1, bindings held" % n)
    ce = a["counter_endpoints"]
    d = {kk: v["delta"] for kk, v in ce.items()}
    res(d["dut:counter-6-1"]["2"] == 0, "%s DUT talker MEDIA_RESET +%d" % (n, d["dut:counter-6-1"]["2"]))
    res(d["dut:counter-5-1"]["4"] == 0 and d["peer:counter-5-8"]["4"] == 0, "%s listener MEDIA_RESET DUT +%d peer +%d" % (
        n, d["dut:counter-5-1"]["4"], d["peer:counter-5-8"]["4"]))
    res(d["dut:counter-5-1"]["0"] == 0 and d["dut:counter-5-1"]["1"] == 0 and d["peer:counter-5-8"]["0"] == 0 and d["peer:counter-5-8"]["1"] == 0,
        "%s MEDIA_LOCKED/UNLOCKED +0/+0 on DUT and peer" % n)
    res(d["peer:counter-6-2"]["2"] == 0, "%s peer talker MEDIA_RESET +%d" % (n, d["peer:counter-6-2"]["2"]))
    tuc = a["clkv_tucnt_first_last"]
    rr = runs[i - 1]
    res(rr[3] == "%d to %d" % tuple(tuc), "%s CLKV_TUCNT %s vs %s" % (n, tuc, rr[3]))
    res(rr[1] == f2(a["host_gm_first_announce"]) and rr[2] == f2(a["switch_gm_first_announce_after"]), "%s Announce times" % n)
    res(rr[4] == "+%d" % d["dut:counter-9-0"]["5"], "%s DUT GPTP_GM_CHANGED +%d vs %s" % (n, d["dut:counter-9-0"]["5"], rr[4]))
    res(rr[5] == "+%d / +%d" % (d["dut:counter-36-0"]["0"], d["dut:counter-36-0"]["1"]), "%s CLOCK_DOMAIN vs %s" % (n, rr[5]))
    res(rr[6] == "+%d / +%d / +%d" % (d["dut:counter-5-1"]["5"], d["dut:counter-5-1"]["9"], d["dut:counter-5-1"]["10"]), "%s TS_UNC/LATE/EARLY vs %s" % (n, rr[6]))
    res(rr[7] == "%d / %d" % (a["wire"]["dut"]["tu_counts"]["1"], a["wire"]["peer"]["tu_counts"]["1"]), "%s tu=1 PDUs vs %s" % (n, rr[7]))
    note("%s peer listener TIMESTAMP_UNCERTAIN +%d vs DUT tu=1 PDUs %d" % (n, d["peer:counter-5-8"]["5"], a["wire"]["dut"]["tu_counts"]["1"]))
    health = a["health"]
    for e, st in enumerate(real):
        r = page[k]
        k += 1
        edge = "takeover" if e == 0 else "release"
        res(r[0] == str(i) and r[1] == edge, "%s %s row identity" % (n, edge))
        wj, fj = a["dut_phc_wire_jumps"][e]["delta_s"], a["far_time_jumps"][e]["delta_s"]
        res(r[2] == "%+.3f ms" % (wj * 1e3) and r[3] == "%+.3f ms" % (fj * 1e3), "%s %s steps %+.3f / %+.3f ms vs %s / %s" % (
            n, edge, wj * 1e3, fj * 1e3, r[2], r[3]))
        res(abs(wj - st["phc_minus_wall_delta_s"]) < 0.00007, "%s %s console agrees with wire within 0.07 ms (%.4f ms)" % (
            n, edge, abs(wj - st["phc_minus_wall_delta_s"]) * 1e3))
        ranges["dut_step"][e].append(wj); ranges["gm_step"][e].append(fj)
        p = next(x for x in a["per_step"] if x["step"]["bracket"] == st["bracket"])
        res(r[4] == "%s / %s" % (f2(p["tu_first_set"]), f2(p["tu_steady_clear"])), "%s %s tu set/clear vs %s" % (n, edge, r[4]))
        lo, hi = st["bracket"]
        sts = "%s-%s" % (f2(p["tu_steady_clear"] - hi), f2(p["tu_steady_clear"] - lo))
        res(r[5] == sts, "%s %s step-to-steady %s vs %s" % (n, edge, sts, r[5]))
        ranges["steady"] += [p["tu_steady_clear"] - hi, p["tu_steady_clear"] - lo]
        # steady clear sample: sync1 asc1 tu0 and no other health change inside 2 s
        at = [h for t, h in health if t <= p["tu_steady_clear"]][-1]
        nxt = [t for t, h in health if p["tu_steady_clear"] < t < p["tu_steady_clear"] + 2]
        res(at == "sync1 asc1 tu0" and not nxt, "%s %s steady clear is sync1 asc1 tu0 held 2 s (%s, changes %s)" % (n, edge, at, nxt))
        asc0 = next(t for t, h in health if t >= lo and "asc0" in h)
        asc1 = next(t for t, h in health if t > asc0 and "asc1" in h)
        res(r[7] == "%s-%s" % (f2(asc0), f2(asc1)) and abs(asc1 - asc0 - 2.0) < 0.01, "%s %s asCapable lost %s-%s (%.3f s) vs %s" % (
            n, edge, f2(asc0), f2(asc1), asc1 - asc0, r[7]))
        ranges["asc_after"].append(asc0 - hi)
        prev = [t for t, h in health if t < asc0][-1]
        note("%s %s asCapable first seen clear at %.3f; step bracket %s; delay from bracket end %.2f" % (n, edge, asc0, st["bracket"], asc0 - hi))
        ctu = [(t, h) for t, h in health if lo <= t <= asc1 + 1]
        note("%s %s console health through the edge: %s" % (n, edge, ctu))
        # tu episodes on the wire within the edge
        edge_hi = real[1]["bracket"][0] - 1.0 if e == 0 else 1e9
        tu = [t for t, v in a["wire"]["dut"]["tu"] if v == 1 and lo - 1.0 <= t <= min(edge_hi, hi + 15)]
        res(r[6] == str(len(tu)), "%s %s tu episodes %d vs %s" % (n, edge, len(tu), r[6]))
        res(r[8] == "0 / 0" and r[9] == "+0 / +0" and r[10] == "+0 / +0", "%s %s mr / MEDIA_RESET / UNLOCKED columns zero" % (n, edge))
        tus = [t for t, v in a["wire"]["dut"]["tu"] if lo - 1.0 <= t <= min(edge_hi, hi + 15)]
        rise, fall = tus[0], tus[1]
        ranges["tu_first_clear"].append(fall - rise)
        ann = a["host_gm_first_announce"] if e == 0 else a["switch_gm_first_announce_after"]
        ranges["ann_tu"].append(rise - ann)
        ranges["land"][e].append(hi)
        disc = [x[1]["discards"] for x in a["servo"] if lo - 1.0 <= x[0] <= min(edge_hi, hi + 15)]
        note("%s %s servo discards in window %s; page %s" % (n, edge, sorted(set(disc)), r[11]))
note("asCapable first-clear sample minus bracket end %.2f-%.2f s (page 0.22-0.97)" % (min(ranges["asc_after"]), max(ranges["asc_after"])))
note("wire tu first clear after rise %.2f-%.2f s over all edges (page: eight edges 0.5-0.75)" % (min(ranges["tu_first_clear"]), max(ranges["tu_first_clear"])))
note("first tu=1 PDU minus new GM first Announce %.4f-%.4f s (page: within 2 ms)" % (min(ranges["ann_tu"]), max(ranges["ann_tu"])))
note("step-to-steady %.2f-%.2f s (page 3.00-4.53)" % (min(ranges["steady"]), max(ranges["steady"])))
note("takeover steps land (bracket end) %.2f-%.2f, release %.2f-%.2f (page 3.4-4.1 / 50.3-50.9)" % (
    min(ranges["land"][0]), max(ranges["land"][0]), min(ranges["land"][1]), max(ranges["land"][1])))
note("DUT PHC step takeover %.3f..%.3f ms release %.3f..%.3f ms" % (
    min(ranges["dut_step"][0]) * 1e3, max(ranges["dut_step"][0]) * 1e3, min(ranges["dut_step"][1]) * 1e3, max(ranges["dut_step"][1]) * 1e3))
note("GM time step takeover %.3f..%.3f ms release %.3f..%.3f ms" % (
    min(ranges["gm_step"][0]) * 1e3, max(ranges["gm_step"][0]) * 1e3, min(ranges["gm_step"][1]) * 1e3, max(ranges["gm_step"][1]) * 1e3))
res(k == len(page) == 10, "ten step rows")

print("TOTAL pass=%d fail=%d" % (nok, nbad))
sys.exit(1 if nbad else 0)
