#!/usr/bin/env python3
"""Reviewer probe, round 2 of PR #826 (#814): planted stage and refresher defects against the gate's
own behaviour arms, a ZQCS period sweep of the shipping refresher, and a structural VALID/READY check.

Usage:
  probe_r2.py <repo-root> mutant <name>      install one planted defect, run its behaviour arm(s) of
                                             sw/litex/test_soc_timing_cuts.py, print every graded line
                                             and 'MUTANT KILLED by [...]' or 'MUTANT SURVIVED'
  probe_r2.py <repo-root> zqcs <period> <cycles>
                                             the shipping RegisteredRefresher against LiteDRAM's own
                                             Refresher, both with a <period>-cycle ZQCS period, idle for
                                             <cycles> sys cycles: every DFI command must be LiteDRAM's
                                             one cycle later; prints the ZQCS cycles and the refresh spacing
  probe_r2.py <repo-root> validdep [mutant]  in the shipping flash and DRAM builds, whether any stage
                                             output's VALID or payload reads that output's READY through
                                             logic alone (a source waiting on READY)

Mutants (each is a stage that keeps the timing cut's registered READY or registered request):
  axi-dropheld      aw and ar: PipeReady's flag and READY kept, the held copy never presented
  axi-dropheld-aw   the same on aw only;   axi-dropheld-ar   on ar only
  axi-duphold       aw and ar: the held beat presented twice
  axi-validwait     aw and ar: the shipping PipeReady, its output VALID ANDed with the output READY
  spi-tx-dropheld / spi-rx-dropheld   one SPI buffer's PipeReady loses the held copy
  spi-tx-duphold  / spi-rx-duphold    one SPI buffer's PipeReady presents the held beat twice
  spi-tx-validwait                    the PHY-side command VALID ANDed with the PHY's READY
  ref-undelayed     registered request, ZQCS timer from reset (the gate's own Z5 plant)
  ref-donedelay     registered request, the ZQCS timer's done pulse one cycle late instead of its start
  ref-hold2         the shipping stage with the ZQCS timer held in reset two cycles instead of one
  ref-holdrefresh   the hold applied to the tREFI timer instead of the ZQCS timer
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw" / "litex"))

from migen import If, Module, ResetInserter, Signal  # noqa: E402
from litex.soc.interconnect import stream  # noqa: E402
import litedram.core.refresher as refresher_module  # noqa: E402
from litedram.core.refresher import Refresher, RefreshTimer  # noqa: E402
import milan_soc  # noqa: E402
import test_soc_timing_cuts as gate  # noqa: E402


class DropHeldPipeReady(Module):
    """READY registered (~held) as PipeReady's, the held beat never presented: lost on a stall."""
    def __init__(self, layout):
        self.sink, self.source = stream.Endpoint(layout), stream.Endpoint(layout)
        held = Signal()
        self.sync += If(self.sink.valid & ~self.source.ready, held.eq(1)).Elif(self.source.ready, held.eq(0))
        self.comb += [self.sink.connect(self.source, omit={"ready"}), self.sink.ready.eq(~held)]


class DupHeldPipeReady(Module):
    """PipeReady whose held beat is presented, and taken, twice before it is released."""
    def __init__(self, layout):
        self.sink, self.source = stream.Endpoint(layout), stream.Endpoint(layout)
        held, again = Signal(), Signal()
        buf = stream.Endpoint(layout)
        self.sync += [
            If(self.sink.valid & self.sink.ready & ~self.source.ready, held.eq(1), buf.eq(self.sink))
            .Elif(held & self.source.ready & ~again, again.eq(1))
            .Elif(held & self.source.ready & again, held.eq(0), again.eq(0))]
        self.comb += [self.sink.ready.eq(~held),
                      If(held, buf.connect(self.source, omit={"ready"}))
                      .Else(self.sink.connect(self.source, omit={"ready"}))]


class ValidWaitPipeReady(Module):
    """The shipping PipeReady, its output VALID waiting on the output READY."""
    def __init__(self, layout):
        self.submodules.pipe = pipe = stream.PipeReady(layout)
        self.sink, self.source = pipe.sink, stream.Endpoint(layout)
        self.comb += [pipe.source.connect(self.source, omit={"valid"}),
                      self.source.valid.eq(pipe.source.valid & self.source.ready)]


def axi_stage(pipe_for):
    class Stage(Module):
        def __init__(self, master, slave):
            for name in ("aw", "ar"):
                layout = getattr(master, name).description
                pipe = pipe_for(name, layout)
                setattr(self.submodules, f"{name}_pipe", pipe)
                self.comb += [getattr(master, name).connect(pipe.sink), pipe.source.connect(getattr(slave, name))]
            self.comb += master.w.connect(slave.w)
            for name in ("b", "r"):
                self.comb += getattr(slave, name).connect(getattr(master, name))
    return Stage


def spi_stage(which, ready_cls):
    """SPIPHYStage with the `which` buffer's PipeReady replaced by `ready_cls` (PipeValid kept)."""
    class Stage(Module):
        def __init__(self, phy):
            self.phy_sink, self.phy_source, self.phy_cs = phy.sink, phy.source, phy.cs
            self.sink = stream.Endpoint(phy.sink.description)
            self.source = stream.Endpoint(phy.source.description)
            self.cs = Signal.like(phy.cs)
            for name, layout in (("tx", phy.sink.description), ("rx", phy.source.description)):
                if name == which:
                    pv, pr = stream.PipeValid(layout), ready_cls(layout)
                    setattr(self.submodules, f"{name}_pv", pv)
                    setattr(self.submodules, f"{name}_pr", pr)
                    self.comb += pv.source.connect(pr.sink)
                    ends = (pv.sink, pr.source)
                else:
                    buf = stream.Buffer(layout, pipe_valid=True, pipe_ready=True)
                    setattr(self.submodules, name, buf)
                    ends = (buf.sink, buf.source)
                if name == "tx":
                    self.comb += [self.sink.connect(ends[0]), ends[1].connect(phy.sink)]
                else:
                    self.comb += [phy.source.connect(ends[0]), ends[1].connect(self.source)]
            self.sync += phy.cs.eq(self.cs)
    return Stage


class DelayedDoneTimer(Module):
    """LiteDRAM's RefreshTimer, its done output registered once; the timer itself is unchanged."""
    def __init__(self, trefi):
        self.submodules.inner = inner = RefreshTimer(trefi)
        self.wait, self.done, self.count = inner.wait, Signal(), inner.count
        self.sync += self.done.eq(inner.done)


def registered_request(build_refresher, hold=None):
    """A refresher class: `build_refresher(...)`'s request registered as the shipping stage does; with
    `hold=(attribute, cycles)`, that timer submodule held in reset for `cycles` cycles after reset."""
    class R(Module):
        def __init__(self, settings, clk_freq, zqcs_freq=1e0, postponing=1):
            self.submodules.refresher = inner = build_refresher(settings, clk_freq, zqcs_freq, postponing)
            self.cmd = cmd = stream.Endpoint(inner.cmd.description)
            self.sync += [cmd.valid.eq(inner.cmd.valid), cmd.last.eq(inner.cmd.last)]
            self.comb += [inner.cmd.connect(cmd, omit={"valid", "last", "ready"}), inner.cmd.ready.eq(cmd.ready)]
            if hold is not None:
                attribute, cycles = hold
                count = Signal(max=cycles + 1)
                self.sync += If(count != cycles, count.eq(count + 1))
                self.comb += ResetInserter()(getattr(inner, attribute)).reset.eq(count != cycles)
    return R


def plain(settings, clk_freq, zqcs_freq, postponing):
    return Refresher(settings, clk_freq, zqcs_freq=zqcs_freq, postponing=postponing)


def done_delayed(settings, clk_freq, zqcs_freq, postponing):
    zqcs_cycles = int(clk_freq / zqcs_freq)
    original = refresher_module.RefreshTimer
    refresher_module.RefreshTimer = lambda n: DelayedDoneTimer(n) if n == zqcs_cycles else original(n)
    try:
        return Refresher(settings, clk_freq, zqcs_freq=zqcs_freq, postponing=postponing)
    finally:
        refresher_module.RefreshTimer = original


MUTANTS = {
    "axi-dropheld": ("AXIReadyStage", axi_stage(lambda n, l: DropHeldPipeReady(l)), "dram_behaviour"),
    "axi-dropheld-aw": ("AXIReadyStage", axi_stage(lambda n, l: DropHeldPipeReady(l) if n == "aw"
                                                   else stream.PipeReady(l)), "dram_behaviour"),
    "axi-dropheld-ar": ("AXIReadyStage", axi_stage(lambda n, l: DropHeldPipeReady(l) if n == "ar"
                                                   else stream.PipeReady(l)), "dram_behaviour"),
    "axi-duphold": ("AXIReadyStage", axi_stage(lambda n, l: DupHeldPipeReady(l)), "dram_behaviour"),
    "axi-validwait": ("AXIReadyStage", axi_stage(lambda n, l: ValidWaitPipeReady(l)), "dram_behaviour"),
    "spi-tx-dropheld": ("SPIPHYStage", spi_stage("tx", DropHeldPipeReady), "flash_behaviour"),
    "spi-rx-dropheld": ("SPIPHYStage", spi_stage("rx", DropHeldPipeReady), "flash_behaviour"),
    "spi-tx-duphold": ("SPIPHYStage", spi_stage("tx", DupHeldPipeReady), "flash_behaviour"),
    "spi-rx-duphold": ("SPIPHYStage", spi_stage("rx", DupHeldPipeReady), "flash_behaviour"),
    "spi-tx-validwait": ("SPIPHYStage", spi_stage("tx", ValidWaitPipeReady), "flash_behaviour"),
    "ref-undelayed": ("RegisteredRefresher", registered_request(plain), "refresh_behaviour"),
    "ref-donedelay": ("RegisteredRefresher", registered_request(done_delayed), "refresh_behaviour"),
    "ref-hold2": ("RegisteredRefresher", registered_request(plain, ("zqcs_timer", 2)), "refresh_behaviour"),
    "ref-holdrefresh": ("RegisteredRefresher", registered_request(plain, ("timer", 1)), "refresh_behaviour"),
}


def mutant(name):
    cls_name, replacement, arm = MUTANTS[name]
    shipping = getattr(milan_soc, cls_name)
    setattr(milan_soc, cls_name, replacement)
    problems = []
    try:
        getattr(gate, arm)(problems)
    except Exception as exc:
        problems.append(f"{arm} raised {type(exc).__name__}: {exc}")
        print(f"  [FAIL] {arm} raised {type(exc).__name__}: {exc}")
    finally:
        setattr(milan_soc, cls_name, shipping)
    ids = [problem.split(" ", 1)[0] for problem in problems]
    print(f"MUTANT {name}: " + (f"KILLED by {ids}" if problems else "SURVIVED"))


def zqcs(period, cycles):
    period, cycles = int(period), int(cycles)

    def short(cls):
        class S(cls):
            def __init__(self, settings, clk_freq, zqcs_freq=1e0, postponing=1):
                cls.__init__(self, settings, clk_freq, zqcs_freq=clk_freq / period, postponing=postponing)
        return S

    staged = gate.dfi_commands(short(milan_soc.RegisteredRefresher), cycles)
    ref = gate.dfi_commands(short(Refresher), cycles)
    shifted = [(c + 1, i, n, a) for c, i, n, a in ref if c + 1 < cycles]
    zs, zr = ([c for c, _, n, _ in run if n == "ZQCS"] for run in (staged, ref))
    refreshes = [c for c, _, n, _ in staged if n == "REFRESH"]
    spacing = sorted({b - a for a, b in zip(refreshes, refreshes[1:])})
    first = next((i for i, (a, b) in enumerate(zip(staged, shifted)) if a != b), None)
    same = staged == shifted
    print(f"ZQCS period {period}, {cycles} cycles: staged ZQCS {zs}, LiteDRAM ZQCS {zr}; "
          f"{len(staged)} staged commands, {len(ref)} LiteDRAM; refresh spacing {spacing}; "
          f"staged == LiteDRAM + 1: {same}" + ("" if same else
          f"; first difference at index {first}: {staged[first:first + 2] if first is not None else staged[len(shifted):][:2]} "
          f"vs {shifted[first:first + 2] if first is not None else shifted[len(staged):][:2]}"))
    print("ZQCS SWEEP " + ("PASS" if same else "FAIL"))
    return 0 if same else 1


def validdep(planted=None):
    if planted:
        cls_name, replacement, _ = MUTANTS[planted]
        setattr(milan_soc, cls_name, replacement)
    bad = []
    flash = gate.build(gate.FlashSoC, [0] * 64)
    stage = flash.spiflash.phy.stage
    net = gate.Netlist(flash.get_fragment())
    faces = [("spi tx (PHY face)", stage.phy_sink), ("spi rx (core face)", stage.source)]
    dram = gate.build(gate.DramSoC)
    stages = gate.find(dram, milan_soc.AXIReadyStage)
    dnet = gate.Netlist(dram.get_fragment())
    for s in stages:
        faces += [(f"axi {n} (LiteDRAM face)", getattr(s, f"{n}_pipe").source) for n in ("aw", "ar")]
    for label, end in faces:
        n = net if label.startswith("spi") else dnet
        reads = set()
        for signal in gate.faces(end, True):
            flops, wires = n.cone(signal)
            reads |= flops | wires
        waits = end.ready.duid in reads
        print(f"  {label}: VALID/payload read READY through logic: {waits}")
        bad += [label] if waits else []
    print(f"VALIDDEP {'FAIL ' + str(bad) if bad else 'PASS'} ({len(faces)} faces, {len(stages)} AXI stage)")
    return 1 if bad else 0


if __name__ == "__main__":
    mode = sys.argv[2]
    if mode == "mutant":
        mutant(sys.argv[3])
    elif mode == "zqcs":
        sys.exit(zqcs(sys.argv[3], sys.argv[4]))
    elif mode == "validdep":
        sys.exit(validdep(sys.argv[3] if len(sys.argv) > 3 else None))
