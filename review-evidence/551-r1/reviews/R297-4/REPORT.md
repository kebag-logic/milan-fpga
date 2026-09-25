[R297] POSITIVE - exact head 0e26e0ac07abf1043ac2712fe39f92de0b34f2dd

# R297-4: composition review of issue #551 / PR #553 on the merge-train candidate

- **Candidate:** `0e26e0ac07abf1043ac2712fe39f92de0b34f2dd`, tree `90218a7ec05d89702ffca25a598ef337df338294`.
  - It merges C_559 `d47a04eb` with PR #553 source head `6e4a3b42`.
- **Predecessors in the candidate:**
  - C_559 `d47a04eb` puts #559 on #443 (`4ee96a61`).
  - #443 sits on the #541 candidate `ec9cf454`.
  - The tree of `ec9cf454` is identical to live dev `fd9e0ebf` (`6cc8996a`).
- **Changes from other lanes:** the PR's merge-base is `864b36f5`. Between it and the candidate, the other lanes' changes are dev #562 (#541), #443 and #559.
- **Scope:** composition acceptance only.
  - The #551 source content already has two independent POSITIVE source reviews at `6e4a3b42`: R296-3 and R297-3.
  - Both are delta rounds on R296-2 and R297-2's full coverage of `f219a5ed`.

## Verdict

**POSITIVE.** The composed tree introduces no defect beyond the reviewed sources, and no finding is open.

- **The merge is exact.**
  - An independent `git merge-tree --write-tree d47a04eb 6e4a3b42` reproduces the candidate tree `90218a7e` exactly.
  - All 10 PR files that no predecessor touched are byte-identical to the source head.
  - In all 5 shared files, #551's added and removed lines are identical in the source diff (`864b36f5..6e4a3b42`) and the composition diff (`d47a04eb..0e26e0ac`).
- **Nothing is lost or shadowed.**
  - No predecessor hunk touches a licence or grant term.
  - No predecessor text brings back ACTIVE-only or residual-window wording.
  - Every executable leg that reads the shared files passes on the composed tree, including each lane's failing arms.

## Overlap inventory (verified)

Evidence: `receipts/files_*.txt`, `receipts/composition_checks.txt`.

| file changed by #551 | also changed by | textual regions | semantic interaction checked |
|---|---|---|---|
| `hdl/milan/milan_datapath.sv` | #443 | Disjoint. #443 has `:1201-1202` (`render_status_w` decl), `:2589` (`.i_render_status`), and `:6153-6154,6164-6168` (tap comment, `g_render_status`). #551 has `:1644-1647`, `:1912-1914`, `:5296-5300`, `:5337` and `:6582-6641`. The licence gate is `:6632-6633`. | No signal is redeclared or shadowed. `render_status_w` is declared once, before its consumer. The gate reads `pp_cd_srp_active_w & pp_cd_srp_sr_admitted_w`, and the latter is declared at `:2276` (dev). xvlog shows 0 first-party findings and lint is at its ratchet (90/90). Every Verilator build is clean apart from the existing `GENUNNAMED` warnings. |
| `tb/verilator/milan_dp/Makefile` | #443 | Disjoint. #443 has `CSR_SRC` (`:112`, `:200`) and `render-csr-controls` (`:434-436`). #551 adds `crflic_probes.vlt` to `CRFLIC_BUILD` (`:270`) and the mutant comment (`:445-447`). | `CRFLIC_BUILD` compiles `$(SRCS)`, which now carries #443's `$(CSR_SRC)`. `crflic`, `crflic-mutants`, `aclk` and `render-csr-controls` all build and pass. The default `run` builds and runs both `obj_crflic` and `obj_aclk`. The unwarmed arm is unconditional (`sim_crf_licence.cpp:1225`). |
| `tb/verilator/milan_dp/README.md` | #443 | Disjoint. #551 has `:27`, `:362` and `:397-475`; #443 has `:953-976`. | The composed-tree run reproduces #551's latency table (`:442-449`) exactly: AAF 5/5 and CRF 3/5 cycles (`receipts/milan_dp_crflic.log:609-967`). |
| `docs/reference/REGISTER_MAP.md` | #443, dev #562 | Disjoint. #551 has `:938`, `:1107-1148` and `:1178-1179`. #443 has `:203`, `:242`, `:1824-1826` and `:1945-1995`. #562 has `:837` (`0x738`). | The Contents entry and anchor for `0x8DC` resolve. `gen_toc --check` and `--verify-anchors` pass (179 cross-page links). docs_check passes in both modes. |
| `CHANGELOG.md` | #443 | Disjoint. #443's section is at `:32`. #551 edits the `licence and LeaveAll scope` section at `:96`. | Both sides' 6 Unreleased sections and all Contents entries are present. The lines of `d47a04eb` missing from the candidate are exactly the lines #551 itself removed (`IDENTICAL`). |

#559's files do not intersect #551's: `ci_events.py`, `docs.yml`, `CI_WORKFLOWS.md`, `nvm_capture_cpu/*` and `TESTING.md`. On the composed tree, `ci_events --check` (1655 items) and `--selftest` pass.

## Executed evidence on the composed tree

All legs used the pinned simulator, Verilator 5.050 rev v5.050 (`receipts/verilator_identity.txt`). Builds used `VERILATOR_JOBS=8` and ran in the foreground.

| command | result | receipt |
|---|---|---|
| `make -C tb/verilator/milan_dp crflic` | rc 0, **415 checks, 0 failures**. `[I]` and `[J]` (unwarmed, changed TSpec) run by default for both sources at both phases. | `milan_dp_crflic.log` |
| `make -C tb/verilator/milan_dp crflic-mutants` | rc 0, **7/7**. The clean leg passes, and all 6 mutants are caught. Three of them remove the real grant. | `milan_dp_crflic_mutants.log` |
| `make -C tb/verilator/milan_dp aclk` (#443 RENDER-CSR) | rc 0, **190 checks, 0 failures** | `milan_dp_aclk.log` |
| `make -C tb/verilator/milan_dp render-csr-controls` (#443) | rc 0, **4/4**. `wrong_fill` and `bit9_window_selection` are caught; `absent_stage` passes. | `milan_dp_render_csr_controls.log` |
| `make -C tb/verilator/milan_dp_render tdm8render` | rc 0, **152 checks, 0 failures** | `milan_dp_render_tdm8render.log` |
| `make -C tb/verilator/milan_dp_render tdm8render-multi` (#443 `RENDER-CSR-MULTI`, called unconditionally at `sim_tdm8_render.cpp:3505`) | rc 0, **65 checks, 0 failures** | `milan_dp_render_tdm8render_multi.log` |
| `behave`, licence feature and full suite | Licence feature 5/5 scenarios. Full suite **14 features, 344 scenarios, 1739 steps**, none failed or skipped. | `bdd_streaming_licence.log`, `bdd_full_suite.log` |
| `docs_check.py`, git mode and no-git mode | rc 0 in both. 0 findings over 166 md files; scrub 23/23 and 22/22. The no-git mode skips only inventory parity. | `gate_docs_check_*.log` |
| `gen_toc.py --check` and `--verify-anchors` | rc 0 for both. 108 pages; 179 links reproduced. | `gate_gen_toc_*.log` |
| `check_em_dash.py --base d47a04eb` | rc 0. 0 findings over 197 added lines in 7 pages; arms 339/339. | `gate_check_em_dash.log` |
| `measure_test_evidence.py --check` | rc 0. Ratchet PASS: 75 ≤ 77, 10 ≤ 10, 0 ≤ 0, 3 ≤ 3. | `gate_measure_test_evidence.log` |
| `gen_module_matrix.py --check` | rc 0. 69 modules, 0 untested; controls 5/5. | `gate_gen_module_matrix_check.log` |
| `xvlog_gate.py --check` and `lint_rtl.py --check` | rc 0 for both. xvlog has 0 first-party findings and 4 pinned-processor findings (equal to the ratchet). Lint is 90 ≤ 90. | `gate_xvlog_gate_check.log`, `gate_lint_rtl_check.log` |
| `ci_events.py --check` and `--selftest` | rc 0 for both. | `gate_ci_events_*.log` |
| `check_doc_style`, `check_doc_paths`, `check_rtl_source_lists`, `check_sv_idiom`, `check_cpp_idiom`, `check_py_idiom`, `git diff --check d47a04eb HEAD` | All rc 0. | `gate_*.log` |

Three gates need the locked Markdown renderer: `gen_toc --check`, `gen_toc --verify-anchors` and `check_em_dash`. They ran under a pre-provisioned interpreter that holds exactly `cmarkgfm 2025.10.22` and `html5lib 1.1` (`tools/markdown/requirements.txt`). The host interpreter lacks the renderer and returns rc 2 "cannot judge". That is an environment limit, not a result. docs_check gives the same result under both interpreters.

## Findings

None.

### Observations outside composition scope

These are not findings and do not affect coverage.

- `docs/testing/TESTING.md:270` still labels the campaign "#530 streaming licence, the three gate mutants". Since #551 it has six.
- `tb/verilator/milan_dp/README.md:914` keeps a dated row: "85 / 0 (2026-09-24 UTC) … its three mutants".

Both lines are byte-identical at source head `6e4a3b42` and at dev `864b36f5` (`receipts/stale_count_provenance.txt`). The composition did not introduce or change them, so they belong to the source reviews. The manager may route them to #495 with the other #551 suggestions.

## Prior public findings on this PR, resolved or retained at the composed head

I read these only after my own pass above.

| finding | status at `0e26e0ac` | evidence |
|---|---|---|
| R296-1 F1 (MAJOR) = R297-1 F1 (MAJOR): stale first-round grant | CLOSED | The processor gitlink is `990f9652` in the candidate, the source and C_559. `[I]` passes for all four source/phase cases (`milan_dp_crflic.log:617-921`). |
| R296-1 F2 (BLOCKER) = R297-1 F2 (MAJOR): the BDD scenario pinned the superseded gate | CLOSED | The feature and step blobs equal the source (`5354d3d2`, `ea20363b`). behave passes 344/0 against the composed `milan_datapath.sv`. |
| R296-1 F3 (MAJOR), R297-1 F3 (MINOR): stale generated traceability | CLOSED | `gen_module_matrix --check` returns rc 0 on the composed tree. |
| R296-1 F4 (MINOR), R297-1 F4 (MINOR): over-claims and ACTIVE-only descriptions | CLOSED | No predecessor hunk touches licence terms, and the tree-wide search for the old wording is empty (`composition_checks.txt`, `semantic_grep*.txt`). |
| R296-2 N1 (MINOR) = R297-2 F1 (MINOR): residual-window comment | CLOSED | The feature blob is unchanged from the source. `git grep -nE "Residual\|pending fix\|previous slope" -- tests/` is empty (`prior_findings_recheck.txt`). |
| R296-2 S2 (SUGGESTION) | CLOSED | README `:468` is unchanged from the source (hunk equality). |
| R296-2 S1, R297-2 S1, R297-2 S2, R296-3 S1 (SUGGESTION) | RETAINED as optional (routed to #495) | The composition does not touch the bench: the `sim_crf_licence.cpp` blob equals the source. |

## Per-lens results

```text
[R297] PASS Conformance - hdl/milan/milan_datapath.sv:6632-6633 at 0e26e0ac; receipts/milan_dp_crflic.log (415/0, [G]-[J] and [INV]); receipts/bdd_*.log; receipts/milan_dp_aclk.log, milan_dp_render_csr_controls.log - checked the composed tree against #551's frozen acceptance: the licence is ACTIVE AND the real per-source grant; a refused changed-TSpec re-declaration shows no licence, no START/STOP pair, no reset and no PDU; the unwarmed arm is required by default. Also checked #443's RENDER_STAT behaviour. Both hold together, and neither lane alters the other's contract.
[R297] PASS RTL - hdl/milan/milan_datapath.sv:1202,2276,2589,5299-5300,6164-6168,6632-6633; receipts/gate_xvlog_gate_check.log, gate_lint_rtl_check.log, milan_dp_crflic.log (build) - checked that #443's render_status_w declaration, CSR port and generate block are disjoint from #551's gate edits. Nothing is redeclared or shadowed. Widths match: N_STREAMS*32 feeds N_LISTENERS_P*32, and the gate uses SRP_TALKERS_C slices. The composed module elaborates under the pinned 5.050 simulator. xvlog shows 0 first-party findings, and lint is at its ratchet.
[R297] PASS Robustness - receipts/milan_dp_crflic.log:617-968 ([I]/[J] for both sources and both round phases, changed and identical TSpecs); receipts/milan_dp_crflic_mutants.log; receipts/milan_dp_render_csr_controls.log (talker and invalid selection, absent stage) - checked that both lanes' refused, unwarmed and feature-absent paths behave on the composed datapath as their sources claim. Each lane's negative arms still fail on it.
[R297] PASS Tests - tb/verilator/milan_dp/Makefile:112,200,270,434-449 and the default run recipe; receipts/milan_dp_*.log, milan_dp_render_*.log, gate_measure_test_evidence.log, gate_gen_module_matrix_check.log - checked that the composed Makefile builds #551's crflic leg (with crflic_probes.vlt and #443's CSR_SRC) and #443's aclk and render-csr-controls legs. Both lanes' mutation and control campaigns detect their defects on the composed tree (7/7, 4/4). The evidence ratchet and module matrix pass, and behave passes 344/0.
[R297] PASS Docs - docs/reference/REGISTER_MAP.md:203,242,938,1107-1148,1178-1179,1824-1826,1945-1995; tb/verilator/milan_dp/README.md:27,397-475,953-976; CHANGELOG.md:11-16,32-171; receipts/gate_docs_check_*.log, gate_gen_toc_*.log, gate_check_em_dash.log, composition_checks.txt - checked that both lanes' rows, sections, Contents entries and anchors coexist. Every CHANGELOG entry from both sides survives. The README latency table matches the composed-tree run. No predecessor text restates ACTIVE-only or residual-window semantics. All doc gates pass.
```

## Reviewer-owned completion ledger

Every lens is in the composition's scope, because shared files fall under each one. This round applied all five to the composed tree.

For #551 content outside the shared files, the covering source reviews are R296-3 and R297-3 at `6e4a3b420e055ef7529ceb16bb2ab5be93c34487`. Those 10 files are byte-identical to the source head. The source reviews rest on R296-2 and R297-2 at `f219a5ed`, and I did not re-derive them.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_datapath.sv:6632-6633`; crflic 415/0 including `[I]`/`[J]`; behave 344/0; #443's aclk and render-csr-controls; issue #551 decision and assignments | R297-4 (composition); R296-3 and R297-3 (source) | `0e26e0ac07abf1043ac2712fe39f92de0b34f2dd` (source: `6e4a3b420e055ef7529ceb16bb2ab5be93c34487`) |
| RTL | CLEAN | composed `milan_datapath.sv` hunks; xvlog; lint; pinned 5.050 elaborations | R297-4; R296-3 and R297-3 | `0e26e0ac07abf1043ac2712fe39f92de0b34f2dd` (source: `6e4a3b420e055ef7529ceb16bb2ab5be93c34487`) |
| Robustness | CLEAN | crflic `[G]`-`[J]`; crflic-mutants 7/7; render-csr-controls 4/4 | R297-4; R296-3 and R297-3 | `0e26e0ac07abf1043ac2712fe39f92de0b34f2dd` (source: `6e4a3b420e055ef7529ceb16bb2ab5be93c34487`) |
| Tests | CLEAN | composed Makefile; all six focused legs; both campaigns; evidence ratchet; module matrix; behave | R297-4; R296-3 and R297-3 | `0e26e0ac07abf1043ac2712fe39f92de0b34f2dd` (source: `6e4a3b420e055ef7529ceb16bb2ab5be93c34487`) |
| Docs | CLEAN | composed regions of REGISTER_MAP, the milan_dp README and CHANGELOG; docs_check in both modes; gen_toc `--check` and `--verify-anchors`; em-dash against `d47a04eb`; doc_style; doc_paths | R297-4; R296-3 and R297-3 | `0e26e0ac07abf1043ac2712fe39f92de0b34f2dd` (source: `6e4a3b420e055ef7529ceb16bb2ab5be93c34487`) |

## Real limits

- **Focused legs only.** I did not run:
  - the full `milan_dp` default sweep;
  - the parent, processor, gPTP, Yosys or builder banks;
  - `render_mutants.py`, `tdm8render-mutants` or `gsi-mutants`;
  - the standalone `tb/verilator/csr` leg. #551 does not touch its inputs (`milan_csr.sv`, `csr/sim_*.cpp`).

  I did not re-execute the manager's source banks at `6e4a3b42`.
- **Build location.** The legs were built inside this review clone. This session did not permit a scratch clone, and an archive export cannot build because the Makefile derives processor sources through git. Afterwards all ignored outputs were removed, and the following were verified (`receipts/post_probe_integrity.txt`):
  - HEAD and tree;
  - the index (`write-tree` = `90218a7e`);
  - the tracked blob hashes and modes (the `ls-files -s` hash equals the `ls-tree -r HEAD` hash);
  - a clean `diff-files` after a full refresh;
  - the gitlinks: `protocol-processor` `990f9652`, `gptp-processor` `e5dcea6e` and `third_party/verilog-axis` `48ff7a7e`, all clean. `external` (`efeb541a`) is uninitialized, as it was found.
- **No hosted evidence for the candidate.** `0e26e0ac` is a local-only commit, and GitHub reports no commit for that SHA.
  - At source head `6e4a3b42` (`receipts/hosted_checks_snapshot.tsv`, 15:13 UTC) there are 19 executed contexts. 18 succeeded; Verilator shard 4/5 was still in progress.
  - "Physical gPTP (nightly and manual)" is a skipped context, not an executed job.
- **Not run.** No Docker, act or host act_ci run was made. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Disposable probes.** The only fault probes were the lanes' own mutation and control campaigns. They mutate temporary source copies. The tracked tree was verified unchanged afterwards.

## Pending manager duties

- **Final candidate.** Build and validate the final current-dev candidate at the merge turn. This review judged the queued order: dev `fd9e0ebf` (tree-equal to `ec9cf454`), then #443, #559 and #551. A different landing order or a dev move invalidates this composition verdict.
- **Hosted and act evidence.** Accept the hosted and act evidence at the exact PR head, including Verilator shard 4/5, which was in progress at capture.
- **Merge and after.** Get explicit maintainer merge authorization, run post-merge containment, close #551 and move it to Done.
- **Optional routing.** Route the retained SUGGESTIONs and the two out-of-scope count observations to #495 if wanted.

## Receipts

- **Scripts:** `scripts/composition_checks.sh`, `scripts/run_leg.sh`, `scripts/run_gates.sh` and `scripts/run_md_gates.sh`.
- **Raw logs:** in `receipts/`. Host paths are replaced by `<CLONE>`, `<PACKET>`, `<PINNED_VERILATOR_5.050>`, `<VERILATOR_IMAGE_ROOT>`, `<MD_VENV>`, `<USER_BIN>` and `<HOME>`.
- **Manifest:** every published file is listed in `MANIFEST.sha256`.

R297-4 FINISHED
