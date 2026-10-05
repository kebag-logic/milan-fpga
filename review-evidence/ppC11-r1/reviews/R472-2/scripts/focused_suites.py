#!/usr/bin/env python3
"""Run three small interface suites concurrently, bounded to 12 build workers."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess

def main():
    p=argparse.ArgumentParser()
    p.add_argument('repo',type=Path)
    p.add_argument('scratch',type=Path)
    p.add_argument('receipts',type=Path)
    p.add_argument('simulator',type=Path)
    a=p.parse_args()
    repo=a.repo.resolve(); scratch=a.scratch.resolve(); receipts=a.receipts.resolve()
    identity=subprocess.check_output([str(a.simulator),'--version'],text=True)
    assert '5.050' in identity,identity
    (receipts/'simulator-identity.txt').write_text(identity)
    tree=scratch/'suite-tree'
    subprocess.run(['git','clone','--shared','--quiet',str(repo),str(tree)],check=True)
    wrapper=scratch/'simulator-bounded'
    wrapper.write_text('#!/usr/bin/env python3\nimport os, sys\na=sys.argv[1:]\nfor i,v in enumerate(a[:-1]):\n    if v == "-j": a[i+1]="4"\nos.execv('+repr(str(a.simulator))+', ['+repr(str(a.simulator))+']+a)\n')
    wrapper.chmod(0o755)
    def run(suite):
        command=['make','-j16','VERILATOR='+str(wrapper)]
        with (receipts/(suite+'.log')).open('w') as out:
            out.write('command: '+repr(command)+'\n');out.flush()
            result=subprocess.run(command,cwd=tree/'tb'/suite,stdout=out,stderr=subprocess.STDOUT,timeout=480)
        (receipts/(suite+'.rc')).write_text(str(result.returncode)+'\n')
        return dict(suite=suite,rc=result.returncode)
    with ThreadPoolExecutor(max_workers=3) as pool:
        results=list(pool.map(run,['side_port','tx_arbiter','rx_validator']))
    (receipts/'focused-suites.json').write_text(json.dumps(results,indent=2)+'\n')
    print(identity.strip(),results)
    assert all(x['rc']==0 for x in results)

if __name__=='__main__':
    main()
