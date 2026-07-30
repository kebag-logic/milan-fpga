# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Milan v1.2 §4.2.7 (MRP/MSRP/MVRP), §4.3.3 (Talker MSRP), §4.3.4 (FQTSS),
# §4.4 (Listener), §4.3.5.1 (MAAP)
# 802.1Q-2022 §34 (FQTSS/CBS), §35 (SRP/MVRP)
# Offline model: tests/steps/milan_8021q_steps.py
# Constants sourced from:
#   hdl/common/ethernet_packet_pkg.sv   (queue count, idle slopes, hi/lo credit)
#   hdl/ieee8021q/ts/credit_based_shaper.sv  (CBS algorithm)
#   hdl/ieee8021q/ts/traffic_class_map.sv     (PCP->TC->queue)
#   hdl/ieee8021q/srp/lwsrp_pkg.sv            (SR class, timers, bandwidth)
#   hdl/ieee8021q/srp/KL_lwsrp_bw_gate.sv     (Σ-slope gate)

@milan_conformance @8021q
Feature: Milan 802.1Q VLAN classification, CBS shaping, and SRP bandwidth

  Milan v1.2 mandates specific 802.1Q behaviours for PAAD end-stations:
  - 5 egress queues in 802.1Q priority order (q4 = highest)
  - PCP 3 maps to SR class A (q4) for tagged AVTP frames
  - CBS shapes SR class A (q4) and class B (q3)
  - idleSlope sum ≤ 75% of port rate (REQ-CBS-03)
  - MRP timers: join=200ms, leave=600ms (Milan relaxes to instant IN→MT),
    leaveall=10-15s
  - MSRP Domain: SR class ID 6, priority 3, VID 2
  - MVRP: listener declares VID for settled sinks
  - MAAP: one contiguous block claim, DMAC = base + stream_index

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

  # === Milan §4.2.7.1: MRP timing and malformed messages ===

  Scenario: the MRP periodic timer is within the Milan tolerance
    Then the MRP periodic timer is between 900 and 1500 ms

  Scenario: the MRP JoinTime is within the Milan tolerance
    Then the MRP JoinTime is between 180 and 240 ms

  @open-finding
  Scenario: the MRP LeaveTime matches the Milan default tolerance
    Then the RTL MRP LeaveTime is between 4500 and 7500 ms

  Scenario: the MRP LeaveAll timer is within the Milan tolerance
    Then the MRP LeaveAll timer is between 9500 and 15500 ms

  Scenario: an invalid vector discards the remainder of its list and subsequent messages
    Given an MRPDU with a valid vector followed by an invalid vector
    When the MRPDU is parsed
    Then information before the invalid vector is retained
    And information after the invalid vector is discarded
    And subsequent messages in the same MRPDU are discarded

  Scenario: a padded MRPDU uses a 0x0000 EndMark
    Given an MRPDU that requires Ethernet padding
    When the MRPDU is serialized
    Then the EndMark is 0x0000 before the padding

  # === Milan §4.2.7.2: MSRP Domain declaration ===

  Scenario: the default MSRP Domain is class A priority 3 on VID 2
    When the MSRP Domain is reset to Milan defaults
    Then the MSRP Domain class ID is 6
    And the MSRP Domain priority is 3
    And the MSRP Domain VID is 2

  Scenario: a received Domain declaration updates all three parameters atomically
    Given the MSRP Domain is class ID 6 priority 3 VID 2
    When a Domain declaration is received with class ID 6 priority 4 VID 3
    Then the MSRP Domain class ID is 6
    And the MSRP Domain priority is 4
    And the MSRP Domain VID is 3
    And the next Domain declaration matches the received FirstValue

  Scenario: Domain declaration is independent of gPTP lock state
    Given gPTP is not locked
    When the MSRP Domain declaration timer expires
    Then an MSRP Domain declaration is transmitted

  Scenario: MSRP Leave causes an instantaneous IN to MT transition
    Given an MSRP Registrar is in state IN
    When an MSRP Leave event is received
    Then the MSRP Registrar state is MT
    And no LeaveTime wait is required

  # === Milan §4.2.7.3 and §4.4.1: MVRP ===

  Scenario: a settled listener sink declares its Stream VLAN through MVRP
    Given a listener sink is settled on VLAN 2
    When the MVRP applicant is evaluated
    Then VID 2 is declared

  Scenario: unbinding the last sink withdraws the MVRP VID
    Given a listener sink is settled on VLAN 2
    And it is the last sink using VLAN 2
    When that listener sink is unbound
    Then VID 2 is withdrawn

  Scenario: another settled sink keeps the shared VID declared
    Given two listener sinks are settled on VLAN 2
    When one listener sink is unbound
    Then VID 2 remains declared

  # === Milan §4.3.3.1: Talker declaration eligibility ===

  Scenario: a talker declares only with a valid MAAP address and recent probe
    Given a talker has a conflict-free MAAP destination address
    And the talker received PROBE_TX 10 seconds ago
    Then the Talker Advertise attribute is eligible for declaration

  Scenario: a MAAP conflict prevents Talker Advertise declaration
    Given a talker has a conflicted MAAP destination address
    And the talker received PROBE_TX 10 seconds ago
    Then the Talker Advertise attribute is not eligible for declaration

  Scenario: a probe older than 15 seconds does not sustain declaration by itself
    Given a talker has a conflict-free MAAP destination address
    And the talker received PROBE_TX 16 seconds ago
    And no matching Listener attribute is registered
    Then the Talker Advertise attribute is not eligible for declaration

  Scenario: a matching Listener registration sustains declaration without a recent probe
    Given a talker has a conflict-free MAAP destination address
    And the talker received PROBE_TX 16 seconds ago
    And a matching Listener attribute is registered
    Then the Talker Advertise attribute is eligible for declaration

  # === Milan §4.3.3.2: TSpec and bandwidth ===

  @open-finding
  Scenario: a 2-channel PCM32 48 kHz stream uses the Milan MaxFrameSize
    When Milan TSpec is calculated for PCM32 48 kHz 2 channels
    Then MaxFrameSize is 73 bytes
    And MaxIntervalFrames is 1
    And reserved bandwidth is 7360 kbps

  Scenario: a CRF stream with one timestamp per PDU uses the Milan TSpec
    When Milan TSpec is calculated for CRF with 1 timestamp per PDU
    Then MaxFrameSize is 29 bytes
    And MaxIntervalFrames is 1
    And reserved bandwidth is 5632 kbps

  Scenario: wire bandwidth accounts for Ethernet header FCS preamble and IPG
    When wire bandwidth is calculated for MaxFrameSize 73 and MaxIntervalFrames 1
    Then the wire slot is 115 bytes
    And reserved bandwidth is 7360 kbps

  # === Σ-slope admission gate / KL_lwsrp_bw_gate.sv ===

  Scenario: streams are admitted in deterministic index order within the ceiling
    Given the port rate is 100000000 bits per second
    And the SRP bandwidth ceiling is 75 percent
    When stream slopes 20000000,20000000,20000000 are requested
    Then all 3 streams are admitted
    And the aggregate idleSlope is 60000000 bits per second

  Scenario: the first stream exceeding the 75 percent ceiling is refused
    Given the port rate is 100000000 bits per second
    And the SRP bandwidth ceiling is 75 percent
    When stream slopes 30000000,30000000,30000000 are requested
    Then streams 0 and 1 are admitted
    And stream 2 is refused
    And the aggregate idleSlope is 60000000 bits per second

  Scenario: withdrawing one stream releases its slope from the aggregate
    Given admitted stream slopes 30000000,30000000
    When stream 0 is withdrawn
    Then the aggregate idleSlope is 30000000 bits per second

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
