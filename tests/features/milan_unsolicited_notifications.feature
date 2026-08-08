# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Milan v1.2 5.4.2.21 + 5.4.5, IEEE 1722.1-2021 7.5.2 - unsolicited
# notifications. A controller REGISTERs once and is then TOLD when state
# changes; if we never push, it shows whatever it last polled, which reads to
# a user as "the counters do not work" even when the fabric is counting
# correctly. Found that way on 2026-07-30.
@class:structure @matrix:M-AECP-UNSOL
Feature: unsolicited notifications are pushed per descriptor, not just for index 0

  Scenario: the registration table and its push queues exist
    Given the AECP response builder RTL
    Then REGISTER and DEREGISTER_UNSOLICITED_NOTIFICATION are handled
    And a push is owed for stream info, input counters, interface counters and SET replay

  Scenario: a STREAM_INPUT counter change is rate limited per Milan 5.4.5
    # "unsolicited GET_COUNTERS only when a counter changed, at most once per
    # second per descriptor" - the rate limit is PER DESCRIPTOR, which is why
    # a single shared limiter cannot be conformant on a multi-sink shape.
    Given the AECP response builder RTL
    Then the STREAM_INPUT counter push is gated on a changed counter
    And the STREAM_INPUT counter push is rate limited to one per second

  Scenario: EVERY stream input can raise an unsolicited counter push
    # THE DEFECT this file existed for, closed by gh #60 F2/F3. The dirty
    # pulse and its rate limiter used to be scalars named in0_*, fed by ONE
    # monitor output, so sinks 1..N-1 could change counters forever and no
    # notification was ever generated for them. The fix is exactly the one
    # this scenario prescribed while it carried @wip: the dirty flag and the
    # limiter are per-sink vectors (the STREAM_OUTPUT idiom mirrored), fed by
    # the monitor's per-context dirty vector, and the push payload reads the
    # SAME diag_idx_i/diag_cnt_o mirror the solicited path serves - sink 0
    # included, so the push and the solicited answer can never disagree on a
    # descriptor again. The CRF Media Clock Input rides its own scalar class
    # at its own descriptor index.
    Given the AECP response builder RTL
    Then the STREAM_INPUT dirty flag is per sink, not a single index-0 scalar
    And the STREAM_INPUT rate limiter is per sink, not a single index-0 scalar
    And the CRF Media Clock Input has its own counter push class

  Scenario: the 60 s lock auto-expiry owes every registered controller a notification
    # Milan v1.2 5.4.2.2 note (gh #58 D4): "in case of automatic unlock by
    # the PAAD-AE itself after the 1-minute timeout period, an unsolicited
    # notification is sent to all registered controllers, and only to these
    # controllers." An EXPLICIT unlock by the owner notifies nobody - the
    # note names the automatic action alone - so the pulse must come off the
    # countdown and off nothing else.
    Given the AECP response builder RTL
    Then a push is owed for the lock auto-expiry
    And the lock expiry pulse fires only from the countdown
