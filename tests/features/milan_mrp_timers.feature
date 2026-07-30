# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Milan v1.2 4.2.7.1.1 (Table 4.3, MRP Timer Tolerances and Default Values)
# and 4.2.7.2.2 (Instantaneous transition from IN to MT).
#
# WHY THIS FILE EXISTS. Our lwSRP implemented the IEEE 802.1Q-2018 Table 10-7
# BASE timers - JoinTime 20 cs, LeaveTime 60-100 cs, LeaveAllTime 1000 cs -
# and the package comment said exactly that, so nothing looked wrong. Milan
# OVERRIDES that table for a PAAD, and its LeaveTime floor is 4500 ms: our
# 600 ms sat a factor of ~8 below it, and no test in this repo asserted an MRP
# timer at all. The gap was found on 2026-07-30 by an independently written
# conformance lane; these scenarios are the standing guard so it cannot come
# back.
#
# The values are READ FROM THE RTL, never transcribed: a Python literal
# mirroring a package constant agrees with it on the day it is written and
# then drifts in silence, which is precisely how the original defect hid.
@class:structure @matrix:M-SRP-MRP
Feature: MRP timers follow Milan's table, not the 802.1Q base defaults

  Scenario: the MRP timers are inside Milan Table 4.3
    Given the MRP timers the lwSRP package elaborates
    # Table 4.3: joinTime 200 ms (180..240), LeaveTime 5000 ms (4500..7500),
    # leavealltimer 10-15 s (9500..15500).
    Then the JoinTime is between 180 and 240 ms
    And the LeaveTime is between 4500 and 7500 ms
    And the LeaveAll time is between 9500 and 15500 ms

  Scenario: an explicit MSRP Leave deregisters at once, with no LeaveTime wait
    # 4.2.7.2.2 replaces the 802.1Q Table 10-4 registrar transition
    #   IN / rLv! -> (Start leavetimer) -> LV
    # with
    #   IN / rLv! -> (Lv) -> MT
    # and the clause's own Note says why: it "allows the PAAD to use a value
    # of 5 seconds for the LeaveTime without requiring 5 seconds to detect
    # that a Stream has been explicitly withdrawn". So the two halves are one
    # change: raising LeaveTime without this would make a withdrawal take 5 s
    # to notice, and making this change without raising LeaveTime leaves the
    # timer nonconformant. Both are asserted here.
    Given an MSRP Registrar is in state IN
    When an MSRP Leave event is received
    Then the Registrar deregisters immediately
    And the explicit-Leave path does not arm the LeaveTime timer
    And no per-lane Registrar arms the LeaveTime timer on an explicit Leave
