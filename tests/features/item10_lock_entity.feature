# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# item-10 per-command setter/semaphore fixture: LOCK_ENTITY.
# Codes verified 1:1 against hdl/ieee17221/aecp/aecp_pkg.sv:
#   CMD_LOCK_ENTITY      = 15'd1        (aecp_pkg.sv:50)
#   STATUS_ENTITY_LOCKED = 5'd3         (aecp_pkg.sv:91)
#   LOCK_TIMER_TICKS_C   = 17'd60_000   (aecp_pkg.sv:168, 60 s x 1 kHz)
# Lock SM verified against KL_aecp_l0_state.sv:132-133,199-221:
#   * LOCK by a free entity -> SUCCESS, records the controller, arms the timer.
#   * A LOCK_ENTITY (lock OR unlock) from a non-owner while locked -> ENTITY_LOCKED
#     with the state untouched (w_lock_denied).
#   * UNLOCK by the owner clears the lock; a re-LOCK by the owner reloads the timer.
#   * The timer auto-unlocks after LOCK_TIMER_TICKS_C+1 ticks.
# The RTL keys UNLOCK off flags bit 0 (KL_aecp_common_parser.sv:193, flags_lsb =
# tdata[16]) — a documented deviation from the spec's 0x80000000; the model and
# the patched frame both use bit 0.

@tsn_gen @item10 @cmd:LOCK_ENTITY @matrix:A-5
Feature: AECP LOCK_ENTITY semaphore (grant / deny / unlock / expiry)

  Background:
    Given the tsn_gen packet generator is available
    And a fresh Milan AECP model

  Scenario: a free entity grants the lock and records the controller
    Given tsn_gen generated a LOCK_ENTITY frame with seed 2
    When I patch field "message_type" to 0
    And I patch field "u" to 0
    And I patch field "command_type" to 1
    And I patch field "lock_entity_flags" to 0
    And I patch field "controller_entity_id" to 0xAABBCCDDEEFF0011
    Then tsn_gen decodes every patched field back
    And our field extractor agrees with tsn_gen on every field
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model entity is locked
    And the model locking controller is 0xAABBCCDDEEFF0011

  Scenario: a second controller is denied ENTITY_LOCKED and the owner is unchanged
    Given tsn_gen generated a LOCK_ENTITY frame with seed 3
    When I patch field "message_type" to 0
    And I patch field "command_type" to 1
    And I patch field "lock_entity_flags" to 0
    And I patch field "controller_entity_id" to 0xAABBCCDDEEFF0011
    And the Milan AECP model processes the frame
    Then the model responds status 0
    When I patch field "controller_entity_id" to 0x1122334455667788
    And the Milan AECP model processes the frame
    Then the model responds status 3
    And the model entity is locked
    And the model locking controller is 0xAABBCCDDEEFF0011

  Scenario: the owner re-locks and reloads the timer (SUCCESS)
    Given tsn_gen generated a LOCK_ENTITY frame with seed 4
    When I patch field "message_type" to 0
    And I patch field "command_type" to 1
    And I patch field "lock_entity_flags" to 0
    And I patch field "controller_entity_id" to 0xAABBCCDDEEFF0011
    And the Milan AECP model processes the frame
    Then the model responds status 0
    When the Milan AECP model processes the frame
    Then the model responds status 0
    And the model entity is locked
    And the model locking controller is 0xAABBCCDDEEFF0011

  Scenario: the owner unlocks and frees the entity
    Given tsn_gen generated a LOCK_ENTITY frame with seed 5
    When I patch field "message_type" to 0
    And I patch field "command_type" to 1
    And I patch field "lock_entity_flags" to 0
    And I patch field "controller_entity_id" to 0xAABBCCDDEEFF0011
    And the Milan AECP model processes the frame
    Then the model entity is locked
    When I patch field "lock_entity_flags" to 1
    And the Milan AECP model processes the frame
    Then the model responds status 0
    And the model entity is unlocked

  Scenario: a non-owner UNLOCK is denied ENTITY_LOCKED and the lock stands
    Given tsn_gen generated a LOCK_ENTITY frame with seed 6
    When I patch field "message_type" to 0
    And I patch field "command_type" to 1
    And I patch field "lock_entity_flags" to 0
    And I patch field "controller_entity_id" to 0xAABBCCDDEEFF0011
    And the Milan AECP model processes the frame
    Then the model entity is locked
    When I patch field "controller_entity_id" to 0x1122334455667788
    And I patch field "lock_entity_flags" to 1
    And the Milan AECP model processes the frame
    Then the model responds status 3
    And the model entity is locked
    And the model locking controller is 0xAABBCCDDEEFF0011

  Scenario: the lock auto-expires after 60001 ticks and another controller can lock
    Given tsn_gen generated a LOCK_ENTITY frame with seed 7
    When I patch field "message_type" to 0
    And I patch field "command_type" to 1
    And I patch field "lock_entity_flags" to 0
    And I patch field "controller_entity_id" to 0xAABBCCDDEEFF0011
    And the Milan AECP model processes the frame
    Then the model entity is locked
    When the 1 kHz lock timer advances 60001 ticks
    Then the model entity is unlocked
    When I patch field "controller_entity_id" to 0x1122334455667788
    And the Milan AECP model processes the frame
    Then the model responds status 0
    And the model entity is locked
    And the model locking controller is 0x1122334455667788
