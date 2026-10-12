"""Probe (scratch, round 12): two routes within the round-12 threat model that the helper's environment does not
close, each run against the pin check of a given checkout:
1. a forged tree object in the stack's object store: the pinned src/ tree's object replaced, loose, by the bytes of
   a tree holding an edit of src/adp.c, which the clone holds; Git reads subtrees for ls-tree -r without checking
   their hash, so the check reads the edit as pinned (git fsck reports the mismatch);
2. a program the repository's own configuration names: core.fsmonitor set in a scratch checkout's .git/config,
   which Git runs when the decision reads the index (ls-files --stage).
usage: python3 -I model_routes_probe.py <checkout> <scratch checkout, disposable> <scratch directory>"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

root, disposable, work = (Path(a).resolve() for a in sys.argv[1:4])
CLEAN = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_build  # noqa: E402


def git(where: Path, *args: str, stdin: str | None = None) -> str:
    """A git command for the probe's own setup, in a clean environment."""
    return subprocess.run(["git", "-C", str(where), *args], check=True, capture_output=True, text=True, input=stdin,
                          env=CLEAN).stdout.strip()


shutil.rmtree(work, ignore_errors=True)
work.mkdir(parents=True)
pin = ctrl_build.stack_gitlink(root)
print(f"checkout {git(root, 'rev-parse', 'HEAD')}, gitlink {pin}")

clone = work / "forged"
git(work, "clone", "--quiet", "--no-hardlinks", str(ctrl_build.STACK), str(clone))
git(clone, "-c", "advice.detachedHead=false", "checkout", "--quiet", pin)
(work / "packs").mkdir()
for pack in sorted((clone / ".git/objects/pack").glob("pack-*")):
    shutil.move(pack, work / "packs" / pack.name)
for pack in sorted((work / "packs").glob("*.pack")):
    with pack.open("rb") as data:
        subprocess.run(["git", "-C", str(clone), "unpack-objects", "-q"], stdin=data, check=True, env=CLEAN)
src = git(clone, "rev-parse", f"{pin}:src")
(clone / "src/adp.c").write_bytes((clone / "src/adp.c").read_bytes() + b"\n")
blob = git(clone, "hash-object", "-w", "src/adp.c")
listing ="\n".join(ln if not ln.endswith("\tadp.c") else
                    " ".join(ln.split(" ")[:2]) + f" {blob}\tadp.c" for ln in git(clone, "ls-tree", src).splitlines())
forged = git(clone, "mktree", stdin=listing + "\n")
target = clone / f".git/objects/{src[:2]}/{src[2:]}"
target.chmod(0o644)
shutil.copyfile(clone / f".git/objects/{forged[:2]}/{forged[2:]}", target)
try:
    print(f"1. forged src/ tree: stack_pin ACCEPTS {ctrl_build.stack_pin(clone, pin)} with src/adp.c edited")
except ctrl_build.Refusal as exc:
    print(f"1. forged src/ tree: refused: {exc}")
fsck = subprocess.run(["git", "-C", str(clone), "fsck"], capture_output=True, text=True, env=CLEAN)
print(f"   git fsck exit {fsck.returncode}: {[ln for ln in (fsck.stdout + fsck.stderr).splitlines() if 'mismatch' in ln][:2]}")

recorder = work / "recorder"
recorder.write_text('#!/bin/sh\necho "$0 $*" >> "$(dirname "$0")/ran"\nexit 1\n', encoding="utf-8")
recorder.chmod(0o755)
git(disposable, "config", "core.fsmonitor", str(recorder))
try:
    res = subprocess.run([sys.executable, "-B", str(disposable / "sw/firmware/ctrl/test/ctrl_build.py"),
                          "--stack-pin"], capture_output=True, text=True, env=CLEAN)
finally:
    git(disposable, "config", "--unset", "core.fsmonitor")
ran = (work / "ran").read_text(encoding="utf-8").strip().splitlines() if (work / "ran").exists() else []
print(f"2. core.fsmonitor in the checkout's .git/config: the check exits {res.returncode} "
      f"({res.stdout.strip()}); Git ran the program {len(ran)} time(s): {ran[:1]}")
