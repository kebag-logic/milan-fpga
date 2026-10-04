#!/usr/bin/env python3
"""Independent of the grader: re-read the probe logs (s0b, s1) for the library's
reports: any flag-type event anywhere in the session, Milan flag on every update,
connection-before-counters order per cycle, the pair held after, and the 1/0 window."""
import collections, json, sys
from pathlib import Path
A = Path(sys.argv[1])
FLAG = {"compat_changed", "diagnostics", "query_error", "unsol_loss", "aecp_timeout", "aecp_unexpected",
        "transport_error", "offline", "unsol_registration"}
fails = 0
for s in ("s0b", "s1"):
    ev = [json.loads(l) for l in (A / f"runs/{s}/{s}-probe.jsonl").read_text().splitlines() if l.startswith("{")]
    kinds = collections.Counter(e["ev"] for e in ev)
    flagged = [e for e in ev if e["ev"] in FLAG]
    nonmilan = [e for e in ev if "compat_names" in e and e["compat_names"] != "IEEE17221|Milan"]
    snaps_events = [e for e in ev if e["ev"] == "snapshot" and (e["dut"].get("events_new") or e.get("peer", {}).get("events_new"))]
    print(f"{s}: events={dict(kinds)}")
    print(f"{s}: flag-type events={len(flagged)} non-Milan compat lines={len(nonmilan)} snapshots with new events={len(snaps_events)}")
    fails += bool(flagged or nonmilan or snaps_events)
    cur = None; C = {}
    for e in ev:
        if e["ev"] == "cycle_begin": cur = e["tag"]; C[cur] = dict(li=e["listener_in"], upd=[], nc=None)
        if cur is None: continue
        c = C[cur]
        if e["ev"] == "unbind": c["tu"] = e["t_cmd"]
        if e["ev"] == "si_connection" and e["who"] == "dut" and e["state"] == "NotConnected": c["nc"] = e["t"]
        if e["ev"] == "si_counters" and e["who"] == "dut" and e["idx"] == c["li"]: c["upd"].append(e)
        if e["ev"] == "snapshot" and e["tag"].endswith("-post"): c["post"] = e["dut"]["lib_counters"]
    for tag, c in C.items():
        after = [u for u in c["upd"] if u["t"] > c["tu"]]
        unl = next(u for u in after if u["counters"]["MU"] >= 1)
        between = [u for u in after if u["t"] < unl["t"]]
        ok = (c["nc"] is not None and c["nc"] < unl["t"] and unl["lib_conn"] == "NotConnected"
              and (unl["counters"]["ML"], unl["counters"]["MU"], unl["counters"]["SI"]) == (1, 1, 0)
              and (c["post"]["ML"], c["post"]["MU"], c["post"]["SI"]) == (1, 1, 0) and not between
              and all(u["counters"]["ML"] == u["counters"]["MU"] for u in after))
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} {s}/{tag} in{c['li']} NotConnected->unlock update {(unl['t']-c['nc'])/1e3:.3f} ms; "
              f"unbind issue->update {(unl['t']-c['tu'])/1e3:.3f} ms; updates after unbind={len(after)}, before the unlock one={len(between)}; post={c['post']['ML']}/{c['post']['MU']}/{c['post']['SI']}")
print("FAILS", fails); sys.exit(1 if fails else 0)
