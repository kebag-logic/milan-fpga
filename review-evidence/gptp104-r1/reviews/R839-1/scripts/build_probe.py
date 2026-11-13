#!/usr/bin/env python3
"""Probe the engine arm's own build() for its ccache key and failure mode.

usage: build_probe.py <mutants.py> <work-root> <label>

Imports the arm from its own file and, with the caller's environment
(CCACHE_DIR, OBJCACHE, PATH as given), stages the unmutated RTL in a new
temporary directory under <work-root>, builds it with the arm's build(),
and prints: whether an executable came back, ccache's counters for this
build alone, and whether any generated C++/header/make file under the
model directory names the temporary work directory (an absolute build path
that would reach the cache key).
"""
import importlib.util
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def stats() -> dict[str, int]:
    """ccache's nonzero counters, or {} when ccache cannot report."""
    out = subprocess.run(["ccache", "--print-stats"], capture_output=True, text=True)
    result = {}
    for line in out.stdout.splitlines():
        key, _, value = line.partition("\t")
        if value.isdigit() and int(value) and not key.endswith("_timestamp") \
                and key.endswith(("hit", "miss")):
            result[key] = int(value)
    return result


def main() -> int:
    driver, root, label = sys.argv[1:]
    spec = importlib.util.spec_from_file_location("arm", driver)
    arm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(arm)
    subprocess.run(["ccache", "--zero-stats"], capture_output=True)
    work = Path(tempfile.mkdtemp(prefix="probe-", dir=root))
    srcdir = arm.stage(work, "clean")
    exe = arm.build(srcdir, work, "clean")
    print(f"{label}: OBJCACHE={os.environ.get('OBJCACHE', '<unset>')!r} "
          f"exe={'built' if exe else 'NONE (build failed)'}")
    print(f"{label}: ccache {stats()}")
    mdir = work / "obj_clean"
    named = sorted(str(p.relative_to(work)) for p in mdir.rglob("*")
                   if p.is_file() and p.suffix in (".cpp", ".h", ".mk", ".d", ".dat")
                   and str(work).encode() in p.read_bytes())
    srcnamed = sorted(p.name for p in mdir.rglob("*") if p.is_file()
                      and p.suffix in (".cpp", ".h")
                      and str(work).encode() in p.read_bytes())
    print(f"{label}: generated C++/headers naming the work dir: {srcnamed or 'none'}")
    print(f"{label}: any generated file (.cpp .h .mk .d .dat) naming it: {len(named)}"
          f" {named[:6]}")
    return 0 if exe else 1


if __name__ == "__main__":
    sys.exit(main())
