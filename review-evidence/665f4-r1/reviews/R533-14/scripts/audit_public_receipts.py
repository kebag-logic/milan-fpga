#!/usr/bin/env python3
"""Check immutable public receipts as data, without executing author helpers."""
import hashlib
import json
from pathlib import Path
import re
import shutil

packet = Path(__file__).resolve().parents[1]
author = packet / "scratch/public-author-r14"
published = json.loads((packet / "scratch/evidence-manifest.json").read_text())
pub = {x["file"]: x for x in published}
records = json.loads((author / "ROUND14-GATES.json").read_text())
assert len(records) == 87 and all(x["rc"] == 0 for x in records)
redacted = 0
for record in records:
    rel = "author-r14/round14-receipts/" + record["log"]
    manifest = pub[rel]
    raw = (author / "round14-receipts" / record["log"]).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == manifest["published_sha256"], rel
    assert record["sha256"] == manifest["original_sha256"], rel
    redacted += bool(manifest["path_redacted"])
print(f"PASS: all 87 successful command records match publisher original/public hash mapping; {redacted} path-redacted logs")
scope = json.loads((author / "ROUND14-SCOPE.JSON").read_text())
assert scope["head"] == "fe1cd0679f5028c749af7242c903a82ca2b3d692"
assert scope["runner_sha256"] == "35890beace97bf9e2b26bb24a8016b585767e24566ffbf9a62a0ada0beccfd66"
assert scope["disposable_runner_matches_head"]
print("PASS: published source/isolated-runner identity names exact reviewed head and runner digest")
logs = author / "round14-receipts"
runner = (logs / "runner-final.log").read_text()
assert sum(line.startswith("  ok   ") for line in runner.splitlines()) == 442
assert runner.rstrip().endswith("selftest: PASS")
print("PASS: published offline runner log has 442 passing checks")
needles = {
    "missing-trusted-entry": "the trusted manifest includes exactly the five approved entries",
    "missing-materialization": "materialization fetches all four public pins",
    "ignore-manifest-equality": "candidate that drops lwSRP is refused before fetch",
    "ignore-manifest-addition": "candidate that adds another lwSRP is refused before fetch",
    "ignore-duplicate-key": "candidate that duplicates lwSRP is refused before fetch",
    "ignore-url-change": "candidate that redirects lwSRP is refused before fetch",
    "ignore-gitlink-omission": "candidate that drops lwSRP gitlink is refused before fetch",
    "ignore-gitlink-addition": "candidate that adds lwSRP gitlink is refused before fetch",
}
mutations = json.loads((author / "ROUND14-MUTATIONS.json").read_text())
assert len(mutations) == 9 and mutations[0]["name"] == "baseline"
assert mutations[0]["failures"] == 0 and mutations[0]["exception"] is None
assert all(x["passed"] for x in mutations)
for name, needle in needles.items():
    text = (logs / ("manifest-" + name + ".log")).read_text()
    assert "FAIL " + needle in text, name
    print(f"PASS published mutation {name}: named assertion failed")
ctrl = (logs / "ctrl.log").read_text()
assert len(re.findall(r"^\[ok\] arm ", ctrl, re.M)) == 51
assert ctrl.rstrip().endswith("test_ctrl_firmware: PASS")
tallies = re.findall(r"checks: (\d+)\s+failures: (\d+)", ctrl)
assert sum(int(n) for n, f in tallies) == 1252
assert all(int(f) == 0 for n, f in tallies)
assert "ALL GATES PASS EXCEPT 1 NOT RUN" in (logs / "builder.log").read_text()
compiler = (logs / "compiler-pinned.log").read_text()
assert "GATE 1b PASS; 0 NOT RUN; 2146 actual firmware compiler invocations" in compiler
print("PASS published ctrl: 51 arms / 1252 checks; compiler: 2146 invocations / no omitted arms")
print("LIMIT published builder: one NOT RUN calibration arm; no hardware proof")
selected = ["runner-final.log", "runner-mutants.log", "manifest-baseline.log",
            *("manifest-" + n + ".log" for n in needles)]
dest = packet / "receipts/published-source"
dest.mkdir(exist_ok=True)
for name in selected:
    shutil.copyfile(logs / name, dest / name)
for name in ("ROUND14-SCOPE.JSON", "ROUND14-MUTATIONS.json", "ROUND14-SUMMARY.json"):
    shutil.copyfile(author / name, dest / name)
print("LIMIT: public author execution evidence audited, not independently rerun")
