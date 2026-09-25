[R322] POSITIVE - exact head ec9cf454bf997fab230d0216dc609e737bc47caa

Round R322-3, composition review of the merge-train candidate for issue #541 / PR #562.
Candidate `ec9cf454bf997fab230d0216dc609e737bc47caa`, tree `6cc8996a3b2040f14950456f9951d994e3660887`.
Parents: the #508 train candidate `b1b334725dcf12e084eaa3bb96b1e6865c052267` and the PR head `fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c`.

## Verdict

POSITIVE. The composed tree introduces no defect beyond the reviewed sources.
No composition finding of any severity is open. All five lenses were applied at this head and are clean.
The PR's own content is covered by the two POSITIVE source reviews at `fa1b5c36`: R322-2 (issuecomment-5829288317) and R323-2 (issuecomment-5830093046).

## What the composition is

Receipt: `receipts/01_topology.txt`.

- **The candidate tree is reproducible.** It equals the clean `git merge-tree` of `b1b33472` and `fa1b5c36`, which is `6cc8996a`. It also equals the merge of live dev `a3d795ae` into the candidate.
- **Dev's content is included, but dev's commit is not.** Live dev `a3d795ae` is not an ancestor of the candidate. Both of its parents are ancestors: `5b73d3f4` through the PR, and `8383e929` through the train. Its tree `a1813edb` is exactly the clean merge of those parents. So the candidate carries all of dev's content.
- **The PR's own change is six files** (`5b73d3f4..fa1b5c36`). It lands on the train byte-for-byte: `b1b33472..ec9cf454` has the same stable patch-id, `8967cdbc`.
- **Three of the six files are also changed by the train** (`a3d795ae..b1b33472`). The textual merge of each is clean, and the regions do not overlap:
  - `docs/reference/REGISTER_MAP.md`. The PR edits the `CRF_CTRL` row at :837. The train edits the LWSRP prose at :1114-1143 and the `PP_CTRL` row at :2184.
  - `docs/testing/TESTING.md`. The PR edits the `crf_rx` row, now at :464 (it was :463 at source). The train adds the #508 `gsi-mutants` row to the explicit-campaign table at :267.
  - `scripts/measure_test_evidence.py`. The PR edits the `tb/verilator/crf_rx/mutants.py` disposition at :597-600. The train adds four dispositions in the same `DUT_READER_DISPOSITIONS` table (:596-662): `desc_mem_guard/mutate.py`, `pp_top/gsi_mutants.py`, `srp_admission/mutants.py` and `milan_dp/gsi_mutants.py`.
- **The other three PR files are not touched by the train:** `hdl/ieee1722/crf/KL_crf_rx.sv`, `tb/verilator/crf_rx/mutants.py` and `tb/verilator/crf_rx/sim_discontinuity.cpp`. No input of the `crf_rx` suite is touched by the train either. `KL_crf_rx.sv`, `KL_mmcm_drp_servo.sv`, `cdc_pulse.sv`, `cdc_handshake.sv`, and the `tb/verilator/crf_rx` and `tb/verilator/mmcm_servo` trees are blob- or tree-identical to `fa1b5c36` (`receipts/06_rtl_strip_and_suite_inputs.txt`).

## Composition checks and results

1. **Reader table (`measure_test_evidence.py`).**
   - The composed `DUT_READER_DISPOSITIONS` has 20 keys and no duplicate key; I checked this by parsing the source, because a Python dict literal would silently let a later duplicate win. Every key resolves to a file in the candidate.
   - The script's own `unexplained` and `stale` checks (:813-814) both come back empty. `--check` and `--selftest` exit 0 (`receipts/03_static/01.log`, `02.log`).
   - Run on the train alone, the audit gives the same ratchet reading: 75 <= 77 suites without a mutation arm, 10 <= 10 unseeded draw sites, 0 <= 0 unexplained readers, 3 <= 3 wall-clock files. The only line that differs between the two outputs is the `crf_rx` disposition text (`receipts/04_mte_train_vs_candidate.txt`).
2. **`TESTING.md` against the suites.**
   - The `crf_rx` row (:464) names `validation_error_unlocks`, `validation_error_refreshes_timeout`, tu, jump, refill, sample-edge and servo-validity mutants, all in the default gate.
   - `make -C tb/verilator/crf_rx` on the candidate runs exactly those ten controls in its default target, and all pass (details under item 4).
   - The #508 explicit-campaign row (:267) and the `crf_rx` row are independent. The `crf_rx` mutants run in the default target, not as an explicit campaign, so no explicit-campaign row is owed. Neither row carries a count that the other side changed.
3. **`REGISTER_MAP.md`.**
   - The composed `CRF_CTRL` row (:837) is byte-identical to the reviewed source line.
   - Its cross-reference to `CRF_STATUS[15:8]` (`0x74C`, :842) agrees with the CSR mux (`hdl/common/csr/milan_csr.sv:784,2358`), which neither side changed.
   - The train's LWSRP and `PP_CTRL` edits are in unrelated rows.
   - The TOC summary for the `0x738` section (:185) agrees with the row.
   - `gen_toc.py --check` passes (107 pages). `--verify-anchors` passes, reproducing 174 cross-page fragment links. `docs_check.py` reports zero findings in both modes: Git (165 md + 867 text) and a Git-free archive of the candidate (one skip, the Git-only inventory parity).
4. **`crf_rx` with its mutant campaign on the candidate.**
   - `make -C tb/verilator/crf_rx` exits 0 in 546 s. Results: 13,836 unit checks, 2,201 discontinuity checks, 69 talker-step checks and 10 mutation controls, with zero failures.
   - `validation_error_unlocks` fails `validation error preserves established lock`, as required. `validation_error_refreshes_timeout` fails `reject stream cannot refresh the 100 ms timeout`, as required.
   - These counts equal the source-head counts published on #541.
   - Receipts: `receipts/02_crf_rx_make_all.log` and `.rc`. The pinned 5.050 build ran with at most 8 jobs (`receipts/00_tool_identity.txt`).
5. **The wider gate bank on the candidate: 29 invocations, all exit 0** (`receipts/03_static/summary.tsv`):
   - `check_em_dash.py --base b1b33472`: 0 findings over the 2 added Markdown lines.
   - Documentation: `check_doc_style` (and its self-test), `check_doc_paths`, `gen_module_matrix --check`, `DOC_MAP.gen --check`, `check_solution_docs`, `check_feature_status` (and its self-test), `check_hygiene --check`.
   - Idiom checks for SV, C++ and Python.
   - Measurement and source checks: `check_todo_ownership`, `measure_fail_fast --check`, `measure_naming --check`, `check_port_contracts`, `check_rtl_source_lists`, `check_archive`.
   - CI: `ci_events --check` (1647 contract items) and `ci_events --selftest`.
   - `git diff --check` against both `b1b33472` and `a3d795ae`.
   - Separately, `gen_hdl_reference.py --selftest` and the full reference build exit 0 (`receipts/07_hdl_reference.log`).
6. **The RTL change is comment-only.** Comment- and whitespace-stripped `KL_crf_rx.sv` is identical at `b1b33472`, at `a3d795ae` and at the candidate (`receipts/06_rtl_strip_and_suite_inputs.txt`). The train's `milan_datapath.sv` edits that mention CRF or lock are comment text only, and the datapath comment that describes CRF unlock (:3068-3070) says silence-only, which matches the corrected contract.
   - A sweep of the live docs and HDL finds no remaining claim that a validation error unlocks. The one old claim is in `docs/history/v1/design/TIME_SYNC.md:351`, which is marked OBSOLETE and which neither side touched.

## Findings

None. No BLOCKER, MAJOR, MINOR or SUGGESTION is raised by this round.

## Prior public findings on this PR, resolved or retained at this head

I read these after completing the independent pass above (`receipts/10_prior_findings_anchors.txt`).

| Finding | Severity / lenses | Status at `ec9cf454` | Evidence |
|---|---|---|---|
| R322-1-F1: "does not refresh the timeout" had no failing arm | MINOR / Tests, Robustness | CLOSED, still closed | The `validation_error_refreshes_timeout` control fails its named check on the candidate (`receipts/02_crf_rx_make_all.log`). `sim_discontinuity.cpp` is blob-identical to `fa1b5c36`. |
| R323-1 F1: the same defect | MINOR / Tests, Robustness | CLOSED, still closed | Same as above. |
| R323-1 F2: the testing index did not name the mutant | SUGGESTION / Docs | Resolved, still resolved | The `crf_rx` row is byte-identical to source (sha prefix `cfaa76e5`), now at `TESTING.md:464`. |
| R322-1-S1: `CRF_CTRL` row qualifiers | SUGGESTION / Docs | Retained, optional, source-owned | `REGISTER_MAP.md:837` is byte-identical to source. The composition does not change it. |
| R322-2-S1: harness-local descriptions predate the #541 checks | SUGGESTION / Docs, Tests | Retained, optional, source-owned | `tb/verilator/crf_rx/Makefile:9` and `sim_discontinuity.cpp:3` are unchanged. The composition does not change them. |

## Lens results

```text
[R322] PASS Conformance - docs/reference/REGISTER_MAP.md:837,842,185 at ec9cf454; hdl/common/csr/milan_csr.sv:784,2358; receipts/01_topology.txt - composed CRF_CTRL row byte-identical to reviewed source; train's LWSRP/PP_CTRL edits in unrelated rows; CSR cross-reference consistent
[R322] PASS RTL - receipts/06_rtl_strip_and_suite_inputs.txt; hdl/ieee1722/crf/KL_crf_rx.sv; hdl/milan/milan_datapath.sv:3068-3070 - composed KL_crf_rx.sv comment-stripped identical to train and dev; train does not touch any crf_rx input; datapath CRF-unlock comment agrees
[R322] PASS Robustness - receipts/02_crf_rx_make_all.log (rejected-stream timeout, lock-retention, discontinuity legs); receipts/06 - suite inputs byte-identical to fa1b5c36; all legs green on the candidate; no composed behaviour change
[R322] PASS Tests - receipts/02_crf_rx_make_all.log; receipts/03_static/01.log,02.log; receipts/04_mte_train_vs_candidate.txt; scripts/measure_test_evidence.py:596-662 - 13,836/2,201/69 checks + 10 controls pass; reader table 20 keys, no duplicates, 0 unexplained, 0 stale; ratchet equal to train
[R322] PASS Docs - docs/testing/TESTING.md:264-268,464; docs/reference/REGISTER_MAP.md:837; receipts/03_static/summary.tsv (docs_check, gen_toc --check/--verify-anchors, em-dash vs b1b33472, style, paths, module matrix, DOC_MAP); receipts/05_docs_check_nogit.log - both docs_check modes 0 findings; anchors resolve
```

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The composition touches this lens through `REGISTER_MAP.md`. Examined `:837,842,185`, `milan_csr.sv:784,2358`, `receipts/01`. The PR's own clause decision is covered by R322-2 and R323-2 at `fa1b5c36`. | R322-3 | `ec9cf454bf997fab230d0216dc609e737bc47caa` |
| RTL | CLEAN | The composition does not change any RTL the PR touches; it was applied anyway (`receipts/06`, `milan_datapath.sv:3068-3070`). The PR's RTL is covered by R322-2 and R323-2. | R322-3 (the PR's own RTL: R322-2, R323-2) | `ec9cf454bf997fab230d0216dc609e737bc47caa` (source reviews: `fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c`) |
| Robustness | CLEAN | The composition does not change the scope. The suite inputs are byte-identical and every leg was rerun on the candidate (`receipts/02`, `receipts/06`). | R322-3 (the PR's own robustness: R322-2, R323-2) | `ec9cf454bf997fab230d0216dc609e737bc47caa` (source reviews: `fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c`) |
| Tests | CLEAN | The composition touches this lens through the shared `measure_test_evidence.py` table and `TESTING.md`. Examined `receipts/02`, `03/01-02`, `04`. | R322-3 | `ec9cf454bf997fab230d0216dc609e737bc47caa` |
| Docs | CLEAN | The composition touches this lens through `TESTING.md` and `REGISTER_MAP.md`. Examined `receipts/03_static`, `05`, `07`. | R322-3 | `ec9cf454bf997fab230d0216dc609e737bc47caa` |

## Real limits

- **This review judges the composition only.** The PR's own design and test sufficiency rest on R322-2 and R323-2 at `fa1b5c36`.
- **Not run:**
  - `xvlog_gate.py`. The analysis tool is not installed on this host.
  - The full parent, PP, gPTP, Yosys and builder banks, which are out of scope.
  - `mmcm_servo`. Its inputs are tree-identical to source, and its unit build was exercised by the `crf_rx` servo mutants.
  - `act`, and the host-side `act_ci` and its self-test, which this round was not permitted to run.
- **Hosted checks exist only for the PR source head `fa1b5c36`** (all executed contexts succeeded, and the nightly physical gPTP context was skipped). The candidate `ec9cf454` is not a hosted head (`receipts/09_hosted_checks.tsv`).
- **Physical calibration was not run.** Skipped field contexts are not hardware proof.
- **The `crf_rx` wall time was 546 s with an 8-job cap.** A slower hosted runner is still expected to fit the 1800 s default suite budget, but I did not measure one.
- **The Markdown renderer and HDL-reference parser** were installed from the repository's hash-locked requirement files into a disposable environment, not a shared one.

## Pending manager duties

- Build and validate the final current-dev candidate at the merge turn. Live dev `a3d795ae` must be an ancestor of the merged commit. Its content is already present here, and the tree is proven equal to merge(`a3d795ae`, candidate), but the commit is not an ancestor of this candidate.
- Own hosted and `act` acceptance on the final candidate, including exact-head `verilator-suites` and `yosys-portability` evidence.
- Get merge authorization from a maintainer.
- Run post-merge containment and close issue #541 (`Closes #541`).
- Optionally file R322-1-S1 and R322-2-S1 (SUGGESTIONs).
- Informational, owned by the train and not caused by #541: the mutation ratchet can be lowered from 77 to 75.

## Packet

`scripts/` holds the portable probes: `verilator_j8.sh` (the job cap), `run_static.sh`, `strip_compare.py` and `mte_train_vs_candidate.sh`. `receipts/` holds the raw outputs. `MANIFEST.sha256` lists every published file. After all probes the clone was restored to the exact head. Tracked blob bytes and modes, the index and the three required submodule gitlinks all match (`receipts/08_clone_integrity.txt`).

R322-3 FINISHED
