#!/usr/bin/env python3
"""product_split.py <clone> <work> <elf> <shape>...: the product split export of each AX7101 shape (the builder's
argv plus --ctrl-mailbox --ctrl-firmware), and the region rows its CPU generator was handed.

Run with the review's generation guard on PYTHONPATH, so an uncached netlist is refused, never generated. For
each shape writes <work>/<shape>/cpu.json: the netlist name, the rows the generator was handed
(VexiiRiscv.memory_regions after finalize), and the SoC's own regions from csr.csv (non-linker memory_region
rows: the SoC bus regions; linker rows: the CPU's own devices), as [[origin, size, mode-from-csr, bus], ...].
"""
import json
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
dump.write_text(json.dumps({"netlist": VexiiRiscv.netlist_name, "error": error,
                            "handed": [list(r) for r in getattr(VexiiRiscv, "memory_regions", [])],
                            "vexii_args": VexiiRiscv.vexii_args}, indent=1))
'''


def run(argv, log, cwd):
    with open(log, 'w') as sink:
        return subprocess.run(argv, cwd=cwd, stdout=sink, stderr=subprocess.STDOUT, check=False).returncode


def main():
    clone, work, elf = (Path(a).resolve() for a in sys.argv[1:4])
    py = sys.executable
    sys.path.insert(0, str(clone / 'sw/builder'))
    import endstation_builder as eb
    for shape in sys.argv[4:]:
        w = work / shape
        w.mkdir(parents=True, exist_ok=True)
        config = clone / 'configs' / f'{shape}.yaml'
        cfg = eb.load_config(str(config))
        rc = run([py, '-B', 'sw/builder/endstation_builder.py', str(config)], w / 'builder.log', clone)
        argv = [*eb.emit_soc_argv(cfg), '--entity-gen-dir', str(clone / 'configs/generated' / cfg['name']),
                '--ctrl-mailbox', '--ctrl-firmware', str(elf), '--output-dir', str(w / 'soc'), '--no-compile-software']
        (w / 'argv.json').write_text(json.dumps(argv, indent=1))
        rc2 = run([py, '-B', '-c', CHILD, str(clone), json.dumps(argv), str(w / 'child.json')], w / 'export.log',
                  clone / 'sw/litex')
        got = json.loads((w / 'child.json').read_text())
        soc, devices = [], []
        csv = w / 'soc/csr.csv'
        if csv.exists():
            for row in (ln.split(',') for ln in csv.read_text().splitlines()):
                if row[0] == 'memory_region':
                    entry = [int(row[2], 16), int(row[3]), row[4], 'p']
                    (devices if 'linker' in row[4] else soc).append(entry)
        got.update(builder_rc=rc, export_rc=rc2, soc_regions=soc, linker_regions=devices)
        (w / 'cpu.json').write_text(json.dumps(got, indent=1))
        print(shape, got['netlist'], 'error:', got['error'], 'builder rc', rc, 'export rc', rc2)


if __name__ == '__main__':
    main()
