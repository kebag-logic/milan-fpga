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

  WHAT LEFT WITH THE lwSRP RTL. The applicant/registrar/bw-gate engine under
  hdl/ieee8021q/srp/** has been deleted; the protocol-processor submodule
  declares now, and milan_datapath drives lwsrp_stream_gate from the
  processor's admitted vector. Three @class:clause scenarios (listener_ready_o,
  the bw-gate req_w, the unconditional TalkerAdvertise inclusion) resolved out
  of that RTL's own expressions and went with it. So did @matrix:M-DEV-13d:
  its subject was the fabric provisioner srp_fab_want_v_w / srp_fab_launch_w,
  which no longer exists - there is no row for the fabric to provision. The
  remaining scenarios read only what still ships: the AAF admission
  composition in milan_datapath, the t>0 identity in KL_aaf_packetizer, and
  the bench capture.

  Background:
    Given the Milan datapath and AAF talker RTL sources

  @class:structure @known-defect
  Scenario: every term that can open the AAF admission gate is accounted for
    When I read the aaf_gate expression from milan_datapath
    Then the gate has exactly one escape hatch and it is named cfg_aaf_bypass
    And with the escape hatch clear the gate requires the lwSRP stream gate
    And the escape hatch is recorded as a Milan 5.3.7.3 conformance defect

  @class:structure @matrix:M-DEV-13e
  Scenario: a talker above 0 egresses on the SRP licence alone, with its own identity
    # The 0x001F round. 0x001E gave every talker row a DECLARATION and the
    # streams still never left, because two more pieces of per-talker state
    # had the same root cause - only the 0x800 window writes them, and no
    # board software drives that window. Silicon m001g: the bind soak's t0
    # leg fully green (listener FRAMES_RX ~18k/s) while t1/t2/t3 sat at zero
    # frames despite CONNECT SUCCESS, declared SRP rows and tu=0.
    When I read the t>0 AAF admission expression from milan_datapath
    # (1) ADMISSION. The per-context TCTX CTRL[0] shadow reset to 0, so on a
    # shape-static build no talker above 0 could EVER egress. It is deleted,
    # not inverted: 1722.1-2021 Table 8-4 bit 12 makes STREAMING_WAIT an
    # OPTION, Milan 5.4.2.19/5.4.2.20 require NOT_SUPPORTED for START_/
    # STOP_STREAMING on a Stream Output, 5.3.7.3 "excludes the possibility
    # for a Stream Output to be stopped", and 5.5.4.1 says a Talker "shall
    # always stream AVTP packets as long as bandwidth is reserved". A
    # per-stream software enable is not ours to have.
    Then the t>0 admission does NOT require a per-context runtime enable
    # ...and the lwSRP gate is REQUIRED, with no engine-off escape:
    # LWSRP_CTRL resets to engine-OFF, so mirroring t0's ~cfg_lwsrp_enable
    # escape would admit unpaced PROBE_TX-only streams straight out of reset
    # (the ~56 kframe/s blast that takes the peer board off the network).
    And the t>0 admission requires the lwSRP stream gate unconditionally
    And the effective t>0 admission is masked by output mapping reservations
    # (2) IDENTITY. The packetizer read dmac/VID/unique_id for t>0 from that
    # same never-written window, so an armed talker framed to dmac all-zeros
    # on VID 0 with stream_id {station_mac, uid 0} - colliding with t0 and
    # reaching no listener - while its own SRP row declared {station_mac,
    # uid t} and the ACMP answer promised dmac base+t.
    When I read the t>0 wire identity from KL_aaf_packetizer
    Then the t>0 identity is derived from the same roots the declaration uses
    And software may still name each identity field explicitly

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
