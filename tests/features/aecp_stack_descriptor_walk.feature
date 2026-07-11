# SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# BDD feature: AECP descriptor enumeration
# Spec refs: IEEE 1722.1-2021 §9.2.9; Milan v1.2 §5.4; aem-aecp.md §3.2.5

@T2 @wip
Feature: AECP stack — controller enumerates Milan listener descriptor tree

  Background:
    Given the full AECP listener pipeline is instantiated
    And the entity_id is 0x001BC5FFFE112233
    And the DUT is reset
    And controller "C1" has id 0xAABBCCDDEEFF0011

  Scenario: READ_DESCRIPTOR for ENTITY (type 0, index 0) returns SUCCESS
    When I send READ_DESCRIPTOR command_type=4 for config_index=0 descriptor_type=0 descriptor_index=0
    Then the response status is 0 (SUCCESS)
    And the response payload contains a non-zero entity_id

  Scenario: READ_DESCRIPTOR for CONFIGURATION (type 1, index 0) returns SUCCESS for configs 0, 1, 2
    When I send READ_DESCRIPTOR for config_index=0 descriptor_type=1 descriptor_index=0
    Then the response status is 0 (SUCCESS)
    When I send READ_DESCRIPTOR for config_index=0 descriptor_type=1 descriptor_index=1
    Then the response status is 0 (SUCCESS)
    When I send READ_DESCRIPTOR for config_index=0 descriptor_type=1 descriptor_index=2
    Then the response status is 0 (SUCCESS)

  Scenario: READ_DESCRIPTOR with out-of-range descriptor_index returns NO_SUCH_DESCRIPTOR
    When I send READ_DESCRIPTOR for config_index=0 descriptor_type=5 descriptor_index=99
    Then the response status is 2 (NO_SUCH_DESCRIPTOR)

  Scenario: GET_CONFIGURATION returns current_configuration_index
    When I send GET_CONFIGURATION
    Then the response status is 0 (SUCCESS)
    And the response configuration_index field is 0

  Scenario: SET_CONFIGURATION 2 then GET_CONFIGURATION returns 2
    When I send SET_CONFIGURATION with config_index=2
    And I send GET_CONFIGURATION
    Then the GET_CONFIGURATION response configuration_index is 2
