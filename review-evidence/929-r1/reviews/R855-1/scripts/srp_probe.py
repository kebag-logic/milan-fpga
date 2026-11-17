#!/usr/bin/env python3
"""srp_probe.py <tree-root> <out> <interfaces> <name> ...: srp_mutants.campaign over the named defects, from the
tree's own table or this reviewer's probes (names starting "r855-"); prints [ok]/[ESCAPED] per defect; rc 1 when any
escaped. An expected escape is the caller's to read."""
import sys
from pathlib import Path
root, out, n = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import srp_mutants  # noqa: E402
D = srp_mutants.Defect
E8 = "endstation_ax7101_8x8"
T = "StartupDeclaresTalkersDomainAndVlan"
PROBES = (
    # an unallocated source past the 1x1 entity's two declared as Talker Advertise
    D("r855-source5-advertised", T, "bool admitted = i->sources[n].allocated &&",
      "bool admitted = (i->sources[n].allocated || n == 5u) &&", "source 5 on interface", entity=E8),
    # the last source of the 8x8 entity never declared
    D("r855-last-source-undeclared", T, "const bool valid = (i->gate & bit) != 0u;",
      "const bool valid = (i->gate & bit) != 0u && n + 1u < CTRL_SRP_SOURCES;", "declares New, New, JoinMt",
      entity=E8),
    # sources past two declared on the wrong VLAN
    D("r855-vid-past-two", T, "value.talker.vlan_id = i->domain.vid;",
      "value.talker.vlan_id = n >= 2u ? 3u : i->domain.vid;", "wire_be16(d.value.data()+14)", entity=E8),
    # the second interface's sources past two carry failure code 1
    D("r855-if1-code-past-two", T, "value.failure_info[8] = i->sources[n].allocated ? 1 : 2;",
      "value.failure_info[8] = i->sources[n].allocated || (n >= 2u && i->index == 1u) ? 1 : 2;",
      "failure code", entity=E8),
)
table = {d.name: d for d in (*srp_mutants.DEFECTS, *PROBES)}
missing = [x for x in sys.argv[4:] if x not in table]
assert not missing, missing
srp_mutants.DEFECTS = tuple(table[x] for x in sys.argv[4:])
sys.exit(1 if srp_mutants.campaign(out, root / "third_party/lwSRP", 4, n) else 0)
