#!/usr/bin/env python3
"""Focused review checks; usage: review_checks.py SOURCE PACKET MODE.

Writes only PACKET. All disposable copies and subprocess temporary files are
under PACKET/scratch. Commands run synchronously; at most eight independent
lightweight subprocesses run concurrently. No HDL banks or hosted writes.
"""
import ast
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True

SOURCE = Path(sys.argv[1]).resolve()
PACKET = Path(sys.argv[2]).resolve()
MODE = sys.argv[3]
SCRATCH = PACKET / 'scratch'
RECEIPTS = PACKET / 'receipts'
HEAD = '2c2f336979e4fdb1da444f041f37551e2c9175df'
BASE = 'c6bd08c6f52632c6d33d834ce842ac3cf63f29cc'
SCRATCH.mkdir(exist_ok=True)
RECEIPTS.mkdir(exist_ok=True)
ENV = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': str(SCRATCH),
       'PYTHONHASHSEED': '0', 'LC_ALL': 'C.UTF-8'}


def run(name, argv, cwd=SOURCE, expected=0, env=None, timeout=540):
    path = RECEIPTS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(argv, cwd=cwd, env=env or ENV, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=timeout)
    path.with_suffix('.log').write_bytes(result.stdout)
    path.with_suffix('.rc').write_text(f'{result.returncode}\n')
    path.with_suffix('.command.json').write_text(json.dumps(
        {'argv': argv, 'cwd': str(cwd.relative_to(PACKET)) if cwd.is_relative_to(PACKET) else '.',
         'expected_rc': expected, 'actual_rc': result.returncode}, indent=2)+'\n')
    print(f'{name}: rc {result.returncode}, expected {expected}', flush=True)
    if expected is not None:
        assert result.returncode == expected, (name, result.stdout.decode(errors='replace')[-4000:])
    return result.stdout.decode(errors='replace')


def read_git(rev, path):
    return subprocess.check_output(['git', 'show', f'{rev}:{path}'], cwd=SOURCE).decode()


def load(path):
    spec = importlib.util.spec_from_file_location('review_selector', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture(name, text=None):
    root = SCRATCH / name
    if root.exists():
        shutil.rmtree(root)
    (root/'scripts').mkdir(parents=True)
    (root/'.github/workflows').mkdir(parents=True)
    shutil.copyfile(SOURCE/'scripts/run_all_suites.sh', root/'scripts/run_all_suites.sh')
    shutil.copyfile(SOURCE/'.github/workflows/rtl.yml', root/'.github/workflows/rtl.yml')
    (root/'scripts/suite_shards.py').write_text(text or (SOURCE/'scripts/suite_shards.py').read_text())
    for makefile in (SOURCE/'tb/verilator').glob('*/Makefile'):
        target = root/'tb/verilator'/makefile.parent.name/'Makefile'
        target.parent.mkdir(parents=True)
        target.touch()
    return root


def gates():
    commands = {
        'suite-selftest': ['python3','scripts/suite_shards.py','--selftest'],
        'ci-events-check': ['python3','scripts/ci_events.py','--check'],
        'ci-events-selftest': ['python3','scripts/ci_events.py','--selftest'],
        'cancellation': ['python3','scripts/test_suite_cancellation.py'],
        'suite-tally-selftest': ['python3','scripts/suite_tally.py','--selftest'],
        'python-idiom': ['python3','scripts/check_py_idiom.py'],
        'docs-check': ['python3','scripts/docs_check.py'],
        'doc-style': ['python3','scripts/check_doc_style.py'],
        'toc-check': ['python3','scripts/gen_toc.py','--check'],
        'doc-paths': ['python3','scripts/check_doc_paths.py'],
        'em-dash': ['python3','scripts/check_em_dash.py','--base', BASE],
        'diff-check': ['git','diff','--check',BASE,HEAD],
    }
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(run, 'gates/'+name, argv, expected=None) for name,argv in commands.items()]
        for future in futures:
            future.result()


def inventory():
    head = load(SOURCE/'scripts/suite_shards.py')
    inventory = sorted(p.parent.name for p in (SOURCE/'tb/verilator').glob('*/Makefile')
                       if p.parent.name != 'milan_dp_gptp')
    serial = run('lists/serial', ['bash','scripts/run_all_suites.sh','--shard','0/1','--list'])
    default = run('lists/default', ['bash','scripts/run_all_suites.sh','--list'])
    assert serial == default and serial.splitlines() == inventory
    shards = [run('lists/worker-'+str(i), ['bash','scripts/run_all_suites.sh','--shard',f'{i}/5','--list']).splitlines()
              for i in range(5)]
    flattened = sum(shards, [])
    assert sorted(flattened) == inventory and len(flattened) == len(set(flattened))
    assert shards[4] == ['milan_dp'] and 'tsn_fuzz' in shards[1] and 'chmap_capture' in shards[3]
    # Independent longest-first assignment, with explicit ownership authorities.
    loads = list(head.WORKER_OVERHEAD_SECONDS)
    owners = {'milan_dp':4, 'tsn_fuzz':1, 'chmap_capture':3}
    for s,i in owners.items(): loads[i] += head.SUITE_SECONDS[s]
    for s in sorted(set(inventory)-owners.keys(), key=lambda s:(-head.SUITE_SECONDS[s],s)):
        i = loads[:4].index(min(loads[:4])); owners[s] = i; loads[i] += head.SUITE_SECONDS[s]
    assert shards == [[s for s in inventory if owners[s]==i] for i in range(5)]
    assert max(loads) <= 120*36
    for rev in (BASE,'a57d384dc697249c2a69f80079b676875d4f7560','61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3'):
        copy = SCRATCH / ('selector-'+rev[:8]+'.py')
        copy.write_text(read_git(rev,'scripts/suite_shards.py'))
        prior = load(copy)
        assert prior.sweep_suites(SOURCE/'tb/verilator') == inventory
        assert prior.select_suites(inventory,0,1) == inventory
        if rev != BASE:
            assert prior.SUITE_SECONDS == head.SUITE_SECONDS
            assert prior.WORKER_OVERHEAD_SECONDS == head.WORKER_OVERHEAD_SECONDS
            assert [prior.select_suites(inventory,i,5) for i in range(5)] == shards
    for seed in ('1','2','12345'):
        for i in range(5):
            out = run(f'lists/seed-{seed}-{i}', ['python3','scripts/suite_shards.py',
                '--suite-root','tb/verilator','--shard',f'{i}/5'], env={**ENV,'PYTHONHASHSEED':seed})
            assert out.splitlines() == shards[i]
    summary = {'suites':len(inventory), 'workers':[len(s) for s in shards],
               'predicted_seconds':loads,'bound_seconds':4320,'base_serial_equal':True,
               'round_1_2_table_assignment_equal':True,'independent_assignment_equal':True}
    (RECEIPTS/'inventory.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))


def mutations():
    original = (SOURCE/'scripts/suite_shards.py').read_text()
    changes = {
      'headroom-75-percent': ('HEADROOM_PERCENT = 60','HEADROOM_PERCENT = 75','ESCAPED the bound applied'),
      'headroom-100-percent': ('HEADROOM_PERCENT = 60','HEADROOM_PERCENT = 100','ESCAPED the bound applied'),
      'bound-formula-div10': ('* HEADROOM_PERCENT // 100','* HEADROOM_PERCENT // 10','ESCAPED the bound applied'),
      'missing-free': ('for suite in suites if suite not in seconds]', 'for suite in () if suite not in seconds]', None),
      'stale-ignored': ('for suite in sorted(set(seconds) - inventory)]','for suite in []]', 'ESCAPED a recorded duration'),
      'zero-allowed': ('seconds[suite] > 0','seconds[suite] >= 0','ESCAPED a recorded duration of 0'),
      'timeout-mirrored': ('found["timeout-minutes"], found["matrix total"]','120, found["matrix total"]','ESCAPED rtl.yml timeout-minutes'),
      'workers-mirrored': ('found["timeout-minutes"], found["matrix total"]','found["timeout-minutes"], 5','ESCAPED rtl.yml at 6 workers'),
      'headroom-removed': ('if value > bound]','if False]','ESCAPED milan_dp at 4241'),
      'headroom-mean': ('if value > bound]','if sum(load) / workers > bound]','ESCAPED milan_dp at 4241'),
      'overhead-dropped': ('load = list(overhead) if layout else [0] * total','load = [0] * total','ESCAPED milan_dp at 4241'),
      'bound-equality-refused': ('if value > bound]','if value >= bound]','ESCAPED milan_dp at 4240'),
      'no-pins': ('fixed.update(PINNED_SUITES)','fixed.update({})','FAIL specialized owners'),
      'mirror-driver': ('named, default = driver_timeouts(driver)','named, default = {}, 1800','ESCAPED with suite_timeout'),
      'ignore-own-arm': ('expected = named.get(suite, default)','expected = default','ESCAPED with its own arm'),
      'ignore-provisional-value': ('elif seconds[suite] != expected:','elif False:','ESCAPED a provisional suite at'),
      'ignore-provisional-missing': ('if suite not in seconds:\n            problems.append', 'if False:\n            problems.append',None),
      'checkout-false': ('return HERE.name == "suite_shards.py" and HERE.parent.name == "scripts"','return False','FAIL head:'),
      'hash-tie': ('(-seconds[suite], suite)','(-seconds[suite], hash(suite))','FAIL the 5 --shard lists'),
      'measurement-from-job-start': ('windows, previous = {}, start','windows, previous = {}, first','FAIL log windows'),
    }
    # Use a missing-duration mutant that supplies zeroes as well as dropping
    # the guard, so the required ESCAPED arms are observed rather than KeyError.
    def one(name, change):
        old,new,marker = change
        assert original.count(old) >= 1, name
        changed=original.replace(old,new)
        if name=='missing-free':
            begin=changed.index('def balance(')
            end=changed.index('def select_suites(',begin)
            changed=changed[:begin]+changed[begin:end].replace('seconds[suite]', 'seconds.get(suite, 0)')+changed[end:]
            marker='ESCAPED an inventory suite with no recorded duration'
        if name=='ignore-provisional-missing':
            changed=changed.replace('elif seconds[suite] != expected:', 'elif suite in seconds and seconds[suite] != expected:')
            marker='ESCAPED a provisional suite with no figure'
        root=fixture('mutation-'+name,changed)
        out=run('mutations/'+name,['python3','scripts/suite_shards.py','--selftest'],cwd=root,expected=1)
        assert marker in out, (name,marker,out)
        return {'case':name,'rc':1,'marker':marker}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results=list(pool.map(lambda item: one(*item), changes.items()))
    (RECEIPTS/'mutations.json').write_text(json.dumps(results,indent=2)+'\n')


def integrity():
    result={}
    def check(root):
        records=subprocess.check_output(['git','ls-tree','-rz','HEAD'],cwd=root).split(b'\0')
        entries=[]; mismatches=[]; count=0; expected_index=[]
        for raw in records:
            if not raw: continue
            info,path=raw.split(b'\t',1); mode,kind,oid=info.split(); rel=os.fsdecode(path)
            expected_index.append((path,mode+b' '+oid+b' 0\t'+path+b'\0'))
            target=root/rel
            if kind==b'commit':
                entries.append({'path':rel,'mode':mode.decode(),'sha':oid.decode()});continue
            data=os.fsencode(os.readlink(target)) if mode==b'120000' else target.read_bytes()
            actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            actualmode='120000' if target.is_symlink() else ('100755' if target.stat().st_mode & 0o111 else '100644')
            count+=1
            if actual != oid.decode() or actualmode != mode.decode(): mismatches.append(rel)
        index=subprocess.check_output(['git','ls-files','--stage','-z'],cwd=root)
        assert index==b''.join(record for _,record in sorted(expected_index)), 'index differs from HEAD entries/stages'
        tree_index=subprocess.check_output(['git','diff','--cached','--raw','HEAD'],cwd=root)
        assert not tree_index and not mismatches,(root,mismatches,tree_index)
        return {'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip(),
            'tree':subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=root).decode().strip(),
            'tracked_blob_bytes_modes_checked':count,'mismatches':mismatches,'gitlinks':entries,
            'index_sha256':hashlib.sha256(index).hexdigest(),'index_equals_head':not tree_index}
    result['superproject']=check(SOURCE)
    assert result['superproject']['head']==HEAD
    for name in ('protocol-processor','gptp-processor','third_party/verilog-axis'):
        expected=next(x['sha'] for x in result['superproject']['gitlinks'] if x['path']==name)
        result[name]=check(SOURCE/name)
        assert result[name]['head']==expected
        result[name]['registered_superproject']=subprocess.check_output(
            ['git','rev-parse','--show-superproject-working-tree'],cwd=SOURCE/name).decode().strip()
        assert Path(result[name]['registered_superproject'])==SOURCE
    for file in ('.github/workflows/rtl.yml','scripts/run_all_suites.sh','scripts/ci_events.py'):
        assert read_git(BASE,file).encode()==(SOURCE/file).read_bytes()
    result['unchanged_workflow_driver_ci_contract']=True
    result['status']=subprocess.check_output(['git','status','--short','--ignored'],cwd=SOURCE).decode()
    (RECEIPTS/'integrity.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


def plants():
    original=(SOURCE/'scripts/suite_shards.py').read_text()
    driver=(SOURCE/'scripts/run_all_suites.sh').read_text()
    workflow=(SOURCE/'.github/workflows/rtl.yml').read_text()
    arm="    aaf) printf '%s\\n' \"${SUITE_TIMEOUT:-1800}\" ;;\n"
    default="    *)                 printf '%s\\n' \"${SUITE_TIMEOUT:-1800}\" ;;"
    cases={
        'missing-duration':('selector',original.replace('    "aaf": 73,\n','')),
        'stale-duration':('selector',original.replace('SUITE_SECONDS = {','SUITE_SECONDS = {\n    "retired_suite": 1,',1)),
        'zero-duration':('selector',original.replace('"aaf": 73','"aaf": 0')),
        'heavy-duration':('selector',original.replace('"gptp_plane": 784','"gptp_plane": 5000')),
        'bad-provisional':('selector',original.replace('PROVISIONAL_SUITES: frozenset[str] = frozenset()',
                                                    'PROVISIONAL_SUITES: frozenset[str] = frozenset({"aaf"})')),
        'six-workers':('workflow',workflow.replace('total: [5]','total: [6]')),
        'low-timeout':('workflow',workflow.replace('    timeout-minutes: 120','    timeout-minutes: 116')),
        'driver-missing':('remove-driver',''),
        'driver-two-name-arm':('driver',driver.replace('capture_coherence) printf','capture_coherence|foo) printf')),
        'driver-duplicate-arm':('driver',driver.replace(default,arm+arm+default)),
        'driver-star-not-last':('driver',driver.replace(default,default+'\n'+arm.rstrip())),
    }
    def one(item):
        name,(kind,text)=item
        root=fixture('plant-'+name,text if kind=='selector' else None)
        if kind=='workflow':(root/'.github/workflows/rtl.yml').write_text(text)
        if kind=='driver':(root/'scripts/run_all_suites.sh').write_text(text)
        if kind=='remove-driver':(root/'scripts/run_all_suites.sh').unlink()
        output=run('plants/'+name,['python3','scripts/suite_shards.py','--selftest'],cwd=root,expected=1)
        assert 'FAIL head' in output,(name,output)
        return {'case':name,'rc':1,'cause':'FAIL head'}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results=list(pool.map(one,cases.items()))
    (RECEIPTS/'plants.json').write_text(json.dumps(results,indent=2)+'\n')


if __name__ == '__main__':
    globals()[MODE]()
