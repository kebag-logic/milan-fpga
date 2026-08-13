# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Milan v1.2 §4.3.4 (FQTSS), §4.4 (Listener)
# 802.1Q-2022 §34 (FQTSS/CBS), §6.9.3 (PCP -> traffic class)
# Offline model: tests/steps/milan_8021q_steps.py
# Constants sourced from:
#   hdl/common/ethernet_packet_pkg.sv   (queue count, idle slopes, hi/lo credit)
#   hdl/ieee8021q/ts/credit_based_shaper.sv  (CBS algorithm)
#   hdl/ieee8021q/ts/traffic_class_map.sv     (PCP->TC->queue)
#
# The MRP/MSRP/MVRP, Talker-Advertise-eligibility, Milan TSpec and Σ-slope
# admission scenarios that used to live here were resolved out of the lwSRP
# RTL (hdl/ieee8021q/srp/**), which no longer exists in this repository: the
# protocol-processor submodule owns SRP now. They were deleted rather than
# retargeted at a model with nothing behind it.

@milan_conformance @8021q
Feature: Milan 802.1Q VLAN classification and CBS shaping

  Milan v1.2 mandates specific 802.1Q behaviours for PAAD end-stations:
  - 5 egress queues in 802.1Q priority order (q4 = highest)
  - PCP 3 maps to SR class A (q4) for tagged AVTP frames
  - CBS shapes SR class A (q4) and class B (q3)
  - idleSlope sum ≤ 75% of port rate (REQ-CBS-03)
  - a listener accepts a stream only on its own VID and channel count

  Background:
    Given a fresh 802.1Q conformance model

  # === §34.5 / ethernet_packet_pkg.sv: Queue architecture ===

  Scenario: there are exactly 5 egress queues in 802.1Q priority order
    Then the number of queues is 5
    And queue 4 is the highest priority
    And queue 0 is the lowest priority

  Scenario: SR class A maps to queue 4
    Then SR class A is on queue 4

  Scenario: SR class B maps to queue 3
    Then SR class B is on queue 3

  # === PCP -> TC -> Queue mapping (§6.9.3 / traffic_class_map.sv) ===

  Scenario: PCP 3 (SR class A) maps to queue 4
    When a tagged frame arrives with PCP 3
    Then the frame is classified to queue 4

  Scenario: PCP 2 (SR class B) maps to queue 3
    When a tagged frame arrives with PCP 2
    Then the frame is classified to queue 3

  Scenario: an untagged control frame uses the default port priority
    When an untagged frame arrives
    Then the frame uses the default port priority for classification

  Scenario: a reserved-DMAC control frame is classified by the DMAC table
    When a control frame with reserved DMAC arrives
    Then the frame is classified by the DMAC table with no EtherType precondition

  # === §34.6 / credit_based_shaper.sv: CBS algorithm ===

  Scenario: the CBS credit accrues at idleSlope while the queue waits
    Given the CBS shaper for queue 4 is enabled
    And the queue has data but transmission is not occurring
    Then the credit is increasing at the idleSlope rate

  Scenario: the CBS credit drains at sendSlope during transmission
    Given the CBS shaper for queue 4 is enabled
    And the queue is transmitting
    Then the credit is decreasing at the sendSlope rate
    And the sendSlope equals idleSlope minus portRate

  Scenario: transmission is allowed only when credit is non-negative
    Given the CBS shaper for queue 4 is enabled
    And the credit is negative
    Then transmission is blocked

  Scenario: transmission is allowed when credit is non-negative
    Given the CBS shaper for queue 4 is enabled
    And the credit is zero
    Then transmission is allowed

  Scenario: credit is clamped to the hiCredit upper bound
    Given the CBS shaper for queue 4 is enabled
    When the credit exceeds hiCredit
    Then the credit is clamped to hiCredit

  Scenario: credit is clamped to the loCredit lower bound
    Given the CBS shaper for queue 4 is enabled
    When the credit drops below loCredit
    Then the credit is clamped to loCredit

  Scenario: an unshaped queue (strict priority) always allows transmission
    Given the CBS shaper for queue 0 is disabled
    Then transmission is always allowed
    And the credit is parked at 0

  # === §34.3 / Milan §4.3.4: idleSlope budgets ===

  Scenario: the shaped idleSlope sum is below 75 percent at 1 Gbit/s
    Given the port rate is 1000000000 bits per second
    Then queue 4 idleSlope is 450000000 bits per second
    And queue 3 idleSlope is 150000000 bits per second
    And the shaped idleSlope sum is at most 75 percent of port rate

  Scenario: the shaped idleSlope sum is below 75 percent at 100 Mbit/s
    Given the port rate is 100000000 bits per second
    Then queue 4 idleSlope is 45000000 bits per second
    And queue 3 idleSlope is 15000000 bits per second
    And the shaped idleSlope sum is at most 75 percent of port rate

  Scenario: hiCredit follows maxInterferenceSize times idleSlope over portRate
    Given the port rate is 1000000000 bits per second
    And queue 4 has idleSlope 450000000 bits per second
    When hiCredit is calculated for a 1522 byte interfering frame
    Then hiCredit equals 684 bytes

  Scenario: loCredit follows maxFrameSize times sendSlope over portRate
    Given the port rate is 1000000000 bits per second
    And queue 4 has idleSlope 450000000 bits per second
    When loCredit is calculated for a 1522 byte frame
    Then loCredit equals -837 bytes

  # === VLAN and stream filtering ===

  Scenario: a tagged AVTP frame on the configured VID and format is accepted
    Given the listener is configured for VID 2 and 4-channel AAF
    When a tagged AVTP frame arrives on VID 2 with 4 channels
    Then the listener accepts the AVTP frame

  Scenario: an AVTP frame on the wrong VID is discarded
    Given the listener is configured for VID 2 and 4-channel AAF
    When a tagged AVTP frame arrives on VID 3 with 4 channels
    Then the listener discards the AVTP frame

  Scenario: an AVTP frame with the wrong channel count is discarded
    Given the listener is configured for VID 2 and 4-channel AAF
    When a tagged AVTP frame arrives on VID 2 with 2 channels
    Then the listener discards the AVTP frame

  Scenario: VID zero is not treated as the configured SR VLAN
    Given the listener is configured for VID 2 and 4-channel AAF
    When a tagged AVTP frame arrives on VID 0 with 4 channels
    Then the listener discards the AVTP frame
