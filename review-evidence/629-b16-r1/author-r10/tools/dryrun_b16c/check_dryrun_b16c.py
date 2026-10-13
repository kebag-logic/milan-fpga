#!/usr/bin/env python3
"""B16c dry run checker: the order of the state-changing requests and the end state against what each scenario
must give. usage: check_dryrun_b16c.py <scenario_dir> <scenario> <rc> <out.json>"""
import json
import sys
from pathlib import Path

T, S, RC, OUT = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3]), sys.argv[4]
ops = [json.loads(x) for x in open(T / "fake/ops.jsonl")] if (T / "fake/ops.jsonl").exists() else []
model = json.load(open(T / "fake/model.json")) if (T / "fake/model.json").exists() else {}
ev = [json.loads(x) for x in open(T / f"pk/runs/dry-{S}/events.jsonl")]
kinds = [e["kind"] for e in ev]
seq = [(o["op"], o.get("who") or o.get("l"), o.get("src", o.get("lu"))) for o in ops]
final = next((e for e in ev if e["kind"] == "final"), {})
checks = {}
end_ok = model.get("clk") == {"dut": 0, "peer": int(1 if S != "peer0" else 0)} and model["rx"]["dut-0"] is None \
    and model["rx"]["dut-1"] is None and model["rx"]["peer-0"] and model["rx"]["peer-8"]
checks["end state as found (clocks, DUT unbound, peer listeners bound)"] = bool(end_ok)
if S in ("bcrf", "baaf", "term"):
    src = 2 if S == "baaf" else 1
    want = [("setclk", "peer", 0), ("bind", "dut", 1), ("bind", "dut", 0), ("setclk", "dut", src),
            ("setclk", "dut", 0), ("unbind", "dut", 0), ("unbind", "dut", 1), ("setclk", "peer", 1)]
    checks["order: peer INTERNAL, binds, DUT set; DUT restored, unbinds, peer restored"] = seq == want
    checks["final read-back equal to found"] = final.get("equal_to_found") is True
    checks["servo LOCKED event"] = any(e["kind"] == "servo-state" and e.get("s_hi") is not None for e in ev)
    checks["window marks 0, 1, 2 and after-restore"] = all(any(e["kind"] == "mark" and e["tag"] == t for e in ev)
                                                          for t in ("window-mark-0", "after-restore"))
    checks["poll summary present"] = "poll-summary" in kinds
    checks["tone summary present"] = "tone-summary" in kinds
    if S == "term":
        checks["aborted by the signal"] = any(e["kind"] == "abort" and "signal 15" in e.get("error", "") for e in ev)
        checks["rc nonzero"] = RC != 0
    else:
        checks["rc 0"] = RC == 0
        checks["window marks 1 and 2"] = all(any(e["kind"] == "mark" and e["tag"] == t for e in ev)
                                             for t in ("window-mark-1", "window-mark-2"))
elif S in ("refuse", "nolock"):
    want = [("setclk", "peer", 0), ("bind", "dut", 1), ("bind", "dut", 0), ("setclk", "dut", 1),
            ("setclk", "dut", 0), ("unbind", "dut", 0), ("unbind", "dut", 1), ("setclk", "peer", 1)]
    checks["order, and every change restored"] = seq == want
    checks["no capture started"] = "captures-started" not in kinds
    checks["final read-back equal to found"] = final.get("equal_to_found") is True
    checks["rc nonzero"] = RC != 0
elif S == "music":
    want = [("setclk", "peer", 0), ("setclk", "peer", 1)]
    checks["peer set, music found before the binds, peer restored; nothing bound"] = seq == want
    checks["WAIT reported"] = any(e["kind"] == "abort" and "WAIT" in e.get("error", "") for e in ev)
    checks["final read-back equal to found"] = final.get("equal_to_found") is True
elif S == "agentdies":
    want = [("setclk", "peer", 0), ("bind", "dut", 1), ("unbind", "dut", 1), ("setclk", "peer", 1)]
    checks["peer set, CRF bind; the agent ends; a new agent unbinds and restores the peer"] = seq == want
    checks["agent restarted"] = any(e["kind"] == "agent-restart" for e in ev)
    checks["final read-back equal to found"] = final.get("equal_to_found") is True
    checks["rc nonzero"] = RC != 0
elif S == "peer0":
    checks["nothing changed"] = seq == []
    checks["refused"] = any(e["kind"] == "abort" and "as found" in e.get("error", "") for e in ev)
res = dict(scenario=S, rc=RC, ops=seq, checks=checks, verdict="PASS" if all(checks.values()) else "FAIL")
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps(dict(scenario=S, verdict=res["verdict"], failed=[k for k, v in checks.items() if not v])))
