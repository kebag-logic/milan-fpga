"""Run --control owner_report N times from a tree with J at once; count red runs and keep each red line.

Usage: python3 -I stress_owner_report.py <tree> <N> <J>
"""
import concurrent.futures, os, subprocess, sys
tree, n, j = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
def one(_i):
    p = subprocess.run([sys.executable, "-B", "scripts/test_suite_cancellation.py", "--control", "owner_report"], cwd=tree,
                       env=env, capture_output=True, text=True, timeout=120, stdin=subprocess.DEVNULL)
    lines = [l for l in (p.stdout + p.stderr).splitlines() if l.strip()]
    return p.returncode, lines[-1] if lines else ""
with concurrent.futures.ThreadPoolExecutor(j) as pool:
    res = list(pool.map(one, range(n)))
red = [l for rc, l in res if rc]
print(f"{tree.rstrip('/').split('/')[-1]} / owner_report: {n} runs, {len(red)} red, load at end {os.getloadavg()}")
for l in red:
    print("red:", l[:300])
