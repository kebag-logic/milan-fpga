[R835] NEGATIVE - exact head 056d619ddba179edb0dd2914e14a4b1d51988dd8

# R835-4: cleared-context internal delta review of PR #901 (issue #895), rounds 6 to 9

- **Head:** `056d619ddba179edb0dd2914e14a4b1d51988dd8`, tree `0e61c5c5587c826d696c205cf70295f7c1c82a9a`, base `dev-soft-core` (source base `cec88385`).
- **Delta reviewed:** round 5's `62298ab5` to `056d619d`. This lane's own patch is `07ed787e..056d619d`, because #902 merged into `dev-soft-core` as `659d7687` with `07ed787e`'s tree. I compared it with round 5's own patch, `7398ec0a..62298ab5`, file by file (`receipts/lane-interdiff-code.txt`). I read #902's merges only for this lane's conflict resolution.
- **Authority:**
  - #895's acceptance 1-5, as amended by issuecomment-6840463408. Acceptance 6 is a bench item and is not reviewed here.
  - The rulings issuecomment-6876349305, -6886630886, -6892130675 and -6895331865.
  - IEEE 802.1Q-2018 35.2.2.8 and Table 10-7.
  - The flip bounds: the 1x1/1if load at most 0.70, and the last queued notice's bound at 140 ms at one interface.
  - The stated-cost rule: each stated cost is the measurement plus 5 %, rounded up to 5 µs.
  - The owner's rule of 11-15 that a ROM overflow becomes S14 debt.

**Verdict: NEGATIVE.** Two MINOR findings are open.

- **F1 (MINOR, Tests and Conformance):** no test or planted defect can fail on the term this round's one ruled wire change moved. That term is the THE TRANSMIT term of `SRP_REDECLARE_CS`. A probe that drops it passes every Talker arm at both interface counts.
- **F2 (MINOR, Docs):** four authoritative prose statements still give #894's figures as this head's: `AECP_QUEUED_MS` at 130 ms, and `CTRL_LOOP_TX_MS` at 99 ms at two interfaces.

Everything else the ruling asked for checks out at the head:

- the image identity and the carry argument;
- every 1x1/1if row;
- the per-pass headroom;
- the restated costs;
- the hold-off's derivation;
- the ledger correction;
- the self-test pin;
- the full-pass receipts.

All prior R835-3 and R836-3 findings are closed. One RESIDUE and three suggestions are new.

## Findings

### R835-4-F1 — MINOR — Tests, Conformance — no executable control holds `SRP_REDECLARE_CS`'s THE TRANSMIT term, the term this round's ruling moved

- **Where:**
  - `sw/firmware/ctrl/srp/srp_mbx.c:35` (`#define SRP_REDECLARE_CS (2u * 1000u + SRP_JOIN_CS + (CTRL_LOOP_TX_MS + 9u) / 10u)`).
  - `sw/firmware/ctrl/test/srp_talker.cpp:52-55` and `:290-312` (`ChangedDestinationWaitsTwoLeaveAllTimePeriods`).
  - `sw/firmware/ctrl/test/srp_talker_mutants.py:110-111`: the only plant on the expression, `talker-hold-off-one-leaveall`, removes a whole LeaveAllTime.
- **Authority:**
  - **Acceptance 2:** a changed destination waits two LeaveAllTime periods after the Leave (IEEE 802.1Q-2018 35.2.2.8, Table 10-7).
  - **Acceptance 3:** unit tests and planted defects cover the withdrawal.
  - **Ruling issuecomment-6895331865, item 2:** the terms above 2,000 cs "cover the Leave's latest departure, so they must follow the tx row". Its item 1 is this round's one wire change, 2,029 to 2,030 cs at two interfaces, made through exactly that term.
- **Evidence (my probe, `scripts/holdoff_mutants.sh`, `receipts/arms/`):**
  - **At the head:** all four arms pass (`receipts/arms/head.log`): `srp_talker.cpp` at 1x1/1if (11 tests) and at 8x8/2if (11), `SrpGate` at 8x8/2if (7), and SRP+ACMP at two interfaces (76).
  - **`m1-drop-tx-term`:** `SRP_REDECLARE_CS` becomes `(2u * 1000u + SRP_JOIN_CS)`, 2,019 cs at both counts. Every Talker arm still passes at both interface counts (rc 0, `receipts/arms/m1-drop-tx-term.log`).
  - **`m2-drop-join-and-tx`:** `(2u * 1000u)`. This one is caught: 3 failures at each count, among them "the changed destination comes no sooner than two LeaveAllTime periods after the Leave" (`receipts/arms/m2-drop-join-and-tx.log`).
  - **Why m1 escapes.** The unit model's Leave departs within about a JoinTime of its request, so 2,019 cs still clears the wire Leave by more than 2,000 cs. The worst case the TX term covers, a Leave delayed by THE TRANSMIT up to `CTRL_LOOP_TX_MS`, is never staged.
  - **The test's own expectation is circular.** `kHoldOffMs` (`srp_talker.cpp:55`) is computed from the same macros as the firmware. Its early check (`:297-303`) is anchored at the gate call `at + kTwoLeaveAllMs`, not at the Leave's wire time plus the hold-off.
  - **After restore,** the clone's `srp_mbx.c` blob equals HEAD's (`receipts/clone-integrity.txt`).
- **Impact:**
  - The firmware at the head is correct; I found no wire defect.
  - But the round's one ruled wire change, and the claim that the hold-off follows the tx row, have no control that can fail. A regression that drops or under-states the TX term passes every test and campaign. Its hold-off is then 2,019 cs from the Leave's request. At 8x8/2if the Leave can depart up to a JoinTime plus 105 ms after that request, so the new declaration can depart under 2,000 cs after the Leave on the wire, against 35.2.2.8.
  - The SRP campaign's 415 rows, including the 70 `talker-` rows, contain no such plant.
- **Required outcome:**
  - Some executable control fails when the hold-off under-states THE TRANSMIT term, at both interface counts. For example: a Talker test that holds the Leave's departure up to the stated `CTRL_LOOP_TX_MS` and checks the new declaration departs at least 2,000 cs after the Leave on the wire; or an equivalent check with its planted control.
  - A planted defect equivalent to `m1` is added to the Talker campaign and caught at 1x1/1if and 8x8/2if.
- **Verification:**
  - `scripts/holdoff_mutants.sh` (or the campaign's new row) reports `m1` caught at both counts, and `m2` still caught.
  - The arms pass at the unmutated head.
  - The SRP campaign's count and its talker-row count are restated.

### R835-4-F2 — MINOR — Docs — four authoritative prose statements give #894's `AECP_QUEUED_MS` 130 ms or `CTRL_LOOP_TX_MS` 99 ms as this head's

- **Where:**
  - `docs/design/SPLIT_CONTROL_MEMORY.md:2266`: "the last's is #894's amendment's 130 ms (`AECP_QUEUED_MS`; ...)", present tense.
  - `sw/firmware/ctrl/aecp/README.md:120`: "every notice queued behind it within `AECP_QUEUED_MS`, 130 ms at 1x1/1if".
  - `tb/verilator/ctrl_service_budget/README.md:172`: "At 1x1/1if the last is held to 130 ms, `AECP_QUEUED_MS` there".
  - `docs/design/SPLIT_CONTROL_MEMORY.md:2689`, in "What is left": "which `CTRL_LOOP_TX_MS` states as 34 ms, and 99 at two interfaces".
- **Authority/evidence:**
  - The head's constants are `AECP_QUEUED_MS (MBX_N_IF == 1u ? 140u : 62u)` (`aecp_mbx.h:75`, `2b7f8428`) and `CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 34u : 105u)` (`ctrl_loop.h:377`, `845364b6`).
  - FR_NFR 3.4.1 (`FR_NFR.md:386-387,415`) and the head's own section 13 paragraphs (`SPLIT_CONTROL_MEMORY.md:2655-2680`) state 140 and 105 correctly.
  - These four sentences came from #894's text, through the syncs (`git blame` of `:2689` is #902's `fe1fd541`). They are true on #894's head, and are not history-marked here. The merges' own rule ("each side's text where it states its own figures") was applied to the image sizes (`056d619d`, checked) but not to these bounds.
- **Impact:** the authoritative design page, the AECP module README and the harness README contradict the header and FR_NFR on a normative bound at this head. A reader of the harness README would grade the last queued notice against 130 ms.
- **Required outcome:** each of the four states this head's figure (140 ms; 105 ms at two interfaces), with #894's 130 or 99 marked as #894's head's or as history.
- **Verification:** a grep at the new head for present-tense 130 ms `AECP_QUEUED_MS` and 99 ms `CTRL_LOOP_TX_MS` statements finds only history-marked or #894-attributed ones; the doc gates pass.

### RESIDUE

- **R835-4-RS1 — RESIDUE — Docs (PR body).**
  - **The defect:** the live PR #901 body names round 5's reviews as the current ones: "Internal cleared-context reviewer: `[R835]` (R835-3, started issuecomment-6881026642) / External reviewer: `[R836]` (R836-3, issuecomment-6881271637)".
  - **Exact fix:** "Internal cleared-context reviewer: `[R835]` (R835-4, started issuecomment-6899719764)", with the external reviewer's line naming R836-4 and its start comment.

### SUGGESTIONS (optional; none affects coverage)

- **R835-4-S1 — Tests/Docs — the 18 µs headroom is to the bounds, not to the flip check.**
  - My probe raises the 1x1/1if base in both stated tables (`scripts/per_pass_probe.sh`, `receipts/per-pass/`). It reproduces the threshold exactly: at a 243 µs base, last 137.93 and txL 49.00; at 244, last 141.36 and txL 49.02.
  - But the flip check already fails at a base of 226 µs (+1 µs): `CTRL_LOOP_TX_MS states 34 ms, under the built design's tx row 34.02 ms`. The statement is at zero slack by construction (34.00 against 34).
  - That failure is a restatement by rule, not a bound. At 1x1/1if no wire change follows below 41 ms, since (TX+9)/10 stays 4.
  - Optional: say in section 13 and the PR that the 18 µs is the bounds' headroom, and that any rise restates `CTRL_LOOP_TX_MS`.
- **R835-4-S2 — Docs.** `SPLIT_CONTROL_MEMORY.md:2659` cites "`per_pass_threshold.py` in the round's receipts", which is not in the tree. Optional: name its published path (`review-evidence/895-r1/author-r8/scripts/per_pass_threshold.py` on the evidence branch).
- **R835-4-S3 — Robustness — the gate's early return (`srp_mbx.c:649-653`, `f14e56a9`).**
  - I checked it is behaviour-neutral. Its premise, "only `srp_mbx_init` and `srp_mbx_gate` write the gate and the sources' destinations" (`srp_mbx.h:83-88`), holds today:
    - `dest_mac` is written only at `:667`;
    - `gate` only at `:478` and `:676`;
    - `allocated` only at `:670`;
    - `init`'s `memset` clears `gate_seen`.
  - Every call that does not return early leaves `gate == valid`.
  - Only the base check is planted (`talker-gate-repeat-ignores-its-base`).
  - Optional: a plant that drops `gate_seen` from the condition, so the first call's path after `init` is held too.

## Focus checks

1. **Prior findings:** see the table below. All of R835-3's and R836-3's MAJOR, MINOR and RESIDUE findings are closed at this head.
2. **The ruling applied exactly (issuecomment-6895331865).**
   - `845364b6` changes `CTRL_LOOP_TX_MS` to `34u : 105u` alone. In C, `CTRL_LOOP_TX_MS`'s only uses are `SRP_REDECLARE_CS` (`srp_mbx.c:35`) and a static assert at one interface only (`ctrl_loop.c:203`).
   - So the only object a two-interface build can change is `srp_mbx.o`, and a one-interface build changes nothing. That makes the carry argument sound even for harness images outside the 552-file set.
   - The published identity receipts (`author-r9/receipts/identity/`) show:
     - 0 one-interface files differing;
     - 12 two-interface files differing, each in only `li a3,2029` -> `li a3,2030` (`7ed00693` -> `7ee00693`) by `objdump -d` and `-s`;
     - 552/552 identical across both syncs.
   - From `73388996` to the head, the only non-comment firmware change is that define.
   - The 8x8/2if `valid-destinations` leg's measured logs are byte-identical to round 8's. Only the stated tables and the build hash differ in `results.json`, as expected.
   - One interface keeps 34 ms and 2,023 cs.
3. **Every 1x1/1if row within its bound at the built slice.** I ran the graders myself at the head (`receipts/graders/`):
   - `flip_grade.py --check --point 1x1/1if` PASS. Its table is byte-identical to `author-r9/.../g-final/flip-1x1.log`: last 136.65/140, ACMP 29.63/30, txL 48.58/49, tx 34.00/49, R4 13.25, R4L 203.57.
   - `tier_grid.py`: CHOSEN slice 900 µs, the built `CTRL_LOOP_SLICE_US` (`ctrl_loop.h:282`); the author's `rules.log` reads "ruled 900 built 900".
   - The load is 0.517/0.514 (`load_grade.py --check` PASS).
   - The 260 µs pass cost and its 278/279 µs threshold are reproduced by my probe (S1).
   - The load inputs are the stated tables. Round 8's survey (`author-r8/receipts/survey/*-head-f93317cb.txt`) shows every stated cost at or above its leg measurement by the rule, with UNDER 0 at both points.
   - Round 8's 1x1/1if legs keep only arm A's 7 long-standing `backlog-owed` misses (62.9 ms against 63.0 at round 5).
   - Joins are 188.102-190.121 ms at 1x1/1if and 185.605-190.228 at 8x8/2if, within 181-239.
4. **The restated costs are at or above their measurements:**
   - 1x1/1if polls' base: 21,094 cycles -> 221.5 -> 225 (`poll_grade.py:99`, `load_grade.py:211`);
   - events' fixed part: 3,041 -> 35;
   - TICK: 4,784 -> 55;
   - 8x8/2if base: 32,705 -> 345;
   - notice past `AECP_FAN_BYTES`: 66,481 -> 700 (`poll_grade.py:101-102`);
   - fixed part: 3,437 -> 40;
   - MAAP slot: 21,120 -> 225;
   - `AMAP_LIVE_WRITE`: 2,465 -> 30 (`rows_tiers.py:101`).
5. **`SRP_REDECLARE_CS` is derived from headers.**
   - It is `2000 + CTRL_LOOP_JOIN_CS (19, ctrl_loop.h:342) + (CTRL_LOOP_TX_MS + 9)/10`: 2,023 cs at one interface and 2,030 at two.
   - The test's horizon is derived from the same macros (`srp_talker.cpp:55`; comment `:53` reads 20,230/20,300 ms, correct). Nothing is typed.
   - What no test holds is the TX term itself: F1.
6. **The ledger.**
   - `ctrl_memory_ledger.py:35` records `PLAT_8X8_1` as 18,240 B.
   - In the author's final ledger, `plat_ledger.py` passes at every point: 8x8/1if `ctrl_plat` 18,240 B at 56.0; platform 8x8/2if 60.5 with 1,368 B left; fixture and harness arms at 59.0 with 368, 60 and 200 B; every other point 56 or under. The merge ledger before the fix is rc 1, as disclosed.
   - `test_ctrl_memory.py` passes at the head here (`receipts/test_ctrl_memory.log`).
   - No lwSRP or HDL change, and no gitlink moved.
7. **The self-test pin.** `selftest_notice.py:83-89` pins `(140, 62)` read from the header. Its over-bound probe moved from 131 to 141 ms (one over), with the within-bound probes unchanged. The `ctrl_loop.h` comment states 140.
8. **The full pass** (author's receipts on clean clones at `056d619d`):
   - `verify-table.md`: 139 steps ran, 226 not run with a reason, 0 bad.
   - Campaigns: 716/716, AECP 299, SRP 415 (70 `talker-`), 0 escaped.
   - Lane gates a/b/c are rc 0, except `flip_check`/`flip_check_8x8`, which exit rc 1 at 8x8/2if by design. `harness_selftest`: 0 failures; its `CONTROL ... ESCAPED` line is the self-test's own expected-escape case (`selftest_share.py:323-339`).
   - Sweep: 4 shards, 65 suites; `tsn_fuzz` 164 and 675 pass.
   - Talker arms rerun at `449d29d2`; I reran them at the head with the same result.
   - INDEX: 670/670 hashes verified (`receipts/author-r9-index-check.txt`). Archive manifest: 1,507/1,507 entries for author-r6..r9 (`receipts/evidence-manifest-verify.txt`).

**Comment rule.** The lane's added source lines (`07ed787e..056d619d`, excluding `*.md`) contain no lane label, review round, reviewer ID or issue-comment ID. The only "round" hits are pre-existing protocol uses ("THE RETRY's round").

## Prior findings at this head

| Finding | State | Evidence at `056d619d` |
|---|---|---|
| R835-3-F1 MAJOR (1x1/1if polls' base 205 against 215 by rule; slice) | **CLOSED** | Base restated to 225 by rule from 21,094 cycles (`poll_grade.py:99`, `load_grade.py:211`, `2657af23`). The slice rule's choice is built (900/900). Round 8's survey shows UNDER 0. |
| R835-3-F2 MINOR (8x8/2if `AMAP_LIVE_WRITE` 25) | **CLOSED** | `rows_tiers.py:101` states 30 (2,465 cycles -> 30 by rule, `b69388c7`). |
| R835-3-RS1 RESIDUE (PR body "to be assigned") | **CLOSED** | The body names the reviewers. Its now-stale round labels are the new RS1. |
| R835-3-S1 (MAAP mark before first opening) | retained, optional | `maap_mbx.c` is unchanged in the delta. |
| R835-3-S2 (raw `STATED` check without the 5 %) | retained, optional | The author now runs a per-round cost survey (`author-r8/scripts/costs_vs_stated.py`), which is outside the tree. |
| R835-3-S3 (table title against `5b264bf2`) | **CLOSED** | The cited title and wording are gone from section 13. |
| R835-2-S2 (INDEX mismatches) | **CLOSED** | author-r9 INDEX: 670/670. |
| R835-2-S1, R835-1-S1 = R835-2-S3, R836-1 S2, R836-1 S3 | retained, optional | The hold-off, licence and swap code is unchanged in the delta. Only `srp_mbx_gate`'s early return was added (S3 above). |
| R836-3-F1 MINOR (closing R4 12.85) | **CLOSED** | "R4 12.85" no longer appears. Section 13's head rows give R4 13.25, matching my `flip-1x1.log`. |
| R836-3-RS1 RESIDUE ("move no byte of any image") | **CLOSED** | Neither phrase appears in section 13 or the PR body. Section 13 now states identity by sha256 and names the one instruction that differs. |

## Lens results

- `[R835] MINOR Tests, Conformance — sw/firmware/ctrl/srp/srp_mbx.c:35, srp_talker.cpp:290-312, srp_talker_mutants.py:110 — F1`
- `[R835] MINOR Docs — SPLIT_CONTROL_MEMORY.md:2266,2689, aecp/README.md:120, ctrl_service_budget/README.md:172 — F2`
- `[R835] PASS RTL — ctrl_loop.h:282,377, aecp_mbx.h:75, srp_mbx.c:35,639-682, srp_mbx.h:83-88, ctrl_loop.c:203, author-r9 identity receipts`
  - No HDL in the delta and no gitlink moved.
  - The constants' widths and rounding are checked: (105+9)/10 = 11, so 2,030 cs; (34+9)/10 = 4, so 2,023 cs.
  - The gate's early return was checked for behaviour-neutrality against every writer of `gate`, `dest_mac` and `allocated`.
  - The 64 B ROM growth at 8x8/1if is attributed to the two new fields and ledgered.
- `[R835] PASS Robustness — srp_mbx.c:639-682 (repeat, reentry, before-attach and mask paths with their plants at srp_talker_mutants.py:174-183), selftest_notice.py:83-89 (within and over-bound probes at both counts), plat_ledger refusal at the uncorrected merge (ledger-merge rc 1)`
  - No new input path. S3 is optional.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | acceptance 1-5 as amended; rulings 6876349305, 6886630886, 6892130675, 6895331865; `ctrl_loop.h:282,377`; `aecp_mbx.h:75`; `srp_mbx.c:35`; `flip_grade`/`tier_grid`/`load_grade` reproduced (`receipts/graders/`); identity receipts; survey receipts | R835-4 | `056d619ddba179edb0dd2914e14a4b1d51988dd8` |
| RTL | CLEAN | as in the PASS line above; `receipts/lane-interdiff-code.txt`; `receipts/clone-integrity.txt` (gitlinks) | R835-4 | `056d619ddba179edb0dd2914e14a4b1d51988dd8` |
| Robustness | CLEAN (S3 optional) | `srp_mbx.c:639-682`; `srp_mbx.h:83-88`; plants at `srp_talker_mutants.py:174-183`; `selftest_notice.py:83-89`; ledger refusal receipts | R835-4 | `056d619ddba179edb0dd2914e14a4b1d51988dd8` |
| Tests | UNCLEAN (F1) | `srp_talker.cpp:52-55,290-312`; `srp_talker_mutants.py`; my Talker arms at the head and the `m1`/`m2` probes (`receipts/arms/`); `rows_tiers` 1033/1033, `flip` 585/585, `load` 26/26 selftests; `test_ctrl_memory.py`; the author's campaigns, gates and sweep receipts | R835-4 | `056d619ddba179edb0dd2914e14a4b1d51988dd8` |
| Docs | UNCLEAN (F2; RS1 residue; S1, S2) | `SPLIT_CONTROL_MEMORY.md:2266,2414,2655-2700` and both merges' resolution; `FR_NFR.md:386-387,415`; SRP README `:218-233`; harness README `:127,172`; AECP README `:120`; live PR body; REVIEW READY issuecomment-6899637516 | R835-4 | `056d619ddba179edb0dd2914e14a4b1d51988dd8` |

## Real limits

- **Not run here:**
  - the full pass, the firmware campaigns, the sweep, the harness legs, the ledger builds and the identity hashing;
  - act and hosted jobs.
  - For these I relied on the author's published receipts, verified against the archive manifest and the INDEX. I ran only the graders, the Talker arms, the ledger unit test and two disposable probes.
- **Probe trees:**
  - The grader probe ran on a `git archive` export of the head, plus copies of the `tsn-c-stack` and `lwSRP` submodules.
  - The hold-off mutants ran in the review clone. After each, `srp_mbx.c` was restored and its blob checked against HEAD's.
  - The clone's index tree equals the head tree; there are no tracked changes and no untracked files; the gitlinks are unchanged (`receipts/clone-integrity.txt`).
- **The evidence archive** `50e931db` is unsigned. Its integrity rests on `MANIFEST.json` (1,507/1,507) and the round's INDEX (670/670).
- **Hosted contexts at the exact head,** read at review time (`receipts/hosted-checkruns-summary.txt`):
  - succeeded: `changes`, `bdd-conformance`, `full-ci-gate`, `wire-accountability`, `docs-check-no-git`, `split-cdc`, `verilator-lint` and pinned Yosys;
  - skipped: physical gPTP;
  - still queued or in progress: the Verilator and Yosys shards and the firmware jobs.
  - The PR is not a draft, and it is MERGEABLE.
- **No manager source bank** at this head is claimed or inferred. Physical calibration is NOT RUN. Field skips are not hardware proof. Acceptance 6 is not reviewed.

## Pending manager duties

- the current-dev merge candidate (live dev `6b66f66d`), with builder and native banks, at the merge turn;
- act and the hosted exact-head contexts;
- carrying RS1 to the residue checklist;
- re-review of F1 and F2 at the corrected head.

R835-4 FINISHED
