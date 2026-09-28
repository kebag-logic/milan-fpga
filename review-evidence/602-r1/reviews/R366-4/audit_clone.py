#!/usr/bin/env python3
"""Verify the review clone is byte-identical to the reviewed head after probes.

Usage: audit_clone.py CLONE
Checks: HEAD and tree; index entries equal the head tree (mode, object, path);
every tracked regular file / symlink hashes to its recorded blob with its mode;
every gitlink's checkout is at the recorded commit and has no local changes;
no untracked or ignored file exists in the superproject or the three
initialised submodules. Exit 0 only when all hold.
"""
import os
import stat
import subprocess
import sys
from pathlib import Path

HEAD = "6c5ca18f12191a252447ec7c7c75363b851f2771"
TREE = "90653220be7a737e3239a56f5621554081c9a8c1"
LINKS = {"protocol-processor": "16be6768f710e79450aace277abacd6c2c3336e5",
         "gptp-processor": "5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d",
         "third_party/verilog-axis": "48ff7a7e2ef782cf778d47910cf85835c64b1bce"}


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True,
                          check=True).stdout


def main() -> int:
    clone = Path(sys.argv[1]).resolve()
    bad = []
    if git(clone, "rev-parse", "HEAD").strip() != HEAD:
        bad.append("HEAD moved")
    if git(clone, "rev-parse", "HEAD^{tree}").strip() != TREE:
        bad.append("tree differs")
    if git(clone, "write-tree").strip() != TREE:
        bad.append("index does not write the head tree")
    entries = git(clone, "ls-tree", "-r", "-z", "--full-tree", HEAD).split("\0")
    counted = {"blob": 0, "commit": 0}
    for line in filter(None, entries):
        meta, path = line.split("\t", 1)
        mode, kind, obj = meta.split()
        full = clone / path
        if kind == "commit":
            counted["commit"] += 1
            if path in LINKS:
                if obj != LINKS[path]:
                    bad.append(f"gitlink pin {path} {obj}")
                if git(full, "rev-parse", "HEAD").strip() != obj:
                    bad.append(f"submodule checkout {path} off pin")
                if git(full, "status", "--porcelain", "--ignored", "--untracked-files=all").strip():
                    bad.append(f"submodule {path} not clean")
            continue
        counted["blob"] += 1
        st = os.lstat(full)
        if mode == "120000":
            ok = stat.S_ISLNK(st.st_mode) and git(clone, "hash-object", "--stdin") is not None
            data = os.readlink(full).encode()
        else:
            want_exec = mode == "100755"
            ok = stat.S_ISREG(st.st_mode) and bool(st.st_mode & 0o111) == want_exec
            data = full.read_bytes()
        got = subprocess.run(["git", "-C", str(clone), "hash-object", "--stdin"], input=data,
                             capture_output=True, check=True).stdout.decode().strip()
        if not ok or got != obj:
            bad.append(f"blob/mode mismatch {path}")
    if git(clone, "status", "--porcelain", "--ignored", "--untracked-files=all").strip():
        bad.append("superproject has untracked, ignored or modified files")
    print(f"blobs checked {counted['blob']}, gitlinks {counted['commit']}")
    for item in bad:
        print(f"[FAIL] {item}")
    print("AUDIT: " + ("CLEAN" if not bad else f"{len(bad)} problem(s)"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
