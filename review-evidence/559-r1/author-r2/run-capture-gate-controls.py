from pathlib import Path
import json,subprocess,sys
out=Path(__file__).parent
results=[]
for name in ['none','bytes','records','clock','ignore-off-timing']:
 argv=['python3','scripts/check_nvm_capture.py']+([] if name=='none' else ['--mutation',name])
 log=out/('capture-gate-'+name+'.log')
 with log.open('w') as stream:
  p=subprocess.run(argv,stdout=stream,stderr=subprocess.STDOUT,timeout=300)
 expected=0 if name=='none' else 1
 text=log.read_text()
 reason='PASS: capture census' if name=='none' else ('OFF timing omitted from maximum' if name=='ignore-off-timing' else 'capture inputs changed; remeasure both arms')
 assert p.returncode==expected and reason in text,(name,p.returncode,text)
 results.append(dict(name=name,argv=argv,returncode=p.returncode,expected=expected,matched_reason=reason))
 print(name,p.returncode,reason,flush=True)
(out/'capture-control-results.json').write_text(json.dumps(results,indent=2)+'\n')
