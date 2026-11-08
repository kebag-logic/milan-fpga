#!/usr/bin/env python3
"""sweep-shard.py <k> <cpus>: launch shard k of the FULL sweep's 4, exactly as native-shards.py launches each of its
shards (its own --shared clone $LANES/a746e-shard<k> of the lane at the spec's head, submodules from the
lane's clones, the spec's suite command with --shard k/4, through run-recorded-gates.py, unit milan-a746e-shard<k>,
MemoryMax 10G, MAKEFLAGS -j4), on the CPU range given: one shard per free range as ranges free up, since the booked
host never had four free at once."""
from pathlib import Path
import json, subprocess, sys

k, cpus = int(sys.argv[1]), sys.argv[2]
n = 4
S = Path("$VALIDATION_STORAGE/scratch/a746e")
spec = json.loads((S / "native-spec.json").read_text())
src, head, out = Path(spec["cwd"]), spec["head"], S / "sweep"
suite = [c for c in spec["commands"] if "scripts/run_all_suites.sh" in c]
assert len(suite) == 1
prefix = suite[0][:suite[0].index("bash")]
RUNNER = Path("$HOME/milan-fpga-management/2026-09-21/run-recorded-gates.py")
run = lambda *a, cwd=None: subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def deps(repo, rev):
    """The submodules the tree's .gitmodules declares, 'external' (the private dependency no bank builds) left out."""
    lines = run("git", "config", "--blob", f"{rev}:.gitmodules", "--get-regexp", r"^submodule\..*\.path$", cwd=repo)
    return [line.split()[1] for line in lines.splitlines() if line.split()[1] != "external"]


clone = Path(f"$LANES/a746e-shard{k}")
if not clone.exists():
    run("git", "clone", "-q", "--shared", "--no-checkout", str(src), str(clone))
run("git", "fetch", "-q", str(src), head, cwd=clone)
run("git", "-c", "advice.detachedHead=false", "checkout", "-q", "-f", "--detach", head, cwd=clone)
DEPS = deps(clone, head)
run("git", "clean", "-q", "-fdx", *[x for d in DEPS for x in ("-e", d)], cwd=clone)
assert run("git", "status", "--porcelain", "--untracked-files=no", cwd=clone) == ""
for dep in DEPS:
    url = str(src / dep) if (src / dep / ".git").exists() else run("git", "config", "--blob", f"{head}:.gitmodules",
                                                                     f"submodule.{dep}.url", cwd=clone)
    run("git", "config", f"submodule.{dep}.url", url, cwd=clone)
run("git", "-c", "protocol.file.allow=always", "submodule", "update", "-q", "--init", "--force", *DEPS, cwd=clone)
shard_dir = out / f"shard-{k}"
shard_dir.mkdir(parents=True)
cmd = prefix + ["bash", "scripts/run_all_suites.sh", str(shard_dir / "logs"), "--wait", "--shard", f"{k}/{n}"]
shard_spec = shard_dir / "spec.json"
shard_spec.write_text(json.dumps(dict(cwd=str(clone), head=head, base=spec.get("base"), commands=[cmd]), indent=1) + "\n")
unit = f"milan-a746e-shard{k}"
subprocess.run(["systemd-run", "--user", f"--unit={unit}", "--collect", "--property=MemoryMax=10G",
                "--setenv=HOME=$HOME", "--setenv=MAKEFLAGS=-j4",
                "--setenv=PATH=$HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin",
                "/usr/bin/taskset", "-c", cpus, "/usr/bin/python3", str(RUNNER), str(shard_spec)], check=True)
print(json.dumps(dict(shard=k, head=head, cpus=cpus, unit=unit, out=str(shard_dir))), flush=True)
