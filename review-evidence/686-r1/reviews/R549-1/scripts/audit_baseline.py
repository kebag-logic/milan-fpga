#!/usr/bin/env python3
"""Compare baseline policy and measurement identities without rerunning synthesis."""
import argparse
import json
import pathlib
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--repo', required=True, type=pathlib.Path)
p.add_argument('--base', default='e21c1ca024d37ea188ad15b5c8f9c2dae18628df')
a = p.parse_args()
path = 'syn/ooc/pp_resource_baseline.json'
before = json.loads(subprocess.check_output(['git','-C',str(a.repo),'show',f'{a.base}:{path}']))
after = json.loads((a.repo/path).read_text())
for name, value in after['endpoints'].items():
    previous = before['endpoints'][name]
    policy = lambda x: {k:v for k,v in x.items() if k not in ('record','measured')}
    assert policy(previous) == policy(value)
    assert previous['record']['identity'] == value['record']['identity']
    print(name+' policy unchanged: '+json.dumps(policy(value),sort_keys=True))
    print(name+' figures: '+json.dumps(value['record']['figures'],sort_keys=True))
    print(name+' input hash: '+value['record']['inputs_sha256'])
    print(name+' identity unchanged: True')
print('Limits: this compares committed records, not raw measurement reports or input bytes.')
