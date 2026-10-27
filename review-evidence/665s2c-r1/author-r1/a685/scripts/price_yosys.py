"""Price VexiiRiscv netlists with Yosys on the xc7 cell library, as syn/yosys/ooc.sh prices a top.

usage: price_yosys.py OUT_JSON NETLIST.v [NETLIST.v ...]
Each netlist is read with LiteX's two generic RAM models beside it, mapped with
`synth_xilinx -family xc7 -top <module> -flatten`, and counted from the final
stat block exactly as ooc.sh counts: LUT1-6, distributed RAM in LUT6 equivalents
(UG474), FD*, RAMB36E1, RAMB18E1, DSP48E1, CARRY4. A netlist whose block cannot be
read, or maps to no cell, fails the run.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

LRAM = {8: ('RAM256X1D', 'RAM512X1S', 'RAM32X8S', 'RAM64X8SW', 'RAM32X16DR8'),
        4: ('RAM32M', 'RAM64M', 'RAM128X1D', 'RAM32M16', 'RAM64M8', 'RAM256X1S', 'RAM32X4S'),
        2: ('RAM32X1D', 'RAM32X1D_1', 'RAM64X1D', 'RAM64X1D_1', 'RAM128X1S', 'RAM128X1S_1', 'RAM32X2S',
            'RAM64X2S'),
        1: ('RAM32X1S', 'RAM32X1S_1', 'RAM64X1S', 'RAM64X1S_1')}


def price(netlist: Path, work: Path) -> dict:
    top = netlist.stem
    rams = [netlist.with_name('Ram_1w_1rs_Generic.v'), netlist.with_name('Ram_1w_1ra_Generic.v')]
    log = work / f'{top}.log'
    script = f"read_verilog {' '.join(map(str, rams))} {netlist}; synth_xilinx -family xc7 -top {top} -flatten; stat"
    with log.open('w') as sink:
        rc = subprocess.run(['yosys', '-q', '-l', str(log.with_suffix('.ylog')), '-p', script],
                            stdout=sink, stderr=subprocess.STDOUT, check=False).returncode
    text = log.with_suffix('.ylog').read_text()
    if rc:
        raise RuntimeError(f'{top}: yosys exited {rc}')
    blocks = re.split(r'^=== (\S+) ===$', text, flags=re.M)
    mine = [blocks[i + 1] for i in range(1, len(blocks) - 1, 2) if blocks[i] == top]
    if not mine:
        raise RuntimeError(f'{top}: no stat block')
    row = dict(LUT=0, LUTRAM=0, FF=0, RAMB36=0, RAMB18=0, DSP=0, CARRY4=0)
    for count, cell in re.findall(r'^\s+(\d+)\s+(\S+)\s*$', mine[-1], re.M):
        n = int(count)
        if re.fullmatch(r'LUT[1-6]', cell):
            row['LUT'] += n
        elif re.fullmatch(r'RAM\d\S*', cell):
            cost = next((c for c, names in LRAM.items() if cell in names), 0)
            if not cost:
                raise RuntimeError(f'{top}: distributed-RAM cell {cell} has no LUT6 cost')
            row['LUTRAM'] += n * cost
        elif re.fullmatch(r'FD[CPRS]E?', cell):
            row['FF'] += n
        elif cell in ('RAMB36E1', 'RAMB18E1', 'DSP48E1', 'CARRY4'):
            row[{'RAMB36E1': 'RAMB36', 'RAMB18E1': 'RAMB18', 'DSP48E1': 'DSP'}.get(cell, cell)] += n
    row['LUT_TOT'] = row['LUT'] + row['LUTRAM']
    row['tiles'] = row['RAMB36'] + row['RAMB18'] / 2
    if not any(row.values()):
        raise RuntimeError(f'{top}: maps to zero xc7 cells')
    return dict(netlist=netlist.name, **row)


def main() -> int:
    out = Path(sys.argv[1])
    rows = []
    with tempfile.TemporaryDirectory(prefix='price-yosys-') as tmp:
        for path in sys.argv[2:]:
            row = price(Path(path), Path(tmp))
            print(json.dumps(row), flush=True)
            rows.append(row)
    out.write_text(json.dumps(rows, indent=1) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
