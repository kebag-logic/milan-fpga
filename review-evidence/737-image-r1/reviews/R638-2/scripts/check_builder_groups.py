#!/usr/bin/env python3
"""Reviewer check of the grouped builder evidence (manager ruling b).

Usage: check_builder_groups.py <checkout> <evidence-commit> <evidence-dir-in-commit>
Reads builder-functions-N.json from the public evidence commit via git, and the
function list from sw/builder/test_builder.py's __main__ loop at the checkout HEAD.
"""
import ast, collections, hashlib, json, subprocess, sys
from pathlib import Path

checkout, commit, base = Path(sys.argv[1]), sys.argv[2], sys.argv[3]


def show(name):
    return subprocess.check_output(["git", "-C", str(checkout), "show", f"{commit}:{base}/{name}"])


source = subprocess.check_output(["git", "-C", str(checkout), "show", "HEAD:sw/builder/test_builder.py"])
head_hash = hashlib.sha256(source).hexdigest()
tree = ast.parse(source)
main = next(n for n in tree.body if isinstance(n, ast.If) and ast.unparse(n.test) == "__name__ == '__main__'")
loop = next(n for n in main.body if isinstance(n, ast.For) and ast.unparse(n.target) == "fn")
names = [n.id for n in loop.iter.elts]
listing = subprocess.check_output(["git", "-C", str(checkout), "ls-tree", "--name-only", commit, base + "/"],
                                  text=True).split()
files = sorted(p.rsplit("/", 1)[1] for p in listing if p.rsplit("/", 1)[1].startswith("builder-functions-"))
reports = {f: json.loads(show(f)) for f in files}
out = {"head_source_sha256": head_hash, "head_functions": len(names), "unique": len(set(names)) == len(names),
       "files": {}}
ran = collections.Counter()
for f, r in reports.items():
    out["files"][f] = {"source_sha256": r.get("source_sha256"), "group": r.get("group"),
                       "require_rv32": r.get("require_rv32"), "results": [x["name"] for x in r.get("results", [])],
                       "groups_equal_head_partition": None}
    for x in r.get("results", []):
        ran[x["name"]] += 1
    groups = r.get("groups")
    flat = [n for g in groups for n in g] if groups else []
    out["files"][f]["groups_equal_head_partition"] = flat == names
    out["files"][f]["assigned_equals_ran"] = groups[r["group"]] == out["files"][f]["results"] if groups else None
out["all_source_equal_head"] = all(v["source_sha256"] == head_hash for v in out["files"].values())
out["all_require_rv32"] = all(v["require_rv32"] is True for v in out["files"].values())
out["groups_seen"] = sorted(v["group"] for v in out["files"].values())
out["missing"] = [n for n in names if ran[n] == 0]
out["duplicated"] = [n for n in names if ran[n] > 1]
out["extra"] = [n for n in ran if n not in names]
out["covered_exactly_once"] = not out["missing"] and not out["duplicated"] and not out["extra"]
print(json.dumps(out, indent=1))
