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
import subprocess
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
    # Tracked files only. Reading the working tree compiles an untracked stray
    # `.sv` that no other checkout has, which is a build that cannot be
    # reproduced and a defect that appears only on one machine.
    out = subprocess.run(["git", "ls-files", "*.sv"], cwd=PP_HDL,
                         capture_output=True, text=True)
    if out.returncode:
        raise SystemExit(f"git ls-files failed in {PP_HDL}: {out.stderr.strip()}")
    files = [PP_HDL / f for f in out.stdout.split()
             if pathlib.Path(f).stem not in EXCLUDE]
    if not files:
        raise SystemExit(f"{PP_HDL} contains no tracked .sv files")
    # A package is a file that DECLARES one, read from the source. Keying on
    # the `_pkg.sv` suffix is a naming convention, and a package in a file
    # named otherwise would sort after its importers and fail to elaborate.
    pkg_re = re.compile(r"^\s*package\s+\w+\s*;", re.M)
    pkgs = sorted(p for p in files if pkg_re.search(p.read_text()))
    rest = sorted(p for p in files if not pkg_re.search(p.read_text()))
    return [f"{prefix}/{p.relative_to(PP_HDL)}" for p in pkgs + rest]


#: Files allowed to name a submodule source literally, mapped to the EXACT
#: literals permitted and why. Not a per-file exemption: exempting a whole file
#: let a reviewer revert `sw/litex/milan_soc.py` to a hand-written list and pass,
#: because the file was already on the list for an unrelated comment. Any
#: literal not named here fails, in every file.
PROSE_OK = {
    "hdl/milan/KL_pp_shadow.sv": (
        {"protocol-processor/hdl/aecp/KL_aecp_engine.sv"},
        "an RTL comment citing the submodule module it wraps"),
    "sw/builder/test_builder.py": (
        {"protocol-processor/hdl/adp/KL_adp_engine.sv",
         "protocol-processor/hdl/adp/pp_adp_pkg.sv"},
        "a gate citing submodule paths in its findings"),
    "sw/litex/milan_soc.py": (
        {"protocol-processor/hdl/top/protocol_processor_top.sv"},
        "a comment citing a submodule line number, not a source entry"),
    "tests/steps/aecp_engine_steps.py": (
        {"protocol-processor/hdl/aecp/KL_aecp_desc_store.sv",
         "protocol-processor/hdl/aecp/KL_aecp_engine.sv",
         "protocol-processor/hdl/aecp/KL_aecp_ucpu.sv"},
        "BDD steps citing the RTL they mirror"),
    "syn/yosys/ooc.sh": (
        {"$PP/aecp/ucpu_pkg.sv", "$PP/acmp/pp_acmp_pkg.sv"},
        "ROM geometry DERIVED by reading the pinned packages at run time "
        "(#245): the opposite of a copied list, and these two names are the "
        "read targets, not compile entries -- its compile list stays derived "
        "through this script"),
}

#: This file's own entry is DERIVED from the table above, because the table is
#: made of the literals it permits and hardcoding them here would mean editing
#: two lists to add one -- which is the defect this whole script is about.
PROSE_OK["scripts/pp_srcs.py"] = (
    {lit for lits, _ in PROSE_OK.values() for lit in lits}
    | {"$PP/common/pp_pkg.sv"},
    "this generator: the table above quotes every literal it permits, and the "
    "docstring and self-test quote a source path")

#: A literal submodule source reference, in any of the spellings the build
#: inputs use for the submodule root.
LITERAL_RE = re.compile(
    r"(?:protocol-processor/hdl|\$PP\b|\$\(PP_DIR\)|\$\{PP\})/\w+/\w+\.sv")


def check(files=None, read=None):
    """Find any build input carrying a literal copy of the source list.

    DISCOVERED, not listed. The first version of this check took a list of
    consumers and exempted any file containing the substring `pp_srcs.py`, so
    it had two holes at once and a reviewer walked through both: reverting a
    consumer to a hand-written literal passed as long as the comment above the
    edit still mentioned the script, and a fifth consumer was invisible because
    the consumer list was itself hand-written -- the same defect the script
    exists to fix, one level up.

    So the property is inverted and widened. No tracked file outside PROSE_OK
    may name a submodule source literally. That cannot be satisfied by a
    comment, it needs no consumer list, and a build input added tomorrow is
    caught the first time it names a source.

    `files` and `read` inject the universe under test. They default to the
    tracked tree, and `selftest()` supplies synthetic ones so that proving this
    function bites does not mean editing the repository to do it.
    """
    if files is None:
        out = subprocess.run(["git", "ls-files"], cwd=ROOT,
                             capture_output=True, text=True)
        if out.returncode:
            return [f"git ls-files failed: {out.stderr.strip()}"], []
        files = out.stdout.split()
    if read is None:
        def read(f):
            return (ROOT / f).read_text()
    tracked = set(files)
    bad, ok = [], []
    for f in files:
        # The submodule names its own sources in its own build inputs; this
        # gate is about THIS repository keeping a copy of them. Markdown is
        # skipped because a document is not a build input: docs cite paths to
        # say where something lives, and a stale citation in prose does not
        # silently drop a module from a netlist.
        if f.startswith("protocol-processor/") or f.endswith(".md"):
            continue
        try:
            text = read(f)
        except (OSError, UnicodeDecodeError):
            continue
        hits = set(LITERAL_RE.findall(text))
        if not hits:
            continue
        allowed, _reason = PROSE_OK.get(f, (set(), ""))
        extra = sorted(hits - allowed)
        if not extra:
            ok.append(f)
            continue
        bad.append(f"{f}: names submodule source(s) literally that are not "
                   f"permitted prose: {', '.join(extra)}. A build input must "
                   "derive the list with this script. If this really is prose, "
                   "add the exact literal to PROSE_OK with the reason.")
    for f in PROSE_OK:
        if f not in tracked:
            bad.append(f"PROSE_OK names {f}, which is not a tracked file")
        elif f not in ok and not any(b.startswith(f + ":") for b in bad):
            bad.append(f"PROSE_OK names {f}, which no longer contains a "
                       "permitted literal -- the entry is dead, remove it")
    return bad, ok


def _world():
    """A synthetic tree that `check()` must find clean: every PROSE_OK file,
    holding exactly the literals its entry permits and nothing else."""
    return {f: " ".join(sorted(lits)) for f, (lits, _) in PROSE_OK.items()}


def selftest():
    """Prove the check bites, on synthetic inputs, without editing the tree.

    CONTRIBUTING.md:171-174 states the bar for a checker in this repository:
    it carries a self-test that runs in a gate "so the tool cannot rot into a
    green that means nothing". Every arm below drives the real `check()`, so
    stubbing it to return no problems fails this.

    The first version of this self-test planted a literal in `syn/yosys/run.sh`
    and restored it afterwards. That works exactly until the process is killed
    between the two writes, and it cannot run on a read-only checkout. Injecting
    the universe instead exercises the same function and touches nothing.
    """
    def run(world):
        return check(files=sorted(world), read=lambda f: world[f])

    problems = []

    def arm(name, world, want):
        bad, _ok = run(world)
        hit = any(want in b for b in bad)
        if not hit:
            problems.append(f"SELF-TEST FAILED [{name}]: expected a finding "
                            f"naming {want}, got {bad or 'no findings'}")

    # Arm 0. The clean world is clean. Without this the other arms could all be
    # passing on a check that simply reports everything.
    bad, ok = run(_world())
    if bad or len(ok) != len(PROSE_OK):
        problems.append(f"SELF-TEST FAILED [clean]: the permitted-prose world "
                        f"must be clean, got {bad}, {len(ok)} prose file(s)")

    # Arm 1. A build input reverted to a hand-written literal.
    w = _world()
    w["syn/yosys/run.sh"] = 'PP_SRCS="$PP/common/pp_pkg.sv"'
    arm("revert", w, "syn/yosys/run.sh")

    # Arm 2. The same revert with the comment that names this script left in
    # place above it -- what a revert actually looks like, and what the first
    # version of this gate passed.
    w = _world()
    w["syn/yosys/ooc.sh"] = ("# Derived from the submodule tree; see "
                             'scripts/pp_srcs.py\nPP_SRCS="$PP/common/pp_pkg.sv"')
    arm("revert-under-comment", w, "syn/yosys/ooc.sh")

    # Arm 3. A consumer nobody added to any list. The gate must not need one.
    w = _world()
    w["syn/vendor/brand_new_flow.tcl"] = (
        "read_verilog protocol-processor/hdl/top/protocol_processor_top.sv")
    arm("new-consumer", w, "brand_new_flow.tcl")

    # Arm 4. A permitted-prose file that grows an EXTRA literal. PROSE_OK is
    # per-literal for this reason: a whole-file exemption would let a listed
    # file carry a full hand-written list.
    w = _world()
    w["sw/litex/milan_soc.py"] += " protocol-processor/hdl/aecp/KL_aecp_engine.sv"
    arm("prose-file-grows-a-list", w, "sw/litex/milan_soc.py")

    # Arm 5. A PROSE_OK entry whose literal is gone. A dead exemption is an
    # exemption nobody re-reads.
    w = _world()
    w["sw/litex/milan_soc.py"] = "# the citation this entry exists for is gone"
    arm("dead-exemption", w, "the entry is dead")

    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prefix", default="protocol-processor/hdl",
                    help="path prefix for each emitted entry")
    ap.add_argument("--check", action="store_true",
                    help="fail if any build input carries a literal source list")
    ap.add_argument("--selftest", action="store_true",
                    help="prove the check fails on a planted literal")
    args = ap.parse_args()

    if args.check or args.selftest:
        bad = selftest() if args.selftest else []
        problems, prose = check()
        bad += problems
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
        print(f"pp source list: {n} tracked source(s) derived; no build input "
              f"carries a literal copy"
              + (" (self-test passed)" if args.selftest else ""))
        for f in prose:
            print(f"  prose    {f}: {PROSE_OK[f][1]}")
        for stem, why in EXCLUDE.items():
            print(f"  excluded {stem}: {why}")
        return 0

    # One space-separated line. The shell consumers word-split it, the Makefile
    # takes it as a variable and the .tcl splits it into a list; a second output
    # format would be a second thing to keep working for no consumer.
    print(" ".join(pp_sources(args.prefix)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
