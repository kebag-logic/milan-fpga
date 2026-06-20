# SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# BDD feature: KL_aecp_l0_state
# Spec refs: IEEE 1722.1-2021 §9.2.7–§9.2.9; Milan v1.2 §5.4.4; aem-aecp.md §3.2.4
# Tier: T1 (Verilator + behave)

Feature: KL_aecp_l0_state — entity lock, acquire and configuration semantics

  Background:
    Given the DUT is KL_aecp_l0_state
    And the entity_id is 0x001BC5FFFE112233
    And the DUT is reset
    And controller "C1" has id 0xAABBCCDDEEFF0011
    And controller "C2" has id 0x1122334455667788

  Scenario: Initial state has no lock and no acquire
    Then l0_state.locked is 0
    And l0_state.acquired is 0
    And l0_state.current_configuration_index is 0

  Scenario: LOCK_ENTITY from C1 sets locked flag and returns SUCCESS
    When I send LOCK_ENTITY command from "C1"
    Then the DUT acknowledges with status SUCCESS (0)
    And l0_state.locked is 1
    And l0_state.locking_controller_id equals "C1"

  Scenario: Write command from C2 while locked by C1 returns ENTITY_LOCKED
    Given the entity is locked by "C1"
    When I send SET_NAME command from "C2"
    Then the DUT acknowledges with status ENTITY_LOCKED (3)
    And reject_o is asserted

  Scenario: Read command from C2 while locked by C1 succeeds
    Given the entity is locked by "C1"
    When I send GET_CONFIGURATION command from "C2"
    Then the DUT acknowledges with status SUCCESS (0)

  Scenario: Lock auto-releases after 60000 ticks
    Given the entity is locked by "C1"
    When I advance the 1 kHz tick by 60001 pulses
    Then l0_state.locked is 0
    And I send SET_NAME command from "C2"
    And the DUT acknowledges with status SUCCESS (0)

  Scenario: LOCK_ENTITY with UNLOCK flag clears the lock
    Given the entity is locked by "C1"
    When I send LOCK_ENTITY UNLOCK command from "C1"
    Then l0_state.locked is 0

  Scenario: ACQUIRE_ENTITY from C1 sets acquired and records controller
    When I send ACQUIRE_ENTITY command from "C1"
    Then the DUT acknowledges with status SUCCESS (0)
    And l0_state.acquired is 1
    And l0_state.acquiring_controller_id equals "C1"

  Scenario: ACQUIRE_ENTITY from C2 while acquired by C1 returns ENTITY_ACQUIRED
    Given the entity is acquired by "C1"
    When I send ACQUIRE_ENTITY command from "C2"
    Then the DUT acknowledges with status ENTITY_ACQUIRED (4)

  Scenario: ACQUIRE_ENTITY with RELEASE flag from C1 clears acquire
    Given the entity is acquired by "C1"
    When I send ACQUIRE_ENTITY RELEASE command from "C1"
    Then l0_state.acquired is 0

  Scenario: SET_CONFIGURATION changes current_configuration_index
    When I send SET_CONFIGURATION command from "C1" with config_index 2
    And the response is sent (cmd_done pulses)
    Then l0_state.current_configuration_index is 2

  Scenario: SET_CONFIGURATION with out-of-range index returns BAD_ARGUMENTS
    When I send SET_CONFIGURATION command from "C1" with config_index 5
    Then the DUT acknowledges with status BAD_ARGUMENTS (7)
    And l0_state.current_configuration_index is unchanged
