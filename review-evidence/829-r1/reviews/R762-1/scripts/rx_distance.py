#!/usr/bin/env python3
"""Independent receive-distance measurement over the product's own objects.
usage: rx_distance.py <repo/sw/litex> <sys_ns> <phases>
Own stimulus (different frame, phases and watcher from the author's receipt):
from the eth_rx edge sampling frame octet 0's first symbol at the pads to the
first macsys edge with core.source.valid, and the first macdp edge with the
crossing's output valid (the edge the plane stamps). Time unit 0.25 ns."""
import random, statistics, sys, zlib
sys.path.insert(0, sys.argv[1])
import gen_mac_tx_model as model
import milan_soc
from migen.sim.core import Simulator
SYS_NS, PHASES = float(sys.argv[2]), int(sys.argv[3])
U = 0.25
records = []
real_record = model.Record
def spy(*a, **k):
    r = real_record(*a, **k); records.append(r); return r
model.Record = spy
rng = random.Random(829)
def once(shape, eth_ns, sys_ph, dp_ph, eth_ph, payload_len):
    records.clear()
    dut = model.build_chain(shape)
    pads = records[-1]
    rx = milan_soc._axis_dp_cdc(dut, "mac_rx_cdc", [("data", 64), ("keep", 8)], "macdp", to_datapath=True,
                                rename=milan_soc._mac_cdc_rename("macdp"))
    milan_soc._payload_in_block_ram(dut.mac_rx_cdc)
    core = dut.core
    dut.comb += [rx.sys.valid.eq(core.source.valid), rx.sys.data.eq(core.source.data),
                 rx.sys.last.eq(core.source.last), rx.dp.ready.eq(1)]
    body = bytes([0x01,0x80,0xC2,0,0,0x0E,0xAA,0xBB,0xCC,0xDD,0xEE,0x01,0x88,0xF7]) + bytes(rng.randrange(256) for _ in range(payload_len))
    fcs = zlib.crc32(body).to_bytes(4, "little")
    wire = bytes([0x55]*7+[0xD5]) + body + fcs
    syms = [s for b in wire for s in ((b & 15, b >> 4) if shape == "mii" else (b,))]
    ref = 16 if shape == "mii" else 8
    t = [0]; seen = {}
    def rx_drive():
        yield dut.eth_phy_rst.eq(1); yield dut.sys_rst.eq(1); yield dut.dp_rst.eq(1)
        for _ in range(40): yield
        yield dut.eth_phy_rst.eq(0); yield dut.sys_rst.eq(0); yield dut.dp_rst.eq(0)
        for _ in range(120): yield
        for i, s in enumerate(syms):
            yield pads.rx_dv.eq(1); yield pads.rx_data.eq(s)
            yield
            if i == ref: seen["ref"] = t[0]
        yield pads.rx_dv.eq(0)
        for _ in range(60): yield
    def watch(signal, key, cycles):
        for _ in range(cycles):
            if (yield signal) and key not in seen: seen[key] = t[0]
            yield
    span_ns = (len(syms) + 240) * eth_ns + 3000
    gens = {"eth_rx": rx_drive(), "macsys": watch(core.source.valid, "core", int(span_ns/SYS_NS)),
            "macdp": watch(rx.dp.valid, "dp", int(span_ns/20))}
    sys_u, dp_u, eth_u = int(SYS_NS/U), int(20/U), int(eth_ns/U)
    clocks = {"macsys": (sys_u, sys_ph % sys_u), "macdp": (dp_u, dp_ph % dp_u), "maceth_tx": (eth_u, eth_ph % eth_u),
              "maceth_rx": (eth_u, eth_ph % eth_u), "eth_tx": (eth_u, eth_ph % eth_u), "eth_rx": (eth_u, eth_ph % eth_u)}
    with Simulator(dut, gens, clocks) as sim:
        inner = sim.time.tick
        def tick():
            r = inner(); t[0] += r[0]; return r
        sim.time.tick = tick
        sim.run()
    return (seen["core"]-seen["ref"])*U, (seen["dp"]-seen["ref"])*U
for shape, eth_ns in (("mii", 40), ("gmii", 8)):
    pts = [once(shape, eth_ns, rng.randrange(200), rng.randrange(200), 0, rng.choice((46, 58, 100))) for _ in range(PHASES)]
    for name, idx in (("core.source", 0), ("plane stamp edge", 1)):
        v = [p[idx] for p in pts]
        print(f"{shape:5} sys={SYS_NS} ns {name:17} mean {statistics.mean(v):8.2f} min {min(v):8.2f} max {max(v):8.2f} n={len(v)}")
