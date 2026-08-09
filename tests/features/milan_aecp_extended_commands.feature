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

  # --- asCapable is the 802.1AS variable, not a pdelay proxy (gh #64 J3) ---
  # IEEE 802.1AS-2020 10.2.5.1 defines asCapable as a per-port determination
  # that the two ends can interoperate via the 802.1AS protocol. IEEE
  # 1722.1-2021 7.4.40.2 carries it as the AVB info flags' AS_CAPABLE bit,
  # and Milan v1.2 Table 5.22 makes it a push trigger - so a proxy that
  # cannot fall is not just a wrong flag, it corrupts the notification law.

  Scenario: asCapable defaults false until the daemon leases a claim
    Then the AVB info AS_CAPABLE flag is clear
    And the AVB info flags are 0x06

  Scenario: a leased claim raises AS_CAPABLE
    Given the gPTP daemon leases asCapable true for 8 quarter-seconds
    Then the AVB info AS_CAPABLE flag is set
    And the AVB info flags are 0x07

  Scenario: a lapsed lease clears asCapable, and the propagation delay does not save it
    Given a measured propagation delay of 139114 ns
    And the gPTP daemon leases asCapable true for 2 quarter-seconds
    Then the AVB info AS_CAPABLE flag is set
    When the lease runs out
    Then the AVB info AS_CAPABLE flag is clear
    And the AVB info propagation delay is still 139114 ns

  Scenario: a zero propagation delay does not clear an asCapable claim
    Given a measured propagation delay of 0 ns
    And the gPTP daemon leases asCapable true for 8 quarter-seconds
    Then the AVB info AS_CAPABLE flag is set

  Scenario: a claim without a lease is not a claim
    Given the gPTP daemon leases asCapable true for 0 quarter-seconds
    Then the AVB info AS_CAPABLE flag is clear

  # --- GET_AS_PATH at depth (gh #64 J4) ---
  # 1722.1-2021 7.4.41.2: path_sequence is the clock identities of the LATEST
  # Announce's PathTrace TLV. Slot 0 is the grandmaster and is never stored
  # twice; a published length of 0 keeps the legacy derivation.

  Scenario: a published three-hop path is served in order
    Given the grandmaster clock identity is 0x001B21FFFE55AA00
    And AS path slot 1 is 0x3CC0C6FFFEFE0210
    And AS path slot 2 is 0xAABBCCFFFE001122
    When the daemon publishes an AS path of 3 entries
    And the model processes GET_AS_PATH for descriptor_type 0x04 descriptor_index 0
    Then the aecp_ext model responds status 0
    And the AS path has 3 hops
    And AS path entry 0 is the grandmaster
    And AS path entry 1 is 0x3CC0C6FFFEFE0210
    And AS path entry 2 is 0xAABBCCFFFE001122
    And the AS path control_data_length is 40

  Scenario: the served path saturates at eight entries
    Given AS path slots 1 through 7 are filled
    When the daemon publishes an AS path of 15 entries
    And the model processes GET_AS_PATH for descriptor_type 0x04 descriptor_index 0
    Then the AS path has 8 hops
    And the AS path control_data_length is 80

  Scenario: slot 0 is refused because the grandmaster is not stored twice
    Given AS path slot 1 is 0x3CC0C6FFFEFE0210
    When the daemon tries to commit AS path slot 0
    Then the commit is refused
    And AS path slot 1 still holds 0x3CC0C6FFFEFE0210

  Scenario: a re-publish of the same path still bumps the generation
    Given AS path slot 1 is 0x3CC0C6FFFEFE0210
    When the daemon publishes an AS path of 2 entries
    And the daemon publishes an AS path of 2 entries
    Then the AS path generation is 2

  Scenario: a published length of zero returns to the legacy derivation
    Given a STREAM_INPUT at index 0 is bound
    And AS path slot 1 is 0x3CC0C6FFFEFE0210
    When the daemon publishes an AS path of 2 entries
    And the daemon publishes an AS path of 0 entries
    And the model processes GET_AS_PATH for descriptor_type 0x04 descriptor_index 0
    Then the aecp_ext model responds status 0
    And the AS path has at least 1 hop

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
