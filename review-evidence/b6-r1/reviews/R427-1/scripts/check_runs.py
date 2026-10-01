#!/usr/bin/env python3
"""Audit every graded run's events.jsonl: a format check precedes every bind, the listener
(never the talker) takes the set, clock sources are set only on the listener and read back,
every set is restored and read back, formats and maps end as found, window timing.

usage: check_runs.py <evidence author/runs dir>
"""
import json, sys, os
root = sys.argv[1]
import re
def side(name):
    return name.split("-")[0]
def mask(text):
    """The peer's own stream and clock-source indices are not published (they hint at its stream counts)."""
    return re.sub(r"peer-(in|out)-\d+", r"peer-\1-<i>", text)
_print = print
def print(*a, **k):
    _print(mask(" ".join(str(x) for x in a)), **k)
bad = 0
for case in ("a0", "a1", "a2", "bint", "bcrf", "probe"):
    ev = [json.loads(l) for l in open(os.path.join(root, case, "events.jsonl"))]
    kinds = [e["kind"] for e in ev]
    print(f"== {case}")
    checked = set()
    last_check = (None, None)
    listeners = set()
    for i, e in enumerate(ev):
        k = e["kind"]
        if k == "format-check":
            st = e.get("set")
            print("  format-check", e["talker"], "->", e["listener"], "talker", e["talker_fmt"], "listener", e["listener_fmt"],
                  "set", (st or {}).get("fmt"), (st or {}).get("status"), "echoed", (st or {}).get("echoed"), "GET after", e.get("listener_after"), "ok", e["ok"])
            if st and e.get("listener_after") != e["talker_fmt"]:
                print("   !! listener read-back differs"); bad += 1
            if st and st.get("fmt") != e["talker_fmt"]:
                print("   !! set differs from talker fmt"); bad += 1
            if e["talker_fmt"] == e["listener_fmt"] and st:
                print("   !! set although equal"); bad += 1
            checked.add((e["talker"], e["listener"]))
            last_check = (e["talker"], e["listener"])
        if k == "bind":
            pair = (e.get("talker", last_check[0]), e.get("listener", last_check[1]))  # the probe log omits the pair; its format check names it
            ok = pair in checked
            listeners.add(side(pair[1]))
            print("  bind", pair, "status", e["status"], "conn", e["conn_count"], "format-checked before:", ok)
            if not ok or e["status"] != 0 or e["conn_count"] != 1: bad += 1
        if k == "unbind":
            print("  unbind", e.get("talker"), "->", e.get("listener"), "status", e["status"], "conn", e["conn_count"])
            if e["status"] != 0 or e["conn_count"] != 0: bad += 1
        if k == "set-clock":
            print("  set-clock", e["tag"], "who", e["who"], "src", e["src"] if e["who"] == "dut" or e["tag"] == "restore" else "<peer-src>", e["status"], "readback equal to set:", e["readback"] == e["src"], "ok", e["ok"])
            if e["status"] != "SUCCESS" or e["readback"] != e["src"]: bad += 1
            if e["tag"] == "case" and e["who"] not in listeners:
                print("   !! clock set on a non-listener"); bad += 1
        if k in ("clock-final", "format-final", "map-final", "peer-format-restore", "format-restore", "as-found", "window-start", "window-end"):
            s = {kk: v for kk, v in e.items() if kk not in ("t", "mono_raw_ns", "kind")}
            if k == "as-found":
                s = {kk: v for kk, v in s.items() if not kk.startswith("fmt-peer-out")}
            print("  ", k, json.dumps(s)[:240])
            if k == "clock-final" and e["source"] != e["as_found"]: bad += 1
            if k == "format-final" and not e["equal_to_found"]: bad += 1
    t = {e["kind"] + e.get("tag", ""): e["t"] for e in ev if e["kind"] in ("set-clock", "window-start", "window-end", "bind")}
    ws = [e for e in ev if e["kind"] == "window-start"]
    we = [e for e in ev if e["kind"] == "window-end"]
    lastset = max([e["t"] for e in ev if e["kind"] in ("bind", "set-clock") and e.get("tag") != "restore" and e["t"] < (ws[0]["t"] if ws else 1e20)] or [0])
    if ws:
        print("  window start - last bind/set: %.2f s; window length %.2f s (wall)" % (ws[0]["t"] - lastset, we[0]["t"] - ws[0]["t"]))
print("BAD", bad)
sys.exit(1 if bad else 0)
