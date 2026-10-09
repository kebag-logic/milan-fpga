#!/usr/bin/env python3
"""Re-run only the explicit campaign in the prepared head tree after an interrupted session."""
import argparse, json, os, pathlib, subprocess, time
HEAD = "62c261c2d1b899a9cf90c901b25b5a85846dfef6"
p = argparse.ArgumentParser()
p.add_argument("--tree", type=pathlib.Path, required=True)
p.add_argument("--compiler", type=pathlib.Path, required=True)
p.add_argument("--receipts", type=pathlib.Path, required=True)
p.add_argument("--workers", type=int, default=16)
a = p.parse_args()
tree, receipts = a.tree.resolve(), a.receipts.resolve()
assert subprocess.check_output(["git", "-C", str(tree), "rev-parse", "HEAD"], text=True).strip() == HEAD
assert subprocess.check_output(["git", "-C", str(tree), "status", "--porcelain"], text=True) == ""
version = subprocess.check_output([str(a.compiler), "--version"], text=True).strip()
assert "5.050" in version
render = tree / "tb/verilator/milan_dp_render"
# Discard every ignored build product of the interrupted run so nothing partial is reused.
subprocess.run(["git", "-C", str(render), "clean", "-fdXq", "."], check=True)
env = os.environ.copy()
for key in ("MAKEFLAGS", "MFLAGS", "MAKELEVEL"):
    env.pop(key, None)
temp = tree.parent / "campaign-tmp"; temp.mkdir(exist_ok=True)
env.update(VERILATOR=str(a.compiler.resolve()), VERILATOR_JOBS=str(a.workers), TMPDIR=str(temp), PYTHONUNBUFFERED="1")
cmd = ["make", "-j16", "-C", "tb/verilator/milan_dp_render", "tdm8render-mutants"]
started = time.monotonic()
with (receipts / "campaign.log").open("w") as log:
    result = subprocess.run(cmd, cwd=tree, env=env, stdout=log, stderr=subprocess.STDOUT)
elapsed = time.monotonic() - started
(receipts / "campaign.rc").write_text(str(result.returncode) + "\n")
(receipts / "campaign.json").write_text(json.dumps({"head": HEAD, "argv": cmd, "compiler": version, "build_workers": a.workers, "elapsed_seconds": elapsed, "rc": result.returncode, "note": "rerun after an interrupted session; ignored build products cleaned first"}, indent=2) + "\n")
raise SystemExit(result.returncode)
