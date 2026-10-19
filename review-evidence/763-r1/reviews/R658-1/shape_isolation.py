#!/usr/bin/env python3
"""Isolate the new test in binaries built by focused.py shapes."""
import argparse
import json
from pathlib import Path
import sys

p = argparse.ArgumentParser()
p.add_argument("repo", type=Path)
p.add_argument("packet", type=Path)
a = p.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
sys.path.insert(0, str(repo / "sw/firmware/gtest"))
import fw_gtest

rows = []
for exe in sorted((packet / "scratch/shapes/build").glob("aecp-core-*/suite")):
    name = exe.parent.name.removeprefix("aecp-core-").removesuffix("-if1")
    ok, log = fw_gtest.run_binary(exe, ["--gtest_filter=Nvm.EmptyAndNonDefaultMapsSurviveTheRealStorePowerCycle"])
    (packet / ("new-only-" + name + ".log")).write_text(log)
    rows.append({"shape": name, "passed": ok})
    print(name, ok)
assert len(rows) == 5
(packet / "new-only-shapes.json").write_text(json.dumps(rows, indent=2) + "\n")
