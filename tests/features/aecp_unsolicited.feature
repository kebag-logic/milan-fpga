# SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# BDD feature: KL_aecp_unsolicited_table
# Spec refs: IEEE 1722.1-2021 §9.2.22–§9.2.23; aem-aecp.md §3.2.8

Feature: KL_aecp_unsolicited_table — 16-deep controller registry

  Background:
    Given the DUT is KL_aecp_unsolicited_table
    And the DUT is reset

  Scenario: REGISTER_UNSOLICITED_NOTIFICATION inserts controller
    When I send REGISTER_UNSOLICITED_NOTIFICATION from controller 0xAABBCCDDEEFF0011
    Then the DUT returns status SUCCESS (0)
    And the controller is in the registry

  Scenario: Registering the same controller twice is idempotent
    Given controller 0xAABBCCDDEEFF0011 is registered
    When I send REGISTER_UNSOLICITED_NOTIFICATION from controller 0xAABBCCDDEEFF0011
    Then the DUT returns status SUCCESS (0)
    And the registry has exactly 1 entry for that controller

  Scenario: DEREGISTER_UNSOLICITED_NOTIFICATION removes controller
    Given controller 0xAABBCCDDEEFF0011 is registered
    When I send DEREGISTER_UNSOLICITED_NOTIFICATION from controller 0xAABBCCDDEEFF0011
    Then the DUT returns status SUCCESS (0)
    And the controller is not in the registry

  Scenario: Table full (16 controllers) returns NO_RESOURCES
    Given 16 distinct controllers are registered
    When I send REGISTER_UNSOLICITED_NOTIFICATION from a new controller
    Then the DUT returns status NO_RESOURCES (8)
    And table_full_o is asserted

  Scenario: State change triggers unsolicited emit for all registered controllers
    Given controllers "C1" and "C2" are registered
    When state_changed_i pulses
    Then emit_valid_o pulses twice
    And emit_o cycles through the indices of "C1" and "C2"

  Scenario: CAM lookup completes in at most 2 cycles
    Given 16 distinct controllers are registered
    When I trigger a lookup for the last-registered controller
    Then emit_valid_o asserts within 2 clock cycles of the trigger
