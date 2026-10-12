"""Check the actual tagged suite runs, then plant a missing new execution record."""
from pathlib import Path
import subprocess
import sys
import json
r=Path('$VALIDATION_STORAGE/pp73-a595/r5')
root=Path('$LANES/pp73-command-model')
side=sys.argv[1]
source=r/'base' if side=='base' else root
out=r/'trace'/side;out.mkdir(parents=True,exist_ok=True)
cmd=['python3','-B',str(source/'scripts/check-req-tags.py'),'--root',str(source),
     '--suites',str(r/'logs'/f'{side}-suites.log'),'--evidence',str(r/f'{side}-tags.txt')]
with (out/'executed.log').open('w') as f:
    rc=subprocess.run(cmd,cwd=source,stdout=f,stderr=subprocess.STDOUT,check=False).returncode
(out/'executed.rc').write_text(str(rc)+'\n')
if rc:raise SystemExit(rc)
if side=='head':
    evidence=(r/'head-tags.txt').read_text().splitlines(True)
    planted=[line for line in evidence if not line.startswith('aecp_cmds check_observed.py:')]
    removed=[line.strip() for line in evidence if line.startswith('aecp_cmds check_observed.py:')]
    assert len(removed)==1,removed
    bad=out/'missing-command-tag.txt';bad.write_text(''.join(planted))
    cmd[-1]=str(bad)
    with (out/'missing-command-tag.log').open('w') as f:
        badrc=subprocess.run(cmd,cwd=source,stdout=f,stderr=subprocess.STDOUT,check=False).returncode
    text=(out/'missing-command-tag.log').read_text()
    assert badrc==1 and 'DEAD TAG REQ-VER-002 tb/aecp_cmds/check_observed.py:' in text and 'ObservedCommands.test_sweep' in text,text
    (out/'missing-command-tag.rc').write_text(str(badrc)+'\n')
    (out/'plant.json').write_text(json.dumps({'plant':'remove new command-suite execution evidence from a copy of the full tagged run','removed':removed,'expected_rc':1,'gate_rc':badrc,'failure':'DEAD TAG REQ-VER-002; ObservedCommands.test_sweep'},indent=2)+'\n')
print((out/'executed.log').read_text(),end='')
if side=='head':print('New execution-tag plant: DEAD TAG REQ-VER-002; ObservedCommands.test_sweep; rc 1 as required')
