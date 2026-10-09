#!/usr/bin/env python3
"""Run independent focused receipts; all child processes are joined."""
import argparse, concurrent.futures, json, os, pathlib, subprocess, time
HEAD = "62c261c2d1b899a9cf90c901b25b5a85846dfef6"
p = argparse.ArgumentParser()
p.add_argument("--source", type=pathlib.Path, required=True)
p.add_argument("--compiler", type=pathlib.Path, required=True)
p.add_argument("--packet", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parents[1])
a = p.parse_args()
source, packet = a.source.resolve(), a.packet.resolve()
scratch, receipts = packet / "scratch", packet / "receipts"
scratch.mkdir(exist_ok=True); receipts.mkdir(exist_ok=True)
cpus = sorted(os.sched_getaffinity(0))
assert len(cpus) >= 16
assert subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip() == HEAD
version = subprocess.check_output([str(a.compiler), "--version"], text=True).strip()
assert "5.050" in version
(receipts / "compiler.txt").write_text(version + "\n")

def prepare(name):
    dest = scratch / name
    with (receipts / (name + "-setup.log")).open("w") as log:
        def run(cmd):
            subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=True)
        run(["git", "clone", "--shared", "--no-checkout", str(source), str(dest)])
        run(["git", "-C", str(dest), "checkout", "--detach", HEAD])
        for sub in ("protocol-processor", "gptp-processor", "third_party/verilog-axis"):
            run(["git", "-C", str(dest), "-c", "protocol.file.allow=always", "submodule", "update", "--init", "--reference", str(source/sub), "--", sub])
    return dest

def campaign(name, affinity, workers, target):
    dest = prepare(name)
    env = os.environ.copy()
    for key in ("MAKEFLAGS", "MFLAGS", "MAKELEVEL"):
        env.pop(key, None)
    temp = scratch / (name + "-tmp"); temp.mkdir(exist_ok=True)
    env.update(VERILATOR=str(a.compiler.resolve()), VERILATOR_JOBS=str(workers), TMPDIR=str(temp), PYTHONUNBUFFERED="1")
    cmd = ["taskset", "-c", ",".join(map(str, affinity)), "make"]
    # Keep the measured default's outer make serial. Campaign builds are bounded.
    if target:
        cmd += ["-j16"]
    cmd += ["-C", "tb/verilator/milan_dp_render"] + target
    started = time.monotonic()
    print(name + " started", flush=True)
    with (receipts / (name + ".log")).open("w") as log:
        result = subprocess.run(cmd, cwd=dest, env=env, stdout=log, stderr=subprocess.STDOUT)
    elapsed = time.monotonic() - started
    (receipts / (name + ".rc")).write_text(str(result.returncode)+"\n")
    (receipts / (name + ".json")).write_text(json.dumps({"head":HEAD,"argv":cmd,"compiler":version,"build_workers":workers,"affinity_count":len(affinity),"elapsed_seconds":elapsed,"rc":result.returncode}, indent=2)+"\n")
    print(name + " finished rc="+str(result.returncode)+" elapsed="+str(elapsed), flush=True)
    return result.returncode

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    tasks = [pool.submit(campaign, "default", cpus[:4], 4, []),
             pool.submit(campaign, "campaign", cpus[4:], 6, ["tdm8render-mutants"])]
    results = [f.result() for f in tasks]
raise SystemExit(1 if any(results) else 0)
