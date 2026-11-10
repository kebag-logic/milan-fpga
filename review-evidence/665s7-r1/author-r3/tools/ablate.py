"""ablate.py MILAN_DP OLD_GRADE_DIR CAPTURES_DIR: the round 3 attribution's evidence, in-process, nothing written
but planted copies in a temporary directory.
 1. the grade at 2131eff4 (OLD_GRADE_DIR/srptx_grade.py) and this head's on the off-grid controls;
 2. this head's grade with each change taken back, one at a time, on the plants and controls it serves:
    - no requested rule (every idle_us dropped): requested-late must escape;
    - no Join attribution (every after_join dropped): the Join interval plants must escape;
    - 2131eff4's time window instead (window: a frame but a LeaveAll one is the Join timer's when the latest Join
      or periodic expiry within ATTRIBUTE_MS before it is a Join expiry, 2131eff4's causes() itself):
      licence-16280 must be refused by F-1's words, the case its control holds;
    - that window over LeaveAll frames too (window-la), which counting a LeaveAll frame the Join timer held, as
      this head does, would need without the bench's record."""
import copy
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import srptx_grade as g  # noqa: E402
import srptx_plants as p  # noqa: E402

spec = importlib.util.spec_from_file_location("old_grade", Path(sys.argv[2]) / "srptx_grade.py")
old = importlib.util.module_from_spec(spec)
sys.modules["old_grade"] = old
spec.loader.exec_module(old)
caps = Path(sys.argv[3])
load = g.load


def run(mode: str, path: Path) -> list[str]:
    """This head's findings on path, with one change taken back."""
    def patched(q):
        cap = load(q)
        window = set()
        for pr in g.APPLICATIONS:
            frames = [f for f in cap.mrpdus if f.proto == pr and not f.error and not cap.queued(f)]
            if mode == "window":
                window |= {id(f) for f, c in zip(frames, old.causes(cap, pr, frames)) if c and c[0] == "join"}
            expiries = [t for t in cap.doc["timers"] if t["proto"] == pr and t["event"] == "expire"
                        and t["kind"] in ("join", "periodic")]
            for f in frames if mode == "window-la" else ():
                near = [t for t in expiries if 0 <= f.us - t["us"] < g.ATTRIBUTE_MS * 1000]
                if near and max(near, key=lambda t: t["us"])["kind"] == "join":
                    window.add(id(f))
        for f in cap.mrpdus:
            if mode == "no-requested":
                f.idle_us = None
            elif mode == "no-join":
                f.after_join = False
            elif mode in ("window", "window-la"):
                f.after_join = id(f) in window
        return cap
    g.load = patched
    try:
        return g.grade(g.load(path))[0]
    finally:
        g.load = load


def planted(name: str, scenario: str, tmp: Path) -> Path:
    doc = copy.deepcopy(json.loads((caps / f"{scenario}.json").read_text()))
    p.plant(name, doc)
    out = tmp / f"{scenario}-{name}.json"
    out.write_text(json.dumps(doc) + "\n")
    return out


print("== 1. the off-grid controls, the grade at 2131eff4 against this head's")
for ms in p.OFF_GRID:
    path = caps / f"licence-{ms}.json"
    was, now = old.grade(old.load(path))[0], g.grade(g.load(path))[0]
    print(f"licence-{ms}: at 2131eff4 {len(was)} finding(s){': ' + was[0] if was else ''}; this head {len(now)}")
print("== 2. this head's grade, one change taken back")
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    rows = [("no-requested", "requested-late"), ("no-requested", "requested-within"),
            ("no-join", "join-early-past-t-svc"), ("no-join", "join-interval-late"),
            ("no-join", "join-early-within-t-svc"), ("no-join", "join-interval-late-within")]
    for mode, name in rows:
        scenario = (p.PLANTS.get(name) or p.WITHIN.get(name))[0]
        path = planted(name, scenario, tmp)
        words = p.WORDS.get(name)
        full, off = g.grade(g.load(path))[0], run(mode, path)
        def verdict(found):
            if words is None:
                return f"{len(found)} finding(s) (a control: clean wanted)"
            hit = [f for f in found if words in f]
            return f"{'REFUSED' if hit else 'ESCAPED'} ({len(found)} finding(s))"
        print(f"{name}: with the change {verdict(full)}; {mode} {verdict(off)}")
    for mode in ("window", "window-la"):
        for scenario in ("wire", "hold", "licence", "licence-16280", "licence-16240"):
            found = run(mode, caps / f"{scenario}.json")
            print(f"{scenario}, Join attribution by {mode}: {len(found)} finding(s)"
                  + "".join(f"\n    {f}" for f in found))
