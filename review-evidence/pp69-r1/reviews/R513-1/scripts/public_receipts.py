#!/usr/bin/env python3
"""Read-only public evidence identity and exact-head hosted execution snapshot."""
import base64, datetime, hashlib, json, pathlib, subprocess
packet=pathlib.Path(__file__).resolve().parents[1]; out=packet/'receipts/public'; out.mkdir(parents=True,exist_ok=True)
repo='Mister-M-alt/protocol-processor-control-plane-avb-milan'; head='cb730a2f9dd7e4f60a03a38d4b47b569e68da8df'
def get(path): return json.loads(subprocess.check_output(['gh','api','--paginate',path]))
manifest=json.loads((out/'MANIFEST.json').read_text()); rows=[]
for row in manifest:
 path=out/row['file']
 if not path.exists():
  data=get('repos/kebag-logic/milan-fpga/contents/review-evidence/pp69-r1/'+row['file']+'?ref=83221a43e3d1f5922143becbaba0661fef2c201b'); path.write_bytes(base64.b64decode(data['content']))
 digest=hashlib.sha256(path.read_bytes()).hexdigest(); assert digest==row['published_sha256']; rows.append(dict(file=row['file'],sha256=digest,verified=True))
(out/'published-digests.json').write_text(json.dumps(rows,indent=2)+'\n')
runs=get(f'repos/{repo}/actions/runs?head_sha={head}')['workflow_runs']; hosted=[]
for run in runs:
 jobs=get(f'repos/{repo}/actions/runs/{run["id"]}/jobs')['jobs']
 hosted.append(dict(id=run['id'],head_sha=run['head_sha'],event=run['event'],status=run['status'],conclusion=run['conclusion'],url=run['html_url'],jobs=[{k:j.get(k) for k in ['id','name','head_sha','status','conclusion','started_at','completed_at','html_url','steps']} for j in jobs]))
snapshot=dict(queried_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),head=head,runs=hosted)
(out/'hosted-jobs.json').write_text(json.dumps(snapshot,indent=2)+'\n')
for run in hosted:
 print(run['id'],run['event'],run['status'],run['conclusion'])
 for job in run['jobs']: print(' ',job['name'],job['status'],job['conclusion'],'skipped steps:',[s['name'] for s in job['steps'] if s['conclusion']=='skipped'])
print('Published digests verified:',len(rows))
