#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Sim verification of RxSteer — the 2-way RX steering front-end (gPTP vs rest).

USER directive 2026-07-26: two ingress queues, "one dedicated to gPTP, one for
everything else". RxSteer used to be a TCP 4-tuple flow hash; the trade-off that
replaced it is written up in docs/reference/EGRESS_QUEUE_MAP.md.

Proven BEFORE a bitstream:
  1. A gPTP frame (DMAC 01-80-C2-00-00-0E + EtherType 0x88F7) lands on q1,
     byte-exact, and on q1 ONLY.
  2. Same for a C-TAGged gPTP frame (0x8100 outer, 0x88F7 inner).
  3. NEGATIVE: 0x88F7 at a foreign DMAC does NOT reach q1 (the REQ-CLS-07 rule
     applied on ingress) — a spoofed sync cannot occupy the PTP queue.
  4. NEGATIVE: the reserved DMAC with a non-PTP EtherType does NOT reach q1.
  5. Bulk TCP/IP goes to q0 — and ALL of it does, i.e. the 4-tuple hash really
     is gone (frames that used to split now share one queue).
  6. hash_sel=1 forces everything, gPTP included, to q0 (bypass).
  7. Interleaved gPTP/bulk keeps both queues byte-exact and in order.
  8. A frame that ends inside the 3-beat head takes q0 (a runt cannot be a valid
     gPTP PDU; the smallest is 60 B on the wire).

Run: cd sw/litex && python3 test_rx_steer.py   (from your LiteX venv)
"""
import sys, importlib.util
from migen import *
from litex.gen import *

sys.path.insert(0, ".")
spec = importlib.util.spec_from_file_location("msoc", "./milan_soc.py")
msoc = importlib.util.module_from_spec(spec); sys.modules["msoc"] = msoc
spec.loader.exec_module(msoc)
RxSteer = msoc.RxSteer

GPTP_DMAC = [0x01, 0x80, 0xC2, 0x00, 0x00, 0x0E]   # 802.1AS-2020 §10.5 reserved
SMAC      = [0x02, 0x00, 0x00, 0x00, 0x00, 0x02]


def _pad8(blob):
    return blob + bytes((-len(blob)) % 8)


def ptp_frame(dmac=None, etype=0x88F7, tagged=False, paylen=44):
    """An 802.1AS event message shape: DMAC + SMAC + [C-TAG] + etype + payload."""
    dmac = GPTP_DMAC if dmac is None else dmac
    blob = bytes(dmac) + bytes(SMAC)
    if tagged:
        blob += bytes([0x81, 0x00, 0x60, 0x02])            # C-TAG, PCP 3, VID 2
    blob += bytes([etype >> 8, etype & 0xFF])
    # PTPv2 common header shape (Sync): msg type 0x00, version 2, ...
    hdr = bytes([0x00, 0x02, 0x00, 0x2C, 0x00, 0x00, 0x02, 0x00])
    blob += hdr + bytes((i * 13) & 0xFF for i in range(paylen))
    return _pad8(blob)


def tcp_frame(sip, dip, sport, dport, paylen=40):
    eth = bytes([0x02, 0, 0, 0, 0, 1, 0x02, 0, 0, 0, 0, 2, 0x08, 0x00])
    doff = 5
    tot = 20 + doff * 4 + paylen
    ip = bytes([0x45, 0, tot >> 8, tot & 0xFF, 0, 0, 0x40, 0, 64, 6, 0, 0]) \
        + bytes(sip) + bytes(dip)
    tcp = bytes([sport >> 8, sport & 0xFF, dport >> 8, dport & 0xFF, 0, 0, 0, 0,
                 0, 0, 0, 0, (doff << 4), 0x10, 0x20, 0, 0, 0, 0, 0])
    return _pad8(eth + ip + tcp + bytes((i * 7) & 0xFF for i in range(paylen)))


def arp_frame():
    return _pad8(bytes([0xff] * 6 + SMAC + [0x08, 0x06]) + bytes(28))


class H:
    def __init__(self, cycles=20000):
        self.dut = RxSteer(depth=64)
        self.cycles = cycles
        self.q = [[], []]      # collected beats per queue: (data, keep, last)

    def send(self, blob):
        d = self.dut
        for i in range(0, len(blob), 8):
            w = int.from_bytes(blob[i:i+8].ljust(8, b'\x00'), "little")
            last = 1 if i + 8 >= len(blob) else 0
            yield d.sink.data.eq(w)
            yield d.sink.keep.eq(0xFF)
            yield d.sink.last.eq(last)
            yield d.sink.valid.eq(1)
            yield
            while not (yield d.sink.ready):
                yield
        yield d.sink.valid.eq(0)
        yield d.sink.last.eq(0)

    def collect(self):
        d = self.dut
        yield d.source0.ready.eq(1)     # model the always-ready RingDMAWriter sinks
        yield d.source1.ready.eq(1)
        for _ in range(self.cycles):
            for qi, s in enumerate((d.source0, d.source1)):
                if (yield s.valid):
                    self.q[qi].append(((yield s.data), (yield s.keep), (yield s.last)))
            yield

    def run(self, stim):
        run_simulation(self.dut, [stim(), self.collect()])

    def frames(self, qi):
        """reassemble queue qi's beats into frames (bytes)."""
        out, cur = [], b""
        for data, keep, last in self.q[qi]:
            for b in range(8):
                if keep & (1 << b):
                    cur += bytes([(data >> (8 * b)) & 0xFF])
            if last:
                out.append(cur); cur = b""
        return out


def _drive(h, blobs, bypass=0):
    def stim():
        yield h.dut.hash_sel.storage.eq(bypass)
        yield
        for blob in blobs:
            yield from h.send(blob)
            for _ in range(3):
                yield
        for _ in range(80):
            yield
    h.run(stim)
    return h.frames(0), h.frames(1)


def test_gptp_to_q1():
    """1+2: untagged and C-TAGged gPTP both take the dedicated queue."""
    h = H()
    plain  = ptp_frame()
    tagged = ptp_frame(tagged=True, paylen=52)
    got0, got1 = _drive(h, [plain, tagged, plain])
    assert got1 == [plain, tagged, plain], \
        f"gPTP must land on q1 in order: got {len(got1)} frames"
    assert got0 == [], f"nothing but gPTP was sent, yet q0 got {len(got0)} frames"
    print(f"PASS gPTP (untagged + C-TAGged) -> q1 byte-exact, q0 empty "
          f"(q1={len(got1)} frames)")


def test_negatives():
    """3+4: the ingress test is DMAC *and* EtherType, exactly like REQ-CLS-07."""
    h = H()
    spoof_dmac = ptp_frame(dmac=[0x01, 0x80, 0xC2, 0x00, 0x00, 0x0F])  # one bit off
    spoof_uni  = ptp_frame(dmac=[0x02, 0x00, 0x00, 0x00, 0x00, 0x68])  # plain unicast
    wrong_et   = ptp_frame(etype=0x88F5)          # reserved DMAC, MVRP EtherType
    good       = ptp_frame()
    got0, got1 = _drive(h, [spoof_dmac, spoof_uni, wrong_et, good])
    assert got1 == [good], \
        f"only the real gPTP frame may reach q1; q1 got {len(got1)} frames"
    assert got0 == [spoof_dmac, spoof_uni, wrong_et], \
        f"the three negatives must land on q0; q0 got {len(got0)} frames"
    print("PASS NEGATIVE: spoofed DMAC / unicast / non-0x88F7 all fall to q0")


def test_bulk_stays_on_q0():
    """5: the 4-tuple flow hash is GONE - every TCP flow shares q0 now."""
    h = H()
    # tuples the old hash deliberately split across q0/q1
    flows = [([192, 168, 1, 2], [192, 168, 1, 1], 5201, 4000 + k) for k in range(6)]
    blobs = [tcp_frame(*f, paylen=40 + 8 * i) for i, f in enumerate(flows)]
    blobs.append(arp_frame())
    got0, got1 = _drive(h, blobs)
    assert got1 == [], f"no gPTP was sent, yet q1 got {len(got1)} frames " \
                       "(the flow hash is supposed to be gone)"
    assert got0 == blobs, f"q0 must carry every bulk frame in order: {len(got0)}"
    print(f"PASS bulk TCP ({len(flows)} tuples) + ARP all on q0, q1 untouched")


def test_bypass():
    """6: hash_sel[0] = 1 forces everything, gPTP included, to q0."""
    h = H()
    got0, got1 = _drive(h, [ptp_frame(), tcp_frame([10, 0, 0, 1], [10, 0, 0, 2],
                                                   1111, 2222, paylen=64)],
                        bypass=1)
    assert got1 == [], f"bypass must leave q1 empty; got {len(got1)} frames"
    assert len(got0) == 2, f"bypass must send both frames to q0; got {len(got0)}"
    print("PASS hash_sel=1 bypass forces gPTP to q0")


def test_interleaved_and_runt():
    """7+8: mixed traffic keeps both queues exact; a head-length runt takes q0."""
    h = H()
    p1 = ptp_frame(paylen=44)
    p2 = ptp_frame(tagged=True, paylen=60)
    b1 = tcp_frame([10, 0, 0, 1], [10, 0, 0, 2], 1111, 2222, paylen=100)
    b2 = tcp_frame([10, 0, 0, 3], [10, 0, 0, 4], 3333, 4444, paylen=56)
    runt = _pad8(bytes(GPTP_DMAC) + bytes(SMAC) + bytes([0x88, 0xF7]))  # 2 beats
    order = [b1, p1, b2, p2, b1, p1, runt]
    got0, got1 = _drive(h, order)
    assert got1 == [p1, p2, p1], \
        f"q1 must hold exactly the gPTP frames, in order: {len(got1)}"
    assert got0 == [b1, b2, b1, runt], \
        f"q0 must hold the bulk frames AND the runt, in order: {len(got0)}"
    print("PASS interleaved gPTP/bulk byte-exact + in order; head-length runt -> q0")


if __name__ == "__main__":
    test_gptp_to_q1()
    test_negatives()
    test_bulk_stays_on_q0()
    test_bypass()
    test_interleaved_and_runt()
    print("ALL PASS")
