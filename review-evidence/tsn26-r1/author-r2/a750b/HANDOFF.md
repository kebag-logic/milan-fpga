# [A750b] HANDOFF: tsn-c-stack issue #26 (ACMP owed bound), round 2

Status: REVIEW READY at 9002bfec5b135da4c0e11892464f509f725feb1f. Every gate returns 0 on both targets.

- Repository: kebag-logic/tsn-c-stack, PR #28, branch `26-acmp-owed`.
- Round 1 head: 3d57262c3614740244de40c40f667908ce6310f7 (pushed). Round 2 adds three commits on top, with no
  rebase, force or amend. Each commit is authored and committed by hackerman-kl <hackerman-kl@kebag-logic.com> and has a one-line subject with no body.
  1. `0e3ae73` Test that a declined BIND_RX and GET_TX_STATE are answered after the hold (F1)
  2. `5bce685` Decline a BIND_RX until two owed slots are free so a deferred binding loses no probe (S1)
  3. `9002bfe` Deliver a kept ACMP command right after the accepting poll, before timer service (R793 S2)
- Not pushed; no PR opened or edited. PR text: `PR-BODY.md` (first line "[A750b]", "Relates to #26").
- Issue #26: "[A750b] TAKEN" posted at start; "[A750b] REVIEW READY 9002bfec5b135da4c0e11892464f509f725feb1f" posted at the end.
- Every core change is inside ACMP (`src/acmp.c`). `include/acmp.h` is unchanged in round 2.

## Findings addressed

| Finding | Disposition |
|---|---|
| F1 MINOR (R793-1 and R794-1, same finding) | Fixed in tests (outcome (a) of both reports). Two new `AcmpOwed` tests check that a declined BIND_RX and a declined GET_TX_STATE are answered after the hold, with their Table 5.32 and 5.47 fields, in order and within 200 ms. The PR body's test sentence now says exactly what each test asserts. |
| S1 (both reviews) | Taken as a design change: a BIND_RX is declined until two owed slots are free, and `acmp_rx_ready` needs two free slots. The rule is stated in PORTING "ACMP owed bound" with Milan v1.2 5.5.3.5 (5.5.3.5.3). A test shows `probes_lost` stays 0 and the probe leaves at once. Two plants that restore the one-slot rule are caught. |
| R793 S2 | PORTING says to deliver the kept frame right after the accepting `acmp_poll`, before timer service. The test port model polls, delivers kept frames, then services due timers. |
| R794 S2 | The PR body's integration note names the parent's `sw/firmware/ctrl/test/acmp_mutants.py:452-453` fragment and gives its new text. Read-only, via the API, at parent dev `0a75aa774b89`. |
| R794 S3 | Same as R793 S2. |

## Design: the two-slot rule (S1)

- `acmp_rx` declines a BIND_RX for this listener while `owed_count + 2 > ACMP_OWED_MAX`, so at 7 or 8 owed. Every
  other command is still declined only at 8. A BIND_RX that starts a binding sends its response and its first
  PROBE_TX in the same call (Milan v1.2 5.5.3.5.3). With two free slots both are owed, so the probe is never LOST.
- The rule reads only the message type. Deciding whether the BIND_RX would probe needs the lock query, which is a
  port call, and a declined command must make no port call. A BIND_RX that is only answered therefore also waits for
  two slots: unknown sink, refused controller, or repeated binding. That costs it at most one more accepted frame.
- `acmp_rx_ready` is now `!in_port && owed_count + 2 <= ACMP_OWED_MAX`. A `true` still guarantees that `acmp_rx`
  takes any frame, so a port that relies on the hook alone never offers a BIND_RX that would be declined. At 7 owed,
  other commands wait one more accepted frame in such a port. Their answer still leaves in the same pass, because
  the queue drains in order either way.
- Timing is unchanged for every deferred answer: pass `ACMP_OWED_MAX` + 1 after the egress returns, 69 ms for a
  60 ms hold. A deferred BIND_RX's probe follows in the next pass, at 70 ms.
- Redelivery before timer service (R793 S2) gives the kept command the freed slot. A timer probe that then finds every
  slot owed is counted in `probes_lost`, and its timeout recovers it. This is the existing ACMP-09 behaviour,
  stated in PORTING:84.

## Changes (file:line at head 9002bfe)

- `src/acmp.c:71`: `#define OWED_BY_BIND 2u` (Milan v1.2 5.5.3.5.3).
- `src/acmp.c:328-336`: `room(a, frames)` succeeds while `owed_count + frames <= ACMP_OWED_MAX`.
- `src/acmp.c:1040`: `acmp_rx_ready` needs `OWED_BY_BIND` free slots.
- `src/acmp.c:1062`: talker commands need one slot: `room(a, 1u)`.
- `src/acmp.c:1074`: listener commands need `OWED_BY_BIND` slots for a BIND_RX and one for any other command.
- `examples/rv32/smoke.c:276-311` (`acmp_owed_smoke`), with codes 91-101:
  - 91: ready exactly while two slots are free.
  - 92-93: the ninth command is declined with no port call.
  - 94: it is taken after one accepted frame.
  - 97: a BIND_RX is declined at 7 owed.
  - 98: it is taken at 6.
  - 99: `busy_declined` 2, 8 owed, `probes_lost` 0.
  - 95-96: the ninth answer (seq 8, SUCCESS) leaves after the eight ahead.
  - 100: the BIND_RX answer (seq 9) leaves next.
  - 101: the PROBE_TX leaves last, with `probes_lost` 0.
- `tests/test_acmp.cpp` (AcmpOwed fixture):
  - Port model `pass()` at `:2580-2592`: poll, redeliver kept frames, then service due timers (`:2587-2591`).
  - `drain()` at `:2593`, `position()` at `:2603`.
- `tests/test_acmp.cpp`, tests:
  - `:2729` `ReadyPredicateMatchesTheOwedBound`: rewritten for the two-slot bound.
  - `:2787` `DeclinedBindIsAnsweredAfterTheHold`: new.
  - `:2822` `DeclinedGetTxStateIsAnsweredAfterTheHold`: new.
  - `:2860` `DeferredBindWaitsForTwoSlotsAndLosesNoProbe`: new.
- `tests/mutations.json`: 415 plants (411 core and 4 generated configuration).
  - Five new: `owed-ready-one-slot`, `owed-bind-one-slot`, `owed-bind-owes-one`,
    `owed-bind-answer-lost-after-decline`, `owed-get-tx-state-answer-lost-after-decline`.
  - Updated for the new `room()` and `acmp_rx_ready` text: `acmp-full-queue-acts` and every `owed-*` plant that
    matches those lines.
  - `owed-ready-off-by-one` has a new killer needle.
  - `owed-bind-rx-drop-restored` and `owed-get-tx-state-drop-restored` gained the new tests as killers.
- `docs/PORTING.md`, owed-bound section:
  - `:78-80`: the BIND_RX two-slot rule with its clause.
  - `:81`: the decline.
  - `:82-84`: redelivery before timer service, and its consequence.
  - `:88`: the ready predicate needs two free slots.
  - `:90`: the cost of a declined command.
  - `:94`: the deferred probe leaves in the next pass.
- `docs/PORTING.md:325`: the `busy_declined` counter row.
- `docs/REQUIREMENTS.md:43` and `:51`, and `docs/requirements.json` (ACMP-12 text): the two-slot rule.
- `scripts/check_port_contracts.py:281-284`: four new critical phrases.
  - `acmp_rx`: 'before it services `acmp_timer_expired`', 'A BIND_RX needs two free owed slots' and 'a deferred binding loses no probe'.
  - `acmp_rx_ready`: 'needs two free owed slots'.
- `docs/VERIFICATION.md:24`: 411 core plants. `:138`: the RV32 smoke row covers the BIND_RX slot rule.
- `CHANGELOG.md:5`: the two-slot rule, the ready predicate and redelivery before timers.
- Generated: `docs/TESTS.md`, `docs/TRACEABILITY.md`.
  - ACMP-12: 11 tests.
  - ACMP-03 gains `DeclinedBindIsAnsweredAfterTheHold`; ACMP-08 gains `DeclinedGetTxStateIsAnsweredAfterTheHold`;
    ACMP-09 gains `DeferredBindWaitsForTwoSlotsAndLosesNoProbe`.
  - Counts: 158 test declarations, 46 requirements.
- `tests/coverage.ratchet:5`: `src/acmp.c` lines 795/795, branches 400/400 → 402/402. The two new branches are the BIND_RX slot
  choice. No new exclusion.

## Tests and the planted mutants they kill

The full ACMP suite has 109 tests. "Killers" is the full-suite failure set of each plant's mutant binary from the
final campaign. "Escape" means rc 0 with no failures once those killers are excluded (`--gtest_filter=-...`).
Every one of the 28 `owed-*`/`acmp-full-queue-acts` rows escapes without its killers (`escape-evidence.json`).

| Test | Proves | Plants that fail it (registered needle) | Escape without the test |
|---|---|---|---|
| `AcmpOwed.DeclinedBindIsAnsweredAfterTheHold` (`:2787`) | See below the table. | **owed-bind-rx-drop-restored** (serves the BIND_RX while full; the decline assertion fails), **owed-bind-answer-lost-after-decline** (loses the redelivered answer). Also fails under owed-listener-drop-restored, owed-get-rx-state-drop-restored, owed-room-off-by-one, owed-decline-uncounted, owed-served-reported-declined, owed-listener-acts-then-declines, acmp-full-queue-acts. | `owed-bind-answer-lost-after-decline` is killed only by this test and the S1 test, both new. Without them it escapes, so the round 1 suite missed it. |
| `AcmpOwed.DeclinedGetTxStateIsAnsweredAfterTheHold` (`:2822`) | See below the table. | **owed-get-tx-state-drop-restored** (serves while full), **owed-get-tx-state-answer-lost-after-decline** (loses the redelivered answer; sole killer). Also fails under owed-talker-drop-restored, owed-talker-acts-then-declines, owed-get-tx-connection-drop-restored, owed-room-off-by-one, owed-decline-uncounted, owed-served-reported-declined, acmp-full-queue-acts. | `owed-get-tx-state-answer-lost-after-decline` escapes (rc 0, 108 tests pass). |
| `AcmpOwed.DeferredBindWaitsForTwoSlotsAndLosesNoProbe` (`:2860`) | BIND_RX declined at 8 owed, declined again at 7 (`busy_declined` 2), taken at 6 with answer and probe both owed. After the drain `probes_lost` is 0. The answer leaves at 69 ms ≤ 200 ms, and the PROBE_TX leaves at once, in the next pass at 70 ms. The sink is in PRB_W_RESP with its retry unused, and NO_RESP runs from the probe's send time. | **owed-bind-one-slot** (the BIND_RX needs one slot again; needles "declined again" and "loses no probe"), **owed-bind-owes-one** (`OWED_BY_BIND` 1), owed-bind-answer-lost-after-decline. Also fails under owed-bind-rx-drop-restored, owed-listener-drop-restored, owed-listener-acts-then-declines, owed-room-off-by-one, owed-decline-uncounted, owed-served-reported-declined, acmp-full-queue-acts. | `owed-bind-one-slot` and `owed-bind-owes-one` are each killed only by this test and the rewritten ready test. Without both they escape. |
| `AcmpOwed.ReadyPredicateMatchesTheOwedBound` (`:2729`, rewritten) | Boundary: 6 owed is ready, and 7 owed is not ready. At 7 owed a BIND_RX is declined and changes nothing, while a GET_RX_STATE is taken (last slot). 8 owed is not ready. After one accepted frame it is still not ready; after two it is ready. Inside a port callback it is not ready, and re-entry is declined and counted as re-entry. | **owed-ready-one-slot** (round 1 predicate; sole killer), **owed-ready-off-by-one** (sole), **owed-ready-ignores-full** (sole), **owed-ready-ignores-reentry** (sole), **owed-reentry-taken** (sole), owed-bind-one-slot, owed-bind-owes-one, owed-room-off-by-one, owed-served-reported-declined. | Each sole-killer plant escapes. |

What the two F1 tests prove:

- `DeclinedBindIsAnsweredAfterTheHold`:
  - Before the hold: the BIND_RX is declined, makes no port call, is counted once and binds nothing. A
    GET_RX_STATE waits behind it in the port.
  - After the 60 ms hold, the BIND_RX is answered with its Table 5.32 fields: SUCCESS, controller, talker and
    talker UID, listener UID 1, count 1, the STREAMING_WAIT flag echoed, no stream ID, MAC or VLAN.
  - The answer leaves 69 ms after arrival (≤ 200 ms), at position 8, right after the eight owed frames, which leave
    in order.
  - The GET_RX_STATE behind it leaves later, at 71 ms, and reports count 1. The binding takes effect only when the
    BIND_RX is taken.
- `DeclinedGetTxStateIsAnsweredAfterTheHold`:
  - Before the hold: the GET_TX_STATE is declined, reads no source state and is counted. A GET_TX_CONNECTION waits
    behind it.
  - The source state changes during the hold.
  - The answer carries the Table 5.47 fields: SUCCESS, listener and listener UID cleared, REGISTERING_FAILED, and
    the stream ID, destination MAC and VLAN from the source state at the time it is taken.
  - It leaves at 69 ms (≤ 200 ms), at position 8. The GET_TX_CONNECTION answer leaves next, at position 9 and 70 ms.

Round 1 tests are unchanged except the ready test, and the fixture's `pass()` now services timers after
redelivery. With it, the existing tests give the same results as before (all 109 pass). Changes in
full-suite killers since round 1:

- `owed-get-rx-state-drop-restored` also fails `DeclinedBindIsAnsweredAfterTheHold`, through the GET_RX_STATE held
  behind the BIND_RX.
- `owed-get-tx-connection-drop-restored` also fails `DeclinedGetTxStateIsAnsweredAfterTheHold`.
- `owed-bind-rx-drop-restored` now fails four tests: A19, the two new BIND_RX tests and the ready test.

Mutation campaign at the final head: 415/415 CAUGHT, 0 ESCAPED, 0 ERROR. Round 1: 410/410.

## Boundary evidence

- Two-slot bound, hosted (`ReadyPredicateMatchesTheOwedBound`, `DeferredBindWaitsForTwoSlotsAndLosesNoProbe`):
  - 6 owed: ready, and a BIND_RX is taken.
  - 7 owed: not ready; a BIND_RX is declined; a GET_RX_STATE is taken.
  - 8 owed: everything addressed to this entity is declined.
- Two-slot bound, RV32 (`acmp_owed_smoke` codes 91, 97, 98 and 99, Debug and Release): the same boundary on the
  bare-metal target.
- No probe lost: `probes_lost` stays 0 on both targets. The probe leaves in the pass after the BIND_RX answer.
  Round 1 lost it, with `probes_lost` 1 (reviewer probes R793-1 and R794-1) and a 200 ms TMR_NO_RESP wait.
- Timing (disposable probe in an exported copy of the head, printing the test's own values):

  | Answer | Time after arrival |
  |---|---|
  | Deferred BIND_RX | 69 ms |
  | GET_RX_STATE behind the BIND_RX | 71 ms |
  | Deferred GET_TX_STATE | 69 ms |
  | GET_TX_CONNECTION behind it | 70 ms |
  | BIND_RX answer in the S1 test | 69 ms |
  | Its first PROBE_TX | 70 ms |

  All are ≤ 200 ms (Milan v1.2 Table 5.26).
- Coverage: `src/acmp.c` 795/795 lines and 402/402 branches (100%).

## Gate table (Linux hosted and bare-metal RV32)

Toolchain:

- GoogleTest/GMock 1.14.0, from the pinned prefix.
- Host GCC 16.2.1 and host Clang for the hosted builds.
- Pinned Clang 18.1.3 (`$VALIDATION_TOOLS/clang-18/bin`, working again) as the lexer.
- CI's clang-tidy 18.1.3 (`$VALIDATION_TOOLS/clang-tidy-18/bin`).
- Mermaid CLI 11.16.0, the CI pin. It was installed in scratch with Node 22.11.0 (checksum verified).
- `validate.py --jobs 8 --graphs` and `baremetal.py --jobs 8` ran concurrently, once per step.

| Gate | 0e3ae73 (F1) | 5bce685 (S1) | 9002bfe tree (S2) | Final 9002bfe | Scope |
|---|---|---|---|---|---|
| entity-golden, entity-controls | 0, 0 | 0, 0 | 0, 0 | 0, 0 | Shared |
| boundary, dependencies | 0, 0 | 0, 0 | 0, 0 | 0, 0 | Hosted |
| needles, assertion-templates | 0, 0 | 0, 0 | 0, 0 | 0, 0 | Assertion contract |
| comments | 0 | 0 | 0 | 0 | Comment contract (includes the RV32 cross-compiled controls) |
| conditionals | 0 | 0 | 0 | 0 | Conditional matrix |
| port-contracts | 0 | 0 | 0 | 0 | PORTING names and meanings |
| acmp-cache, registration-controls, license | 0 | 0 | 0 | 0 | |
| traceability, test-inventory | 0, 0 | 0, 0 | 0, 0 | 0, 0 | 157 → 158 declarations; 412 → 415 plants |
| coverage-controls, privacy-selftest | 0, 0 | 0, 0 | 0, 0 | 0, 0 | |
| privacy | 0 | 0 | 0 | 0 | Final: 18 commits, 295 blobs, 98 files |
| gcc configure / build / test | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | Hosted |
| coverage | 0 | 0 | 0 | 0 | acmp.c 100% lines and branches |
| clang-sanitizers configure / build / test | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | ASan, UBSan, leaks |
| static-analysis | 0 | 0 | 0 | 0 | clang-tidy 18.1.3 and cppcheck |
| mutation | 0 (412) | 0 (415) | 0 (415) | 0 (415 CAUGHT) | Hosted campaign |
| mutation-controls | 0 | 0 | 0 | 0 | |
| graphs | 0 | 0 | 0 | 0 | 4 rendered |
| `baremetal.py` Debug | rc 0 | rc 0 | rc 0 | rc 0 | RV32I ILP32 freestanding link and QEMU smoke, including `acmp_owed_smoke` |
| `baremetal.py` Release | rc 0 | rc 0 | rc 0 | rc 0 | Same, -O3 |

Each step's gates ran on the exact working tree that was then committed; `git status` was compared before each commit.
The final column is a full rerun on the committed head. Its working tree was clean, so the privacy gate also covers
the three new commit messages. Receipts:

- Per step: `gates-f1.json`, `gates-s1b.json` and `gates-s2.json`, with `rv32-*-results.json`.
- Final: `final-gates.json` and `final-rv32-results.json`.

One run failed and was not committed. The first S1 run had mutation rc 1: `acmp-full-queue-acts` did not compile,
because `if (true)` leaves the new `frames` parameter unused under `-Werror`. The plant now reads
`if (a->owed_count + frames <= ACMP_OWED_MAX || true)`. The rerun (`s1b`) passed every gate, and only that state
was committed.

Commands (from the lane):

```sh
python3 scripts/validate.py --work build-validation --jobs 8 --graphs
python3 scripts/baremetal.py --work build-rv32 --jobs 8
```

## Bare-metal image size, memory and cost

### Image (`scripts/baremetal.py`, `rv32_smoke.elf`)

main 70936b7, round 1 3d57262 and round 2 9002bfe were each exported and built at paths of equal length, so the
Debug ELF sizes compare fairly.

| Build | ELF bytes | `.text` | `.rodata` | `.bss` | `acmp.c` object text |
|---|---|---|---|---|---|
| Release: main → round 1 → round 2 | 46552 → 47512 → 48152 | 34856 → 35752 → 36392 | 1961 | 8 | 18053 → 18213 → 18537 |
| Debug: main → round 1 → round 2 | 141724 → 144312 → 145380 | 45460 → 46928 → 47608 | 2048 | 8 | 20729 → 20869 → 20917 |

- Release, round 1 → round 2: +640 `.text`. Of that, 324 bytes are the `acmp.c` object (-O3 inlining changes) and the rest is the longer
  smoke check.
- Split-firmware flags (`-march=rv32im -Os`), `acmp.c` object text: 10697 → 10689 → 10685.
- ELF sha256:
  - Release: main `0d8f3876…55f0` and round 1 `a9fad2c0…f356`, both byte-identical to round 1's receipts.
  - Release, round 2: `a908542f5ae6c8a043f09f6884e37f7ba4709a62b2b67e02170ba29507be3f41`, identical from the
    lane build and the export build.
  - Debug, round 2 lane build: `cf87e129d622ae85192bc08c7a1deb03f4b9c89d8494883ea092d78c21ee4ef1`, 145264 bytes.
    Its debug information records the lane path; the export build is 145380 bytes.

### Memory

Measured by compiling `sizeof` into both targets (`measure/sizes.c` and `measure/sizes-run.sh`):

- The owed set is 8 × 80 = 640 bytes, plus `owed_head` and `owed_count`, on both targets.
- `sizeof(struct acmp)` is 5064 bytes on RV32 and 5072 bytes on x86-64.
- These are the same at main, round 1 and round 2. Round 2 adds no state.

### Record path cost

The cost is RV32 instructions retired per call. QEMU `virt` runs with `-icount shift=0`, and a CSR read pair costs 1.

- Configuration: 16 sinks, 16 sources and 1 interface, with stub ports.
- Harness: `measure/measure.c`, `measure/build.sh` and `measure/measure-run.sh`. It is round 1's harness with one
  label renamed, `bind_rx_owed_behind_7_probe_lost` → `bind_rx_behind_7`, because that step is now a decline.
- The main and round 1 outputs are identical to round 1's receipts, apart from that label.

| Step | rv32i -O3: main | round 1 | round 2 | rv32im -Os: main | round 1 | round 2 |
|---|---:|---:|---:|---:|---:|---:|
| **Worst `acmp_rx` step**: BIND_RX behind 6 owed (response and probe owed) | 7882 | 7899 | **7904** | 24374 | 24381 | **24383** |
| BIND_RX sent directly | 7397 | 7414 | 7419 | 23789 | 23796 | 23798 |
| BIND_RX behind 7 owed | 7626 (probe lost) | 7643 (probe lost) | **200 (declined)** | 23760 | 23767 | **348** |
| GET_RX_STATE sent directly | 6250 | 6269 | 6274 | 19758 | 19763 | 19766 |
| GET_RX_STATE behind 7 owed | 6621 | 6640 | 6645 | 20384 | 20389 | 20392 |
| A command behind the full owed set | 5408 (dropped) | 197 | 200 | 16522 | 344 | 348 |
| PROBE_TX behind the full owed set | 5404 | 195 | 196 | 16518 | 340 | 341 |
| PROBE_TX sent directly | 6445 | 6464 | 6469 | 20255 | 20262 | 20262 |
| `acmp_poll`, one owed frame | 5436 | 5436 | 5436 | 16454 | 16454 | 16454 |
| `acmp_rx_ready` | n/a | 9 | 10 | n/a | 9 | 10 |

The figures are instruction counts, not cycles. Raw outputs: `measure/*-result.txt`.

Measurement ELF sha256:

| Build | main | round 1 | round 2 |
|---|---|---|---|
| rv32i -O3 | 73a6dcb7fc4e5a6188cacd74b4fd7c0a10e5c2e77cfdca5944be2c72389184db | df30b853f9edd92305ee98ffc554c338153fa515c7a90e391c9fad86db30de12 | e2ff8cc874cd87c77855351fd0d1e217d4e11826456c094898ba7dd59cafa70a |
| rv32im -Os | cfddc6133d8f645b3bed11f40192e535fafb814f1e3696b3d571ed546b81ed4d | 6b674a23c70199fcf4bc672957fcb98313f32f6b5b7c06752eb0447fe6829815 | d8a12bf98c20c26f7fc7ab0579e852196fae2467322ae73e989c0a600a03993f |

## Acceptance items (issue #26)

| Item | Status | Evidence |
|---|---|---|
| Past the bound the entity still answers every command (queued or refused, never silently dropped); bound and behaviour stated in the docs | Met in the core, given a port that follows the contract | `docs/PORTING.md:74-97`, ACMP-12. A port that ignores the return value still loses the command. |
| A test fills the owed set with the egress held, sends a further command, and it is answered within its timeout after the egress returns | Met, now for all seven command types | GET_RX_STATE (Held), PROBE_TX, DISCONNECT_TX and GET_TX_CONNECTION (Talker), UNBIND_RX (DeclinedUnbind), BIND_RX (DeclinedBind and DeferredBind), GET_TX_STATE (DeclinedGetTxState). All answers come at 69-71 ms, ≤ 200 ms. RV32 smoke covers GET_RX_STATE and BIND_RX. |
| A planted mutant restoring the silent drop is caught | Met | Seven per-command `owed-*-drop-restored` plants and two generic ones are caught. Two new answer-lost plants are also caught. Each escapes without its killers. |
| milan-fpga's harness row "an ACMP command behind the owed input" gets an answer time | **Not met here** | The parent must bind `ctrl_loop_set_rx_ready(l, MBX_CH_ACMP, ...)` to `acmp_rx_ready` (or keep declined frames), update `acmp_mutants.py:452-453` (new text in PR-BODY) and measure the harness again. That is out of scope for this repository and lane. |

Hence the PR says "Relates to #26".

## Environment notes

- The pinned `clang-18` wrapper works again, and the pinned `clang-tidy-18` matches CI. No scratch wrappers were
  needed this round.
- Mermaid CLI 11.16.0 was installed in scratch (`$VALIDATION_STORAGE/tsn26-a750b/mmdc`), with Puppeteer's browser cache also in scratch.
- Scratch: `$VALIDATION_STORAGE/tsn26-a750b/`. The output directory holds only text receipts (172 KB in total, no file
  over 200 KB).
- Memory: MemoryCurrent was 4.4 GB when sampled during a gate run. The unit's MemoryPeak, including page cache, reached 10.7 GB at some point in
  the session. The 12 GB cap was never hit, and no OOM event occurred. The likely cause is the cost
  measurement and the RV32 export builds running alongside the S1 gates.
- A `setsid nohup … &` launch returns the PID of `setsid`, which exits at once. Wait on the runner's own PID
  (`pgrep -f run_gates.sh`) or on its done file.
