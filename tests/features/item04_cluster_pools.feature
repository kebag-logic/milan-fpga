# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@item04 @builder @clusters @matrix:AEM-3 @class:enumeration
Feature: Item-4 D8/D10 - the cluster model a CONTROLLER enumerates
  The end-station builder emits the AEM cluster/map layout from one config
  (docs/ENDSTATION_BUILDER.md D1/D2/D8/D10). These scenarios walk that
  emitted model exactly as a controller would - STREAM_PORT geometry, every
  AUDIO_CLUSTER in the advertised block, every AUDIO_MAP row - so a config
  that would ship a model no controller can enumerate fails here, before a
  bitstream exists.

  Clause basis: IEEE 1722.1-2021 7.2.13 (STREAM_PORT number_of_clusters /
  base_cluster / number_of_maps / base_map), 7.2.16 + 7.2.16.1 (mono MBLA
  AUDIO_CLUSTER), 7.2.19 (an AUDIO_MAP maps to clusters "contained in the
  same" port and mapping_cluster_offset is "the offset from the base_cluster
  of the STREAM_PORT_INPUT or STREAM_PORT_OUTPUT" - PORT-RELATIVE - plus its
  two uniqueness rules), 6.2.2.8 (object_name is NOT model structure), and
  Milan v1.2 5.4.2.27/28 (the dynamic mapping commands are required only for
  ports with NO Audio Map; a port WITH Audio Maps answers NOT_SUPPORTED,
  which is conformance and is asserted here rather than flagged).

  @class:enumeration
  Scenario: the DEPLOYED arty shape enumerates completely
    Given the end-station config "arty_current" is built
    Then the entity advertises 16 AUDIO_CLUSTER descriptors
    And every AUDIO_CLUSTER in every STREAM_PORT block answers READ_DESCRIPTOR
    And every AUDIO_MAP a STREAM_PORT declares answers READ_DESCRIPTOR
    And every AUDIO_MAP row is port-relative and inside its own cluster block
    And no AUDIO_MAP violates the 7.2.19 uniqueness rules
    And the AEM descriptor ROM generates from the overlay
    And the descriptor ROM fits the 16-bit AEM store address space

  @class:enumeration @negative
  Scenario: the DEPLOYED arty shape refuses the descriptor past its block
    Given the end-station config "arty_current" is built
    Then the AUDIO_CLUSTER one past the last block answers NO_SUCH_DESCRIPTOR

  @class:identity
  Scenario: D10 renaming the clusters did not move the pinned model id
    Given the end-station config "arty_current" is built
    Then no AUDIO_CLUSTER is named "Input"
    And no AUDIO_CLUSTER is named "Output"
    And every AUDIO_CLUSTER object_name matches its role
    And the entity_model_id is 0x001BC50AC1000001
    And renaming an AUDIO_CLUSTER leaves the entity_model_id unchanged

  @class:enumeration
  Scenario: the 4x4 cap-at-interface shape enumerates completely
    Given the end-station config "arty_4x4" is built
    Then the cluster policy is "cap-at-interface"
    And the entity advertises 32 AUDIO_CLUSTER descriptors
    And every AUDIO_CLUSTER in every STREAM_PORT block answers READ_DESCRIPTOR
    And every AUDIO_MAP row is port-relative and inside its own cluster block
    And no AUDIO_MAP violates the 7.2.19 uniqueness rules
    And every AUDIO_CLUSTER object_name matches its role

  @class:enumeration @d8
  Scenario: the AX 8x8 role-pool shape enumerates completely
    Given the end-station config "ax7101_8x8" is built
    Then the cluster policy is "role-pools"
    And the entity advertises 200 AUDIO_CLUSTER descriptors
    And every AUDIO_CLUSTER in every STREAM_PORT block answers READ_DESCRIPTOR
    And every AUDIO_MAP a STREAM_PORT declares answers READ_DESCRIPTOR
    And every AUDIO_MAP row is port-relative and inside its own cluster block
    And no AUDIO_MAP violates the 7.2.19 uniqueness rules
    And the AEM descriptor ROM generates from the overlay
    And the descriptor ROM fits the 16-bit AEM store address space

  @class:enumeration @d8
  Scenario: the AX advertises NO physical clusters because it routes no audio pins
    Given the end-station config "ax7101_8x8" is built
    Then the board routes 0 capture and 0 render physical channels
    And no AUDIO_CLUSTER carries the "physical" role
    And no AUDIO_CLUSTER carries the "virtual" role

  @class:enumeration @d8
  Scenario: the AX talkers wake on a pool this build can actually feed
    # task #65. The talkers used to wake mapped to the LOOPBACK pool, which
    # reads beautifully in a controller - "Loopback S0 ch 0" on every talker
    # channel - and carried digital silence on the wire, because
    # milan_datapath never connected KL_chan_map_capture's LOOP bucket to
    # the depacketizer. The clusters are still OFFERED (a controller may map
    # to them, and the lane is one declaration away), but the POWER-ON image
    # may only name a source the bitstream contains: with
    # cluster_mapping.fabric.loopback_lane false that is the host pool,
    # behind the single elaborated KL_pcm_tx ring. Milan v1.2 5.3.9.1 makes
    # the alternative explicit - a Stream Output channel is "either not
    # mapped or mapped to a channel of an Audio Cluster" - so under-claiming
    # is conformant while a source that cannot exist is merely invisible.
    Given the end-station config "ax7101_8x8" is built
    Then every talker AUDIO_MAP row lands in the "host" pool
    And each talker port offers a distinct "loopback" source set
    And every AUDIO_CLUSTER object_name matches its role

  @class:posture
  Scenario: Milan 5.4.2.27/28 - the fully dynamic ship refuses NOWHERE
    # USER 08-01: every ship talker went map_mode dynamic alongside the
    # listeners, so the shape carries ZERO Audio Maps and the dynamic
    # commands are a SHALL on every stream port. The WITH-maps refusal
    # posture is still proven below, on the deployed static shape.
    Given the end-station config "ax7101_8x8" is built
    When a controller sends ADD_AUDIO_MAPPINGS to every STREAM_PORT
    Then every port serves the dynamic commands (no Audio Maps anywhere)

  @class:posture
  Scenario: Milan 5.4.2.28 holds for the DEPLOYED shape too
    Given the end-station config "arty_current" is built
    When a controller sends ADD_AUDIO_MAPPINGS to every STREAM_PORT
    Then every port with Audio Maps answers NOT_SUPPORTED
