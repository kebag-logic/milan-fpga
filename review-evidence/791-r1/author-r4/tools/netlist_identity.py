#!/usr/bin/env python3
"""netlist_identity.py <scratch> [<run dir>, default final]: every VexiiRiscv netlist this round's runs named, at the final head and at round 1's
head 03447eaa in the same environment (PYTHONHASHSEED=0), with the sha256 and size of the cached netlist each name
reads. LiteX names a netlist by an MD5 over every generator input (region list, arguments, reset address, ...), so
one name at both heads is one generator input, and the cached file is the netlist both builds elaborate."""
import hashlib
import re
import sys
from pathlib import Path

S = Path(sys.argv[1])
RUN = sys.argv[2] if len(sys.argv) > 2 else 'final'
CACHE = Path('$WORKSPACE_HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog')
NAME = re.compile(r'VexiiRiscvLitex_[0-9a-f]{32}')
RUNS = {
    'region-decode self-test (none, single-mask, cover)': (f'{RUN}/region-self-test.log', 'r1/r1-region-self-test.log'),
    'product split export 1x1': (f'{RUN}/decode/endstation_ax7101_1x1_tdm8.txt', 'r1/r1-decode/endstation_ax7101_1x1_tdm8.txt'),
    'product split export 8x8': (f'{RUN}/decode/endstation_ax7101_8x8.txt', 'r1/r1-decode/endstation_ax7101_8x8.txt'),
    **({'split boot 1x1': ('final/boot-1x1.log', None), 'split boot 8x8': ('final/boot-8x8.log', None)}
       if RUN == 'final' else {}),
}
fails = 0
for what, (head, r1) in RUNS.items():
    names = list(dict.fromkeys(NAME.findall((S / head).read_text())))
    then = list(dict.fromkeys(NAME.findall((S / r1).read_text()))) if r1 else None
    same = then is None or names == then
    fails += not same
    print(f'{what}: final head {names}; at 03447eaa {then if then is not None else "(not re-run: R826-1 records 99bc789b at 03447eaa)"}: {"same" if same else "DIFFERENT"}')
    for n in names:
        f = CACHE / f'{n}.v'
        data = f.read_bytes()
        print(f'  {n}.v sha256 {hashlib.sha256(data).hexdigest()} ({len(data)} bytes)')
ga = sorted(p.name for p in (S / RUN).glob('*.log') if 'VexiiRiscv generation command' in p.read_text(errors='replace'))
print(f'logs with a generator command (a netlist generated, not read from the cache): {ga or "none"}')
print(f'{fails} difference(s)')
sys.exit(1 if fails or ga else 0)
