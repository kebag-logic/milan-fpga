[R712] NEGATIVE - exact head d930ea98f75be96f1062217d62bccd24dd291265

# R712-5: external review of PR #810 (#665 S2b), the delta a3f23bba..d930ea98

- Head `d930ea98f75be96f1062217d62bccd24dd291265`, tree `76a51c452dc5f631981c40dcb95880460d24101d`; PR #810 is open and ready, and its live head is this commit. Base `dev-soft-core` `a68536fa`.
- Delta judged: `a3f23bba..d930ea98`, 29 commits, 47 files (rounds 15, 15 continued, 15 continued (2) and 16).
- Judged against the [A10] rulings on #665 (issuecomment-6620376502, -6630265194, -6634982529) and the round 16 REVIEW READY (issuecomment-6673169386).
- Authorities: AGENTS.md sections 6 to 8; `docs/reference/FR_NFR.md` section 3.4.1; `ctrl_loop.h` (THE BOUND, THE SHARE, THE STEP, THE RETRY, THE TRANSMIT, THE TICK); `aecp.h`; `srp_mbx.c`/`srp_bounds.h`; `SPLIT_CONTROL_MEMORY.md` sections 13 and 14; lwSRP `mrp_mad.c` (the join timer).
- Role: external reviewer, cleared context. All five lenses were applied.
- I wrote my verdict and findings (`receipts/independent-verdict.txt`) before I read R711-4 and R712-4.

## Verdict in one paragraph

The mechanics of the delta are sound, and the published measurements are true.

- THE RETRY's age bounds a retried notice.
- THE TRANSMIT takes SRP's build out of every pass that takes a record.
- THE TICK's cap takes the heaviest pass to 190,420 cycles.
- Every figure I checked matches its receipt.
- I rebuilt two images at the exact head, and both match the measured legs byte for byte.
- I re-ran the 8x8 notice leg at the exact head, and its table is byte-identical to the published one.

The verdict is NEGATIVE on two MAJOR findings and one MINOR, all about bounds that are claimed "by construction":

- **F1.** The 8x8 composed burst's last SRP record is within 18 ms by measurement only. The constants bound that row at about 34 ms. The round 16 ruling's item 1 asks for the bound to be derived from the constants, and the author says it is not.
- **F2.** THE TRANSMIT can now hold an MRPDU that a join timer made owed for up to 44 ms by its own constants, and 176 ms for the fourth participant. FR_NFR 3.4.1 bounds MRP join, leave, periodic and LeaveAll service at 18 ms from the timer's deadline. The head grades the hold against the 200 ms JoinTime instead, and no harness row times it under load. Before this delta, the poll built one MRPDU a pass, so the hold was a few passes.
- **F3.** The 20 ms retried-notice bound holds for the first of several retried notices whose ports answer together. By the head's own constants, the second is 22 ms.

One RESIDUE and four suggestions follow. Every prior finding from R711-4 and R712-4 is resolved at this head.

## Method

**Context, in order:**
1. AGENTS.md (CONTRIBUTING.md through it).
2. The three rulings and the round 16 REVIEW READY.
3. FR_NFR.md 3.4.1.
4. The diff `a3f23bba..HEAD`, with `ctrl_loop.c` `ctrl_loop_service` and the new parts of `aecp.c` and `srp_mbx.c` read whole.
5. lwSRP's transmit gate (`mrp_mad.c:850-854`, `:1421`).
6. The author's public packet, `review-evidence/665s2b-r1/author-r16`, at evidence commit `cd93800c4a4dacb88a5a296a7f9a7e273e94f067`.

**Evidence integrity** (`scripts/check_evidence.py`, `receipts/evidence-check.txt`):
- The packet's `MANIFEST.json` lists 609 `author-r16` files. Every one matches its `published_sha256`: 0 bad, 0 missing, 0 unlisted.
- Five receipts differ from the packet's own `INDEX.md`. All five are among the 65 the manifest marks as path-redacted.

**Image identity:**
- The legs ran on clones of `12e5ec56`, firmware `65a56d02`.
- Since `65a56d02`, the head changes only comments in firmware sources outside the tests, plus one `_Static_assert` rewritten to read `CTRL_LOOP_SRP_MS` (`srp_mbx.c:31`). Neither emits code.
- I rebuilt the 1x1 and 8x8 arm A images at the exact head (`scripts/imgcheck.sh`, `receipts/imgcheck.txt`):
  - `ccedce05...49242` matches leg N-A1.
  - `3f6f8ac5...33f6b` matches leg N-A8.
- The author's image-identity check covers 9 of 9 no-draft images, and its exact-head G-A1 and G-A8 tables equal the N-A1 and N-A8 tables (`cmp`).

**My own leg** (`scripts/leg.sh`, `receipts/NT-8.run.log`, `receipts/table-compare.txt`):
- The 8x8/2if `answering-later` notice groups, `notice-retried-0` to `-7`, at the exact head, on the pinned Verilator 5.050 (identity checked), with 16 jobs.
- Result: 8 groups, 0 refusals, 0 of 7,540 passes over the share. The notices land 12.540 to 12.990 ms after the port's answer.
- The image is `f6c70312...`, and `table.md` is byte-identical to the published NT-8 table.
- An earlier attempt of mine was invalid. A second invocation, started while the first was still grading, overwrote its group logs. The receipt is the clean third run, with `--reuse-build` on the same build.

**Sums** (`receipts/evidence-check.txt`):
- Twelve head legs: 94 + 80 + 93 + 79 + 56 + 56 + 55 + 55 + 4 x 8 = 600 groups.
- With X4-A8, X4-NT8 and P81-A8: 1,489,645 work passes, 0 over the share, 0 refusals.
- Only the three egress-held paths miss, six instances a leg, as before.
- All match the REVIEW READY.

**Gates at the committed head:**
- Every lane gate's `.rc` is 0: baremetal, behave, the boot runs, boundary a/b, census, the idiom gates, the hot list, ctrl_memory, both diff checks, fw_coverage, the rv32 self-test, the mailbox generator, the harness self-test, lint, the store's self-test, soc_options and test_builder.
- The four sweep shards each report `exit_code 0` at `d930ea98`.
- The firmware shards report `RESULT: PASS`, `mutants: 669 of 669 caught` and `named plants not caught: none`.
- docs.yml: 64 steps ran, 0 bad, 31 hosted-only steps not run with reasons. The first docs-gates-0 run failed only for a missing `wavedrom` pin in the local environment, and the re-run is rc 0.
- Every name in `aecp_retry_mutants.py`, `srp_transmit_mutants.py` and `loop_step_mutants.py` appears in the shard logs.

**Comment rule:**
- I scanned the added non-document lines of the delta (`receipts/comment-scan.txt`).
- Every hit is the retry "round" concept, the loop's assumption labels A1 to A4, or a test ID.
- No lane label, lane name, review round, reviewer ID or comment ID. No new comment-rule RESIDUE.

## Findings

### F1 - MAJOR - Conformance, RTL (architecture), Robustness, Docs - SRP's 18 ms row is met by measurement, not derived from the constants

- **Where:** `sw/firmware/ctrl/loop/ctrl_loop.h:296-315` (`CTRL_LOOP_SRP_MS`); `ctrl_loop.h:62-69` (THE SHARE); `docs/design/SPLIT_CONTROL_MEMORY.md:1839-1846`.
- **Authority:** round 16 ruling item 1 (issuecomment-6634982529): "Bring the 8x8 composed burst's last SRP record within 18 ms ... Choose the construction by pass class and derive its bound from the constants, as THE STEP and THE RETRY are." FR_NFR.md 3.4.1: SRP/MRP is bound at 18 ms.
- **Evidence:**
  - `CTRL_LOOP_SRP_MS` is defined as `9u * CTRL_LOOP_SHARE_US / 1000u`, which is THE SHARE restated. Its comment says that "this bound does not count the composed burst's passes": 32 SRP records at two a pass take sixteen passes, "so that row fits by those passes' measured cost". Section 13 (`:1843`) says the same.
  - The REVIEW READY's open question says so directly: "the constants bound that row at about 34 ms".
  - THE SHARE (`ctrl_loop.h:65-68`) still derives the 2.0 ms share from "(N + 1) passes must fit that bound. The deepest admitted wait is the A3 row of seven owed frames". The ruling places the composed burst in the SRP row's scope. So the deepest admitted wait is SRP's sixteen passes, plus one for each THE TICK pass, and the header contradicts itself.
  - The measured fit is real. The notice groups give 16.48 to 17.11 ms at 8x8/2if, and my own leg reproduces it. Over every window the most is 17.765 ms, 0.235 ms inside the bound.
- **Impact:**
  - Nothing in the build or the gates holds the row. A later change to any record handler's cost, an untested configuration, or a new layout can move it past 18 ms without any compile-time or construction argument failing. Only a re-run of the harness would show it.
  - This is the "fits by chance" case the same ruling's item 2 rejects for passes.
  - No manager decision on the author's open question has been published.
- **Required outcome:** one of these two.
  - (a) A construction whose stated bound, derived from the constants by pass class, puts the composed burst's last SRP record within 18 ms at both points, with THE SHARE's derivation correct for the deepest admitted wait.
  - (b) A public manager decision that amends round 16 item 1, accepting a measured bound for this row and naming what gate keeps it.

  In either case, `ctrl_loop.h:62-69` must no longer state that the deepest admitted wait is eight passes.
- **Verification:**
  - For (a), the derivation in `ctrl_loop.h` and a compile-time check, plus a plant that breaks it and is caught by name.
  - For (b), the decision's link in `ctrl_loop.h` and section 13.
  - In both cases, the THE SHARE paragraph restated.

### F2 - MAJOR - Conformance, RTL (architecture), Robustness, Tests, Docs - THE TRANSMIT can hold a timer-driven MRPDU 44 ms, 176 ms for the fourth participant, against an 18 ms service bound

- **Where:** `ctrl_loop.h:271-295` (`CTRL_LOOP_TX_AGE`, `CTRL_LOOP_TX_MS`); `srp_mbx.c:27-34` (the `SRP_JOIN_CS` static asserts) and `:73-74` (`tick` holds the build); `SPLIT_CONTROL_MEMORY.md:1834`.
- **Authority:** FR_NFR.md 3.4.1:
  - `:343` and `:384`: SRP/MRP "join, leave, periodic and LeaveAll", bound 18 ms.
  - `:353`: "A timer event starts at its armed deadline, not dequeue."
  - `:364`: "No extra budget is granted at timer arm, expiry or retry."
  - Round 16 ruling item 1: "No other channel's bound may move past its own."
- **Evidence:**
  - lwSRP transmits only once `join_wait` is zero (`mrp_mad.c:1421`), which `on_join_timer` sets (`:850-854`) from the centisecond the loop dispatches. So an MRPDU becomes owed at the join timer's expiry, in `tick`.
  - At the head, `tick` sets `tx_held`, and the build waits for a pass that takes no record, at most one event and no centisecond. Failing that, it waits for its age: more than two held centiseconds, then the next pass after an ordinary one.
  - `CTRL_LOOP_TX_MS` states the result as 30 + 7 x 2 = 44 ms from the hold. `srp_mbx.c:33` holds 2 x `MBX_N_IF` x 44 = 176 ms, one MRPDU a call, against the 200 ms JoinTime.
  - That compares the hold with the JoinTime. It is not the 18 ms the row grants after the timer's deadline.
  - Before this delta, the poll built one MRPDU in every pass, the participants in turn, so a timer-driven MRPDU waited a few passes.
  - The harness's only SRP transmit row is `srp.domain` (`scenario.py:668-670`, measured at 2.034 ms in N-A8). It runs in the idle `srp` group, with W = 200 ms. No row times a join, periodic or LeaveAll MRPDU under the composed sustained-record load, where the build would age.
  - Section 13 (`:1877`) confirms that no staged group ages a build.
- **Impact:**
  - Under sustained records, which the ruling counts as admitted input, a join-timer MRPDU can leave up to 44 ms after its deadline by construction, and the fourth participant's up to 176 ms. That is past the 18 ms MRP service bound.
  - Since the next transmit opportunity is gated by JoinTime, a request that arrives just after a transmission is served at JoinTime plus up to 44 ms: 244 ms, past Milan's 240 ms maximum JoinTime.
  - The bound this delta moved belongs to SRP's own family. It is not one of the record rows the REVIEW READY lists as unmoved.
- **Required outcome:** one of these two.
  - (a) A construction that keeps an MRPDU made owed by a timer within 18 ms of the timer's deadline under any admitted input, stated in `ctrl_loop.h` from the constants.
  - (b) A public decision on how FR_NFR 3.4.1's W applies to MRP transmit opportunities, with FR_NFR.md and `ctrl_loop.h` stating the graded bound if JoinTime is to absorb THE TRANSMIT's hold.

  Either way, a harness row must time a timer-driven MRPDU from its deadline to its TX commit under the composed sustained load, at both points.
- **Verification:** the new row in section 13 at both points and both arms, with a control that ages the build and is caught by name.

### F3 - MINOR - Conformance, Robustness, Tests - the retried-notice bound covers only the first of several notices answered together

- **Where:** `sw/firmware/ctrl/aecp/aecp.h:27-36`; `aecp.c:631-693` (`scan`); `ctrl_loop.h:247-265`.
- **Authority:** the round 15 continued (2) ruling item 1 (issuecomment-6630265194): "a retried notice is built and committed within 20 ms under every input". FR_NFR.md 3.4.1 `:355` and `:364`.
- **Evidence:**
  - A round builds the first notice its port answers, and returns (`aecp.c:660-676`).
  - `aecp.h:31-35` limits the 8 + 10 = 18 ms bound to "while nothing waits ahead of its round", with "each notice owed ahead of it costing it its own round and the pass that sends it".
  - Take two descriptors whose retries are held while the face block does not answer, and whose ports answer together. That is the held or resetting datapath the round 15 ruling names. The second is built in the aged-retry pass after the first is sent, which adds two passes of THE SHARE. By the head's own constants it is committed within 8 + 10 + 2 x 2 = 22 ms of its port's answer, over 20. Each further notice adds 4 ms.
  - The harness stages one retried notice. The measured 12.3 to 13.5 ms rows leave room for one or two more by measurement, but not by construction, and not for many.
  - The round 16 ruling says the round 15 continued (2) items "stand as met", and this caveat was in `aecp.h` at `d0eef1cb`. I record it because no review has applied a lens to it and the text states a conditional bound under a ruling that says "every input".
- **Impact:** a datapath reset with several pending notices can deliver the later ones past their 20 ms. Nothing measures this case.
- **Required outcome:** one of these two.
  - (a) A round, or a bound, that keeps every retried notice answered together within 20 ms, with the most notices a reset can make pending stated and derived.
  - (b) A public decision that the bound is per round, with `aecp.h` and section 13 saying so.
- **Verification:** a notice group with two or more retried notices whose ports answer together, graded per notice. Plus a unit test with a plant.

### RESIDUE-1 - wording and format only - `sw/firmware/ctrl/loop/ctrl_loop.h:163-164, :178-179, :225-226, :251, :262`

Several comment paragraphs the delta added have ragged wraps:
- a one-phrase line: `:164` "cycles at 8x8/2if. Built in", `:225` "record a channel", `:251` "which sends what the round";
- lines past the file's comment width: `:178` and `:262`, about 130 columns.

**Exact fix:** reflow those paragraphs to the surrounding comment width, with the wording unchanged.

### Suggestions (optional)

- **S1. Measure the aged build's pass class.** "Given whole to an aged build" is bounded only by composition, 171,351 + 12,571 = 183,922 cycles (`ctrl_loop.h:111-114`). No group stages it. A labelled control that withholds `tx_pass`, so that every build ages, would give the class a measured heaviest at both points.
- **S2. The struct-ends subset.** The struct-ends layout ran the notice groups and arm A's windows and saves, not `srp` or `acmp-notk`. Section 13 argues the rest is at least 28,649 cycles under the share. If a later round re-runs the struct-ends layout, running every group would make the claim direct.
- **S3. The step's room** (retained from R712-4 SUGGESTION-2). The step's 0.97 ms against `NVM_STEP_US` is still not gated.
- **S4. Retained from R712-4 SUGGESTION-1 and -3:** the save's worst case on the product's flash part, and `capture_coherence`'s mutant-driver sizing. Neither changed.

## The checks requested

1. **THE RETRY.**
   - Met for a single notice. Retry/aged-retry ordering (`ctrl_loop.c:190-224`): an aged step comes first and takes the round after the step, then an aged retry, then an aged build after an ordinary pass. No two passes given whole run back to back.
   - `CTRL_LOOP_RETRY_MS` = 4 + 3 x 2 = 10 ms is derived from the constants. `aecp_mbx.c` holds 8 + 10 <= `AECP_NOTICE_MS` at compile time.
   - Rows: 12.30 to 13.51 ms, and my leg gives 12.540 to 12.990 ms at 8x8.
   - `retry-ageless` is caught at both points (RA-1, RA-8).
   - My run of the harness self-test at the head gives rc 0, `self-test: 0 failures` and 151 `MUTANT caught` lines, the two `transmit-beside-records` grader mutants among them (`receipts/harness-selftest.log`). The packet's `gates/lane/harness_selftest.log` is a 162-line excerpt that does not show that count.
   - Every plant name I extracted from the three plant tables (22) appears in the firmware shard logs, which report none missed.
   - F3 is the multi-notice gap.
2. **The SRP lever.**
   - The measured row is met at both points, with and without drafts: 16.48 to 17.11, 15.98 to 16.46, 10.74 to 10.88 and 10.23 to 10.42 ms.
   - `transmit-beside-records` is caught, 8 of 8 (TB-8, 19.59 to 20.11 ms).
   - "Derived by pass class" is not met: F1. One bound moved: F2.
   - The other record rows stay within their bounds (`tables/notice-rows.md`, section 13).
3. **Pass classes.**
   - Every figure in `ctrl_loop.h:101-116` matches `tables/pass-classes.md`.
   - The least margin is 9,580 cycles at the head layout and 10,844 at struct-ends, both at least 6,490.
   - The aged-build class is bounded by composition (S1).
4. **Re-measure.**
   - The twelve legs plus struct-ends and 8x8/1if: 667 groups, 1,489,645 passes, 0 refusals, 0 over the share.
   - The notice-retried groups and the save windows are included.
   - The least row margin is 0.235 ms (N-A8 `table.md:377-379`).
5. **Restatement.**
   - `ctrl_loop.h`, `aecp.h` and sections 13 and 14 match the receipts. Every table row of `section13-rows.md`, `pass-classes.md` and `notice-rows.md` appears verbatim in the document. Section 14 matches `estimate-32x32.md` apart from capitalisation.
   - F1 covers the THE SHARE paragraph that was not restated.
6. **Gates.** Every round 15 gate is rc 0 at the committed head (Method).

## Prior findings at this head

| Finding | State at this head | Evidence |
|---|---|---|
| R711-4 F1 / R712-4 F1 (an aged step among a window's records; the basis for N = 2) | **Resolved** | Aged windows staged at limit and one short (`c9cf8138`, `bc4685ec`); `ctrl_loop.h:230-239` restates the reason; least margin 0.235 ms measured (N-A8 `table.md:377-379`) |
| R711-4 F2 (a change's worst case with a save in flight) | **Resolved** | `nvm_store.h:32`: 22.15 s beside a save in flight (`3ec8aad9`); the in-flight save is re-measured in the save legs |
| R712-4 F2 (the age's test cannot tell centiseconds from dispatches) | **Resolved** | `test_port_loop.cpp:994-1010`, one TICK record of three; plant `step-age-counts-dispatches` (`loop_step_mutants.py:131-133`) caught |
| R711-4 RESIDUE-1 / R712-4 RESIDUE-1 (S paragraph said twice) | **Resolved** | `SPLIT_CONTROL_MEMORY.md:2046` says it once |
| R711-4 RESIDUE-2 (test-list line split) | **Resolved** | `test_nvm_more.cpp:12-24` |
| R711-4 RESIDUE-3 (longest step rounded two ways) | **Resolved** | 0.97 ms in both `nvm_store.h:97` and `ctrl_loop.h:121` |
| R712-4 RESIDUE-2 (the age's definition dropped "or owed nothing") | **Resolved** | `SPLIT_CONTROL_MEMORY.md:1436, 1442, 1595` |
| R712-4 SUGGESTION-1, -2, -3 | Retained as S3 and S4 | Unchanged |

## Lens results at this head

| Lens | Result | Examined at d930ea98 |
|---|---|---|
| Conformance | UNCLEAN: F1, F2, F3 | the three rulings; FR_NFR.md 3.4.1 `:331-400`; `ctrl_loop.h:62-116, 230-315`; `aecp.h:18-49, 282-293`; `aecp_mbx.c:169-200`; `srp_mbx.c:27-34`; lwSRP `mrp_mad.c:850-854, 1421`; `tables/*.md`; my NT-8 leg |
| RTL (architecture) | UNCLEAN: F1, F2 | `ctrl_loop.c:122-267` (pass classes, the tick cap at `:153-154` and `:161-163`, aged ordering `:190-224`, `ordinary` at `:261`); `srp_mbx.c` `tick` `:59-76`, `poll` `:890-1011`, `transmit` `:1014-1069`, `transmit_aged` `:1073-1077`, attach and destroy; `aecp.c:189-211, 631-693, 741-770` |
| Robustness | UNCLEAN: F1, F2, F3 | sustained-input and backlog paths of all three deferrals; refusal paths (`ctrl_loop_set_retry` and `_set_transmit` null and re-entry; `srp_mbx_attach` with a transmit taken); `round_waits` guards; `srp_mbx_destroy` unbinding; a BAD record consumes a slot (`ctrl_loop.c:172-175`) |
| Tests | UNCLEAN: F2, F3 | `test_port_loop.cpp` L17 `:1102`, L18 `:774`, L19 `:1163`, L20 `:1243`, L21 `:1325`; `srp_mbx.cpp:1495-1595`; `test_aecp.cpp:1580-1632, 2230-2262`; `aecp_retry_mutants.py`, `srp_transmit_mutants.py`, `loop_step_mutants.py`; shard logs (669 of 669, named plants none missed); harness controls RA-1, RA-8, TB-8, AH-A8; `selftest_notice.py`, `selftest_share.py` |
| Docs | UNCLEAN: F1, F2; RESIDUE-1 | `ctrl_loop.h` header; `aecp.h`; the AECP, SRP, ctrl, gtest, ctrl_nvm and harness READMEs; `MAILBOX_SPLIT.md`; `SPLIT_CONTROL_MEMORY.md:1797-2146`; comment-rule scan (`receipts/comment-scan.txt`) |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MAJOR, F2 MAJOR, F3 MINOR) | rulings 6620376502, 6630265194, 6634982529; FR_NFR.md 3.4.1; `ctrl_loop.h:62-315`; `aecp.h`; `srp_mbx.c:27-34`; `mrp_mad.c:1421`; packet tables; NT-8 re-run | R712-5 | d930ea98f75be96f1062217d62bccd24dd291265 |
| RTL | UNCLEAN (F1, F2) | `ctrl_loop.c:122-267`; `srp_mbx.c` THE TRANSMIT client; `aecp.c` retry round and age | R712-5 | d930ea98f75be96f1062217d62bccd24dd291265 |
| Robustness | UNCLEAN (F1, F2, F3) | sustained, backlog and refusal paths above | R712-5 | d930ea98f75be96f1062217d62bccd24dd291265 |
| Tests | UNCLEAN (F2, F3) | unit tests, plants, harness controls, shard logs, my NT-8 leg (`receipts/table-compare.txt`) | R712-5 | d930ea98f75be96f1062217d62bccd24dd291265 |
| Docs | UNCLEAN (F1, F2); RESIDUE-1 does not affect coverage | `ctrl_loop.h`, `aecp.h`, READMEs, `SPLIT_CONTROL_MEMORY.md` sections 13 and 14, comment scan | R712-5 | d930ea98f75be96f1062217d62bccd24dd291265 |

## Real limits

- **Simulation only.** No hardware ran. Physical calibration was NOT RUN, and field skips are not hardware proof. Every figure is the harness's simulated CPU at 100 MHz on `sys`.
- **What I reproduced.** One leg (NT-8) and two images (N-A1, N-A8) at the exact head. Every other leg rests on the published receipts, the author's image-identity check (9 of 9 no-draft images) and the firmware equivalence I verified by diff. The drafts and struct-ends images are labelled scratch trees and were not rebuilt.
- **No probe for F2 or F3.** Both are derived from the head's own stated constants and code paths. I staged neither an aged MRPDU nor two simultaneous retried notices.
- **No source bank.** I did not run, and do not claim, any manager source bank at this head.
- **Hosted checks are a snapshot.** At 2026-11-06T01:37Z, the exact head's hosted checks had no failure, and several Verilator shards, `elaborate` and `firmware-boundary` were still in progress or queued. Physical gPTP was skipped.

## Pending manager duties

- Rule on F1. It is also the author's open question in the REVIEW READY.
- Rule on F2's reading of W for MRP transmit opportunities, or return it to construction.
- Rule on F3.
- Acceptance of the hosted and act runs at the exact head.
- Building and validating the current-dev merge candidate (live dev `cc204c6fd2349b543d73f15c97162a2c4434c86e`) at the merge turn.
- Carry RESIDUE-1 to the residue checklist.
- A second independent positive review at a head that includes the fixes.

R712-5 FINISHED
