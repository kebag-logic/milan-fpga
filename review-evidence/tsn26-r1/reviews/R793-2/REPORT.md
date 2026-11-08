[R793] NEGATIVE - exact head 968a164929698b9a2c4eb96ec207979ff7fea856

# R793-2: independent internal review of kebag-logic/tsn-c-stack PR #28 (issue #26), delta round

- Exact head: `968a164929698b9a2c4eb96ec207979ff7fea856`, tree `c1922c5f987572a550f9baa7deafb25708845a5e` (verified in the clone: `receipts/clone-state.txt`).
- Previously reviewed head: `3d57262` (R793-1, NEGATIVE on F1). Source base: `70936b77`.
- Delta since 3d57262:
  - Three author commits: `0e3ae73` (F1 tests), `5bce685` (two-slot BIND_RX), `9002bfe` (redelivery before timer service).
  - Two syncs with main: `13dd785` merges main `d7e6a2a1` (#29, `wire_put_be`), and `968a164` merges main `cc3362f8` (#30, privacy exemption).
- Verdict: **NEGATIVE**, on one new open MINOR (F2, Robustness and Docs).
  - Every prior finding of both reviews is resolved at its cause. F1 is fixed, and the two answer-lost plants escape the round-1 suite (106/106 pass), which shows the new tests were needed.
  - All 28 gates pass at the exact head (rc 0), 417/417 plants are caught, and the cost figures and Release ELFs are byte-identical to the author's receipts.
  - F2 is new and comes from the round-2 design change. The two-slot rule lets a sink's timer probe take the single freed slot ahead of a kept BIND_RX, even when the port follows the new delivery order. The documented and claimed pass count (`ACMP_OWED_MAX` + 1, "unchanged") is then wrong by one pass per such probe. The design itself is sound (it trades a lost probe and a 200 ms retry for one pass), but the port contract's timing figure needs correcting.

## Reconstruction order followed

1. CONTRIBUTING.md (the repository has no AGENTS.md), then the docs index: ARCHITECTURE, PORTING, REQUIREMENTS, TESTS, TRACEABILITY, VERIFICATION.
2. Issue #26: body and acceptance, unchanged since round 1. Its comments are only the author's TAKEN / REVIEW READY / STOP markers. No maintainer or manager comment narrows the scope, and there are no manager evidence comments on the issue or PR beyond the review-start notices.
3. PR #28 body at this head (Round 2, Sync with main d7e6a2a1, Sync with main cc3362f8 sections) and the public review-start comment for R793-2.
4. Authorities, unchanged from round 1: ACMP-12 (updated text), ACMP-03/08/09; IEEE 1722.1-2021 8.2.4, 8.2.5, Tables 8-1 and 8-3; Milan v1.2 5.5.2.3, 5.5.3.5 (5.5.3.5.3, 5.5.3.5.16), 5.5.4, Tables 5.26, 5.32 and 5.47.
5. `git diff 70936b77..968a164` and its history. I read in full `git diff 3d57262 9002bfe` (author delta) and the remerge diffs of `13dd785` and `968a164`.
6. Public evidence at milan-fpga `a380b1d9` (`tsn26-review-evidence` tip), `review-evidence/tsn26-r1`, read by section: `author-r2/a750b`, `author-r2/a750c` and `author-r2/sync-cc3362f8`.
7. My own verdict-relevant pass and probes were finished before I read the prior public findings: R793-1 (my own) and R794-1 (external, PR comment 6719845303). Their resolution is tabulated below.

## Answers to the focus items

1. **F1 (both reviews): RESOLVED at its cause.**
   - New tests:
     - `AcmpOwed.DeclinedBindIsAnsweredAfterTheHold` (`tests/test_acmp.cpp:2787`) asserts the Table 5.32 fields: SUCCESS, controller, talker and uid, listener and uid, count 1, the echoed STREAMING_WAIT and zero stream fields. The answer comes 69 ms after arrival (≤ 200 ms) at position 8, after the 8 owed frames, which leave in order. The GET_RX_STATE held behind it is answered later, reports count 1, and is also within 200 ms.
     - `AcmpOwed.DeclinedGetTxStateIsAnsweredAfterTheHold` (`:2822`) asserts the Table 5.47 fields from the source state at take time, at position 8, with GET_TX_CONNECTION next at position 9, both within 200 ms.
   - Full-suite killer matrix at the head (`receipts/full-suite-killers.txt`, 110-test binary):
     - `owed-bind-rx-drop-restored` and `owed-bind-answer-lost-after-decline` both fail the new BIND test.
     - `owed-get-tx-state-drop-restored` and `owed-get-tx-state-answer-lost-after-decline` both fail the new GET_TX_STATE test. The second of these has that test as its only killer.
   - Applied to the round-1 tree, both answer-lost plants pass all 106 tests (`receipts/answer-lost-at-round1.txt`). So the round-1 suite really missed them, and the new tests close that gap.
   - The PR body's "How to validate" now says A19 checks only the decline and names the two new tests.
   - One SUGGESTION remains (S3): the GET_TX_STATE test does not assert connection_count.
2. **S1 taken as a design change: correct, with one unstated cost (F2).**
   - Code: `room(a, frames)` (`src/acmp.c:328`) takes `OWED_BY_BIND` (2, `:71`) for a BIND_RX (`:1074`). `acmp_rx_ready` needs two free slots (`:1040`).
   - A BIND_RX owes at most two frames. In `bind()` (`:823-851`), `bind_response` makes one `respond`, `probe` makes one `send_probe`, and `srp_stop`, `disc_start` and `publish` send no ACMP frame. So two slots are sufficient and necessary.
   - `DeferredBindWaitsForTwoSlotsAndLosesNoProbe` (`:2860`) and RV32 smoke checks 97-101 show the following: declined at 8 and at 7, taken at 6, `probes_lost` 0, and the probe leaves in the pass after the answer with TMR_NO_RESP timed from its send.
   - Plants: `owed-bind-one-slot`, `owed-bind-owes-one` and `owed-ready-one-slot` are each caught by the gtest suite. On the RV32 target, `owed-bind-one-slot` and `owed-ready-one-slot` each make the smoke exit nonzero (`receipts/rv32-plants/`).
   - The stated trade-off is acceptable. A BIND_RX that would only be answered, such as one for an unknown sink or a rebind of the same talker, waits one pass for a second slot. Its answer still queues behind the same frames, so its departure pass does not move.
   - The same holds for any command that a port gating on `acmp_rx_ready` holds at 7 owed. It is accepted one pass later, but its answer still sits behind the frame whose departure it waited for.
   - The benefit is real: no 200 ms TMR_NO_RESP delay and no used-up retry for each deferred binding.
   - The cost the PR does not state is F2.
3. **S2 (redelivery before timer service): RESOLVED.**
   - `docs/PORTING.md:82-84` gives the order and the reason.
   - The test port model's `pass()` (`tests/test_acmp.cpp:2580-2592`) polls, delivers kept frames, then services due timers. `scripts/check_port_contracts.py` pins the new phrases, and its self-test refuses 33 meaning-removal controls.
   - For a BIND_RX waiting for its second slot, this order no longer keeps the freed slot for the kept command (F2).
4. **Integration note: RESOLVED and accurate.**
   - Parent `sw/firmware/ctrl/test/acmp_mutants.py` lines 452-453 at milan-fpga dev `0a75aa774b89ac89351700f63dd8cbb89694af6c` match exactly the old `room()` body, `busy_drops` included.
   - The note's `-Werror` claim also holds. A plain `if (true)` body at this head fails with `unused parameter 'frames'` under `-Wall -Wextra -Werror` (`receipts/parent-fragment-werror.txt`).
5. **Sync with main d7e6a2a1 (`13dd785`): correct.**
   - VERIFICATION: 413 core plants = 411 (branch: 384 at base + 22 in round 1 + 5 in round 2) + main's 2 `wire-put-be-*` plants. The campaign at the head reports 417 CAUGHT (413 + 4 generated).
   - TRACEABILITY: the conflicted ACMP-02 and ACMP-03 rows keep the branch's tests and anchors and add `Wire.W1PutBeWritesTheLowBytesMostSignificantFirst` (`#L2893`).
   - `tests/coverage.ratchet`: `include/wire.h` 14/14 from main and `src/acmp.c` 795/795 and 402/402 from the branch. My coverage gate run (host GCC 16) gives exactly these.
   - TESTS.md: the Wire anchor `#L2562` was corrected to `#L2893`.
   - The traceability and test-inventory gates pass.
6. **Sync with main cc3362f8 (`968a164`): correct.**
   - The only conflict was CHANGELOG, and both Unreleased entries are kept.
   - `13dd785..968a164` changes only main's `scripts/check_privacy.py`, `docs/IMPORT.md`, `docs/VERIFICATION.md` (privacy rows) and CHANGELOG. No source, test or example changes.
   - Privacy passes at the head: 25 commits, 316 historical blobs and 98 current files, with the exact #29 merge exception.
7. **Cost table: reproduced, and it moved only by main's wire change.**
   - Using the author's published harness, my rv32i -O3 and rv32im -Os measurement ELFs at the exact head are byte-identical to the author's sync receipts (`mg-*-elf.sha256`). The results and `acmp.o` text (18897 and 10605) are identical too (`receipts/measure/`).
   - The "after sync" column equals round 2 plus main's own delta at every step. For example, the worst step is 7904 + (8039 − 7882) = 8061 and 24383 + (22251 − 24374) = 22260. GET_RX_STATE sent is 6274 + 67 = 6341 and 19766 − 941 = 18825. The declined paths stay at 200 and 348, and `acmp_rx_ready` at 10.
   - `sizeof` is unchanged (5064 B RV32, 5072 B x86-64; owed set 640 B), per the author's `sizes-and-images.txt`. This sync changes no `include/acmp.h` byte.
8. **Gates on both targets: reproduced.**
   - This review ran `validate.py --graphs` at the exact head: **28/28 rc 0**, including mutation 417 CAUGHT / 0 ESCAPED / 0 ERROR, privacy, coverage, both sanitizer arms and graphs (4 rendered).
   - `baremetal.py` at the exact head: rc 0 in Debug and Release. The Release ELF `71c3bde3…`, 48952 B, is byte-identical to the author's `13dd785` receipt.
   - The author's own published receipt at `968a164` covers 5 checks: privacy, its self-test, comments, port-contracts and license. Their full 28 was published at `9002bfe` and at each round-2 step, and as 27 + privacy (main's failure) at `13dd785` (S4).

## Findings

### F2: MINOR (Robustness, Docs). With the two-slot rule, a due sink timer probe takes the freed slot ahead of a kept BIND_RX, so the documented pass count is wrong for it
- **Where:**
  - `docs/PORTING.md:82-84`: deliver before timer service, because "Timer service first could let a probe take the freed slot".
  - `docs/PORTING.md:92-93`: "sends it in pass `ACMP_OWED_MAX` + 1 after the egress returns. That delay plus the egress hold must stay within the 200 ms …".
  - PR body, Round 2 item 2: "The pass count for every deferred answer is unchanged."
  - Code: `src/acmp.c:1074` (a BIND_RX needs two slots) together with `transmit`/`send_probe` (`:292-313`, `:720-744`). A timer probe takes any single free slot.
- **Evidence:**
  - Reviewer probe `scripts/probe_timer_ahead.cpp` (`receipts/probe-timer-ahead.txt`) uses the head's own port model (poll, redeliver, then timers), copied into the probe so it runs unchanged at both revisions. Each case fills the owed set, keeps a command, and releases the egress so that the TMR_NO_RESP of other bound sinks falls due in passes 1, 2, …. Answer pass is counted after the egress returns:

    | Kept command, sink timers due during release | Head 968a164 | Round 1 3d57262 |
    |---|---|---|
    | BIND_RX, none | pass 9, `probes_lost` 0 | pass 9, `probes_lost` 1 |
    | BIND_RX, one | **pass 10**, `probes_lost` 0 | pass 9, `probes_lost` 2 |
    | BIND_RX, two | **pass 11**, `probes_lost` 0 | pass 9, `probes_lost` 2 |
    | GET_RX_STATE, one or two | pass 9, `probes_lost` 1 | pass 9, `probes_lost` 1 |

  - What happens: at 7 owed the kept BIND_RX is declined because it needs two slots, so the timer serviced after it finds one free slot and owes its probe there. The next poll frees one slot again, and the BIND_RX is declined again.
  - Commands kept behind the BIND_RX slip by the same passes, because no later frame may be delivered before a kept one.
  - Bound, from code reading:
    - A sink's probe that is owed holds its timer (`timer_held`). TMR_NO_RESP restarts only when that probe leaves (`probe_left`).
    - So each bound sink adds at most one pass while the window lasts less than TMR_NO_RESP. That is at most `n_sinks` (≤ `ACMP_MAX_SINKS` = 16) extra passes.
- **Impact:**
  - The port contract's budget formula, the one an integrator uses to keep "egress hold + passes" within Milan Table 5.26's 200 ms, understates a kept BIND_RX's answer time by up to `n_sinks` passes.
  - The PR's "unchanged" claim is false in this case.
  - PORTING:83-84 implies that delivering first prevents probe interference, which no longer holds for a BIND_RX.
  - Conformance holds for the modelled port (60 + 9 + 16 = 85 ms < 200 ms). The core's behaviour is a sound trade: one pass instead of a lost probe and a 200 ms retry. So this is a contract-accuracy defect, not a code defect.
  - It changes a stated timing figure, so it is not RESIDUE.
- **Required outcome:**
  - (a) In "ACMP owed bound", state the exception and its bound. For example: "Delivering first keeps each freed slot for a kept command, except for a BIND_RX that still needs a second slot. A sink probe that falls due meanwhile takes the freed slot and adds one pass, at most one per bound sink. A kept BIND_RX, and every command kept behind it, is therefore answered by pass `ACMP_OWED_MAX` + 1 + `n_sinks`. Budget the egress hold with that count." Adjust PORTING:83 to match.
  - (b) Correct the PR body sentence. For example: "The pass count is unchanged unless a sink timer falls due during the release. Each such probe now delays a kept BIND_RX by one pass instead of being lost."
  - (c) Recommended, not required: a committed `AcmpOwed` test that pins the slip, for example one due timer giving pass 10 with `probes_lost` 0, plus a plant that the test kills.
- **Verification:**
  - `python3 scripts/validate.py --work <w> --jobs 16 --graphs` gives 28/28. This covers port-contracts: update `CRITICAL` in `scripts/check_port_contracts.py` if pinned phrases change.
  - The PR text no longer claims an unconditional pass count.
  - If (c) is done, `python3 scripts/mutation.py --work <w> --select owed- --jobs 16` shows all CAUGHT.

### SUGGESTION
- **S3 (Tests).** `DeclinedGetTxStateIsAnsweredAfterTheHold` (`tests/test_acmp.cpp:2846-2849`) checks every Table 5.47 field the core sets except connection_count (0).
  - Add `r.count == 0u`, or compare the whole PDU with `same()` as A20 does (`:993`).
  - This is not a behaviour gap: the response builder is shared and A20 pins the count.
- **S4 (Docs, evidence).** With the next sync, publish a full `validate.py` and `baremetal.py` receipt at the exact head.
  - At `968a164` the author's receipt covers 5 checks. The PR's "28 of 28 once main's privacy fix is in" at that head currently rests on this review's run.

### RESIDUE (wording only, carried to the residue checklist)
- **RES1 (PR body, "Sync with main d7e6a2a1" image table).** Round 2's Debug ELF appears as 145380 in the round-2 table and as 145180 in the sync table.
  - Both are real author receipts (`a750b` and `a750c` `sizes-and-images.txt`), built at different export paths. `.text` 47608 and the object text 20917 agree.
  - Fix: after the sync table add "Round 2's Debug ELF reads 145180 here and 145380 above because the two sets were built at different paths; compare Debug ELF bytes only within one table."
- **RES2 (PR body, same section).**
  - "Round 3 merges main d7e6a2a1" → "This sync merges main d7e6a2a1".
  - End the privacy bullet with "Main fixed this in #30; see Sync with main cc3362f8."
- **RES3 (`docs/ARCHITECTURE.md:11`).** "Eight owed frames; past them a command is declined to the port" → "Eight owed frames; past them a command, and a BIND_RX with fewer than two free, is declined to the port".
- **RES4 (PR body, "How to validate", mutation plants).** "Run against the full 109-test ACMP suite" → "Run against the full ACMP test binary (110 tests at this head: the 109 ACMP tests and main's Wire test)".

Comment rule: over the delta's added lines in `src`, `include`, `tests`, `examples` and `scripts`, new comments carry only requirement and clause IDs (`// Milan v1.2 5.5.3.5.3`, `// REQ: ACMP-12, ACMP-03/08/09`). None shows a bench lane label, lane name, review round, reviewer ID or issue-comment ID. The comments gate passes. No RESIDUE arises from it.

## Prior public review findings at this head

| Finding | Source | Status at 968a164 | Evidence |
|---|---|---|---|
| F1 MINOR (Tests, Docs): answered-after-redelivery claimed but not tested for BIND_RX and GET_TX_STATE | R793-1 | **Resolved** | Two new tests with Table 5.32 / 5.47 fields, ≤ 200 ms and in order. Killed by the serve-while-full and answer-lost plants. Answer-lost plants escape at 3d57262 (106/106). PR sentence corrected. TESTS/TRACEABILITY regenerated (gates rc 0). |
| S1 SUGGESTION: a redelivered BIND_RX always loses its first probe | R793-1 | **Resolved** (design change) | Two-slot rule, `probes_lost` 0 in test, RV32 smoke and probe. Residual cost recorded as F2. |
| S2 SUGGESTION: say when to redeliver relative to timer service | R793-1 | **Resolved** | PORTING:82-84, test model `pass()`, port-contract phrases pinned. BIND_RX exception recorded as F2. |
| F1 MINOR (Tests, Docs): same gap | R794-1 | **Resolved** | As R793-1 F1. Its verification ("killed by a plant that serves the command while full, or that loses the redelivered answer") is met by both kinds for each test. |
| S1 SUGGESTION: deferred BIND_RX loses its first probe | R794-1 | **Resolved** | As R793-1 S1. |
| S2 SUGGESTION: name the parent's `busy_drops` fragment | R794-1 | **Resolved** | PR integration note names `sw/firmware/ctrl/test/acmp_mutants.py` 452-453. Verified at parent dev `0a75aa77`, and the `-Werror` claim was reproduced. |
| S3 SUGGESTION: redelivery relative to timer service | R794-1 | **Resolved** | As R793-1 S2, with F2 as the remaining BIND_RX case. |

Neither prior report recorded RESIDUE.

## Lens results

| Lens | Result | Artifact-specific evidence |
|---|---|---|
| Conformance | CLEAN | Every taken own command still gets one specified response, never an error status (IEEE 1722.1-2021 8.2.4/8.2.5, Table 8-3). A BIND_RX owes ≤ 2 frames (code reading of `bind`, `bind_response`, `probe`), so the two-slot rule declines it before any state change. Redelivered answers carry the Milan Table 5.32 and 5.47 fields and leave within 200 ms (Table 5.26) in the new tests. The F2 slip of ≤ `n_sinks` passes keeps the modelled port within 200 ms. `OWED_BY_BIND`'s clause tag (5.5.3.5.3, BIND_RX) is apt. Clause text is judged from repository citations (limits). |
| RTL | CLEAN | No HDL in the delta, so Verilator was not used. Applied to the bare-metal RV32 target: `baremetal.py` rc 0 in Debug and Release at the exact head. The Release ELF is byte-identical to the author's sync receipt. Smoke checks 91-101 step through the two-slot bound. Plants `owed-bind-one-slot` and `owed-ready-one-slot` each make the smoke exit nonzero. Both measurement ELFs are byte-identical to the author's. |
| Robustness | UNCLEAN (F2) | Memory unchanged (640 B owed set, `sizeof` 5064/5072 B). The declined path is 200 / 348 instructions. Two-slot rule: no lost probe, and the retry stays unused. Starvation is bounded: one pass per due sink probe (code reading, probe shows 1 and 2). Re-entry is unchanged (`ReadyPredicateMatchesTheOwedBound`). F2: the pass-count contract is wrong for a kept BIND_RX when sink timers fall due. |
| Tests | CLEAN | 417/417 plants CAUGHT at the exact head. Killer matrix over the 28 owed and full-queue plants on the 110-test binary: every plant fails ≥ 1 test, and each new test is killed by its two plant kinds. Answer-lost plants escape the round-1 suite. Coverage `acmp.c` 795/795 lines and 402/402 branches, `wire.h` 14/14. GCC and Clang-sanitizer suites 8/8. S3 is optional. |
| Docs | UNCLEAN (F2) | PORTING owed-bound section, ACMP-12 (REQUIREMENTS and requirements.json), counter table, VERIFICATION (413 + 4 plants, RV32 row), TRACEABILITY, TESTS, CHANGELOG, port-contract pins and PR body checked against code and receipts. F2 is the timing-figure defect. RES1-RES4 are wording only. |

## Executed evidence (this review, exact head unless stated)

Pinned tool root: GoogleTest 1.14.0, clang-tidy 18 and the clang-18 lexer (`scripts/env.sh`). The GCC arm used host GCC 16.2.1, the sanitizer arm host Clang 23.1.4, and RV32 used riscv64-elf-gcc 16.2.0 with QEMU 11.1.2.
- `scripts/run_gates.sh` runs `validate.py --graphs` (12 jobs) and `baremetal.py` (4 jobs) concurrently. Results: **28/28 rc 0** (`receipts/gates/validate.out`, `validate.rc`, `gates.json`, `logs/`) and bare-metal rc 0 (`receipts/gates/baremetal.out`).
- Full-suite killer matrix: `scripts/full_suite_killers.py` (`receipts/full-suite-killers.{txt,json}`).
- Answer-lost plants at 3d57262: `scripts/plant_at_rev.sh` (`receipts/answer-lost-at-round1.txt`).
- Timer-ahead probe at the head and at 3d57262: `scripts/probe_timer_ahead.cpp` and `scripts/run_probe_timer_ahead.sh` (`receipts/probe-timer-ahead.txt`).
- Cost harness: `scripts/measure.sh` with the author's `measure.c` (`scripts/measure-r2.c`, `-DLANE`) (`receipts/measure/`).
- RV32 plants: `scripts/rv32_plant_smoke.sh` (`receipts/rv32-plants/`).
- Parent fragment compile: `receipts/parent-fragment-werror.txt`.
- Author evidence: milan-fpga `a380b1d9`. All 196 `MANIFEST.json` entries hash-match, and no file is unlisted (`receipts/author-evidence-check.txt`).
- Hosted CI at the exact head, inspected only (`receipts/hosted-checks.txt`): push run `42473350284` and PR run `42473353964`. In each, quality and bare-metal succeeded with all 7 steps executed (none skipped). Hosted and act acceptance belong to the manager.
- Clone restored and verified after the probes (`receipts/clone-state.txt`):
  - Worktree and index equal HEAD. The index tree is `c1922c5f…`, and the blob listing matches HEAD.
  - 98 files, all mode 100644. No gitlinks or `.gitmodules` are required or present.
  - The ignored `scripts/__pycache__/` left by the gate run was removed. There are 0 untracked or ignored entries.
  - All probes ran in exported copies under the packet's `scratch/`.

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `src/acmp.c` (`room`, `acmp_rx`, `acmp_rx_ready`, `bind`, `bind_response`, `probe`, `send_probe`, talker GET_TX_STATE), ACMP-12 text, PORTING owed bound, new tests' field assertions, issue #26 acceptance | R793-2 (delta). Untouched code keeps its R793-1 verdict | 968a164929698b9a2c4eb96ec207979ff7fea856 |
| RTL | CLEAN | `examples/rv32/smoke.c` `acmp_owed_smoke` (checks 91-101), `baremetal.py` Debug and Release, Release ELF and object hashes against the author's receipts, two RV32 plants, measurement ELFs | R793-2 | 968a164929698b9a2c4eb96ec207979ff7fea856 |
| Robustness | UNCLEAN (F2) | two-slot rule and readiness predicate, timer-probe interaction (reviewer probe at the head and at 3d57262), starvation bound, memory and instruction counts | R793-2 | 968a164929698b9a2c4eb96ec207979ff7fea856 |
| Tests | CLEAN | `tests/test_acmp.cpp` (three new tests, ready test rewrite, `pass`/`drain`), `tests/mutations.json` (5 new and 19 updated plants, 3d57262 → 9002bfe), coverage ratchet, full validate run, killer matrix, round-1 escape check, author escape evidence | R793-2 | 968a164929698b9a2c4eb96ec207979ff7fea856 |
| Docs | UNCLEAN (F2) | PORTING, REQUIREMENTS, requirements.json, TRACEABILITY, TESTS, VERIFICATION, ARCHITECTURE, CHANGELOG, `check_port_contracts.py`, PR body (all sections), merge resolutions, comment-rule scan | R793-2 | 968a164929698b9a2c4eb96ec207979ff7fea856 |

## Real limits

- The IEEE 1722.1-2021 and Milan v1.2 texts were not available. Clause content was judged from the repository's citations, the code's clause tags and the cited table contents, not re-read from the standards.
- F2's bound (at most one extra pass per bound sink) comes from code reading. The probe confirms the one- and two-sink cases in the 3-sink fixture, not the 16-sink worst case.
- The evidence commit `a380b1d9` has no cryptographic signature (`%G?` = N). Its integrity rests on the MANIFEST.json hashes, which I verified, and on the public branch tip.
- The sanitizer arm ran with host Clang 23, because pinned Clang 18 serves only as the lexer. CI's Ubuntu 24.04 Clang 18 arm is covered by the hosted run, not by this review. Coverage ran with host GCC 16 and matched the ratchet the author generated with GCC 13.3.
- Debug ELF bytes depend on the build path: mine is 145772 B, and it was not compared. Debug figures are judged from the author's two receipt sets (RES1).
- The parent harness row ("an ACMP command behind the owed input") still needs the parent PR that binds `acmp_rx_ready` and renames `busy_drops`. Issue #26 stays open by design ("Relates to").
- Physical calibration NOT RUN. No hardware was used, and field skips are not hardware proof.
- No manager source bank runs at this head, and none is claimed or inferred. Source-head execution evidence is the author's published receipts plus this review's own runs.

## Pending manager duties

- Build and validate the current-dev merge candidate at the merge turn (source base 70936b77 against live dev 0a75aa774b89ac89351700f63dd8cbb89694af6c; builder and native banks), and link those receipts on the PR.
- Own hosted and act acceptance. Both runs at the exact head showed success at inspection.
- Route F2 to the author. After the fix, obtain two independent positive reviews at the new head.
- Carry RES1-RES4 to the residue checklist, and S3 and S4 as optional.
- Track the parent PR: bind the ready hook to `acmp_rx_ready` (or keep declined frames), change the `acmp_mutants.py` 452-453 fragment, then measure the harness row.

R793-2 FINISHED
