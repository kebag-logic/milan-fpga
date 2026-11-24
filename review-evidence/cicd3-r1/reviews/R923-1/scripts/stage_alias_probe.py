#!/usr/bin/env python3
"""Two concurrent holders of scripts/mutant_stage.py's slot, reaching the same
physical temporary directory through two TMPDIR spellings (a directory and a
symbolic link to it). Reports whether both were handed the same physical slot.

usage: python3 -I stage_alias_probe.py REPO SCRATCH
"""

import importlib.util
import os
import sys
import tempfile
from pathlib import Path


def main() -> int:
    repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    scratch.mkdir(parents=True, exist_ok=False)
    real = scratch / "tmp"
    real.mkdir()
    alias = scratch / "tmp-alias"
    alias.symlink_to(real)
    spec = importlib.util.spec_from_file_location("mutant_stage", repo / "scripts/mutant_stage.py")
    stage = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(stage)
    os.environ["TMPDIR"] = str(real)
    tempfile.tempdir = None
    with stage.directory("alias-") as first:
        Path(first, "live-build-output.o").write_text("in use by the first holder\n")
        os.environ["TMPDIR"] = str(alias)
        tempfile.tempdir = None
        with stage.directory("alias-") as second:
            same = Path(first).resolve() == Path(second).resolve()
            survived = Path(first, "live-build-output.o").exists()
            print(f"first holder:  {Path(first).relative_to(scratch)}")
            print(f"second holder: {Path(second).relative_to(scratch)}")
            print(f"same physical slot while both held: {same}; first holder's file survived: {survived}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
