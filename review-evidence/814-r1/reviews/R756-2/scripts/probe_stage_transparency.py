#!/usr/bin/env python3
"""Probe: the shipping AXIReadyStage and SPIPHYStage under random valid/ready.

For each stage, a random source offers beats (holding VALID and payload until
the handshake, as AXI and LiteX streams require) and a random sink stalls
READY. Graded per channel:
  - the beats out equal the beats in, in order (no drop, duplicate or reorder);
  - the stage's own output keeps VALID and payload until its handshake;
  - SPIPHYStage only: the PHY-side chip select is the core's, one cycle later.
A planted lossy registered-ready stage must fail the first check (the probe can
go red).

Usage: python3 probe_stage_transparency.py <repo>/sw/litex [cycles]
"""
import random
import sys

sys.path.insert(0, sys.argv[1])
import milan_soc  # noqa: E402
from migen import Module, Signal, run_simulation  # noqa: E402
from litex.soc.interconnect import axi, stream  # noqa: E402
from litespi.common import spi_core2phy_layout, spi_phy2core_layout  # noqa: E402

CYCLES = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
problems = []


def check(ok, what):
    print(f"  [{'ok  ' if ok else 'FAIL'}] {what}")
    if not ok:
        problems.append(what)


class LossyReady(Module):
    """Planted defect: READY registered from the last stall, payload combinational."""

    def __init__(self, layout):
        self.sink, self.source = stream.Endpoint(layout), stream.Endpoint(layout)
        stall = Signal()
        self.sync += stall.eq(self.source.valid & ~self.source.ready)
        self.comb += [self.sink.connect(self.source, omit={"ready"}), self.sink.ready.eq(~stall)]


class LossyAXIStage(Module):
    def __init__(self, master, slave):
        for name in ("aw", "ar"):
            pipe = LossyReady(getattr(master, name).description)
            setattr(self.submodules, f"{name}_pipe", pipe)
            self.comb += [getattr(master, name).connect(pipe.sink), pipe.source.connect(getattr(slave, name))]
        self.comb += master.w.connect(slave.w)
        for name in ("b", "r"):
            self.comb += getattr(slave, name).connect(getattr(master, name))


def producer(ep, field, values, rng, p_valid, log):
    """Offer each value, holding VALID and payload until READY; give up after CYCLES cycles."""
    budget = CYCLES - 10
    for v in values:
        while rng.random() > p_valid and budget > 0:
            budget -= 1
            yield
        yield ep.valid.eq(1)
        yield getattr(ep, field).eq(v)
        yield
        budget -= 1
        while not (yield ep.ready) and budget > 0:
            budget -= 1
            yield
        if budget <= 0:
            break
        log.append(v)
        yield ep.valid.eq(0)
    yield ep.valid.eq(0)
    yield


def consumer(ep, field, rng, p_ready, log, violations):
    """Drive READY at random; each cycle sample valid, ready and payload of that same cycle."""
    held = None
    for _ in range(CYCLES):
        v, r, d = (yield ep.valid), (yield ep.ready), (yield getattr(ep, field))
        if held is not None and (not v or d != held):
            violations.append(("dropped-valid-or-payload-changed", held, v, d))
        if v and r:
            log.append(d)
            held = None
        elif v:
            held = d
        else:
            held = None
        yield ep.ready.eq(int(rng.random() < p_ready))
        yield


def run_axi(stage_cls, seed):
    rng = random.Random(seed)
    m = axi.AXIInterface(data_width=256, address_width=32, id_width=8, version="axi4")
    s = axi.AXIInterface(data_width=256, address_width=32, id_width=8, version="axi4")
    dut = stage_cls(m, s)
    res = {}
    gens = []
    for ch in ("aw", "ar", "w"):
        field = "addr" if ch != "w" else "data"
        vals = [rng.getrandbits(32) for _ in range(300)]
        sent, got, viol = [], [], []
        res[ch] = (vals, sent, got, viol)
        gens += [producer(getattr(m, ch), field, vals, random.Random(seed + hash(ch) % 97), 0.7, sent),
                 consumer(getattr(s, ch), field, random.Random(seed * 7 + len(ch)), 0.45, got, viol)]
    for ch in ("b", "r"):
        getattr(m, ch).ready.reset = 1
    run_simulation(dut, gens)
    return res


def run_spi(stage_cls, seed):
    rng = random.Random(seed)

    class Phy(Module):
        def __init__(self):
            self.sink = stream.Endpoint(spi_core2phy_layout)
            self.source = stream.Endpoint(spi_phy2core_layout)
            self.cs = Signal()

    phy = Phy()
    stage = stage_cls(phy)
    top = Module()
    top.submodules.phy, top.submodules.stage = phy, stage
    res = {}
    tx_vals = [rng.getrandbits(32) for _ in range(300)]
    rx_vals = [rng.getrandbits(32) for _ in range(300)]
    tx = (tx_vals, [], [], [])
    rx = (rx_vals, [], [], [])
    res["tx"], res["rx"] = tx, rx
    cs_core, cs_phy = [], []

    def cs_drive():
        r = random.Random(seed + 5)
        for _ in range(CYCLES):
            v = int(r.random() < 0.6)
            yield stage.cs.eq(v)
            yield
            cs_core.append(v)
            cs_phy.append((yield stage.phy_cs))

    gens = [producer(stage.sink, "data", tx_vals, random.Random(seed + 1), 0.7, tx[1]),
            consumer(stage.phy_sink, "data", random.Random(seed + 2), 0.45, tx[2], tx[3]),
            producer(stage.phy_source, "data", rx_vals, random.Random(seed + 3), 0.7, rx[1]),
            consumer(stage.source, "data", random.Random(seed + 4), 0.45, rx[2], rx[3]),
            cs_drive()]
    run_simulation(top, gens)
    res["cs"] = (cs_core, cs_phy)
    return res


def grade(name, res):
    for ch, (vals, sent, got, viol) in ((k, v) for k, v in res.items() if k != "cs"):
        n = min(len(sent), len(got))
        check(len(sent) > 150 and got == sent[:len(got)] and len(sent) - len(got) <= 2 and sent == vals[:len(sent)],
              f"{name} {ch}: {len(sent)} beats in, {len(got)} out, in order, none lost or duplicated")
        check(not viol, f"{name} {ch}: output VALID and payload held until the handshake ({len(viol)} violations)")
    if "cs" in res:
        core, phy = res["cs"]
        check(phy[1:] == core[:-1], f"{name} cs: PHY chip select is the core's one cycle later over {len(core)} cycles")


for seed in (1, 2, 3):
    print(f"seed {seed}")
    grade("AXIReadyStage", run_axi(milan_soc.AXIReadyStage, seed))
    grade("SPIPHYStage", run_spi(milan_soc.SPIPHYStage, seed))

print("planted lossy registered-ready stage (must FAIL):")
before = len(problems)
grade("LossyAXIStage", run_axi(LossyAXIStage, 1))
planted = len(problems) - before
del problems[before:]
check(planted > 0, f"the planted lossy stage fails the probe ({planted} failures)")
print(f"RESULT: {'PASS' if not problems else 'FAIL'} ({len(problems)} problems)")
sys.exit(1 if problems else 0)
