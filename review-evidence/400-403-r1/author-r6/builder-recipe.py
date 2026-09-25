from pathlib import Path
import json,runpy,subprocess,sys
from unittest.mock import patch
mode=sys.argv[1]
native=str(Path.home()/'br-milan-rv32/host/bin/riscv32-linux-gcc')
sdk='$VALIDATION_STORAGE/504-manager-r1/sdk-install/bin/riscv32-linux-gcc'
records=Path('$MANAGEMENT/2026-09-23/400-403-a323/builder-'+mode+'-argv.jsonl')
cross={native,'riscv64-elf-gcc','riscv32-unknown-elf-gcc'}
real_run=subprocess.run
with records.open('w') as audit:
 def selected_run(args,*positional,**keyword):
  if isinstance(args,(list,tuple)) and args and str(args[0]) in cross:
   if mode=='absent':
    audit.write(json.dumps(dict(requested=list(args),result='deliberately absent'))+'\n'); audit.flush()
    raise FileNotFoundError('deliberately absent RV32 candidate')
   if str(args[0])==native:
    actual=[sdk,*args[1:]]
    result=real_run(actual,*positional,**keyword)
    audit.write(json.dumps(dict(requested=list(args),executed=actual,exit_code=result.returncode))+'\n'); audit.flush()
    return result
  return real_run(args,*positional,**keyword)
 sys.argv=['sw/builder/test_builder.py','--require-rv32' if mode=='sdk' else '--require-elaboration']
 with patch('subprocess.run',selected_run):runpy.run_path('sw/builder/test_builder.py',run_name='__main__')
assert records.stat().st_size>0
