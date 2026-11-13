"""Reviewer fault probes (disposable): each plants one change the lane's tables do not plant, on a copy of the
firmware tree under --output, through the repository's own campaign drivers, and records which checks fail. A probe
that fails no check marks an untested branch. usage: python3 -I reviewer_probes.py <repo-root> {aecp,control} --output DIR"""
import argparse, re, sys
from pathlib import Path
ap = argparse.ArgumentParser(); ap.add_argument('root', type=Path); ap.add_argument('which', choices=('aecp', 'control'))
ap.add_argument('--output', type=Path, required=True); a = ap.parse_args()
test = a.root.resolve() / 'sw/firmware/ctrl/test'
sys.path.insert(0, str(test)); sys.path.insert(0, str(a.root.resolve() / 'sw/firmware/gtest'))
out = a.output.resolve(); out.mkdir(parents=True, exist_ok=True)
if a.which == 'aecp':
    import aecp_mutants as M
    probe = 'Queued.BackToBackCommandsOfTwoControllersOweTheirNoticesInOrder'
    M.DEFECTS = (
        # P1: the queue's drain keeps a counter notice's event, so its frames re-mark that counter as awaiting output
        M.defect('rp1-queue-drain-keeps-the-counter-event', 'aecp.c',
                 '\t\t\ta->counter_event = a->cfg.model->count;\n', '', (probe, '(no named words)')),
        # P2: the poll reports nothing owed while a long notice waits behind a just-drained queue
        M.defect('rp2-long-notice-not-reported-owed', 'aecp.c', '\t\treturn a->owed_count != 0u || a->notify;\n',
                 '\t\treturn a->owed_count != 0u;\n', (probe, '(no named words)')),
    )
    M.controls = lambda: None
    M.campaign(out, 2, (0, 1))
    for d in M.DEFECTS:
        log = (out / (d.name + '.log')).read_text()
        failed = sorted(set(re.findall(r'\[  FAILED  \] (\S+) \(', log)))
        print(f'{d.name}: rc-failing tests {len(failed)}: {failed}')
else:
    import ctrl_mutants as M
    from ctrl_mutant import Mutant
    M.MUTANTS = (
        # P3: a pass that took nothing leaves round_one as a pass given whole set it: its round may be one notice
        Mutant('rp3-ordinary-round-keeps-round-one', 'loop/ctrl_loop.c', '\t\tl->round_one = false;\n', '', 'port',
               'Loop.L27TierTwoRoundsComeAfterTheDrainInSlices', '(no named words)'),
    )
    M.unnamed_tests = lambda: []
    M.campaign(out, out / 'reuse', 2, shard=[0, 1])
