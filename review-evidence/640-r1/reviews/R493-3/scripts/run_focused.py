#!/usr/bin/env python3
"""Foreground controller, at most eight concurrently executing light checks."""
import argparse,concurrent.futures,os,subprocess,sys
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument("repo"); ap.add_argument("packet"); ap.add_argument("--jobs",type=int,default=8)
a=ap.parse_args(); assert 1<=a.jobs<=16
root=Path(a.repo).resolve(); packet=Path(a.packet).resolve(); py=sys.executable
jobs={
"integrity-initial":[py,str(packet/"scripts/check_integrity.py"),str(root)],
"delta-probe":[py,str(packet/"scripts/delta_probe.py"),str(root),str(packet)],
"docs-check":[py,"scripts/docs_check.py"],
"docs-selftest":[py,"scripts/docs_check.py","--selftest"],
"doc-style":[py,"scripts/check_doc_style.py"],
"doc-paths":[py,"scripts/check_doc_paths.py"],
"feature-status":[py,"scripts/check_feature_status.py"],
"em-dash":[py,"scripts/check_em_dash.py","--base","5603c353137e90c1fa95429f6d00ef7a2298d9ee"],
"toc-check":[py,"scripts/gen_toc.py","--check"],
"toc-anchors":[py,"scripts/gen_toc.py","--verify-anchors"],
"resource-baseline":[py,"syn/ooc/pp_resource_gate.py","check-baseline"],
"diff-check":["git","diff","--check","5603c353137e90c1fa95429f6d00ef7a2298d9ee","HEAD"],
}
def run(item):
    name,argv=item
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",TMPDIR=str(packet/"scratch"))
    with (packet/"receipts"/(name+".log")).open("w") as f:
        f.write("COMMAND: "+" ".join(x.replace(str(root),"$REPO").replace(str(packet),"$PACKET") for x in argv)+"\n"); f.flush()
        r=subprocess.run(argv,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=540)
    (packet/"receipts"/(name+".rc")).write_text(str(r.returncode)+"\n")
    return name,r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
    results=list(pool.map(run,jobs.items()))
for name,rc in results: print(name,rc)
raise SystemExit(any(rc for _,rc in results))
