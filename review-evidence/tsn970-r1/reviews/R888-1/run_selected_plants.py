#!/usr/bin/env python3
"""Restrict only a disposable copy's mutation registry to the seven changed plants."""
import json, os, pathlib, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve()
p=pathlib.Path(__file__).resolve().parent
copy=p/'scratch/selected-stack'
copy.mkdir(exist_ok=True)
subprocess.run(['tar','-x','-C',str(copy)],input=subprocess.check_output(['git','-C',str(root),'archive','HEAD']),check=True)
names={'link-up-draws-startup-kind','draw-kinds-merged','link-up-draws-delay-kind','link-up-range-is-the-delay-range','every-draw-the-first-range','startup-range-two-seconds','link-up-range-four-seconds'}
table=json.loads((copy/'tests/mutations.json').read_text())
table=[m for m in table if m['name'] in names]
assert len(table)==7
(copy/'tests/mutations.json').write_text(json.dumps(table))
cmd=['python3','scripts/mutation.py','--work',str(p/'scratch/selected-plants'),'--jobs','4']
r=subprocess.run(cmd,cwd=copy,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
(p/'receipts/selected-plants.log').write_text(r.stdout.replace(str(p),'$PACKET'))
(p/'receipts/selected-plants.rc').write_text(str(r.returncode)+'\n')
print('selected-plants',r.returncode)
sys.exit(r.returncode)
