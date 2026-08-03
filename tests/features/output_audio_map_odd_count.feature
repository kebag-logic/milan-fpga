# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@tsn_gen @cmd:AUDIO_MAPS @matrix:M-AECP-4
Feature: A record COUNT is never a reason to refuse ADD/REMOVE_AUDIO_MAPPINGS
  Reported from the wire by Hive against our live entity on 2026-08-03:
  addStreamOutputAudioMappings and removeStreamOutputAudioMappings on
  STREAM_PORT_OUTPUT 0 both answered BAD_ARGUMENTS, with the surrounding
  lock/unlock succeeding. The cause was an engine rule that refused an ODD
  number_of_mappings - our capture crossbar routes a PAIR of stream channels
  per slot, and that geometry had leaked into protocol acceptance. Hive maps
  one channel at a time, so every command it sent was rejected.

  THE CLAUSES SAY NO SUCH RULE EXISTS.

  IEEE 1722.1-2021 7.4.45 ADD_AUDIO_MAPPINGS: "The number_of_mappings field
  is set to the number of mappings which are contained in the mappings
  field." and "If any mapping in the mappings field is invalid, then none of
  the mappings are added to the Stream Port and the command fails with a
  BAD_ARGUMENTS status. The determination of what constitutes a valid
  mapping at a particular point in time is governed by a set of vendor
  defined rules." Both sentences are about A MAPPING. The field's only
  bound is the PDU: control_data_length = 20 + 8*n and an AECPDU carries at
  most 1500 octets, i.e. n <= 183. No maximum is named anywhere.

  IEEE 1722.1-2021 7.4.46 REMOVE_AUDIO_MAPPINGS repeats it for removal:
  "If any mapping in the mappings field is invalid or not present, then none
  of the mappings are removed from the Stream Port and the command fails
  with a BAD_ARGUMENTS status."

  Milan v1.2 5.4.2.27 enumerates every BAD_ARGUMENTS condition a PAAD-AE
  shall or may raise for a Stream Port Output - a channel absent from the
  current format, a streaming channel where TALKER_DYNAMIC_MAPPINGS_WHILE_
  RUNNING is clear, two mappings on the same stream channel with different
  cluster channels - and 5.4.2.28 does the same for removal. A record count
  is not among them. 5.4.2.26 settles the granularity in the other
  direction: "there is at most one dynamic mapping per Stream Output's
  channel", so ONE channel is the unit a controller edits.

  The model under test is written from those clauses (see
  MilanOutputAudioMapModel), not from the RTL, so a disagreement with the
  gateware is a disagreement rather than two copies of one mistake. The
  per-mapping vendor rules it does keep are the physical ones 7.4.45
  delegates: the port's own stream, the cluster's source half must match its
  stream channel's parity, and one pair slot carries one source pair.

  # ---------------------------------------------------------------- #
  # The defect, stated directly.
  # ---------------------------------------------------------------- #
  @class:action @regression
  Scenario: ADD of a single mapping is accepted (7.4.45)
    Given a dynamic STREAM_PORT_OUTPUT of 4 stereo cluster pairs
    And stream channel 0 is mapped to cluster_offset 0
    And stream channel 1 is mapped to cluster_offset 1
    When a controller ADDs these output mappings
      | stream_index | stream_channel | cluster_offset | cluster_channel |
      | 0            | 1              | 1              | 0               |
    Then the output audio-map model responds status 0

  @class:action @regression
  Scenario: REMOVE of a single mapping is accepted (7.4.46)
    Given a dynamic STREAM_PORT_OUTPUT of 4 stereo cluster pairs
    And stream channel 0 is mapped to cluster_offset 0
    And stream channel 1 is mapped to cluster_offset 1
    When a controller REMOVEs these output mappings
      | stream_index | stream_channel | cluster_offset | cluster_channel |
      | 0            | 1              | 1              | 0               |
    Then the output audio-map model responds status 0

  @class:action @regression
  Scenario Outline: every record count the PDU can carry is accepted
    Milan 5.4.2.27 lists no count among its BAD_ARGUMENTS conditions, so an
    odd command and an even command differ only in how many valid mappings
    they carry.

    Given a dynamic STREAM_PORT_OUTPUT of 4 stereo cluster pairs
    When a controller ADDs these output mappings
      | stream_index | stream_channel | cluster_offset | cluster_channel |
      | 0            | 0              | 0              | 0               |
      | 0            | 1              | 1              | 0               |
      | 0            | 2              | 2              | 0               |
    Then the output audio-map model responds status 0
    And GET_AUDIO_MAP lists 3 output mappings
    And capture pair slot 0 carries source pair 0 on halves "LR"
    And capture pair slot 1 carries source pair 1 on halves "L"

    Examples: the command above carries an ODD count of THREE
      | note                                  |
      | 7.4.45 bounds n by the PDU, not by 2  |

  # ---------------------------------------------------------------- #
  # What accepting an odd count MEANS in the fabric: read-modify-write.
  # ---------------------------------------------------------------- #
  @class:action
  Scenario: a single ADD leaves the sibling channel's mapping alone
    Given a dynamic STREAM_PORT_OUTPUT of 4 stereo cluster pairs
    And stream channel 4 is mapped to cluster_offset 4
    When a controller ADDs these output mappings
      | stream_index | stream_channel | cluster_offset | cluster_channel |
      | 0            | 5              | 5              | 0               |
    Then the output audio-map model responds status 0
    And GET_AUDIO_MAP lists stream channel 5 at cluster_offset 5
    And GET_AUDIO_MAP lists stream channel 4 at cluster_offset 4
    And capture pair slot 2 carries source pair 2 on halves "LR"

  @class:action
  Scenario: a single REMOVE clears only its channel, sibling keeps its audio
    Milan v1.2 5.3.9.1 lets a channel of a Stream Output be "not mapped".
    The removed channel must then be SILENT - not carrying the source pair's
    other half, which GET_AUDIO_MAP does not report.

    Given a dynamic STREAM_PORT_OUTPUT of 4 stereo cluster pairs
    And stream channel 4 is mapped to cluster_offset 4
    And stream channel 5 is mapped to cluster_offset 5
    When a controller REMOVEs these output mappings
      | stream_index | stream_channel | cluster_offset | cluster_channel |
      | 0            | 5              | 5              | 0               |
    Then the output audio-map model responds status 0
    And GET_AUDIO_MAP lists no mapping for stream channel 5
    And GET_AUDIO_MAP lists stream channel 4 at cluster_offset 4
    And capture pair slot 2 carries source pair 2 on halves "L"

  @class:action
  Scenario: removing both channels of a slot leaves it silent, not half-armed
    Given a dynamic STREAM_PORT_OUTPUT of 4 stereo cluster pairs
    And stream channel 6 is mapped to cluster_offset 6
    And stream channel 7 is mapped to cluster_offset 7
    When a controller REMOVEs these output mappings
      | stream_index | stream_channel | cluster_offset | cluster_channel |
      | 0            | 6              | 6              | 0               |
      | 0            | 7              | 7              | 0               |
    Then the output audio-map model responds status 0
    And capture pair slot 3 is silent

  @class:action
  Scenario: a slot whose sibling is unmapped may take a different source pair
    Given a dynamic STREAM_PORT_OUTPUT of 4 stereo cluster pairs
    When a controller ADDs these output mappings
      | stream_index | stream_channel | cluster_offset | cluster_channel |
      | 0            | 3              | 1              | 0               |
    Then the output audio-map model responds status 0
    And capture pair slot 1 carries source pair 0 on halves "R"

  @class:action
  Scenario: three mappings over two slots compose, listed out of order
    The two records that share slot 0 are NOT adjacent in the command, so a
    commit that judged each record against the store as it stood at that
    moment would get the first one wrong. 7.4.45's all-or-nothing wording
    makes the command, not the record, the unit of effect.

    Given a dynamic STREAM_PORT_OUTPUT of 4 stereo cluster pairs
    When a controller ADDs these output mappings
      | stream_index | stream_channel | cluster_offset | cluster_channel |
      | 0            | 1              | 3              | 0               |
      | 0            | 7              | 7              | 0               |
      | 0            | 0              | 2              | 0               |
    Then the output audio-map model responds status 0
    And GET_AUDIO_MAP lists 3 output mappings
    And capture pair slot 0 carries source pair 1 on halves "LR"
    And capture pair slot 3 carries source pair 3 on halves "R"

  # ---------------------------------------------------------------- #
  # The per-MAPPING vendor rules 7.4.45 does delegate still bite.
  # ---------------------------------------------------------------- #
  @class:action @negative
  Scenario: a cluster's source half must match its stream channel's parity
    Slot p emits its source pair's L into stream channel 2p and its R into
    2p+1, so "the R half of a source onto an even channel" is a route the
    crossbar cannot make. That is a property of ONE mapping, which is
    exactly what 7.4.45 delegates to "vendor defined rules".

    Given a dynamic STREAM_PORT_OUTPUT of 4 stereo cluster pairs
    When a controller ADDs these output mappings
      | stream_index | stream_channel | cluster_offset | cluster_channel |
      | 0            | 2              | 1              | 0               |
    Then the output audio-map model responds status 7

  @class:action @negative
  Scenario: one pair slot carries one source pair
    Given a dynamic STREAM_PORT_OUTPUT of 4 stereo cluster pairs
    And stream channel 0 is mapped to cluster_offset 0
    When a controller ADDs these output mappings
      | stream_index | stream_channel | cluster_offset | cluster_channel |
      | 0            | 1              | 3              | 0               |
    Then the output audio-map model responds status 7
    And GET_AUDIO_MAP lists 1 output mappings

  @class:action @negative
  Scenario: two mappings on the same stream channel are refused (5.4.2.27)
    Given a dynamic STREAM_PORT_OUTPUT of 4 stereo cluster pairs
    When a controller ADDs these output mappings
      | stream_index | stream_channel | cluster_offset | cluster_channel |
      | 0            | 0              | 0              | 0               |
      | 0            | 0              | 2              | 0               |
    Then the output audio-map model responds status 7
    And GET_AUDIO_MAP lists 0 output mappings

  @class:action @negative
  Scenario: REMOVE of a mapping that is not present is refused (7.4.46)
    Given a dynamic STREAM_PORT_OUTPUT of 4 stereo cluster pairs
    When a controller REMOVEs these output mappings
      | stream_index | stream_channel | cluster_offset | cluster_channel |
      | 0            | 0              | 0              | 0               |
    Then the output audio-map model responds status 7

  @class:action
  Scenario: a mono pilot cluster may feed either channel of a slot
    The tone bucket puts the same value on both halves, so it is the one
    source a cluster can feed from either parity - and a lone mapping onto
    it is still one mapping.

    Given a dynamic STREAM_PORT_OUTPUT of 4 stereo cluster pairs plus a mono pilot cluster
    When a controller ADDs these output mappings
      | stream_index | stream_channel | cluster_offset | cluster_channel |
      | 0            | 5              | 8              | 0               |
    Then the output audio-map model responds status 0
    And capture pair slot 2 carries source pair 0 on halves "R"
