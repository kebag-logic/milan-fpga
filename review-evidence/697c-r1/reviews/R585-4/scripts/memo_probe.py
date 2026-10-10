#!/usr/bin/env python3
"""Judge every boundary self-test control in full (no early stop), with the run's preprocessing reuse on or off,
and write each control's findings. Usage: python3 -I memo_probe.py <tree> <on|off> <out.json> [jobs]"""
import dataclasses, json, sys, tempfile, time
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/firmware/ctrl/test"))
import ctrl_boundary as cb  # noqa: E402
mode, out = sys.argv[2], Path(sys.argv[3])
cb.JOBS = int(sys.argv[4]) if len(sys.argv) > 4 else 8
if mode == "off":
    cb.Judgement.lookup = lambda self, argv, unit: None
work = Path(tempfile.mkdtemp(prefix="memo-"))
rv32 = cb.fw_rv32.compiler()
res, t0 = {}, time.time()
for plant in (cb.BASE, *cb.PLANTS):
    trees = cb.planted(plant, work / "plants")
    try:
        f = cb.judge(trees, rv32, work / "build", control=dataclasses.replace(plant, needle=""))
    except cb.Refusal as exc:
        f = [f"REFUSED: {exc}"]
    f = [x.replace(str(work), "<WORK>") for x in f]
    ok = (not f) if not plant.needle else any(plant.needle in x for x in f)
    res[plant.name] = {"findings": sorted(f), "verdict_ok": ok}
    print(f"[{'ok' if ok else 'BAD'}] {plant.name}: {len(f)} finding(s)", flush=True)
json.dump({"mode": mode, "seconds": round(time.time() - t0, 1), "ran": cb.MEMO.total("ran"),
           "reused": cb.MEMO.total("reused"), "controls": res}, out.open("w"), indent=1, sort_keys=True)
print(f"done {mode}: {time.time() - t0:.0f}s ran {cb.MEMO.total('ran')} reused {cb.MEMO.total('reused')}")
