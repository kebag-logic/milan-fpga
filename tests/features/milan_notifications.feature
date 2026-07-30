# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Milan v1.2 §5.4.5 (Notifications), §5.4.4.18 (LOCK_ENTITY), §5.4.4.1 (ACQUIRE)
# 1722.1-2021 §9.2.7 (unsolicited notifications)
# Offline model: tests/steps/milan_conformance_steps.py

@milan_conformance @notifications
Feature: Milan unsolicited notifications and lock lifecycle

  Milan v1.2 §5.4.5 and IEEE 1722.1-2021 §9.2.7 define the unsolicited
  notification mechanism. The entity must notify all registered controllers
  when state changes, and must handle lock expiry and controller departure.

  Background:
    Given a fresh Milan notification model
    And the entity_id is 0x001BC5FFFE112233
    And controller "C0a" has id 0xAABBCCDDEEFF0011
    And controller "C0b" has id 0x1122334455667788
    And controller "C0c" has id 0xFFFFFFFFFFFFFFFF

  # --- Test 6.1: Multiple registered controllers ---

  Scenario: a state change notifies all registered controllers
    Given notif controllers "C0a" and "C0b" are registered for notifications
    When a state change event occurs
    Then controller "C0a" receives an unsolicited notification
    And controller "C0b" receives an unsolicited notification
    And the notification count is 2

  Scenario: an unregistered controller does not receive notifications
    Given controller "C0a" is registered for notifications
    And controller "C0b" is not registered
    When a state change event occurs
    Then controller "C0a" receives an unsolicited notification
    And controller "C0b" does not receive an unsolicited notification

  # --- Test 6.2: No notification to the requesting controller ---

  Scenario: the requesting controller does not get an unsolicited for its own command
    Given notif controllers "C0a" and "C0b" are registered for notifications
    When controller "C0a" sends a SET_NAME command
    Then controller "C0b" receives an unsolicited notification
    And controller "C0a" does not receive an unsolicited notification

  # --- Test 6.3: Automatic unlock notifications ---

  Scenario: lock expiry sends an unsolicited notification to registered controllers
    Given the notif entity is locked by "C0a"
    And controller "C0b" is registered for notifications
    When the lock timer expires after 60001 ticks
    Then the entity is unlocked
    And controller "C0b" receives an unsolicited notification

  Scenario: lock expiry does not notify if no controllers are registered
    Given the notif entity is locked by "C0a"
    And no controllers are registered for notifications
    When the lock timer expires after 60001 ticks
    Then the entity is unlocked
    And the notification count is 0

  # --- Test 6.4: Detection of departing controllers ---

  Scenario: a departing controller's registration is removed
    Given controller "C0a" is registered for notifications
    When controller "C0a" departs (ADP ENTITY_DEPARTING observed)
    Then controller "C0a" is removed from the notification registry
    And a subsequent state change does not notify controller "C0a"

  # --- Registration table limits ---

  Scenario: the notification registry has a bounded size
    Given 16 controllers are registered for notifications
    When a 17th controller attempts to register
    Then the notif model responds status 8 (NO_RESOURCES)

  Scenario: a deregistered controller can re-register
    Given controller "C0a" is registered for notifications
    When controller "C0a" deregisters
    Then controller "C0a" is not in the notification registry
    When controller "C0a" registers for notifications
    Then controller "C0a" is in the notification registry

  # --- Lock + notification interaction (Test 4.18) ---

  Scenario: a LOCK_ENTITY from the owner while locked reloads the timer
    Given the notif entity is locked by "C0a"
    When controller "C0a" sends a LOCK_ENTITY command
    Then the aecp_ext model responds status 0
    And the lock timer is reloaded

  Scenario: a SET command from a non-owner while locked returns ENTITY_LOCKED
    Given the notif entity is locked by "C0a"
    When controller "C0b" sends a SET_NAME command
    Then the notif model responds status 3 (ENTITY_LOCKED)
    And the entity is still locked
    And the locking controller is still "C0a"

  Scenario: a GET command from a non-owner while locked succeeds
    Given the notif entity is locked by "C0a"
    When controller "C0b" sends a GET_CONFIGURATION command
    Then the aecp_ext model responds status 0
