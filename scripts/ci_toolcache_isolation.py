#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run both elaboration legs' toolchain setup at once on one planted tool cache.

act mounts one tool-cache volume into every job container of a replay, while
each job keeps its own HOME, RUNNER_TEMP and workspace. This control rebuilds
that sharing in one process tree, with no container: it copies a CPython
installation into a planted tool cache and runs the setup steps of both
elaboration legs, read from the workflow at --rev, side by side. Each leg has
its own home, temporary directory, workspace export and PATH and environment
files, and every step of both legs starts together, which is when two act jobs
on one tool cache collide.

The legs are isolated when every step of both passes, each leg's LiteX
interpreter and VexiiRiscv checkout live under that leg's RUNNER_TEMP, gate
23h and its negative control pass in each leg, and every path of the tool
cache is byte for byte what was planted. Anything else exits 1.

--shared drops the job-private environment step from both legs, so both
install, clone and patch in the tool cache's own site-packages. A --rev that
predates that step plants the same sharing from its own workflow text.

Run: python3 scripts/ci_toolcache_isolation.py --python <CPython prefix>
         --work <empty scratch directory> [--rev REV] [--shared]
         [--pip-cache DIR] [--report FILE]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import time

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ".github/workflows/elaborate.yml"
LEGS = ("elaborate-gates-0", "elaborate-gates-1")
SETUP_ACTION = "actions/setup-python@"
PRIVATE_STEP = "Put a job-private Python environment on PATH"
LAST_STEP = "Apply the toolchain patch series"
#: The steps between setup-python and the patch series that this control runs.
RUN = (PRIVATE_STEP, "Install LiteX at the pinned revisions",
       "Place the VexiiRiscv source at the revision LiteX pins", LAST_STEP)
#: The other steps of that window, and why each is left out. A step in the
#: window that is in neither table refuses the run, so a new setup step cannot
#: be passed over in silence.
SKIP = {
    "Cache the pinned pip downloads": "restored by --pip-cache into each leg's own home",
    "Cache the Scala toolchain": "restores into the leg's home; no step run here reads it",
    "Cache the generated CPU metadata": "restores into the leg's home; the placement step "
                                        "creates the directory when it is absent",
    "Install sbt": "unpacks into /opt/sbt, outside the tool cache, with sudo; "
                   "no step run here reads it",
}
GATES = "test_toolchain_patches_are_applied,test_toolchain_patch_gate_bites"
BASE_PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
PROBE = ("import sys, litex, pythondata_cpu_vexiiriscv as p; "
         "print(sys.prefix); print(litex.__file__); print(p.data_location)")


def window(job: dict, shared: bool) -> list[dict]:
    """The leg's steps after setup-python up to the patch series, each accounted for."""
    names = [step.get("uses", "") for step in job["steps"]]
    start = next(i for i, uses in enumerate(names) if uses.startswith(SETUP_ACTION)) + 1
    steps = job["steps"][start:]
    end = next(i for i, step in enumerate(steps) if step.get("name") == LAST_STEP) + 1
    chosen = []
    for step in steps[:end]:
        name = step.get("name", "")
        if shared and name == PRIVATE_STEP:
            continue
        if name in SKIP:
            continue
        if name not in RUN or "run" not in step or "${{" in step["run"]:
            raise ValueError(f"{name!r}: a setup step this control neither runs nor declares")
        chosen.append(step)
    return chosen


def manifest(top: Path) -> dict[str, str]:
    """Every path under `top` with its type, mode and content or link target."""
    rows = {}
    for directory, dirs, files in os.walk(top):
        for name in sorted(dirs + files):
            path = Path(directory) / name
            stat = path.lstat()
            if path.is_symlink():
                what = "link " + os.readlink(path)
            elif path.is_dir():
                what = "dir"
            else:
                what = "file " + hashlib.sha256(path.read_bytes()).hexdigest()
            rows[str(path.relative_to(top))] = f"{stat.st_mode:o} {what}"
    return rows


def plant(python: Path, cache: Path) -> Path:
    """The tool cache's interpreter directory, laid out as setup-python finds it."""
    version = subprocess.run([python / "bin/python3", "-c",
                              "import platform; print(platform.python_version())"],
                             capture_output=True, text=True, check=True).stdout.strip()
    home = cache / "Python" / version / "x64"
    shutil.copytree(python, home, symlinks=True)
    # A hosted tool-cache interpreter carries no installer lock, so pip accepts it.
    for marker in home.glob("lib/python3*/EXTERNALLY-MANAGED"):
        marker.unlink()
    (cache / "Python" / version / "x64.complete").touch()
    return home


class Leg:
    """One job: its own home, temporary directory, workspace and step log."""

    def __init__(self, name: str, base: Path, rev: str, interpreter: Path,
                 pip_cache: Path | None) -> None:
        self.name, self.base = name, base
        self.home, self.temp, self.workspace = base / "home", base / "temp", base / "workspace"
        for path in (self.home, self.temp, self.workspace):
            path.mkdir(parents=True)
        if pip_cache:
            shutil.copytree(pip_cache, self.home / ".cache/pip", symlinks=True)
        archive = subprocess.run(["git", "-C", str(ROOT), "archive", rev],
                                 capture_output=True, check=True).stdout
        subprocess.run(["tar", "-x", "-C", str(self.workspace)], input=archive, check=True)
        self.paths = [str(interpreter / "bin")]
        self.env_file, self.path_file = base / "github_env", base / "github_path"
        self.extra: dict[str, str] = {}
        self.log = base / "steps.log"
        self.results: list[dict] = []

    def environment(self) -> dict[str, str]:
        """The variables a runner gives this job's next step."""
        env = {"HOME": str(self.home), "RUNNER_TEMP": str(self.temp), "LANG": "C.UTF-8",
               "GITHUB_ENV": str(self.env_file), "GITHUB_PATH": str(self.path_file),
               "PIP_CONSTRAINT": str(self.workspace / "ci/constraints-ci.txt"),
               "PATH": ":".join([*self.paths, BASE_PATH])}
        env.update(self.extra)
        return env

    def absorb(self) -> None:
        """Apply what the last step appended to GITHUB_PATH and GITHUB_ENV, as a runner does."""
        if self.path_file.exists():
            for line in self.path_file.read_text().splitlines():
                if line.strip():
                    self.paths.insert(0, line.strip())
            self.path_file.unlink()
        if self.env_file.exists():
            for line in self.env_file.read_text().splitlines():
                if "<<" in line.partition("=")[0]:
                    raise ValueError(f"{self.name}: multi-line GITHUB_ENV is not modelled")
                key, _, value = line.partition("=")
                if key:
                    self.extra[key] = value
            self.env_file.unlink()

    def run(self, label: str, argv: list[str]) -> int:
        """One step, timed, its output kept in the leg's log."""
        began = time.monotonic()
        with self.log.open("a") as out:
            out.write(f"===== {label}\n")
            out.flush()
            rc = subprocess.run(argv, cwd=self.workspace, env=self.environment(),
                                stdout=out, stderr=subprocess.STDOUT, check=False).returncode
        self.results.append({"step": label, "rc": rc,
                             "seconds": round(time.monotonic() - began, 1)})
        self.absorb()
        return rc


def drive(leg: Leg, steps: list[dict], barrier: threading.Barrier) -> None:
    """Run the steps in order, starting each together with the other leg."""
    for step in steps:
        try:
            barrier.wait()
        except threading.BrokenBarrierError:
            pass
        script = leg.base / "step.sh"
        script.write_text(step["run"])
        if leg.run(step["name"], ["bash", "-e", str(script)]) != 0:
            barrier.abort()
            return
    barrier.abort()


def verify(leg: Leg, cache: Path) -> list[str]:
    """Where the leg's interpreter lives, and whether gate 23h holds on its trees."""
    problems = []
    probe = subprocess.run(["python3", "-c", PROBE], cwd=leg.workspace,
                           env=leg.environment(), capture_output=True, text=True, check=False)
    places = probe.stdout.split()
    if probe.returncode != 0 or len(places) != 3:
        return [f"{leg.name}: the LiteX interpreter does not import ({probe.stderr.strip()})"]
    for place in places:
        if not Path(place).resolve().is_relative_to(leg.temp.resolve()):
            problems.append(f"{leg.name}: {place} is not under the leg's RUNNER_TEMP")
        if Path(place).resolve().is_relative_to(cache.resolve()):
            problems.append(f"{leg.name}: {place} is inside the shared tool cache")
    if leg.run("gate 23h", ["python3", "sw/builder/test_builder.py", "--gates", GATES]) != 0:
        problems.append(f"{leg.name}: gate 23h failed (see {leg.log})")
    return problems


def main() -> int:
    """Plant the cache, run both legs together, verify each and the cache."""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--python", type=Path, required=True,
                        help="a CPython installation prefix to plant as the tool cache's")
    parser.add_argument("--work", type=Path, required=True, help="an empty scratch directory")
    parser.add_argument("--rev", default="HEAD", help="the revision whose workflow and tree run")
    parser.add_argument("--shared", action="store_true",
                        help="drop the job-private environment step from both legs")
    parser.add_argument("--pip-cache", type=Path, help="a pip cache to restore into each home")
    parser.add_argument("--report", type=Path, help="write the JSON report here")
    args = parser.parse_args()
    if args.work.exists() and any(args.work.iterdir()):
        sys.exit(f"{args.work}: not empty")
    text = subprocess.run(["git", "-C", str(ROOT), "show", f"{args.rev}:{WORKFLOW}"],
                          capture_output=True, text=True, check=True).stdout
    jobs = yaml.safe_load(text)["jobs"]
    plans = {name: window(jobs[name], args.shared) for name in LEGS}
    cache = args.work / "toolcache"
    interpreter = plant(args.python.resolve(), cache)
    before = manifest(cache)
    legs = [Leg(name, args.work / name, args.rev, interpreter, args.pip_cache) for name in LEGS]
    barrier = threading.Barrier(len(legs))
    began = time.monotonic()
    threads = [threading.Thread(target=drive, args=(leg, plans[leg.name], barrier))
               for leg in legs]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    setup_seconds = round(time.monotonic() - began, 1)
    problems = []
    for leg in legs:
        failed = [row for row in leg.results if row["rc"] != 0]
        if failed or len(leg.results) != len(plans[leg.name]):
            problems.append(f"{leg.name}: setup did not pass every step: {leg.results}")
    for leg in legs:
        problems.extend(verify(leg, cache))
    after = manifest(cache)
    changed = sorted(path for path in before.keys() | after.keys()
                     if before.get(path) != after.get(path))
    if changed:
        problems.append(f"the tool cache changed at {len(changed)} paths, first {changed[:5]}")
    report = {"rev": subprocess.run(["git", "-C", str(ROOT), "rev-parse", args.rev],
                                    capture_output=True, text=True, check=True).stdout.strip(),
              "shared": args.shared, "planted_paths": len(before),
              "changed_paths": len(changed), "changed_sample": changed[:20],
              "setup_seconds": setup_seconds,
              "legs": {leg.name: leg.results for leg in legs},
              "problems": problems, "isolated": not problems}
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + "\n")
    for leg in legs:
        for row in leg.results:
            print(f"{leg.name}: {row['step']}: rc {row['rc']} in {row['seconds']} s")
    print(f"tool cache: {len(before)} planted paths, {len(changed)} changed")
    for problem in problems:
        print("PROBLEM: " + problem)
    print("ISOLATED" if not problems else "NOT ISOLATED")
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
