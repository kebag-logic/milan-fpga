#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Sim verification of the RingDMAReader TX-BD (descriptor zero-copy) mode — P5 v1.

Proven BEFORE a bitstream:
  1. Single-segment frame: payload streamed byte-exact from an arbitrary 8-aligned
     address, exact-length last-beat keep, `rd` advances 16/BD, sent++.
  2. Multi-segment frame (staged header + page frag): one AXIS frame — `last` ONLY on
     the EOF segment's final beat; mid segment (len%8==0 contract) keeps 0xFF.
  3. Bad BD (len 0/oversize): resync rd:=wr, second BD word drained, nothing streamed.
  4. BD ring wrap + enable-off rd reset (reload hygiene).

Run: cd sw/litex && /home/alex/litex-milan/venv/bin/python3 test_tx_bd.py
"""
import sys, importlib.util
from migen import *
from litex.gen import *

sys.path.insert(0, ".")
spec = importlib.util.spec_from_file_location("ttx", "./test_ring_tx.py")
ttx = importlib.util.module_from_spec(spec); sys.modules["ttx"] = ttx
spec.loader.exec_module(ttx)
Harness = ttx.Harness

BD_BASE = 0x40000               # BD ring
SEG_A   = 0x50000               # segment buffers (8-aligned)
SEG_B   = 0x58000


class BDHarness(Harness):
    def init_bd(self, entries=8):
        dut = self.dut
        yield dut.bd_base.storage.eq(BD_BASE)
        yield dut.mask.storage.eq(entries * 16 - 1)
        yield dut.enable.storage.eq(1)
        yield

    def put_bd(self, idx, addr, length, eof):
        w0 = (addr & 0xFFFFFFFF) | (length << 32) | ((1 if eof else 0) << 48)
        self.mem[BD_BASE + 16 * idx] = w0
        self.mem[BD_BASE + 16 * idx + 8] = 0

    def put_seg(self, addr, data_bytes):
        # pad the tail with 0xEE (NOT zero): real DRAM beyond a segment is nonzero —
        # a shifter that fails to mask tail garbage must fail these tests.
        words = [int.from_bytes(data_bytes[i:i+8].ljust(8, b'\xee'), 'little')
                 for i in range(0, len(data_bytes), 8)]
        for k, w in enumerate(words):
            self.mem[addr + 8 * k] = w
        self.mem[addr + 8 * len(words)] = 0xEEEEEEEEEEEEEEEE

    def rx_bytes(self):
        out = b''
        for d, k, l in self.beats:
            for i in range(8):
                if k & (1 << i):
                    out += bytes([(d >> (8 * i)) & 0xFF])
        return out


def test_bd_single_segment():
    h = BDHarness(ring_size=4096)
    pay = bytes(range(1, 61))            # 60 B — exact keep on the last beat

    def stim():
        yield from h.init_bd()
        h.put_seg(SEG_A, pay)
        h.put_bd(0, SEG_A, len(pay), eof=True)
        yield h.dut.wr_ptr.storage.eq(16)         # doorbell: 1 BD queued
        yield
        for _ in range(600):
            if (yield h.dut.sent.status) == 1:
                break
            yield
        assert (yield h.dut.sent.status) == 1
        assert (yield h.dut.rd_ptr.status) == 16
    h.run(stim)
    assert h.rx_bytes() == pay, "payload mismatch"
    lasts = [l for _, _, l in h.beats]
    assert lasts == [0] * (len(h.beats) - 1) + [1], "last only on final beat"
    print("PASS TX-BD single segment (byte-exact, keep, rd+16)")


def test_bd_multi_segment():
    h = BDHarness(ring_size=4096)
    hdrp = bytes(range(0x40, 0x40 + 56))          # 56 B header seg (%8==0, non-EOF)
    frag = bytes((i * 7) & 0xFF for i in range(1000))   # 1000 B frag (EOF, odd tail)

    def stim():
        yield from h.init_bd()
        h.put_seg(SEG_A, hdrp)
        h.put_seg(SEG_B, frag)
        h.put_bd(0, SEG_A, len(hdrp), eof=False)
        h.put_bd(1, SEG_B, len(frag), eof=True)
        yield h.dut.wr_ptr.storage.eq(32)         # doorbell: both BDs queued
        yield
        for _ in range(2500):
            if (yield h.dut.sent.status) == 1:
                break
            yield
        assert (yield h.dut.sent.status) == 1, "frame not sent"
        assert (yield h.dut.rd_ptr.status) == 32
    h.run(stim)
    assert h.rx_bytes() == hdrp + frag, "stitched frame mismatch"
    lasts = [l for _, _, l in h.beats]
    assert sum(lasts) == 1 and lasts[-1] == 1, "exactly one last, at the end"
    print("PASS TX-BD multi segment (header+frag stitched, one last)")


def test_bd_bad_descriptor():
    h = BDHarness(ring_size=4096)

    def stim():
        yield from h.init_bd()
        h.put_bd(0, SEG_A, 0, eof=True)           # len 0 = software bug
        yield h.dut.wr_ptr.storage.eq(16)
        yield
        for _ in range(300):
            yield
        assert (yield h.dut.sent.status) == 0
        assert (yield h.dut.rd_ptr.status) == 16, "must resync rd to wr"
    h.run(stim)
    assert h.beats == [], "nothing may be streamed for a bad BD"
    print("PASS TX-BD bad-descriptor resync")


def test_bd_wrap_and_disable():
    h = BDHarness(ring_size=4096, cycles=20000)
    pay = bytes(range(64))

    def stim():
        yield from h.init_bd(entries=4)           # 64 B BD ring
        h.put_seg(SEG_A, pay)
        for i in range(6):                        # 6 BDs through a 4-entry ring
            h.put_bd(i % 4, SEG_A, len(pay), eof=True)
            yield h.dut.wr_ptr.storage.eq(((i + 1) * 16) & 63)
            yield
            for _ in range(800):
                if (yield h.dut.sent.status) == i + 1:
                    break
                yield
            assert (yield h.dut.sent.status) == i + 1, f"frame {i} stuck"
        yield h.dut.enable.storage.eq(0)          # reload hygiene: rd resets
        for _ in range(8):
            yield
        assert (yield h.dut.rd_ptr.status) == 0, "rd must reset on disable"
    h.run(stim)
    print("PASS TX-BD ring wrap + disable-reset")


def test_bd_unaligned_offsets():
    """v2 realign: segment addresses at every offset 0..7 (Ethernet's skb->data is
    ≡2 mod 8 essentially always — o=2 is THE production case), including the 1-input
    'DRAIN-only' segment (o+len <= 8) and a >1-burst segment (carry across bursts)."""
    for off in range(8):
        for length in (6, 60, 1000, 1514):
            if off + length <= 8 and length > 6:
                continue
            h = BDHarness(ring_size=4096, cycles=40000)
            pay = bytes(((i * 13) ^ off) & 0xFF for i in range(length))

            def stim(h=h, pay=pay, off=off):
                yield from h.init_bd()
                base = SEG_A + off
                # place the payload at the unaligned address
                blob = b'\xEE' * off + pay
                h.put_seg(SEG_A, blob)
                h.put_bd(0, base, len(pay), eof=True)
                yield h.dut.wr_ptr.storage.eq(16)
                yield
                for _ in range(6000):
                    if (yield h.dut.sent.status) == 1:
                        break
                    yield
                assert (yield h.dut.sent.status) == 1, f"stuck o={off} len={len(pay)}"
            h.run(stim)
            assert h.rx_bytes() == pay, f"payload mismatch o={off} len={length}"
    print("PASS TX-BD unaligned offsets (o=0..7 x lengths incl. drain + multi-burst)")


def _csum_ref(data: bytes) -> int:
    """16-bit LE-lane ones-complement sum, folded (the engine's convention)."""
    if len(data) & 1:
        data += b'\x00'
    t = 0
    for i in range(0, len(data), 2):
        t += data[i] | (data[i + 1] << 8)
    while t >> 16:
        t = (t & 0xFFFF) + (t >> 16)
    return (~t) & 0xFFFF


def test_bd_csum_insert():
    """v2b HW checksum-insert: BD w1 {en<<63, off<<16}; the engine pre-passes the
    segment, folds the ones-complement sum (csum field pre-seeded like checksum_help
    expects), and patches the folded value into bytes [off, off+2). Tested across
    offsets/alignments incl. the o=2 Ethernet case."""
    for off in (0, 2):
        for length, csoff in ((60, 40), (1000, 50), (1514, 50)):
            h = BDHarness(ring_size=4096, cycles=60000)
            pay = bytearray(((i * 11) ^ 0x5A) & 0xFF for i in range(length))
            pay[csoff:csoff + 2] = b'\x34\x12'          # seeded csum field
            pay = bytes(pay)

            def stim(h=h, pay=pay, off=off, csoff=csoff):
                yield from h.init_bd()
                h.put_seg(SEG_A, b'\xEE' * off + pay)
                w0 = ((SEG_A + off) & 0xFFFFFFFF) | (len(pay) << 32) | (1 << 48)
                h.mem[BD_BASE] = w0
                h.mem[BD_BASE + 8] = (1 << 63) | (csoff << 16)   # en + csum_off
                yield h.dut.wr_ptr.storage.eq(16)
                yield
                for _ in range(9000):
                    if (yield h.dut.sent.status) == 1:
                        break
                    yield
                assert (yield h.dut.sent.status) == 1, f"stuck o={off} len={len(pay)}"
            h.run(stim)
            got = h.rx_bytes()
            exp_csum = _csum_ref(pay)
            expect = bytearray(pay)
            expect[csoff] = exp_csum & 0xFF
            expect[csoff + 1] = exp_csum >> 8
            assert got == bytes(expect), \
                f"csum patch wrong o={off} len={length}: got {got[csoff:csoff+2].hex()} " \
                f"want {bytes(expect[csoff:csoff+2]).hex()}"
    print("PASS TX-BD HW csum-insert (offsets x lengths, folded+patched correctly)")


def test_bd_arbitrary_chain():
    """Cross-BD continuity: mid-segments of ARBITRARY length (the old %8 contract is
    dead) at arbitrary offsets — one seamless wire frame, byte-exact, exact tail keep.
    This is the SG-enabling property: TCP frags have arbitrary sizes."""
    import random
    random.seed(7)
    for trial in range(4):
        segs = [(random.randrange(8), random.choice([3, 13, 61, 97, 200, 1000]))
                for _ in range(random.randrange(2, 6))]
        h = BDHarness(ring_size=4096, cycles=200000)
        payload = b''
        addr = SEG_A
        for i, (off, ln) in enumerate(segs):
            data = bytes(((i * 29 + k * 7) ^ 0xC3) & 0xFF for k in range(ln))
            h.put_seg(addr, b'\x55' * off + data)
            h.put_bd(i, addr + off, ln, eof=(i == len(segs) - 1))
            payload += data
            addr += 0x1000
        def stim(h=h, n=len(segs)):
            yield from h.init_bd()
            yield h.dut.wr_ptr.storage.eq((16 * n) & 127)
            yield
            for _ in range(30000):
                if (yield h.dut.sent.status) == 1:
                    break
                yield
            assert (yield h.dut.sent.status) == 1, f"trial {trial} stuck"
        h.run(stim)
        got = h.rx_bytes()
        assert got == payload, \
            f"trial {trial} segs={segs}: mismatch at " \
            f"{next(i for i,(a,b) in enumerate(zip(got,payload)) if a!=b)}"
        lasts = [l for _, _, l in h.beats]
        assert sum(lasts) == 1 and lasts[-1] == 1
    print("PASS TX-BD arbitrary-length chains (SG-ready: %8 contract removed)")


if __name__ == "__main__":
    test_bd_single_segment()
    test_bd_multi_segment()
    test_bd_bad_descriptor()
    test_bd_wrap_and_disable()
    test_bd_unaligned_offsets()
    test_bd_csum_insert()
    test_bd_arbitrary_chain()
    print("ALL PASS")
