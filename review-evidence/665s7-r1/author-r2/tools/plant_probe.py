"""plant_probe.py GRADER_DIR CAPTURE_DIR: srptx_plants.main() against copies of the captures under three grades:
the new Join-interval check switched off (JOIN_BOUNDS_MS unbounded), and the grade's allowance re-derived at 18 and
22 ms. Each run's per-plant lines, its verdict, and for the ablation the findings of the two plants it adds."""
import contextlib, io, shutil, sys, tempfile
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import srptx_grade as g
import srptx_plants as p
src = Path(sys.argv[2])


def derive(svc):
    g.SVC_MS = svc
    g.RATE_WINDOW_MS = 3 * g.JOIN_MS // 2 - svc
    g.JOIN_FOLLOW_MS = g.JOIN_MS + svc
    g.JOIN_BOUNDS_MS = (g.JOIN_RANGE_MS[0] - svc, g.JOIN_RANGE_MS[1] + svc)
    g.LEAVE_ALL_BOUNDS_MS = (g.LEAVE_ALL_MS - g.JOIN_MS - svc, 3 * g.LEAVE_ALL_MS // 2 + g.JOIN_MS + svc)


def run(title):
    with tempfile.TemporaryDirectory() as d:
        for n in ("wire", "hold", "licence"):
            shutil.copy(src / f"{n}.json", d)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = p.main.__wrapped__() if hasattr(p.main, "__wrapped__") else (sys.argv.__setitem__(slice(1, None), [d]) or p.main())
        lines = [l for l in buf.getvalue().splitlines() if l.startswith("FAIL") or l.startswith("srptx plants")]
        print(f"== {title}: rc {rc}")
        print("\n".join(l[:260] for l in lines))
        if title.startswith("ablated"):
            docs = {n: __import__("json").loads((src / f"{n}.json").read_text()) for n in ("wire",)}
            for name in ("join-early-past-t-svc", "join-interval-late"):
                found = p.planted_findings(Path(d), docs, name, "wire")
                print(f"   {name} without the new check: {len(found)} finding(s) {found[:2]}")


argv = list(sys.argv)
saved = g.JOIN_BOUNDS_MS
g.JOIN_BOUNDS_MS = (float("-inf"), float("inf"))
run("ablated: JOIN_BOUNDS_MS unbounded, SVC_MS 20")
sys.argv[:] = argv
for svc in (18, 22):
    derive(svc)
    run(f"SVC_MS re-derived at {svc} ms")
    sys.argv[:] = argv
derive(20)
run("SVC_MS 20 (as committed)")
