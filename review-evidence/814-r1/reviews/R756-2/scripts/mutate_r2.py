#!/usr/bin/env python3
"""Round-2 mutation probe: does test_soc_timing_cuts.py kill each planted defect?

Independent mutants for the round-4 changes (the ZQCS timer hold and the stall arms).
Each replaces one shipping class in milan_soc for the named arms of the test, imported
unchanged from the tree under review. KILLED when those arms record a failure (or raise).

  zqcs_hold2            ZQCS timer held two cycles after reset instead of one.
  zqcs_rephase_extra    one-cycle hold kept, plus a hold on the cycle after every ZQCS end
                        (first ZQCS right, every re-phase one cycle late). A hold on the
                        ZQCS-end cycle itself is LiteDRAM's own reload, so equivalent.
  zqcs_hold_both        one-cycle hold on the refresh timer too (refresh two cycles late).
  ref_last_comb_h, ref_ready_registered_h, ref_no_last_h
                        the round-1 refresher mutants, with the shipping ZQCS hold, so each
                        isolates its own defect from the ZQCS change.
  axi_valid_waits_ready aw/ar VALID offered only while READY (VALID waits on READY).
  spi_tx_valid_waits_ready, spi_rx_valid_waits_ready  the same on one SPI buffer.
  axi_dup               aw/ar skid that presents the held beat, then presents it again.
  spi_rx_dup            the same on the SPI rx buffer.

Usage: python3 mutate_r2.py <repo>/sw/litex <mutant>
"""
import sys

sys.path.insert(0, sys.argv[1])
import milan_soc  # noqa: E402
import test_soc_timing_cuts as t  # noqa: E402
from litedram.core.refresher import Refresher  # noqa: E402
from litex.soc.interconnect import stream  # noqa: E402
from migen import If, Module, ResetInserter, Signal  # noqa: E402


def refresher(hold=1, rephase_extra=False, hold_refresh=False, last="reg", ready="comb"):
    class R(Module):
        def __init__(self, settings, clk_freq, zqcs_freq=1e0, postponing=1):
            self.submodules.refresher = inner = Refresher(settings, clk_freq, zqcs_freq=zqcs_freq,
                                                          postponing=postponing)
            self.cmd = cmd = stream.Endpoint(inner.cmd.description)
            self.sync += cmd.valid.eq(inner.cmd.valid)
            if last == "reg":
                self.sync += cmd.last.eq(inner.cmd.last)
            elif last == "comb":
                self.comb += cmd.last.eq(inner.cmd.last)
            self.comb += inner.cmd.connect(cmd, omit={"valid", "last", "ready"})
            if ready == "reg":
                self.sync += inner.cmd.ready.eq(cmd.ready)
            else:
                self.comb += inner.cmd.ready.eq(cmd.ready)
            if hold:
                count = Signal(max=hold + 1)
                started = Signal()
                self.sync += If(count != hold, count.eq(count + 1))
                self.comb += started.eq(count == hold)
                zreset = ~started
                if rephase_extra:
                    late = Signal()
                    self.sync += late.eq(inner.zqs_executer.done)
                    zreset = zreset | late
                self.comb += ResetInserter()(inner.zqcs_timer).reset.eq(zreset)
                if hold_refresh:
                    self.comb += ResetInserter()(inner.timer).reset.eq(~started)
    return R


class ValidWaitsReady(Module):
    """PipeReady-shaped skid whose output VALID is offered only while READY is high."""

    def __init__(self, layout):
        self.submodules.p = p = stream.PipeReady(layout)
        self.sink, self.source = p.sink, stream.Endpoint(layout)
        self.comb += [p.source.connect(self.source, omit={"valid"}),
                      self.source.valid.eq(p.source.valid & self.source.ready)]


class Dup(Module):
    """Skid that holds a beat taken into a stall, then presents it twice."""

    def __init__(self, layout):
        self.sink, self.source = stream.Endpoint(layout), stream.Endpoint(layout)
        held, again = Signal(), Signal()
        buf = stream.Endpoint(layout)
        self.sync += [
            If(self.sink.valid & self.sink.ready & ~self.source.ready,
               held.eq(1), self.sink.connect(buf, omit={"valid", "ready"}))
            .Elif(held & self.source.ready & ~again, again.eq(1))
            .Elif(held & self.source.ready & again, held.eq(0), again.eq(0))]
        self.comb += [
            self.sink.ready.eq(~held),
            If(held, buf.connect(self.source, omit={"valid", "ready"}), self.source.valid.eq(1))
            .Else(self.sink.connect(self.source, omit={"ready"}))]


def axi_stage(factory):
    class Stage(Module):
        def __init__(self, master, slave):
            for name in ("aw", "ar"):
                pipe = factory(getattr(master, name).description)
                setattr(self.submodules, f"{name}_pipe", pipe)
                self.comb += [getattr(master, name).connect(pipe.sink), pipe.source.connect(getattr(slave, name))]
            self.comb += master.w.connect(slave.w)
            for name in ("b", "r"):
                self.comb += getattr(slave, name).connect(getattr(master, name))
    return Stage


def after_valid(factory):
    def make(layout):
        class B(Module):
            def __init__(self):
                self.submodules.a = a = stream.PipeValid(layout)
                self.submodules.b = b = factory(layout)
                self.sink, self.source = a.sink, b.source
                self.comb += a.source.connect(b.sink)
        return B()
    return make


def buffered(layout):
    return stream.Buffer(layout, pipe_valid=True, pipe_ready=True)


def spi_stage(tx_factory, rx_factory):
    class Stage(Module):
        def __init__(self, phy):
            self.phy_sink, self.phy_source, self.phy_cs = phy.sink, phy.source, phy.cs
            self.sink = stream.Endpoint(phy.sink.description)
            self.source = stream.Endpoint(phy.source.description)
            self.cs = Signal.like(phy.cs)
            self.submodules.tx = tx = tx_factory(phy.sink.description)
            self.submodules.rx = rx = rx_factory(phy.source.description)
            self.comb += [self.sink.connect(tx.sink), tx.source.connect(phy.sink),
                          phy.source.connect(rx.sink), rx.source.connect(self.source)]
            self.sync += phy.cs.eq(self.cs)
    return Stage


REF = ["refresh_structure", "refresh_behaviour"]
MUTANTS = {
    "zqcs_hold2": ("RegisteredRefresher", refresher(hold=2), REF),
    "zqcs_rephase_extra": ("RegisteredRefresher", refresher(rephase_extra=True), REF),
    "zqcs_hold_both": ("RegisteredRefresher", refresher(hold_refresh=True), REF),
    "ref_last_comb_h": ("RegisteredRefresher", refresher(last="comb"), REF),
    "ref_ready_registered_h": ("RegisteredRefresher", refresher(ready="reg"), REF),
    "ref_no_last_h": ("RegisteredRefresher", refresher(last="none"), REF),
    "ref_shipping_equivalent": ("RegisteredRefresher", refresher(), REF),   # control: must SURVIVE
    "axi_valid_waits_ready": ("AXIReadyStage", axi_stage(ValidWaitsReady), ["dram_structure", "dram_behaviour"]),
    "axi_dup": ("AXIReadyStage", axi_stage(Dup), ["dram_structure", "dram_behaviour"]),
    "spi_tx_valid_waits_ready": ("SPIPHYStage", spi_stage(after_valid(ValidWaitsReady), buffered),
                                 ["flash_structure", "flash_behaviour"]),
    "spi_rx_valid_waits_ready": ("SPIPHYStage", spi_stage(buffered, after_valid(ValidWaitsReady)),
                                 ["flash_structure", "flash_behaviour"]),
    "spi_rx_dup": ("SPIPHYStage", spi_stage(buffered, after_valid(Dup)), ["flash_structure", "flash_behaviour"]),
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
