# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The polls by source's trace and plants (#665, the round 22 ruling, item 1): the functions the testbench reports for a
pass's polls and their heavy items (build.SPAN_SYMBOLS; poll_grade.py grades them), and the planted firmware defects
that test that gate (build.MUTATIONS, run.verdict)."""
from __future__ import annotations

#: The first and the last firmware poll of a pass, whose spans bound its polls.
FIRST, LAST = 'adp_mbx:on_poll', 'ctrl_app_srp:deliver'
#: Each item: the function the testbench traces, and the channel a commit on which marks a call that did the item's
#: work, or None where every call does.
ITEMS = {'withdraw': ('srp_mbx:reset_interface', None), 'rebuild': ('srp_mbx:open_interface', None),
         'walk': ('mrp_attr_visit', None), 'reclaim': ('mrp_reclaim', None),
         'retained': ('srp_mbx:apply_receive', None), 'mrpdu': ('srp_mbx:build_mrpdu', None),
         'acmp': ('acmp_mbx:on_poll', 'acmp'), 'aecp': ('aecp:transmit', 'aecp')}
#: build.SPAN_SYMBOLS' entries for them: a global by its symbol, a static function as (module, function).
SPANS = tuple(tuple(label.split(':')) if ':' in label else label
              for label in (FIRST, LAST, *(label for label, _ in ITEMS.values())))
#: The planted defects: build.MUTATIONS' entries, each run on the group with a link change, and the words of the
#: STATED line each must make there.
PLANTS = {
    # a heavy item in the base: SRP's poll rebuilds an interface whose link came back through its participants'
    # creation itself, not as the rebuild item (open_interface, which it keeps, never taken, so the image's code
    # layout and its hot list hold), so the pass that rebuilds carries the rebuild in its base and passes the base's
    # stated cost
    'polls-rebuild-in-the-base': ('srp/srp_mbx.c',
                                  '            if (!open_interface(i)) {\n                ++m->refused; owed = true;\n',
                                  '            if (!(m->refused == 0xFFFFFFFFu ? open_interface(i) :\n'
                                  '                  (create_participants(i) && (hold(i), true)))) {\n'
                                  '                ++m->refused; owed = true;\n', 'backlog', 'none'),
    # a heavier item: the rebuild creates an interface's participants twice, so a rebuild passes its stated cost
    'polls-rebuild-twice': ('srp/srp_mbx.c', '    if (create_participants(i)) {\n        // its declarations are owed',
                            '    if (create_participants(i) && (msrp_app_destroy(i->msrp), mvrp_app_destroy(i->mvrp), '
                            'create_participants(i))) {\n        // its declarations are owed', 'backlog', 'none'),
}
CONTROLS = {'polls-rebuild-in-the-base': "a pass's polls base of", 'polls-rebuild-twice': 'a rebuild item of'}
