[R794] NEGATIVE - exact head 968a164929698b9a2c4eb96ec207979ff7fea856

# R794-2: external independent delta review of kebag-logic/tsn-c-stack PR #28 (issue #26)

- **Exact head:** `968a164929698b9a2c4eb96ec207979ff7fea856`, tree `c1922c5f987572a550f9baa7deafb25708845a5e`. Source base `70936b77`.
- **Previously reviewed head:** `3d57262` (my R794-1 report, NEGATIVE on F1).
- **Delta since 3d57262:**
  - Three author commits: `0e3ae73` (F1 tests), `5bce685` (two-slot BIND_RX) and `9002bfe` (redelivery before timer service).
  - Two merges of main: `13dd785` (main `d7e6a2a1`, #29) and `968a164` (main `cc3362f8`, #30).
  - Every subject is one line with no body.
- **Verdict: NEGATIVE**, on one new open MINOR (F2: Conformance, Robustness, Tests, Docs).
  - F1 is resolved. S1, S2 and S3 of my round 1 report are taken.
  - The S1 design change creates F2. A deferred BIND_RX now gives the one free slot it cannot use to timer probes of other sinks. Each such probe goes ahead of it, so the documented pass count ACMP_OWED_MAX + 1, which the PR says is "unchanged", no longer holds for a BIND_RX.
  - A reviewer probe shows the consequence. A port sized exactly to the documented figure answers a deferred BIND_RX at 201 ms, past the 200 ms command timeout, when one other sink's retry probe falls due during the drain. The one-slot control and a GET_RX_STATE stay at 200 ms.
- **Also recorded:** one RESIDUE (PR-body figure note) and two SUGGESTIONs.

## Reconstruction (in the required order)

1. `CONTRIBUTING.md` (there is no `AGENTS.md`). The docs set: PORTING "ACMP owed bound" and the counters table, REQUIREMENTS ACMP-12, `requirements.json`, TESTS, TRACEABILITY, VERIFICATION and CHANGELOG.
2. Issue #26:
   - The body and acceptance are unchanged since round 1.
   - The comments since round 1 are only the author's TAKEN, REVIEW READY (`9002bfe`) and STOP (`13dd785`) markers. No maintainer or manager comment narrows the scope.
   - The PR still says "Relates to #26".
3. PR #28 body at this head and the review-start comment (6720855196). The only other PR comments, apart from review reports, are review-start markers. There is no manager evidence comment.
4. Authorities, as cited in the repository:
   - ACMP-12, ACMP-03, ACMP-08, ACMP-09 and PORT-01.
   - IEEE 1722.1-2021 8.2.4 and 8.2.5, Tables 8-1 and 8-3.
   - Milan v1.2 5.5.3.5 and 5.5.3.5.3 (bind and first probe), 5.5.3.5.10 and 5.5.3.5.16 (DELAY and NO_RESP expiry), and Tables 5.26, 5.32 and 5.47.
5. `git diff 70936b77..968a164` and `git diff 3d57262..968a164`, with history.
   - `13dd785..968a164` equals `d7e6a2a..cc3362f` byte for byte, apart from the CHANGELOG, where both Unreleased entries are kept.
   - `9002bfe..13dd785` has the same file set and stat as `70936b77..d7e6a2a`. Its conflicts were in VERIFICATION, TRACEABILITY and `coverage.ratchet`, which `git merge-tree` confirms.
6. Public evidence: milan-fpga `a380b1d9` (the tip of `tsn26-review-evidence`), `review-evidence/tsn26-r1`, everything except `reviews/` (`receipts/evidence-check.txt`):
   - All 90 non-review files were fetched by blob id, and each git blob hash was checked.
   - Each matches its `MANIFEST.json` `published_sha256`, with no unlisted file. 13 files under `author-r2/` are path-redacted, as declared.
   - The evidence commit is not GPG-signed (GitHub reports "unsigned"). Integrity therefore rests on the manifest hashes and the git blob ids, not on a signature.
7. Hosted checks at the exact head (`receipts/hosted-checks.txt`, `receipts/hosted-artifact-summary.txt`):
   - The push run (42473350284) and the pull_request run (42473353964) both executed `quality` and `bare-metal`, and every step concluded success.
   - The pull_request run's `quality-evidence` artifact has `gates.json` 28/28 rc 0, including `privacy` and `graphs`, mutation `{"CAUGHT": 417, "ESCAPED": 0, "ERROR": 0}`, and coverage `src/acmp.c` 795/795 lines and 402/402 branches.
   - Its `rv32-evidence` has Debug and Release rc 0.

## Round 1 items at their cause

| Item (R794-1) | Status at 968a164 | Evidence |
|---|---|---|
| F1 MINOR: deferred BIND_RX and GET_TX_STATE never shown answered | **Resolved** | `tests/test_acmp.cpp:2787` and `:2822` release the egress after 60 ms and assert the Table 5.32 and 5.47 fields, the 200 ms bound, position `ACMP_OWED_MAX` (right after the eight owed frames), owed-frame order, and the command held behind. My `--select owed-` campaign at this head gives 42/42 CAUGHT (`receipts/mutation-owed.log`). The driver needs every listed kill to fire (`scripts/mutation.py:241`). So both serve-while-full plants (`owed-bind-rx-drop-restored`, `owed-get-tx-state-drop-restored`) and both answer-lost plants (`owed-*-answer-lost-after-decline`) are caught by named assertions in the new tests. The PR test sentence is corrected: A19 "does not release the egress; the two new tests above check those answers". |
| S1 SUGGESTION: a deferred BIND_RX loses its first probe | **Taken** as a design change; the stated trade-off is sound, but the change creates **F2** | `src/acmp.c:71, 1040, 1074`. My probe (`receipts/probe2-head.txt`) gives a hold sweep of 0/60/131/191/192 ms → answers at 9/69/140/200/201 ms, the same as round 1, with `probes_lost` 0. The one-slot control loses 1 (`receipts/probe2-one-slot-control.txt`). The RV32 smoke kills `owed-bind-one-slot` (exit 97), `owed-bind-owes-one` (91) and `owed-bind-answer-lost-after-decline` (99) in Debug and Release. The unplanted head exits 0 (`receipts/rv32-plant-exit-codes.txt`). |
| S2 SUGGESTION: name the parent's `busy_drops` mutant fragment | **Taken** | The PR integration note names `sw/firmware/ctrl/test/acmp_mutants.py:452-453` and the new body. At live dev `0a75aa77` (read-only) those two lines are exactly the old `room()` fragment. A residual gap is noted in S5. |
| S3 SUGGESTION: say when to redeliver relative to timer service | **Taken**, but for a BIND_RX the ordering no longer gives the guarantee the docs draw from it (**F2**) | `docs/PORTING.md:82-83`. The port model `tests/test_acmp.cpp:2580-2592` polls, then redelivers, then services due timers. |

## Judgement of the stated trade-off

The PR states that a BIND_RX that would only be answered (unknown sink, refused controller or repeated binding) also waits for two slots, because the rule reads only the message type. The author's reason is that the lock query is a port call, and a decline must make no port call. That reasoning holds.

- **Reviewer probe** (`AnsweredOnlyBindFromSevenOwed`, `receipts/probe2-head.txt`). From 7 owed, a BIND_RX for an unknown sink is declined once (`busy_declined` 1) and then answered LISTENER_UNKNOWN_ID in pass 8, at position 7. A GET_RX_STATE for the same sink is taken at once and answered in the same pass 8, at position 7. The one-slot control matches.
- **Cost, absent timer events:** one extra decline and redelivery (200 instructions rv32i -O3, 348 rv32im -Os). The answer leaves no later, because the owed set drains in order either way.
- **`acmp_rx_ready` keeps its guarantee.** It now needs two free slots (`src/acmp.c:1040`), so a `true` still guarantees `acmp_rx` takes any frame. No path owes more than two frames for one command. `bind()` (`src/acmp.c:823-854`) owes only its response, whose change release rides on the response, and one PROBE_TX.

The stated trade-off is acceptable. The unstated one is F2.

## Lens results

### Conformance: UNCLEAN (F2)

- The answering argument is unchanged from round 1 and still holds: IEEE 1722.1-2021 8.2.4 and 8.2.5, Table 8-3 has no status for a full output queue, and the specified response is given behind the owed frames.
- The new tests pin the Milan Table 5.32 BIND_RX fields (SUCCESS, count 1, streaming-wait echoed, no stream fields) and the Table 5.47 GET_TX_STATE fields (listener fields cleared, registering-failed flag, and stream, MAC and VLAN read when the command is taken).
- The 200 ms Table 5.26 duty rests on the documented pass count, and F2 falsifies that count for a deferred BIND_RX.
- Limit: no standards PDFs were available. Clause numbers were checked against the repository's own usage.

### RTL (C core, both targets): CLEAN

This repository has no HDL. The lens was applied to the C core and both build targets.

- **Code:** `room(a, frames)` is `owed_count + frames <= ACMP_OWED_MAX` (`src/acmp.c:328-335`). Talkers pass 1 and a BIND_RX passes `OWED_BY_BIND` (2). No new state, no header change in round 2, and no change to `struct acmp`. The round 1 sizes therefore stand: 640-byte owed set, and 5072 / 5064 bytes on x86-64 / RV32.
- **Targets at the exact head:**
  - My `scripts/baremetal.py` run: Debug and Release rc 0, and both smoke logs end "ADP, ACMP and MAAP smoke checks: rc 0".
  - The Release ELF sha256 `71c3bde3…` is byte-identical to the author's sync receipt (`a750c/merge-rv32-results.json`). The Debug ELF differs only by the build path in its debug info (`receipts/reproduction.txt`).
  - The local GCC Debug suite passes 8/8 ctest targets.
  - Hosted: 28/28 gates and RV32 rc 0, as above.
- **Cost:** my rebuild of the published harness at this head, rv32i -O3 and rv32im -Os, gives result files, `acmp.o` sizes and harness ELF hashes byte-identical to the author's "after sync" receipts (`a750c/measure/mg-*`). Those figures include worst step 8061 / 22260, decline 200 / 348, BIND_RX behind 7 at 200 / 348, and `acmp_rx_ready` 10.
- **Cost movement:** the only source change between `9002bfe` and the head is main's `include/wire.h`. So the move from the round 2 column to the "after sync" column comes from main's wire change alone, as the brief states.

### Robustness: UNCLEAN (F2)

- The decline still changes no state. The new code paths are the same `room()` test with a different frame count.
- No livelock: the extra delay in F2 is bounded. A sink's NO_RESP timeout runs from when its probe leaves (`src/acmp.c:736-740`), and the replies that would restart probing are ACMP frames, which the port holds behind the kept one. By that analysis, each sink adds at most about one probe per 200 ms window.
- F2 is the unstated consequence of the two-slot rule. Every pass in which a kept BIND_RX finds 7 owed, it is declined, and the timer service that follows may fill the free slot.
- Ports that ignore the return value now also lose a BIND_RX at 7 owed, not only at 8 (S5).

### Tests: UNCLEAN (F2)

- F1 is closed (see above). The coverage ratchet moves 400 → 402 branches for the new comparison, with no new exclusion. 27 `owed-*` plants plus `acmp-full-queue-acts`. VERIFICATION's 413 core plants + 4 generated = 417, which matches `tests/mutations.json`.
- Gap: the port model services timers, but no test has a probe fall due while a kept BIND_RX waits for its second slot. The behaviour behind F2 is neither pinned nor bounded.

### Docs: UNCLEAN (F2)

- `docs/PORTING.md:92` and the PR body ("The pass count for every deferred answer is unchanged") state a figure that does not hold for a deferred BIND_RX.
- `docs/PORTING.md:82-83` implies that redelivering before timer service keeps a probe from taking the freed slot. For a BIND_RX at 7 owed, it does not.
- Everything else in the round 2 docs delta is consistent with the code and with each other, and the port-contracts gate enforces the new phrases: PORTING:78-80, 84 and 94, the counter row, ACMP-12 in REQUIREMENTS and `requirements.json`, the TESTS, TRACEABILITY and VERIFICATION rows, and CHANGELOG.
- **Comment rule:** every comment added in `3d57262..968a164` under `src`, `include`, `tests`, `examples` and `scripts` is a `REQ:` tag, a clause citation (`OWED_BY_BIND // Milan v1.2 5.5.3.5.3`) or a behaviour statement. There is no lane label, lane name, review round, reviewer ID or issue-comment ID. The `check_privacy.py` comment is main's, from #30.
- **Syncs:** both are as the PR describes:
  - VERIFICATION mutation row 413.
  - TRACEABILITY regenerated (ACMP-02 lists the Wire test).
  - `coverage.ratchet` `include/wire.h` 14/14.
  - The TESTS.md anchor is corrected; the hosted `traceability` and `test-inventory` gates pass at the head.
  - CHANGELOG keeps both Unreleased entries.

## Findings

### F2: MINOR (Conformance, Robustness, Tests, Docs). Timer probes overtake a deferred BIND_RX, so its documented pass count and 200 ms budget do not hold

- **Where:**
  - `src/acmp.c:1040, 1074` (two-slot rule) and `tests/test_acmp.cpp:2580-2592` (port model).
  - `docs/PORTING.md:82-83` and `:92-93`.
  - PR body, Round 2 item 2: "The pass count for every deferred answer is unchanged."
- **Cause:** with the set full and a BIND_RX kept, each accepting `acmp_poll` leaves 7 owed. The redelivered BIND_RX is then declined, because it needs two free slots. The timer service the contract places after redelivery runs next. If any other sink's DELAY expiry or NO_RESP retry falls due (`src/acmp.c:776-788`), its probe takes the 8th slot. Each such probe delays the BIND_RX, and every frame the port holds behind it, by one pass.
- **Evidence.** Reviewer probe `TimerProbesAgainstTheDeferredBind` on a disposable copy, using the repository's own port model and a 60 ms hold (`receipts/probe2-head.txt`):

  | Retry probes falling due, one per pass | GET_RX_STATE answer pass | BIND_RX answer pass | BIND_RX `probes_lost` |
  |---|---|---|---|
  | 0 | 9 | 9 | 0 |
  | 1 | 9 | 10 | 0 |
  | 4 | 9 | 13 | 0 |
  | 14 | 9 | 23 | 0 |

  - **One-slot control** (the registered plant `owed-bind-owes-one` applied, `receipts/probe2-one-slot-control.txt`): the BIND_RX is always answered in pass 9. Its own first probe and the colliding probe are lost instead (`probes_lost` +2).
  - **At the documented margin** (`DocumentedBudgetAtTheMargin`): a hold of 191 ms leaves exactly the documented 9 passes of 1 ms. One other sink's retry falling due in pass 1 puts the BIND_RX answer at **201 ms** (`within_200=0`). The GET_RX_STATE and the one-slot control stay at 200 ms.
  - So a port that budgets "hold + `ACMP_OWED_MAX` + 1 passes ≤ 200 ms", as PORTING:92-93 tells it to, can miss the BIND_RX command timeout of Milan v1.2 Table 5.26.
  - The author's handoff (`author-r2/a750b/HANDOFF.md:32-41`) states "at most one more accepted frame" and "Redelivery before timer service gives the kept command the freed slot". Neither holds for a BIND_RX at 7 owed.
- **Impact:**
  - The figure the port contract gives integrators for the 200 ms budget is wrong for the costliest command, and for every frame held behind it.
  - The extra delay is bounded, by my analysis at about one pass per sink with a probe falling due. It is not a livelock.
  - It is unstated, untested and contradicted by the PR body.
- **Required outcome, either of:**
  1. Keep the design, and state the bound. In PORTING "ACMP owed bound" (and ACMP-12's text where it gives timing), say that a kept BIND_RX, and every frame behind it, can wait one more pass for each probe the timer service sends while it waits for its second slot. Give the worst case in sinks, so a port budgets hold + (`ACMP_OWED_MAX` + 1 + that bound) passes. Correct PORTING:83 and the PR-body sentence to match. Add a test that has another sink's probe fall due during the drain and asserts the bound and the order.
  2. Change the design so the kept BIND_RX cannot be overtaken. For example, while a BIND_RX has been declined for want of its second slot, a timer probe that would take the last free slot is held, with its timer re-armed, instead of owed. Pin that with the same test.
- **Verification:** the new test passes at the new head, and a plant that removes the bound or the hold is caught by a named assertion. Re-run `--select owed-` and the margin scenario above (`scripts/run_probes2.sh`).

### R1: RESIDUE (Docs, PR body only). The round 2 Debug ELF size reads differently in the two image tables

- The round 2 Release image table gives Debug ELF bytes "141724 → 144312 → 145380". The "after the sync" table gives "145180 → 141796 → 145492". The round 2 column reads 145380 in one and 145180 in the other.
- Both are true measurements, from two campaigns built at different path lengths (`a750b/measure/sizes-and-images.txt` and `a750c/measure/sizes-and-images.txt`). Debug info records the path.
- **Exact fix:** after the second table, add "Debug ELF bytes in this table come from a different build path than the round 2 table above, so round 2 reads 145180 here and 145380 there; `.text` and the `acmp.c` object are equal in both."

### S4: SUGGESTION (Tests). Pin the timer interplay in the RV32 smoke as well

- Once F2 is settled, consider adding the "another sink's probe falls due during the drain" step to `acmp_owed_smoke` (`examples/rv32/smoke.c:288-311`). Both targets would then carry the bound.

### S5: SUGGESTION (Robustness; parent-integration note). Name the rest of the parent mutant entry and the wider decline window

- At parent live dev `0a75aa77`, `acmp_mutants.py:454-455` also names the killer test `AcmpCore.A19AFullQueueDropsTheCommandBeforeItActs`, which this PR renames to `…DeclinesTheCommandBeforeItActs`. It also names the needle "A19 a command whose response would find the queue full is dropped". The current needles are "is declined before it changes anything" and "is declined to the port, not taken".
- The note says "A port that ignores the return value still loses the command, as before". Such a port now also loses a BIND_RX at 7 owed, which was previously taken with its probe lost.
- Adding both points to the integration note would save the parent author a failed campaign.

## Prior public review findings at this head

### Disclosure and timing

I read the other reviewer's published reports only after the verdict, findings and ledger above were written:

- R793-1 at `3d57262`, comment 6719691645;
- R793-2 at this head, comment 6720959003, which was already published when I looked.

Nothing above was changed after reading them. My own round 1 items are resolved in "Round 1 items at their cause".

### R793-1 at 3d57262

| Prior item | Status at 968a164 | Basis |
|---|---|---|
| F1 MINOR (Tests, Docs): answered-after-redelivery claimed but not tested for BIND_RX and GET_TX_STATE | **Resolved** | New tests at `tests/test_acmp.cpp:2787` and `:2822`. Serve-while-full and answer-lost plants are caught by named assertions (my `owed-` campaign 42/42). The PR sentence is corrected. |
| S1 SUGGESTION: a redelivered BIND_RX always loses its first probe | **Resolved** (design change), with consequence **F2** | `probes_lost` 0 in my sweep. RV32 smoke kills the one-slot plants. |
| S2 SUGGESTION: say when to redeliver relative to timer service | **Resolved** in PORTING:82-83 and the port model. The guarantee drawn from it fails for a BIND_RX (**F2**). | `tests/test_acmp.cpp:2580-2592` |

### R793-2 at this head (concurrent round, read after my verdict)

| Its item | My position | Basis |
|---|---|---|
| F2 MINOR (Robustness, Docs): a due sink timer probe takes the freed slot ahead of a kept BIND_RX | **Same defect as my F2**, reached independently | My probes (`receipts/probe2-*.txt`) and the 201 ms margin case. I also attribute Conformance (the Table 5.26 budget) and Tests (no test pins the interplay). |
| RES1: round 2 Debug ELF 145380 vs 145180 | **Same as my R1** | |
| S3 SUGGESTION: the GET_TX_STATE test omits connection_count | **Concur** | `tests/test_acmp.cpp:2846-2849` checks every other Table 5.47 field but not `r.count == 0u`. |
| S4 SUGGESTION: publish a full `validate.py` and `baremetal.py` receipt at the exact head | **Concur** | The author's receipt at `968a164` covers 5 checks. Exact-head 28/28 is otherwise carried by the hosted artifact (this report) and the reviews' own runs. |
| RES2: "Round 3 merges main d7e6a2a1" and the stale privacy bullet in the PR body | **Concur, RESIDUE** | That section was written before #30, and the cc3362f8 section supersedes it. |
| RES3: `docs/ARCHITECTURE.md:11` omits the two-slot BIND_RX case | **Concur, RESIDUE** | The line reads "Eight owed frames; past them a command is declined to the port". The behaviour is stated correctly in the linked PORTING section and in ACMP-12. |
| RES4: "the full 109-test ACMP suite" in the PR body | **Concur, RESIDUE** | That was accurate for `a750b`'s escape campaign at `9002bfe`. At this head the binary lists 110 tests (109 ACMP plus main's `Wire.W1PutBeWritesTheLowBytesMostSignificantFirst`). |

The author can take the exact fixes for RES2-RES4 from R793-2. None of them changes my verdict, and I record them only so this report carries every open item.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | ACMP-12 text and row; PORTING "ACMP owed bound"; `src/acmp.c:322-335, 776-788, 814-854, 1036-1080`; new tests' Table 5.32 and 5.47 assertions; trade-off, hold-sweep, timer-interplay and margin probes | R794-2 (delta); unchanged parts from R794-1 | 968a164929698b9a2c4eb96ec207979ff7fea856 |
| RTL (C core, both targets) | CLEAN | `room()` and ready-predicate change; `bind()` owes at most 2; `baremetal.py` Debug/Release rc 0, Release ELF byte-identical to author; local ctest 8/8; cost harness byte-identical (2 builds); hosted 28/28 and RV32 rc 0 at exact head | R794-2 | 968a164929698b9a2c4eb96ec207979ff7fea856 |
| Robustness | UNCLEAN (F2) | Two-slot rule against the port model's timer order; probe sources (DELAY, NO_RESP retry); bound analysis; legacy-port decline window; parent fragment at `0a75aa77` (read-only) | R794-2 | 968a164929698b9a2c4eb96ec207979ff7fea856 |
| Tests | UNCLEAN (F2) | Three new tests and the changed ready test; `tests/mutations.json` delta (5 new, 22 updated); `--select owed-` 42/42 CAUGHT; author escape evidence (28 plants); RV32 smoke under 3 plants (exit 97/91/99); hosted 417/417 and coverage 795/795, 402/402 | R794-2 | 968a164929698b9a2c4eb96ec207979ff7fea856 |
| Docs | UNCLEAN (F2; R1 is RESIDUE) | PORTING, REQUIREMENTS, `requirements.json`, TESTS, TRACEABILITY, VERIFICATION, CHANGELOG deltas; PR body (all sections); both merge resolutions; comment-rule scan of every added line; commit subjects | R794-2 | 968a164929698b9a2c4eb96ec207979ff7fea856 |

## Real limits

- No standards PDFs were available. Clause numbers and titles were judged from the repository's citations.
- Per the owner's token-economy rule, I did not rerun the full validation kit or the full mutation campaign myself. Exact-head execution evidence for those comes from the hosted run's artifact (28/28, 417/417), and the author's receipts cover `9002bfe` and `13dd785`. My own runs at the exact head were:
  - the RV32 gate;
  - the GCC Debug suite;
  - the `owed-` mutation selection;
  - RV32 smoke under 3 plants;
  - the cost harness;
  - the probes.
- The F2 bound "about one pass per sink with a probe falling due" comes from code reading plus a 14-probe scenario. It is not a proof.
- The evidence commit is unsigned. Its integrity was checked by manifest sha256 and git blob ids only.
- No physical calibration or hardware was run. Field skips are not hardware proof.
- I ran no manager source bank, parent build or parent harness, and I infer none. Hosted jobs were judged by their job and step conclusions and their two artifacts.

## Receipts and reproduction

- Every published file is listed in `MANIFEST.sha256`. The receipts contain no host paths.
- Scripts. Set `TOOLS` to a prefix holding `gtest-1.14.0`; the RV32 scripts also need `riscv64-elf-gcc` and `qemu-system-riscv32`.
  - `scripts/fetch_evidence.sh TREE_TSV OUT`: fetches evidence blobs by id and checks each git blob hash.
  - `scripts/run_probes2.sh HEAD_TREE WORK OUT [one-slot]`: appends `scripts/probe_owed2.inc` to a disposable copy and runs the probes. `one-slot` applies `owed-bind-owes-one` as the control.
  - `scripts/rv32_plant.sh HEAD_TREE WORK PLANT OUT`: runs the RV32 gate under one registered plant. The exit codes in `receipts/rv32-plant-exit-codes.txt` come from running each smoke ELF directly under QEMU.
  - `scripts/measure_cost.sh TREE OUT ISA OPT MEASURE_C -DLANE`: rebuilds the published cost harness.
- Clone integrity after all probes (`receipts/clone-state.txt`):
  - HEAD, the HEAD tree and the index tree are exact.
  - The worktree equals the index and HEAD, and all 98 worktree blobs match the index.
  - All 98 entries are mode 100644. The repository tracks no gitlinks.
  - There are no untracked or ignored files. The bytecode cache my `--help` calls created under `scripts/` was removed.

## Pending manager duties

- Validate the current-dev merge candidate (source base 70936b77, live dev 0a75aa774b89ac89351700f63dd8cbb89694af6c) with the builder and native banks at the merge turn, and link those receipts. Hosted and act acceptance are the manager's.
- Carry R1, and the other review's RES2-RES4 that I concur with, to the residue checklist.
- Re-review at the head that addresses F2.
- The parent PR that binds the receive-ready hook to `acmp_rx_ready` must update `acmp_mutants.py:452-455` (S5) and re-measure the harness row. Until then #26 stays open, as the PR intends.

R794-2 FINISHED
