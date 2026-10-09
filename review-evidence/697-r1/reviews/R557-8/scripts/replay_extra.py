#!/usr/bin/env python3
import json,os,pathlib,subprocess,sys
r=pathlib.Path(sys.argv[1]).resolve();p=pathlib.Path(sys.argv[2]).resolve();w=p/'scratch/replays';w.mkdir(exist_ok=True)
e=dict(os.environ);e.update(json.loads((p/'scratch/environment.json').read_text()))
def run(name,args):
 with (w/(name+'.log')).open('w') as f:rc=subprocess.run(args,cwd=r,env=e,stdout=f,stderr=subprocess.STDOUT).returncode
 (w/(name+'.rc')).write_text(str(rc)+'\n');print(name,rc);return rc
s=p/'scratch/prior-public'
assert run('document-lint',[sys.executable,str(s/'R556-3/scripts/doc_lint.py'),str(r),'docs/CODING_STANDARD.md','docs/VERIFICATION.md'])==0
assert run('document-links',[sys.executable,str(s/'R557-6/scripts/check_documents.py'),str(r),str(w/'document-links.json')])==0
assert run('adp-input-build',['gcc','-std=c11','-Wall','-Wextra','-Werror','-Iinclude','-Iexamples',str(s/'R557-1/scripts/adp_input_probe.c'),'src/adp.c','examples/adp_port.c','-o',str(w/'adp-input')])==0
assert run('adp-input',[str(w/'adp-input')])==1
assert 'malformed input controls accepted: 3/3' in (w/'adp-input.log').read_text()
