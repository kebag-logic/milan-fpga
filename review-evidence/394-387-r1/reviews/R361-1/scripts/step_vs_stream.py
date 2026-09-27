"""For each cycle, place the PHC step bracket against the stream state the
packet recorded: the last CRF PDU each way before the gap, the DUT CRF
talker licence word (0x750) dropping and returning, and the first valid
PDU each way after return. All times are seconds after the OFF command,
on the recorder clock (tap times carry the packet's stated offset).

Usage: python3 -B step_vs_stream.py <packet author dir>
Exit 0 when, in every cycle, the step bracket ends before the first
returning PDU in both directions and after the licence drop (the step
landed while no stream flowed); exit 1 otherwise.
"""
import json
import sys
from pathlib import Path

pkt = Path(sys.argv[1])
allstopped = True
print("cycle | licence drop | step bracket | licence return | first DUT PDU | first peer PDU | streams stopped at step")
for n in range(1, 11):
    s = json.loads((pkt / f"cycle{n:02d}" / "analysis.json").read_text())
    off = s["off"]
    lic = s["crf_licence"]
    drop = next(t for t, v in lic if v == 3) - off
    ret = next((t for t, v in lic if t - off > drop and v != 3), None)
    ret = ret - off if ret else None
    b0, b1 = (t - off for t in s["large_phc_discontinuities"][0]["bracket"])
    dut = s["wire"]["dut"]["first_after_on"] - off
    peer = s["wire"]["peer"]["first_after_on"] - off
    stopped = drop < b0 and b1 < min(dut, peer) and (ret is None or b1 < ret)
    allstopped &= stopped
    print(f"{n} | {drop:.2f} | {b0:.2f}-{b1:.2f} | {ret:.2f} | {dut:.2f} | {peer:.2f} | {stopped}")
print("ALL CYCLES STEP WHILE STREAMS STOPPED:", allstopped)
sys.exit(0 if allstopped else 1)
