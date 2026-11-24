#!/usr/bin/env python3
"""Probe scripts/mutant_stage.py's trust in its predictable per-user root.

usage: python3 -I stage_root_probe.py REPO SCRATCH

The root is <TMPDIR>/milan-mutant-stage-<uid>, a name any local account can
predict and create first in a shared, sticky /tmp. Each arm pre-creates the
root in a shape another account could leave there, then asks the helper for
a staging directory and reports what it accepted. Nothing outside SCRATCH is
touched; every arm runs as the calling user, so "foreign" is modelled by the
shape and mode of the root, not by a second account.
"""

import importlib.util
import os
import stat
import sys
import tempfile
from pathlib import Path


def load(repo: Path):
    """The helper module from the tree under review."""
    spec = importlib.util.spec_from_file_location("mutant_stage", repo / "scripts/mutant_stage.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def arm(stage, scratch: Path, label: str, prepare) -> None:
    """Run one arm in its own TMPDIR."""
    tmp = scratch / label
    tmp.mkdir(parents=True)
    os.environ["TMPDIR"] = str(tmp)
    tempfile.tempdir = None
    root = tmp / f"milan-mutant-stage-{os.getuid()}"
    prepare(root, tmp)
    try:
        with stage.directory("probe-") as path:
            real = Path(path).resolve()
            info = os.lstat(root)
            print(f"{label}: ACCEPTED; staged at {real.relative_to(scratch)}; "
                  f"root is_symlink={stat.S_ISLNK(info.st_mode)} "
                  f"root mode={oct(stat.S_IMODE(os.stat(root).st_mode))} "
                  f"slot mode={oct(stat.S_IMODE(os.stat(real).st_mode))}")
    except Exception as error:  # the refusal shape is part of the result
        print(f"{label}: RAISED {type(error).__name__}: {error}")


def main() -> int:
    repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    scratch.mkdir(parents=True, exist_ok=False)
    stage = load(repo)
    for name in ("CCACHE_BASEDIR", "CCACHE_NOHASHDIR"):
        os.environ.pop(name, None)

    def fresh(root: Path, tmp: Path) -> None:
        """Nothing there: the helper creates the root itself."""

    def world_writable(root: Path, tmp: Path) -> None:
        """A root another account created first, writable by every account."""
        root.mkdir()
        os.chmod(root, 0o777)

    def symlinked(root: Path, tmp: Path) -> None:
        """A root that is a symbolic link to a directory chosen by its creator."""
        elsewhere = tmp / "chosen-by-another-account"
        elsewhere.mkdir()
        os.chmod(elsewhere, 0o777)
        root.symlink_to(elsewhere)

    def locks_is_file(root: Path, tmp: Path) -> None:
        """A root whose locks entry is a plain file."""
        root.mkdir()
        (root / "locks").write_text("")

    arm(stage, scratch, "fresh-root", fresh)
    arm(stage, scratch, "world-writable-root", world_writable)
    arm(stage, scratch, "symlinked-root", symlinked)
    arm(stage, scratch, "locks-is-a-file", locks_is_file)
    plain = Path(tempfile.mkdtemp(prefix="probe-", dir=scratch))
    print(f"tempfile.mkdtemp (the base's call): {plain.relative_to(scratch)} "
          f"mode={oct(stat.S_IMODE(os.stat(plain).st_mode))}, random name, created atomically")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
