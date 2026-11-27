[R957] NEGATIVE - exact head 3181a3ec372b6473175cc1c842ada8133a96b127

# R957-3: internal independent review of PR #993 (#977), rounds 11 to 11b (`25ff0632..3181a3ec`)

- Head `3181a3ec372b6473175cc1c842ada8133a96b127`, tree `da2f2b0635071acfcfe49efb6c9e2cb0450e85da`. This is a detached, clean clone, and it was restored and verified after the probes (`receipts/restore-check.txt`). The gitlinks are unchanged: lwSRP `e27b34c9`, tsn-c-stack `5a07d9b7`.
- Scope is narrow, as briefed. It covers the round-2 findings: internal 7226275798 (F1, S1, R1 to R3) and external 7226304210 (F1, R1 to R3). It also covers the `srp_binding.hpp` EOF fix that failed the merge candidate's builder. Code the delta does not touch keeps its prior lens verdict.
- Reading order: AGENTS.md, then #977's rulings and owner decisions, then the 8-commit delta, then the author-r11 packet at evidence commit `be39b0e1`. I read the prior review comments only after my own pass over the diff. I did not open the other reviewers' reports in the evidence tree (`977-r1/reviews/`).
- **Verdict: NEGATIVE.**
  - One MAJOR finding: the deliveries term's baseline understates the deferred work. Against a baseline that represents the passes without that work, the 8x8/1if load by the rule is 0.7806. That is over the 0.78 now being asked of the owner.
  - One MINOR finding: the "manager's decision" the term cites is not public.
  - Everything else in scope is closed.

## 1. The ceiling question, and the baseline I accept

- **At 0.78** (commit `9976b94f`, "owner decision pending"), the head's gates pass with the stated term. My runs give:
  - `load_grade.py --check`: PASS; `--selftest`: 32 of 32.
  - `flip_grade.py --check` at both points: PASS; `--selftest`: 628 of 628.
  - 8x8/1if load at the pin: 0.77864 with the term, 0.76614 without it, 0.77414 at the dearest-before cost.
  - 1x1/1if load: 0.53210 at the pin, against 0.70.
  - Receipts: `receipts/load_grade.py_--check.txt`, `receipts/flip_grade.py_*.txt`, `receipts/load_probe.txt`.
- **At 0.77, without `9976b94f`, the PR does not pass.** With the ceiling patched to 0.77 in memory, the flip check finds "8x8/1if: the load 0.779 at the pin is over the flip ceiling 0.77" (`receipts/load_probe.txt`). `9976b94f` is droppable alone: the next commit, `3181a3ec`, touches none of its files, and its reverse applies to the head (`receipts/droppable-check.txt`). The owner's answer decides 0.78. I judge everything else at 0.78.
- **Baseline.** I do not accept the dearest-before baseline (0.774). It is a lower bound: it subtracts the dearest pre-record pass, which is itself base work.
- I also do not accept the median of the 50 ms before the record as stated, for the reason in F1.
- I accept a median ordinary-pass baseline that represents the passes without the deferred work. The published receipts bound that at no higher than round 10d's 500 ms median of 13,249 cycles, which my round-2 F1 quoted.
- At that baseline the swap's share by the rule is 145 µs a sink. The term is 0.0145, and the 8x8/1if load is **0.78064**, over 0.78. Unruled, it is 0.77978.

## 2. Findings

### R957-3-F1 MAJOR (Conformance, RTL, Tests, Docs): `DELIVERY_US` at 8x8/1if is set against a pre-record median above the ordinary passes after the swap, and against a faithful baseline the load is over 0.78

**Location**
- `tb/verilator/ctrl_service_budget/load_grade.py:374-384`: `DELIVERY_US = {'1x1/1if': 190, '8x8/1if': 125}`. Its stated baseline is "the median base of the ordinary passes in the 50 ms before the record".
- `load_grade.py:9-13`: the premise.
- `docs/design/SPLIT_CONTROL_MEMORY.md:2548`.
- PR body, Status and the deliveries row.

**Authority**
- #977 acceptance 4: the owner bounds hold.
- R957-2-F1's required outcome (a): a cost "stated by the rule against a stated baseline", with the 8x8/1if load and flip checks passing with it. Otherwise outcome (b), the STOP of ruling 7212897415 item 5 and ruling 7210763364 item 6.
- The load model's own rule that no term is kept as a margin and every term has its source (`load_grade.py:19-20`).

**Evidence** (`scripts/baseline_probe.py`, `receipts/baseline_probe.txt`; both inputs are hash-verified packet receipts)
- *Round 10d's receipt* (`author-r10/receipts/r10d/meas/postswap-8x8-1if.txt`), answering-ports swap: against the median of the 500 ms before the record (13,249 cycles), 11 of the 40 passes after the record are over it, by 122,780 cycles in all. So the other 29 passes after the record have a polls base at or under 13,249.
- *Round 11's receipt* (`author-r11/receipts/meas/deliveries-8x8-1if.txt`), same record: against the median of the 50 ms before it (14,942), the excess is 104,157 cycles.
- The difference is exactly 11 × 1,693 cycles, where 1,693 is the step between the two medians. The same 11 passes carry the work in both windows. The whole drop from 0.0136 to 0.0125 comes from the baseline. The none arm shows the same pattern: 101,050 − 77,847 = 11 × 2,109.
- So the pre-record 50 ms median is at least 1,693 cycles above the ordinary passes that follow the swap's deliveries.
  - The deferred work is the window's base above what those passes would otherwise cost, which is the post-record ordinary base.
  - Against that base the excess is at least the 500 ms figure: 13,642 cycles a sink, 145 µs by the rule (`5 · ceil(c/100 · 1.05 / 5)`, the rule `deliv11.py` itself applies).
  - Load = 0.76614 + 145 · 3 · 9 / 270 / 1000 = **0.78064**.
- The 50 ms window is a new parameter in round 11. The previously stated median figure, 0.0136 (`SPLIT_CONTROL_MEMORY.md:2548` at `25ff0632`, quoted by R957-2-F1), was replaced without a note of the change or of its effect, in the documents or in the PR body.
- The gate's only floor for the cost is the dearest-before figure, which is the rejected baseline (`load_grade.py:696-697`, `load_deliveries.py:35-38`). So `load_grade --check` cannot refuse an understated `DELIVERY_US`.

**Impact**
- 8x8/1if passes the pending 0.78 by 0.0014 only on a baseline that understates the deferred work in the group that sets the figure.
- The owner is being asked about 0.78 with 0.77864. A faithful baseline gives at least 0.7806, so even an approved 0.78 would not hold.
- 1x1/1if is not at risk: 0.532 against 0.70.

**Required outcome.** Both of these, recorded publicly before merge:
- State `DELIVERY_US` against a baseline that represents passes without the deferred work, with its window and the reason for it in `load_grade.py` and section 13. For example: the ordinary passes after the delivery window, or the lower of the pre-record medians. Then re-derive the 8x8/1if load.
- If that load is over the ceiling the owner decides, STOP to the owner with both figures (0.7806 by the rule, 0.7798 unruled), as the rulings require.

The gate's floor for `DELIVERY_US` must be the accepted baseline's figure, not the dearest-before one.

**Verification**
- The deliveries receipt re-run with the stated baseline, its per-record excess shown.
- `load_grade.py --check` and `flip_grade.py --check --point 8x8/1if` at the decided ceiling.
- A `load_deliveries.py` control that refuses a cost under the accepted figure.

### R957-3-F2 MINOR (Conformance, Docs): the "manager's decision of 2026-11-27 on the deferred deliveries" that the term rests on is not public

**Location**
- `docs/design/SPLIT_CONTROL_MEMORY.md:2561`: links "the manager's decision of 2026-11-27 on #977's deferred deliveries" to PR comment 7226275798. That is my round-2 NEGATIVE review, whose required outcome offered options (a) to (c). It is not a decision.
- The same decision is cited without a link at:
  - `tb/verilator/ctrl_service_budget/load_grade.py:13`, `:374`;
  - `load_deliveries.py:3-4`;
  - `flip_grade.py:66-67`;
  - `docs/reference/FR_NFR.md:427`.

**Authority**
- AGENTS.md section 2: a cold reviewer must reconstruct the task from GitHub and the repository alone.
- R957-2-F1: the outcome must be "recorded publicly before merge"; "the executor may not choose between (a) to (c) privately".

**Evidence**
- #977's last comment is the owner decision 7217388999 (2026-11-27 11:42Z). PR #993's comments after the round-2 reviews are only the two review-start notices (public API listings).
- REVIEW-READY.md and the PR body say "the manager decided option (a)", with no link.

**Impact**
- The authority for a new load term, and for its baseline (which decides pass or fail at 0.78, F1), cannot be reconstructed publicly.
- The design document points readers to a review as if it were the decision.

**Required outcome**
- The manager publishes the decision on #977, naming the option and the baseline with its window.
- The six sites cite and link it. Until then, they cite the finding as a finding.

**Verification**
- Each link resolves to a decision comment that names option (a) and the baseline.

### Residue (wording only; does not unclean a lens; for the residue checklist)

- **R957-3-R1** — `tb/verilator/ctrl_service_budget/load_grade.py:378`: "(tools' deliv11.py)" names a script that is not in the tree, under a round-numbered name. Exact fix: "(measured by the script published with #977's review evidence)", or describe the method without the tool's name.
- **R957-3-R2** — `tb/verilator/ctrl_service_budget/README.md:244`: "A pass's own cost is no source and is reported beside the load." now omits the module's one exception. Exact fix: append ", but for the binding changes and loss completions a registering record defers into later passes, the `deliveries` term (`load_grade.py`; its controls in `load_deliveries.py`)".
- **R957-3-R3** — The live PR body, Status: "[internal internal review ](…)" and "[external external review ](…)" (a label scrub left duplicated words and a trailing space). Exact fix: "[the internal review](…7226275798) and [the external review](…7226304210)".
- **R957-3-R4** (packet only)
  - `author-r11/receipts/INDEX.md` lists `fwgate-shard{1,2,3}-9976b94f.txt.gz` and `harness-run.py_--self-test-9976b94f.txt.gz`, which are published as `.txt`. This repeats the packet part of R957-2-R3.
  - REVIEW-READY.md and HANDOFF-r11.md say a dated supersession note was appended to round 10's index. The published `author-r10/receipts/INDEX.md` carries none.
  - Exact fix: regenerate the index from the published files, and publish the note or drop the claim.

### Suggestion

- **R957-3-S1 (Tests)**: D8 and D9's three plants are planted only at 1x1/2if, by the campaign's design (the gate receipts show them caught there). A one-line note in `srp_deliver_mutants.py`'s docstring saying where the unprefixed plants run would save a cold reader the search. Optional.

## 3. Prior findings at this head

| Finding | Status | Evidence at `3181a3ec` |
|---|---|---|
| R957-2-F1 MAJOR | **Retained**, narrowed to R957-3-F1 and F2 | The term exists, is sourced, and counts V a record at the registration rate (`load_grade.py:610-612`). Its four controls are refused (`load_deliveries.py`; 32 of 32). It passes only at the pending 0.78, fails at 0.77 (`receipts/load_probe.txt`), rests on an understated baseline (F1), and its decision is not public (F2). |
| R957-2-S1 SUGGESTION | **Resolved** | `srp_binding.hpp:519-578` (D8, D9, D10) against `ctrl_app_srp.c:136-209`. Plants at `srp_deliver_mutants.py:61-76`. The gate receipts (`fwgate-shard*-9976b94f`) catch from-the-first, never-advanced and always-first at 1x1/2if, and loss-in-a-record's-pass at 1x1/1if and 8x8/1if. I read each test against `deliver`: each assertion fails under its plant. |
| R957-2-R1 RESIDUE | **Closed** | No "round 9's STOP" and no undated "2026-11-27, item N" citation remain in sw/, tb/ or docs/ (`receipts/prior-residue-check.txt`). |
| R957-2-R2 RESIDUE | **Closed** | `ctrl_loop.h:395-397`, `SPLIT_CONTROL_MEMORY.md:3095` and `FR_NFR.md:454` read "79.49 ms … (79.48 at the ruling's 415 us SETTLE)". `flip_grade --check --point 8x8/1if` prints 79.49. |
| R957-2-R3 RESIDUE | PR body **closed**; packet part **retained** as R957-3-R4 | The PR body now reads "289 + 2 pairs: 285 exit 0, and the 4 single srp-kept and srp-bound runs are refused by `kept_grade`'s pairing and pass as the 2 pairs" (`receipts/pr-body-check.txt`). |
| R958-2-F1 MINOR | **Closed** | `SPLIT_CONTROL_MEMORY.md:172` reads 65.5 and 61.5, matching `sw/litex/ctrl_memory_ledger.py:90` (65.5 past 65.0) and `:99` (61.5 past 61.0), with the table at `:140` (61.0). |
| R958-2-R1 RESIDUE | **Closed** | As for R957-2-R1. The B25, B26 and B27 prefixes are gone from `test_plat_boot.cpp:1353,1372,1410`. |
| R958-2-R2 RESIDUE | **Closed** | The PR body's Pins row reads "used by the default-option shapes; the published ELF comparisons cover those images too". |
| R958-2-R3 RESIDUE | Current prose **closed**; the packet's note **not found** (R957-3-R4) | `SPLIT_CONTROL_MEMORY.md:2548,3095` and `ctrl_loop.h:398` cite "approved by the owner's decision of 2026-11-27" (7217388999). The PR body names the reviewers. |
| Builder step 43, `srp_binding.hpp` EOF | **Closed** | `git diff --check` is clean at both bases: merge base `71bad8c0` and dev-soft-core `0b594023`. At `9976b94f` it reported "srp_binding.hpp:580: new blank line at EOF". `9976b94f..3181a3ec` removes that one line only (`receipts/whitespace-check.txt`). |

## 4. Delta checks (own pass)

- **Product bytes.**
  - The delta's product sources differ only in comments. A token comparison with comments and whitespace stripped gives SAME for `ctrl_app.h`, `ctrl_app_srp.c`, `ctrl_loop.h`, `srp_mbx.c`, `srp_mbx.h` and the hot list's non-comment lines (`receipts/product-comment-only.txt`).
  - No `__LINE__`, `__FILE__` or `__COUNTER__` appears in product ctrl code. The one `assert` (`srp_mbx.c:80`) sits above both changed hunks.
  - The author's identity receipt (`r11b/elf-identity-3181a3ec.txt`) lists 80 hashes at each head. Its two lists match path for path (30 distinct images), and it reports "identical: 80 of 80".
  - So round 10d's measurement and routes stand. I did not rebuild ELFs.
- **The term's formula.** It is `DELIVERY_US · 3 · V / (1.5 · 180 ms)`. At 8x8/1if (V 9) it gives 0.01250, and at 1x1/1if (V 4) 0.00844, as reproduced by `scripts/load_probe.py`. It sums with the other terms in the flip check's column. `delivery_findings` and its four controls bite as named (code read; selftest 32 of 32).
- **D8 to D10** (`srp_binding.hpp:519-578`):
  - D8 re-latches sink 0's loss before each delivery and requires sink n-1's loss within n deliveries.
  - D9 sets `srp_lost_last` with both owed and requires the binding change, with the loss left owed.
  - D10 checks that a record's pass leaves `srp_lost_last` false and makes no change, and that the next delivery completes the loss first.
  - Each fails under its plant (`srp_deliver_mutants.py:61-76`); the gate receipts at `9976b94f` show each caught. The head differs from that commit by the EOF line only.
- **Comment rule over the added lines** (`receipts/comment-rule-scan.txt`):
  - No lane, round, reviewer or comment-ID label was added.
  - "the manager's decision" is a role, not a label; its problem is F2.
  - "tools' deliv11.py" is R957-3-R1.
- **Packet.** The evidence commit `be39b0e1` is unsigned. All 47 author-r11 files match `MANIFEST.json`'s `published_sha256` (`packet-manifest-check.txt`).
- **Hosted evidence at the exact head.** No check runs, no statuses and no workflow runs (`receipts/hosted-checks-3181a3ec.txt`; the PR is a draft). Nothing hosted was executed at this head.

## 5. Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | #977 acceptance 4; rulings 7212897415 item 5 and 7210763364 item 6; owner decisions 7213594113 and 7217388999; R957-2-F1's required outcome; `load_grade.py:9-13,374-384,607-612,686-698`; `flip_grade.py:62-68`; the round 10d and round 11 deliveries receipts; `receipts/baseline_probe.txt`, `load_probe.txt` | R957-3 | `3181a3ec372b6473175cc1c842ada8133a96b127` |
| RTL | UNCLEAN (F1) | `ctrl_app_srp.c:101-210` (`deliver`, unchanged but for comments); `receipts/product-comment-only.txt`; `r11b/elf-identity-3181a3ec.txt` (80 of 80); the deferred-work CPU cost as the load model states it (F1) | R957-3 | `3181a3ec372b6473175cc1c842ada8133a96b127` |
| Robustness | CLEAN | `srp_binding.hpp:519-578` (a repeated loss re-latched each delivery, both owed after a loss, a record's pass); `ctrl_app_srp.c:136-209`; `srp_deliver_mutants.py:61-76`; `fwgate-shard*-9976b94f.txt` (each plant caught); `load_deliveries.py:16-39` (term absent, halved, at none, under its floor); no product behaviour changed (ELF identity) | R957-3 | `3181a3ec372b6473175cc1c842ada8133a96b127` |
| Tests | UNCLEAN (F1) | D8 to D10 and their four plants (clean as such); `load_deliveries.py`, `load_grade.py:686-698` (its floor is the rejected baseline, F1); `flip_grade.py:196-201,422` (0.780 within, 0.781 over); my `load_grade`/`flip_grade` runs (32/32, 628/628, PASS); `receipts/whitespace-check.txt` | R957-3 | `3181a3ec372b6473175cc1c842ada8133a96b127` |
| Docs | UNCLEAN (F1, F2; residue R1 to R4 does not unclean it) | `SPLIT_CONTROL_MEMORY.md:172,2548,2561,2577-2578,3095`; `FR_NFR.md:427,454`; `ctrl_loop.h:345-350,392-399`; `srp/README.md:149-153`; `tb/verilator/ctrl_service_budget/README.md:244`; the live PR body (`receipts/pr-body-check.txt`); author-r11 REVIEW-READY, HANDOFF and INDEX | R957-3 | `3181a3ec372b6473175cc1c842ada8133a96b127` |

## 6. Real limits

- I did not re-derive `DELIVERY_US` from raw harness logs, because they are not published. F1 rests on the two published, hash-verified measurement receipts, and its inference is arithmetic on them: the 11-pass match is exact.
- The post-record ordinary base could be lower than 13,249. If so, the true load is higher than 0.78064. F1 states a lower bound.
- I rebuilt no ELF and ran no firmware gate, mutant campaign or builder at this head. Product identity rests on the comment-only token comparison and the author's 80/80 receipt.
- The mutant and gate receipts are at `9976b94f`, which differs from the head by one blank line at EOF in a test file.
- The scoped Verilator was not needed and was not used.
- No manager source bank ran at this head, and I infer none. The current-dev merge candidate (builder and native banks; source base dev-soft-core, live dev `e275d795`) is the manager's.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- No hosted job ran at this head.

## 7. Pending manager duties

- Bring F1 to a public outcome: a restated baseline and load, or the STOP to the owner with 0.7806 (by the rule) beside 0.77864.
- Publish the deliveries decision (F2) and have the six sites link it.
- Record the owner's answer on 0.78. If refused, revert `9976b94f` (it reverts cleanly), and 8x8/1if waits for #1025.
- Carry R957-3-R1 to R4 to the residue checklist.
- Hosted and act acceptance on the exact head once the PR is ready, and the current-dev candidate's builder and native banks at the merge turn.

R957-3 FINISHED
