#!/usr/bin/env python3
"""Direct tap gap checks after run_probes.py. Usage: run_direct.py PINNED_EXECUTABLE."""
from pathlib import Path
import concurrent.futures as cf
import subprocess as sp
import sys
root=Path(__file__).resolve().parent
exe=Path(sys.argv[1]).resolve()
flags='--cc --exe --build -j 4 --top-module KL_aaf_rx_depacketizer --prefix Vdepkt_top -GN_STREAMS_P=4 -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-CASEINCOMPLETE -CFLAGS "-std=c++17 -O2 -Wall -Wextra"'
def check(item):
    tree,lead=item
    name=f'direct-{tree}-{lead}'
    build=root/'scratch'/('build-'+name)
    with (root/(name+'-build.log')).open('w') as log:
        rc=sp.run(['make','-j4','-C',str(root/'scratch'/tree/'tb/verilator/avtp_rxmon'),'depkt-build',f'VERILATOR={exe}',f'DTFLAGS={flags}',f'DT_LEAD={lead}',f'DT_MDIR={build}'],stdout=log,stderr=sp.STDOUT).returncode
    assert rc==0,(name,rc)
    with (root/(name+'.log')).open('w') as log:
        rc=sp.run([str(build/'Vdepkt')],stdout=log,stderr=sp.STDOUT).returncode
    (root/(name+'.rc')).write_text(str(rc)+'\n')
    assert rc==0,(name,rc)
    return name+' PASS'
with cf.ThreadPoolExecutor(max_workers=4) as pool:
    for result in pool.map(check,[(t,n) for t in ('control','bubbles') for n in (0,16)]): print(result,flush=True)
