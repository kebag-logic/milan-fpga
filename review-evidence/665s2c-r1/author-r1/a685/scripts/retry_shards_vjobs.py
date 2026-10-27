"""Probe: re-run chosen shards of a native-shards.py sweep in their existing clones, with that
script's own per-shard steps: the clone at the sweep's head, `git clean -fdx` keeping the
submodules, a clean status, a fresh shard spec and log directory, and the same systemd-run
unit properties (MemoryMax 10G, -j4, taskset to the given CPUs), with VERILATOR_JOBS=4 as the
hosted runners set it, so one suite's Verilator builds stay within the unit's memory.

usage: retry_shards.py <label> <sweep-out> <tag> <k>:<cpus> [<k>:<cpus> ...]
"""
from pathlib import Path
import json, subprocess, sys

label, out, tag = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
picks = [a.split(":") for a in sys.argv[4:]]
RUNNER = Path("$MANAGEMENT/2026-09-21/run-recorded-gates.py")
run = lambda *a, cwd=None: subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()
for k, cpus in picks:
    first = json.loads((out / f"shard-{k}" / "spec.json").read_text())
    clone, head = Path(first["cwd"]), first["head"]
    unit = f"milan-{label}-shard{k}"
    assert run("systemctl", "--user", "show", unit, "-p", "ActiveState") in ("ActiveState=inactive", "ActiveState=failed"), unit
    assert run("git", "rev-parse", "HEAD", cwd=clone) == head, clone
    deps = [ln.split()[1] for ln in run("git", "config", "-f", ".gitmodules", "--get-regexp",
                                        r"^submodule\..*\.path$", cwd=clone).splitlines() if ln.split()[1] != "external"]
    run("git", "clean", "-q", "-fdx", *[x for d in deps for x in ("-e", d)], cwd=clone)
    assert run("git", "status", "--porcelain", "--untracked-files=no", cwd=clone) == "", clone
    shard_dir = out / f"shard-{k}-{tag}"
    shard_dir.mkdir()
    cmd = list(first["commands"][0])
    cmd[cmd.index("bash") + 2] = str(shard_dir / "logs")
    spec = shard_dir / "spec.json"
    spec.write_text(json.dumps(dict(cwd=str(clone), head=head, base=first.get("base"), commands=[cmd]), indent=1) + "\n")
    subprocess.run(["systemd-run", "--user", f"--unit={unit}", "--collect", "--property=MemoryMax=10G",
                    "--setenv=HOME=$WORKSPACE_HOME", "--setenv=MAKEFLAGS=-j4", "--setenv=VERILATOR_JOBS=4",
                    "--setenv=PATH=$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin",
                    "/usr/bin/taskset", "-c", cpus, "/usr/bin/python3", str(RUNNER), str(spec)], check=True)
    print(json.dumps(dict(shard=k, unit=unit, clone=str(clone), head=head, cpus=cpus, logs=str(shard_dir / "logs"))))
