"""mutant_probe.py WORK: from srptx_mutants.py's own build() and run(), the short Join timer arms (10 and 15 cs, and
R814-1's 17 cs, which is not a committed arm), each graded in full and with the Join-interval check switched off
(JOIN_BOUNDS_MS unbounded). Run from tb/verilator/milan_dp of a clone; the capture of each arm is kept in WORK."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
import srptx_grade as g
import srptx_mutants as m

work = Path(sys.argv[1])
arms = {"10cs": "ps->join_cs - 10u", "15cs": "ps->join_cs - 5u", "17cs": "ps->join_cs - 3u"}
text = m.MRP.read_text()
assert text.count(m.JOIN_ARM) == 1
for name, cs in arms.items():
    arm = work / name
    arm.mkdir(parents=True, exist_ok=True)
    copy = arm / m.MRP.name
    copy.write_text(text.replace(m.JOIN_ARM, f"    shlan_timer_arm(&ps->join_timer, {cs});"))
    ok, out = m.build(arm, m.MRP, copy)
    if not ok:
        print(f"{name}: BUILD FAILED\n{out}")
        continue
    rc, found, _ = m.run(arm, "wire", 3000)
    cap = g.load(arm / "wire-3000.json")
    full = g.grade(cap)[0]
    saved = g.JOIN_BOUNDS_MS
    g.JOIN_BOUNDS_MS = (float("-inf"), float("inf"))
    ablated = g.grade(cap)[0]
    g.JOIN_BOUNDS_MS = saved
    msrp = [f.ms for f in cap.mrpdus if f.proto == "MSRP"][:4]
    print(f"== Join timer {name} ({cs}): binary rc {rc}; first MSRP frames at ms {msrp}")
    print(f"   full grade: {len(full)} finding(s); with the arm's words: {sum(m.JOIN_SPACING in f for f in full)}")
    for f in full[:4]:
        print(f"     {f}")
    print(f"   without the Join-interval check: {len(ablated)} finding(s) {ablated[:2]}")
