#!/usr/bin/env python3
"""allfabric.py <base-clone> <head-clone> <work> <out.txt>: the all-fabric SoC, base against head, per shipped config.

Run with the review's generation guard on PYTHONPATH. For each configs/*.yaml at each side: the builder into
<work>/<side>/<config>/builder (-o) and into its default directory (which the export reads), then milan_soc's
export on the builder's own argv (emit_soc_argv: no --ctrl-mailbox), no software, no Vivado, in a child that records
the CPU's netlist name, the rows handed to its generator, its arguments and any refusal. Compared: every builder
output; the netlist name and the cached netlist's bytes; the rows; the arguments; the refusal; csr.csv, csr.json,
soc.h and every gateware *.v. Each side's own paths are replaced first. A file whose raw bytes differ is compared
again with comments stripped (.v/.h: /* */ blocks and // to end of line; csr.csv: lines starting '#'), and its
raw differing lines are written to <work>/diffs/ for inspection.
"""
import difflib
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

CHILD = r'''
import json, sys
from pathlib import Path
clone, argv, dump = Path(sys.argv[1]), json.loads(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(clone / "sw/litex"))
import milan_soc
from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv
sys.argv = ["milan_soc.py", *argv]
error = None
try:
    milan_soc.main()
except BaseException as exc:
    error = f"{type(exc).__name__}: {exc}"
dump.write_text(json.dumps({"netlist": VexiiRiscv.netlist_name,
                            "rows": [list(r) for r in getattr(VexiiRiscv, "memory_regions", [])],
                            "vexii_args": VexiiRiscv.vexii_args, "error": error}, indent=1))
'''


def run(argv, log, cwd):
    with open(log, 'w') as sink:
        return subprocess.run(argv, cwd=cwd, stdout=sink, stderr=subprocess.STDOUT, check=False).returncode


def strip(name, data):
    if name.endswith(('.v', '.h')):
        data = re.sub(rb'/\*.*?\*/', b'', data, flags=re.S)
        data = re.sub(rb'//[^\n]*', b'', data)
        return b'\n'.join(ln.rstrip() for ln in data.splitlines() if ln.strip())
    if name.endswith('.csv'):
        return b'\n'.join(ln for ln in data.splitlines() if not ln.startswith(b'#'))
    return data


def side(clone, w, config):
    py = sys.executable
    w.mkdir(parents=True, exist_ok=True)
    cfgpath = clone / 'configs' / f'{config}.yaml'
    rc_b = run([py, '-B', 'sw/builder/endstation_builder.py', str(cfgpath), '-o', str(w / 'builder')], w / 'builder.log', clone)
    rc_d = run([py, '-B', 'sw/builder/endstation_builder.py', str(cfgpath)], w / 'builder-default.log', clone)
    code = ('import json, sys; sys.path.insert(0, sys.argv[1]); import endstation_builder as eb; '
            'cfg = eb.load_config(sys.argv[2]); print(json.dumps([eb.emit_soc_argv(cfg), cfg["name"]]))')
    argv, name = json.loads(subprocess.run([py, '-B', '-c', code, str(clone / 'sw/builder'), str(cfgpath)], cwd=clone,
                                           check=True, capture_output=True, text=True).stdout)
    argv += ['--entity-gen-dir', str(clone / 'configs/generated' / name), '--output-dir', str(w / 'soc'),
             '--no-compile-software']
    rc_e = run([py, '-B', '-c', CHILD, str(clone), json.dumps(argv), str(w / 'cpu.json')], w / 'export.log',
               clone / 'sw/litex')
    cpu = json.loads((w / 'cpu.json').read_text())
    import pythondata_cpu_vexiiriscv as vex
    files = {f'builder/{p.relative_to(w / "builder")}': p.read_bytes()
             for p in sorted((w / 'builder').rglob('*')) if p.is_file()}
    files['cpu/netlist-name'] = str(cpu['netlist']).encode()
    nl = Path(vex.data_location) / f"{cpu['netlist']}.v"
    files['cpu/netlist.v sha256'] = hashlib.sha256(nl.read_bytes()).hexdigest().encode() if nl.exists() else b'absent'
    files['cpu/rows'] = json.dumps(cpu['rows']).encode()
    files['cpu/vexii_args'] = str(cpu['vexii_args']).encode()
    files['export/refusal'] = str(cpu['error']).encode()
    for rel in ('csr.csv', 'csr.json', 'software/include/generated/soc.h'):
        p = w / 'soc' / rel
        if p.exists():
            files[f'soc/{rel}'] = p.read_bytes()
    for p in sorted((w / 'soc/gateware').glob('*.v')):
        files[f'soc/gateware/{p.name}'] = p.read_bytes()
    for k in list(files):
        files[k] = files[k].replace(str(clone).encode(), b'<clone>').replace(str(w).encode(), b'<work>')
    return files, dict(builder=rc_b, builder_default=rc_d, export=rc_e), cpu


def main():
    base, head, work, out = (Path(a).resolve() for a in sys.argv[1:5])
    (work / 'diffs').mkdir(parents=True, exist_ok=True)
    lines, bad = [], 0
    for config in sorted(p.stem for p in (head / 'configs').glob('*.yaml')):
        b, rb, cb = side(base, work / 'base' / config, config)
        h, rh, ch = side(head, work / 'head' / config, config)
        keys = sorted(set(b) | set(h))
        raw = [k for k in keys if b.get(k) != h.get(k)]
        real = [k for k in raw if k not in b or k not in h or strip(k, b[k]) != strip(k, h[k])]
        for k in raw:
            d = difflib.unified_diff(b.get(k, b'').decode(errors='replace').splitlines(),
                                     h.get(k, b'').decode(errors='replace').splitlines(), 'base', 'head', lineterm='', n=0)
            (work / 'diffs' / f'{config}--{k.replace("/", "_")}.diff').write_text('\n'.join(d) + '\n')
        bad += bool(real)
        lines.append(f'{config}: {len(keys)} entries; raw differ {len(raw)} {raw}; differ with comments stripped '
                     f'{len(real)} {real}; netlist base {cb["netlist"]} head {ch["netlist"]}; '
                     f'refusal base {cb["error"]!s:.160} | head {ch["error"]!s:.160}; rc base {rb} head {rh}')
        print(lines[-1], flush=True)
    out.write_text('\n'.join(lines) + '\n')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
