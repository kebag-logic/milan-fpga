#!/usr/bin/env python3
"""Run focused read-only gates in joined foreground workers.

Usage: python3 run_gates.py CHECKOUT [--jobs 4]
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('checkout',type=Path)
    ap.add_argument('--jobs',type=int,default=4)
    args=ap.parse_args()
    packet=Path(__file__).resolve().parent
    receipts=packet/'receipts/gates';receipts.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(packet/'scratch'))
    checks={'capture':['python3','-B','scripts/check_nvm_capture.py'],
            'c-idiom':['python3','-B','scripts/check_cpp_idiom.py'],
            'python-idiom':['python3','-B','scripts/check_py_idiom.py'],
            'docs':['python3','-B','scripts/docs_check.py'],
            'diff':['git','diff','--check','fa450d30..HEAD']}
    def run(item):
        name,cmd=item
        with (receipts/(name+'.log')).open('w') as f:
            f.write('COMMAND '+json.dumps(cmd)+'\n');f.flush()
            r=subprocess.run(cmd,cwd=args.checkout,stdout=f,stderr=subprocess.STDOUT,
                             env=env,timeout=500)
        (receipts/(name+'.rc')).write_text(str(r.returncode)+'\n')
        print(name,r.returncode,flush=True)
        return r.returncode
    with ThreadPoolExecutor(max_workers=min(16,max(1,args.jobs))) as pool:
        result=list(pool.map(run,checks.items()))
    return int(any(result))
if __name__=='__main__':
    sys.exit(main())
