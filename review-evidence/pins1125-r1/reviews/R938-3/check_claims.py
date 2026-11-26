#!/usr/bin/env python3
"""Check the corrected public claims against retained source and receipts."""
import ast
from pathlib import Path
import sys

packet = Path(__file__).resolve().parent
repo = Path(sys.argv[1]).resolve()
receipts = packet / 'public/pins1125-r2/author/receipts'
body = (packet / 'pr-body.md').read_text()
row = next(x for x in body.splitlines() if x.startswith('| `tb/verilator/gptp_shadow` phase 22'))
assert 'as it does when' in row and 'only when' not in row
assert 'within 64 ns' in row
instruction = next(x for x in body.splitlines() if x.startswith('To see the regression go red'))
assert 'gptp_shadow run` (25 FAIL)' in instruction
assert 'gptp_plane run` (32 FAIL)' in instruction
old = (receipts / 'old-generator-red.log').read_text()
shadow_fails = [x for x in old.splitlines() if x.startswith('FAIL #109')]
assert len(shadow_fails) == 25
assert '490 checks: 465 PASS, 25 FAIL' in old
print('PASS corrected PR phase-22 wording and shadow reproduction tally: 25 failures')
tree = ast.parse((repo / 'tb/verilator/gptp_plane/link_delay.py').read_text())
definition = next(x.value for x in tree.body if isinstance(x, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == 'DEFECTS' for t in x.targets))
assert len(definition.elts) == 8
plane = (receipts / 'gptp_plane.log').read_text()
for item in definition.elts:
    name = ast.literal_eval(item.elts[0])
    assert 'PASS planted defect ' + name + ':' in plane
names = ['public_bank_publishes_a_negative_delay', 'public_bank_keeps_a_stale_offset',
         'graded_follow_up_not_sent']
shadow = (receipts / 'gptp_shadow.log').read_text()
mutants = (repo / 'tb/verilator/gptp_shadow/mutants.py').read_text()
for name in names:
    assert '"' + name + '"' in mutants
    assert '[ ok ] ' + name + ': caught by ' in shadow
assert 'Eleven planted defects each fail a named check.' in (repo / 'CHANGELOG.md').read_text()
print('PASS eleven named gPTP defect catches: eight plane plus three shadow; no clean control counted')
clean = (packet / 'public/prior-probes/clean.log').read_text()
assert 'OFFSET delay=-3 before=1 after=-400 delta=-401' in clean
assert 'OFFSET delay=-263 before=-12 after=-408 delta=-396' in clean
p6 = (packet / 'public/prior-probes/probe_p6_used_as_zero.log').read_text()
assert 'before=1 after=-397 delta=-398' in p6
assert '490 checks: 484 PASS, 6 FAIL' in p6
print('PASS spot-checked published offset observations and wrong-delay tolerance counterexample')
