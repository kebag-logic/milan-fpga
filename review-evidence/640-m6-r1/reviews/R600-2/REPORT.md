[R600] NEGATIVE - exact head 1a042affce2f252f10ed40b3ec25659611b3974b

# R600-2: composition review of PR #719 (issue #640, Mark II lane M6) on the merge-train candidate

- Exact head: `1a042affce2f252f10ed40b3ec25659611b3974b`, tree `9ef4b6a221a43ec301f137501e948ba8ad2b9239`.
- Parents: dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5` (M2, PR #710, merged) and PR source head `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937`. Merge base: `e8454e2751d05b02ee8e5a571857589ab358ab86`.
- Role: internal cleared-context reviewer, composition round. All five lenses are applied to what the composition can change. The source head already has two POSITIVE source reviews: R600-1 and R601-1, both at `ee0fc6fd9`.

## Verdict

NEGATIVE, because of one MINOR finding. **R600-2-F1:** the PR body makes GitHub treat #640 as an issue this PR closes. `dev` is the default branch, so merging the PR would close the open milestone issue #640.

The composed tree itself is sound:
- It is the clean three-way merge of dev and the PR.
- Every line either lane added or removed in the three shared documents survives as intended.
- Every ledger row, running total and headroom figure recomputes from its rows.
- Every gate that reads the shared files passes on the candidate.
- F1 needs no change to the tree. It needs a PR-body edit, or an unlink, before merge.

There are also two optional SUGGESTIONs. No BLOCKER or MAJOR finding is open.

## Reconstruction, in order

1. AGENTS.md and CONTRIBUTING.md: lens contract, completion bar, merge rules.
2. docs/README.md: the authority map.
3. Issue #640:
   - Frozen acceptance: routed image at most 38,040 LUT with timing met; function unchanged; gate re-recorded by the change that reaches the target.
   - Lane M6 assignment (comment 6098405082): scope, proof, and "no change to default shipping behaviour, the register map or the wire format".
   - TAKEN and REVIEW READY for M6.
   - M2's ledger and D7: the record stays until M9.
4. Interface authorities in the shared files: `docs/design/MARK_II_AREA_PLAN.md` (Ledger, L3, L9, the firmware and block-RAM ledger, the cumulative estimates), `docs/design/AREA_BUDGET.md` (resource gate, lane table, memory ledger), `docs/testing/TESTING.md` (suite index, LiteX simulation paragraph) and `syn/ooc/pp_resource_baseline.json`.
5. `git diff ac2c5e77..1a042aff` plus history, then the source-side evidence.
6. Prior public findings on PR #719, read only after this round's own pass (see the section below).

## Composition analysis

### Shared files: verified, not assumed

`receipts/composition/merge_composition.txt` comes from `scripts/composition_check.sh`. It shows:
- The files the PR changes since the merge base that dev also changes are exactly `docs/design/AREA_BUDGET.md`, `docs/design/MARK_II_AREA_PLAN.md` and `docs/testing/TESTING.md`. This matches the manager's list.
- `git merge-tree --write-tree ac2c5e77 ee0fc6fd9` gives `9ef4b6a2`, the candidate tree.
- The candidate differs from dev only in the PR's 19 files, and from the PR head only in dev's 13 files.
- For each shared file, `git merge-file` reproduces the candidate byte for byte with 0 conflicts.

Line survival in each shared file:

| File | dev-added lines present | PR-added lines present | dev-removed lines absent | PR-removed lines absent |
|---|---:|---:|---:|---:|
| AREA_BUDGET.md | 6/6 | 4/4 | 2/2 | 0/0 |
| MARK_II_AREA_PLAN.md | 30/30 | 40/40 | 3/3 | 0/0 |
| TESTING.md | 16/16 | 2/2 | 0/0 | 2/2 |

Both TESTING.md suite texts remain:
- M2's `test_retained_cdc_storage.py` paragraph at `docs/testing/TESTING.md:681-695`.
- M6's `avtp_rxmon` and `chmap_capture` index rows at `:582` and `:587`.

### Ledger arithmetic on the merged text

`scripts/ledger_arith.py` gives `receipts/composition/ledger_arith.txt`: 79 checks, 0 failures.

- **Base rows.** The M2 and M6 base rows (`MARK_II_AREA_PLAN.md:686`, `:938`) are identical. Both equal the `route-1x1` gate record (LUT 50,267, FF 54,413, SLICE 15,779, 87.5 tiles) and the `AREA_BUDGET.md:164` headline.
- **Routed deltas.** Recomputed from each lane's own route:
  - M2: -128 LUT, -59 FF, -8 slices, 0/0 RAMB, WNS/WHS +0.007/-0.012.
  - M6: -706 LUT, -958 FF, +12 slices, 0/0 RAMB, WNS/WHS -0.158/-0.013.
- **M6 block credits** (`:947-952`). The two changed blocks sum to 468 routed, 418 post-synthesis and 839 FF. The two unchanged blocks are not credited. These figures match the text (`:959`) and the AREA_BUDGET note (`AREA_BUDGET.md:208`).
- **M2 figures.** 34 post-synthesis and 128 routed match `:688-689`, `:698` and `AREA_BUDGET.md:197`.
- **No double count.** M2 credits only SoC MAC/CSR crossing arrays (`:675-700`). M6 credits only the listener monitor and the channel-map capture (`:947-959`). L9 states "No M2 table credit overlaps these arrays" (`:555`). Neither lane credits the unchanged-block movement: the wrapper for M2; the protocol processor and the gPTP shadow for M6.
- **Running totals stay on the planning figures by design.** Both lanes say "keeps the planning figure until the week-4 re-measure" (`:701`, `:963`). So:
  - The cumulative table (`:971-982`) still recomputes row by row: 50,267 → 36,267 → 36,067 → 35,467 → 34,867 → 34,367 → 33,367 → 31,667.
  - The AREA_BUDGET lane table (`:184-195`) recomputes the same way.
  - Headroom 6,373 and 2,173 are correct (`:984-986`).
  - No row is counted twice and none is lost. No combined M2+M6 measured figure is claimed anywhere.
- **Block-RAM ledgers in both documents** (`MARK_II_AREA_PLAN.md:803-811`, `AREA_BUDGET.md:240-248`). The running tile totals recompute: 87.5, 81, 87, 68.5, 118.5, 120.5, 109.5. M2's +2 allowance row is kept, and M2's prose says it is unused (`:700`). M6 adds no tile (`:962`). So the composition adds no block-RAM debit.
- **The arithmetic script can fail.** `scripts/ledger_probe.py` gives `receipts/probes/P2_ledger_script_can_fail.txt`. It planted 8 errors and caught all 8: a cumulative row, an M6 block credit, an M2 route figure, an M6 claim on an M2 array, a BRAM running total, a budget lane row, and each lane's AREA_BUDGET note removed.

### Other semantic interactions checked

- **Anchors and TOC.**
  - `gen_toc.py --check` and `--verify-anchors` pass (143 pages; 470 cross-page fragments).
  - The two new cross-page links resolve: `AREA_BUDGET.md:198` → `#m2-intermediate-measurement` and `:209` → `#m6-intermediate-measurement`.
  - Probe P1 (`receipts/probes/P1_lost_anchor.txt`) renamed the M2 heading in the clone, then restored it. `--verify-anchors` failed on the AREA_BUDGET link; `docs_check.py` and `check_doc_paths.py` stayed green. So same-page fragments are not gated by the repository.
  - I therefore checked them with `scripts/intra_anchors.py` (`receipts/composition/intra_anchors.txt`): plan 27/27, AREA_BUDGET 5/5, TESTING 14/14 resolve, including `MARK_II_AREA_PLAN.md:454` and `:556`. Probe P3 (`receipts/probes/P3_intra_anchor_can_fail.txt`) shows this check fails on a lost heading.
- **Registries and inventories.** All pass on the candidate:
  - `measure_test_evidence.py --check`: M6 edits `scripts/measure_test_evidence_readers.py`; M2 adds a LiteX test. Result: 0 unexplained DUT-source readers.
  - `check_rtl_source_lists.py`: 108 files in the datapath closure, 4/4 consumer lists.
  - `check_soc_sources.py`: 43 modules registered, 77 sources.
  - `check_port_contracts.py`: undocumented-port ratchets equal.
  - `pp_srcs.py --check`.
  - `ci_events.py --check` and `--selftest`: 1,749 contract items.
  - `ci_scope.py --selftest`.
- **Global ratchets** (a sum of both lanes could exceed a budget that each lane met alone). All pass:
  - lint: 90 <= 90, pinned Verilator 5.050.
  - naming, fail-fast, hygiene, and the SV/C++/Python/shell idiom budgets.
- **Resource gate.** `pp_resource_gate.py check-baseline` passes (3 endpoints) and `--selftest` passes. The record is unchanged under D7.
- **RTL surface.**
  - M6 changes no top-level port. `milan_datapath.sv` changes only the internal wiring of the monitor's GET_COUNTERS read (`diag_col_i`/`diag_q_o`).
  - M2 changes only `sw/litex`, `scripts/run_litex_sims.sh` and the regenerated `tb/verilator/gptp_txts/generated/mac_tx_chain.v` and manifest. Only `gptp_txts` consumes those, and it builds none of M6's files.
  - No stale `diag_cnt_o` reference exists outside the lockstep reference copies.
  - M2's `test_retained_cdc_storage.py` reads no `hdl/` file. Its inputs are byte-identical between dev and the candidate.
- **Lockstep reference copies.** `receipts/composition/reference_identity.txt`: both `reference/*_ref.sv` files differ from the dev module only in name-bearing lines (the file header, plus one `$error` text in the capture). This holds at `e8454e27` and at `ac2c5e77`, so the "module of dev `e8454e27`" statement in TESTING.md is still exactly true on the composed dev.
- **Em dashes.** `check_em_dash.py` reports 0 findings for both ranges:
  - `--base ac2c5e77`: 53 added lines, 3 pages.
  - `--base e8454e27`: 1,236 lines, 7 pages, so both lanes together.

## Executions (this round, at the exact head)

All runs are reviewer-run, in the foreground, and in parallel where independent. Interpreter: the pinned Markdown-renderer environment (CPython 3.14.7, html5lib 1.1). Simulator: Verilator 5.050 (`receipts/gates/TOOLS.txt`).

| Run | Result | Receipt |
|---|---|---|
| 35 repository gates (`scripts/run_gates.sh`, `scripts/gates.txt`) | 35/35 rc 0 | `receipts/gates/SUMMARY.txt`, `receipts/gates/*.log`, `*.rc` |
| Merge reproduction and line survival | all match | `receipts/composition/merge_composition.txt` |
| Ledger arithmetic | 79/79 PASS | `receipts/composition/ledger_arith.txt` |
| Same-page anchors | 46/46 resolve | `receipts/composition/intra_anchors.txt` |
| Reference-copy identity | name-only differences | `receipts/composition/reference_identity.txt` |
| Probes P1-P3 | each failed as planted | `receipts/probes/` |
| Clone integrity after probes | head, tree, index and worktree identical; 0 untracked; gitlinks as recorded; required submodules clean | `receipts/integrity.txt` |

### Manager-owned candidate banks, read only and not re-run

`receipts/manager_candidate_banks.txt` records digests of the manager's banks at this exact head and tree:
- Builder: 48/48 rc 0.
- Native: 5/5 rc 0. This covers the full suite bank in 5 shards (each rc 0), Yosys, the protocol-processor suites, gPTP `make all` and BDD.

From those logs:
- `avtp_rxmon`: lockstep N=1 and N=8 at 36 checks / 0 failures each; mutants 5/5.
- `chmap_capture`: lockstep, then 4/4.
- `tkdiag`, `render_setpoint`, `milan_dp`, `capture_coherence`, `gptp_txts` and `csr` all pass.

These are the manager's receipts, cited as such.

### Hosted evidence (inspected only)

`receipts/hosted_snapshot.txt` covers PR source head `ee0fc6fd9`: 22 contexts completed with success, and one scheduled context (`Physical gPTP (nightly and manual)`) was skipped. A skip is not an executed pass. The candidate `1a042aff` is not on the remote, so no hosted run exists for it.

## Findings

### R600-2-F1 - MINOR - Conformance, Docs - PR #719 body line 22 - the body's own sentence makes the merge close issue #640

- **Authority/evidence (`receipts/pr_closing_reference.txt`):**
  - The body reads "It must not close #640." GitHub parses "close #640" as a closing keyword and ignores the negation. `gh pr view 719 --json closingIssuesReferences` returns `[640]`.
  - The repository default branch is `dev`, and the PR targets `dev`. A PR merged into the default branch closes its closing references.
  - The sibling #640 lanes (#702 and #710, both merged into `dev`, and #713) word this as "Relates to #640". They carry `closingIssuesReferences=[]`, and #640 stayed open after their merges.
  - Issue #640's frozen acceptance (routed image <= 38,040 LUT and the gate re-record) is not met by this lane. The PR body itself says #640 must stay open.
  - AGENTS.md section 7 makes closing the Issue a completion step, valid only when the task is complete.
  - The source rounds did not raise this, and no public comment mentions it.
- **Impact:** merging the candidate through the PR would close the Mark II milestone issue. Its state would then falsely show NFR-RES-01 as met, and the issue would drop out of the open-work view while lanes M5, M7, M8 and M9 still report there. The tree and every figure are unaffected.
- **Required outcome:** before the merge, PR #719 carries no closing reference to #640, and #640 is OPEN after the merge lands. One example rewording of line 22 is "It leaves #640 open." Any wording works if no closing keyword sits directly before `#640`, or the link is removed in the Development panel.
- **Verification:**
  - `gh pr view 719 -R kebag-logic/milan-fpga --json closingIssuesReferences` returns `[]` before the merge.
  - `gh issue view 640 --json state` returns `OPEN` after it.
  - This changes no tree byte, so no gate or bank needs re-running.
- **Why MINOR, not RESIDUE:** the fix is a wording change, but the defect is not wording only. GitHub machine-reads the sentence into an issue-state change that misstates the milestone's conformance.

### R600-2-S1 - SUGGESTION - Docs - `docs/design/AREA_BUDGET.md:197-210`, `docs/design/MARK_II_AREA_PLAN.md:673,920` - the two lanes' notes sit apart in the merged text

- AREA_BUDGET now carries two near-identical notes, each ending "This table keeps its planning estimates until the week-4 re-measure."
  - They are separated by the split paragraph (`:201-206`).
  - M6's "This table" now sits two paragraphs below the table it refers to.
- In the plan, M2's intermediate measurement sits before "Default split saving basis", and M6's sits after "Remaining levers without overlap".
- Every figure is correct and every link resolves. This is a readability point produced by merging two independent insertions.
- **Optional:** at the week-4 re-measure, put the lane notes in one paragraph directly under the lane table, and the intermediate measurements in one place in the Ledger.

### R600-2-S2 - SUGGESTION - Docs - `docs/design/MARK_II_AREA_PLAN.md:834,861`, `docs/design/AREA_BUDGET.md:270,278` - deferral text still names M6 as a block-RAM consumer

- "Unpriced M6/M7 RAM conversions ... consume that allowance" and "defer new M6/M7 block-RAM conversions first" now sit beside M6's measured "M6 adds no block-RAM tile" (`:962`).
- M2 updated its own clause the same way: "adds no tile, so deferring it frees none" (`:860`).
- This is present identically at the reviewed source head, so the composition does not introduce it.
- **Optional:** name M7, or "any later RAM conversion", at the week-4 re-measure.

No BLOCKER, MAJOR or RESIDUE finding from this round.

## Prior public review findings on PR #719 (read after this round's own pass)

The artifacts behind every source finding are byte-identical at the candidate. `git diff ee0fc6fd9 1a042aff` touches no `hdl/` file, no file in `tb/verilator/avtp_rxmon/` or `tb/verilator/chmap_capture/`, and not `docs/design/MEDIA_CLOCK_FOLLOWING.md`. Each finding is therefore retained unchanged:

- **R600-1-RES1 (RESIDUE, Docs):** the stale monitor line citations at `docs/design/MEDIA_CLOCK_FOLLOWING.md:315,317,459,960` are still present (`:465-491`, `:218`, `:486-491`, `:173-174`). Retained, with its exact fix. It goes to the residue checklist.
- **R600-1-S1 (SUGGESTION, RTL):** retained. The monitor file is unchanged.
- **R601-1-S1 (SUGGESTION, Tests):** retained.
- **R601-1-S2 (SUGGESTION, Tests, Robustness):** retained.
- **R601-1-S3 (SUGGESTION, Docs):** retained.
- **R601-1-R1 (RESIDUE, Docs, PR body "Status"):** still present at body line 16 ("GREEN at `ee0fc6fd9`: full sweep ..."). Retained, with its exact fix. It goes to the residue checklist.

None of these is MINOR or worse, and the composition makes none of them worse.

## Lens results

```text
[R600] UNCLEAN Conformance - PR #719 body:22, receipts/pr_closing_reference.txt - R600-2-F1: the merge would close #640, whose frozen acceptance is unmet. Otherwise: no register-map, wire, parameter-default or shipping change enters through the composition (datapath ports unchanged; M2 touches only SoC/LiteX files); acceptance re-evidenced on the candidate by the manager's banks at this exact head (manager_candidate_banks.txt)
[R600] PASS RTL - hdl/milan/milan_datapath.sv:3447-3536,6334-6347 at 1a042aff; tb/verilator/gptp_txts/generated/manifest.json; receipts/gates/{lint_rtl,soc_sources,rtl_source_lists,port_contracts,pp_srcs}.log - no shared module or top-level port between M2's SoC/MAC-chain changes and M6's blocks; lint 90<=90 on the composed tree; reference copies equal composed dev modules (reference_identity.txt)
[R600] PASS Robustness - receipts/manager_candidate_banks.txt (avtp_rxmon lockstep N=1/N=8 hazard cases H1-H4, chmap_capture lockstep, capture_coherence 20,832/0) at 1a042aff - composition adds no path, reset, capacity or configuration change to M6's blocks; the hazard and refusal legs pass on the composed tree; source robustness coverage stands (R600-1, R601-1 at ee0fc6fd9)
[R600] PASS Tests - receipts/gates/{test_evidence_check,test_evidence_selftest,ci_events_check,ci_scope_selftest}.log; docs/testing/TESTING.md:582,587,681-695; receipts/probes/P1-P3 - test registries and inventories reconcile with both lanes' tests; both suite texts survive; my own arithmetic and anchor checks shown able to fail; manager candidate banks 48/48 and 5/5 at this head
[R600] UNCLEAN Docs - PR #719 body:22 (R600-2-F1). Tree docs otherwise clean: docs/design/AREA_BUDGET.md:164-283, docs/design/MARK_II_AREA_PLAN.md:450-1003, docs/testing/TESTING.md:579-695 verified by merge_composition.txt, ledger_arith.txt (79/79), intra_anchors.txt (46/46) and gates docs_check, gen_toc --check/--verify-anchors/--selftest, check_em_dash (both ranges), doc_style, doc_paths, DOC_MAP --check, module matrix, solution docs, feature status
```

## Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R600-2-F1 open) | Issue #640 acceptance and M6 assignment; PR #719 body and closing references; the composition's lack of ABI, wire or default changes; the manager's candidate banks | R600-2 (composition); source: R600-1, R601-1 | composition `1a042affce2f252f10ed40b3ec25659611b3974b`; source `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937` |
| RTL | CLEAN | The composition touches no shared RTL. Datapath wiring `:3447-3536,6334-6347`; M2's generated MAC chain and manifest; lint, SoC-source, RTL-list, port-contract and `pp_srcs` gates on the composed tree. M6's RTL is covered by the source reviews. | R600-2 (interaction); source: R600-1, R601-1 | `1a042affce2f252f10ed40b3ec25659611b3974b`; `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937` |
| Robustness | CLEAN | Not touched by the composition (no path, reset or configuration change enters through the merge). The candidate's hazard, lockstep and coherence legs pass in the manager's banks. | Source: R600-1, R601-1; R600-2 confirms no interaction | `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937`; `1a042affce2f252f10ed40b3ec25659611b3974b` |
| Tests | CLEAN | TESTING.md rows and paragraph; test-evidence registry; CI events and scope; probes P1-P3; the manager's candidate banks | R600-2 | `1a042affce2f252f10ed40b3ec25659611b3974b` |
| Docs | UNCLEAN (R600-2-F1 open; S1 and S2 optional; RES1 and R601-1-R1 are RESIDUE) | AREA_BUDGET and MARK_II_AREA_PLAN ledgers and notes; TESTING.md; anchors and TOC; em-dash; PR body | R600-2 | `1a042affce2f252f10ed40b3ec25659611b3974b` |

Once F1 is fixed, by a body edit with no tree change, Conformance and Docs need only the verification in F1. No tree content would need re-review.

## Real limits

- **The composed image (M2 + M6) has not been routed.** Each lane's route was measured separately against `e8454e27`. The combined LUT, WNS and WHS are unmeasured. The merged text claims no combined figure, and the gate record stays under D7. Re-measuring belongs to the week-4 re-measure and M9.
- **I did not re-run the simulation banks.** Suite, lockstep, Yosys, protocol-processor and builder results at this head are the manager's candidate banks, which I read only.
- **M2's `test_retained_cdc_storage.py` was not run here.** This host has no LiteX environment, and the manager's banks show no log for it. Its inputs are byte-identical between dev and the candidate, so the composition cannot change its result. Its evidence is M2's own.
- **Gate interpreter.** The gates ran under CPython 3.14.7 in the pinned renderer environment, not the hosted CPython 3.12.
- **Gate gap.** The repository gates do not judge same-page fragment links (probe P1). This round checked them for the three shared files only.
- **No hardware.** Physical calibration and bench were NOT RUN. The hosted physical gPTP context is a scheduled skip, not proof.
- **No hosted run for the candidate.** The candidate is not on the remote, so it has none.

## Pending manager duties

- Resolve R600-2-F1 before the merge: reword PR #719 body line 22 or unlink #640, and confirm `closingIssuesReferences` is `[]`. After the merge, confirm #640 is OPEN.
- At the merge turn, validate the current-dev candidate. If dev has moved past `ac2c5e77`, rebuild the candidate and re-run the shared-file gates and `scripts/ledger_arith.py`.
- Hosted and local-replica acceptance at the merged head.
- Carry R600-1-RES1 and R601-1-R1 (RESIDUE) to the residue checklist. Carry the optional S1 and S2 to the week-4 re-measure.
- Schedule the composed route at the week-4 re-measure or M9.

R600-2 FINISHED
