# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@tsn_gen
Feature: Milan v1.2 ACMP listener state machine driven by tsn_gen ACMPDUs
  ACMP frames come from tsn-gen packet_gen rendering the repo's own ACMPDU
  protocol YAML (tests/protocols/acmp — tsn-gen carries no ACMP definition);
  field patches are bit-exact and verified through packet_gen --decode. The
  listener model mirrors KL_acmp_listener (pipewire acmp-milan-v12.c
  contract; the RTL is verified by tb/verilator/acmp_lstn, 89 checks).

  Background:
    Given the tsn_gen packet generator is available

  Scenario: BIND_RX binds, answers Table 5.32 and probes the talker
    Given tsn_gen generated a ACMP frame with seed 11
    And the Milan listener model adopts the frame's listener entity id
    When I patch field "message_type" to 6
    And I patch field "status" to 0
    And I patch field "listener_unique_id" to 0
    And I patch field "flags" to 0x0002
    Then tsn_gen decodes every patched field back
    And our field extractor agrees with tsn_gen on every field
    When the frame is delivered to the listener model
    Then the listener responds message_type 7 with status 0
    And the response connection_count is 1
    And the response stream fields are zero
    And the response clears FAST_CONNECT and SRP_REGISTRATION_FAILED
    And the listener state is PRB_W_RESP
    And a PROBE_TX command was emitted to the bound talker
    And the probe sequence id was 0

  Scenario: full walk — bind, probe answer, SRP settle, unbind
    Given tsn_gen generated a ACMP frame with seed 11
    And the Milan listener model adopts the frame's listener entity id
    When I patch field "message_type" to 6
    And I patch field "listener_unique_id" to 0
    And the frame is delivered to the listener model
    Then the listener state is PRB_W_RESP
    When the talker answers the probe with status 0 stream_id 0x0200000000010000 dmac 0x91E0F000FE01 vlan 2
    Then the listener state is SETTLED_NO_RSV
    And the listener sink is active
    And the bound stream vlan is 2
    When the TalkerAdvertise registrar reports registered
    Then the listener state is SETTLED_RSV_OK
    When I patch field "message_type" to 10
    And the frame is delivered to the listener model
    Then the listener responds message_type 11 with status 0
    And the response connection_count is 1
    And the response talker matches the bound talker
    When I patch field "message_type" to 8
    And the frame is delivered to the listener model
    Then the listener responds message_type 9 with status 0
    And the response connection_count is 0
    And the response talker entity id is zero
    And the response stream fields are zero
    And the listener state is UNBOUND
    And the listener sink is inactive

  Scenario: reservation loss after settle re-enters the probe path
    Given tsn_gen generated a ACMP frame with seed 12
    And the Milan listener model adopts the frame's listener entity id
    When I patch field "message_type" to 6
    And I patch field "listener_unique_id" to 0
    And the frame is delivered to the listener model
    And the talker answers the probe with status 0 stream_id 0x0200000000010000 dmac 0x91E0F000FE01 vlan 2
    And the TalkerAdvertise registrar reports registered
    Then the listener state is SETTLED_RSV_OK
    When the TalkerAdvertise registrar reports unregistered
    Then the listener state is PRB_W_AVAIL
    And the listener sink is inactive

  Scenario: probe rejection parks the listener in the retry state
    Given tsn_gen generated a ACMP frame with seed 13
    And the Milan listener model adopts the frame's listener entity id
    When I patch field "message_type" to 6
    And I patch field "listener_unique_id" to 0
    And the frame is delivered to the listener model
    And the talker answers the probe with status 5 stream_id 0 dmac 0 vlan 0
    Then the listener state is PRB_W_RETRY
    And the listener sink is inactive

  Scenario: nonzero listener_unique_id answers LISTENER_UNKNOWN_ID
    Given tsn_gen generated a ACMP frame with seed 14
    And the Milan listener model adopts the frame's listener entity id
    When I patch field "message_type" to 6
    And I patch field "listener_unique_id" to 5
    Then tsn_gen decodes every patched field back
    When the frame is delivered to the listener model
    Then the listener responds message_type 7 with status 1
    And the listener state is UNBOUND

  Scenario: frames for another listener are ignored
    Given tsn_gen generated a ACMP frame with seed 15
    And a Milan listener model with entity id 0x020000FFFE000003
    When I patch field "message_type" to 6
    And I patch field "listener_unique_id" to 0
    And the frame is delivered to the listener model
    Then the listener ignores the frame
    And the listener state is UNBOUND

  Scenario: seeded fuzz — 30 random ACMPDUs never confuse the dispatcher
    Given a Milan listener model with entity id 0x020000FFFE000003
    When I deliver 30 tsn_gen ACMP frames with seeds 200 to 229 to the listener model
    Then only listener commands addressed to the model were answered
