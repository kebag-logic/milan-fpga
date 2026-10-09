#!/usr/bin/env python3
"""Plant actual source comments in an archive; never edit the reviewed checkout."""
import io
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
repo,packet=map(lambda s:Path(s).resolve(),sys.argv[1:3])
root=packet/'scratch/comment-controls'
root.mkdir(parents=True,exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive','HEAD'],cwd=repo))) as a:
    a.extractall(root,filter='data')
p=root/'src/adp.c'
original=p.read_text()
variants={
    'baseline':'',
    'plain-prose':'\n// This is forbidden integrator narrative.\n',
    'spdx-block-prose':'\n/* SPDX-License-Identifier: MIT\nThis is forbidden integrator narrative.\n*/\n',
    'spliced-spdx-prose':'\n// SPDX-License-Identifier: MIT \\\nThis is forbidden integrator narrative.\n',
}
results=[]
for name,plant in variants.items():
    p.write_text(original+plant)
    result=subprocess.run([sys.executable,'scripts/check_comments.py'],cwd=root,text=True,capture_output=True,
                           env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    flags=['-std=c11','-Wall','-Wextra','-Werror']
    if name=='spliced-spdx-prose':flags+=['-Wno-comment']
    compilation=subprocess.run(['gcc',*flags,'-Iinclude','-c','src/adp.c','-o','probe.o'],cwd=root,text=True,capture_output=True)
    results.append({'control':name,'plant':plant,'gate_rc':result.returncode,'compile_rc':compilation.returncode,
                    'compile_flags':flags,'object_sha256':hashlib.sha256((root/'probe.o').read_bytes()).hexdigest(),
                    'output':result.stdout+result.stderr,'compiler_output':compilation.stdout+compilation.stderr})
    print(name, 'gate_rc',result.returncode,'compile_rc',compilation.returncode)
p.write_text(original)
(packet/'receipts/comment-controls.json').write_text(json.dumps(results,indent=2)+'\n')
assert results[0]['gate_rc']==0 and results[1]['gate_rc']==1
assert all(x['compile_rc']==0 for x in results)
assert results[2]['gate_rc']==results[3]['gate_rc']==0
