#!/usr/bin/env python3
"""Run focused review checks concurrently; every child is waited in the foreground.
Usage: python3 run_focused.py SOURCE_REPOSITORY PACKET_DIRECTORY
At most five builds at three native jobs each; no implementation source is changed.
"""
import concurrent.futures, json, os, pathlib, subprocess, sys, tarfile
repo, packet = map(lambda x: pathlib.Path(x).resolve(), sys.argv[1:])
scratch = packet / "scratch"
scratch.mkdir(exist_ok=True)
tree = scratch / "focused-tree"
if not tree.exists():
    tree.mkdir()
    archive = scratch / "exact-head.tar"
    with archive.open("wb") as f:
        subprocess.run(["git", "-C", str(repo), "archive", "75c4eee4589e9317aca3d07b91f94a38b4cc86af"], stdout=f, check=True)
    with tarfile.open(archive) as t: t.extractall(tree, filter="data")
if not (tree / ".git").exists():
    subprocess.run(["git", "init", "-q", str(tree)], check=True)
    subprocess.run(["git", "-C", str(tree), "fetch", "-q", "--no-tags", str(repo), "75c4eee4589e9317aca3d07b91f94a38b4cc86af"], check=True)
    subprocess.run(["git", "-C", str(tree), "reset", "-q", "--mixed", "75c4eee4589e9317aca3d07b91f94a38b4cc86af"], check=True)
env = os.environ.copy()
env.update(TMPDIR=str(scratch), MAKEFLAGS="-j16", PYTHONDONTWRITEBYTECODE="1")
verilator = str(packet / "scripts/verilator_bounded.py")
mutants = "cancel_one_per_command report_fail_ignores_probe report_rsp_ignores_probe owner_turns_dropped settle_dropped depth_shared depth_not_keyed registry_tag_port_bits monitor_tag_port_bits expiry_port_dropped rgy_port_from_latest_frame dereg_matches_other_port".split()
cmds = {
    "round2-controls": ["python3", "tb/pp_top/notify_mutants.py", "--output", str(packet/"receipts/round2-controls"), "--verilator", verilator, "--jobs", "3", "--only", *mutants],
    "notify-suite": ["make", "-j16", "-C", "tb/aecp_notify", "VERILATOR="+verilator, "run"],
    "adp-suite": ["make", "-j16", "-C", "tb/adp_engine", "VERILATOR="+verilator, "run"],
    "docs-check": ["make", "-j16", "check"],
}
def run(item):
    name, cmd = item
    log = packet/"receipts"/(name+".log")
    with log.open("w") as f:
        f.write("COMMAND " + json.dumps(cmd) + "\n"); f.flush()
        rc = subprocess.run(cmd, cwd=tree, env=env, stdout=f, stderr=subprocess.STDOUT).returncode
    (packet/"receipts"/(name+".rc")).write_text(str(rc)+"\n")
    print(name, "rc", rc, flush=True)
    return name, rc
with concurrent.futures.ThreadPoolExecutor(4) as pool:
    results = dict(pool.map(run, cmds.items()))
(packet/"receipts/focused-results.json").write_text(json.dumps(results, indent=2)+"\n")
sys.exit(any(results.values()))
