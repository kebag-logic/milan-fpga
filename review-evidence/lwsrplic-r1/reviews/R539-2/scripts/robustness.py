#!/usr/bin/env python3
"""Syntax, configuration and disposable licence sensitivity checks."""
import ast
from concurrent.futures import ThreadPoolExecutor
import configparser
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

packet = Path(__file__).resolve().parents[1]
scratch, receipts = packet/'scratch', packet/'receipts'
source = scratch/'exact-source'
sys.path.insert(0,str(scratch/'pydeps'))
import kconfiglib
import yaml
os.environ['PYTHONDONTWRITEBYTECODE']='1'

def run(name, cmd, cwd=source, expected=0):
    result=subprocess.run(cmd,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
    (scratch/(name+'.raw.log')).write_bytes(result.stdout)
    text=result.stdout.decode(errors='replace').replace(str(scratch),'$SCRATCH')
    (receipts/(name+'.log')).write_text(text)
    (receipts/(name+'.rc')).write_text(str(result.returncode)+'\n')
    assert (result.returncode == 0) == (expected == 0), (name,result.returncode)
    return name,result.returncode

def syntax():
    count=0
    for file in source.rglob('*.py'):
        if 'build' in file.relative_to(source).parts:
            continue
        ast.parse(file.read_text(),filename=str(file.relative_to(source)))
        count+=1
    data=yaml.safe_load((source/'zephyr/module.yml').read_text())
    assert data=={'name':'lwsrp','build':{'cmake':'.','kconfig':'Kconfig.zephyr'}}
    config=kconfiglib.Kconfig(str(source/'Kconfig.zephyr'),warn_to_stderr=False)
    assert config.syms['LWSRP'].type==kconfiglib.BOOL
    ini=configparser.ConfigParser()
    ini.read(source/'behave.ini')
    assert ini['behave']['paths']=='tests/features'
    text=f'Python AST files: {count}; PASS\nModule YAML exact key/value schema: PASS\nKconfig LWSRP boolean: PASS\nScenario INI: PASS\n'
    (receipts/'syntax.log').write_text(text)
    (receipts/'syntax.rc').write_text('0\n')
    return 'syntax',0

def probes():
    logs=[]
    root=scratch/'probes'
    root.mkdir(exist_ok=True)
    def copy(name):
        dest=root/name
        dest.mkdir(exist_ok=True)
        for entry in source.iterdir():
            if entry.name=='build':continue
            if entry.is_dir():shutil.copytree(entry,dest/entry.name,dirs_exist_ok=True)
            else:shutil.copy2(entry,dest/entry.name)
        return dest
    for file in ('LICENSE','NOTICE'):
        dest=copy('missing-'+file.lower())
        (dest/file).unlink()
        logs.append(run('probe-missing-'+file.lower(),['python3','doc/tools/check_links.py','--local-only'],dest,expected=1))
    dest=copy('invalid-c-header')
    file=dest/'src/core/switch_ctrl.c'
    file.write_text(file.read_text().replace('/* SPDX-License-Identifier: Apache-2.0 */','# SPDX-License-Identifier: Apache-2.0',1))
    logs.append(run('probe-c-header',['cc','-std=c11','-Isrc/include','-fsyntax-only','src/core/switch_ctrl.c'],dest,expected=1))
    dest=copy('invalid-feature-header')
    file=dest/'tests/features/switch.feature'
    file.write_text(file.read_text().replace('# SPDX-License-Identifier: Apache-2.0','/* SPDX-License-Identifier: Apache-2.0 */',1))
    logs.append(run('probe-feature-header',['behave','--dry-run'],dest,expected=1))
    dest=copy('invalid-kconfig-header')
    file=dest/'Kconfig.zephyr'
    file.write_text(file.read_text().replace('# SPDX-License-Identifier: Apache-2.0','/* SPDX-License-Identifier: Apache-2.0 */',1))
    rejected=False
    try:kconfiglib.Kconfig(str(file),warn_to_stderr=False)
    except kconfiglib.KconfigError:rejected=True
    assert rejected
    logs.append(('probe-kconfig-header','rejected'))
    dest=copy('invalid-module-header')
    file=dest/'zephyr/module.yml'
    file.write_text(file.read_text().replace('# SPDX-License-Identifier: Apache-2.0','/* SPDX-License-Identifier: Apache-2.0 */',1))
    try:rejected=yaml.safe_load(file.read_text())!={'name':'lwsrp','build':{'cmake':'.','kconfig':'Kconfig.zephyr'}}
    except yaml.YAMLError:rejected=True
    assert rejected
    logs.append(('probe-module-header','rejected by exact schema'))
    (receipts/'probes.log').write_text('\n'.join(f'{n}: {r} (expected rejection)' for n,r in logs)+'\nSix disposable sensitivity probes: PASS\n')
    (receipts/'probes.rc').write_text('0\n')
    return 'probes',0

with ThreadPoolExecutor(max_workers=4) as pool:
    jobs=[pool.submit(syntax),pool.submit(probes),
          pool.submit(run,'queue-syntax',['cc','-std=c11','-Wall','-Wextra','-Wpedantic','-Isrc/include','-fsyntax-only','src/core/switch_ctrl.c']),
          pool.submit(run,'shell-syntax',['bash','-n','build.sh']),
          pool.submit(run,'shell-execution',['bash','build.sh'])]
    for job in jobs:print(job.result())
print('All robustness campaigns joined.')
