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


def test_bd_csum_chain():
    """cs-across-BDs (soft-TSO enabler): w1 {en,off} on the chain's FIRST BD makes
    the engine pre-pass the WHOLE chain (accumulator survives BD hops), rewind the
    BD ring, and stream the assembled frame with the folded sum patched at the
    frame-relative csum_off. Shape mirrors the TSO driver: a +2-aligned header BD
    + arbitrary payload BDs. Also proves rd only PUBLISHES at frame end (the
    pre-pass rd excursion must stay invisible to the reaping driver)."""
    import random
    random.seed(11)
    for trial in range(3):
        hdr_len = 66
        csoff = 50                                   # TCP check field, frame-relative
        p1 = random.choice([137, 200, 1000])
        p2 = random.choice([3, 61, 448])
        h = BDHarness(ring_size=4096, cycles=250000)
        hdr = bytearray(((i * 13) ^ 0x77) & 0xFF for i in range(hdr_len))
        hdr[csoff:csoff + 2] = b'\x9a\x04'           # pseudo-header seed
        d1 = bytes(((trial * 31 + k * 3) ^ 0x1F) & 0xFF for k in range(p1))
        d2 = bytes(((trial * 17 + k * 5) ^ 0xA5) & 0xFF for k in range(p2))
        h.put_seg(SEG_A, b'\xEE' * 2 + bytes(hdr))   # +2 arena alignment
        h.put_seg(SEG_B, d1)
        h.put_seg(SEG_B + 0x2000, b'\xEE' * 6 + d2)  # odd offset frag
        h.put_bd(0, SEG_A + 2, hdr_len, eof=False)
        h.mem[BD_BASE + 8] = (1 << 63) | (csoff << 16)   # w1 on the FIRST BD
        h.put_bd(1, SEG_B, p1, eof=False)
        h.put_bd(2, SEG_B + 0x2000 + 6, p2, eof=True)

        def stim(h=h):
            yield from h.init_bd()
            yield h.dut.wr_ptr.storage.eq(48)
            yield
            for _ in range(40000):
                if (yield h.dut.sent.status) == 1:
                    break
                yield
            assert (yield h.dut.sent.status) == 1, "chain-csum frame stuck"
            assert (yield h.dut.rd_ptr.status) == 48, "rd must publish 3 BDs"
        h.run(stim)
        frame = bytes(hdr) + d1 + d2
        exp_csum = _csum_ref(frame)
        expect = bytearray(frame)
        expect[csoff] = exp_csum & 0xFF
        expect[csoff + 1] = exp_csum >> 8
        got = h.rx_bytes()
        assert got == bytes(expect), \
            f"trial {trial}: chain csum mismatch got {got[csoff:csoff+2].hex()} " \
            f"want {bytes(expect[csoff:csoff+2]).hex()} (lens {p1}/{p2})"
    print("PASS TX-BD cs-across-BDs (chain pre-pass + rewind + patch, rd published at EOF)")


def _lanes(data: bytes) -> int:
    """LE-lane 16-bit sum, unfolded (the engine/kernel convention)."""
    if len(data) & 1:
        data += b'\x00'
    return sum(data[i] | (data[i + 1] << 8) for i in range(0, len(data), 2))


def _fold_nc(t: int) -> int:
    while t >> 16:
        t = (t & 0xFFFF) + (t >> 16)
    return t


def _ip_check(hdr20: bytes) -> int:
    """classical BE IP header checksum (returns the two wire bytes as an int)."""
    t = sum((hdr20[i] << 8) | hdr20[i + 1] for i in range(0, 20, 2))
    while t >> 16:
        t = (t & 0xFFFF) + (t >> 16)
    return (~t) & 0xFFFF


def _mk_template(mss, seq0, thlen=20, flags=0x10):
    """eth+IPv4+TCP template as the DRIVER builds it: tot_len/check for a full-mss
    segment, tcp.check=0, flags already masked for a FIRST segment."""
    eth = bytes([0x02,0,0,0,0,1, 0x02,0,0,0,0,2, 0x08,0x00])
    tot = 20 + thlen + mss
    ip = bytearray([0x45,0, tot>>8, tot&0xFF, 0x13,0x37, 0x40,0, 64,6, 0,0,
                    192,168,127,2, 192,168,127,1])
    ck = _ip_check(bytes(ip))
    ip[10] = ck >> 8; ip[11] = ck & 0xFF
    tcp = bytes([0x14,0x51, 0x14,0x51,
                 (seq0>>24)&0xFF,(seq0>>16)&0xFF,(seq0>>8)&0xFF,seq0&0xFF,
                 0,0,0,0, ((thlen//4)<<4), flags, 0x20,0, 0,0, 0,0]) \
          + bytes(thlen - 20)
    return eth + bytes(ip) + tcp


def _tso_reference(tmpl, payload, mss, seq0, fmid, flast):
    """expected wire frames + the driver-side descriptor constants, all checksums
    computed CLASSICALLY — independently validating the P-seed algebra."""
    hlen = len(tmpl)
    thlen = hlen - 34
    frames = []
    off = 0
    k = 0
    chunk_last = len(payload) - (len(payload) - 1) // mss * mss
    lenlast = 20 + thlen + chunk_last
    iplast = bytearray(tmpl[14:34])
    iplast[2] = lenlast >> 8; iplast[3] = lenlast & 0xFF
    iplast[10] = iplast[11] = 0
    cklast = _ip_check(bytes(iplast))
    while off < len(payload):
        chunk = min(mss, len(payload) - off)
        last = (off + chunk == len(payload))
        hdr = bytearray(tmpl)
        if last:
            hdr[16] = lenlast >> 8; hdr[17] = lenlast & 0xFF
            hdr[24] = cklast >> 8;  hdr[25] = cklast & 0xFF
        if k > 0:
            sq = (seq0 + off) & 0xFFFFFFFF
            hdr[38:42] = sq.to_bytes(4, 'big')
            hdr[47] = flast if last else fmid
        pay = payload[off:off + chunk]
        # classical TCP checksum (BE) -> stored LE-lane like the engine patches it
        pseudo = tmpl[26:34] + bytes([0, 6]) + (thlen + chunk).to_bytes(2, 'big')
        t = _lanes(pseudo) + _lanes(bytes(hdr[34:])) + _lanes(pay)
        ck = (~_fold_nc(t)) & 0xFFFF
        hdr[50] = ck & 0xFF; hdr[51] = ck >> 8
        frames.append(bytes(hdr) + pay)
        off += chunk
        k += 1
    # descriptor constants exactly as the driver computes them
    def P(seg_hdr34, tcplen):
        pseudo = tmpl[26:34] + bytes([0, 6]) + tcplen.to_bytes(2, 'big')
        return (_lanes(pseudo) + ((~_fold_nc(_lanes(seg_hdr34))) & 0xFFFF)) & 0xFFFFFFFF
    hdr_last34 = bytes(tmpl[:16]) + bytes([lenlast >> 8, lenlast & 0xFF]) + \
                 tmpl[18:24] + bytes([cklast >> 8, cklast & 0xFF]) + tmpl[26:34]
    return (frames, P(tmpl[:34], thlen + mss), P(hdr_last34, thlen + chunk_last),
            lenlast, cklast)


def test_tso_hw():
    """HW header-generation TSO: ONE descriptor pair + frag payload BDs -> N wire
    frames, byte-exact incl. IP/TCP checksums computed classically (independent
    check of the P-seed algebra). Covers short last segment, exact-mss tail, frag
    boundaries inside segments, a frag spanning segments, and doff=8 templates."""
    import random
    random.seed(23)
    cases = [
        dict(mss=200, pay=520,  frags=[520],           thlen=20),  # short last
        dict(mss=160, pay=480,  frags=[480],           thlen=20),  # exact tail
        dict(mss=176, pay=600,  frags=[100, 260, 240], thlen=32),  # frags x segs
        dict(mss=120, pay=444,  frags=[371, 73],       thlen=20),  # frag spans segs
    ]
    for ci, c in enumerate(cases):
        mss, thlen = c['mss'], c['thlen']
        seq0 = 0x11220000 + ci
        tmpl = _mk_template(mss, seq0, thlen=thlen, flags=0x10)
        hlen = len(tmpl)
        payload = bytes(((ci * 37 + i * 3) ^ 0xA7) & 0xFF for i in range(c['pay']))
        fmid, flast = 0x10, 0x18                     # PSH only on the last segment
        frames, Pf, Pl, lenlast, cklast = _tso_reference(tmpl, payload, mss,
                                                         seq0, fmid, flast)
        h = BDHarness(ring_size=4096, cycles=600000)
        h.put_seg(SEG_A, b'\xEE' * 2 + tmpl)         # +2 arena alignment
        addr = SEG_B
        fbds = []
        off = 0
        for fl in c['frags']:
            o = random.randrange(8)
            h.put_seg(addr, b'\xEE' * o + payload[off:off + fl])
            fbds.append((addr + o, fl))
            off += fl
            addr += 0x2000
        assert off == len(payload)

        def stim(h=h, fbds=fbds, mss=mss, pay=len(payload), hlen=hlen,
                 Pf=Pf, Pl=Pl, lenlast=lenlast, cklast=cklast, seq0=seq0,
                 nseg=len(frames)):
            yield from h.init_bd(entries=16)
            h.mem[BD_BASE + 0] = (SEG_A + 2) | (hlen << 32) | (1 << 49)
            h.mem[BD_BASE + 8] = mss | (pay << 16) | (0x10 << 32) | (0x18 << 40)
            h.mem[BD_BASE + 16] = Pf | (Pl << 32)
            h.mem[BD_BASE + 24] = lenlast | (cklast << 16) | (seq0 << 32)
            for i, (fa, fl) in enumerate(fbds):
                h.put_bd(2 + i, fa, fl, eof=(i == len(fbds) - 1))
            yield h.dut.wr_ptr.storage.eq((2 + len(fbds)) * 16)
            yield
            for _ in range(120000):
                if (yield h.dut.sent.status) == nseg:
                    break
                yield
            assert (yield h.dut.sent.status) == nseg, \
                f"case {ci}: sent {(yield h.dut.sent.status)}/{nseg}"
            assert (yield h.dut.rd_ptr.status) == (2 + len(fbds)) * 16, "rd publish"
        h.run(stim, throttle=(0.3 if ci == 2 else 0.0), seed=5)
        got = h.rx_bytes()
        exp = b''.join(frames)
        assert len(got) == len(exp), f"case {ci}: len {len(got)} != {len(exp)}"
        if got != exp:
            bad = next(i for i, (a, b) in enumerate(zip(got, exp)) if a != b)
            raise AssertionError(f"case {ci}: byte {bad}: got {got[bad]:#x} "
                                 f"want {exp[bad]:#x}")
        lasts = sum(l for _, _, l in h.beats)
        assert lasts == len(frames), f"case {ci}: {lasts} frames"
    print("PASS HW-TSO (descriptor -> N frames, classical csums, frags x segments)")


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
    test_bd_csum_chain()
    test_tso_hw()
    test_bd_arbitrary_chain()
    print("ALL PASS")
