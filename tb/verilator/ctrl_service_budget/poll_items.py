# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The polls by source's trace and plants (#665): the functions the testbench reports for a
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
#: A pass's parts (#665: the cuts' stated costs): each channel's record and event handler, each module's
#: poll and the centisecond's dispatch as build.SPAN_SYMBOLS' entries, and each event taken and record dispatched as
#: build.CALL_SYMBOLS', which cut a pass into them; the load gate's stated costs are measured from them (load_grade.py).
PART_SPANS = (('ctrl_loop', 'dispatch_ticks'), ('aecp_mbx', 'frame'), ('srp_mbx', 'receive'),
              ('acmp_mbx', 'on_adp_frame'), ('acmp_mbx', 'on_frame'), ('maap_mbx', 'receive'), ('aecp_mbx', 'poll'),
              ('srp_mbx', 'poll'), ('maap_mbx', 'poll'), ('ctrl_app_aecp', 'deliver'), ('acmp_mbx', 'on_event'),
              ('adp_mbx', 'on_event'), ('aecp_mbx', 'event'), ('maap_mbx', 'event'), ('srp_mbx', 'on_event'),
              ('adp_mbx', 'on_frame'))
PART_CALLS = ('mbx_event_take', ('ctrl_loop', 'service_rx'))
#: A notice's recipients in aecp.c's fan_out (#665): walked by their mask and addressed in place, and as they were.
FAN_NOW = ('\tunsigned k = a->recipient;\n'
           '\twhile (!owed && k < total) {\n'
           '\t\tconst unsigned i = k / AECP_REGISTRATIONS;\n'
           '\t\tstruct aecp_registration *r = &a->registry[i][k % AECP_REGISTRATIONS];\n'
           "\t\t// the interface's used slots from k on (aecp.used), each a step of r and k\n"
           '\t\tfor (unsigned slots = (unsigned)a->used[i] >> (k % AECP_REGISTRATIONS); slots != 0u; slots >>= 1, ++r,'
           ' ++k) {\n'
           '\t\t\tif ((slots & 1u) == 0u || r->controller == a->requester) {\n'
           '\t\t\t\tcontinue;\n'
           '\t\t\t}\n'
           '\t\t\taddress(frame, r, a->cfg.mac[i]);\n'
           '\t\t\tconst enum aecp_fan taken = fan ? a->ports->fan(a->ports->ctx, i, frame, a->response_bytes) :\n'
           '\t\t\t\ta->ports->send(a->ports->ctx, i, frame, a->response_bytes, a->tx_cookie) ? AECP_FAN_TAKEN :\n'
           '\t\t\t\tAECP_FAN_REFUSED;\n'
           '\t\t\tif (taken != AECP_FAN_TAKEN) {\n'
           '\t\t\t\towed = true;\n'
           '\t\t\t\tlost = taken == AECP_FAN_LOST;\n'
           '\t\t\t\tbreak;\n'
           '\t\t\t}\n'
           '\t\t\tif (fan) {\n'
           '\t\t\t\tuint8_t *next = other;\n'
           '\t\t\t\tother = frame;\n'
           '\t\t\t\tframe = next;\n'
           '\t\t\t\theld = k;\n'
           '\t\t\t\theld_r = r;\n'
           '\t\t\t} else {\n'
           '\t\t\t\tsent_frame(a);\n'
           '\t\t\t}\n'
           '\t\t\t++r->sequence;\n'
           '\t\t}\n'
           '\t\tif (!owed) {\n'
           '\t\t\tk = (i + 1u) * AECP_REGISTRATIONS;\n'
           '\t\t}\n'
           '\t}\n')
#: The walk as it was before the cut (#665: the recipient found from its index, its frame addressed through the put
#: helpers' calls), with the lost frame's report the fan port gives today, so the plant keeps today's resume.
FAN_BEFORE = ('\twhile (a->recipient < total) {\n'
              '\t\tunsigned i = a->recipient / AECP_REGISTRATIONS;\n'
              '\t\tunsigned n = a->recipient % AECP_REGISTRATIONS;\n'
              '\t\tstruct aecp_registration *r = &a->registry[i][n];\n'
              '\t\tif (used(a, i, n) && r->controller != a->requester) {\n'
              '\t\t\taecp_put48(frame, r->mac);\n'
              '\t\t\taecp_put48(frame + 6, a->cfg.mac[i]);\n'
              '\t\t\taecp_put64(frame + 26, r->controller);\n'
              '\t\t\taecp_put16(frame + 34, r->sequence);\n'
              '\t\t\tconst enum aecp_fan taken = fan ? a->ports->fan(a->ports->ctx, i, frame, a->response_bytes) :\n'
              '\t\t\t\ta->ports->send(a->ports->ctx, i, frame, a->response_bytes, a->tx_cookie) ? AECP_FAN_TAKEN :\n'
              '\t\t\t\tAECP_FAN_REFUSED;\n'
              '\t\t\tif (taken != AECP_FAN_TAKEN) {\n'
              '\t\t\t\towed = true;\n'
              '\t\t\t\tlost = taken == AECP_FAN_LOST;\n'
              '\t\t\t\tbreak;\n'
              '\t\t\t}\n'
              '\t\t\tif (fan) {\n'
              '\t\t\t\tuint8_t *next = other;\n'
              '\t\t\t\tother = frame;\n'
              '\t\t\t\tframe = next;\n'
              '\t\t\t\theld = a->recipient;\n'
              '\t\t\t\theld_r = r;\n'
              '\t\t\t} else {\n'
              '\t\t\t\tsent_frame(a);\n'
              '\t\t\t}\n'
              '\t\t\t++r->sequence;\n'
              '\t\t}\n'
              '\t\t++a->recipient;\n'
              '\t}\n'
              '\tunsigned k = a->recipient;\n')
#: srp_mbx.c's same: the bytes compared one by one, and through memcmp as they were.
SAME_NOW = ('    while (n != 0u) {\n        --n;\n        if (a[n] != b[n]) {\n            return false;\n'
            '        }\n    }\n    return true;\n')
SAME_BEFORE = '    return memcmp(a, b, n) == 0;\n'
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
    # the old cost of a notice's recipients (#665: the notice built once): the fan-out as it was, each
    # registration found from the recipient's index and its frame addressed through the put helpers' calls, so the
    # group whose notice goes to every registered controller passes the AECP item's stated cost
    'notice-fan-out-as-it-was': ('aecp/aecp.c', FAN_NOW, FAN_BEFORE, 'aecp-fanout', 'none'),
    # the old cost of an SRP record's comparisons (#665: StreamIDs and MACs compared by same()): each StreamID and MAC
    # compared through memcmp, so the group with the heaviest SRP record passes its retry's stated cost
    'srp-compared-by-memcmp': ('srp/srp_mbx.c', SAME_NOW, SAME_BEFORE, 'notice-every-2', 'answering-every-port'),
}
CONTROLS = {'polls-rebuild-in-the-base': "a pass's polls base of", 'polls-rebuild-twice': 'a rebuild item of',
            'notice-fan-out-as-it-was': 'a aecp item of', 'srp-compared-by-memcmp': "an SRP record's apply of"}
