"""Scratch (round 7): judge a snapshot of a capture with the gate's own functions, without held()'s builder checks
(a partial capture holds only some builders): dependency outputs, files read first, and both sides' findings.

usage: judge_snapshot.py <checkout> <capture> <snapshot dir>
"""
import collections
import json
import shutil
import sys
from pathlib import Path

checkout, capture, snap = (Path(a).resolve() for a in sys.argv[1:4])
sys.path[:0] = [str(checkout / "sw/firmware/ctrl/test"), str(checkout / "sw/firmware/gtest")]
import ctrl_boundary  # noqa: E402
import ctrl_capture  # noqa: E402
import ctrl_configs  # noqa: E402

snap.mkdir(parents=True, exist_ok=True)
lines = (capture / "records.jsonl").read_text(encoding="utf-8").splitlines(keepends=True)
complete = [ln for ln in lines if ln.endswith("\n")]
(snap / "records.jsonl").write_text("".join(complete), encoding="utf-8")
shutil.copy(capture / "manifest.jsonl", snap / "manifest.jsonl") if (capture / "manifest.jsonl").is_file() else \
    (snap / "manifest.jsonl").write_text("", encoding="utf-8")
if not (snap / "text").exists():
    (snap / "text").symlink_to(capture / "text")
cap = ctrl_capture.load(snap)
print(f"{len(cap.invocations)} invocations")
print("dependency refusals:", ctrl_configs.unlisted(cap)[:10])
print("expansion refusals:", ctrl_configs.expanded(cap, ctrl_configs.places((checkout,)))[:10])
places = ctrl_boundary.Places((checkout,), ctrl_boundary.targets(cap, (checkout,)))
found = ctrl_boundary.judged(cap, places)
print(f"{len(found)} finding(s)")
for core, builders in list(found.items())[:40]:
    print("  ", core, sorted(builders))
print("counts:", ctrl_boundary.counted(cap, places))
kinds = collections.Counter()
for inv in cap.invocations:
    impl = ctrl_boundary.implementation(inv)
    for s in inv.sources:
        if s.lang in ctrl_configs.COMPILED:
            kinds[(s.lang, places.kind(s.path, impl))] += 1
print(json.dumps({f"{a}/{b}": n for (a, b), n in sorted(kinds.items())}, indent=1))
