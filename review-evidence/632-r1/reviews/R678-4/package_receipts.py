#!/usr/bin/env python3
"""Copy a bounded set of hash-verified public receipts for the review packet."""
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
source = ROOT / 'scratch/public/author-r7/receipts/round7'
files = []
for folder, names in {
    'tdm8render_mutants_d835ba12': ['HEAD.txt', 'command.txt', 'rc', 'tdm8render-campaign.log'],
    'gmstep_mutants_c2c996fa': ['HEAD.txt', 'command.txt', 'rc', 'gmstep-campaign.log'],
    'gsi_mutants_dc9cda7d': ['HEAD.txt', 'rc', 'gsi_mutants.log'],
    'notify_dc9cda7d': ['HEAD.txt', 'pp_HEAD.txt', 'summary.txt', 'notify.log'],
    'gmstep_fix_c2c996fa': ['README.txt', 'clean_leg_tree.log', 'stop_leg_head.log', 'stop_leg_dev.log', 'exempt_leg_head.log', 'exempt_leg_dev.log', 'dev_clone_head.txt', 'dev_clone_status.txt', 'dev_e5b480a3_testfix.patch', 'check_baseline_c2c996fa.log', 'lint_c2c996fa.log'],
    'capture_coherence_rerun_c2c996fa': ['HEAD.txt', 'command.txt', 'rc', 'README.txt', 'verdict_lines.txt', 'tally.txt', 'large_logs.sha256'],
    'cc-rerun-c2c996fa': ['rc', 'capture_coherence.log', 'tally.txt', 'time.txt'],
    'campaign_audit_c2c996fa': ['README.txt', 'campaign_audit.txt', 'campaign_audit.json'],
    'docs_steps_c2c996fa': ['README.txt'],
    'docs-417ec528': ['HEAD.txt', 'summary.txt'],
    'firmware_boundary_c2c996fa': ['ctrl_boundary.rc', 'ctrl_boundary.log'],
    'yosys_d835ba12': ['yosys-d835ba12.head', 'yosys-d835ba12.rc', 'yosys-d835ba12.log'],
    'lint_d835ba12': ['lint-d835ba12.head', 'lint-d835ba12.rc', 'lint-d835ba12.log'],
    'builder_bank_d835ba12': ['builder.head', 'builder.rc', 'builder.log'],
    'merge_dc9cda7d': ['merge_commit.txt', 'conflicts.txt', 'gitlinks.txt', 'gsi_anchor_check.txt', 'dynmap_anchor_check.txt'],
    'vivado_bank_5282b8b6_r7b': ['route-1x1-record.json', 'ooc-1x1-record.json', 'ooc-8x8-record.json', 'route-1x1-check-final.log', 'ooc-1x1-check-final.log', 'ooc-8x8-check-final.log', 'check-baseline.log', 'bank-steps.txt', 'route_facts.txt'],
}.items():
    files.extend(source / folder / name for name in names)
for i in range(4):
    files.extend(source / f'sweep_c2c996fa/shard{i}' / name for name in ('summary.txt', 'shard.rc'))
files.extend((source / 'firmware_gates_d835ba12').glob('*.rc'))
files.extend((source / 'pullin_d835ba12').glob('pullin_*.log'))
files.extend(source / 'pullin_d835ba12' / name for name in ('HEAD.txt', 'command.txt', 'rc'))
verified = {r['file']: r['sha256'] for r in json.loads((ROOT / 'public-evidence-verification.json').read_text())}
for p in files:
    rel = p.relative_to(source)
    assert hashlib.sha256(p.read_bytes()).hexdigest() == verified['author-r7/receipts/round7/' + str(rel)]
    dest = ROOT / 'receipts/published' / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(p, dest)
print(f'Packaged {len(files)} public receipts; each hash matches the public manifest.')
