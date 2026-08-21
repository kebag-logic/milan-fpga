#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Emit the protocol-processor source list, derived from the tree.

WHY THIS EXISTS. Four build inputs carried the same hand-written list of
submodule filenames: ``syn/yosys/run.sh``, ``syn/yosys/ooc.sh``,
``tb/verilator/milan_dp/Makefile`` and ``sw/litex/milan_soc.py``. Nothing
compared any of them against the tree, and each copy names the other as
authoritative, so the authority was circular.

The failure mode is not that a copy is wrong. All four are correct against the
pin they were written for, and they stay correct until the submodule moves.
When it moves, a module added on the submodule side is in every tree and in no
list, and the first symptom is an elaboration error naming the missing module
rather than the stale list::

    [FAIL] KL_pp_shadow   yosys: ERROR: Module `\\KL_aecp_ca_originator'
                          referenced in module `\\protocol_processor_top' ...
                          is not part of the design.

That is the loud case. The silent case is worse: a module that no current top
instantiates is simply never built, and the portability sweep reports PASS over
a design that does not contain it. The gate's claim is that every top
elaborates off-vendor, and that claim was only ever as wide as the list.

ORDERING. Packages first, because a package must be declared before the modules
that import it; everything else sorted, because the tools do not care and a
stable order keeps diffs readable. That is the only ordering constraint the old
lists encoded, and ``tb/verilator/milan_dp/Makefile`` says so in as many words.

EXCLUSIONS are explicit and carry a reason, printed on a clean ``--check`` run.
There are none today: every ``.sv`` under the submodule's ``hdl/`` is a design
file, and the submodule keeps no testbench or simulation sources there. An
exclusion added later must say why, so that a file dropped on purpose cannot be
confused with one dropped by accident.
"""

import argparse
import pathlib
import re
import sys

#: Repository root, from this file's location.
ROOT = pathlib.Path(__file__).resolve().parent.parent
PP_HDL = ROOT / "protocol-processor" / "hdl"

#: {stem: reason}. Empty on purpose; see the module docstring.
EXCLUDE: dict[str, str] = {}


def pp_sources(prefix="protocol-processor/hdl"):
    """Every submodule design source, packages first, then sorted."""
    if not PP_HDL.is_dir():
        raise SystemExit(
            f"{PP_HDL} not found. The protocol-processor submodule is not "
            "checked out; run `git submodule update --init protocol-processor`. "
            "This script refuses to emit an empty list, because an empty list "
            "builds cleanly and proves nothing.")
    files = [p for p in PP_HDL.rglob("*.sv") if p.stem not in EXCLUDE]
    if not files:
        raise SystemExit(f"{PP_HDL} contains no .sv files")
    pkgs = sorted(p for p in files if p.name.endswith("_pkg.sv"))
    rest = sorted(p for p in files if not p.name.endswith("_pkg.sv"))
    return [f"{prefix}/{p.relative_to(PP_HDL)}" for p in pkgs + rest]


def check(paths):
    """Report any listed file that names a stale set. Returns (problems, derived).

    A file that invokes this script has no literal to check and cannot go
    stale, so it is reported as derived rather than scanned. Scanning it would
    report every source as missing, which is true of the text and false of the
    build.
    """
    have = {pathlib.Path(s).stem for s in pp_sources()}
    bad, derived = [], []
    for f in paths:
        p = ROOT / f
        if not p.is_file():
            bad.append(f"{f}: not found")
            continue
        text = p.read_text()
        if "pp_srcs.py" in text:
            derived.append(f)
            continue
        listed = set(re.findall(r"(\w+)\.sv", text)) & (
            have | set(EXCLUDE))
        missing = sorted(have - listed)
        excluded = sorted(set(EXCLUDE) & listed)
        if missing:
            bad.append(f"{f}: {len(missing)} submodule source(s) absent from "
                       f"this list: {', '.join(missing)}")
        if excluded:
            bad.append(f"{f}: names deliberately excluded source(s): "
                       f"{', '.join(excluded)}")
    return bad, derived


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prefix", default="protocol-processor/hdl",
                    help="path prefix for each emitted entry")
    ap.add_argument("--sep", default=" ", help="separator (default: a space)")
    ap.add_argument("--python-list", action="store_true",
                    help="emit as a Python list literal")
    ap.add_argument("--check", nargs="*", metavar="FILE",
                    help="verify these files name every submodule source")
    args = ap.parse_args()

    if args.check is not None:
        bad, derived = check(args.check)
        for b in bad:
            print("  -", b)
        if bad:
            print("\nA build input names a stale set of submodule sources. This "
                  "is what a\nsubmodule bump breaks and what nothing used to "
                  "catch: the copies are\ncorrect against the pin they were "
                  "written for and go stale the moment it\nmoves. Derive the "
                  "list with this script rather than editing the copy.")
            return 1
        n = len(pp_sources())
        literal = len(args.check) - len(derived)
        print(f"pp source list: {n} file(s); {len(derived)} consumer(s) derive it, "
              f"{literal} carry a literal and agree")
        for d in derived:
            print(f"  derived  {d}")
        for stem, why in EXCLUDE.items():
            print(f"  excluded {stem}: {why}")
        return 0

    srcs = pp_sources(args.prefix)
    if args.python_list:
        print("[\n" + "".join(f'    "{s}",\n' for s in srcs) + "]")
    else:
        print(args.sep.join(srcs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
