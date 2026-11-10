"""plant_ablate.py MILAN_DP CAPTURE_DIR OUT_DIR: the round 2 timing plants and controls, graded in-process
(1) as committed, (2) with the two-sided Join-interval check off (JOIN_BOUNDS_MS unbounded), and (3) with the
grade's SVC_MS moved 1 ms each way (19, 21), re-deriving every bound the grade derives from it. Also prints, for
the 219 ms control, the interval after the moved frame (the READMEs' 179.99 ms figure).
Writes planted copies only under OUT_DIR."""
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import srptx_grade as g  # noqa: E402
import srptx_plants as p  # noqa: E402

src, out = Path(sys.argv[2]), Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
docs = {s: json.loads((src / f"{s}.json").read_text()) for s in ("wire", "hold", "licence")}
NAMES = ["join-late", "join-late-past-t-svc", "join-early-past-t-svc", "join-interval-late"]
CONTROLS = list(p.WITHIN)


def planted(name):
    doc = copy.deepcopy(docs["wire"])
    p.plant(name, doc)
    path = out / f"wire-{name}.json"
    path.write_text(json.dumps(doc) + "\n")
    return g.load(path)


def derive(svc):
    g.SVC_MS = svc
    g.RATE_WINDOW_MS = 3 * g.JOIN_MS // 2 - svc
    g.JOIN_FOLLOW_MS = g.JOIN_MS + svc
    g.JOIN_BOUNDS_MS = (g.JOIN_RANGE_MS[0] - svc, g.JOIN_RANGE_MS[1] + svc)
    g.LEAVE_ALL_BOUNDS_MS = (g.LEAVE_ALL_MS - g.JOIN_MS - svc, 3 * g.LEAVE_ALL_MS // 2 + g.JOIN_MS + svc)


def run(label):
    print(f"== {label}: SVC_MS {g.SVC_MS}, JOIN_BOUNDS_MS {g.JOIN_BOUNDS_MS}")
    for name in NAMES:
        words = p.PLANTS[name][2]
        found = g.grade(planted(name))[0]
        caught = [f for f in found if words in f]
        print(f"   plant {name}: {'refused' if caught else 'ESCAPED'}; {len(found)} finding(s)"
              + (f"; first: {found[0][:150]}" if found and not caught else ""))
    for name in CONTROLS:
        found = g.grade(planted(name))[0]
        print(f"   control {name}: {'clean' if not found else 'REFUSED: ' + found[0][:150]}")


run("as committed")
cap = planted("join-late-within-t-svc")
frames = [f for f in cap.mrpdus if f.proto == "MSRP" and not f.error and not cap.queued(f)]
print("   join-late-within-t-svc first MSRP egress (ms):", [round(f.us / 1000, 3) for f in frames[:4]],
      "gaps:", [round((b.us - a.us) / 1000, 3) for a, b in zip(frames[:4], frames[1:4])])
saved = g.JOIN_BOUNDS_MS
g.JOIN_BOUNDS_MS = (float("-inf"), float("inf"))
run("Join-interval check off")
g.JOIN_BOUNDS_MS = saved
for svc in (19, 21):
    derive(svc)
    run(f"grade SVC_MS re-derived at {svc}")
derive(20)
