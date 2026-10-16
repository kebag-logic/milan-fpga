"""Lane B19 box 4: the #729 per-AVTPDU counter rule against the wire, over one observe action; no bench access.

usage: avtpdu_parity.py <name>   reads /tmp/a624/raw/<name>, writes bench/<name>/avtpdu-parity.json
FRAMES_TX of the DUT's CRF talker (STREAM_OUTPUT 1) between its first and last poll is compared with the
CRF AVTPDUs the tap saw from the DUT in the same window (polls placed on the tap clock through the
controller host's measured offset, lane B1's method; each window edge is uncertain by the poll's round
trip and that offset, so the expected difference is a few PDUs). The AAF counters are compared across
the two ends instead (the capture drops AAF): the DUT's AAF FRAMES_TX against the peer's FRAMES_RX on
its input 0, and the peer's AAF FRAMES_TX against the DUT's FRAMES_RX on input 0, as rates.
"""
from pathlib import Path
import json, statistics, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wire_summary import records, decode

name = sys.argv[1]
root = Path("/tmp/a624/raw") / name
out = Path(__file__).resolve().parent.parent / "bench" / name
load = lambda n: [json.loads(l) for l in (root / n).read_text().splitlines() if l.strip()]
events, ctrl = load("events.jsonl"), load("controller.jsonl")
off = lambda role: (lambda r: r["remote"] - (r["t0"] + r["t1"]) / 2)(min((e for e in events if e["kind"] == "clock" and e["role"] == role), key=lambda e: e["t1"] - e["t0"]))
co, to = off("controller"), off("tap")
series = {}
for r in ctrl:
    if r.get("what", "").startswith("counter-") and r["response"].get("status") == "SUCCESS":
        series.setdefault(f"{r['role']}:{r['what']}", []).append((r["t"] - co, r["response"]["counters"]))
raw = list(records(str(root / "tap.pcap")))
anchor = statistics.median((x["host_ns"] - x["tap_ns"]) / 1e9 for x in raw)
crf_t = sorted(x["tap_ns"] / 1e9 + anchor - to for x in raw if x["port"] == 3 and decode(x).get("kind") == "CRF")
s = series["dut:counter-6-1"]
(t0, c0), (t1, c1) = s[0], s[-1]
wire = sum(1 for t in crf_t if t0 < t <= t1)
S = dict(name=name, window_s=round(t1 - t0, 3), crf_frames_tx_delta=c1["4"] - c0["4"], crf_wire_pdus=wire,
         difference=(c1["4"] - c0["4"]) - wire)


def rate(key, idx):
    a = series[key]
    (ta, ca), (tb, cb) = a[0], a[-1]
    return round((cb[idx] - ca[idx]) / (tb - ta), 2)


S["rates_per_s"] = {"DUT AAF talker FRAMES_TX": rate("dut:counter-6-0", "4"), "peer AAF listener (input 0) FRAMES_RX": rate("peer:counter-5-0", "11"),
                    "peer AAF talker FRAMES_TX": rate("peer:counter-6-0", "4"), "DUT AAF listener (input 0) FRAMES_RX": rate("dut:counter-5-0", "11"),
                    "DUT CRF talker FRAMES_TX": rate("dut:counter-6-1", "4"), "peer CRF listener (input 8) FRAMES_RX": rate("peer:counter-5-8", "11")}
out.mkdir(parents=True, exist_ok=True)
(out / "avtpdu-parity.json").write_text(json.dumps(S, indent=1) + "\n")
print(json.dumps(S, indent=1))
