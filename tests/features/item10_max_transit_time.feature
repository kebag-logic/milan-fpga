# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# item-10 per-command getter/setter fixture: SET/GET_MAX_TRANSIT_TIME.
# Codes verified 1:1 against hdl/ieee17221/aecp/aecp_pkg.sv:
#   CMD_SET_MAX_TRANSIT_TIME = 15'h004C  (aecp_pkg.sv:82)
#   CMD_GET_MAX_TRANSIT_TIME = 15'h004D  (aecp_pkg.sv:83)
# Behaviour verified against the responder KL_aecp_response_builder.sv:2005-2036:
# addresses STREAM_OUTPUT[0] (0x0006/0); the max_transit_time u64 drives the
# framer's presentation offset (same source of truth as SET_STREAM_INFO
# ACC_LAT). value > 0x7FFFFFFF ns -> BAD_ARGUMENTS; wrong descriptor ->
# NO_SUCH_DESCRIPTOR. No dedicated tsn-gen YAML exists, so the frame is
# generated from SET_STREAM_FORMAT (the nearest AEM SET whose u64 'stream_format'
# lands at the exact bytes 6-13 the max_transit_time u64 occupies) with
# command_type patched to 0x4C/0x4D — documented in tsn_gen_steps.py.

@tsn_gen @item10 @cmd:MAX_TRANSIT_TIME @matrix:A-5
Feature: AECP SET/GET_MAX_TRANSIT_TIME on STREAM_OUTPUT[0]

  Background:
    Given the tsn_gen packet generator is available
    And a fresh Milan AECP model

  Scenario: SET_MAX_TRANSIT_TIME stores, GET_MAX_TRANSIT_TIME reflects
    Given tsn_gen generated a MAX_TRANSIT_TIME frame with seed 2
    When I patch field "message_type" to 0
    And I patch field "u" to 0
    And I patch field "command_type" to 0x4C
    And I patch field "descriptor_type" to 0x0006
    And I patch field "descriptor_index" to 0
    And I patch field "stream_format" to 2000000
    Then tsn_gen decodes every patched field back
    And our field extractor agrees with tsn_gen on every field
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model max_transit_time is 2000000
    When I patch field "command_type" to 0x4D
    And I patch field "stream_format" to 0
    And the Milan AECP model processes the frame
    Then the model responds status 0
    And the model max_transit_time is 2000000

  Scenario: SET_MAX_TRANSIT_TIME above 0x7FFFFFFF ns is refused
    Given tsn_gen generated a MAX_TRANSIT_TIME frame with seed 3
    When I patch field "message_type" to 0
    And I patch field "command_type" to 0x4C
    And I patch field "descriptor_type" to 0x0006
    And I patch field "descriptor_index" to 0
    And I patch field "stream_format" to 0x80000000
    Then tsn_gen decodes every patched field back
    When the Milan AECP model processes the frame
    Then the model responds status 7
    And the model max_transit_time is 0

  Scenario: SET_MAX_TRANSIT_TIME with the u64 upper word set is refused
    Given tsn_gen generated a MAX_TRANSIT_TIME frame with seed 4
    When I patch field "message_type" to 0
    And I patch field "command_type" to 0x4C
    And I patch field "descriptor_type" to 0x0006
    And I patch field "descriptor_index" to 0
    And I patch field "stream_format" to 0x0000000100000000
    Then tsn_gen decodes every patched field back
    When the Milan AECP model processes the frame
    Then the model responds status 7

  Scenario: MAX_TRANSIT_TIME against a non-STREAM_OUTPUT descriptor
    Given tsn_gen generated a MAX_TRANSIT_TIME frame with seed 5
    When I patch field "message_type" to 0
    And I patch field "command_type" to 0x4D
    And I patch field "descriptor_type" to 0x0005
    And I patch field "descriptor_index" to 0
    Then tsn_gen decodes every patched field back
    When the Milan AECP model processes the frame
    Then the model responds status 2

  Scenario: MAX_TRANSIT_TIME on STREAM_OUTPUT with a non-zero index
    Given tsn_gen generated a MAX_TRANSIT_TIME frame with seed 6
    When I patch field "message_type" to 0
    And I patch field "command_type" to 0x4C
    And I patch field "descriptor_type" to 0x0006
    And I patch field "descriptor_index" to 1
    And I patch field "stream_format" to 1000
    Then tsn_gen decodes every patched field back
    When the Milan AECP model processes the frame
    Then the model responds status 2
    And the model max_transit_time is 0
