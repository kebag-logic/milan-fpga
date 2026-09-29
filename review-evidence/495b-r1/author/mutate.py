#!/usr/bin/env python3
"""Apply each mutant in place, run its check, restore the bytes and verify them.

Usage: mutate.py <repo> <spec.json> [name ...]

spec: {"check": [argv...], "cwd": "<repo-relative>", "timeout": s, "env": {..},
       "mutants": [{"name": .., "expect": "pass"|"killed", "check": [..]?, "env": {..}?,
                    "edits": [{"path": .., "old": .., "new": .., "count": 1?}
                              | {"path": .., "base": "<rev>"}]}]}
A mutant is KILLED when its check exits non-zero. Every touched file is restored
from the bytes read before the edit, and its sha256 is compared afterwards.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


def sha(data: bytes) -> str:
    """Hex sha256 of bytes."""
    return hashlib.sha256(data).hexdigest()


def run_mutant(repo: Path, spec: dict, mutant: dict) -> tuple[str, int, str]:
    """Apply, check, restore; return (verdict, rc, tail)."""
    saved: dict[Path, bytes] = {}
    try:
        for edit in mutant.get("edits", []):
            path = repo / edit["path"]
            if path not in saved:
                saved[path] = path.read_bytes()
            if "base" in edit:
                data = subprocess.run(["git", "-C", str(repo), "show", f"{edit['base']}:{edit['path']}"],
                                      check=True, capture_output=True).stdout
                path.write_bytes(data)
                continue
            text = path.read_text()
            count = text.count(edit["old"])
            want = edit.get("count", 1)
            if count != want:
                raise SystemExit(f"{mutant['name']}: anchor count {count} != {want} in {edit['path']}: "
                                 f"{edit['old'][:60]!r}")
            path.write_text(text.replace(edit["old"], edit["new"]))
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        env.update(spec.get("env", {}))
        env.update(mutant.get("env", {}))
        check = mutant.get("check", spec["check"])
        result = subprocess.run(check, cwd=repo / mutant.get("cwd", spec.get("cwd", ".")), env=env,
                                text=True, capture_output=True, timeout=spec.get("timeout", 900))
    finally:
        for path, data in saved.items():
            path.write_bytes(data)
            if sha(path.read_bytes()) != sha(data):
                raise SystemExit(f"RESTORE FAILED: {path}")
    logdir = os.environ.get("MUTATE_LOGDIR")
    if logdir:
        name = "".join(ch if ch.isalnum() else "_" for ch in mutant["name"])[:60]
        Path(logdir, f"{name}.log").write_text(f"rc={result.returncode}\n{result.stdout}\n--- stderr\n{result.stderr}")
    out = (result.stdout + result.stderr).strip().splitlines()
    tail = [line for line in out if "Error" in line or "assert" in line.lower() or "FAIL" in line
            or "error" in line][-2:] or out[-1:]
    verdict = "PASS" if result.returncode == 0 else "KILLED"
    return verdict, result.returncode, " | ".join(tail)[:400]


def main() -> int:
    """Run every selected mutant and report expectation mismatches."""
    repo = Path(sys.argv[1]).resolve()
    spec = json.loads(Path(sys.argv[2]).read_text())
    names = set(sys.argv[3:])
    before = subprocess.run(["git", "-C", str(repo), "diff", "--binary", "HEAD"], capture_output=True).stdout
    bad = 0
    for mutant in spec["mutants"]:
        if names and mutant["name"] not in names:
            continue
        verdict, rc, tail = run_mutant(repo, spec, mutant)
        expect = mutant.get("expect", "killed").upper()
        ok = (verdict == "PASS") == (expect == "PASS")
        bad += not ok
        print(f"{'ok ' if ok else 'BAD'} {mutant['name']}: {verdict} rc={rc} (expected {expect}) :: {tail}",
              flush=True)
    after = subprocess.run(["git", "-C", str(repo), "diff", "--binary", "HEAD"], capture_output=True).stdout
    if sha(before) != sha(after):
        print("WORKTREE CHANGED BY THE RUN")
        return 2
    print(f"worktree diff sha256 unchanged: {sha(after)}")
    print(f"expectation mismatches: {bad}")
    return int(bad != 0)


if __name__ == "__main__":
    sys.exit(main())
