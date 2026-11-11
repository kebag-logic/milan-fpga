#!/usr/bin/env python3
"""af_diff.py <af-dir> <out-dir>: base against head, per config: every builder output, the CPU netlist name, the
region rows and generator args, and the export's Verilog, csr.csv, csr.json and soc.h. Raw unified diffs (each
side's own scratch path replaced by <work>/<clone>) are written to <out-dir>/<config>.diff; a file that differs
raw is re-compared with only comments removed (C/Verilog // and /* */; csr.csv '#' lines)."""
import difflib, hashlib, json, re, sys
from pathlib import Path
af, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
import os
P = os.environ.get('P', '$REVIEWS/791-r825-1-packet') + '/scratch'
def norm(b, side, cfg):
    return (b.replace(f'{P}/af/{side}/{cfg}'.encode(), b'<work>').replace(f'{P}/clone-{side}'.encode(), b'<clone>'))
def strip(name, b):
    if name.endswith('.csv'):
        return b'\n'.join(l for l in b.splitlines() if not l.startswith(b'#'))
    b = re.sub(rb'/\*.*?\*/', b'', b, flags=re.S)
    return b'\n'.join(re.sub(rb'//.*$', b'', l).rstrip() for l in b.splitlines())
summary = []
for cfg in sorted(p.name for p in (af / 'head').iterdir() if p.is_dir()):
    files = {}
    for side in ('base', 'head'):
        w = af / side / cfg
        f = {f'builder/{p.relative_to(w / "builder")}': p.read_bytes() for p in sorted((w / 'builder').rglob('*')) if p.is_file()}
        cpu = json.loads((w / 'cpu.json').read_text())
        f['cpu/netlist-name'] = (cpu['netlist'] or '').encode(); f['cpu/rows'] = json.dumps(cpu['rows']).encode()
        f['cpu/vexii_args'] = cpu['vexii_args'].encode(); f['cpu/export-error'] = (cpu['error'] or 'none').encode()
        for rel in ('csr.csv', 'csr.json', 'software/include/generated/soc.h'):
            if (w / 'soc' / rel).exists(): f[f'soc/{rel}'] = (w / 'soc' / rel).read_bytes()
        for p in sorted((w / 'soc/gateware').glob('*.v')): f[f'soc/gateware/{p.name}'] = p.read_bytes()
        files[side] = {k: norm(v, side, cfg) for k, v in f.items()}
    keys = sorted(set(files['base']) | set(files['head']))
    lines, diffs = [], []
    for k in keys:
        a, b = files['base'].get(k), files['head'].get(k)
        if a == b: continue
        if a is None or b is None:
            lines.append(f'  {k}: present only at {"head" if a is None else "base"}'); diffs.append(k); continue
        same = strip(k, a) == strip(k, b)
        d = list(difflib.unified_diff(a.decode(errors='replace').splitlines(), b.decode(errors='replace').splitlines(), f'base/{k}', f'head/{k}', n=0, lineterm=''))
        changed = sum(1 for l in d if l[:1] in '+-' and not l.startswith(('+++', '---')))
        lines.append(f'  {k}: differs raw ({changed} changed lines); with comments removed: {"IDENTICAL" if same else "DIFFERENT"}')
        if not same: diffs.append(k)
        (out / f'{cfg}.diff').open('a').write('\n'.join(d) + '\n')
    name = files['head']['cpu/netlist-name'].decode()
    summary.append(f'{cfg}: {len(keys)} entries compared; non-comment differences: {diffs or "none"}; CPU netlist base '
                   f'{files["base"]["cpu/netlist-name"].decode()} head {name}; rows equal: '
                   f'{files["base"]["cpu/rows"] == files["head"]["cpu/rows"]}; export error at head: '
                   f'{files["head"]["cpu/export-error"].decode()[:70]}')
    summary += lines
(out / 'summary.txt').write_text('\n'.join(summary) + '\n'); print('\n'.join(summary))
