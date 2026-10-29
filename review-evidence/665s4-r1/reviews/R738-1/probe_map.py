#!/usr/bin/env python3
"""Exercise the exact map comparison function without loading the SoC dependencies."""
import ast
import importlib.util
import json
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('review_port', root / 'sw/firmware/ctrl_nvm/plat/gen_flash_port.py')
port = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = port
spec.loader.exec_module(port)
source = ast.parse((root / 'tb/verilator/ctrl_service_budget/split_soc.py').read_text())
node = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == 'map_deviations')
scope = {'Path': Path, 'json': json}
exec(compile(ast.Module(body=[node], type_ignores=[]), 'map_deviations', 'exec'), scope)
check = scope['map_deviations']
work = packet / 'scratch/map-probe'
work.mkdir(parents=True, exist_ok=True)
csv, header = port.render(port.GOOD_CSV)
export = port.Export()
port.parse_csv(csv, export)
port.parse_header(header, export)
(work / 'flash_port.json').write_text(json.dumps(port.port_map(export, {})))
assert not check(csv, work)
print('PASS unchanged product-shaped map')
plants = [(name, port.planted(port._set(('registers', name), (addr + 4, size, access))))
          for name, (addr, size, access) in port.GOOD_CSV['registers'].items()]
plants.append(('flash window', port.planted(port._set(('regions', 'spiflash'), [(0x20000000, 16777216)]))))
for name, planted in plants:
    findings = check(port.render(planted)[0], work)
    assert findings, name
    print('PASS refusal:', name, findings)
