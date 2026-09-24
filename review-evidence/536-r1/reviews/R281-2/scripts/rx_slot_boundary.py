#!/usr/bin/env python3
"""Is the RTL's silence for an over-slot AECPDU MVU-specific or general?

Sends, through the same tb/pp_top probe, GET_MILAN_INFO and an unserved AEM
command (DECREMENT_CONTROL 0x001B, NOT_IMPLEMENTED) at the RX slot boundary:
AVTPDU 576 octets (cdl 564) and 577 octets (cdl 565), and cdl 600.  Reports
the RTL and the head model answer for each.  The model can be run from a
base-commit tree too (--repo), to show the gap predates the PR.

Usage: rx_slot_boundary.py --repo <tree> --sim <probe dir> --out <receipt>
"""
import argparse
import os
import struct
import subprocess
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--repo", required=True)
ap.add_argument("--sim", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()
sys.path.insert(0, str(Path(args.repo).resolve() / "tests" / "steps"))
import aecp_engine_model as M   # noqa: E402

PP_OWN_MAC = bytes.fromhex("0A0B0C0D0E0F")
PP_EID = 0x123456789ABCDEF0
PP_CTLR_MAC = bytes.fromhex("0202DEADBEEF")
PP_CTLR_EID = 0x7777000000000042
env = dict(target_eid=PP_EID, ctlr_eid=PP_CTLR_EID, src_mac=PP_CTLR_MAC,
           dst_mac=PP_OWN_MAC)

cases = []
for cdl in (564, 565, 600):
    fill = bytes(i & 0xFF for i in range(cdl - 12))
    aem = M.build_command(M.MT_AEM_COMMAND, 0x001B, fill, seq=0xE000 + cdl,
                          **env)
    cases.append(("AEM DECREMENT_CONTROL cdl%d" % cdl, aem))
    if hasattr(M, "MVU_COMMAND_FORMS"):
        mvu = M.build_mvu_command(0, from_32=fill[8:], seq=0xE100 + cdl, **env)
        cases.append(("MVU GET_MILAN_INFO cdl%d" % cdl, mvu))

work = Path(args.out).resolve().parent.parent / "scratch"
pin, pout = work / "slot_in.txt", work / "slot_out.txt"
pin.write_text("\n".join(f.hex() for _, f in cases) + "\n")
subprocess.run(["./obj_dir/Vpp_top_sim"], cwd=args.sim, check=True,
               env=dict(os.environ, PROBE_IN=str(pin), PROBE_OUT=str(pout)),
               capture_output=True, timeout=3000)
rtl = [l.split() for l in pout.read_text().splitlines()]
out = ["model tree: %s" % args.repo]
for (label, f), r in zip(cases, rtl):
    kw = {}
    if "mvu_served" in M.AecpEngineModel.__init__.__code__.co_varnames:
        import aecp_engine_steps as S
        kw["mvu_served"] = S.SERVED_MVU
    from aecp_engine_steps import SERVED
    m = M.AecpEngineModel(SERVED, M.DescriptorImage(), entity_id=PP_EID,
                          own_mac=PP_OWN_MAC, **kw).deliver(f)
    def d(b):
        return "SILENCE" if b is None else "status %d cdl %d" % (
            b[16] >> 3, ((b[16] & 7) << 8) | b[17])
    rb = None if r[1] == "SILENCE" else bytes.fromhex(r[1])
    out.append("%s | AVTPDU %d | RTL %s %s | model %s" % (
        label, len(f) - 14 if len(f) > 60 else 46, d(rb), r[2], d(m)))
Path(args.out).write_text("\n".join(out) + "\n")
print("\n".join(out))
