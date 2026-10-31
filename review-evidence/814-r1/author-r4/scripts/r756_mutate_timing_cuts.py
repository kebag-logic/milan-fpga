#!/usr/bin/env python3
"""Mutation probe: does test_soc_timing_cuts.py kill each planted stage defect?

Each mutant replaces one shipping class in milan_soc for the duration of the
named arms of the test (imported unchanged from the tree under review). A
mutant is KILLED when those arms record at least one failure.

Usage: python3 mutate_timing_cuts.py <repo>/sw/litex <mutant>
"""
import sys

sys.path.insert(0, sys.argv[1])
import milan_soc  # noqa: E402
import test_soc_timing_cuts as t  # noqa: E402
from migen import Module, Signal  # noqa: E402
from litex.soc.interconnect import stream  # noqa: E402


class LossyReady(Module):
    """READY registered from the last stall, payload combinational: loses a beat offered into a fresh stall."""

    def __init__(self, layout):
        self.sink, self.source = stream.Endpoint(layout), stream.Endpoint(layout)
        stall = Signal()
        self.sync += stall.eq(self.source.valid & ~self.source.ready)
        self.comb += [self.sink.connect(self.source, omit={"ready"}), self.sink.ready.eq(~stall)]


def axi_stage(pipe_for):
    class Stage(Module):
        def __init__(self, master, slave):
            for name in ("aw", "ar"):
                layout = getattr(master, name).description
                pipe = pipe_for(name, layout)
                if pipe is None:
                    self.comb += getattr(master, name).connect(getattr(slave, name))
                    continue
                setattr(self.submodules, f"{name}_pipe", pipe)
                self.comb += [getattr(master, name).connect(pipe.sink), pipe.source.connect(getattr(slave, name))]
            self.comb += master.w.connect(slave.w)
            for name in ("b", "r"):
                self.comb += getattr(slave, name).connect(getattr(master, name))
    return Stage


def spi_stage(tx_factory, rx_factory, cs_registered=True):
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
            if cs_registered:
                self.sync += phy.cs.eq(self.cs)
            else:
                self.comb += phy.cs.eq(self.cs)
    return Stage


def buffered(layout):
    return stream.Buffer(layout, pipe_valid=True, pipe_ready=True)


def valid_lossy(layout):
    class P(Module):
        def __init__(self):
            self.submodules.a = a = stream.PipeValid(layout)
            self.submodules.b = b = LossyReady(layout)
            self.sink, self.source = a.sink, b.source
            self.comb += a.source.connect(b.sink)
    return P()


def refresher(register_last=True, drop_last=False, register_ready=False):
    from litedram.core.refresher import Refresher

    class R(Module):
        def __init__(self, settings, clk_freq, zqcs_freq=1e0, postponing=1):
            self.submodules.refresher = inner = Refresher(settings, clk_freq, zqcs_freq=zqcs_freq,
                                                          postponing=postponing)
            self.cmd = cmd = stream.Endpoint(inner.cmd.description)
            self.sync += cmd.valid.eq(inner.cmd.valid)
            if drop_last:
                pass
            elif register_last:
                self.sync += cmd.last.eq(inner.cmd.last)
            else:
                self.comb += cmd.last.eq(inner.cmd.last)
            self.comb += inner.cmd.connect(cmd, omit={"valid", "last", "ready"})
            if register_ready:
                self.sync += inner.cmd.ready.eq(cmd.ready)
            else:
                self.comb += inner.cmd.ready.eq(cmd.ready)
    return R


MUTANTS = {
    # name: (class name in milan_soc, replacement, arms)
    "axi_ar_unstaged": ("AXIReadyStage", axi_stage(lambda n, l: None if n == "ar" else stream.PipeReady(l)),
                        ["dram_structure"]),
    "axi_lossy_ready": ("AXIReadyStage", axi_stage(lambda n, l: LossyReady(l)), ["dram_structure", "dram_behaviour"]),
    "axi_pipevalid": ("AXIReadyStage", axi_stage(lambda n, l: stream.PipeValid(l)), ["dram_structure", "dram_behaviour"]),
    "spi_cs_comb": ("SPIPHYStage", spi_stage(buffered, buffered, cs_registered=False), ["flash_structure"]),
    "spi_tx_no_pipe_ready": ("SPIPHYStage", spi_stage(lambda l: stream.Buffer(l, pipe_valid=True, pipe_ready=False),
                                                      buffered), ["flash_structure"]),
    "spi_tx_lossy_ready": ("SPIPHYStage", spi_stage(valid_lossy, buffered), ["flash_structure", "flash_behaviour"]),
    "spi_rx_lossy_ready": ("SPIPHYStage", spi_stage(buffered, valid_lossy), ["flash_structure", "flash_behaviour"]),
    "ref_last_comb": ("RegisteredRefresher", refresher(register_last=False), ["refresh_structure"]),
    "ref_ready_registered": ("RegisteredRefresher", refresher(register_ready=True), ["refresh_behaviour"]),
    "ref_no_last": ("RegisteredRefresher", refresher(drop_last=True), ["refresh_behaviour"]),
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
