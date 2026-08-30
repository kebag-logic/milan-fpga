# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@torture @wire_truth @level:L3 @matrix:M-AAF-WIRE @matrix:M-CLK-2
Feature: AVTP wire truth - the declared format is the format on the wire
  The payload analyser (tb/tools/avtp_wire_truth.py) is the campaign's only
  check whose oracle is THE WIRE, and these scenarios are the desk half of it:
  every frame here is BUILT BY HAND from the figures in IEEE 1722-2016, not
  produced by our RTL, so if the analyser and the fabric ever disagree the
  disagreement is about the standard and not about taste.

  LEVEL / ORACLE (docs/testing/methodology.md). LEVEL 3 - conformance to the
  standard. ORACLE: THE CLAUSE, encoded as a hand-built byte vector. What this
  level CANNOT see: whether the fabric emits these bytes (that is L2,
  tb/verilator/milan_dp, and L5 on a tap). What it CAN see, and nothing else in
  the tree could before: whether the ANALYSER that will judge a real capture is
  itself right, and whether it can say NO.

  Clauses under test, quoted where the exact words matter:
    IEEE 1722-2016 Figure 26 - the AAF PCM AVTPDU layout.
    IEEE 1722-2016 Annex I.2.4.1 - the AAF stream_format qword, and the
      sentence the whole feature rests on: the format field "matches the
      setting of the channels_per_frame field in the Stream AVTPDU when this
      stream format is the current format for the stream".
    IEEE 1722-2016 7.3.3 - channels_per_frame is "a positive integer greater
      than zero (0)"; 7.3.4 - bit_depth "shall not be set to a value of zero"
      and not larger than the format's own width.
    IEEE 1722-2016 4.4.3.2 - "The 1-octet subtype field": the whole octet.
    IEEE 1722-2016 4.4.4.6 / 10.4.6 - sequence_num increments by one with
      wrapping; the CRF one is ONE OCTET and wraps FF -> 00.
    IEEE 1722-2016 Figure 72 + Milan v1.2 7.3.2 - "The base frequency shall be
      48000Hz. Each PDU shall contain 1 timestamp, and the timestamp interval
      shall be 96."
    Milan v1.2 7.3.3 - "An AVB Class A Stream Reservation shall be used to
      transmit" a CRF Media Clock Stream, so an untagged CRF frame is a
      finding.
    Milan v1.2 5.3.7.3 - a bound talker streams, so an unfed one owes SILENT
      FRAMES and not silence.
    IEEE 1722.1-2021 6.2.1 / 9.2.1.1.6 - the 82-octet ADPDU and the rule that
      control_data_length counts the octets after target_entity_id.

  Background:
    Given the wire-truth analyser is importable

  # ---------------------------------------------------------------- decoders
  @class:decoder
  Scenario: an AAF PCM AVTPDU decodes field for field off Figure 26
    Given a hand-built AAF frame with 4 channels sequence 7 timestamp 0x11223344
    Then the analyser reads channels_per_frame 4
    And the analyser reads sequence_num 7
    And the analyser reads avtp_timestamp 0x11223344
    And the analyser reads bit_depth 32 and nsr 5 and format 2
    And the analyser reads 6 sample events in the payload

  @class:decoder @regression
  Scenario: channels_per_frame survives the two-octet split
    # 7.3.3 is a TEN-bit field spanning octets 17 and 18 of the AVTPDU. A
    # decoder that reads one octet passes every stereo test ever written.
    Given a hand-built AAF frame with 261 channels sequence 0 timestamp 0
    Then the analyser reads channels_per_frame 261

  @class:decoder @regression
  Scenario: the subtype is the whole octet, so a control frame stays a control frame
    # IEEE 1722-2016 4.4.3.2 calls it "The 1-octet subtype field". Masking off
    # the top bit - the 1722-2011 cd bit - turns ADP (0xFA) into 0x7A, and the
    # ADP checks then silently never run. This scenario is the reason that mask
    # is not in the analyser.
    Given a hand-built ADPDU with available_index 1
    Then the analyser classifies the frame as ADP
    And the analyser counts 1 ADPDU

  @class:decoder
  Scenario: the ATDECC AAF stream_format qwords decode to their channel counts
    Then stream_format "0205022000806000" declares 2 channels
    And stream_format "0205022001006000" declares 4 channels
    And stream_format "0205022002006000" declares 8 channels
    And stream_format "0215022002006000" has the up-to bit set
    And stream_format "0205022001006000" declares 6 samples per frame

  @class:decoder @clause:Milan-7.3.2
  Scenario: the Milan CRF format string decodes to the Milan CRF parameters
    # Milan v1.2 Table 7.1 pins the whole format as one constant, and it only
    # decodes with a 29-bit base_frequency - which is how the field width was
    # settled rather than guessed from the prose.
    Then the Milan CRF stream format is 0x041060010000BB80
    And it decodes to type 1 interval 96 timestamps 1 pull 0 base 48000

  # ------------------------------------------------ declared versus emitted
  @class:invariant @clause:1722-I.2.4.1
  Scenario: a talker declaring 8 channels and emitting 2 is caught
    # The 2026-07-27 escape, reproduced on demand. Every gate in the repo was
    # green while this was true on the bench, because every gate compared a
    # declaration to another declaration.
    Given the controller was told the format is "0205022002006000"
    And a hand-built AAF frame with 2 channels sequence 0 timestamp 0
    When the analyser checks the declared format against the wire
    Then the analyser reports FAIL on "declared-vs-wire"
    And the mismatch names channels_per_frame

  @class:invariant @negative-control
  Scenario: the honest declaration passes the same check
    # A check that only ever fails proves as little as one that only ever
    # passes (methodology R2).
    Given the controller was told the format is "0205022000806000"
    And a hand-built AAF frame with 2 channels sequence 0 timestamp 0
    When the analyser checks the declared format against the wire
    Then every declared-vs-wire verdict is PASS

  @class:invariant @clause:1722-7.3.3 @clause:1722-7.3.4
  Scenario Outline: illegal header fields are reported, not rounded away
    Given a hand-built AAF frame that is illegal because <why>
    When the analyser checks header legality
    Then the analyser reports FAIL on "header-legal"
    And the violation mentions "<needle>"

    Examples:
      | why                          | needle                |
      | channels_per_frame is zero   | channels_per_frame 0  |
      | bit_depth is zero            | bit_depth 0           |
      | bit_depth exceeds the format | > format width        |

  # -------------------------------------------------------------- continuity
  @class:invariant @clause:1722-4.4.4.6
  Scenario: an AAF sequence_num gap is found and the 8-bit wrap is not one
    Given hand-built AAF frames with sequence numbers 254,255,0,1
    When the analyser checks sequence continuity
    Then every sequence verdict is PASS
    Given hand-built AAF frames with sequence numbers 1,2,4
    When the analyser checks sequence continuity
    Then the analyser reports FAIL on "seq-continuity"
    And the gap count is 1

  @class:invariant @clause:1722-10.4.6 @regression
  Scenario: the CRF sequence_num is one octet, so FF to 00 is a wrap
    # 10.4.6: "This field is to wrap from 11111111(2) to 00000000(2)". Read as
    # 16 bits it looks like a gap of -255 on every wrap, i.e. a healthy media
    # clock stream reporting a fault 195 times a second at 500 pps.
    Given hand-built CRF frames with sequence numbers 254,255,0
    When the analyser checks sequence continuity
    Then every sequence verdict is PASS

  # ------------------------------------------------------------- timestamps
  @class:invariant @clause:1722-7.5
  Scenario: the presentation time advances by exactly one AVTPDU of media
    Given hand-built AAF frames whose timestamps step by 125000 ns
    When the analyser checks the presentation timestamps
    Then the analyser reports PASS on "pts-step"
    And the expected step is 125000 ns

  @class:invariant @negative-control
  Scenario: a presentation time that steps four times too far is caught
    Given hand-built AAF frames whose timestamps step by 500000 ns
    When the analyser checks the presentation timestamps
    Then the analyser reports FAIL on "pts-step"

  @class:honesty @clause:methodology-R5
  Scenario: the class-A transit check SKIPS rather than inventing a timebase
    # A pcap timestamp is the capture host's CLOCK_REALTIME. Comparing it to an
    # AVTP timestamp yields a confident number that means nothing, which is
    # exactly the failure mode R5 forbids: a structural zero read as a
    # measurement.
    Given a hand-built AAF frame with 2 channels sequence 0 timestamp 0
    When the analyser checks the presentation timestamps
    Then the analyser reports SKIP on "class-a-transit"
    And the skip reason mentions "CLOCK_REALTIME"

  @class:invariant @clause:8021BA-class-A
  Scenario: with a gPTP reference supplied the 2 ms class-A window is enforced
    Given a gPTP reference of 1000000 ns
    And a hand-built AAF frame presented 1500000 ns after the reference
    When the analyser checks the presentation timestamps
    Then the analyser reports PASS on "class-a-transit"
    Given a gPTP reference of 1000000 ns
    And a hand-built AAF frame presented 9000000 ns after the reference
    When the analyser checks the presentation timestamps
    Then the analyser reports FAIL on "class-a-transit"

  # ------------------------------------------------------------------- VLAN
  @class:invariant @clause:8021Q-9.6 @regression
  Scenario: VID 0 is reported as its own defect, not as a generic mismatch
    # VID 0 frames leave the reserved SR tree: bridges strip the tag on egress
    # and the stream floods unshaped. It is a distinct failure from "the wrong
    # VID", so it gets its own field in the verdict.
    Given a hand-built AAF frame tagged with VID 0
    When the analyser checks the VLAN class
    Then the analyser reports FAIL on "c-tag-vid"
    And the verdict records that VID zero was seen

  @class:invariant @clause:Milan-7.3.3
  Scenario: an untagged CRF frame fails the class-A reservation requirement
    # Measured on this bench 2026-07-28: 4001 untagged CRF frames in 8 s
    # reached a port with no CRF listener, while zero AAF frames did. The
    # bridge was correct in both halves.
    Given a hand-built untagged CRF frame
    When the analyser checks the VLAN class
    Then the analyser reports FAIL on "crf.c-tag-present"

  @class:invariant @negative-control
  Scenario: conformant tags pass every VLAN check on both stream classes
    Given a hand-built AAF frame with 2 channels sequence 0 timestamp 0
    And a hand-built CRF frame
    When the analyser checks the VLAN class
    Then every VLAN verdict is PASS

  # -------------------------------------------------------------- zero fill
  @class:invariant @clause:Milan-5.3.7.3
  Scenario: an unfed bound talker owes silent FRAMES, and absence is not silence
    Given stream 0x0200000000020000 is declared bound but unfed
    And a hand-built silent AAF frame on stream 0x0200000000020000
    When the analyser checks zero fill
    Then every zero-fill verdict is PASS

  @class:invariant @clause:Milan-5.3.7.3 @negative-control
  Scenario: a declared-silent stream that sent nothing at all fails
    Given stream 0x0200000000020000 is declared bound but unfed
    When the analyser checks zero fill
    Then the analyser reports FAIL on "zero-fill-present"

  @class:invariant @negative-control
  Scenario: a fed stream carrying all zeros is the silence defect
    Given stream 0x0200000000020000 is declared fed
    And a hand-built silent AAF frame on stream 0x0200000000020000
    When the analyser checks zero fill
    Then the analyser reports FAIL on "fed-non-silent"

  # --------------------------------------------------------------- CRF rate
  @class:invariant @clause:Milan-7.3.2
  Scenario: 500 CRF PDUs a second is derived from the format, not measured first
    Given 101 hand-built CRF frames at 2 ms spacing
    When the analyser checks the CRF format and rate
    Then every CRF format verdict is PASS
    And the expected CRF rate is 500 PDUs per second
    And the analyser reports PASS on "crf.pdu-rate"

  @class:invariant @negative-control
  Scenario: a CRF timestamp_interval of 48 fails Milan 7.3.2
    Given a hand-built CRF frame with timestamp interval 48
    When the analyser checks the CRF format and rate
    Then the analyser reports FAIL on "crf.milan-format"

  # ------------------------------------------------------------------ ADP
  @class:invariant @clause:17221-6.2.1
  Scenario: the 82-octet ADPDU rule and the available_index that must advance
    Given hand-built ADPDUs with available indices 1,2,3
    When the analyser checks the ADP frame rule
    Then every ADP verdict is PASS
    And the built ADPDU frame is 82 octets

  @class:invariant @negative-control
  Scenario: a repeated available_index reads as an incoherent entity
    # Silicon-diagnosed 2026-07-12: bump-on-change-only made controllers treat
    # the entity as incoherent.
    Given hand-built ADPDUs with available indices 5,5,6
    When the analyser checks the ADP frame rule
    Then the analyser reports FAIL on "available-index-advances"

  @class:invariant @clause:17221-9.2.1.1.6 @regression
  Scenario: a frame that lies about its control_data_length is caught
    # The defect a status-byte-only tool cannot see at all: our SET/GET_NAME
    # lock path once declared 84 and put 20 octets on the wire.
    Given a hand-built ADPDU that claims control_data_length 200
    When the analyser checks control length honesty
    Then the analyser reports FAIL on "length-honest"
    And the liar's declared control_data_length is 200

  @class:honesty @negative-control
  Scenario: an empty capture is a FAIL, never a clean pass
    # The commonest false green on this bench: a mirror port that never joined
    # the stream multicast group returns control frames and nothing else.
    When the analyser checks the capture shape
    Then the analyser reports FAIL on "stream-frames-present"

  @class:decoder @regression
  Scenario: a ProfiShark tap capture only decodes with its 28-octet offset
    # Tap records carry a 28-byte header and keep the FCS. Reading such a file
    # without the offset yields zero AVTP
    # frames - and a check that treats "no frames" as a pass would call that
    # capture clean.
    Given a written pcap of 3 tap records with a 28 octet header and an FCS
    When the analyser reads it with the tap offset
    Then the analyser reports PASS on "stream-frames-present"
    When the analyser reads it without the tap offset
    Then the analyser reports FAIL on "stream-frames-present"

  @class:honesty @negative-control @rule:empty-collection-is-a-SKIP
  Scenario: an empty capture leaves NO check silent and NO check passing
    # THE EMPTY-COLLECTION RULE. On an empty capture eight of the twelve check
    # families used to emit NOTHING - so the log could not tell "did not apply"
    # from "was not run" - and wt.control.length-honest emitted PASS, because
    # `not []` is True over an empty list of liars. An empty capture is this
    # project's commonest false green, so: no check may PASS, and every family
    # must be REPRESENTED by a SKIP that names what was absent.
    When the analyser checks an empty capture end to end
    Then no check verdict is PASS
    And every check family is represented
    And every SKIP names what was absent
    And the capture-shape verdict is FAIL

  # ------------------------------------------------------- SRP, from the tap
  # MSRP (0x22EA) and MVRP (0x88F5) go to 01:80:C2:00:00:0E, which a bridge does
  # NOT forward. So the SRP exchange is invisible to the controller host and to
  # any mirror port: an INLINE TAP is the only place it can be seen, and
  # therefore the only place the Listener Ready half of the Milan v1.2 5.3.7.3
  # licence appears on the wire. This check set found a real fabric defect from
  # the wire alone - only 2 of 5 talker stream_ids declaring a Talker Advertise.
  @class:srp @clause:8021Q-35.2.2 @clause:Milan-5.3.7.2
  Scenario: the Talker Advertise FirstValue decodes to its 25 clause-defined octets
    # 802.1Q-2018 35.2.2.8: StreamID(8 = 6-octet MAC + 2-octet unique_id) +
    # DataFrameParameters(destination_address 6 + vlan_identifier 2) +
    # TSpec(MaxFrameSize 2 + MaxIntervalFrames 2) + PriorityAndRank(1) +
    # AccumulatedLatency(4) = 25 octets.
    Given a hand-built MSRP Talker Advertise for stream 0200000000020003
    When the analyser decodes the MRPDU
    Then the attribute is a Talker Advertise
    And the declared destination address is 91e0f000fe07
    And the declared vlan identifier is 2
    And the declared MaxFrameSize is 1024
    And the attribute is declaring

  @class:srp @clause:8021Q-35.2.2.8.2
  Scenario: a Listener attribute's declaration type rides the FourPackedEvents vector
    # 802.1Q-2018 35.2.2.8.2: the 8-octet Listener FirstValue is the StreamID
    # only; Ignore/Asking Failed/Ready/Ready Failed is two bits per value in a
    # SEPARATE vector. A decoder that reads it out of the value sees nothing.
    Given a hand-built MSRP Listener Ready for stream 0200000000020003
    When the analyser decodes the MRPDU
    Then the listener declaration is "Ready"

  @class:srp @clause:Milan-5.3.7.2 @regression
  Scenario: a talker Stream Output that never declares is found from the wire
    # Milan v1.2 5.3.7.2: "For each of the Stream Outputs of its currently set
    # Configuration, a PAAD shall always declare an MSRP Talker attribute as soon
    # as it has valid SRP parameters for this stream." Pass the entity's WHOLE
    # Stream Output set and the capture answers which of them never declared -
    # exactly how the 2-of-5 defect was found.
    Given the entity declares 5 talker stream ids from 0200000000020000
    And only stream 0200000000020000 and 0200000000020001 advertise
    When the analyser checks the SRP declarations
    Then the analyser reports FAIL on "talker-advertise-declared"
    And the missing declarations are named

  @class:srp @clause:Milan-5.3.7.3 @negative-control
  Scenario: frames on the wire with no Listener Ready are unreserved
    # 5.3.7.3 licenses a talker only while it is "receiving a Listener Ready or
    # Listener Ready Failed attribute for a Stream Output". An Asking Failed is
    # not that, so frames present anyway carry no reservation.
    Given a stream on the wire whose only Listener declaration is "Asking Failed"
    When the analyser checks the SRP declarations
    Then the analyser reports FAIL on "listener-declaration-present"

  @class:srp @clause:Milan-5.3.7.4 @negative-control
  Scenario Outline: the declaration and the frames must agree about <parameter>
    # Milan v1.2 5.3.7.4 makes the Stream Destination MAC Address and the Stream
    # VLAN ID SRP PARAMETERS of the Stream Output, so the declaration and the
    # tag are one value. A stream riding a DMAC or VID it never declared is
    # outside its own reservation.
    Given a stream whose wire <parameter> differs from its declaration
    When the analyser checks the SRP declarations
    Then the analyser reports FAIL on "<check>"

    Examples:
      | parameter | check                     |
      | dmac      | declared-dmac-matches-wire |
      | vid       | declared-vid-matches-wire  |

  @class:srp @clause:8021Q-35.2.2.9
  Scenario: a capture with no MRP frames says the tap is what is missing
    # A mirror port and the controller host can NEVER see these frames, so the
    # SKIP has to say so rather than reading as "nothing wrong here".
    Given a stream on the wire with no MRP frames captured at all
    When the analyser checks the SRP declarations
    Then every SRP verdict is SKIP
    And the SRP skip says an inline tap is required
