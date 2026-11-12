#!/usr/bin/env python3
"""Reviewer probes of the AECP notice fan-out (#665): plant each defect into a disposable copy of the ctrl tree, run
the AECP app arm (core + mailbox adapter, 2 interfaces) and the unit arm's MbxDma tests, and list every failing test.
Usage: fan_probes.py <repo root> <scratch dir> [names...]"""
import re, shutil, sys
from pathlib import Path
repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
only = set(sys.argv[3:])
sys.path.insert(0, str(repo / 'sw/firmware/ctrl/test'))
import aecp_arms, ctrl_arms, fw_gtest, aecp_mutants
from ctrl_build import CTRL, ROOT, STACK, Tree, Refusal, stack_pin
A, M = 'aecp/aecp.c', 'aecp/aecp_mbx.c'
FANEND = 'a->ports->fan_end(a->ports->ctx, a->tx_cookie, !owed);'
P = [  # (name, file, old, new, arm)
 ('baseline-aecp', None, None, None, 'aecp'),
 ('baseline-unit', None, None, None, 'unit'),
 # the author's three new rows, as their table plants them
 *[(d.name, d.path, d.old, d.new, 'aecp') for d in aecp_mutants.DEFECTS if d.name in (
   'fan-end-refused-taken-as-lost', 'refused-mid-fan-after-a-taken-frame-taken-as-lost',
   'notice-completion-kept-for-a-walk-left-owed')],
 ('author-T6-keeps-completion-for-partial', M, '\tif (!whole) {\n\t\treturn AECP_FAN_TAKEN;\n\t}\n', '\t(void)whole;\n', 'unit'),
 # reviewer plants
 ('r-whole-is-not-lost', A, FANEND, 'a->ports->fan_end(a->ports->ctx, a->tx_cookie, !lost);', 'aecp'),
 ('r-refused-completion-taken-as-done', A, '\t\towed = end != AECP_FAN_TAKEN || owed;\n',
  '\t\towed = end == AECP_FAN_LOST || owed;\n', 'aecp'),
 ('r-partial-walk-not-committed', M, '\tstruct aecp_mbx *m = ctx;\n\tif (!mbx_tx_commit(MBX_CH_AECP)) {\n\t\treturn AECP_FAN_LOST;\n\t}\n\tif (!whole) {\n\t\treturn AECP_FAN_TAKEN;\n\t}\n',
  '\tstruct aecp_mbx *m = ctx;\n\tif (!whole) {\n\t\treturn AECP_FAN_TAKEN;\n\t}\n\tif (!mbx_tx_commit(MBX_CH_AECP)) {\n\t\treturn AECP_FAN_LOST;\n\t}\n', 'aecp'),
 ('r-partial-walk-not-committed-unit', M, '\tstruct aecp_mbx *m = ctx;\n\tif (!mbx_tx_commit(MBX_CH_AECP)) {\n\t\treturn AECP_FAN_LOST;\n\t}\n\tif (!whole) {\n\t\treturn AECP_FAN_TAKEN;\n\t}\n',
  '\tstruct aecp_mbx *m = ctx;\n\tif (!whole) {\n\t\treturn AECP_FAN_TAKEN;\n\t}\n\tif (!mbx_tx_commit(MBX_CH_AECP)) {\n\t\treturn AECP_FAN_LOST;\n\t}\n', 'unit'),
 ('r-completion-checked-before-commit', M, '\tif (!mbx_tx_commit(MBX_CH_AECP)) {\n\t\treturn AECP_FAN_LOST;\n\t}\n\tif (!whole) {\n\t\treturn AECP_FAN_TAKEN;\n\t}\n\tif (m->completion_count == AECP_MBX_COMPLETIONS) {\n\t\treturn AECP_FAN_REFUSED;\n\t}\n',
  '\tif (whole && m->completion_count == AECP_MBX_COMPLETIONS) {\n\t\treturn AECP_FAN_REFUSED;\n\t}\n\tif (!mbx_tx_commit(MBX_CH_AECP)) {\n\t\treturn AECP_FAN_LOST;\n\t}\n\tif (!whole) {\n\t\treturn AECP_FAN_TAKEN;\n\t}\n', 'aecp'),
 ('r-lost-resend-keeps-spent-sequence', A, '\t\t--held_r->sequence;\n', '\t\t(void)held_r;\n', 'aecp'),
 ('r-lost-resumes-past-held', A, '\t\tk = held;\n\t\t--held_r->sequence;\n', '\t\t(void)held;\n\t\t--held_r->sequence;\n', 'aecp'),
 ('r-completion-checked-before-commit-unit', M, '\tif (!mbx_tx_commit(MBX_CH_AECP)) {\n\t\treturn AECP_FAN_LOST;\n\t}\n\tif (!whole) {\n\t\treturn AECP_FAN_TAKEN;\n\t}\n\tif (m->completion_count == AECP_MBX_COMPLETIONS) {\n\t\treturn AECP_FAN_REFUSED;\n\t}\n',
  '\tif (whole && m->completion_count == AECP_MBX_COMPLETIONS) {\n\t\treturn AECP_FAN_REFUSED;\n\t}\n\tif (!mbx_tx_commit(MBX_CH_AECP)) {\n\t\treturn AECP_FAN_LOST;\n\t}\n\tif (!whole) {\n\t\treturn AECP_FAN_TAKEN;\n\t}\n', 'unit'),
]
print('tsn-c-stack at', stack_pin(STACK.resolve()), flush=True)
config = ROOT / 'configs/endstation_ax7101_1x1_tdm8.yaml'
build = fw_gtest.Build(jobs=16)
for name, path, old, new, arm in P:
    if only and name not in only:
        continue
    root = scratch / name
    shutil.rmtree(root, ignore_errors=True)
    src = root / 'work/ctrl'
    shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    shutil.copytree(CTRL.parent / 'ctrl_nvm', src.parent / 'ctrl_nvm', ignore=shutil.ignore_patterns('test', '__pycache__', '*.pyc'))
    if path:
        t = src / path; text = t.read_text()
        if text.count(old) != 1:
            print(f'[NO-SITE] {name}: {text.count(old)} sites', flush=True); continue
        t.write_text(text.replace(old, new))
    tree = Tree(src, root / 'work/build', root / 'work/reuse', build, STACK.resolve())
    try:
        res = aecp_arms.core_arm(tree, config, 2, 'app', '*') if arm == 'aecp' else ctrl_arms.arm_unit(tree)
        log, rc = res.log, getattr(res, 'returncode', getattr(res, 'rc', None))
    except Refusal as e:
        log, rc = f'refused: {e}', 2
    (scratch / f'{name}.log').write_text(log)
    failed = sorted(set(re.findall(r'\[  FAILED  \] (\S+?)(?: |,|$)', log)))
    verdict = re.findall(r'^\s*verdict: .*$', log, re.M)
    print(f'{name} [{arm}] rc={rc} failed={len(failed)} {failed[:8]} {verdict[-1:] }', flush=True)
    shutil.rmtree(root, ignore_errors=True)
