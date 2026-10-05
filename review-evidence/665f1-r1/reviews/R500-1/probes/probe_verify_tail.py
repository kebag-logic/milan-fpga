#!/usr/bin/env python3
# R500-1 probe V: what the surviving defect "verify_skips_last_stretch" does.
# The last page program of a change commit is dropped by the device (the
# flash model's program-drop fault, skipping every earlier page). The reviewed
# store must refuse that container (VD_VERIFY) and retry; the planted store
# moves the authority to a slot that cannot boot, and the next boot falls back.
from __future__ import annotations

import sys

from probe_mutants import MUTANTS
from r500_common import bench, planted_tree

STEM = sys.argv[1] if len(sys.argv) > 1 else "endstation_ax7101_1x1_tdm8"
for label, tree in (("reviewed", None),
                    ("verify_skips_last_stretch",
                     planted_tree("vt_mut", MUTANTS["verify_skips_last_stretch"]))):
    b = bench(STEM, f"vt_{label}", tree) if tree else bench(STEM, "vt_reviewed")
    golden = b.file("g.bin", b.assemble(b.frames, 5))
    pages = -(-len(b.assemble(b.frames, 0)) // 256)
    rid = max(b.frames)
    plen = len(b.frames[rid]) - 8
    new = bytes((rid * 13 + j * 11 + 8) & 0xFF for j in range(plen)).hex()
    r = b.run("--slot-b", golden, "--boot", "--fault", f"program-drop:1:{pages - 1}",
              "--set", f"{rid}:{new}", "--run-ms", "1500", "--dump-slot-a", "a.bin",
              "--dump-slot-b", "b.bin")
    w = b.run("--slot-a", str(b.work / "a.bin"), "--slot-b", str(b.work / "b.bin"), "--boot")
    print(f"{label}: commit ok={r.s['ok']} failed={r.s['failed']} auth={r.s['auth']} "
          f"seq={r.s['seq']} pending={r.s['pending']} | next boot vd_a={w.s['vd_a']} "
          f"vd_b={w.s['vd_b']} auth={w.s['auth']} seq={w.s['seq']}")
