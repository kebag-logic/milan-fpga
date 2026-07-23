#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Unit-sim of the PCM ring path: non-stallable source -> CDC-depth FIFO ->
_PCMRingNxN (WishboneDMAWriter) over a contention-modeled wishbone slave.

Regression encoded here (silicon 2026-07-23, mf52): with the 16-deep CDC lane,
concurrent CPU reads of the ring DRAM region slowed the wishbone writer to
~23/24 of the PCM rate; the real-time datapath side cannot stall, so exactly
one 64-bit frame in 24 was shed - ring holes at a stable mod-24 phase, a 2 kHz
whole-frame artifact in every arecord rw capture (ring idle-clean, loaded-
holed; proven with a concurrent pcm_ring_dump). The fix is depth=128 (80ee795).

This sim recreates the exact wiring truth:
  * the source NEVER waits: a beat offered while the FIFO is full is COUNTED
    AS DROPPED and lost (the depacketizer/pcm-route contract);
  * PDU shape is the real one: 6 back-to-back beats per PDU (48 kHz stereo
    S32, AAF class A), then an inter-PDU gap;
  * the wishbone slave alternates fast service with contention bursts whose
    duty is calibrated so the SUSTAINED drain rate lands between the offered
    rate and 23/24 of it - the mf52 regime.

Tests:
  1. depth=16  + contention  -> beats ARE dropped (the silicon failure class
     reproduces; guards the sim's own realism);
  2. depth=128 + the same contention -> ZERO drops AND the ring content is
     the exact uninterrupted sequence (data integrity, per-beat);
  3. depth=128, 4 streams interleaved -> tuser routing lands every beat at
     base + s*stride + offset[s] with per-stream sequence integrity and
     correct offset CSR readback (the layout the ALSA driver consumes).

Run: cd sw/litex && python3 test_pcm_ring.py
"""
import importlib.util
import sys

from migen import *
from migen.sim import passive
from litex.gen import *
from litex.soc.interconnect import stream, wishbone

# ---- load _PCMRingNxN out of milan_soc.py without elaborating the SoC -------
spec = importlib.util.spec_from_file_location("milan_soc", __file__.rsplit("/", 1)[0] + "/milan_soc.py")
milan_soc = importlib.util.module_from_spec(spec)
sys.modules["milan_soc"] = milan_soc
spec.loader.exec_module(milan_soc)
_PCMRingNxN = milan_soc._PCMRingNxN

RING_WORDS = 512               # ring words per stream in the model slave
NB = 8                          # 64-bit bus


class Harness(Module):
    def __init__(self, depth, n_streams):
        bus = wishbone.Interface(data_width=64, adr_width=32 - 3, addressing="word")
        self.bus = bus
        self.submodules.dut = _PCMRingNxN(bus, n_streams=n_streams)
        # the CDC lane stand-in: same-cd ClockDomainCrossing degrades to a
        # SyncFIFO of the same depth - the depth semantics under test are
        # identical, without needing a second sim clock domain
        layout = [("data", 64), ("user", 4)]
        self.submodules.fifo = stream.SyncFIFO(layout, depth=depth, buffered=True)
        self.comb += self.fifo.source.connect(self.dut.sink)
        self.src = self.fifo.sink

        # model DRAM: per-stream flat arrays + write log
        self.mem = {}
        self.writes = []

    # -- wishbone slave with a contention profile ---------------------------
    @passive
    def wb_slave(self, fast_ack=1, slow_ack=24, slow_every=6):
        """Edge-driven service: one ack (and ONE log entry) per stb-qualified
        transaction; every `slow_every`-th write first eats `slow_ack` stall
        cycles (a CPU contention burst), the rest `fast_ack`. The ack is a
        strict one-cycle pulse and the next transaction is only considered
        on the cycle AFTER the pulse (no double-service race)."""
        n = 0
        while True:
            if (yield self.bus.cyc) and (yield self.bus.stb):
                n += 1
                lat = slow_ack if (slow_every and n % slow_every == 0) else fast_ack
                for _ in range(lat):
                    yield
                adr = yield self.bus.adr
                dat = yield self.bus.dat_w
                self.mem[adr] = dat
                self.writes.append((adr, dat))
                yield self.bus.ack.eq(1)
                yield
                yield self.bus.ack.eq(0)
                yield              # ack low for one full cycle before re-poll
            else:
                yield

    # -- the non-stallable PDU source ---------------------------------------
    def source(self, pdus, gap, streams=(0,), result=None):
        """Offer `pdus` PDUs of 6 back-to-back beats each, round-robin over
        `streams`; a beat offered while sink.ready==0 is DROPPED (counted),
        exactly like the real-time datapath. `gap` idle cycles between PDUs."""
        dropped = 0
        offered = 0
        seq = {s: 0 for s in streams}
        for p in range(pdus):
            s = streams[p % len(streams)]
            for b in range(6):
                word = (s << 56) | (seq[s] & 0xFFFFFFFF)
                seq[s] += 1
                yield self.src.data.eq(word)
                yield self.src.user.eq(s)
                yield self.src.valid.eq(1)
                yield
                offered += 1
                if not (yield self.src.ready):
                    dropped += 1        # the wire does not wait
            yield self.src.valid.eq(0)
            for _ in range(gap):
                yield
        # drain time for the FIFO + writer
        for _ in range(depth_drain(pdus)):
            yield
        if result is not None:
            result["offered"] = offered
            result["dropped"] = dropped

    def init(self, n_streams, stride_words=RING_WORDS):
        yield self.dut._base.storage.eq(0)
        yield self.dut._length.storage.eq(RING_WORDS * NB)
        yield self.dut._stride.storage.eq(stride_words * NB)
        yield self.dut._enable.storage.eq(1)
        yield


def depth_drain(pdus):
    return 60 * pdus + 2000


def run(h, gens):
    run_simulation(h, gens, vcd_name=None)


def check(name, cond, detail=""):
    tag = "ok" if cond else "FAIL"
    print(f"  [{tag:4s}] {name}{('  ' + detail) if detail else ''}")
    return 0 if cond else 1


def test_depth16_drops():
    """the silicon failure class must REPRODUCE at depth 16 (sim realism gate)"""
    print("[1] depth=16 + contention -> beats shed (mf52 regression shape)")
    h = Harness(depth=16, n_streams=1)
    res = {}

    def stim():
        yield from h.init(1)
        yield from h.source(pdus=120, gap=100, streams=(0,), result=res)

    run(h, [stim(), h.wb_slave(fast_ack=2, slow_ack=500, slow_every=50)])
    fails = 0
    fails += check("beats offered", res["offered"] == 720, str(res))
    fails += check("drops occurred at depth 16 (reproduces the class)",
                   res["dropped"] > 0, f"dropped={res['dropped']}")
    return fails


def test_depth128_clean():
    """the 80ee795 fix: same contention, depth 128 -> zero drops + intact data"""
    print("[2] depth=128 + same contention -> ZERO drops, byte-exact ring")
    h = Harness(depth=128, n_streams=1)
    res = {}

    def stim():
        yield from h.init(1)
        yield from h.source(pdus=120, gap=100, streams=(0,), result=res)

    run(h, [stim(), h.wb_slave(fast_ack=2, slow_ack=500, slow_every=50)])
    fails = 0
    fails += check("zero drops at depth 128", res["dropped"] == 0,
                   f"dropped={res['dropped']}")
    fails += check("every offered beat reached memory",
                   len(h.writes) == res["offered"],
                   f"writes={len(h.writes)} offered={res['offered']}")
    seq_ok = all(dat & 0xFFFFFFFF == i for i, (_, dat) in enumerate(h.writes))
    fails += check("ring sequence uninterrupted (no holes, no repeats)", seq_ok)
    return fails


def test_nxn_routing():
    """4-stream tuser routing: the layout truth the ALSA driver consumes"""
    print("[3] depth=128, 4 streams -> per-stream sub-rings + offset CSRs")
    h = Harness(depth=128, n_streams=4)
    res = {}

    def stim():
        yield from h.init(4)
        yield from h.source(pdus=96, gap=100, streams=(0, 1, 2, 3), result=res)
        # offset CSR readback per stream (the hw_ptr source the driver polls)
        for s in range(4):
            yield h.dut._sel.storage.eq(s)
            yield
            yield
            res[f"off{s}"] = (yield h.dut._offset.status)

    run(h, [stim(), h.wb_slave(fast_ack=2, slow_ack=500, slow_every=50)])
    fails = 0
    fails += check("zero drops", res["dropped"] == 0, f"dropped={res['dropped']}")
    per = {s: [] for s in range(4)}
    for adr, dat in h.writes:
        s = adr // RING_WORDS
        per[s].append((adr % RING_WORDS, dat))
    for s in range(4):
        seq_ok = all(dat & 0xFFFFFFFF == i and (dat >> 56) == s and off == i % RING_WORDS
                     for i, (off, dat) in enumerate(per[s]))
        fails += check(f"stream {s}: {len(per[s])} beats at base+{s}*stride, in order",
                       seq_ok and len(per[s]) == 96 // 4 * 6)
        fails += check(f"stream {s}: offset CSR = beats*8 mod ring",
                       res[f"off{s}"] == (len(per[s]) * NB) % (RING_WORDS * NB),
                       f"csr={res[f'off{s}']}")
    return fails


if __name__ == "__main__":
    fails = 0
    fails += test_depth16_drops()
    fails += test_depth128_clean()
    fails += test_nxn_routing()
    print(f"pcm_ring: {'PASS' if fails == 0 else f'{fails} FAILURES'}")
    sys.exit(1 if fails else 0)
