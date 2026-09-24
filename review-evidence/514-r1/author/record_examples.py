import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

root=Path(sys.argv[1]).resolve()
out=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'scripts'))
import check_merge_containment as mc
import merge_containment_selftest_linear as examples
from merge_containment_selftest import _Fixture
from merge_containment_selftest_scratch import quiet_git

head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
assertions=[]
receipts=[]
def refs():
    return {name:subprocess.check_output(['git','rev-parse',name],text=True).strip() for name in ['pr','main']}
def case(name,got,want,why):
    if name == 'linear-kills-measurement-mutant':
        receipts[-1]['kind']='in-process T bypass under injected object-read failure'
    assertions.append(dict(name=name,got=got,want=want,pass_=got==want,why=why))
    print('PASS' if got==want else 'FAIL',name,repr(got),flush=True)
def run(args):
    stdout,stderr=io.StringIO(),io.StringIO()
    with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
        rc=mc.main(['checker',*args])
    receipts.append(dict(kind='production',args=args,heads=refs(),rc=rc,stdout=stdout.getvalue(),stderr=stderr.getvalue()))
    return rc,stdout.getvalue()
saved=examples._mutant
def record_mutant(fx,args,before,after):
    result=saved(fx,args,before,after)
    receipts.append(dict(kind='mutant',args=args,heads=refs(),before=before.decode(),after=after.decode(),rc=result[0],stdout=result[1]))
    return result
with quiet_git(),patch.object(examples,'_mutant',record_mutant):
    examples.linear_retention_cases(_Fixture(mc,case,run))
(out/'logs/linear-examples.json').write_text(json.dumps(dict(head=head,assertions=assertions,receipts=receipts),indent=2)+'\n')
raise SystemExit(any(not row['pass_'] for row in assertions))
