#!/usr/bin/env python3
"""allfabric_compare.py <base-clone> <head-clone> <work> <out>: the all-fabric SoC's generated CPU, base against head (#791).

For every shipped config (configs/*.yaml): the builder's outputs (endstation_builder.py -o, and again into its
default output directory, which the export reads), then milan_soc.py's
export on the builder's own argv (emit_soc_argv, the all-fabric placement: no --ctrl-mailbox), with no software
and no Vivado, at each side. Compared file by file: every builder output, and the export's CPU netlist (its name
and bytes), the region rows the generator was handed, the top Verilog, csr.csv, csr.json and soc.h with each
side's own paths replaced. Writes <out>/allfabric-compare.txt; exit 0 when every pair is byte-identical.
"""
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
except Exception as exc:     # the CPU may have named its netlist before a later refusal; keep both
    error = f"{type(exc).__name__}: {exc}"
dump.write_text(json.dumps({"netlist": VexiiRiscv.netlist_name,
                            "rows": [list(r) for r in getattr(VexiiRiscv, "memory_regions", [])],
                            "vexii_args": VexiiRiscv.vexii_args, "error": error}, indent=1))
sys.exit(1 if error else 0)
'''


def run(argv, log, cwd):
    with open(log, 'w') as sink:
        rc = subprocess.run(argv, cwd=cwd, stdout=sink, stderr=subprocess.STDOUT, check=False).returncode
    return rc


def side(clone: Path, work: Path, config: str) -> tuple[dict, list[str]]:
    """One side's builder outputs and export; the files to compare, by relative name, and its failures."""
    py = sys.executable
    w = work / config
    w.mkdir(parents=True, exist_ok=True)
    fails = []
    if run([py, '-B', 'sw/builder/endstation_builder.py', f'configs/{config}.yaml', '-o', str(w / 'builder')],
           w / 'builder.log', clone):
        fails.append(f'{config}: builder exited nonzero')
    # the export reads the builder's default output directory (sw/builder/out/<name>, ignored by git)
    if run([py, '-B', 'sw/builder/endstation_builder.py', f'configs/{config}.yaml'], w / 'builder-default.log', clone):
        fails.append(f'{config}: builder (default output) exited nonzero')
    sys.path.insert(0, str(clone / 'sw/builder'))
    code = ('import json, sys; sys.path.insert(0, sys.argv[1]); import endstation_builder as eb; '
            'cfg = eb.load_config(sys.argv[2]); print(json.dumps([eb.emit_soc_argv(cfg), cfg["name"]]))')
    argv, name = json.loads(subprocess.run([py, '-B', '-c', code, str(clone / 'sw/builder'),
                                            str(clone / 'configs' / f'{config}.yaml')], cwd=clone, check=True,
                                           capture_output=True, text=True).stdout)
    argv += ['--entity-gen-dir', str(clone / 'configs/generated' / name), '--output-dir', str(w / 'soc'),
             '--no-compile-software']
    rc = run([py, '-B', '-c', CHILD, str(clone), json.dumps(argv), str(w / 'cpu.json')], w / 'export.log',
             clone / 'sw/litex')
    if not (w / 'cpu.json').exists():
        fails.append(f'{config}: export exited {rc} before naming its CPU')
        return {}, fails
    cpu = json.loads((w / 'cpu.json').read_text())
    if not cpu['netlist']:
        fails.append(f'{config}: no CPU netlist named ({cpu["error"]})')
        return {}, fails
    import pythondata_cpu_vexiiriscv as vex
    files = {f'builder/{p.relative_to(w / "builder")}': p.read_bytes()
             for p in sorted((w / 'builder').rglob('*')) if p.is_file()}
    files['cpu/netlist-name'] = cpu['netlist'].encode()
    files['cpu/netlist.v'] = (Path(vex.data_location) / f"{cpu['netlist']}.v").read_bytes()
    files['cpu/rows'] = json.dumps(cpu['rows']).encode()
    files['cpu/vexii_args'] = cpu['vexii_args'].encode()
    files['export/refusal'] = (cpu['error'] or 'none').encode()
    for rel in ('csr.csv', 'csr.json', 'software/include/generated/soc.h'):
        p = w / 'soc' / rel
        if p.exists():
            files[f'soc/{rel}'] = p.read_bytes()
    for p in sorted((w / 'soc/gateware').glob('*.v')):
        files[f'soc/gateware/{p.name}'] = p.read_bytes()
    for key in list(files):
        files[key] = files[key].replace(str(clone).encode(), b'<clone>').replace(str(w).encode(), b'<work>')
        if key.startswith('soc/') and key.endswith(('.v', '.h')):
            # LiteX's header: a /* */ block (its hierarchy listing, whose order varies run to run) and // lines
            body = re.sub(rb'/\*.*?\*/', b'', files[key], flags=re.S)
            files[key + ' (comment lines set aside)'] = b'\n'.join(
                ln for ln in body.splitlines() if not ln.lstrip().startswith(b'//'))
        if key.endswith('csr.csv'):
            # its banner: '#' lines carrying the export's time
            files[key + ' (comment lines set aside)'] = b'\n'.join(
                ln for ln in files[key].splitlines() if not ln.startswith(b'#'))
    return files, fails


def main():
    base, head, work, out = (Path(a).resolve() for a in sys.argv[1:5])
    out.mkdir(parents=True, exist_ok=True)
    configs = sorted(p.stem for p in (head / 'configs').glob('*.yaml'))
    lines, fails = [], []
    for config in configs:
        got = {}
        for label, clone in (('base', base), ('head', head)):
            got[label], f = side(clone, work / label, config)
            fails += [f'{label} {x}' for x in f]
        keys = sorted(set(got['base']) | set(got['head']))
        differ = [k for k in keys if got['base'].get(k) != got['head'].get(k)]
        name = got['head'].get('cpu/netlist-name', b'?').decode()
        sha = hashlib.sha256(got['head'].get('cpu/netlist.v', b'')).hexdigest()
        refusal = got['head'].get('export/refusal', b'?').decode()
        aside = ' (comment lines set aside)'
        comments = [k for k in differ if (k + aside) in keys and got['base'].get(k + aside) == got['head'].get(k + aside)]
        real = [k for k in differ if k not in comments]
        lines.append(f'{config}: {len(keys)} entries, {len(differ)} differ ({len(comments)} only in comment lines: '
                     f'{comments}); CPU netlist {name} sha256 {sha}; export refusal at head: {refusal}'
                     + (f'; DIFFER: {real}' if real else ''))
        fails += [f'{config}: {k} differs' for k in real]
        if got['base'].get('export/refusal') not in (None, b'none') and \
                got['base'].get('export/refusal') == got['head'].get('export/refusal'):
            lines.append(f'  {config}: the export is refused after the CPU is named, at base and head alike')
    git = lambda c: subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=c, capture_output=True, text=True).stdout.strip()
    dirty = [str(c) for c in (base, head) if subprocess.run(['git', 'status', '--porcelain'], cwd=c,
                                                            capture_output=True, text=True).stdout.strip()]
    report = [f'base {git(base)}', f'head {git(head)}', *lines,
              f'trees clean after the runs: {"yes" if not dirty else "NO: " + ", ".join(dirty)}',
              f'{len(fails)} failure(s)' + (': ' + '; '.join(fails) if fails else '')]
    text = '\n'.join(report).replace(str(base), '<base>').replace(str(head), '<head>').replace(str(work), '<work>')
    (out / 'allfabric-compare.txt').write_text(text + '\n')
    print(text)
    return 1 if fails or dirty else 0


if __name__ == '__main__':
    sys.exit(main())
