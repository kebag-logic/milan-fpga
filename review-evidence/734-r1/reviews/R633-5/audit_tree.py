#!/usr/bin/env python3
"""Read-only exact-tree, index, file-mode, and merge-preservation audit."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

HEAD = "7c862ad980dfe829ef4d85ff8f4fb4fab451984f"
TREE = "622e79ae2a21917a49426c675d417307104112a1"
PREVIOUS = "59354ffe75697e17a16fd117d9ba853e104394bc"
DEV = "0136de16291a127e0a34627c77ac09cd41efc08b"
BASE = "a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1", GIT_OPTIONAL_LOCKS="0")

    def git(*words):
        return subprocess.check_output(["git", "-c", "core.fsmonitor=false", "-C", str(root), *words], env=env)

    def entries(rev):
        result = {}
        for record in git("ls-tree", "-rz", rev).split(b"\0"):
            if record:
                meta, name = record.split(b"\t", 1)
                mode, kind, oid = meta.decode().split()
                result[name.decode()] = [mode, kind, oid]
        return result

    assert git("rev-parse", "HEAD").decode().strip() == HEAD
    assert git("rev-parse", "HEAD^{tree}").decode().strip() == TREE
    assert git("show", "-s", "--format=%P", HEAD).decode().strip() == f"{PREVIOUS} {DEV}"
    expected, previous, dev = entries(HEAD), entries(PREVIOUS), entries(DEV)
    failures, links = [], []
    for path, (mode, kind, oid) in expected.items():
        target = root / path
        if mode == "160000":
            checked = None
            if (target / ".git").exists():
                checked = subprocess.check_output(["git", "-C", str(target), "rev-parse", "HEAD"], env=env).decode().strip()
                if checked != oid:
                    failures.append(f"off-pin checkout: {path}")
            links.append({"path": path, "pin": oid, "checkout": checked})
            continue
        if not target.exists() and not target.is_symlink():
            failures.append(f"missing: {path}")
            continue
        info = target.lstat()
        actual_mode = "120000" if stat.S_ISLNK(info.st_mode) else "100755" if info.st_mode & 0o111 else "100644"
        data = os.readlink(target).encode() if actual_mode == "120000" else target.read_bytes()
        actual_oid = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if mode != actual_mode or oid != actual_oid:
            failures.append(f"blob/mode mismatch: {path}")
    index = {}
    for record in git("ls-files", "--stage", "-z").split(b"\0"):
        if record:
            meta, name = record.split(b"\t", 1)
            mode, oid, stage = meta.decode().split()
            assert stage == "0", (name, stage)
            index[name.decode()] = [mode, "commit" if mode == "160000" else "blob", oid]
    if index != expected:
        failures.append("index differs from HEAD tree")
    distinct = sorted(p for p in set(expected) | set(dev) if expected.get(p) != dev.get(p))
    allowed = {".github/workflows/docs.yml", ".github/workflows/elaborate.yml", ".github/workflows/rtl-fast.yml", ".github/workflows/rtl.yml", "docs/testing/CI_WORKFLOWS.md", "docs/testing/TESTING.md", "scripts/act_ci.py", "scripts/ci_events.py", "scripts/ci_scope.py", "scripts/ci_scope_history.py"}
    assert set(distinct) == allowed
    assert expected["scripts/ci_scope_history.py"] == previous["scripts/ci_scope_history.py"]
    source = ast.parse((root / "scripts/act_ci.py").read_text())
    manifest = next(ast.literal_eval(n.value) for n in source.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "TRUSTED_SUBMODULES" for t in n.targets))
    assert len(manifest) == 6
    assert ("third_party/tsn-c-stack", "third_party/tsn-c-stack", "https://github.com/kebag-logic/tsn-c-stack.git") in manifest
    remerge = git("show", "--format=", "--remerge-diff", HEAD).decode()
    conflicts = [line for line in remerge.splitlines() if line.startswith("remerge CONFLICT")]
    assert conflicts == ["remerge CONFLICT (content): Merge conflict in scripts/ci_events.py"]
    payload = {"head": HEAD, "tree": TREE, "parents": [PREVIOUS, DEV], "tracked_entries": len(expected), "index_equals_tree": index == expected, "tracked_blob_and_mode_failures": failures, "gitlinks": links, "different_from_dev": distinct, "all_other_entries_equal_dev": True, "scope_history_identical_to_previous": True, "trusted_manifest_entries": manifest, "conflicts": conflicts, "status": git("status", "--porcelain=v2").decode()}
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    for name, words in {"merge-resolution.diff": ("show", "--format=", "--remerge-diff", HEAD), "scope-lane.diff": ("diff", DEV, HEAD), "merge-delta.diff": ("diff", PREVIOUS, HEAD), "original-base.diff": ("diff", BASE, HEAD), "lane-history.txt": ("log", "--first-parent", "--format=%H %P %s", f"{BASE}..{HEAD}")}.items():
        (args.output.parent / name).write_bytes(git(*words))
    print(json.dumps(payload, indent=2))
    assert not failures
    assert payload["status"] == ""


if __name__ == "__main__":
    main()
