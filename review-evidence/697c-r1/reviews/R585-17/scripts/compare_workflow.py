#!/usr/bin/env python3
"""compare_workflow.py REPO: compare rtl-fast.yml jobs at the head with the branch parent and dev parent."""
import subprocess, sys, yaml, json
repo = sys.argv[1]
HEAD, BR, DEV = "27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c", "5b4ea55160c5ee34263e24140f960c4f03d923bc", "dc4d06cbfec209cc2ff76806f4b49c51f46639ae"
def load(rev, path=".github/workflows/rtl-fast.yml"):
    return yaml.safe_load(subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout)
h, b, d = load(HEAD), load(BR), load(DEV)
TSN = " third_party/tsn-c-stack"
def strip_tsn(job):
    j = json.loads(json.dumps(job))
    for s in j.get("steps", []):
        if s.get("name") == "Fetch RTL dependencies":
            s["run"] = s["run"].replace(TSN, "")
    return j
ok = True
top = {k: v for k, v in h.items() if k != "jobs"}
print("top-level keys equal branch:", top == {k: v for k, v in b.items() if k != "jobs"}, "dev:", top == {k: v for k, v in d.items() if k != "jobs"})
for name in sorted(set(h["jobs"]) | set(b["jobs"]) | set(d["jobs"])):
    hj, bj, dj = h["jobs"].get(name), b["jobs"].get(name), d["jobs"].get(name)
    if name == "rtl-fast":
        continue
    eqb, eqd = hj == bj, hj == dj
    note = ""
    if hj is None:
        note = "MISSING AT HEAD"; ok = False
    elif not (eqb or eqd):
        # dev's split jobs: equal to dev once the tsn-c-stack fetch is removed?
        if dj is not None and strip_tsn(hj) == dj:
            note = "= dev + tsn-c-stack fetch"
        else:
            note = "DIFFERS FROM BOTH"; ok = False
    print(f"{name:26s} head==branch {str(eqb):5s} head==dev {str(eqd):5s} {note}")
agg = h["jobs"]["rtl-fast"]
need = set(agg["needs"])
want = (set(b["jobs"]) | set(d["jobs"])) - {"rtl-fast"}
print("aggregate needs == every other job (union of parents):", need == want, sorted(want - need), sorted(need - want))
ok &= need == want
env = agg["steps"][0]["env"]; run = agg["steps"][0]["run"]
for j in sorted(want):
    key = j.upper().replace("-", "_") + "_RESULT"
    has_env = env.get(key) == "${{ needs.%s.result }}" % j
    has_loop = f'"{j}:${key}"' in run
    ok &= has_env and has_loop and run.count(f'"{j}:') == 1
    print(f"  aggregate {j:26s} env {has_env} loop {has_loop} count {run.count(chr(34)+j+':')}")
for k in ("name", "if", "runs-on", "timeout-minutes"):
    ok &= agg.get(k) == b["jobs"]["rtl-fast"].get(k) == d["jobs"]["rtl-fast"].get(k)
# each check step exactly once across the firmware jobs
from collections import Counter
runs = Counter(s.get("run", "").strip() for n, j in h["jobs"].items() if n.startswith("firmware") for s in j["steps"]
               if s.get("name", "").startswith(("Run ", "Hold ", "Prove ")))
dup = {r: c for r, c in runs.items() if c != 1}
print("firmware check steps:", len(runs), "duplicates:", dup)
ok &= not dup
print("RESULT:", "OK" if ok else "FINDING")
