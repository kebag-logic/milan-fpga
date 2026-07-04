#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Unit-sim of RingDMAReader (TX ring: DRAM ring -> AXIS frames via AXI read bursts).

Covers: exact payload bytes + last-beat keep mask (non-x8 lengths), back-to-back queued
frames, source backpressure mid-frame (PacketFIFO downstream makes this legal), ring
wrap (bursts split at the boundary), the 4 KB AXI rule (slave asserts), header-desync
resync (len==0 -> rd := wr), rd_ptr advance and the sent counter.

Run: cd sw/litex && python3 test_ring_tx.py
"""
import sys, importlib.util, random
from migen import *
from litex.gen import *

sys.path.insert(0, ".")
sys.path.insert(0, "./platforms")
spec = importlib.util.spec_from_file_location("msoc", __file__.rsplit("/", 1)[0] + "/milan_soc.py")
msoc = importlib.util.module_from_spec(spec)
sys.modules["msoc"] = msoc
spec.loader.exec_module(msoc)

from litex.soc.interconnect import axi

BASE = 0x20000


def pack_frame(payload):
    """payload: list of byte values -> (header_word, [payload words], padded_len)"""
    n = len(payload)
    padded = payload + [0] * ((-n) % 8)
    words = []
    for i in range(0, len(padded), 8):
        w = 0
        for j in range(8):
            w |= padded[i + j] << (8 * j)
        words.append(w)
    return n, words


class Harness:
    def __init__(self, ring_size, ar_stall=0, r_stall=0, cycles=8000):
        self.ring = ring_size
        self.dut = msoc.RingDMAReader(
            axi.AXIInterface(data_width=64, address_width=32, id_width=4))
        self.mem = {}                    # byte addr (8-aligned) -> 64-bit word
        self.ar_stall, self.r_stall = ar_stall, r_stall
        self.cycles = cycles
        self.errors = []
        self.done = False
        self.beats = []                  # (data, keep, last) accepted from source

    def put_frame(self, off, payload):
        """Write one frame slot into the ring image at byte offset `off`; return new off."""
        n, words = pack_frame(payload)
        self.mem[BASE + (off & (self.ring - 1))] = n          # header {len}
        for k, w in enumerate(words):
            self.mem[BASE + ((off + 8 + 8 * k) & (self.ring - 1))] = w
        return (off + 8 + 8 * len(words)) & (self.ring - 1)

    # ---- AXI read slave: AR -> R burst from self.mem, with protocol checks ----------
    def axi_slave(self):
        bus = self.dut.bus
        for _ in range(self.cycles):
            if self.done:
                return
            if (yield bus.ar.valid):
                for _ in range(self.ar_stall):
                    yield
                addr = (yield bus.ar.addr)
                blen = (yield bus.ar.len) + 1
                if (yield bus.ar.size) != 3:
                    self.errors.append("arsize != 3")
                if (addr & ~0xFFF) != ((addr + 8 * blen - 1) & ~0xFFF):
                    self.errors.append(f"read burst crosses 4K @0x{addr:x} len{blen}")
                yield bus.ar.ready.eq(1)
                yield
                yield bus.ar.ready.eq(0)
                for i in range(blen):
                    for _ in range(self.r_stall):
                        yield
                    if addr + 8 * i not in self.mem:
                        self.errors.append(f"read of unwritten addr 0x{addr + 8*i:x}")
                    yield bus.r.data.eq(self.mem.get(addr + 8 * i, 0))
                    yield bus.r.last.eq(1 if i == blen - 1 else 0)
                    yield bus.r.valid.eq(1)
                    yield
                    while not (yield bus.r.ready):
                        yield
                yield bus.r.valid.eq(0)
            else:
                yield

    # ---- AXIS sink: collect beats, optional random backpressure ----------------------
    def sink_mon(self, throttle=0.0, rng=None):
        src = self.dut.source
        yield src.ready.eq(1)
        for _ in range(self.cycles):
            if self.done:
                return
            if rng and throttle and rng.random() < throttle:
                yield src.ready.eq(0)
                yield
                yield src.ready.eq(1)
                continue
            yield
            if (yield src.valid):
                self.beats.append(((yield src.data), (yield src.keep), (yield src.last)))

    def init_csr(self, wr=0):
        dut = self.dut
        yield dut.base.storage.eq(BASE)
        yield dut.mask.storage.eq(self.ring - 1)
        yield dut.enable.storage.eq(1)
        yield dut.wr_ptr.storage.eq(wr)
        yield

    def wait_done(self, nframes, settle=60):
        stable = 0
        for _ in range(self.cycles):
            if (yield self.dut.sent.status) >= nframes:
                stable += 1
                if stable >= settle:
                    return
            yield

    def run(self, stim, throttle=0.0, seed=None):
        rng = random.Random(seed) if seed is not None else None
        def wrapped():
            yield from stim()
            self.done = True
        run_simulation(self.dut, [wrapped(), self.axi_slave(),
                                  self.sink_mon(throttle=throttle, rng=rng)])
        assert not self.errors, self.errors

    def frames_from_beats(self):
        """Reassemble collected beats into frames of exact byte lists."""
        frames, cur = [], []
        for data, keep, last in self.beats:
            nbytes = bin(keep).count("1")
            assert keep == (1 << nbytes) - 1, f"non-contiguous keep {keep:#x}"
            for j in range(nbytes):
                cur.append((data >> (8 * j)) & 0xFF)
            if last:
                frames.append(cur)
                cur = []
        assert not cur, "trailing beats without last"
        return frames


def payload(tag, n):
    return [(tag + i) & 0xFF for i in range(n)]


# ---- 1. exact bytes + partial last keep + rd/sent ---------------------------------------
def test_basic():
    h = Harness(ring_size=4096)
    P1, P2 = payload(0x10, 60), payload(0x80, 21)   # 60 = 7.5 beats, 21 = 2.6 beats

    def stim():
        off = 0
        off = h.put_frame(off, P1)
        off = h.put_frame(off, P2)
        yield from h.init_csr(wr=off)
        yield from h.wait_done(2)
        assert (yield h.dut.rd_ptr.status) == off, "rd_ptr"
        assert (yield h.dut.sent.status) == 2
    h.run(stim)
    assert h.frames_from_beats() == [P1, P2], "payload/keep mismatch"
    print("PASS basic exact-length frames")


# ---- 2. source backpressure mid-frame ----------------------------------------------------
def test_backpressure():
    h = Harness(ring_size=4096, cycles=20000)
    F = [payload(0x20 + 7 * i, 100 + i) for i in range(4)]

    def stim():
        off = 0
        for p in F:
            off = h.put_frame(off, p)
        yield from h.init_csr(wr=off)
        yield from h.wait_done(4)
    h.run(stim, throttle=0.5, seed=11)
    assert h.frames_from_beats() == F, "backpressured frames corrupted"
    print("PASS source backpressure")


# ---- 3. wrap: frame crosses the ring end --------------------------------------------------
def test_wrap():
    h = Harness(ring_size=256)
    P1, P2 = payload(0x31, 160), payload(0x42, 60)  # P2 wraps: 168 + 8+64 > 256

    def stim():
        off = 0
        off = h.put_frame(off, P1)     # 8+160 = 168
        off = h.put_frame(off, P2)     # wraps the 256-byte ring
        yield from h.init_csr(wr=off)
        yield from h.wait_done(2)
    h.run(stim)
    assert h.frames_from_beats() == [P1, P2], "wrapping frame corrupted"
    print("PASS ring wrap")


# ---- 4. 4 KB boundary split (slave asserts the rule) --------------------------------------
def test_4k():
    h = Harness(ring_size=8192, cycles=30000)
    P0 = payload(0x01, 2008)           # 2x (8+2008) = 0xFC0: parks the next slot @0xFC0
    P1 = payload(0x02, 2008)           # (2008 <= the reader's 2048 max-frame sanity cap)
    P  = payload(0x55, 200)            # header @0xFC0, payload @0xFC8 -> crosses BASE+0x1000

    def stim():
        off = 0
        off = h.put_frame(off, P0)
        off = h.put_frame(off, P1)
        assert off == 0xFC0, hex(off)
        off = h.put_frame(off, P)
        yield from h.init_csr(wr=off)
        yield from h.wait_done(3)
    h.run(stim)
    assert h.frames_from_beats() == [P0, P1, P], "4K-straddling frame corrupted"
    print("PASS 4 KB burst split")


# ---- 5. desync header -> resync rd := wr ---------------------------------------------------
def test_desync():
    h = Harness(ring_size=4096)

    def stim():
        # a zero header at rd=0 (bug injection), wr far ahead
        h.mem[BASE + 0] = 0
        yield from h.init_csr(wr=512)
        for _ in range(300):
            yield
        assert (yield h.dut.rd_ptr.status) == 512, "resync rd != wr"
        assert (yield h.dut.sent.status) == 0
    h.run(stim)
    assert h.beats == [], "streamed garbage after desync"
    print("PASS desync resync")


if __name__ == "__main__":
    test_basic()
    test_backpressure()
    test_wrap()
    test_4k()
    test_desync()
    print("ALL PASS")
