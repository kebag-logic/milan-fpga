#!/usr/bin/env python3
"""Focused independent stack review; all child jobs are awaited in the foreground."""
import concurrent.futures as cf
import json, os, pathlib, subprocess, sys
root = pathlib.Path(sys.argv[1]).resolve()
packet = pathlib.Path(__file__).resolve().parent
scratch = packet / 'scratch'
logs = packet / 'receipts'
logs.mkdir(exist_ok=True)
env = os.environ.copy()
prefix = pathlib.Path(os.environ['REVIEW_GTEST_PREFIX']).resolve()
env.update(PKG_CONFIG_PATH=str(prefix/'lib/pkgconfig'), CMAKE_PREFIX_PATH=str(prefix), LD_LIBRARY_PATH=str(prefix/'lib'))
env['PATH'] = os.environ.get('REVIEW_COMPILER_PATH', '') + os.pathsep + env['PATH']
env['TMPDIR'] = str(scratch)
def run(name, cmds):
    output = ''
    rc = 0
    for cmd in cmds:
        p = subprocess.run(cmd, cwd=root, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output += '$ ' + ' '.join(map(str,cmd)) + '\n' + p.stdout + '\nrc=' + str(p.returncode) + '\n'
        rc = p.returncode
        if rc: break
    for a,b in [(str(root),'$STACK'),(str(packet),'$PACKET'),(str(prefix),'$GTEST')]: output=output.replace(a,b)
    (logs/(name+'.log')).write_text(output)
    (logs/(name+'.rc')).write_text(str(rc)+'\n')
    print(name,rc,flush=True)
    return name,rc
build = str(scratch/'stack-build')
tasks = [
 ('stack-host', [['cmake','-S','.', '-B',build,'-DCMAKE_BUILD_TYPE=Debug','-DTSN_COVERAGE=ON'], ['cmake','--build',build,'-j4'],['ctest','--test-dir',build,'--output-on-failure','-j4'],['python3','scripts/coverage.py',build]]),
 ('stack-plants', [['python3',str(packet/'run_selected_plants.py'),str(root)]]),
 ('stack-rv32', [['python3','scripts/baremetal.py','--work',str(scratch/'stack-rv32'),'--jobs','4']]),
 ('stack-contracts', [['python3','scripts/check_port_contracts.py'],['python3','scripts/check_comments.py'],['python3','scripts/check_license.py']]),
]
with cf.ThreadPoolExecutor(4) as pool: results=list(pool.map(lambda x:run(*x),tasks))
# Generators use the completed build; no tracked edits are made.
results.append(run('stack-generated', [['python3','scripts/traceability.py','--build',build,'--jobs','4'],['python3','scripts/test_inventory.py','--build',build,'--jobs','4']]))
# This repository driver controls its own 16 workers, so it runs alone.
results.append(run('stack-static', [['python3','scripts/static_analysis.py']]))
(logs/'stack-results.json').write_text(json.dumps(dict(results),indent=2)+'\n')
