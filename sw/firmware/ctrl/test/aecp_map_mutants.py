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
KEYS = 'Core.EveryAcceptedMapKeyIsItsOwn'
DOMAIN = 'Core.EveryKeyOfTheDomainIsItsOwn'
OUTSIDE = 'Core.MapKeysOutsideTheDomainAreRefusedAtTheirTurn'
CLEARED = 'Core.MapEditWorkReadsOnlyWhatItCleared'
ECHO = 'Core.MapCommandsEchoTheirDescriptorAndPage'
#: Not a test: a row whose check this is is caught only by its own file's compile refusal on the words
#: (aecp_mutants.refused), at the campaign's configuration, 1x1/1if.
BUILD = 'Build.refused'

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
    # the table: a key's slot is its position in the domain, one key's alone (#894's ruling of 2026-11-14, item 1),
    # no key outside the domain forms one, and a value is compared whole
    ('map-index-channel-dropped', 'aecp_maps.c',
     '? first * MAP_CHANNELS + channel : MAP_SLOTS;',
     '? first * MAP_CHANNELS : MAP_SLOTS;',
     (KEYS, 'an ADD of every key the port accepts holds each as its own')),
    ('map-index-stream-or-cluster-dropped', 'aecp_maps.c',
     '? first * MAP_CHANNELS + channel : MAP_SLOTS;',
     '? channel : MAP_SLOTS;',
     (KEYS, 'an ADD of every key the port accepts holds each as its own')),
    ('map-index-stride-short', 'aecp_maps.c',
     '? first * MAP_CHANNELS + channel : MAP_SLOTS;',
     '? first * (MAP_CHANNELS - 1u) + channel : MAP_SLOTS;',
     (DOMAIN, 'an ADD of every key of the domain holds each as its own')),
    ('map-domain-a-channel-wide', 'aecp_maps.c',
     'return first < MAP_FIRSTS && channel < MAP_CHANNELS ?',
     'return first < MAP_FIRSTS && channel <= MAP_CHANNELS ?',
     (OUTSIDE, 'a key outside the domain is refused at its turn, before its port is read')),
    ('map-outside-row-looked-up', 'aecp_maps.c',
     'for (size_t v = s < MAP_SLOTS ? e->slot[s] : 0u; v != 0u; v = e->next[v - 1u]) {',
     'for (size_t v = e->slot[s < MAP_SLOTS ? s : 0u]; v != 0u; v = e->next[v - 1u]) {',
     (OUTSIDE, 'a row outside the domain bars no mapping')),
    # the table's declared slots hold every position place() forms, MAP_FIRSTS x MAP_CHANNELS, at compile time: a
    # table of the larger direction's own product is 16 slots at 1x1/1if, where an input key's index reaches 56
    ('map-table-each-direction-alone', 'aecp_maps.c',
     '#define MAP_SLOTS MAP_MOST(MAP_DOMAIN, MAP_FLOOR)',
     '#define MAP_SLOTS MAP_MOST(AECP_ENTITY_KEY_STREAMS * AECP_ENTITY_KEY_STREAM_CHANNELS, '
     'AECP_ENTITY_KEY_CLUSTERS * AECP_ENTITY_KEY_CLUSTER_CHANNELS)',
     (BUILD, 'static assertion failed: "the table holds every position place() forms"')),
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
    # #894: a REMOVE reads only the rows of its port's map from the first equal to a held mapping to one past the
    # last (the reach its FOUND pass holds), keeps those before in place, and moves those after down unread
    ('map-remove-reach-a-row-late', 'aecp_maps.c',
     'from = from == count ? k : from;',
     'from = from == count ? k + 1u : from;',
     (EDIT, "the edit's map is its definition's, row for row")),
    ('map-remove-reach-a-row-short', 'aecp_maps.c',
     '\t\t\t\tto = k + 1u;',
     '\t\t\t\tto = k;',
     (EDIT, "the edit's map is its definition's, row for row")),
    ('map-remove-rows-past-the-reach-dropped', 'aecp_maps.c',
     '\t\tfor (; k < count; ++k) {\n\t\t\tassign(&rows[kept++], &rows[k]);\n\t\t}\n',
     '',
     (EDIT, "the edit's map is its definition's, row for row")),
    ('map-remove-kept-row-unmoved', 'aecp_maps.c',
     '} else if (kept++ != k) {',
     '} else if (kept++ == k) {',
     (EDIT, "the edit's map is its definition's, row for row")),
    # #894: a row's words are composed in place and a mapping copied a coordinate at a time, never by memcpy
    ('map-row-words-cluster-channel-dropped', 'aecp_maps.c',
     'r->cluster | (uint32_t)r->cluster_channel << 16}};',
     'r->cluster}};',
     (EDIT, 'status for command')),
    ('map-copy-cluster-channel-dropped', 'aecp_maps.c',
     '\tto->cluster_channel = from->cluster_channel;\n',
     '',
     (EDIT, "the edit's map is its definition's, row for row")),
    # #894: an edit clears what it reads before it writes, and only that, which the work arm's edits, each started
    # from the table an earlier one left (aecp_maps.c, stale), would read otherwise
    ('map-slots-cleared-a-slot-short', 'aecp_maps.c',
     'memset(e.slot, 0, MAP_DOMAIN);',
     'memset(e.slot, 0, MAP_DOMAIN - 1u);',
     (CLEARED, "an ADD beside a row at the domain's last position is accepted")),
    ('map-marks-uncleared', 'aecp_maps.c',
     'e.next[n] = e.flags[n] = e.copies[n] = 0u;',
     'e.next[n] = e.copies[n] = 0u;',
     (CLEARED, "an ADD beside a row at the domain's last position is accepted")),
    ('map-occurrences-uncleared', 'aecp_maps.c',
     'e.next[n] = e.flags[n] = e.copies[n] = 0u;',
     'e.next[n] = e.flags[n] = 0u;',
     (CLEARED, 'a REMOVE of one of two equal rows removes one')),
    ('map-links-uncleared', 'aecp_maps.c',
     'e.next[n] = e.flags[n] = e.copies[n] = 0u;',
     'e.flags[n] = e.copies[n] = 0u;',
     (CLEARED, 'visits past twice their sum')),
    # #894: a map command's descriptor and GET_AUDIO_MAP's page are echoed a byte at a time
    ('map-echo-page-dropped', 'aecp_maps.c',
     'k < (cmd == 43u ? 6u : 4u)',
     'k < 4u',
     (ECHO, "a map command's response echoes its descriptor and page")),
    ('map-echo-index-short', 'aecp_maps.c',
     'k < (cmd == 43u ? 6u : 4u)',
     'k < (cmd == 43u ? 6u : 3u)',
     (ECHO, "a map command's response echoes its descriptor and page")),
    # the work is linear in the mappings (#894's egress ruling of 2026-11-13, item 3): a REMOVE's other values of a
    # key linked at the key's first, never appended by a walk of those already held, which is n(n+1)/2 for n of them
    # and changes no outcome, so only the count of the work refuses it
    ('map-remove-values-rewalked', 'aecp_maps.c',
     '\t\t\te.next[n] = e.next[*at - 1u];\n\t\t\te.next[*at - 1u] = (uint8_t)(n + 1u);\n',
     '\t\t\tsize_t tail = *at - 1u;\n\t\t\twhile (e.next[tail] != 0u) {\n\t\t\t\tVISIT();\n'
     '\t\t\t\ttail = e.next[tail] - 1u;\n\t\t\t}\n\t\t\te.next[tail] = (uint8_t)(n + 1u);\n',
     (WORK, 'not under n(n+1)/2')),
    # a lookup that scans the table to its key's slot changes no outcome either, and is n x the table's slots
    ('map-table-scanned', 'aecp_maps.c',
     '\tsize_t channel = k >> 16;\n\tVISIT();\n',
     '\tsize_t channel = k >> 16;\n\tfor (size_t t = 0; t <= MAP_SLOTS; ++t) {\n\t\tVISIT();\n\t}\n',
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
