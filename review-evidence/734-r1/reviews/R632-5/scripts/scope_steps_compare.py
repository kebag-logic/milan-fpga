"""Compare every workflow scope/decision step and classifier between two commits.

Usage: python3 -I scope_steps_compare.py <repo> <before> <after>
Prints one row per compared artifact and exits 1 if any differs.
"""
import hashlib
import subprocess
import sys

import yaml

STEPS = (
    (".github/workflows/rtl-fast.yml", "changes"),
    (".github/workflows/elaborate.yml", "elaborate"),
    (".github/workflows/rtl.yml", "full-ci-gate"),
)


def show(repo: str, rev: str, path: str) -> str:
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], check=True,
                          capture_output=True, text=True).stdout


def digest(obj: object) -> str:
    return hashlib.sha256(yaml.safe_dump(obj, sort_keys=True).encode()).hexdigest()[:16]


def main() -> int:
    repo, before, after = sys.argv[1:4]
    differ = 0
    for path, job in STEPS:
        jobs = [yaml.safe_load(show(repo, rev, path))["jobs"] for rev in (before, after)]
        b, a = (j[job] for j in jobs)
        # The checkout and every step that reads or publishes the scope answer, plus the job guard.
        for key in ("if", "needs", "outputs", "steps"):
            same = b.get(key) == a.get(key)
            differ |= not same
            print(f"{path}\t{job}.{key}\t{'same' if same else 'DIFFERS'}\t{digest(b.get(key))}\t{digest(a.get(key))}")
    for path in ("scripts/ci_scope.py", "scripts/ci_scope_history.py"):
        texts = [show(repo, rev, path) for rev in (before, after)]
        # ci_scope.py: the classifier body is everything above the self-test case table.
        cut = [t.split("def _cases()")[0] for t in texts]
        same = cut[0] == cut[1]
        differ |= not same
        print(f"{path}\tbefore-_cases()\t{'same' if same else 'DIFFERS'}\t"
              f"{hashlib.sha256(cut[0].encode()).hexdigest()[:16]}\t{hashlib.sha256(cut[1].encode()).hexdigest()[:16]}")
    return 1 if differ else 0


if __name__ == "__main__":
    raise SystemExit(main())
