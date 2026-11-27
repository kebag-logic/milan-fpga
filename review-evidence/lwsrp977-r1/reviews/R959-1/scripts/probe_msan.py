# SPDX-License-Identifier: Apache-2.0
"""Reviewer probe: is the lean validation's delivering-pass zeroing guarded by
the head's MemorySanitizer run? Plants its removal and runs the head's own
sanitized() on the end-station build.

usage: python3 -I probe_msan.py <checkout> <new-work-dir> <clang> [--milan OFF|ON] [--seeds N]
"""
import argparse
import importlib.util
from pathlib import Path
import shutil
import sys

OLD = "                if (on_attr) {\n                    memset(value, 0, sizeof(value));\n                }\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("checkout", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("clang")
    ap.add_argument("--milan", default="OFF")
    ap.add_argument("--seeds", type=int, default=200)
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location("cd", a.checkout / "tests/check_differential.py")
    cd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cd)
    work = a.work.resolve()
    work.mkdir(parents=True)
    tree = work / "probe-lean-delivered-unzeroed"
    shutil.copytree(a.checkout / "src", tree / "src")
    target = tree / "src/core/mrp_pdu.c"
    text = target.read_text()
    if OLD not in text:
        print("TARGET-MISSING")
        return 2
    target.write_text(text.replace(OLD, "", 1))
    seen = cd.sanitized(work, tree / "src", a.clang, a.milan, a.seeds, cd.PROGRAMS["mad"][2], "probe")
    print(f"{'REPORTED' if isinstance(seen, int) else ('BUILD-FAIL' if seen else 'NOT REPORTED')} "
          f"lean-delivered-unzeroed under MemorySanitizer milan={a.milan}" +
          (f" at seed {seen}" if isinstance(seen, int) else f" over {a.seeds} seeds"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
