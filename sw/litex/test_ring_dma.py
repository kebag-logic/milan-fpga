#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Unit-sim of RingDMAWriter v2 (AXI burst master + always-ready drop-FIFO ingress).

Regressions encoded here (each caught or nearly-shipped a silicon bug):
  * always-ready: sink.ready must be 1 EVERY cycle — v1 backpressured LiteEth and the
    un-stallable GMII side silently lost mid-frame beats (frames > ~700 B were 100% lost);
  * mid-frame bubbles: v1's un-gated wishbone cycle wrote stale sink.data during valid=0
    gaps (never caught: the v1 sim source never bubbled);
  * slow drain: frames must be dropped WHOLE (dropped counter) and every committed frame
    must be intact — no merges, seq contiguous;
  * ring full: buffered frame discarded, dropped++, committed region untouched;
  * wrap + AXI rules: bursts split at the ring end and 4 KB boundaries, awlen matches
    the W beat count, wlast on the final beat only;
  * commit-after-B: wr_ptr only moves once every B of the frame arrived.

Run: cd sw/litex && python3 test_ring_dma.py
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

BASE = 0x10000


class Harness:
    """One DUT + AXI-slave memory model + always-ready monitor, driven per scenario."""
    def __init__(self, ring_size, fifo_beats=64, max_frame_beats=16, burst_beats=4,
                 aw_stall=0, w_stall=0, b_delay=2, cycles=6000):
        self.ring = ring_size
        self.dut = msoc.RingDMAWriter(
            axi.AXIInterface(data_width=64, address_width=32, id_width=4),
            max_frame_beats=max_frame_beats, fifo_beats=fifo_beats, burst_beats=burst_beats)
        self.mem = {}            # byte addr (8-aligned) -> 64-bit word
        self.aw_stall, self.w_stall, self.b_delay = aw_stall, w_stall, b_delay
        self.cycles = cycles
        self.errors = []
        self.done = False

    # ---- AXI slave: sequential AW -> W xblen -> B, with protocol checks -------------
    def axi_slave(self):
        bus = self.dut.bus
        for _ in range(self.cycles):
            if self.done:
                return
            if (yield bus.aw.valid):
                for _ in range(self.aw_stall):
                    yield
                addr = (yield bus.aw.addr)
                blen = (yield bus.aw.len) + 1
                if (yield bus.aw.size) != 3:
                    self.errors.append("awsize != 3")
                # AXI rule: a burst must not cross a 4 KB boundary
                if (addr & ~0xFFF) != ((addr + 8 * blen - 1) & ~0xFFF):
                    self.errors.append(f"burst crosses 4K @0x{addr:x} len{blen}")
                yield bus.aw.ready.eq(1)
                yield
                yield bus.aw.ready.eq(0)
                got = 0
                while got < blen:
                    for _ in range(self.w_stall):
                        yield                      # w.ready is low during stalls
                    yield bus.w.ready.eq(1)
                    yield
                    while not (yield bus.w.valid):
                        yield
                    _d = (yield bus.w.data)
                    _st = (yield bus.w.strb)
                    if _st == 0xFF:
                        self.mem[addr + 8 * got] = _d
                    else:                          # partial write: merge by strb
                        _m = 0
                        for _i in range(8):
                            if _st & (1 << _i):
                                _m |= 0xFF << (8 * _i)
                        _o = self.mem.get(addr + 8 * got, 0)
                        self.mem[addr + 8 * got] = (_o & ~_m) | (_d & _m)
                    is_last = (yield bus.w.last)
                    got += 1
                    if is_last != (1 if got == blen else 0):
                        self.errors.append(f"wlast at beat {got}/{blen}")
                    yield bus.w.ready.eq(0)        # exactly one beat per handshake
                for _ in range(self.b_delay):
                    yield
                yield bus.b.valid.eq(1)
                yield
                if not (yield bus.b.ready):
                    self.errors.append("b.ready low")
                yield bus.b.valid.eq(0)
            else:
                yield

    # ---- the always-ready invariant ---------------------------------------------------
    def ready_monitor(self):
        for _ in range(self.cycles):
            if self.done:
                return
            if not (yield self.dut.sink.ready):
                self.errors.append("sink.ready dropped low")
                return
            yield

    # ---- frame feeder: optional mid-frame bubbles -------------------------------------
    def send_frame(self, words, bubbles=0.0, rng=None):
        dut = self.dut
        for i, w in enumerate(words):
            while rng and bubbles and rng.random() < bubbles:
                yield dut.sink.valid.eq(0)
                yield
            yield dut.sink.data.eq(w)
            yield dut.sink.last.eq(1 if i == len(words) - 1 else 0)
            yield dut.sink.valid.eq(1)
            yield
        yield dut.sink.valid.eq(0)
        yield dut.sink.last.eq(0)

    def init_csr(self, rd=0):
        dut = self.dut
        yield dut.base.storage.eq(BASE)
        yield dut.mask.storage.eq(self.ring - 1)
        yield dut.enable.storage.eq(1)
        yield dut.rd_ptr.storage.eq(rd)
        yield

    def wait_idle(self, settle=80):
        """Wait until nothing is buffered AND wr_ptr has been stable for `settle` cycles
        (covers frames still in the AXI FSM after the FIFOs drained)."""
        last, stable = None, 0
        for _ in range(self.cycles):
            lvl = (yield self.dut.data_fifo.level)
            pend = (yield self.dut.len_fifo.level)
            wr = (yield self.dut.wr_ptr.status)
            stable = stable + 1 if (lvl == 0 and pend == 0 and wr == last) else 0
            last = wr
            if stable >= settle:
                return
            yield

    # ---- ring readback helpers ---------------------------------------------------------
    def ring_word(self, off):
        return self.mem.get(BASE + (off & (self.ring - 1)), None)

    @staticmethod
    def csum_ref(words):
        """Ones-complement sum of 16-bit LE lanes — what the ingress must deliver."""
        s = 0
        for w in words:
            for k in range(4):
                s += (w >> (16 * k)) & 0xFFFF
        while s >> 16:
            s = (s & 0xFFFF) + (s >> 16)
        return s

    def read_frames(self, rd, count):
        """Walk `count` committed frames from ring offset rd; return (frames, seqs, rd).
        Verifies each header's CHECKSUM_COMPLETE field against the stored payload."""
        frames, seqs = [], []
        for _ in range(count):
            hdr = self.ring_word(rd)
            assert hdr is not None, f"no header @+0x{rd:x}"
            length = hdr & 0xFFFF
            seqs.append((hdr >> 16) & 0xFFFF)
            assert length % 8 == 0 and length > 0, f"bad length {length}"
            words = []
            for k in range(length // 8):
                words.append(self.ring_word(rd + 8 + 8 * k))
            hw_csum = (hdr >> 32) & 0xFFFF
            assert hw_csum == self.csum_ref(words), \
                f"csum mismatch @+0x{rd:x}: hw {hw_csum:#x} != ref {self.csum_ref(words):#x}"
            frames.append(words)
            rd = (rd + 8 + length) & (self.ring - 1)
        return frames, seqs, rd

    def run(self, stim):
        def wrapped():
            yield from stim()
            self.done = True
        run_simulation(self.dut, [wrapped(), self.axi_slave(), self.ready_monitor()])
        assert not self.errors, self.errors


def frame(tag, nbeats):
    return [(tag << 48) | b for b in range(nbeats)]


# ---- 1. basic commit + content + header-in-burst + commit-after-B ----------------------
def test_basic():
    h = Harness(ring_size=4096)
    F1, F2 = frame(0xA1, 3), frame(0xB2, 7)

    def stim():
        yield from h.init_csr()
        yield from h.send_frame(F1)
        yield from h.send_frame(F2)
        yield from h.wait_idle()
        assert (yield h.dut.wr_ptr.status) == (8 + 24) + (8 + 56), "wr_ptr"
        assert (yield h.dut.dropped.status) == 0
    h.run(stim)
    frames, seqs, _ = h.read_frames(0, 2)
    assert frames == [F1, F2], f"payload mismatch: {frames}"
    assert seqs == [0, 1], f"seq: {seqs}"
    print("PASS basic commit/content/seq")


# ---- 2. mid-frame bubbles (the v1 stale-data bug) ---------------------------------------
def test_bubbles():
    h = Harness(ring_size=4096)
    rng = random.Random(7)
    F = [frame(0xC0 + i, 5) for i in range(4)]

    def stim():
        yield from h.init_csr()
        for f in F:
            yield from h.send_frame(f, bubbles=0.6, rng=rng)
        yield from h.wait_idle()
        assert (yield h.dut.dropped.status) == 0
    h.run(stim)
    frames, seqs, _ = h.read_frames(0, 4)
    assert frames == F, "bubbled frames corrupted"
    assert seqs == [0, 1, 2, 3]
    print("PASS mid-frame bubbles")


# ---- 3. slow drain -> whole-frame ingress drops, survivors intact ----------------------
def test_slow_drain_drops():
    # tiny ingress FIFO (2 frames' worth) + a very slow AXI slave
    h = Harness(ring_size=65536, fifo_beats=16, max_frame_beats=8, burst_beats=4,
                aw_stall=20, w_stall=6, b_delay=20, cycles=20000)
    N, LEN = 12, 6
    F = [frame(0x10 + i, LEN) for i in range(N)]

    def stim():
        yield from h.init_csr()
        for f in F:
            yield from h.send_frame(f)     # back-to-back, no gaps
        yield from h.wait_idle(settle=500)
        drops = (yield h.dut.dropped.status)
        wr = (yield h.dut.wr_ptr.status)
        committed = wr // (8 + LEN * 8)
        assert drops > 0, "expected ingress drops with slow AXI"
        assert committed + drops == N, f"{committed}+{drops} != {N}"
        h.n_committed = committed
    h.run(stim)
    frames, seqs, _ = h.read_frames(0, h.n_committed)
    # every survivor must be one of the sent frames, INTACT (no merges/truncation)
    for f in frames:
        assert f in F, f"corrupt survivor: {[hex(w) for w in f]}"
        assert len(f) == LEN
    assert seqs == list(range(h.n_committed)), f"seq gap: {seqs}"
    print(f"PASS slow-drain drops ({h.n_committed} committed, {N - h.n_committed} dropped whole)")


# ---- 4. ring full -> DISCARD, committed region untouched --------------------------------
def test_ring_full():
    h = Harness(ring_size=128)   # tiny ring: 2 frames of 3 beats fill it
    F = [frame(0xD0 + i, 3) for i in range(4)]

    def stim():
        yield from h.init_csr(rd=0)      # rd never advances
        for f in F:
            yield from h.send_frame(f)
            yield from h.wait_idle()
        drops = (yield h.dut.dropped.status)
        wr = (yield h.dut.wr_ptr.status)
        assert wr == 3 * 32, f"wr {wr}"          # 3 frames of (8+24) fit in 128 (8 spare)
        assert drops == 1, f"drops {drops}"
    h.run(stim)
    frames, seqs, _ = h.read_frames(0, 3)
    assert frames == F[:3] and seqs == [0, 1, 2]
    print("PASS ring-full discard")


# ---- 5. wrap + 4 KB splits + rd release --------------------------------------------------
def test_wrap():
    h = Harness(ring_size=128, burst_beats=16)
    F1, F2, F3 = frame(0xE1, 8), frame(0xE2, 4), frame(0xE3, 4)

    def stim():
        yield from h.init_csr()
        yield from h.send_frame(F1)      # 72 B @0
        yield from h.send_frame(F2)      # 40 B @72..111
        yield from h.wait_idle()
        h.snap = dict(h.mem)             # F3 will overwrite released F1 space
        # release consumed space, then a third frame wraps over old F1
        yield h.dut.rd_ptr.storage.eq((yield h.dut.wr_ptr.status))
        yield
        yield from h.send_frame(F3)      # 40 B @112 -> wraps to 0..23
        yield from h.wait_idle()
        assert (yield h.dut.dropped.status) == 0
    h.run(stim)
    final, h.mem = h.mem, h.snap
    frames, seqs, rd = h.read_frames(0, 2)
    assert frames == [F1, F2] and seqs == [0, 1], "pre-wrap frames corrupted"
    h.mem = final
    frames3, seqs3, _ = h.read_frames(rd, 1)
    assert frames3 == [F3] and seqs3 == [2], "wrapping frame corrupted"
    print("PASS wrap + rd-release")


# ---- 6. 4 KB boundary split (base offset makes a burst straddle) ------------------------
def test_4k_split():
    h = Harness(ring_size=8192, burst_beats=16, cycles=60000)
    # 16-beat frame; base=0x10000 (4K-aligned) so offset 0xFC0.. straddles 0x1000
    F = frame(0xF4, 15)

    def stim():
        yield from h.init_csr()
        # park wr near the 4K line by feeding filler frames the reader consumes
        filler = frame(0x01, 15)
        for _ in range(31):              # 31*(8+120)=3968 -> next frame @0xF80
            yield from h.send_frame(filler)
            yield from h.wait_idle(settle=40)
            yield h.dut.rd_ptr.storage.eq((yield h.dut.wr_ptr.status))
            yield
        yield from h.send_frame(F)       # header @0xF80, payload crosses 0x1000
        yield from h.wait_idle()
        assert (yield h.dut.dropped.status) == 0
        h.rd0 = 31 * 128
    h.run(stim)
    frames, seqs, _ = h.read_frames(h.rd0, 1)
    assert frames == [F], "4K-straddling frame corrupted"
    print("PASS 4 KB burst split")   # slave asserts the no-crossing rule itself


if __name__ == "__main__":
    test_basic()
    test_bubbles()
    test_slow_drain_drops()
    test_ring_full()
    test_wrap()
    test_4k_split()
    print("ALL PASS")
