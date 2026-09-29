#!/usr/bin/env python3
"""(2) The merge adds only dev's content outside docs/findings/README.md, and
(4) the candidate tree equals the merge tree. Run from the repository root."""
import subprocess, sys
def g(*a): return subprocess.run(["git", *a], check=True, capture_output=True).stdout.decode()
def raw(a, b):
    rows = {}
    for l in g("diff", "--raw", "--no-renames", "--no-abbrev", a, b).splitlines():
        meta, path = l.split("\t", 1)
        f = meta.split()
        rows[path] = (f[1], f[3], f[4])  # new mode, new blob, status
    return rows
merge_delta = raw("5c579274", "d62b1e1a")
dev_delta = raw("13eda870", "79c36963")
ok = True
m = {k: v for k, v in merge_delta.items() if k != "docs/findings/README.md"}
d = {k: v for k, v in dev_delta.items() if k != "docs/findings/README.md"}
print("merge-introduced paths outside README:", len(m), " dev paths outside README:", len(d))
print("identical path/mode/blob sets:", m == d); ok &= (m == d)
# PR files at merge are byte-identical to the reviewed source head
for p in ("docs/findings/606_FIRST_BIND_MEASUREMENT.md", "docs/findings/608_75_WITHDRAWAL_AND_RESTART.md"):
    a = g("rev-parse", f"5c579274:{p}").strip(); b = g("rev-parse", f"61752396:{p}").strip()
    print(p, a[:12], b[:12], a == b); ok &= a == b
t = [g("rev-parse", f"{r}^{{tree}}").strip() for r in ("d62b1e1a", "61752396")]
print("trees", t, t[0] == t[1] == "b4a1f5ed6a5b00ecde3dcba7781f45fb72480b59"); ok &= t[0] == t[1] == "b4a1f5ed6a5b00ecde3dcba7781f45fb72480b59"
par = g("rev-list", "--parents", "-n1", "61752396").split()
print("candidate parents", par[1:]); ok &= par[1:] == ["79c36963660c10e4c1c11a744fb5bff41a552b8b", "d62b1e1a3a37283ebad039880163873698a011db"]
par = g("rev-list", "--parents", "-n1", "d62b1e1a").split()
print("merge parents", par[1:]); ok &= par[1:] == ["5c57927413e0dae279f06a75d2a58e3fec8a2bb0", "79c36963660c10e4c1c11a744fb5bff41a552b8b"]
# composed tree vs dev: only the PR's three paths differ
cd = raw("79c36963", "61752396")
print("candidate vs dev paths:", sorted(cd)); ok &= sorted(cd) == ["docs/findings/606_FIRST_BIND_MEASUREMENT.md", "docs/findings/608_75_WITHDRAWAL_AND_RESTART.md", "docs/findings/README.md"]
# gitlinks unchanged dev -> candidate
gl = lambda r: sorted(l for l in g("ls-tree", "-r", r).splitlines() if l.startswith("160000"))
print("gitlinks equal dev/candidate:", gl("79c36963") == gl("61752396"), len(gl("61752396"))); ok &= gl("79c36963") == gl("61752396")
print("RESULT", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
