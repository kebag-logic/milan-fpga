#!/usr/bin/env python3
"""Isolate cached CPU inputs and limit native compilation to sixteen jobs."""
import json, os, shutil
from pathlib import Path
packet=Path(os.environ['REVIEW_PACKET']); scratch=packet/'scratch'
import pythondata_cpu_vexiiriscv as cpu
src=Path(cpu.__file__).parent; dest=scratch/'python/pythondata_cpu_vexiiriscv'
(dest/'verilog').mkdir(parents=True,exist_ok=True)
shutil.copy2(src/'__init__.py',dest/'__init__.py')
names=set()
for label in ('A1','A8'):
    spec=json.loads((scratch/'public/author-r3/receipts/builds'/f'{label}.build.json').read_text())
    names.update(Path(s).name for s in spec['sources'] if 'pythondata' in s)
for p in (src/'verilog').iterdir():
    if p.is_file() and (p.suffix=='.py' or p.name in names):shutil.copy2(p,dest/'verilog'/p.name)
(scratch/'python/sitecustomize.py').write_text('from litex.soc.cores.cpu.vexiiriscv.core import VexiiRiscv\n'
    'def refuse_generation():\n    raise RuntimeError("cached CPU input missing; generation disabled")\n'
    'VexiiRiscv.generate_netlist = staticmethod(refuse_generation)\n')
(scratch/'bin').mkdir(exist_ok=True)
(scratch/'bin/make').write_text('#!/usr/bin/python3\nimport fcntl, os, subprocess, sys\n'
    'with open(os.environ["REVIEW_PACKET"]+"/scratch/compile.lock","w") as lock:\n'
    '    fcntl.flock(lock,fcntl.LOCK_EX)\n'
    '    raise SystemExit(subprocess.call(["/usr/bin/make",*sys.argv[1:]]))\n')
(scratch/'bin/make').chmod(0o755)
print('Isolated cached CPU package; native make invocations serialized at -j16.')
