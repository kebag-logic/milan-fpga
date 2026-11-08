[A750f] Decline, never drop, an ACMP command at the owed bound

Relates to #26

## What

With all `ACMP_OWED_MAX` (8) frames owed and the egress held, main drops a
further ACMP command and never answers it. This change makes the core decline
that command to the port instead. The port then delivers it again once room
returns, and the command gets its specified response.

- `acmp_rx` now returns `bool`. While all `ACMP_OWED_MAX` frames are owed, it
  returns `false` for a command addressed to this entity's listener or talker.
  A declined command changes no state, apart from the `bind_waiting` mark
  below, and makes no port call; `busy_declined` counts it (renamed from
  `busy_drops`). Every other frame is still taken and
  returns `true`: malformed, foreign and probe-response frames. A refused
  callback re-entry also returns `false`.
- A BIND_RX needs two free owed slots, one for its response and one for the
  first PROBE_TX of its binding (Milan v1.2 5.5.3.5, 5.5.3.5.3). With fewer free
  slots it is declined the same way, so a deferred binding never loses its first
  probe. The rule looks only at the message type.
- While such a BIND_RX waits for its second slot, a timer probe of any sink that
  falls due (a TMR_DELAY expiry or a TMR_NO_RESP retry) is held, with its timer
  re-armed 1 ms on, instead of owed. It neither delays the BIND_RX nor is lost;
  `probes_held` counts each held probe once per pass (round 3). No other expiry
  is held.
- New `acmp_rx_ready(const struct acmp *)`: `true` when `acmp_rx` takes any
  frame now, which needs two free owed slots; `false` otherwise or inside a port
  callback. A port whose receive ring cannot give a frame back tests this first
  and leaves the frame in its ring.
- Port contract (`docs/PORTING.md`, "ACMP owed bound"): keep a declined frame
  and deliver it again right after each `acmp_poll` that accepts an owed frame,
  before servicing `acmp_timer_expired`. Deliver no later ACMP frame before it.
  After each such poll, offer the waiting ACMP frames in arrival order, the
  kept one first, until `acmp_rx` declines one or none is left, and only then
  service the timers (round 5); the bound below assumes this.
  The served command receives its normal response behind the frames owed ahead
  of it, never an error status.
- The port contract derives when every kept command leaves: in pass
  n + 1 + f + r after the egress returns, where n is the number of frames owed
  then (`ACMP_OWED_MAX`, or one less when the first kept frame is a BIND_RX
  declined with one slot free), f counts the frames owed by the kept commands
  ahead of it and r the refused polls. It gives the egress-hold budget for the
  deepest backlog a port keeps (round 4; n since round 5).
- New requirement ACMP-12 (origin: issue #26), with traceability, test
  inventory, mutation plants and an RV32 smoke check.

### Why defer rather than answer with an error status

- IEEE 1722.1-2021 8.2.4 and 8.2.5 answer each received command through
  `txResponse`, and Table 8-3 has no status for a full output queue.
  `COULD_NOT_SEND_MESSAGE` is assigned only to a Listener whose own command to a
  Talker could not be sent (8.2.4.2.4).
- Milan v1.2 5.5.3.5 and 5.5.4 fix every response's fields and status; for
  example, GET_RX_STATE in UNBOUND answers SUCCESS (Table 5.34).
- While the egress is held, no answer can leave at once. An error frame would
  need the same storage as the deferred command.
- The deferred answer must still meet the 200 ms command timeouts of Milan v1.2
  Table 5.26 (IEEE 1722.1-2021 Table 8-1 allows 200 ms or more for each
  command).

## Round 2

Three new commits on top of the round 1 head 3d57262. Nothing was rebased or
amended.

1. **Answer checks for a deferred BIND_RX and GET_TX_STATE** (review finding F1).
   Round 1's body said the A19 test checks these two answers after
   redelivery. It only checks that they are declined. Two new tests now check
   the answers:
   - `AcmpOwed.DeclinedBindIsAnsweredAfterTheHold`
   - `AcmpOwed.DeclinedGetTxStateIsAnsweredAfterTheHold`

   Each test is caught by two plants: one that serves the command while the
   owed set is full (`owed-bind-rx-drop-restored`,
   `owed-get-tx-state-drop-restored`) and one that loses the redelivered answer
   (`owed-bind-answer-lost-after-decline`,
   `owed-get-tx-state-answer-lost-after-decline`). Both answer-lost plants pass
   the round 1 suite unnoticed.
2. **A new binding waits for two free owed slots** (suggestion S1 of both
   reviews). In round 1, a BIND_RX delivered again was taken with one slot
   free. Its response took that slot, and its first PROBE_TX was lost
   (`probes_lost` 1), so the binding waited for the 200 ms TMR_NO_RESP retry.
   Now the BIND_RX is declined once more with one slot free and taken with two.
   Its probe leaves in the pass after its answer, and `probes_lost` stays 0.
   - `acmp_rx_ready` now needs two free slots, so a port that relies on it
     alone never offers a BIND_RX that would be declined.
   - With no timer probe falling due, the pass count for every deferred answer
     is unchanged. A probe of another sink that fell due while the BIND_RX
     waited for its second slot took that slot and delayed it one pass each
     time (review finding F2). Round 3 holds such a probe instead.
   - Plants `owed-bind-one-slot`, `owed-bind-owes-one` and `owed-ready-one-slot`
     restore the one-slot rule and are all caught.
3. **Redelivery order against timer service** (suggestion S2 of the internal
   review). The port contract now says to deliver the kept frame right after the
   accepting `acmp_poll`, before timer service. The test port model polls,
   delivers kept frames, then services due timers.
   - If timers were serviced first, a timer probe could take the freed slot and
     decline the kept command for one more pass.
   - A timer probe that then finds every slot owed is counted in `probes_lost`,
     and its timeout recovers it, as before. Since round 3 this applies only
     while no probe is held and no BIND_RX waits for its second slot.

### Cost

- Owed-set memory is unchanged: 8 × 80 = 640 bytes, plus head and count, on
  both targets. `sizeof(struct acmp)` is unchanged: 5064 bytes RV32, 5072 bytes
  x86-64.
- RV32 instructions retired per call, counted under QEMU with exact instruction
  counting. The configuration has 16 sinks and 16 sources. "Round 1" is
  3d57262; "after" is this head.

  | Step | rv32i -O3 (`baremetal.py` Release): main | round 1 | after | rv32im -Os: main | round 1 | after |
  |---|---:|---:|---:|---:|---:|---:|
  | Worst measured `acmp_rx` step (BIND_RX behind 6 owed frames) | 7882 | 7899 | 7904 | 24374 | 24381 | 24383 |
  | A command behind the full owed set | 5408 (dropped) | 197 (declined) | 200 (declined) | 16522 (dropped) | 344 (declined) | 348 (declined) |
  | BIND_RX behind 7 owed frames | 7626 (probe lost) | 7643 (probe lost) | 200 (declined) | 23760 (probe lost) | 23767 (probe lost) | 348 (declined) |
  | GET_RX_STATE sent directly | 6250 | 6269 | 6274 | 19758 | 19763 | 19766 |
  | `acmp_poll`, one owed frame | 5436 | 5436 | 5436 | 16454 | 16454 | 16454 |
  | `acmp_rx_ready` | n/a | 9 | 10 | n/a | 9 | 10 |

- Bare-metal image (`scripts/baremetal.py`), main → round 1 → after:

  | Build | ELF bytes | `.text` | `acmp.c` object text |
  |---|---|---|---|
  | Release | 46552 → 47512 → 48152 | 34856 → 35752 → 36392 | 18053 → 18213 → 18537 |
  | Debug | 141724 → 144312 → 145380 | 45460 → 46928 → 47608 | 20729 → 20869 → 20917 |

  Debug ELF bytes depend on the build directory, which the debug information
  records. These three were built from exported trees at paths of equal length.
  Round 2 adds 324 bytes to the Release `acmp.c` object, from different -O3
  inlining. The rest of the growth is the longer RV32 smoke check. In an
  rv32im -Os build, the `acmp.c` object goes from 10697 (main) to 10689
  (round 1) to 10685 bytes.

### Integration note

- Ports must now keep a declined frame. A port that ignores the return value
  still loses the command, as before, and now also loses a BIND_RX offered
  with seven frames owed, which round 1 took with its first probe lost.
- A dispatcher with a per-channel receive-ready hook can bind it to
  `acmp_rx_ready` and leave the frame in its ring; the two-slot rule for
  BIND_RX then holds without further work. Such a port gives the core no sign
  of the waiting frame, so the round 3 hold cannot apply: each timer probe
  owed while the frame waits takes a slot ahead of it and delays it one pass,
  at most one per sink. It budgets `ACMP_OWED_MAX` + 1 + `n_sinks` passes
  against the 200 ms timeout, or offers the waiting frame from its ring after
  each accepting `acmp_poll` and leaves it there when declined
  (`docs/PORTING.md`, "ACMP owed bound").
- The parent firmware's mutant fragment in
  `sw/firmware/ctrl/test/acmp_mutants.py` (lines 452-453 at its current dev)
  matches the old `room()` body, `if (a->owed_count < ACMP_OWED_MAX)` …
  `a->busy_drops++`. That fragment must change in the same parent change that
  moves the pin to this head:
  - The body now reads `if (a->owed_count + frames <= ACMP_OWED_MAX)` …
    `a->busy_declined++`.
  - A plain `if (true)` replacement leaves `frames` unused and fails to compile
    with `-Werror`. This repository's `acmp-full-queue-acts` plant uses
    `if (a->owed_count + frames <= ACMP_OWED_MAX || true)`.
  - The same entry's lines 454-455 name the killer test
    `AcmpCore.A19AFullQueueDropsTheCommandBeforeItActs` and the needle "A19 a
    command whose response would find the queue full is dropped". This PR
    renames the test `AcmpCore.A19AFullQueueDeclinesTheCommandBeforeItActs`;
    its needle here is "is declined before it changes anything", and
    `AcmpOwed.HeldEgressDefersTheCommandBehindTheOwedSet` adds "is declined to
    the port, not taken".
- Round 3 changes the `sm_stop` body that the parent's
  `acmp-stop-keeps-the-hold` fragment selects
  (`sw/firmware/ctrl/test/acmp_review_mutants.py`, line 143 at its current
  dev). The body now also clears `probe_held`:
  `\ts->timer = ACMP_TIMER_NONE;\n\ts->timer_held = false;\n\ts->probe_held = false;\n}`.
  This repository's plant of the same name drops only the `timer_held` line.
  Every other ACMP fragment of the parent's two mutant tables that selects one
  place at 968a164 still selects one place at this head (checked by parsing
  both tables read-only, 198 fragments).
- The S2b harness row "an ACMP command behind the owed input" gets an answer
  time only after the parent firmware adopts this and the harness is measured
  again. That work is outside this repository, so this PR relates to #26
  rather than closing it.

## Sync with main d7e6a2a1

This sync merges main d7e6a2a1 (PR #29, issue #27: `wire_put_be` in two 32-bit
halves) into this branch with a merge commit. Nothing was rebased or amended.
The merge changes no ACMP source; it brings in main's change and regenerates
the generated files.

- Conflicts and their resolutions:
  - `docs/VERIFICATION.md`, mutation row: 413 core plants. That is the 411
    from this branch plus main's `wire-put-be-skips-an-odd-field-first-byte` and
    `wire-put-be-writes-past-an-odd-field`.
  - `docs/TRACEABILITY.md`: regenerated with `scripts/traceability.py --write`.
    ACMP-02 now also lists main's `Wire.W1PutBeWritesTheLowBytesMostSignificantFirst`.
  - `tests/coverage.ratchet`: regenerated with `scripts/coverage.py --write` on
    Ubuntu 24.04 with GCC 13.3 and GoogleTest 1.14, CI's packages. Result:
    `include/wire.h` 14/14 lines and `src/acmp.c` 795/795 lines and 402/402
    branches.
- `docs/TESTS.md` merged without a conflict but kept main's stale line anchor
  for the Wire test. `scripts/test_inventory.py --write` corrected it.
- The mutation campaign catches all 417 plants, from both sides.
- Every gate on both targets passes except one: `privacy` fails, as it does on
  main itself at d7e6a2a1 (CI run 42467930308). The gate needs a one-line
  message on every reachable commit, and main's merge commit for PR #29 has a
  second paragraph. A change on main has to fix this, for example by extending
  the gate's exact-commit exception to d7e6a2a1. After that, this branch needs
  another sync and no other change. Main fixed this in #30; see Sync with main
  cc3362f8.

### Cost after the sync

Main's `wire_put_be` change moves the send paths. This branch's decline paths
and the owed-set memory do not move: `sizeof(struct acmp)` is still 5064 bytes
on RV32 and 5072 bytes on x86-64. Figures are RV32 instructions retired per
call, from the same harness and configuration as above.

| Step | rv32i -O3: round 2 | main d7e6a2a1 | after sync | rv32im -Os: round 2 | main d7e6a2a1 | after sync |
|---|---:|---:|---:|---:|---:|---:|
| Worst measured `acmp_rx` step (BIND_RX behind 6 owed frames) | 7904 | 8039 | 8061 | 24383 | 22251 | 22260 |
| A command behind the full owed set | 200 (declined) | 5408 (dropped) | 200 (declined) | 348 (declined) | 16522 (dropped) | 348 (declined) |
| BIND_RX behind 7 owed frames | 200 (declined) | 7783 (probe lost) | 200 (declined) | 348 (declined) | 21637 (probe lost) | 348 (declined) |
| GET_RX_STATE sent directly | 6274 | 6317 | 6341 | 19766 | 18817 | 18825 |
| `acmp_poll`, one owed frame | 5436 | 5436 | 5436 | 16454 | 16454 | 16454 |
| `acmp_rx_ready` | 10 | n/a | 10 | 10 | n/a | 10 |

Bare-metal image (`scripts/baremetal.py`), round 2 → main d7e6a2a1 → after
sync. All three were built from exported trees at paths of equal length:

| Build | ELF bytes | `.text` | `acmp.c` object text |
|---|---|---|---|
| Release | 48152 → 47352 → 48952 | 36392 → 35652 → 37188 | 18537 → 18413 → 18897 |
| Debug | 145180 → 141796 → 145492 | 47608 → 45380 → 47528 | 20917 → 20713 → 20901 |

Round 2's Debug ELF reads 145180 here and 145380 in the Round 2 table because
the two sets were built at different paths, which the debug information
records; `.text` and the `acmp.c` object agree. Compare Debug ELF bytes only
within one table.

Release grows by 360 bytes in the `acmp.c` object, because -O3 inlines the
two-half `wire_put_be`. In an rv32im -Os build the object shrinks from 10685 to
10605 bytes.

## How to validate

```sh
python3 scripts/validate.py --work build-validation --jobs 16 --graphs
python3 scripts/baremetal.py --work build-rv32 --jobs 16
python3 scripts/mutation.py --work build-mutations --jobs 16 --select owed-
```

Each test below fills the owed set with the egress held, then releases the
egress after 60 ms. The test port model polls once per 1 ms pass, then offers
every waiting frame in arrival order until `acmp_rx` declines one or none is
left, then services its timers.

- `AcmpOwed.HeldEgressDefersTheCommandBehindTheOwedSet`: a GET_RX_STATE is
  declined with no port call and counted. After the hold it is answered with
  its Milan Table 5.34 fields, 69 ms after arrival and within 200 ms, in the
  pass after the eight frames owed ahead of it. All nine answers leave in
  order.
- `AcmpOwed.TalkerCommandsBehindTheOwedSetAreAnsweredInTime`: a PROBE_TX is
  declined, reads no source state and is counted. A DISCONNECT_TX and a
  GET_TX_CONNECTION wait behind it in the port. After the hold all three are
  answered with their Table 5.43, 5.45 and 5.48 fields, within 200 ms and in
  arrival order.
- `AcmpOwed.DeclinedUnbindChangesNothingUntilItIsTaken`: an UNBIND_RX for a
  bound sink is declined. It changes no instance byte except its counter and
  calls no port, environment or publish service. After the hold it unbinds and
  is answered with its Table 5.36 fields within 200 ms.
- `AcmpOwed.DeclinedBindIsAnsweredAfterTheHold` (new): a BIND_RX is declined.
  It binds nothing, makes no port call and is counted. A GET_RX_STATE waits
  behind it in the port. After the hold, the BIND_RX is answered with its
  Table 5.32 fields: SUCCESS, count 1, the streaming-wait flag echoed, no
  stream fields. The answer leaves 69 ms after arrival, right after the eight
  owed frames, which leave first and in order. The GET_RX_STATE behind it is
  answered later, at 71 ms, and reports the new binding.
- `AcmpOwed.DeclinedGetTxStateIsAnsweredAfterTheHold` (new): a GET_TX_STATE is
  declined, reads no source state and is counted. A GET_TX_CONNECTION waits
  behind it in the port. The source state changes during the hold. Afterwards
  the GET_TX_STATE is answered with its Table 5.47 fields: listener fields
  cleared, connection count 0, registering-failed flag, and stream ID,
  destination MAC and VLAN from the source state at the time it is taken. The answer leaves 69 ms after
  arrival, right after the eight owed frames. The GET_TX_CONNECTION is answered
  next, at 70 ms.
- `AcmpOwed.DeferredBindWaitsForTwoSlotsAndLosesNoProbe` (new): a BIND_RX is
  declined at 8 owed, declined again at 7 and taken at 6, so its answer and its
  probe are both owed. After the drain, `probes_lost` is 0. The answer leaves at
  69 ms and the first PROBE_TX at 70 ms, in the next pass. The sink waits in
  PRB_W_RESP with its retry unused, and TMR_NO_RESP runs from the probe's send
  time.
- `AcmpOwed.ProbesFallingDueInTheDrainWaitForTheDeferredBind` (round 3): other
  sinks' probes fall due during the drain while a BIND_RX waits. Five cases:
  one TMR_NO_RESP retry in pass 1; one TMR_DELAY expiry in pass 1; four
  retries, one per pass; four retries in the same pass; two retries with two
  GET_RX_STATE commands kept behind the BIND_RX. In each case the BIND_RX is
  declined once more and taken in pass 2, and answered in pass
  `ACMP_OWED_MAX` + 1 (69 ms), right after the eight owed frames.
  `probes_lost` is 0. Its own probe leaves next, then the commands kept behind
  it, then every held probe in sink order. Each held probe is owed exactly in
  the pass the documented bound gives, its TMR_NO_RESP runs from when it left,
  and `probes_held` equals the passes each probe was held, summed over the held
  probes. Since round 4 the case with two kept commands also asserts their
  answer passes, 11 and 12.
- `AcmpOwed.DeferredBindAtTheDocumentedMarginMeetsItsTimeout` (round 3): a
  191 ms hold leaves exactly the documented passes. With one and with four
  retries falling due from pass 1, the BIND_RX answer leaves at 200 ms, within
  Milan v1.2 Table 5.26, and every probe is held and sent, none lost. Without
  the hold it leaves at 201 ms and 204 ms.
- `AcmpOwed.HoldEndsWithTheLastHeldProbe` (round 3): a retry held beside the
  waiting BIND_RX is dropped with its probing when its talker departs. With no
  probe held and no BIND_RX waiting, a later retry that finds every slot owed is
  lost and counted again.
- `AcmpOwed.KeptCommandsLeaveOnePassPerFrameOwedAheadOfThem` (round 4): nine
  frames wait behind the full set: a BIND_RX, a GET_RX_STATE, a BIND_RX for an
  unknown sink, a rebind to the same talker, an UNBIND_RX, a foreign frame, a
  GET_TX_STATE, a second new binding and a GET_RX_STATE. Four retries fall due
  from pass 1 and are held. Each answer leaves in exactly pass
  `ACMP_OWED_MAX` + 1 + f (9, 11, 12, 13, 14, 15, 16 and 18); the held probes
  follow the last kept frame one per pass, in sink order, none lost.
- `AcmpOwed.KeptCommandsBehindSevenOwedLeaveOnePassSooner` (round 5): the
  egress returns with seven frames owed, behind a BIND_RX declined with one slot
  free, a GET_RX_STATE and a second new binding. A retry falling due in the
  hold is held. The answers leave in passes 8, 10 and 11, each
  `ACMP_OWED_MAX` + f, and the held retry follows in pass 13, none lost.
- `AcmpOwed.AnsweredProbeEndsTheHoldOfItsRetry` (round 5): the answer to the
  probe a held retry repeats waits behind the kept BIND_RX; once taken it ends
  the hold, with a failure status in PRB_W_RETRY and with SUCCESS in
  SETTLED_NO_RSV, and the retry is never sent.
- `AcmpOwed.KeptBacklogWithinTheDocumentedBudgetMeetsItsTimeout` (round 4):
  five backlogs, each with the hold the budget allows (200 ms less
  `ACMP_OWED_MAX` + 1 + f passes, for example 187 ms for three new bindings).
  The last kept command leaves at exactly 200 ms and every other one within it.
- `AcmpOwed.RefusedPollLeavesTheBindWaitingAndItsHold` (round 4): the egress
  refuses one poll while the BIND_RX waits, and a retry falls due in that pass.
  For a port that delivers again only after accepting polls, and for one that
  delivers after every poll, `bind_waiting` stays set, the frame delivered
  again is declined, the retry is held with its timer 1 ms on, and the BIND_RX
  is answered in pass `ACMP_OWED_MAX` + 2 at position 8.
- `AcmpOwed.OnlyTimerProbesAreHeldBesideTheWaitingBind` (round 4): while a
  BIND_RX waits, the TMR_NO_RESP that ends PRB_W_RESP2, a TMR_RETRY and a
  TMR_NO_TK each take their Milan v1.2 5.5.3.5.23, .30 and .36 transitions at
  their deadlines; `probes_held` stays 0.
- `AcmpOwed.BindDeclinedBehindTheFullSetHoldsNoProbe` (round 4): a BIND_RX
  declined with no slot free sets no `bind_waiting`; a retry falling due before
  the egress returns is lost and counted, and its timeout runs.
- `AcmpOwed.BindToAnotherTalkerEndsTheHoldOfTheProbeItReplaces` and
  `AcmpOwed.SameTalkerRebindKeepsTheHeldProbe` (round 4): a new binding clears
  `probe_held`, so the next full-set retry is lost; a rebind to the same talker
  keeps the held probe, which is owed once a slot is free.
- `AcmpOwed.GatedPortBudgetsOnePassPerProbeOwedAhead` (round 4): a port that
  tests `acmp_rx_ready` instead of offering its frame has nothing declined or
  held; four retries owed meanwhile delay its BIND_RX to pass 13, one pass each.
- `AcmpOwed.AnsweredOnlyBindAlsoWaitsForTwoSlots` and
  `AcmpOwed.OwedSetIsEightFramesOfEightyBytes` (round 4): a BIND_RX for an
  unknown sink and a same-talker rebind are declined at one free slot; the owed
  set is 8 × 80 = 640 bytes.
- `AcmpOwed.ReadyPredicateMatchesTheOwedBound`: checks the readiness boundary
  and callback re-entry.
  - 6 owed is ready; 7 owed is not.
  - At 7 owed a BIND_RX is declined and a GET_RX_STATE is taken.
  - 8 owed is not ready. One accepted frame leaves it not ready; a second makes
    it ready.
- `AcmpOwed.OnlyOwnCommandsAreDeclined`: with the set full, malformed, foreign
  and probe-response frames are still taken.
- `AcmpCore.A19AFullQueueDeclinesTheCommandBeforeItActs`: with the set full, a
  BIND_RX and a GET_TX_STATE are each declined, the sink stays UNBOUND, no port
  is called and both are counted. It does not release the egress; the two new
  tests above check those answers.
- Mutation plants:
  - 53 `owed-*` plants, all caught, and nine ACMP plants that the owed-bound
    assertions also kill (`acmp-full-queue-acts`, `acmp-stop-keeps-the-hold`,
    `acmp-probe-before-response`, `acmp-rebind-same-reprobes`,
    `acmp-owed-probe-no-resp-2s`, `acmp-lost-probe-uncounted`,
    `acmp-poll-newest-first`, `acmp-poll-drains-everything` and
    `acmp-response-passes-an-owed-frame`).
  - Each per-command plant restores the silent drop for its command only.
  - Run against the full ACMP test binary (125 tests at this head: 124 ACMP
    tests and main's Wire test), every one of these 62 plants fails at least
    one test and passes once its failing tests are excluded. Seven of the 15
    round 4 plants pass the whole round 3 suite, and both round 5 plants pass
    every test but the round 5 test that kills each.
  - The campaign counts 439 core plants (437 from this branch and main's two
    `wire-put-be-*` plants) and 4 generated configuration plants.
- The RV32 smoke check `acmp_owed_smoke` steps through the bound:
  - The core is ready through 6 owed frames.
  - It declines the ninth command and takes it once room returns.
  - It declines a BIND_RX at 7 owed and takes it at 6.
  - The ninth answer, the BIND_RX answer and then its probe leave in that
    order, and `probes_lost` stays 0.
  - Round 3: with the set full again and a BIND_RX for a second sink kept,
    the first sink's TMR_NO_RESP retry falls due in pass 1. It is held in
    passes 1 and 2, the BIND_RX is answered in pass `ACMP_OWED_MAX` + 1, its
    probe leaves next and the held retry after it, with `probes_lost` 0.

## Sync with main cc3362f8

Main's privacy gate is green again (PR #30 exempts the merge of #29 from the one-line rule). This branch merges main at `968a164`; the only conflict was `CHANGELOG.md`, where both Unreleased entries are kept. At the merge head `check_privacy.py` (25 commits) and its self-test, `check_comments.py`, `check_port_contracts.py --selftest` and `check_license.py` pass.

## Round 3

Three new commits on top of 968a164 (round 2 plus both syncs with main).
Nothing was rebased or amended.

1. **Timer probes no longer overtake a deferred BIND_RX** (finding F2 of both
   reviews, taken as a design change).
   - The defect: the two-slot rule declines a BIND_RX delivered again with one
     slot free. The timer service that followed could owe another sink's probe
     into that slot, so the BIND_RX, and every command behind it, slipped one
     pass for each such probe. With the 191 ms hold that the documented pass
     count leaves, one probe put the BIND_RX answer at 201 ms, past the 200 ms
     of Milan v1.2 Table 5.26.
   - The change, in `src/acmp.c` only:
     - A BIND_RX declined with one slot free sets `bind_waiting`. The next
       `acmp_poll` that accepts an owed frame clears it; a port that follows the
       contract then delivers the BIND_RX again before its timer service.
     - While `bind_waiting` is set, at most one slot is free. A TMR_DELAY
       expiry or TMR_NO_RESP retry of any sink that falls due then is held
       instead of owed: its timer is re-armed 1 ms on, so the next pass retries
       it when passes are at least 1 ms apart, and `probes_held` counts each
       held probe once per pass.
     - A held probe is never lost. While any probe is held, a probe that finds
       every slot owed is held with it. Held probes take freed slots one per
       pass, after the commands the port still keeps.
     - With no probe held and no BIND_RX waiting, a probe that finds every slot
       owed is still lost and counted in `probes_lost`, as before.
   - Result: a deferred BIND_RX at the head of the kept frames is answered in
     pass n + 1 (`ACMP_OWED_MAX` + 1 from a full set), whatever probes fall
     due; a command kept behind it follows one pass per frame owed ahead of
     it. No timer probe is owed ahead of a kept command. Round 4 derives the
     whole bound.
   - The held probe's own delay, stated in `docs/PORTING.md` "ACMP owed bound"
     (Milan v1.2 5.5.3.5): it waits at most from the pass it falls due through the pass
     that takes the BIND_RX, plus one pass for each frame owed by a command
     kept behind the BIND_RX and for each other probe owed before it, at most
     one per other sink under the conditions Round 5 states. Its TMR_NO_RESP
     runs from when it leaves, so its response window is unchanged.
   - New state: `acmp.bind_waiting` and `acmp_sink.probe_held`, which fill
     existing padding, and the counter `acmp.probes_held`.
2. **Review suggestions and residue.**
   - `DeclinedGetTxStateIsAnsweredAfterTheHold` also asserts connection count 0.
   - `docs/ARCHITECTURE.md` names the BIND_RX slot rule.
   - The RV32 smoke `acmp_owed_smoke` has the same timer-probe step.
   - This body: the Round 2 pass-count sentence, the sync section's wording and
     Debug ELF note, the test count in "How to validate", and the integration
     note's parent killer test, needles, gated-port budget and changed fragment.
   - The round 3 test also covers commands kept behind the BIND_RX.
3. **Wording.** The hold covers a timer probe of any sink, which would take the
   last free owed slot or find none.

### Evidence

Pass counts from the round 3 tests (60 ms hold unless stated; 1 ms passes):

| Case | BIND_RX answer: this head | with the hold removed (`owed-timer-probe-not-held`) |
|---|---|---|
| One TMR_NO_RESP retry in pass 1 | pass 9 (69 ms) | pass 10 |
| One TMR_DELAY expiry in pass 1 | pass 9 | pass 10 |
| Four retries, one per pass from pass 1 | pass 9 | pass 13 |
| Four retries, all in pass 1 | pass 9 | pass 10 |
| 191 ms hold, one retry from pass 1 | 200 ms | 201 ms |
| 191 ms hold, four retries, one per pass | 200 ms | 204 ms |

At this head every case also has `probes_lost` 0, and every held probe is sent.

Plants, all caught:

- Nine new: `owed-timer-probe-not-held`, `owed-hold-skips-delay`,
  `owed-hold-skips-retry`, `owed-held-probe-lost`, `owed-bind-wait-unset`,
  `owed-bind-wait-kept`, `owed-hold-uncounted`, `owed-hold-rearmed-late` and
  `owed-held-flag-kept`. Each passes the full ACMP binary once the three round
  3 tests are excluded, so the round 2 suite would have missed it.
- Re-anchored for the new lines, meaning unchanged: `owed-listener-drop-restored`,
  `owed-listener-acts-then-declines` and `acmp-stop-keeps-the-hold`.
- On RV32, seven of the nine make `acmp_owed_smoke` exit nonzero (checks 104,
  105 and 106) in Debug and Release. `owed-hold-skips-delay` and
  `owed-held-flag-kept` need a TMR_DELAY expiry or a talker departure, which
  only the hosted tests drive.
- Campaign: 426/426 caught (422 core, 4 generated configuration).

Coverage: `src/acmp.c` 813/813 lines and 424/424 branches, regenerated in the
CI environment (Ubuntu 24.04, GCC 13.3, GoogleTest 1.14).

### Memory and cost

- The owed set is unchanged: 8 × 80 = 640 bytes on both targets.
  `sizeof(struct acmp_sink)` is unchanged at 256 bytes. `sizeof(struct acmp)`
  grows by 8 bytes, 5064 → 5072 on RV32 and 5072 → 5080 on x86-64: 4 for
  `probes_held` and 4 of alignment padding. The two flags fill existing
  padding.
- RV32 instructions retired per call, as before (QEMU `virt`, exact
  instruction counting, 16 sinks and 16 sources). "Before" is 968a164. Three
  timer rows are new to the harness; the other rows match the earlier harness.

| Step | rv32i -O3: before | after | rv32im -Os: before | after |
|---|---:|---:|---:|---:|
| Worst measured `acmp_rx` step (BIND_RX behind 6 owed frames) | 8061 | 8062 | 22260 | 22261 |
| A command behind the full owed set (GET_RX_STATE) | 200 | 200 | 348 | 350 |
| BIND_RX behind the full owed set | 200 | 202 | 348 | 350 |
| BIND_RX behind 7 owed frames (declined, sets `bind_waiting`) | 200 | 205 | 348 | 355 |
| GET_RX_STATE sent directly | 6341 | 6341 | 18825 | 18826 |
| `acmp_poll`, one owed frame | 5436 | 5437 | 16454 | 16455 |
| `acmp_rx_ready` | 10 | 10 | 10 | 10 |
| Timer retry owed behind 7 frames | 6666 | 6679 | 19100 | 19142 |
| Timer retry beside a BIND_RX waiting at 7 (owed before, held now) | 6666 | 5575 | 19100 | 16753 |
| Timer retry behind the full set (lost; scans 16 sinks for a held probe) | 6408 | 6491 | 18500 | 18641 |

- Bare-metal image (`scripts/baremetal.py`), 968a164 → this head, both built
  from exported trees at paths of equal length:

| Build | ELF bytes | `.text` | `acmp.c` object text |
|---|---|---|---|
| Release | 48952 → 50504 | 37188 → 38668 | 18897 → 19365 |
| Debug | 145432 → 150332 | 47528 → 49812 | 20901 → 21321 |

  The Release `acmp.c` object grows by 468 bytes; the rest of the Release
  growth is the longer RV32 smoke check. In an rv32im -Os build the object goes
  from 10605 to 10789 bytes. The 968a164 Release ELF is byte-identical to the
  one recorded for the first sync. Debug ELF bytes depend on the build path, as
  noted above.

### Gates at the round 3 head (b7a5988)

On a clean clone of this head, `python3 scripts/validate.py --work <w> --jobs 16 --graphs`
returns 0 for all 28 gates, including the full mutation campaign (426 caught,
0 escaped, 0 errors), privacy, coverage, both sanitizer arms, static analysis
and graphs. `python3 scripts/baremetal.py --work <w> --jobs 8` returns 0 in
Debug and Release. Each of the three commits passed the same gates on its own
tree before it was committed.

## Round 4

Three new commits on top of b7a5988. Nothing was rebased or amended. No core
source changes: `src/`, `include/` and `examples/` are as at round 3, so the
behaviour, memory, instruction counts and bare-metal image are unchanged. This
round states the whole timing bound and pins every behaviour that ACMP-12 and
the port contract state.

1. **The whole bound** (finding F3 of the internal review).
   - Round 3 gave one pass count, `ACMP_OWED_MAX` + 1, for every kept command.
     It holds only for the first. A command kept behind others leaves one pass
     later for each frame they owe: at the 191 ms hold, a GET_RX_STATE kept
     behind a BIND_RX was answered at 202 ms.
   - `docs/PORTING.md` "ACMP owed bound" now derives the bound in one place:
     - Each accepted `acmp_poll` sends the oldest owed frame, and the owed set
       never empties while a command is kept, because a command is declined
       only with seven or eight frames owed. So owed frames leave one per pass,
       and each refused poll delays every later frame by one pass.
     - Each slot an accepted poll frees goes to the oldest kept command. No
       timer probe is owed ahead of a kept command.
     - So a kept command leaves in pass n + 1 + f + r. Here n, `ACMP_OWED_MAX`
       or one less, is the number of frames owed when the egress returns (one
       less only when the first kept frame is a BIND_RX declined with one slot
       free; round 5). f counts the frames owed by the kept commands ahead of
       it: two for a BIND_RX that starts a binding, one for any other command
       (a BIND_RX that is only answered included), none for a frame that needs
       no answer. r counts the polls refused since the egress returned.
     - Held probes follow the frames of the last kept command, one per pass. A
       held probe's own wait is as round 3 stated it, now as an upper bound.
     - Budget: with passes p ms apart, the hold plus
       (`ACMP_OWED_MAX` + 1 + f + r) × p ms must stay within the 200 ms of
       Milan v1.2 Table 5.26 for the last command the port keeps. For Q kept
       commands f is at most 2 × (Q − 1), so with 1 ms passes and no refused
       poll a hold of at most 193 − 2 × Q ms meets every timeout: 191 ms for
       one kept command, 189 ms for two. The budget uses `ACMP_OWED_MAX` for
       n, so it holds from either start.
     - The redelivery rule the bound assumes is stated with a refused poll: it
       frees no slot and leaves `bind_waiting` set, so the port may wait for
       the next accepting poll or deliver the kept frame again, which is
       declined again.
     - The bound assumes that after each `acmp_poll` that accepts an owed
       frame the port offers its waiting ACMP frames in arrival order, the kept
       one first, until `acmp_rx` declines one or none is left, and only then
       services `acmp_timer_expired`. Since round 5 the redelivery rule says
       so; a port that offers fewer can leave a slot free for a timer probe
       ahead of a later kept command.
   - The Round 3 "Result" sentence above now reads: a deferred BIND_RX at the
     head of the kept frames is answered in pass n + 1 (`ACMP_OWED_MAX` + 1
     from a full set), whatever probes fall due; a command kept behind it
     follows one pass per frame owed ahead of it.
   - Two new tests assert the bound, and the round 3 drain test's kept-behind
     case now asserts the kept answers' passes (11 and 12).
   - `scripts/check_port_contracts.py` pins 16 new phrases of the derivation,
     the hold's scope and the residue wording; its self-test refuses 61
     meaning-removal controls, up from 45.
2. **Every stated behaviour pinned** (finding F4 of the internal review,
   finding F3 of the external review).
   - Each sentence of ACMP-12 (its prose and its requirement row) and of the
     owed-bound section was mapped to the named assertions that pin what it
     states, and to the registered plants those assertions kill. There are 64
     sentences and clauses. Each of the 50 that state core behaviour has at
     least one named assertion and a registered plant that it kills and the
     campaign catches. Five are port obligations, whose effect on the core is
     asserted where it has one. The other nine are references, rationale,
     assumptions and the target statement. A checker verifies the map against
     the tree, the registered kills, the campaign results and the escape
     evidence; the map and the checker are published with the round 4
     evidence.
   - ACMP-12 now says that the hold lasts until the next accepted owed frame
     and covers timer probes and no other expiry.
   - New tests, and the plants each one kills:

| Test | What it pins | Plants it kills |
|---|---|---|
| `KeptCommandsLeaveOnePassPerFrameOwedAheadOfThem` | Every kept frame kind behind the full set: each answer in pass `ACMP_OWED_MAX` + 1 + f; held probes after the last kept frame, one per pass | acmp-rebind-same-reprobes, owed-bind-wait-unset, owed-timer-probe-not-held |
| `KeptBacklogWithinTheDocumentedBudgetMeetsItsTimeout` | Five backlogs at the budgeted hold: the last answer at exactly 200 ms, the others within it | owed-bind-wait-unset, owed-timer-probe-not-held |
| `RefusedPollLeavesTheBindWaitingAndItsHold` | A refused poll frees nothing and keeps `bind_waiting`; a redelivered frame is declined; the retry is held 1 ms on; one pass of delay | owed-bind-one-slot, **owed-bind-wait-cleared-by-refused-poll**, owed-hold-rearmed-late, owed-refused-poll-drops-the-frame, owed-timer-probe-not-held |
| `OnlyTimerProbesAreHeldBesideTheWaitingBind` | The PRB_W_RESP2 timeout, TMR_RETRY and TMR_NO_TK run at their deadlines beside a waiting BIND_RX | **owed-hold-widened-to-every-timer**, **owed-hold-widened-to-second-no-resp** |
| `BindDeclinedBehindTheFullSetHoldsNoProbe` | A BIND_RX declined at 8 owed sets no wait; a retry is lost and counted, its timeout running | **owed-bind-wait-set-at-full**, owed-hold-whenever-full |
| `BindToAnotherTalkerEndsTheHoldOfTheProbeItReplaces` | A new binding clears `probe_held`; the next full-set retry is lost | owed-hold-whenever-full, **owed-rebind-keeps-the-hold** |
| `SameTalkerRebindKeepsTheHeldProbe` | A same-talker rebind keeps the held probe, owed once a slot is free | owed-same-talker-rebind-cancels-the-hold |
| `GatedPortBudgetsOnePassPerProbeOwedAhead` | A port that tests `acmp_rx_ready`: nothing declined or held, one pass per probe owed meanwhile | owed-ready-ignores-full, owed-ready-one-slot |
| `AnsweredOnlyBindAlsoWaitsForTwoSlots` | An unknown-sink BIND_RX and a same-talker rebind are declined at one free slot | **owed-answered-bind-takes-one-slot** |
| `OwedSetIsEightFramesOfEightyBytes` | The owed set is 8 frames of 80 bytes, 640 bytes | **owed-entry-widened** |

   - Reviewer plants. Each review's plant names stay free, so that its
     scripts run unchanged; the same edit is registered under an `owed-` name:

| Review plant | Registered as | Killed by |
|---|---|---|
| `rv-bind-wait-cleared-by-every-poll` (internal) | `owed-bind-wait-cleared-by-refused-poll` | `RefusedPollLeavesTheBindWaitingAndItsHold` |
| `rv-bind-wait-set-when-full` (internal), `reviewer-bind-wait-at-full` (external) | `owed-bind-wait-set-at-full` | `BindDeclinedBehindTheFullSetHoldsNoProbe` |
| `rv-hold-widened-to-the-timeout` (internal), `reviewer-hold-second-no-resp` (external) | `owed-hold-widened-to-second-no-resp` | `OnlyTimerProbesAreHeldBesideTheWaitingBind` |
| `rv-hold-widened-to-every-timer` (internal), `reviewer-hold-every-timer` (external) | `owed-hold-widened-to-every-timer` | `OnlyTimerProbesAreHeldBesideTheWaitingBind` |
| `rv-bind-unsets-no-hold` (internal) | `owed-rebind-keeps-the-hold` | `BindToAnotherTalkerEndsTheHoldOfTheProbeItReplaces` |
| `rv-probe-held-never-set` (internal) | `owed-probe-held-never-set` | `BindToAnotherTalkerEndsTheHoldOfTheProbeItReplaces`, `DeferredBindAtTheDocumentedMarginMeetsItsTimeout`, `HoldEndsWithTheLastHeldProbe`, `KeptCommandsLeaveOnePassPerFrameOwedAheadOfThem`, `ProbesFallingDueInTheDrainWaitForTheDeferredBind`, `RefusedPollLeavesTheBindWaitingAndItsHold`, `SameTalkerRebindKeepsTheHeldProbe` |
| `rv-hold-scan-skips-the-last-sink` (internal), `reviewer-scan-skips-last-sink` (external) | `owed-hold-scan-skips-the-last-sink` | `DeferredBindAtTheDocumentedMarginMeetsItsTimeout`, `KeptCommandsLeaveOnePassPerFrameOwedAheadOfThem`, `ProbesFallingDueInTheDrainWaitForTheDeferredBind`, `RefusedPollLeavesTheBindWaitingAndItsHold`, `SameTalkerRebindKeepsTheHeldProbe` |
| `rv-hold-whenever-full` (internal) | `owed-hold-whenever-full` | `A19AProbeWithoutRoomIsLostAndRecovered`, `BindDeclinedBehindTheFullSetHoldsNoProbe`, `BindToAnotherTalkerEndsTheHoldOfTheProbeItReplaces`, `HoldEndsWithTheLastHeldProbe` |
| `reviewer-hold-at-seven` (external) | `owed-hold-at-seven` | `ProbesFallingDueInTheDrainWaitForTheDeferredBind`, `SameTalkerRebindKeepsTheHeldProbe` |

   - Escape evidence: against the full ACMP test binary (123 tests: 122 ACMP
     tests and main's Wire test), each of the 60 owed-bound plants fails at
     least one test and passes once its failing tests are excluded. Seven of
     the 15 new plants pass the whole round 3 suite. A plant in bold escapes
     once only that one test is excluded.
3. **Residue and suggestions.** `probes_held` counts each held probe once per
   pass (PORTING and the counter row); a held probe waits "at most" its bound;
   the 1 ms re-arm is the next pass only for passes at least 1 ms apart, and
   the pass counts say so; a held probe is never dropped for want of a slot and
   is cancelled only when its sink stops probing or, for a retry, when the probe
   it repeats is answered (round 5). Two suggestions are taken: a held probe
   keeps waiting, its timer re-armed every 1 ms and its probing not advancing
   until it is owed or cancelled, while the port keeps commands or nothing is
   accepted; the one-per-sink counts hold while no sink's probing restarts (an
   ADP re-advertisement that does not raise the available index, a new
   discovery after its talker departs or its advertisement times out, or
   `acmp_tk_unregistered`) and, for a held probe, while it has waited less than
   TMR_NO_RESP (200 ms); past that, another sink's TMR_NO_RESP retry can also be
   owed before it (round 5). This body: the Round 3 "Result" sentence and the
   `probes_held` wording.

### Both reviews' scripts at this head

Both round 3 reviews published their probe and plant scripts. They were rerun
unchanged on a clean clone of this head:

- The internal review's eight plants: each now fails at least one of the 123
  tests. At round 3, five of them passed every test.
- The external review's five plants: each fails the full ACMP binary, and the
  three that passed every ctest target at round 3 now fail the ACMP target. The
  RV32 smoke does not step through these boundaries, so they still exit 0 there.
- The external review's boundary probes pass at this head, and each of its
  three plants fails the probe for its boundary.
- The probes agree with the derivation. A mixed backlog of five kept commands
  is answered in passes 9, 11, 12, 14 and 15, each `ACMP_OWED_MAX` + 1 + f
  from the full set. A
  BIND_RX and then a GET_RX_STATE kept at a 191 ms hold leave at 200 ms and
  202 ms; the budget for two kept commands is 189 ms. A refused poll puts the
  BIND_RX in pass 10 with the retry after it. A gated port with 14 retries
  answers in pass 23, within its budget of 25.

### Gates at this head

On a clean clone of this head, `python3 scripts/validate.py --work <w> --jobs 16 --graphs`
returns 0 for all 28 gates, including the full mutation campaign (441 caught,
0 escaped, 0 errors), privacy, coverage (`src/acmp.c` 813/813 lines and 424/424
branches, unchanged), both sanitizer arms, static analysis and graphs.
`python3 scripts/baremetal.py --work <w> --jobs 8` returns 0 in Debug and
Release. Each of the three commits passed the same gates on its own tree
before it was committed.

The core is unchanged, so memory and instruction counts are as in the Round 3
tables. The Release RV32 image is byte-identical to round 3's: 50504 bytes,
`.text` 38668, `acmp.c` object text 19365. The Debug image is 150332 bytes for
both heads, built from exported trees at paths of equal length.

## Round 5

Four new commits on top of a0a3211. Nothing was rebased or amended. No core
source changes: `src/`, `include/` and `examples/` are as at round 3, so the
behaviour, memory, instruction counts and bare-metal image are unchanged. All
three round 4 findings concern the port contract's timing statements; the core
behaves as stated in every case.

1. **The port offers every waiting frame** (finding F5 of the internal review,
   option a).
   - The derived bound assumed that after each accepting poll the port offers
     its waiting frames in order until one is declined, but the contract did
     not ask for it. A port that offers only the oldest waiting frame per
     accepting poll leaves a slot free after a frame that needs no answer or a
     BIND_RX that is only answered. A timer probe owed there delays each later
     kept command one pass: at the 189 ms budget for two kept commands, a
     GET_RX_STATE behind two foreign frames was answered at 201 ms.
   - The redelivery rule in `docs/PORTING.md` now states the obligation: after
     each `acmp_poll` that accepts an owed frame, the port offers its waiting
     ACMP frames in arrival order, the kept one first, until `acmp_rx` declines
     one or none is left, and only then services `acmp_timer_expired`. The
     bound assumes this. A further sentence says what offering fewer frames
     costs.
   - `docs/TESTS.md` says that the test port's `pass()` does exactly this: it
     advances the clock 1 ms, polls once, offers every waiting frame in arrival
     order until `acmp_rx` declines one or none is left, then services each due
     interface timer.
   - The change log, the What section and Round 4 item 1 above say the same.
2. **The answer pass from seven owed** (finding F4 of the external review,
   option a, the exact form).
   - A command is kept only with seven or eight frames owed. The egress
     returns with seven owed when the first kept frame is a BIND_RX declined
     with one slot free, and then every kept command leaves one pass sooner
     than the round 4 figure.
   - PORTING, the change log and this body now state the pass as
     n + 1 + f + r. Here n, `ACMP_OWED_MAX` or one less, is the number of frames
     owed when the egress returns, and it is one less only when the first kept
     frame is a BIND_RX declined with one slot free. The first kept command
     leaves in pass n + 1 (`ACMP_OWED_MAX` + 1 from a full set).
   - The budget is unchanged. It uses `ACMP_OWED_MAX` for n, so it holds from
     either start.
   - New test `KeptCommandsBehindSevenOwedLeaveOnePassSooner`:
     - Seven frames are owed: seven GET_RX_STATE, or five and a taken BIND_RX.
     - A BIND_RX declined with one slot free, a GET_RX_STATE and a second new
       binding are kept.
     - Two refused passes follow in the hold, and a TMR_NO_RESP retry falls
       due in the second. This runs both with and without the BIND_RX
       delivered again in those passes.
     - The egress returns with seven owed, `bind_waiting` set and the retry
       held.
     - The kept commands leave in passes 8, 10 and 11, each `ACMP_OWED_MAX` +
       f, and the held retry follows in pass 13. Nothing is lost.
   - New plant `owed-bind-wait-only-on-a-second-decline`:
     - It sets `bind_waiting` only once some command has been declined
       before, as if every waiting BIND_RX had first met the full set.
     - The retry falling due in the hold then takes the last slot. The egress
       returns with eight owed, and the BIND_RX waits an extra pass (pass 9,
       not 8).
     - The new test kills it, and without that test it passes all 124 other
       tests.
3. **The held probe's conditions** (finding F6 of the internal review, and
   suggestion S9 of the external review).
   - The count of one probe per other sink also needs the held probe's wait to
     stay under TMR_NO_RESP. Past 200 ms, a sink whose TMR_DELAY probe was owed
     before the held probe can owe its TMR_NO_RESP retry before it too. In the
     internal review's sustained probe, sink 3 left after both of sink 2's
     probes, with no restart.
   - PORTING now says "at most one per other sink while no sink's probing
     restarts (an ADP re-advertisement that does not raise the available index,
     a new discovery after its talker departs or its advertisement times out,
     or `acmp_tk_unregistered`) and the held probe has waited less than
     TMR_NO_RESP (200 ms); past that, another sink's TMR_NO_RESP retry can also
     be owed before it". The gated-port sentence uses the same "probing
     restarts".
   - S9 named two restart paths. The code has a third that lets a sink owe a
     second probe within 200 ms: its talker departs, by ENTITY_DEPARTING or by
     the end of the advertisement's valid time. When the talker is discovered
     again, a new TMR_DELAY is armed. The text names all three.
4. **Residue** (RES7 of the internal review), and two sentences found in the
   final re-check.
   - A held retry is also cancelled when the probe it repeats is answered.
     PORTING, the `probes_held` counter row and Round 4 item 3 now say so.
   - New test `AnsweredProbeEndsTheHoldOfItsRetry`: the answer waits behind
     the kept BIND_RX, and once taken it ends the hold. A failure status leaves
     the sink in PRB_W_RETRY with TMR_RETRY, and SUCCESS leaves it in
     SETTLED_NO_RSV with TMR_NO_TK. The retry is never sent, held again or lost.
     Its plant, `owed-answer-keeps-the-hold`, keeps `probe_held` across the
     answer; it passes every other test.
   - "its sink's probing does not advance until the probe is owed" now ends
     "or cancelled".
   - ACMP-12's prose and the change log said that timer probes are held while
     a BIND_RX waits. A BIND_RX declined with no slot free also waits, and a
     probe that falls due then is lost; `BindDeclinedBehindTheFullSetHoldsNoProbe`
     pins that. Both now say "while it waits with one slot free", as the
     requirement row already did.
   - `scripts/check_port_contracts.py` pins 13 new phrases and re-pins the
     changed pass phrase. Its self-test refuses 74 meaning-removal controls, up
     from 61.
5. **Not taken:** the optional RV32 smoke step (S7 of the internal review, S8 of
   the external review) and the test of a port that offers one frame per poll
   (S8 of the internal review, useful only under option b).

### Every stated behaviour, again

Every sentence of the owed-bound section and of ACMP-12 was checked against
the code again, including the port behaviours the contract allows: waiting or
delivering again after a refused poll, and testing `acmp_rx_ready` instead.
That re-check found the departure path in item 3 and the two sentences in
item 4. The sentence map now has 66 sentences and clauses, 50 of
which state core behaviour. Each of those has a named assertion and a
registered plant that it kills and the campaign catches. The map's checker
passes against this tree, the final campaign and the escape evidence.

### Both reviews' probes at this head

The four round 4 probes ran unchanged on a clean clone of this head:
`probe_r4.cpp` with `probe_r4b.cpp`, and `probe_r4c.cpp`, from the internal
review, and `probe_owed6.inc` from the external review. Every line they print
is identical to the reviews' own receipts, because the core is unchanged.
Each falls within the corrected sentences:

| Probe | Output | Sentence it meets |
|---|---|---|
| `probe_r4` and `probe_r4b`, port "all" | Every answer in the pass the formula gives (9 and 10); at the 189 ms budget for two commands, 198 and 199 ms; at 190 ms, the last answer at 200 ms | n + 1 + f + r with n = 8, and the budget |
| `probe_r4` and `probe_r4b`, port "one" | One pass late behind an only-answered BIND_RX or two foreign frames (201 ms at 189 ms) | The port offers one frame per poll, which the redelivery rule now excludes. The sentence on offering fewer frames gives the cost. |
| `probe_r4`, GET then a foreign frame | The retry finds the set full with nothing held, and is lost (`probes_lost` 1) | "With no probe held and no BIND_RX waiting … counted in `probes_lost`" |
| `probe_r4c`, sustained | Sink 2's TMR_DELAY probe leaves in pass 11 and its TMR_NO_RESP retry in pass 250, both before sink 3's held retry (pass 251) | Past 200 ms, another sink's TMR_NO_RESP retry can also be owed before the held probe |
| `probe_r4c`, failure response | `probe_held` goes from 1 to 0; PRB_W_RETRY, probing ACTIVE, TMR_RETRY | Cancelled when a held retry's earlier probe is answered; its probing advances once the probe is cancelled |
| `probe_owed6`, eight owed (control) | 9, 11 and 12 | n = 8 |
| `probe_owed6`, seven owed, both ways | 8, 10 and 11, `probes_lost` 0. The probe still prints its own "stated" column from the round 4 figure | n = 7: n + 1 + f with f = 0, 2 and 3 |

### Gates at this head

On a clean clone of this head, `python3 scripts/validate.py --work <w> --jobs 16 --graphs`
returns 0 for all 28 gates. That includes the full mutation campaign
(443 caught, 0 escaped, 0 errors), privacy, coverage (`src/acmp.c` 813/813 lines and 424/424
branches, unchanged), both sanitizer arms, static analysis and graphs.
`python3 scripts/baremetal.py --work <w> --jobs 8` returns 0 in Debug and
Release. Each of the four commits passed the same gates on its own tree
before it was committed.

The core is unchanged, so memory and instruction counts are as in the Round 3
tables. The Release RV32 image is byte-identical to round 4's: 50504 bytes,
`.text` 38668, `acmp.c` object text 19365. The Debug image is 150332 bytes for
both heads, built from exported trees at paths of equal length.

Issue #26 stays open: the parent firmware's harness row still needs the parent
to adopt this head (see the integration note). Round 5 changes no source, so
no parent fragment moves.
