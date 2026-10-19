#!/usr/bin/env python3
"""Which files changed by BASE..HEAD are CI image inputs (inventory rows, recipe
files, or named in any ci/image/*.json)? Prints committed vs head digests for
every stale inventory row. Usage: ci_input_scope.py <repo> <base> <head>"""
import hashlib, json, subprocess, sys
from pathlib import Path
repo, base, head = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
def git(*a): return subprocess.run(["git", "-C", str(repo), *a], check=True, capture_output=True, text=True).stdout
changed = git("diff", "--name-only", f"{base}..{head}").split()
print("changed:", changed)
inv = json.loads(git("show", f"{head}:ci/image/tool-inventory.json"))["inputs"]
for path in changed:
    print(f"{path}: inventory_input={path in inv}")
# recipe file list is literal in ci/image/build.py recipe_inputs()
src = git("show", f"{head}:ci/image/build.py")
recipe = src[src.index("def recipe_inputs"):src.index("def layer_sources")]
for path in changed:
    print(f"{path}: named_in_recipe_inputs={Path(path).name in recipe}")
for js in git("ls-tree", "--name-only", head, "ci/image/").split():
    if js.endswith(".json"):
        body = git("show", f"{head}:{js}")
        hits = [p for p in changed if p in body]
        print(f"{js}: names_changed_files={hits}")
print("stale inventory rows at head (path committed head):")
stale = 0
for path, digest in sorted(inv.items()):
    blob = subprocess.run(["git", "-C", str(repo), "show", f"{head}:{path}"], capture_output=True)
    if blob.returncode:
        continue  # submodule content, not in this tree object
    now = hashlib.sha256(blob.stdout).hexdigest()
    if now != digest:
        stale += 1
        print(f"  {path} {digest} {now}")
print("stale_count", stale)
