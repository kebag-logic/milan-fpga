#!/usr/bin/env python3
"""Run independent scoped checks in foreground, retaining logs and return codes."""
import concurrent.futures, json, os, pathlib, shutil, subprocess, sys, time
root = pathlib.Path(sys.argv[1]).resolve()
packet = pathlib.Path(__file__).resolve().parent
scratch = packet / 'scratch'
env = dict(os.environ, TMPDIR=str(scratch), SV2V='$VALIDATION_TOOLS/sv2v-v0.0.12/sv2v',
           VERILATOR='$VALIDATION_TOOLS/pinned-verilator-5.050/verilator', VBUILD_JOBS='1')
def run(name, argv, cwd=root):
    began = time.monotonic()
    with (packet / (name + '.log')).open('w') as out:
        out.write('argv: '+repr(argv)+'\n'); out.flush()
        rc = subprocess.run(argv, cwd=cwd, env=env, stdout=out, stderr=subprocess.STDOUT).returncode
    receipt = {'argv': argv, 'returncode':rc, 'seconds':round(time.monotonic()-began,3)}
    (packet / (name+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    print(name, receipt, flush=True)
    return rc
bench = scratch/'bench/tb/verilator/mbx'
shutil.copytree(root/'tb/verilator/mbx', bench, ignore=shutil.ignore_patterns('obj*','__pycache__'), dirs_exist_ok=True)
shutil.copytree(root/'tb/common', scratch/'bench/tb/common', dirs_exist_ok=True)
def mailbox():
    run('mbx-suite',['make','-j16', 'ROOT='+str(root), 'VBUILD_JOBS=1','run-wb','run-axil','run-if2'],bench)
    return run('mbx-mutants',['python3','-B','tb/verilator/mbx/mutants.py','--jobs','4','--keep',str(scratch/'mutants')])
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    tasks=[pool.submit(run,'census',['python3','-B','sw/mailbox/publication_census.py','--check','--selftest','--jobs','4']),
           pool.submit(mailbox),
           pool.submit(run,'generator',['python3','-B','sw/mailbox/gen_mailbox.py','--check','--crosscheck','--selftest'])]
    for f in concurrent.futures.as_completed(tasks):
        print('campaign returned',f.result(),flush=True)
