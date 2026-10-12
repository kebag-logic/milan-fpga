#!/usr/bin/env python3
"""Portable reproduction: run_checks.py REPO AUTHOR_R4 REVIEW_PACKET.

Run in the foreground. Independent checks use at most four concurrent children.
All temporary copies live under REVIEW_PACKET/scratch. No source edits occur.
The independent coverage campaign is expected to return 1 at the reviewed head.
"""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import sys

repo, author, output = (Path(a).resolve() for a in sys.argv[1:4])
scripts=Path(__file__).parent
output.mkdir(parents=True,exist_ok=True)
(output/'scratch').mkdir(exist_ok=True)
(output/'receipts').mkdir(exist_ok=True)
page=repo/'docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md'
py=[sys.executable,'-I']
checks={
 'figures-check':py+[author/'tools/check_b16_figures.py',page,author,output/'figures-rows.tsv',output/'figures-coverage.tsv'],
 'r4-controls':py+[author/'tools/r4_check_controls.py',author/'tools/check_b16_figures.py',page,author,output/'scratch/r4-controls',output/'r4-controls.json'],
 'r3-controls':py+[author/'tools/r3_check_controls.py',author/'tools/check_b16_figures.py',page,author,output/'scratch/r3-controls',output/'r3-controls.json'],
 'rebuild':py+[author/'tools/r4_figures_build.py',page,author/'tools/r4_figures_spec.py',author/'tools/check_b16_figures.py',output/'scratch/regenerated-check.py'],
 'packet-location':py+[author/'tools/r4_evidence_receipt.py',repo,'b84584e4ccb069248909f0fdeb7f8b72a1c41ae4','0782c55f',output/'packet-location.json'],
 'receipt-audit':py+[scripts/'audit_receipts.py',author,output/'receipt-audit.json'],
 'coverage-probes':py+[scripts/'probe_coverage.py',repo,author,output],
 'prior-probe':py+[scripts/'probe_figure_coverage.py',repo,author,output],
 'publication':py+[scripts/'verify_packet.py',repo,output/'publication.json'],
 'integrity':py+[scripts/'verify_checkout.py',repo,output/'integrity.json'],
 'diff-check':['git','-C',repo,'diff','--check','c20c85bd..HEAD'],
}
def run(item):
    name,cmd=item
    r=subprocess.run([str(x) for x in cmd],text=True,capture_output=True,timeout=300,cwd=repo)
    (output/(name+'.log')).write_text(r.stdout+r.stderr)
    (output/(name+'.rc')).write_text(str(r.returncode)+'\n')
    return name,r.returncode
with ThreadPoolExecutor(max_workers=4) as pool:
    result=dict(pool.map(run,checks.items()))
print(json.dumps(result,indent=2))
sys.exit(0 if all(v==0 for v in result.values()) else 1)
