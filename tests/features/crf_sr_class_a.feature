# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@srp @crf @class_a @matrix:M-CLK-2 @matrix:SRP-1
Feature: CRF Media Clock Output is an SR class A stream (Milan v1.2 7.3.3)
  Milan v1.2 7.3.3 requires the media clock stream to be carried under an SRP
  reservation of the specified class, and 7.2.3 makes a CRF Media Clock Output
  MANDATORY on any AAF Media Listener with two or more AAF Media Inputs. Until
  2026-07-28 ours was neither declared nor tagged: measured on the bench that
  day, 4001 UNTAGGED AVTP/CRF frames in 8 s from our MAC - 500 pps, the
  KL_crf_tx rate - reached a port with no CRF listener, while ZERO AAF frames
  did. The bridge was correct in both halves (802.1Q 35.1.2: a declaration is
  what buys pruning toward registered Listeners; an undeclared multicast DMAC
  is just multicast and floods).

  Closing it is THREE things that only work together - the 802.1Q C-TAG, the
  data lane, and the MSRP Talker Advertise. The first two are still ours and
  are checked here. The THIRD is not: the lwSRP applicant, its TSpec
  provisioning, the Σ-slope gate and the tag/declaration interlock were
  resolved out of hdl/ieee8021q/srp/**, which no longer exists in this
  repository - the protocol-processor submodule declares the reservation now.
  Those scenarios were DELETED rather than repointed at RTL that cannot
  answer them; when the processor's declaration state is testable from this
  layer they come back against it.

  LEVEL AND ORACLE (docs/testing/methodology.md). Every scenario here is L3
  conformance-to-clause: the oracle is the CITED CLAUSE, and the subject read
  is the RTL source itself - no expected-byte table is retyped here, every
  number is resolved out of the emitter's own constants so a change to the
  frame breaks the reservation check. What this level CANNOT see: the frame
  on the wire (that is L2, tb/verilator/crf_tx + milan_dp NxN, byte-exact)
  and a bridge actually granting the reservation (L5, the silicon acceptance
  procedure - RTL green is not silicon fixed). The lane-binding scenario is
  L1 and says so in its own step: its wire form is CRF jitter under a
  controller enumeration burst, measured at the tap.

  Background:
    Given the CRF talker RTL

  @clause:8021Q-9.5 @clause:8021Q-9.6
  Scenario: The tagged frame is a well-formed 802.1Q C-TAG
    Then the CRF emitter builds an 802.1Q C-TAG with TPID 0x8100 at octet 12
    And the TCI is {PCP, DEI, VID} with DEI 0
    And the EtherType moves to octet 16 in the tagged shape
    And the PCP and VID are wires, not literals

  @clause:8021Q-9.5 @regression
  Scenario: The tag replaces pad, it does not resize the frame
    Then both frame shapes are the same 60-octet frame

  @level:L1 @clause:Milan-7.3.3
  Scenario: The media clock stream leaves on the data lane, not the control merge
    Then the CRF AXIS is bound to the data lane, not the control merge
