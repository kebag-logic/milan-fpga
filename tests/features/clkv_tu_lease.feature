# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# The AVTP "tu" (timestamp uncertain) bit: the FABRIC VERDICT
# (KL_ptp_clock_validity) and the SOFTWARE LEASE POLICY that feeds it
# (gptp2csr.sh writing CLKV_CTRL 0x778), modelled offline.
#
# WHY THIS FEATURE EXISTS (measured 2026-07-28, both boards at VERSION
# 0x0001_0016).  CLKV_STAT read 0x00000005 on BOTH boards - tu asserted, no
# live lease, sync never claimed - and CLKV_TUCNT climbed at exactly 1.00/s
# since boot, i.e. tu was set in 100 % of observation intervals.  Meanwhile
# the ALINX was a healthy grandmaster (portState MASTER, gmIdentity == its
# own clockIdentity) and the Arty was SLAVE at master_offset -93 ns.  Two
# perfectly synchronised boards were telling every listener that their
# presentation timestamps could not be trusted, because NOTHING on either
# board ever wrote CLKV_CTRL.
#
# The RTL was right.  Reset tu = 1 is deliberate ("unknown clock state means
# NOT valid") and the 0x778 group exists precisely so software can lease the
# claim.  The gap was the lease WRITER, and this feature pins both halves so
# neither can regress:
#   * the fabric verdict must stay fail-safe (no lease => tu = 1), and
#   * the daemon policy must actually claim when, and only when, the clock
#     really is disciplined.
#
# CLAUSE POSITION - the "reset it" half is as mandatory as the "set it" half:
#   IEEE 1722-2016 4.4.4.7   "When a Talker detects a discontinuity in gPTP
#                             time, it should set the tu ... field to one (1)
#                             ... Once the Talker has determined that the
#                             gPTP clock has returned to a normal state, the
#                             tu field should be reset to zero (0)."
#   IEEE 1722-2016 PICS AAF-10, status AAF:M (MANDATORY) -
#                             "Is the tu field set to zero (0) when gPTP time
#                             is stable?"
#   IEEE 1722-2016 PICS AVTP-15, status M -
#                             "Does the device support set/reset the value in
#                             the tu field as described?"
#   Milan v1.2 4.3.5.2        "A Talker PAAD shall set the AVTP 'tu' bit as
#                             described in [AVTP, Clause 4.4.4.7]" - promoting
#                             ALL of 4.4.4.7, both directions, to a shall.
#   Milan v1.2 4.4.2.3        A Listener PAAD SHOULD use the tu bit, and after
#                             it is RESET should free-wheel its media clock
#                             for an appropriate time - so a talker that never
#                             resets tu never lets a conformant listener leave
#                             free-wheel.
#   Milan v1.2 Annex B.1.1    "In case of a change of grandmaster, the tu bit
#                             shall be set to 1 for the duration of 0.25
#                             seconds."
#   Milan v1.2 Table 5.4      TIMESTAMP_UNCERTAIN "Incremented at the end of
#                             every observation interval during which the 'tu'
#                             bit has been set in any of the transmitted
#                             Stream Data AVTPDUs.  The duration of the
#                             observation interval ... shall be less than or
#                             equal to 1 second."
# Quoted from the copies in /home/alex/standards (1722-2016.pdf and
# Milan_Specification_Consolidated_v1.2_Final_Approved 20231130.pdf).
#
# The offset threshold is Milan's own number: v1.2 4.4.2.1 derives the
# Listener buffering requirement from "2 ms (maximum presentation time
# offset) + 125 us (timing uncertainty) + 1 us (gPTP accuracy)", so 1 us is
# the gPTP accuracy the rest of the specification assumes.

@clkv @tu @milan:4.3.5.2 @milan:4.4.2.3 @milan:B.1.1 @milan:Table5.4 @avtp:4.4.4.7 @pics:AAF-10 @pics:AVTP-15
Feature: AVTP tu bit - fabric verdict and the gPTP sync lease

  Background:
    Given a clock-validity engine with a 4-quarter-tick observation interval

  # ---------------------------------------------------------------------
  # The fabric verdict: fail-safe, and the mutation anchor for the whole
  # feature.  A build that hard-wires tu = 0 fails the first scenario; a
  # build that hard-wires tu = 1 fails "a stable clock resets tu to zero".
  # ---------------------------------------------------------------------
  @fabric
  Scenario: unknown clock state is NOT valid - reset asserts tu
    When nothing has ever written CLKV_CTRL
    Then the tu bit is 1
    And CLKV_STAT reports no live lease
    And CLKV_STAT reports sync_ok clear

  @fabric @pics:AAF-10
  Scenario: a stable clock resets tu to zero - IEEE 1722-2016 PICS AAF-10 is MANDATORY
    When software leases the sync claim with sync_ok 1 and a lease of 8 quarter-seconds
    Then the tu bit is 0
    And CLKV_STAT reports sync_ok set

  @fabric
  Scenario: sync_ok with a zero lease is a legal way to say "never trust me"
    When software leases the sync claim with sync_ok 1 and a lease of 0 quarter-seconds
    Then the tu bit is 1
    And CLKV_STAT reports no live lease

  @fabric
  Scenario: a claim nobody renews lapses - the watchdog, not a flag
    When software leases the sync claim with sync_ok 1 and a lease of 4 quarter-seconds
    And the tu bit is 0
    And 5 quarter-ticks elapse with no further CLKV_CTRL write
    Then the tu bit is 1
    And CLKV_STAT reports no live lease

  @fabric
  Scenario: a daemon that keeps renewing keeps the claim alive
    When software renews a 4-quarter-second lease every 2 quarter-ticks for 20 quarter-ticks
    Then the tu bit is 0

  @fabric @milan:B.1.1
  Scenario: a grandmaster change holds tu for at least 0.25 s
    Given software holds a long-lived sync claim
    When the published grandmaster identity changes to 0x020000FFFE000001
    Then the tu bit is 1
    And tu stays asserted for at least 1 quarter-tick

  @fabric @avtp:4.4.4.7
  Scenario Outline: a PHC step is a gPTP discontinuity the fabric sees for itself
    Given software holds a long-lived sync claim
    When the fabric observes a <event>
    Then the tu bit is 1
    And CLKV_STAT reports a holdover in progress

    Examples:
      | event    |
      | settime  |
      | adjtime  |

  # ---------------------------------------------------------------------
  # Milan Table 5.4 TIMESTAMP_UNCERTAIN - the shape of the counter is the
  # test (R4): a per-frame bit measured per observation interval.
  # ---------------------------------------------------------------------
  @fabric @milan:Table5.4
  Scenario: TIMESTAMP_UNCERTAIN counts observation intervals, never frames
    Given software holds a long-lived sync claim
    When 40 quarter-ticks elapse
    Then CLKV_TUCNT did not move

  @fabric @milan:Table5.4
  Scenario: TIMESTAMP_UNCERTAIN advances once per interval while tu is set
    When nothing has ever written CLKV_CTRL
    And 40 quarter-ticks elapse
    Then CLKV_TUCNT advanced by 10

  # ---------------------------------------------------------------------
  # The software lease POLICY (gptp2csr.sh).  These are the checks that can
  # fail against a lazy fix: hardcoding sync_ok = 1 passes every scenario
  # above and fails every "refuses to claim" scenario below.
  # ---------------------------------------------------------------------
  @policy
  Scenario: a locked slave inside Milan's 1 us gPTP accuracy budget claims sync
    Given ptp4l reports portState SLAVE with a grandmaster present
    And the servo reports a master_offset of -93 ns
    Then the lease policy claims sync

  @policy
  Scenario: a slave adrift from the domain refuses to claim - the 2026-07-27 defect
    Given ptp4l reports portState SLAVE with a grandmaster present
    And the servo reports a master_offset of 216446000000000 ns
    Then the lease policy refuses to claim
    And the reason mentions the offset

  @policy
  Scenario Outline: an offset outside Milan 4.4.2.1's 1 us budget refuses to claim
    Given ptp4l reports portState SLAVE with a grandmaster present
    And the servo reports a master_offset of <offset> ns
    Then the lease policy <verdict>

    Examples:
      | offset | verdict         |
      | 999    | claims sync     |
      | 1000   | claims sync     |
      | 1001   | refuses to claim |
      | -1500  | refuses to claim |

  @policy
  Scenario: the grandmaster itself claims sync - its PHC defines gPTP time
    Given ptp4l reports portState MASTER with no grandmaster present
    And the reported grandmaster identity is our own clockIdentity
    Then the lease policy claims sync

  @policy
  Scenario: a port that has not finished BMCA is not a grandmaster
    Given ptp4l reports portState LISTENING with no grandmaster present
    Then the lease policy refuses to claim

  @policy
  Scenario: a dead ptp4l fails CLOSED
    Given pmc returns nothing at all
    Then the lease policy refuses to claim

  @policy
  Scenario: claiming health is harder than losing it
    Given ptp4l reports portState SLAVE with a grandmaster present
    And the servo reports a master_offset of -93 ns
    When the policy has seen 1 consecutive good sample
    Then the lease policy refuses to claim
    When the policy has seen 3 consecutive good samples
    Then the lease policy claims sync
    When one bad sample arrives
    Then the lease policy refuses to claim

  # ---------------------------------------------------------------------
  # End to end: policy feeding the fabric, in both directions.  This is the
  # scenario that would have caught the defect on 2026-07-28.
  # ---------------------------------------------------------------------
  @policy @fabric
  Scenario: a healthy board drives tu to zero and stops counting
    Given ptp4l reports portState MASTER with no grandmaster present
    And the reported grandmaster identity is our own clockIdentity
    When the daemon runs for 24 quarter-ticks
    Then the tu bit is 0
    And CLKV_TUCNT did not move over the last 8 quarter-ticks

  @policy @fabric
  Scenario: killing the daemon returns tu to 1 without any write at all
    Given ptp4l reports portState MASTER with no grandmaster present
    And the reported grandmaster identity is our own clockIdentity
    When the daemon runs for 24 quarter-ticks
    And the daemon is killed
    And 40 quarter-ticks elapse
    Then the tu bit is 1
    And CLKV_STAT reports no live lease
    And CLKV_TUCNT advanced over the last 8 quarter-ticks
