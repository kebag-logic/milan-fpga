# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""aecp_map_mutants.py - the AECP campaign's planted defects in ADD and REMOVE_AUDIO_MAPPINGS' one pass (#904):
the table each edit holds its mappings in, its passes over the command, its port's map and the other output ports'
maps, and its turns, each against the edit's definition mapping by mapping; and in a restore, which still compares
rows whole and checks the output owner itself. aecp_mutants.py plants each row; every named check must fail on its
own words."""

EDIT = 'Core.MapEditsAreTheirDefinitionRowForRow'
RESTORE = 'Core.RestoredOutputMapsHaveOneGlobalOwner'
OWNER = 'Core.OutputMappingsHaveOneGlobalOwner'

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
     'if (conflict(m->type == 14u, &rows[n], &rows[k])) return AECP_BAD_ARGUMENTS;',
     '(void)rows[k];',
     (RESTORE, 'two saved rows of one stream channel with different clusters conflict')),
    # the table: a lookup is its key's, and a value is compared whole
    ('map-table-key-unchecked', 'aecp_maps.c',
     '\t\tif (key(e->input, h) != k) {\n\t\t\tcontinue;\n\t\t}\n',
     '',
     (EDIT, 'status for command')),
    ('map-value-cluster-channel-ignored', 'aecp_maps.c',
     'h->w[0] == first && h->w[1] == second',
     'h->w[0] == first && (uint16_t)(h->w[1] ^ second) == 0u',
     (EDIT, "the edit's map is its definition's, row for row")),
    # the passes and the turns
    ('map-add-stops-early', 'aecp_maps.c',
     'steps = n + 1u;',
     'steps = n;',
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
     'if (!topology(a, port, &e.rows[n].r, true) || (held & BARRED) != 0u ||',
     'if ((held & BARRED) != 0u || !topology(a, port, &e.rows[n].r, true) ||',
     (EDIT, 'the edit reads its port for each output mapping its definition reaches')),
    ('map-repeat-counted', 'aecp_maps.c',
     'additions += adding && e.rep[n] == n && (held & FOUND) == 0u;',
     'additions += adding && (held & FOUND) == 0u;',
     (EDIT, 'status for command')),
    # a REMOVE takes the first rows equal to each mapping, one an occurrence
    ('map-remove-every-copy', 'aecp_maps.c',
     'if (v != 0u && e->copies[v - 1u] != 0u) {',
     'if (v != 0u) {',
     (EDIT, "the edit's map is its definition's, row for row")),
)
