#!/usr/bin/env python3
"""Extract cost evidence, linked-image identity and the region-decode delta."""
import difflib
import hashlib
import json
import os
from pathlib import Path
import sys

root = Path(os.environ['REVIEW_ROOT'])
packet = Path(os.environ['REVIEW_PACKET'])
scratch = packet / 'scratch'
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import grade

specs = {arm: json.loads((scratch / arm / 'build.json').read_text())
         for arm in ('A1', 'A8', 'asbuilt')}
out = {}
for arm in ('A1', 'A8'):
    spec = specs[arm]
    logs = {}
    for path in (scratch / arm / 'results').glob('*.log'):
        text = path.read_text()
        if 'RESULT: PASS' in text:
            logs[path.stem] = grade.parse(text, spec['sys_hz'], spec['cpu_hz'])
    passes = [(name, p) for name, log in logs.items() for p in log.passes]
    srp = max(passes, key=lambda pair: pair[1].modules.get('mrp_mad', 0))
    idle = min((p for _, p in passes if p.modules.get('aecp') and p.modules.get('aecp_nvm')),
               key=lambda p: p.cycles)
    accesses = {}
    for key in ('fetch_rom', 'load_flash', 'mbx_read', 'mbx_write'):
        vals = [list(map(int, log.summary[key].split('/'))) for log in logs.values()
                if key in log.summary and int(log.summary[key].split('/')[0])]
        count, cycles = sum(v[0] for v in vals), sum(v[1] for v in vals)
        accesses[key] = dict(count=count, cpu_cycles=cycles, mean_cpu_cycles=cycles/count,
                             minimum=min(v[2] for v in vals), maximum=max(v[3] for v in vals))
    out[arm] = {'sys_hz': spec['sys_hz'], 'cpu_hz': spec['cpu_hz'],
                'vexii_args': spec['vexii_args'], 'ctrl_plan': spec['ctrl_plan'],
                'elf_sha256': hashlib.sha256((scratch / arm / 'image/ctrl_app.elf').read_bytes()).hexdigest(),
                'largest_mrp_mad': {'group': srp[0], 'pass_cycles': srp[1].cycles,
                                    'start_sys': srp[1].start_sys, 'modules': srp[1].modules},
                'smallest_pass_with_both_aecp_polls': {'cycles': idle.cycles, 'modules': idle.modules},
                'accesses': accesses,
                'flash_load_to_bram_fetch_ratio': accesses['load_flash']['mean_cpu_cycles'] / accesses['fetch_rom']['mean_cpu_cycles'],
                'code_max_bytes': {k: max(int(log.code.get(k, 0)) for log in logs.values())
                                   for k in ('boot_bytes', 'service_bytes', 'service_only_bytes')}}

def core(arm):
    spec = specs[arm]
    path = next(Path(p) for p in spec['sources'] if Path(p).name == spec['netlist'] + '.v')
    return path.read_text().replace(spec['netlist'], 'CORE').splitlines(True)
diff = ''.join(difflib.unified_diff(core('A1'), core('asbuilt'), fromfile='cover/core.v', tofile='as-built/core.v'))
(packet / 'core-region-decode.diff').write_text(diff)
out['region_delta_lines'] = sum(line.startswith(('+', '-')) and not line.startswith(('+++', '---')) for line in diff.splitlines())
(packet / 'cost-audit.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({a: {'ratio': out[a]['flash_load_to_bram_fetch_ratio'],
                     'mrp_mad': out[a]['largest_mrp_mad'],
                     'code': out[a]['code_max_bytes']} for a in ('A1', 'A8')}, indent=2))
