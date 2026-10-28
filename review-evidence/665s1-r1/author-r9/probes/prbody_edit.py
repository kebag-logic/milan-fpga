#!/usr/bin/env python3
"""Write PR-BODY.md from the previous round's body with this continuation's edits; each edit must apply once.
usage: prbody_edit.py OLD NEW SWEEP_LINE"""
import sys
from pathlib import Path

old, new, sweep = sys.argv[1], sys.argv[2], sys.argv[3]
text = Path(old).read_text()
EDITS = [
    ('[A680j]\n', '[A680k]\n'),
    ('GREEN at head `bdad673a7824d84c922d771ff5950e8f69083c27`, three commits on round 8\'s `27c54171`. Every gate this round touches is rc 0, including the four-shard sweep (64 of 64 suites, 2,191,124 checks), and two findings are open for a decision. `665-s1-faces` -> `dev-soft-core`.',
     f'GREEN at head `614635b7f9aed7c9138aef53d0b93ca6030ae31e`, five commits on round 8\'s `27c54171`. Every gate the last two commits touch is rc 0, including the four-shard sweep ({sweep}). Both findings the previous handoff left for a decision are ruled (6463964028). `665-s1-faces` -> `dev-soft-core`.'),
    ('Round 8 answers R701-7 (NEGATIVE at `0052e62e`) under the round-8 assignment and the ruling on its STOP, option (c).',
     'Round 8 answers R701-7 (NEGATIVE at `0052e62e`) under the round-8 assignment, the ruling on its STOP (option (c)) and the ruling 6463964028 on the two findings it left open.'),
    ('The harness now measures this branch\'s firmware at both points. Arm A\'s `aecp` group measures 25 of 25 probes at 1x1 and 39 of 39 at 8x8, with 0 T_svc misses. Two findings are open for a decision ([Known limitations](#known-limitations--out-of-scope)): the `as-built` control escapes on this branch, and SET_CONFIGURATION\'s face publication takes arm B\'s row over T_svc.',
     'The harness now measures this branch\'s firmware at both points. Arm A\'s `aecp` group measures 25 of 25 probes at 1x1 and 39 of 39 at 8x8, with 0 T_svc misses. The `as-built` control is caught on this branch: it now accepts an access fault of cause 1 or 5, either being #791\'s decode defect, and a planted control shows that a clean image escapes it. Arm B\'s SET_CONFIGURATION row misses T_svc at 1x1 and exceeds the 24 ms ceiling at 8x8; the cause is #801, outside this PR ([Known limitations](#known-limitations--out-of-scope)).'),
    ('ruling 6461910715 on its STOP). This PR is one lane',
     'ruling 6461910715 on its STOP, ruling 6463964028 on the two findings left open). This PR is one lane'),
    ('Executor: `[A680j]` (earlier: `[A680]`, `[A680b]`, `[A680c]`, `[A680d]`, `[A680e]`, `[A680f]`, `[A680g]`, `[A680h]` and `[A680i]`)',
     'Executor: `[A680k]` (earlier: `[A680]`, `[A680b]`, `[A680c]`, `[A680d]`, `[A680e]`, `[A680f]`, `[A680g]`, `[A680h]`, `[A680i]` and `[A680j]`)'),
    ('## Description\n\n',
     '## Description\n\n'
     '**The `as-built` control (round 8, `124191ca` and `614635b7`, ruling 6463964028 item 1).** The control builds the CPU with the SoC\'s rom and sram regions unchanged, so #791\'s decode defect excludes every rom address with bit 15 set, and it must see the boot refused by that defect. It required an instruction access fault, cause 1, which is what the firmware of `e76a755a` met first. On this branch the 1x1 image\'s `.data` load image is at 0x197b0, so the start code\'s first copy load meets the defect first, as a load access fault, cause 5, and the control escaped.\n\n'
     '| Piece | What changed |\n|---|---|\n'
     '| The control | `run.py` `AS_BUILT_CAUSES = (1, 5)` and `as_built_faults`: the run is caught by a trap refusal naming an access fault (interrupt bit 0) of cause 1 or 5, matched as a whole field. It prints `CONTROL as-built caught: an instruction or load access fault (cause 1 or 5)`. |\n'
     '| Self-test | Two checks grade synthetic boot-fault logs through `grade.grade` and `run.verdict`. A cause 1 and a cause 5 fault are caught. A clean boot, an illegal instruction (2), a store access fault (7), cause 15, an interrupt numbered 5, and a bus error each escape. Four mutants, each caught: cause 1 only (the earlier rule), any trap, the cause matched by its leading digit, and caught whatever the boot does. 91 checks pass and 68 mutants are caught. |\n'
     '| Real runs, 1x1 | The control at this head is caught: `TRAP 166 0 5 00000020`, rc 0. The planted control is the same run with the CPU generator handed the regions\' power-of-two cover, a CPU that decodes correctly, so the image boots clean. It is graded with no trap and prints `CONTROL as-built ESCAPED`, rc 1. Its CPU netlist is the one arm A measures with. |\n'
     '| README, `scenario.py` | The control\'s rule and why either cause is the same defect; at this head it is caught with cause 5, and a clean image escapes it. |\n\n'),
    ('- `run.py --self-test` (S2\'s harness) reports 0 failures: 89 checks pass, and every one of its 64 mutants is caught.',
     '- `run.py --self-test` (S2\'s harness) reports 0 failures: 91 checks pass, and every one of its 68 mutants is caught.'),
    ('round-8 assignment 6461128613 and the ruling on its STOP 6461910715 (option (c));',
     'round-8 assignment 6461128613, the ruling on its STOP 6461910715 (option (c)) and ruling 6463964028;'),
    ('The new rows are SET_CONFIGURATION\'s ([Known limitations](#known-limitations--out-of-scope)).',
     'The new rows are SET_CONFIGURATION\'s, whose cause is #801 ([Known limitations](#known-limitations--out-of-scope)).'),
    ('**`as-built` prints `CONTROL as-built ESCAPED` and exits 1** on this branch: an open finding ([Known limitations](#known-limitations--out-of-scope)).',
     '`as-built` prints `CONTROL as-built caught`, rc 0: the boot is refused with `TRAP 166 0 5 00000020`, a load access fault.'),
    ('- **SET_CONFIGURATION\'s face publication is slow (finding, for a decision).**\n'
     '  - On a configuration change, `aecp_face.c`\'s `publish(..., every)` writes every stream entry of the configuration on every interface, looking each one up through `aecp_find`, a linear search over the model\'s descriptors.\n'
     '  - In arm B that adds 131,573 CPU cycles at 1x1 (9.233 -> 11.660 ms, now over T_svc) and 439,826 at 8x8 interface 0 (19.788 -> 26.980 ms, now over the 24 ms ceiling).\n'
     '  - Arm A\'s fan-out does not run SET_CONFIGURATION (its formal rows equal S2\'s verdicts), so no formal row changes.\n'
     '  - Looking each entry up once is a firmware change outside this round\'s scope.\n',
     '- **Arm B\'s SET_CONFIGURATION misses T_svc at 1x1 and exceeds the 24 ms ceiling at 8x8; the cause is #801, outside this PR** (ruling 6463964028 item 2).\n'
     '  - At 1x1 the row measures 11.660 ms (S2: 9.233 ms), over T_svc. At 8x8 interface 0 it measures 26.980 ms (S2: 19.788 ms), over the 24 ms ceiling.\n'
     '  - The cause, #801: on a configuration change, `aecp_face.c`\'s `publish(..., every)` writes every stream entry of the configuration on every interface, looking each one up through `aecp_find`, a linear search over the model\'s descriptors. That adds 131,573 CPU cycles at 1x1 and 439,826 at 8x8 interface 0.\n'
     '  - Arm A\'s fan-out does not run SET_CONFIGURATION (its formal rows equal S2\'s verdicts), so no formal row changes.\n'),
    ('- **The `as-built` control escapes on this branch (finding, for a decision).**\n'
     '  - At this head and at the merge head `0052e62e`, the 1x1 image\'s start code copies `.data` from its load image at 0x197b0, which has bit 15 set. So the generator\'s rom decode defect (#791) surfaces first as a load access fault, cause 5, at pc 0x20 (`TRAP 166 0 5 00000020`). In S2\'s firmware it was an instruction access fault, cause 1, at pc 0x6880.\n'
     '  - The control requires cause 1 (`run.py:262-264`), so it prints `ESCAPED` and exits 1.\n'
     '  - The rule is not changed here. Whether to widen the control to either access fault, or to keep cause 1 and arrange the fixture\'s first rom access above 0x8000 to be a fetch, is the decision asked for. The README states it.\n',
     '- **The `as-built` control does not say which access met #791\'s defect**, only that an instruction or load access fault refused the boot (ruling 6463964028 item 1). At this head it is the start code\'s first `.data` copy load (pc 0x20); in S2\'s firmware it was a call to 0xb1ec (cause 1). The trap line in the driver log names the address.\n'),
    ('`test_ctrl_memory.py` was run again at round 8, which changes a comment in `ctrl_memory.py`.',
     '`test_ctrl_memory.py` was run again at round 8, which changes a comment in `ctrl_memory.py`. '
     'The last two commits (`124191ca`, `614635b7`) change only the harness\'s `run.py`, `selftest.py`, `selftest_mutants.py`, a docstring in `scenario.py`, and its README. '
     'After them the harness self-test, the `as-built` control and its planted control at 1x1, the docs workflow, both `ctrl_boundary.py` legs (the boundary reads `scenario.py` and `selftest.py`), behave and the sweep were run again. '
     'The firmware self-test, `fw_coverage.py`, `test_ctrl_nvm.py`, `test_builder.py`, `test_ctrl_memory.py`, `gen_mailbox.py --check` and the linked images read none of those files, so their `bdad673a` receipts stand. '
     'So do the arm A and arm B legs and `slow-adp-rx`: the change touches `run.py` only on the `as-built` path, and `scenario.py` only in a docstring.'),
]
for a, b in EDITS:
    n = text.count(a)
    if n != 1:
        raise SystemExit(f'edit applies {n} times: {a[:80]!r}')
    text = text.replace(a, b)
Path(new).write_text(text)
print('ok', len(EDITS), 'edits')
