#!/usr/bin/env python3
"""Run bounded focused checks concurrently, joining every child before exit."""
import argparse
import concurrent.futures
import hashlib
import importlib.util
import os
import subprocess
import sys
import tarfile
import time
from pathlib import Path

HEAD = '49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('repo', type=Path)
    ap.add_argument('--compiler', type=Path, required=True)
    ap.add_argument('--packet', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--jobs', type=int, default=4)
    a = ap.parse_args()
    assert 1 <= a.jobs <= 4
    p = a.packet.resolve()
    receipts = p/'receipts'
    receipts.mkdir(exist_ok=True)
    scratch = p/'scratch'
    scratch.mkdir(exist_ok=True)
    ident = subprocess.check_output([str(a.compiler), '--version'], text=True)
    assert ident.startswith('Verilator 5.050 '), ident
    (receipts/'compiler-identity.txt').write_text(ident + hashlib.sha256(a.compiler.read_bytes()).hexdigest() + '  compiler\n')
    assert subprocess.check_output(['git','-C',str(a.repo),'rev-parse','HEAD'],text=True).strip() == HEAD
    src = scratch/'source'
    assert not src.exists(), 'Use a fresh packet scratch/source directory'
    src.mkdir()
    archive = scratch/'source.tar'
    with archive.open('wb') as f:
        subprocess.run(['git','-C',str(a.repo),'archive',HEAD],stdout=f,check=True)
    with tarfile.open(archive) as tf:
        tf.extractall(src, filter='data')
    tmp = scratch/'tmp'
    tmp.mkdir(exist_ok=True)
    env = dict(os.environ, TMPDIR=str(tmp), PYTHONDONTWRITEBYTECODE='1',
               PATH=str(a.compiler.parent)+os.pathsep+os.environ['PATH'])
    def run(name, args, cwd=src):
        start = time.monotonic()
        with (receipts/(name+'.log')).open('w') as f:
            f.write('command: '+repr(args)+'\n'); f.flush()
            rc = subprocess.run(args,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=480).returncode
        (receipts/(name+'.rc')).write_text(str(rc)+'\n')
        print(name, 'rc', rc, 'elapsed', round(time.monotonic()-start,2), flush=True)
        return rc
    def small():
        cmds = [
            ('docs',['make','-j16','docs']),
            ('contract',['make','-j16','contract']),
            ('ooc-clock',['python3','syn/ooc/check_ooc_clock.py']),
            ('ooc-clock-selftest',['python3','syn/ooc/check_ooc_clock.py','--selftest']),
        ]
        return sum(run(n,c) != 0 for n,c in cmds)
    def parser():
        flags = '--cc --exe --build -j '+str(a.jobs)+' --top-module KL_gptp_rx_parser -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -CFLAGS "-std=c++17 -O2 -I'+str(src/'tb/verilator/parser')+' -Wall -Wextra"'
        return run('parser',['make','-j16','run','VERILATOR='+str(a.compiler),'VFLAGS='+flags],src/'tb/verilator/parser')
    def mutations():
        # Import the exact committed mutation definitions and verdict; only
        # replace its build/run plumbing to cap jobs and retain raw receipts.
        sys.path.insert(0,str(src/'tb'))
        spec = importlib.util.spec_from_file_location('parser_mutants',src/'tb/verilator/parser/mutants.py')
        m = importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        work = scratch/'mutations';work.mkdir()
        cases = [('clean', [], ())] + m.MUTATIONS
        failures = 0
        with (receipts/'mutations.log').open('w') as summary:
            for i, (name, edits, expected) in enumerate(cases):
                text = (m.HDL/m.PARSER).read_text()
                assert all(text.count(before) == 1 for before,_ in edits)
                tag = f'case{i}'
                staged = m.stage(work,tag,edits or None)
                mdir = work/('obj_'+tag)
                flags = list(m.VFLAGS);flags[flags.index('-j')+1] = str(a.jobs)
                cmd = [str(a.compiler),*flags,'--Mdir',str(mdir),'-CFLAGS',f'-std=c++17 -O2 -I{m.HERE} -Wall -Wextra',*[str(staged/s) for s in m.RTL_SOURCES],str(m.HERE/'sim_main.cpp'),'-o','Vparser']
                built = run('mutation-'+tag+'-build',cmd)
                rc = run('mutation-'+tag+'-run',[str(mdir/'Vparser')]) if built == 0 else None
                output = (receipts/('mutation-'+tag+'-run.log')).read_text() if rc is not None else ''
                verdict = m.verdict(rc,output) if rc is not None else 'build failed'
                fail_lines = [line for line in output.splitlines() if line.startswith('FAIL ')]
                missing = [e for e in expected if not any(e in s for s in fail_lines)]
                ok = verdict == ('pass' if i == 0 else 'caught') and not missing
                summary.write(f'{tag}: {name}: {"PASS" if ok else "FAIL"}; verdict={verdict}; named={len(expected)}; missing={missing}\n');summary.flush()
                failures += not ok
            summary.write(f'{len(cases)} checks: {len(cases)-failures} PASS, {failures} FAIL\n')
        (receipts/'mutations.rc').write_text(str(bool(failures)*1)+'\n')
        return failures
    # Two compiler builds at four jobs each plus one small gate stream.
    # No detached shell jobs; each child and every future is joined.
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        tasks = [pool.submit(f) for f in (small,parser,mutations)]
        results = [f.result() for f in tasks]
    rc = int(any(results))
    (receipts/'focused.rc').write_text(str(rc)+'\n')
    return rc

if __name__ == '__main__':
    sys.exit(main())
