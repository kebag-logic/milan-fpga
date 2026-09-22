from pathlib import Path
import json,os,subprocess,sys,time
out=Path(sys.argv[1]).resolve();candidate=json.loads((out/'candidate.json').read_text())
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==candidate['head']
assert not subprocess.check_output(['git','status','--porcelain'])
assert all(r['exit']==0 for r in json.loads((out/'final-controls.json').read_text()))
assert all(r['exit']==0 for r in json.loads((out/'benchmark-progress.json').read_text()))
assert json.loads((out/'measurement-verification.json').read_text())['all_input_executable_and_per_leg_bytes_equal']
assert json.loads((out/'final-process-inventory.json').read_text())['empty']
for name in ('HANDOFF.md','PR-BODY.md','REVIEW-READY.md','COMMANDS.md'):
 text=(out/name).read_text();assert 'PENDING FINAL' not in text
argv=['gh','issue','comment','517','--repo','kebag-logic/milan-fpga','--body-file',str(out/'REVIEW-READY.md')]
start=time.time();proc=subprocess.run(argv,capture_output=True,text=True)
(out/'review-ready-receipt.json').write_text(json.dumps({'argv':argv,'cwd':os.getcwd(),'source_head':candidate['head'],'started_utc':start,'exit':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr},indent=2)+'\n')
assert proc.returncode==0,proc.stderr
url=proc.stdout.strip()
with (out/'HANDOFF.md').open('a') as f:f.write('\nPublic REVIEW READY: '+url+'\n')
subprocess.run(['rtk','proxy',sys.executable,str(out/'scripts/manifest.py'),str(out)],check=True)
print(url)
