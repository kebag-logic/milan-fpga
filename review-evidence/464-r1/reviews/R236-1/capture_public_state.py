import json,subprocess,datetime
from pathlib import Path
out=Path(__file__).parent
repo='repos/kebag-logic/milan-fpga/'
def get(endpoint,name):
 b=subprocess.check_output(['rtk','proxy','gh','api',repo+endpoint]);(out/name).write_bytes(b);return json.loads(b)
runs=get('actions/runs?head_sha=a769d9dbc937fb324c4726e60dee5b2f7ad349e3&per_page=30','hosted-runs-final.json')
for r in runs['workflow_runs']:
 jobs=get(f"actions/runs/{r['id']}/jobs?per_page=100",'hosted-jobs-final-'+r['name']+'.json')
 print(r['name'],r['status'],r['conclusion'],[(j['name'],j['conclusion']) for j in jobs['jobs'] if j['name'] in ['verilator-suites','yosys-portability']])
pr=get('pulls/513','pr-final.json');dev=get('git/ref/heads/dev','remote-dev-final.json')
# Filter before storing or displaying; no other review report is consumed.
comments=json.loads(subprocess.check_output(['rtk','proxy','gh','api',repo+'issues/513/comments?per_page=100']))
selected=[c for c in comments if c['body'].startswith('[A10]')]
(out/'pr-manager-comments-final.json').write_text(json.dumps(selected,indent=2)+'\n')
print('manager updates:',[(c['id'],c['body'].splitlines()[0]) for c in selected])
(out/'public-state-time.json').write_text(json.dumps({'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr_head':pr['head']['sha'],'live_dev':dev['object']['sha']},indent=2)+'\n')
