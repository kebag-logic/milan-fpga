# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@tsn_gen @item10 @cmd:CLOCK_SOURCE @matrix:CMD-11
Feature: Item-10 GET/SET_CLOCK_SOURCE - getter/setter round-trip (paired fixture)
  The paired fixture (docs/testing/PDU_GETTER_SETTER_VERIFICATION.md, class 3):
  the getter must REFLECT the setter. GET_CLOCK_SOURCE and SET_CLOCK_SOURCE share
  the wire layout (both carry clock_source_index), so the GET frame is the SET
  frame with command_type patched to 18 (GET) vs 22 (SET). Frames are tsn_gen-
  generated + decode-cross-checked; the Milan AECP model mirrors
  KL_aecp_response_builder (the RTL itself is verified by tb/verilator/aecp).

  Background:
    Given the tsn_gen packet generator is available
    And a fresh Milan AECP model

  @class:getter
  Scenario: GET_CLOCK_SOURCE returns the current source, well-formed
    Given tsn_gen generated a SET_CLOCK_SOURCE frame with seed 10
    When I patch field "message_type" to 0
    And I patch field "command_type" to 23
    And I patch field "descriptor_type" to 0x24
    And I patch field "descriptor_index" to 0
    Then tsn_gen decodes every patched field back
    And our field extractor agrees with tsn_gen on every field
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model clock_source_index is 0

  @class:paired
  Scenario: the getter reflects the setter (SET then GET round-trip)
    Given tsn_gen generated a SET_CLOCK_SOURCE frame with seed 2
    When I patch field "message_type" to 0
    And I patch field "command_type" to 22
    And I patch field "descriptor_type" to 0x24
    And I patch field "descriptor_index" to 0
    And I patch field "clock_source_index" to 1
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model clock_source_index is 1
    Given tsn_gen generated a SET_CLOCK_SOURCE frame with seed 11
    When I patch field "message_type" to 0
    And I patch field "command_type" to 23
    And I patch field "descriptor_type" to 0x24
    And I patch field "descriptor_index" to 0
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model clock_source_index is 1

  @class:getter @negative
  Scenario: GET_CLOCK_SOURCE on a non-CLOCK_DOMAIN descriptor is refused
    Given tsn_gen generated a SET_CLOCK_SOURCE frame with seed 12
    When I patch field "message_type" to 0
    And I patch field "command_type" to 23
    And I patch field "descriptor_type" to 0x00
    And I patch field "descriptor_index" to 0
    When the Milan AECP model processes the frame
    Then the model responds status 2
