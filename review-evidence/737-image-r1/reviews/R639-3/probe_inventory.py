#!/usr/bin/env python3
"""Probe literal command traversal without executing any planted installer."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

checkout = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
os.environ['CI_IMAGE_SHFMT'] = str(packet / 'scratch/shfmt')
sys.path.insert(0, str(checkout / 'scripts'))
import ci_tool_inventory as inventory

cases = [
    ('make-long-file', 'make --file=install.mk', {'Makefile':'all:\n\techo clean\n', 'install.mk':'all:\n\tbrand_new_command install tool\n'}),
    ('make-short-file', 'make -finstall.mk', {'Makefile':'all:\n\techo clean\n', 'install.mk':'all:\n\tbrand_new_command install tool\n'}),
    ('make-default-goal', 'make', {'Makefile':'clean:\n\techo clean\n.DEFAULT_GOAL := install\ninstall:\n\tbrand_new_command install tool\n'}),
    ('make-pattern-target', 'make install', {'Makefile':'%:\n\tbrand_new_command install tool\n'}),
    ('python-literal-kwargs', 'python3 bootstrap.py', {'bootstrap.py':'import subprocess\nsubprocess.run(**{"args": ["brand_new_command", "install"]})\n'}),
    ('python-literal-starargs', 'python3 bootstrap.py', {'bootstrap.py':'import subprocess\nsubprocess.run(*(["brand_new_command", "install"],))\n'}),
    ('python-positional', 'python3 bootstrap.py', {'bootstrap.py':'import subprocess\nsubprocess.run(["brand_new_command", "install"])\n'}),
    ('shell-cwd-subshell', '(cd subdir); bash bootstrap.sh', {'bootstrap.sh':'brand_new_command install tool\n', 'subdir/bootstrap.sh':'echo clean\n'}),
    ('shell-cwd-step-default', 'bash bootstrap.sh', {'bootstrap.sh':'echo clean\n', 'subdir/bootstrap.sh':'brand_new_command install tool\n'}),
]
records=[]
for name, command, files in cases:
    with tempfile.TemporaryDirectory(dir=packet/'scratch', prefix='inventory-probe-') as temporary:
        root=Path(temporary)
        (root/'ci/image').mkdir(parents=True)
        for file in ('command-table.json','sources.lock.json'):
            shutil.copyfile(checkout/'ci/image'/file, root/'ci/image'/file)
        for file, content in files.items():
            target=root/file
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        workflow=root/'.github/workflows/probe.yml'
        workflow.parent.mkdir(parents=True)
        body={'jobs':{'probe':{'steps':[{'run':command}]}}}
        if name=='shell-cwd-step-default':
            body['jobs']['probe']['steps'][0]['working-directory']='subdir'
        import yaml
        workflow.write_text(yaml.safe_dump(body))
        try:
            result=inventory.derive(root)
            outcome={'accepted':True, 'tools':result['tools'], 'residue':result['residue'],
                     'followed': sorted(result['inputs'])}
            write = subprocess.run([sys.executable, str(checkout/'scripts/ci_tool_inventory.py'), '--root', str(root), '--write'], capture_output=True, text=True)
            check = subprocess.run([sys.executable, str(checkout/'scripts/ci_tool_inventory.py'), '--root', str(root), '--check'], capture_output=True, text=True)
            outcome['cli_write_rc']=write.returncode
            outcome['cli_check_rc']=check.returncode
            assert write.returncode == check.returncode == 0
            if name.startswith('make-'):
                import shlex
                dry=subprocess.run(['make', '-n', *shlex.split(command)[1:]], cwd=root, capture_output=True,text=True)
                outcome['make_dry_run']={'rc':dry.returncode,'stdout':dry.stdout,'stderr':dry.stderr}
                assert 'brand_new_command install tool' in dry.stdout
        except inventory.Refusal as error:
            outcome={'accepted':False, 'error':str(error).replace(str(root),'<fixture>')}
        records.append({'name':name,'command':command,'files':files,**outcome})
print(json.dumps(records, indent=2))
