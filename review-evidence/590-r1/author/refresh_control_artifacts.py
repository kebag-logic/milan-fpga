"""Record final control artifacts after any bound-log regrading."""
from pathlib import Path
import hashlib
import json
out=Path(__file__).parent
artifact=lambda p:dict(path=str(p),size=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
controls=[]
for stem in ('byte-only','skip-copy','no-traffic'):
    base=Path('/tmp/a385-final3-capture-'+stem)
    for p in (base/'sources.json',base/'capture.log',base/'measurement.json',Path(str(base)+'.log')):
        if p.exists():controls.append(artifact(p))
for stem in ('remove-dispatch','no-publish'):
    base=Path('/tmp/a385-final3-service-'+stem)
    for p in (base/'service_spec.json',Path(str(base)+'.log'),*base.glob('service-*.log'),*base.glob('service-*.json')):
        if p.exists():controls.append(artifact(p))
(out/'control-artifacts-final.json').write_text(json.dumps(controls,indent=2)+'\n')
p=Path('/tmp/a385-final3-service-remove-dispatch/service-queued-short-1-0-0.json')
d=json.loads(p.read_text());small=artifact(p)
small.update({k:d[k] for k in ('heartbeat_max_gap_ms','service_findings','phy')})
(out/'service-remove-dispatch-final-artifact.json').write_text(json.dumps(small,indent=2)+'\n')
print('Bound',len(controls),'control artifacts')
