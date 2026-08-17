# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@item10 @chmap64 @matrix:M-AECP-4
Feature: the chmap64 render-crossbar binding contract

  A dynamic audio mapping is, on this device, an ADDRESS and a WORD in the
  render crossbar: {en, stream[2:0], ch[2:0]} written at the GLOBAL cluster
  key base_cluster + port-relative offset, which is KL_chan_map_render's
  map-RAM address. That projection is the executable chmap64 binding
  contract (docs/CHMAP64_AEM_BINDING.md), and the crossbar it addresses -
  KL_chan_map_render and its capture twin KL_chan_map_capture - still ships.

  The protocol processor serves READ_DESCRIPTOR from its main-memory image and
  GET_AUDIO_MAP through the root gather face. ADD_AUDIO_MAPPINGS and
  REMOVE_AUDIO_MAPPINGS use a validate pass followed by a commit pass, then
  write the live render or capture map RAM through the transaction face.
  The processor and milan_dp harnesses grade the wire commands, all-or-nothing
  refusal, notification, and live payload effect. The offline model here keeps
  the crossbar projection independently executable without tsn_gen.

  WHAT STAYED, and why it is still a real check: the key-space law. Milan
  v1.2 5.3.3.9 - "The Stream Port Input of a Configuration shall not contain
  any AUDIO_MAP descriptor. Note: this means that a PAAD-AE implements
  dynamic mappings on all of its Stream Port Inputs" - is what makes the
  crossbar address base_cluster + offset rather than a bare offset, and the
  scenarios below are what hold the projection to it.

  Background:
    Given a fresh Milan audio-map model

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

  # (f) roadmap 23: Milan v1.2 5.3.3.9 — "The Stream Port Input of a
  # Configuration shall not contain any AUDIO_MAP descriptor. Note: this
  # means that a PAAD-AE implements dynamic mappings on all of its Stream
  # Port Inputs." Both NxN configs ship map_mode: dynamic on every listener,
  # so the engine has to keep the ports independent: the wire offset is
  # PORT-RELATIVE (1722.1-2021 Table 7-33) while the store key — and the
  # render crossbar address — is base_cluster + offset.
  @class:action @fabric @roadmap23
  Scenario: every Stream Port Input maps independently into one key space
    Given a Milan audio-map model with 4 dynamic ports of 4 clusters and page 4
    When on input port 1 I ADD stream 1 channel 3 at cluster_offset 2
    Then the audio-map model responds status 0
    And the fabric map word at cluster_offset 6 is en 1 stream 1 ch 3
    And the fabric render crossbar has 1 enabled words
    When on input port 0 I ADD stream 0 channel 3 at cluster_offset 2
    Then the audio-map model responds status 0
    And the fabric map word at cluster_offset 2 is en 1 stream 0 ch 3
    And the fabric render crossbar has 2 enabled words
    When the audio-map model GETs input port 1 page 0
    Then the audio-map model responds status 0
    And the last GET lists 1 mappings
    And the last GET contains stream 1 channel 3 at cluster_offset 2
    When the audio-map model GETs input port 3 page 0
    Then the audio-map model responds status 0
    And the last GET lists 0 mappings

  @class:action @negative @roadmap23
  Scenario: a cluster_offset past the addressed port never reaches its neighbour
    Given a Milan audio-map model with 4 dynamic ports of 4 clusters and page 4
    When on input port 0 I ADD stream 0 channel 0 at cluster_offset 4
    Then the audio-map model responds status 7
    And the fabric render crossbar has 0 enabled words
    When on input port 4 I ADD stream 0 channel 0 at cluster_offset 0
    Then the audio-map model responds status 2
    When the audio-map model GETs input port 0 page 1
    Then the audio-map model responds status 7

  @class:action @negative @roadmap23
  Scenario: mapping_stream_index names a Stream Input, and never the CRF sink
    Given a Milan audio-map model with 2 dynamic ports of 4 clusters and page 4
    When on input port 0 I ADD stream 1 channel 2 at cluster_offset 0
    Then the audio-map model responds status 0
    And the fabric map word at cluster_offset 0 is en 1 stream 1 ch 2
    When on input port 0 I ADD stream 2 channel 0 at cluster_offset 1
    Then the audio-map model responds status 7
    When on input port 0 I ADD stream 3 channel 0 at cluster_offset 1
    Then the audio-map model responds status 7
    # 7.4.46.1: "If any of the mappings in the command are invalid or not
    # present then the command shall fail with a BAD_ARGUMENTS status and
    # none of the mappings shall be removed." The stored row names stream 1,
    # so a REMOVE naming stream 0 is NOT PRESENT - refused, not ignored.
    When on input port 0 I REMOVE stream 0 channel 2 at cluster_offset 0
    Then the audio-map model responds status 7
    And the fabric map word at cluster_offset 0 is en 1 stream 1 ch 2
    When on input port 0 I REMOVE stream 1 channel 2 at cluster_offset 0
    Then the audio-map model responds status 0
    And the fabric render crossbar has 0 enabled words

  @class:action @boundary @roadmap23
  Scenario: the mapping command limit is 63 complete records
    When I ADD 63 copies of stream_channel 0 at cluster_offset 0
    Then the audio-map model responds status 0
    And the fabric render crossbar has 1 enabled words
    When I ADD 64 copies of stream_channel 1 at cluster_offset 1
    Then the audio-map model responds status 7
    And the fabric render crossbar has 1 enabled words
