#!/usr/bin/env python3
"""Create the explicit publication allowlist; never publish scratch/history."""
import hashlib
import json
from pathlib import Path
import sys
p=Path(sys.argv[1]).resolve()
names=[
 'run_focused.py','run_controls.py','run_static.py','run_probes.py','probe_owner.cpp',
 'audit_public.py','check_integrity.py','fetch_public.py','snapshot_hosted.py','seal_packet.py',
 'focused-results.json','controls-results.json','static-results.json','evidence-audit.json',
 'pin-audit.json','integrity-final.json','review-history.json','hosted-summary.json',
 'hosted-jobs.json','environment.json','public-evidence-tree.json','scope-decisions.json',
 'owner-probe.log','owner-probe.rc','bounds-if1.log','bounds-if2.log',
]
for name in ['adp','acmp','acmpif2','maap','maap_if2','srp-composition-1','srp-composition-2','srp-unit-2',
             'mailbox-generator','submodule-docs','docs-check','doc-paths','diagram']:
    names.extend([name+'.log',name+'.rc'])
names.extend(str(f.relative_to(p)) for f in (p/'controls').rglob('*') if f.is_file())
names.extend(str(f.relative_to(p)) for f in (p/'metadata').rglob('*') if f.is_file())
# Public evidence has already been published at the immutable upstream commit.
# Preserve the source receipts; omit duplicate narratives and publication indices.
names.extend(str(f.relative_to(p)) for f in (p/'public').rglob('*') if f.is_file()
             and f.name not in ['REVIEW-READY.md','PR-BODY.md','MANIFEST.sha256'])
assert all(not n.startswith('scratch/') and 'resume-work-history' not in n for n in names)
names=sorted(set(names))
lines=[]
for name in names:
    data=(p/name).read_bytes()
    lines.append(hashlib.sha256(data).hexdigest()+'  '+name)
(p/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
report=(p/'REPORT.md').read_text()
assert report.splitlines()[0]=='[R583] NEGATIVE - exact head db29bdd07529fbc697b7956827092f64b1241714'
assert report.splitlines()[-1]=='R583-1 FINISHED'
assert 'SKELETON' not in report
assert all('| '+lens+' | UNCLEAN' in report for lens in ['Conformance','RTL','Robustness','Tests','Docs'])
print('Sealed',len(names),'publishable files plus REPORT.md;',sum((p/n).stat().st_size for n in names),'receipt bytes.')
