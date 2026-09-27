#!/usr/bin/env python3
"""Run read-only review packets with bounded foreground receipts."""
import json
from pathlib import Path
from run_gates import run

ROOT = Path('$LANES/593-mr-tu-soak')
OUT = Path(__file__).resolve().parent
INTERNAL = Path('$REVIEWS/593-r362-2-packet/probes')
EXTERNAL = Path('$REVIEWS/593-r363-2-packet/scripts')
SCRATCH = Path('/tmp/593-a384-review')

if __name__ == '__main__':
    commands = [
        ('internal-probe', [INTERNAL / 'r362_2_behaviour.py', ROOT]),
        ('external-probe', [EXTERNAL / 'probe_r2.py', ROOT / 'tb/tools/torture_campaign.py']),
        ('internal-mutants', [INTERNAL / 'r362_2_mutants.py', ROOT, SCRATCH / 'internal']),
        ('external-mutants', [EXTERNAL / 'reviewer_mutants.py', ROOT, SCRATCH / 'external',
                              EXTERNAL / 'probe_r2.py']),
        ('external-round1-reanchored', [EXTERNAL / 'round1_reanchored.py', ROOT,
                                       SCRATCH / 'round1', EXTERNAL / 'probe_r2.py']),
        ('external-witnesses', [EXTERNAL / 'witness_survivors.py', ROOT / 'tb/tools/torture_campaign.py',
                                SCRATCH / 'external/m01/torture_campaign.py',
                                SCRATCH / 'external/m04/torture_campaign.py']),
        ('external-residual', [EXTERNAL / 'residual_probe.py', ROOT / 'tb/tools/torture_campaign.py']),
        ('base-mutants-retained', [EXTERNAL / 'check586_mutants.py', '6d5ebd73', 'HEAD']),
    ]
    results = []
    for label, arguments in commands:
        results.append(run(label, ['python3', '-B', *map(str, arguments)]))
        (OUT / 'reviews.json').write_text(json.dumps(results, indent=2) + '\n')
