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
       pass, after the commands the port still keeps or offers before its timer
       service (round 6).
     - With no probe held and no BIND_RX waiting, a probe that finds every slot
       owed is still lost and counted in `probes_lost`, as before.
   - Result: a deferred BIND_RX at the head of the kept frames is answered in
     pass n + 1 (`ACMP_OWED_MAX` + 1 from a full set), whatever probes fall
     due; a command kept behind it follows one pass per frame owed ahead of
     it. No timer probe is owed ahead of a kept command. Round 4 derives the
     whole bound.
   - The held probe's own delay, stated in `docs/PORTING.md` "ACMP owed bound"
     (Milan v1.2 5.5.3.5): a held probe is never dropped for want of a slot. It
     takes a freed slot only at timer service with no BIND_RX waiting, after
     every command the core takes first, whether kept or offered for the first
     time, so no command answer waits for it. Its wait has no upper limit while
     commands keep taking the freed slots (round 6 removed the earlier limit).
     Its own TMR_NO_RESP runs from when it leaves, so its response window is
     unchanged.
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

