"""Usage: python3 -I compare_workflow_jobs.py <repo> <old> <new> <workflow path>...
Reports, per job, whether its definition changed between two commits, ignoring runs-on."""
import json, subprocess, sys
import yaml
repo, old, new, *paths = sys.argv[1:]
def load(rev, p):
    return yaml.safe_load(subprocess.run(["git", "-C", repo, "show", f"{rev}:{p}"], check=True, capture_output=True, text=True).stdout)
for p in paths:
    a, b = load(old, p)["jobs"], load(new, p)["jobs"]
    for j in sorted(set(a) | set(b)):
        ja, jb = a.get(j), b.get(j)
        if ja is None or jb is None:
            print(p, j, "ADDED" if ja is None else "REMOVED"); continue
        ra, rb = ja.get("runs-on"), jb.get("runs-on")
        ja = {k: v for k, v in ja.items() if k != "runs-on"}; jb = {k: v for k, v in jb.items() if k != "runs-on"}
        print(p, j, "runs-on:%s->%s" % (ra, rb), "BODY-SAME" if json.dumps(ja, sort_keys=True) == json.dumps(jb, sort_keys=True) else "BODY-CHANGED")
