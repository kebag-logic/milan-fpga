#!/usr/bin/env python3
"""Reproduce #548 against the notification build recipe printed by make.

Run from the candidate repository root. Only logs and this script stay in
its output directory; the mutated RTL and build directory are temporary.
"""
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import time

ROOT = Path.cwd()
HERE = ROOT / "tb/verilator/milan_dp"
OUT = Path(__file__).resolve().parent
ENV = dict(os.environ, VERILATOR_JOBS="8")
RESULTS = []


def run(name, command, cwd=HERE):
    started = time.monotonic()
    with (OUT / f"{name}.log").open("w") as log:
        result = subprocess.run(command, cwd=cwd, env=ENV, stdout=log,
                                stderr=subprocess.STDOUT, check=False)
    record = {"name": name, "command": shlex.join(command), "cwd": str(cwd),
              "rc": result.returncode, "seconds": round(time.monotonic() - started, 3)}
    RESULTS.append(record)
    (OUT / "notify-results.json").write_text(json.dumps(RESULTS, indent=2) + "\n")
    print(f"{name}: rc={result.returncode}, seconds={record['seconds']}", flush=True)
    return result.returncode


def main():
    if run("notify-prerequisites", ["make", "ltn_rom.hex", "ucode.hex"]):
        return 1
    if run("notify-recipe", ["make", "-n", "run"]):
        return 1
    lines = (OUT / "notify-recipe.log").read_text().replace("\\\n", " ").splitlines()
    recipes = [shlex.split(line) for line in lines if "--Mdir obj_notify" in line]
    if len(recipes) != 1:
        raise RuntimeError(f"Expected one notification recipe, found {len(recipes)}")
    recipe = recipes[0]
    if run("notify-clean-build", recipe):
        return 1
    if run("notify-clean", ["./obj_notify/Vmilan_dp_notify"]):
        return 1
    source = ROOT / "hdl/milan/milan_datapath.sv"
    before = "  assign aecp_ctlr_diag = 32\x27d0;"
    after = "  assign aecp_ctlr_diag = 32\x27h01001001;"
    text = source.read_text()
    if text.count(before) != 1:
        raise RuntimeError("Expected exactly one diagnostic tie-off")
    with tempfile.TemporaryDirectory(prefix="issue548-notify-") as tmp:
        work = Path(tmp)
        mutant = work / "milan_datapath.sv"
        mutant.write_text(text.replace(before, after))
        mdir = work / "obj_notify"
        command = recipe.copy()
        command[command.index("--Mdir") + 1] = str(mdir)
        candidates = [i for i, arg in enumerate(command)
                      if arg.endswith("/milan/milan_datapath.sv")]
        if len(candidates) != 1:
            raise RuntimeError("Expected one datapath source in notification recipe")
        command[candidates[0]] = str(mutant)
        if run("notify-mutant-build", command):
            return 1
        rc = run("notify-mutant", [str(mdir / "Vmilan_dp_notify")])
        clean = (OUT / "notify-clean.log").read_text()
        mutated = (OUT / "notify-mutant.log").read_text()
        label = "[NOTIFY-T] CTLR_DIAG (0x6F4) is STRUCTURAL ZERO after controller traffic"
        failures = [line for line in mutated.splitlines() if "[FAIL]" in line]
        if rc != 1 or len(failures) != 1 or label not in failures[0]:
            raise RuntimeError("Mutant must exit 1 with only the named zero check failing")
        if not any("[ok]" in line and label in line for line in clean.splitlines()):
            raise RuntimeError("Clean run must pass the named zero check")
        print(failures[0], flush=True)
    print("PASS: clean notification leg and caught nonzero diagnostic mutant", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
