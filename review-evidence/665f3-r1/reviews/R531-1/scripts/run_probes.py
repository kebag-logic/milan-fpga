#!/usr/bin/env python3
import concurrent.futures,os,shutil,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve();packet=Path(sys.argv[2]).resolve()
sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
import ctrl_build as cb
import fw_gtest
work=packet/'scratch/probes';work.mkdir(parents=True,exist_ok=True)
def run(n):
 src=work/('if'+str(n))/'ctrl'
 shutil.copytree(root/'sw/firmware/ctrl',src,dirs_exist_ok=True)
 if n==2:
  gen=src.parent/'gen'
  subprocess.run([sys.executable,'-B',str(root/'sw/mailbox/gen_mailbox.py'),'--variant-interfaces','2','--out',str(gen)],check=True,capture_output=True)
  shutil.copyfile(gen/'mbx_contract.h',src/'mbx/mbx_contract.h')
 tree=cb.Tree(src,src.parent/'build',work,fw_gtest.Build(jobs=4))
 objects=cb.firmware(tree,cb.PORTABLE,'firmware')
 objects+=fw_gtest.compile_tests(tree.build,cb.includes(tree),[packet/'scripts/independent_probes.cpp'],tree.out/'tests')
 exe=cb.link(tree,'independent_probes',objects)
 result=subprocess.run([str(exe)],capture_output=True,text=True)
 (packet/'receipts'/('independent-if'+str(n)+'.log')).write_text(result.stdout+result.stderr)
 (packet/'receipts'/('independent-if'+str(n)+'.rc')).write_text(str(result.returncode)+'\n')
 print('interfaces',n,'test rc',result.returncode,flush=True)
 return result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(run,[1,2]))
# These are specification assertions; a test failure is preserved, not treated as a passing gate.
print('Probe run completed; inspect the specification failures in the receipts.')
