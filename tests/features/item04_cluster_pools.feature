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
    And the entity advertises 24 AUDIO_CLUSTER descriptors
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
  Scenario: the AX talkers are sourced from the loopback pool, distinctly
    Given the end-station config "ax7101_8x8" is built
    Then every talker AUDIO_MAP row lands in the "loopback" pool
    And each talker port offers a distinct "loopback" source set
    And every AUDIO_CLUSTER object_name matches its role

  @class:posture
  Scenario: Milan 5.4.2.28 - ports WITH Audio Maps refuse the dynamic commands
    Given the end-station config "ax7101_8x8" is built
    When a controller sends ADD_AUDIO_MAPPINGS to every STREAM_PORT
    Then every port with Audio Maps answers NOT_SUPPORTED

  @class:posture
  Scenario: Milan 5.4.2.28 holds for the DEPLOYED shape too
    Given the end-station config "arty_current" is built
    When a controller sends ADD_AUDIO_MAPPINGS to every STREAM_PORT
    Then every port with Audio Maps answers NOT_SUPPORTED
