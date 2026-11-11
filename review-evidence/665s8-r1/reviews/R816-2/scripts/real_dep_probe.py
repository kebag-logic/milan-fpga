# Reviewer probe (#868 ruling item 5): the reuse guard's read_by_tools() on a REAL split-top build's
# dependency files, and an edit of a file only those files name (an `include`d header) refused.
# Usage: python3 -I -B real_dep_probe.py <disposable checkout> <build dir holding split/ from make build-split>
# Writes stand-ins for the other build outputs in <build dir>; edits and restores the header's exact bytes.
import json, sys
from pathlib import Path
root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_wire_timing'))
import wire_build as wb
found = wb.read_by_tools(out)
names = sorted({str(p.relative_to(root)) if root in p.parents else str(p) for p in found})
print('read_by_tools: %d files' % len(names))
for want in ('ethernet_events.svh', 'adp_shape_defaults.svh', 'milan_datapath.sv', 'tb_split_top.sv', 'verilated.cpp'):
    hits = [n for n in names if n.endswith(want)]
    print(f'  {want}: {hits[:2] if hits else "NOT RECORDED"}')
headers = [p for p in found if p.name in ('ethernet_events.svh', 'adp_shape_defaults.svh')]
listed = set(wb.split_sources(out, {'split_vars': wb.split_vars('endstation_ax7101_1x1_tdm8', 1)}))
for p in headers:
    print(f'  {p.name} also in print-split-srcs: {p in listed}')
for rel in ('image/ctrl_app.elf', 'soc/gateware/rom.init', 'wire_config.hpp', 'native/Vsim'):
    q = out / rel
    q.parent.mkdir(parents=True, exist_ok=True)
    q.write_bytes(b'stand-in ' + rel.encode())
spec = dict(elf=str(out / 'image/ctrl_app.elf'), sources=[], split_vars=wb.split_vars('endstation_ax7101_1x1_tdm8', 1))
spec['inputs'] = wb.inputs(out, spec)
spec['executable_sha256'] = wb.digest(out / 'native/Vsim')
(out / 'build.json').write_text(json.dumps(spec))
def ask():
    try:
        wb.reused(out)
        return 'ACCEPTED'
    except RuntimeError as why:
        return 'refused: ' + str(why)[:160]
print('unchanged:', ask())
for p in headers:
    before = p.read_bytes()
    try:
        p.write_bytes(before + b'\n// reviewer probe\n')
        print(f'{p.relative_to(root) if root in p.parents else p} edited:', ask())
    finally:
        p.write_bytes(before)
print('after restore:', ask())
