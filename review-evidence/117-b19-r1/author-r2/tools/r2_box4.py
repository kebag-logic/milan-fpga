"""Lane B19 round 2: the box 4 receive-counter figures, derived from the hashed controller transcripts; no bench access.

usage: r2_box4.py <raw-root> <packet-root>   writes round2/box4-derivations.json and prints it

Counter indices follow GET_COUNTERS (#726, docs/testing/726_STREAM_COUNTERS.md): STREAM_INPUT 6
TIMESTAMP_VALID and 11 FRAMES_RX, STREAM_OUTPUT 4 FRAMES_TX.
  peer CRF input   the peer's Stream Input 8 FRAMES_RX between its first and last answered poll of the
                   retention action, beside the DUT's CRF Stream Output 1 FRAMES_TX over its own polls
  receive lag      TIMESTAMP_VALID minus FRAMES_RX of the DUT's AAF listener (Stream Input 0): at the
                   first and last answered poll of each of the 13 measured actions (26 reads), and
                   over every answered poll of those actions
"""
from pathlib import Path
import json, sys

ACTIONS = ["firstreach", "retention"] + [f"cycle{i:02d}" for i in range(1, 7)] + [f"gm{i:02d}" for i in range(1, 6)]


def polls(raw, name, role, what):
    rs = [json.loads(l) for l in (raw / name / "controller.jsonl").read_text().splitlines() if l.strip()]
    return [r["response"]["counters"] for r in rs if r.get("role") == role and r.get("what") == what and r["response"].get("status") == "SUCCESS"]


def main():
    raw, pkt = Path(sys.argv[1]), Path(sys.argv[2])
    p8, d61 = polls(raw, "retention", "peer", "counter-5-8"), polls(raw, "retention", "dut", "counter-6-1")
    out = dict(retention=dict(peer_crf_input_frames_rx=p8[-1]["11"] - p8[0]["11"], peer_polls=len(p8),
                              dut_crf_output_frames_tx=d61[-1]["4"] - d61[0]["4"], dut_polls=len(d61)))
    ends, every = [], []
    for name in ACTIONS:
        s = polls(raw, name, "dut", "counter-5-0")
        lag = [c["6"] - c["11"] for c in s]
        ends += [(name, "first", lag[0]), (name, "last", lag[-1])]
        every.append(dict(action=name, polls=len(lag), min=min(lag), max=max(lag), negative=sum(x < 0 for x in lag)))
    out["receive_lag_first_last"] = dict(reads=len(ends), min=min(x[2] for x in ends), max=max(x[2] for x in ends), values=ends)
    out["receive_lag_every_poll"] = dict(polls=sum(e["polls"] for e in every), min=min(e["min"] for e in every),
                                         max=max(e["max"] for e in every), negative=sum(e["negative"] for e in every), per_action=every)
    (pkt / "round2").mkdir(exist_ok=True)
    (pkt / "round2" / "box4-derivations.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
