# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@tsn_gen @item10 @cmd:STREAM_INFO @matrix:CMD-7
Feature: Item-10 GET/SET_STREAM_INFO - getter + Milan documented-partial setter
  Paired fixture (docs/testing/PDU_GETTER_SETTER_VERIFICATION.md, class 3) for STREAM_INFO.
  GET_STREAM_INFO (0x000F) shares the SET_STREAM_INFO (0x000E) wire layout, so the GET frame
  is the SET frame with command_type patched. The Milan SET is documented-partial (§5.4.2.9,
  traceability CMD-7 / es-4.5,4.6): unsupported on a Listener STREAM_INPUT, and on a Talker
  STREAM_OUTPUT only the MSRP_ACC_LAT sub-command is honoured - every other spec-defined flag
  is refused NOT_SUPPORTED. Frames are tsn_gen-generated; the Milan AECP model mirrors
  KL_aecp_response_builder (the flags word is 'msrp_flags' in the YAML, MSRP_ACC_LAT at bit 61).

  Background:
    Given the tsn_gen packet generator is available
    And a fresh Milan AECP model

  @class:getter
  Scenario: GET_STREAM_INFO on the Talker source[0] returns SUCCESS, well-formed
    Given tsn_gen generated a SET_STREAM_INFO frame with seed 60
    When I patch field "message_type" to 0
    And I patch field "command_type" to 15
    And I patch field "descriptor_type" to 0x06
    And I patch field "descriptor_index" to 0
    Then tsn_gen decodes every patched field back
    And our field extractor agrees with tsn_gen on every field
    When the Milan AECP model processes the frame
    Then the model responds status 0

  @class:setter @negative
  Scenario: SET_STREAM_INFO on a Listener STREAM_INPUT is refused NOT_SUPPORTED
    Given tsn_gen generated a SET_STREAM_INFO frame with seed 61
    When I patch field "message_type" to 0
    And I patch field "command_type" to 14
    And I patch field "descriptor_type" to 0x05
    And I patch field "descriptor_index" to 0
    When the Milan AECP model processes the frame
    Then the model responds status 11

  @class:setter
  Scenario: SET_STREAM_INFO MSRP_ACC_LAT-only on the Talker STREAM_OUTPUT succeeds
    Given tsn_gen generated a SET_STREAM_INFO frame with seed 62
    When I patch field "message_type" to 0
    And I patch field "command_type" to 14
    And I patch field "descriptor_type" to 0x06
    And I patch field "descriptor_index" to 0
    And I patch field "msrp_flags" to 0x2000000000000000
    And I patch field "msrp_accumulated_latency" to 500000
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model msrp_acc_lat is 500000

  @class:setter @negative
  Scenario: SET_STREAM_INFO with any other flag on STREAM_OUTPUT is refused NOT_SUPPORTED
    Given tsn_gen generated a SET_STREAM_INFO frame with seed 63
    When I patch field "message_type" to 0
    And I patch field "command_type" to 14
    And I patch field "descriptor_type" to 0x06
    And I patch field "descriptor_index" to 0
    And I patch field "msrp_flags" to 0x8000000000000000
    When the Milan AECP model processes the frame
    Then the model responds status 11
