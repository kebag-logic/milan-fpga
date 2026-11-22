# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""aecp_map_mutants.py - the AECP campaign's planted defects in ADD and REMOVE_AUDIO_MAPPINGS' one pass (#904):
the table each edit holds its mappings in, its passes over the command, its port's map and the other output ports'
maps, and its turns, each against the edit's definition mapping by mapping; and in a restore, which still compares
rows whole and checks the output owner itself. aecp_mutants.py plants each row; every named check must fail on its
own words. THE PACE (aecp_mbx.h) holds the record after an edit; its rows are planted here too. So are the edit's
commit to the datapath's map store (#923): the core's edit port, the face's transaction on the EDIT window and the
restored maps' commit at AECP's open. And the output port's running check, which observes each stream an edit maps
once, at the first of its mappings to reach the check (#963)."""

EDIT = 'Core.MapEditsAreTheirDefinitionRowForRow'
RESTORE = 'Core.RestoredOutputMapsHaveOneGlobalOwner'
OWNER = 'Core.OutputMappingsHaveOneGlobalOwner'
PACE = 'Mailbox.AnEditHoldsTheNextRecordForThePaceAndDropsNone'
WORK = 'Core.MapEditWorkIsLinearInItsMappings'
STREAMS = 'Core.MapEditWorkObservesEachOutputStreamOnce'
KEYS = 'Core.EveryAcceptedMapKeyIsItsOwn'
STORE = 'Core.AnAcceptedEditReachesTheStoreBeforeTheMap'
STORE_REFUSES = 'Core.AStoreRefusalIsTheAnswerAndChangesNothing'
STORE_UNREACHED = 'Core.ARefusedEditNeverReachesTheStore'
RESTORE_ORDER = 'Core.RestoredMapsReachTheStoreRemovalsFirst'
RESTORE_CLIP = 'Core.TheStoresResetSetIsTheClippedOne'
RESTORE_REFUSED = 'Core.ARefusedRestoreKeepsWhatTheStoreHolds'
RESTORE_SCOPE = 'Core.TheRestoreCommitsOnlyAClosedCoresMapsInForce'
RESTORE_OPEN = 'AppStore.TheRestoredMapsReachTheStoreBeforeAecpOpens'
WINDOW = 'Face.AnEditIsTheReleasesTransactionOnTheEditWindow'
WINDOW_REFUSES = 'Face.ARefusedBeatAbortsAndNothingMoves'
WINDOW_SILENT = 'Face.AnUnansweredEditFailsUntilItsCommitIsReserved'
WINDOW_RESTORE = 'Face.RestoredMapsReachTheStoreThroughTheEditWindow'
WINDOW_LATE = 'Face.ALostReplyAfterTheReservedCommitLeavesTheStoreAndTheMapAgreeing'
RESTORE_LATE = 'Face.ALostReplyInTheRestoresCommitLeavesTheStoreAndTheMapAgreeing'
WINDOW_PICK = 'Face.AnEditCommitsTheMappingsTheCorePicksAndNoOthers'
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
    # an edit's reads are its streams' (#963), which a map's pass left out leaves as they are in the first edit it
    # breaks, so each is caught by that edit's map
    ('map-port-rows-unread', 'aecp_maps.c',
     'mark(&e, m, adding ? BARRED : 0u, FOUND);',
     '(void)0;',
     (EDIT, "the edit's map is its definition's, row for row")),
    ('map-owners-unread', 'aecp_maps.c',
     'mark(&e, v, BARRED, BARRED);',
     '(void)v;',
     (EDIT, "the edit's map is its definition's, row for row"),
     (OWNER, 'another port already owns this stream channel')),
    ('map-checked-before-its-read', 'aecp_maps.c',
     'if ((e.flags[n] & ILLEGAL) != 0u || !idle(a, &e, port, &e.rows[n].r) || (held & BARRED) != 0u ||',
     'if ((e.flags[n] & ILLEGAL) != 0u || (held & BARRED) != 0u || !idle(a, &e, port, &e.rows[n].r) ||',
     (EDIT, 'the edit reads its port once for each output stream its definition reaches')),
    # #963: the running check observes each stream an edit maps once, at its first mapping to reach the check, from
    # a table of streams the edit clears; one found running or unanswered refuses the edit at that mapping, by the
    # running check's own verdict (aecp_commands.c, aecp_running)
    ('map-stream-observed-every-mapping', 'aecp_maps.c',
     '\t*word |= bit;\n',
     '',
     (STREAMS, 'an edit observes each stream it maps once, in its order'),
     (EDIT, 'the edit reads its port once for each output stream its definition reaches')),
    ('map-stream-idle-uncleared', 'aecp_maps.c',
     '\tmemset(e.idle, 0, sizeof e.idle);\n',
     '',
     (STREAMS, 'an edit observes each stream it maps once, in its order')),
    ('map-stream-idle-one-bit', 'aecp_maps.c',
     'const uint32_t bit = 1u << (r->stream % 32u);',
     'const uint32_t bit = 1u;',
     (STREAMS, 'a stream found running refuses the edit at its first mapping')),
    ('map-stream-running-accepted', 'aecp_maps.c',
     'return aecp_running(a, 6u, r->stream) == AECP_SUCCESS;',
     'return aecp_running(a, 6u, r->stream) != AECP_ENTITY_MISBEHAVING;',
     (STREAMS, 'a stream found running refuses the edit at its first mapping')),
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
    # the edit's commit to the datapath's map store (#923): the mappings that change the map, each once, before the
    # map moves, all or none
    ('edit-store-skipped', 'aecp_maps.c',
     '\tif (changes != 0u && a->ports->edit != NULL) {',
     '\tif (changes != 0u && a->ports->edit != NULL && false) {',
     (STORE, 'one store edit for the command'),
     (WINDOW, 'begin, validate each record, begin the commit, commit each, finish')),
    ('edit-every-record', 'aecp_maps.c',
     '\t\tif (e.rep[n] == n && (!adding || (e.flags[n] & FOUND) == 0u)) {',
     '\t\tif (true) {',
     (STORE, "an ADD's additions alone, each once, in command order")),
    ('edit-held-mappings-added', 'aecp_maps.c',
     '(!adding || (e.flags[n] & FOUND) == 0u)',
     '(!adding || true)',
     (STORE, "an ADD's additions alone, each once, in command order")),
    ('edit-repeats-sent', 'aecp_maps.c',
     '\t\tif (e.rep[n] == n && (!adding',
     '\t\tif ((!adding || e.rep[n] == n) && (!adding',
     (STORE, "a REMOVE's every distinct mapping, each once, in command order")),
    ('edit-refusal-ignored', 'aecp_maps.c',
     '\t\tif (status != AECP_SUCCESS) {\n\t\t\treturn status;\n\t\t}\n\t}\n\tsize_t was = m->count;',
     '\t\t(void)status;\n\t}\n\tsize_t was = m->count;',
     (STORE_REFUSES, "the store's refusal is the command's status"),
     (WINDOW_REFUSES, 'the map keeps its mappings')),
    ('edit-before-the-checks', 'aecp_maps.c',
     '\t// Each mapping\'s checks in its turn, so the port is read as each was before.\n',
     '\tif (a->ports->edit != NULL) {\n'
     '\t\t(void)a->ports->edit(a->ports->ctx, !adding, type, index, in + 8, NULL, count);\n\t}\n',
     (STORE_UNREACHED, 'a command the core refuses never reaches the store')),
    # the restored maps' commit: every removal before any addition, the clipped reset set, the store's refusals
    ('restore-adds-beside-its-removal', 'aecp_maps.c',
     '!unmoved(a, m) && commit(a, m, true, true) != AECP_SUCCESS) {',
     '!unmoved(a, m) && (commit(a, m, true, true) != AECP_SUCCESS || commit(a, m, false, false) != AECP_SUCCESS)) {',
     (RESTORE_ORDER, 'two removals and two additions')),
    ('restore-removes-what-it-adds', 'aecp_maps.c',
     '\t\tstatus = a->ports->edit(a->ports->ctx, remove, m->type, m->index, a->response, NULL, count);',
     '\t\tstatus = a->ports->edit(a->ports->ctx, !remove, m->type, m->index, a->response, NULL, count);',
     (RESTORE_ORDER, "the input port's reset set removed"),
     (WINDOW_RESTORE, 'the reset set removed first')),
    ('restore-reset-set-unclipped', 'aecp_maps.c',
     '\treturn d != NULL && d->length >= 82u && r->channel < channels(wire_be64(d->value + 74));\n}\n\n// Whether',
     '\treturn d != NULL && d->length >= 82u;\n}\n\n// Whether',
     (RESTORE_CLIP, 'a map that is the clipped reset set has not moved')),
    ('restore-refused-reset-unclipped', 'aecp_maps.c',
     '\t\tif (kept(a, m, &m->defaults[n])) {\n\t\t\tm->rows[m->count++] = m->defaults[n];\n\t\t}\n',
     '\t\tif (a != NULL) {\n\t\t\tm->rows[m->count++] = m->defaults[n];\n\t\t}\n',
     (RESTORE_CLIP, 'a refused removal keeps the clipped reset set the store holds')),
    ('restore-removal-refusal-ignored', 'aecp_maps.c',
     '\t\t\treset(a, m, true);\n\t\t}\n\t}\n\tfor (struct aecp_map *m',
     '\t\t}\n\t}\n\tfor (struct aecp_map *m',
     (RESTORE_REFUSED, 'a refused removal keeps the reset set the store holds')),
    ('restore-not-put-back', 'aecp_maps.c',
     '\t\t\treset(a, m, commit(a, m, false, true) == AECP_SUCCESS);',
     '\t\t\treset(a, m, true);',
     (RESTORE_REFUSED, "a refused put-back leaves the store's empty port empty")),
    ('restore-put-back-trusted', 'aecp_maps.c',
     '\t\t\treset(a, m, commit(a, m, false, true) == AECP_SUCCESS);',
     '\t\t\treset(a, m, ((void)commit(a, m, false, true), true));',
     (RESTORE_REFUSED, "a refused put-back leaves the store's empty port empty")),
    ('restore-commits-an-open-core', 'aecp_maps.c',
     '\tif (!aecp_enter(a) || a->open || a->ports->edit == NULL) return;\n\tstruct aecp_map *end',
     '\tif (!aecp_enter(a) || a->ports->edit == NULL) return;\n\tstruct aecp_map *end',
     (RESTORE_SCOPE, 'an open core commits no restored map')),
    ('restore-past-a-page', 'aecp_maps.c',
     '\tif (m->capacity > AECP_MAP_PAGE) {\n\t\treturn AECP_ENTITY_MISBEHAVING;\n\t}\n',
     '',
     (RESTORE_SCOPE, 'a port past a page reaches no store')),
    ('restore-every-configuration', 'aecp_maps.c',
     '\t\tif (m->configuration == a->configuration && !unmoved(a, m) && commit(a, m, true, true)',
     '\t\tif (!unmoved(a, m) && commit(a, m, true, true)',
     (RESTORE_SCOPE, 'a map of another configuration is not committed')),
    ('restore-not-committed-at-open', 'app/ctrl_app_aecp.c',
     '\taecp_restore_commit(&c->aecp->core);\n',
     '',
     (RESTORE_OPEN, "AECP's open commits the restored maps")),
    # the face's transaction on the EDIT window, the release processor's walk
    ('window-never-aborts', 'aecp_face.c',
     '\t\t(void)beat(f, request, ABORT, 0u, 1u, 2u, &ok);\n',
     '',
     (WINDOW_REFUSES, 'a refused record aborts')),
    ('window-validation-trusted', 'aecp_face.c',
     '\t\tstatus = !record(f, request, VALIDATE, records, pick, k, &ok) ? AECP_ENTITY_MISBEHAVING\n'
     '\t\t\t: ok ? AECP_SUCCESS : AECP_BAD_ARGUMENTS;',
     '\t\tstatus = !record(f, request, VALIDATE, records, pick, k, &ok) ? AECP_ENTITY_MISBEHAVING\n'
     '\t\t\t: AECP_SUCCESS;',
     (WINDOW_REFUSES, 'a refused record aborts')),
    ('window-commit-begin-trusted', 'aecp_face.c',
     '\t\tstatus = !beat(f, request, COMMIT, 0u, 1u, 2u, &ok) ? AECP_ENTITY_MISBEHAVING\n'
     '\t\t\t: ok ? AECP_SUCCESS : AECP_BAD_ARGUMENTS;',
     '\t\tstatus = !beat(f, request, COMMIT, 0u, 1u, 2u, &ok) ? AECP_ENTITY_MISBEHAVING\n'
     '\t\t\t: AECP_SUCCESS;',
     (WINDOW_REFUSES, 'a refused commit-begin aborts')),
    ('window-begin-trusted', 'aecp_face.c',
     '? (ok ? AECP_SUCCESS : AECP_NOT_SUPPORTED) : AECP_ENTITY_MISBEHAVING;',
     '? AECP_SUCCESS : AECP_ENTITY_MISBEHAVING;',
     (WINDOW_REFUSES, 'a refused begin aborts')),
    ('window-record-halves-swapped', 'aecp_face.c',
     '\trequest[3] = (uint32_t)wire_be32(r);\n\trequest[2] = (uint32_t)wire_be32(r + 4);',
     '\trequest[2] = (uint32_t)wire_be32(r);\n\trequest[3] = (uint32_t)wire_be32(r + 4);',
     (WINDOW, 'the record as its two wire quadlets')),
    ('window-port-every-beat', 'aecp_face.c',
     '\treturn beat(f, request, phase, k, 1u, 4u, accepted);',
     '\treturn beat(f, request, phase, k, 0u, 4u, accepted);',
     (WINDOW, 'EDIT_REQ written once a transaction')),
    ('window-request-words-from-the-first', 'mbx/mbx.c',
     '\tfor (unsigned k = from; k < to && k < w->words; ++k) {',
     '\tfor (unsigned k = from & 0u; k < to && k < w->words; ++k) {',
     (WINDOW, 'EDIT_REQ written once a transaction')),
    ('window-begin-asked-once', 'aecp_face.c',
     'beat(f, request, BEGIN, 0u, 0u, 2u, &ok) || beat(f, request, BEGIN, 0u, 0u, 2u, &ok)',
     'beat(f, request, BEGIN, 0u, 0u, 2u, &ok)',
     (WINDOW_SILENT, 'a begin the boot sweep holds is asked once more')),
    ('window-reserved-commit-refuses', 'aecp_face.c',
     '\t\t(void)record(f, request, APPLY, records, pick, k, &ok);',
     '\t\tif (!record(f, request, APPLY, records, pick, k, &ok)) {\n\t\t\treturn AECP_ENTITY_MISBEHAVING;\n\t\t}',
     (WINDOW_SILENT, 'after the reserved commit, the edit stands')),
    ('window-silence-uncounted', 'aecp_face.c',
     '\t\t++f->unanswered;\n\t\treturn false;\n\t}\n\t*accepted',
     '\t\t(void)f;\n\t\treturn false;\n\t}\n\t*accepted',
     (WINDOW_SILENT, 'each unanswered beat is counted')),
    # a lost reply stops the commit: the store's application of the records after it is missing, the edit answered
    ('window-lost-reply-stops-the-commit', 'aecp_face.c',
     '\tfor (size_t k = 0; k < count; ++k) {\n\t\t(void)record(f, request, APPLY, records, pick, k, &ok);\n\t}\n',
     '\tfor (size_t k = 0; k < count && record(f, request, APPLY, records, pick, k, &ok); ++k) {\n\t}\n',
     (WINDOW_LATE, "GET_AUDIO_MAP and the datapath's store hold the same mappings"),
     (RESTORE_LATE, "GET_AUDIO_MAP and the datapath's store hold the same mappings")),
    # the face reads the command's first records in place of the ones the core picked: a held one for the new one
    ('window-pick-ignored', 'aecp_face.c',
     '\tconst uint8_t *r = records + 8u * (pick != NULL ? pick[k] : k);',
     '\tconst uint8_t *r = records + 8u * (pick != NULL ? k : k);',
     (WINDOW_PICK, 'the records the core picked are committed')),
)
