#!/usr/bin/env python3
"""Focused documentation/traceability checks in a disposable clone."""
import os
from pathlib import Path
import re
import subprocess
p=Path(__file__).resolve().parents[1]
tree=p/'scratch/decode'
env=dict(os.environ,TMPDIR=str(p/'scratch'),PYTHONDONTWRITEBYTECODE='1')
with (p/'receipts/docs-checks.log').open('w') as f:
    rc=subprocess.run(['make','-j16','links','ids','reqtags','matrix','modmatrix','params'],cwd=tree,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
(p/'receipts/docs-checks.rc').write_text(str(rc)+'\n')
diff=subprocess.check_output(['git','diff','--unified=0','08023123..HEAD','--','hdl','tb'],cwd=tree,text=True)
added=[line[1:] for line in diff.splitlines() if line.startswith('+') and not line.startswith('+++')]
comments=[line for line in added if line.lstrip().startswith(('#','//'))]
pattern=r'\blane\s+[A-Za-z0-9]|\bB17\b|\bR\d+-\d+|issuecomment-|review round'
hits=[line for line in comments if re.search(pattern,line,re.I)]
(p/'receipts/source-comment-audit.txt').write_text('Added source-comment lines examined: '+str(len(comments))+'\nNew prohibited provenance labels: '+str(hits)+'\n\n'+'\n'.join(comments)+'\n')
assert not hits
with (p/'receipts/commit-shorthand.txt').open('w') as f:
    for rev in ('0b097464','0b097460'):
        r=subprocess.run(['git','rev-parse','--verify',rev+'^{commit}'],cwd=tree,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        f.write(rev+': rc='+str(r.returncode)+'\n'+r.stdout)
raise SystemExit(rc)
