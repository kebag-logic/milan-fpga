#!/usr/bin/env python3
"""Independent provisioned-collision and same-ID PCP probes; one injected fault."""
import concurrent.futures, json, os, pathlib, shutil, subprocess, sys
ROOT = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(__file__).resolve().parent
SCR = OUT / 'scratch'
ENV = dict(os.environ, TMPDIR=str(SCR), MAKEFLAGS='-j16')
def case(label, fault):
    tree = SCR / label
    for rel in ['hdl', 'tb/common', 'tb/acmp_talker']:
        shutil.copytree(ROOT / rel, tree / rel, ignore=shutil.ignore_patterns('obj*','__pycache__'), dirs_exist_ok=True)
    path = tree / 'tb/acmp_talker/sid_cases.hpp'
    txt = path.read_text()
    old = '  sid.cursor_lap();\n'
    assert txt.count(old) == 1
    path.write_text(txt.replace(old, old + (OUT / 'own-cases.inc').read_text()))
    if fault:
        path = tree / 'hdl/acmp/KL_acmp_talker.sv'
        txt = path.read_text()
        old = 'for (int unsigned j = 0; j < N_STREAM_OUT_P; j++) begin'
        assert txt.count(old) == 1
        path.write_text(txt.replace(old, 'for (int unsigned j = 0; j < N_STREAM_OUT_P-1; j++) begin'))
    args = ['make', '-j16', 'run', 'VERILATOR='+str(OUT / 'scoped-compiler.py')]
    with (OUT / (label+'.log')).open('w') as log:
        log.write('command: '+repr(args)+'\n'); log.flush()
        rc = subprocess.run(args, cwd=tree/'tb/acmp_talker', env=ENV, stdout=log, stderr=subprocess.STDOUT).returncode
    (OUT / (label+'.rc')).write_text(str(rc)+'\n')
    text = (OUT / (label+'.log')).read_text()
    record = dict(label=label, rc=rc, completed='checks:' in text,
                  failures=[s for s in text.splitlines() if s.startswith('FAIL:')],
                  observations=[s for s in text.splitlines() if s.startswith('OWN ')])
    print(json.dumps(record), flush=True)
    return record
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(lambda args: case(*args), [('own-head',False),('own-last-slot-fault',True)]))
(OUT/'own-results.json').write_text(json.dumps(results,indent=2)+'\n')
