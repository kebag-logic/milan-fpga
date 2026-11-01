#!/usr/bin/env python3
"""Print every line a finding cites, at the head, and compare citations untouched by the round against the old tree.
Usage: citations.py REPO OLD_DATA_REV OLD_TREE_REV NEW_REV. Reads git objects only; submodule paths read through the pinned gitlink."""
import json, re, subprocess, sys
repo, old_data, old_tree, new = sys.argv[1:5]
def sh(*a, cwd=repo):
    return subprocess.run(a, cwd=cwd, capture_output=True, text=True, errors="replace")
def gitlink(rev, sub):
    return sh("git", "ls-tree", rev, sub).stdout.split()[2]
def blob(rev, path):
    for sub in ("protocol-processor", "gptp-processor"):
        if path.startswith(sub + "/"):
            r = sh("git", "show", f"{gitlink(rev, sub)}:{path[len(sub)+1:]}", cwd=f"{repo}/{sub}")
            return r.stdout.split("\n") if r.returncode == 0 else None
    r = sh("git", "show", f"{rev}:{path}")
    return r.stdout.split("\n") if r.returncode == 0 else None
CITE = re.compile(r"`([\w./-]+\.[\w]+)`[^`;]*?\blines? ((?:\d+(?:-\d+)?(?:, | and )?)+)")
LOOSE = re.compile(r"\b(top )?lines? ((?:\d+(?:-\d+)?(?:, | and )?)+)")
def cites(text):
    return [(m.group(1), r) for m in CITE.finditer(text) for r in re.findall(r"\d+(?:-\d+)?", m.group(2))]
def data(rev):
    return {f["id"]: f for f in json.loads(sh("git", "show", f"{rev}:scripts/docs_inventory.json").stdout)["findings"]}
A, B = data(old_data), data(new)
mode = sys.argv[5] if len(sys.argv) > 5 else "print"
for i, f in sorted(B.items()):
    for key in ("source", "correction"):
        for path, r in cites(f.get(key, "")):
            lo, hi = (int(x) for x in (r.split("-") + [r])[:2])
            now = blob(new, path)
            if now is None:
                print(f"{i} {key} {path}:{r} MISSING AT HEAD"); continue
            if mode == "print":
                print(f"{i} {key} {path}:{r}")
                for n in range(lo, min(hi, lo + 3) + 1):
                    print(f"    {n}: {now[n-1][:150] if n <= len(now) else '<past EOF>'}")
            else:
                was = A.get(i, {}).get(key, "")
                if (path, r) in cites(was):
                    old = blob(old_tree, path)
                    if old is None:
                        print(f"{i} {key} {path}:{r} not at old tree"); continue
                    same = old[lo-1:hi] == now[lo-1:hi]
                    print(("SAME " if same else "MOVED"), i, key, f"{path}:{r}")
