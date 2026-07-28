# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@milan @clause:5.3.7.3 @clause:5.3.7.2 @matrix:M-DEV-13c @srp
Feature: Milan v1.2 5.3.7.3 - the licence to stream is CONDITIONAL
  Verbatim, Milan Specification Consolidated v1.2 (2023-11-30) Section 5.3.7.3:

    "As long as a PAAD is declaring a Talker Advertise attribute and receiving a
     Listener Ready or Listener Ready Failed attribute for a Stream Output, it
     shall be streaming AVTP packets. This specification excludes the possibility
     for a Stream Output to be stopped (STREAMING_WAIT state shall not be
     implemented)."

  Two obligations, not one. The "shall be streaming" is gated on BOTH terms; the
  second sentence only forbids implementing STREAMING_WAIT. Section 5.3.7.2 keeps
  the Talker attribute unconditional - "a PAAD shall always declare an MSRP Talker
  attribute as soon as it has valid SRP parameters for this stream" - and lists the
  three registration states, of which only Ready / Ready Failed license streaming.

  This repo read 5.3.7.3 as an unconditional "never stop streaming" until
  2026-07-28 (traceability row M-DEV-13a said exactly that), and on that reading
  both boards shipped with the AAF admission gate BYPASSED: measured on the
  ProfiShark inline tap, 18,488 SR-class-A-tagged AAF frames in 6 s from a talker
  whose LWSRP_STATUS reported no Listener registration and a shut stream gate.

  These scenarios pin the clause against the RTL that implements it, so a future
  edit cannot quietly re-widen the condition. The wire evidence is a byte-exact
  MSRPDU captured from the certified bench bridge on 2026-07-28.

  Background:
    Given the lwSRP RTL sources

  @class:clause
  Scenario: listener_ready is exactly "Ready or Ready Failed", per 5.3.7.3
    When I read the listener_ready_o expression from KL_lwsrp_registrar
    Then it requires the Listener attribute to be registered
    And it accepts the declaration Ready
    And it accepts the declaration ReadyFailed
    And it rejects the declaration AskingFailed
    And it rejects the declaration Ignore

  @class:clause
  Scenario: the bandwidth gate's request term carries the licence
    When I read the req_w expression from KL_lwsrp_bw_gate
    Then the request requires talker_declared_i
    And the request requires listener_ready_i

  @class:clause @negative
  Scenario: the Talker attribute is declared unconditionally, per 5.3.7.2
    When I read the TalkerAdvertise inclusion term from KL_lwsrp_tx
    Then the Talker attribute does not depend on any Listener registration

  @class:structure @known-defect
  Scenario: every term that can open the AAF admission gate is accounted for
    When I read the aaf_gate expression from milan_datapath
    Then the gate has exactly one escape hatch and it is named cfg_aaf_bypass
    And with the escape hatch clear the gate requires the lwSRP stream gate
    And the escape hatch is recorded as a Milan 5.3.7.3 conformance defect

  @class:wire
  Scenario: the bench bridge declares Listener Ready for our StreamID
    Given the MSRPDU captured from the bench bridge on 2026-07-28
    Then it is a well-formed MRPDU whose every AttributeLength matches 802.1Q Table 35-1
    And it declares a Listener attribute for StreamID 0200000000010000
    And that Listener declaration is Ready
    And the SR class A domain is present as the +1 value of a B-first packed pair

  @class:wire @negative
  Scenario: the same capture is not mistaken for a licence when it withdraws
    Given the MSRPDU captured from the bench bridge on 2026-07-28
    When the Listener three-packed event is changed to Lv
    Then the Listener declaration is a withdrawal and licenses nothing
