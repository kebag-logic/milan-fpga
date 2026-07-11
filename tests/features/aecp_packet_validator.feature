# SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# BDD feature: KL_aecp_packet_validator
# Spec refs: IEEE 1722.1-2021 §9.2.1; aem-aecp.md §3.2.1
# Tier: T1 (Verilator + behave)

Feature: KL_aecp_packet_validator — AECP frame admission control

  Background:
    Given the DUT is KL_aecp_packet_validator
    And the DUT is reset
    And the AECP protocol directory is "/home/alex/tsn-gen/protocols"

  Scenario: Valid AEM_COMMAND with minimum CDL is accepted
    When I send an AECP frame with message_type 0 and control_data_length 20
    Then valid_o pulses once on tlast
    And drop_o remains low
    And status_o is 0

  Scenario: Valid VENDOR_UNIQUE_COMMAND (message_type 6) is accepted
    When I send an AECP frame with message_type 6 and control_data_length 24
    Then valid_o pulses once on tlast
    And drop_o remains low

  Scenario Outline: Invalid message_type causes drop with INVALID_COMMAND
    When I send an AECP frame with message_type <msg_type> and control_data_length 20
    Then drop_o pulses once on tlast
    And valid_o remains low
    And status_o is 10

    Examples:
      | msg_type |
      | 2        |
      | 3        |
      | 4        |
      | 5        |

  Scenario: CDL below minimum causes drop with BAD_ARGUMENTS
    When I send an AECP frame with message_type 0 and control_data_length 15
    Then drop_o pulses once on tlast
    And status_o is 7

  Scenario: Non-zero status in incoming AEM_COMMAND causes drop
    When I send an AECP frame with message_type 0 and control_data_length 20 and incoming_status 5
    Then drop_o pulses once on tlast
    And status_o is 11

  Scenario: 100 random valid packets are all accepted
    When I send 100 valid AECP AEM_COMMAND frames with seed 40
    Then all 100 frames produce valid_o pulses
    And no frame produces drop_o

  Scenario: 50 random invalid-msgtype packets are all dropped
    When I send 50 AECP frames with random invalid message_type and seed 41
    Then all 50 frames produce drop_o pulses
    And status_o is 10 for each

  Scenario: Back-pressure from m_axis does not corrupt classification
    Given m_axis.tready is held low for 5 cycles between beats
    When I send an AECP frame with message_type 0 and control_data_length 20
    Then valid_o pulses once on tlast
    And drop_o remains low
