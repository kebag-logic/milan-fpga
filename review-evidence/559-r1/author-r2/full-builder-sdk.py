from pathlib import Path
import json,runpy,subprocess,sys
from unittest.mock import patch
native=str(Path.home()/'br-milan-rv32/host/bin/riscv32-linux-gcc')
bootlin='$VALIDATION_STORAGE/504-manager-r1/sdk-install/bin/riscv32-linux-gcc'
records=Path('$MANAGEMENT/2026-09-23/559-a309/builder-sdk-argv.jsonl')
assert not records.exists()
real_run=subprocess.run
def selected_run(args,*positional,**keyword):
 if isinstance(args,(list,tuple)) and args and str(args[0])==native:
  actual=[bootlin,*args[1:]]
  result=real_run(actual,*positional,**keyword)
  with records.open('a') as f:f.write(json.dumps(dict(requested=list(args),executed=actual,exit_code=result.returncode))+'\n')
  return result
 return real_run(args,*positional,**keyword)
subprocess.run(['python3','scripts/ci_rv32_sdk.py','--destination',str(Path(bootlin).parents[1]),'--verify-only'],check=True)
print('Exact compiler argv mapping:',native,'->',bootlin,flush=True)
sys.argv=['sw/builder/test_builder.py','--require-rv32']
with patch('subprocess.run',selected_run):runpy.run_path('sw/builder/test_builder.py',run_name='__main__')
assert records.exists() and records.stat().st_size>0
