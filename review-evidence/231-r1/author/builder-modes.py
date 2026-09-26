from pathlib import Path
import json, os, runpy, subprocess, sys
from unittest.mock import patch
mode=sys.argv[1]
out=Path('$MANAGEMENT/2026-09-23/231-a328/gates')
native=str(Path.home()/'br-milan-rv32/host/bin/riscv32-linux-gcc')
compiler='$VALIDATION_STORAGE/504-manager-r1/sdk-install/bin/riscv32-linux-gcc'
cross={native,'riscv64-elf-gcc','riscv32-unknown-elf-gcc'}
records=out/f'builder-{mode}-compiler.jsonl'
real_run=subprocess.run
with records.open('w') as audit:
    def selected_run(args,*positional,**keyword):
        if isinstance(args,(list,tuple)) and args and str(args[0]) in cross:
            requested=list(map(str,args))
            if mode=='absent':
                audit.write(json.dumps(dict(requested=requested,executed=None,result='deliberately absent'))+'\n')
                audit.flush()
                raise FileNotFoundError('deliberately absent RV32 compiler')
            if str(args[0])==native:
                actual=[compiler,*args[1:]]
                result=real_run(actual,*positional,**keyword)
                audit.write(json.dumps(dict(requested=requested,executed=list(map(str,actual)),exit_code=result.returncode))+'\n')
                audit.flush()
                return result
        return real_run(args,*positional,**keyword)
    if mode=='sdk':
        real_run(['python3','scripts/ci_rv32_sdk.py','--destination',str(Path(compiler).parents[1]),'--verify-only'],check=True)
    elif mode!='absent':
        raise ValueError(mode)
    print('Full builder mode:',mode,flush=True)
    sys.argv=['sw/builder/test_builder.py']+(['--require-rv32'] if mode=='sdk' else [])
    with patch('subprocess.run',selected_run):
        runpy.run_path('sw/builder/test_builder.py',run_name='__main__')
