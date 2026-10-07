#!/usr/bin/env python3
"""Replay duplicate published commands and focused checker/harness controls."""
import concurrent.futures
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

source, packet = [Path(x).resolve() for x in sys.argv[1:3]]
scratch=packet/'scratch'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
for key,value in [('CMAKE_PREFIX_PATH',scratch/'sdk'),('CPATH',scratch/'sdk/include'),
                  ('LIBRARY_PATH',scratch/'sdk/lib'),('LD_LIBRARY_PATH',scratch/'sdk/lib'),
                  ('TMPDIR',scratch/'temporary')]:
    env[key]=str(value)
(scratch/'temporary').mkdir(exist_ok=True)
(scratch/'browser.json').write_text(json.dumps({'args':['--no-sandbox'],'userDataDir':str(scratch/'render-profile')})+'\n')

def run(name,cmd,cwd,expected=0):
    r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True,timeout=540)
    output=(r.stdout+r.stderr).replace(str(packet),'$PACKET').replace(str(source),'$SOURCE')
    (packet/'receipts'/f'{name}.log').write_text(output)
    (packet/'receipts'/f'{name}.rc').write_text(str(r.returncode)+'\n')
    print(name,r.returncode,'expected',expected,flush=True)
    assert r.returncode==expected,output

def duplicate_sequence():
    host=scratch/'host'
    for name,cmd in [('tester-configure',['cmake','-S','.','-B','build','-DCMAKE_BUILD_TYPE=Debug']),
                     ('tester-build',['cmake','--build','build','--parallel','2']),
                     ('tester-ctest',['ctest','--test-dir','build','--output-on-failure']),
                     ('tester-scenarios',['behave'])]:
        run(name,cmd,host)

def controls():
    probe=scratch/'reference-probe'
    f=probe/'README.md';original=f.read_bytes()
    try:
        f.write_bytes(original+b'\nUse Kconfig.zephyr.\n')
        run('bare-kconfig',['python3','doc/tools/check_references.py'],probe,1)
        f.write_bytes(original+('\n'+' '.join(['word']*26)+'.\n').encode())
        run('long-sentence',['python3','doc/tools/check_sentences.py'],probe,1)
        f.write_bytes(original+b'\nRead [missing heading](doc/developer.md#not-an-existing-heading).\n')
        run('bad-heading',['python3','doc/tools/check_links.py','--local-only'],probe,1)
    finally:
        f.write_bytes(original)
    run('extra-controls-restored',['python3','doc/tools/check_references.py'],probe)
    host=scratch/'host'
    executable=host/'build/unit_tests'
    backup=executable.read_bytes();mode=executable.stat().st_mode
    # Exact empty suite behaviour, with the original executable restored afterward.
    empty=scratch/'empty-suite.c'
    empty.write_text('#include <cgreen/cgreen.h>\nint main(void) {return run_test_suite(create_test_suite(), create_text_reporter());}\n')
    try:
        run('empty-suite-compile',['cc',str(empty),'-lcgreen','-o',str(executable)],host)
        run('empty-suite-direct',[str(executable)],host)
        run('empty-suite-rejected',['ctest','--test-dir','build','--output-on-failure'],host,8)
    finally:
        executable.write_bytes(backup);executable.chmod(mode)
    run('empty-suite-restored',['./build/unit_tests'],host)

# Duplicate suite execution and executable mutation are dependent; keep them serial.
def serial_host():
    duplicate_sequence()
    controls()

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    jobs=[pool.submit(serial_host),pool.submit(run,'graph-render-final',
          ['python3','doc/tools/render_mermaid.py','--output',str(packet/'graphs'),
           '--puppeteer-config',str(scratch/'browser.json')],source)]
    for job in jobs:job.result()
