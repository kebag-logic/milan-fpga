#!/usr/bin/env python3
"""Run public review probes unchanged, with private temporary output only."""
import concurrent.futures,os,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve(); p=Path(sys.argv[2]).resolve()
up=p/"scripts/upstream"
commands={
"render-tables-plan":[sys.executable,str(up/"render_tables.py"),"docs/design/MARK_II_AREA_PLAN.md"],
"render-tables-budget":[sys.executable,str(up/"render_tables.py"),"docs/design/AREA_BUDGET.md"],
"repro-block-probe":["bash",str(up/"repro_block_probe.sh"),".",str(p/"scratch/published-repro")],
"recompute":[sys.executable,"-I",str(up/"recompute_r492_2.py"),"."],
}
def run(item):
    name,cmd=item
    with (p/"receipts"/(name+".log")).open("w") as f:
        r=subprocess.run(cmd,cwd=root,stdout=f,stderr=subprocess.STDOUT,timeout=120,
            env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",TMPDIR=str(p/"scratch")))
    (p/"receipts"/(name+".rc")).write_text(str(r.returncode)+"\n")
    return name,r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(run,commands.items()))
for name,rc in results: print(name,rc)
raise SystemExit(any(rc for _,rc in results))
