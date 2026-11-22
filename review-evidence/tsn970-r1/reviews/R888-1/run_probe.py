#!/usr/bin/env python3
"""Compare public API draw populations without editing either source checkout."""
import os,pathlib,subprocess,sys
p=pathlib.Path(__file__).resolve().parent
root=pathlib.Path(sys.argv[1]).resolve()
base=p/'scratch/base-stack';base.mkdir(parents=True,exist_ok=True)
subprocess.run(['tar','-x','-C',str(base)],input=subprocess.check_output(['git','-C',str(root),'archive','715589c1db7cf67e2f3259fd7083ebc7f0923376']),check=True)
lines=[]
for name,src in [('base',base),('head',root)]:
    exe=p/'scratch'/('draw-'+name)
    subprocess.run([os.environ.get('CC','gcc'),'-std=c11','-O2','-Wall','-Wextra','-Werror','-I'+str(src/'include'),str(p/'draw_probe.c'),str(src/'src/adp.c'),'-o',str(exe)],check=True)
    r=subprocess.run([str(exe)],capture_output=True,text=True,check=True)
    lines.append(name+'\n'+r.stdout)
text='\n'.join(lines)
(p/'receipts/draw-distribution.txt').write_text(text)
print(text)
