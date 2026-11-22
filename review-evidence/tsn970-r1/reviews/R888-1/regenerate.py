#!/usr/bin/env python3
"""Regenerate all three stack tables in a disposable exact-head source copy."""
import pathlib,subprocess,sys
p=pathlib.Path(__file__).resolve().parent
root=pathlib.Path(sys.argv[1]).resolve()
copy=p/'scratch/doc-stack';copy.mkdir(parents=True,exist_ok=True)
subprocess.run(['tar','-x','-C',str(copy)],input=subprocess.check_output(['git','-C',str(root),'archive','HEAD']),check=True)
log=''
for script in ('traceability.py','test_inventory.py'):
    cmd=['python3','scripts/'+script,'--write','--build',str(p/'scratch/doc-build'),'--jobs','4']
    q=subprocess.run(cmd,cwd=copy,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log+='$ '+' '.join(cmd)+'\n'+q.stdout+'\nrc='+str(q.returncode)+'\n'
    assert q.returncode==0,log
for f in ('docs/REQUIREMENTS.md','docs/TRACEABILITY.md','docs/TESTS.md'):
    same=(root/f).read_bytes()==(copy/f).read_bytes()
    log+=f+' byte-identical after generators: '+str(same)+'\n'
    assert same,f
(p/'receipts/regeneration.log').write_text(log.replace(str(p),'$PACKET'))
print(log[-450:])
