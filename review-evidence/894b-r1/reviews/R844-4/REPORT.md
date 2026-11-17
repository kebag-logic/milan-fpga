[R844] NEGATIVE - exact head 8883d4998496c6d2e234143b43807731e8851b63

External independent review R844-4, issue #894 / PR #914. Tree `a169a601df764715eec1b404b16da3df73217142`. One MAJOR and one MINOR finding remain open. All five lenses were applied and are unclean. No approval or merge authorization is given.

Scope and authority

The review reconstructed AGENTS.md, CONTRIBUTING.md, docs/README.md, the frozen issue contract and public decisions, requirements/interface authorities, the requested `7398ec0aeea468d92ff642a03a06e291a0cd58d1..8883d4998496c6d2e234143b43807731e8851b63` diff/history, then public execution evidence. An independent verdict and five-lens ledger were written before prior public review findings were read. Prior findings were then reconciled at their causes.

The handoff's five-file, no-image-change description applies to `af2c4d7a..d539f162`, not this exact head. Later public scope includes #901's composition, #930's Listener copies and measured costs, and the two retargeted Listener plants. Those dependent changes were reviewed too; no ancestor verdict was silently carried over them. Unchanged code retains its prior verdict subject to changed dependencies. See `receipts/delta-history.txt`.

Authorities include [the 8x8/1if scope](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867393730), [measured gate/recorded misses](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6871343905), [ledger derivation](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6892938049), [composition](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6914952893), [Listener-copy scope](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6918853411), [latest ledger adjustment](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6934688411), [plant decision](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6938589932), and [exact-head readiness](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6939551029). FR_NFR 3.4.1 and SPLIT_CONTROL_MEMORY section 13 distinguish the measured gate from every-source rows reported under #872. This review preserves that distinction.

R844-4-F1 — MAJOR — Conformance, RTL, Robustness, Tests, Docs

Artifact: `sw/firmware/ctrl/loop/ctrl_loop.h:355`; `sw/firmware/ctrl/srp/srp_mbx.c:30-36`; `tb/verilator/ctrl_service_budget/flip_grade.py:404,420`; `rows_tiers.py:557`; `sw/firmware/ctrl/srp/README.md:225-229`.

Authority/evidence: `CTRL_LOOP_TX_MS` is expressly the built design's every-source transmit row rounded up. Firmware uses it to cover the Leave's latest departure when computing `SRP_REDECLARE_CS`. The source contract cites IEEE 802.1Q-2018 35.2.2.8 and two configured 1000 cs LeaveAllTime periods after the Leave. #901's composition set 8x8/1if to 70 ms for its then 69.84 ms row. Subsequent SRP cost changes produce **74.26 ms**, also present in the author's published current row receipt, but firmware still states **70 ms**.

`scripts/transmit_contract_probe.py` reconstructs 8x8/1if inputs using the published row recipe and supplies them to the existing `tx_statements` checker. It refuses: `8x8/1if: CTRL_LOOP_TX_MS states 70 ms, under the built design's tx row 74.26 ms`. The independently generated row table equals the published current table byte for byte. This is an explicit shape-input probe; it does not claim that the unmodified default CLI already checks this shape.

Impact: the current hold-off is 2026 cs from the Leave request. Subtracting configured JoinTime (190 ms) and the latest modeled transmit delay (74.26 ms) leaves **19995.74 ms**, below the documented 20000 ms floor. Covering the current model needs at least 75 ms, making the dependent hold-off 2027 cs. This establishes an invalid timing envelope, **not an observed early wire frame**. Reporting general model rows under #872 does not waive correctness of a bound actively used by firmware.

The test gap matters: `flip_grade.py` removes reported shapes from `rowed`, then checks transmit statements only through that set. Default `rows_tiers` points also omit 8x8/1if. Consequently the 8x8/1if flip check passes despite the understated firmware bound. The Talker timing test's `kHoldOffMs` and associated plants derive from the same constant (`sw/firmware/ctrl/test/srp_talker.cpp:51-55`, `srp_talker_mutants.py:118-125`); they check the implemented timer without independently validating its model envelope.

Required outcome: make the statement and dependent hold-off cover the final model; check this statement at 8x8/1if independently of whether its general rows are reported; add a named understatement control at that shape. Refresh affected images/measurement receipts and comments/docs still saying 69.84/70/2026, including `ctrl_loop.h:327,467` and `SPLIT_CONTROL_MEMORY.md:2814`. Preserve the agreed measured-gate and #872 scope.

Verification: `receipts/transmit-contract.txt`, `current-8x8-rows.txt`, `published-8x8-rows.txt`, and the passing `flip-8x8.log` reproduce the contradiction. Re-review must see a passing independent envelope check, the new understatement control refused by name, and resulting image evidence.

R844-4-F2 — MINOR — Conformance, Docs

Artifact: `docs/design/SPLIT_CONTROL_MEMORY.md:2765,2808,2832-2835`; `docs/design/MAILBOX_SPLIT.md:390`.

Authority/evidence: section 13 must attribute the head's gate and derived figures to the corresponding image/receipt, as required by FR_NFR 3.4.1 and R843-3-F1's correction. The new Listener-copy paragraph gives current results, but a later paragraph still says **“as the head derives them”** while citing `rows-8x8-1if-af2c4d7a.txt`:

| Claim presented as current | Stated | Current receipt/model |
|---|---:|---:|
| R4 | 19.82 ms, within 20 ms | 21.39 ms, over 20 ms |
| R5 | 126.36 ms | 136.64 ms |
| Last queued notice | 325.90 ms | 387.95 ms |
| tx | 67.24 ms | 74.26 ms |
| txL | 134.96 ms | 159.82 ms |
| Largest-command load | 0.969 “at the head” | 1.034 |

Line 2765 also calls round 5's measurement “on the head's image” (SRP 32047 cycles), and line 2808 attributes 2453084 retry rounds and last notice 26.636 ms to “the head's image.” Current measurement instead has SRP 32936 cycles, 2403014 rounds and last notice 25.625 ms. The adjacent old share-pass result needs an explicit historical scope if retained. MAILBOX_SPLIT separately states a 0.95 ms slice at 1x1/1if while this composed head's `ctrl_loop.h:339` states 900 us.

Impact: conflicting current-head measurements and a false within-bound conclusion. These are figure and conformance claims, not wording-only residue. This finding does not require the agreed reported R4 debt to pass 20 ms.

Required outcome: replace current claims with the final receipt's complete figures/conclusions, or explicitly scope the entire old blocks to their historical image, including load/share and within-bound conclusions. Link current receipts for current rows. Change the current 1x1/1if slice statement to **0.90 ms**.

Verification: compare labeled rows, image identities and conclusions, not number substrings found anywhere in a section. `current-8x8-rows.txt` and `published-8x8-rows.txt` agree; current measurement receipts and the shape header establish the other corrections. This is recurrence of R843-3-F1's cause after the valid r7 fix.

Retained residue and suggestions

- **R843-4-R1 — RESIDUE — Docs — `docs/reference/FR_NFR.md:393`.** Retain the historical-qualifier residue: “as on each image before it” unnecessarily generalizes the current result. Exact fix, preserving the prior report's correction: replace that blanket historical qualifier with “and as on round 3's image, the one whose THE RETRY's round costs are its shape's ([#894's round 3 ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6878014227)), with its own load figures there, each holds:”. Keep the preceding current-image identification and the separately scoped composition figures. Impact is the prior wording ambiguity; the current measured verdict and 0.735 figure stay unchanged. Verify that each historical image has its own figures and the blanket “each image before it” attribution is gone.
- **R843-2-S2 / R843-3-S2 — SUGGESTION — RTL, Robustness — `sw/firmware/ctrl/test/aecp_arms.py` debug arm and `aecp_wire.py` contract setup.** Retain the precise prior suggestion: at two interfaces these still compile the core against the tracked one-interface contract. Their comments explain why, and neither measures round costs. Optional outcome: give them their interface contract too, or assert that they measure no round cost. Verify the generated contract or explicit assertion and the relevant arm receipts. This remains optional, with no present timing defect asserted.
- **R843-4-S1 — SUGGESTION — Tests, Docs — `author-r7/scripts/f1_check.py`, public archive.** Its substring checks can accept a figure under the wrong row/image. Retain the structured row/image comparison suggestion; verify a swapped figure or wrong image attribution is refused. This optional checker improvement is separate from mandatory correction of F2's actual false claims.

Prior findings reconciliation

Public references: [R844-1](https://github.com/kebag-logic/milan-fpga/pull/914#issuecomment-6885381555), [R843-1](https://github.com/kebag-logic/milan-fpga/pull/914#issuecomment-6885564795), [R843-2](https://github.com/kebag-logic/milan-fpga/pull/914#issuecomment-6888161058), [R844-2](https://github.com/kebag-logic/milan-fpga/pull/914#issuecomment-6888161829), [R844-3](https://github.com/kebag-logic/milan-fpga/pull/914#issuecomment-6895790018), [R843-3](https://github.com/kebag-logic/milan-fpga/pull/914#issuecomment-6895954911), [R843-4](https://github.com/kebag-logic/milan-fpga/pull/914#issuecomment-6898124949). These were read after the independent verdict/ledger was recorded.

| Prior item | Exact-head disposition and evidence |
|---|---|
| R844-1-F1: held-egress growth unguarded | Resolved. `egress_ledger.py` derives ruled limits and rejects larger/new misses. Published current log passes; seven independent +0.001 ms plants each refuse their row (`ledger-boundary.txt`). Later adjustments have explicit public rulings. |
| R844-1-R1 / R843-1-R1: source-comment labels | Resolved for reviewed additions: no new prohibited label in added source comments (`source-comment-scan.txt`). Existing debt stays #746. |
| R843-1-S1: guard and arms contract | Addressed within the stated limit: `aecp.h:67` diagnoses an explicitly declared charging unit missing its table; `aecp_arms.py` prepares the two-interface core contract and `test_aecp.cpp` asserts interface agreement. An undeclared future charging unit retains the ordinary compiler-error limitation. Debug/wire remainder is S2 above. |
| R843-2-S1: directory-summary refusal | Resolved at its cause: `egress_ledger.py:157,176` reads run-level refusals from results.json, with missing-summary/refused-run controls at :400-407 and a reader-bypass mutant at :438. Local self-test passes. |
| R843-2-S2 / R843-3-S2 | Optional coverage retained above. |
| R843-2-S3: evidence digests | Current publication checked: all 1233 extracted author evidence entries (excluding review-report paths) match published SHA256 values. This proves content integrity, not signer authentication. |
| R843-2-RES1 / RES2 / RES3 and R844-2-R1 / R2 | Earlier ledger-rule wording, assertion scope, “most units” include wording and carried-receipt issues are corrected in current source/public evidence. New stale current-image claims are separately retained as F2. |
| R844-3-R1: point name | Resolved: `record_classes.point_name` names #894's 8x8/1if shape rather than calling it “reported.” |
| R844-3-R2 / R843-3-R1: mailbox slice qualifier | Corrected to 1x1/1if with THE SHAPES link. Now-stale numerical slice is F2; this dependency is not banked clean. |
| R844-3-R3: old load/rows | Old round-3 block is labeled historical. Later contradictory current-image claims remain F2. |
| R844-3-R4: reversed survey comparison | Corrected in the current public PR body. |
| R843-3-F1: current-image figures | r7's receipt supports 36 figure checks plus historical qualifiers at d539f162; af2c4d7a's document fails 37 checks. Fix valid then; later composition/cost changes reintroduce the cause as F2. |
| R843-3-F2: mixed-point completeness | Resolved. Head probe refuses missing 1x1/1if arm A and accepted SET_CONFIGURATION by name (two findings). Replacing only the module with af2c4d7a's yields zero. New plant is present; self-test 14/14. See both `mixed-*.txt` receipts. |
| R843-3-R2: FR_NFR ledger link | Resolved: section 3.4.1 cites section 13 and distinguishes recorded misses from passes. |
| R843-3-S1: retained retry explanation | Addressed by current apply measurement/cost explanation (`poll_grade.py:111-123`, section 13): 32618 cycles at 8x8/1if gives 345 us; 1x1/1if stays 280 us against 23144 cycles. No new policy inferred. |
| R843-4-R1 / S1 | Retained above. |

Evidence applied by lens

- **Conformance:** compared issue measured-row/load/slice/platform rules and FR_NFR 3.4.1 with exact-head constants, published image/measurement receipts and section 13. Current recorded 8x8/1if load is 0.735 and measured CPU rows fit. General every-source misses remain #872 debt. The separate firmware hold-off dependency fails F1; false current documentation fails F2.
- **RTL and architecture:** no HDL delta requires a new RTL implementation review. Examined changed firmware integration: `srp_mbx.c:178` Listener indication, `:396` observer presence updates, `:416` deferred walk, initialization/reset and publication against pinned lwSRP registrar/indication ordering. Compared copies with the retained reference walk and differential fixture. No additional callback/reset/interface defect found. F1 affects a real firmware timing dependency.
- **Robustness:** inspected `srp_listeners.cpp` differential sequences (two seeds, 3000 records each), registration/Leave/reset/refusal paths, held Talker/LeaveAll composition, incomplete mixed-shape passes, and seven ledger-boundary refusals. Existing constant-derived timer expectations do not cover F1's final model envelope.
- **Tests:** inspected `srp_listener_mutants.py`, `srp_listeners.cpp`, and retargeted `srp_mutants.py:95,227` plants at the Listener indication; checked current published SRP/shard evidence. Focused grader self-tests and falsification probes are below. Restored completeness detects its intended old defect; the independent 8x8/1if transmit-statement control is missing (F1).
- **Docs:** compared MAILBOX_SPLIT, SPLIT_CONTROL_MEMORY section 13, FR_NFR 3.4.1, SRP/harness README, current PR text and public evidence attribution. Current-image figures must agree even where history is retained. F1/F2 remain; residue and optional items are listed above.

Execution and evidence

The [public archive](https://github.com/kebag-logic/milan-fpga/tree/88f4b944a0be6b418cab966e9828ea2bcc3716f5/review-evidence/894b-r1) was read at its full commit. All 1233 extracted author evidence entries (excluding review-report paths) match manifest SHA256 values. No private author material was used. The archive commit has no Git signature and no separate signature was supplied in the author paths: **signer authentication is not established**. This report claims hash/content verification only.

r7 evidence includes 45 lane-gate results (four expected negative-control exit-1 results), successful harness self-test, 61 executed documentation steps, and the round-5 regrade/figure receipt matching d539f162's image/statements. The eight-image af2c4d7a/d539f162 hash identity applies to that stage only; it cannot carry the old image over #901/#930.

At this head all eight published ELF/loadable-byte hash pairs equal the measured `46cf2a7d` image's pairs. Current measurement covers 117 groups/1762 instances at 8x8/1if and 118/1290 at 1x1/1if. Spot-checks include record/apply/reclaim costs, joins, last queued notice, and the held-egress row changed by explicit phase ruling. No local image rebuild is claimed.

r11's public workflow receipt has 83 executed steps: 61 documentation steps successful, and 22 rtl-fast steps including one failed SRP plant step. That failed attempt is not relabeled green; r12 supplies the later successful retargeted campaign. Six published shard receipts total **37 suites and 966909 checks**, no failed suites. The final SRP campaign has no escaped plant; its nested `[ok]` lines are not a count of distinct campaign plants. The public twin/twin-plant base mismatch belongs to #935 under the manager's explicit disposition, not a new source finding here.

Independent execution:

- `record_classes.py --selftest`: 14/14; mixed-point probe refuses at head and accepts the bad pass with the old module.
- `shape_costs.py --check --selftest`, `flip_grade.py --selftest` (612 controls), both 1x1/1if and 8x8/1if flip checks: exit 0.
- `rows_tiers.py --selftest` (1033 controls), load check/self-test (28 controls), egress ledger self-test (15 controls): exit 0.
- Seven held-egress boundary plants: baseline passes; all larger rows refuse by name.
- Published row recipe rerun: byte-identical current output; transmit-envelope probe exposes F1.
- Harness self-test: **exit 0, zero failures, all 259 mutants caught** (`harness-corrected.log`, `harness-corrected.rc`). Initial `--selftest` was an invocation error (exit 2); corrected command is `run.py --self-test`. Both attempts are retained transparently.

Portable scripts and raw receipts are listed in MANIFEST.sha256; REPRODUCE.md documents commands and probe scope. No source fixes, commits, pushes, GitHub writes, heavyweight banks or hardware operations were performed.

Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — F1, F2 | #894 decisions; FR_NFR 3.4.1; ctrl_loop.h; srp_mbx.c hold-off; section 13; current row/measurement receipts | R844-4 | 8883d4998496c6d2e234143b43807731e8851b63 |
| RTL | UNCLEAN — F1 | srp_mbx.c indication/observer/reset/hold-off; pinned lwSRP registrar ordering; ctrl_loop.h/c shape timing | R844-4 | 8883d4998496c6d2e234143b43807731e8851b63 |
| Robustness | UNCLEAN — F1 | srp_listeners.cpp; Talker hold-off tests; mixed-point and ledger-boundary probes | R844-4 | 8883d4998496c6d2e234143b43807731e8851b63 |
| Tests | UNCLEAN — F1 | srp_listener_mutants.py; srp_mutants.py; record_classes controls; rows/flip/shape/load/ledger checks; r11/r12 receipts | R844-4 | 8883d4998496c6d2e234143b43807731e8851b63 |
| Docs | UNCLEAN — F1, F2 | MAILBOX_SPLIT; SPLIT_CONTROL_MEMORY section 13; FR_NFR 3.4.1; SRP/harness README; PR/evidence attribution | R844-4 | 8883d4998496c6d2e234143b43807731e8851b63 |

Limits and manager duties

Fixes and independent re-review of affected lenses are required. Ancestor coverage is not banked over changed dependencies. Reported #872 row debt, #902's subsequent comments/docs and #901's already-composed shape-keyed bounds are not new findings.

Source-head execution is the author's published evidence. **No manager source bank was run or inferred.** Hosted/act acceptance remains the manager's; this review did not run act or treat skipped contexts as executed jobs. The manager must validate the final current-dev merge candidate, publish builder/native-bank and mandatory hosted receipts, reconcile any other in-flight review, obtain required approvals, and perform authorized merge/post-merge containment. Source base `7398ec0aeea468d92ff642a03a06e291a0cd58d1` and the handoff's live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a` differ; the actual live tip must be checked at merge time.

Physical calibration is **NOT RUN**. Field skips and model/simulated timing are not hardware proof. Image equality here compares published receipts, not independently rebuilt binaries. Parent tracked blob bytes/modes/index and initialized required submodule gitlinks are checked in `receipts/checkout-integrity.txt`; the uninitialized external gitlink is disclosed and supplies no runtime evidence.

R844-4 FINISHED
