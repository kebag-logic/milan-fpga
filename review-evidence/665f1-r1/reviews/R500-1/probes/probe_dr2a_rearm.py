#!/usr/bin/env python3
# R500-1 probe W: DR2a's 1,000 ms first-dirty window after a change that is
# made while a capture is running and is captured by it. nvm_store_changed()
# arms the window's start only when it is not armed, and only the next
# capture's start disarms it; a change captured by the running capture leaves
# it armed with that change's time. Harness-only seam: a script word that
# services until a given write phase. The store is unchanged.
from __future__ import annotations

import sys

from r500_common import bench, planted_tree

STEM = sys.argv[1] if len(sys.argv) > 1 else "endstation_ax7101_1x1_tdm8"
SEAM = [("test/nvm_test.c",
         "\telse if (strcmp(a, \"--flip\") == 0)\n",
         "\telse if (strcmp(a, \"--until-phase\") == 0) {\n"
         "\t\twhile (nvm_store_status()->phase != (enum nvm_phase)strtoul(v, NULL, 0))\n"
         "\t\t\tt_service();\n"
         "\t} else if (strcmp(a, \"--flip\") == 0)\n")]
tree = planted_tree("phase_harness", SEAM)
b = bench(STEM, "phase_harness", tree)
golden = b.file("g.bin", b.assemble(b.frames, 5))
rids = sorted(b.frames)
x, y, z = rids[0], rids[len(rids) // 2], rids[-1]


def val(rid: int, seed: int) -> str:
    plen = len(b.frames[rid]) - 8
    return bytes((rid * 13 + j * 11 + seed) & 0xFF for j in range(plen)).hex()


common = ["--slot-b", golden, "--boot", "--set", f"{x}:{val(x, 1)}", "--until-phase", "2"]
cases = {
    # control: Y is made before the capture starts; Z, 5 s after the commit,
    # must wait its own 1,000 ms window
    "control_y_before_capture": ["--slot-b", golden, "--boot", "--set", f"{x}:{val(x, 1)}",
                                 "--set", f"{y}:{val(y, 1)}", "--until-idle", "--run-ms", "5000",
                                 "--set", f"{z}:{val(z, 1)}", "--run-ms", "50"],
    # Y is made after the capture started and is captured by it; Z, 5 s later
    "y_during_capture": common + ["--set", f"{y}:{val(y, 1)}", "--until-idle", "--run-ms", "5000",
                                  "--set", f"{z}:{val(z, 1)}", "--run-ms", "50"],
}
for name, script in cases.items():
    r = b.run(*script)
    e = r.erases
    print(f"{name}: ok={r.s['ok']} erases={r.s['erases']} dirty={r.s['dirty']} "
          f"erase_starts_us={e} now_ms={r.s['now_ms']}")
