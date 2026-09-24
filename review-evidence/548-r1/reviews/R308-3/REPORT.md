[R308] POSITIVE - exact head 0b81fdc969131b82c535c4a183a78065fd1cd2d8

Round R308-3, composition acceptance for issue #548 / PR #556.
Candidate head `0b81fdc969131b82c535c4a183a78065fd1cd2d8`, tree `3f312155566a7c38094d3b55851e55317756142f`.
Parents: `e1333a144115f074f8e3bdcd1de2d3a29d7f9dfd` is the #387b merge-train candidate, and `8544472a19a4b4d3853d64b15dea22f999372a32` is the reviewed PR source head.
Source merge base: `573f0052a0e4412e81f0845438fcec2086ce5d55`.

Verdict scope: the composed tree adds no defect beyond the reviewed sources.
This round did not re-review the source change; R308-2 and R309-2 did that at `8544472a`.

## Findings

None at any severity: no BLOCKER, MAJOR, MINOR or SUGGESTION.

```text
[R308] PASS Conformance - REGISTER_MAP.md:191,1247,1251-1260; 117_GPTP_SILICON_EVIDENCE.md:468-474,524; milan_datapath.sv:3220; receipts/notify/run_positive.log:148 - composed text and the composed notify leg meet #548 acceptance 2 and decision 5821224656; source patch reproduced exactly (receipts/composition_identity.txt)
[R308] PASS RTL - hdl/milan/milan_datapath.sv, hdl/common/csr/milan_csr.sv; receipts/rtl_comment_equiv.txt - all 137 HDL files comment-stripped identical to the #387b candidate e1333a14 with working controls; lint 90 and xvlog 4 equal to their ratchets
[R308] PASS Robustness - receipts/rtl_comment_equiv.txt; receipts/notify/run_positive.log - no new input, state or reset path in the composed gateware; probe, retry, eviction and survivor graded 147/0 on the #387b RTL
[R308] PASS Tests - tb/verilator/milan_dp/sim_nxn.cpp:1594-1597,1240; receipts/notify/ - composed positive run 147/0; the nonzero-tie mutant fails exactly the new check (147/1); check lists identical
[R308] PASS Docs - REGISTER_MAP.md, 117_GPTP_SILICON_EVIDENCE.md; receipts/gates/, receipts/anchor_probe.txt, receipts/tree_search*.txt - 36/36 gates, including docs_check (both modes), em-dash against e1333a14, gen_toc check, anchors and selftest, and ci_events check and selftest; 84/84 fragment links resolve; no live-count claim
```

## What the composition is

| Check | Result | Receipt |
|---|---|---|
| Candidate tree equals `git merge-tree --write-tree e1333a14 8544472a` | yes, `3f312155...` (clean, no conflict) | `receipts/composition_identity.txt` |
| Composition patch (`e1333a14..0b81fdc9`) equals the source patch (`573f0052..8544472a`) | whole-patch and per-file `git patch-id --stable` identical for all 5 files | `receipts/composition_identity.txt`, `receipts/composition.patch` |
| The other side (`8544472a..0b81fdc9`) equals the predecessor side (`573f0052..e1333a14`) | patch-id identical (`a21a3f8b...`) | `receipts/composition_identity.txt` |
| Gitlinks | `external` `efeb541a`, `gptp-processor` `e5dcea6e`, `protocol-processor` `09f9bf38`, `third_party/verilog-axis` `48ff7a7e`: identical at all three commits | `receipts/composition_identity.txt` |

The source and the predecessor both change three files, confirmed with `git diff --name-only`:

- `docs/reference/REGISTER_MAP.md`: #387b edits the `mr` note (about `:124`). #548 edits the 0x6A4 TOC gloss (`:191`), the 0x6F4 row (`:1247`) and its paragraph (`:1251-1260`). The hunks are disjoint.
- `hdl/milan/milan_datapath.sv`: #387b changes functional RTL around `:3068-3110` (`media_rebase_p_w`, `mcr_restart_p_w`) and `:5934-6027` (`render_recentre_p_w`). #548 changes comments only, at `:1500-1502` and `:3218-3219`. The tie `assign aecp_ctlr_diag = 32'd0;` at `:3220` is unchanged by either side.
- `tb/verilator/milan_dp/sim_nxn.cpp`: #387b edits the per-stream `tgt_r` toggle at about `:3102`. #548 adds one AXI-Lite check at `:1594-1597`, inside `prove_the_departing_controller_monitor`, which is called only when `timed` is set (`:1240`). The hunks are disjoint and so are the legs that run them.

Semantic interactions checked:

- **Functional RTL.** With comments stripped, all 137 tracked HDL files at the candidate are identical to the predecessor candidate `e1333a14`. The only byte changes are in `milan_csr.sv` and `milan_datapath.sv`. The stripper flags a planted nonzero tie and ignores a comment-only edit. As a positive control, it reports functional differences between `573f0052` and `e1333a14` (the #387b RTL). So the composed gateware is exactly the #387b candidate's gateware. Receipt: `receipts/rtl_comment_equiv.txt`.
- **Behaviour on the composed RTL.** I built the timed notification leg (`obj_notify`) from the candidate with the milan_dp Makefile's own recipe and Verilator 5.050, the CI pin. It passes 147 checks with 0 failures, and `[NOTIFY-T] CTLR_DIAG (0x6F4) is STRUCTURAL ZERO after controller traffic = 0x0`. A mutant that changes only `aecp_ctlr_diag` to `32'h01001001` (through the Makefile's `DP_SRC` override) builds and exits 1. Its check list is identical, and exactly that check fails with `got=0x1001001 exp=0x0`. Receipts: `receipts/notify/`.
- **Documentation registries, TOC and anchors.** `gen_toc.py --check` and `--verify-anchors` pass (168 cross-page fragment links). Both changed pages are in that corpus. A separate probe resolves all 84 repository fragment links on the two changed pages, including the new `117_GPTP_SILICON_EVIDENCE.md:474` link to `REGISTER_MAP.md#how-to-read-this-page-now-three-verdicts-and-why-the-distinction-matters`, whose heading is at `:92`. Receipt: `receipts/anchor_probe.txt`.
- **Workflow, gate inventories and pins.** `ci_events.py --check` reports 1647 contract items OK, and `--selftest` passes. The inventory and evidence ratchets pass: `measure_test_evidence --check`, `check_rtl_source_lists`, `pp_srcs --check`, `check_tied_inputs.sh` (29 tied, 0 unjustified) and `lint_rtl --check` (90, equal to the ratchet). `xvlog_gate --check` finds 4, equal to the ratchet. `ci_scope` classifies the composition diff as RTL-relevant (`true`), the same as the source diff. Receipts: `receipts/gates/`, `receipts/ci_scope.txt`.
- **Stale live-count claims.** Excluding frozen `docs/history`, which the composition does not touch, a tree-wide search of the candidate for `CTLR_DIAG|0x6F4|ctlr_diag` finds only STRUCTURAL ZERO statements, the retained CSR port and mux plumbing, the tie, and the new check. A consumer search over `sw tests scripts avdecc tb docs` finds no reader that treats 0x6F4 as a count. Receipts: `receipts/tree_search.txt`, `receipts/tree_search_consumers.txt`.
- **Processor claims at the pinned gitlink.** `protocol-processor` `09f9bf38` contains `hdl/aecp/KL_aecp_notify.sv` and `hdl/aecp/KL_aecp_ca_originator.sv`, both of which implement the 5.4.5.3 CONTROLLER_AVAILABLE monitor. No probe, reply or eviction count output exists under `hdl/`. This matches the new comments at `milan_datapath.sv:1500-1502` and the text at `REGISTER_MAP.md:1255-1257`.

## Gates run on the candidate

All 36 returned 0. The script is `scripts/gates.sh` and the per-gate logs are under `receipts/gates/logs/`. They ran at most 8 in parallel, in the review clone, with `PYTHONDONTWRITEBYTECODE=1`.

- `docs_check.py` in Git mode reports 0 findings over 165 md files. With `GIT_DIR=/dev/null` it also reports 0 findings; its inventory-parity arm is skipped by design in that mode.
- `check_em_dash.py --base e1333a14` (the composition parent) reports 0 findings over 20 added lines. `--base 573f0052` reports 0 over 708 lines, and `--selftest` passes 339 arms.
- `gen_toc.py --check`, `--verify-anchors` and `--selftest` all pass.
- `ci_events.py --check` and `--selftest` both pass.
- Documentation checks: `check_doc_style`, `check_doc_paths`, `check_gptp_docs` (with and without `--with-submodule`), `check_solution_docs`, `check_submodule_docs`, `DOC_MAP.gen.py --check`, `gen_module_matrix.py --check`, `check_feature_status`, `check_hygiene --check` and `check_archive`.
- Code and inventory checks: `check_port_contracts`, `check_soc_sources`, `check_rtl_source_lists`, `check_sv_idiom`, `check_cpp_idiom`, `check_py_idiom`, `measure_naming --check`, `measure_fail_fast --check`, `measure_test_evidence --check`, `check_todo_ownership`, `pp_srcs --check`, `lint_rtl --check` (pinned Verilator 5.050 first on `PATH`), `xvlog_gate --check` and `check_tied_inputs.sh`.
- `git diff --check e1333a14 HEAD` is clean.

The gate scripts need a pinned Markdown renderer. I installed it into a private scratch virtual environment from `tools/markdown/requirements.txt` with `--require-hashes`. Nothing shared was installed.

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The composition touches this lens only through the three shared files. Composed acceptance evidence: the 0x6F4 row, paragraph and gloss (`REGISTER_MAP.md:191,1247,1251-1260`) state STRUCTURAL ZERO. The #117 page (`:468-474,524`) keeps the wire facts and draws no eviction inference. The tie at `milan_datapath.sv:3220` is 0. The notify leg reads 0 at `0x6F4` after controller traffic, and its nonzero mutant fails. The per-file patch identity with the source holds. | R308-3 (composition). Source-content coverage: R308-2 and R309-2 | `0b81fdc969131b82c535c4a183a78065fd1cd2d8` (source rounds: `8544472a19a4b4d3853d64b15dea22f999372a32`) |
| RTL | CLEAN | `hdl/milan/milan_datapath.sv` and `hdl/common/csr/milan_csr.sv`: comment-stripped equality of all 137 HDL files against `e1333a14`, with positive and negative controls. The composed `obj_notify` elaborates and runs on Verilator 5.050. `lint_rtl --check` 90 = ratchet, `xvlog_gate --check` 4 = ratchet, tied inputs 0 unjustified. The #387b `media_rebase_p_w` path is untouched by #548. | R308-3 (composition). Source-content coverage: R308-2 and R309-2 | `0b81fdc969131b82c535c4a183a78065fd1cd2d8` (source rounds: `8544472a19a4b4d3853d64b15dea22f999372a32`) |
| Robustness | CLEAN | The composition adds no new input handling, state or reset path, because the gateware is comment-identical to `e1333a14` (`receipts/rtl_comment_equiv.txt`). The diagnostic word is a constant with no reset, wrap or ordering behaviour. The composed notify leg exercises probe, retry, silence eviction and the survivor across the #387b RTL with 0 failures. | R308-3 (composition). Source-content coverage: R308-2 and R309-2 | `0b81fdc969131b82c535c4a183a78065fd1cd2d8` (source rounds: `8544472a19a4b4d3853d64b15dea22f999372a32`) |
| Tests | CLEAN | `tb/verilator/milan_dp/sim_nxn.cpp:1594-1597`, composed beside #387b's `:3102` edit. The positive run passes 147/0. The mutant (`receipts/notify/mutant.diff`) fails 147/1 on exactly the new check, and both runs have the same check list. `measure_test_evidence --check`, `check_cpp_idiom` and `ci_events` pass. The check sits only in the timed leg (`:1240`), so the untimed legs' counts, such as the README's `obj_nxn` 1679, are unaffected. | R308-3 (composition). Source-content coverage: R308-2 and R309-2 | `0b81fdc969131b82c535c4a183a78065fd1cd2d8` (source rounds: `8544472a19a4b4d3853d64b15dea22f999372a32`) |
| Docs | CLEAN | `docs/reference/REGISTER_MAP.md` (disjoint from #387b's `:124` edit) and `docs/findings/117_GPTP_SILICON_EVIDENCE.md`. Gates: docs_check in both modes, em-dash against the composition parent, gen_toc check, anchors and selftest, doc style and paths, DOC_MAP and the module matrix. The anchor probe resolves 84/84 links. The tree-wide and consumer searches find no live-count claim. `docs/history` is untouched. | R308-3 (composition). Source-content coverage: R308-2 and R309-2 | `0b81fdc969131b82c535c4a183a78065fd1cd2d8` (source rounds: `8544472a19a4b4d3853d64b15dea22f999372a32`) |

All five lenses are within the composition's scope, because the three shared files and the two #548-only files are docs, RTL comments and a test. Each lens was applied to the composed tree in this round.
The source rounds cover the content of the change at `8544472a`. This round covers only what composition could add: overlap, ordering, registries, anchors, inventories and composed behaviour. It found nothing.

## Prior public findings

I read these only after my own pass and the ledger above were written. Sources: the PR comments for R308-1 and R309-1 (both NEGATIVE at `e41703b2`) and R308-2 and R309-2 (both POSITIVE at `8544472a`). Each item is checked at this head in `receipts/prior_findings_at_head.txt`.

| Prior item | Severity and lenses | Status at `0b81fdc9` | Evidence at this head |
|---|---|---|---|
| R308-1-F1 and R309-F1 (the same defect): the CSR address table and read mux still described `CTLR_DIAG` as a live count | MINOR / MAJOR; Conformance, RTL, Docs | **RESOLVED** | `milan_csr.sv:761-765` and `:2397-2401` state STRUCTURAL ZERO, the deleted source, processor ownership and ABI retention. The reserved-word note at `:766-767` is intact. `milan_csr.sv` is byte-identical between `8544472a` and this head, and the predecessor does not touch it. My tree-wide search finds no live-count statement. |
| R308-1-S1 and R309-S1: `axi_read` returns 0 on a read timeout and ignores RRESP | SUGGESTION; Tests, Robustness | **RETAINED** as SUGGESTION | `sim_nxn.cpp:600-640` is identical to `8544472a`. In the composed build the path is shown live at that exact point: the nonzero mutant read `0x1001001` there. |
| R308-1-S2: the 0x6F4 row lacks a "Was: `[31:24]/[23:12]/[11:0]`" layout clause | SUGGESTION; Docs | **RETAINED** as SUGGESTION | The row is unchanged. It sits at `REGISTER_MAP.md:1247` in the composed tree because #387b added 3 lines above it. |
| R309-S2: the listener-ladder "Timers per the reference" line follows the CTLR_DIAG paragraph | SUGGESTION; Docs | **RETAINED** as SUGGESTION, outside #548 scope | Unchanged, now at `REGISTER_MAP.md:1262`. |
| Out-of-scope observation from R308-1: `A_ACMPL_DBG` (0x6E8) is still labelled "RO live" | Not a finding against this PR | Unchanged, at `milan_csr.sv:758` | The register map calls 0x6E8 STRUCTURAL ZERO. A search found no follow-up Issue for this or for the timers line. |

None of these leaves a MINOR, MAJOR or BLOCKER open, and composition changed none of them.

## Real limits

- Physical calibration: NOT RUN. No hardware was touched. Field or physical skips are not hardware proof.
- I did not run the full milan_dp sweep, the parent, processor or gPTP banks, the Yosys gate, the builder bank, `run_all_suites.sh`, `act` or Docker. That was by assignment. The composed gateware is comment-identical to `e1333a14`, so its synthesis and sweep results are those of the #387b candidate. The manager runs and owns them.
- The composed head `0b81fdc9` is not on the remote: the check-runs API answers "No commit found". Hosted evidence exists only for the source head `8544472a`. There, every executed context concluded success: rtl-fast, verilator-suites and its 5 shards, yosys-portability and its 4 shards, yosys-elaboration, elaborate, verilator-lint, wire-accountability, docs-check, docs-check-no-git, bdd-conformance, changes and full-ci-gate. "Physical gPTP (nightly and manual)" was skipped, and that skip is not an execution.
- The PR and issue carry no public manager evidence comment for the composed head. The public evidence tree at `29dce329` (`review-evidence/548-r1`) holds source-head author evidence.
- The notify leg and its mutant were built from a local clone of the candidate, with pinned-gitlink clones of the three submodules, under the unpublished scratch directory. The clone's HEAD and tree were checked equal to the candidate.
- In the build logs, the local install prefix of the pinned Verilator is replaced by `<PINNED_VERILATOR_5.050_PREFIX>`. No other receipt is edited.

## Pending manager duties

- Build the final current-dev candidate from live `dev` (`ffcbd33de70278ae34b533dcbadde0b36c8cba13` at assignment) at the merge turn. If `dev` or the queued predecessors move, this composition verdict does not carry over.
- Record both object IDs and the full CONTRIBUTING step 7 gate results on that candidate: the full Verilator sweep, both repositories' suites, behave, the lint ratchet and Yosys. Also record the hosted and `act` acceptance, which the manager owns.
- File separate Issues, if wanted, for the two out-of-scope observations above: the 0x6E8 "RO live" comment, and the timers line that now follows the CTLR_DIAG paragraph. Neither blocks this PR.
- Merge only with explicit maintainer authorization. After merge, run `check_merge_containment.py` and `check_merge_review_integrity.py`.

## Clone integrity after probes

The review clone is back at the exact head bytes. `receipts/integrity_before.txt` and `receipts/integrity_after.txt` are identical and show:

- HEAD, tree and index tree are all `3f312155...`, and the staged-index hash is unchanged.
- All 884 tracked blobs match their HEAD bytes and modes, with 0 mismatches.
- There are no untracked or ignored entries. A bytecode cache that this round's first help invocation created was removed.
- The gitlinks and the submodule checkouts are at `09f9bf38`, `e5dcea6e` and `48ff7a7e`, and all three are clean.

No source was edited, committed or pushed, and nothing was written to GitHub.

R308-3 FINISHED
