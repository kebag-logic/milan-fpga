"""Recompute the findings page's per-cycle table and summary claims from the
published packet's analysis.json files, independently of the operator's
report generator, and compare with the page at the reviewed head.

Usage: python3 -B recompute_table.py <packet author dir> <page path>
Exit 0 when every compared cell and claim matches, 1 otherwise.
"""
import json
import re
import sys
from pathlib import Path

pkt = Path(sys.argv[1])
page = Path(sys.argv[2]).read_text()
f2 = lambda x: f"{x:.2f}"
bad = 0


def check(label, got, want):
    global bad
    ok = got == want
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {label}: page={want!r} recomputed={got!r}")


rows = {}
for line in page.splitlines():
    m = re.match(r"^\| (\d+) \| (\d+\.\d\d) \|", line)
    if m:
        rows[int(m[1])] = [c.strip() for c in line.strip().strip("|").split("|")]

cycles = []
for n in range(1, 11):
    s = json.loads((pkt / f"cycle{n:02d}" / "analysis.json").read_text())
    cycles.append(s)
    off = s["off"]
    steps = s["large_phc_discontinuities"]
    check(f"c{n} single PHC discontinuity", len(steps), 1)
    br = steps[0]["bracket"]
    car = [(t - off, v) for t, v in s["carrier"] if t > off]
    down = next(t for t, v in car if v == 0)
    up = next(t for t, v in car if v == 1)
    relock = max(s["media_locked_at"]["dut"], s["servo_locked_at"], s["gptp_recovered_at"])
    seq = [v["2"] for _, v in s["counter_transitions"]["dut:counter-6-1"]]
    seq = [v for i, v in enumerate(seq) if i == 0 or v != seq[i - 1]]
    want = [
        str(n),
        f2(s["on"] - s["off"]),
        f"{f2(down)} / {f2(up)}",
        f"{f2(s['first_gm'] - off)} / {f2(br[0] - off)}-{f2(br[1] - off)}",
        f2(s["gptp_recovered_at"] - s["first_gm"]),
        f"{f2(s['wire']['dut']['first_after_on'] - off)} / {f2(s['wire']['peer']['first_after_on'] - off)}",
        f"{f2(relock - br[1])}-{f2(relock - br[0])}",
        f"{len(s['wire']['dut']['mr']) - 1} / {len(s['wire']['peer']['mr']) - 1}",
        " > ".join(str(v) for v in seq),
    ]
    check(f"c{n} row", want, rows.get(n))
    # counters the page asserts per cycle
    ce = s["counter_endpoints"]
    check(f"c{n} AVB LINK_UP/DOWN/GM_CHANGED delta", [ce["dut:counter-9-0"]["delta"][k] for k in "015"], [0, 0, 2])
    check(f"c{n} LINK_UP/DOWN absolute last", [ce["dut:counter-9-0"]["last"][k] for k in "01"], [1, 0])
    check(f"c{n} STREAM_INPUT MEDIA_LOCKED/UNLOCKED delta", [ce["dut:counter-5-1"]["delta"][k] for k in "01"], [1, 1])
    check(f"c{n} CLOCK_DOMAIN LOCKED/UNLOCKED delta", [ce["dut:counter-36-0"]["delta"][k] for k in "01"], [1, 1])
    check(f"c{n} DUT STREAM_OUTPUT START/STOP delta", [ce["dut:counter-6-1"]["delta"][k] for k in "01"], [1, 1])
    check(f"c{n} peer STREAM_OUTPUT START/STOP delta", [ce["peer:counter-6-2"]["delta"][k] for k in "01"], [1, 1])
    check(f"c{n} MAC_STATUS values", sorted({v for _, v in s["mac_status"]}), [13])
    check(f"c{n} reset epochs", s["reset_epochs"], [1])
    check(f"c{n} bindings ok / steady", [s["bindings_ok"], s["steady_recovered"]], [True, True])
    check(f"c{n} post-return tu=1 PDUs dut/peer", [s["wire"]["dut"]["post_tu1"], s["wire"]["peer"]["post_tu1"]], [0, 0])
    check(f"c{n} all PDUs valid", all(s["wire"][r]["pdus"] == s["wire"][r]["valid_pdus"] for r in ("dut", "peer")), True)
    check(f"c{n} servo sequence", [v for _, v in s["servo_states"]], [4, 5, 3, 4])
    check(f"c{n} GM sequence length", len(s["gm"]), 3)
    check(f"c{n} switch frames absent while off", s["switch_frames_absent_off"], True)
    print(f"    c{n} step s={steps[0]['phc_minus_wall_delta_s']:.2f} last-wire-before-gap={s['last_wire_before_gap'] - off:.2f}"
          f" first-wire-return={s['first_wire_return'] - off:.2f} dut-first-after-wire={s['wire']['dut']['first_valid_after_wire_return_s']:.2f}"
          f" peer-first-after-wire={s['wire']['peer']['first_valid_after_wire_return_s']:.2f} crf-licence={s['crf_licence']}")

rec = [s["gptp_recovery_s"] for s in cycles]
check("gPTP recovery range", f"{f2(min(rec))} to {f2(max(rec))}", "0.44 to 1.82")
wr = [s["wire"][r]["first_valid_after_wire_return_s"] for s in cycles for r in ("dut", "peer")]
check("first PDU after wire return range", f"{f2(min(wr))}-{f2(max(wr))}", "5.07-14.00")
mx = max(max(s["media_locked_at"]["dut"], s["servo_locked_at"], s["gptp_recovered_at"]) - s["large_phc_discontinuities"][0]["bracket"][0] for s in cycles)
check("longest step-to-media", f2(mx), "12.54")
check("largest console gap", f"{max(s['max_console_gap_s'] for s in cycles):.3f}", "0.251")
st = [s["large_phc_discontinuities"][0]["phc_minus_wall_delta_s"] for s in cycles]
check("cycle 1 step (s, rounded)", round(st[0]), -358781)
check("cycle 2 step", f2(st[1]), "-162.46")
check("cycles 3-10 step range", f"{f2(max(st[2:]))}..{f2(min(st[2:]))}", "-95.74..-96.47")
check("intermediate zero caught", sum(1 for s in cycles if 0 in [v["2"] for _, v in s["counter_transitions"]["dut:counter-6-1"]][1:]), 5)
hr = [(s["clock_half_rtt_s"]["tap"], s["clock_half_rtt_s"]["controller"]) for s in cycles]
print("half-RTT tap max %.3f controller max %.3f" % (max(a for a, _ in hr), max(b for _, b in hr)))
sp = [x for s in cycles for x in s["tap_anchor_spread_s"]]
print("tap anchor spread %.3f..%.3f" % (min(sp), max(sp)))
print("FAILURES", bad)
sys.exit(1 if bad else 0)
