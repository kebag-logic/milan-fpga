"""Round-2d campaigns against round 2c's, case by case.

Every 128-case quiet/arrival log and every 32-run pull-in log is compared byte
for byte with the round-2c run of the same case (same argv, same seed, same
model apart from this round's one capture term), and the quiet-distribution
reader's JSON is compared field for field. Any difference is listed with its
first differing lines. Exit 0 = every case completed rc 0 in both rounds.
"""
import difflib
import json
from pathlib import Path

w = Path('$VALIDATION_STORAGE/645-a531/round2d')
c = Path('$VALIDATION_STORAGE/645-a531/round2c')
report = {'campaign': {}, 'pullin': {}, 'quiet_distributions': None}
rc = 0


def compare(kind, new_dir, old_dir, pattern):
    global rc
    rows = report[kind]
    for new in sorted(new_dir.glob(pattern)):
        rel = new.relative_to(new_dir)
        old = old_dir / rel
        new_rc = new.with_suffix('.rc').read_text().strip()
        old_rc = old.with_suffix('.rc').read_text().strip() if old.with_suffix('.rc').exists() else None
        same = old.exists() and old.read_bytes() == new.read_bytes()
        row = {'rc_round2d': new_rc, 'rc_round2c': old_rc, 'byte_identical': same}
        if not same and old.exists():
            row['first_differences'] = list(difflib.unified_diff(
                old.read_text().splitlines(), new.read_text().splitlines(), lineterm='', n=0))[:12]
        rows[str(rel)] = row
        rc |= new_rc != '0' or old_rc != '0'


compare('campaign', w / 'candidate/campaigns', c / 'candidate/campaigns', '*/b8_*.log')
compare('pullin', w / 'candidate/pullin', c / 'final-pullin/sweep', 'pullin_*.log')
qn = json.loads((w / 'candidate/quiet-distributions.json').read_text())
qo = json.loads((c / 'candidate/campaigns/quiet-distributions.json').read_text())
report['quiet_distributions'] = {'identical': qn == qo, 'round2d': qn, 'round2c': qo}
summary = {k: {'cases': len(v), 'byte_identical': sum(r['byte_identical'] for r in v.values()),
               'rc0_both': sum(r['rc_round2d'] == '0' and r['rc_round2c'] == '0' for r in v.values())}
           for k, v in report.items() if k != 'quiet_distributions'}
summary['quiet_distributions_identical'] = qn == qo
report['summary'] = summary
rc |= summary['campaign']['cases'] != 128 or summary['pullin']['cases'] != 32
(w / 'campaign-compare.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(summary, indent=2))
for kind in ('campaign', 'pullin'):
    for name, row in report[kind].items():
        if not row['byte_identical']:
            print('DIFFERS', kind, name, *row.get('first_differences', ['(no round-2c log)']), sep='\n  ')
raise SystemExit(rc)
