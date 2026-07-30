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
  data lane, and the MSRP Talker Advertise - so these scenarios check the
  artifacts that have to agree, INCLUDING the interlock that makes the
  half-done state unreachable.

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

  @clause:8021Q-34.5 @clause:Milan-4.2.7.2.1
  Scenario: The stream carries the SR class A priority the bridge expects
    Then the SR class A priority is 3
    And the TalkerAdvertise PriorityAndRank octet is 0x70
    And the frame PCP and the declared priority are one constant
    And the frame VID and the declared VID are one wire

  @clause:8021Q-35.2.2.4
  Scenario: The TSpec describes the frame that is actually emitted
    Then the declared MaxFrameSize is Table 4.4's, and its reservation still covers the emitted frame
    And the declared MaxIntervalFrames is 1
    And the reservation fits the 75 percent class A budget on a 100 Mb link
    And the reservation fits the 75 percent class A budget on a 1000 Mb link
    And the reservation is over-provisioned by at least 16x the real rate

  @clause:8021Q-35.1.2 @negative
  Scenario: A tag can never exist without the declaration that justifies it
    Then the tag is derived from the provisioned reservation, not from a bare bit
    And a bare CSR request cannot tag the stream on its own

  @clause:Milan-7.3.3
  Scenario: The reservation names the stream the fabric actually emits
    Then the reservation row is provisioned by the fabric, not by software
    And the request retires only on the beat the engine sampled it

  @level:L1 @clause:Milan-7.3.3
  Scenario: The media clock stream leaves on the data lane, not the control merge
    Then the CRF AXIS is bound to the data lane, not the control merge

  @clause:Milan-5.3.7.3 @observability
  Scenario: A pruned reservation is readable, not a stream that silently vanished
    Then the reservation state is readable, not inferable from silence

  @negative @coverage-honesty
  Scenario: SR class B is not silently claimed by this change
    Then SR class B is still not reachable
