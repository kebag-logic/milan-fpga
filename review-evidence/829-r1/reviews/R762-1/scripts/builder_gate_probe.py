#!/usr/bin/env python3
"""Run only the builder gates this PR touches, then cut the observer's ready wire.
usage: builder_gate_probe.py <clone>"""
import sys
root = sys.argv[1]
sys.path.insert(0, root + "/sw/builder")
import test_builder as tb
from pathlib import Path
soc = (Path(root) / "sw/litex/milan_soc.py").read_text()
tb.test_gptp_launch_shape_follows_the_phy()
tb._gptp_observer_reads_the_mac_stream(soc)
print("gate 1d on the head source: held")
tb.test_reboot_egress_statement()
tb.test_reboot_egress_statement_gate_bites()
print("reboot statement gates: held")
cut = soc.replace("            i_gmii_tready_i = self.phy.sink.ready,\n", "            i_gmii_tready_i = 1,\n")
assert cut != soc
try:
    tb._gptp_observer_reads_the_mac_stream(cut)
    print("gate 1d ACCEPTED a tied ready")
except AssertionError as err:
    print("gate 1d refused a tied ready:", str(err)[:100])
for name, shape in (("configs/endstation_ax7101_1x1.yaml", None), ("configs/endstation_arty_current.yaml", None)):
    p = Path(root) / name
    if p.exists():
        import endstation_builder as eb
        cfg = eb.load_config(str(p)) if hasattr(eb, "load_config") else None
        if cfg is not None:
            print(name, {k: v for k, v in eb.datapath_params(cfg).items() if k.startswith(("GPTP_", "REBOOT_"))})
