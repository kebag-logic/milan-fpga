[R312] POSITIVE - exact head 2ab66c9de3a63942c4d3251e1354e8ad3a50d88c

Round R312-5: composition acceptance for issue #501 / PR #557.
Candidate `2ab66c9de3a63942c4d3251e1354e8ad3a50d88c`, tree `c31836885d0319953ec3ea3613a88c6b93977fbf`.
Parents: `0b81fdc969131b82c535c4a183a78065fd1cd2d8` (the queued predecessors) and the reviewed PR source head `efcabc379b1e0be1366bfc05bdcc05a759b55616`.
PR source base: `573f0052a0e4412e81f0845438fcec2086ce5d55`.

(Verdict and ledger were written before any prior review finding was read. The prior-findings section is added after them.)

## Scope reconstructed

- Issue #501 body, the 2026-09-23 decision (grow the dynamic output-map record to the stream-channel key space at 8x8; 1x1 byte-identical), the Ready scope items 1-6, and the round 2-4 assignments and corrected capture-hold decision (#559 owns it).
- AGENTS.md sections 6-7 and CONTRIBUTING.md 2.1 step 7 (validate the candidate merge result).
- `git diff 0b81fdc9..2ab66c9d` (14 files, the PR's own set) and the candidate's merge history.

## What the candidate is

Receipt: `receipts/composition_check.log` (script `composition_check.sh`).

- The candidate tree equals a clean `git merge-tree --write-tree 0b81fdc9 efcabc37`: `c31836885d03...`. The merge added no resolution work.
- `files(0b81fdc9..candidate)` equals the PR's 14-file set. `files(efcabc37..candidate)` equals the predecessors' 33-file set.
- Predecessor steps on the first-parent chain: dev (#408, merge `44873590`), 387b (`e1333a14`), and 548 (`0b81fdc9`).
  - `44873590`'s tree equals live dev `ffcbd33d`.
  - Live dev moved during this round to `c266432d` (PR #555 merged). Its tree `8ecccb1d...` equals the candidate's 387b step `e1333a14`, so the candidate is still live dev plus 548 plus 501 (`receipts/hosted_state.txt`).
- Files changed by both this PR and a predecessor (verified with git, and matching the brief):
  - `docs/integration/BAREMETAL_FIRMWARE.md`: dev(408) and 387b
  - `sw/builder/test_builder.py`: dev(408) and 387b
  - 548 touches neither.
- For both overlap files, the PR's own change has the same stable patch-id before and after the merge (`d0801bc4...`, `eccd231a...`). The merge took both sides without altering either.
- The predecessors do not reach the PR's inputs:
  - the `amap_edit_validate` block of `hdl/milan/milan_datapath.sv` (the stream-channel key the record size derives from) is byte-identical from base to candidate;
  - `hdl/milan/KL_nvm_backend.sv` and all three required gitlinks are unchanged.

## Semantic interactions examined

1. **Gate 1b and the compiled census (#408, 387b) against the renamed writer constants (#501).**
   - #408 retired gate 1b's text rules onto per-selection grading and a compiled, resolved store census of `sw/firmware/milan_baremetal/milan_baremetal.c`. It stubs the generated headers from `census_defines` (`sw/builder/test_builder.py:4462`).
   - #501 renames `MILAN_NVM_MAP{IN,OUT}_CLUSTERS_k` to `..._ENTRIES_k` in the writer (`milan_baremetal.c:273-306,383-394,498-503,735-737`), in `firmware_constants` (`scripts/nvm_shape.py:177`), and in that stub (`test_builder.py:4485-4487`).
   - No other consumer names the old spelling: `git grep` finds no `MAP(IN|OUT)_CLUSTERS` or `nvm_map(in|out)_clusters` anywhere. `sw/litex/milan_soc.py:3980` and the host test publish the constants generically.
   - The #408 closure table keeps exactly one `#error` (the saved-state contract guard). The PR's firmware edit is a line-for-line rename that adds no directive.
   - Executed: `test_baremetal_profile_contract` alone on the candidate, with `--require-rv32` and the RV32 cross compiler, exits 0 in 474 s (`receipts/builder_profile_contract.log`). The census compiled the renamed writer.
   - Fault probe (`probe_overlap_census.sh`, run in a disposable clone of the candidate):
     - It plants a mis-resolved overlap, with the census stub keeping `..._CLUSTERS_k` while the writer uses `..._ENTRIES_k`.
     - The same test then fails with "the compiled census could not build the firmware", and GCC's diagnostic names the stale stub. The exact blob `e0a8c002...` was restored afterwards.
     - Receipts: `receipts/probe_overlap_census.log` and `receipts/probe_overlap_census.planted_test_output.log`.
     - The first run of this probe used an acceptance pattern that required the ENTRIES spelling in the log. The gate prints only the tail of GCC's output, so that run reported "NOT caught" although the test had failed for this cause. The criterion was corrected and the probe re-run. Both receipts are kept (`receipts/probe_overlap_census.run1_strict_criterion.log`).
2. **`BAREMETAL_FIRMWARE.md`.**
   - #408 and 387b rewrote the gate 1b sections (lines 265-1707 region). #501 changes one sentence in "Saved state: the flash writer" (`:1719-1722`).
   - The composed paragraph reads coherently. Its anchor `#editing-contract-for-this-firmware` resolves.
   - No predecessor-added line restates an NVM figure, a record length or a map-constant name (searched every `+` line of `573f0052..0b81fdc9`). No predecessor-added line cites a line number in a PR-changed file.
3. **Gate inventories and records.**
   - `measure_test_evidence.py` (387b added two dispositions): `--check` and `--selftest` pass. The PR adds no DUT-source reader.
   - `ci_events.py` (predecessors edited `CI_WORKFLOWS.md`): `--check` passes with 1647 contract items, and `--selftest` passes. It pins `check_nvm_record_space.py` and `test_nvm_firmware.py`, which the PR changes.
   - `TESTING.md` and `RUNNING_TESTS.md` (387b) state no nvm_backend count.
   - `git grep` for the old 8x8 image (8,648 B) finds nothing. Every 12,680 B statement is in a PR-owned page.
4. **Stale figures from composition.** None found. One pre-existing figure outside the composition's reach is recorded under "Observation outside this round's scope".

## Gates executed on the candidate

At most 8 in parallel, all in the foreground.

Static batch (`run_static_gates.sh`, `receipts/static/SUMMARY.tsv`): 31 of 31 exit 0.
- The renderer-backed gates ran with the pinned renderer from `tools/markdown/requirements.txt`, hash-installed into a private virtual environment under the scratch directory.
- The documentation gates:
  - `docs_check.py`: 0 findings, 165 md files
  - `check_em_dash.py --base 0b81fdc9...`: 0 findings over 258 added lines in 5 pages, arms 339/339
  - `check_doc_style.py` and its `--selftest`
  - `DOC_MAP.gen.py --check`
  - `gen_toc.py --selftest`, `--verify-anchors` (173 cross-page fragments) and `--check` (107 pages)
  - `check_doc_paths.py`, `gen_module_matrix.py --check`, and `check_feature_status.py` and its `--self-test`
- The NVM gates:
  - `check_nvm_record_space.py`: 0 findings over 5 configs. It reports 8x8 at 156 records, top id 0xE2, a 12,680 B image, commit at most 3.26 s, and K16=10 / boundary=72 decode, cleared-first restore and over-capacity refusal OK on every output port.
  - `check_nvm_record_space.py --self-test`: 18 of 18 named controls.
  - `test_nvm_firmware.py`, with and without `--self-test`.
- The inventory and policy gates:
  - `check_baremetal_only.py --check` and `--selftest`
  - `measure_test_evidence.py --check` and `--selftest`
  - `ci_events.py --check` and `--selftest`
- The idiom and hygiene gates: `check_cpp_idiom.py`, `check_py_idiom.py`, `check_hygiene.py --check`, `check_todo_ownership.py`, `measure_naming.py --check`, `measure_fail_fast.py --check`, `check_rtl_source_lists.py` and `check_archive.py`.
- `git diff --check 0b81fdc9 2ab66c9d`.

Focused native suites, in a disposable git clone of the candidate with submodules checked out at their gitlinks:
- Verilator is `Verilator 5.050 2026-07-01 rev v5.050`, matching the workflow pin `v5.050`.
- `make -C tb/verilator/nvm_backend`: rc 0. 525 checks at 8x8 and 208 at 1x1, 0 failures. The four negative controls (alias, stride, stale_mask, blind_read) are each RED (`receipts/nvm_backend.log`).
- `make -C tb/verilator/nvm_cosim`: rc 0. 465/465 checks, 39 of 39 mutants killed by their named checks, and the identity-wrap controls pass (`receipts/nvm_cosim.log`). This is the suite the PR names as the instrument for a wrong firmware output-length table, run against the composed writer.

Focused builder test, in the review clone: `test_baremetal_profile_contract` only, as above.

## Findings

None. No BLOCKER, MAJOR, MINOR or SUGGESTION is raised against the composition.

## Observation outside this round's scope (not a composition finding)

O1 concerns `docs/design/SAVED_STATE_FASTCONNECT.md:996` (section 8.3, "The area, measured"). It is pre-existing on dev, and this merge neither introduces nor changes it.

- The sentence reads: "at 8x8 the two directions are 72 and 144 framed bytes, and at 1x1 they are 8 and 144".
- The emitted fixtures give different lengths (`records_*.txt`, first MAPS_IN / MAPS_OUT row):

  | Revision | 8x8 in / out (framed bytes) | 1x1 in / out (framed bytes) |
  |---|---|---|
  | base `573f0052` | 8 / 80 | 72 / 144 |
  | candidate | 8 / 584 | 72 / 144 |

- So the sentence was wrong on dev for both 8x8 figures and the 1x1 input figure, and stays wrong at the PR head and the candidate. The line is blamed to `772b2121`, not to this PR. The page's `:835` is the same claim inside a narrative about an earlier round.
- This PR corrected the same inversion in `tb/verilator/nvm_backend/Makefile` and `README.md`. But section 8.3 is outside #501's frozen items (4.2, 4.3, the materialization sizes, and the reviewer-listed figures of the round-2 assignment), and the composition does not touch it.
- No prior review round lists it. R312-1 F3's table covers image totals, not per-record framed lengths.
- **Needs a manager scope decision.** The round-2 assignment (issue #501 comment 5823589125, item 1) says "No saved-state page may size an output map record by cluster count". The 144-byte figure is the framed length of an old 17-cluster output port, and it sits in present tense on a saved-state page.
  - If the manager reads item 1 as page-wide, O1 is a MINOR (Conformance, Docs) against the PR source. The source Conformance and Docs coverage at `efcabc37` would then not clear until it is fixed.
  - If not, it is new work under AGENTS.md section 4 and belongs in a new issue.
  - This composition round does not choose between the two. Either way it does not change whether the composed tree adds a defect beyond the reviewed sources, which is what this verdict answers.

`docs/development/CODE_QUALITY.md:1581-1582` cites `test_builder.py:1439` and `:1557` for `rv32_verdict_edge` and `rv32_unit`. Those functions are at `:1744`/`:1874` at the PR base, `:1749`/`:1879` on live dev, and unchanged by this PR's 1:1 edit. This is also pre-existing on dev, and outside scope.

## Prior public findings on PR #557: disposition at this head

These were read only after the verdict, the ledger and the sections above were written.

Sources: PR #557 comments 5823344017 (R312-1), 5823585783 (R313-1), 5824109822 (R312-2), 5824206585 (R313-2), 5824394329 (R312-3), 5824395155 (R313-3), 5824554040 (R313-4 POSITIVE at `efcabc37`) and 5824566202 (R312-4 POSITIVE at `efcabc37`).

Why the closures carry over to the candidate (`receipts/pr_files_identity.txt`):
- 12 of the PR's 14 files have the same blob and mode at `efcabc37` and at the candidate. That includes all three SAVED_STATE pages, `check_nvm_record_space.py`, `nvm_contract.py`, `nvm_map_checks.py`, `nvm_shape.py`, the firmware and the nvm_backend files.
- The two overlap files carry the PR's delta with an unchanged patch-id.
- So every closure the source rounds verified at `efcabc37` is present byte-for-byte in the candidate.

| Finding | Severity (lenses) | Status at `2ab66c9d` | Evidence in this round |
|---|---|---|---|
| R312-1 F1 = R313-1-F1, writer framing sized by clusters | MAJOR (Conformance, Docs) | RESOLVED, retained closed | MATERIALIZATION blob `421a7295` identical to source, where R312-4 and R313-4 report no open finding |
| R312-1 F2 = R313-1-F3, capture-hold exposure | MAJOR / MINOR (RTL, Robustness, Docs) | RESOLVED as documentation per the corrected decision (#559 owns measurement) | SNAPSHOT_OWNERSHIP blob `dad091ac` identical; `KL_nvm_backend.sv` unchanged; see pending duty on maintainer acceptance |
| R312-1 F3 = R313-1-F2, stale figures | MINOR (Docs; Conformance for R313) | RESOLVED, retained closed | FASTCONNECT/SNAPSHOT/MATERIALIZATION blobs identical. `git grep` for 8,648 finds nothing. `BAREMETAL_FIRMWARE.md:1720` carries the ENTRIES wording in the composed file |
| R313-1-F4, self-test accepts crashes | MINOR (Tests, Docs) | RESOLVED, retained closed | `check_nvm_record_space.py --self-test` on the candidate: 18 of 18 controls, each with its named FINDING (static/13) |
| R312-2 F1 = R313-2-F1, capture copy premise | MAJOR / MINOR (Conformance, RTL, Robustness, Docs) | RESOLVED, retained closed | SNAPSHOT_OWNERSHIP section 18 and UNRESOLVED 6 blob identical |
| R312-3 F1 = R313-3-F1, donor capture-hold sentence | MINOR (Conformance, Docs) | RESOLVED, retained closed | MATERIALIZATION blob identical to `efcabc37`, where both source rounds verified the deletion |
| R312-1 S1/S2 = R313-1-S1/S2 | SUGGESTION (Tests) | Taken at source | `nvm_cosim` on the candidate: 465/465, 39/39 |
| R312-1 S3 | SUGGESTION (Tests) | Not taken; optional | none needed |
| R312-2 S1 (historical row), R313-3-S1 ("at this head" wording), R312-4 S1 (PR body status wording) | SUGGESTION (Docs) | Open, optional; they do not affect coverage | none needed |

No prior BLOCKER, MAJOR or MINOR is open at this head.

## Completion ledger (reviewer-owned)

| Lens | Result | Does the composition touch its scope? Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Composition does not change its scope. The PR's inputs are unchanged across the merge: `amap_edit_validate` block hash `6232a7e4...` at base and candidate, the backend RTL and the gitlinks. `check_nvm_record_space.py` on the candidate shows 72 entries per 8x8 output port, K16 and boundary decode/restore, and the 1x1 digest `103ce107...` held (static/12, 13). Source conformance is covered by the source rounds R312-4 and R313-4, POSITIVE at `efcabc37`. | R312-5 (composition); source R312-4, R313-4 | 2ab66c9d (composition); efcabc37 (source) |
| RTL | CLEAN | No synthesizable RTL in the PR. Predecessor RTL (`milan_datapath.sv`, `milan_csr.sv`, `KL_render_setpoint.sv`, `KL_media_clock_restart.sv`, `KL_crf_tx.sv`) is disjoint from the NVM path, and `KL_nvm_backend.sv` blob `b6dc1f05` is unchanged. Candidate `nvm_backend` (525/208, 4/4 controls) and `nvm_cosim` (465/465, 39/39) pass under Verilator 5.050. Source RTL coverage is R312-4 and R313-4. | R312-5; source R312-4, R313-4 | 2ab66c9d; efcabc37 |
| Robustness | CLEAN | Candidate over-capacity refusal (record-space K16/boundary, one-over refusal), backend one-byte-over read/write refusals and span-exact erase (`sim_main.cpp:761`), and cosim mutants (identity wrap, stale ack, failed slot) all pass. The composition adds no input path. | R312-5; source R312-4, R313-4 | 2ab66c9d; efcabc37 |
| Tests | CLEAN | Composition touches `test_builder.py` (overlap). The focused `test_baremetal_profile_contract` passes on the candidate, and the planted mis-resolution of the overlap makes it fail (probe). Record-space `--self-test` 18/18, `test_nvm_firmware --self-test`, `measure_test_evidence --check/--selftest` and `ci_events --check/--selftest` all pass. | R312-5 | 2ab66c9d |
| Docs | CLEAN | Composition touches `BAREMETAL_FIRMWARE.md` (overlap). The composed text at `:1710-1735` was read. `docs_check`, `check_em_dash --base 0b81fdc9`, `check_doc_style` (+selftest), `DOC_MAP --check`, `gen_toc --selftest/--verify-anchors/--check`, `check_doc_paths` and `gen_module_matrix --check` all pass. No stale macro name or NVM figure comes from composition. O1 is pre-existing and outside scope. | R312-5 | 2ab66c9d |

## Real limits

- Physical calibration was NOT RUN. Field and hardware persistence acceptance remain with #70. Nothing here is hardware proof.
- The full parent, processor, gPTP, Yosys and builder banks were not run (not permitted in this round). Of the builder, only `test_baremetal_profile_contract` ran on the candidate. `milan_dp` and the other Verilator suites were not run on the candidate.
- The hosted contexts listed below are for the PR source head. The candidate `2ab66c9d` has not been pushed, so no hosted run exists for it. No `act` run was made.
- The manager's candidate-bank evidence was not found in a public location at review time. Evidence branch tip `00feb935` holds only author and source-review archives. This round's verdict rests on its own receipts.
- The renderer-backed documentation gates used the pinned wheels in a private virtual environment on this host's interpreter, not the hosted runner's.

## Pending manager duties

- The final current-dev candidate build and full local bar at the merge turn. Live dev is now `c266432d`, tree-equal to this candidate's 387b step. If dev moves again, or the 548 queue entry changes, this composition verdict no longer covers the result.
- Hosted and `act` acceptance on the exact head that merges. At 2026-09-25T00:50Z every exact-head context for the PR source head `efcabc37` was complete and successful: rtl-fast, docs-check, docs-check-no-git, wire-accountability, elaborate, verilator-suites (5 shards) and yosys-portability (4 shards). "Physical gPTP (nightly and manual)" was skipped; that skip is not an executed job.
- Decide O1's scope: under round-2 item 1 in this lane, or a new issue. Route the CODE_QUALITY line citations to an issue if not already tracked.
- Carried from the source rounds (R312-3, restated by R313-4): obtain explicit maintainer acceptance that the modelled 8x8 capture-hold exposure (0.78x under doubled costs) merges with #559 open. This applies unless the manager's corrected decision (issue #501 comment 5824117439) is taken as that acceptance.
- Post-merge containment and closure per CONTRIBUTING.md 2.1 step 7.

Publishable receipts are listed in `MANIFEST.sha256`. The receipts contain local absolute paths of the review host. The scratch directory, including the private renderer environment and the disposable candidate clone, is not published.

R312-5 FINISHED
