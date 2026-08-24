#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Print the source list of a top named in syn/yosys/run.sh, one path per line.

THE POINT IS THAT THERE IS NO SECOND COPY. A top's source list is the
"<top>|..." entry in syn/yosys/run.sh -- the one the portability gate proves
elaborates on every run -- and its submodule half comes from scripts/pp_srcs.py,
which derives it from the tree. A hand-maintained duplicate in a Vivado .tcl
would drift the first time a module lands, and the drift would show up as a
synthesis result quietly missing a block. So the .tcl execs this instead.

This file scraped run.sh's `PP_SRCS="..."` textually until that assignment
became a command substitution, whose inner quotes truncated the non-greedy
capture: 104 sources became 62, exit 0, no diagnostic, and Vivado said only
`module 'KL_pp_shadow' not found`. Scraping a build file is a recogniser;
calling the generator resolves.

`--top` selects the entry. It defaults to `milan_datapath`, which is the only
top this file served when it was written; `KL_pp_shadow` is the second. That
script assembled its own read set instead -- the submodule half from
scripts/pp_srcs.py plus a hand-named axis_fifo.v -- and the one file the
assembly did not name was the module it passed to `synth_design -top`, so the
documented plane-area recipe read 41 sources and then failed with
`ERROR: [Synth 8-439] module 'KL_pp_shadow' not found` (Issue #235). Hence the
last check below: this file refuses to emit a list in which nothing declares
the top it was asked for, whatever the list was built from.

Used by syn/ooc/milan_datapath_ooc.tcl and syn/ooc/pp_shadow_ooc.tcl.
"""
import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

#: This repository's own two wrappers, which run.sh appends to the derived
#: submodule half. They are the parent's files, not the submodule's, so the
#: generator does not emit them; every consumer names them. Named here so the
#: assertion below can prove they survived the expansion.
PARENT_WRAPPERS = ("hdl/milan/KL_pp_shadow.sv", "hdl/milan/KL_pp_maap_shim.sv")


def _reader(path):
    with open(path) as fh:
        return fh.read()


def build(top, run_sh, derived, repo=REPO, exists=os.path.exists, read=_reader):
    """Expand `top`'s entry in run.sh's text. Returns (files, problems, rc).

    `run_sh`, `derived`, `exists` and `read` are the inputs, injected rather
    than read, so that `selftest()` can prove every check below bites without
    editing the repository to do it.
    """
    m = re.search(r'"%s\|(.*?)"\n' % re.escape(top), run_sh, re.S)
    if not m:
        return [], ["dp_srcs: no %s top in run.sh" % top], 2
    srcs = m.group(1)

    # The one collected list that entry references. It used to be three
    # (AECP_SRCS / LWSRP_SRCS / PP_SRCS): the first two named the 1722.1 and
    # SRP planes, which are deleted, and PP_SRCS - the protocol processor that
    # replaced them - is no longer optional, so the datapath entry expands it
    # like any other source. A name listed here that run.sh no longer defines
    # is a hard error on purpose: silently dropping it would emit a source list
    # missing a whole plane, and Vivado would only say "module not found".
    # PP_SRCS is DERIVED, so there is nothing in run.sh to scrape. This used to
    # lift the literal with `PP_SRCS="(.*?)"`, and when run.sh switched to a
    # command substitution the inner quotes truncated that capture to
    # `$(python3 ` -- 104 sources became 62, exit 0, no diagnostic, and Vivado
    # only said `module 'KL_pp_shadow' not found`. Calling the generator cannot
    # fail that way: it either returns the list or exits non-zero.
    if "$PP_SRCS" not in srcs:
        return [], ["dp_srcs: the %s entry in run.sh no longer references "
                    "$PP_SRCS. Expanding it now would emit a top without its "
                    "control plane, at exit 0." % top], 2
    # run.sh's PP_SRCS is the derived submodule half PLUS this repository's own
    # two wrappers; compose it the same way or the OOC netlist loses them and
    # Vivado reports `module 'KL_pp_shadow' not found`.
    srcs = srcs.replace("$PP_SRCS", " ".join(
        derived + [os.path.join(repo, w) for w in PARENT_WRAPPERS]))

    env = {
        "R": repo,
        "A": os.path.join(repo, "third_party/verilog-axis/rtl"),
        "C": os.path.join(repo, "hdl/common"),
        "Q": os.path.join(repo, "hdl/ieee8021q/ts"),
        "P": os.path.join(repo, "hdl/ieee8021as/ptp_timestamp"),
        "E": os.path.join(repo, "hdl/common/eth_event_counter"),
        "D": os.path.join(repo, "hdl/ieee17221/adp"),
        "F": os.path.join(repo, "hdl/ieee8021q/filtering"),
        # the protocol-processor submodule root, as run.sh's PP_SRCS spells it
        "PP": os.path.join(repo, "protocol-processor/hdl"),
    }
    # longest key first: "$PP/" must not be eaten by the "$P" rule
    for k in sorted(env, key=len, reverse=True):
        srcs = srcs.replace("$" + k + "/", env[k] + "/")

    files = [f for f in srcs.split() if f.endswith((".sv", ".v"))]
    missing = [f for f in files if not exists(f)]
    if missing:
        return files, ["dp_srcs: missing sources:\n  " + "\n  ".join(missing)], 1

    # A SHORT LIST AT EXIT 0 IS THE FAILURE THIS FILE CAUSED ONCE ALREADY, so
    # assert what the output must contain rather than trusting the expansion.
    # The old guards could not see it: one only checked that the variable NAME
    # was present, the other only inspected tokens ending in .sv/.v, and the
    # truncation residue ended in neither. Both stayed silent while the control
    # plane vanished from the netlist.
    emitted = set(files)
    lost = [f for f in derived if f not in emitted]
    lost += [w for w in PARENT_WRAPPERS
             if os.path.join(repo, w) not in emitted]
    # ...and name the plane itself, not just a count. A generator that returned
    # a truncated list would satisfy the loop above -- everything it derived
    # survived -- while emitting a top with no processor in it. This is the
    # module milan_datapath.sv and KL_pp_shadow.sv both instantiate, so its
    # absence is not a stale list, it is a netlist that cannot elaborate.
    if not any(os.path.basename(f) == "protocol_processor_top.sv" for f in files):
        lost.append("protocol_processor_top.sv (the control plane itself)")
    if lost:
        return files, ["dp_srcs: %d source(s) were derived but did not survive "
                       "expansion into the %s entry:\n  %s"
                       % (len(lost), top, "\n  ".join(lost))], 2

    # THE TOP ITSELF. Every check above compares the list against what went
    # into it, and all of them pass on a list that contains everything except
    # the one module the consumer will name as `-top`: that is Issue #235,
    # where pp_shadow_ooc.tcl read its 41 sources and Vivado answered
    # `module 'KL_pp_shadow' not found`. So compare the list against the top as
    # well, by reading the sources for the declaration rather than by matching
    # a file name -- a file named after the module is a convention, and the
    # convention is not what synthesis resolves.
    decl = re.compile(r"^[ \t]*module[ \t]+%s\b" % re.escape(top), re.M)
    if not any(decl.search(read(f)) for f in files):
        return files, ["dp_srcs: none of the %d source(s) in run.sh's \"%s|...\" "
                       "entry declares `module %s`. Synthesis would read every "
                       "one of them and then fail with `module '%s' not found` "
                       "(Issue #235), which reads as a missing module and is "
                       "really a read set that never contained the top."
                       % (len(files), top, top, top)], 2

    return files, [], 0


def selftest(top="faketop"):
    """Prove every check bites, on synthetic inputs, without editing the tree.

    CONTRIBUTING.md section 3 states the bar for a checker in this repository:
    it carries a self-test that runs in a gate "so the tool cannot rot into a
    green that means nothing". Every arm below drives the real `build()`, so
    stubbing it to return no problems fails this.

    Planting the defect in syn/yosys/run.sh and restoring it afterwards would
    work exactly until the process is killed between the two writes, and it
    cannot run on a read-only checkout. Injecting the inputs instead exercises
    the same function and touches nothing. scripts/pp_srcs.py:selftest makes
    the same argument for the same reason.
    """
    pp = os.path.join(REPO, "protocol-processor/hdl")
    derived = [os.path.join(pp, "common/pp_pkg.sv"),
               os.path.join(pp, "top/protocol_processor_top.sv")]
    wrappers = [os.path.join(REPO, w) for w in PARENT_WRAPPERS]
    # what each synthetic source declares, for the top-declaration check
    text = {f: "module %s;\nendmodule\n" % os.path.basename(f)[:-3]
            for f in derived + wrappers + [os.path.join(REPO, "a/axis_fifo.v")]}
    text[wrappers[0]] = "module %s #(\n) ();\nendmodule\n" % top

    def run(world, tp=top):
        return build(tp, world, derived, exists=lambda f: True,
                     read=lambda f: text.get(f, ""))

    clean = '  "%s|$A/axis_fifo.v $PP_SRCS"\n' % top
    problems = []

    def arm(name, world, want, tp=top):
        _files, bad, rc = run(world, tp)
        if not any(want in b for b in bad) or rc == 0:
            problems.append("SELF-TEST FAILED [%s]: expected a finding naming "
                            "%r at rc!=0, got rc=%d %s"
                            % (name, want, rc, bad or "no findings"))

    # Arm 0. The clean world is clean. Without this the other arms could all be
    # passing on a check that simply reports everything.
    files, bad, rc = run(clean)
    if bad or rc or len(files) != len(derived) + len(wrappers) + 1:
        problems.append("SELF-TEST FAILED [clean]: the well-formed entry must "
                        "expand clean, got rc=%d %s, %d file(s)"
                        % (rc, bad, len(files)))

    # Arm 1. The entry is gone, or the top was misspelled by its consumer.
    arm("no-entry", clean, "no othertop top in run.sh", tp="othertop")

    # Arm 2. The entry stops referencing the collected list.
    arm("no-pp-srcs", '  "%s|$A/axis_fifo.v"\n' % top, "no longer references")

    # Arm 3. A derived source that does not survive the expansion, because
    # the suffix filter below the substitution drops it. That filter is what
    # made the historical truncation invisible: it inspected only tokens
    # ending in .sv/.v, and what was left of the list ended in neither.
    saved, derived = derived, derived + [os.path.join(pp, "acmp/ghost.svh")]
    arm("derived-source-lost", clean, "did not survive expansion")
    derived = saved

    # Arm 4. The plane itself missing, which a count-based check cannot see.
    saved, derived = derived, [os.path.join(pp, "common/pp_pkg.sv")]
    arm("plane-lost", clean, "protocol_processor_top.sv (the control plane")
    derived = saved

    # Arm 5. ISSUE #235. Every source present and correct, and not one of them
    # declares the top. Vivado's answer to this list is `module not found`.
    saved, text[wrappers[0]] = text[wrappers[0]], "module something_else;\n"
    arm("top-not-in-read-set", clean, "declares `module %s`" % top)
    text[wrappers[0]] = saved

    # Arm 6. The same, one step subtler: the file is named after the top and
    # does not declare it, which a file-name check would pass.
    saved, text[wrappers[0]] = text[wrappers[0]], "// KL_pp_shadow lives here\n"
    arm("named-not-declared", clean, "declares `module %s`" % top)
    text[wrappers[0]] = saved

    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--top", default="milan_datapath",
                    help="the run.sh entry to expand (default: milan_datapath)")
    ap.add_argument("--selftest", action="store_true",
                    help="prove each check fails on a planted defect")
    args = ap.parse_args()

    if args.selftest:
        bad = selftest()
        for b in bad:
            print("  -", b, file=sys.stderr)
        if bad:
            return 2
        print("dp_srcs self-test: 7 arm(s) passed")
        return 0

    with open(os.path.join(REPO, "syn", "yosys", "run.sh")) as fh:
        run_sh = fh.read()
    pp = subprocess.run(
        [sys.executable, os.path.join(REPO, "scripts", "pp_srcs.py"),
         "--prefix", os.path.join(REPO, "protocol-processor", "hdl")],
        capture_output=True, text=True)
    if pp.returncode != 0:
        sys.stderr.write(pp.stderr)
        return 2
    files, problems, rc = build(args.top, run_sh, pp.stdout.split())
    for p in problems:
        print(p, file=sys.stderr)
    if rc:
        return rc
    print("\n".join(files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
