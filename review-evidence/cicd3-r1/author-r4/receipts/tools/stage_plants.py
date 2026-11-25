#!/usr/bin/env python3
"""Each planted defect removes one protection from scripts/mutant_stage.py; its --selftest must fail.

usage: python3 -I stage_plants.py TREE SCRATCH
Prints, per plant: the substitution, the self-test's exit status, the last control that passed and the
failing assertion's first line. A plant whose anchor is not found once is reported as BAD-ANCHOR.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

PLANTS = {
    "lock in a TMPDIR- and uid-named lock directory, not on the slot itself (the round-3 domain)": (
        '            fd = _hold(path)\n',
        '            import fcntl as _f, hashlib as _h\n'
        '            _locks = Path(tempfile.gettempdir()) / f"milan-mutant-stage-{os.getuid()}" / "locks"\n'
        '            _locks.mkdir(parents=True, exist_ok=True)\n'
        '            fd = os.open(_locks / (_h.sha256(str(path).encode()).hexdigest()[:24] + ".lock"), os.O_RDWR | os.O_CREAT)\n'
        '            try:\n'
        '                _f.flock(fd, _f.LOCK_EX | _f.LOCK_NB)\n'
        '            except BlockingIOError:\n'
        '                os.close(fd); fd = None\n'
        '            if fd is not None:\n'
        '                shutil.rmtree(path, ignore_errors=True); path.mkdir(parents=True)\n'),
    "TMPDIR not resolved": (
        "    return Path(tempfile.gettempdir()).resolve()\n",
        "    return Path(tempfile.gettempdir())\n"),
    "a slot owned by another user is taken": (
        "        if info.st_uid != _uid():\n            return None  # another user's slot",
        "        if False:\n            return None  # another user's slot"),
    "a symbolic-link root is accepted": (
        "    if stat.S_ISLNK(info.st_mode):\n        return None, f\"{root} is a symbolic link\"\n",
        ""),
    "a root others may write is accepted": (
        "    if info.st_mode & 0o022:\n        return None, f\"{root} may be written by others",
        "    if False:\n        return None, f\"{root} may be written by others"),
    "a root owned by another user is accepted": (
        "    if info.st_uid != _uid():\n        return None, f\"{root} is owned by uid {info.st_uid}\"\n",
        ""),
    "a non-sticky TMPDIR others may write is accepted": (
        "    if info.st_mode & 0o022 and not info.st_mode & stat.S_ISVTX:",
        "    if False:"),
    "a non-directory root is accepted": (
        "    if not stat.S_ISDIR(info.st_mode):\n        return None, f\"{root} is not a directory\"\n",
        ""),
    "emptying a taken slot follows a link": (
        "            if entry.is_dir(follow_symlinks=False):\n                shutil.rmtree(entry.path)",
        "            if entry.is_dir(follow_symlinks=True):\n                for sub in Path(entry.path).iterdir():\n                    sub.unlink() if sub.is_file() else None\n                shutil.rmtree(entry.path, ignore_errors=True)"),
    "an earlier readable root is not made private": (
        "            os.fchmod(fd, 0o700)  # an earlier, readable root",
        "            pass  # an earlier, readable root"),
}


def main() -> int:
    tree, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    source = (tree / "scripts/mutant_stage.py").read_text()
    bad = 0
    for n, (name, (old, new)) in enumerate(PLANTS.items()):
        if source.count(old) != 1:
            print(f"BAD-ANCHOR {name}")
            bad += 1
            continue
        work = scratch / f"plant-{n}"
        shutil.rmtree(work, ignore_errors=True)
        (work / "scripts").mkdir(parents=True)
        (work / "scripts/mutant_stage.py").write_text(source.replace(old, new))
        run = subprocess.run([sys.executable, "-I", str(work / "scripts/mutant_stage.py"), "--selftest"],
                             capture_output=True, text=True, timeout=300)
        passed = [line for line in run.stdout.splitlines() if line.startswith("mutant stage control:")]
        err = [line for line in run.stderr.splitlines() if line.strip()]
        caught = run.returncode != 0
        bad += not caught
        print(f"{'CAUGHT' if caught else 'MISSED'} rc={run.returncode} plant: {name}\n"
              f"    last control passed: {passed[-1][len('mutant stage control: '):] if passed else '(none)'}\n"
              f"    failure: {err[-1][:220] if err else '(none)'}")
        shutil.rmtree(work)
    print(f"{len(PLANTS) - bad}/{len(PLANTS)} plants caught")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
