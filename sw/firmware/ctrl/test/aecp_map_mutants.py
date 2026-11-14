# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""aecp_map_mutants.py - the AECP campaign's planted defects in ADD and REMOVE_AUDIO_MAPPINGS' one pass (#904):
the table each edit holds its mappings in, its passes over the command, its port's map and the other output ports'
maps, and its turns, each against the edit's definition mapping by mapping; and in a restore, which still compares
rows whole and checks the output owner itself. aecp_mutants.py plants each row; every named check must fail on its
own words. THE PACE (aecp_mbx.h) holds the record after an edit; its rows are planted here too."""

EDIT = 'Core.MapEditsAreTheirDefinitionRowForRow'
RESTORE = 'Core.RestoredOutputMapsHaveOneGlobalOwner'
OWNER = 'Core.OutputMappingsHaveOneGlobalOwner'
PACE = 'Mailbox.AnEditHoldsTheNextRecordForThePaceAndDropsNone'
WORK = 'Core.MapEditWorkIsLinearInItsMappings'
KEYS = 'Core.MapKeysThatShareASlotAreTheirOwn'

#: (name, file, planted text, its replacement, (test, failing words), ...)
ROWS = (
    # a restore compares saved rows whole and checks the output owner itself
    ('restore-cluster-channel-ignored', 'aecp_maps.c',
     'a->cluster_channel == b->cluster_channel;',
     '((void)a->cluster_channel, true);',
     (RESTORE, 'a saved row that differs only in its cluster channel is its own')),
    ('restore-owner-unchecked', 'aecp_maps.c',
     'other->rows[k].channel == r->channel) return false;',
     'other->rows[k].channel == r->channel) continue;',
     (RESTORE, 'another output port owns stream channel 1')),
    ('restore-conflict-unchecked', 'aecp_maps.c',
     'return same && !equal(a, b);',
     'return same && false;',
     (RESTORE, 'two saved rows of one stream channel with different clusters conflict')),
    # the table: a lookup is its key's, and a value is compared whole
    ('map-table-key-unchecked', 'aecp_maps.c',
     '|| key(e->input, &e->rows[e->slot[s] - 1u]) == k) {',
     '|| (uint16_t)(key(e->input, &e->rows[e->slot[s] - 1u]) ^ k) == 0u) {',
     (KEYS, 'an ADD of two keys that share a slot adds both')),
    ('map-value-cluster-channel-ignored', 'aecp_maps.c',
     'return x->w[0] == y->w[0] && x->w[1] == y->w[1];',
     'return x->w[0] == y->w[0] && (uint16_t)(x->w[1] ^ y->w[1]) == 0u;',
     (EDIT, "the edit's map is its definition's, row for row")),
    # the passes and the turns: an ADD's earlier conflict, or a mapping its port's geometry refuses, ends the table
    # at its own turn, which refuses it before its port is read
    ('map-add-stops-early', 'aecp_maps.c',
     '\t\t\tif (adding) {\n\t\t\t\tsteps = n + 1u;',
     '\t\t\tif (adding) {\n\t\t\t\tsteps = n;',
     (EDIT, 'status for command')),
    ('map-illegal-ends-early', 'aecp_maps.c',
     '\t\t\te.flags[n] = ILLEGAL;\n\t\t\tsteps = n + 1u;',
     '\t\t\te.flags[n] = ILLEGAL;\n\t\t\tsteps = n;',
     (EDIT, 'status for command')),
    ('map-illegal-unflagged', 'aecp_maps.c',
     '\t\t\te.flags[n] = ILLEGAL;\n',
     '',
     (EDIT, 'status for command')),
    ('map-port-rows-unread', 'aecp_maps.c',
     'mark(&e, m, adding ? BARRED : 0u, FOUND);',
     '(void)0;',
     (EDIT, 'the edit reads its port for each output mapping its definition reaches')),
    ('map-owners-unread', 'aecp_maps.c',
     'mark(&e, v, BARRED, BARRED);',
     '(void)v;',
     (EDIT, 'the edit reads its port for each output mapping its definition reaches'),
     (OWNER, 'another port already owns this stream channel')),
    ('map-checked-before-its-read', 'aecp_maps.c',
     'if ((e.flags[n] & ILLEGAL) != 0u || !idle(a, port, &e.rows[n].r) || (held & BARRED) != 0u ||',
     'if ((e.flags[n] & ILLEGAL) != 0u || (held & BARRED) != 0u || !idle(a, port, &e.rows[n].r) ||',
     (EDIT, 'the edit reads its port for each output mapping its definition reaches')),
    ('map-repeat-counted', 'aecp_maps.c',
     'additions += adding && e.rep[n] == n && (held & FOUND) == 0u;',
     'additions += adding && (held & FOUND) == 0u;',
     (EDIT, 'status for command')),
    # a REMOVE takes the first rows equal to each mapping, one an occurrence
    ('map-remove-every-copy', 'aecp_maps.c',
     'if (is && left == 0u && e->copies[v - 1u] != 0u) {',
     'if (is && left == 0u) {',
     (EDIT, "the edit's map is its definition's, row for row")),
    # the work is linear in the mappings (#894's egress ruling of 2026-11-13, item 3): a REMOVE's other values of a
    # key linked at the key's first, never appended by a walk of those already held, which is n(n+1)/2 for n of them
    # and changes no outcome, so only the count of the work refuses it
    ('map-remove-values-rewalked', 'aecp_maps.c',
     '\t\t\te.next[n] = e.next[*at - 1u];\n\t\t\te.next[*at - 1u] = (uint8_t)(n + 1u);\n',
     '\t\t\tsize_t tail = *at - 1u;\n\t\t\twhile (e.next[tail] != 0u) {\n\t\t\t\tVISIT();\n'
     '\t\t\t\ttail = e.next[tail] - 1u;\n\t\t\t}\n\t\t\te.next[tail] = (uint8_t)(n + 1u);\n',
     (WORK, 'not under n(n+1)/2')),
    ('map-hash-the-stream-alone', 'aecp_maps.c',
     'for (size_t s = (k + 9u * (k >> 16)) & (MAP_SLOTS - 1u);;',
     'for (size_t s = k & (MAP_SLOTS - 1u);;',
     (WORK, 'past twice their sum')),
    # THE PACE: an edit that is checked holds the next record until AECP_PACE_MS after its take
    ('pace-not-held', 'aecp_mbx.c',
     'return aecp_ready(&m->core) && (uint32_t)(m->core.now - m->core.edited_ms) >= AECP_PACE_MS;',
     'return aecp_ready(&m->core);',
     (PACE, 'ms after the edit, to the pace\'s last millisecond')),
    ('pace-a-millisecond-short', 'aecp_mbx.c',
     '(uint32_t)(m->core.now - m->core.edited_ms) >= AECP_PACE_MS;',
     '(uint32_t)(m->core.now - m->core.edited_ms) >= AECP_PACE_MS - 1u;',
     (PACE, 'ms after the edit, to the pace\'s last millisecond')),
    ('pace-from-boot', 'aecp_mbx.c',
     '\tm->core.edited_ms = 0u - AECP_PACE_MS;',
     '',
     (PACE, 'before any edit nothing is held')),
    ('pace-unstamped', 'aecp_maps.c',
     '\ta->edited_ms = a->now;\n',
     '',
     (PACE, 'ms after the edit, to the pace\'s last millisecond')),
    ('pace-a-refused-edit', 'aecp_maps.c',
     '\tif (aecp_foreign_lock(a)) {\n\t\treturn AECP_ENTITY_LOCKED;',
     '\tif (aecp_foreign_lock(a)) {\n\t\ta->edited_ms = a->now;\n\t\treturn AECP_ENTITY_LOCKED;',
     (PACE, 'an edit refused before its checks holds nothing')),
)
