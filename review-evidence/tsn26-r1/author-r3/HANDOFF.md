# [A750d] HANDOFF: tsn-c-stack issue #26 (ACMP owed bound), round 3

Status: REVIEW READY at b7a59887f5f2ff729206b87a268972c637882dc0. Every gate returns 0 on both targets, on a clean
clone of that head.

- Repository: kebag-logic/tsn-c-stack, PR #28, branch `26-acmp-owed`.
- Start head: 968a164929698b9a2c4eb96ec207979ff7fea856 (round 2 plus two syncs with main, pushed).
- Round 3 adds three commits. There was no rebase, force or amend. Each is authored and committed by hackerman-kl
  <hackerman-kl@kebag-logic.com> and has a one-line subject with no body or trailers.
  1. `8a1cb08` Hold a timer probe while a declined BIND_RX waits for its second owed slot, so the BIND_RX keeps its
     pass count and no held probe is lost (F2 of both reviews, the manager's ruling; also R794-2 S4)
  2. `d355236` Assert the deferred GET_TX_STATE count, test a held probe behind commands kept after the BIND_RX, and
     name the BIND_RX slot rule in the architecture table (R793-2 S3, RES3)
  3. `b7a5988` Say that the hold covers a timer probe of any sink, which would take the last free owed slot or find
     none (wording)
- Not pushed; no PR opened or edited. PR text: `PR-BODY.md` (first line "[A750d]", "Relates to #26").
- Issue #26: "[A750d] TAKEN" posted at the start; "[A750d] REVIEW READY b7a59887f5f2ff729206b87a268972c637882dc0"
  posted at the end.
- Every core change is inside ACMP (`src/acmp.c`, `include/acmp.h`). No other module changed.

## Findings addressed

| Finding | Disposition |
|---|---|
| F2 MINOR (R793-2 and R794-2, one defect) | Fixed by the ruled design change (R794-2 option 2). See "Design". The BIND_RX answer is in pass `ACMP_OWED_MAX` + 1 in every case. At the 191 ms margin it leaves at 200 ms; without the hold it leaves at 201 ms (one probe) and 204 ms (four). `probes_lost` is 0. The held probe's own bound is in PORTING "ACMP owed bound" with Milan v1.2 5.5.3.5. Three hosted tests, an RV32 smoke step and nine plants. |
| R793-2 S3 | `DeclinedGetTxStateIsAnsweredAfterTheHold` asserts `r.count == 0u` (`tests/test_acmp.cpp:2908`). |
| R793-2 S4 | Full receipts at the exact final head are in `receipts/`: 28 of 28 gates, the 426-plant campaign log, coverage, privacy, bare-metal Debug and Release, and clone status before and after. |
| R793-2 RES1, R794-2 R1 | PR body: a note after the sync image table explains 145180 against 145380. |
| R793-2 RES2 | PR body: "This sync merges main d7e6a2a1"; the privacy bullet ends "Main fixed this in #30; see Sync with main cc3362f8." |
| R793-2 RES3 | `docs/ARCHITECTURE.md:11`, with R793-2's exact wording. |
| R793-2 RES4 | PR body: "Run against the full ACMP test binary (113 tests at this head: 112 ACMP tests and main's Wire test)". |
| R794-2 S4 | `examples/rv32/smoke.c` `acmp_owed_smoke`, checks 102-109: the same step on RV32. |
| R794-2 S5 | PR body integration note. It names parent `acmp_mutants.py` lines 454-455: the killer test and its renamed form, the old needle and the current needles. It also covers the wider decline window for ports that ignore the return value. |
| PORTING:83 and the PR pass-count sentence | PORTING:85-89 and :97 restate the timing. In the Round 2 section of the PR body, "The pass count for every deferred answer is unchanged" now carries its condition and points to round 3. |

## Design (F2)

- `bind_waiting` (`include/acmp.h:423`) is set when `acmp_rx` declines a BIND_RX for this listener with exactly one
  slot free (`src/acmp.c:1100-1102`). The next `acmp_poll` that accepts an owed frame clears it
  (`src/acmp.c:1268`).
  - Under the contract, the port then delivers the kept BIND_RX before timer service, and the BIND_RX either is taken
    (six owed) or sets the mark again.
  - So the mark is never stale for longer than one accepting poll, even if a port drops the kept frame.
  - While it is set, seven or eight slots are owed.
- `probe_yields` (`src/acmp.c:776-792`) returns true when `bind_waiting` is set. Otherwise it returns true when every
  slot is owed and some sink's `probe_held` (`include/acmp.h:381`) is set.
- `sm_expired` (`src/acmp.c:798-804`) applies the hold before it changes any state. It covers only the two expiries that
  send a probe: TMR_DELAY (5.5.3.5.10) and TMR_NO_RESP in PRB_W_RESP (5.5.3.5.16).
  - The timer keeps its kind and its state, and is re-armed `now + 1` ms. A port that services timers once per pass
    retries it in the next pass. The `while` loop in `acmp_timer_expired` ends, because the new deadline is not due.
  - `probe_held` is set and `probes_held` (`include/acmp.h:441`) is incremented.
  - No sequence ID is drawn until the probe is owed.
- A held probe is never lost. While any probe is held, a probe that finds the set full is held too, so several probes
  falling due during the drain lose none. When the set is not full and no BIND_RX waits, the probe is owed. This
  happens one per pass, after the commands the port redelivers first.
- `sm_stop` clears `probe_held` (`src/acmp.c:355`). Every path that cancels or replaces a held probe goes through it:
  expiry, unbind, rebind to another talker, talker departure, a matching probe response, and sink reset.
  `HoldEndsWithTheLastHeldProbe` covers the departure case. `sm_timer` is never called on a held sink before
  `sm_stop`, so it needs no clear. I removed one that I had added, because no plant could kill it.
- Afterwards ACMP-09 is unchanged. With no probe held and no BIND_RX waiting, a probe that finds every slot owed is lost
  and counted, and its timeout recovers it. This is shown at the end of `HoldEndsWithTheLastHeldProbe`.
- The held probe's own bound (PORTING:88, with the Milan v1.2 5.5.3.5 and Table 5.26 links at :86):
  - It is held from the pass it falls due through the pass that takes the BIND_RX.
  - Add one pass for each frame owed by a command kept behind the BIND_RX.
  - Add one pass for each other probe owed before it, at most one per other sink. A sink whose probe is owed holds its
    TMR_NO_RESP until that probe leaves.
  - The ruling suggested "at most the passes until the BIND_RX is taken". The exact figure is one pass more: the pass
    that takes the BIND_RX leaves the set full, so the first held probe is owed in the next pass. Commands kept behind
    the BIND_RX also go first. I stated the exact bound, and the tests assert it pass by pass.
- What the hold cannot cover (disclosed in PORTING:100-101 and the PR integration note): a port that gates on
  `acmp_rx_ready` instead of offering its waiting frame gives the core no decline and therefore no mark.
  - Each timer probe owed while its frame waits delays that frame one pass, for any command type, at most one per
    sink. Such a port budgets `ACMP_OWED_MAX` + 1 + `n_sinks` passes, or offers the frame and leaves it in its queue
    when declined.
  - This behaviour comes from round 2's two-slot ready predicate. Round 3 did not create it, and the ruling did not ask
    for it to change.
  - The parent's planned integration binds its receive-ready hook to `acmp_rx_ready`, so the manager may want to rule
    on it.

## Changes (file:line at b7a5988)

- `include/acmp.h`:
  - `:381` `bool probe_held` in `struct acmp_sink`, in padding; `sizeof(struct acmp_sink)` stays 256.
  - `:423` `bool bind_waiting` in `struct acmp`, in padding.
  - `:441` `uint32_t probes_held`, with the ACMP-12 counters.
- `src/acmp.c`:
  - `:355` `sm_stop` clears `probe_held`.
  - `:776-792` `probe_yields`.
  - `:798-804` the hold in `sm_expired`.
  - `:1100-1102` `bind_waiting` set on a BIND_RX decline with one slot free.
  - `:1268` `bind_waiting` cleared by an accepting `acmp_poll`.
- `tests/test_acmp.cpp`:
  - `:2627-2687` fixture helpers: `sinks_on_one_interface`, `retries_due` and
    `bind_behind_the_owed_set_with_probes_due`, which drives passes and records the pass that owes each probe.
  - `:2908` the S3 count.
  - `:2952` `ProbesFallingDueInTheDrainWaitForTheDeferredBind`.
  - `:3010` `DeferredBindAtTheDocumentedMarginMeetsItsTimeout`.
  - `:3027` `HoldEndsWithTheLastHeldProbe`.
- `examples/rv32/smoke.c`:
  - `:184-196` port fields (clock, timer, send log).
  - `:211-255` `acmp_send` logging, `owed_clock`, `owed_timer`, `egress`, `owed_pass`.
  - `:316-380` `acmp_owed_smoke` with two sinks and checks 102-109.
- `tests/mutations.json`:
  - `:2331-2510` nine new plants.
  - `owed-listener-drop-restored`, `owed-listener-acts-then-declines` and `acmp-stop-keeps-the-hold` are re-anchored
    for the new lines, with their meaning unchanged.
  - 426 plants: 422 core, 4 generated configuration.
- `docs/PORTING.md`:
  - `:69` frames-and-buffers note.
  - `:82` the mark.
  - `:85-89` the hold, never lost, the held probe's bound, and ACMP-09 afterwards.
  - `:95` decline cost.
  - `:97` the pass count, "whatever timer probes fall due meanwhile".
  - `:100-101` the gated-port budget.
  - `:303` `probe_held` row; `:317` `bind_waiting` row; `:336` `probes_held` row.
- `docs/REQUIREMENTS.md:44` and `:52`, and `docs/requirements.json:221` (ACMP-12 text): hold each timer probe while a
  BIND_RX declined with one slot free waits, and never lose a held probe.
- `docs/ARCHITECTURE.md:11` RES3.
- `docs/VERIFICATION.md:24` 422 core plants; `:138` RV32 smoke row.
- `CHANGELOG.md:6`.
- `scripts/check_port_contracts.py`:
  - REQUIRED gains `bind_waiting` and `probes_held` (owed bound), `bind_waiting` and `probe_held` (machine storage),
    and `probes_held` (counters).
  - CRITICAL `:289-296` gains 12 phrases for `acmp_rx_ready`, `bind_waiting` and `probes_held`. The self-test now
    refuses 45 meaning-removal controls.
- Generated: `docs/TESTS.md` and `docs/TRACEABILITY.md` (46 requirements, 162 test declarations, 426 plants), and
  `tests/coverage.ratchet` (`src/acmp.c` 813/813 lines, 424/424 branches). The ratchet was written in the CI image
  (`receipts/coverage-ci.log`); the final host gate measures the same.

## Tests and the planted mutants they kill

- "Killers" are the failing tests of each plant's mutant binary in the final campaign, run on the full 113-test ACMP
  binary.
- "Escape" means rc 0 with those tests excluded.
- `receipts/escape-evidence.json` covers 38 plants: the 36 `owed-*` plants, `acmp-full-queue-acts` and
  `acmp-stop-keeps-the-hold`.
  - Every plant fails the full binary.
  - Every plant escapes once its killers are excluded.
  - The nine new plants escape once only the three round 3 tests are excluded. The round 2 suite would have missed
    each of them.
  - The 29 older plants are still killed by older tests.

| Test | Proves | Plants that fail it (registered kill in bold) | Escape without it |
|---|---|---|---|
| `ProbesFallingDueInTheDrainWaitForTheDeferredBind` (`:2952`) | See the list after this table. | **owed-timer-probe-not-held**, **owed-hold-skips-delay** (sole killer), **owed-hold-skips-retry**, **owed-held-probe-lost**, **owed-bind-wait-unset**, **owed-bind-wait-kept**, **owed-hold-uncounted**, **owed-hold-rearmed-late** (sole killer), owed-held-flag-kept; older: owed-listener-drop-restored, owed-bind-rx-drop-restored and others. | `owed-hold-skips-delay` and `owed-hold-rearmed-late` escape with this test excluded (rc 0, 112 pass). |
| `DeferredBindAtTheDocumentedMarginMeetsItsTimeout` (`:3010`) | 191 ms hold (200 − 9). With one retry, and with four retries one per pass, the BIND_RX answer leaves at exactly 200 ms (the hold removed gives 201 and 204). `probes_lost` 0, at least one probe held, every frame sent. | **owed-timer-probe-not-held**, **owed-hold-skips-retry**, **owed-bind-wait-unset**; also owed-held-probe-lost, owed-bind-wait-kept, owed-hold-uncounted. | Each of these is also killed by the drain test. |
| `HoldEndsWithTheLastHeldProbe` (`:3027`) | A retry beside the waiting BIND_RX is held (`probe_held`, `probes_held` 1, 7 owed). When its talker departs it is dropped with its probing: mark cleared, PRB_W_AVAIL, no timer. After the drain, the new binding's retry that finds every slot owed is lost and counted (`probes_lost` 1, `probes_held` still 1). | **owed-timer-probe-not-held**, **owed-hold-skips-retry**, **owed-bind-wait-unset**, **owed-bind-wait-kept** (the stale mark holds instead of losing), **owed-hold-uncounted**, **owed-held-flag-kept** (the stale mark after the departure). | `owed-held-flag-kept` is killed only by this test and the drain test (through the DELAY case's final `!probe_held`). |
| `DeclinedGetTxStateIsAnsweredAfterTheHold` (`:2883`, S3 line `:2908`) | Adds connection_count 0 to the Table 5.47 fields. | Unchanged from round 2: `owed-get-tx-state-drop-restored`, `owed-get-tx-state-answer-lost-after-decline`. | No new plant. The response builder's count is also pinned by A20. |

What the drain test proves. It has five cases:

1. One TMR_NO_RESP retry in pass 1.
2. One TMR_DELAY expiry in pass 1.
3. Four retries, one per pass.
4. Four retries, all in pass 1.
5. Two retries, with two GET_RX_STATE commands kept behind the BIND_RX.

In each case:

- The BIND_RX is declined once more and taken in pass 2 (`busy_declined` = 2 + kept).
- It is answered in pass 9 at position 8, at 69 ms, within 200 ms.
- `probes_lost` is 0.
- Its own probe leaves next, then the kept commands (count 1), then each held probe in sink order.
- Each held probe is owed in exactly pass `taken + 1 + kept + j`.
- Each held probe's TMR_NO_RESP runs from its send, and its mark is cleared.
- A held DELAY expiry sends the first probe (PRB_W_RESP); a held retry sends the duplicate (PRB_W_RESP2).
- `probes_held` equals the sum of the passes held.

RV32 (`acmp_owed_smoke` checks 102-109, Debug and Release; `receipts/rv32-plant-exit-codes.txt`, run on an export of
b7a5988):

- The unplanted tree exits 0.
- `owed-timer-probe-not-held`, `owed-hold-skips-retry`, `owed-bind-wait-unset` and `owed-hold-uncounted` exit 104.
- `owed-held-probe-lost` exits 105.
- `owed-bind-wait-kept` and `owed-hold-rearmed-late` exit 106.
- `owed-hold-skips-delay` and `owed-held-flag-kept` exit 0. The smoke drives no TMR_DELAY expiry and no talker
  departure, so these two are hosted-only.

## Boundary evidence

The test port model polls once per 1 ms pass, redelivers kept frames, then services timers. Holds are 60 ms unless
stated.

| Case | BIND_RX answer at b7a5988 | Same binary with `owed-timer-probe-not-held` |
|---|---|---|
| One TMR_NO_RESP retry in pass 1 | pass 9 (69 ms) | pass 10 |
| One TMR_DELAY expiry in pass 1 (the draw is 183 ms; the clock only moves forward) | pass 9 | pass 10 |
| Four retries, one per pass | pass 9 | pass 13 |
| Four retries in pass 1 | pass 9 | pass 10 |
| 191 ms hold, one retry | 200 ms | 201 ms |
| 191 ms hold, four retries | 200 ms | 204 ms |

- The head values are asserted exactly by the tests. The plant values are the "Which is" lines in
  `receipts/hold-removed-gtest.txt`. A disposable copy with the hold removed gave the same 201 and 204 before the plant
  was registered.
- The held probe's bound is asserted pass by pass by the drain test, including the case with two kept commands, where
  owed passes are 5 and 6 against 3 and 4 without them.
- The hold's end is shown by `HoldEndsWithTheLastHeldProbe`: lost and counted again once nothing is held.
- The two-slot and ready boundaries are unchanged from round 2: 6 owed ready, 7 not ready, BIND_RX declined at 7.
- Coverage of `src/acmp.c` is 100%: 813/813 lines and 424/424 branches. The 22 new branches are the hold, the mark and
  the held-probe scan.

## Gate table (Linux hosted and bare-metal RV32)

Toolchain:

- GoogleTest/GMock 1.14.0, from the pinned prefix.
- Host GCC 16.2.1 and host Clang for the hosted arms.
- Clang 18.1.3 lexer and clang-tidy 18.1.3, from the pinned paths, first on PATH.
- Mermaid CLI 11.16.0, the CI pin, installed in scratch with `npm ci`, with Node 22.11.0 and Puppeteer's cache in
  scratch.
- QEMU and riscv64-elf-gcc for RV32.

Each step ran `python3 scripts/validate.py --work <w> --jobs 16 --graphs` and `python3 scripts/baremetal.py --work <w>
--jobs 8` concurrently on the exact tree that was then committed, with `git status` compared before and after. The
final column ran on a fresh clone of b7a5988 whose status was empty before and after.

| Gate | 8a1cb08 tree (s1b) | d355236 tree (s2) | b7a5988 tree (s3) | Final, clean clone b7a5988 |
|---|---|---|---|---|
| entity-golden, entity-controls | 0, 0 | 0, 0 | 0, 0 | 0, 0 |
| boundary, dependencies | 0, 0 | 0, 0 | 0, 0 | 0, 0 |
| needles, assertion-templates | 0, 0 | 0, 0 | 0, 0 | 0, 0 |
| comments (incl. RV32 controls) | 0 | 0 | 0 | 0 |
| conditionals | 0 | 0 | 0 | 0 |
| port-contracts | 0 | 0 | 0 | 0 |
| acmp-cache, registration-controls, license | 0, 0, 0 | 0, 0, 0 | 0, 0, 0 | 0, 0, 0 |
| traceability, test-inventory | 0, 0 | 0, 0 | 0, 0 | 0, 0 |
| coverage-controls, privacy-selftest | 0, 0 | 0, 0 | 0, 0 | 0, 0 |
| privacy | 0 | 0 | 0 | 0 (28 commits, 337 historical blobs, 98 current files) |
| gcc configure / build / test | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| coverage | 0 | 0 | 0 | 0 (acmp.c 813/813, 424/424) |
| clang-sanitizers configure / build / test | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| static-analysis | 0 | 0 | 0 | 0 |
| mutation | 0 (426 caught) | 0 (426) | 0 (426) | 0 (426 caught, 0 escaped, 0 error) |
| mutation-controls | 0 | 0 | 0 | 0 |
| graphs | 0 | 0 | 0 | 0 |
| `baremetal.py` Debug, Release | 0, 0 | 0, 0 | 0, 0 | 0, 0 |

Runs that failed or were stopped, none of them committed:

- First step 1 run (s1): `static-analysis` rc 1, and every other gate was 0. cppcheck `redundantAssignment` flagged
  the smoke's `p.io.room = false` after an earlier `p.io.room = true`; the read happens through the callback `ctx`,
  which it cannot see. The new step now toggles the egress through `egress()`. The rerun (s1b) passed every gate, and
  only that tree was committed.
- First step 3 run: I stopped it after the source gates, to fold the REQUIREMENTS:44 "any sink" wording into the
  same commit. The rerun (s3) passed every gate.

Receipts (`receipts/`):

- `final-gates.json`, `final-validate.log`, `final-mutation.log`, `final-coverage.log`, `final-privacy.log`,
  `final-baremetal.log`, `final-rv32-results.json`, `final-head.txt` and `final-clone-status.txt`.
- `gates-{s1b,s2,s3}.json` and `rv32-{s1b,s2,s3}-results.json`.
- `escape-evidence.json`, `escape-summary.txt`, `hold-removed-gtest.txt`, `rv32-plant-exit-codes.txt`,
  `parent-fragments.txt` and `coverage-ci.log`.
- Scripts: `scripts/`.

## Bare-metal image size, memory and cost

### Image (`scripts/baremetal.py`, `rv32_smoke.elf`; `measure/sizes-and-images.txt`)

968a164 and b7a5988 were exported with `git archive` to paths of equal length (`xa` and `xb`) and built there.

| Build | 968a164 | b7a5988 |
|---|---|---|
| Release ELF bytes | 48952 | 50504 |
| Release `.text` | 37188 | 38668 |
| Release `acmp.c` object text | 18897 | 19365 |
| Debug ELF bytes | 145432 | 150332 |
| Debug `.text` | 47528 | 49812 |
| Debug `acmp.c` object text | 20901 | 21321 |

- `.rodata` (1961 Release, 2048 Debug) and `.bss` (8) are unchanged.
- Release `.text` grows by 1480 bytes: 468 are the `acmp.c` object and the rest is the longer smoke check.
- Split-firmware flags (`-march=rv32im -Os`), `acmp.c` object text: 10605 → 10789.
- The 968a164 Release ELF, `71c3bde3353ee62ee322483a884f6c3070f1191d19b425cf95770e4e5414f93a`, is byte-identical to the
  first sync's receipt.
- The b7a5988 Release ELF, `f1fd4b902e73676c67985024f7b5e8e4650cedf605efdabd000484cbf067a7c2`, is identical from the
  export and from the clean-clone gate build.
- Debug ELFs record the build path. 968a164 reads 145432 here against 145492 in the sync receipt (different path
  lengths), and the b7a5988 clean-clone Debug is 150400 bytes, sha256 `2185598c…`.

### Memory (`measure/sizes.c`, `measure/sizes-run.sh`)

| | 968a164 | b7a5988 |
|---|---|---|
| owed set (8 × 80) | 640 / 640 | 640 / 640 |
| `sizeof(struct acmp_sink)` RV32 / x86-64 | 256 / 256 | 256 / 256 |
| `sizeof(struct acmp)` RV32 / x86-64 | 5064 / 5072 | 5072 / 5080 |

The two flags sit in existing padding. The counter adds 4 bytes, plus 4 of tail padding to the 8-byte alignment.

### Record path cost (RV32 instructions retired, QEMU `virt`, `-icount shift=0`, 16 sinks, 16 sources)

The harnesses are in `measure/r2/measure.c` and `measure/r3/measure.c`.

- `measure/r2/measure.c` is the round 2 harness, byte for byte. At 968a164 it reproduces the first sync's receipts
  exactly, both the results and the ELF sha256: `start-r2h-*`.
- `measure/r3/measure.c` is the same harness with three timer rows added.
  - Its existing rows match r2 except `bind_rx_sent` and `probe_tx_sent`, which read +1. Those counts include the
    harness's own callbacks, whose code the larger file changes.
  - So the before and after columns below both use r3: `start-*` and `final-*`.
- The step 1 tree and b7a5988 give identical results.

| Step | rv32i -O3: 968a164 | b7a5988 | rv32im -Os: 968a164 | b7a5988 |
|---|---:|---:|---:|---:|
| **Worst `acmp_rx` step**: BIND_RX behind 6 owed | 8061 | **8062** | 22260 | **22261** |
| BIND_RX sent directly | 7577 | 7578 | 21676 | 21677 |
| BIND_RX behind 7 owed (declined; now sets the mark) | 200 | 205 | 348 | 355 |
| BIND_RX behind the full set | 200 | 202 | 348 | 350 |
| GET_RX_STATE behind the full set | 200 | 200 | 348 | 350 |
| PROBE_TX behind the full set | 196 | 196 | 341 | 339 |
| GET_RX_STATE sent directly | 6341 | 6341 | 18825 | 18826 |
| GET_RX_STATE behind 7 owed | 6712 | 6712 | 19451 | 19452 |
| UNBIND_RX sent directly | 6429 | 6433 | 18974 | 18974 |
| `acmp_poll`, one owed frame | 5436 | 5437 | 16454 | 16455 |
| `acmp_rx_ready` | 10 | 10 | 10 | 10 |
| Timer retry owed behind 7 (new row) | 6666 | 6679 | 19100 | 19142 |
| Timer retry beside a BIND_RX waiting at 7 (new row: owed before, held now) | 6666 | **5575** | 19100 | **16753** |
| Timer retry behind the full set, lost (new row: now scans 16 sinks) | 6408 | 6491 | 18500 | 18641 |

Measurement ELF sha256 (r3 harness):

- rv32i -O3: 968a164 `f774fb87…6214`, b7a5988 `5f6556bd…5e0c`.
- rv32im -Os: 968a164 `737f664a…f3ce`, b7a5988 `ac27df49…7ca5`.
- Full values are in `measure/*-elf.sha256`.

## Acceptance items (issue #26)

| Item | Status | Evidence |
|---|---|---|
| Past the bound the entity still answers every command (queued or refused, never silently dropped); bound and behaviour stated in the docs | Met in the core for a port that follows the contract | PORTING "ACMP owed bound", ACMP-12. Round 3 adds that timer probes no longer delay a deferred BIND_RX and none is lost. |
| A test fills the owed set with the egress held, sends a further command, and it is answered within its timeout after the egress returns | Met for all seven command types, now also with timer probes falling due | Round 2 tests plus the three round 3 tests (pass 9, 200 ms at the margin). RV32 smoke covers GET_RX_STATE and BIND_RX, now with a held retry. |
| A planted mutant restoring the silent drop is caught | Met | Unchanged, plus nine hold plants, all caught. |
| milan-fpga's harness row "an ACMP command behind the owed input" gets an answer time | **Not met here** | Needs the parent to adopt this head: bind its ready hook, update `acmp_mutants.py:452-455` and `acmp_review_mutants.py:143` (texts in PR-BODY), and measure. The gated-port budget above applies to it. |

Hence "Relates to #26".

## Environment notes

- Scratch: `$VALIDATION_STORAGE/tsn26-a750d/`. It holds the clean clone (`clone`), the exports (`xt-*`, `xa`, `xb`), the
  CI-image coverage tree (`covtree`), Node, the Mermaid CLI, Puppeteer's cache, and the plant work directories.
- The parent tables were read read-only through the GitHub API at milan-fpga dev `0a75aa774b89`, and parsed with `ast`,
  never imported (`scripts/parent_fragments.py`). Nothing was written to milan-fpga.
- Memory: MemoryCurrent stayed about 7.7-7.8 GB during gate runs. The unit's MemoryPeak, including page cache,
  reached 10.7 GB, during the first step 1 run while the RV32 plant builds and cost builds ran beside it. The 12 GB cap
  was never hit. Later runs kept other work light.
- The lane's ignored `build-registration/` predates this session and was left alone. `scripts/__pycache__` from gate
  runs was removed before each commit.
