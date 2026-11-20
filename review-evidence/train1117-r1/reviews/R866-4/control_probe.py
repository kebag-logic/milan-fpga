#!/usr/bin/env python3
"""Re-anchored controls must detect their plants and fail with blinded checks."""
import sys
from pathlib import Path
from unittest import mock
sys.path.insert(0,str(Path.cwd()/'tb/verilator/ctrl_service_budget'))
import rows_tiers as r
import flip_grade as f
import shape_costs as s
import load_grade as l
import selftest_notice as n
import notice_window as w
import run
root=Path.cwd()
assert not r.channel_controls(root)
assert not f.channel_controls(root)
assert not s.retry_controls(root)
assert all(x[1] for x in n.queue_checks())
print('All re-anchored controls refuse their plants with intact detectors')
with mock.patch.object(r,'tx_statements',lambda *a,**k:[]):
    for module in (r,f):
        escaped=module.channel_controls(root)
        assert "THE TRANSMIT's stated figure under its row" in escaped, escaped
        print(module.__name__,'blind TX detector:',escaped)
old=s.findings
with mock.patch.object(s,'findings',lambda *a,**k:[x for x in old(*a,**k) if 'AECP_QUEUED_MS is' not in x]):
    escaped=s.retry_controls(root)
    assert any('last queued notice' in x for x in escaped),escaped
    print('Blind queued-value detector:',escaped)
with mock.patch.object(run,'notice_misses',lambda *a,**k:[]):
    bad=[x for x in n.queue_checks() if not x[1]]
    assert bad
    print('Blind late-notice detector:',bad)
old=w.queued_ms
with mock.patch.object(w,'queued_ms',lambda interfaces,*a,**k:old(interfaces,*a,**k)+1):
    bad=[x for x in n.queue_checks() if not x[1]]
    assert any("bound is the constants'" in x[0] for x in bad),bad
    print('Wrong queued constant:',bad)
print('Slice selected:',r.ruled(root))
assert r.ruled(root)==950
for p in ('1x1/1if','8x8/1if'):
    terms=l.load(root,p,l.STATED_US)
    print(p,'load at pin',sum(terms.values()),'terms',terms)
