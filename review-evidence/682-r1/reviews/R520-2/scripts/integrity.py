#!/usr/bin/env python3
"""Usage: integrity.py <repo> <expected-head> <round2-head>

Verify the review clone is at exact head bytes after probes: worktree blob
bytes and modes equal the index, the index equals HEAD's tree, no untracked
or ignored files remain, the round-3 delta is only the two Markdown files,
gitlinks are unchanged from the round-2 head, and each initialized submodule
sits clean at its gitlink."""
import os, stat, subprocess, sys, json
repo, head, prev = sys.argv[1:4]
def git(*a, cwd=repo):
    return subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True, check=True).stdout
out = {}
out["head"] = git("rev-parse", "HEAD").strip()
out["tree"] = git("rev-parse", "HEAD^{tree}").strip()
idx = {}
for line in git("ls-files", "-s", "-z").split("\0"):
    if line:
        meta, path = line.split("\t", 1); mode, sha, st = meta.split()
        idx[path] = (mode, sha, st)
tree = {}
for line in git("ls-tree", "-r", "-z", "HEAD").split("\0"):
    if line:
        meta, path = line.split("\t", 1); mode, typ, sha = meta.split()
        tree[path] = (mode, sha)
out["index_equals_head_tree"] = {p: (m, s) for p, (m, s, _) in idx.items()} == tree
out["index_stages_all_zero"] = all(v[2] == "0" for v in idx.values())
blobs = [p for p, (m, _) in tree.items() if m != "160000"]
hashed = subprocess.run(["git", "hash-object", "--stdin-paths", "--no-filters"], cwd=repo, input="\n".join(blobs) + "\n",
                        capture_output=True, text=True, check=True).stdout.split()
bad = []
for p, h in zip(blobs, hashed):
    m, s = tree[p]
    fp = os.path.join(repo, p)
    lst = os.lstat(fp)
    if m == "120000":
        ok = stat.S_ISLNK(lst.st_mode) and subprocess.run(["git", "hash-object", "--stdin"], cwd=repo,
             input=os.readlink(fp), capture_output=True, text=True).stdout.strip() == s
    else:
        want_x = m == "100755"
        ok = stat.S_ISREG(lst.st_mode) and h == s and bool(lst.st_mode & 0o100) == want_x
    if not ok:
        bad.append(p)
out["tracked_blobs_checked"] = len(blobs)
out["tracked_blob_mismatches"] = bad
out["status_porcelain_including_ignored"] = git("status", "--porcelain=v1", "--ignored", "--untracked-files=all").splitlines()
out["round3_delta_name_status"] = git("diff", "--name-status", prev, head).splitlines()
gl = lambda rev: sorted(l for l in git("ls-tree", "-r", rev).splitlines() if l.startswith("160000"))
out["gitlinks_head"] = gl(head)
out["gitlinks_unchanged_from_round2"] = gl(head) == gl(prev)
subs = {}
for l in gl(head):
    sha, path = l.split()[2], l.split("\t")[1]
    p = os.path.join(repo, path)
    if os.path.exists(os.path.join(p, ".git")):
        subs[path] = {"gitlink": sha, "checked_out": git("rev-parse", "HEAD", cwd=p).strip(),
                      "clean": git("status", "--porcelain", "--untracked-files=all", cwd=p) == ""}
    else:
        subs[path] = {"gitlink": sha, "initialized": False}
out["submodules"] = subs
ok = (out["head"] == head and out["index_equals_head_tree"] and out["index_stages_all_zero"] and not bad
      and not out["status_porcelain_including_ignored"] and out["gitlinks_unchanged_from_round2"]
      and sorted(x.split("\t")[1] for x in out["round3_delta_name_status"]) == ["CHANGELOG.md", "docs/testing/PP_SHADOW_BASELINE_RECIPE.md"]
      and all(v.get("checked_out") == v["gitlink"] and v.get("clean") for k, v in subs.items() if k in ("protocol-processor", "gptp-processor", "third_party/verilog-axis")))
out["verdict"] = "PASS" if ok else "FAIL"
print(json.dumps(out, indent=1))
sys.exit(0 if ok else 1)
