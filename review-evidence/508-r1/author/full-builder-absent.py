from pathlib import Path
import json,runpy,subprocess,sys
from unittest.mock import patch
cross={str(Path.home()/'br-milan-rv32/host/bin/riscv32-linux-gcc'),'riscv64-elf-gcc','riscv32-unknown-elf-gcc'}
records=Path(__file__).with_name('full-builder-absent-argv.jsonl')
real_run=subprocess.run
hidden=set()
def selected_run(args,*positional,**keyword):
 if isinstance(args,(list,tuple)) and args and str(args[0]) in cross:
  hidden.add(str(args[0]))
  with records.open('a') as f:f.write(json.dumps(dict(requested=list(args),executed=None,result='deliberately absent'))+'\n')
  raise FileNotFoundError('deliberately absent RV32 candidate')
 return real_run(args,*positional,**keyword)
sys.argv=['sw/builder/test_builder.py']
with patch('subprocess.run',selected_run):runpy.run_path('sw/builder/test_builder.py',run_name='__main__')
assert hidden == cross, hidden
