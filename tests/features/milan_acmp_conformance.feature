# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Milan v1.2 §5.5.2 (ACMP usage), §5.5.3 (Listener SM), §5.5.4 (Talker behaviour),
# §5.6.3 (ADP advertise SM)
# Offline model: tests/steps/milan_acmp_conformance_steps.py
# The models mirror:
#   hdl/ieee17221/acmp/acmp_pkg.sv          (status codes, state enum, timers)
#   hdl/ieee17221/acmp/KL_acmp_lstn_ctx.sv  (listener binding SM)
#   hdl/ieee17221/acmp/KL_acmp_tlkr_ctx.sv  (talker PROBE_TX responder)
#   hdl/ieee17221/adp/adp_advertiser.sv     (ADP advertise SM)

@milan_conformance @acmp
Feature: Milan ACMP connection management and ADP advertise conformance

  Milan v1.2 mandates a specific connection-management protocol that differs from
  base 1722.1 ACMP: BIND_RX replaces CONNECT_RX, PROBE_TX replaces CONNECT_TX,
  the talker is stateless (no connection tracking), the listener drives the SM
  autonomously via Auto Connect, and the ADP advertise SM has a fixed 5-second
  cadence with a random delay before each ADPDU.

  Background:
    Given a fresh Milan ACMP conformance model
    And the entity_id is 0x001BC5FFFE112233
    And the talker entity_id is 0x0200000000020001
    And controller "C0" has id 0xAABBCCDDEEFF0011
    And controller "C1" has id 0x1122334455667788

  # === §5.5.2.2: PDU format and naming ===

  Scenario: the Milan ACMPDU is 56 bytes (truncated PDU, §5.5.2.2)
    When the model builds a BIND_RX_COMMAND
    Then the ACMPDU is 56 bytes long
    And the ACMPDU message_type is 6 (BIND_RX_COMMAND)

  Scenario: BIND_RX_COMMAND is CONNECT_RX_COMMAND renamed (§5.5.2.2)
    When the model builds a BIND_RX_COMMAND
    Then the ACMPDU message_type is 6

  Scenario: UNBIND_RX_COMMAND is DISCONNECT_RX_COMMAND renamed (§5.5.2.2)
    When the model builds an UNBIND_RX_COMMAND
    Then the ACMPDU message_type is 8

  Scenario: PROBE_TX_COMMAND is CONNECT_TX_COMMAND renamed (§5.5.2.2)
    When the model builds a PROBE_TX_COMMAND
    Then the ACMPDU message_type is 0

  Scenario: GET_RX_STATE_COMMAND uses message_type 10
    When the model builds a GET_RX_STATE_COMMAND
    Then the ACMPDU message_type is 10

  # === §5.5.2.4: Controller Bind — the listener receives BIND_RX ===

  Scenario: a BIND_RX_COMMAND to a valid unbound sink returns SUCCESS
    Given the model has a sink at index 0 in state UNBOUND
    When the model receives a BIND_RX_COMMAND for sink 0 from "C0"
    Then the acmp response status is 0 (SUCCESS)
    And the acmp response connection_count is 1
    And the response FAST_CONNECT is 0
    And the sink state is PRB_W_RESP

  Scenario: a BIND_RX_COMMAND to an invalid sink returns LISTENER_UNKNOWN_ID
    When the model receives a BIND_RX_COMMAND for sink 99 from "C0"
    Then the acmp response status is 1 (LISTENER_UNKNOWN_ID)

  Scenario: a BIND_RX_COMMAND while locked by another controller returns CONTROLLER_NOT_AUTHORIZED
    Given the model has a sink at index 0 in state UNBOUND
    And the acmp entity is locked by "C0"
    When the model receives a BIND_RX_COMMAND for sink 0 from "C1"
    Then the acmp response status is 16 (CONTROLLER_NOT_AUTHORIZED)

  Scenario: a BIND_RX_COMMAND from the locking controller is accepted
    Given the model has a sink at index 0 in state UNBOUND
    And the acmp entity is locked by "C0"
    When the model receives a BIND_RX_COMMAND for sink 0 from "C0"
    Then the acmp response status is 0 (SUCCESS)

  # === §5.5.2.5: Controller Unbind ===

  Scenario: an UNBIND_RX_COMMAND to a bound sink returns SUCCESS and goes UNBOUND
    Given the model has a sink at index 0 in state SETTLED_RSV_OK
    When the model receives an UNBIND_RX_COMMAND for sink 0 from "C0"
    Then the acmp response status is 0 (SUCCESS)
    And the acmp response connection_count is 0
    And the sink state is UNBOUND

  Scenario: an UNBIND_RX_COMMAND while locked by another controller is rejected
    Given the model has a sink at index 0 in state SETTLED_RSV_OK
    And the acmp entity is locked by "C0"
    When the model receives an UNBIND_RX_COMMAND for sink 0 from "C1"
    Then the acmp response status is 16 (CONTROLLER_NOT_AUTHORIZED)

  # === §5.5.3.5.3: BIND_RX from UNBOUND sends PROBE_TX immediately ===

  Scenario: a successful BIND from UNBOUND immediately sends a PROBE_TX_COMMAND
    Given the model has a sink at index 0 in state UNBOUND
    When the model receives a BIND_RX_COMMAND for sink 0 from "C0"
    Then a PROBE_TX_COMMAND was sent to the talker
    And the PROBE_TX_COMMAND has FAST_CONNECT set to 1
    And the PROBE_TX_COMMAND has connection_count 0

  # === §5.5.3.5.18: PROBE_TX_RESPONSE handling ===

  Scenario: a successful PROBE_TX_RESPONSE settles the sink
    Given the model has a sink at index 0 in state PRB_W_RESP
    When the talker responds with PROBE_TX_RESPONSE status 0
    Then the sink state is SETTLED_NO_RSV
    And the sink has stream parameters set

  Scenario: a failed PROBE_TX_RESPONSE parks the sink in PRB_W_RETRY
    Given the model has a sink at index 0 in state PRB_W_RESP
    When the talker responds with PROBE_TX_RESPONSE status 5
    Then the sink state is PRB_W_RETRY

  # === §5.5.3.5.16/23: Probe timeout ===

  Scenario: the first probe timeout resends and goes to PRB_W_RESP2
    Given the model has a sink at index 0 in state PRB_W_RESP
    When the TMR_NO_RESP timer expires (200 ms)
    Then the sink state is PRB_W_RESP2
    And a duplicate PROBE_TX_COMMAND was sent

  Scenario: the second probe timeout goes to PRB_W_RETRY
    Given the model has a sink at index 0 in state PRB_W_RESP2
    When the TMR_NO_RESP timer expires (200 ms)
    Then the sink state is PRB_W_RETRY
    And the sink ACMP status is 7 (LISTENER_TALKER_TIMEOUT)

  # === §5.5.4.1: Talker PROBE_TX behaviour ===

  Scenario: the talker responds to PROBE_TX with SUCCESS and live stream params
    Given the talker has a valid source at index 0
    When the talker receives a PROBE_TX_COMMAND for source 0
    Then the talker responds with status 0 (SUCCESS)
    And the PROBE_TX_RESPONSE has a non-zero stream_id
    And the PROBE_TX_RESPONSE has a non-zero stream_dest_mac
    And the PROBE_TX_RESPONSE has FAST_CONNECT set

  Scenario: the talker responds to PROBE_TX for an invalid source with TALKER_UNKNOWN_ID
    When the talker receives a PROBE_TX_COMMAND for source 99
    Then the talker responds with status 2 (TALKER_UNKNOWN_ID)

  Scenario: the talker ignores STREAMING_WAIT and always streams when bandwidth is reserved
    Given the talker has a valid source at index 0
    When the talker receives a PROBE_TX_COMMAND for source 0 with STREAMING_WAIT set
    Then the talker responds with status 0 (SUCCESS)

  # === §5.5.2.7: Talker is stateless ===

  Scenario: the talker does not track bound listeners
    Given the talker has a valid source at index 0
    When the talker receives a PROBE_TX_COMMAND for source 0
    Then the talker connection_count is 0

  Scenario: a DISCONNECT_TX_COMMAND always returns SUCCESS without state change
    Given the talker has a valid source at index 0
    When the talker receives a DISCONNECT_TX_COMMAND for source 0
    Then the talker responds with status 0 (SUCCESS)

  # === §5.5.2.6: Auto Connect — the listener re-probes after talker departure ===

  Scenario: a talker departure during SETTLED_RSV_OK transitions to PRB_W_AVAIL
    Given the model has a sink at index 0 in state SETTLED_RSV_OK
    When the talker departs (EVT_TK_DEPARTED)
    Then the sink state is PRB_W_AVAIL

  Scenario: a talker reappearance during PRB_W_AVAIL triggers probing
    Given the model has a sink at index 0 in state PRB_W_AVAIL
    When the talker is discovered (EVT_TK_DISCOVERED)
    Then the sink state is PRB_W_DELAY

  Scenario: an SRP registration during SETTLED_NO_RSV transitions to SETTLED_RSV_OK
    Given the model has a sink at index 0 in state SETTLED_NO_RSV
    When the SRP Talker attribute is registered (EVT_TK_REGISTERED)
    Then the sink state is SETTLED_RSV_OK

  Scenario: an SRP unregistration during SETTLED_RSV_OK transitions to SETTLED_NO_RSV
    Given the model has a sink at index 0 in state SETTLED_RSV_OK
    When the SRP Talker attribute is unregistered (EVT_TK_UNREGISTERED)
    Then the sink state is SETTLED_NO_RSV

  # === §5.6.3: ADP advertise state machine ===

  Scenario: the ADP advertise timer is 5 seconds (§5.6.3.5.9)
    Then the ADP TMR_ADVERTISE value is 5 seconds

  Scenario: the ADP random delay is between 0 and 4 seconds (§5.6.3.5.3)
    Then the ADP TMR_DELAY range is 0 to 4 seconds

  Scenario: on link-up the ADP SM goes to DELAY (not WAITING)
    Given the ADP SM is in state DOWN
    When a LINK_UP event occurs
    Then the ADP SM is in state DELAY

  Scenario: on TMR_DELAY expiry the ADP SM sends ENTITY_AVAILABLE and goes to WAITING
    Given the ADP SM is in state DELAY
    When the TMR_DELAY timer expires
    Then an ADP ENTITY_AVAILABLE message is sent
    And the ADP SM is in state WAITING

  Scenario: on TMR_ADVERTISE expiry the ADP SM goes to DELAY
    Given the ADP SM is in state WAITING
    When the TMR_ADVERTISE timer expires
    Then the ADP SM is in state DELAY

  Scenario: on LINK_DOWN from WAITING the ADP SM goes to DOWN
    Given the ADP SM is in state WAITING
    When a LINK_DOWN event occurs
    Then the ADP SM is in state DOWN

  Scenario: on RCV_ADP_DISCOVER from WAITING the ADP SM goes to DELAY
    Given the ADP SM is in state WAITING
    When an ADP ENTITY_DISCOVER message is received
    Then the ADP SM is in state DELAY

  Scenario: on GM_CHANGE from WAITING the ADP SM goes to DELAY
    Given the ADP SM is in state WAITING
    When a GM_CHANGE event occurs
    Then the ADP SM is in state DELAY

  Scenario: on SHUTDOWN the ADP SM sends ENTITY_DEPARTING
    Given the ADP SM is in state WAITING
    When a SHUTDOWN event occurs
    Then an ADP ENTITY_DEPARTING message is sent

  # === §5.5.2.3: Command timeouts ===

  Scenario: all ACMP command timeouts are 200 ms
    Then the PROBE_TX_COMMAND timeout is 200 ms
    And the BIND_RX_COMMAND timeout is 200 ms
    And the UNBIND_RX_COMMAND timeout is 200 ms
    And the GET_RX_STATE_COMMAND timeout is 200 ms

  Scenario: the TMR_RETRY timeout is 4 seconds
    Then the TMR_RETRY timeout is 4000 ms

  Scenario: the TMR_NO_TK timeout is 10 seconds
    Then the TMR_NO_TK timeout is 10000 ms
