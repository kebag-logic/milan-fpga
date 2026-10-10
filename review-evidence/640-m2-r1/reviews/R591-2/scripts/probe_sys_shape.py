#!/usr/bin/env python3
"""Feature-off shape: milan_cd == "sys" builds no crossing and touches no storage.
Usage: pinned_py.sh probe_sys_shape.py <sw/litex dir>"""
import sys
sys.path.insert(0, sys.argv[1])
import milan_soc
from migen import Module
from litex.soc.interconnect import axi
mac = milan_soc.MilanMAC(milan_soc.alinx_ax7101.Platform(), data_width=64, milan_cd="sys")
print("MilanMAC(sys) has mac_tx_cdc:", hasattr(mac, "mac_tx_cdc"), "mac_rx_cdc:", hasattr(mac, "mac_rx_cdc"))
host = Module(); axil = axi.AXILiteInterface(data_width=32, address_width=32)
out = milan_soc._cross_csr_bus(host, axil, "sys")
print("_cross_csr_bus(sys) returns the same interface:", out is axil, "adds milan_axil_cdc:", hasattr(host, "milan_axil_cdc"))
# refusal: a crossing whose storage is not payload+params+2 flags must be refused
from litex.soc.interconnect import stream
bad = stream.ClockDomainCrossing([("data", 8)], cd_from="a", cd_to="b", depth=4)
core, storage = milan_soc._crossing_storage(bad)
storage.width += 1
try:
    milan_soc._payload_in_block_ram(bad); print("width guard: NOT refused")
except ValueError as e:
    print("width guard refused:", e)
same = stream.ClockDomainCrossing([("data", 8)], cd_from="a", cd_to="a", depth=4)
try:
    milan_soc._payload_in_block_ram(same); print("same-domain guard: NOT refused")
except ValueError as e:
    print("same-domain guard refused:", e)
