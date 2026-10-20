#!/usr/bin/env python3
"""Repeat the read-only delta, receipt, freshness and checkout spot-checks."""
from pathlib import Path
import subprocess
import sys
p=Path(__file__).resolve().parent
repo=Path(sys.argv[1]).resolve()
commands=[
 ('delta-check',[sys.executable,str(p/'check_delta.py'),str(repo)]),
 ('evidence-audit',[sys.executable,str(p/'audit_evidence.py')]),
 ('freshness-spotcheck',[sys.executable,'scripts/check_results_fresh.py','--log',str(p/'published/author-r2/receipts/r2-tsnfuzz/tsnfuzz.log'),'--artifact','hdl/ieee1722/avtp/doc/TEST_RESULTS.md','--label','hdl/ieee1722/avtp/doc/TEST_RESULTS.md']),
 ('tree-verification',[sys.executable,str(p/'verify_tree.py'),str(repo)]),
]
for name,args in commands:
 with (p/(name+'.log')).open('w') as out:
  result=subprocess.run(args,cwd=repo,stdout=out,stderr=subprocess.STDOUT)
 (p/(name+'.rc')).write_text(str(result.returncode)+'\n')
 print(name,'rc',result.returncode)
 if result.returncode: sys.exit(result.returncode)
