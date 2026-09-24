#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Feed every command the RTL probe sent to the offline model and compare the
model's frame with the frame the pinned RTL emitted, byte for byte.

usage: r280_rtl_vs_model.py <milan-fpga checkout> <rtl_probe_run.txt>
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tests" / "steps"))
import aecp_engine_model as m  # noqa: E402
from aecp_engine_steps import SERVED, SERVED_MVU  # noqa: E402

EID = 0x123456789ABCDEF0          # tb/pp_top/sim_main.cpp
OWN_MAC = bytes.fromhex("0a0b0c0d0e0f")

cmds, gots = {}, {}
for line in Path(sys.argv[2]).read_text(encoding="utf-8").splitlines():
    parts = line.split()
    if len(parts) == 4 and parts[0] == "R280":
        (cmds if parts[1] == "CMD" else gots)[parts[2]] = bytes.fromhex(parts[3])
assert cmds and cmds.keys() == gots.keys(), "probe log incomplete"

bad = 0
for name, cmd in cmds.items():
    model = m.AecpEngineModel(SERVED, m.DescriptorImage(), entity_id=EID,
                              own_mac=OWN_MAC, mvu_served=SERVED_MVU)
    want = model.deliver(cmd)
    ok = want == gots[name]
    r = m.decode(gots[name])
    print("%-4s %-30s rtl status %d cdl %d" % ("OK" if ok else "FAIL", name,
                                              r["status"],
                                              r["control_data_length"]))
    if not ok:
        bad += 1
        print("     rtl   %s\n     model %s" % (gots[name].hex(),
                                                want.hex() if want else None))
print("%d cases, %d model/RTL mismatches" % (len(cmds), bad))
sys.exit(1 if bad else 0)
