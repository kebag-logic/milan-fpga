#!/usr/bin/env python3
"""R246-1 segmented reproduction of the milan_dp default `run` target.

A single foreground reviewer command is capped at ten minutes, and a complete
cold run takes longer. This driver therefore executes the SAME command lines
make would run, in the same order, split into segments whose wall times are
summed. It never edits the Makefile.

  seg.py make <suite-dir> <receipt-dir> <label> <make-args...>
      run `make <make-args>` in the suite dir, timed (prerequisite targets).
  seg.py plan <suite-dir> <receipt-dir> [make-vars...]
      record `make -n -o gptp -o gptp-lat -o gmstep -o gmstep-build run`,
      one logical shell line per entry, into plan.json.
  seg.py run <suite-dir> <receipt-dir> <first> <last>
      execute plan lines first..last (inclusive) with /bin/sh -c, in order,
      stopping at the first non-zero status; while a line runs, /proc is
      polled for live Vmilan_dp_* leg processes to record observed
      concurrency. Every line's argv, status and wall time goes to
      segments.jsonl; its output to seg-<first>-<last>.log.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

GROUP = {"Vmilan_dp_notify", "Vmilan_dp_nxn", "Vmilan_dp_nxndv", "Vmilan_dp_nxn8",
         "Vmilan_dp_nxn4c"}
ORDINARY = GROUP | {"Vmilan_dp_sim", "Vmilan_dp_crflic", "Vmilan_dp_nolpf",
                    "Vmilan_dp_prune", "Vmilan_dp_ax1x1", "Vmilan_dp_aclk"}


def legs_alive(suite: Path) -> list[str]:
    alive = []
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        try:
            exe = os.readlink(f"/proc/{entry}/exe")
            stat = Path(f"/proc/{entry}/stat").read_bytes()
        except OSError:
            continue
        state = stat[stat.rfind(b")") + 2:].split()[0]
        if state != b"Z" and exe.startswith(str(suite)) and Path(exe).name in ORDINARY:
            alive.append(Path(exe).name)
    return alive


def append(receipts: Path, row: dict) -> None:
    with (receipts / "segments.jsonl").open("a") as fh:
        fh.write(json.dumps(row) + "\n")


def main() -> int:
    mode, suite, receipts = sys.argv[1], Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
    receipts.mkdir(parents=True, exist_ok=True)
    if mode == "make":
        label, args = sys.argv[4], sys.argv[5:]
        t0 = time.monotonic()
        with (receipts / f"make-{label}.log").open("wb") as log:
            rc = subprocess.run(["make", *args], cwd=suite, stdout=log, stderr=subprocess.STDOUT).returncode
        wall = time.monotonic() - t0
        append(receipts, dict(kind="make", label=label, argv=["make", *args], rc=rc, seconds=wall))
        print(f"make {label}: rc={rc} seconds={wall:.3f}")
        return rc
    if mode == "plan":
        extra = sys.argv[4:]
        argv = ["make", "-n", "-o", "gptp", "-o", "gptp-lat", "-o", "gmstep", "-o", "gmstep-build",
                "run", *extra]
        out = subprocess.run(argv, cwd=suite, capture_output=True, text=True, check=True).stdout
        lines = [line for line in out.replace("\\\n", " ").splitlines() if line.strip()]
        (receipts / "plan.json").write_text(json.dumps(dict(argv=argv, lines=lines), indent=1))
        for k, line in enumerate(lines):
            print(k, line[:150])
        return 0
    first, last = int(sys.argv[4]), int(sys.argv[5])
    plan = json.loads((receipts / "plan.json").read_text())["lines"]
    with (receipts / f"seg-{first}-{last}.log").open("ab") as log:
        for k in range(first, last + 1):
            line = plan[k]
            log.write(f"### line {k}: {line}\n".encode())
            log.flush()
            t0 = time.monotonic()
            proc = subprocess.Popen(["/bin/sh", "-c", line], cwd=suite, stdout=log,
                                    stderr=subprocess.STDOUT)
            peak, peak_group, samples = 0, 0, 0
            while proc.poll() is None:
                alive = legs_alive(suite)
                samples += 1
                peak = max(peak, len(alive))
                peak_group = max(peak_group, sum(1 for name in alive if name in GROUP))
                time.sleep(0.25)
            wall = time.monotonic() - t0
            row = dict(kind="line", index=k, line=line, rc=proc.returncode, seconds=wall,
                       samples=samples, peak_legs=peak, peak_group=peak_group)
            append(receipts, row)
            print(f"line {k}: rc={proc.returncode} seconds={wall:.3f} peak_legs={peak} "
                  f"peak_group={peak_group} :: {line[:90]}", flush=True)
            if proc.returncode != 0:
                return proc.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
