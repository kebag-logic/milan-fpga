# SPDX-License-Identifier: Apache-2.0
"""Run one foreground check; publish output with location-only substitutions."""
import argparse, os, pathlib, subprocess, sys
p=argparse.ArgumentParser()
p.add_argument('--source',type=pathlib.Path,required=True)
p.add_argument('--packet',type=pathlib.Path,required=True)
p.add_argument('--label',required=True)
p.add_argument('--cwd',type=pathlib.Path)
p.add_argument('command',nargs=argparse.REMAINDER)
a=p.parse_args(); cmd=a.command[1:] if a.command[:1]==['--'] else a.command
root=a.packet.resolve(); (root/'receipts').mkdir(exist_ok=True)
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
env['LD_LIBRARY_PATH']=str(root/'scratch/prefix/lib')+':'+env.get('LD_LIBRARY_PATH','')
r=subprocess.run(cmd,cwd=a.cwd or a.source,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=540)
raw=r.stdout;(root/'scratch'/f'{a.label}.raw.log').write_text(raw)
for old,new in [(str(a.source.resolve()),'SOURCE'),(str(root),'PACKET'),(str(pathlib.Path.home()),'USER_HOME')]:raw=raw.replace(old,new)
raw=raw.replace('/usr/bin/','SYSTEM_BIN/').replace('/tmp/','TEMP/')
(root/'receipts'/f'{a.label}.log').write_text('# SPDX-License-Identifier: Apache-2.0\n'+raw)
(root/'receipts'/f'{a.label}.rc').write_text(str(r.returncode)+'\n')
print(a.label+': rc='+str(r.returncode)); print(raw[-3500:]);sys.exit(r.returncode)
