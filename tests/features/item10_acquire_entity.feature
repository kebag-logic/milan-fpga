# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# item-10 per-command setter/semaphore fixture: ACQUIRE_ENTITY.
# Codes verified 1:1 against hdl/ieee17221/aecp/aecp_pkg.sv:
#   CMD_ACQUIRE_ENTITY   = 15'd0    (aecp_pkg.sv:49)
#   STATUS_NOT_SUPPORTED = 5'd11    (aecp_pkg.sv:99)
# Behaviour verified against the responder: KL_aecp_l0_state.sv:145-147 answers
# ACQUIRE_ENTITY with STATUS_NOT_SUPPORTED and NEVER mutates state (l0_state
# .acquired is hardwired 0 at :81); the response builder just relays l0_status
# (KL_aecp_response_builder.sv:1403-1404). This is Milan v1.2 (es-4.1): ACQUIRE
# is not a supported acquisition model. The model reflects the real RTL, not the
# 1722.1-ideal SUCCESS/ENTITY_ACQUIRED handshake.

@tsn_gen @item10 @cmd:ACQUIRE_ENTITY @matrix:A-5
Feature: AECP ACQUIRE_ENTITY is NOT_SUPPORTED (Milan v1.2)

  Background:
    Given the tsn_gen packet generator is available
    And a fresh Milan AECP model

  Scenario: ACQUIRE_ENTITY with no flags returns NOT_SUPPORTED and never acquires
    Given tsn_gen generated a ACQUIRE_ENTITY frame with seed 2
    When I patch field "message_type" to 0
    And I patch field "u" to 0
    And I patch field "command_type" to 0
    And I patch field "acquire_entity_flags" to 0
    Then tsn_gen decodes every patched field back
    And our field extractor agrees with tsn_gen on every field
    When the Milan AECP model processes the frame
    Then the model responds status 11
    And the model has not acquired the entity

  Scenario: ACQUIRE_ENTITY with the PERSISTENT flag is still NOT_SUPPORTED
    Given tsn_gen generated a ACQUIRE_ENTITY frame with seed 3
    When I patch field "message_type" to 0
    And I patch field "command_type" to 0
    And I patch field "acquire_entity_flags" to 0x40000000
    Then tsn_gen decodes every patched field back
    When the Milan AECP model processes the frame
    Then the model responds status 11
    And the model has not acquired the entity

  Scenario: ACQUIRE_ENTITY with the RELEASE flag is still NOT_SUPPORTED
    Given tsn_gen generated a ACQUIRE_ENTITY frame with seed 4
    When I patch field "message_type" to 0
    And I patch field "command_type" to 0
    And I patch field "acquire_entity_flags" to 0x80000000
    Then tsn_gen decodes every patched field back
    When the Milan AECP model processes the frame
    Then the model responds status 11
    And the model has not acquired the entity

  Scenario: back-to-back ACQUIRE from two controllers never returns ENTITY_ACQUIRED
    Given tsn_gen generated a ACQUIRE_ENTITY frame with seed 5
    When I patch field "message_type" to 0
    And I patch field "command_type" to 0
    And I patch field "acquire_entity_flags" to 0
    And I patch field "controller_entity_id" to 0xAABBCCDDEEFF0011
    And the Milan AECP model processes the frame
    Then the model responds status 11
    When I patch field "controller_entity_id" to 0x1122334455667788
    And the Milan AECP model processes the frame
    Then the model responds status 11
    And the model has not acquired the entity
