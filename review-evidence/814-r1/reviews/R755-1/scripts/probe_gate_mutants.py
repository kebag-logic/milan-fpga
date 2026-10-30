#!/usr/bin/env python3
"""Reviewer probe: run arms of sw/litex/test_soc_timing_cuts.py against planted defects.

Usage: probe_gate_mutants.py <repo-root> <arm>

Arms:
  hold          shipping stages; report whether the gate's own behaviour traffic
                ever engages each skid register (AXI aw/ar PipeReady, SPI tx/rx
                PipeReady), i.e. whether the stall path is exercised at all.
  axi-lossy     AXIReadyStage whose skid buffer drops a beat it accepts while full;
                runs the gate's DRAM arms (D0..D4).
  spi-lossy     SPIPHYStage whose tx/rx skid buffers drop a beat accepted while full;
                runs the gate's flash behaviour arms (F3..F5).
  ref-2cycle    RegisteredRefresher with valid/last registered twice; runs Z3.
  ref-lastcomb  RegisteredRefresher with last left combinational; runs Z0..Z2.
  spi-cscomb    SPIPHYStage with chip select left combinational; runs F0..F2.
  axi-aronly    AXIReadyStage piping ar only; runs D0..D2.
  hold-dram     the DRAM half of 'hold' only.
  axi-dropheld  AXIReadyStage keeping registered READY but losing the held beat; D0..D4.
  spi-dropheld  SPIPHYStage keeping registered READY but losing the held beat; F0..F5.
Prints the gate's own [ok]/[FAIL] lines and 'MUTANT KILLED' / 'MUTANT SURVIVED'.
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
arm = sys.argv[2]
sys.path.insert(0, str(root / "sw" / "litex"))

from migen import Module, Signal, If  # noqa: E402
from migen.sim import passive  # noqa: E402
from litex.soc.interconnect import stream  # noqa: E402
import milan_soc  # noqa: E402
import test_soc_timing_cuts as gate  # noqa: E402


class LossyPipeReady(Module):
    """Accepts a beat while full and drops it (READY tied high)."""
    def __init__(self, layout):
        self.sink = sink = stream.Endpoint(layout)
        self.source = source = stream.Endpoint(layout)
        valid = Signal()
        sink_d = stream.Endpoint(layout)
        self.sync += [If(sink.valid & ~source.ready, valid.eq(1)).Elif(source.ready, valid.eq(0)),
                      If(~source.ready & ~valid, sink_d.eq(sink))]
        self.comb += [sink.ready.eq(1),
                      If(valid, sink_d.connect(source, omit={"ready"})).Else(sink.connect(source, omit={"ready"}))]


class LossyAXIStage(Module):
    def __init__(self, master, slave):
        for name in ("aw", "ar"):
            pipe = LossyPipeReady(getattr(master, name).description)
            setattr(self.submodules, f"{name}_pipe", pipe)
            self.comb += [getattr(master, name).connect(pipe.sink), pipe.source.connect(getattr(slave, name))]
        self.comb += master.w.connect(slave.w)
        for name in ("b", "r"):
            self.comb += getattr(slave, name).connect(getattr(master, name))


class DropHeldPipeReady(Module):
    """READY still registered (~full), but the held beat is never presented: lost on a stall."""
    def __init__(self, layout):
        self.sink = sink = stream.Endpoint(layout)
        self.source = source = stream.Endpoint(layout)
        valid = Signal()
        self.sync += If(sink.valid & ~source.ready, valid.eq(1)).Elif(source.ready, valid.eq(0))
        self.comb += [sink.ready.eq(~valid), sink.connect(source, omit={"ready"})]


class DropHeldAXIStage(Module):
    def __init__(self, master, slave):
        for name in ("aw", "ar"):
            pipe = DropHeldPipeReady(getattr(master, name).description)
            setattr(self.submodules, f"{name}_pipe", pipe)
            self.comb += [getattr(master, name).connect(pipe.sink), pipe.source.connect(getattr(slave, name))]
        self.comb += master.w.connect(slave.w)
        for name in ("b", "r"):
            self.comb += getattr(slave, name).connect(getattr(master, name))


class DropHeldSPIStage(Module):
    def __init__(self, phy):
        self.phy_sink, self.phy_source, self.phy_cs = phy.sink, phy.source, phy.cs
        self.sink = stream.Endpoint(phy.sink.description)
        self.source = stream.Endpoint(phy.source.description)
        self.cs = Signal.like(phy.cs)
        for name, desc in (("tx", phy.sink.description), ("rx", phy.source.description)):
            pv, pr = stream.PipeValid(desc), DropHeldPipeReady(desc)
            setattr(self.submodules, f"{name}_pv", pv)
            setattr(self.submodules, f"{name}_pr", pr)
            self.comb += pv.source.connect(pr.sink)
            if name == "tx":
                self.comb += [self.sink.connect(pv.sink), pr.source.connect(phy.sink)]
            else:
                self.comb += [phy.source.connect(pv.sink), pr.source.connect(self.source)]
        self.sync += phy.cs.eq(self.cs)


class AROnlyAXIStage(Module):
    def __init__(self, master, slave):
        pipe = stream.PipeReady(master.ar.description)
        self.submodules.ar_pipe = pipe
        self.comb += [master.ar.connect(pipe.sink), pipe.source.connect(slave.ar),
                      master.aw.connect(slave.aw), master.w.connect(slave.w)]
        for name in ("b", "r"):
            self.comb += getattr(slave, name).connect(getattr(master, name))


class LossySPIStage(Module):
    def __init__(self, phy):
        self.phy_sink, self.phy_source, self.phy_cs = phy.sink, phy.source, phy.cs
        self.sink = stream.Endpoint(phy.sink.description)
        self.source = stream.Endpoint(phy.source.description)
        self.cs = Signal.like(phy.cs)
        for name, desc in (("tx", phy.sink.description), ("rx", phy.source.description)):
            pv, pr = stream.PipeValid(desc), LossyPipeReady(desc)
            setattr(self.submodules, f"{name}_pv", pv)
            setattr(self.submodules, f"{name}_pr", pr)
            self.comb += pv.source.connect(pr.sink)
            if name == "tx":
                self.comb += [self.sink.connect(pv.sink), pr.source.connect(phy.sink)]
            else:
                self.comb += [phy.source.connect(pv.sink), pr.source.connect(self.source)]
        self.sync += phy.cs.eq(self.cs)


class CombCSStage(milan_soc.SPIPHYStage):
    def __init__(self, phy):
        self.phy_sink, self.phy_source, self.phy_cs = phy.sink, phy.source, phy.cs
        self.sink = stream.Endpoint(phy.sink.description)
        self.source = stream.Endpoint(phy.source.description)
        self.cs = Signal.like(phy.cs)
        self.submodules.tx = tx = stream.Buffer(phy.sink.description, pipe_valid=True, pipe_ready=True)
        self.submodules.rx = rx = stream.Buffer(phy.source.description, pipe_valid=True, pipe_ready=True)
        self.comb += [self.sink.connect(tx.sink), tx.source.connect(phy.sink),
                      phy.source.connect(rx.sink), rx.source.connect(self.source), phy.cs.eq(self.cs)]


class TwoCycleRefresher(Module):
    def __init__(self, settings, clk_freq, zqcs_freq=1e0, postponing=1):
        from litedram.core.refresher import Refresher
        self.submodules.refresher = r = Refresher(settings, clk_freq, zqcs_freq=zqcs_freq, postponing=postponing)
        self.cmd = cmd = stream.Endpoint(r.cmd.description)
        v, l = Signal(), Signal()
        self.sync += [v.eq(r.cmd.valid), l.eq(r.cmd.last), cmd.valid.eq(v), cmd.last.eq(l)]
        self.comb += [r.cmd.connect(cmd, omit={"valid", "last", "ready"}), r.cmd.ready.eq(cmd.ready)]


class LastCombRefresher(Module):
    def __init__(self, settings, clk_freq, zqcs_freq=1e0, postponing=1):
        from litedram.core.refresher import Refresher
        self.submodules.refresher = r = Refresher(settings, clk_freq, zqcs_freq=zqcs_freq, postponing=postponing)
        self.cmd = cmd = stream.Endpoint(r.cmd.description)
        self.sync += cmd.valid.eq(r.cmd.valid)
        self.comb += [r.cmd.connect(cmd, omit={"valid", "ready"}), r.cmd.ready.eq(cmd.ready)]


problems = []
if arm in ("hold", "hold-dram"):
    seen = {}
    orig_build, orig_run = gate.build, gate.run_simulation
    last = {}

    def build(*a, **k):
        soc = orig_build(*a, **k)
        last["soc"] = soc
        return soc

    def run(soc, gens, **kw):
        watched = []
        if hasattr(soc, "cpu") and hasattr(getattr(soc.cpu, "memory_port_stage0", None), "aw_pipe"):
            st = soc.cpu.memory_port_stage0
            watched = [("axi.aw_pipe", st.aw_pipe.sink), ("axi.ar_pipe", st.ar_pipe.sink)]
        elif hasattr(soc, "spiflash") and hasattr(soc.spiflash.phy.stage, "tx") and hasattr(soc.spiflash.phy.stage.tx, "pipe_ready"):
            st = soc.spiflash.phy.stage
            watched = [("spi.tx.pipe_ready", st.tx.pipe_ready.sink), ("spi.rx.pipe_ready", st.rx.pipe_ready.sink)]

        @passive
        def watch():
            while True:
                for name, sink in watched:
                    if not (yield sink.ready):
                        seen[name] = seen.get(name, 0) + 1
                    else:
                        seen.setdefault(name, 0)
                yield
        if isinstance(gens, dict):
            gens = {k: list(v) for k, v in gens.items()}
            gens.setdefault("sys", []).append(watch())
        else:
            gens = list(gens) + [watch()]
        return orig_run(soc, gens, **kw)

    gate.build, gate.run_simulation = build, run
    if arm == "hold":
        gate.flash_behaviour(problems)
        print(f"HOLD flash traffic: cycles with skid register full: {dict(seen)}")
    seen.clear()
    gate.dram_behaviour(problems)
    print(f"HOLD dram traffic: cycles with skid register full: {dict(seen)}")
    print(f"gate problems: {problems}")
    sys.exit(0)

plan = {
    "axi-lossy": ("AXIReadyStage", LossyAXIStage, [gate.dram_structure, gate.dram_behaviour]),
    "axi-dropheld": ("AXIReadyStage", DropHeldAXIStage, [gate.dram_structure, gate.dram_behaviour]),
    "spi-dropheld": ("SPIPHYStage", DropHeldSPIStage, [gate.flash_structure, gate.flash_behaviour]),
    "axi-aronly": ("AXIReadyStage", AROnlyAXIStage, [gate.dram_structure]),
    "spi-lossy": ("SPIPHYStage", LossySPIStage, [gate.flash_behaviour]),
    "spi-cscomb": ("SPIPHYStage", CombCSStage, [gate.flash_structure]),
    "ref-2cycle": ("RegisteredRefresher", TwoCycleRefresher, [gate.refresh_behaviour]),
    "ref-lastcomb": ("RegisteredRefresher", LastCombRefresher, [gate.refresh_structure]),
}
name, cls, arms = plan[arm]
setattr(milan_soc, name, cls)
# the gate's own build() restores milan_soc.<name> to what it found, which is now the mutant
for a in arms:
    a(problems)
print(f"gate failures under {arm}: {len(problems)}")
print("MUTANT KILLED" if problems else "MUTANT SURVIVED")
