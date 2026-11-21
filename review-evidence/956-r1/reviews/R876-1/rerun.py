#!/usr/bin/env python3
"""Reuse the focused executables to exercise unchanged notification paths too."""
import concurrent.futures
import subprocess
from pathlib import Path
packet=Path(__file__).resolve().parent
jobs=[
 ('aecp-1x1-if2-existing','aecp-1x1-if2','AppOutputs.*:App.SrpDeclarationChangeIsItsStreamOutputsNotice:App.NoPassIsIdleWhileAStreamOutputsNoticeIsOwed'),
 ('aecp-8x8-if1-existing','aecp-8x8-if1','AppOutputs.*:App.SrpDeclarationChangeIsItsStreamOutputsNotice:App.NoPassIsIdleWhileAStreamOutputsNoticeIsOwed'),
 ('srp-8x8-if2-existing','phases-8x8-if2','Talker.*-Talker.LatestPhase*'),
]
def run(row):
    name,build,selection=row
    exe=next((packet/'scratch'/build/'build').glob('*/suite'))
    with (packet/(name+'.log')).open('w') as f:
        r=subprocess.run([str(exe),f'--gtest_filter={selection}'],stdout=f,stderr=subprocess.STDOUT,timeout=300)
    (packet/(name+'.rc')).write_text(str(r.returncode)+'\n')
    print(name+': rc '+str(r.returncode),flush=True)
    return r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(run,jobs))
raise SystemExit(bool(any(results)))
