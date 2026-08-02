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
  Scenario: the MAAP conflict entry asserts the withdraw-wait-reallocate sequence
    # Milan v1.2 Table 5.3 spells out the sequence, and the 2 LeaveAll wait is
    # part of it: an immediate re-claim is a different behaviour, not a faster
    # version of the same one.
    When the torture area is planned
    Then the MAAP conflict step asserts a withdraw and reallocate
    And the MAAP conflict clause mentions the LeaveAll wait

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
    # 2026-08-02: amx-pi OUT4 = the switch DN-1, OUT0 = the DUT) drives them
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
  @class:runner
  Scenario: areas can be selected, and an unknown area is refused
    Then selecting the audio area yields only audio steps
    And selecting an unknown area raises
    And selecting nothing yields all five areas

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
