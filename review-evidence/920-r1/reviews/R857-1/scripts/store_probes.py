#!/usr/bin/env python3
"""Reviewer's disposable store probes (#920): defects in the join, the next save's start and the step a pass that
the PR's mutant list does not plant, each graded by the store suite's own self-test machinery at its self-test shape.

Usage: store_probes.py PROBE_TREE  (a disposable clone of the reviewed head; its nvm_mutants.MUTANTS is replaced)
Each probe names every write-path check as its kill list, so the self-test's verdict line reports which checks
went red ("caught by ...") or that none did (every check a survivor)."""
import sys
from pathlib import Path

tree = Path(sys.argv[1])
mut = tree / 'sw/firmware/ctrl_nvm/test/nvm_mutants.py'
CHECKS = ('first_commit_bytes', 'change_commit_bytes', 'debounce', 'capture_joins', 'busy_steps', 'open_count',
          'unchanged_no_erase', 'failed_commit_not_skipped', 'media_failures', 'recovers_after_failure',
          'dr2c_unchanged_set', 'dr2c_console', 'service_bound', 'step_room', 'powercut', 'nothing_to_save',
          'change_unknown_record', 'change_by_record_id', 'capture_window_edges')
PROBES = [
    # the next save's flag survives the capture it started: a later first change has no window, idle passes step
    ('probe_next_now_kept', '\tnvm.next_now = 0;\n\tnvm.st.phase = NVM_P_CAPTURE;', '\tnvm.st.phase = NVM_P_CAPTURE;'),
    # the walk-again flag survives into the next capture: its first walk skips a record in flight that changed
    ('probe_rewound_kept', '\tnvm.rewound = 0;\n', ''),
    # the walk again is asked for by any changed record, one the capture took included: the capture never ends
    ('probe_joined_behind_any_dirty', 'if (nvm.dirty.bit[i] & ~nvm.inflight.bit[i])', 'if (nvm.dirty.bit[i])'),
    # a step not owed taken with no room left before the deadline
    ('probe_busy_ignores_room', '\tif ((int32_t)(deadline - nvm_store_clock(ctx)) < (int32_t)NVM_STEP_US) {',
     '\tif (nvm.owed && (int32_t)(deadline - nvm_store_clock(ctx)) < (int32_t)NVM_STEP_US) {'),
    # a change during the verify counted as outside the save in flight: its next save waits for a window
    ('probe_verify_not_in_flight', 'nvm.st.phase <= NVM_P_VERIFY;', 'nvm.st.phase < NVM_P_VERIFY;'),
    # a change to a record no capture holds, marked on the walk again, does not join
    ('probe_rewound_walk_refuses_join', '(!nvm_bit(&nvm.inflight, id) || ',
     '((!nvm.rewound && !nvm_bit(&nvm.inflight, id)) || '),
    # the join's early return dropped: a joined change also opens a window and flags the next save
    ('probe_join_also_flags_next', '\tif (joins) {\n\t\tnvm_publish();\n\t\treturn;\n\t}\n',
     '\tif (joins && 0) {\n\t\tnvm_publish();\n\t\treturn;\n\t}\n'),
]
text = mut.read_text()
body = ',\n'.join(f'    _m({n!r}, STORE, {o!r}, {r!r}, *{CHECKS!r})' for n, o, r in PROBES)
text += f'\n\nMUTANTS = (\n{body},\n)\n'
mut.write_text(text)
print(f'{len(PROBES)} probes planted into {mut}')
