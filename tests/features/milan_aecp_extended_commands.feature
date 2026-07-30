# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Milan v1.2 §5.4.4 (AECP command set), §5.4.4.4 (SET_STREAM_INFO),
# §5.4.2.11 (START_STREAMING/STOP_STREAMING), §5.4.2.15 (GET_AVB_INFO),
# §5.4.2.14 (GET_AS_PATH)
# Offline model: tests/steps/milan_conformance_steps.py
# The model mirrors the AECP response builder's per-command behaviour.

@milan_conformance @aecp_extended
Feature: Milan AECP extended command coverage

  Milan v1.2 §5.4.4 mandates a specific set of AECP commands. This feature
  covers the commands not already tested in the item10 series: SET_STREAM_INFO
  (talker), GET_STREAM_INFO (listener), START_STREAMING / STOP_STREAMING,
  GET_AVB_INFO, GET_AS_PATH, and GET_MILAN_INFO.

  Background:
    Given a fresh Milan AECP extended model
    And the entity_id is 0x001BC5FFFE112233

  # --- SET_STREAM_INFO (Milan §5.4.4.4, Test 4.5) ---

  Scenario: SET_STREAM_INFO with MSRP_ACC_LAT succeeds on a STREAM_OUTPUT
    When the model processes SET_STREAM_INFO for descriptor_type 0x05 descriptor_index 0
    Then the aecp_ext model responds status 0
    And the model stream_info MSRP_acc_latency is updated

  Scenario: SET_STREAM_INFO on a STREAM_INPUT is refused
    When the model processes SET_STREAM_INFO for descriptor_type 0x04 descriptor_index 0
    Then the aecp_ext model responds status 2

  Scenario: SET_STREAM_INFO on an out-of-range index is refused
    When the model processes SET_STREAM_INFO for descriptor_type 0x05 descriptor_index 99
    Then the aecp_ext model responds status 2

  # --- GET_STREAM_INFO listener (Milan §5.4.4, Test 4.6) ---

  Scenario: GET_STREAM_INFO on a STREAM_INPUT returns the bound state
    Given a STREAM_INPUT at index 0 is not bound
    When the model processes GET_STREAM_INFO for descriptor_type 0x04 descriptor_index 0
    Then the aecp_ext model responds status 0
    And the stream_info has no bound talker

  Scenario: GET_STREAM_INFO on a bound STREAM_INPUT returns the talker identity
    Given a STREAM_INPUT at index 0 is bound to talker 0x0200000000020000
    When the model processes GET_STREAM_INFO for descriptor_type 0x04 descriptor_index 0
    Then the aecp_ext model responds status 0
    And the stream_info has bound talker 0x0200000000020000

  # --- START_STREAMING / STOP_STREAMING (Milan §5.4.2.11, Test 4.11) ---

  Scenario: START_STREAMING on a bound STREAM_INPUT succeeds
    Given a STREAM_INPUT at index 0 is bound to talker 0x0200000000020000
    When the model processes START_STREAMING for descriptor_type 0x04 descriptor_index 0
    Then the aecp_ext model responds status 0
    And the stream is started

  Scenario: START_STREAMING on an unbound STREAM_INPUT is refused
    Given a STREAM_INPUT at index 0 is not bound
    When the model processes START_STREAMING for descriptor_type 0x04 descriptor_index 0
    Then the aecp_ext model responds status 7

  Scenario: STOP_STREAMING on a started stream succeeds
    Given a STREAM_INPUT at index 0 is started
    When the model processes STOP_STREAMING for descriptor_type 0x04 descriptor_index 0
    Then the aecp_ext model responds status 0
    And the stream is stopped

  Scenario: STOP_STREAMING on an already-stopped stream still succeeds
    Given a STREAM_INPUT at index 0 is stopped
    When the model processes STOP_STREAMING for descriptor_type 0x04 descriptor_index 0
    Then the aecp_ext model responds status 0

  # --- GET_AVB_INFO (Milan §5.4.2.15, Test 4.13) ---

  Scenario: GET_AVB_INFO returns the interface state
    When the model processes GET_AVB_INFO
    Then the aecp_ext model responds status 0
    And the response contains a non-zero MAC address
    And the response contains an interface_index

  # --- GET_AS_PATH (Milan §5.4.2.14, Test 4.14) ---

  Scenario: GET_AS_PATH returns at least one hop for a bound stream
    Given a STREAM_INPUT at index 0 is bound
    When the model processes GET_AS_PATH for descriptor_type 0x04 descriptor_index 0
    Then the aecp_ext model responds status 0
    And the AS path has at least 1 hop

  Scenario: GET_AS_PATH on an unbound stream returns an empty path
    Given a STREAM_INPUT at index 0 is not bound
    When the model processes GET_AS_PATH for descriptor_type 0x04 descriptor_index 0
    Then the aecp_ext model responds status 0
    And the AS path has 0 hops

  # --- GET_MILAN_INFO (Milan §5.4.4.17, Test 4.17) ---

  Scenario: GET_MILAN_INFO returns the Milan capabilities
    When the model processes GET_MILAN_INFO
    Then the aecp_ext model responds status 0
    And the response contains a Milan version field

  # --- GET_COUNTERS (Milan §5.4.2.25, Test 4.15) ---

  Scenario: GET_COUNTERS on a STREAM_INPUT returns the 10 mandatory counters
    When the model processes GET_COUNTERS for descriptor_type 0x04 descriptor_index 0
    Then the aecp_ext model responds status 0
    And the response contains 10 counter values
    And the counters include MEDIA_LOCKED
    And the counters include MEDIA_UNLOCKED
    And the counters include STREAM_INTERRUPTED
    And the counters include SEQ_NUM_MISMATCH
    And the counters include MEDIA_RESET
    And the counters include TIMESTAMP_UNCERTAIN
    And the counters include UNSUPPORTED_FORMAT
    And the counters include LATE_TIMESTAMP
    And the counters include EARLY_TIMESTAMP
    And the counters include FRAMES_RX

  Scenario: GET_COUNTERS on a STREAM_OUTPUT returns the talker counters
    When the model processes GET_COUNTERS for descriptor_type 0x05 descriptor_index 0
    Then the aecp_ext model responds status 0
    And the response contains counter values
    And the counters include FRAMES_TX
