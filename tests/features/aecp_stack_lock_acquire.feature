# SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# BDD feature: Stack-level LOCK/ACQUIRE round-trip
# Tier: T2 (integration — full AECP pipeline including common_parser + l0_state + response_builder)
# Spec refs: IEEE 1722.1-2021 §9.2.7, §9.2.8; Milan v1.2 §5.4; aem-aecp.md §5.3

@T2 @wip
Feature: AECP stack — LOCK and ACQUIRE entity round-trips with a simulated controller

  Background:
    Given the full AECP listener pipeline is instantiated
    And the entity_id is 0x001BC5FFFE112233
    And the DUT is reset
    And controller "C1" has id 0xAABBCCDDEEFF0011
    And controller "C2" has id 0x1122334455667788
    And the AECP protocol directory is "/home/alex/tsn-gen/protocols"

  Scenario: Controller C1 locks the entity and receives SUCCESS response
    When I inject a LOCK_ENTITY AECP frame from "C1" to entity 0x001BC5FFFE112233
    Then the DUT emits an AEM_RESPONSE on m_axis
    And the response message_type is 1 (AEM_RESPONSE)
    And the response sequence_id matches the command
    And the response status is 0 (SUCCESS)
    And the response target_entity_id matches the controller_entity_id of the command

  Scenario: Controller C2 fails to SET_NAME while entity is locked by C1
    Given a LOCK_ENTITY from "C1" has been processed
    When I inject a SET_NAME AECP frame from "C2"
    Then the DUT emits an AEM_RESPONSE with status 3 (ENTITY_LOCKED)

  Scenario: Lock auto-expires and C2 can then SET_NAME
    Given a LOCK_ENTITY from "C1" has been processed
    When the 1 kHz tick fires 60001 times
    And I inject a SET_NAME AECP frame from "C2"
    Then the DUT emits an AEM_RESPONSE with status 0 (SUCCESS)

  Scenario: ACQUIRE_ENTITY by C1 then C2 attempt returns ENTITY_ACQUIRED
    When I inject an ACQUIRE_ENTITY AECP frame from "C1"
    Then the response status is 0 (SUCCESS)
    When I inject an ACQUIRE_ENTITY AECP frame from "C2"
    Then the response status is 4 (ENTITY_ACQUIRED)

  Scenario: End-to-end sequence_id echo
    Given 20 consecutive LOCK_ENTITY commands from "C1" with sequence_ids 0–19
    When each command is injected
    Then each response echoes the corresponding sequence_id
