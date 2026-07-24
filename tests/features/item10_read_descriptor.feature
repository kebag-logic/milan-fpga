# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@tsn_gen @item10 @cmd:READ_DESCRIPTOR @matrix:CMD-4 @class:getter
Feature: Item-10 READ_DESCRIPTOR - descriptor getter (read-only, idempotent, reject-unknown)
  Getter fixture (docs/testing/PDU_GETTER_SETTER_VERIFICATION.md, class 1) for the AEM
  READ_DESCRIPTOR (0x0004) command. READ_DESCRIPTOR is getter-only - there is no SET pair:
  reading a KNOWN Milan-entity descriptor returns SUCCESS with a well-formed response; an
  unknown descriptor_type or an out-of-range descriptor_index returns NO_SUCH_DESCRIPTOR; and
  the read is idempotent (it never mutates entity state). The known-descriptor set mirrors the
  Milan entity AEM: ENTITY[0], CONFIGURATION[0..2], AUDIO_UNIT[0], STREAM_INPUT[0],
  STREAM_OUTPUT[0], CLOCK_DOMAIN[0]. Frames are tsn_gen-generated; the Milan AECP model mirrors
  KL_aecp_response_builder.

  Background:
    Given the tsn_gen packet generator is available
    And a fresh Milan AECP model

  @class:getter
  Scenario: READ_DESCRIPTOR of ENTITY[0] returns SUCCESS, well-formed
    Given tsn_gen generated a READ_DESCRIPTOR frame with seed 50
    When I patch field "message_type" to 0
    And I patch field "command_type" to 4
    And I patch field "descriptor_type" to 0x0000
    And I patch field "descriptor_index" to 0
    Then tsn_gen decodes every patched field back
    And our field extractor agrees with tsn_gen on every field
    When the Milan AECP model processes the frame
    Then the model responds status 0

  @class:getter
  Scenario: READ_DESCRIPTOR of CONFIGURATION[2] (last valid index) returns SUCCESS
    Given tsn_gen generated a READ_DESCRIPTOR frame with seed 51
    When I patch field "message_type" to 0
    And I patch field "command_type" to 4
    And I patch field "descriptor_type" to 0x0001
    And I patch field "descriptor_index" to 2
    Then tsn_gen decodes every patched field back
    When the Milan AECP model processes the frame
    Then the model responds status 0

  @class:getter @negative
  Scenario: READ_DESCRIPTOR of an unknown descriptor_type is refused
    Given tsn_gen generated a READ_DESCRIPTOR frame with seed 52
    When I patch field "message_type" to 0
    And I patch field "command_type" to 4
    And I patch field "descriptor_type" to 0x00FF
    And I patch field "descriptor_index" to 0
    When the Milan AECP model processes the frame
    Then the model responds status 2

  @class:getter @negative
  Scenario: READ_DESCRIPTOR of CONFIGURATION with an out-of-range index is refused
    Given tsn_gen generated a READ_DESCRIPTOR frame with seed 53
    When I patch field "message_type" to 0
    And I patch field "command_type" to 4
    And I patch field "descriptor_type" to 0x0001
    And I patch field "descriptor_index" to 9
    When the Milan AECP model processes the frame
    Then the model responds status 2

  @class:getter
  Scenario: READ_DESCRIPTOR is idempotent - two reads of ENTITY[0] both SUCCESS
    Given tsn_gen generated a READ_DESCRIPTOR frame with seed 54
    When I patch field "message_type" to 0
    And I patch field "command_type" to 4
    And I patch field "descriptor_type" to 0x0000
    And I patch field "descriptor_index" to 0
    When the Milan AECP model processes the frame
    Then the model responds status 0
    When the Milan AECP model processes the frame
    Then the model responds status 0
