#!/usr/bin/env python3
"""Check every patch and plant all three exact-text tables in disposable copies."""
import argparse
import concurrent.futures
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

sys.dont_write_bytecode = True
parser = argparse.ArgumentParser()
parser.add_argument("repo", type=Path)
parser.add_argument("--jobs", type=int, default=4)
args = parser.parse_args()
assert 1 <= args.jobs <= 16
repo = args.repo.resolve()
packet = Path(__file__).resolve().parents[1]
pin = "2139f3dc10161b456dfbd51d2f73a63f9164e041"
base = "e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8"
tree = packet / "scratch/planting-head"
tree.mkdir(parents=True, exist_ok=False)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(["git", "-C", str(repo), "archive", pin]))) as archive:
    archive.extractall(tree, filter="data")
lines = ["  logic                cancel_hit_w;", "  logic [IFL_AW_C-1:0] cancel_ix_w;", "  logic       fifo_ne_w, fifo_full_w, vq_ne_w, vq_full_w;", "  logic       push_w, vd_push_w, vd_val_w, rd_fire_w, retire_w;"]
searches = []
for revision in [base, pin]:
    for line in lines:
        command = ["git", "-C", str(repo), "grep", "-n", "-F", "-e", line, revision, "--", "tb/**/*.patch", "tb/**/*.py"]
        p = subprocess.run(command, capture_output=True, text=True)
        searches.append({"revision": revision, "text": line, "rc": p.returncode, "stdout": p.stdout, "stderr": p.stderr})
        assert p.returncode == 1, searches[-1]
tracked = subprocess.check_output(["git", "-C", str(repo), "ls-tree", "-r", "--name-only", pin, "tb"], text=True).splitlines()
patches = [p for p in tracked if p.endswith(".patch")]

def check_patch(path):
    command = ["git", "apply", "--check", str(tree / path)]
    p = subprocess.run(command, cwd=tree, capture_output=True, text=True)
    return {"patch": path, "rc": p.returncode, "stdout": p.stdout, "stderr": p.stderr}

with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
    patch_results = list(pool.map(check_patch, patches))
assert len(patch_results) == 277 and all(r["rc"] == 0 for r in patch_results)
exact_results = []
for table in ["notify_mutants", "acmp_mutants", "d3_mutants"]:
    path = tree / "tb/pp_top" / (table + ".py")
    spec = importlib.util.spec_from_file_location(table, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[table] = module
    spec.loader.exec_module(module)
    for index, arm in enumerate(module.MUTANTS):
        with tempfile.TemporaryDirectory(prefix=table + "-", dir=packet / "scratch") as directory:
            scratch = Path(directory)
            for rel, _, _ in arm.edits:
                dest = scratch / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes((tree / rel).read_bytes())
            refusal = module.plant(scratch, arm.edits)
            exact_results.append({"table": table, "index": index, "name": arm.name, "suite": arm.suite.directory, "paths": [edit[0] for edit in arm.edits], "refusal": refusal})
            assert not refusal, exact_results[-1]
assert len(exact_results) == 199
result = {"pin": pin, "jobs": args.jobs, "searches": searches, "patches": patch_results, "exact_text_arms": exact_results, "patch_count": len(patch_results), "exact_arm_count": len(exact_results), "planting_only": True}
(packet / "receipts/planting.json").write_text(json.dumps(result, indent=2) + "\n")
print(f"PASS: {len(patch_results)} patch applications checked; {len(exact_results)} exact-text arms planted; 8 fixed-text searches had no match")
