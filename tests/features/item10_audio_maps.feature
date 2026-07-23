# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@tsn_gen @item10 @cmd:AUDIO_MAPS @matrix:M-AECP-4
Feature: Item-10 dynamic audio maps + chmap64 AEM->fabric binding contract
  IEEE 1722.1-2021 GET_AUDIO_MAP (cmd 43 / 0x2B), ADD_AUDIO_MAPPINGS (44 /
  0x2C) and REMOVE_AUDIO_MAPPINGS (45 / 0x2D) on the dynamic STREAM_PORT_INPUT[0]
  (Milan es-4.16 / 5.4.2.26-28). Command codes are the RTL/spec values verified
  against hdl/ieee17221/aecp/aecp_pkg.sv. Frames are tsn_gen-generated and
  decode-cross-checked; the Milan audio-map model mirrors the `AEM_DYNMAP path
  of KL_aecp_response_builder (KEYS=8, NMAPS=2, PAGE=4 - the RTL itself is
  verified by tb/verilator/aecp).

  Each accepted mapping projects to a chmap64 render map word
  {en, stream[2:0], ch[2:0]} at the cluster-offset (physical-channel) address,
  each removal disables it - the executable chmap64 binding contract
  (docs/CHMAP64_AEM_BINDING.md).

  Background:
    Given the tsn_gen packet generator is available
    And a fresh Milan audio-map model

  # (a) getter, well-formed on the default (empty) dynamic map
  @class:getter
  Scenario: GET_AUDIO_MAP on the default input map is well-formed and empty
    Given tsn_gen generated a GET_AUDIO_MAP frame with seed 3
    When I patch field "message_type" to 0
    And I patch field "command_type" to 43
    And I patch field "descriptor_type" to 0x0E
    And I patch field "descriptor_index" to 0
    And I patch field "map_index" to 0
    Then tsn_gen decodes every patched field back
    And our field extractor agrees with tsn_gen on every field
    When the audio-map model processes the frame
    Then the audio-map model responds status 0
    And the last GET lists 0 mappings
    And the fabric render crossbar has 0 enabled words

  # (b) action + getter round-trip: ADD then GET reflects the added mapping
  @class:action @paired
  Scenario: ADD_AUDIO_MAPPINGS then GET_AUDIO_MAP reflects the added mapping
    Given tsn_gen generated a AUDIO_MAPPINGS frame with seed 5
    When I patch field "message_type" to 0
    And I patch field "command_type" to 44
    And I patch field "descriptor_type" to 0x0E
    And I patch field "descriptor_index" to 0
    And I patch field "number_of_mappings" to 1
    And I patch field "mapping_stream_index" to 0
    And I patch field "mapping_stream_channel" to 3
    And I patch field "mapping_cluster_offset" to 0
    And I patch field "mapping_cluster_channel" to 0
    Then tsn_gen decodes every patched field back
    And our field extractor agrees with tsn_gen on every field
    When the audio-map model processes the frame
    Then the audio-map model responds status 0
    And the fabric map word at cluster_offset 0 is en 1 stream 0 ch 3
    And the fabric map word at cluster_offset 0 equals 0x43
    And the fabric render crossbar has 1 enabled words
    Given tsn_gen generated a GET_AUDIO_MAP frame with seed 6
    When I patch field "message_type" to 0
    And I patch field "command_type" to 43
    And I patch field "descriptor_type" to 0x0E
    And I patch field "descriptor_index" to 0
    And I patch field "map_index" to 0
    When the audio-map model processes the frame
    Then the audio-map model responds status 0
    And the last GET lists 1 mappings
    And the last GET contains stream_channel 3 at cluster_offset 0

  # (c) action + getter round-trip: REMOVE then GET reflects the removal
  @class:action @paired
  Scenario: REMOVE_AUDIO_MAPPINGS then GET_AUDIO_MAP reflects the removal
    When I ADD mapping stream_channel 3 at cluster_offset 0
    Then the audio-map model responds status 0
    And the fabric render crossbar has 1 enabled words
    Given tsn_gen generated a AUDIO_MAPPINGS frame with seed 7
    When I patch field "message_type" to 0
    And I patch field "command_type" to 45
    And I patch field "descriptor_type" to 0x0E
    And I patch field "descriptor_index" to 0
    And I patch field "number_of_mappings" to 1
    And I patch field "mapping_stream_index" to 0
    And I patch field "mapping_stream_channel" to 3
    And I patch field "mapping_cluster_offset" to 0
    And I patch field "mapping_cluster_channel" to 0
    Then tsn_gen decodes every patched field back
    And our field extractor agrees with tsn_gen on every field
    When the audio-map model processes the frame
    Then the audio-map model responds status 0
    And the fabric map word at cluster_offset 0 is en 0 stream 0 ch 0
    And the fabric render crossbar has 0 enabled words
    When the audio-map model GETs input page 0
    Then the audio-map model responds status 0
    And the last GET lists 0 mappings

  # (d) negatives - the codes the RTL actually returns (BAD_ARGUMENTS = 7)
  @class:action @negative
  Scenario: ADD with an out-of-range stream_index is refused, nothing projected
    Given tsn_gen generated a AUDIO_MAPPINGS frame with seed 9
    When I patch field "message_type" to 0
    And I patch field "command_type" to 44
    And I patch field "descriptor_type" to 0x0E
    And I patch field "descriptor_index" to 0
    And I patch field "number_of_mappings" to 1
    And I patch field "mapping_stream_index" to 5
    And I patch field "mapping_stream_channel" to 1
    And I patch field "mapping_cluster_offset" to 0
    And I patch field "mapping_cluster_channel" to 0
    Then tsn_gen decodes every patched field back
    When the audio-map model processes the frame
    Then the audio-map model responds status 7
    And the fabric render crossbar has 0 enabled words

  @class:action @negative
  Scenario: ADD with a duplicate cluster key in one command is refused (all-or-nothing)
    When I ADD a same-key mapping pair at cluster_offset 2 with stream_channels 1 and 2
    Then the audio-map model responds status 7
    And the fabric render crossbar has 0 enabled words

  @class:action @negative
  Scenario: ADD on the static STREAM_PORT_OUTPUT map is NOT_SUPPORTED
    Given tsn_gen generated a AUDIO_MAPPINGS frame with seed 11
    When I patch field "message_type" to 0
    And I patch field "command_type" to 44
    And I patch field "descriptor_type" to 0x0F
    And I patch field "descriptor_index" to 0
    And I patch field "number_of_mappings" to 1
    And I patch field "mapping_stream_index" to 0
    And I patch field "mapping_stream_channel" to 0
    And I patch field "mapping_cluster_offset" to 0
    And I patch field "mapping_cluster_channel" to 0
    When the audio-map model processes the frame
    Then the audio-map model responds status 11

  @class:getter @negative
  Scenario: GET_AUDIO_MAP on an unknown descriptor is refused
    Given tsn_gen generated a GET_AUDIO_MAP frame with seed 13
    When I patch field "message_type" to 0
    And I patch field "command_type" to 43
    And I patch field "descriptor_type" to 0x05
    And I patch field "descriptor_index" to 0
    And I patch field "map_index" to 0
    When the audio-map model processes the frame
    Then the audio-map model responds status 2

  @class:getter @negative
  Scenario: GET_AUDIO_MAP with an out-of-range map_index is BAD_ARGUMENTS
    When the audio-map model GETs input page 2
    Then the audio-map model responds status 7

  # (e) the chmap64 binding contract: the crossbar tracks accepted mappings
  @class:action @fabric
  Scenario: the render crossbar projects, replaces and clears map words
    When I ADD mapping stream_channel 1 at cluster_offset 0
    And I ADD mapping stream_channel 2 at cluster_offset 1
    Then the audio-map model responds status 0
    And the fabric map word at cluster_offset 0 equals 0x41
    And the fabric map word at cluster_offset 1 equals 0x42
    And the fabric render crossbar has 2 enabled words
    When I ADD mapping stream_channel 4 at cluster_offset 1
    Then the audio-map model responds status 0
    And the fabric map word at cluster_offset 1 is en 1 stream 0 ch 4
    And the fabric render crossbar has 2 enabled words
    When I REMOVE mapping stream_channel 1 at cluster_offset 0
    Then the audio-map model responds status 0
    And the fabric map word at cluster_offset 0 is en 0 stream 0 ch 0
    And the fabric map word at cluster_offset 1 equals 0x44
    And the fabric render crossbar has 1 enabled words
