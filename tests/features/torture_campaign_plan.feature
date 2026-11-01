# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@torture @campaign @level:L3 @matrix:M-CAMPAIGN
Feature: The torture campaign's own coverage is auditable at a desk
  Bench time is the scarce resource, so the campaign that spends it has to be
  reviewable without spending any. tb/tools/torture_campaign.py is the PLAN -
  every pair, every index, every churn sequence, every adverse condition, and
  for each the exact assertions it owes with the clause behind them - and it
  performs no I/O at all. These scenarios audit that plan: they are the reason
  "we test every combination" and "we tested link loss" can be checked instead
  of believed.

  LEVEL / ORACLE (docs/testing/methodology.md). LEVEL 3. ORACLE: the clause
  list, plus the standing user rules the plan encodes. What this level cannot
  see: whether the device passes - only whether the right questions get asked,
  of every index, with a clause attached to each.

  WHY A PLAN AUDIT IS WORTH SCENARIOS OF ITS OWN. A runner that decides its
  coverage as it goes can only be audited by running it on hardware. Four
  separate per-index defects on this device hid behind index-0-only testing
  (GET_STREAM_INFO serving index 0's answer for every index, MAX_TRANSIT_TIME
  existing only at index 0, GET_COUNTERS answering only index 0, and the
  per-stream window's talker state bits hardwired 0 above index 0), and index 0
  is the LEAST representative index here because the 0x800 window makes it a
  hard alias of the legacy flat registers.

  THE ADVERSE-CONDITIONS SOURCING, and the two honesty rules that follow from
  reading it rather than remembering it:
    The Milan adverse-network-conditions recommended practice covers exactly ONE
    condition - sustained high rate traffic - in four traffic classes, and it is
    a RECOMMENDATION: "It is not a current requirement for a Milan device to
    support the features mentioned."  It says nothing about malformed packets.
    Therefore
    (1) the storm entries are severity RECOMMENDED, and a failure is a finding
    with a cost decision attached, not a conformance failure; and
    (2) the same clause says "As AVDECC traffic is Non-Priority, it is not
    expected that a Milan device remains responsive to AVDECC commands while
    subjected to high rate Non-Priority traffic" - so control-plane
    responsiveness under storm is RECORDED and never failed, and the malformed
    frame entries cite IEEE 1722.1-2021 because that document does not cover
    them.
    It is cited generically, with no version: the version is a detail visible
    only to a document holder and no technical claim here needs it.

  THE LICENCE, which is why this plan has a step of its own for it:
    Milan v1.2 5.3.7.3 licenses a talker only "As long as a PAAD is declaring a
    Talker Advertise attribute AND receiving a Listener Ready or Listener Ready
    Failed attribute for a Stream Output".  The second half of that conjunction
    arrives over MSRP from the listener, so a bind that returns SUCCESS does not
    grant it.  On this fabric it is readable as LWSRP_STATUS (0x694) bit 8, and
    0x30 - talker declared, domain ok, GATE SHUT - is what a CORRECTLY silent
    bound talker reads.  A plan that put the frames-advance verdicts on the bind
    step therefore turned every conformant bound-but-ungated pair into a SHALL
    failure; they live on the licence-owning step instead, and SKIP when the
    reading is unavailable.

  Background:
    Given the campaign plan is importable

  # ---------------------------------------------------------------- coverage
  @class:coverage @rule:never-index-0-only
  Scenario: the matrix walks every talker and listener index in both directions
    When the matrix area is planned
    Then the plan covers every DUT talker index
    And the plan covers every DUT listener index
    And the plan covers every peer talker index
    And the plan covers every peer listener index
    And the plan contains outbound, return and loopback pair sets

  @class:coverage @rule:never-index-0-only @negative-control
  Scenario: the index audit can say no
    # A plan over a one-stream device covers only index 0 - and the audit must
    # report exactly that rather than reporting success. A coverage check that
    # cannot distinguish full coverage from index-0-only is not a check.
    When the matrix area is planned for a device with 1 talker and 1 listener
    Then the plan covers only index 0
    And that is fewer indices than the real DUT shape

  @class:coverage @clause:Milan-7.2.2 @clause:Milan-7.2.3
  Scenario: the CRF media clock stream is part of the matrix, not an extra
    # Milan v1.2 7.2.2/7.2.3 make a CRF Media Clock Input mandatory on an AAF
    # Media Talker and on an AAF Media Listener with two or more AAF Media
    # Inputs, and a CRF Media Clock Output likewise - so a matrix that stops at
    # the AAF streams has skipped a mandatory stream.
    When the matrix area is planned
    Then the CRF talker index is in the plan
    And the CRF listener index is in the plan
    And the CRF pair steps are marked as the media clock pair

  # -------------------------------------------------------- the assertion set
  @class:contract @clause:Milan-5.3.8.10 @clause:Milan-Table-5.4
  Scenario: every bind step owes the whole bound-and-streaming assertion set
    # ACMP status, ADP liveness, the three counter masks, both invariants,
    # TV+TNV, the RX and TX rates, and no growth in LATE/EARLY/SEQ_NUM_MISMATCH/
    # UNSUPPORTED_FORMAT. A step carrying fewer is a step that can pass while
    # something is wrong.
    When the matrix and churn areas are planned
    Then every connect step carries the full bound-streaming assertion set
    And that includes the rebind steps
    And no bind step grades whether frames are advancing

  @class:contract @clause:Milan-5.3.7.3 @honesty
  Scenario: the licence is measured BEFORE any START_STREAMING is sent
    # Milan v1.2 5.3.7.3 makes the Talker Advertise plus the Listener Ready the
    # whole licence and says STREAMING_WAIT "shall not be implemented", so a
    # talker that needs an AECP START_STREAMING before it frames has implemented
    # the state the clause forbids. A harness that always sends START_STREAMING
    # after a bind cannot see the difference - the workaround becomes an
    # invisible permanent behaviour. So the plan measures first and records
    # which of the two happened.
    When the matrix and churn areas are planned
    Then every bind is followed by a measure-before-start step
    And that step asserts the stream starts on the bind alone
    And that step measures before it sends anything
    And that step asks the SRP licence before it grades any silence

  @class:contract @clause:Milan-5.3.7.3 @honesty @multi-sided
  Scenario: the licence-owning step measures every participant, not only the DUT
    # A verdict derived from one side's counters is a CLAIM; one corroborated
    # across every side is a FACT. So the step that decides "is this stream
    # running" carries the DUT, the reference device and the test machine, and
    # the test machine is a health gate as well as a witness: if its rx_dropped
    # moved, its listener-side verdicts are downgraded rather than blamed on the
    # device.
    When the matrix area is planned
    Then every bind is followed by a measure-before-start step
    And the licence-owning step carries the cross-participant invariants

  @class:contract @clause:Milan-5.3.7.3 @honesty
  Scenario: every unbind VERIFIES the stop, so the next pair can still be measured
    # There was no STOP_STREAMING anywhere in the layer. After the first
    # START_STREAMING latched a talker, every later pair measured an
    # already-streaming talker and stream.starts-on-bind-alone reported PASS -
    # a false PASS for 94 of the matrix's 95 pairs. The anti-STREAMING_WAIT
    # assertion destroyed itself.
    When the matrix and churn areas are planned
    Then every unbind verifies the stop took effect

  @class:contract @clause:Milan-Table-5.6 @honesty
  Scenario: the growth assertions can actually fail
    # They were emitted as INFO - never PASS, never FAIL - so at SHALL severity
    # they contributed nothing to the exit code, and their own note claimed the
    # verdict came from a rate probe that only re-read FRAMES_TX/FRAMES_RX.
    When the whole campaign is planned
    Then the whole campaign has no assertion that can only be INFO at SHALL severity

  @class:coverage @rule:never-index-0-only @honesty
  Scenario: coverage is audited PER AREA, because the whole-plan audit is blind
    # plan_covers_every_index() over the whole plan is masked by the matrix
    # area's full coverage, which is how the audio area stayed index-0-only under
    # a green report.
    When the whole campaign is planned
    Then coverage is audited per area
    And the per-area audit can say no about one area while another is complete

  @class:runner @honesty
  Scenario: the topology is configuration, not a source edit
    # Hardcoded entity ids and MACs make a campaign single-bench, and a
    # misspelled override would run the whole thing against the wrong shape and
    # then report full coverage of it.
    When the matrix area is planned
    Then the topology is configuration and a typo is refused

  @class:contract @clause:methodology-R3
  Scenario: every assertion in the whole campaign names a clause and a severity
    When the whole campaign is planned
    Then every assertion carries a non-empty clause
    And every assertion severity is SHALL or RECOMMENDED or INFO

  @class:contract
  Scenario: every step id in the campaign is unique, so two mornings can be diffed
    When the whole campaign is planned
    Then no two steps share an id
    And every step serialises to JSON with its clauses attached

  # ------------------------------------------------------------------ churn
  @class:churn @clause:Milan-5.5.3.5.43
  Scenario: the churn area reaches the implicit rebind a bind/unbind loop cannot
    # 5.5.3.5.43 (SETTLED_RSV_OK / RCV_BIND_RX_CMD): a BIND_RX for a Stream
    # Input that is ALREADY bound is honoured as an implicit rebind with no
    # intervening unbind. A loop that always unbinds first never reaches that
    # transition at all.
    When the churn area is planned
    Then there is a rebind step that does not unbind first
    And each rebind moves to a DIFFERENT talker index than its first bind
    And the rebind step asserts the counter reset on not-bound to bound

  @class:churn @clause:17221-8.2.2.6.2.1
  Scenario: the churn area binds a second listener while the first is streaming
    When the churn area is planned
    Then there is a bind-while-streaming step

  @class:churn @clause:Milan-5.5.3.5.43
  Scenario: the rebind storm is auditable by an invariant, not by guessing the winner
    # After twenty back-to-back implicit rebinds nobody knows which bind won,
    # and it does not matter: the lock invariant and ADP liveness are true or
    # they are not.
    When the churn area is planned
    Then there is a rebind storm step with at least 20 iterations
    And the rebind storm asserts the lock invariant and ADP liveness

  # --------------------------------------------------------- adverse honesty
  @class:torture @clause:Milan-adverse-conditions
  Scenario: storm entries are RECOMMENDED, and control responsiveness is INFO
    # Marking these SHALL would fail a device for something no requirement asks
    # of it, and failing an entity for not answering AVDECC under storm would
    # assert the opposite of the cited sentence.
    When the torture area is planned
    Then every storm step marks stream continuity as RECOMMENDED
    And every storm step marks control responsiveness as INFO
    And the storm steps cover non-priority broadcast, unicast to our own MAC, AVDECC and AVB management

  @class:torture @clause:17221-9.2.1.1.6 @honesty
  Scenario: malformed-frame entries do NOT cite the adverse-conditions document
    # That recommended practice covers sustained high rate traffic and nothing
    # else, so citing it for a malformed frame would be citing a section that is
    # not in it.
    When the torture area is planned
    Then no malformed-frame step cites the adverse-conditions recommendation
    And every malformed-frame step cites IEEE 1722.1 or IEEE 1722
    And every malformed-frame step asserts the entity does not wedge

  @class:torture @honesty @rule:cite-generically
  Scenario: no clause in the campaign carries a draft version number
    When the whole campaign is planned
    Then no clause in the campaign carries a draft version number

  @class:torture
  Scenario: the malformed matrix fuzzes the length fields in both directions
    # A frame that OVERSTATES its control_data_length and one that UNDERSTATES
    # it are different defects: the first invites a read past the buffer, the
    # second invites parsing pad as payload.
    When the torture area is planned
    Then the malformed matrix includes an overstated control_data_length
    And the malformed matrix includes an understated control_data_length
    And the malformed matrix includes a truncated AECP payload
    And the malformed matrix includes an AAF stream_data_length that overstates the payload

  @class:torture @clause:Milan-5.3.7.5
  Scenario: the MAAP conflict entry asserts the withdraw, the reallocation and the Stream ID move
    # Milan v1.2 Table 5.3 lets the PAAD use another Stream ID after a
    # conflict, and IEEE 802.1Q-2018 35.2.2.8 asks for the 2 LeaveAll wait
    # only before the SAME StreamID returns with another FirstValue. Since
    # processor #202 the device moves the source to a new Stream ID and
    # declares it at once (#799), so the entry grades the move, not a wait.
    When the torture area is planned
    Then the MAAP conflict step asserts a withdraw and reallocate
    And the MAAP conflict step asserts the new Stream ID on the wire and in the answers
    And the MAAP conflict clause limits the LeaveAll wait to the same Stream ID

  @class:torture @clause:8021Q-9.6
  Scenario: VLAN misconfiguration covers the wrong SR VID and VID zero separately
    When the torture area is planned
    Then there is a wrong-SR-VID step
    And there is a VID-zero step
    And the VID-zero step asserts no untagged stream frames

  @class:torture @clause:Milan-5.3.7.3
  Scenario: starvation asserts silence-with-frames, and stream loss asserts the interrupt counter
    When the torture area is planned
    Then the source-starvation step asserts the talker keeps framing
    And the stream-stop step asserts STREAM_INTERRUPTED advances

  # ------------------------------------------------------- the human entries
  @class:human @rule:print-do-not-skip
  Scenario: entries a human must perform are printed as a checklist, never skipped
    # A skipped adverse-condition entry that nobody sees is how "we tested link
    # loss" becomes true in a report and false on the bench.
    When the whole campaign is planned
    Then at least 3 steps need a human
    And the checklist names every human step with its action and its clause
    And an empty plan produces a checklist that says so

  @class:human
  Scenario: the physical conditions are still covered - by strip or by hand
    # The gm-change, gm-loss and power-cycle entries moved to the physical
    # area, where a runner with the powerstrip hook (USER authorization
    # 2026-08-02: powerstrip OUT4 = the switch DN-1, OUT0 = the DUT) drives them
    # automatically.  In the PLAN they stay needs_human, so a bench without
    # the hook hands them back as NEEDS-HUMAN exactly as before - never a
    # silent skip.  The cable pull stays human forever: a powerstrip cannot
    # pull one cable.
    When the whole campaign is planned
    Then the human entries include a cable pull
    And the human entries include a grandmaster change
    And the human entries include a grandmaster loss
    And the human entries include a power cycle
    And the power-cycle step asserts the non-volatile state is restored

  @class:human @class:physical @rule:no-regression-without-hook
  Scenario: the physical family is powerstrip-automatable, serialized, and runs last
    # A partition mid-matrix would pollute every later verdict, so the
    # physical area is the LAST thing the campaign runs; the partition window
    # itself is the condition applied, so timeouts inside it are never
    # failures; and the plan states the recovery budgets so a red is a
    # measured miss, not an opinion.
    When the whole campaign is planned
    Then the physical area is the last thing the campaign runs
    And every physical cycle step is still a human entry in the plan
    And the physical cycle steps name the outlet role they need
    And the physical recovery budgets respect the bench floors
    And the partition window is asserted as the condition, not a failure
    And each physical family ends with a full proof pair at a non-zero index

  # ------------------------------------------------------ runner integration
  # Issue #396 owner decisions 2026-10-26: a 24-hour soak with the audio
  # integrity run inside it, and 200 power cycles (100 idle cold cuts, 50 cold
  # cuts inside a journal commit, 50 soft resets), with the stricter criteria.
  @class:release @clause:REQ-VER-06
  Scenario Outline: release areas observe every index and bind both directions
    When the <area> release area is planned
    Then the plan covers every DUT talker index
    And the plan covers every DUT listener index
    And the plan covers every peer talker index
    And the plan covers every peer listener index
    And every release repeat observes every index including each CRF sink
    And every release repeat binds compatible AAF and CRF in both directions

    Examples:
      | area  |
      | soak  |
      | audio |
      | power |

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario Outline: release coverage refuses omissions even with a complete matrix
    When the <area> release plan loses its <missing>
    Then that release area fails its own audit
    And the complete matrix still passes its audit

    Examples:
      | area  | missing   |
      | soak  | index     |
      | soak  | direction |
      | soak  | CRF sink  |
      | audio | index     |
      | audio | direction |
      | audio | CRF sink  |
      | power | index     |
      | power | direction |
      | power | CRF sink  |

  @class:release @clause:REQ-VER-06
  Scenario: release defaults encode the decided soak, audio run and cycle mix
    When the whole campaign is planned
    Then the soak lasts 24 hours with periodic and endpoint observations
    And the audio run lasts the whole soak window inside it
    And power repeats 100 idle and 50 journal-commit cold cuts and 50 soft resets
    And release assertions require complete measured evidence

  # Issue #787: the 50 soft resets are the controller's AECP REBOOT of ENTITY 0
  # (IEEE 1722.1-2021 7.4.43), and each is graded on its own exchange and on
  # the gPTP relock with correct TX timestamps (IEEE 802.1AS-2011 11.2.15).
  @class:release @clause:REQ-VER-06
  Scenario: every soft reset is an AECP REBOOT, graded on its exchange and the gPTP relock
    When the power release area is planned
    Then the soft resets send an AECP REBOOT of ENTITY 0 and require SUCCESS
    And the soft resets owe the REBOOT exchange and the gPTP relock, and the cold cuts do not

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario Outline: the REBOOT oracle refuses a soft reset that did not happen
    When a soft reset's REBOOT exchange shows <defect>
    Then the REBOOT oracle grades it <verdict>

    Examples:
      | defect                        | verdict |
      | nothing                       | PASS    |
      | a status other than SUCCESS   | FAIL    |
      | no ENTITY_DEPARTING           | FAIL    |
      | a link still up after 11 s    | FAIL    |
      | an incomplete capture         | NOT RUN |

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario Outline: the gPTP relock oracle refuses wrong TX timestamps after a soft reset
    When a soft reset's gPTP readings show <defect>
    Then the gPTP relock oracle grades it <verdict>

    Examples:
      | defect                              | verdict |
      | nothing                             | PASS    |
      | no asCapable by the deadline        | FAIL    |
      | the peer's link delay moved 50 ns   | FAIL    |
      | the DUT's link delay moved 50 ns    | FAIL    |
      | an unlocked pre-reset reading       | NOT RUN |

  @class:release @clause:REQ-VER-06
  Scenario: the power cycle mix adds up to 200
    When the power release area is planned
    Then the power phases add up to 200 cycles
    And 150 of them are cold cuts and a third of those land in a journal commit
    And every cycle restores the eight Milan items and the binding

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario Outline: a cycle mix that does not add up fails the power audit
    When the power release plan loses one <phase> cycle
    Then that release area fails its own audit
    And the complete matrix still passes its audit

    Examples:
      | phase          |
      | idle           |
      | journal_commit |
      | soft_reset     |

  @class:release @clause:REQ-VER-06
  Scenario: no release repeat may skip a required assertion
    When the whole campaign is planned
    Then every release repeat carries its area's required assertions at SHALL severity
    And every release repeat refuses an unsupported operation instead of skipping it

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario Outline: dropping or downgrading one required assertion fails the audit
    When release repeat <repeat> has its <assertion> assertion <change>
    Then that release area fails its own audit
    And the complete matrix still passes its audit

    Examples:
      | repeat               | assertion                | change     |
      | soak.continuous      | soak.no-counter-errors   | dropped    |
      | soak.continuous      | soak.tu-within-holdover  | downgraded |
      | audio.integrity      | audio.zero-dut-glitches  | dropped    |
      | audio.integrity      | audio.planted-arms-found | downgraded |
      | power.idle           | power.state-restored     | dropped    |
      | power.journal_commit | power.single-boot        | downgraded |
      | power.soft_reset     | power.adp-valid-time     | dropped    |
      | power.soft_reset     | power.reboot-reset       | dropped    |
      | power.soft_reset     | power.gptp-relock        | downgraded |

  @class:release @clause:REQ-VER-06 @clause:Milan-Table-5.6 @negative-control
  Scenario Outline: the soak counters admit no growth and no unplanted unlock
    When an input's soak counter walk shows <growth>
    Then the soak counter oracle grades it <verdict>

    Examples:
      | growth                                    | verdict |
      | nothing                                   | PASS    |
      | one SEQ_NUM_MISMATCH                      | FAIL    |
      | one STREAM_INTERRUPTED                    | FAIL    |
      | one LATE_TIMESTAMP                        | FAIL    |
      | one EARLY_TIMESTAMP                       | FAIL    |
      | one MEDIA_UNLOCKED                        | FAIL    |
      | one MEDIA_UNLOCKED in a planted event     | PASS    |
      | one MEDIA_UNLOCKED beside a planted event | FAIL    |
      | two MEDIA_UNLOCKED in one planted event   | FAIL    |

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario Outline: each negative control fails its own assertion and only by its defect
    When the <control> negative control is run at the desk
    Then the control fails <assertion>
    And the same oracle passes once the defect is removed

    Examples:
      | control                            | assertion               |
      | power.control.first-boot-restart   | power.single-boot       |
      | power.control.persistence-disabled | power.state-restored    |
      | audio.control.planted-drop         | audio.zero-dut-glitches |

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario: the audio grader classifies the planted drop exactly, offline
    When the planted audio drop is graded on its synthetic capture
    Then the grader finds one 5-sample drop at the planted sample on every channel
    And every planted arm is found and attributed apart from the DUT

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario Outline: the audio grader names each discontinuity class
    When a synthetic counter capture carries <event>
    Then the audio grader reports <class> on <channels> channels

    Examples:
      | event                       | class    | channels |
      | a 3-sample drop             | dropped  | 4        |
      | a 2-sample repeat           | repeated | 4        |
      | 6 samples of silence        | silence  | 4        |
      | a bit flip on one channel   | bit-flip | 1        |
      | a swap of two channels      | swap     | 2        |

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario Outline: the audio grader sizes a slip of whole blocks exactly
    When the counter capture shows a <n>-sample <kind>
    Then the audio grader reports <class> of <n> samples on 4 channels within 63 samples of the slip

    Examples:
      | kind   | n      | class    |
      | drop   | 2048   | dropped  |
      | drop   | 4096   | dropped  |
      | repeat | 4096   | repeated |
      | drop   | 409600 | dropped  |

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario: a channel-number flip on one channel is corruption, not a swap
    When a synthetic counter capture flips one channel-number bit on one channel
    Then the audio grader reports one bit-flip with that mask and no swap

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario: a one-sample hold reads as one repeated and then one dropped sample
    When a synthetic counter capture holds one sample on every channel
    Then the audio grader reports a 1-sample repeat and then a 1-sample drop on every channel

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario: a channel swap from the first frame fails as a swap with every arm found
    When a synthetic counter capture swaps two channels for the whole run
    Then the audio grader fails the run with two swaps and every planted arm found

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario: a capture loss is time that ran, so later events keep true clocks
    When a synthetic counter capture loses frames at the capture before a corrupted sample
    Then the corrupted sample's wall and gPTP times include the lost frames
    And without an anchor after the event its times are null, not invented

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario: arms planted only in the middle of the capture void the run
    When a synthetic counter capture plants every arm in the middle of the run
    Then the audio grader voids the run as NOT RUN for arms outside the first and the last tenth

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario: the audio grader states its qualified interval and needs 24 hours of it
    When a clean counter capture is graded with the release's required duration
    Then the audio grader returns NOT RUN for a qualified interval shorter than 24 hours
    And the verdict states an interval from 63 samples after acquisition to 63 samples before the end
    And the same capture passes when the required duration is its qualified length

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario Outline: a slip of whole blocks at a capture's end is unresolved, never exact
    When a counter capture ends <back> samples after a <n>-sample drop
    Then the audio grader reports only unresolved events that bound the slip, or passes outside the qualified interval

    Examples:
      | n    | back |
      | 2048 | 1    |
      | 4096 | 1    |
      | 4096 | 30   |
      | 8192 | 62   |

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario Outline: a constant-mask corruption of any length is one bit-flip
    When a synthetic counter capture XORs <mask> into <n> consecutive words on one channel
    Then the audio grader reports one bit-flip of <n> words with mask <mask>

    Examples:
      | mask       | n   |
      | 0x00000100 | 63  |
      | 0x00000100 | 64  |
      | 0x00000100 | 65  |
      | 0x00000100 | 100 |
      | 0x00080000 | 100 |

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario: a slip and a one-word corruption in one window are both graded
    When a synthetic counter capture drops 3 samples 5 samples before a code-bit flip
    Then the audio grader reports the 3-sample drop on every channel and the flip at its sample

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario Outline: a slip of whole blocks after a one-word corruption is graded as both events
    When a synthetic counter capture flips <mask> on one channel at 3000 and every channel slips <n> samples at <at>
    Then the audio grader reports the flip at 3000 and on every channel a slip of <n> located around <at>

    Examples:
      | mask       | n     | at   |
      | 0x00080000 | 4096  | 3005 |
      | 0x00000100 | 4096  | 3005 |
      | 0x00000100 | -2048 | 3040 |

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario Outline: a slip of whole blocks just after the planted flip arm fails with every arm found
    When a synthetic counter capture slips every channel <n> samples <k> samples after the planted flip arm
    Then the audio grader fails the run with every planted arm found

    Examples:
      | n     | k |
      | 4096  | 1 |
      | 4096  | 2 |
      | 4096  | 3 |
      | -4096 | 1 |
      | 8192  | 1 |

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario Outline: a constant-mask excursion beside a one-word corruption stays one bit-flip
    When a synthetic counter capture XORs 0x00080000 into 100 words from 3000 and flips the code bit at <flip>
    Then the audio grader reports one bit-flip of 100 words and the code-bit flip at <flip>

    Examples:
      | flip |
      | 2995 |
      | 3100 |
      | 3162 |

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario Outline: a code-bit corruption over whole blocks is one bit-flip wherever it ends
    When a synthetic counter capture flips the code bit of the words from <first> to <end> on one channel
    Then the audio grader reports one code-bit flip of those words

    Examples:
      | first | end  |
      | 2000  | 4096 |
      | 1000  | 6144 |
      | 2047  | 6143 |

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario: an event at a logged loss's own index counts that loss
    When a synthetic counter capture logs a 3000-frame loss at the index of its slip
    Then the slip's acquisition index and times include the 3000 lost frames

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario Outline: a journal-commit cut passes only with placed, non-vacuous evidence
    When a journal-commit cut <case>
    Then the state oracle grades the commit cut <verdict>

    Examples:
      | case                                                   | verdict |
      | restores the new snapshot inside its commit window     | PASS    |
      | restores the old snapshot inside its commit window     | PASS    |
      | restores a mix of old and new values                   | FAIL    |
      | pends default values while persistence is disabled     | NOT RUN |
      | pends one default value                                | NOT RUN |
      | lands after its commit window closed                   | NOT RUN |
      | has no cut-phase evidence                              | NOT RUN |

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario: a missed planted arm voids the audio run
    When a synthetic counter capture logs an arm the source never planted
    Then the audio grader voids the run as NOT RUN
    And a logged capture loss is attributed to the capture, not the DUT

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario Outline: each repeat detects omissions on both sides
    When release repeat <repeat> loses <role> <missing>
    Then that release area fails its own audit
    And the complete matrix still passes its audit

    Examples:
      | repeat               | role | missing        |
      | soak.continuous      | DUT  | talker index   |
      | soak.continuous      | DUT  | listener index |
      | soak.continuous      | DUT  | CRF sink       |
      | soak.continuous      | DUT  | AAF direction  |
      | soak.continuous      | DUT  | CRF direction  |
      | soak.continuous      | peer | talker index   |
      | soak.continuous      | peer | listener index |
      | soak.continuous      | peer | CRF sink       |
      | soak.continuous      | peer | AAF direction  |
      | soak.continuous      | peer | CRF direction  |
      | power.idle           | DUT  | talker index   |
      | power.idle           | DUT  | listener index |
      | power.idle           | DUT  | CRF sink       |
      | power.idle           | DUT  | AAF direction  |
      | power.idle           | DUT  | CRF direction  |
      | power.idle           | peer | talker index   |
      | power.idle           | peer | listener index |
      | power.idle           | peer | CRF sink       |
      | power.idle           | peer | AAF direction  |
      | power.idle           | peer | CRF direction  |
      | power.journal_commit | DUT  | talker index   |
      | power.journal_commit | DUT  | listener index |
      | power.journal_commit | DUT  | CRF sink       |
      | power.journal_commit | DUT  | AAF direction  |
      | power.journal_commit | DUT  | CRF direction  |
      | power.journal_commit | peer | talker index   |
      | power.journal_commit | peer | listener index |
      | power.journal_commit | peer | CRF sink       |
      | power.journal_commit | peer | AAF direction  |
      | power.journal_commit | peer | CRF direction  |
      | power.soft_reset     | DUT  | talker index   |
      | power.soft_reset     | DUT  | CRF sink       |
      | power.soft_reset     | peer | AAF direction  |
      | power.soft_reset     | peer | CRF direction  |
      | audio.integrity      | DUT  | talker index   |
      | audio.integrity      | DUT  | listener index |
      | audio.integrity      | DUT  | CRF sink       |
      | audio.integrity      | DUT  | AAF direction  |
      | audio.integrity      | peer | talker index   |
      | audio.integrity      | peer | CRF sink       |
      | audio.integrity      | peer | AAF direction  |
      | audio.integrity      | peer | CRF direction  |

  @class:release @clause:REQ-VER-06
  Scenario: release timing and totals are parameterized
    When a diagnostic release profile uses non-default timing and counts
    Then every release repeat preserves those parameters and its timing origins

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario Outline: partial CLI topology never qualifies the release profile
    When the release CLI omits only <shape> from the <role> topology
    Then every release repeat reports diagnostic topology

    Examples:
      | shape    | role |
      | CRF keys | DUT  |
      | listener | DUT  |
      | CRF keys | peer |
      | listener | peer |

  @class:release @clause:REQ-VER-06
  Scenario Outline: restoration eligibility honors the provisional release ceiling
    When an explicit release profile uses a restoration bound of <seconds> seconds
    Then every release repeat is <eligibility> for release

    Examples:
      | seconds | eligibility |
      | 29      | eligible    |
      | 30      | eligible    |
      | 31      | ineligible  |

  @class:release @clause:REQ-VER-06
  Scenario: uncertainty intervals need a recorded event and the implemented bound
    When the soak release area is planned
    Then uncertainty is correlated and bounded by half a second plus observation resolution

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario: the last discontinuity anchors a chained uncertainty interval
    When the soak release area is planned
    Then a chained discontinuity clearing at 0.62 seconds is PASS
    And a chained discontinuity clearing at 0.8 seconds is FAIL
    And an uncertainty interval without a discontinuity fails

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario Outline: wire observation resolution contains a lone discontinuity
    When the soak release area is planned
    Then a lone discontinuity at <event> seconds with <resolution> second resolution is <verdict>

    Examples:
      | event     | resolution | verdict |
      | -0.0005   | 0.001      | PASS    |
      | -0.002    | 0.001      | FAIL    |
      | 0         | 0.001      | PASS    |
      | 0         | 0          | PASS    |
      | -0.1      | 0.001      | FAIL    |
      | -0.001    | 0.001      | PASS    |
      | -0.001001 | 0.001      | FAIL    |
      | 0.4       | 0.001      | FAIL    |
      | 0.401     | 0.001      | FAIL    |

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario: a second successful boot cannot hide the first-boot restart
    Then the first-boot restart control fails the release boot assertion

  @class:runner
  Scenario: areas can be selected, and an unknown area is refused
    Then selecting the audio area yields only audio steps
    And selecting an unknown area raises
    And selecting nothing yields all configured areas

  @class:runner
  Scenario: the verdict record shape is stable and the exit codes are graded
    # 0 all good, 1 a SHALL failure, 2 only RECOMMENDED failures or outstanding
    # human entries. A SKIP alone never fails a run - it is honest - but it is
    # counted so it cannot hide.
    Then a verdict record carries schema, step, assertion, verdict, severity and clause
    And a SHALL failure exits 1
    And a RECOMMENDED failure exits 2
    And an outstanding human entry exits 2
    And a SKIP alone exits 0
    And the summary counts every verdict kind

  @class:release @clause:REQ-VER-06 @negative-control
  Scenario: every grandmaster change needs a following uncertainty hold
    When the soak release area is planned
    Then the planned uncertainty oracle rejects missing holds for every GM change
