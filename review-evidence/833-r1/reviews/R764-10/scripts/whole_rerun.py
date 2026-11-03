#!/usr/bin/env python3
"""Re-run the whole suite-cancellation test, SIGHUP at its default, on the head copy and every sweep survivor tree.

usage: whole_rerun.py HEAD_TREE SWEEP_JSON RAW_DIR OUT.json JOBS
A launcher that ignores SIGHUP (nohup) makes the whole test's HUP stops time out; this resets it for each run.
"""
import concurrent.futures, json, os, signal, subprocess, sys, time
from pathlib import Path

head, sweep, raw, out, jobs = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]), int(sys.argv[5])
result = json.loads(sweep.read_text())["result"]
survivors = [k for k, v in result.items() if k != "none" and not v["red"]]
trees = {"none (head)": head, **{s: raw / s.replace("/", "__") for s in survivors}}
env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}

def run(item):
    name, root = item
    began = time.monotonic()
    try:
        p = subprocess.run([sys.executable, "-B", str(root / "scripts/test_suite_cancellation.py")], cwd=root, env=env,
                           stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=600, start_new_session=True,
                           preexec_fn=lambda: signal.signal(signal.SIGHUP, signal.SIG_DFL))
        rc, text = p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        rc, text = None, "cut at 600 s"
    lines = [l for l in text.splitlines() if l.strip()]
    return name, rc, round(time.monotonic() - began, 1), (lines[-1][:200] if lines else "")

with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    rows = list(pool.map(run, trees.items()))
out.write_text(json.dumps(rows, indent=1))
for name, rc, secs, last in rows:
    print(f"{name}: whole rc {rc} {secs} s: {last[:120]}")
print(f"survivors green on the whole test: {sum(1 for n, rc, *_ in rows[1:] if rc == 0)} of {len(rows) - 1}")
