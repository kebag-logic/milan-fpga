import json, runpy, subprocess, sys
from pathlib import Path
from unittest.mock import patch
cross={str(Path.home()/"br-milan-rv32/host/bin/riscv32-linux-gcc"),"riscv64-elf-gcc","riscv32-unknown-elf-gcc"}
real_run=subprocess.run
records=Path(__file__).with_name("builder-absent-argv.jsonl")
def selected_run(args,*positional,**keyword):
 if isinstance(args,(list,tuple)) and args and str(args[0]) in cross:
  with records.open("a") as f:f.write(json.dumps(dict(requested=list(args),result="deliberately absent RV32 compiler"))+"\n")
  raise FileNotFoundError("deliberately absent RV32 candidate")
 return real_run(args,*positional,**keyword)
sys.argv=["sw/builder/test_builder.py"]
with patch("subprocess.run",selected_run):runpy.run_path("sw/builder/test_builder.py",run_name="__main__")
