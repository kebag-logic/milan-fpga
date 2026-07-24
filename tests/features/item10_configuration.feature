# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@tsn_gen @item10 @cmd:CONFIGURATION @matrix:CMD-6
Feature: Item-10 GET/SET_CONFIGURATION - getter/setter round-trip (paired)
  Paired fixture (docs/testing/PDU_GETTER_SETTER_VERIFICATION.md, class 3) for the entity-
  level current configuration. GET_CONFIGURATION (0x0007) shares the SET_CONFIGURATION
  (0x0006) wire layout, so the GET frame is the SET frame with command_type patched. Frames
  are tsn_gen-generated; the Milan AECP model mirrors KL_aecp_response_builder.

  Background:
    Given the tsn_gen packet generator is available
    And a fresh Milan AECP model

  @class:getter
  Scenario: GET_CONFIGURATION returns the current configuration_index, well-formed
    Given tsn_gen generated a SET_CONFIGURATION frame with seed 30
    When I patch field "message_type" to 0
    And I patch field "command_type" to 7
    Then tsn_gen decodes every patched field back
    And our field extractor agrees with tsn_gen on every field
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model configuration_index is 0

  @class:paired
  Scenario: the getter reflects the setter (SET configuration 2 then GET)
    Given tsn_gen generated a SET_CONFIGURATION frame with seed 31
    When I patch field "message_type" to 0
    And I patch field "command_type" to 6
    And I patch field "configuration_index" to 2
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model configuration_index is 2
    Given tsn_gen generated a SET_CONFIGURATION frame with seed 32
    When I patch field "message_type" to 0
    And I patch field "command_type" to 7
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model configuration_index is 2

  @class:setter @negative
  Scenario: SET_CONFIGURATION out-of-range is refused, configuration unchanged
    Given tsn_gen generated a SET_CONFIGURATION frame with seed 33
    When I patch field "message_type" to 0
    And I patch field "command_type" to 6
    And I patch field "configuration_index" to 9
    When the Milan AECP model processes the frame
    Then the model responds status 7
    And the model configuration_index is 0
