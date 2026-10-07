#!/usr/bin/env python3
"""Run bounded independent campaigns with joined foreground orchestration."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tarfile

source = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
scratch, receipts = packet/'scratch', packet/'receipts'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', LC_ALL='C.UTF-8')
def run(name, cmd, cwd=source):
    result = subprocess.run(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=540)
    raw = result.stdout
    (scratch/(name+'.raw.log')).write_bytes(raw)
    public = raw.decode(errors='replace').replace(str(scratch), '$SCRATCH').replace(str(source), '$SOURCE')
    (receipts/(name+'.log')).write_text(public)
    (receipts/(name+'.rc')).write_text(str(result.returncode)+'\n')
    print(name, 'rc', result.returncode, flush=True)
    return result.returncode

def docs():
    for name, args in [
        ('links-local', ['check_links.py','--local-only']),
        ('sentences', ['check_sentences.py']),
        ('references', ['check_references.py']),
        ('references-selftest', ['check_references.py','--self-test']),
        ('links-authenticated', ['check_links.py','--github-auth']),
    ]:
        run(name, ['python3', str(source/'doc/tools'/args[0]), *args[1:]])

def build():
    dep, depbuild, install = scratch/'cgreen-1.7.0', scratch/'cgreen-build', scratch/'dependency'
    if run('dependency-configure', ['cmake','-S',str(dep),'-B',str(depbuild),'-DCMAKE_POLICY_VERSION_MINIMUM=3.5','-DCGREEN_WITH_UNIT_TESTS=OFF','-DCGREEN_WITH_LIBXML2=OFF','-DCMAKE_INSTALL_PREFIX='+str(install)]):
        return
    if run('dependency-build', ['make','-C',str(depbuild),'-j16']):
        return
    if run('dependency-install', ['cmake','--install',str(depbuild)]):
        return
    work = scratch/'exact-source'
    work.mkdir(exist_ok=True)
    archive = scratch/'exact-source.tar'
    with archive.open('wb') as out:
        subprocess.run(['git','-C',str(source),'archive','4eba61b7b1c49fc9b7260a487240ca86f9d38168'],stdout=out,check=True)
    with tarfile.open(archive) as f:
        f.extractall(work, filter='data')
    env['LD_LIBRARY_PATH'] = str(install/'lib') + ':' + env.get('LD_LIBRARY_PATH','')
    if run('configure', ['cmake','-S','.','-B','build','-DCMAKE_BUILD_TYPE=Debug','-DCMAKE_PREFIX_PATH='+str(install)], work):
        return
    if run('build', ['make','-C','build','-j16'], work):
        return
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs = [pool.submit(run, 'ctest', ['ctest','--test-dir','build','-V','--output-on-failure'], work),
                pool.submit(run, 'unit-direct', ['./build/unit_tests'], work),
                pool.submit(run, 'behave', ['behave'], work)]
        for job in jobs:
            job.result()
    run('behave-dry', ['behave','--dry-run'], work)

with ThreadPoolExecutor(max_workers=2) as pool:
    jobs = [pool.submit(docs), pool.submit(build)]
    for job in jobs:
        job.result()
print('All campaigns joined; no child work left running.', flush=True)
