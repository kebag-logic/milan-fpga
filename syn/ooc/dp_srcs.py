#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Print the milan_datapath source list, one absolute path per line.

THE POINT IS THAT THERE IS NO SECOND COPY. The datapath entry is the
"milan_datapath|..." line in syn/yosys/run.sh — the one the portability gate
proves elaborates on every run — and its submodule half comes from
scripts/pp_srcs.py, which derives it from the tree. A hand-maintained duplicate
in a Vivado .tcl would drift the first time a module lands, and the drift would
show up as a synthesis result quietly missing a block. So the .tcl execs this
instead.

This file scraped run.sh's `PP_SRCS="..."` textually until that assignment
became a command substitution, whose inner quotes truncated the non-greedy
capture: 104 sources became 62, exit 0, no diagnostic, and Vivado said only
`module 'KL_pp_shadow' not found`. Scraping a build file is a recogniser;
calling the generator resolves.

Used by syn/ooc/milan_datapath_ooc.tcl.
"""
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


def main() -> int:
    run_sh = os.path.join(REPO, "syn", "yosys", "run.sh")
    with open(run_sh) as fh:
        s = fh.read()

    m = re.search(r'"milan_datapath\|(.*?)"\n', s, re.S)
    if not m:
        print("dp_srcs: no milan_datapath top in run.sh", file=sys.stderr)
        return 2
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
        print("dp_srcs: the milan_datapath entry in run.sh no longer references "
              "$PP_SRCS. Expanding it now would emit a datapath without its "
              "control plane, at exit 0.", file=sys.stderr)
        return 2
    pp = subprocess.run(
        [sys.executable, os.path.join(REPO, "scripts", "pp_srcs.py"),
         "--prefix", os.path.join(REPO, "protocol-processor", "hdl")],
        capture_output=True, text=True)
    if pp.returncode != 0:
        sys.stderr.write(pp.stderr)
        return 2
    derived = pp.stdout.split()
    # run.sh's PP_SRCS is the derived submodule half PLUS this repository's own
    # two wrappers; compose it the same way or the OOC netlist loses them and
    # Vivado reports `module 'KL_pp_shadow' not found`.
    srcs = srcs.replace("$PP_SRCS", " ".join(
        derived + [os.path.join(REPO, w) for w in PARENT_WRAPPERS]))

    env = {
        "R": REPO,
        "A": os.path.join(REPO, "third_party/verilog-axis/rtl"),
        "C": os.path.join(REPO, "hdl/common"),
        "Q": os.path.join(REPO, "hdl/ieee8021q/ts"),
        "P": os.path.join(REPO, "hdl/ieee8021as/ptp_timestamp"),
        "E": os.path.join(REPO, "hdl/common/eth_event_counter"),
        "D": os.path.join(REPO, "hdl/ieee17221/adp"),
        "F": os.path.join(REPO, "hdl/ieee8021q/filtering"),
        # the protocol-processor submodule root, as run.sh's PP_SRCS spells it
        "PP": os.path.join(REPO, "protocol-processor/hdl"),
    }
    # longest key first: "$PP/" must not be eaten by the "$P" rule
    for k in sorted(env, key=len, reverse=True):
        srcs = srcs.replace("$" + k + "/", env[k] + "/")

    files = [f for f in srcs.split() if f.endswith((".sv", ".v"))]
    missing = [f for f in files if not os.path.exists(f)]
    if missing:
        print("dp_srcs: missing sources:\n  " + "\n  ".join(missing), file=sys.stderr)
        return 1

    # A SHORT LIST AT EXIT 0 IS THE FAILURE THIS FILE CAUSED ONCE ALREADY, so
    # assert what the output must contain rather than trusting the expansion.
    # The old guards could not see it: one only checked that the variable NAME
    # was present, the other only inspected tokens ending in .sv/.v, and the
    # truncation residue ended in neither. Both stayed silent while the control
    # plane vanished from the netlist.
    emitted = set(files)
    lost = [f for f in derived if f not in emitted]
    lost += [w for w in PARENT_WRAPPERS
             if os.path.join(REPO, w) not in emitted]
    # ...and name the plane itself, not just a count. A generator that returned
    # a truncated list would satisfy the loop above -- everything it derived
    # survived -- while emitting a datapath with no processor in it. This is
    # the module milan_datapath.sv instantiates through KL_pp_shadow, so its
    # absence is not a stale list, it is a netlist that cannot elaborate.
    if not any(os.path.basename(f) == "protocol_processor_top.sv" for f in files):
        lost.append("protocol_processor_top.sv (the control plane itself)")
    if lost:
        print("dp_srcs: %d source(s) were derived but did not survive expansion "
              "into the milan_datapath entry:\n  %s"
              % (len(lost), "\n  ".join(lost)), file=sys.stderr)
        return 2

    print("\n".join(files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
