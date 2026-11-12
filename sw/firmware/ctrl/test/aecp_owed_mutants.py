# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""aecp_owed_mutants.py - the AECP campaign's planted defects in the owed-notice queue (#894, the ruling of 2026-11-12 on
aecp_ready, its conditions (a) to (d)) and in THE RETRY's client's first notice (THE TIERS, ctrl_loop.h). aecp_mutants.py
plants each row; every named check must fail on its own words."""

QA = 'Queued.BackToBackCommandsOfTwoControllersOweTheirNoticesInOrder'
QC = 'Queued.TheOwedQueueIsBoundedAndHoldsTheNextRecordWhileFull'
QL = 'Queued.ALongerNoticeWaitsInTheResponseBufferBehindTheQueue'
QR = 'Queued.AQueuedNoticeResumesAtItsRecipient'
NONE = 'Core.WithNoOwedSlotsTheNextRecordWaitsForTheNotice'
FIRST = 'Mailbox.ARoundBesideHeldWorkIsAQueuesFirstNoticeAlone'
TRANSMIT = 'return respond(a) || notices(a, false);'
HEAD = '\t\t\tstruct aecp_owed *o = &a->cfg.owed[a->owed_head];\n'
READY = '(a->owed_count == 0u || a->owed_count < a->cfg.owed_slots)'

ROWS = (
    # (a) per-controller order FIFO, each recipient its notice once at its next sequence_id
    ('owed-newest-first', 'aecp.c', HEAD, HEAD.replace('a->owed_head]', 'a->owed_head + a->owed_count - 1u]'),
     (QA, '(a) in the order their commands were taken')),
    ('owed-requester-forgotten', 'aecp.c', '\to->requester = a->requester;\n', '\to->requester = 0u;\n',
     (QA, "(a) the first requester has the second's")),
    ('owed-walk-restarts', 'aecp.c', '\t\t\tif (!fan_out(a, o->frame,',
     '\t\t\ta->owed_recipient = 0u;\n\t\t\tif (!fan_out(a, o->frame,',
     (QR, '(a) the walk resumes at the recipient it stopped at')),
    ('owed-long-notice-before-the-queue', 'aecp.c', '\tif (a->owed_count != 0u) {\n\t\tif (drains) {',
     '\tif (a->owed_count != 0u && !a->notify) {\n\t\tif (drains) {',
     (QL, "(a) the queue's notice first, then the long one")),
    # (b) a command's response before the notices it causes, and no notice in a record's turn
    ('owed-notice-before-its-response', 'aecp.c', TRANSMIT, 'return notices(a, true) || respond(a);',
     (QA, "(b) each response is committed in its record's turn, and no notice yet")),
    ('owed-drained-in-the-records-turn', 'aecp.c', TRANSMIT, 'return respond(a) || notices(a, true);',
     (QA, "(b) each response is committed in its record's turn, and no notice yet")),
    # (c) bounded, AECP not ready while it is full, a slot freed as its notice ends, a long notice not queued
    ('owed-ready-while-full', 'aecp.c', READY, 'true', (QC, '(c) AECP is not ready while the queue is full')),
    ('owed-never-ready-without-slots', 'aecp.c', READY, '(a->owed_count < a->cfg.owed_slots)',
     (NONE, 'command produces a response')),
    ('owed-slot-never-freed', 'aecp.c', '\t\t\t\t--a->owed_count;\n', '',
     (QC, '(c) its slot free, AECP is ready again')),
    ('owed-long-notice-queued', 'aecp.c', ' || a->response_bytes > AECP_OWED_BYTES) {', ') {',
     (QL, "its response waits for the poll, as every notice's did")),
    ('owed-not-queued', 'aecp.c', "(!a->notify || owe(a))", "!a->notify",
     (QA, '(c) a command\'s notice owed in the queue does not hold the next record')),
    # THE TIERS: a queue's first notice alone beside held work, and only the first
    ('retry-first-never-cleared', 'aecp_mbx.c',
     'l->retry_first = !owed || (l->retry_first && m->core.tx_cookie == sent);', 'l->retry_first = true;',
     (FIRST, "and the queue's next is no longer its first")),
    ('retry-round-one-ignored', 'aecp_mbx.c', 'l->round_one ? 1u : ', '',
     (FIRST, "a round beside held work builds a queue's first notice alone")),
    ('retry-first-never-set', 'aecp_mbx.c', '\tl->retry_first = true;\n\t// AECP', '\t// AECP',
     (FIRST, "a queue's first notice is tier 1's from the attach")),
)
