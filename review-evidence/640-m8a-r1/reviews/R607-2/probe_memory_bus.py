#!/usr/bin/env python3
"""Independent Wishbone scoreboard over fixed bank decompositions."""
from pathlib import Path
import random
import sys
from migen import Module, ClockDomain, run_simulation

sys.path.insert(0, str(Path(sys.argv[1]) / 'sw/litex'))
import ctrl_memory as cm
from milan_soc import CtrlMemory

checks = 0
for banks in ((2048,), (65536,32768,8192,4096,2048), (131072,65536,16384,8192,4096,2048)):
    for readonly in (False, True):
        region = cm.ROM if readonly else cm.RAM
        length = sum(banks) // 4
        expected = {i: (i * 2246822519 + 3266489917) & 0xffffffff for i in range(length)}
        top = Module()
        top.clock_domains.cd_sys = ClockDomain('sys')
        top.submodules.mem = CtrlMemory(region, banks,
                                       list(expected.values()) if readonly else None)
        bus = top.mem.bus
        edges, at = {0, length-1, length, 57343,57344,65535}, 0
        for size in banks:
            edges.update((at,at+1,at+size//4-1))
            at += size//4
        rng = random.Random(607)
        addresses = sorted(edges | {rng.randrange(65536) for _ in range(128)})

        def access(address, write=False, value=0, select=15):
            yield bus.adr.eq(region.origin//4+address)
            yield bus.dat_w.eq(value)
            yield bus.sel.eq(select)
            yield bus.we.eq(write)
            yield bus.cyc.eq(1)
            yield bus.stb.eq(1)
            for clocks in range(8):
                yield
                ack, err = (yield bus.ack), (yield bus.err)
                if ack or err:
                    result = ack,err,(yield bus.dat_r)
                    break
            else:
                raise AssertionError(('timeout', banks, address))
            yield bus.cyc.eq(0)
            yield bus.stb.eq(0)
            yield
            return result

        def stimulus():
            global checks
            if not readonly:
                for address in addresses:
                    if address < length:
                        got = yield from access(address, True, expected[address])
                        assert got[:2] == (1,0)
            for address in addresses:
                got = yield from access(address)
                assert got[:2] == ((1,0) if address < length else (0,1)), (address,got)
                if address < length:
                    assert got[2] == expected[address], (address, got, expected[address])
                    got = yield from access(address, True, 0x01020304, 5)
                    assert got[:2] == (1,0)
                    want = expected[address] if readonly else (expected[address] & 0xff00ff00) | 0x00020004
                    got = yield from access(address)
                    assert got == (1,0,want), (address,got,want)
                else:
                    got = yield from access(address, True, 0xffffffff)
                    assert got[:2] == (0,1)
                checks += 1
        run_simulation(top, stimulus())
        print('PASS', 'rom' if readonly else 'sram', 'banks', banks,
              'addresses', len(addresses), 'including word 65535')
print('PASS independent bus scoreboard:', checks, 'address cases')
