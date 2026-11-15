"""Round 4's item 3 on a checkout: the AECP campaign's two new build rows (aecp.h's #error, THE SHAPES not in force
where aecp.c charges a refused attempt) beside one earlier row of the same file, and the host arms the static
assertion in test_aecp.cpp holds (MBX_N_IF == AECP_TEST_INTERFACES): the core arm at one and at two interfaces, the
8x8/1if mailbox arm (EIGHT_ONE), the debug arm at two interfaces, and the plant, a core arm at two interfaces compiled
against the tracked one-interface contract, refused in the assertion's words. One line a check; exit 1 on any
unexpected result.
usage: python3 -B arm_checks.py CHECKOUT OUT"""
import sys
from pathlib import Path
from unittest.mock import patch

root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import aecp_arms  # noqa: E402
import aecp_mutants  # noqa: E402
import fw_gtest  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_build import CTRL, ROOT, STACK, Refusal, Tree  # noqa: E402

assert ROOT == root, (ROOT, root)
ROWS = ('attempt-charged-without-the-shapes', 'attempt-charged-before-the-shapes', 'retry-attempt-uncharged')
ASSERTED = "THE SHAPES: the host arm's mailbox contract (MBX_N_IF) is not at its interfaces (AECP_TEST_INTERFACES)"
bad = []


def line(name: str, ok: bool, detail: str) -> None:
    print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}", flush=True)
    if not ok:
        bad.append(name)


# the campaign's rows, its own loop and reader (aecp_mutants.campaign), on its own copy of the tree
picked = tuple(d for d in aecp_mutants.DEFECTS if d.name in ROWS)
line('the three rows are in the table', sorted(d.name for d in picked) == sorted(ROWS), str([d.name for d in picked]))
try:  # the campaign's own controls on the whole table: every test claimed, the reader's fixture
    aecp_mutants.controls()
    line("the campaign's controls on the whole table", True, f'{len(aecp_mutants.DEFECTS)} rows')
except Refusal as error:
    line("the campaign's controls on the whole table", False, str(error)[:300])
with patch.object(aecp_mutants, 'DEFECTS', picked), patch.object(aecp_mutants, 'controls', lambda: None):
    escaped = aecp_mutants.campaign(out / 'campaign', jobs=8, stack=STACK.resolve())
import json  # noqa: E402
for r in json.loads((out / 'campaign/results.json').read_text()):
    log = (out / 'campaign' / (r['name'] + '.log')).read_text()
    words = [w for _, w in r['checks']]
    line(f"campaign row {r['name']}", r['caught'], f"caught by {[t for t, _ in r['checks']]} on {words!r}; "
         f"its log's first error: {next((l.strip() for l in log.splitlines() if 'error' in l), '-')[:240]}")
line('the campaign ended with no escape', not escaped, f'escaped={escaped}')

build = fw_gtest.Build(jobs=8)
tree = Tree(CTRL, out / 'arms', out / 'arms/reuse', build, STACK.resolve())
shipping = ROOT / 'configs/endstation_ax7101_1x1_tdm8.yaml'
eight = ROOT / 'configs/endstation_ax7101_8x8.yaml'


def arm(name: str, *args, **kw) -> None:
    try:
        o = aecp_arms.core_arm(*args, **kw)
        tally = next((l for l in o.log.splitlines() if 'PASSED' in l or 'tests ran' in l), '').strip()
        line(name, o.rc == 0, f'rc {o.rc}; {tally}')
    except Refusal as error:
        line(name, False, f'refused: {str(error)[:300]}')


arm('core arm, one interface (Core.*)', Tree(CTRL, out / 'arms/c1', tree.reuse, build, tree.stack), shipping, 1, 'core')
arm('core arm, two interfaces, its own contract (Core.*)', Tree(CTRL, out / 'arms/c2', tree.reuse, build, tree.stack),
    shipping, 2, 'core')
arm('8x8/1if mailbox arm (EIGHT_ONE)', Tree(CTRL, out / 'arms/m8', tree.reuse, build, tree.stack), eight, 1, 'mailbox',
    aecp_arms.EIGHT_ONE)
arm('debug arm, two interfaces (the campaign\'s)', Tree(CTRL, out / 'arms/d2', tree.reuse, build, tree.stack), shipping,
    2, 'debug')
# the plant: the arm's earlier contract, the tracked one-interface one, at two interfaces
with patch.object(srp_arms, 'prepared', lambda t, n, o, c: (t.src, [])):
    try:
        o = aecp_arms.core_arm(Tree(CTRL, out / 'arms/p2', tree.reuse, build, tree.stack), shipping, 2, 'core')
        line('plant: a two-interface core arm at the tracked contract is refused', False, f'compiled, rc {o.rc}')
    except Refusal as error:
        text = str(error)
        line('plant: a two-interface core arm at the tracked contract is refused', ASSERTED in text and
             text.startswith('test_aecp.cpp does not compile:'), next((l.strip() for l in text.splitlines()
                                                                       if 'static assert' in l or ASSERTED in l),
                                                                      text[:200])[:300])
print('RESULT:', 'FAIL ' + ', '.join(bad) if bad else 'PASS')
sys.exit(1 if bad else 0)
