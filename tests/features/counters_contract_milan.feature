# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@torture @counters @level:L3 @matrix:M-AECP-COUNTERS @cmd:GET_COUNTERS
Feature: GET_COUNTERS is a contract - the mask, the layout and the invariants
  Everything a controller learns about a stream's health arrives through
  GET_COUNTERS, and every part of that answer is a place to be silently wrong:
  the mask can claim a counter nothing drives, the block can put a value at the
  neighbouring offset, and the invariants Milan states in prose can hold in the
  fabric and not in the reader. These scenarios pin all three, and they pin the
  three READING TRAPS that have already cost this project time.

  LEVEL / ORACLE (docs/testing/methodology.md). LEVEL 3 for the clause work -
  ORACLE: the clause, quoted below. The last two scenarios are LEVEL 1: they
  read the RTL source and assert the masks the fabric EMITS are the ones this
  contract names, so a mask drift in the response builder breaks a desk gate
  instead of waiting for a controller to notice.

  THE THREE READING TRAPS, each with the evidence.

  (1) THE BIT NUMBERING IS MSB-FIRST IN THE TABLE AND LSB-FIRST ON THE WIRE.
      IEEE 1722.1-2021 Table 7-156 lists "Bit # 31 ... MEDIA_LOCKED", and
      MEDIA_LOCKED is the counter at counters_block offset 0. Table 6-2 numbers
      entity_capabilities the same way, and there the "Bit # 31" entry is
      EFU_MODE - the flag every implementation writes as 1u << 0. So the table's
      bit number is 31 - offset/4 and the wire mask is 1 << offset/4. A reader
      who takes the table literally inverts every mask, and then a device
      serving the mandatory ten looks like one serving eight entity-specific
      counters.

  (2) STREAM_OUTPUT HAS TWO LAYOUTS AND THEY ARE NOT COMPATIBLE.
      Milan v1.2 Table 5.4 defines FIVE counters densely: STREAM_START,
      STREAM_STOP, MEDIA_RESET, TIMESTAMP_UNCERTAIN, FRAMES_TX.
      IEEE 1722.1-2021 Table 7-159 defines EIGHT, with STREAM_INTERRUPTED at
      the third slot and FRAMES_TX at the eighth. The same NAME therefore sits
      at a different offset in the two tables, so a decoder that picks the
      wrong one reports our FRAMES_TX as TIMESTAMP_UNCERTAIN. This is not a
      hypothetical: la_avdecc carries both enums side by side
      (StreamOutputCounterValidFlagMilan12 and StreamOutputCounterValidFlag17221)
      precisely because a device serves one or the other.

  (3) FRAMES_RX / FRAMES_TX MEAN TWO DIFFERENT THINGS, A FACTOR OF ~8000 APART.
      IEEE 1722.1-2021 Table 7-157: FRAMES_RX "Increments on each Stream data
      AVTPDU received".
      Milan v1.2 Table 5.6: FRAMES_RX is "Incremented at the end of every
      observation interval during which at least one Stream Data AVTPDU has
      been received on this Stream Input. The duration of the observation
      interval is implementation-specific and shall be less than or equal to 1
      second."
      Both are legitimate; they differ by the frame rate. So TV + TNV ==
      FRAMES_RX is a 1722.1 identity and NOT a Milan one, and a checker that
      asserts it unconditionally files a conformant interval counter as an
      8000x defect. The model here reports WHICH READING is in force instead.

  Clauses under test:
    Milan v1.2 5.3.8.10 + Table 5.6 - the ten Stream Input counters, the lock
      invariant, and the reset on not-bound -> bound.
    Milan v1.2 5.3.7.7 + Table 5.4 - the five Stream Output counters and the
      STREAM_START/STREAM_STOP invariant.
    Milan v1.2 5.4.2.25 - GET_COUNTERS is implemented for each descriptor.
    IEEE 1722.1-2021 7.4.42.2.2/.4/.5 + Tables 7-152/7-156/7-158 - the
      counters_valid fields; Tables 7-153/7-157/7-159 - the block offsets.

  Background:
    Given the counters contract is importable

  # ------------------------------------------------------- the counter tables
  @class:table @clause:Milan-Table-5.6
  Scenario: Milan Table 5.6 is exactly ten counters, in the 1722.1 block order
    Then the Milan Stream Input counter set has 10 members
    And the Milan Stream Input counter set is
      | counter             |
      | MEDIA_LOCKED        |
      | MEDIA_UNLOCKED      |
      | STREAM_INTERRUPTED  |
      | SEQ_NUM_MISMATCH    |
      | MEDIA_RESET         |
      | TIMESTAMP_UNCERTAIN |
      | UNSUPPORTED_FORMAT  |
      | LATE_TIMESTAMP      |
      | EARLY_TIMESTAMP     |
      | FRAMES_RX           |
    And the Milan Stream Input mandatory wire mask is 0xF3F

  @class:table @clause:Milan-Table-5.4
  Scenario: Milan Table 5.4 is exactly five counters and its mask is 0x01F
    Then the Milan Stream Output counter set has 5 members
    And the Milan Stream Output wire mask is 0x01F
    And the Milan Stream Output counter set is
      | counter             |
      | STREAM_START        |
      | STREAM_STOP         |
      | MEDIA_RESET         |
      | TIMESTAMP_UNCERTAIN |
      | FRAMES_TX           |

  @class:table @clause:17221-Table-7-157
  Scenario: the 1722.1 Stream Input block adds the two tv tallies, so the mask is 0xFFF
    Then the IEEE Stream Input block has 12 members
    And the IEEE Stream Input full wire mask is 0xFFF
    And TIMESTAMP_VALID is at block offset 24
    And TIMESTAMP_NOT_VALID is at block offset 28
    And FRAMES_RX is at block offset 44

  # ------------------------------------------------------- trap 1: numbering
  @class:trap @clause:17221-Table-7-156 @regression
  Scenario: the table's bit number is 31 minus the block slot
    # Read the table literally and every mask inverts.
    Then the IEEE table bit number for block offset 0 is 31
    And the IEEE table bit number for block offset 44 is 20
    And the IEEE table bit number for block offset 124 is 0
    And a block offset that is not quadlet aligned is refused

  @class:trap @clause:17221-Table-6-2
  Scenario: the same numbering is what makes entity_capabilities bit 31 the value 1
    # Table 6-2 lists "Bit # 31 ... EFU_MODE", and EFU_MODE is 0x00000001 in
    # every implementation - that is the fact that settles the convention
    # rather than an opinion about how IEEE numbers bits.
    Then the table bit number 31 corresponds to wire mask 0x00000001
    And the table bit number 0 corresponds to wire mask 0x80000000

  # -------------------------------------------------------- trap 2: layouts
  @class:trap @clause:Milan-Table-5.4 @clause:17221-Table-7-159 @regression
  Scenario: the two Stream Output layouts put the same name at different offsets
    Then in the Milan layout FRAMES_TX is at slot 4
    And in the IEEE layout FRAMES_TX is at slot 7
    And in the Milan layout MEDIA_RESET is at slot 2
    And in the IEEE layout MEDIA_RESET is at slot 3
    And decoding a Milan Stream Output block with the IEEE layout mislabels FRAMES_TX

  # -------------------------------------------------------- the mask itself
  @class:mask @clause:Milan-5.3.8.10
  Scenario: a claimed slot the layout cannot name is reported, not dropped
    Given a GET_COUNTERS payload for descriptor 5 index 3 claiming mask 0x100F3F
    When the contract decodes it as a Stream Input block
    Then the decode reports claimed-but-unnamed slot 20

  @class:mask @clause:methodology-R5
  Scenario: an unclaimed counter is ABSENT from the decode, never zero
    # R5: a structural zero is not a measurement. A counter block that reads
    # zero because nothing drives it is indistinguishable from a healthy idle
    # one, so an unclaimed slot must not appear at all.
    Given a GET_COUNTERS payload for descriptor 5 index 0 claiming mask 0x001
    When the contract decodes it as a Stream Input block
    Then the decode names only MEDIA_LOCKED

  @class:mask @negative-control
  Scenario: a truncated counters payload is refused rather than half-decoded
    Given a GET_COUNTERS payload truncated to 12 octets
    Then decoding it raises

  # -------------------------------------------------------- the invariants
  @class:invariant @clause:Milan-Table-5.6
  Scenario Outline: the Milan lock invariant admits exactly two states
    Given MEDIA_LOCKED <locked> and MEDIA_UNLOCKED <unlocked>
    Then the lock invariant verdict is <verdict>

    Examples: the two legal states and the two illegal ones
      | locked | unlocked | verdict |
      | 4      | 4        | PASS    |
      | 5      | 4        | PASS    |
      | 6      | 4        | FAIL    |
      | 3      | 4        | FAIL    |

  @class:invariant @clause:Milan-Table-5.6
  Scenario: the lock invariant also says WHICH state the stream is in
    # "MEDIA_LOCKED=MEDIA_UNLOCKED+1 (in this case, the input stream is
    # synchronized on the media clock)" - so the pair is a lock STATE readout,
    # not only a consistency check, and a runner can use it instead of
    # inventing a lock flag.
    Given MEDIA_LOCKED 5 and MEDIA_UNLOCKED 4
    Then the lock invariant reports the stream synchronized
    Given MEDIA_LOCKED 4 and MEDIA_UNLOCKED 4
    Then the lock invariant reports the stream not synchronized

  @class:invariant @clause:Milan-Table-5.4
  Scenario Outline: the talker invariant admits exactly two states
    Given STREAM_START <start> and STREAM_STOP <stop>
    Then the talker invariant verdict is <verdict>

    Examples:
      | start | stop | verdict |
      | 3     | 3    | PASS    |
      | 3     | 2    | PASS    |
      | 3     | 1    | FAIL    |
      | 1     | 3    | FAIL    |

  @class:invariant @clause:17221-Table-7-157 @regression
  Scenario: TV + TNV == FRAMES_RX holds under the 1722.1 per-frame reading
    Given TIMESTAMP_VALID 1000 TIMESTAMP_NOT_VALID 0 FRAMES_RX 1000
    Then the tv-tnv verdict is PASS
    And the reading in force is "1722.1-per-frame"

  @class:invariant @clause:Milan-Table-5.6 @regression
  Scenario: under the Milan interval reading the same identity does NOT hold, and that is not a defect
    # 8000 frames in one second with FRAMES_RX ticking once is the interval
    # counter Milan Table 5.6 describes. A checker that fails here is asserting
    # 1722.1 against a Milan device.
    Given TIMESTAMP_VALID 8000 TIMESTAMP_NOT_VALID 0 FRAMES_RX 1
    Then the tv-tnv verdict is INFO
    And the reading in force is "milan-interval"

  @class:invariant @negative-control
  Scenario: FRAMES_RX above TV plus TNV is a defect under BOTH readings
    # Every frame is counted by exactly one of the two tv tallies, so no
    # observation interval can produce more FRAMES_RX than the sum.
    Given TIMESTAMP_VALID 5 TIMESTAMP_NOT_VALID 0 FRAMES_RX 99
    Then the tv-tnv verdict is FAIL

  @class:invariant @honesty @clause:Milan-5.3.8.10
  Scenario: an all-zero counter block cannot conclude which reading is in force
    # THE VACUITY THAT WAS THE ONLY STATE THIS CHECK WAS EVER CALLED IN.
    # Milan v1.2 5.3.8.10: "The PAAD-AE shall reset all of these counters to
    # zero each time the Stream Input changes its state from not bound to
    # bound." The runner took its ONE stream_input snapshot immediately after
    # the bind, so a CORRECT device answered 0/0/0 - and abs(0 - 0) <= tolerance
    # returned a definite PASS that also announced which of the two readings the
    # device implemented, from zero samples. All three at zero is now SKIP.
    Given TIMESTAMP_VALID 0 TIMESTAMP_NOT_VALID 0 FRAMES_RX 0
    Then the tv-tnv verdict is SKIP
    And the tv-tnv skip says the block was reset at the bind

  @class:growth @clause:Milan-Table-5.6 @rule:one-tick-is-a-failure
  Scenario Outline: the error counters get a growth VERDICT, not an INFO note
    # Milan v1.2 Table 5.6 defines SEQ_NUM_MISMATCH, UNSUPPORTED_FORMAT,
    # LATE_TIMESTAMP and EARLY_TIMESTAMP as "Incremented at the end of every
    # observation interval during which ...", so the question is "did it tick in
    # ANY interval" and one tick is one bad interval. These three assertions used
    # to be emitted as INFO - never PASS, never FAIL - so at SHALL severity they
    # contributed NOTHING to the exit code, and a board discarding 296,294 of
    # 296,294 frames as UNSUPPORTED_FORMAT passed green.
    Given <counter> reads <before> then <after>
    Then the growth verdict is <verdict>

    Examples: the two real escapes and their controls
      | counter            | before | after  | verdict |
      | UNSUPPORTED_FORMAT | 0      | 0      | PASS    |
      | UNSUPPORTED_FORMAT | 0      | 296294 | FAIL    |
      | UNSUPPORTED_FORMAT | 0      | 1      | FAIL    |
      | LATE_TIMESTAMP     | 12     | 12     | PASS    |
      | LATE_TIMESTAMP     | 12     | 5100000| FAIL    |
      | SEQ_NUM_MISMATCH   | 3      | 4      | FAIL    |
      | EARLY_TIMESTAMP    | 9      | 0      | INFO    |

  @class:growth @honesty
  Scenario: a counter the mask never claimed is a SKIP, not a clean growth pass
    Given UNSUPPORTED_FORMAT is not claimed by the mask
    Then the growth verdict is SKIP

  @class:invariant @clause:Milan-Table-5.4
  Scenario Outline: a measured frames rate is classified, not asserted
    # THE CLAUSE BOUNDS THE INTERVAL FROM ABOVE ONLY: "The duration of the
    # observation interval is implementation-specific and shall be less than or
    # equal to 1 second." So every interval in (0, 1 s] is conformant, and the
    # ONLY non-conformant interval reading is one that implies MORE than a
    # second. The first version of this table called 200.0/s - a perfectly legal
    # 5 ms interval - "neither", i.e. the defect, and a passing unit test
    # asserting exactly that cemented it. 0.4/s implies a 2.5 s interval and IS
    # the violation.
    Given a measured frames rate of <rate> per second
    Then the rate is consistent with the <reading> reading

    Examples: the silicon numbers from the 2026-07-29 talker/listener window
      | rate   | reading   |
      | 7995.7 | per-frame |
      | 4000.0 | per-frame |
      | 3999.0 | interval  |
      | 200.0  | interval  |
      | 1.0    | interval  |
      | 0.4    | neither   |
      | 0.0    | neither   |

  @class:invariant @clause:Milan-Table-5.4 @honesty
  Scenario: the interval a rate implies is reported, and only over a second is a defect
    Given a measured frames rate of 200.0 per second
    Then the implied observation interval is 0.005 seconds
    And the rate is consistent with the interval reading
    Given a measured frames rate of 0.4 per second
    Then the implied observation interval is 2.5 seconds
    And the reading refusal cites the 1 second ceiling

  # --------------------------------------------------- per-index obligations
  @class:coverage @clause:Milan-5.4.2.25
  Scenario: every Stream Input and Stream Output index owes an answer, not just index 0
    # Milan v1.2 5.3.8.10 keeps counters "For each Stream Input of the
    # currently set Configuration" and 5.3.7.7 "For each Stream Output". Index
    # 0 is the least representative index on this fabric: the 0x800 window
    # makes it a HARD ALIAS of the legacy flat registers, so an index-0 pass
    # exercises the alias and not the indexed path.
    Then the campaign plan asks for counters on every Stream Input index
    And the campaign plan asks for counters on every Stream Output index
    And the campaign plan includes the CRF Media Clock indices

  @class:coverage @clause:Milan-5.3.8.10
  Scenario: the CRF Media Clock Input is a Stream Input, so it owes the ten too
    # 5.3.8.10 says "for each Stream Input" with no CRF exemption, and
    # la_avdecc's per-enumeration mandatory-set check drops the Milan badge on
    # a CRF input that answers an empty mask.
    Then the CRF Media Clock Input index is in the plan's listener coverage
    And the mandatory mask required of it is 0xF3F

  # --------------------------------------------------- L1: the fabric binding
  @level:L1 @class:binding
  Scenario: the response builder emits the masks this contract names
    # An L1 check: it asks whether the fabric is CONNECTED to the contract, not
    # whether the counters are right. A mask edited in the RTL without this
    # file changing breaks here, at a desk, in three seconds.
    Then KL_aecp_response_builder serves Stream Output mask 0x1F
    And KL_aecp_response_builder serves AVB_INTERFACE mask 0x23
    And KL_aecp_response_builder serves the Stream Input mandatory mask

  @level:L1 @class:binding @open-finding @clause:Milan-5.3.8.10
  Scenario: GET_COUNTERS answers every declared Stream Input, not the first two
    # AN OPEN FINDING, DELIBERATELY RED, and tagged @open-finding so
    # `behave --tags ~@open-finding` remains a clean gate.
    #
    # Milan v1.2 5.3.8.10: "For each Stream Input of the currently set
    # Configuration, the PAAD-AE shall keep track of the counters in Table 5.6",
    # and 5.4.2.25 makes GET_COUNTERS mandatory per descriptor. No sink is
    # exempt - not the CRF Media Clock Input either.
    #
    # WHAT THE SOURCE IN THIS TREE SAYS, and every line of it is checkable:
    #   * the CMD_GET_COUNTERS case spans lines 1944-2012 of
    #     KL_aecp_response_builder.sv;
    #   * that block contains NO `w_in_fidx` and NO `AEM_N_STRIN_C`;
    #   * its only STREAM_INPUT guard is `w_gs_index < 16'd2`;
    #   * it calls `load_input_counters_consts(w_gs_index == 16'd0)`, which emits
    #     mask 0xF3F and loads real counter VALUES only for sink 0.
    # So sinks >= 2 fall through to BAD_ARGUMENTS and sink 1 answers 0xF3F over
    # an all-zero block.
    #
    # This scenario was briefly re-scoped to grep the WHOLE builder for
    # `w_gs_index < 16'(AEM_N_STRIN_C)`, which passes by matching line 395 - the
    # `w_in_fidx` declaration, whose own comment says "range validity is decided
    # separately in the STREAM_FORMAT arm". A whole-file grep standing in for an
    # arm-anchored check is precisely the descriptor-context-free defect this
    # round exists to remove, so the check is anchored on the arm again and its
    # failure message prints the guard text it found. If silicon disagrees with
    # the four bullets above, reconcile it against those line numbers.
    Then the STREAM_INPUT GET_COUNTERS arm answers every Stream Input the entity declares

  @level:L1 @class:binding @open-finding @clause:Milan-5.5.1.2
  Scenario: every declared Stream Input has somewhere to store a stream format
    # The SECOND finding in the same file, and a different subsystem from the one
    # above. The per-input format registers live behind `ifdef
    # AEM_PER_STREAM_FMT, and the `else arm keeps only inputs 0..1
    # (`fmt_in0_r` / `fmt_in1_r`). If no shipped config defines that macro then
    # every sink above index 1 has nowhere to store a format - against Milan v1.2
    # 5.5.1.2, which makes the Listener's current format the value the bind is
    # checked against, and against the standing directive that a controller must
    # ALWAYS SET_STREAM_FORMAT the listener rather than refuse the bind.
    Then the per-input STREAM_FORMAT store covers every declared Stream Input

  @level:L1 @class:binding
  Scenario: the per-stream window exposes the ten counters at the block offsets
    # docs/reference/REGISTER_MAP.md 0x830-0x854 is the full-width path to the
    # same ten values; the flat 0x6B8/0x6C0 words are SATURATING summaries, so
    # a bench read that uses them cannot see a counter past 255.
    Then the register map documents A_STRMW_CNT0..9 as the ten Table 5.6 counters
    And the register map warns that the flat views saturate
