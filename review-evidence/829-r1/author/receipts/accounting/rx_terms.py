#!/usr/bin/env python3
"""Scratch: receive chain term by term through the product's own objects, MII and GMII: the sampling edge of frame octet 0's
first symbol at the pads, to the first valid at each pipeline stage, to the first beat out of the product's mac_rx_cdc in the
datapath domain (the edge the plane stamps). Time unit 0.25 ns. usage: rx_terms.py <sys_mhz> [phases]"""
import sys, statistics
sys.path.insert(0, sys.argv[3] if len(sys.argv) > 3 else "$LANES/583-arty/sw/litex")
import gen_mac_tx_model as model
import milan_soc
from migen.sim.core import Simulator
captured = []
orig = model.Record
def rec(*a, **k):
    r = orig(*a, **k); captured.append(r); return r
model.Record = rec

def crc32(data):
    c = 0xFFFFFFFF
    for b in data:
        c ^= b
        for _ in range(8):
            c = (c >> 1) ^ (0xEDB88320 if c & 1 else 0)
    return (~c) & 0xFFFFFFFF

sys_mhz = float(sys.argv[1]); nph = int(sys.argv[2]) if len(sys.argv) > 2 else 6
U = 0.25
def run(shape, eth_ns, dp_ns, sys_ns, ph_sys, ph_dp, ph_eth):
    captured.clear()
    dut = model.build_chain(shape)
    pads = captured[-1]
    layout = [("data", 64), ("keep", 8)]
    rx_dp = milan_soc._axis_dp_cdc(dut, "mac_rx_cdc", layout, "macdp", to_datapath=True, rename=milan_soc._mac_cdc_rename("macdp"))
    milan_soc._payload_in_block_ram(dut.mac_rx_cdc)
    core = dut.core
    dut.comb += [rx_dp.sys.valid.eq(core.source.valid), rx_dp.sys.data.eq(core.source.data), rx_dp.sys.last.eq(core.source.last), rx_dp.dp.ready.eq(1)]
    pl = core.rx_datapath.pipeline
    stages = []
    for i, s in enumerate(pl):
        ep = getattr(s, "source", s if hasattr(s, "valid") else None)
        if ep is not None and hasattr(ep, "valid"):
            stages.append((f"{i}:{type(s).__name__}", ep))
    stages.append(("dp", rx_dp.dp))
    body = bytes([0x01,0x80,0xC2,0,0,0x0E, 0x02,0,0,0,0,2, 0x88,0xF7]) + bytes(range(0x10, 0x10+58))
    frame = bytes([0x55]*7 + [0xD5]) + body + crc32(body).to_bytes(4, "little")
    syms = [x for b in frame for x in ((b & 0xF, b >> 4) if shape == "mii" else (b,))]
    per = 2 if shape == "mii" else 1
    ref_idx = 8 * per
    log = {}
    sim_box = [None]
    cur = [0]
    def now():
        return cur[0]
    def drive():
        yield dut.eth_phy_rst.eq(1); yield dut.sys_rst.eq(1); yield dut.dp_rst.eq(1)
        for _ in range(30): yield
        yield dut.eth_phy_rst.eq(0); yield dut.sys_rst.eq(0); yield dut.dp_rst.eq(0)
        for _ in range(80): yield
        for i, s in enumerate(syms):
            yield pads.rx_dv.eq(1); yield pads.rx_data.eq(s)
            yield
            # this edge samples symbol i into the PHY stage's first register
            if i == ref_idx: log["ref"] = now()
        yield pads.rx_dv.eq(0)
        for _ in range(100): yield
    def watcher(names, n):
        for _ in range(n):
            for name, ep in stages:
                if name in names:
                    v = (yield ep.valid)
                    k = f"first:{name}"
                    if v and k not in log:
                        log[k] = now()
            yield
    dur_ns = len(syms) * eth_ns + 2600 + 110*eth_ns
    gens = {"eth_rx": drive(),
            "macdp": watcher(["dp"], int(dur_ns/dp_ns)),
            "macsys": watcher([n for n, _ in stages if n != "dp"], int(dur_ns/sys_ns))}
    clocks = {"macdp": (int(dp_ns/U), ph_dp), "macsys": (int(sys_ns/U), ph_sys), "maceth_tx": (int(eth_ns/U), ph_eth), "maceth_rx": (int(eth_ns/U), ph_eth), "eth_tx": (int(eth_ns/U), ph_eth), "eth_rx": (int(eth_ns/U), ph_eth)}
    with Simulator(dut, gens, clocks) as s:
        sim_box[0] = s
        orig_tick = s.time.tick
        def tick():
            r = orig_tick(); cur[0] += r[0]; return r
        s.time.tick = tick
        s.run()
    return log, stages

for shape, eth_ns, in (("mii", 40), ("gmii", 8)):
    sys_ns = 1000.0 / sys_mhz
    sys_u = int(round(sys_ns/U)); sys_u += sys_u % 2; dp_u = 80; eth_u = int(eth_ns/U)
    res = {}
    for k in range(nph):
        log, stages = run(shape, eth_ns, 20.0, sys_u*U, (k*17) % sys_u, (k*29) % dp_u, 0)
        ref = log["ref"]
        for name, _ in stages:
            res.setdefault(name, []).append((log.get(f"first:{name}", 0) - ref) * U)
    print(f"== {shape} eth={eth_ns} ns sys={sys_u*U} ns dp=20 ns, {nph} phases; time from the sampling edge of frame octet 0 first symbol (ns)")
    for name, _ in stages:
        v = res[name]
        print(f"  {name:42} min {min(v):8.2f} mean {statistics.mean(v):8.2f} max {max(v):8.2f}")
