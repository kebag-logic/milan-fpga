# SPDX-License-Identifier: Apache-2.0
import os,sys,concurrent.futures
sys.dont_write_bytecode = True
from run_common import *
def probes(mode):
    build=SCRATCH/('build-'+mode);exe=SCRATCH/('probe-'+mode)
    cmd=['cc','-std=c11','-I'+str(ROOT/'src/include'),'-I'+str(ROOT/'src'),'-I'+str(ROOT/'tests/unit'),PACKET/'scripts/probe.c',ROOT/'tests/unit/fault_alloc.c','-L'+str(build),'-Wl,-rpath,'+str(build),'-lshlan','-o',exe]
    assert run(mode+'-final-probe-build',cmd)[0]==0
    assert run(mode+'-final-probe',[exe])[0]==0
    assert run(mode+'-cross-port',[exe,'cross-port'])[0]==1
def extra():
    assert run('embedded',[sys.executable,'tests/check_embedded.py','--work-dir',SCRATCH/'embedded'])[0]==0
    assert run('freestanding-OFF',[sys.executable,'tests/check_freestanding.py'])[0]==0
    assert run('freestanding-ON',[sys.executable,'tests/check_freestanding.py'],env=os.environ|{'CC':'cc -DLWSRP_MILAN=1'})[0]==0
def graphs():
    config=SCRATCH/'browser.json';config.write_text('{"args":["--no-sandbox"]}')
    run('graphs',[sys.executable,'doc/tools/render_mermaid.py','--output',SCRATCH/'graphs','--puppeteer-config',config])
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    fs=[pool.submit(probes,m) for m in ['OFF','ON']]+[pool.submit(extra),pool.submit(graphs)]
    for f in fs:f.result()
