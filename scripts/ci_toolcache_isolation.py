#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run both elaboration legs' toolchain setup at once on one planted tool cache.

act mounts one tool-cache volume into every job container of a replay, while
each job keeps its own HOME, RUNNER_TEMP and workspace. This control rebuilds
that sharing in one process tree, with no container: it copies a CPython
installation into a planted tool cache and runs the setup steps of both
elaboration legs, read from the workflow at --rev, side by side. Each leg has
its own home, temporary directory, workspace and PATH and environment files,
and every step of both legs starts together, which is when two act jobs on one
tool cache collide (#748; REQ-VER-04).

The legs are isolated when every step of both passes, each leg's LiteX
interpreter and VexiiRiscv checkout live under that leg's RUNNER_TEMP, gate
23h and its negative control each ran and passed in each leg, and every path
of the tool cache is byte for byte what was planted. A patch check that did
not run, for want of a dependency or for any other recorded reason, is a
failure named by the check: a skipped check proves nothing about the trees.
Anything else exits 1.

--gate-legs then runs each leg's elaboration gate step, both started together,
before the tool cache is compared, so the Scala generation and every gate that
writes through the LiteX interpreter are inside the comparison too. That needs
the three source dependencies initialised in this checkout, an installed RV32
SDK (--rv32-sdk), and sv2v and sbt on --tool-dir or the system PATH. The fetch
step is replaced by initialising those dependencies from this checkout.

--shared drops the job-private environment step from both legs, so both
install, clone and patch in the tool cache's own site-packages. A --rev that
predates that step plants the same sharing from its own workflow text.

Every path argument may be relative; each is made absolute before anything is
derived from it.

Run: python3 scripts/ci_toolcache_isolation.py --python <CPython prefix>
         --work <empty scratch directory> [--rev REV] [--shared]
         [--pip-cache DIR] [--report FILE]
         [--gate-legs --rv32-sdk DIR [--tool-dir DIR ...]]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
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
                   "the gate legs use an sbt on --tool-dir or the system PATH",
}
#: With --gate-legs: the step before setup-python whose environment the gate
#: legs read, the one that fetches their source dependencies, and the step
#: prefixes after the patch series that run.
BUDGET_STEP = "Set CPU-derived job budgets"
FETCH_STEP = "Fetch the source dependencies the elaboration reads"
TAIL_RUN = ("Elaboration gates, leg ", "Keep the generated CPU netlist arguments")
#: The other step prefixes after the patch series, and why each is left out.
TAIL_SKIP = {
    "Cache the pinned RV32 SDK": "--rv32-sdk links an installed SDK into each leg's home",
    "Install and verify the pinned RV32 SDK": "--rv32-sdk links an installed SDK into "
                                              "each leg's home",
    "Cache the pinned Verilator build": "only the LiteX aggregate reads Verilator",
    "Resolve exact package downloads": "only the LiteX aggregate reads Verilator",
    "Cache exact package downloads": "only the LiteX aggregate reads Verilator",
    "Build Verilator from source": "only the LiteX aggregate reads Verilator",
    "Put Verilator on PATH": "only the LiteX aggregate reads Verilator",
    "Standalone LiteX simulation aggregate": "needs the pinned Verilator build; it runs "
                                             "the interpreter the probe places",
    "Record executed gate outcomes": "writes the hosted receipt under RUNNER_TEMP",
    "Upload executed gate outcomes": "an upload, no toolchain write",
    "Record actual job execution": "writes the hosted receipt under RUNNER_TEMP",
    "Upload actual job execution": "an upload, no toolchain write",
}
#: Gate 23h and its negative control. Each must run and pass in each leg.
GATES = ("test_toolchain_patches_are_applied", "test_toolchain_patch_gate_bites")
BASE_PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
PROBE = ("import sys, litex, pythondata_cpu_vexiiriscv as p; "
         "print(sys.prefix); print(litex.__file__); print(p.data_location)")


def shell(step: dict) -> bool:
    """Whether the step is a script this control can run: text, with no expression in it."""
    return isinstance(step.get("run"), str) and "${{" not in step["run"]


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
        if name not in RUN or not shell(step):
            raise ValueError(f"{name!r}: a setup step this control neither declares "
                             "nor can run as a script")
        chosen.append(step)
    return chosen


def tail(job: dict) -> list[dict]:
    """The job-budget step, then the leg's steps after the patch series, each accounted for."""
    named = {step.get("name", ""): step for step in job["steps"]}
    steps = job["steps"]
    start = next(i for i, step in enumerate(steps) if step.get("name") == LAST_STEP) + 1
    chosen = [named[BUDGET_STEP]]
    for step in steps[start:]:
        name = step.get("name", "")
        if name.startswith(tuple(TAIL_SKIP)):
            continue
        if not name.startswith(TAIL_RUN) or not shell(step):
            raise ValueError(f"{name!r}: a gate-leg step this control neither declares "
                             "nor can run as a script")
        chosen.append(step)
    if not shell(chosen[0]):
        raise ValueError(f"{BUDGET_STEP!r}: not a script this control can run")
    return chosen


def modules(job: dict) -> list[str]:
    """The source dependencies the leg's fetch step initialises."""
    step = next(step for step in job["steps"] if step.get("name") == FETCH_STEP)
    found = re.fullmatch(r"git submodule update --init ([\w./ -]+)", step["run"].strip())
    if not found:
        raise ValueError(f"{FETCH_STEP!r}: not the submodule fetch this control models")
    return found.group(1).split()


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


def digest(rows: dict[str, str]) -> str:
    """One hash over a whole manifest, so two of them compare in a receipt."""
    return hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()


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


def checkout(workspace: Path, rev: str, paths: list[str]) -> None:
    """A clone at `rev` with `paths` initialised from this checkout's own dependencies.

    The gate legs bind their receipts to the head and tree, which needs a git
    checkout; the setup steps need only the files.
    """
    subprocess.run(["git", "clone", "-q", "--no-checkout", str(ROOT), str(workspace)],
                   check=True)
    subprocess.run(["git", "-C", str(workspace), "checkout", "-q", "--detach", rev], check=True)
    for path in paths:
        source = ROOT / path
        top = subprocess.run(["git", "-C", str(source), "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=False).stdout.strip()
        if not top or Path(top).resolve() != source.resolve():
            raise ValueError(f"{source}: not an initialised source dependency")
        subprocess.run(["git", "-C", str(workspace), "submodule", "init", path],
                       capture_output=True, check=True)
        subprocess.run(["git", "-C", str(workspace), "config", f"submodule.{path}.url",
                        str(source)], check=True)
        subprocess.run(["git", "-C", str(workspace), "-c", "protocol.file.allow=always",
                        "submodule", "update", "-q", path], check=True)


class Leg:
    """One job: its own home, temporary directory, workspace and step log."""

    def __init__(self, name: str, base: Path, interpreter: Path,
                 args: argparse.Namespace, paths: list[str] | None) -> None:
        self.name, self.base = name, base
        self.home, self.temp, self.workspace = base / "home", base / "temp", base / "workspace"
        for path in (self.home, self.temp):
            path.mkdir(parents=True)
        if args.pip_cache:
            shutil.copytree(args.pip_cache, self.home / ".cache/pip", symlinks=True)
        if paths is None:
            self.workspace.mkdir()
            archive = subprocess.run(["git", "-C", str(ROOT), "archive", args.rev],
                                     capture_output=True, check=True).stdout
            subprocess.run(["tar", "-x", "-C", str(self.workspace)], input=archive, check=True)
        else:
            checkout(self.workspace, args.rev, paths)
            (self.home / "br-milan-rv32").symlink_to(args.rv32_sdk)
        self.paths = [str(interpreter / "bin")]
        self.tools = [str(path) for path in args.tool_dir]
        self.env_file, self.path_file = base / "github_env", base / "github_path"
        self.extra: dict[str, str] = {}
        self.log = base / "steps.log"
        self.results: list[dict] = []

    def environment(self) -> dict[str, str]:
        """The variables a runner gives this job's next step."""
        # act's RUNNER_TEMP is /tmp, so a job's temporary files land in it too.
        env = {"HOME": str(self.home), "RUNNER_TEMP": str(self.temp), "LANG": "C.UTF-8",
               "TMPDIR": str(self.temp),
               "GITHUB_ENV": str(self.env_file), "GITHUB_PATH": str(self.path_file),
               "PIP_CONSTRAINT": str(self.workspace / "ci/constraints-ci.txt"),
               "PATH": ":".join([*self.paths, *self.tools, BASE_PATH])}
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


def together(legs: list[Leg], plans: dict[str, list[dict]]) -> tuple[float, list[str]]:
    """Run each leg's plan side by side; the seconds taken and any leg that fell short."""
    barrier = threading.Barrier(len(legs))
    began = time.monotonic()
    marks = {leg.name: len(leg.results) for leg in legs}
    threads = [threading.Thread(target=drive, args=(leg, plans[leg.name], barrier))
               for leg in legs]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    problems = []
    for leg in legs:
        rows = leg.results[marks[leg.name]:]
        if any(row["rc"] != 0 for row in rows) or len(rows) != len(plans[leg.name]):
            problems.append(f"{leg.name}: not every step passed: {rows}")
    return round(time.monotonic() - began, 1), problems


def checks(name: str, rc: int, receipt: Path) -> tuple[dict[str, str], list[str]]:
    """What each patch check did, from the driver's own receipt, and what that refuses.

    The exit code alone cannot carry this: the driver records a check that
    found no interpreter importing migen, litex and litex_boards as NOT RUN
    and still exits 0, which here would read a missing dependency as a pass.
    """
    if not receipt.exists():
        return ({gate: "no receipt" for gate in GATES},
                [f"{name}: gate 23h wrote no receipt (rc {rc}), so neither patch check "
                 "is known to have run"])
    ledger = {row["gate"]: row for row in json.loads(receipt.read_text())["gates"]}
    status, problems = {}, []
    for gate in GATES:
        row = ledger.get(gate)
        if row is None or row["verdict"] != "pass":
            status[gate] = "did not run"
        elif row["not_run"]:
            status[gate] = "NOT RUN: " + "; ".join(f"[{arm}] {why}"
                                                   for arm, why, _kind in row["not_run"])
        else:
            status[gate] = "ran and passed"
        if status[gate] != "ran and passed":
            problems.append(f"{name}: {gate} {status[gate]}")
    if rc != 0:
        problems.append(f"{name}: gate 23h exited {rc}")
    return status, problems


def verify(leg: Leg, cache: Path) -> tuple[dict[str, str], list[str]]:
    """Where the leg's interpreter lives, and whether both patch checks ran and held."""
    problems = []
    probe = subprocess.run(["python3", "-c", PROBE], cwd=leg.workspace,
                           env=leg.environment(), capture_output=True, text=True, check=False)
    places = probe.stdout.split()
    if probe.returncode != 0 or len(places) != 3:
        problems.append(f"{leg.name}: the LiteX interpreter does not import "
                        f"({probe.stderr.strip()})")
        places = []
    for place in places:
        if not Path(place).resolve().is_relative_to(leg.temp.resolve()):
            problems.append(f"{leg.name}: {place} is not under the leg's RUNNER_TEMP")
        if Path(place).resolve().is_relative_to(cache.resolve()):
            problems.append(f"{leg.name}: {place} is inside the shared tool cache")
    receipt = leg.base / "gate-23h.json"
    rc = leg.run("gate 23h", ["python3", "sw/builder/test_builder.py", "--gates",
                              ",".join(GATES), "--receipt", str(receipt)])
    status, refused = checks(leg.name, rc, receipt)
    return status, problems + refused


def arguments() -> argparse.Namespace:
    """The command line, with every path made absolute and --rev a commit before use."""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--python", type=Path, required=True,
                        help="a CPython installation prefix to plant as the tool cache's")
    parser.add_argument("--work", type=Path, required=True,
                        help="an empty scratch directory, relative or absolute")
    parser.add_argument("--rev", default="HEAD", help="the revision whose workflow and tree run")
    parser.add_argument("--shared", action="store_true",
                        help="drop the job-private environment step from both legs")
    parser.add_argument("--pip-cache", type=Path, help="a pip cache to restore into each home")
    parser.add_argument("--report", type=Path, help="write the JSON report here")
    parser.add_argument("--gate-legs", action="store_true",
                        help="run each leg's elaboration gate step before the final comparison")
    parser.add_argument("--rv32-sdk", type=Path,
                        help="an installed RV32 SDK, linked into each home for --gate-legs")
    parser.add_argument("--tool-dir", type=Path, action="append", default=[],
                        help="a directory put on each leg's PATH after its interpreters")
    args = parser.parse_args()
    # Each step runs in its leg's workspace, where a relative path names
    # something else, so no path is kept relative.
    for key in ("python", "work", "pip_cache", "report", "rv32_sdk"):
        if getattr(args, key) is not None:
            setattr(args, key, getattr(args, key).resolve())
    args.tool_dir = [path.resolve() for path in args.tool_dir]
    if args.gate_legs and (args.rv32_sdk is None or not args.rv32_sdk.is_dir()):
        parser.error("--gate-legs needs --rv32-sdk naming an installed SDK directory")
    if args.work.exists() and any(args.work.iterdir()):
        parser.error(f"--work {args.work}: not empty")
    found = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--verify", "--quiet",
                            f"{args.rev}^{{commit}}"], capture_output=True, text=True, check=False)
    if found.returncode != 0:
        parser.error(f"--rev {args.rev}: not a commit")
    args.rev = found.stdout.strip()
    return args


def main() -> int:
    """Plant the cache, run both legs together, verify each and the cache."""
    args = arguments()
    text = subprocess.run(["git", "-C", str(ROOT), "show", f"{args.rev}:{WORKFLOW}"],
                          capture_output=True, text=True, check=True).stdout
    jobs = yaml.safe_load(text)["jobs"]
    plans = {name: window(jobs[name], args.shared) for name in LEGS}
    tails = {name: tail(jobs[name]) for name in LEGS} if args.gate_legs else {}
    cache = args.work / "toolcache"
    interpreter = plant(args.python, cache)
    before = manifest(cache)
    legs = [Leg(name, args.work / name, interpreter, args,
                modules(jobs[name]) if args.gate_legs else None) for name in LEGS]
    setup_seconds, problems = together(legs, plans)
    status = {}
    for leg in legs:
        status[leg.name], refused = verify(leg, cache)
        problems.extend(refused)
    gate_seconds = None
    if args.gate_legs and problems:
        problems.append("gate legs not run: the setup above did not isolate")
    elif args.gate_legs:
        gate_seconds, refused = together(legs, tails)
        problems.extend(refused)
    after = manifest(cache)
    changed = sorted(path for path in before.keys() | after.keys()
                     if before.get(path) != after.get(path))
    if changed:
        problems.append(f"the tool cache changed at {len(changed)} paths, first {changed[:5]}")
    report = {"rev": args.rev, "shared": args.shared, "gate_legs": args.gate_legs,
              "planted_paths": len(before), "changed_paths": len(changed),
              "planted_manifest_sha256": digest(before), "final_manifest_sha256": digest(after),
              "changed_sample": changed[:20],
              "setup_seconds": setup_seconds, "gate_leg_seconds": gate_seconds,
              "patch_checks": status,
              "legs": {leg.name: leg.results for leg in legs},
              "problems": problems, "isolated": not problems}
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + "\n")
    for leg in legs:
        for row in leg.results:
            print(f"{leg.name}: {row['step']}: rc {row['rc']} in {row['seconds']} s")
        for gate, what in status[leg.name].items():
            print(f"{leg.name}: {gate}: {what}")
    print(f"tool cache: {len(before)} planted paths, {len(changed)} changed; manifest "
          f"{report['planted_manifest_sha256']} planted, {report['final_manifest_sha256']} final")
    for problem in problems:
        print("PROBLEM: " + problem)
    print("ISOLATED" if not problems else "NOT ISOLATED")
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
