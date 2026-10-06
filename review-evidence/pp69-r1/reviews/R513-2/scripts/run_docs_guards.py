#!/usr/bin/env python3
"""Rerun the documentation gate with metadata and lint the interface guards."""
import concurrent.futures, json, os, pathlib, subprocess, sys
repo, packet = map(lambda x: pathlib.Path(x).resolve(), sys.argv[1:])
tree = packet/"scratch/focused-tree"
if not (tree/".git").exists():
    subprocess.run(["git", "init", "-q", str(tree)], check=True)
    subprocess.run(["git", "-C", str(tree), "fetch", "-q", "--no-tags", str(repo), "75c4eee4589e9317aca3d07b91f94a38b4cc86af"], check=True)
    subprocess.run(["git", "-C", str(tree), "reset", "-q", "--mixed", "75c4eee4589e9317aca3d07b91f94a38b4cc86af"], check=True)
env=os.environ.copy(); env["TMPDIR"]=str(packet/"scratch")
commands={"docs-check-metadata": ["make", "-j16", "check"],
          "interface-guards": ["make", "-j16", "-C", "tb/pp_top", "if-guards", "VERILATOR="+str(packet/"scripts/verilator_bounded.py")]}
def run(item):
    name, cmd = item
    with (packet/"receipts"/(name+".log")).open("w") as f:
        f.write("COMMAND " + json.dumps(cmd) + "\n"); f.flush()
        rc=subprocess.run(cmd,cwd=tree,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
    (packet/"receipts"/(name+".rc")).write_text(str(rc)+"\n")
    print(name,rc,flush=True)
    return rc
with concurrent.futures.ThreadPoolExecutor(2) as pool: results=list(pool.map(run, commands.items()))
sys.exit(any(results))
