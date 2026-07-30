# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Milan v1.2 §4.2.7.2 (MSRP Operation), §4.3.3 (Talker MSRP), §4.3.3.1
# 802.1Q-2022 §35.2.2.8 (MRPDU Domain attributes), §35.2.7 (MSRP attributes)
# Offline model: tests/steps/milan_conformance_steps.py
# The model mirrors hdl/ieee8021q/srp/KL_lwsrp_tx.sv (Domain TX) and
# hdl/ieee8021q/srp/lwsrp_pkg.sv (SR class, timers, bandwidth).

@milan_conformance @srp
Feature: Milan SRP default parameters and Domain declarations

  Milan v1.2 §4.2.7.2 requires the DUT to declare the MSRP Domain attribute
  with the correct SR class parameters. The lwSRP engine in fabric
  (KL_lwsrp_tx.sv) sends Domain MRPDUs on link-up and periodically.

  Key parameters verified (Milan v1.2 §4.2.7.2, 802.1Q Table 10-7):
  - SR Class ID = 6 (class A)
  - Priority = 3
  - Default VLAN ID = 2
  - JoinTime = 200 ms
  - LeaveTime = 600 ms
  - LeaveAllTime = 10_000 ms
  - First Domain MRPDU within 20 seconds of link-up
  - Domain MRPDU interval < 15.5 seconds (JoinMt cadence)

  Background:
    Given a fresh Milan SRP Domain model
    And the SR class is A
    And the SR class ID is 6
    And the SR priority is 3
    And the SR VLAN ID is 2

  # --- Domain attribute defaults (Test 1.2 offline analysis) ---

  Scenario: the Domain MRPDU carries the correct SR class parameters
    When the SRP engine transmits a Domain MRPDU
    Then the Domain MRPDU contains SR Class ID 6
    And the Domain MRPDU Priority is 3
    And the Domain MRPDU VLAN ID is 2

  Scenario: the first Domain MRPDU is sent within 20 seconds of link-up
    When the SRP engine starts from link-up
    Then the first Domain MRPDU is transmitted within 20 seconds

  Scenario: the Domain MRPDU interval does not exceed 15.5 seconds
    When the SRP engine transmits over a 90 second observation window
    Then the interval between consecutive Domain MRPDUs is at most 15.5 seconds
    And at least 2 Domain MRPDUs are transmitted in the window

  Scenario: the last Domain MRPDU is no more than 15.5 seconds before observation end
    When the SRP engine transmits over a 90 second observation window
    Then the last Domain MRPDU is within 15.5 seconds of the window end

  # --- MRP timer defaults (802.1Q Table 10-7, Milan §4.2.7.1) ---

  Scenario: the MRP timers are set to the 802.1Q defaults
    Then the JoinTime is 200 ms
    And the LeaveTime is 600 ms
    And the LeaveAllTime is 10000 ms

  # --- Bandwidth gate (Milan §4.3.3.2, 802.1Q §34.3) ---

  Scenario: the SR class A bandwidth limit is 75 percent of the port rate
    Then the SR class A bandwidth limit is 75 percent

  Scenario: a single 2-channel AAF stream reserves within the class-A ceiling
    Given a 2-channel AAF talker stream at 48 kHz
    When the SRP engine computes the TSpec
    Then the MaxFrameSize is 72
    And the MaxIntervalFrames is 1
    And the reserved bandwidth is at most 75 percent of the port rate

  Scenario: an 8-channel AAF stream on 1G has the correct TSpec
    Given an 8-channel AAF talker stream at 48 kHz
    When the SRP engine computes the TSpec
    Then the MaxFrameSize is 216
    And the MaxIntervalFrames is 1

  # --- LeaveAll (802.1Q §35.2.2.5) ---

  Scenario: a LeaveAll event causes the Domain to be re-declared
    When a LeaveAll timer expires
    Then the SRP engine transmits a Domain MRPDU with the LeaveAll event

  # --- Link down/up restores defaults (Test 1.2) ---

  Scenario: after a link down/up the Domain parameters are restored
    When the link goes down
    And the link comes back up
    Then the first Domain MRPDU after link-up carries SR Class ID 6
    And the Domain MRPDU Priority is 3
    And the Domain MRPDU VLAN ID is 2
