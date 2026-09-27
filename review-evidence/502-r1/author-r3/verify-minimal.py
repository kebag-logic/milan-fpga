from pathlib import Path
import hashlib
import json
import re
import subprocess

path = 'hdl/milan/milan_datapath.sv'
base = subprocess.check_output(['git', 'show', '104c8a54:' + path], text=True)
current = Path(path).read_text()

def phase5(text):
    start = text.index("          3'd5: begin\n", text.index('begin : amap_edit_commit'))
    return text[start:text.index('          default: ;', start)]

expanded = phase5(current)
for direction in ('in', 'out'):
    name = 'amap_edit_' + direction + '_change_w'
    condition = re.search(r'assign ' + name + r' = (.*?);', current, re.S).group(1)
    expanded = expanded.replace(name, condition)
compact = lambda value: re.sub(r'\s+', '', value)
assert compact(expanded) == compact(phase5(base))
assert subprocess.check_output(['git', 'diff', '220c9d56', '--', 'tb/verilator/pp_shadow', 'hdl/milan/KL_pp_shadow.sv']) == b''
result = {
    'base': '104c8a54b183cd9215ed1e3a2e1be1634f48d33d',
    'current_hdl_sha256': hashlib.sha256(current.encode()).hexdigest(),
    'expanded_phase5_equals_base_ignoring_whitespace': True,
    'shadow_and_tests_unchanged_from_220c9d56': True,
    'priority': 'Input change wins; absent input change falls through to output change.'
}
print(json.dumps(result, indent=2))
