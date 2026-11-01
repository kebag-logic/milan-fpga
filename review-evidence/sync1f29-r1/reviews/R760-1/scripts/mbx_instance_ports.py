#!/usr/bin/env python3
"""KL_mbx's instance in an exported top against the module's declared ports, and its unconnected or tied ones."""
import re, sys
from pathlib import Path
top, mod = Path(sys.argv[1]).read_text(), Path(sys.argv[2]).read_text()
decl = re.findall(r'^\s*(input|output)\s+(?:wire|logic)\s*(?:\[[^\]]*\])?\s*(\w+)\s*,?', mod.split(');', 1)[0], re.M)
m = re.search(r'\bKL_mbx\b\s*(?:#\((.*?)\)\s*)?\w*\s*\((.*?)\n\);', top, re.S)
body = m.group(2)
inst = dict(re.findall(r'^\s*\.(\w+)\s*\((.*)\),?\s*$', body, re.M))
ports = {n for _, n in decl}
print('module ports', len(ports), 'instance ports', len(inst))
print('in module not in instance:', sorted(ports - set(inst)))
print('in instance not in module:', sorted(set(inst) - ports))
for name in ('pub_src_sid_o', 'pub_sid_o', 'fw_send_o', 'fw_ack_p_i', 'gsi_req_o', 'asp_chg_p_i'):
    print(' ', name, '->', inst.get(name, 'ABSENT')[:60])
