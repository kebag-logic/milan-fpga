"""Probe (scratch, round 12): the pin check from its command line (ctrl_build.py --stack-pin <stack>), run in a
given checkout with one Git variable in the environment it inherits, on a stack clone prepared so that the variable,
reaching Git, makes a stack that is not the gitlink's read as pinned:
- GIT_INDEX_FILE: an index whose gitlink is the stack's previous revision, the clone checked out there;
- GIT_DIR: a repository whose HEAD and index gitlink are a commit holding an edit of src/adp.c, the clone edited so.
Each prints the check's verdict and exit status, and whether that verdict names a stack other than the gitlink's.
usage: python3 -I inherit_probe.py <checkout> <scratch directory>"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
STACK = root / "third_party/tsn-c-stack"
CLEAN = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git(where: Path, *args: str) -> str:
    """A git command for the probe's own setup, in a clean environment."""
    return subprocess.run(["git", "-C", str(where), *args], check=True, capture_output=True, text=True,
                          env=CLEAN).stdout.strip()


def check(stack: Path, extra: dict[str, str]) -> None:
    """The pin check on `stack` with `extra` inherited."""
    res = subprocess.run([sys.executable, "-B", str(root / "sw/firmware/ctrl/test/ctrl_build.py"), "--stack-pin",
                          str(stack)], capture_output=True, text=True, env={**CLEAN, **extra})
    said = (res.stdout + res.stderr).strip().splitlines()
    verdict = said[-1] if said else "no output"
    escaped = res.returncode == 0 and pin not in verdict
    print(f"  {', '.join(extra)}: exit {res.returncode}: {verdict}  =>  {'ESCAPE' if escaped else 'held'}")


shutil.rmtree(work, ignore_errors=True)
work.mkdir(parents=True)
pin = git(root, "ls-files", "--stage", "--", "third_party/tsn-c-stack").split()[1]
print(f"checkout {git(root, 'rev-parse', 'HEAD')}, gitlink {pin}")

previous = work / "previous"
git(work, "clone", "--quiet", "--no-hardlinks", str(STACK), str(previous))
git(previous, "-c", "advice.detachedHead=false", "checkout", "--quiet", f"{pin}~1")
git(work, "init", "--quiet", "index")
git(work / "index", "update-index", "--add", "--cacheinfo", f"160000,{git(previous, 'rev-parse', 'HEAD')},"
    "third_party/tsn-c-stack")
check(previous, {"GIT_INDEX_FILE": str(work / "index/.git/index")})

edited = work / "edited"
git(work, "clone", "--quiet", "--no-hardlinks", str(STACK), str(edited))
git(edited, "-c", "advice.detachedHead=false", "checkout", "--quiet", pin)
other = work / "other"
git(work, "clone", "--quiet", "--no-hardlinks", str(edited), str(other))
for tree in (edited, other):
    (tree / "src/adp.c").write_bytes((tree / "src/adp.c").read_bytes() + b"\n")
git(other, "-c", "user.name=probe", "-c", "user.email=probe@invalid", "commit", "--quiet", "--all", "-m", "edited")
git(other, "update-index", "--add", "--cacheinfo", f"160000,{git(other, 'rev-parse', 'HEAD')},third_party/tsn-c-stack")
check(edited, {"GIT_DIR": str(other / ".git")})
