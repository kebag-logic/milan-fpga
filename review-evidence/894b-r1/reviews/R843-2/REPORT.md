[R843] POSITIVE - exact head 98c0b62be911f5cff7a03ebfee7f837c23847d14

# R843-2: internal independent delta review of PR #914 (issue #894, also #872), round 4

- **Head:** `98c0b62be911f5cff7a03ebfee7f837c23847d14`, tree `42431e547e28fcdaa50feec57700fef4887d92e0`, on a detached clean clone.
- **Delta reviewed:** `716a8ae7..98c0b62b`, four commits:
  - `6da0dc73`, the source-comment sweep;
  - `b7feef24`, the THE SHAPES guard and each host arm's own contract;
  - `3bb204c8`, `egress_ledger.py`;
  - `98c0b62b`, the idiom fix to `egress_ledger.py`.
- **Prior coverage:** the round-3 head `716a8ae7` was reviewed in full by R843-1 (POSITIVE) and R844-1 (NEGATIVE on F1). Code this delta does not touch keeps R843-1's lens verdicts, because nothing it depends on changed: every image is byte-identical and every grader except `egress_ledger.py` changed only in comments.
- **Result:** every prior finding is resolved at its cause. No BLOCKER, MAJOR or MINOR finding is open. There are three SUGGESTIONs and three RESIDUE items.
- **Constraints kept:** no source change, commit, push or GitHub write.

## Context reconstructed

I read AGENTS.md, CONTRIBUTING.md and docs/README, then the authorities named in the brief:

- **#894's held-egress ruling, item (a):** a new or larger held-egress miss fails the leg, and the seven rows stay recorded misses, never passes.
- **The flip rows and ceilings:** they are unchanged by this delta.
- **FR_NFR.md 3.4.1, and SPLIT_CONTROL_MEMORY.md section 13** (the ledger table and the ruling-name map).
- **The diff and history** `7398ec0a..98c0b62b`, with the delta `716a8ae7..98c0b62b` read in full.
- **The author packet** `review-evidence/894b-r1/author-r4` at `843c40b1`. I fetched it read-only into a scratch bare repository.

I read the prior findings (R844-1, issuecomment-6885381555; R843-1, issuecomment-6885564795) only after my own pass over the diff.

## Prior findings at this head

| Finding | Disposition at 98c0b62b | Evidence |
|---|---|---|
| R844-1-F1 (MAJOR): larger held-egress misses still pass | **RESOLVED at its cause** | See F1 below |
| R844-1-R1 / R843-1-R1 (RESIDUE): issue-comment IDs and review rounds in source comments | **RESOLVED** | See R1 below |
| R843-1-S1 (SUGGESTION): `AECP_ATTEMPT_US` names a table `aecp.h` does not include; two-interface core arms at the tracked contract | **TAKEN**; a stated remainder is carried as S2 | See S1 below |

### F1: the seven held-egress rows held to their ledger

**The tree's rule.** `tb/verilator/ctrl_service_budget/egress_ledger.py:140-161` (`findings`) holds the rows as follows:

- Each of the seven ledger rows fails when its most possible value is over its figure (`over`, `:66-68`). The value is held in 10 ns units: exact for a grade, and the printed value plus half a microsecond for a log.
- A row never released or answered fails.
- A ledger row with no measured instance fails (`unseen`).
- An instance that is not measured fails.
- Any other budget miss fails (`new_miss`).

No row is waived by its name. The one place a name matters is `is_row`: a ledger name in a group other than `backlog-owed` is graded as a new miss, not as a ledger row.

**The ledger matches section 13.** `LEDGER` (`:43-46`) equals the table at `SPLIT_CONTROL_MEMORY.md:2528-2536`, row for row. The self-test enforces this, and a mutant that moves one figure by a hundredth is caught. The table's row names are now the harness's own probe names: `backlog-owed.service.{acmp,aecp}.last.if0`, as the round-3 leg log prints them (`C-A0.log:300-306`).

**My runs.**

| Run | Result |
|---|---|
| `egress_ledger.py --selftest` at head (`receipts/egress_ledger_selftest.log`) | 60 controls PASS (30 in process, 30 as a process), all 8 mutants caught, rc 0. This includes the earlier waive-by-name rule. |
| My R844-1-shaped input (`probe_enlarged.py`, `receipts/probe_enlarged.txt`) | All seven rows at their figures: rc 0. `backlog.owed.if0` at 100.0 ms: rc 1, naming it, +36.76 ms. `backlog-owed.service.aecp.last.if0` one bus cycle over: rc 1, naming it. |

**The packet gate.** I read `scripts/gate_r4.py` in full:

- Its held-egress and new-miss decisions are `egress_ledger.from_results`, `from_log` and `findings` from the tree.
- `gate-r4-controls.txt` records 20 of 20 controls, including the 14 per-row plants and R844-1's two inputs (the enlarged row and the unmeasured required row), both exiting 1.

**The regrade of round 3's six 8x8/1if legs from their logs is sound and valid evidence for item (a):**

- **The logs are the published ones.** The six published logs hash to the values in `PROVENANCE.txt`, and the packet INDEX entries for them match.
- **My rerun passes.** Rerunning the tree's tool over them (`receipts/egress_ledger_round3_logs.txt`) gives PASS, rc 0. The seven rows sit 0.150 to 0.231 ms under their figures after the +0.5 us bound, so rounding cannot flip any of them.
- **A log is complete for this criterion.** run.py prints one `BUDGET` line per budget miss straight from the grades (`run.py:534-544`, `:778-779`). `from_log` requires exactly one run summary, zero refusals, and as many `BUDGET` lines as summary misses. The summaries give 7, 0, 0, 0, 0 and 0 misses with 0 refusals over 112 groups, so "no other row missed" is proven by the counts, not inferred.
- **The other criteria rest on round 3's grades.** The CPU-decided rows, queued notices, R4L, joins, slices and rounds need the deleted per-group grades. gate_r4 says so openly ("not regraded from them"). Those criteria stand on round 3's `gate_r3` grade, which R843-1 accepted at `716a8ae7`. This delta changes neither the image nor any grader that decides them.
- **Log at `d8629751`.** The logs ran at `d8629751`, an ancestor of `716a8ae7`. Round 3 accepted that carry, and `img-3-final-against-716a8ae7.txt` records all eight images at 98c0b62b as byte-identical to 716a8ae7's.

### R1: the source-comment rule

- **My scan finds nothing.** `comment_scan.sh` over every added non-Markdown, non-docs line of `7398ec0a..98c0b62b` (1,722 added lines) finds 0 issue-comment IDs, review rounds, reviewer or author IDs, or lane labels (`receipts/comment_scan_7398ec0a_98c0b62b.txt`).
- **Every replacement names the right ruling.** I paired each hunk of `6da0dc73` by its removed IDs and added ruling names. All 44 hunks map correctly:

  | Comment ID | Ruling name |
  |---|---|
  | 6867393730 | shape |
  | 6870437042 | map-keying |
  | 6871343905 | held-egress |
  | 6878014227 | retry-cost |

  `SPLIT_CONTROL_MEMORY.md:2471` maps the names for a cold reader, and the links sit in the paragraph before it (`:2469`).
- **The sweep changed no code** (`ident_check.py`, `receipts/sweep_identity_716a8ae7_6da0dc73.txt`). All 23 C/H/C++ and Python files are identical by comment-stripped token stream or by docstring-stripped AST. The two exceptions are `selftest_notice.py` and `selftest_round.py`, whose differences are exactly the five printed check descriptions.
- **This supports carrying the sweep, the 8x8/1if measurement and the harness legs.** The receipts show every image byte-identical (ELF and loadable bytes). My own spot check found `aecp.c`'s host object across the include reorder byte-identical in `.text` and in disassembly at both heads (`receipts/aecp_object_identity.txt`).

### S1 (prior): the THE SHAPES guard and the arms' contract

- **The guard fires where it should, and only there.**
  - `aecp.h:67-69` raises `#error` when `AECP_CHARGES_ATTEMPTS` is defined and `CTRL_LOOP_RETRY_ATTEMPT_US` is not.
  - `aecp.c:1-8` includes `ctrl_loop.h`, then defines the flag, then includes `aecp_internal.h`. `ctrl_loop.h` includes only `mbx.h`, so no include-guard path skips the check.
  - My probe (`receipts/aecp_guard_probe.txt`): the head compiles rc 0 with no `#error`. Both planted orders (no table, and the table only after `aecp.h`) fail at `aecp.h:68` in the exact THE SHAPES words. The campaign rows `attempt-charged-without-the-shapes` and `attempt-charged-before-the-shapes` match those orders (`aecp_retry_mutants.py:198-207`), and the receipts show both refused in those words inside 277 of 277.
- **The stated limit is acceptable.** The guard fires only for a unit that declares it charges a refused attempt. Every other unit includes `aecp.h` without charging anything, and a unit that used `AECP_ATTEMPT_US` without the table would still fail to compile, on an undeclared name.
- **The two-interface core arm now gets its own contract.** `test_aecp.cpp:42-43` asserts `MBX_N_IF == AECP_TEST_INTERFACES`. `aecp_arms.py:111-119` gives a two-interface core or work arm with no mailbox group its own generated contract, through `srp_arms.prepared`'s variant tree. The receipt shows the core arm at two interfaces passing 83 of 83 tests on its own contract, and a planted two-interface arm at the tracked contract refused by the assertion's words.

## Gates at 98c0b62b (author receipts, spot-verified)

- **Hosted steps:** `workflows-verify-98c0b62b.md` has 365 rows: 139 steps ran with rc 0 and 226 did not run, each with a reason (`not_run.json`), and none is bad.
  - **The LiteX timeout and its rerun.** `elaborate-gates-1` gate_19's first run hit the `test_soc_timing_cuts` 900 s wall-clock limit. The harness reports that as UNKNOWN, not a failure. The job's rerun on a fresh clone passed 8 of 8.
- **Lane gates:** 59 gates. The four nonzero exits are exactly the by-design `*_exits_1` gates (`rows_tiers_report`, `flip_check`, `flip_check_1x1_as_built`, `flip_check_8x8`), and every clone was clean afterwards.
- **Firmware campaigns:** control 716, AECP 277 and SRP 345, all `[ok]` with 0 escaped.
- **`docs_inventory --check` was not run.** It exists only on dev and arrives with the sync, which is a stated, acceptable not-run.
- **Packet index:** 41 of the 45 INDEX entries match their published bytes. Four scripts do not; see S3.

## Findings

**S1: SUGGESTION.**
- **Lenses:** Robustness, Tests.
- **Where:** `tb/verilator/ctrl_service_budget/egress_ledger.py:76-86` (`from_results`), `:112-126` (`read`).
- **Evidence:** in results-directory mode the tool skips `results.json` and reads only group grades. A group that the harness refuses outright gets no grade file (`run.py:529-533`), and the same is true of the run-level refusals from `unstated` and `long_notice.missing`. So such a refusal is invisible in this mode, while log mode fails it. My probe (`probe_ledger.py`, `receipts/probe_ledger_dirmode.txt`, P1) gives rc 0 for a directory whose `results.json` records a refused group.
- **Why it is not a defect:** run.py exits 1 on any refusal even with `--record-budget-findings` (`run.py:643-648`), and gate_r4 fails any leg that did not end rc 0. No leg can pass this way, which matches how R844-1 treated the round-3 gate's permissive unmeasured-input handling. P2 and P3 in the same receipt are synthetic and cannot arise from `grade.py`.
- **Optional:** in directory mode, read `results.json`'s `refusals`, or require it and fail when they are present, so both input modes hold "any instance not measured" alone, with a matching control.
- **Verification:** P1 exits 1.

**S2: SUGGESTION (the stated remainder of R843-1-S1).**
- **Lenses:** RTL, Robustness.
- **Where:** `sw/firmware/ctrl/test/aecp_arms.py:113-116` (the debug arm) and `sw/firmware/ctrl/test/aecp_wire.py:133-136`.
- **Evidence:** at two interfaces these still compile the core at the tracked one-interface contract, which is the shipping shape's attempt cost. Both say so in their comments, with a reason, and neither measures THE RETRY's costs, so it is harmless today.
- **Optional:** give them their interfaces' contract too, or assert in each that it measures no round cost.

**S3: SUGGESTION (the evidence packet, not the tree).**
- **Lens:** Docs.
- **Where:** `author-r4/INDEX.md`.
- **Evidence:** the published bytes of `scripts/index.py`, `scripts/lane_gates_r4.sh`, `scripts/launchR4.py` and `scripts/mkqueueR4.sh` differ from their indexed sha256 and size. They look like edits made after indexing. No receipt, and not `gate_r4.py`, is affected, and no verdict here rests on those four.
- **Optional:** regenerate INDEX.md after the last edit, or record the edit.

**RES1: RESIDUE.**
- **Lens:** Docs.
- **Where:** `egress_ledger.py:42` and `:318`.
- **Problem:** two pieces of history wording.
  - `:42` reads "its measurement on the image the follow-up started from". "The follow-up" is a development-history reference that a cold reader cannot resolve.
  - `:318`'s mutant description reads "the earlier rule: ...".
- **Exact fix:**
  - `:42`: "(section 13's ledger figures at 8x8/1if, which the held-egress ruling, item (a), holds a miss to)".
  - `:318`: "a ledger row waived by its name whatever its size".
- **Impact:** wording only. The second is a printed description and changes no outcome.

**RES2: RESIDUE.**
- **Where:** the PR body (`author-r4/PR-BODY.md:22`).
- **Problem:** "`test_aecp.cpp` asserts that each host arm's contract is at its own interfaces" is too broad. The debug arm compiles `test_aecp_debug.cpp`, and both it and the wire comparison keep the tracked contract by design.
- **Exact fix:** "...each host arm that compiles `test_aecp.cpp`...".

**RES3: RESIDUE.**
- **Where:** packet prose, `receipts/source/carry-by-identity.txt`.
- **Problem:** it names "counters-f5-3bb204c8.txt" and the range "716a8ae7..3bb204c8", but the published receipt is `counters-f5-98c0b62b.txt` and the head is 98c0b62b. `3bb204c8..98c0b62b` touches only `egress_ledger.py`, which is already listed, so the listing itself is complete.
- **Exact fix:** name `counters-f5-98c0b62b.txt` and the range `716a8ae7..98c0b62b`.

## Lens results (artifact evidence)

**PASS: Conformance.**
- **Artifact:** `egress_ledger.py:140-161` against #894's held-egress ruling, item (a).
- **What was checked:** the seven rows stay recorded misses and are never called passes; a larger miss (one cycle or 36.76 ms) or a new one fails; R844-1's inputs fail.
- **Also checked:** the flip rows and ceilings, which are unchanged because the images are identical and the deciding graders are AST-identical. FR_NFR.md:394 and section 13:2526 state the rule as the code implements it.

**PASS: RTL (firmware and architecture).**
- **Artifact:** `aecp.h:58-70`, `aecp.c:1-8` and `ctrl_loop.h:224-227`.
- **What was checked:** the include graph; the guard firing only when the table is missing; `aecp.c`'s object identical across the reorder; all eight images byte-identical; the comment-only sweep in `ctrl_loop.h`, `aecp_mbx.[ch]` and `aecp.h` (identical token streams).

**PASS: Robustness.**
- **Artifact:** `egress_ledger.py` (the input modes and fail-closed paths) and my probes P1-P3 and the enlarged-row probe.
- **What was checked:** a malformed `BUDGET` line, a missing or doubled summary, a refusal, a short `BUDGET` count, a never-answered row, an unmeasured row, a ledger name in another group, an unknown point (rc 2), and the 10 ns and 1 us bounds.
- **Not a failure:** the one directory-mode gap is covered upstream (S1).

**PASS: Tests.**
- **Artifact:** `egress_ledger.py:204-349` (30 controls run two ways, 8 mutants), `aecp_retry_mutants.py:198-207`, `test_aecp.cpp:42-43`, gate_r4's 20 controls, the regrade, and my rerun of the self-test and the regrade.
- **What was checked:** each new control can fail for its defect. Each mutant is caught by a named control, and the planted arm and include orders fail in their words.

**PASS: Docs.**
- **Artifact:** `SPLIT_CONTROL_MEMORY.md:2469-2471` and `:2526-2536`, `FR_NFR.md:394`, the harness `README.md:156-163`, `aecp/README.md:22-32`, the `rows_grade.py:120` docstring line, and the PR body's finding table.
- **What was checked:** the claims against code and receipts, and the ledger table against `LEDGER` and the leg log's names. Remaining items are RESIDUE and SUGGESTION only.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `egress_ledger.py:140-161` against item (a); gate_r4's controls; the regrade of six logs; FR_NFR.md:394; section 13:2526-2536; the flip ceilings carried by identical images and graders | R843-2 | `98c0b62be911f5cff7a03ebfee7f837c23847d14` |
| RTL | CLEAN | `aecp.h:58-70`; `aecp.c:1-8`; `ctrl_loop.h` comment-only; aecp.c object identity; the 8-image identity receipt | R843-2 | `98c0b62be911f5cff7a03ebfee7f837c23847d14` |
| Robustness | CLEAN (S1, S2 optional) | `egress_ledger.py` reader and decision paths; probes P1-P3; the enlarged and one-cycle probe; the guard's planted orders | R843-2 | `98c0b62be911f5cff7a03ebfee7f837c23847d14` |
| Tests | CLEAN (S1 optional) | `egress_ledger.py --selftest` (60 PASS, 8 of 8 caught); the campaign rows; `test_aecp.cpp:42-43`; the arm receipts; gate_r4's 20 controls | R843-2 | `98c0b62be911f5cff7a03ebfee7f837c23847d14` |
| Docs | CLEAN (RES1-RES3 carried, S3 optional) | section 13; FR_NFR.md 3.4.1; the harness and AECP READMEs; the comment scan of `7398ec0a..98c0b62b`; the ruling-name mapping, 44 of 44 hunks; the PR body | R843-2 | `98c0b62be911f5cff7a03ebfee7f837c23847d14` |

For code the delta leaves untouched, R843-1's coverage at `716a8ae7` carries to this head. Nothing within those lenses' scope changed except comments, which are proven token- and AST-identical, so no lens is un-covered.

**Residue checklist:** RES1, RES2, RES3. (R843-1-R1 and R844-1-R1 are resolved.)

## Real limits

- **This was a delta review.** I did not rerun the sweep, the 8x8/1if harness legs, the firmware campaigns, the hosted steps or the lane gates. Those rest on the author's published receipts, which I spot-checked, plus my own runs of the self-test, the regrade, the probes, the guard probe and the object identity.
- **I did not rebuild the eight images.** Their identity is the author's receipt. My object identity check covered `aecp.c` only, on host gcc.
- **The regrade proves the held-egress criterion only.** It reads logs. The other 8x8/1if criteria rest on round 3's `gate_r3` grade of the same images.
- **No CI job runs the self-test.** `egress_ledger.py --selftest` is a lane gate, as the sibling grader self-tests are. No workflow runs it.
- **Physical calibration was not run, and field skips are not hardware proof.** No manager source bank runs at this head, and none is claimed or inferred. No merge candidate result is claimed.

## Pending manager duties

- Publish this packet.
- Carry RES1-RES3 to the residue checklist.
- Re-sync this PR onto #902's final head after #902 merges, then build and validate the current-dev merge candidate: source base `7398ec0a`, live dev `6b66f66d`, with the builder and native banks and hosted/act acceptance. Any source change re-opens the lenses whose scope it touches.
- Track Mailbox.ARoundFillsWhatItsPassHasLeft's pre-existing 8x8/1if failure separately, as stated.

## Receipts and scripts (MANIFEST.sha256)

- **Scripts:** `ident_check.py`, `comment_scan.sh`, `probe_ledger.py`, `probe_enlarged.py`.
- **Receipts:** `receipts/egress_ledger_selftest.log`, `receipts/egress_ledger_round3_logs.txt`, `receipts/probe_enlarged.txt`, `receipts/probe_ledger_dirmode.txt`, `receipts/aecp_guard_probe.txt`, `receipts/aecp_object_identity.txt`, `receipts/sweep_identity_716a8ae7_6da0dc73.txt`, `receipts/comment_scan_7398ec0a_98c0b62b.txt`.

After my probes, the clone is at exact head with a clean index and worktree. The only generated file, a `__pycache__`, was removed. The six initialized submodule gitlinks match the tree, and `external` is uninitialized, as it was before.

R843-2 FINISHED
