import json, pathlib, runpy, subprocess, sys
from unittest.mock import patch
root=pathlib.Path.cwd()
cross={str(pathlib.Path.home()/"br-milan-rv32/host/bin/riscv32-linux-gcc"), "riscv64-elf-gcc", "riscv32-unknown-elf-gcc"}
original=subprocess.run
hidden=set()
def run(argv, *args, **kwargs):
    if not isinstance(argv, str) and str(argv[0]) in cross:
        hidden.add(str(argv[0]))
        raise FileNotFoundError("Deliberately absent cross compiler for full builder control")
    return original(argv,*args,**kwargs)
sys.path.insert(0,str(root/"sw/builder"))
sys.argv=[str(root/"sw/builder/test_builder.py"), "--require-elaboration"]
try:
    with patch.object(subprocess,"run",side_effect=run):
        runpy.run_path(sys.argv[0],run_name="__main__")
finally:
    print("Full builder compiler-absent candidates:",json.dumps(sorted(hidden)))
