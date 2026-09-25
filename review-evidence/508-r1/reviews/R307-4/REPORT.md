[R307] POSITIVE - exact head b1b334725dcf12e084eaa3bb96b1e6865c052267

Round R307-4: composition acceptance review for issue #508 / PR #560. Reviewer role: [R307], independent, cleared context.

- Candidate: merge-train commit `b1b334725dcf12e084eaa3bb96b1e6865c052267`, tree `2719e15f7238e9c1947f9fffb9154ae8a91a2678`.
- Parents: `b74fb111` (the queued train) and `9d66cfe0` (the PR source head).
- Scope: composition only. The PR source head already has two independent POSITIVE source reviews: R306-3 and R307-3 at `9d66cfe0dc87ffe4a5f45691d5c86b041b050b38`.
- POSITIVE means that the composed tree adds no defect beyond the reviewed sources.

## 1. What was reconstructed

**Authority read.** I read AGENTS.md, then CONTRIBUTING.md step 7 (candidate-merge validation). I then read the #508 issue body and its frozen acceptance 1-6. Next came the public maintainer and manager decisions:
- [5819498419](https://github.com/kebag-logic/milan-fpga/issues/508#issuecomment-5819498419): the assignment;
- 5822047670: the processor follow-up;
- 5825732419: the acceptance-2 reading, ACTIVE with `acmp_status` 0 at bind, then PASSIVE after an unanswered retry;
- 5825850226 and 5826348330: the round scopes.

Last, I read the PR body and the diff `b74fb111..b1b33472` with its history.

**The candidate is the exact automatic merge.** `git merge-tree --write-tree b74fb111 9d66cfe0` reproduces tree `2719e15f`, with no conflict ([receipts/01](receipts/01_composition_identity.txt)).

**Train structure.** The train is #408, #387b, #548, #501, #546, #544 and #532 on dev `573f0052`. The tree after #387b equals dev `c266432d`, which is the PR's merge base. The tree after #501 (`2ab66c9d`) equals live dev `c533b481` byte for byte (`c3183688…`). So the candidate's content is live dev + #546 + #544 + #532 + #508.

**Files changed on both sides since the merge base `c266432d`.** There are exactly five, matching the manager's list:

| File | Train owner(s) | PR change |
|---|---|---|
| `docs/reference/REGISTER_MAP.md` | #548 (CTLR_DIAG structural zero, :1252 and index), #546 (CRF_RATE row, :841) | PP_CTRL[1] "set it on every boot" (:2184); LWSRP published-round prose (:1117, :1140-1143) |
| `docs/testing/TESTING.md` | #546 (crf_rx row, :464) | gsi-mutants campaign row (:267) |
| `hdl/milan/milan_datapath.sv` | #548 (CTLR_DIAG comments :1500, :3219-3221), #546 (`crf_rate_valid_w` :1725, :5502, :5561) | GET_STREAM_INFO gather: selectors 4/5/7 left to the processor (:4780-4800 area) |
| `scripts/measure_test_evidence.py` | #546 (`crf_rx/mutants.py` disposition :597) | three processor and one parent disposition (:601-626) |
| `tb/verilator/milan_dp/sim_nxn.cpp` | #548 (`[NOTIFY-T] CTLR_DIAG` check :1598) | the `[GSI]` G1-G10 section (+660 lines) |

**Every overlapping file is an exact union.** The train's changed lines equal the `9d66cfe0 -> candidate` delta, and the PR's changed lines equal the `b74fb111 -> candidate` delta, for all five files ([receipts/02](receipts/02_overlap_hunk_identity.txt)). Every non-overlapping file's candidate blob equals its side's blob (23 PR-only files, 38 train-only files).

**Semantic interactions beyond shared files.**
1. #548 adds a check inside the same timed `obj_notify` leg that carries the PR's `[GSI]` section. The check shares the leg's clock, check totals and README counts.
2. #546 changes the datapath CRF path, which every `milan_dp` leg elaborates. The PR changes `sim_aclk.cpp`, `sim_main.cpp` and the render leg on the same datapath.
3. #501 changes `scripts/nvm_contract.py`, `nvm_shape.py` and `check_nvm_record_space.py`. `nvm_shape.py` reads processor sources through `pp_srcs.py`. `tb/verilator/nvm_cosim`, which the PR changes, imports `nvm_contract.py` and runs `check_nvm_record_space.py --emit-record-table`. The PR moves the processor pin these read.
4. #544 and #532 change builder, firmware-census, workflow and runner files. They do not intersect the PR's files. They share the gate inventories: `ci_events.py`, `measure_*` ratchets and docs gates.
5. There are shared registries and ratchets: test-evidence dispositions, lint, naming, port contracts, fail-fast, hygiene and idiom budgets. There is also the TOC/anchor inventory and line citations into files the other side changed.

## 2. Executed evidence on the candidate (all foreground; raw logs in `receipts/`)

**Tool identity.** Verilator is the scoped wrapper `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`: `Verilator 5.050 2026-07-01 rev v5.050`, wrapper sha256 `905795b9…`. Yosys is 0.66, which matches the pin. Python is 3.14.7. The documentation gates used a disposable environment with the hash-locked `tools/markdown/requirements.txt` and `tools/hdl_reference/requirements.txt`, plus `wavedrom==2.0.3.post3` and `pyyaml`.

| Receipt | Command | Result |
|---|---|---|
| [10](receipts/10_notify_candidate.log) | `make -C tb/verilator/milan_dp notify` | **381 checks, 0 failures**. The PR head's 380 plus #548's `[NOTIFY-T] CTLR_DIAG` check, which passes at its line 569 of the log |
| [11](receipts/11_gsi_mutants_candidate.log) | `make -C tb/verilator/milan_dp gsi-mutants` | **9/9**: the clean control plus all eight mutants caught on their named checks. Failure counts equal the PR's: 7, 7, 7, 7, 21, 42, 14, and 2 for the duplicate withdrawal |
| [20](receipts/20_static_gates/SUMMARY.tsv) | 82 static gate commands ([script](scripts/run_static_gates.sh)) | **82/82 rc 0** |
| [21](receipts/21_nogit_archive_docs.log) | `git archive` extract, no `.git`, empty gitlink directories: `docs_check.py` and `check_feature_status.py` | 0 findings, rc 0. Only the git inventory-parity arm is skipped, by design |
| [30](receipts/30_milan_dp_run_expanded.txt), [31](receipts/31_milan_dp_sweep/SUMMARY.tsv) | the complete default `make -C tb/verilator/milan_dp run` recipe, expanded and executed command by command ([runner](scripts/run_expanded_range.py)) | **45/45 commands rc 0** (per-leg tallies below) |
| [40](receipts/40_cite_drift.txt) | composition citation-drift probe ([script](scripts/cite_drift_composition.py)) | 0 citations moved by the merge itself (one resolver false positive, adjudicated in the receipt) |
| [50](receipts/50_nvm_cosim_candidate.log) | `make -C tb/verilator/nvm_cosim` | **465/465 checks; 39 of 39 mutants killed by their named check**; identity control red as required |
| [51](receipts/51_nvm_backend_candidate.log) | `make -C tb/verilator/nvm_backend` | 8x8: 525/0; 1x1_tdm8: 208/0; all four negative controls RED as required |
| [52](receipts/52_pp_shadow_candidate.log) | `make -C tb/verilator/pp_shadow` | **371 checks, 0 failures** |
| [53](receipts/53_yosys_elaborate_candidate.log) | `syn/yosys/run.sh --mode elaborate --no-structural` on `milan_datapath`, `KL_pp_shadow` and `KL_gptp_shadow`, plus `syn/ooc/ooc_tcl_selftest.py` | 3/3 PASS; the self-test rc 0 |
| [54](receipts/54_behave_candidate.log) | `cd tests && behave --no-capture -f plain` | 14 features, 344 scenarios, 1739 steps, 0 failed, 0 skipped |
| [55](receipts/55_milan_dp_render_candidate.log) | `make -C tb/verilator/milan_dp_render`. The PR changes `sim_tdm8_render.cpp`, and the suite elaborates the datapath that #546 changed | 152/0 and 60/0; 5/5 control and defect arms |
| [60](receipts/60_prior_findings_recheck.txt) | re-checks of every prior public finding at this head (section 8) | all resolved findings remain resolved |
| [00](receipts/00_baseline_tree_state.txt), [90](receipts/90_final_tree_state.txt) | exact-head state before and after | identical (details in section 6) |

**Default sweep tallies on the candidate** ([31](receipts/31_milan_dp_sweep/SUMMARY.tsv)):

| Leg or campaign | Result |
|---|---|
| `obj_gptp` | 181/0 |
| `obj_gptplat` | 181/0 |
| `gmstep` | 48/0 |
| `obj_dir` | 234/0 |
| `obj_notify` | 381/0 |
| `obj_crflic` | 85/0 |
| `obj_nxn` | 1709/0 |
| `obj_nxndv` | 1711/0 |
| `obj_nxn8` | 3137/0 |
| `obj_nxn4c` | 1709/0 |
| `obj_nolpf` | 234/0 |
| `obj_prune` | 33/0 |
| `obj_ax1x1` | 231/0 |
| `obj_aclk` | 144/0 |
| render mutants | 6/6 |
| gmstep controls | 4/4 |

The sweep's measured command time on this host is about 1,415 s, against the 3,600 s `milan_dp` suite deadline in `scripts/run_all_suites.sh:245`.

**Static gates that read the shared files** ([20](receipts/20_static_gates/)):
- `docs_check.py`: 0 findings over 165 md + 867 text files.
- `check_em_dash.py`: 0 findings with `--base b74fb111` (222 added lines, 9 pages) and with `--base c266432d` (1076 lines, 21 pages), arms 339/339.
- `gen_toc.py`: `--verify-anchors` reproduces 174 fragment links; `--check` and `--selftest` pass.
- `check_doc_paths.py`: 847 cited paths resolve.
- `ci_events.py --check`: 1647 contract items. `--selftest` passes.
- `measure_test_evidence.py`:
  - `--check`: 75 <= 77 suites without a mutation arm, 10 <= 10 unseeded draw sites, 0 <= 0 unexplained DUT-source readers, 3 <= 3 wall-clock-dependent files.
  - `--selftest`: passes.
- `lint_rtl.py --check --self-test`: 90 <= 90.
- `check_port_contracts.py`: every tree at its budget; no identity added.
- `measure_naming.py --check`: 96 recorded.
- `measure_fail_fast.py --check`: 82 <= 84, 4 <= 4, 0 <= 0.
- `check_rtl_source_lists.py`: 106 files, 4 of 4 consumers; processor 35/41 tops with 6 recorded.
- `gen_module_matrix.py --check`: 69 modules.
- `check_nvm_record_space.py`: 0 findings over 5 configs; `--self-test` passes.
- `sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test`: passes.
- Also passing: `pp_srcs.py --check --selftest`, `check_submodule_docs.py`, `submodule_boundaries.gen.py --check`, `check_diagram_pngs.py`, `check_baremetal_only.py --check`, the hygiene and idiom gates, `suite_shards.py --selftest`, `gen_hdl_reference.py`, `syn/ooc/dp_srcs.py` and `git diff --check` from both parents.

## 3. Findings

**F1 - SUGGESTION - Docs, Tests - `tb/verilator/milan_dp/README.md:499` and the table at :501-510.**

*Evidence.* The README reads "Measured on 2026-09-25 UTC: the clean leg passes 380/380 checks". The mutant rows read "N of 380", and the duplicate row reads "2 of 396". In the composed tree the clean leg is 381/0, because #548's `[NOTIFY-T] CTLR_DIAG` check (`sim_nxn.cpp:1598`) runs in the same `obj_notify` leg ([receipts/10](receipts/10_notify_candidate.log)). The campaign reports 381 and 397 ([receipts/11](receipts/11_gsi_mutants_candidate.log)).

*Why this is a suggestion.* The sentence is a dated measurement of the PR head. The same README (:834-840) states that its counts are "pre-merge measurements from the two implementation branches" and that "No count is inferred for their merged tree". `gsi_mutants.py` grades named failing checks, never totals, so no gate misreads the count. Every named failure count is unchanged.

*Impact.* A reader running the leg on the merged tree sees 381 where the page says 380. No verdict changes.

*Optional outcome.* After the merge, a later count refresh could re-measure the leg on the merged head, or attribute the 380 to the PR head `9d66cfe0` explicitly.

*Verification.* `make -C tb/verilator/milan_dp notify gsi-mutants` on the merged head, compared with the page.

No BLOCKER, MAJOR or MINOR finding is open.

## 4. Per-lens coverage (reviewer-owned)

Each lens below was applied to the composed tree. Each line names what was examined at `b1b33472`.

- `[R307] PASS Conformance` - `obj_notify` [GSI] G1-G10 on the candidate ([receipts/10](receipts/10_notify_candidate.log)), `gsi_mutants.py` ([receipts/11](receipts/11_gsi_mutants_candidate.log)), `hdl/milan/milan_datapath.sv:4780-4800`.
  - Checked: acceptance 2-5 as graded by the leg, with 5825732419's reading of acceptance 2. G1 is ACTIVE with 0 at bind; G2 is 7 and 3; G3 is PASSIVE. G4 is DISABLED then COMPLETED; G5-G7 carry the 64-bit bridge IDs and codes per sink. G8 is exactly two pushes per controller with solicited equality; G9 excludes the requester; G10 is reset.
  - Result: all pass alongside #548's CTLR_DIAG check in the same leg. All eight negative controls still fail on their named checks, with unchanged failure counts. The composition touches this lens only through the shared leg and datapath; no protocol behaviour of either side changed.
- `[R307] PASS RTL` - `hdl/milan/milan_datapath.sv` (#546 :1725/:5502/:5561, #548 :1500/:3221, PR's gather), with every `milan_dp` elaboration in the default recipe ([receipts/31](receipts/31_milan_dp_sweep/SUMMARY.tsv)), both `milan_dp_render` elaborations ([receipts/55](receipts/55_milan_dp_render_candidate.log)) and Yosys elaboration of `milan_datapath`, `KL_pp_shadow` and `KL_gptp_shadow` ([receipts/53](receipts/53_yosys_elaborate_candidate.log)).
  - Checked: the union is non-overlapping. The #546 port additions (`rate_valid_o`, `crf_rate_valid_i`) and the PR's gather edits elaborate together in all shapes: 1x1, 4x4, divergent, 8x8 loopback, 4x4 four-channel, LPF-off, pruned, AX 1x1, audio-clock, notify, crflic, gPTP, gPTP-latency and gmstep.
  - Also checked: the whole-tree lint ratchet (90 <= 90), port contracts, naming, fail-fast and the derived source lists.
- `[R307] PASS Robustness` - candidate runs of `tb/verilator/nvm_cosim` ([50](receipts/50_nvm_cosim_candidate.log)), `nvm_backend` ([51](receipts/51_nvm_backend_candidate.log)) and `check_nvm_record_space.py` with its self-test and `test_nvm_firmware.py --self-test` ([20](receipts/20_static_gates/)), plus G8, G10 and the missing-descriptor case in [10](receipts/10_notify_candidate.log).
  - Checked: #501's record-shape, contract and record-space changes against the PR's processor pin at `990f9652` (bounded boot walk, NVM arbiter, abort and deadline). This covers malformed images, the four backend negative controls and 39 of 39 persistence mutants, plus reset, withdrawal and missing-descriptor paths in the composed notify leg.
- `[R307] PASS Tests` - `scripts/measure_test_evidence.py:597-626` (both sides' dispositions), `docs/testing/TESTING.md:267/:464` and the three mutation campaigns on the candidate: gsi 9/9, render 6/6, gmstep 4/4 ([11](receipts/11_gsi_mutants_candidate.log), [31](receipts/31_milan_dp_sweep/)).
  - Checked: the shared registry passes `--check` and `--selftest` with both lanes' entries. The combined ratchets hold (3 <= 3 wall-clock, 0 <= 0 unexplained readers). `suite_shards.py --selftest` and `ci_events.py --check` pass. Each campaign still bites on the composed sources (the datapath-copy mutant's pattern is unique in the merged `milan_datapath.sv`).
  - F1 is a SUGGESTION and does not affect coverage.
- `[R307] PASS Docs` - `docs/reference/REGISTER_MAP.md` (:841, :1117, :1252, :2184), `docs/testing/TESTING.md`, `tb/verilator/milan_dp/README.md`, the 82-command static bank ([20](receipts/20_static_gates/SUMMARY.tsv)), the archive no-git run ([21](receipts/21_nogit_archive_docs.log)) and the citation probe ([40](receipts/40_cite_drift.txt)).
  - Checked: TOC and anchors, em-dash from both bases, links, cited paths, submodule docs and the pinned diagram. The composition moves no line citation by itself: 51 parent-carried citation sites show exactly one source head's state.
  - F1 is a SUGGESTION.

**Ledger** (the composition touches every lens's scope, so every lens was applied here rather than deferred to the source reviews):

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `sim_nxn.cpp` [GSI] G1-G10 and `[NOTIFY-T]` on `obj_notify` (381/0); `gsi_mutants.py` 9/9; `milan_datapath.sv` gather | R307-4 | `b1b334725dcf12e084eaa3bb96b1e6865c052267` |
| RTL | CLEAN | `milan_datapath.sv` union; all default `milan_dp` elaborations; `milan_dp_render` 152/0, 60/0, 5/5; Yosys elaborate 3/3; lint 90<=90; port-contract, naming, fail-fast and source-list gates | R307-4 | `b1b334725dcf12e084eaa3bb96b1e6865c052267` |
| Robustness | CLEAN | `nvm_cosim` 465/465 + 39/39; `nvm_backend` 525/0, 208/0, 4 controls; `check_nvm_record_space` + self-test; `test_nvm_firmware` self-test; G8/G10/missing descriptor | R307-4 | `b1b334725dcf12e084eaa3bb96b1e6865c052267` |
| Tests | CLEAN (F1 SUGGESTION only) | `measure_test_evidence.py` check/selftest; gsi, render and gmstep campaigns; the full default sweep 45/45; `suite_shards`; `ci_events` | R307-4 | `b1b334725dcf12e084eaa3bb96b1e6865c052267` |
| Docs | CLEAN (F1 SUGGESTION only) | REGISTER_MAP, TESTING and README union; 82 static gates; no-git archive; citation-drift probe | R307-4 | `b1b334725dcf12e084eaa3bb96b1e6865c052267` |

For content that is PR-only and unchanged in the candidate (the 23 PR-only files are byte-equal to `9d66cfe0`), source coverage remains with R306-3 and R307-3 at `9d66cfe0dc87ffe4a5f45691d5c86b041b050b38`. For train-only files (38, byte-equal to `b74fb111`), it remains with those lanes' own reviews. This round's CLEAN results concern the composition.

## 5. Real limits

1. **Not the final current-dev candidate.** This clone's first-parent chain is the manager's train on `573f0052`, not a merge onto live dev commit `c533b481`. Its content equals live dev plus #546, #544, #532 and #508, because the post-#501 tree equals `c533b481`'s. The manager still builds and validates the final current-dev candidate at the merge turn.
2. **Not run:**
   - the builder (`sw/builder/test_builder.py`, both modes);
   - the RV32 SDK and compiler controls;
   - the full Yosys synthesis bank, the full parent `run_all_suites.sh`, the processor and gPTP banks;
   - the host `act_ci` runner and its self-test;
   - `make -C gptp-processor docs`;
   - `milan_dp_gptp` (physical);
   - the render suite's separate `tdm8render-mutants` target;
   - #546's `crf_rx`, `mmcm_servo` and `mmcm_servo_autorepair` suites, which read none of the PR's files.

   The manager reports its own source static/builder and native banks as passing. This round did not reproduce them.
3. **Hosted evidence is for the source head only.** The candidate commit is not on the remote; the API answers "No commit found". Hosted contexts exist for the PR source head `9d66cfe0`: 21 completed with success, and "Physical gPTP (nightly and manual)" was skipped. Those runs test GitHub's merge with the dev of that time, not this train. Physical calibration was NOT RUN, and skipped field contexts are not hardware proof.
4. **Tool deviation.** The local `sv2v` is v0.0.13; the workflows pin v0.0.12. The Yosys elaboration, `check_rtl_source_lists.py` and `dp_srcs.py` results used v0.0.13.
5. **Process deviations, disclosed.**
   - The fourth sweep chunk exceeded the foreground time limit and continued detached. While it ran, I removed its render-campaign temporary directory, not knowing it was live. That attempt's `render_mutants.py` therefore ended rc 1 ([cmd43-interrupted-first-attempt.log](receipts/31_milan_dp_sweep/cmd43-interrupted-first-attempt.log); summary row `43 1 276`).
   - I reran `render_mutants.py` in the foreground: 6/6, rc 0. The detached chunk's `gmstep_mutants.py` completed rc 0 (4/4) concurrently with that rerun.
   - `render_mutants.py` and `gmstep_mutants.py` call `make` without `VERILATOR_JOBS`, so their Verilator builds used the recipe default `-j 0` (all cores). Together with the overlap, this exceeded the 8-parallel-job allowance for part of that window. The `nvm_*`, `pp_shadow`, `milan_dp_render` and Yosys runs were bounded with `taskset -c 0-7`.
   - The shared `/data` filesystem filled to 100% during the first `nvm_cosim` attempt: one mutant's compiler temp write failed with "No space left on device" ([attempt 1](receipts/50_nvm_cosim_candidate-attempt1-disk-full.log)). I freed this clone's ignored build products, and the rerun passed.
   - No result counted above comes from an interrupted or host-faulted run.

## 6. Clone restoration

The pre-run state ([00](receipts/00_baseline_tree_state.txt)) and the post-run state ([90](receipts/90_final_tree_state.txt)) are identical:
- HEAD `b1b33472`, tree and index tree `2719e15f`;
- `git ls-files -s` sha256 `2d9a6169…`;
- 846 files of mode 100644, 45 of mode 100755 and 4 gitlinks;
- `git diff --quiet HEAD` and `git diff --cached --quiet HEAD` exit 0;
- no untracked or ignored files in the superproject;
- `protocol-processor` at `990f9652`, `gptp-processor` at `e5dcea6e` and `third_party/verilog-axis` at `48ff7a7e`, each with zero status lines including ignored. `external` is uninitialised, as at the start.

## 7. Pending manager duties

- Build and gate the final current-dev candidate at the merge turn (CONTRIBUTING step 7).
- Hosted and act acceptance at the merged head.
- The builder in both modes.
- Post-merge containment and the review-integrity audit.
- Maintainer merge authorization.
- Optionally act on F1 in a later count refresh.

## 8. Prior public review findings on this PR

This section was written after the verdict, findings and ledger above were fixed. It reads only the finding and disposition lines of the earlier rounds, which are public on the PR. Each finding is re-checked at `b1b33472` ([receipts/60](receipts/60_prior_findings_recheck.txt)). None changes the verdict.

| Prior finding | Status at `b1b33472` | Evidence at this head |
|---|---|---|
| Round-1 author-declared docs-check BLOCKER (5822002238, decided 5822047670) | **RESOLVED** | `check_port_contracts.py`, `measure_naming.py --check` and `measure_test_evidence.py --check` rc 0, with #546's disposition added ([20](receipts/20_static_gates/SUMMARY.tsv) rows 39, 41, 47) |
| R307-1 F1 = R306-1 F1 (MINOR, Docs): processor #116/#113 lines in the historical `CHANGELOG.md` section | **RESOLVED** | CHANGELOG blob equals the PR head's; no train commit touches it. The "licence and LeaveAll scope" section is byte-identical to `c266432d`'s. Issues 116 and 113 appear once each (:51, :53), in the `990f9652` section |
| R307-1 F2 = R306-1 F4 (MINOR, Conformance): acceptance 2 "PASSIVE after bind" | **RESOLVED** by decision 5825732419 | G1 ACTIVE/`acmp_status` 0 on bind and G3 PASSIVE after the unanswered retry pass in the composed leg ([10](receipts/10_notify_candidate.log)) |
| R306-1 F2 (MINOR, Docs): stale processor line citations | **RESOLVED** | The gitlink is unchanged from the PR head (`990f9652`). `pp_shadow/sim_main.cpp` is byte-equal to the PR head. The processor-citation set in `milan_datapath.sv` is identical to the PR head's. The citation probe moves nothing ([40](receipts/40_cite_drift.txt)) |
| R306-1 F3 = R307-1 S1 (MINOR/SUGGESTION): G8 withdrawal push count ungraded | **RESOLVED** | The G8 exact-count and per-push checks pass (381/0). The duplicate-withdrawal mutant fails both named G8 counts ([11](receipts/11_gsi_mutants_candidate.log)) |
| R306-2 F1 (BLOCKER) = R307-2 F1 (MAJOR), Docs/Tests: README:488 relative links into the processor submodule | **RESOLVED** | No relative `protocol-processor/` link in the README (grep rc 1). Both links are blob URLs pinned at `990f9652` with their fragments. The `git archive` `docs_check.py` returns 0 findings ([21](receipts/21_nogit_archive_docs.log)) |
| R306-2 F2 = R307-2 F2 (MINOR, Docs): campaign described as seven arms | **RESOLVED** | No "seven" campaign wording in the four named files (grep rc 1). Executed campaign: 8 mutants + clean = 9 runs ([11](receipts/11_gsi_mutants_candidate.log)) |
| R307-1 S2 = R306-1 S1, R306-1 S2/S3 (SUGGESTION) | **RETAINED** as SUGGESTION | Artifacts unchanged by the composition. The render file is byte-equal to the PR head's |
| R306-2 S1/S2 (SUGGESTION) | **RETAINED** as SUGGESTION | `sim_nxn.cpp`'s [GSI] hunks and the processor pin are unchanged by the composition |
| R307-2 S1 (ordinal G8 labels) and S2 (`README.md:849` dated 345/0 row), SUGGESTION | **RETAINED** as SUGGESTION | This round's F1 is the same class of observation, the dated README counts. The composition adds one check to the leg those counts describe |

No prior BLOCKER, MAJOR or MINOR is reopened by the composition.

R307-4 FINISHED
