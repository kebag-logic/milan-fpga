#!/usr/bin/env python3
"""Bind real floating-point instances and cache geometry to export hashes."""
import hashlib
import json
from pathlib import Path
import re
import sys

packet = Path(sys.argv[1])
rows = json.loads((packet / 'receipts/cpu-measurements.json').read_text())
index = {row['label']: row for row in rows}
evidence = []
for width in (32, 64):
    texts = {}
    for option in ('none', 'fpu', 'l2'):
        row = index[f'naxriscv-{width}-{option}']
        raw = (packet / 'scratch/cpu/naxriscv' / row['netlist']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row['sha256']
        texts[option] = raw.decode()
    patterns = [r'^  FpuCore FpuEmbedded_logic_core \(', r'^  FpuDiv flt_div_divider \(', r'^  FpuSqrt flt_sqrt_sqrt \(']
    fpu_evidence = []
    for pattern in patterns:
        assert not re.search(pattern, texts['none'], re.M)
        match = re.search(pattern, texts['fpu'], re.M)
        assert match
        fpu_evidence.append({'text': match[0], 'line': texts['fpu'][:match.start()].count('\n') + 1})
    geometry = {}
    for option in ('none', 'l2'):
        # Select the RAM parameter block of the actual L2 data bank instance.
        text = texts[option]
        end = text.index(') cache_data_banks_0_ram (')
        start = text.rfind('  Ram_', 0, end)
        assert start >= 0
        block = text[start:end]
        count = int(re.search(r'\.wordCount\((\d+)\)', block)[1])
        bits = int(re.search(r'\.wordWidth\((\d+)\)', block)[1])
        geometry[option] = {'line': text[:start].count('\n') + 1, 'words': count,
                            'bits_per_word': bits, 'bytes': count * bits // 8,
                            'parameter_block': block}
    assert geometry['none']['bytes'] == 131072
    assert geometry['l2']['bytes'] == 8192
    evidence.append({'width': width, 'floating_point_instances_added': fpu_evidence, 'L2_geometry': geometry})
print(json.dumps(evidence, indent=2))
