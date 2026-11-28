"""Independent arithmetic of the 4x4 point's stated figures, from the published measurements and the head's tables.
usage: python3 -I arith_check.py CLONE"""
import math, sys
from decimal import Decimal, ROUND_CEILING
from pathlib import Path
clone = Path(sys.argv[1]); sys.path.insert(0, str(clone / 'tb/verilator/ctrl_service_budget'))
import egress_ledger, bind_save, egress_mii
bad = 0
def check(name, ok, detail):
    global bad; bad += not ok; print(f'{"PASS" if ok else "FAIL"} {name}: {detail}')
fig = lambda ms: float(60 + ((Decimal(str(ms)) - 60) * Decimal('1.05')).quantize(Decimal('0.01'), ROUND_CEILING))
doc = (clone / 'docs/design/SPLIT_CONTROL_MEMORY.md').read_text()
for row, ms in egress_ledger.ARTY_4X4.items():
    want = fig(ms); got = egress_ledger.LEDGER['arty-4x4'][row]
    check(f'ledger {row}', got == want and f'| `{row}` | {ms:.5f} | {want:.2f} |' in doc.split('Arty 4x4 held-egress row')[1],
          f'measured {ms}, rule {want}, tool {got}')
check('ledger max', max(egress_ledger.LEDGER['arty-4x4'].values()) == 63.50, 'the largest figure is 63.50 ms')
check('1x1 and 8x8/1if ledgers untouched', set(egress_ledger.LEDGER) >= {'arty-1x1', '8x8-1if', 'arty-4x4'}, str(sorted(egress_ledger.LEDGER)))
save = 353.671 - 100
flight = math.ceil(2 * save / 50) * 50; saves = math.floor((630 - 100) / save) + 2
check('bind in flight', bind_save.FLIGHT_MS['arty-4x4'] == flight == 550, f'2 x {save:.3f} = {2*save:.3f} -> {flight}')
check('bind burst saves', bind_save.BURST_SAVES['arty-4x4'] == saves == 4, f'floor(530 / {save:.3f}) + 2 = {saves}')
row = (446.76 + 54.88) * 1.05 + egress_mii.MII_FIXED_NS / 1000
check('100 Mb/s egress row', abs(row - 527.04) < 0.005, f'(446.76 + 54.88) x 1.05 + {egress_mii.MII_FIXED_NS} ns = {row:.3f} us')
row300 = (446.76 + 54.88) * 1.05 + 0.300
print(f'INFO with the 300.0 ns measured at 100 MHz instead of the stated 320: {row300:.3f} us')
p = egress_mii.params(dict(shape='endstation_arty_split_4x4', sys_hz=100_000_000, milan_hz=50_000_000))
check('4x4 SR load', p.sr_bytes == (90, 90, 90, 90, 46) and p.sys_ps == 10_000, f'{p.sr_bytes}, sys {p.sys_ps} ps')
kbps = lambda frame: (frame + 43) * 64
check('egress envelope', 4 * kbps(72) + 5632 == 35072 and abs(35072 / 75000 - 0.468) < 0.001, f'4 x {kbps(72)} + 5632 = {4*kbps(72)+5632} kb/s')
check('ingress envelope', 4 * kbps(216) + 5632 == 71936 <= 75000, f'4 x {kbps(216)} + 5632 = {4*kbps(216)+5632} kb/s')
check('SHARE', abs(173322 / 100e6 * 1e3 - 1.733) < 0.0005, '173322 cycles at 100 MHz = 1.733 ms')
rom = 131072 + 2048; sram = 65536 + 4096
check('memory ledger', 114844 + 17630 + 184 <= rom and 184 + 61104 + 8192 <= sram and (rom + sram) / 4096 == 49.5,
      f'ROM {114844+17630+184} of {rom}, SRAM {184+61104+8192} of {sram}, {(rom+sram)/4096} RAMB36')
print('RESULT', 'PASS' if not bad else f'FAIL {bad}'); sys.exit(bool(bad))
