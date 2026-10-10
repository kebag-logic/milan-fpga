[R570] POSITIVE - exact head d96b4a8471028d3dfd370ce61dbe05ca9957320a

Round R570-2, internal cleared-context review of issue #621 / PR #707.
Head `d96b4a8471028d3dfd370ce61dbe05ca9957320a`, tree `19060afdf9e0e8f8c10f8adba9393922028211a4`.
Delta reviewed: `e0ee38f9..d96b4a84`, four linear one-line commits (`7ad00dbc`, `47b9b7e8`, `167798a0`, `d96b4a84`). The donor gitlink `7dda9c3b` is unchanged, and so are protocol-processor `2ad2f845` and verilog-axis `48ff7a7e`.

Verdict basis: no BLOCKER, MAJOR or MINOR is open at this head. Every R570-1 and R571-1 finding is resolved at this head (table below). This round adds one SUGGESTION. All five lenses were applied, and all five are clean.

## Reconstruction (public state only)

- AGENTS.md, CONTRIBUTING.md and docs/README.md.
- Issue #621 body; assignment 6084306147 and correction 6084315762; rulings 6087415319, 6087498843, 6087655217 and 6088189432, and the final receipt ruling 6089776382; round 2 assignment 6095695340; REVIEW READY 6096109824.
- PR #707 body at this head (`receipts/pr707_body_snapshot.txt`), the PR comments, `git diff e0ee38f9..d96b4a84` and the `5603c353..d96b4a84` stat.
- Public evidence tree `02d43fb7…/review-evidence/621-r1` (the author's round 1 evidence).
- I read the prior review reports (the R570-1 archive in `origin/621-review-evidence` and the R571-1 PR comment) only after the independent pass. Its draft verdict and ledger were already written by then.

## Findings

### S1 - SUGGESTION - Conformance, Docs - `docs/design/GPTP_PLANE.md:128-130`, `tb/verilator/gptp_plane/sim_phc_step.cpp:325-357` - the allowedLostResponses reading is recorded only in the PR body

- Authority/evidence:
  - The new arm pins the donor's existing threshold (`gptp-processor/hdl/ucode/gen_gptp_ucode.py:1491`, `CMP … LOST_N_C + 1`): asCapable falls when the fourth consecutive request is judged lost.
  - The PR body (Known limitations) and REVIEW READY 6096109824 give two readings. The IEEE 802.1AS-2020 11.2.13.4 definition ("above which") gives the fourth. The RESET state of Figure 11-9, read literally, gives the fifth.
  - Round 2 assignment 6095695340 fixes "the fourth" as the acceptance, so the lane follows a recorded decision.
  - The durable design page states the fourth and does not mention the other reading.
- Impact: none on this PR. A future reader of the design page cannot see that the threshold is a reading choice.
- Suggested outcome: a follow-up issue settles the reading, or the design page records it. The donor threshold predates this lane, which does not change it.
- No lens effect (SUGGESTION).

### Prior findings at this head

| ID | Severity | State at this head | Evidence |
|---|---|---|---|
| R570-1-F1 = R571-1-F1 | BLOCKER / MAJOR | RESOLVED | `scripts/measure_test_evidence_readers.py:104-110` adds a disposition for `tb/verilator/gptp_plane/phc_step.py`, and it matches the driver. The driver reads `gen_gptp_ucode.py` and writes five named plants into scratch copies. Each plant must fail its named runtime check, and the clean image must pass. Expected values come from the peer model and the link constants. `measure_test_evidence.py --check` exits 0 (`0 <= 0 unexplained`), and `--selftest` exits 0 (105/105). At this exact head, hosted `docs-check` job 114182327965 ran all 55 steps with `success` and skipped none. That includes step 37, "Test-evidence ratchet", and steps 38-51 (`receipts/hosted_docs_check_steps.txt`). The PR body names the gate. |
| R570-1-F2 | MINOR | RESOLVED | `production_spec` (`scripts/check_nvm_capture.py:55-62`) forces `mutation='none'` and passes only the named scenario fields. The grading call at `:91` uses it. The control `opt_out_control` (`:131-159`) runs before every verdict. The gate exits 0. Each of `--mutation bytes/records/clock/ignore-off-timing/receipt-opt-out` exits 1 for its named reason. R570-1's `probe_receipt_mutation_key.py` (sha256 `0c5c1b03…`) is byte-identical to the archived copy. Its plain plant is refused while the probe builds it. Its `mutation: byte-only` plant reports `REFUSED: worst measured copy exceeds half the 49 ms hold floor`. Reviewer probe `scripts/probe_receipt_guard.py` plants an over-bound arm whose `mutation` field is byte-only, skip-copy, no-traffic, an arbitrary value, or absent. The unplanted gate refuses every one. The probe also removes the guard in three ways: grading the raw arm at the call site, a spec that keeps the arm's mutation, and a spec that copies the whole arm. Each removal makes the gate's own control fail with `receipt arm escaped the production timing bound`. |
| R570-1-F3 = R571-1-F3 | MINOR | RESOLVED | `scripts/compare_page_receipt.py` makes 44 comparisons of section 18 (`SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1619-1667`) and limits item 6 (`:1809-1820`) against `measurements.json`, and all are EQUAL. Identities: the date, the ruling, the firmware hash, measured commit `034e2e30` and tree `a5d1a1b0`, which equals `git rev-parse 034e2e30^{tree}`. Protocol pin `2ad2f845` and gPTP pin `7dda9c3b` equal the gitlinks of `034e2e30`. Figures: worst 8x8 13.86318 ms, 3.5345x, margin 10.63682 ms; 1x1 3.96728 ms / 12.3510x. All six table rows are recomputed from the receipt rows, along with the census and the 96 captures. None of `a2f17342`, `c28595df`, `b2db3a97`, 13.86484, 3.5341x, 10.63516, 13.84836 or 13.67682 remains on the page. |
| R570-1-F4 = R571-1-F2 | MINOR | RESOLVED | `exercise_liveness` (`sim_phc_step.cpp:325-357`) places a crossing step between the returned t1 and the answered response. It then leaves every later request unanswered. It requires exactly one drop, with exactly 4 unanswered requests at the drop. The clean image logs `LOSS … unanswered=4` and passes 55 checks with 0 failures. The campaign plants `liveness-not-marked` and `r571-no-liveness` are byte-identical (sha256 `b7aef03b…`) to the output of each prior round's own plant script and to my own derivation. Each fails only `asCapable falls at the fourth unanswered request after a crossing exchange got=3 exp=4`. The donor generator is unchanged (gitlink `7dda9c3b`). |
| R570-1-F5 | MINOR | RESOLVED | Round 2 did not assign it, but its required outcome holds. `closingIssuesReferences` is `[]` (`receipts/pr707_closing_refs.json`). The body reads "Relates to #621" and "The later lane's physical five-step repeat completes #621." |
| R570-1-R1, R571-1-R1 | RESIDUE | RESOLVED | The PR body's Status line reads "Pushed; independent review in progress." |
| R570-1-S1..S5, R571-1-S1..S3 | SUGGESTION | carried, no lens effect | Not reopened. Two are still visibly open. CHANGELOG has no Unreleased entry for `7dda9c3b` (R570-1-S2). The `docs/testing/TESTING.md:585` row does not mention `phc-step` (R570-1-S5). |

## Evidence by lens (artifact-specific)

```text
[R570] PASS Conformance - sim_phc_step.cpp:325-357; check_nvm_capture.py:55-62,91,131-159; gen_gptp_ucode.py:1472-1497,1727-1738 (donor 7dda9c3b) - the liveness arm implements assignment 6095695340 item 4: asCapable falls exactly at the fourth unanswered request after an answered crossing exchange, not the third. The donor's LOST_N_C+1 compare and the PDEPOCH S_PDGOT credit produce that behavior. The receipt gate grades all six receipt arms as production, which is consistent with ruling 6087415319: the bound applies to production arms, and every receipt arm is a production point. The receipt and the page were judged against the identities in final ruling 6089776382.
[R570] PASS RTL - git diff e0ee38f9..d96b4a84 over *.sv, *.v, hdl/, syn/, configs/, sw/ and every submodule path is empty; the gitlinks of e0ee38f9 and d96b4a84 are equal (gptp-processor 7dda9c3b, protocol-processor 2ad2f845, verilog-axis 48ff7a7e) - the delta changes no RTL or donor artifact. The unchanged donor RTL was executed at this head under pinned Verilator 5.050: gptp_plane run 29/29, phc_step 55 checks with 0 failures.
[R570] PASS Robustness - scripts/probe_receipt_guard.py on check_nvm_capture.py; reviewer plants rv-credit-zero, rv-threshold-third and rv-threshold-fifth on gen_gptp_ucode.py - the receipt guard fails closed for every mutation-key value and for a missing key (the KeyError path is caught as FAIL). The liveness arm rejects a zero credit, an early threshold (got=3) and a late threshold (no drop inside the window, and the peer-silence check also fails). At the boundary, one tick over half the floor is refused.
[R570] PASS Tests - phc_step.py campaign 6/6 at this head; reviewer plants and the original donor 5dce647a run through --generator; the prior rounds' remaining plants (step-not-flagged, r571-deferred-bypass, r571-followup-bypass, r571-step-unmarked) - every planted defect fails at least one named check, and the clean image passes. The new check fails for the defect it names. check_nvm_capture.py's receipt-opt-out mutation and three source-level guard removals each fail. measure_test_evidence.py --check and --selftest exit 0.
[R570] PASS Docs - docs/design/GPTP_PLANE.md:128-137; SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1619-1667,1711,1809-1820; tb/verilator/nvm_capture_cpu/README.md:184-194; measure_test_evidence_readers.py:104-110; PR body - every figure and identity equals measurements.json (44/44). The docs describe the five plants and the receipt-opt-out mutation as they actually run. Local docs_check, check_em_dash --base 5603c353 (97 added lines, 0 findings), gen_toc --check, check_doc_style, check_gptp_docs --with-submodule, check_py_idiom, check_cpp_idiom and git diff --check all exit 0. Hosted docs-check, docs-check-no-git and wire-accountability succeed at this head.
```

Executed at this head under pinned Verilator 5.050. Identity: `Verilator 5.050 2026-07-01 rev v5.050`, wrapper sha256 `905795b9…`.

| Run | Result | Receipt |
|---|---|---|
| `phc_step.py --mutants` | rc 0; clean 55 checks, 0 failures; 5 plants rejected by name; campaign 6/6 | `receipts/phc/phc-official.*` |
| `make -C tb/verilator/gptp_plane` + `suite_tally.py --verdict` | rc 0 / rc 0; run 29/29, phc_step 55/0, campaign 6/6 | `receipts/gptp_plane_make.*` |
| `--generator` rv-credit-deleted / rv-credit-zero | rc 1; only the liveness check fails, got=3 exp=4 | `receipts/phc/phc-rv-credit-*` |
| `--generator` rv-threshold-third | rc 1; liveness check got=3 exp=4 | `receipts/phc/phc-rv-threshold-third.*` |
| `--generator` rv-threshold-fifth | rc 1; peer-silence and liveness checks fail | `receipts/phc/phc-rv-threshold-fifth.*` |
| `--generator` original donor `5dce647a` | rc 1; 14 failing checks, including the liveness check | `receipts/phc/phc-orig-donor-5dce647a.*` |
| prior plants (4) | rc 1 each | `receipts/phc/prior-*` |
| `check_nvm_capture.py` + 5 mutations | rc 0; rc 1 for each mutation, with its named reason | `receipts/check_nvm_capture.*` |
| `probe_receipt_guard.py` | expected outcome, rc 0 | `receipts/probe_receipt_guard.*` |
| `probe_receipt_mutation_key.py` (R570-1) | both plants REFUSED | `receipts/probe_receipt_mutation_key.*` |
| `compare_page_receipt.py` | ALL EQUAL, rc 0 | `receipts/compare_page_receipt.*` |
| `measure_test_evidence.py --check` / `--selftest` | rc 0 / rc 0 | `receipts/measure_test_evidence.*` |
| static documentation and idiom gates (8) | rc 0 each | `receipts/static*` |
| restore verification | RESTORE: EXACT; 0 tracked blobs differ; 3 gitlinks equal; parent and submodules clean | `receipts/verify_restore.*` |

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `sim_phc_step.cpp:325-357`, donor `gen_gptp_ucode.py:1472-1497,1727-1738`, `check_nvm_capture.py:55-62,91`, rulings 6087415319 / 6089776382, assignment 6095695340 | R570-2 | d96b4a8471028d3dfd370ce61dbe05ca9957320a |
| RTL | CLEAN | empty RTL/donor/pin delta `e0ee38f9..d96b4a84`; equal gitlinks; donor RTL executed in `gptp_plane` (29 + 55 checks) | R570-2 | d96b4a8471028d3dfd370ce61dbe05ca9957320a |
| Robustness | CLEAN | `probe_receipt_guard.py` (5 key values, 3 guard removals), credit-zero and threshold plants, one-tick boundary | R570-2 | d96b4a8471028d3dfd370ce61dbe05ca9957320a |
| Tests | CLEAN | `phc_step.py` campaign, 4 reviewer plants, original donor, 4 prior plants, gate mutations, test-evidence ratchet | R570-2 | d96b4a8471028d3dfd370ce61dbe05ca9957320a |
| Docs | CLEAN | `GPTP_PLANE.md:128-137`, `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1619-1667,1711,1809-1820`, capture README `:184-194`, readers disposition, PR body; 8 local gates; hosted docs contexts | R570-2 | d96b4a8471028d3dfd370ce61dbe05ca9957320a |

## Real limits

- No manager source bank exists at this head, and none is claimed or inferred.
- I did not run the full suite sweep, Yosys, the lint ratchet, any vendor stage, the builder gate or the capture campaign.
  - The source-head evidence for those is the author's published gate receipts at `e0ee38f9`.
  - The round 2 delta changes no RTL, donor file, pin, capture-harness file or `milan_dp` input (`sim_gmstep.cpp` is not in the delta).
  - The one suite the delta touches, `gptp_plane`, was run here.
- The capture receipt was judged statically, through the gate and the page comparison, against final ruling 6089776382. This round did not re-execute the lane invariant (base and candidate capture logs byte-identical); the earlier rounds stand for it.
- Hosted `rtl-full` was still in progress when read.
  - `full-ci-gate`, Yosys shards 0-3 and Verilator shards 0, 2 and 3 succeeded; shards 1 and 4 were still running.
  - The `verilator-suites` and `yosys-portability` aggregate contexts had not been emitted yet.
  - "Physical gPTP" is a skipped context, not hardware evidence.
- The IEEE 802.1AS-2020 text was not consulted directly in this session. The threshold reading follows the clause references in the PR, the donor and the round 2 assignment (see S1).
- Physical calibration NOT RUN. Issue #621 scope item 3, the bench five-step repeat, is still open and belongs to a later lane. Simulation passes are not hardware proof.
- In the receipts, local absolute paths were replaced with the placeholders `<CHECKOUT>`, `<PACKET>` and `<PINNED_VERILATOR_…>`. No other receipt content was changed.
- A read-only fetch refreshed the review clone's remote-tracking refs. Tracked bytes were not touched.

## Pending manager duties

- Confirm the hosted `verilator-suites` and `yosys-portability` conclusions on this exact head.
- Build and validate the current-dev merge candidate (source base `5603c353`, live dev `e8454e27`) with the builder and native banks, and link the receipts on the PR.
- Publish the donor branch `7dda9c3b` before the parent merge, so the gitlink is fetchable.
- Carry the capture-SoC RTL hashing gap in `scripts/check_nvm_capture.py` to the #495 residue checklist (ruling 6088189432).
- Decide on S1 (a follow-up issue for the allowedLostResponses reading).
- Keep #621 open for the physical repeat; `closingIssuesReferences` is currently `[]`.
- Before merge, an external positive review and the rest of the AGENTS.md section 7 bar are still required.

R570-2 FINISHED
