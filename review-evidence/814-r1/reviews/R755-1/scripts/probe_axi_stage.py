#!/usr/bin/env python3
"""Reviewer probe: AXIReadyStage under random stalls and back-to-back beats.

Usage: probe_axi_stage.py <repo-root> [shipping|lossy|dup]

Drives the stage's master face with AXI-legal traffic (VALID held until the
handshake, payload stable while held) on aw, w and ar, with a random slave
READY on the far side, and checks:
  - the slave sees exactly the master's accepted beats, in order (no drop,
    duplicate or reorder), on every channel;
  - the slave face keeps VALID and payload stable while READY is low;
  - the stage's hold register engages (the stall path is exercised);
  - b and r pass back unchanged.
The 'lossy' and 'dup' arms replace the stage with a defective skid buffer and
must be reported as failing, so the probe can go red.
"""
import random
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw" / "litex"))
variant = sys.argv[2] if len(sys.argv) > 2 else "shipping"

from migen import Module, Signal, If, run_simulation  # noqa: E402
from litex.soc.interconnect import axi, stream  # noqa: E402
import milan_soc  # noqa: E402


class LossyPipeReady(Module):
    """A skid buffer that accepts a beat while full and drops it."""
    def __init__(self, layout):
        self.sink = sink = stream.Endpoint(layout)
        self.source = source = stream.Endpoint(layout)
        valid = Signal()
        sink_d = stream.Endpoint(layout)
        self.sync += [If(sink.valid & ~source.ready, valid.eq(1)).Elif(source.ready, valid.eq(0)),
                      If(~source.ready & ~valid, sink_d.eq(sink))]
        self.comb += [sink.ready.eq(1),
                      If(valid, sink_d.connect(source, omit={"ready"})).Else(sink.connect(source, omit={"ready"}))]


class DupPipeReady(Module):
    """A skid buffer that replays its held beat once after the pass-through beat."""
    def __init__(self, layout):
        self.sink = sink = stream.Endpoint(layout)
        self.source = source = stream.Endpoint(layout)
        valid = Signal()
        sink_d = stream.Endpoint(layout)
        self.sync += [If(sink.valid & source.ready, valid.eq(1), sink_d.eq(sink)).Elif(source.ready, valid.eq(0))]
        self.comb += [sink.ready.eq(~valid),
                      If(valid, sink_d.connect(source, omit={"ready"})).Else(sink.connect(source, omit={"ready"}))]


if variant != "shipping":
    pipe_cls = {"lossy": LossyPipeReady, "dup": DupPipeReady}[variant]
    milan_soc.stream = type("S", (), {"PipeReady": pipe_cls})


class Top(Module):
    def __init__(self):
        self.m = axi.AXIInterface(data_width=64, address_width=32, id_width=4, version="axi4")
        self.s = axi.AXIInterface(data_width=64, address_width=32, id_width=4, version="axi4")
        self.submodules.stage = milan_soc.AXIReadyStage(self.m, self.s)


random.seed(814)
top = Top()
N = 400
sent = {"aw": [], "w": [], "ar": []}
got = {"aw": [], "w": [], "ar": []}
violations = []
hold_cycles = {"aw": 0, "ar": 0}
back = []


def field(ch):
    return "addr" if ch in ("aw", "ar") else "data"


def master(ch):
    port = getattr(top.m, ch)
    for i in range(N):
        value = random.getrandbits(32) | (i << 32 if ch == "w" else 0)
        if ch != "w":
            value &= 0xFFFFFFFF
        # random idle gap, often zero (back-to-back)
        for _ in range(random.choice([0, 0, 0, 1, 2])):
            yield port.valid.eq(0)
            yield
        yield getattr(port, field(ch)).eq(value)
        if ch != "w":
            yield port.id.eq(i & 0xF)
            yield port.len.eq(i & 0x7)
        yield port.valid.eq(1)
        yield
        while not (yield port.ready):
            yield
        sent[ch].append(value)
    yield port.valid.eq(0)


def slave(ch):
    port = getattr(top.s, ch)
    prev = None
    for _ in range(N * 12):
        r = random.random() < 0.45
        yield port.ready.eq(int(r))
        yield
        v = yield port.valid
        rd = yield port.ready
        d = yield getattr(port, field(ch))
        if prev is not None and prev[0] and not prev[1]:
            if not v or d != prev[2]:
                violations.append((ch, "slave face dropped VALID or changed payload while READY low"))
        if v and rd:
            got[ch].append(d)
        prev = (v, rd, d)
        if ch in hold_cycles:
            if not (yield getattr(top.m, ch).ready):
                hold_cycles[ch] += 1


def responses():
    for i in range(50):
        yield top.s.r.valid.eq(1)
        yield top.s.r.data.eq(i)
        yield top.m.r.ready.eq(1)
        yield
        if (yield top.m.r.valid) != 1 or (yield top.m.r.data) != i or (yield top.s.r.ready) != 1:
            back.append(i)


run_simulation(top, [master("aw"), master("w"), master("ar"), slave("aw"), slave("w"), slave("ar"), responses()])

ok = True
for ch in ("aw", "w", "ar"):
    same = got[ch][:len(sent[ch])] == sent[ch] and len(got[ch]) == len(sent[ch])
    print(f"  {ch}: master accepted {len(sent[ch])}, slave accepted {len(got[ch])}, identical order: {same}")
    ok &= same
print(f"  hold register engaged (master READY low) cycles: {hold_cycles}")
print(f"  slave-face VALID/payload stability violations: {len(violations)}")
print(f"  r passthrough mismatches: {len(back)}")
ok &= not violations and not back and all(hold_cycles[c] > 0 for c in hold_cycles)
print(f"PROBE {variant}: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
