#!/usr/bin/env python3
"""Remove the field-oracle job count in memory and ask the production contract."""
import copy,json,pathlib,sys
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(root/'scripts'))
import ci_events as c
from ci_gate_workflows import generate
world=c.parse_world(c.read_tree(root));assert not c.check(world).findings
changed=copy.deepcopy(world);template=changed['.github/ci-templates/rtl.yml']
found=0
for job in template['jobs'].values():
 for step in job['steps']:
  body=step.get('run','')
  if '--target packet_gen --parallel "$CI_TOOL_BUILD_JOBS"' in body:
   step['run']=body.replace('--target packet_gen --parallel "$CI_TOOL_BUILD_JOBS"','--target packet_gen --parallel');found+=1
assert found==1
changed['.github/workflows/rtl.yml']=generate('rtl',template)
findings=c.check(changed).findings;assert len(findings)>=2 and all('packet_gen' in str(f) for f in findings)
result={'mutation':'s4-unbounded-field-oracle','pristine_findings':0,'mutated_findings':list(map(str,findings))}
(out/'field-bound-probe.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
