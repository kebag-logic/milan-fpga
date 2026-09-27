#!/usr/bin/env python3
"""Cycle cost of the real LiteSPI SDR PHY core (1x, divisor 8) per transfer.

Run with the LiteX venv python. Measures, in system cycles, (a) sink.valid ->
source.valid for one 8-bit and one 32-bit transfer inside an open CS, and
(b) the extra wait before the first transfer after CS is re-asserted
(cs_delay). The harness models each transfer as len*8+1 cycles and no CS delay.
"""
from migen import Record, run_simulation
from litex.gen import LiteXModule
from litespi.phy.generic_sdr import LiteSPISDRPHYCore
from litespi.modules import N25Q128A13
from litespi.opcodes import SpiNorFlashOpCodes as C

class Pads:
    def __init__(self):
        self.clk = Record([('clk', 1)]).clk
        self.cs_n = Record([('cs_n', 1)]).cs_n
        self.mosi = Record([('mosi', 1)]).mosi
        self.miso = Record([('miso', 1)]).miso

dut = LiteSPISDRPHYCore(Pads(), N25Q128A13(C.READ_1_1_1_FAST), device='xc7', clock_domain='sys', default_divisor=8)
res = {}

def tb():
    for _ in range(30):
        yield
    def xfer(bits, label):
        yield dut.sink.valid.eq(1); yield dut.sink.len.eq(bits); yield dut.sink.width.eq(1)
        yield dut.sink.mask.eq(1); yield dut.sink.data.eq(0xa5)
        yield dut.source.ready.eq(1)
        t = 0
        while not (yield dut.sink.ready):
            yield; t += 1
        wait_accept = t
        yield; t += 1
        yield dut.sink.valid.eq(0)
        while not (yield dut.source.valid):
            yield; t += 1
        yield; t += 1
        res[label] = (wait_accept, t)
    yield dut.cs.eq(1)
    yield from xfer(8, 'first8_after_cs_assert')
    yield from xfer(8, 'second8_same_cs')
    yield from xfer(32, 'next32_same_cs')
    yield dut.cs.eq(0)
    yield
    yield dut.cs.eq(1)
    yield from xfer(8, 'first8_after_cs_reassert')

run_simulation(dut, tb())
for k, (acc, tot) in res.items():
    bits = 32 if '32' in k else 8
    print(f'{k:28} accept_wait={acc:3} total_cycles={tot:4} harness_model={bits*8+1:4} delta={tot-(bits*8+1):+d}')
