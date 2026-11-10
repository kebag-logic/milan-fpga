"""arm_probe.py MILAN_DP WORK: the two short-Join-timer code arms srptx_mutants.py commits (10 and 15 cs), built
and run through srptx_mutants.build() and run() into WORK, each capture graded in-process (1) in full, (2) with
the two-sided Join-interval check off (JOIN_BOUNDS_MS unbounded). Prints each arm's first MSRP egress times, the
findings carrying the arm's committed words, and the finding count without the new check."""
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import srptx_grade as g  # noqa: E402
import srptx_mutants as m  # noqa: E402

work = Path(sys.argv[2])
arms = [a for a in m.ARMS if a[0] in ("a Join timer of 10 centiseconds", "a Join timer of 15 centiseconds")]
assert len(arms) == 2, arms
for name, src, old, new, scenario, ms, words in arms:
    text = src.read_text()
    assert text.count(old) == 1
    arm = work / name.replace(" ", "_")
    arm.mkdir(parents=True, exist_ok=True)
    copy = arm / src.name
    copy.write_text(text.replace(old, new))
    ok, out = m.build(arm, src, copy)
    if not ok:
        print(f"{name}: BUILD FAILED\n{out}")
        continue
    rc, found, _ = m.run(arm, scenario, ms)
    cap = g.load(arm / f"{scenario}-{ms}.json")
    full = g.grade(cap)[0]
    saved = g.JOIN_BOUNDS_MS
    g.JOIN_BOUNDS_MS = (float("-inf"), float("inf"))
    off = g.grade(cap)[0]
    g.JOIN_BOUNDS_MS = saved
    first = [round(f.us / 1000, 3) for f in cap.mrpdus if f.proto == "MSRP"][:5]
    print(f"== {name} ({new.strip()}): binary rc {rc}; first MSRP egress ms {first}")
    print(f"   subprocess grade findings {len(found)}; in-process full {len(full)}; "
          f"with the arm's words {sum(words in f for f in full)}")
    for f in full[:4]:
        print(f"     {f}")
    print(f"   with the Join-interval check off: {len(off)} finding(s) {off[:2]}")
