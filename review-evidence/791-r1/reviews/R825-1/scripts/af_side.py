#!/usr/bin/env python3
"""af_side.py <clone> <config> <work> [extra milan_soc argv...]: one export of a shipped config through the
builder's own argv (emit_soc_argv), run with no software and no Vivado. Records the CPU netlist name, the region
rows LiteX handed the generator, and the generator args, in <work>/cpu.json. Extra argv (e.g. --ctrl-mailbox
--ctrl-firmware ELF) is appended for the product split export."""
import json, subprocess, sys
from pathlib import Path
clone, config, work = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve()
extra = sys.argv[4:]
work.mkdir(parents=True, exist_ok=True)
py = sys.executable
def run(argv, log):
    with open(work / log, 'w') as f:
        return subprocess.run(argv, cwd=clone, stdout=f, stderr=subprocess.STDOUT).returncode
rc_b = run([py, '-B', 'sw/builder/endstation_builder.py', f'configs/{config}.yaml', '-o', str(work / 'builder')], 'builder.log')
rc_d = run([py, '-B', 'sw/builder/endstation_builder.py', f'configs/{config}.yaml'], 'builder-default.log')
sys.path.insert(0, str(clone / 'sw/builder'))
import endstation_builder as eb
cfg = eb.load_config(str(clone / 'configs' / f'{config}.yaml'))
argv = eb.emit_soc_argv(cfg) + extra + ['--entity-gen-dir', str(clone / 'configs/generated' / cfg['name']),
                                        '--output-dir', str(work / 'soc'), '--no-compile-software']
child = r'''
import json, sys
from pathlib import Path
DUMP = Path(sys.argv[3])
sys.path.insert(0, sys.argv[1] + "/sw/litex")
import milan_soc
from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv
sys.argv = ["milan_soc.py", *json.loads(sys.argv[2])]
err = None
try:
    milan_soc.main()
except BaseException as e:
    err = f"{type(e).__name__}: {e}"
DUMP.write_text(json.dumps({"netlist": VexiiRiscv.netlist_name, "rows": [list(r) for r in getattr(VexiiRiscv, "memory_regions", [])], "vexii_args": VexiiRiscv.vexii_args, "error": err}, indent=1))
'''
with open(work / 'export.log', 'w') as f:
    rc_e = subprocess.run([py, '-B', '-c', child, str(clone), json.dumps(argv), str(work / 'cpu.json')],
                          cwd=clone / 'sw/litex', stdout=f, stderr=subprocess.STDOUT).returncode
(work / 'side.json').write_text(json.dumps({'builder_rc': rc_b, 'builder_default_rc': rc_d, 'export_rc': rc_e, 'argv': argv}, indent=1))
print(config, rc_b, rc_d, rc_e)
