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

  # ------------------------------------------- the per-counter UPDATE LAW
  # Trap (3) above is one counter's version of a question every counter owes an
  # answer to: WHEN does it move? Milan Table 5.6 answers it in two different
  # grammars, and this project has been wrong in BOTH directions - it once
  # counted the interval seven per frame, and the opposite mistake (dragging a
  # per-frame counter onto the interval tick) is just as available. So the law
  # is stated here per counter, as prose, and the RTL and the bench grader are
  # both held to this table.
  @class:law @clause:Milan-Table-5.6 @regression
  Scenario: every Stream Input counter has a stated update law, and there are three
    # "Incremented each time ..." is not the same sentence as "Incremented at
    # the end of every observation interval during which ...", and neither is
    # 1722.1's "Increments on receipt of ...". The grammar IS the requirement.
    Then every Stream Input counter has an update law
    And the update laws in use are "per-event, per-frame, per-interval"

  @class:law @clause:Milan-Table-5.6
  Scenario Outline: the update law of each counter, and the clause that fixes it
    # Milan v1.2 Table 5.6 defines ten of the twelve. It does NOT define
    # TIMESTAMP_VALID or TIMESTAMP_NOT_VALID - Table 5.16's mandatory mask
    # 0xF3F skips bits 6 and 7 - so those two are governed only by IEEE
    # 1722.1-2021 Table 7-157 and keep its per-frame reading. That is why a
    # conformant device shows TIMESTAMP_VALID about 8000x FRAMES_RX at class A:
    # the split is mandated, not a defect in either counter.
    Then the update law of <counter> is <law> per <clause>

    Examples: the three state-change counters - "Incremented each time ..."
      | counter            | law         | clause               |
      | MEDIA_LOCKED       | per-event   | Milan v1.2 Table 5.6 |
      | MEDIA_UNLOCKED     | per-event   | Milan v1.2 Table 5.6 |
      | STREAM_INTERRUPTED | per-event   | Milan v1.2 Table 5.6 |

    # the seven "at the end of every observation interval during which ..."
    # counters, interval implementation-specific and <= 1 second
    Examples: the seven observation-interval counters
      | counter             | law          | clause               |
      | SEQ_NUM_MISMATCH    | per-interval | Milan v1.2 Table 5.6 |
      | MEDIA_RESET         | per-interval | Milan v1.2 Table 5.6 |
      | TIMESTAMP_UNCERTAIN | per-interval | Milan v1.2 Table 5.6 |
      | UNSUPPORTED_FORMAT  | per-interval | Milan v1.2 Table 5.6 |
      | LATE_TIMESTAMP      | per-interval | Milan v1.2 Table 5.6 |
      | EARLY_TIMESTAMP     | per-interval | Milan v1.2 Table 5.6 |
      | FRAMES_RX           | per-interval | Milan v1.2 Table 5.6 |

    Examples: the two Milan does not define, so 1722.1 alone governs them
      | counter             | law       | clause                     |
      | TIMESTAMP_VALID     | per-frame | IEEE 1722.1-2021 Table 7-157 |
      | TIMESTAMP_NOT_VALID | per-frame | IEEE 1722.1-2021 Table 7-157 |

  @class:law @clause:Milan-Table-5.6
  Scenario Outline: the trigger condition each counter is counting
    # A counter can have the right update law and still watch the wrong thing.
    # MEDIA_RESET is the case in point: this fabric counted the LOCAL I2S
    # playback buffer's overrun/underrun rail - a signal no clause mentions,
    # and one tied to 1'b0 outright on a shape built without a DAC - so a
    # talker-signalled media clock restart could never be counted at all.
    Then the trigger for <counter> mentions "<phrase>"

    Examples:
      | counter             | phrase                                      |
      | MEDIA_RESET         | 'mr' bit was toggled                        |
      | TIMESTAMP_UNCERTAIN | 'tu' bit was set                            |
      | SEQ_NUM_MISMATCH    | non-sequential sequence_num                 |
      | UNSUPPORTED_FORMAT  | did not match the current format            |
      | LATE_TIMESTAMP      | timestamp field that was in the past         |
      | EARLY_TIMESTAMP     | too far in the future                       |
      | FRAMES_RX           | at least one Stream Data AVTPDU              |
      | TIMESTAMP_VALID     | tv bit set                                  |
      | MEDIA_LOCKED        | synchronized on the media clock              |

  @class:law @clause:Milan-Table-5.6 @rule:frames-rx-is-the-interval-clock
  Scenario: FRAMES_RX is the observation-interval clock, so nothing may out-tick it
    # THE SOUND FORM OF THE SEMANTICS CHECK. The clause bounds the observation
    # interval from ABOVE only, so no absolute rate is a defect on its own and a
    # rate band cannot decide the question. But every one of the seven
    # per-interval triggers arrives IN a received frame, and FRAMES_RX ticks in
    # every interval during which any frame was received. So for any interval
    # counter X and any window, delta(X) <= delta(FRAMES_RX) - regardless of
    # what the implementation's interval actually is.
    Given a stream input window where FRAMES_RX advanced by 30
    And TIMESTAMP_UNCERTAIN advanced by 30 in that window
    And LATE_TIMESTAMP advanced by 2 in that window
    Then the interval-ceiling verdict is PASS

  @class:law @negative-control @rule:frames-rx-is-the-interval-clock
  Scenario: a counter still counting per frame while FRAMES_RX counts per interval is caught
    # The half-converted state this fabric shipped before the seven listener
    # counters were moved onto the interval tick - and the exact shape a partial
    # revert would leave behind.
    Given a stream input window where FRAMES_RX advanced by 30
    And TIMESTAMP_UNCERTAIN advanced by 240060 in that window
    Then the interval-ceiling verdict is FAIL
    And the interval-ceiling offender is TIMESTAMP_UNCERTAIN

  @class:law @honesty
  Scenario: the two tv tallies are exempt from the ceiling, because Milan never defined them
    # TIMESTAMP_VALID out-ticks an interval FRAMES_RX by the frame rate BY
    # DESIGN, so the ceiling must not look at it. LATE_TIMESTAMP is in the
    # window too, so the check actually runs rather than skipping for want of
    # anything to grade.
    Given a stream input window where FRAMES_RX advanced by 30
    And LATE_TIMESTAMP advanced by 2 in that window
    And TIMESTAMP_VALID advanced by 240060 in that window
    Then the interval-ceiling verdict is PASS

  @class:law @honesty
  Scenario: a window with no frames cannot grade the interval clock
    Given a stream input window where FRAMES_RX advanced by 0
    And TIMESTAMP_UNCERTAIN advanced by 0 in that window
    Then the interval-ceiling verdict is SKIP

  @class:law @clause:Milan-Table-5.6
  Scenario Outline: a single counter is graded against its own law, with the clause named
    Given <counter> advanced by <delta> over <window> seconds with the stream flowing
    Then the semantics verdict is <verdict> and the reading is <reading>

    Examples: the silicon shape - a bound sink at class A, mask 0xFFF
      | counter         | delta  | window | verdict | reading   |
      | FRAMES_RX       | 30     | 30     | PASS    | interval  |
      | TIMESTAMP_VALID | 240060 | 30     | PASS    | per-frame |
      | MEDIA_LOCKED    | 1      | 30     | PASS    | per-event |

    Examples: the two directions of getting the law wrong
      | counter         | delta  | window | verdict | reading    |
      | TIMESTAMP_VALID | 30     | 30     | FAIL    | interval   |
      | FRAMES_RX       | 15     | 30     | FAIL    | neither    |
      | FRAMES_RX       | 240060 | 30     | INFO    | per-frame  |

    Examples: nothing measured is nothing concluded
      | counter            | delta | window | verdict | reading |
      | UNSUPPORTED_FORMAT | 0     | 30     | SKIP    | static  |

  @class:law @honesty @clause:Milan-Table-5.6 @rule:only-frames-rx-implies-the-interval
  Scenario Outline: only FRAMES_RX's rate implies the observation interval
    # THE TRAP THIS PROJECT HAS NOW HIT THREE TIMES, caught the third time by
    # running the grader against real silicon before trusting it.
    #
    # Table 5.6 increments each interval counter "at the end of every
    # observation interval DURING WHICH <condition>", so a counter ticks only
    # in the intervals where its OWN condition held. FRAMES_RX's condition -
    # "at least one Stream Data AVTPDU has been received" - is the only one
    # that holds in every interval of a flowing stream, which is what makes its
    # rate the interval clock. The other six are intermittent BY DEFINITION.
    #
    # The numbers below are the AX7101's sink 0 read on 2026-08-03 after
    # 60,248,450 frames (about 7,531 s at class A): FRAMES_RX 7,545 gives a
    # 0.998 s observation interval, inside the ceiling. Dividing the OTHER
    # counters by the same window implies intervals of minutes, and an earlier
    # cut of this grader duly failed both of them.
    Given <counter> advanced by <delta> over 7531 seconds with the stream flowing
    Then the semantics verdict is <verdict> and the reading is <reading>

    Examples: the interval clock is graded against the 1 s ceiling
      | counter   | delta | verdict | reading  |
      | FRAMES_RX | 7545  | PASS    | interval |

    Examples: an intermittent condition is not a slow clock
      | counter             | delta | verdict | reading  |
      | TIMESTAMP_UNCERTAIN | 23    | PASS    | interval |
      | LATE_TIMESTAMP      | 74    | PASS    | interval |
      | SEQ_NUM_MISMATCH    | 1     | PASS    | interval |

  @class:law @negative-control
  Scenario: more ticks than frames is impossible under every reading
    Given FRAMES_RX advanced by 900000 over 30 seconds with the stream flowing
    Then the semantics verdict is FAIL and the reading is impossible

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

  @class:law @honesty @clause:Milan-5.4.2.25 @rule:advertised-is-measured
  Scenario: a counter advertised in the mask must be a measurement, never a constant
    # THE DEFECT CLASS THIS RULE EXISTS FOR (traceability AVTP-5t, found by the
    # 2026-08-03 STREAM_INPUT audit). The CRF Media Clock Input advertised the
    # full mandatory 0xF3F while STREAM_INTERRUPTED, MEDIA_RESET,
    # TIMESTAMP_UNCERTAIN, LATE_TIMESTAMP and EARLY_TIMESTAMP were served as
    # constant zeros - the engine kept no such tallies. That is WORSE than
    # leaving the bits unclaimed: an unclaimed bit tells a controller "I do not
    # measure this", while a claimed constant tells it "I measure this and it
    # never happened". A controller cannot distinguish the second from a
    # healthy stream, so the fault it is supposed to surface is hidden by the
    # very counter that was added to surface it.
    #
    # The rule is symmetric: the valid mask and the set of counters backed by a
    # real tally must be THE SAME SET. Narrowing the mask is a legal fix; a
    # served constant is not.
    #
    # WHERE THE SECOND HALF READS NOW. It used to catch the constant at the
    # AECP response builder's CRF loader. hdl/ieee17221/aecp/** is deleted, so
    # there is no loader; but a counter with no register behind it is a
    # constant zero however it is served, so the check is resolved out of
    # KL_crf_rx - the engine that would have to keep the tally - instead.
    Then a counter is either claimed in the mask and measured, or claimed by neither
    And the CRF Media Clock Input counters advertised as valid are all backed by a tally

  @class:law @clause:Milan-Table-5.6 @rule:advertised-is-measured
  Scenario Outline: the CRF Media Clock Input obeys the SAME law per counter as an AAF sink
    # Table 5.6 is written per Stream Input, not per stream FORMAT: there is no
    # separate CRF grammar. So the CRF sink's five newly-measured counters take
    # the identical laws the AAF sinks take - the split is per counter, never
    # per descriptor.
    Then the update law of <counter> is <law> per Milan v1.2 Table 5.6
    And the CRF Media Clock Input applies the <law> law to <counter>

    Examples: the per-event one among the five that were constant
      | counter            | law         |
      | STREAM_INTERRUPTED | per-event   |

    Examples: the four observation-interval ones
      | counter             | law          |
      | MEDIA_RESET         | per-interval |
      | TIMESTAMP_UNCERTAIN | per-interval |
      | LATE_TIMESTAMP      | per-interval |
      | EARLY_TIMESTAMP     | per-interval |

  @class:law @clause:Milan-5.3.8.10 @rule:era-wipe
  Scenario: the bind edge wipes all ten, and the unbind edge wipes none
    # The sentence that CLOSES Table 5.6: "The PAAD-AE shall reset all of these
    # counters to zero each time the Stream Input changes its state from not
    # bound to bound", immediately followed by its deliberate asymmetry: "the
    # PAAD-AE does not reset these counters when the Stream Input changes its
    # state from bound to not bound".
    #
    # Both halves are law and both are load-bearing. A total carried ACROSS a
    # bind is unreadable - a Controller that just bound a stream cannot tell
    # this era's faults from a previous talker's - which is the same defect
    # class the five constant zeros were. A total dropped ON an unbind would
    # instead destroy the evidence of the fault that caused the unbind.
    #
    # The pair MEDIA_LOCKED / MEDIA_UNLOCKED carries a third obligation: Table
    # 5.6 reads it as STATE ("either MEDIA_LOCKED=MEDIA_UNLOCKED ... or
    # MEDIA_LOCKED=MEDIA_UNLOCKED+1"), so zeroing both while the sink still
    # believes it is locked, or letting a pending unlock walk +1 over the
    # zeroed pair, leaves it in a state the clause does not define.
    Then the CRF Media Clock Input zeroes all ten counters on the bind edge
    And the CRF Media Clock Input era wipe fires on the bind edge only
    And the CRF Media Clock Input bind edge drops media lock without scoring an unlock

  # --------------------------------------------------- L1: the fabric binding
  # (the KL_aecp_response_builder mask-serving and the two @open-finding
  #  scenarios that lived here were resolved out of hdl/ieee17221/aecp/**,
  #  which has been deleted - this device answers no AECP command at all,
  #  so there is no builder to hold to a mask and no GET_COUNTERS arm to
  #  hold to a descriptor index. What survives is the DOCUMENTED register
  #  window, which is still the fabric path to the same ten values.)

  @level:L1 @class:binding
  Scenario: the per-stream window exposes the ten counters at the block offsets
    # docs/reference/REGISTER_MAP.md 0x830-0x854 is the full-width path to the
    # same ten values; the flat 0x6B8/0x6C0 words are SATURATING summaries, so
    # a bench read that uses them cannot see a counter past 255.
    Then the register map documents A_STRMW_CNT0..9 as the ten Table 5.6 counters
    And the register map warns that the flat views saturate
