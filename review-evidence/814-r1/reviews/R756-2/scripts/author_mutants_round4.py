#!/usr/bin/env python3
"""mutants_round4.py <repo>/sw/litex <mutant>: does test_soc_timing_cuts.py kill each planted defect?

The mutants the two round-3 reviews describe without a runnable script, and the alternative ZQCS fix the
round-4 ruling names:
  axi_dropheld, spi_tx_dropheld, spi_rx_dropheld: LiteX's PipeReady flag logic kept (READY is the registered
    "not holding"), but the held beat is never presented: the output always shows the input, so the beat taken
    into a stall is lost. aw and ar for the AXI stage; one of the two SPI buffers (behind its PipeValid).
  ref_zqcs_done_delayed: the registered request, and LiteDRAM's ZQCS timer's done pulse delayed one cycle
    instead of its start (right for the first idle ZQCS, one cycle late after the timer re-phases).
Each mutant replaces one shipping class in milan_soc for the named arms of the unchanged test. KILLED when those
arms record a failure (or raise).
"""
import sys

sys.path.insert(0, sys.argv[1])
import milan_soc  # noqa: E402
import test_soc_timing_cuts as t  # noqa: E402
import litedram.core.refresher as refresher_module  # noqa: E402
from litedram.core.refresher import RefreshTimer  # noqa: E402
from litex.soc.interconnect import stream  # noqa: E402
from migen import If, Module, Signal  # noqa: E402
from migen.fhdl.bitcontainer import bits_for  # noqa: E402


class DropHeld(Module):
    """PipeReady's flag and READY, the held copy never presented."""

    def __init__(self, layout):
        self.sink, self.source = stream.Endpoint(layout), stream.Endpoint(layout)
        valid = Signal()
        self.sync += If(self.sink.valid & ~self.source.ready, valid.eq(1)).Elif(self.source.ready, valid.eq(0))
        self.comb += [self.sink.connect(self.source, omit={"ready"}), self.sink.ready.eq(~valid)]


class DropHeldBuffer(Module):
    def __init__(self, layout):
        self.submodules.a = a = stream.PipeValid(layout)
        self.submodules.b = b = DropHeld(layout)
        self.sink, self.source = a.sink, b.source
        self.comb += a.source.connect(b.sink)


class AXIDropHeld(Module):
    def __init__(self, master, slave):
        for name in ("aw", "ar"):
            pipe = DropHeld(getattr(master, name).description)
            setattr(self.submodules, f"{name}_pipe", pipe)
            self.comb += [getattr(master, name).connect(pipe.sink), pipe.source.connect(getattr(slave, name))]
        self.comb += master.w.connect(slave.w)
        for name in ("b", "r"):
            self.comb += getattr(slave, name).connect(getattr(master, name))


def spi_dropheld(which):
    class Stage(Module):
        def __init__(self, phy):
            self.phy_sink, self.phy_source, self.phy_cs = phy.sink, phy.source, phy.cs
            self.sink = stream.Endpoint(phy.sink.description)
            self.source = stream.Endpoint(phy.source.description)
            self.cs = Signal.like(phy.cs)
            tx, rx = (DropHeldBuffer(layout) if name == which else stream.Buffer(layout, pipe_valid=True, pipe_ready=True)
                      for name, layout in (("tx", phy.sink.description), ("rx", phy.source.description)))
            self.submodules.tx, self.submodules.rx = tx, rx
            self.comb += [self.sink.connect(tx.sink), tx.source.connect(phy.sink),
                          phy.source.connect(rx.sink), rx.source.connect(self.source)]
            self.sync += phy.cs.eq(self.cs)
    return Stage


class DoneDelayedTimer(RefreshTimer):
    """RefreshTimer whose `done` output is its count-zero compare one cycle late; it reloads on its own compare."""

    def __init__(self, trefi):
        self.wait, self.done, self.count = Signal(), Signal(), Signal(bits_for(trefi))
        done, count = Signal(), Signal(bits_for(trefi), reset=trefi - 1)
        self.sync += [If(self.wait & ~done, count.eq(count - 1)).Else(count.eq(count.reset)), self.done.eq(done)]
        self.comb += [done.eq(count == 0), self.count.eq(count)]


class DoneDelayed(t.UndelayedZQCSRefresher):
    """The registered request, and LiteDRAM's ZQCS timer built as DoneDelayedTimer."""

    def __init__(self, settings, clk_freq, zqcs_freq=1e0, postponing=1):
        zqcs_cycles = int(clk_freq / zqcs_freq)
        original = refresher_module.RefreshTimer
        refresher_module.RefreshTimer = lambda n: DoneDelayedTimer(n) if n == zqcs_cycles else original(n)
        try:
            t.UndelayedZQCSRefresher.__init__(self, settings, clk_freq, zqcs_freq, postponing)
        finally:
            refresher_module.RefreshTimer = original


MUTANTS = {
    "axi_dropheld": ("AXIReadyStage", AXIDropHeld, ["dram_structure", "dram_behaviour"]),
    "spi_tx_dropheld": ("SPIPHYStage", spi_dropheld("tx"), ["flash_structure", "flash_behaviour"]),
    "spi_rx_dropheld": ("SPIPHYStage", spi_dropheld("rx"), ["flash_structure", "flash_behaviour"]),
    "ref_zqcs_done_delayed": ("RegisteredRefresher", DoneDelayed, ["refresh_structure", "refresh_behaviour"]),
}

name = sys.argv[2]
cls_name, replacement, arms = MUTANTS[name]
shipping = getattr(milan_soc, cls_name)
setattr(milan_soc, cls_name, replacement)
problems = []
try:
    for arm in arms:
        try:
            getattr(t, arm)(problems)
        except Exception as exc:  # an arm that crashes on the mutant has also gone red
            problems.append(f"{arm} raised {type(exc).__name__}: {exc}")
            print(f"  [FAIL] {arm} raised {type(exc).__name__}: {exc}")
finally:
    setattr(milan_soc, cls_name, shipping)
print(f"MUTANT {name}: {'KILLED' if problems else 'SURVIVED'} ({len(problems)} failures: {problems[:3]})")
