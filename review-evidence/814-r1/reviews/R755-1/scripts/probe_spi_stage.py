#!/usr/bin/env python3
"""Reviewer probe: SPIPHYStage under stalls, and whether the real PHY stalls it.

Usage: probe_spi_stage.py <repo-root> standalone|realphy

standalone: the shipping SPIPHYStage in front of a stand-in PHY face. The core
  side sends commands (VALID held until accepted, payload stable) while the PHY
  side takes them with a random READY; the PHY side returns responses with a
  random VALID while the core side takes them with a random READY. Checks: no
  command or response is dropped, duplicated or reordered; the PHY's cs equals
  the core's cs one cycle earlier, every cycle; both skid registers fill.
realphy: the gate's own FlashSoC with the real LiteSPI PHY on the board pads
  (as its structural arm builds it), driven with the gate's own read pattern;
  counts the cycles the stage's tx and rx skid registers are full. A non-zero
  tx count shows the stall path is reached on the shipping PHY (its chip-select
  delay holds the first command of a new burst), which the gate's behaviour
  arms, on LiteSPI's model PHY, never reach.
"""
import random
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
arm = sys.argv[2]
sys.path.insert(0, str(root / "sw" / "litex"))

from migen import Module, Signal, run_simulation  # noqa: E402
from migen.sim import passive  # noqa: E402
from litex.soc.interconnect import stream  # noqa: E402
from litespi.common import spi_core2phy_layout, spi_phy2core_layout  # noqa: E402
import milan_soc  # noqa: E402

if arm == "standalone":
    class FakePHY(Module):
        def __init__(self):
            self.sink = stream.Endpoint(spi_core2phy_layout)
            self.source = stream.Endpoint(spi_phy2core_layout)
            self.cs = Signal()

    class Top(Module):
        def __init__(self):
            self.submodules.phy = phy = FakePHY()
            self.phy_sink, self.phy_source, self.phy_cs = phy.sink, phy.source, phy.cs
            milan_soc.stage_spi_phy(phy)
            self.core_sink, self.core_source, self.core_cs = phy.sink, phy.source, phy.cs

    random.seed(814)
    top = Top()
    N = 300
    cmd_sent, cmd_got, rsp_sent, rsp_got, cs_bad, full = [], [], [], [], [], {"tx": 0, "rx": 0}

    def core_tx():
        for i in range(N):
            for _ in range(random.choice([0, 0, 1, 3])):
                yield top.core_sink.valid.eq(0)
                yield
            v = random.getrandbits(32)
            yield top.core_sink.data.eq(v)
            yield top.core_sink.len.eq(i & 0x1F)
            yield top.core_sink.valid.eq(1)
            yield
            while not (yield top.core_sink.ready):
                yield
            cmd_sent.append(v)
        yield top.core_sink.valid.eq(0)

    def phy_rx():
        for _ in range(N * 8):
            yield top.phy_sink.ready.eq(int(random.random() < 0.4))
            yield
            if (yield top.phy_sink.valid) and (yield top.phy_sink.ready):
                cmd_got.append((yield top.phy_sink.data))

    def phy_tx():
        for i in range(N):
            for _ in range(random.choice([0, 0, 2])):
                yield top.phy_source.valid.eq(0)
                yield
            v = random.getrandbits(32)
            yield top.phy_source.data.eq(v)
            yield top.phy_source.valid.eq(1)
            yield
            while not (yield top.phy_source.ready):
                yield
            rsp_sent.append(v)
        yield top.phy_source.valid.eq(0)

    def core_rx():
        for _ in range(N * 8):
            yield top.core_source.ready.eq(int(random.random() < 0.4))
            yield
            if (yield top.core_source.valid) and (yield top.core_source.ready):
                rsp_got.append((yield top.core_source.data))

    @passive
    def cs_watch():
        prev = 0
        while True:
            yield top.core_cs.eq(int(random.random() < 0.5))
            yield
            now_phy = yield top.phy_cs
            if now_phy != prev:
                cs_bad.append(1)
            prev = yield top.core_cs
            stage = top.phy.stage
            full["tx"] += 1 - (yield stage.tx.pipe_ready.sink.ready)
            full["rx"] += 1 - (yield stage.rx.pipe_ready.sink.ready)

    run_simulation(top, [core_tx(), phy_rx(), phy_tx(), core_rx(), cs_watch()])
    ok = cmd_got == cmd_sent and rsp_got == rsp_sent and not cs_bad and full["tx"] > 0 and full["rx"] > 0
    print(f"  commands: sent {len(cmd_sent)}, PHY took {len(cmd_got)}, identical order {cmd_got == cmd_sent}")
    print(f"  responses: sent {len(rsp_sent)}, core took {len(rsp_got)}, identical order {rsp_got == rsp_sent}")
    print(f"  cycles PHY cs != core cs one cycle earlier: {len(cs_bad)}")
    print(f"  cycles skid register full: {full}")
    print(f"PROBE standalone: {'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)

import test_soc_timing_cuts as gate  # noqa: E402
soc = gate.build(gate.FlashSoC, None)
stage = soc.spiflash.phy.stage
full = {"tx": 0, "rx": 0, "tx_handshakes": 0}
addresses = [0, 1, 2, 3, 17, 18, 40, 9, 10, 11, 63, 62]


def master():
    axil = soc.axil
    yield axil.r.ready.eq(1)
    for _ in range(4):
        yield
    for index in addresses:
        yield axil.ar.addr.eq(gate.FLASH_ORIGIN + 4 * index)
        yield axil.ar.valid.eq(1)
        yield
        while not (yield axil.ar.ready):
            yield
        yield axil.ar.valid.eq(0)
        n = 0
        while not (yield axil.r.valid):
            yield
            n += 1
            if n > 20000:
                print("  read timed out")
                return
        yield


@passive
def watch():
    while True:
        full["tx"] += 1 - (yield stage.tx.pipe_ready.sink.ready)
        full["rx"] += 1 - (yield stage.rx.pipe_ready.sink.ready)
        if (yield stage.phy_sink.valid) and (yield stage.phy_sink.ready):
            full["tx_handshakes"] += 1
        yield


run_simulation(soc, [master(), watch()])
print(f"  real PHY, the gate's read pattern: cycles skid register full {full}")
print(f"PROBE realphy: {'STALL PATH REACHED' if full['tx'] or full['rx'] else 'STALL PATH NOT REACHED'}")
