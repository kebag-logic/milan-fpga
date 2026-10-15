#!/usr/bin/env python3
"""Challenge isolation verification with real pinned packages and unavailable gate dependencies."""
import argparse
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import venv

ap = argparse.ArgumentParser()
ap.add_argument("repo", type=Path)
ap.add_argument("packet", type=Path)
ap.add_argument("--python", default="python3.12")
a = ap.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
work = packet / "scratch" / "skip-gate-py312"
work.mkdir(parents=True)
os.environ["TMPDIR"] = str(work)
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo / "scripts"))
m = importlib.import_module("ci_toolcache_isolation")
leg = m.Leg("fault-fixture", work / "leg", "HEAD", Path(sys.prefix), None)
private = leg.temp / "litex-venv"
subprocess.run([a.python, "-m", "venv", str(private)], check=True)
leg.paths.insert(0, str(private / "bin"))
leg.extra["TMPDIR"] = str(leg.temp)
leg.extra["PIP_CONFIG_FILE"] = "/dev/null"
leg.extra["PIP_INDEX_URL"] = "https://pypi.org/simple"
pins = (repo / "sw/litex/litex_pins.txt").read_text().splitlines()
board = next(x for x in pins if x.startswith("git+") and "/litex-boards.git@" in x)
kept = [x for x in pins if x.startswith("git+") and x != board]
rc = leg.run("Install pinned packages except litex-boards", ["python3", "-m", "pip", "install", "--quiet", "pyyaml", *kept])
assert rc == 0, rc
cache = work / "unchanged-cache"
cache.mkdir()
(cache / "sentinel").write_text("unchanged\n")
before = m.manifest(cache)
problems_without = m.verify(leg, cache)
print("without litex-boards; patches deliberately absent:", problems_without, flush=True)
rc = leg.run("Restore pinned litex-boards", ["python3", "-m", "pip", "install", "--quiet", board])
assert rc == 0, rc
problems_with = m.verify(leg, cache)
print("with litex-boards; same absent patches:", [x.replace(str(work), "<scratch>") for x in problems_with], flush=True)
assert m.manifest(cache) == before
log = leg.log.read_text()
(packet / "probe-skipped-gate-steps.log").write_text(log.replace(str(work), "<scratch>"))
result = {"head": subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip(),
          "without_boards_problems": problems_without,
          "with_boards_problems": [x.replace(str(work), "<scratch>") for x in problems_with],
          "cache_changed": False,
          "skips_visible": "GATE ARM(S) DID NOT RUN" in log}
(packet / "probe-skipped-gate.json").write_text(json.dumps(result, indent=2) + "\n")
assert not problems_without, "The suspected acceptance hole did not reproduce"
assert problems_with, "The positive refusal control did not work"
print("REPRODUCED: verify() accepts skipped gate 23h and rejects the same unpatched tree when its dependency is available")
