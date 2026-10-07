#!/usr/bin/env python3
"""Run focused checks synchronously; each command gets its own raw log and rc."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("group", choices=("docs", "build"))
p.add_argument("repo", type=Path)
p.add_argument("packet", type=Path)
p.add_argument("--prefix", type=Path)
args = p.parse_args()
repo, packet = args.repo.resolve(), args.packet.resolve()
env = os.environ.copy()
env["PYTHONDONTWRITEBYTECODE"] = "1"
env["TMPDIR"] = str(packet / "scratch/tmp")
Path(env["TMPDIR"]).mkdir(parents=True, exist_ok=True)
if args.prefix:
    prefix = args.prefix.resolve()
    env["CMAKE_PREFIX_PATH"] = str(prefix)
    env["LD_LIBRARY_PATH"] = str(prefix / "lib") + ":" + str(prefix / "lib64")
results = []

def run(name, command, timeout=540):
    start = datetime.now(timezone.utc).isoformat()
    before = time.monotonic()
    with (packet / "receipts" / (name + ".log")).open("w") as out:
        out.write("Command: " + json.dumps(command) + "\n")
        out.flush()
        try:
            rc = subprocess.run(command, cwd=repo, env=env, stdout=out, stderr=subprocess.STDOUT, timeout=timeout).returncode
        except subprocess.TimeoutExpired:
            out.write("TIMEOUT\n")
            rc = 124
    (packet / "receipts" / (name + ".rc")).write_text(str(rc) + "\n")
    results.append(dict(name=name, command=command, rc=rc, started_utc=start, elapsed_seconds=round(time.monotonic()-before, 3)))
    (packet / "receipts" / (args.group + "-commands.json")).write_text(json.dumps(results, indent=2) + "\n")
    print(name, "rc=" + str(rc), flush=True)
    return rc

if args.group == "docs":
    run("sentences", [sys.executable, "doc/tools/check_sentences.py"])
    run("references", [sys.executable, "doc/tools/check_references.py"])
    run("references-self-test", [sys.executable, "doc/tools/check_references.py", "--self-test"])
    run("links-anonymous", [sys.executable, "doc/tools/check_links.py"])
else:
    for profile in ("OFF", "ON"):
        build = packet / "scratch" / ("build-" + profile.lower())
        label = profile.lower()
        if run("configure-" + label, ["cmake", "-S", str(repo), "-B", str(build), "-G", "Unix Makefiles", "-DCMAKE_BUILD_TYPE=Debug", "-DLWSRP_MILAN=" + profile]):
            continue
        if run("build-" + label, ["make", "-C", str(build), "-j16"]):
            continue
        run("ctest-" + label, ["ctest", "--test-dir", str(build), "--output-on-failure", "-V"])
        run("unit-" + label, [str(build / "unit_tests")])
        env["SHLAN_LIBRARY"] = str(build / "libshlan.so")
        run("behave-" + label, ["behave"])
sys.exit(int(any(item["rc"] for item in results)))
