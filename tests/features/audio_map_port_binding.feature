# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@item10 @cmd:AUDIO_MAP @matrix:CMD-19 @matrix:CMD-19b @matrix:AEM-3 @silicon:0x0016
Feature: GET_AUDIO_MAP serves the ANSWERING PORT's own map, within that port's bounds
  Measured on silicon 2026-07-28 against gateware 0x0001_0016 by a controller-grade
  check: GET_AUDIO_MAP(STREAM_PORT_OUTPUT, 0) returned 8 mappings with cluster_offset
  0..7 out of a port declaring number_of_clusters = 2.

  WHY NOTHING SAW IT. IEEE 1722.1-2021 7.2.19 Table 7-162 defines
  mapping_cluster_offset as the index of the cluster OFFSET FROM base_cluster of the
  STREAM_PORT that owns the map. The offsets are PORT-RELATIVE, so two ports
  legitimately publish the SAME offsets onto DIFFERENT global AUDIO_CLUSTERs - which
  means no comparison of one declaration against another can tell a right map from a
  wrong one. Only the answering port's own number_of_clusters can. The responder
  hardcoded BOTH ends of the answer: AUDIO_MAP descriptor index 1 and a fixed 8
  mappings / 64 octets. At the 1x1 deployed shape AUDIO_MAP[1] IS the output port's
  map and holds 8 rows, so the constants were accidentally right and every harness
  passed. At the 8x8 ship shape AUDIO_MAP[1] belongs to STREAM_PORT_INPUT[1] and the
  output port's map is AUDIO_MAP[8]: 24 octets, 2 rows. The responder read 64 octets
  out of it and put 48 octets of the following descriptors on the wire.

  The clauses cited here are for the RESPONSE FORMAT (7.4.44.2, >= 12 B) and the
  FIELD BOUNDS (7.2.19 / 7.2.13 / 7.2.16). The IEEE and Milan texts are paywalled and
  are NOT in this repo, so no sentence of them is quoted. Where the standard is
  SILENT it is said so: 7.4.44 fixes no ORDER for the mappings in a response, so the
  comparison below is a multiset and ordering is not asserted.

  Scenario: every STREAM_PORT of every tracked config points at an AUDIO_MAP that exists
    Given the generated AEM models for every tracked end-station config
    Then every STREAM_PORT base_map names an AUDIO_MAP the model defines
    And every AUDIO_MAP holds exactly the mappings it declares
    And every mapping is inside its own port's number_of_clusters

  Scenario: the RTL serving table binds each port to ITS OWN map, not a fixed index
    Given the generated AEM models for every tracked end-station config
    Then the static serving table addresses each port's own base_map descriptor
    And the static serving table row count is that descriptor's own number_of_mappings

  Scenario: at the 8x8 ship shape the pre-fix constants address the WRONG descriptor
    Given the generated AEM model for config "endstation_ax7101_8x8"
    Then AUDIO_MAP index 1 belongs to STREAM_PORT_INPUT 1, not to an output port
    And STREAM_PORT_OUTPUT 0 is served from a different address than AUDIO_MAP index 1
    And serving 8 mappings from STREAM_PORT_OUTPUT 0 would read past its descriptor

  Scenario Outline: the model gate REFUSES a map that leaves its port's bounds
    Given the deployed AEM model spec
    When the audio map is mutated by "<mutation>"
    Then building the model is refused naming "<clause>"

    Examples: out-of-bounds models that used to build silently
      | mutation           | clause  |
      | global_cluster_idx | 7.2.19  |
      | missing_base_map   | 7.2.13  |
      | two_maps_one_port  | 7.4.44.1|
      | cluster_channel_oob| 7.2.16  |
      | stream_index_oob   | 7.2.13  |
      | duplicate_cluster  | 5.4.2.26|
      | map_onto_crf       | 1722    |

  Scenario: the recorded stream_channel deviation is exactly the recorded one
    Given the deployed AEM model spec
    Then the open AUDIO_MAP deviations are exactly the recorded list
    And an empty allowlist makes that deviation FAIL

  Scenario Outline: the controller-grade over-read rule (hive_compliance C10)
    Given a served GET_AUDIO_MAP response described by "<case>"
    Then the C10 over-read rule reports <violations> violation(s)

    Examples: the measured defect and its negative controls
      | case                  | violations |
      | own_map               | 0          |
      | own_map_reordered     | 0          |
      | other_ports_map       | 9          |
      | declares_more_than_it_carries | 3  |
      | descriptor_overdeclares | 2        |
      | no_descriptor_dynamic | 0          |
