# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# WHY THIS FEATURE EXISTS (measured on silicon, 2026-07-28, gateware 0x0001_0016).
#
# USER report: "when the device receive packet, the gPTP GM changed for no
# reason" (open defect D7). It had never been reproduced - a 25 s sample held
# steady - so there was no way to prove any fix.
#
# It reproduces DETERMINISTICALLY: a 60 s saturating unicast RX flood aimed at
# the grandmaster board. During the flood the ALINX grandmaster emits ZERO
# Announce and ZERO Sync - not late, ABSENT - because sustained ingress traffic
# starves time-sync processing. Every peer then loses the master and re-elects.
#
# THE RE-ELECTION IS NOT THE DEFECT. Losing a grandmaster that stopped
# announcing is exactly what IEEE 802.1AS-2020 REQUIRES (the
# PortAnnounceInformation state machine, ANNOUNCE_RECEIPT_TIMEOUT_EXPIRES,
# Clause 10.3; the timeout is announceReceiptTimeout x announceInterval and
# announceReceiptTimeout defaults to 3). The defect is UPSTREAM of the BMCA:
# the grandmaster stopped transmitting. So this feature pins BOTH halves -
# the required BMCA response, and the cadence budget that must hold for the
# BMCA never to be provoked in the first place.
#
# LEVEL / ORACLE (docs/testing/methodology.md): L3 conformance. The oracle is
# the clause for the BMCA scenarios, and MEASURED SILICON COUNTS for the
# cadence-budget scenarios - both a passing measurement and a failing one, so
# the check demonstrably can fail (R2).
#
# Intervals asserted here are the 802.1AS-2020 Clause 10.6 defaults, which are
# also what Milan v1.2 4.2.6.2 requires:
#   logAnnounceInterval 0  -> 1 Announce/s      announceReceiptTimeout 3 -> 3 s
#   logSyncInterval    -3  -> 8 Sync/s
#   logMinPdelayReqInterval 0 -> 1 Pdelay_Req/s

@gptp @bmca @clause:802.1AS-10.3 @clause:802.1AS-10.6 @defect:D7
Feature: gPTP grandmaster is not lost while the announce cadence holds

  A grandmaster change is only legitimate when the BMCA was given a reason.
  These scenarios separate "the BMCA did its job" from "our transmitter went
  silent and made the BMCA do its job".

  Background:
    Given a gPTP port with the 802.1AS default intervals

  # ----------------------------------------------------------------- BMCA --
  # Oracle: IEEE 802.1AS-2020 Clause 10.3 (PortAnnounceInformation /
  # ANNOUNCE_RECEIPT_TIMEOUT_EXPIRES). announceReceiptTimeoutTime =
  # announceReceiptTimeout (3) x announceInterval (1 s) = 3 s.

  Scenario: a grandmaster that keeps announcing is never displaced by a worse claimant
    Given grandmaster "020000fffe000001" with priority1 238
    And a competing claimant "3cc0c6fffefe0210" with priority1 246
    When the grandmaster announces every 1.0 s for 60 s
    Then the selected grandmaster is "020000fffe000001"
    And the grandmaster changed 0 times

  Scenario: an announce gap SHORTER than announceReceiptTimeout must NOT move the grandmaster
    # NEGATIVE CONTROL for the timeout itself. If this scenario also lost the
    # grandmaster, the model would be declaring loss on any gap at all and the
    # timeout scenario below would prove nothing.
    Given grandmaster "020000fffe000001" with priority1 238
    And a competing claimant "3cc0c6fffefe0210" with priority1 246
    When the grandmaster stops announcing for 2.0 s
    Then the selected grandmaster is "020000fffe000001"
    And the grandmaster changed 0 times

  Scenario: an announce gap of announceReceiptTimeout expires the master and re-elects
    # REQUIRED behaviour, not a defect - Clause 10.3.
    Given grandmaster "020000fffe000001" with priority1 238
    And a competing claimant "3cc0c6fffefe0210" with priority1 246
    When the grandmaster stops announcing for 3.0 s
    Then the selected grandmaster is "3cc0c6fffefe0210"
    And the grandmaster changed 1 times

  Scenario: the measured D7 flap - 60 s of silence, then automatic recovery
    # Replays what the bench measured on 2026-07-28: the ALINX emitted no
    # Announce for the whole 60 s flood, the segment re-elected the priority1
    # 246 device, and when the flood stopped the ALINX won BMCA again with no
    # operator action. Recovery MUST be automatic (USER rule, D9) - a scenario
    # that only checks the loss would let a non-recovering build pass.
    Given grandmaster "020000fffe000001" with priority1 238
    And a competing claimant "3cc0c6fffefe0210" with priority1 246
    When the grandmaster stops announcing for 60.0 s
    Then the selected grandmaster is "3cc0c6fffefe0210"
    When the grandmaster announces every 1.0 s for 10 s
    Then the selected grandmaster is "020000fffe000001"
    And the grandmaster changed 2 times

  # ------------------------------------------------------- cadence budget --
  # The wire-observable property that had no test: gPTP message intervals must
  # hold WHILE RX load runs. Counts below are real `pmc GET PORT_STATS_NP`
  # deltas taken on the bench, so these rows are measurements, not fixtures.

  Scenario Outline: the announce cadence budget over an observed window
    When <sent> Announce messages are observed over <window> s
    Then the announce cadence budget <verdict>

    # E1, 2026-07-28: 58 Mb/s TCP RX into the ALINX for 60 s. Announce held.
    # This is the row that proves the budget check does not just always fail.
    Examples: load the grandmaster survives
      | sent | window | verdict |
      | 105  | 93.27  | holds   |

    # E2, 2026-07-28: 935 Mb/s UDP RX flood into the ALINX for 60 s inside the
    # same window. 116 Announce where 183 were due - the 60 s flood contributed
    # essentially none. This is the row that proves the check can fail.
    Examples: load the grandmaster does not survive
      | sent | window | verdict |
      | 116  | 183.51 | breaks  |

  Scenario Outline: the sync cadence budget over an observed window
    When <sent> Sync messages are observed over <window> s
    Then the sync cadence budget <verdict>

    Examples: E1 nominal, E2 flood
      | sent | window | verdict |
      | 823  | 93.27  | holds   |
      | 917  | 183.51 | breaks  |

  Scenario Outline: the pdelay cadence budget over an observed window
    # Pdelay is the asCapable input: lose it long enough and the port leaves
    # the domain entirely (Clause 11.2 / AS-8), which moves the grandmaster
    # even when Announce is healthy.
    When <sent> Pdelay_Req messages are observed over <window> s
    Then the pdelay cadence budget <verdict>

    Examples: E1 nominal, E2 flood
      | sent | window | verdict |
      | 105  | 93.27  | holds   |
      | 117  | 183.51 | breaks  |
