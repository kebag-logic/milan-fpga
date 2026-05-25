# SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# BDD feature: KL_aecp_timers
# Spec refs: IEEE 1722.1-2021 §9.2.1.6; Milan v1.2 §5.4; aem-aecp.md §3.2.9

Feature: KL_aecp_timers — 1 kHz strobe, lock timer, counter throttle, staleness

  Background:
    Given the DUT is KL_aecp_timers
    And the DUT is reset

  Scenario: tick_1khz_o period is 125000 clock cycles at 125 MHz
    When I observe 10 consecutive tick_1khz_o pulses
    Then each inter-pulse gap is between 124900 and 125100 cycles

  Scenario: Lock timer expires after exactly 60000 ticks
    When I pulse lock_start_i
    And I advance 60000 tick_1khz_o pulses
    Then lock_expired_o is asserted within 2 clock cycles

  Scenario: Lock timer does not expire before 60000 ticks
    When I pulse lock_start_i
    And I advance 59999 tick_1khz_o pulses
    Then lock_expired_o remains low

  Scenario: lock_clear_i prevents lock_expired_o
    When I pulse lock_start_i
    And I advance 30000 tick_1khz_o pulses
    And I pulse lock_clear_i
    And I advance 60000 tick_1khz_o pulses
    Then lock_expired_o remains low

  Scenario: counter_gate_o fires every 1000 tick_1khz_o pulses
    When I observe 5 consecutive counter_gate_o pulses
    Then each inter-pulse gap in ticks is between 990 and 1010

  Scenario: stale_tick_o fires once per tick_1khz_o pulse
    When I observe 10 consecutive tick_1khz_o pulses
    Then stale_tick_o fires exactly once during each tick_1khz_o period
