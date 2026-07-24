# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@tsn_gen @item10 @cmd:SAMPLING_RATE @matrix:CMD-20
Feature: Item-10 GET/SET_SAMPLING_RATE - getter/setter round-trip (paired)
  Paired fixture (docs/testing/PDU_GETTER_SETTER_VERIFICATION.md, class 3) for the AUDIO_UNIT
  media sampling rate. GET_SAMPLING_RATE (0x0015) shares the SET_SAMPLING_RATE (0x0014) wire
  layout, so the GET frame is the SET frame with command_type patched. Frames are tsn_gen-
  generated; the Milan AECP model mirrors KL_aecp_response_builder.

  Background:
    Given the tsn_gen packet generator is available
    And a fresh Milan AECP model

  @class:getter
  Scenario: GET_SAMPLING_RATE returns the current rate (default 48 kHz), well-formed
    Given tsn_gen generated a SET_SAMPLING_RATE frame with seed 40
    When I patch field "message_type" to 0
    And I patch field "command_type" to 21
    And I patch field "descriptor_type" to 0x02
    And I patch field "descriptor_index" to 0
    Then tsn_gen decodes every patched field back
    And our field extractor agrees with tsn_gen on every field
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model sampling_rate is 48000

  @class:paired
  Scenario: the getter reflects the setter (SET 96 kHz then GET)
    Given tsn_gen generated a SET_SAMPLING_RATE frame with seed 41
    When I patch field "message_type" to 0
    And I patch field "command_type" to 20
    And I patch field "descriptor_type" to 0x02
    And I patch field "descriptor_index" to 0
    And I patch field "sampling_rate" to 96000
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model sampling_rate is 96000
    Given tsn_gen generated a SET_SAMPLING_RATE frame with seed 42
    When I patch field "message_type" to 0
    And I patch field "command_type" to 21
    And I patch field "descriptor_type" to 0x02
    And I patch field "descriptor_index" to 0
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model sampling_rate is 96000

  @class:setter @negative
  Scenario: SET_SAMPLING_RATE to an unsupported rate is refused, rate unchanged
    Given tsn_gen generated a SET_SAMPLING_RATE frame with seed 43
    When I patch field "message_type" to 0
    And I patch field "command_type" to 20
    And I patch field "descriptor_type" to 0x02
    And I patch field "descriptor_index" to 0
    And I patch field "sampling_rate" to 12345
    When the Milan AECP model processes the frame
    Then the model responds status 7
    And the model sampling_rate is 48000

  @class:getter @negative
  Scenario: GET_SAMPLING_RATE on a non-AUDIO_UNIT descriptor is refused
    Given tsn_gen generated a SET_SAMPLING_RATE frame with seed 44
    When I patch field "message_type" to 0
    And I patch field "command_type" to 21
    And I patch field "descriptor_type" to 0x00
    And I patch field "descriptor_index" to 0
    When the Milan AECP model processes the frame
    Then the model responds status 2
