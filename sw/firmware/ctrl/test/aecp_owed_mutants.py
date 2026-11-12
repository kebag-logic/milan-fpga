# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""aecp_owed_mutants.py - the AECP campaign's planted defects in the owed-notice queue (#894, the ruling of
2026-11-12 on aecp_ready, its conditions (a) to (d)) and in THE RETRY's client's first notice (THE TIERS,
ctrl_loop.h). aecp_mutants.py plants each row; every named check must fail on its own words."""

QA = 'Queued.BackToBackCommandsOfTwoControllersOweTheirNoticesInOrder'
QC = 'Queued.TheOwedQueueIsBoundedAndHoldsTheNextRecordWhileFull'
QL = 'Queued.ALongerNoticeWaitsInTheResponseBufferBehindTheQueue'
QR = 'Queued.AQueuedNoticeResumesAtItsRecipient'
QD = 'Queued.AQueueTooDeepOrWithNoStorageIsRefused'
QF = 'Queued.BesideALongerNoticeTheQueuesGoesFrameByFrame'
ROUND = 'Core.HeldRetryWaitsForTheRoundAndTheRoundForAnOwedResponse'
NONE = 'Core.WithNoOwedSlotsTheNextRecordWaitsForTheNotice'
FIRST = 'Mailbox.ARoundBesideHeldWorkIsAQueuesFirstNoticeAlone'
TRANSMIT = 'return respond(a) || notices(a, drains);'
HEAD = '\t\t\tstruct aecp_owed *o = &a->cfg.owed[a->owed_head];\n'
READY = '(a->owed_count == 0u || a->owed_count < a->cfg.owed_slots)'

ROWS = (
    # the queue's storage: its tail wraps past the head's slot, its depth and storage are the integrator's, checked
    ('owed-tail-overwrites-the-head', 'aecp.c', 'tail < a->cfg.owed_slots ? tail : tail - a->cfg.owed_slots]',
     'tail < a->cfg.owed_slots ? tail : a->owed_head]',
     (QC, "the queue's tail wraps to its freed first slot, its notices in their order")),
    ('owed-depth-unbounded', 'aecp.c', 'cfg->owed_slots > 0xffu ||', '',
     (QD, '(c) a queue deeper than its 8-bit counts')),
    ('owed-slots-without-storage', 'aecp.c', '(cfg->owed_slots != 0u && cfg->owed == NULL) ||', '',
     (QD, '(c) slots with no storage')),
    # THE RETRY waits on the queue as on every other notice owed, and the queue's fan-out leaves a held notice whole
    ('owed-round-beside-the-queue', 'aecp.c',
     'return a->response_owed || a->notify || a->waiting || a->start_pending || a->owed_count != 0u;',
     'return a->response_owed || a->notify || a->waiting || a->start_pending;',
     (ROUND, 'the round waits while the owed-notice queue holds a notice')),
    ('owed-fan-over-the-held-notice', 'aecp.c', 'a->notify ? NULL : a->response)', 'a->response)',
     (QF, "the queue's frame by frame, the long notice's two through the fan port")),
    # (a) per-controller order FIFO, each recipient its notice once at its next sequence_id
    ('owed-newest-first', 'aecp.c', HEAD, HEAD.replace('a->owed_head]', 'a->owed_head + a->owed_count - 1u]'),
     (QA, '(a) in the order their commands were taken')),
    ('owed-requester-forgotten', 'aecp.c', '\to->requester = a->requester;\n', '\to->requester = 0u;\n',
     (QA, '(a) two notices, each to the two registered controllers not its requester')),
    ('owed-walk-restarts', 'aecp.c', '\t\t\tif (!fan_out(a, o->frame,',
     '\t\t\ta->owed_recipient = 0u;\n\t\t\tif (!fan_out(a, o->frame,',
     (QR, '(a) the walk resumes at the recipient it stopped at')),
    ('owed-long-notice-before-the-queue', 'aecp.c', '\tif (a->owed_count != 0u) {\n\t\tif (drains) {',
     '\tif (a->owed_count != 0u && !a->notify) {\n\t\tif (drains) {',
     (QL, "(a) the queue's notice first, then the long one")),
    # (b) a command's response before the notices it causes, and no notice in a record's turn
    ('owed-notice-before-its-response', 'aecp.c', TRANSMIT, 'return notices(a, drains) || respond(a);',
     (QA, "(b) each response is committed in its record's turn, and no notice yet")),
    ('owed-drained-in-the-records-turn', 'aecp.c', '\t\t(void)transmit(a, false);\n', '\t\t(void)transmit(a, true);\n',
     (QA, "(b) each response is committed in its record's turn, and no notice yet")),
    # (c) bounded, AECP not ready while it is full, a slot freed as its notice ends, a long notice not queued
    ('owed-ready-while-full', 'aecp.c', READY, 'true', (QC, '(c) AECP is not ready while the queue is full')),
    ('owed-never-ready-without-slots', 'aecp.c', READY, '(a->owed_count < a->cfg.owed_slots)',
     (NONE, 'command produces a response')),
    ('owed-slot-never-freed', 'aecp.c', '\t\t\t\t--a->owed_count;\n', '',
     (QC, '(c) its slot free, AECP is ready again')),
    ('owed-long-notice-queued', 'aecp.c', ' || a->response_bytes > AECP_OWED_BYTES) {', ') {',
     (QL, "its response waits for the poll, as every notice's did")),
    ('owed-not-queued', 'aecp.c', "(!a->notify || owe(a))", "(!a->notify || (false && owe(a)))",
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
