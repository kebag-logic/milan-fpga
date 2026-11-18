#!/usr/bin/env python3
"""split_burst_mutants.py TREE: move #920's burst mutants (and their one helper) out of the harness's
selftest_mutants.py into selftest_mutants_burst.py, spread back into MUTANTS where they stood, so the mutant table,
its order and every mutant's patches are unchanged and selftest_mutants.py stays within check_py_idiom's
LONG_MODULE_LINES (the union of #914 and #938 put it past; each alone was within)."""
import ast
import sys
from pathlib import Path

H = Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'
src = (H / 'selftest_mutants.py').read_text()
helper_start = src.index('def _burst_cut_any_slot(')
helper_end = src.index('MUTANTS: dict[str, Patches] = {\n')
helper = src[helper_start:helper_end].rstrip('\n') + '\n'
head = 'MUTANTS: dict[str, Patches] = {\n'
block_start = helper_end + len(head)
block_end = src.index("    'marker: the frame tag is ignored': _start_with(_tag_ignored),\n", block_start)
block = src[block_start:block_end]
assert block.startswith("    # #920: a burst's and a change in flight's grade (save_burst.py)\n"), block[:80]
assert block.count("': lambda: [patch.object(") + block.count('": lambda: [patch.object(') == 5, block
assert src.count('save_burst.') == block.count('save_burst.') + helper.count('save_burst.'), \
    'save_burst used outside the burst block'
new = (src[:helper_start] + head + '    **selftest_mutants_burst.MUTANTS,\n' + src[block_end:])
new = new.replace('import save_burst\n', '', 1)
new = new.replace('import scenario\n', 'import scenario\nimport selftest_mutants_burst\n', 1)
module = ('# SPDX-FileCopyrightText: 2026 Kebag Logic\n'
          '# SPDX-License-Identifier: CERN-OHL-W-2.0\n'
          '"""#920\'s mutants of the self-test (selftest_mutants.py): a burst\'s and a change in flight\'s grade\n'
          '(save_burst.py), each replacing one of its rules with a plausible defect; selftest_mutants.MUTANTS takes them\n'
          'first, in this order."""\n'
          'from __future__ import annotations\n\n'
          'from collections.abc import Callable\n'
          'from pathlib import Path\n'
          'from unittest.mock import patch\n\n'
          'import save_burst\n\n\n'
          + helper + '\n\n'
          'MUTANTS: dict[str, Callable[[], list]] = {\n' + block.replace(
              "    # #920: a burst's and a change in flight's grade (save_burst.py)\n", '') + '}\n')
ast.parse(new)
ast.parse(module)
(H / 'selftest_mutants.py').write_text(new)
(H / 'selftest_mutants_burst.py').write_text(module)
print('selftest_mutants.py', len(new.splitlines()), 'lines; selftest_mutants_burst.py', len(module.splitlines()))
