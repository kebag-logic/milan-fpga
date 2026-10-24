"""rtlfast_combine.py <run1 receipts.json> <run2 receipts.json> <rtl-fast.yml>: one verdict per `needs:` job.

Run 1 is the full replica, whose six firmware jobs failed at the SDK install step (an SDK copied from another
directory). Run 2 reruns `changes` and those six jobs at the same head with the SDK installed by the repo's own
installer. Each job's verdict is taken from run 2 where it ran, else from run 1.
"""
import json
import sys
import yaml

r1, r2 = (json.load(open(p)) for p in sys.argv[1:3])
needs = yaml.safe_load(open(sys.argv[3]))['jobs']['rtl-fast']['needs']
assert r1['head'] == r2['head'] == r1['head_after'] == r2['head_after'], 'heads differ'
assert not r1['tracked_changes'] and not r2['tracked_changes'], 'clone dirty'
rows, bad = [], []
for job in needs:
    src, rec = ('run 2', r2['jobs'][job]) if job in r2['jobs'] else ('run 1', r1['jobs'][job])
    steps = [s for s in rec.get('steps', []) if 'rc' in s]
    rows.append(f"{rec['result']:8} {job:26} {src}  {len(steps)} steps run, {sum(s['seconds'] for s in steps):7.1f} s")
    if rec['result'] not in ('success', 'skipped'):
        bad.append(job)
print(f"head {r1['head']}; changes rtl={r2['jobs']['changes']['outputs'].get('rtl')} (run 1: {r1['jobs']['changes']['outputs'].get('rtl')})")
print('\n'.join(rows))
print(f"rtl-fast needs: {len(needs)} jobs, {len(needs) - len(bad)} success, failed: {bad or 'none'}")
sys.exit(1 if bad else 0)
