"""Verify every tracked worktree byte/mode and index entry against the assigned commit."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

ROOT = Path(sys.argv[1]).resolve()
PACKET = Path(__file__).resolve().parents[1]
HEAD = "7f56fc4d7f5102cac6dacb9c00f372d20d3b379e"
TREE = "34af6de87215cc90a774757debc8af90073aaa87"

def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])

assert git("rev-parse", "HEAD").decode().strip() == HEAD
assert git("rev-parse", "HEAD^{tree}").decode().strip() == TREE
assert git("write-tree").decode().strip() == TREE
records = []
for raw in git("ls-tree", "-rz", HEAD).split(b"\0"):
    if not raw:
        continue
    meta, name = raw.split(b"\t")
    mode, kind, oid = meta.decode().split()
    rel = os.fsdecode(name)
    path = ROOT / rel
    if mode == "160000":
        subhead = subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "HEAD"]).decode().strip()
        assert subhead == oid, rel
        records.append({"path": rel, "mode": mode, "gitlink": oid, "verified": True})
        continue
    data = os.fsencode(os.readlink(path)) if mode == "120000" else path.read_bytes()
    actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    actual_mode = ("120000" if path.is_symlink() else
                   "100755" if path.stat().st_mode & stat.S_IXUSR else "100644")
    assert actual == oid and actual_mode == mode, rel
    records.append({"path": rel, "mode": mode, "blob": oid, "verified": True})
status = git("status", "--porcelain=v2", "--untracked-files=all").decode()
assert not status, status
result = {"head": HEAD, "tree": TREE, "index_tree": TREE,
          "status": status, "tracked_entries": len(records),
          "source_gitlinks": [r for r in records if r["mode"] == "160000"],
          "records": records}
(PACKET / "receipts/final-integrity.json").write_text(json.dumps(result, indent=2) + "\n")
print(f"PASS: {len(records)} tracked blobs/modes; exact index/tree; clean worktree.")
