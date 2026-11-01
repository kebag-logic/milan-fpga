#!/usr/bin/env python3
"""Independent receive-distance probe through the product's own objects.

Times the first valid beat at core.source and at mac_rx_cdc's datapath side from
the eth_rx edge that samples frame octet 0's first symbol at the pads. The time
base is a free-running counter in its own fast clock domain, so no simulator
internals are patched for time.
usage: rx_distance.py <tree> <shape> <eth_ns> <sys_quarter_ns> <phase_index>"""
import json, sys
tree, shape, eth_ns, sys_u, k = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
sys.path.insert(0, tree + "/sw/litex")
import gen_mac_tx_model as model
import milan_soc
from migen import Signal, ClockDomain
from migen.sim.core import Simulator

U = 0.25
records = []
real_record = model.Record
def record_spy(*a, **k_):
    r = real_record(*a, **k_); records.append(r); return r
model.Record = record_spy
dut = model.build_chain(shape)
pads = records[-1]

rx_dp = milan_soc._axis_dp_cdc(dut, "mac_rx_cdc", [("data", 64), ("keep", 8)], "macdp",
                               to_datapath=True, rename=milan_soc._mac_cdc_rename("macdp"))
milan_soc._payload_in_block_ram(dut.mac_rx_cdc)
core = dut.core
dut.comb += [rx_dp.sys.valid.eq(core.source.valid), rx_dp.sys.data.eq(core.source.data),
             rx_dp.sys.last.eq(core.source.last), core.source.ready.eq(rx_dp.sys.ready),
             rx_dp.dp.ready.eq(1)]

# the independent time base: one count per two simulator units
dut.clock_domains.cd_probe = ClockDomain(reset_less=True)
stamp = Signal(32, reset_less=True)
dut.sync.probe += stamp.eq(stamp + 1)

def crc32(data):
    c = 0xFFFFFFFF
    for b in data:
        c ^= b
        for _ in range(8):
            c = (c >> 1) ^ (0xEDB88320 if c & 1 else 0)
    return (~c) & 0xFFFFFFFF

body = bytes([0x01, 0x80, 0xC2, 0, 0, 0x0E, 0x02, 0, 0, 0, 0, 2, 0x88, 0xF7]) + bytes(range(0x10, 0x4A))
frame = bytes([0x55] * 7 + [0xD5]) + body + crc32(body).to_bytes(4, "little")
syms = [x for b in frame for x in ((b & 0xF, b >> 4) if shape == "mii" else (b,))]
ref_index = 8 * (2 if shape == "mii" else 1)
marks, done = {}, []

def drive():
    yield dut.eth_phy_rst.eq(1); yield dut.sys_rst.eq(1); yield dut.dp_rst.eq(1)
    for _ in range(30): yield
    yield dut.eth_phy_rst.eq(0); yield dut.sys_rst.eq(0); yield dut.dp_rst.eq(0)
    for _ in range(80): yield
    for s in syms:
        yield pads.rx_dv.eq(1); yield pads.rx_data.eq(s)
        yield
    yield pads.rx_dv.eq(0)
    for _ in range(100): yield
    done.append(1)

def pad_watch():
    seen = 0
    while not done:
        # a generator reads pre-edge values: rx_dv high here is sampled at this edge
        if (yield pads.rx_dv):
            if seen == ref_index and "ref" not in marks:
                marks["ref"] = (yield stamp)
            seen += 1
        yield

def watch(name, endpoint):
    while not done:
        if name not in marks and (yield endpoint.valid):
            marks[name] = (yield stamp)
        yield

eth_u, dp_u, probe_u = eth_ns * 4, 80, 2
phase_sys, phase_dp = (k * 17) % sys_u, (k * 29) % dp_u
clocks = {"probe": (probe_u, 0), "macdp": (dp_u, phase_dp), "macsys": (sys_u, phase_sys),
          "maceth_tx": (eth_u, 0), "maceth_rx": (eth_u, 0), "eth_tx": (eth_u, 0), "eth_rx": (eth_u, 0)}
gens = {"eth_rx": [drive(), pad_watch()], "macsys": watch("core_source", core.source), "macdp": watch("dp", rx_dp.dp)}
with Simulator(dut, gens, clocks) as s:
    s.run()
print(json.dumps({"shape": shape, "sys_mhz": round(1000 / (sys_u * U), 3), "phase": k,
                  "core_source_ns": (marks["core_source"] - marks["ref"]) * probe_u * U,
                  "dp_ns": (marks["dp"] - marks["ref"]) * probe_u * U}))
