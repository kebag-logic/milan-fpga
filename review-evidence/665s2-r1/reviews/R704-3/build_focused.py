#!/usr/bin/env python3
"""Two focused builds, joined in the foreground; compilation uses a shared lock."""
import concurrent.futures, json, os, subprocess, sys, time
from pathlib import Path
root=Path(os.environ['REVIEW_ROOT']);packet=Path(os.environ['REVIEW_PACKET'])
if len(sys.argv)>1:
    sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
    import build
    label=sys.argv[1]
    build.build(packet/'scratch'/label,'endstation_ax7101_1x1_tdm8' if label=='A1' else 'endstation_ax7101_8x8',1 if label=='A1' else 2)
else:
    def one(label):
        start=time.monotonic()
        with (packet/'scratch'/f'{label}-build.log').open('w') as log:
            rc=subprocess.call([sys.executable,'-B',__file__,label],stdout=log,stderr=subprocess.STDOUT)
        record=dict(returncode=rc,seconds=round(time.monotonic()-start,3))
        (packet/f'{label}-build.rc.json').write_text(json.dumps(record)+'\n')
        print(label,record,flush=True)
        return rc
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        codes=list(pool.map(one,('A1','A8')))
    raise SystemExit(bool(any(codes)))
