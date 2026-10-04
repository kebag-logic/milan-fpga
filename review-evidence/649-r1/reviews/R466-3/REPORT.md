[R466] POSITIVE - exact head 172fd6586e79d3b2471409c31ad089ee5af2f479

Round R466-3 is an internal, cleared-context, independent review of issue #649 / PR #650.

- Tree: `9d62fb9421491153da8d72b6ebd657474f977647`.
- Source base: `241f91845230ae410506dffb16b71937127fd175`.
- Live dev: `fea346e76c2a57ed5cd131af8fc68dfeff57f877`. It is an ancestor of the head and is still the remote tip (`receipts/remote_refs.txt`).

I applied all five lenses at this head. No BLOCKER, MAJOR or MINOR finding is open. Five RESIDUE items are carried: two are new, and three are prior R467-2 residue not yet applied. Seven SUGGESTIONs are listed.

Every prior public finding on this PR is resolved at this head:
- R466-1 F1 to F6;
- R467-1 F1 to F7;
- R466-2 F1.

R467-2 opened no finding.

## Basis

I read, in this order:
- AGENTS.md and CONTRIBUTING.md (sections 3, 5 and 6, with 6.1);
- docs/README.md;
- issue #649: its body, the lane assignment (5976977547), TAKEN, both REVIEW READY comments, and the round-2 assignment with its CPU/cache/L2 ruling (5978713464);
- the authorities the page cites:
  - `docs/design/AREA_BUDGET.md:105-139`;
  - `docs/reference/FR_NFR.md`: FR-CTRL-03, FR-MVU-03, NFR-SCOUT-05, NFR-RES-01;
  - `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:452`;
  - `syn/ooc/pp_resource_baseline.json` `route-1x1`;
  - the RTL lines the page cites;
- `git diff 241f9184..172fd658` (22 commits, including the `--no-ff` merge of dev `fea346e7`);
- the evidence branch `649-review-evidence`, author material only: `review-evidence/649-r2/author/` at `2ff33d3c` and `review-evidence/649-r1/author/` at `096998f8`;
- the manager's evidence comments: PR 5980942776, 5981115521 and 5981117432.

I finished my own pass over the diff, with every probe below, before I read any prior reviewer report. Those reports changed none of my findings. I carry forward three R467-2 residue items that are still unapplied.

**Scope.**
- Against live dev `fea346e7`, the lane touches only `syn/resmap/` (8 new files), `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md` and one row of `docs/findings/README.md`.
- `git diff 241f9184..HEAD` over `hdl protocol-processor gptp-processor third_party configs sw syn/yosys syn/ooc scripts .github` is empty.
- The gitlinks are unchanged.
- The extra files in `241f9184..HEAD` (the tb and design pages) come from the dev merge, not from the lane.
- Round 3 (`4742d2c0..172fd658`) changes 5 lines of the page only. It applies R466-2 F1 and RES1 to RES3.

## Independent evidence at this head

All raw receipts are under `receipts/`, and the portable scripts that produced them are under `scripts/`.

| Check | Result | Receipt |
|---|---|---|
| Cold rerun from the published round-2 `inputs/`, in a `git archive` of the head | Every command exits 0. The five self-tests PASS (map 15 of 15). `resmap_map.py map` prints `TIED: 175 blocks, depth 5; LUT 50767, FF 59634, slices 15832.00, CARRY4 3506, RAMB36 79, RAMB18 27, DSP 14`. The regenerated `models.json` is byte-equal to the published one. `resmap_tables.py ... --page` prints "every table equals a fresh generation". `map.json`, `blocks_ranked.md`, `partition.md`, `lut_sharing.md` and `tables.md` are byte-equal to the published `outputs/`. | `cold_rerun.log` |
| Census provenance | `map_cells.tsv` has 129,909 lines (header plus 129,908 cells, matching the log's `129908 primitive cells written`) and sha256 `b377ddec…`. The committed `route_map.tcl` hashes to the published `tcl.sha256`. The redacted `route_map.log` has original digest `51cc25fd…`, equal to the page's receipt row. Checkpoint digest `769a04bb…` equals #638's round-7 `run-receipts.json` on `234-review-evidence`. `4d81e10d..241f9184` touches only docs and `pp_resource_baseline.json`. | `census_provenance.txt`, `cold_rerun.log` |
| Real-image plants (published inputs; ancestry kept legal) | All 6 plants are refused by the expected tie, and the clean control ties. The plants: a LUT moved between two unrecorded sibling leaves; an FF moved likewise; a census FF re-owned; a census LUT re-owned; a sharing adjustment deepened together with the flat report; flat slices. | `real_plants.log`, `real_plants.json` |
| Code mutants against the scripts' own self-tests | 28 of 32 killed. Every tie, the census LUT tie over parents, the stray-owner check, the depth boundary, the I/O-tile FF split, every guard fail-closed path and exclusion, the rank check, the page check and the SoC variant arithmetic all die. The 4 survivors are listed below. | `mutation_probe.log`, `mutation_probe.json` |
| Elaboration guards re-linted with the pinned Verilator 5.050 (`--version`: `Verilator 5.050 2026-07-01 rev v5.050`) on 12 points, clean tree at this head | 12 of 12 match the published records. Five are refused: `streams-8`, `pp-names-235`, `pp-line-512`, `pp-line-1152` and `pp-ctrl-32`, each with the same messages. Seven are clean: `ship`, `ship-8x8`, `streams-4`, `pp-ship`, `pp-line-768`, `pp-names-128` and `pp-ctrl-12`. The builder accepts `rm_ax7101_8x8_tdm8` (rc 0), and its header carries `AEM_NAME_ENTRIES_C = 235`. The tracked 8x8 header carries 107, 4x4 carries 123 and 1x1 carries 39. | `guard-shapes.log`, `guard-relint.log`, `guard-relint-compare.txt` |
| Vivado anchors | The published `synth_`/`opt_hierarchy.rpt` of the four anchors (8 files) hash to the round-1 receipts. All five anchor runs, including the refused 8x8 TDM8 one, record the `datapath_ooc.tcl` digest `8c654957…`, which equals the committed script. | `anchor-report-digests.txt` |
| Touched docs and quality gates (28) | All rc 0. They include `docs_check` with and without git (0 findings, scrub 23/23) and `check_em_dash` against both bases (0 findings over 1,312 added lines, arms 339/339). Also `gen_toc --check` and `--verify-anchors`, `check_doc_paths` (909 paths), `check_py_idiom`, the hygiene, naming, fail-fast and test-evidence ratchets, `pp_srcs --check --selftest`, `check_rtl_source_lists`, `pp_resource_gate check-baseline` and `git diff --check` against both bases. | `gates-summary.txt`, `gates/*.log` |
| Prose against the generated tables | Every figure in the summary, the map prose, the stream and channel, TDM, optional-block, processor, SoC-variant, redundancy, calibration and opportunity text recomputes from the tables. Examples: 23,904 / 18,296 / 8,567; 3,828 / 2,911 / 1.5; 4,739 then 3,463.5; 10,327.7 below the line; 2.24 to 2.82; 0.9674; 1.129 / 1.157; 12,727; 18 slices; 7,100 / 9,918. The exceptions are RES-A and SUGGESTION S5. | `prose_figure_checks.txt` |
| Hosted, exact head (read only) | `rtl-fast`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0 to 3, Verilator shard 3, `full-ci-gate`, `bdd-conformance`, `wire-accountability`, `docs-check-no-git` and `changes` succeeded. `docs-check`, `elaborate` and Verilator shards 0, 1, 2 and 4 were in progress. `Physical gPTP` was skipped, which is not hardware evidence. | `hosted_checks_snapshot.txt` |

## Findings

No BLOCKER, MAJOR or MINOR finding is open.

### RESIDUE (wording only; each changes no measurement, figure, table, code, test or clause claim)

| ID | Where | Why | Exact fix |
|---|---|---|---|
| RES-A (new) | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:1047` | "Several blocks differ by a factor of four or more" lists `avtp_stream_parser`. Its factor from the page's own table is 1,991 / 519 = 3.84 (`prose_figure_checks.txt`). | "Several blocks differ by a factor of about four or more" |
| RES-B (new) | PR #650 body, Status | The Status names only `4742d2c0`. The head is `172fd658`, and its docs-only commit is not described. | Append: "Round 2b: one docs-only manager commit, `172fd658`, applies R466-2 F1 and RES1 to RES3; no code, figure or table changed, and the table check still reports every table equal to a fresh generation." |
| R467-2 RES-1 (retained, not yet applied) | page `:78`; PR body Round 2 item 1 | "plants a wrong figure per arm: 15 arms". Of the 15 counted arms, one is the clean fixture: 12 `PLANTS` plus 2 record plants plus the fixture (`resmap_map.py:615-628`). | As R467-2 wrote. Page: "builds a small consistent image and requires it to tie (one arm), then plants a wrong figure in each of 14 more arms, each caught by the tie that the arm names." PR body: "(14 planted arms and the clean fixture, 15 in all)". |
| R467-2 RES-4, item-6 half (retained) | PR body Round 2 item 6 | It still says "once published" and "the file is kept for the manager to publish beside it". The census is published as `inputs/map_cells.tsv.xz` (page `:1217`, comment 5980942776). | "published at `67855cfa`, the census as `inputs/map_cells.tsv.xz`" |
| R467-2 RES-5 (retained) | PR body Description (`yosys_sweep.py` row) and Round 2 item 7 | "records HEAD and a clean tree in every receipt". None of the 59 published point receipts or guard records carries a `tree` field (checked over `summary.json`). They predate the change. | Append "(receipts written from round 2 on; the published round-1 receipts predate it)" |

### SUGGESTION

- **S1 (Tests).** The per-leaf slice attribution formula (`resmap_map.py:201-204`) has no self-test arm.
  - A mutant that splits each slice equally instead of by BEL count survives 15 of 15, because only the slice total is asserted.
  - The page publishes slices for all 175 blocks and in the opportunities table.
  - Assert one fixture leaf's attributed share.
- **S2 (Tests).** `yosys_sweep.py` has two unarmed spots:
  - the `require_clean` refusal (`:280-285`): a no-op mutant survives, because the self-test reads `tree_state` but never drives the refusal;
  - the first half of `tie()` (`:599-600`): disabling it survives, because the second half catches the same plant.
- **S3 (Robustness).** `resmap_models.py` silently skips a plan point that is absent from `summary.json` (`:168`, `:231`, `:255`, `:346`).
  - Only the rank check and the generated tables would show it.
  - List or refuse plan points that have no summary entry.
- **S4 (Docs, Conformance).** "Only 1x1 can be routed on this device" (page `:705`, and the PR's "One route" limitation) is inferred from slice arithmetic against the 18 free slices and the repository's binding-slice statement (`AREA_BUDGET.md:120`). No 2x2 route was attempted. Label it as an inference.
- **S5 (Docs).** Page `:1002`, "about 1.5 percent ... at every anchor": the anchors measure 1.54, 1.60, 1.68 and 1.69 percent. Write "1.5 to 1.7 percent".
- **S6 (Docs).** The `tdm-model` table (page `:710-716`) prints the three points but not the fitted per-slot cost and residual that `models.json` holds (0.26 LUT per slot, RMS 1.7). Print the fit row. The prose spread ("within 7 LUTs") is correct.
- **Carried open:** R467-2 S6 (a record-scope-missing arm), S7 (the L2 BRAM fit per KiB without its residual), S8 (a stale `guards.json` after a failed re-lint), and R466-1 S3 = R467-1 S4 (a talker-only or listener-only point), which the lane lists as open.

### Survivors of my mutation probe, accounted for

| Mutant | Status |
|---|---|
| `map-slice-equal-split` | S1 |
| `sweep-require-clean-noop` | S2 |
| `sweep-tie-off` | S2 |
| `models-vivado-depth-off-by-one` | Equivalent: `(indent-1)//2` and `indent//2` agree on every odd indent, and Vivado's report rows are indented 1, 3, 5 and so on. Not a finding. |

## Prior public findings: resolution at this head

| Item | Disposition | My evidence at this head |
|---|---|---|
| R466-1 F1 = R467-1 F1 (tie set, stray owner, depth comment) | Resolved. Partition is an identity (page `:58-63`, `resmap_map.py:13-22`). The census LUT tie reads every row (`:299-314`). The stray-owner arm exists (`:598-601`). The depth comment matches the check (`route_map.tcl:22-24`). | the census-LUT, stray, depth and owner mutants are killed; the real-image LUT-move and census re-owning plants are caught |
| R466-1 F2 = R467-1 F5 (LUT sum) | Resolved: generated table `map-lut-sharing` (51,123 leaves, 17 adjustments -356, 50,767) | cold rerun, byte-equal `lut_sharing.md` |
| R466-1 F3 = R467-1 F6 (curvature) | Resolved: sub-linear at page `:631`, `:681-682` and `:797`; residual signs -,+,+,- (processor) and -,+,- (datapath) | `models.json` from the cold rerun |
| R466-1 F4 = R467-1 F2 (59 points, one census rate) | Resolved: the README row says 59 (52 + 7); 64 lines a second at page `:1115` and `route_map.tcl:59-60` | plan has 59 points; 59 receipt rows totalling 247.9 min |
| R466-1 F5 = R467-1 F7 (guards fail open) | Resolved: `resmap_models.py:148-156`, `:358-365`; per-point handling at `yosys_sweep.py:493-499` | the missing-record, hard-error and four exclusion mutants and the page-check mutant are killed |
| R466-1 F6 = R467-1 F3 (CPU, cache, L2) | Resolved by ruling (b): priced from a scratch recipe copy, labelled, two generation failures recorded with their reason | page `:877-939`; tables regenerate equal from `soc_prices.json` |
| R467-1 F4 (re-runnable receipts) | Resolved | cold rerun |
| R466-2 F1 (SoC directive) | Resolved at `172fd658`. Page `:127` states `synth_design -directive default`, matching the published `soc_ooc.tcl`. Page `:938` states that the 1.13/1.16 factor absorbs the directive change. | `inputs/soc-variants/ship/soc_ooc.tcl` |
| R466-2 RES1 to RES3 | Applied: page `:935`, `:1099` and `:1217`; the PR "How to validate" | page and PR body at head |
| R466-1 RES1 to RES4 = R467-1 RES-1 to RES-5 | Applied: page `:21`, `:24`, `:17` and `:258`; PR Status wording | page at head |
| R467-2 RES-1, RES-4 (item 6), RES-5 | Not yet applied; retained above | page `:78`; PR body |
| R467-2 RES-2, RES-3, RES-4 ("How to validate") | Applied | page `:935`, `:1217`; PR body |
| R466-1 S1, S2, S4 = R467-1 S2, S3, S5 | Taken: clean-tree receipts (refusal unarmed, S2 above), rank check (killed), `ship-8x8` guard record published | `mutation_probe.log`; guard records |

## Lens results (exact head 172fd6586e79d3b2471409c31ad089ee5af2f479)

```text
[R466] PASS Conformance - issue #649 acceptance 1-4 and ruling 5978713464; page :19-28, :58-81, :167-320, :509-574, :577-1094; pp_resource_baseline.json route-1x1 (7 figures, 51 scopes); AREA_BUDGET.md:111-139; FR_NFR.md FR-CTRL-03/FR-MVU-03/NFR-SCOUT-05/NFR-RES-01; 234_...:452 - map tied and reproduced cold; every parameter class priced at >= 3 points or two-valued by construction (render lane, optional blocks, XLEN, core); calibration at 4 anchors; scripts, page and receipts published; no RTL/config/baseline change
[R466] PASS RTL - diff scope (no hdl/configs/sw/syn-ooc/scripts/gitlink change since 241f9184); route_map.tcl (read-only reopen, list-length check); datapath_ooc.tcl (AreaOptimized_high + ExploreArea, Synth 8-4445 promoted; digest equals all five anchor receipts); soc_ooc.tcl (-directive default, now stated); milan_datapath.sv:941, :966-976, :1636, :5596, :5940, :6188; KL_nvm_backend.sv:288-290; KL_aecp_engine.sv:960-967; protocol_processor_top.sv:860 - every RTL fact the page relies on holds; 12 guard verdicts re-derived
[R466] PASS Robustness - resmap_map.py:125-136, :208-228, :299-322; resmap_models.py:127-156, :354-365; resmap_tables.py:226-282, :462-475; yosys_sweep.py:101-117, :128-146, :202-210, :271-286, :456-503, :517-536 - input refusals, fail-closed guards, rank refusal, exactly-once rewrites, ROM re-hash, per-point failure handling; real-image plants all refused (S3 is optional)
[R466] PASS Tests - five self-tests at head (map 15/15); 32 code mutants, 28 killed, survivors accounted (S1, S2, one equivalent); 6 real-image plants refused plus clean control; cold rerun byte-equal; 12-point guard re-lint matches
[R466] PASS Docs - docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md (1,217 lines, prose recomputed against its tables); docs/findings/README.md:25; script headers; PR #650 body; 28 docs/quality gates rc 0 - RESIDUE RES-A, RES-B and R467-2 RES-1/4/5 carried; no wording defect changes a figure or claim
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #649 body, lane comment, ruling 5978713464; page in full; `sweep_plan.json`; `pp_resource_baseline.json` route-1x1; `AREA_BUDGET.md:105-139`; `FR_NFR.md` (4 IDs); `234_...:436-462`; cold-rerun `map.json`/`models.json`/`tables.md`; builder shapes (39/123/235/107 names) | R466-3 | 172fd6586e79d3b2471409c31ad089ee5af2f479 |
| RTL | CLEAN | empty RTL/config/tooling diff since base; `route_map.tcl`; `datapath_ooc.tcl` and its 5 anchor receipt digests; `soc_ooc.tcl`; the cited RTL lines above; 12-point Verilator 5.050 guard re-lint | R466-3 | 172fd6586e79d3b2471409c31ad089ee5af2f479 |
| Robustness | CLEAN | `resmap_map.py`, `resmap_models.py`, `resmap_tables.py`, `yosys_sweep.py`, `soc_sweep.py` refusal and fail-closed paths at the lines above; real-image plants; guard mutants | R466-3 | 172fd6586e79d3b2471409c31ad089ee5af2f479 |
| Tests | CLEAN | five self-tests; `mutation_probe.json` (32 mutants); `real_plants.json` (7 runs); cold rerun; `guard-relint-compare.txt` | R466-3 | 172fd6586e79d3b2471409c31ad089ee5af2f479 |
| Docs | CLEAN (RESIDUE carried) | page (1,217 lines); README row; the five script docstrings; PR #650 body; `gates/*.log` (28 gates) | R466-3 | 172fd6586e79d3b2471409c31ad089ee5af2f479 |

Every lens was applied at the merge-candidate source head itself, so no ancestor coverage is relied on.

## Real limits

- **Not run by me:**
  - No Vivado and no LiteX ran. The route reopen, the four anchors, the refused 8x8 TDM8 anchor and the 20 SoC-variant syntheses are taken from their published reports, digests and receipts.
  - The `Synth 8-6058` stop of the refused anchor is taken from the page; only its log digest `9c2ac5ce…` is published.
  - No Yosys point was re-mapped in this round. Rounds 1 and 2 reproduced points byte-equal, and the RTL and tooling are unchanged since then.
- **Not run on this host:**
  - GNU Make 4.3 is not installed here (4.4.1 is), so `make -C gptp-processor docs` was not run.
  - These self-tests were not run here: `ci_scope`, `ci_events`, `gen_toc`, `check_em_dash`, `check_doc_style`, `check_archive`, `check_feature_status`, `measure_control_flow` and `measure_cohesion`. The lane does not touch those scripts, and the manager's banks cover them.
- **Physical calibration NOT RUN.** Field and physical skips are not hardware proof.
- **Hosted contexts** were only read, and some were still in progress (snapshot above). Hosted and act acceptance is the manager's.
- **Clone restored and verified** (`receipts/clone_restore_check.txt`):
  - HEAD and the index tree equal the exact head and tree;
  - `git status --porcelain --ignored` is empty;
  - all 1,008 tracked non-gitlink blobs re-hash raw to their ids, with matching modes;
  - the gitlinks are at their pins: `gptp-processor 5dce647a`, `protocol-processor 631eeb34`, `third_party/verilog-axis 48ff7a7e`;
  - `external` is uninitialized, as at start, and each submodule worktree is clean.
- **Disposable trees** are under `scratch/` only.

## Pending manager duties

- Carry RES-A, RES-B and R467-2 RES-1, RES-4 (item 6) and RES-5 to the residue checklist.
- File the tooling findings as their own issues:
  - the Yosys flows do not enforce sv2v-converted elaboration guards;
  - the builder accepts an AEM name count above the saved-state backend's 128 (235 at 8x8 TDM8; builder rc 0 here);
  - `milan_soc.py --with-fpu` is a no-op on the VexiiRiscv path.
- Post, or delegate, the issue's summary comment on #229 and #640. Scope item 4 requires it, and it is unposted.
- Hosted and act exact-head acceptance, including `docs-check`, `elaborate` and the Verilator shards still running at the snapshot.
- Build and validate the candidate merge on live dev `fea346e7`, which is already an ancestor of the head.
- Post-merge containment.
- Note that the PR body's "Closes #649" closes the issue while the #229 and #640 comment is still owed.

R466-3 FINISHED
