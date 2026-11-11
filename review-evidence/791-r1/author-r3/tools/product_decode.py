#!/usr/bin/env python3
"""product_decode.py <clone> <work> <out> <shape>...: the product split export of each shape and its CPU decode (#791).

For each shape: the builder's all-fabric argv plus --ctrl-mailbox --ctrl-firmware (the split SoC, as
test_ctrl_memory.py's split export builds it), on a stand-in image of the shape at the split layout; the export
run in a child with ctrl_memory.cpu_regions wrapped to record the rows it is handed; then
tb/verilator/ctrl_region_decode/decode.py on the netlist against those rows and the CPU's own devices
(csr.csv's linker rows). Writes <out>/<shape>.txt with clone and scratch paths replaced.
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
import ctrl_memory, milan_soc
from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv
handed = []
split = ctrl_memory.cpu_regions
def recording(rows):
    handed.append([list(r) for r in rows])
    return split(rows)
ctrl_memory.cpu_regions = recording
sys.argv = ["milan_soc.py", *argv]
milan_soc.main()
dump.write_text(json.dumps({"netlist": VexiiRiscv.netlist_name, "soc_rows": handed,
                            "cpu_rows": [list(r) for r in VexiiRiscv.memory_regions]}, indent=1))
'''


def run(argv, log, cwd):
    with open(log, 'w') as sink:
        rc = subprocess.run(argv, cwd=cwd, stdout=sink, stderr=subprocess.STDOUT, check=False).returncode
    if rc:
        raise SystemExit(f'{argv[1] if len(argv) > 1 else argv[0]} exited {rc}; see {log}')


def main():
    clone, work, out = (Path(a).resolve() for a in sys.argv[1:4])
    shapes = sys.argv[4:]
    py = sys.executable
    work.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    runtime = work / 'runtime'
    if not (runtime / 'libc.a').exists():
        code = ('import sys, subprocess, litex; from pathlib import Path; import pythondata_software_compiler_rt as crt, '
                'pythondata_software_picolibc as pl; sys.exit(subprocess.run([sys.executable, "-B", '
                '"tb/verilator/ctrl_service_budget/runtime_ssp.py", "--picolibc", pl.data_location, "--compiler-rt", '
                f'crt.data_location, "--litex-software", str(Path(litex.__file__).parent / "soc/software"), "--output", '
                f'"{runtime}"]).returncode)')
        run([py, '-B', '-c', code], work / 'runtime.log', clone)
    sys.path.insert(0, str(clone / 'sw/builder'))
    sys.path.insert(0, str(clone / 'tb/verilator/ctrl_region_decode'))
    import endstation_builder as eb
    import decode
    for shape in shapes:
        w = work / shape
        w.mkdir(exist_ok=True)
        config = clone / 'configs' / f'{shape}.yaml'
        cfg = eb.load_config(str(config))
        run([py, '-B', 'sw/builder/endstation_builder.py', str(config)], w / 'builder.log', clone)
        run([py, '-B', 'sw/firmware/ctrl/test/ctrl_srp_image.py', '--config', str(config), '--interfaces', '1',
             '--with-aecp', '--layout', 'split', '--output', str(w / 'img'), '--libc', str(runtime / 'libc.a'),
             '--compiler-runtime', str(runtime / 'libcompiler_rt.a')], w / 'img.log', clone)
        argv = [*eb.emit_soc_argv(cfg), '--entity-gen-dir', str(clone / 'configs/generated' / cfg['name']),
                '--ctrl-mailbox', '--ctrl-firmware', str(w / 'img/ctrl_app.elf'), '--output-dir', str(w / 'soc'),
                '--no-compile-software']
        run([py, '-B', '-c', CHILD, str(clone), json.dumps(argv), str(w / 'decode.json')], w / 'export.log',
            clone / 'sw/litex')
        got = json.loads((w / 'decode.json').read_text())
        rows = [r for r in (ln.split(',') for ln in (w / 'soc/csr.csv').read_text().splitlines())
                if r[0] == 'memory_region' and 'linker' in r[4]]
        devices = [[int(r[2], 16), int(r[3]), 'rw', 'p'] for r in rows]
        import pythondata_cpu_vexiiriscv as vex
        netlist = Path(vex.data_location) / f"{got['netlist']}.v"
        text = netlist.read_text()
        lines = [f'shape {shape} (config {cfg["name"]}), split export: the builder argv + --ctrl-mailbox --ctrl-firmware',
                 f'netlist {got["netlist"]}.v sha256 {hashlib.sha256(text.encode()).hexdigest()} '
                 f'({len(text.encode())} bytes)',
                 f'normalised sha256 (netlist name replaced) '
                 f'{hashlib.sha256(re.sub(r"VexiiRiscvLitex_[0-9a-f]+", "VexiiRiscvLitex_X", text).encode()).hexdigest()}',
                 'rows LiteX collected (handed to ctrl_memory.cpu_regions):',
                 *[f'  [0x{o:08x}, +0x{s:x}) {m} {b}' for o, s, m, b in got['soc_rows'][0]],
                 'rows the generator was handed:',
                 *[f'  [0x{o:08x}, +0x{s:x}) {m} {b}' for o, s, m, b in got['cpu_rows']],
                 'the CPU devices (csr.csv linker rows): ' + ', '.join(f'[0x{o:08x}, +0x{s:x})' for o, s, *_ in devices),
                 'the netlist bus decoder, one compare per row:',
                 *['  ' + ln.strip() for ln in text.splitlines() if re.match(r'\s*assign argsHits_\d+_addrHit = ', ln)],
                 'the netlist PMA fault terms:',
                 *['  ' + ln.strip() for ln in text.splitlines()
                   if re.match(r'\s*assign (FetchL1Plugin_logic_ctrl_pmaPort_rsp_fault|'
                               r'LsuCachelessPlugin_logic_onPma_port_rsp_fault) = ', ln)]]
        results = decode.check(netlist, got['soc_rows'][0] + devices)
        lines += [f'DECODE {"PASS" if ok else "FAIL"} {name}: {detail}' for name, ok, detail in results]
        report = '\n'.join(lines) + '\n'
        report = report.replace(str(clone), '<clone>').replace(str(work), '<work>')
        (out / f'{shape}.txt').write_text(report)
        print(report)
        if not all(ok for _, ok, _ in results):
            raise SystemExit(f'{shape}: the decode is not exact')


if __name__ == '__main__':
    main()
