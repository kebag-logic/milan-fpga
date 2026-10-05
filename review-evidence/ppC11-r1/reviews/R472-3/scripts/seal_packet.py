#!/usr/bin/env python3
"""Seal only explicitly selected publishable receipts; scratch is never included."""
import argparse
import hashlib
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('packet',type=Path);a=ap.parse_args();p=a.packet.resolve()
names={'REPORT.md'}
names.update(str(x.relative_to(p)) for x in (p/'scripts').glob('*') if x.is_file())
stems=['make-check','make-ids','side_port','tx_arbiter','tx_slots','rx_validator','ids-probes','artifact-probes']
for stem in stems:
 for ext in ['log','rc']:names.add(f'receipts/{stem}.{ext}')
for stem in ['browser-measure','native-measure']:names.add(f'receipts/{stem}.rc')
json_names=['ids-probes','artifact-probes','browser-bounds','native-bounds','identities','checks','integrity','integrity-suite-copy','integrity-probe-copy','parent-live-gitlinks','public-MANIFEST','public-manifest-check','public-evidence-tree','pr','issue-body','issue-70','issue-71','issue-75','issue-84','origin-296','final-manager-comments-27','final-manager-comments-156','hosted-summary','hosted-runs','hosted-pr-merge-tree','hosted-docs-extract']
names.update('receipts/'+n+'.json' for n in json_names)
for glob in ['hosted-jobs-*.json','hosted-docs-*.log','hosted-docs-*.rc','browser-*.png','native-*.png']:
 names.update(str(x.relative_to(p)) for x in (p/'receipts').glob(glob))
names.update('receipts/'+n for n in ['independent-assessment.md','first-parent-history.txt','round3-code.diff','stat.txt','native-measure.log'])
text=(p/'REPORT.md').read_text()
assert text.splitlines()[0]=='[R472] NEGATIVE - exact head 5123548eb4de35f24d43eb088c12dab70b06d01d'
assert 'SKELETON' not in text and text.splitlines()[-1]=='R472-3 FINISHED'
lines=[]
for name in sorted(names):
 assert not name.startswith('scratch/')
 f=p/name;assert f.is_file(),name
 lines.append(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+name)
(p/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
print('Sealed',len(names),'files;',sum((p/n).stat().st_size for n in names),'bytes; scratch excluded.')
