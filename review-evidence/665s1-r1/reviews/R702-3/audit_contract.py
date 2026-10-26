#!/usr/bin/env python3
"""Compare existing contract structure and unchanged external scope to the base."""
import json,pathlib,subprocess,sys,yaml
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(__file__).resolve().parent
base='e76a755afc0536453161e3cd33f6f4d2dcd7641f'
old=yaml.safe_load(subprocess.check_output(['git','show',base+':sw/mailbox/mailbox.yaml'],cwd=root))
new=yaml.safe_load((root/'sw/mailbox/mailbox.yaml').read_text())
changes=[]; additions=[]
def walk(a,b,path):
    if isinstance(a,dict):
        for key,value in a.items():
            if key not in b: changes.append([path+'.'+str(key),'REMOVED'])
            elif key!='doc': walk(value,b[key],path+'.'+str(key))
        additions.extend(path+'.'+str(key) for key in b if key not in a)
    elif isinstance(a,list):
        if len(b)<len(a): changes.append([path,'SHORTENED'])
        for i,value in enumerate(a):
            if i<len(b): walk(value,b[i],path+'['+str(i)+']')
        if len(b)>len(a): additions.append([path,len(b)-len(a)])
    elif a!=b: changes.append([path,a,b])
walk(old,new,'contract')
assert changes==[['contract.version.minor',2,3]],changes
(packet/'additivity.json').write_text(json.dumps({'existing_changes':changes,'additions':additions},indent=2)+'\n')
paths=['hdl/milan/milan_datapath.sv','hdl/common/csr/milan_csr.sv','docs/reference/REGISTER_MAP.md',
       '.github','scripts/ci_gate_workflows.py']
for path in paths:
    assert not subprocess.check_output(['git','diff','--name-only',base+'..HEAD','--',path],cwd=root),path
(packet/'unchanged-scope.json').write_text(json.dumps({'byte_identical_paths':paths,'version':'0x0002_0060'},indent=2)+'\n')
print('PASS: additive 2.3; external scope and VERSION unchanged')
