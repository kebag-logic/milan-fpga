#!/usr/bin/env python3
"""Record both-parent retention and test-name inventories without editing sources."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

env = {**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"}
def git(*args):
    return subprocess.check_output(["git", *args], env=env)

head = "a6e6916826448f81de2b779ca61a87a9f8c47278"
f4 = "f74b9403b330ce316eeec6f724846f16def98443"
dev = "d8b355fe0f41d49dca6cae1cd8b3826e2edde364"
assert git("show", "-s", "--format=%P", head).decode().split() == [f4, dev]
def tree(rev):
    result = {}
    for rec in git("ls-tree", "-rz", rev).split(b"\0"):
        if rec:
            meta, name = rec.split(b"\t", 1)
            result[name.decode()] = meta.decode()
    return result

trees = {rev: tree(rev) for rev in (head, f4, dev)}
base = git("merge-base", f4, dev).decode().strip()
base_tree = tree(base)
retention = {}
for parent in (f4, dev):
    changed = {name for name in set(base_tree) | set(trees[parent])
               if base_tree.get(name) != trees[parent].get(name)}
    retained = sorted(name for name in changed if trees[parent].get(name) == trees[head].get(name))
    reconciled = sorted(changed - set(retained))
    retention[parent] = {"changed_from_merge_base": len(changed),
                         "exact_parent_entries_retained": retained,
                         "resolution_entries_to_examine": reconciled}
protected = ("hdl/", "sw/mailbox/", "docs/reference/MAILBOX_CONTRACT.md",
             "docs/reference/REGISTER_MAP.md", "protocol-processor", "gptp-processor")
changes = git("diff", "--name-only", dev, head).decode().splitlines()
assert not any(name.startswith(protected) for name in changes)
assert trees[head]["sw/firmware/ctrl/srp/srp_mbx.c"] == trees[f4]["sw/firmware/ctrl/srp/srp_mbx.c"]
pattern = re.compile(rb"\bTEST(?:_F|_P)?\s*\(\s*([\w]+)\s*,\s*([\w]+)\s*\)")
inventories = {}
for parent in (f4, dev):
    total = 0
    for name in trees[parent]:
        if not name.startswith("sw/firmware/ctrl/test/") or not name.endswith((".c", ".cpp", ".h", ".hpp")):
            continue
        before = set(pattern.findall(git("show", parent + ":" + name)))
        if not before:
            continue
        after = set(pattern.findall(git("show", head + ":" + name)))
        assert before <= after, (parent, name, before - after)
        total += len(before)
    inventories[parent] = total
diff_hashes = {parent: hashlib.sha256(git("diff", "--no-ext-diff", "--no-textconv", parent, head)).hexdigest()
               for parent in (f4, dev)}
print(json.dumps({"head": head, "merge_base": base, "retention": retention,
                  "all_named_tests_retained_from_each_parent": inventories,
                  "protected_paths_equal_dev": True, "srp_adapter_equal_f4": True,
                  "raw_diff_sha256": diff_hashes}, indent=2))
