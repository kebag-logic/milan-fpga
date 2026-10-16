#!/usr/bin/env python3
"""Independent re-derivation of the software-grandmaster step figures from the raws.
Usage: probe_gm.py RAW_ROOT
Per run: console samples (count, asCapable 0, PDELAY range), every console tu
rise/fall from the full history (times at command send, s after gm-start),
DUT GET_AVB_INFO polls (answered, unanswered, as_capable 0, pdelay range)."""
import json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
tot = dict(samples=0, asc0=0, polls=0, polls_unans=0, polls_asc0=0)
pd_all, ppd_all = [], []
for i in range(1, 6):
    d = root / f"gm{i:02d}"
    ev = [json.loads(l) for l in open(d / "events.jsonl") if l.strip()]
    t0 = next(e["t"] for e in ev if e["kind"] == "gm-start")
    s = []
    for l in open(d / "console.jsonl"):
        if not l.strip():
            continue
        r = json.loads(l)
        if r["cmd"] != "milan_status":
            continue
        kv = dict(re.findall(r"(\w+)=([0-9A-Za-z]+)", r["raw"]))
        if "TU" not in kv:
            continue
        s.append((r["t"] - t0, r["end"] - t0, kv["SYNC"], kv["ASCAPABLE"], kv["TU"], int(kv["PDELAY_NS"])))
    trans = [(round(s[k][0], 3), s[k - 1][4] + "->" + s[k][4]) for k in range(1, len(s)) if s[k][4] != s[k - 1][4]]
    pd = [x[5] for x in s]
    asc0 = sum(x[3] != "1" for x in s)
    # steady clear: first sample after each rise from which sync1 asc1 tu0 hold for 2 s
    steady = []
    for t, tr in trans:
        if tr == "0->1":
            k = next(k for k in range(len(s)) if round(s[k][0], 3) == t)
            for j in range(k + 1, len(s)):
                ok = lambda x: x[2] == "1" and x[3] == "1" and x[4] == "0"
                win = [x for x in s[j:] if x[0] < s[j][0] + 2.0]
                if all(ok(x) for x in win):
                    steady.append(round(s[j][0], 3)); break
    polls = []
    for l in open(d / "controller.jsonl"):
        if not l.strip():
            continue
        r = json.loads(l)
        if r.get("role") == "dut" and r.get("what") == "avb":
            polls.append(r)
    ans = [p for p in polls if isinstance(p.get("response"), dict) and p["response"].get("status") == "SUCCESS" and "decoded" in p["response"]]
    pasc0 = sum(p["response"]["decoded"]["as_capable"] != 1 for p in ans)
    ppd = [p["response"]["decoded"]["pdelay_ns"] for p in ans]
    print(f"gm{i:02d} samples={len(s)} asc0={asc0} pdelay={min(pd)}..{max(pd)} tu_transitions={trans} steady_clear={steady} "
          f"polls={len(polls)} answered={len(ans)} poll_asc0={pasc0} poll_pdelay={min(ppd)}..{max(ppd)}")
    tot["samples"] += len(s); tot["asc0"] += asc0; tot["polls"] += len(ans); tot["polls_unans"] += len(polls) - len(ans); tot["polls_asc0"] += pasc0
    pd_all += pd; ppd_all += ppd
print("TOTAL", tot, f"console_pdelay={min(pd_all)}..{max(pd_all)} poll_pdelay={min(ppd_all)}..{max(ppd_all)}")
