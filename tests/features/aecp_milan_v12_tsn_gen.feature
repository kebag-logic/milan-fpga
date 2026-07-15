# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@tsn_gen
Feature: Milan v1.2 AECP commands validated with tsn_gen frames
  The tsn-gen packet_gen binary (the AM65x-validation tool) generates the
  AECP PDUs from its protocol YAMLs; the tests patch fields bit-exactly and
  cross-check every patch through packet_gen --decode, then drive the Milan
  v1.2 semantic model that mirrors KL_aecp_response_builder (the RTL itself
  is verified by tb/verilator/aecp, 345 checks).

  Background:
    Given the tsn_gen packet generator is available
    And a fresh Milan AECP model

  Scenario: SET_CLOCK_SOURCE accept path — patched frame, decode-verified
    Given tsn_gen generated a SET_CLOCK_SOURCE frame with seed 2
    When I patch field "message_type" to 0
    And I patch field "status" to 0
    And I patch field "u" to 0
    And I patch field "descriptor_type" to 0x24
    And I patch field "descriptor_index" to 0
    And I patch field "clock_source_index" to 1
    Then tsn_gen decodes every patched field back
    And our field extractor agrees with tsn_gen on every field
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model clock_source_index is 1

  Scenario: SET_CLOCK_SOURCE out-of-range source is refused
    Given tsn_gen generated a SET_CLOCK_SOURCE frame with seed 3
    When I patch field "descriptor_type" to 0x24
    And I patch field "descriptor_index" to 0
    And I patch field "clock_source_index" to 3
    Then tsn_gen decodes every patched field back
    When the Milan AECP model processes the frame
    Then the model responds status 7
    And the model clock_source_index is 0

  Scenario: SET_CLOCK_SOURCE against a non-CLOCK_DOMAIN descriptor
    Given tsn_gen generated a SET_CLOCK_SOURCE frame with seed 5
    Then field "descriptor_type" equals 30
    When the Milan AECP model processes the frame
    Then the model responds status 2

  Scenario: the known tsn-gen CDL model deviation stays pinned
    # tsn-gen counts target_entity_id into control_data_length; the Milan
    # wire CDL for SET_CLOCK_SOURCE is 20 (silicon-diagnosed 2026-07:
    # never use tsn-gen as the CDL oracle)
    Given tsn_gen generated a SET_CLOCK_SOURCE frame with seed 1
    Then the tsn_gen control_data_length overshoots the Milan wire CDL 20 by 8

  Scenario: IDENTIFY control accepts only 0 and 255 (step-255 LINEAR_UINT8)
    Given tsn_gen generated a SET_CONTROL frame with seed 4
    When I patch field "message_type" to 0
    And I patch field "descriptor_type" to 0x1A
    And I patch field "descriptor_index" to 0
    And I patch field "control_values" to 0xFF00000000000000
    Then tsn_gen decodes every patched field back
    And our field extractor agrees with tsn_gen on every field
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model identify level is 255
    When I patch field "control_values" to 0x0700000000000000
    And the Milan AECP model processes the frame
    Then the model responds status 7
    And the model identify level is 255
    When I patch field "control_values" to 0
    And the Milan AECP model processes the frame
    Then the model responds status 0
    And the model identify level is 0

  Scenario: seeded fuzz — no illegal clock-source write is ever accepted
    When the model processes 25 SET_CLOCK_SOURCE frames from seeds 100 to 124
    Then every SUCCESS was a valid CLOCK_DOMAIN write and nothing else mutated state
