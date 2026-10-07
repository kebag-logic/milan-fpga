#!/usr/bin/env python3
"""Read-only patch applicability and sequential exact-text plant audit."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

source = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0,str(source/'tb/common'))
spec = importlib.util.spec_from_file_location('notify_plants', source/'tb/pp_top/notify_mutants.py')
nm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nm)
rows = []
for mutant in nm.MUTANTS:
    buffers = {}
    counts = []
    for path,old,new in mutant.edits:
        text = buffers.get(path,(source/path).read_text())
        counts.append(text.count(old))
        assert text.count(old)==1, (mutant.name,path,text.count(old))
        buffers[path] = text.replace(old,new,1)
    rows.append({'name':mutant.name,'edits':len(counts),'all_unique':True})
patches = []
for path in sorted((source/'tb').rglob('*.patch')):
    proc = subprocess.run(['git','apply','--check',str(path)],cwd=source,capture_output=True,text=True)
    patches.append({'path':str(path.relative_to(source)),'rc':proc.returncode,'diagnostic':proc.stderr})
oldtext = subprocess.check_output(['git','show','c4539ff1:tb/pp_top/notify_mutants.py'],cwd=source,text=True)
oldnames = set(__import__('re').findall(r'Mutant\("([^\"]+)"', oldtext)) - {'golden-'}
newnames = {m.name for m in nm.MUTANTS}
assert not oldnames-newnames
report = {'notify_arms':len(rows),'notify_edits':sum(x['edits'] for x in rows),
          'new_arms':sorted(newnames-oldnames),'removed_arms':sorted(oldnames-newnames),
          'notify':rows,'patch_count':len(patches),'patch_failures':sum(bool(x['rc']) for x in patches),'patches':patches}
(packet/'receipts/plant-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('notify','patches')},indent=2))
sys.exit(bool(report['patch_failures']))
