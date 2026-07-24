# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@tsn_gen @item10 @cmd:CONTROL @matrix:CMD-13
Feature: Item-10 GET/SET_CONTROL (IDENTIFY) - getter/setter round-trip (paired)
  Paired fixture (docs/testing/PDU_GETTER_SETTER_VERIFICATION.md, class 3) for the
  IDENTIFY CONTROL (LINEAR_UINT8, only 0/255 legal). GET_CONTROL (0x0019=25) shares
  the SET_CONTROL (0x0018=24) wire layout, so the GET frame is the SET frame with
  command_type patched. Frames are tsn_gen-generated; the Milan AECP model mirrors
  KL_aecp_response_builder (the RTL is verified by tb/verilator/aecp).

  Background:
    Given the tsn_gen packet generator is available
    And a fresh Milan AECP model

  @class:getter
  Scenario: GET_CONTROL returns the current IDENTIFY level, well-formed
    Given tsn_gen generated a SET_CONTROL frame with seed 20
    When I patch field "message_type" to 0
    And I patch field "command_type" to 25
    And I patch field "descriptor_type" to 0x1A
    And I patch field "descriptor_index" to 0
    Then tsn_gen decodes every patched field back
    And our field extractor agrees with tsn_gen on every field
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model identify level is 0

  @class:paired
  Scenario: the getter reflects the setter (SET IDENTIFY=255 then GET)
    Given tsn_gen generated a SET_CONTROL frame with seed 21
    When I patch field "message_type" to 0
    And I patch field "command_type" to 24
    And I patch field "descriptor_type" to 0x1A
    And I patch field "descriptor_index" to 0
    And I patch field "control_values" to 0xFF00000000000000
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model identify level is 255
    Given tsn_gen generated a SET_CONTROL frame with seed 22
    When I patch field "message_type" to 0
    And I patch field "command_type" to 25
    And I patch field "descriptor_type" to 0x1A
    And I patch field "descriptor_index" to 0
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model identify level is 255

  @class:setter @negative
  Scenario: SET_CONTROL with an out-of-range IDENTIFY value is refused
    Given tsn_gen generated a SET_CONTROL frame with seed 23
    When I patch field "message_type" to 0
    And I patch field "command_type" to 24
    And I patch field "descriptor_type" to 0x1A
    And I patch field "descriptor_index" to 0
    And I patch field "control_values" to 0x0100000000000000
    When the Milan AECP model processes the frame
    Then the model responds status 7
