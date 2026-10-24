"""Probe: what the parent's offline behave AECP model answers for GET_AVB_INFO.

Usage: python3 -P probe_behave_model_gavb.py <repo>
Sends the sweep's own command shape (build_aem_command default operands,
descriptor_type ENTITY at @24, cdl 20) plus AVB_INTERFACE 0 and CLOCK_DOMAIN 0
at cdl 16, and prints the status the model returns and the status the sweep
partition step expects for opcode 0x0027.
"""
import struct, sys, pathlib
repo = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "tests" / "steps"))
import aecp_engine_model as m
import aecp_engine_steps as s
eng = m.AecpEngineModel(s.SERVED, m.DescriptorImage(), mvu_served=s.SERVED_MVU)
def status(rsp):
    return (rsp[m.ETH_HDR + 2] >> 3) & 0x1F if rsp else None
def cdl(rsp):
    p = rsp[m.ETH_HDR:]
    return ((p[2] & 7) << 8) | p[3]
cases = [
    ("sweep shape (ENTITY at @24, cdl 20)", m.build_aem_command(0x0027)),
    ("AVB_INTERFACE 0 (0x0009), cdl 16", m.build_aem_command(0x0027, struct.pack(">HH", 0x0009, 0))),
    ("CLOCK_DOMAIN 0 (0x0024), cdl 16", m.build_aem_command(0x0027, struct.pack(">HH", 0x0024, 0))),
]
for name, cmd in cases:
    r = eng.deliver(cmd)
    print("GET_AVB_INFO %-40s model status=%s cdl=%s" % (name, status(r), cdl(r) if r else None))
print("sweep partition expects status", s.SERVED[0x0027]["verdict"], "for opcode 0x0027")
