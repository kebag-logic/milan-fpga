#!/usr/bin/env python3
"""Compare scripts/docs_inventory.json verified_pages with the old release-facing rule at the baseline."""
import json, re, subprocess, sys
repo, head = sys.argv[1], sys.argv[2]
base = sys.argv[3] if len(sys.argv) > 3 else "1e80128f"
rule = re.compile(r"README\.md|REQUIREMENTS\.md|docs/README\.md|docs/(guides|integration|reference)/.*")
def tree(rev):
    out = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev], check=True, capture_output=True, text=True).stdout
    return set(out.split("\n")) - {""}
data = json.loads(subprocess.run(["git", "-C", repo, "show", f"{head}:scripts/docs_inventory.json"], check=True, capture_output=True, text=True).stdout)
listed = set(data["verified_pages"])
at_base = tree(base); at_head = tree(head)
md = lambda s: {p for p in s if p.endswith(".md") or p.endswith(".rst") or p.endswith(".txt")}
old_base = {p for p in at_base if rule.fullmatch(p)}
old_head = {p for p in at_head if rule.fullmatch(p)}
print("listed", len(listed), "sorted", data["verified_pages"] == sorted(data["verified_pages"]), "dups", len(data["verified_pages"]) - len(listed))
print("listed missing at baseline:", sorted(listed - at_base))
print("listed missing at head:", sorted(listed - at_head))
print("old rule at baseline (all files):", len(old_base), "md only:", len(md(old_base)))
print("old-rule baseline md pages not listed:", sorted(md(old_base) - listed))
print("old-rule baseline non-md files:", sorted(old_base - md(old_base)))
print("listed but outside old rule:", sorted(listed - old_base))
print("old rule at head md:", len(md(old_head)), "added since baseline:", sorted(md(old_head) - md(old_base)), "removed since baseline:", sorted(md(old_base) - md(old_head)))
