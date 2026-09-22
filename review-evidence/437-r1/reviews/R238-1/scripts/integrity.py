#!/usr/bin/env python3
"""[R238] review-checkout integrity: blob, mode, kind, index and submodules.

Usage: integrity.py <checkout> <label>

Writes receipts/integrity-<label>.json and prints a summary. Every tracked
path of HEAD's tree is compared with the index record (mode, blob, stage 0,
no assume-unchanged or skip-worktree flag) and with the bytes on disk: a
regular file must hash to its blob with the right executable bit, a symlink
must be a symlink whose target hashes to its blob, and a gitlink must be a
checkout at exactly the pinned commit with a clean worktree (or an empty
uninitialised directory). Untracked and ignored paths are listed as well.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True).stdout


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main() -> int:
    repo, label = Path(sys.argv[1]).resolve(), sys.argv[2]
    head = git(repo, "rev-parse", "HEAD").strip()
    tree = git(repo, "rev-parse", "HEAD^{tree}").strip()
    entries = {}
    for line in git(repo, "ls-tree", "-r", "-z", "HEAD").split("\0"):
        if line:
            meta, path = line.split("\t", 1)
            mode, kind, sha = meta.split()
            entries[path] = (mode, kind, sha)
    index = {}
    for line in git(repo, "ls-files", "-s", "-z").split("\0"):
        if line:
            meta, path = line.split("\t", 1)
            mode, sha, stage = meta.split()
            index.setdefault(path, []).append((mode, sha, stage))
    flags = {}
    for line in git(repo, "ls-files", "-v", "-z").split("\0"):
        if line:
            flags[line[2:]] = line[0]
    problems = []
    if set(index) != set(entries):
        problems.append(f"index paths differ from HEAD tree: "
                        f"{sorted(set(index) ^ set(entries))[:10]}")
    # Filtered hashes, path-aware, for regular files (.gitattributes applies).
    regular = [p for p, (m, _, _) in entries.items() if m in ("100644", "100755")]
    proc =subprocess.run(["git", "-C", str(repo), "hash-object", "--stdin-paths"],
                          input="\n".join(regular) + "\n", capture_output=True,
                          text=True, check=True)
    disk = dict(zip(regular, proc.stdout.split()))
    for path, (mode, kind, sha) in sorted(entries.items()):
        rec = index.get(path, [])
        if rec != [(mode, sha, "0")]:
            problems.append(f"{path}: index record {rec} != tree {(mode, sha)}")
        if flags.get(path) != "H":
            problems.append(f"{path}: ls-files -v flag {flags.get(path)!r}")
        full = repo / path
        if mode in ("100644", "100755"):
            if full.is_symlink() or not full.is_file():
                problems.append(f"{path}: not a regular file on disk")
                continue
            if disk.get(path) != sha:
                problems.append(f"{path}: disk blob {disk.get(path)} != {sha}")
            exe = bool(full.stat().st_mode & 0o111)
            if exe != (mode == "100755"):
                problems.append(f"{path}: executable bit {exe} vs mode {mode}")
        elif mode == "120000":
            if not full.is_symlink() or blob_id(os.readlink(full).encode()) != sha:
                problems.append(f"{path}: symlink mismatch")
        elif mode == "160000":
            if full.is_symlink() or not full.is_dir():
                problems.append(f"{path}: gitlink path is not a directory")
            elif not any(full.iterdir()):
                pass  # uninitialised by design
            else:
                sub = git(full, "rev-parse", "HEAD").strip()
                dirty = git(full, "status", "--porcelain=v1", "--untracked-files=all",
                            "--ignore-submodules=none")
                if sub != sha:
                    problems.append(f"{path}: submodule HEAD {sub} != pin {sha}")
                if dirty.strip():
                    problems.append(f"{path}: submodule worktree dirty")
        else:
            problems.append(f"{path}: unexpected mode {mode}")
    status = git(repo, "status", "--porcelain=v2", "--untracked-files=all",
                 "--ignored=matching", "--ignore-submodules=none")
    extra = [l for l in status.splitlines() if not l.startswith("#")]
    result = {"checkout": str(repo), "label": label, "head": head, "tree": tree,
              "tracked": len(entries),
              "kinds": {m: sum(1 for e in entries.values() if e[0] == m)
                        for m in sorted({e[0] for e in entries.values()})},
              "tree_listing_sha256": hashlib.sha256(
                  json.dumps(sorted(entries.items())).encode()).hexdigest(),
              "status_lines": extra, "problems": problems}
    (OUT / "receipts").mkdir(exist_ok=True)
    (OUT / "receipts" / f"integrity-{label}.json").write_text(json.dumps(result, indent=1))
    print(json.dumps({k: v for k, v in result.items() if k != "problems"}, indent=1))
    print(f"problems: {len(problems)}")
    for p in problems[:20]:
        print("  ", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
