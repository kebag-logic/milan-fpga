#!/usr/bin/env python3
"""Exercise real CLI missing/orphan comparisons and regeneration without installers."""
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
os.environ['CI_IMAGE_SHFMT'] = str(packet/'scratch/shfmt')
sys.path.insert(0,str(root/'scripts'))
import ci_tool_inventory as inventory
from ci_inventory_patterns_selftest import Fixture

results=[]
with tempfile.TemporaryDirectory(dir=packet/'scratch',prefix='drift-') as d:
    f=Fixture(Path(d))
    f.run('python3 -m pip install fixture==1.0')
    path=f.root/'ci/image/tool-inventory.json'
    def run(name,mode,expected):
        sys.argv=['inventory','--root',str(f.root),mode]
        output=io.StringIO()
        with contextlib.redirect_stdout(output),contextlib.redirect_stderr(output):
            rc=inventory.main()
        assert rc==expected,(name,rc,output.getvalue())
        results.append(dict(name=name,mode=mode,rc=rc,output=output.getvalue()))
    run('baseline','--write',0)
    run('baseline','--check',0)
    clean=json.loads(path.read_text())
    missing=json.loads(json.dumps(clean));missing['tools']=[]
    path.write_text(inventory.serialized(missing))
    run('missing entry','--check',2)
    orphan=json.loads(json.dumps(clean));orphan['tools'].append({'tool':'unused','pin':'1'})
    path.write_text(inventory.serialized(orphan))
    run('orphan entry','--check',2)
    path.write_text(inventory.serialized(clean))
    f.run('python3 -m pip install fixture==1.0 another==2.0')
    run('new installation','--check',2)
    run('record added installation','--write',0)
    assert {r['tool'] for r in json.loads(path.read_text())['tools']}=={'fixture','another'}
    run('current added inventory','--check',0)
(packet/'drift-controls.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS: real CLI missing, orphan and newly added installation controls')
