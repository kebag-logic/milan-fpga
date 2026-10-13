import os
import contextlib,io,json,sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path.cwd()/'sw/firmware/ctrl/test'))
import ctrl_build as b
import ctrl_pin as p
import ctrl_pin_env as e
import ctrl_pin_lifecycle as c
work=Path(os.environ['WORK']) / 'lifecycle-mutants'
work.mkdir(exist_ok=True)
clone=p.Clone(work,b.stack_gitlink())
def rethrow(fn,path,error):raise error[1]
cases=[('missing-command-gc',b,'HELPER_CONFIG',tuple(x for x in b.HELPER_CONFIG if not x.startswith('gc.auto=')), 'every Git call overrides enabled local maintenance'),('missing-command-maintenance',b,'HELPER_CONFIG',tuple(x for x in b.HELPER_CONFIG if not x.startswith('maintenance.auto=')), 'every Git call overrides enabled local maintenance'),('missing-clone-gc',e,'NO_MAINTENANCE',('maintenance.auto=false',),'clone, init and secondary clone disable maintenance'),('missing-clone-maintenance',e,'NO_MAINTENANCE',('gc.auto=0',),'clone, init and secondary clone disable maintenance'),('rethrow-vanished',p,'vanished',rethrow,'file vanishing after enumeration'),('swallow-all-errors',p,'vanished',lambda *args:None,'permission error is propagated')]
rows=[]
base,total=c.controls(clone)
assert base==0
for name,owner,key,replacement,needle in cases:
    stream=io.StringIO()
    with patch.object(owner,key,replacement),contextlib.redirect_stdout(stream):bad,total=c.controls(clone)
    log=stream.getvalue()
    (work/(name+'.log')).write_text(log)
    caught=bad>0 and any('[ESCAPED]' in line and needle in line for line in log.splitlines())
    print(name, 'CAUGHT' if caught else 'ESCAPED',flush=True)
    rows.append(dict(name=name,caught=caught,control=needle))
(work/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
raise SystemExit(not all(r['caught'] for r in rows))
