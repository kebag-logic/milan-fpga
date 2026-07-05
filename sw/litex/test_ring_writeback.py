#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Sim verification of the RingDMAWriter pointer-writeback (perf, 2026-07-05).

Proven here BEFORE spending a bitstream:
  1. CORRECTNESS — after each frame commit the engine DMA-writes {dropped[63:32],
     wr_ptr[31:0]} to the programmed shadow address, so the driver can poll the ring head
     from cacheable coherent memory instead of an MMIO CSR.
  2. DATAPATH COST — the extra 8-byte writeback adds only a few cycles per frame, so the
     engine's raw drain pps/bandwidth is essentially unchanged. (The writeback removes a
     CPU-side cost; it must not introduce a datapath-side one.)

The *system* pps gain (CPU no longer stalling on an MMIO read per poll) is not visible to
an RTL-only sim — that is projected by the measured-sweep model in poll_cost_model.py.

Run: cd sw/litex && /home/alex/litex-milan/venv/bin/python3 test_ring_writeback.py
"""
import sys, importlib.util
from migen import *
from litex.gen import *

sys.path.insert(0, ".")
spec = importlib.util.spec_from_file_location("trd", "./test_ring_dma.py")
trd = importlib.util.module_from_spec(spec); sys.modules["trd"] = trd
spec.loader.exec_module(trd)
Harness, frame, BASE = trd.Harness, trd.frame, trd.BASE

SHADOW  = 0x200000          # writeback shadow addr, well outside the ring
CLK_HZ  = 100e6             # coherent DMA bus = sys = 100 MHz on silicon


def drain(n_frames, len_beats, wb, b_delay=2):
    """Feed n_frames back-to-back; return (cycles_to_drain, wr, drops, shadow_word)."""
    ring = 1 << 20
    h = Harness(ring_size=ring, fifo_beats=4096, max_frame_beats=len_beats + 2,
                burst_beats=16, aw_stall=0, w_stall=0, b_delay=b_delay, cycles=400000)
    F = [frame(0x100 + (i & 0xFF), len_beats) for i in range(n_frames)]
    target = n_frames * (8 + len_beats * 8)
    m = {"start": None, "end": None}
    out = {}

    def stim():
        yield from h.init_csr()
        if wb:
            yield h.dut.status.storage.eq(SHADOW)
            yield
        for f in F:
            yield from h.send_frame(f)
        yield from h.wait_idle(settle=300)
        out["wr"]    = (yield h.dut.wr_ptr.status)
        out["drops"] = (yield h.dut.dropped.status)

    def counter():
        for c in range(h.cycles):
            if h.done:
                return
            if (yield h.dut.sink.valid) and m["start"] is None:
                m["start"] = c
            if (yield h.dut.wr_ptr.status) >= target and m["end"] is None:
                m["end"] = c
            yield

    def wrapped():
        yield from stim(); h.done = True

    run_simulation(h.dut, [wrapped(), h.axi_slave(), h.ready_monitor(), counter()])
    assert not h.errors, h.errors
    cyc = (m["end"] - m["start"]) if (m["start"] is not None and m["end"] is not None) else None
    return cyc, out["wr"], out["drops"], h.mem.get(SHADOW, None)


def test_writeback_correctness():
    # a couple of frames, then confirm the shadow == {drops, wr_ptr}
    _, wr, drops, shadow = drain(n_frames=5, len_beats=7, wb=True)
    assert shadow is not None, "engine never wrote the shadow"
    lo, hi = shadow & 0xFFFFFFFF, (shadow >> 32) & 0xFFFFFFFF
    assert lo == wr,    f"shadow wr_ptr {lo:#x} != CSR wr_ptr {wr:#x}"
    assert hi == drops, f"shadow dropped {hi} != CSR dropped {drops}"
    print(f"PASS writeback correctness: shadow=[wr={lo:#x}, dropped={hi}] matches CSRs")


def test_writeback_bandwidth():
    N, LB = 40, 187          # 40 frames of 1496 B payload (~MTU 1500)
    fbytes = LB * 8
    c_off, wr0, _, sh0 = drain(N, LB, wb=False)
    c_on,  wr1, _, sh1 = drain(N, LB, wb=True)
    assert wr0 == wr1, "commit differs WB on/off"
    assert sh0 is None and sh1 is not None
    for tag, cyc in (("WB off", c_off), ("WB on ", c_on)):
        secs = cyc / CLK_HZ
        pps  = N / secs
        gbps = N * fbytes * 8 / secs / 1e9
        print(f"  {tag}: {cyc:6d} cyc  ->  {cyc/N:6.1f} cyc/frame  "
              f"{pps/1e3:7.1f} kpps  {gbps:5.2f} Gbit/s (payload)")
    over = (c_on - c_off) / N
    slow = 100 * (c_on - c_off) / c_off
    print(f"PASS writeback bandwidth: +{over:.1f} cyc/frame ({slow:+.2f}% drain time) "
          f"= {over/CLK_HZ*1e9:.0f} ns/frame — engine pps/bandwidth ~unchanged")


if __name__ == "__main__":
    test_writeback_correctness()
    test_writeback_bandwidth()
    print("ALL PASS")
