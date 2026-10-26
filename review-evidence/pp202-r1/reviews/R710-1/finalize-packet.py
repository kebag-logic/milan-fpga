#!/usr/bin/env python3
"""Check receipt outcomes, then hash the complete publishable packet."""
import hashlib,json,pathlib
root=pathlib.Path(__file__).resolve().parent
report=(root/'REPORT.md').read_text()
assert report.startswith('[R710] NEGATIVE - exact head a8aa626e1cba30625ac764c70e1fb8fb02c69c40\n')
assert report.rstrip().endswith('R710-1 FINISHED') and 'SKELETON' not in report
records=json.loads((root/'assigned-mutants/results.json').read_text())
assert sum(x['verdict']=='KILLED' for x in records)==20
assert sum(x['verdict']=='PASS' for x in records)==2
assert (root/'docs-check.rc').read_text().strip()=='0'
own={x['label']:x for x in json.loads((root/'own-results.json').read_text())}
assert own['own-head']['completed'] and len(own['own-head']['failures'])==2
assert len(own['own-last-slot-fault']['failures'])==8
parent=json.loads((root/'parent-probe-result.json').read_text())
assert parent['build_rc']==0 and parent['run_rc']==1
integrity=json.loads((root/'source-integrity.json').read_text())
assert integrity['bytes_and_modes_match'] and integrity['index_matches'] and integrity['status_clean']
assert integrity['gitlinks']==[] and integrity['tracked_files']==705
files=sorted(p for p in root.rglob('*') if p.is_file() and p.relative_to(root).parts[0]!='scratch' and p.name!='MANIFEST.sha256')
lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(root).as_posix() for p in files]
(root/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
print('Publishable files:',len(files),'(scratch excluded); receipt outcomes verified.')
