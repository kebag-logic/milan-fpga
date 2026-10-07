# SPDX-License-Identifier: Apache-2.0
"""Focused foreground review: independent suites and probes run concurrently."""
import argparse, concurrent.futures as cf, json, os, subprocess, threading
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--packet', type=Path, required=True)
p.add_argument('--jobs', type=int, default=4)
a = p.parse_args()
src, packet = a.source.resolve(), a.packet.resolve()
scratch, receipts = packet/'scratch', packet/'receipts'
prefix = scratch/'deps'
env = os.environ | {'PYTHONDONTWRITEBYTECODE':'1', 'TMPDIR':str(scratch),
    'LD_LIBRARY_PATH':str(prefix/'lib'), 'ASAN_OPTIONS':'detect_leaks=1:abort_on_error=1'}
records, lock, build_lock = [], threading.Lock(), threading.Lock()

def run(label, cmd, extra=None):
    r = subprocess.run(list(map(str,cmd)), cwd=src, env=env | (extra or {}), capture_output=True, text=True, timeout=540)
    output = r.stdout+r.stderr
    (scratch/(label+'.raw.log')).write_text(output)
    clean = output.replace(str(src),'$SOURCE').replace(str(packet),'$PACKET')
    (receipts/(label+'.log')).write_text(clean)
    (receipts/(label+'.rc')).write_text(str(r.returncode)+'\n')
    with lock:
        records.append({'label':label, 'command':[str(x).replace(str(src),'$SOURCE').replace(str(packet),'$PACKET') for x in cmd], 'rc':r.returncode})
        (receipts/'review-commands.json').write_text(json.dumps(records,indent=2)+'\n')
        print(label, 'rc='+str(r.returncode), clean[-220:].strip(), flush=True)
    return r.returncode

def profile(mode):
    b=scratch/('build-'+mode)
    with build_lock:
        if run('configure-'+mode,['cmake','-S',src,'-B',b,'-DCMAKE_BUILD_TYPE=Debug',f'-DCMAKE_PREFIX_PATH={prefix}',f'-DLWSRP_MILAN={mode}']): return
        if run('build-'+mode,['make','-C',b,'-j16']): return
    run('ctest-'+mode,['ctest','--test-dir',b,'--output-on-failure'])
    run('unit-'+mode,[b/'unit_tests'])
    run('scenario-'+mode,['behave'], {'SHLAN_LIBRARY':str(b/'libshlan.so')})

def probes(mode):
    common=['cc','-std=c11','-g','-O1','-fno-omit-frame-pointer','-fsanitize=address,undefined','-no-pie',
        '-DLWSRP_MILAN='+('1' if mode=='ON' else '0'),'-Isrc/include','-Isrc','-Itests/unit']
    sources=['src/core/mrp_mad.c','src/core/mrp_pdu.c','src/ports/timer.c','src/modules/msrp.c']
    for name in ['probe_fault','probe_flush','probe_r3','probe_r4','probe_rx']:
        binary=scratch/(name+'-'+mode)
        allocator=packet/'scripts/probe_alloc.c' if name=='probe_r3' else src/'tests/unit/fault_alloc.c'
        extras=['src/modules/mvrp.c','src/modules/mmrp.c'] if name=='probe_rx' else []
        if not run(name+'-build-'+mode,common+[packet/'scripts'/(name+'.c'),*sources,*extras,allocator,'-o',binary]):
            run(name+'-'+mode,[binary])
    units=sorted(src.glob('tests/unit/*_test.c'))+[src/'tests/unit/main.c']
    binary=scratch/('sanitized-unit-'+mode)
    if not run('sanitized-build-'+mode,common+['-I'+str(prefix/'include'),*units,*sources,'tests/unit/fault_alloc.c','src/modules/mmrp.c','src/modules/mvrp.c','src/core/switch.c','-L'+str(prefix/'lib'),'-lcgreen','-o',binary]):
        run('sanitized-unit-'+mode,[binary])

def docs():
    for name,args in [('sentences',[]),('references',[]),('references-selftest',['--self-test']),('links',['--github-auth'])]:
        file='check_references.py' if name=='references-selftest' else 'check_'+name+'.py'
        run('docs-'+name,['python3','doc/tools/'+file,*args])
    config=scratch/'browser.json'
    config.write_text(json.dumps({'args':['--no-sandbox']}))
    run('docs-graphs',['python3','doc/tools/render_mermaid.py','--output',scratch/'graphs','--puppeteer-config',config])

with cf.ThreadPoolExecutor(max_workers=min(a.jobs,4)) as pool:
    fut=[pool.submit(profile,m) for m in ['OFF','ON']]+[pool.submit(probes,m) for m in ['OFF','ON']]+[pool.submit(docs)]
    for f in fut: f.result()
print('Review commands complete; inspect each recorded result.')
