#!/usr/bin/env python3
"""Compare job and step names of .github/workflows/elaborate.yml between two revisions.
usage: wf_struct.py <repo> <base-rev> <head-rev>"""
import subprocess, sys, yaml
repo, a, b = sys.argv[1:4]
def load(rev): return yaml.safe_load(subprocess.check_output(["git", "-C", repo, "show", f"{rev}:.github/workflows/elaborate.yml"]))
A, B = load(a), load(b)
print("on (base == head):", A.get(True) == B.get(True))
for job in sorted(set(A["jobs"]) | set(B["jobs"])):
    ja, jb = A["jobs"].get(job), B["jobs"].get(job)
    if ja == jb: print(f"{job}: identical"); continue
    na = [s.get("name", s.get("uses")) for s in (ja or {}).get("steps", [])]
    nb = [s.get("name", s.get("uses")) for s in (jb or {}).get("steps", [])]
    print(f"{job}: changed; timeout {ja and ja.get('timeout-minutes')} -> {jb and jb.get('timeout-minutes')}; needs {ja and ja.get('needs')} -> {jb and jb.get('needs')}")
    print("   removed steps:", [n for n in na if n not in nb]); print("   added steps:", [n for n in nb if n not in na])
    if ja and jb:
        same = [n for n in na if n in nb]
        diff = [n for n in same if next(s for s in ja["steps"] if s.get("name", s.get("uses")) == n) != next(s for s in jb["steps"] if s.get("name", s.get("uses")) == n)]
        print("   steps with changed bodies:", diff)
