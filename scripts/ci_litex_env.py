#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
ci_litex_env.py - put a CI runner in a state where the SoC can be elaborated.

WHY THIS EXISTS. Every argv-to-RTL-parameter chain in this repository used to
be proven by source-text greps against sw/litex/milan_soc.py, because no CI
job elaborated the SoC (#154). Three separate blockers in three lanes were
the same defect underneath: a flag parsed, threaded part of the way, and never
reaching the parameter it names. Gate 23f observes what elaboration really
hands Instance("milan_datapath"), which closes the class - but it needs LiteX,
and CI had none.

WHAT IT DOES. Two things a `pip install` cannot:

  1. Clones the VexiiRiscv Scala source into the pythondata package, because
     LiteX's own `git_setup` returns immediately unless --update-repo asks it
     to, and milan_soc.py never passes that. Without it the CPU wrapper's
     netlist-argument generator has nothing to run and elaboration dies before
     the datapath is reached.

  2. DERIVES the revision from LiteX rather than restating it. The pin lives
     in litex/soc/cores/cpu/vexiiriscv/core.py as the argument of the
     git_setup call; this script reads that call. A pin copied to a second
     place is a pin that goes stale in silence (the derive-never-mirror rule),
     and the failure mode is not a red build: it is a netlist generated from
     the wrong CPU source. If the call cannot be found the script REFUSES,
     because guessing a revision is the thing it exists to prevent.

WHAT IT DOES NOT DO. It places the VexiiRiscv SOURCE and nothing else. The
patches that make this tree elaborable at all are carried in
sw/litex/patches/ and applied by that directory's apply.sh, which is a
separate step and must run after this one - upstream LiteX has no `baremetal`
VexiiRiscv variant and the revision it pins rejects the --scala-args four of
the five configs pass (#185). Gate 23g names any recipe it could not run
rather than passing over it.

Run: python3 scripts/ci_litex_env.py [--check]
     --check reports what it would do and changes nothing.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

#: The call this script reads its pin out of, in LiteX's own source.
#: Deliberately anchored on the repository name as well as the function, so a
#: refactor that moves the call still matches and one that renames the CPU
#: does not silently match the NaxRiscv line two screens below it.
GIT_SETUP = re.compile(
    r'git_setup\(\s*"VexiiRiscv"\s*,\s*\w+\s*,\s*"([^"]+)"\s*,'
    r'\s*"([^"]+)"\s*,\s*"([0-9a-f]{7,40})"')


def _pin():
    """(url, branch, sha) LiteX pins VexiiRiscv to, read out of LiteX."""
    from litex.soc.cores.cpu.vexiiriscv import core
    m = GIT_SETUP.search(Path(core.__file__).read_text(encoding="utf-8"))
    if not m:
        sys.exit(f"{core.__file__}: no git_setup(\"VexiiRiscv\", ...) call "
                 "with a pinned revision. This script refuses to guess one: "
                 "a wrong revision does not fail the build, it generates a "
                 "netlist from the wrong CPU source.")
    return m.groups()


def _run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> int:
    """Place the VexiiRiscv source at the revision LiteX itself pins, and say where.

    Always 0: every way this can fail - an unreadable pin, a clone or checkout
    that does not run, a HEAD that is not the pin - raises or exits rather than
    returning, because a runner left with the wrong CPU source does not fail
    the build, it generates a netlist nobody asked for.
    """
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="report the pin and the target path, change nothing")
    args = ap.parse_args()

    from pythondata_cpu_vexiiriscv import data_location
    url, branch, sha = _pin()
    ext = Path(data_location) / "ext" / "VexiiRiscv"
    print(f"VexiiRiscv pin (read from LiteX): {sha} on {branch} of {url}")
    print(f"target: {ext}")
    if args.check:
        print("--check: nothing done")
        return 0

    if not (ext / ".git").is_dir():
        ext.parent.mkdir(parents=True, exist_ok=True)
        # A blobless clone rather than --depth 1: the pin is not the branch
        # tip, so a shallow clone cannot check it out, and blobless keeps the
        # transfer to the same order as a shallow one.
        _run(["git", "clone", "--filter=blob:none", "--no-checkout",
              url, str(ext)])
    _run(["git", "checkout", "--detach", sha], cwd=ext)
    _run(["git", "submodule", "update", "--init", "--recursive",
          "--filter=blob:none"], cwd=ext)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ext,
                          capture_output=True, text=True).stdout.strip()
    assert head == sha or sha.startswith(head[:len(sha)]) or \
        head.startswith(sha), f"{ext}: HEAD is {head}, want {sha}"
    print(f"VexiiRiscv ready at {head}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
