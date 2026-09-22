#!/usr/bin/env python3
"""Portable, full milan_dp measurement; telemetry is not a test verdict.

Invoke with --lane, --out, --verilator, --expect-head, --jobs 1|2 and
--temperature cold|warm. The output directory must not exist. Cold means
the suite's existing clean target, not eviction of the operating-system cache.
Warm means reuse the preceding run's build artifacts. Both run the entire
unchanged default suite, including gPTP prerequisites and render mutants.
"""
import argparse
import hashlib
import json
import os
import resource
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def capture(cmd, **kw):
    return subprocess.check_output(["rtk", "proxy", *map(str, cmd)], text=True, **kw)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def identities(lane):
    roots = ("hdl", "protocol-processor/hdl", "gptp-processor/hdl", "configs",
             "third_party/verilog-axis/rtl", "sw/builder", "avdecc")
    paths = set()
    for name in roots:
        paths.update(p for p in (lane / name).rglob("*") if p.is_file()
                     and p.suffix in (".sv", ".svh", ".v", ".py", ".yaml", ".json")
                     and "out" not in p.relative_to(lane / name).parts)
    suite = lane / "tb/verilator/milan_dp"
    paths.update(p for p in suite.iterdir() if p.suffix in (".cpp", ".hex"))
    paths.update(p for p in (suite / "gen_divergent").rglob("*") if p.is_file())
    return {str(p.relative_to(lane)): digest(p) for p in sorted(paths)}


def headers(lane, destination):
    destination.mkdir()
    for name in ("endstation_ax7101_1x1_tdm8", "endstation_arty_4x4", "endstation_ax7101_8x8"):
        relative = f"configs/generated/{name}/gen/adp_shape_defaults.svh"
        data = (lane / relative).read_bytes()
        committed = subprocess.check_output(["rtk", "proxy", "git", "-C", str(lane), "show", f"HEAD:{relative}"])
        if data != committed:
            raise RuntimeError(f"tracked header differs from committed bytes: {relative}")
        (destination / f"{name}.svh").write_bytes(data)


def tool_files(verilator):
    root = Path(capture([verilator, "--getenv", "VERILATOR_ROOT"]).strip())
    candidates = [verilator.resolve(), root / "bin/verilator", root / "bin/verilator_bin",
                  root.parent.parent / "bin/verilator", root.parent.parent / "bin/verilator_bin"]
    found = {str(p): digest(p) for p in candidates if p.is_file()}
    if not any(Path(p).name == "verilator_bin" for p in found):
        raise RuntimeError("cannot establish installed Verilator binary identity")
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lane", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--verilator", type=Path, required=True)
    ap.add_argument("--expect-head", required=True)
    ap.add_argument("--jobs", type=int, choices=(1, 2), required=True)
    ap.add_argument("--temperature", choices=("cold", "warm"), required=True)
    args = ap.parse_args()
    lane, out = args.lane.resolve(), args.out.resolve()
    head = capture(["git", "-C", lane, "rev-parse", "HEAD"]).strip()
    if head != args.expect_head or capture(["git", "-C", lane, "status", "--porcelain"]):
        raise SystemExit("refusing dirty or unexpected source")
    version = capture([args.verilator, "--version"]).strip()
    if not version.startswith("Verilator 5.050 "):
        raise SystemExit("refusing tool other than pinned Verilator 5.050")
    out.mkdir(parents=True, exist_ok=False)
    suite = lane / "tb/verilator/milan_dp"
    env = dict(os.environ)
    env.update(PATH=str(args.verilator.resolve().parent) + os.pathsep + env["PATH"],
               VERILATOR_JOBS="8", SIM_JOBS=str(args.jobs), MAKEFLAGS="", MFLAGS="")
    for key in ("MILAN_COUNTER_FRAME_OUT", "MAKELEVEL", "MAKEOVERRIDES"):
        env.pop(key, None)
    # Preserve one scratch root and identical inherited affinity/limits for all runs.
    scratch = out.parent / "scratch"
    scratch.mkdir(exist_ok=True)
    env["TMPDIR"] = str(scratch)
    cmd = ["make", "-j1", "-C", str(suite), "run"]
    cgroup = Path("/proc/self/cgroup").read_text().strip().split(":", 2)[-1]
    cgroot = Path("/sys/fs/cgroup") / cgroup.lstrip("/")
    identity = dict(head=head, tree=capture(["git", "-C", lane, "rev-parse", "HEAD^{tree}"]).strip(),
                    tool=str(args.verilator.resolve()), tool_sha256=digest(args.verilator), tool_files=tool_files(args.verilator),
                    version=version, command=cmd, mode=args.temperature,
                    affinity=sorted(os.sched_getaffinity(0)),
                    environment={k: env.get(k) for k in ("PATH", "VERILATOR_JOBS", "SIM_JOBS",
                                                         "TMPDIR", "MAKEFLAGS", "MFLAGS")},
                    limits={str(k): resource.getrlimit(k) for k in
                            (resource.RLIMIT_AS, resource.RLIMIT_CPU, resource.RLIMIT_NPROC,
                             resource.RLIMIT_NOFILE, resource.RLIMIT_STACK)},
                    cgroup={n: (cgroot / n).read_text() for n in
                            ("cpu.max", "memory.max", "memory.swap.max", "cpuset.cpus.effective")
                            if (cgroot / n).exists()},
                    submodules=capture(["git", "-C", lane, "submodule", "status"]))
    dump(out / "identity.json", identity)
    dump(out / "inputs-before.json", identities(lane))
    headers(lane, out / "headers-before")
    if args.temperature == "cold":
        with (out / "clean.log").open("wb") as log:
            subprocess.run(["rtk", "proxy", "make", "-C", str(suite), "clean"], env=env,
                           stdout=log, stderr=subprocess.STDOUT, check=True)
    (out / "make-dry-run.txt").write_text(capture(["make", "-n", "-j1", "-C", suite, "run"], env=env))
    observe = [sys.executable, str(HERE / "observe.py"), "--log", str(out / "milan_dp.log"),
               "--samples", str(out / "samples.jsonl"), "--summary", str(out / "summary.json"),
               "--interval", "0.1", "--", *cmd]
    rc = subprocess.run(["rtk", "proxy", *observe], cwd=lane, env=env).returncode
    if (suite / "obj_legs").exists():
        shutil.copytree(suite / "obj_legs", out / "legs")
    dump(out / "inputs-after.json", identities(lane))
    headers(lane, out / "headers-after")
    assert tool_files(args.verilator) == identity["tool_files"], "tool changed during run"
    dump(out / "executables.json", {str(p.relative_to(suite)): digest(p)
                                     for p in sorted(suite.glob("obj_*/Vmilan_dp_*")) if p.is_file()})
    verdict = subprocess.run(["rtk", "proxy", sys.executable, str(lane / "scripts/suite_tally.py"),
                              "--verdict", str(out / "milan_dp.log")], capture_output=True)
    (out / "verdict.txt").write_bytes(verdict.stdout + verdict.stderr)
    tally_dir = out / "tally"
    tally_dir.mkdir()
    shutil.copy2(out / "milan_dp.log", tally_dir / "milan_dp.log")
    tally = subprocess.run(["rtk", "proxy", sys.executable, str(lane / "scripts/suite_tally.py"),
                            str(tally_dir)], capture_output=True)
    (out / "tally.txt").write_bytes(tally.stdout + tally.stderr)
    status = capture(["git", "-C", lane, "status", "--porcelain"])
    (out / "status-after.txt").write_text(status)
    ending = capture(["git", "-C", lane, "rev-parse", "HEAD"]).strip()
    dump(out / "exit.json", dict(make=rc, verdict=verdict.returncode, tally=tally.returncode,
                                 clean=not status, same_head=ending == head))
    return int(bool(rc or verdict.returncode or tally.returncode or status or ending != head))


if __name__ == "__main__":
    sys.exit(main())
