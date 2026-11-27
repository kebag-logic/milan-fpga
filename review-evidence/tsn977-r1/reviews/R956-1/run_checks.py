#!/usr/bin/env python3
"""Run from an unchanged exact-head clone; outputs and disposable builds in packet."""
import argparse, concurrent.futures, json, os, pathlib, shutil, subprocess, sys

p = argparse.ArgumentParser()
p.add_argument('source', type=pathlib.Path)
p.add_argument('packet', type=pathlib.Path)
p.add_argument('--phase', choices=['host', 'campaigns', 'gates'], required=True)
a = p.parse_args()
src, out = a.source.resolve(), a.packet.resolve()
scratch = out / 'scratch'
scratch.mkdir(exist_ok=True)
(out / 'receipts').mkdir(exist_ok=True)
env = os.environ.copy()
env.update(ASAN_OPTIONS='detect_leaks=1:halt_on_error=1', UBSAN_OPTIONS='halt_on_error=1')
results = []

def run(name, argv):
    with (out / 'receipts' / (name + '.log')).open('w') as log:
        r = subprocess.run(list(map(str, argv)), cwd=src, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=550)
    (out / 'receipts' / (name + '.rc')).write_text(str(r.returncode) + '\n')
    result = dict(name=name, rc=r.returncode)
    print(json.dumps(result), flush=True)
    results.append(result)
    return r.returncode

if a.phase == 'host':
    # Full parallel builds are serialized to keep total compiler jobs at most 16.
    for name, cc, cxx, opt in [('gcc', 'gcc', 'g++', '-DTSN_COVERAGE=ON'), ('clang', 'clang', 'clang++', '-DTSN_SANITIZERS=ON')]:
        build = scratch / name
        if run(name+'-configure', ['cmake', '-S', src, '-B', build, '-DCMAKE_BUILD_TYPE=Debug', '-DCMAKE_C_COMPILER='+cc, '-DCMAKE_CXX_COMPILER='+cxx, opt]):
            continue
        if run(name+'-build', ['make', '-C', build, '-j16']):
            continue
        run(name+'-test', ['ctest', '--test-dir', build, '--output-on-failure', '-j16', '--output-junit', out/'receipts'/(name+'-tests.xml')])
        if name == 'gcc':
            run('coverage', [sys.executable, 'scripts/coverage.py', build])
elif a.phase == 'campaigns':
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        tasks = [pool.submit(run, 'mutations', [sys.executable, 'scripts/mutation.py', '--work', scratch/'mutations', '--jobs', '8']),
                 pool.submit(run, 'baremetal', [sys.executable, 'scripts/baremetal.py', '--work', scratch/'rv32', '--jobs', '4'])]
        for task in tasks:
            task.result()
    for directory in ['mutations', 'rv32']:
        for path in (scratch/directory).rglob('*'):
            if path.is_file() and path.suffix in ['.xml', '.json', '.log', '.map']:
                dest = out/'receipts'/directory/path.relative_to(scratch/directory)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, dest)
else:
    jobs = [('comments', 'check_comments.py', []), ('needles', 'needle_audit.py', []), ('port-contracts', 'check_port_contracts.py', []),
            ('traceability', 'traceability.py', ['--build', scratch/'gcc', '--jobs', '4']), ('test-inventory', 'test_inventory.py', ['--build', scratch/'gcc', '--jobs', '4']),
            ('license', 'check_license.py', []), ('boundary', 'check_boundary.py', ['--work', scratch/'boundary', '--jobs', '4'])]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        tasks = [pool.submit(run, name, [sys.executable, 'scripts/'+script, *args]) for name, script, args in jobs]
        for task in tasks:
            task.result()
(out/'receipts'/(a.phase+'-results.json')).write_text(json.dumps(results, indent=2)+'\n')
sys.exit(any(r['rc'] for r in results))
