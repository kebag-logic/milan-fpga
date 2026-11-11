#!/bin/bash
# cone_check.sh <netlist.v> <csr.csv> <workdir>: exhaustive word-address check of a CPU netlist's fetch/load PMA
# against the SoC's regions from LiteX's csr.csv (memory_region rows; mode from the row: io rows are rw only,
# 'cached' rows on rom/spiflash/main_ram are rx(+w for sram/main_ram) -- see modes below).
set -e
NL=$1; CSV=$2; W=$3; P=${P:-$REVIEWS/791-r825-1-packet}
mkdir -p "$W"
python3 -I $P/scripts/cone_extract.py "$NL" "$W"
python3 -I - "$CSV" "$W/spec.h" <<'PY'
import sys
# Modes as LiteX's SoC gives them (SoCRegion mode): rom and spiflash 'rx', sram and main_ram 'rwx', io 'rw'.
X = {'rom', 'sram', 'spiflash', 'main_ram'}
rows = [l.split(',') for l in open(sys.argv[1]).read().splitlines() if l.startswith('memory_region,')]
fetch, load = [], []
for _, name, origin, size, kind in rows:
    lo, hi = int(origin, 16), int(origin, 16) + int(size)
    load.append((lo, hi))
    if name in X:
        fetch.append((lo, hi))
out = ['struct Range { unsigned long long lo, hi; };']
for n, rs in (('FETCH', fetch), ('LOAD', load)):
    out.append(f'static const Range {n}_OK[] = {{' + ', '.join(f'{{0x{a:x}ull, 0x{b:x}ull}}' for a, b in rs) + '};')
    out.append(f'static const int N_{n} = {len(rs)};')
open(sys.argv[2], 'w').write('\n'.join(out) + '\n')
print('spec fetch', [(hex(a), hex(b)) for a, b in fetch]); print('spec load', [(hex(a), hex(b)) for a, b in load])
PY
cd "$W"
verilator --cc --exe --build -O3 -j 4 -Wno-fatal --top-module pma_cone -CFLAGS "-O2 -I$W" pma_cone.v $P/scripts/cone_sweep.cpp -o sweep > verilate.log 2>&1
./obj_dir/sweep
