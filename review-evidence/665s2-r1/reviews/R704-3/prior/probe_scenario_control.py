#!/usr/bin/env python3
"""A missing backlog channel must not redefine the required stress population."""
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch
root=Path(os.environ['REVIEW_ROOT']);packet=Path(os.environ['REVIEW_PACKET'])
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import scenario,selftest
original=scenario.Group.offer
def omitted(self,channel,step,frame):
    if self.name.startswith('backlog') and channel=='srp':return
    return original(self,channel,step,frame)
with patch.object(scenario.Group,'offer',omitted):
    failures=[name for name,ok,_ in selftest.checks() if not ok]
    spec=json.loads((packet/'scratch/A1/build.json').read_text())
    group=scenario.backlog_groups(scenario.point('1x1',spec))[0]
    result=dict(plant='omit SRP from backlog scenarios and their self-declared load',
                load=group.load,failed_checks=failures)
(packet/'scenario-control.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
