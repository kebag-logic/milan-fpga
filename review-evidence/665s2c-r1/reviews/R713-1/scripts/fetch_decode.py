"""The fetch side's region check (fault and io) of a VexiiRiscv netlist, with the fetch plugin's
prefix folded, so a cacheless and a cached netlist compare. usage: fetch_decode.py A.v B.v"""
import re
import sys
from pathlib import Path

def fetch_decode(path):
    core = Path(path).read_text()
    core = core[core.index('\nmodule VexiiRiscv ('):]
    core = core[:core.index('\nendmodule')]
    out = set()
    for line in core.splitlines():
        m = re.match(r'\s*assign (\S+) = (.*);$', line)
        if not m or not re.search(r'(FetchCachelessPlugin|FetchL1Plugin)\w*(pma|Pma)', m.group(1)):
            continue
        if m.group(1).endswith('_cmd_address'):
            continue
        s = line.strip()
        s = re.sub(r'FetchCachelessPlugin_logic_onPma_port|FetchL1Plugin_logic_ctrl_pmaPort', 'FETCH_PMA', s)
        s = re.sub(r'FetchCachelessPlugin_pmaBuilder|FetchL1Plugin_pmaBuilder', 'FETCH_PMA_BUILDER', s)
        out.add(s)
    return out

a, b = fetch_decode(sys.argv[1]), fetch_decode(sys.argv[2])
print(f'{Path(sys.argv[1]).name}: {len(a)}; {Path(sys.argv[2]).name}: {len(b)}; identical: {a == b}')
for s in sorted(a ^ b):
    print(('A ' if s in a else 'B ') + s[:200])
