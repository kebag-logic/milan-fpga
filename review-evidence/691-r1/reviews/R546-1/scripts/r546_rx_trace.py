#!/usr/bin/env python3
"""Reviewer probe R546-1: drive the GMII receiver importable on PYTHONPATH.

Independent of sw/litex/test_gmii_rx_capture.py. Writes one line per cycle
(inputs applied, then visible valid/data/last) and checks every line against
a pad-sample model of upstream's synchronous-reset receiver:

  at each edge k:  valid' = rst_k ? 0 : dv_k ;  data' = rst_k ? 0 : data_k
  between edges:   last   = ~dv_pad_now & valid

The model is the reviewer's own reading of upstream LiteEth (three flops with
a synchronous reset); the pre-patch receiver must also satisfy it, which is
checked by running this probe against both packages and comparing traces.

usage: r546_rx_trace.py OUT_TRACE [--cycles N] [--seed S] [--emit VERILOG]
exit 0 = every cycle matches the model; 1 = mismatch.
"""
import argparse
import hashlib
import random
import sys

from migen import ClockDomain, Module, Record, Signal
from migen.fhdl import verilog
from migen.sim import run_simulation
from liteeth.phy.gmii import LiteEthPHYGMIIRX


class Bench(Module):
    def __init__(self):
        self.clock_domains.cd_sys = ClockDomain("sys")
        self.pads = Record([("rx_dv", 1), ("rx_data", 8), ("rx_er", 1)])
        self.rst = Signal()
        self.comb += self.cd_sys.rst.eq(self.rst)
        self.submodules.rx = LiteEthPHYGMIIRX(self.pads)


def stimulus(cycles, seed):
    rng = random.Random(seed)
    seq = []
    # 1) every ordered pair of (dv, rst) states, each with two data values
    states = [(dv, rst) for dv in (0, 1) for rst in (0, 1)]
    for a in states:
        for b in states:
            for d in (0x00, 0xFF, 0x5A, 0xA5):
                seq += [(d, a[0], a[1]), (d ^ 0xFF, b[0], b[1])]
    # 2) frame-shaped traffic with reset pulses landing on every phase of a
    #    frame: before, first byte, middle, last byte, first idle after
    for length in (1, 2, 3, 8, 64):
        for rst_at in range(-1, length + 3):
            seq += [(0, 0, 0)] * 2
            for i in range(length + 3):
                dv = 1 if i < length else 0
                seq.append((rng.randrange(256) if dv else rng.randrange(256),
                            dv, 1 if i == rst_at else 0))
    # 3) long random run with bursty reset and back-to-back frames
    dv, rst = 0, 0
    for _ in range(cycles):
        if rng.random() < 0.08:
            dv ^= 1
        rst = (rng.random() < 0.3) if rng.random() < 0.05 else (rst and rng.random() < 0.7)
        seq.append((rng.randrange(256), dv, int(rst)))
    return seq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--cycles", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=546)
    ap.add_argument("--emit")
    args = ap.parse_args()

    dut = Bench()
    seq = stimulus(args.cycles, args.seed)
    lines, bad = [], []

    def gen():
        model_valid, model_data = 0, 0
        for n, (data, dv, rst) in enumerate(seq):
            yield dut.pads.rx_data.eq(data)
            yield dut.pads.rx_dv.eq(dv)
            yield dut.pads.rx_er.eq((data >> 3) & 1)
            yield dut.rst.eq(rst)
            yield dut.rx.source.ready.eq(n & 1)
            yield
            got = ((yield dut.rx.source.valid), (yield dut.rx.source.data),
                   (yield dut.rx.source.last))
            # visible registered state still reflects the previous sample;
            # last already sees the pad level just driven
            want = (model_valid, model_data, (1 - dv) & model_valid)
            lines.append(f"{n} {data:02x} {dv} {rst} -> {got[0]} {got[1]:02x} {got[2]}")
            if got != want:
                bad.append((n, (data, dv, rst), got, want))
            model_valid = 0 if rst else dv
            model_data = 0 if rst else data

    run_simulation(dut, gen())
    text = "\n".join(lines) + "\n"
    open(args.out, "w").write(text)
    print(f"cycles {len(seq)} trace_sha256 {hashlib.sha256(text.encode()).hexdigest()}")
    if args.emit:
        d = Bench()
        ios = {d.cd_sys.clk, d.rst, d.pads.rx_dv, d.pads.rx_data, d.pads.rx_er,
               d.rx.source.valid, d.rx.source.data, d.rx.source.last,
               d.rx.source.ready}
        verilog.convert(d, ios=ios, name="rxcap").write(args.emit)
    if bad:
        print(f"MODEL MISMATCH: {len(bad)} cycles; first {bad[:3]}")
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
