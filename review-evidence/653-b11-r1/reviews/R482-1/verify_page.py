#!/usr/bin/env python3
"""Recompute every per-cycle column and every aggregate the page states from the
public evidence: the grader JSON, the provided decoder's outputs (timing rebuilt
from its swapped words), and the probe log. Prints one line per check."""
import json, re, sys
from pathlib import Path
page = Path(sys.argv[1]).read_text(encoding="utf-8")
A = Path(sys.argv[2])  # .../review-evidence/653-b11-r1/author
G = json.loads((A / "summary/o653-grade.json").read_text())
fails = 0
def chk(name, ok, detail=""):
    global fails
    fails += not ok
    print(("PASS " if ok else "FAIL ") + name + (" :: " + detail if detail else ""))

cyc = {k.split("/")[1]: v for k, v in G.items() if not k.endswith("_session")}
rows = re.findall(r"^\| (C0 \(control\)|A\d\d|R\d\d) \| (.*) \|$", page, re.M)
chk("23 per-cycle rows", len(rows) == 23 and len(cyc) == 23, f"{len(rows)} rows, {len(cyc)} graded")
num = lambda s: float(s.replace(",", ""))
for tag, rest in rows:
    t = "C0" if tag.startswith("C0") else tag
    c = rest.split(" | ")
    lib, w = cyc[t]["library"], cyc[t]["wire"]
    exp_in = ("AAF, 0" if lib["listener"] == 0 else "CRF, 1")
    up = w["unlock_push"]; lu = lib["lib_unlock_update"]; po = lib["post"]["counters"]
    got = dict(input=c[0], lock=int(c[1]), hold=int(c[2]), c2r=num(c[3]), r2p=num(c[4]), order=c[5], pair=c[6],
               frames=int(num(c[7])), conn=c[8], flags=c[9], after=c[10], cap=c[11].strip("`"))
    exp = dict(input=exp_in, lock=lib["lock_ms"], hold=lib["hold_ms"], c2r=w["cmd_to_rsp_us"], r2p=w["rsp_to_push_us"],
               order=w["order"], pair=f'{up["ML"]}/{up["MU"]}/{up["SI"]}', frames=w["stream_frames_after_cmd"],
               conn=lu["lib_conn"], flags="none" if not lib["library_flagged"] else "yes",
               after=f'{po["ML"]}/{po["MU"]}/{po["SI"]}', cap=w["sha256"][:12])
    bad = {k: (got[k], exp[k]) for k in got if got[k] != exp[k]}
    chk(f"row {t} equals grader", not bad, str(bad))
    chk(f"row {t} stream sub matches input", w["stream_sub"] == exp_in[:3], w["stream_sub"])
    chk(f"row {t} decoder order agrees", w["decoder_order"] == w["order"] == "RESPONSE_FIRST" and w["decoder_rc"] == 0)
    chk(f"row {t} unbind SUCCESS, bind Success, tap monotonic", w["unbind_status"] == 0 and lib["bind"] == "Success"
        and lib["unbind"] == "Success" and w["tap_time_monotonic_in_file_order"])
    chk(f"row {t} formats equal, none set", lib["formats"]["equal"] and "set_listener_format" not in lib)
    chk(f"row {t} talker streaming at cmd", w["talker_streaming_at_cmd"])
    chk(f"row {t} library order response first", lib["lib_order"] == "RESPONSE_FIRST")
    chk(f"row {t} post state", lib["post"]["conn"] == "NotConnected" and lib["post"]["compat"] == "IEEE17221|Milan"
        and not lib["post"]["events_new"] and not lib["post"]["peer_events_new"] and lib["result"] == "OK")

aaf = [cyc[k] for k in cyc if cyc[k]["library"]["listener"] == 0]
crf = [cyc["R01"], cyc["R02"]]
rng = lambda xs: (min(xs), max(xs))
print("AAF rsp->push", rng([c["wire"]["rsp_to_push_us"] for c in aaf]))
print("AAF frames after cmd", rng([c["wire"]["stream_frames_after_cmd"] for c in aaf]))
print("AAF last frame after cmd ms", rng([c["wire"]["last_stream_frame_after_cmd_ms"] for c in aaf]))
print("CRF last frame after cmd ms", [c["wire"]["last_stream_frame_after_cmd_ms"] for c in crf])
nc = [round((c["library"]["lib_unlock_update"]["t"] - c["library"]["t_lib_notconnected"]), 0) for c in aaf]
print("AAF lib NotConnected->unlock update us", rng(nc))
print("AAF lib unbind issue->unlock update ms", rng([c["library"]["lib_unlock_after_unbind_ms"] for c in aaf]))
print("CRF lib 1/0 window ms", [c["library"]["lib_held_1_0_after_unbind_ms"] for c in crf])
print("C0 own rsp->cmd us", cyc["C0"]["wire"]["control"])
print("frames between rsp and push", {k: cyc[k]["wire"]["frames_between"] for k in cyc if cyc[k]["wire"]["frames_between"] != ["DUT->sw UNSOL GET_STREAM_INFO RSP"]})
print("all cmd->rsp", sorted({c["wire"]["cmd_to_rsp_us"] for c in cyc.values()}))
print("lock ms set", sorted({c["library"]["lock_ms"] for c in cyc.values()}))
chk("aggregate AAF rsp->push 114.2..116.8", rng([c["wire"]["rsp_to_push_us"] for c in aaf]) == (114.2, 116.8))
chk("aggregate AAF frames 303..1562", rng([c["wire"]["stream_frames_after_cmd"] for c in aaf]) == (303, 1562))
chk("aggregate AAF last frame 37.8..195.2 ms", tuple(round(x, 1) for x in rng([c["wire"]["last_stream_frame_after_cmd_ms"] for c in aaf])) == (37.8, 195.2))
chk("aggregate CRF last frame 35.7, 63.3 ms (page lists ascending, not per run)", sorted([round(c["wire"]["last_stream_frame_after_cmd_ms"], 1) for c in crf]) == [35.7, 63.3])
chk("aggregate AAF NotConnected->update 51..113 us", (round(min(nc)), round(max(nc))) == (51, 113), str(rng(nc)))
chk("aggregate AAF unbind->update 0.9..5.2 ms", tuple(round(x, 1) for x in rng([c["library"]["lib_unlock_after_unbind_ms"] for c in aaf])) == (0.9, 5.2))
chk("aggregate CRF 1/0 window 95.0, 100.0 ms", [round(c["library"]["lib_held_1_0_after_unbind_ms"], 1) for c in crf] == [95.0, 100.0])
chk("C0 control COUNTERS_FIRST vs own, own 1/0/0, 1629.8 us", cyc["C0"]["wire"]["control"] == {"own_counters": {"ML": 1, "MU": 0, "SI": 0}, "order_vs_own": "COUNTERS_FIRST", "own_rsp_to_cmd_us": 1629.8})
chk("R01 has GET_AVB_INFO between", any("GET_AVB_INFO" in x or "0x27" in x for x in cyc["R01"]["wire"]["frames_between"]))
chk("CRF rsp->push 99346.2, 99731.4", [c["wire"]["rsp_to_push_us"] for c in crf] == [99346.2, 99731.4])
print("FAILS", fails)
sys.exit(1 if fails else 0)
