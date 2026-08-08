# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@tsn_gen @item10 @cmd:STREAM_FORMAT @matrix:CMD-8
Feature: Item-10 GET/SET_STREAM_FORMAT - getter/setter round-trip (paired)
  Paired fixture (docs/testing/PDU_GETTER_SETTER_VERIFICATION.md, class 3) for the STREAM_INPUT/
  STREAM_OUTPUT AAF stream format. GET_STREAM_FORMAT (0x0009) shares the SET_STREAM_FORMAT
  (0x0008) wire layout, so the GET frame is the SET frame with command_type patched. Frames are
  tsn_gen-generated; the Milan AECP model mirrors KL_aecp_response_builder. The formats are the
  real AAF_PCM 48 kHz strings from avdecc/milan-v12-entity.json: 2ch default 0x0205022000806000
  (= 145524899430031360) and up-to-8ch 0x0215022002006000 (= 150028499082567680).

  Background:
    Given the tsn_gen packet generator is available
    And a fresh Milan AECP model

  @class:getter
  Scenario: GET_STREAM_FORMAT returns the current format (default AAF_PCM 48k 2ch), well-formed
    Given tsn_gen generated a SET_STREAM_FORMAT frame with seed 80
    When I patch field "message_type" to 0
    And I patch field "command_type" to 9
    And I patch field "descriptor_type" to 0x05
    And I patch field "descriptor_index" to 0
    Then tsn_gen decodes every patched field back
    And our field extractor agrees with tsn_gen on every field
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model stream_format is 145524899430031360

  @class:paired
  Scenario: the getter reflects the setter (SET up-to-8ch then GET)
    Given tsn_gen generated a SET_STREAM_FORMAT frame with seed 81
    When I patch field "message_type" to 0
    And I patch field "command_type" to 8
    And I patch field "descriptor_type" to 0x05
    And I patch field "descriptor_index" to 0
    And I patch field "stream_format" to 0x0215022002006000
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model stream_format is 150028499082567680
    Given tsn_gen generated a SET_STREAM_FORMAT frame with seed 82
    When I patch field "message_type" to 0
    And I patch field "command_type" to 9
    And I patch field "descriptor_type" to 0x05
    And I patch field "descriptor_index" to 0
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model stream_format is 150028499082567680

  @class:setter @negative
  Scenario: SET_STREAM_FORMAT to an unsupported format is refused, format unchanged
    Given tsn_gen generated a SET_STREAM_FORMAT frame with seed 83
    When I patch field "message_type" to 0
    And I patch field "command_type" to 8
    And I patch field "descriptor_type" to 0x06
    And I patch field "descriptor_index" to 0
    And I patch field "stream_format" to 0xDEADBEEFDEADBEEF
    When the Milan AECP model processes the frame
    Then the model responds status 7
    And the model stream_format is 145524899430031360

  @class:getter @negative
  Scenario: GET_STREAM_FORMAT on a non-STREAM descriptor is refused
    Given tsn_gen generated a SET_STREAM_FORMAT frame with seed 84
    When I patch field "message_type" to 0
    And I patch field "command_type" to 9
    And I patch field "descriptor_type" to 0x00
    And I patch field "descriptor_index" to 0
    When the Milan AECP model processes the frame
    Then the model responds status 2

  @class:setter @negative @gh58
  Scenario: SET_STREAM_FORMAT on a BOUND input refuses STREAM_IS_RUNNING, format unchanged
    # gh #58 D1 (Milan 5.4.2.6 / 5.3.8.2): the ACMP bind LEVEL alone refuses
    # the SET - value-independent (this is a VALID format), and the refusal
    # outranks the format check. Status 12 = STREAM_IS_RUNNING (wire bytes
    # 16-17 carry the 0x60 class).
    Given tsn_gen generated a SET_STREAM_FORMAT frame with seed 85
    And the listener sink is bound over ACMP
    When I patch field "message_type" to 0
    And I patch field "command_type" to 8
    And I patch field "descriptor_type" to 0x05
    And I patch field "descriptor_index" to 0
    And I patch field "stream_format" to 0x0215022002006000
    When the Milan AECP model processes the frame
    Then the model responds status 12
    And the model stream_format is 145524899430031360

  @class:setter @gh58
  Scenario: the unbound twin of the same SET is accepted (adaptation order survives)
    # The Milan adaptive-listener flow (DISCONNECT -> SET -> CONNECT): the
    # identical frame lands once the bind level fell.
    Given tsn_gen generated a SET_STREAM_FORMAT frame with seed 86
    And the listener sink is unbound
    When I patch field "message_type" to 0
    And I patch field "command_type" to 8
    And I patch field "descriptor_type" to 0x05
    And I patch field "descriptor_index" to 0
    And I patch field "stream_format" to 0x0215022002006000
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model stream_format is 150028499082567680
