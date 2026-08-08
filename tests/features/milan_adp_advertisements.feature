# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Milan v1.2 §5.2 (ADP), §5.6.3 (ADP timings), IEEE 1722.1-2021 §6.2 (ADPDU format)
# Offline model: tests/steps/milan_conformance_steps.py
# The model mirrors hdl/ieee17221/adp/adp_advertiser.sv and KL_adp_parser.sv.

@milan_conformance @adp
Feature: Milan ADP advertisement format, timing, and grandmaster reaction

  The ADP advertiser in fabric (adp_advertiser.sv) shall:
  - send ENTITY_AVAILABLE with control_data_length = 56 (1722.1 §6.2.4)
  - advertise at intervals between 4.5s and 9.5s (Milan v1.2 §5.6.3.5.9,
    valid_time/2 = 10/2 = 5s, MAX(1, valid_time/2) seconds per 1722.1 Fig 6-2)
  - increment available_index on every ENTITY_AVAILABLE (1722.1 §6.2.4.2)
  - set the gPTP grandmaster identity fields from the current GM (Milan §5.6.3.5)
  - re-advertise on GM_CHANGE with index bump (Milan §5.6.3.5.3)
  - respond to ENTITY_DISCOVER within the mandated window

  Background:
    Given a fresh Milan ADP advertiser model
    And the entity_id is 0x001BC5FFFE112233
    And the station MAC is 02:00:00:00:00:01

  # --- ADPDU format (Test 2.1 offline analysis) ---

  Scenario: a spontaneously transmitted ADPDU has the correct L2/L3 format
    When the advertiser transmits an ADPDU
    Then the ADPDU destination MAC is 91:e0:f0:01:00:00
    And the ADPDU EtherType is 0x22F0
    And the ADPDU has no VLAN tag
    And the ADPDU cd field is 1
    And the ADPDU subtype is 0x7A
    And the ADPDU sv field is 0
    And the ADPDU version is 0
    And the ADPDU message_type is 0 (ENTITY_AVAILABLE)
    And the ADPDU control_data_length is 56

  Scenario: the available_index increments on every ENTITY_AVAILABLE
    When the advertiser transmits 3 consecutive ADPDUs
    Then the first ADPDU has available_index 0
    And the second ADPDU has available_index 1
    And the third ADPDU has available_index 2

  Scenario: the available_index wraps from 255 to 0
    Given the advertiser has already sent 255 ADPDUs
    When the advertiser transmits an ADPDU
    Then the ADPDU has available_index 255
    When the advertiser transmits an ADPDU
    Then the ADPDU has available_index 0
    When the advertiser transmits an ADPDU
    Then the ADPDU has available_index 1

  # --- Advertisement timing (Milan v1.2 §5.6.3.5.9, 1722.1 Fig 6-2) ---

  Scenario: the advertisement interval is MAX(1, valid_time/2) seconds
    Given the valid_time field is 10
    When the advertiser transmits over a 60 second observation window
    Then the interval between consecutive ADPDUs is at most 9.5 seconds
    And the interval between consecutive ADPDUs is at least 4.5 seconds
    And at least 2 ADPDUs are transmitted in a 60 second window

  Scenario: the first ADPDU after link-up arrives within 9.5 seconds
    When the advertiser is started from link-up
    Then the first ADPDU is transmitted within 9.5 seconds

  # --- Grandmaster change (Milan v1.2 §5.6.3.5.3) ---

  Scenario: a GM_CHANGE triggers an immediate re-advertise with index bump
    Given the advertiser has transmitted an ADPDU with available_index 5
    When a gPTP grandmaster change event arrives
    Then the advertiser transmits an ADPDU immediately
    And the ADPDU available_index is 6

  Scenario: a GM_CHANGE does not reset the available_index sequence
    Given the advertiser has transmitted an ADPDU with available_index 100
    When a gPTP grandmaster change event arrives
    Then the ADPDU available_index is 101

  # --- ENTITY_DEPART (Milan v1.2 §5.6.3.5.6) ---

  Scenario: an ENTITY_DEPART is sent when the entity goes offline
    When the entity is commanded to depart
    Then the advertiser transmits a message_type 1 (ENTITY_DEPARTING)
    And the ENTITY_DEPARTING has control_data_length 56

  # --- ENTITY_DISCOVER response (1722.1 §6.2.3) ---

  Scenario: the advertiser responds to ENTITY_DISCOVER within the observation window
    When an ENTITY_DISCOVER message is received
    Then the advertiser transmits an ADPDU within 2 seconds
    And the ADPDU message_type is 0 (ENTITY_AVAILABLE)

  # --- TMR_ADVERTISE restarts on EVERY send (Milan v1.2 §5.6.3.5.9 step 2,
  #     §5.6.3.5.4 step 1: the discover response is itself an ENTITY_AVAILABLE
  #     send, so the periodic cadence re-bases from the response, not from the
  #     pre-discover schedule) ---

  Scenario: a discover response restarts the advertise timer
    Given the valid_time field is 10
    And the advertise timer has 1 second left to run
    When an ENTITY_DISCOVER message is received
    Then the ADPDU message_type is 0 (ENTITY_AVAILABLE)
    And the next periodic ADPDU arrives a full advertise interval later
    And the interval between consecutive ADPDUs is at most 9.5 seconds
    And the interval between consecutive ADPDUs is at least 4.5 seconds

  # --- Milan v1.2 §5.6.3.5.2 arming is level-triggered, not edge ---

  Scenario: an enabled entity advertises without requiring a pulse
    Given the advertiser is enabled
    When the advertiser is started from link-up
    Then the advertiser transmits ADPDUs at the mandated cadence
    And no explicit arm pulse is required
