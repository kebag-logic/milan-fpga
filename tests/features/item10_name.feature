# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@tsn_gen @item10 @cmd:NAME @matrix:CMD-16
Feature: Item-10 GET/SET_NAME - getter/setter round-trip (paired)
  Paired fixture (docs/testing/PDU_GETTER_SETTER_VERIFICATION.md, class 3) for the AVDECC
  object name. GET_NAME (0x0011) shares the SET_NAME (0x0010) wire layout, so the GET frame
  is the SET frame with command_type patched. object_name is a 64-octet (512-bit) avdecc_string;
  the round-trip patches it to a distinctive sentinel and asserts the getter reflects the setter
  on the model's stored value. Frames are tsn_gen-generated; the Milan AECP model mirrors
  KL_aecp_response_builder.

  Background:
    Given the tsn_gen packet generator is available
    And a fresh Milan AECP model

  @class:getter
  Scenario: GET_NAME on the ENTITY descriptor is well-formed and read-only
    Given tsn_gen generated a SET_NAME frame with seed 50
    When I patch field "message_type" to 0
    And I patch field "command_type" to 17
    And I patch field "descriptor_type" to 0x0000
    And I patch field "descriptor_index" to 0
    And I patch field "name_index" to 0
    Then tsn_gen decodes every patched field back
    And our field extractor agrees with tsn_gen on every field
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model object_name is 0

  @class:paired
  Scenario: the getter reflects the setter (SET object_name then GET)
    Given tsn_gen generated a SET_NAME frame with seed 51
    When I patch field "message_type" to 0
    And I patch field "command_type" to 16
    And I patch field "descriptor_type" to 0x0000
    And I patch field "descriptor_index" to 0
    And I patch field "name_index" to 0
    And I patch field "name" to 12648430
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model object_name is 12648430
    Given tsn_gen generated a SET_NAME frame with seed 52
    When I patch field "message_type" to 0
    And I patch field "command_type" to 17
    And I patch field "descriptor_type" to 0x0000
    And I patch field "descriptor_index" to 0
    And I patch field "name_index" to 0
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model object_name is 12648430

  @class:getter @negative
  Scenario: GET_NAME on an unknown descriptor_type is refused
    Given tsn_gen generated a SET_NAME frame with seed 53
    When I patch field "message_type" to 0
    And I patch field "command_type" to 17
    And I patch field "descriptor_type" to 0x00FF
    And I patch field "descriptor_index" to 0
    And I patch field "name_index" to 0
    When the Milan AECP model processes the frame
    Then the model responds status 2
