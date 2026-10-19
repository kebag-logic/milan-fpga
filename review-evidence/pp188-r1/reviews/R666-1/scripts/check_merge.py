#!/usr/bin/env python3
"""Check both parent mutant inventories and every merged mutation anchor."""
import json
from pathlib import Path
import subprocess
import sys
import types

root = Path(sys.argv[1]).resolve()
packet = Path(sys.argv[2]).resolve()
sys.dont_write_bytecode = True
def inventory(rev, file):
    code = subprocess.check_output(['git', 'show', f'{rev}:{file}'], cwd=root)
    name = 'inventory_' + rev.replace('^','_') + file.replace('/','_').replace('.','_')
    module = types.ModuleType(name)
    module.__file__ = str(root / file)
    sys.modules[name] = module
    exec(compile(code, module.__file__, 'exec'), module.__dict__)
    return module.MUTANTS

out = {}
for file in ['tb/srp_top/mutants.py', 'tb/pp_top/acmp_mutants.py']:
    inventories = {rev: inventory(rev, file) for rev in ['HEAD^1','HEAD^2','HEAD']}
    def key(m):
        return (m.name, m.suite.directory, m.suite.run) if hasattr(m,'name') else tuple(m)
    keys = {rev:set(map(key, inv)) for rev, inv in inventories.items()}
    missing = (keys['HEAD^1'] | keys['HEAD^2']) - keys['HEAD']
    assert not missing, missing
    assert keys['HEAD'] == keys['HEAD^1'] | keys['HEAD^2']
    changes=[]
    merged={key(m):m for m in inventories['HEAD']}
    for rev in ['HEAD^1','HEAD^2']:
        for old in inventories[rev]:
            new=merged[key(old)]
            if hasattr(old,'edits'):
                assert old.edits==new.edits, (rev,key(old),'mutation edit changed')
                if old.checks!=new.checks:
                    assert old.name=='st_ls_teardown_as_declare' and rev=='HEAD^2'
                    changes.append({'parent':rev,'id':old.name,
                                    'old_checks':old.checks,'merged_checks':new.checks})
            else:
                patch=f'tb/srp_top/mutations/{old[0]}.patch'
                previous=subprocess.check_output(['git','show',f'{rev}:{patch}'],cwd=root,text=True)
                current=(root/patch).read_text()
                def edits(text):
                    return [line for line in text.splitlines()
                            if line[:1] in ['+','-'] and not line.startswith(('+++','---'))]
                assert edits(previous)==edits(current),(rev,patch,'patch intent changed')
    anchor_results = []
    for m in inventories['HEAD']:
        if hasattr(m,'edits'):
            for rel, old, new in m.edits:
                n=(root/rel).read_text().count(old)
                assert n == 1, (m.name,rel,n)
            anchor_results.append({'id':m.name,'suite':m.suite.directory,'anchors':'unique'})
        else:
            patch = root/'tb/srp_top/mutations'/f'{m[0]}.patch'
            p = subprocess.run(['git','apply','--check',str(patch)],cwd=root,capture_output=True,text=True)
            assert p.returncode == 0, (m,p.stderr)
            anchor_results.append({'id':m[0],'suite':m[1],'group':m[2],'anchor':'patch applies'})
    out[file] = {'parent1':len(keys['HEAD^1']),'parent2':len(keys['HEAD^2']),
                 'merged':len(keys['HEAD']),'exact_union':True,
                 'parent_mutation_edits_preserved':True,'expected_check_updates':changes,
                 'anchors':anchor_results}
(packet/'receipts/merge-inventory.json').write_text(json.dumps(out,indent=2)+'\n')
for file,result in out.items():
    print(file, {k:v for k,v in result.items() if k!='anchors'})
