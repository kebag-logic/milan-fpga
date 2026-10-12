#!/usr/bin/env python3
"""Run one foreground command, retaining its output, status, and elapsed time."""
import argparse, datetime, json, os, pathlib, subprocess, time
p = argparse.ArgumentParser()
p.add_argument("--packet", type=pathlib.Path, required=True)
p.add_argument("--cwd", type=pathlib.Path, required=True)
p.add_argument("--name", required=True)
p.add_argument("argv", nargs=argparse.REMAINDER)
a = p.parse_args()
argv = a.argv[1:] if a.argv[:1] == ["--"] else a.argv
packet = a.packet.resolve()
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(packet / "scratch"), MAKEFLAGS="-j16")
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
now = time.monotonic()
raw = packet / "scratch" / (a.name + ".raw.log")
with raw.open("w") as log:
    result = subprocess.run(argv, cwd=a.cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
elapsed = time.monotonic() - now
def public(text):
    return text.replace(str(a.cwd.resolve()), "$SOURCE").replace(str(packet), "$PACKET")
(packet / "receipts" / (a.name + ".log")).write_text(public(raw.read_text(errors="replace")))
(packet / "receipts" / (a.name + ".rc")).write_text(str(result.returncode) + "\n")
record = {"argv": argv, "cwd": str(a.cwd), "started_utc": start, "elapsed_seconds": elapsed, "rc": result.returncode}
(packet / "receipts" / (a.name + ".json")).write_text(public(json.dumps(record, indent=2)) + "\n")
print(a.name, "rc", result.returncode, "elapsed", round(elapsed, 2), flush=True)
raise SystemExit(result.returncode)
