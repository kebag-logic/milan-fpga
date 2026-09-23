#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run the engine suite's own mutation arm, or a reviewer-owned list, from an
exported source tree.

The tree's tb/verilator/engine/mutants.py is imported unchanged; only three
module attributes are replaced before its main() runs:
  * MUTATIONS: a round-robin slice of its own list, or the reviewer list;
  * VFLAGS: the Verilator build job count ("-j 4" -> "-j <jobs>");
  * nothing else. The control (unmutated sources must pass) always runs.

usage:
  mutant_slices.py <tree> own <slice> <nslices> [jobs]
  mutant_slices.py <tree> reviewer [jobs]
Staging goes to $TMPDIR, as mutants.py already does; the tree is not written.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

GEN = "ucode/gen_gptp_ucode.py"

#: (name, file under hdl/, pattern, replacement, the property it should break)
REVIEWER_MUTATIONS = [
    ("R1 every good Pdelay verdict re-arms the link-up", GEN,
     "    p.emit(\"CMP\", ra=RU, rb=0, fmt=FMT_D, imm=FL_ASCAP_C)\n"
     "    p.emit(\"BRS\", cnd=BRS_Z, label=\"done\")           "
     "# already capable\n",
     "",
     "only an asCapable RISE re-arms the link-up, not every good exchange"),
    ("R2 the asCapable fall re-arms instead of the rise", GEN,
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_LOCK, fmt=FMT_Q)"
     "  # rose: link-up\n"
     "    p.emit(\"BR\", label=\"done\")\n"
     "    p.label(\"bad\")\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_PDOK, fmt=FMT_Q)\n",
     "    p.emit(\"BR\", label=\"done\")\n"
     "    p.label(\"bad\")\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_PDOK, fmt=FMT_Q)\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_LOCK, fmt=FMT_Q)\n",
     "a reset and every other asCapable fall re-arm through the rise"),
    ("R3 link-up threshold 1 ns wider", GEN,
     "STEP_LINKUP_NS_C = 20000 ",
     "STEP_LINKUP_NS_C = 20001 ",
     "a link-up pair steps above exactly 20 us"),
    ("R4 link-up threshold 1 ns narrower", GEN,
     "STEP_LINKUP_NS_C = 20000 ",
     "STEP_LINKUP_NS_C = 19999 ",
     "a link-up pair of exactly 20 us slews"),
    ("R5 locked threshold 1 ns wider", GEN,
     "STEP_LOCKED_NS_C = 100000 ",
     "STEP_LOCKED_NS_C = 100001 ",
     "a locked pair steps above exactly 100 us"),
    ("R6 locked threshold 1 ns narrower", GEN,
     "STEP_LOCKED_NS_C = 100000 ",
     "STEP_LOCKED_NS_C = 99999 ",
     "a locked pair of exactly 100 us slews"),
]


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    mode = sys.argv[2]
    path = tree / "tb/verilator/engine/mutants.py"
    spec = importlib.util.spec_from_file_location("engine_mutants", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    if mode == "own":
        k, n = int(sys.argv[3]), int(sys.argv[4])
        jobs = sys.argv[5] if len(sys.argv) > 5 else "2"
        m.MUTATIONS = m.MUTATIONS[k::n]
    elif mode == "reviewer":
        jobs = sys.argv[3] if len(sys.argv) > 3 else "2"
        m.MUTATIONS = REVIEWER_MUTATIONS
    else:
        raise SystemExit(f"unknown mode {mode}")
    vf = list(m.VFLAGS)
    vf[vf.index("-j") + 1] = jobs
    m.VFLAGS = vf
    print(f"mutants in this run: {len(m.MUTATIONS)}; build jobs {jobs}")
    for name, *_ in m.MUTATIONS:
        print(f"  - {name}")
    sys.stdout.flush()
    return m.main()


if __name__ == "__main__":
    sys.exit(main())
