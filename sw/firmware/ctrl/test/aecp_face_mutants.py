# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""aecp_face_mutants.py - the AECP campaign's planted defects in GET_AS_PATH's read through the face (#897; IEEE
1722.1-2021 7.4.41): the count at kind 2 selector 0, each entry at selector 8 by its ordinal, through its own
interface's window, at most the core's capacity; a word with no answer fails the port; AS_PATH_CHANGED notifies the
AVB interface that changed (Milan v1.2 Table 5.22). aecp_mutants.py plants each row; every named check must fail on
its own words."""

SEQUENCE = 'Face.AsPathIsTheDatapathsSequenceThroughItsOwnWindow'
BOUND = 'Face.AsPathCarriesItsWholeBoundAndFailsACountPastIt'
UNANSWERED = 'Face.AnUnansweredAsPathWordFailsItsPortThere'
CHANGE = 'AppFace.AnAsPathChangeNotifiesTheDatapathsSequence'
#: GET_AS_PATH's two window reads, as aecp_face.c holds them.
AS_PATH_COUNT = 'if (!gsi(f, interface, 2u, AVB_INTERFACE, index, 0u, 0u, 0u, &n) || n > capacity) {'
AS_PATH_ENTRY = 'if (!gsi(f, interface, 2u, AVB_INTERFACE, index, 8u, k, 0u, &out[k])) {'
#: The AECP application's sink for AS_PATH_CHANGED (ctrl_app_aecp.c).
AS_PATH_SINK = 'ctrl_app_aecp_changed(c, 9u, e->interface, 4u);'

ROWS = (
    ('face-as-path-count-read-as-avb-info', 'aecp_face.c', AS_PATH_COUNT,
     AS_PATH_COUNT.replace('interface, 2u, AVB_INTERFACE', 'interface, 1u, AVB_INTERFACE'),
     (SEQUENCE, 'the count, then each entry once')),
    ('face-as-path-entries-at-one-ordinal', 'aecp_face.c', AS_PATH_ENTRY,
     AS_PATH_ENTRY.replace('8u, k, 0u', '8u, 0u, 0u'),
     (SEQUENCE, 'at selector 8, by its ordinal')),
    ('face-as-path-through-the-first-interface', 'aecp_face.c', AS_PATH_COUNT,
     AS_PATH_COUNT.replace('gsi(f, interface, 2u', 'gsi(f, 0u, 2u'),
     (SEQUENCE, "read through its own interface's window")),
    ('face-as-path-truncated-at-its-bound', 'aecp_face.c', AS_PATH_COUNT + '\n\t\treturn false;\n\t}\n',
     AS_PATH_COUNT.replace(' || n > capacity', '') + '\n\t\treturn false;\n\t}\n'
     '\tn = n > capacity ? capacity : n;\n',
     (BOUND, 'a count past the bound fails the port')),
    ('face-as-path-bound-off-by-one', 'aecp_face.c', AS_PATH_COUNT,
     AS_PATH_COUNT.replace('n > capacity', 'n >= capacity'),
     (BOUND, 'AECP_PATH_ITEMS entries are carried')),
    ('face-as-path-count-unanswered-ignored', 'aecp_face.c', AS_PATH_COUNT,
     AS_PATH_COUNT.replace('if (!gsi(f, interface, 2u, AVB_INTERFACE, index, 0u, 0u, 0u, &n) ||',
                           'if ((gsi(f, interface, 2u, AVB_INTERFACE, index, 0u, 0u, 0u, &n) && false) ||'),
     (UNANSWERED, 'the count unanswered fails the port')),
    ('face-as-path-entry-unanswered-ignored', 'aecp_face.c', AS_PATH_ENTRY,
     AS_PATH_ENTRY.replace('&out[k])) {', '&out[k]) && false) {'),
     (UNANSWERED, 'an entry unanswered fails the port')),
    ('face-as-path-change-notifies-avb-info', 'app/ctrl_app_aecp.c', AS_PATH_SINK,
     'ctrl_app_aecp_changed(c, 9u, e->interface, 2u);',
     (CHANGE, 'an AS_PATH change notifies GET_AS_PATH')),
    ('face-as-path-change-on-the-first-interface', 'app/ctrl_app_aecp.c', AS_PATH_SINK,
     'ctrl_app_aecp_changed(c, 9u, 0u, 4u);',
     (CHANGE, 'an AS_PATH change notifies GET_AS_PATH')),
)
