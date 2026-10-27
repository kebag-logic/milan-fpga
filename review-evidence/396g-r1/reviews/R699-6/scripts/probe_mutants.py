"""Re-run named release controls in parallel, each in its own copy.

usage: python3 -I probe_mutants.py <repo> <workdir> <jobs> <out.json> <name>...
A control is killed when the mutated planner's --self-test exits 1 and names
the control's test as FAIL, as tb/tools/torture_release_mutants.py requires.
"""
import concurrent.futures
import importlib.util
import json
import os
import subprocess
import sys
import time


def main():
    repo, work, jobs, out, names = sys.argv[1], os.path.abspath(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5:]
    tools = os.path.join(repo, "tb", "tools")
    sys.path.insert(0, tools)
    spec = importlib.util.spec_from_file_location("trm", os.path.join(tools, "torture_release_mutants.py"))
    trm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(trm)
    table = {m[0]: m for m in trm.MUTANTS}
    text = open(os.path.join(tools, "torture_campaign.py"), encoding="utf-8").read()

    def run(name):
        _, old, new, test = table[name]
        if text.count(old) != 1:
            return name, test, "anchor-count", None, 0
        d = os.path.join(work, "m%03d" % list(table).index(name))
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, "torture_campaign.py")
        open(path, "w", encoding="utf-8").write(text.replace(old, new))
        t0 = time.time()
        try:
            r = subprocess.run([sys.executable, "-B", path, "--self-test"], capture_output=True, text=True,
                               timeout=1200, cwd=d)
        except subprocess.TimeoutExpired:
            return name, test, "timeout", None, time.time() - t0
        killed = r.returncode == 1 and f"FAIL: {test} " in r.stderr
        fails = sorted({line.split()[1] for line in r.stderr.splitlines() if line.startswith(("FAIL: ", "ERROR: "))})
        return name, test, "killed" if killed else "survived", fails, round(time.time() - t0, 1)

    with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
        rows = list(pool.map(run, names))
    json.dump([dict(zip(("name", "test", "outcome", "failing_tests", "seconds"), r)) for r in rows],
              open(out, "w"), indent=1)
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
