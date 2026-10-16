"""Lane B19 quick recovery check after one OUT4 cycle or software-GM run, before the next starts.

exit 0 = the DUT is healthy to the end (the last 40 console samples name the switch with sync 1,
asCapable 1, tu 0), it never restarted (RST_EPOCH 1, largest console gap under 2 s), every polled
binding reads connected at its last poll, and with the CRF pair polled the DUT's CRF is on the wire
in the last 10 s of the tap; 3 = not.  usage: cyc_check.py <name>
"""
from pathlib import Path
import json, re, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wire_summary import records, decode

name = sys.argv[1]
root = Path("/tmp/a624/raw") / name
load = lambda n: [json.loads(l) for l in (root / n).read_text().splitlines() if l.strip()]
console, ctrl = load("console.jsonl"), load("controller.jsonl")
sts = [(r["t"], dict(re.findall(r"(\w+)=([a-zA-Z0-9_]+)", r["raw"]))) for r in console if r["cmd"] == "milan_status"]
sts = [(t, d) for t, d in sts if "SYNC" in d]
ep = {m[1] for r in console if r["cmd"] == "mem_read 0x90000720 4" for m in [re.search(r"0x90000720  ([0-9a-f]{2})", r["raw"])] if m}
gap = max(b[0] - a[0] for a, b in zip(sts, sts[1:]))
tail = all(d["SYNC"] == "1" and d["ASCAPABLE"] == "1" and d["TU"] == "0" and d["GPTP_GM"] == "3cc0c6fffefe0210" for _, d in sts[-40:])
last = {}
for r in ctrl:
    if str(r.get("what", "")).startswith("state-"):
        last[(r["role"], r["what"])] = r["response"]
bound = {f"{k[0]}:{k[1]}": (v.get("status"), v.get("conn_count")) for k, v in last.items()}
crf_polled = ("peer", "state-5-8") in last
wire_ok = True
if crf_polled:
    recs = list(records(str(root / "tap.pcap")))
    end = recs[-1]["tap_ns"]
    n = sum(1 for r in recs if r["port"] == 3 and end - r["tap_ns"] < 10e9 and decode(r).get("kind") == "CRF")
    wire_ok = n > 4000
else:
    n = None
ok = tail and ep == {"01"} and gap < 2 and all(v == (0, 1) for v in bound.values()) and wire_ok
print(json.dumps(dict(name=name, samples=len(sts), tail_healthy=tail, epochs=sorted(ep), max_console_gap_s=round(gap, 3),
                      bindings=bound, crf_last_10s=n)))
print("RECOVERED" if ok else "NOT_RECOVERED")
sys.exit(0 if ok else 3)
