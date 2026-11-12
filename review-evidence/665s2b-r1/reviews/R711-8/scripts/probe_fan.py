"""Reviewer probes (R711-8): the head's AECP fan-out plants and reviewer plants, each against the whole AECP core and
mailbox suites, on a disposable copy of the ctrl tree. Run: python3 -B <this> <clone>/sw/firmware/ctrl/test <outdir>."""
import re, shutil, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import aecp_arms, aecp_fan_mutants, fw_gtest
from ctrl_build import CTRL, ROOT, STACK, Tree, Refusal
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
src = out / 'work/ctrl'
shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
shutil.copytree(CTRL.parent / 'ctrl_nvm', src.parent / 'ctrl_nvm', dirs_exist_ok=True,
                ignore=shutil.ignore_patterns('test', '__pycache__', '*.pyc'))
tree = Tree(src, out / 'work/build', out / 'work/reuse', fw_gtest.Build(jobs=16), STACK)
config = ROOT / 'configs/endstation_ax7101_1x1_tdm8.yaml'
head = [(r[0], 'aecp/' + r[1], r[2], r[3]) for r in aecp_fan_mutants.ROWS[-3:]]
mine = [
    ('reviewer-refused-recipient-skipped', 'aecp/aecp.c',
     '\t\t\t\towed = true;\n\t\t\t\tlost = taken == AECP_FAN_LOST;\n\t\t\t\tbreak;\n',
     '\t\t\t\towed = true;\n\t\t\t\tlost = taken == AECP_FAN_LOST;\n\t\t\t\tif (!lost) {\n\t\t\t\t\t++k;\n\t\t\t\t}\n\t\t\t\tbreak;\n'),
    ('reviewer-completion-refusal-taken-as-done', 'aecp/aecp.c',
     '\t\towed = end != AECP_FAN_TAKEN || owed;\n', '\t\towed = end == AECP_FAN_LOST || owed;\n'),
    ('reviewer-whole-only-when-nothing-lost', 'aecp/aecp.c',
     'a->ports->fan_end(a->ports->ctx, a->tx_cookie, !owed);', 'a->ports->fan_end(a->ports->ctx, a->tx_cookie, !lost);'),
    ('reviewer-adapter-whole-ignored-after-room-check', 'aecp/aecp_mbx.c',
     '\tif (!whole) {\n\t\treturn AECP_FAN_TAKEN;\n\t}\n\tif (m->completion_count == AECP_MBX_COMPLETIONS) {\n\t\treturn AECP_FAN_REFUSED;\n\t}\n',
     '\tif (m->completion_count == AECP_MBX_COMPLETIONS) {\n\t\treturn AECP_FAN_REFUSED;\n\t}\n\tif (!whole) {\n\t\treturn AECP_FAN_TAKEN;\n\t}\n'),
]
def failed(log):
    return sorted(set(re.findall(r'\[  FAILED  \] (\S+) \(', log)))
res = aecp_arms.core_arm(tree, config, 2, 'app', '*')
print(f'unplanted: rc {res.rc}, failed {failed(res.log)}', flush=True)
for name, path, old, new in head + mine:
    t = src / path
    orig = t.read_text()
    if orig.count(old) != 1:
        print(f'{name}: site count {orig.count(old)}'); continue
    t.write_text(orig.replace(old, new))
    try:
        r = aecp_arms.core_arm(tree, config, 2, 'app', '*')
        (out / f'{name}.log').write_text(r.log)
        print(f'{name}: rc {r.rc}, failed {failed(r.log)}', flush=True)
    except Refusal as e:
        print(f'{name}: REFUSAL {str(e)[:300]}', flush=True)
    finally:
        t.write_text(orig)
