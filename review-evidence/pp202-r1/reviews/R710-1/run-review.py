#!/usr/bin/env python3
"""Foreground bounded review: exact source copies; concurrent independent checks."""
import concurrent.futures, importlib.util, json, os, pathlib, shutil, subprocess, sys
sys.dont_write_bytecode = True
ROOT = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(__file__).resolve().parent
SCR = OUT / 'scratch'
SCR.mkdir(exist_ok=True)
ENV = dict(os.environ, TMPDIR=str(SCR), MAKEFLAGS='-j16', PYTHONDONTWRITEBYTECODE='1')
COMPILER = str(OUT / 'scoped-compiler.py')
os.chmod(COMPILER, 0o755)

def run(name, args, cwd):
    with (OUT / (name + '.log')).open('w') as f:
        f.write('command: ' + repr(args) + '\n'); f.flush()
        rc = subprocess.run(args, cwd=cwd, env=ENV, stdout=f, stderr=subprocess.STDOUT).returncode
    (OUT / (name + '.rc')).write_text(str(rc) + '\n')
    print(name, rc, flush=True)
    return rc

tree = SCR / 'source'
if not tree.exists():
    subprocess.run(['git', 'clone', '--no-hardlinks', '--quiet', str(ROOT), str(tree)], check=True)
spec = importlib.util.spec_from_file_location('campaign', ROOT / 'tb/pp_top/acmp_mutants.py')
mod = importlib.util.module_from_spec(spec); sys.modules['campaign'] = mod; spec.loader.exec_module(mod)
names = sorted({m.name for m in mod.STREAM_ID})
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    jobs = [pool.submit(run, 'assigned-mutants', [sys.executable, str(ROOT / 'tb/pp_top/acmp_mutants.py'), '--output', str(OUT / 'assigned-mutants'), '--verilator', COMPILER, '--jobs', '4', '--only', *names], ROOT),
            pool.submit(run, 'docs-check', ['make', '-j16', 'check'], tree)]
    results = [job.result() for job in jobs]
(OUT / 'campaign-summary.json').write_text(json.dumps(dict(zip(['assigned-mutants','docs-check'], results)), indent=2)+'\n')
