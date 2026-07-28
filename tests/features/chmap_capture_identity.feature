# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@chmap64 @identity @matrix:M-AAF-CHMAP @level:L3
Feature: Channel IDENTITY through the capture mux (rx -> talker loopback)
  LEVEL L3 - conformance to the standard. ORACLE: the clause. The model in
  steps/chmap_capture_steps.py is derived from IEEE 1722-2016 7.3.5 and NOT
  from the RTL, so if the RTL and this file disagree, one of them is wrong
  about the standard - which is the entire point of running both. (The same
  properties are checked at L0/L2 against the real packetizer's emitted
  AVTPDU bytes in tb/verilator/chmap_capture.)
  The property this project has never tested. Every audio result so far has
  been PRESENCE-shaped - a counter moved, audio was heard - and presence
  cannot tell a correct channel map from one that swapped L and R, duplicated
  a channel over its neighbour, or dropped one silently. It could not be
  tested before because the only multi-channel source on the boards emitted
  the SAME sample on every channel (the pilot tone is {tone, tone}) and the
  AX7101 has no audio input at all. The rx -> talker loopback source
  (docs/CHANNEL_MAP_64.md §5, capture SRC = 5) is the first source that
  carries per-channel-DISTINCT content, so identity is finally observable.

  Clauses under test:
    IEEE 1722-2016 7.3.5 - the AAF-PCM payload is a chronological sequence of
      sample events, each carrying one sample per channel IN CHANNEL ORDER,
      so payload sample k belongs to wire channel k mod channels_per_frame.
    IEEE 1722-2016 7.3.3 - channels_per_frame is carried ON THE WIRE. The
      de-interleave follows the wire, never the AEM store (1-to-1 wire truth).
    IEEE 1722.1-2021 7.2.19 - AUDIO_MAP entries are port-relative
      (stream_index, stream_channel) -> (cluster_offset, cluster_channel);
      the capture map is that mirror on the egress side, at pair granularity.
    Milan v1.2 es-4.16 - dynamic audio maps are the canonical programmer.

  Every sample driven here is DISTINCT per (stream, channel, sample event):
  a scenario that drove equal values on two channels could not fail on a swap.

  Background:
    Given a fabric capture mux with 32 pair slots over 8 RX streams of 8 channels

  # -- nominal identity -----------------------------------------------------
  @class:identity
  Scenario: a received stream's pairs land on the mapped slots, uncrossed
    When RX stream 3 delivers a 8-channel PDU of 2 sample events from event 1
    And I map capture slot 0 to RX stream 3 pair 0
    And I map capture slot 1 to RX stream 3 pair 1
    And I map capture slot 2 to RX stream 3 pair 2
    And I map capture slot 3 to RX stream 3 pair 3
    And the media tick walks the capture slots
    # 7.3.5: pair p is wire channels {2p, 2p+1} = {L, R}
    Then capture slot 0 carries RX stream 3 wire channels 0 and 1
    And capture slot 1 carries RX stream 3 wire channels 2 and 3
    And capture slot 2 carries RX stream 3 wire channels 4 and 5
    And capture slot 3 carries RX stream 3 wire channels 6 and 7
    And capture slot 0 L and R are different
    And capture slot 3 L and R are different
    And every emitted capture channel is distinct
    And no emitted capture channel is silent

  @class:identity
  Scenario: two different RX streams keep their own channels
    When RX stream 3 delivers a 8-channel PDU of 2 sample events from event 1
    And RX stream 5 delivers a 8-channel PDU of 2 sample events from event 1
    And I map capture slot 0 to RX stream 3 pair 1
    And I map capture slot 1 to RX stream 5 pair 1
    And the media tick walks the capture slots
    Then capture slot 0 carries RX stream 3 wire channels 2 and 3
    And capture slot 1 carries RX stream 5 wire channels 2 and 3
    And every emitted capture channel is distinct

  @class:identity
  Scenario: the same pair fanned out to two slots duplicates deliberately
    # fan-out is legal and must be exact - it is the ONE case where two
    # emitted channels may be equal, and it must be equal to the RIGHT thing
    When RX stream 2 delivers a 8-channel PDU of 2 sample events from event 1
    And I map capture slot 4 to RX stream 2 pair 2
    And I map capture slot 5 to RX stream 2 pair 2
    And the media tick walks the capture slots
    Then capture slot 4 carries RX stream 2 wire channels 4 and 5
    And capture slot 5 carries RX stream 2 wire channels 4 and 5
    And capture slot 4 L and R are different

  # -- 7.3.3 wire truth -----------------------------------------------------
  @class:wire_truth
  Scenario: the de-interleave follows the WIRE, not the AEM store
    Given the AEM store believes RX stream 1 carries 8 channels
    When RX stream 1 delivers a PDU carrying 8 channels of samples but declaring 2 on the wire
    And I map capture slot 0 to RX stream 1 pair 0
    And I map capture slot 1 to RX stream 1 pair 1
    And the media tick walks the capture slots
    # with 2 channels on the wire only pair 0 exists; believing the AEM store
    # would have filled pairs 1..3 with samples that are not there
    Then capture slot 0 L and R are different
    And capture slot 1 is silent

  @class:wire_truth
  Scenario: the pre-first-accept channel count 0 is read as 2
    When RX stream 4 delivers a PDU carrying 2 channels of samples but declaring 0 on the wire
    And I map capture slot 0 to RX stream 4 pair 0
    And I map capture slot 1 to RX stream 4 pair 1
    And the media tick walks the capture slots
    Then capture slot 0 L and R are different
    And capture slot 1 is silent

  # -- the two ways to be silent (§4) ---------------------------------------
  @class:absence
  Scenario: a DISABLED slot emits nothing, an unresolvable one emits silence
    When RX stream 3 delivers a 8-channel PDU of 2 sample events from event 1
    And I map capture slot 0 to RX stream 3 pair 0
    And I map capture slot 1 to RX stream 3 pair 1 DISABLED
    And I map capture slot 2 to RX stream 9 pair 0
    And I map capture slot 3 to RX stream 3 pair 5
    And the media tick walks the capture slots
    Then capture slot 0 L and R are different
    And capture slot 1 emits nothing at all
    And capture slot 2 is silent
    And capture slot 3 is silent

  @class:absence
  Scenario: a stream that has never delivered a PDU is silence, not garbage
    When I map capture slot 0 to RX stream 7 pair 0
    And the media tick walks the capture slots
    Then capture slot 0 is silent

  # -- the §5 map word ------------------------------------------------------
  @class:encoding
  Scenario Outline: the loopback map word is EN | SRC 5 | stream | pair
    Then the CSR word for RX stream <s> pair <p> is 0x<word>
    And the capture entry at slot 0 reads 0x000

    Examples:
      | s | p | word |
      | 0 | 0 | D000 |
      | 3 | 1 | D031 |
      | 7 | 3 | D073 |

  # -- the recorded scale technique -----------------------------------------
  @class:identity @walking_tone
  Scenario: a binary walking tone identifies 8 channels in 3 captures
    # channel N is driven ON in round b iff bit b of N is set, so each channel
    # reports its own index as a bit pattern; a swap makes two channels report
    # each other, a duplication makes two report the same, a dead channel
    # reports 0. This is the recorded way to do identity at N-channel scale.
    Given a fabric capture mux with 32 pair slots over 8 RX streams of 8 channels
    When I map capture slot 0 to RX stream 6 pair 0
    And I map capture slot 1 to RX stream 6 pair 1
    And I map capture slot 2 to RX stream 6 pair 2
    And I map capture slot 3 to RX stream 6 pair 3
    And I run a binary walking-tone identification over 8 channels of RX stream 6
    Then every channel reports its own index
    And it took 3 captures
