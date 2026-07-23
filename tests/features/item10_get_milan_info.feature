# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# item-10 per-command getter fixture: MVU GET_MILAN_INFO.
# Codes verified 1:1 against hdl/ieee17221/aecp/aecp_pkg.sv:
#   MSG_VENDOR_UNIQUE_COMMAND = 4'd6           (aecp_pkg.sv:43)
#   VU_GET_MILAN_INFO         = 15'h0000       (aecp_pkg.sv:149)
#   MILAN_PROTOCOL_ID_C       = 48'h001BC50AC100 (aecp_pkg.sv:33)
# Response verified against the responder KL_aecp_response_builder.sv:1328-1341:
# protocol_id must match (else the frame is silently dropped), and the getter
# returns protocol_version = 1, features_flags = 0, certification_version = 0
# (0 stays 0 until AVnu-certified). Frame generated from the tsn-gen
# VENDOR_UNIQUE YAML; the MVU command_type rides the top 16 bits of vendor_data.

@tsn_gen @item10 @cmd:GET_MILAN_INFO @matrix:A-8
Feature: MVU GET_MILAN_INFO getter (Milan v1.2 vendor-unique)

  Background:
    Given the tsn_gen packet generator is available
    And a fresh Milan AECP model

  Scenario: well-formed GET_MILAN_INFO returns the Milan info block
    Given tsn_gen generated a VENDOR_UNIQUE frame with seed 2
    When I patch field "message_type" to 6
    And I patch field "protocol_id" to 0x001BC50AC100
    And I patch field "vendor_data" to 0x0000000000000000
    Then tsn_gen decodes every patched field back
    And our field extractor agrees with tsn_gen on every field
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model milan_version is 1
    And the model milan features_flags is 0
    And the model certification_version is 0

  Scenario: GET_MILAN_INFO under a foreign protocol_id is silently ignored
    Given tsn_gen generated a VENDOR_UNIQUE frame with seed 3
    When I patch field "message_type" to 6
    And I patch field "protocol_id" to 0x001122334455
    And I patch field "vendor_data" to 0x0000000000000000
    Then tsn_gen decodes every patched field back
    When the Milan AECP model processes the frame
    Then the AECP model ignores the frame

  Scenario: an unknown MVU command under the Milan protocol_id is not modelled
    Given tsn_gen generated a VENDOR_UNIQUE frame with seed 4
    When I patch field "message_type" to 6
    And I patch field "protocol_id" to 0x001BC50AC100
    And I patch field "vendor_data" to 0x7FFF000000000000
    Then tsn_gen decodes every patched field back
    When the Milan AECP model processes the frame
    Then the AECP model ignores the frame
