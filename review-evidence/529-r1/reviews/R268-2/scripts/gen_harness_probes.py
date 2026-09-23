#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Write the silence-shortcut probe harnesses next to sim_nxn.cpp.

usage: gen_harness_probes.py <tb/verilator/milan_dp dir of a disposable tree>

  sim_nxn_fullsilence.cpp  no counter write; the whole 100 ms silence and the
                           same 0.1 ms margin run for real (equivalence probe)
  sim_nxn_nowrite.cpp      no counter write; only the 1.1 ms tail runs (the
                           unlock checks must go red: they depend on the timeout)
  sim_nxn_shorttail.cpp    the counter write, then 0.99 ms instead of 1.1 ms
                           (must go red: the write alone must not unlock)
Each substitution is anchored on the exact head text and must match once.
"""
import hashlib
import pathlib
import sys

WRITE = ("        dut->rootp->milan_datapath__DOT__crf_rx__DOT__tout_r = "
         "kCrfSilenceCyc - kFabricMsCyc;\n")
LOOP = "        for (uint32_t c = 0; c < kFabricMsCyc + kFabricMsCyc / 10; c++) step();\n"

PROBES = {
    "sim_nxn_fullsilence.cpp": [
        (WRITE, ""),
        (LOOP, "        for (uint32_t c = 0; c < kCrfSilenceCyc + kFabricMsCyc / 10; c++) step();\n"),
    ],
    "sim_nxn_nowrite.cpp": [(WRITE, "")],
    "sim_nxn_shorttail.cpp": [
        (LOOP, "        for (uint32_t c = 0; c < kFabricMsCyc - kFabricMsCyc / 100; c++) step();\n"),
    ],
}


def main() -> int:
    d = pathlib.Path(sys.argv[1])
    src = (d / "sim_nxn.cpp").read_text()
    for name, subs in PROBES.items():
        m = src
        for old, new in subs:
            if m.count(old) != 1:
                raise SystemExit(f"{name}: anchor matched {m.count(old)} times: {old!r}")
            m = m.replace(old, new)
        (d / name).write_text(m)
        print(name, hashlib.sha256(m.encode()).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
