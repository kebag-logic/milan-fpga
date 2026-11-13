"""Reviewer driver: plant only the lane's new and changed defects through the repository's own campaign drivers
(ctrl_mutants, aecp_mutants, srp_mutants), each on a copy of the firmware tree under --output, and grade each by the
driver's own reader (its named test failing on its words). The drivers' whole-table ownership checks (every test named
by some defect) are suspended for the subset, since a subset names few tests by construction.
usage: python3 -I plant_subset.py <repo-root> {control,aecp,srp} --output DIR [--shard I N] [--jobs J]"""
import argparse, sys
from pathlib import Path
ap = argparse.ArgumentParser()
ap.add_argument('root', type=Path); ap.add_argument('which', choices=('control', 'aecp', 'srp'))
ap.add_argument('--output', type=Path, required=True); ap.add_argument('--shard', type=int, nargs=2, default=(0, 1))
ap.add_argument('--jobs', type=int, default=2)
a = ap.parse_args()
test = a.root.resolve() / 'sw/firmware/ctrl/test'
sys.path.insert(0, str(test)); sys.path.insert(0, str(a.root.resolve() / 'sw/firmware/gtest'))
LOOP_NEW = set('''tier1-others-beside-the-first tier1-first-to-its-cap tier1-first-past-its-time tier1-held-by-a-module-not-ready
tier1-held-by-an-empty-ring tier2-beside-tier1 whole-beside-tier1 holds-a-module-not-ready whole-row-beside-tier1
round-before-the-drain drained-beside-the-drain first-notice-not-tier1 round-one-never-told round-slice-is-the-share
slice-end-past-the-deadline slice-starts-at-the-cap transmit-told-a-whole-build step-before-the-polls
retry-before-the-polls retry-after-the-step retry-owed-lets-it-sleep retry-age-ignored retry-told-all-of-the-pass
retry-told-past-the-margin transmit-pass-uncounted transmit-after-an-aged-step transmit-in-the-aged-steps-pass
drain-past-its-time drain-to-the-cap-alone drain-past-its-records'''.split())
SRP_NEW = set('''build-resumed-from-the-first-participant build-whole-in-any-slice build-reclaim-left-to-the-next-slice
build-resumed-past-a-reset transmit-built-by-the-poll transmit-reentry-unguarded transmit-second-interface-starved'''.split())
FAN_CHANGED = {'notice-resumed-from-the-first-recipient', 'notice-to-a-freed-registration', 'notice-to-the-one-that-asked'}
out = a.output.resolve(); out.mkdir(parents=True, exist_ok=True)
if a.which == 'control':
    import ctrl_mutants as M
    M.MUTANTS = tuple(m for m in M.MUTANTS if m.name in LOOP_NEW)
    assert len(M.MUTANTS) == len(LOOP_NEW), (len(M.MUTANTS), len(LOOP_NEW))
    M.unnamed_tests = lambda: []
    print(f'subset: {len(M.MUTANTS)} control plants, shard {a.shard}', flush=True)
    rc = M.campaign(out, out / 'reuse', a.jobs, shard=list(a.shard))
elif a.which == 'aecp':
    import aecp_mutants as M, aecp_owed_mutants as O
    owed = {r[0] for r in O.ROWS}
    M.DEFECTS = tuple(d for d in M.DEFECTS if d.name in owed | FAN_CHANGED)
    assert len(M.DEFECTS) == len(owed | FAN_CHANGED), len(M.DEFECTS)
    M.controls = lambda: None
    print(f'subset: {len(M.DEFECTS)} AECP plants, shard {a.shard}', flush=True)
    rc = M.campaign(out, a.jobs, tuple(a.shard))
else:
    import srp_mutants as M
    M.DEFECTS = tuple(d for d in M.DEFECTS if d.name in SRP_NEW)
    assert len(M.DEFECTS) == len(SRP_NEW), len(M.DEFECTS)
    print(f'subset: {len(M.DEFECTS)} SRP plants at two interfaces', flush=True)
    rc = M.campaign(out, a.root.resolve() / 'third_party/lwSRP', a.jobs)
print(f'plant_subset {a.which}: {"ESCAPED" if rc else "every plant caught"}', flush=True)
sys.exit(1 if rc else 0)
