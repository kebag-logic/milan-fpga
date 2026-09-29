#!/usr/bin/env python3
"""Run the processor entry points or the parent consumer set at one committed head.

Each command runs to completion, one after another; its exit status, duration,
log size and log SHA-256 are appended to <out>/results.jsonl, and <out>/DONE-<group>
is written last. The processor clone and the scratch parent must already be at the
head (the parent's protocol-processor gitlink staged there). The parent group is the
manager's fifteen-command consumer set.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

PINNED = "$VALIDATION_STORAGE/pp131-manager-e1ae468f/pinned-tool-bin"
VROOT = ("$WORKSPACE_HOME/.local/share/containers/storage/overlay/"
         "9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff/usr/share/verilator")
PROCESSOR = [
    ["./scripts/run_suites.sh"],
    ["./scripts/lint_hdl.sh"],
    ["make", "check"],
    ["python3", "scripts/gen_matrix.py", "--check"],
    ["./syn/yosys/run.sh"],
    ["make", "-C", "tb/nvm_port", "figures"],
    ["python3", "tb/pp_top/d3_mutants.py", "--output", "OUT/d3-mutants", "--jobs", "6",
     "--verilator", PINNED + "/verilator"],
    ["make", "-C", "tb/srp_top", "mutants"],
]
PARENT = [
    ["python3", "scripts/check_cpp_idiom.py"],
    ["python3", "scripts/check_py_idiom.py"],
    ["python3", "scripts/xvlog_gate.py", "--check"],
    ["python3", "scripts/check_rtl_source_lists.py"],
    ["python3", "scripts/pp_srcs.py", "--check", "--selftest"],
    ["python3", "sw/builder/test_builder.py"],
    ["make", "-C", "tb/verilator/pp_shadow", "-j8"],
    ["python3", "scripts/check_port_contracts.py"],
    ["python3", "scripts/measure_naming.py", "--check"],
    ["python3", "scripts/measure_test_evidence.py", "--check"],
    ["python3", "scripts/docs_check.py"],
    ["make", "-C", "tb/verilator/nvm_cosim", "lint"],
    ["make", "-C", "tb/verilator/nvm_cosim", "quick"],
    ["make", "-C", "tb/verilator/milan_dp", "-j8"],
    ["make", "-C", "tb/verilator/milan_dp_render", "-j8"],
]


def run(label, cwd, cmd, out, env):
    """Run one command to completion and record it."""
    cmd = [c.replace("OUT", str(out)) for c in cmd]
    name = f"{label}-" + "_".join(c.replace("/", "_") for c in cmd
                                  if not c.startswith(str(out)) and not c.startswith(PINNED))[:80]
    log = out / f"{name}.log"
    start = time.monotonic()
    with log.open("wb") as stream:
        rc = subprocess.run(cmd, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT,
                            env=env, check=False).returncode
    data = log.read_bytes()
    row = {"group": label, "cwd": str(cwd), "command": cmd, "rc": rc,
           "seconds": round(time.monotonic() - start, 1), "log": log.name,
           "size": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    with (out / "results.jsonl").open("a") as rec:
        rec.write(json.dumps(row) + "\n")
    print(f"{label} rc={rc} {row['seconds']}s {' '.join(cmd)}", flush=True)


def main():
    """processor clone, scratch parent, output directory, group (processor or parent)."""
    pp, parent, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    which = sys.argv[4]
    out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PATH=PINNED + ":" + os.environ["PATH"], VERILATOR_ROOT=VROOT,
               TMPDIR=str(out / "tmp"))
    (out / "tmp").mkdir(exist_ok=True)
    if which == "processor":
        for cmd in PROCESSOR:
            run("processor", pp, cmd, out, env)
    if which == "parent":
        for cmd in PARENT:
            run("parent", parent, cmd, out, env)
    (out / f"DONE-{which}").write_text("done\n")


if __name__ == "__main__":
    main()
