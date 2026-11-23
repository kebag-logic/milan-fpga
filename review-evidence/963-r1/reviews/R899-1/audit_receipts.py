#!/usr/bin/env python3
"""Check the published source-evidence packet without treating summaries as new execution."""
import collections
import hashlib
import json
import sys
from pathlib import Path
packet=Path(sys.argv[1]).resolve()
source=packet/'scratch/review-evidence/963-r1'
manifest=json.loads((source/'MANIFEST.json').read_text())
for row in manifest:
    assert hashlib.sha256((source/row['file']).read_bytes()).hexdigest()==row['published_sha256'],row['file']
r=source/'author/receipts'
rows=json.loads((r/'harness-final/strict-rows.json').read_text())
keys=[(x['point'],x['arm'],x['group']) for x in rows]
assert len(keys)==len(set(keys))==481
assert all(x['exact'] and x['difference'] is None and x['changed_frames']=={} for x in rows)
assert all(x['rc']==['0','0'] and x['stated']==[0,0] for x in rows)
calibrations=[json.loads(p.read_text()) for p in (r/'harness-final/calibration').glob('*.json')]
assert len(calibrations)==16
assert all(x['same'] and x['reference_sha256']==x['checkpoint_sha256'] for x in calibrations)
images=json.loads((r/'placement-correction/image-proof.json').read_text())
assert len(images)==16 and all(x['same_load_layout'] and x['only_map_command'] for x in images)
counts=collections.Counter(f"{x['point']}/{x['arm']}" for x in rows)
census=json.loads((packet/'shard-census.json').read_text())
assert len(census)==4
invocations=[collections.Counter(v.split(':',1)[0] for v in shard) for shard in census]
summary=dict(publication_commit='e31126d8e3c975f09a9c539f1496d3bccf44e8f2',
    checked_published_hashes=len(manifest),paired_groups=len(rows),exact_groups=len(rows),
    group_counts=dict(sorted(counts.items())),targets=[x for x in rows if x['target']],
    calibrated_head_arms=len(calibrations),placement_proofs=len(images),
    load=json.loads((r/'harness-final/load-comparison.json').read_text()),
    shard_invocations=[dict(x) for x in invocations],
    note='Published evidence audited; this script does not execute the 481 simulations or full campaigns.')
(packet/'receipt-audit.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
