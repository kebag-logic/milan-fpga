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

  Scenario: the registration table and its four push queues exist
    Given the AECP response builder RTL
    Then REGISTER and DEREGISTER_UNSOLICITED_NOTIFICATION are handled
    And a push is owed for stream info, counters, interface counters and SET replay

  Scenario: a STREAM_INPUT counter change is rate limited per Milan 5.4.5
    # "unsolicited GET_COUNTERS only when a counter changed, at most once per
    # second per descriptor" - the rate limit is PER DESCRIPTOR, which is why
    # a single shared limiter cannot be conformant on a multi-sink shape.
    Given the AECP response builder RTL
    Then the STREAM_INPUT counter push is gated on a changed counter
    And the STREAM_INPUT counter push is rate limited to one per second

  @wip
  Scenario: EVERY stream input can raise an unsolicited counter push
    # THE DEFECT this file exists for. The dirty pulse and its rate limiter
    # are scalars named in0_*, fed by ONE monitor output, so sinks 1..N-1 can
    # change counters forever and no notification is ever generated for them.
    # The per-sink data is already there - the same monitor exposes
    # diag_idx_i/diag_cnt_o, "every sink's Table 5.6 set, muxed by the AECP's
    # GET_COUNTERS descriptor index" - so the fix is to widen the dirty flag
    # and the limiter to a per-sink vector and drive them from that mux.
    # Tagged @wip: it FAILS today on purpose and is the acceptance test for
    # the fix, not a passing assertion.
    Given the AECP response builder RTL
    Then the STREAM_INPUT dirty flag is per sink, not a single index-0 scalar
    And the STREAM_INPUT rate limiter is per sink, not a single index-0 scalar
