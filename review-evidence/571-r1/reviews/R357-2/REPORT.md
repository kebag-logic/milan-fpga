[R357] POSITIVE - exact head b16e9dadb5a7c6c5cd38852faea9a5c4fdbbd5f5

# R357-2: composition review of the #571 merge-train candidate (PR #597)

- Role: independent composition reviewer, cleared context, round R357-2.
- Candidate: `b16e9dadb5a7c6c5cd38852faea9a5c4fdbbd5f5`, tree `5c28ef6817aa920e696de985a83bdac3eebb3c33`.
  Parents: C_580 `da3f492ece88e81ac50a2801730973f2b32e376b` (dev `2a2a7bb6` + #396 + #397 + #580) and PR #597 source head `f8a52f919bd309960046330a5af127b56731cb27`.
- Scope: composition acceptance only. The source head already carries POSITIVE reviews R356-1 and R357-1 at `f8a52f91`.
- Verdict: **POSITIVE**. The composed tree introduces no defect beyond the reviewed sources. No BLOCKER, MAJOR or MINOR finding. One new SUGGESTION (C1). All five prior SUGGESTIONs are retained unchanged. None affects coverage.

## 1. What the composition is

- The candidate tree is the clean automatic merge of C_580 and the PR head. `git merge-tree --write-tree da3f492e f8a52f91` yields exactly `5c28ef68`, so the merge commit adds no manual edit (`receipts/merge_composition.txt`).
- The PR changes 12 files (`receipts/pr597_source_files.txt`). The predecessors change 33 paths between dev `2a2a7bb6` and C_580 (`receipts/predecessor_files.txt`).
- **Exactly one file is changed by both**: `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` (`receipts/overlap_files.txt`).
- Candidate vs PR head differs by exactly the predecessor path set, and candidate vs C_580 by exactly the PR path set (`receipts/merge_composition.txt`).
- Both hunks on the shared page survive verbatim. The PR's +/- lines from `2a2a7bb6..f8a52f91` equal those from `da3f492e..b16e9dad`, and #580's from `2a2a7bb6..da3f492e` equal those from `f8a52f91..b16e9dad` (`receipts/page_hunk_preservation.txt`).
- The predecessors touch nothing under `hdl/`, `configs/`, `sw/`, or the two shape-gate scripts. The candidate equals the PR head byte for byte on all of those paths (`receipts/rtl_path_identity.txt`).
- The one semantic, non-textual interaction is the **processor gitlink**. The PR was written against `870ff88a`, and the candidate carries #580's `16be6768` (`receipts/restore_integrity.txt`).

## 2. Manager questions, answered

### (1) Is the composed page coherent?

Yes. Evidence is from `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` at the candidate:

- #571's unit-count paragraph and table are at `:49-70`, inside "Ownership boundary". #580's text is elsewhere on the page:
  - audit-pin wording at `:5`;
  - L1/L2 rows at `:84-85`;
  - F07.2 disposition at `:161-165`;
  - audit-pin probe note at `:196-197`;
  - F5/F7 rows at `:278,280`;
  - `[cluster-decision]`/`[cluster-fix]` definitions at `:334-335`.
- No statement contradicts another:
  - #571 says the parent emits one AUDIO_UNIT, CLOCK_DOMAIN and CONTROL per image and zero is unreachable. #580's L1 row says "Single AUDIO_UNIT/domain".
  - #580's F5 is about the Milan 5.3.3.8 cluster minimum on 8x8 input pools. It makes no claim about unit counts.
  - #580's F7 covers packer body/key refusal, which #571 does not touch.
  - #571 cites Milan 5.3.3 for the mandatory descriptor classes. #580 cites 5.3.2 (L1) and 5.3.3.10 (L8). These are different clauses for different claims, and R357-1 S1 already records the precision nit.
- Anchors and cross-references all resolve on the candidate:
  - `gen_toc.py --check` OK, 113 pages (`receipts/gen_toc_check.txt`).
  - `gen_toc.py --verify-anchors` reproduced 188 cross-page fragment links (`receipts/gen_toc_anchors.txt`).
  - `check_doc_paths.py` resolved 850 cited paths (`receipts/doc_paths.txt`).
  - `docs_check.py` found 0 findings (`receipts/docs_check_venv.txt`).
  - `check_em_dash.py` found 0 findings with `--base da3f492e` (23 added lines, the composed #571 delta) and with `--base 2a2a7bb6` (957 added lines, whole train), plus `--selftest` 339/339 (`receipts/em_dash_*.txt`).
  - `check_doc_style.py` OK (`receipts/doc_style.txt`).
- The page's in-page `#follow-up-allocation` links resolve to `## Follow-up allocation` at `:266`.

### (2) Do #571's processor claims hold at `16be6768`?

Yes. The one citation pinned to `870ff88a` still matches.

- `870ff88a` is an ancestor of `16be6768`. Four commits separate them, touching 6 files (`receipts/pp_870ff88a_to_16be6768_stat.txt`).
- Under `hdl/`, only `hdl/aecp/desc/gen_desc_image.py` changed (the packer body/key refusal). **Every `.sv`/`.svh` is byte-identical**, including `hdl/top/protocol_processor_top.sv` and `hdl/aecp/KL_aecp_dyn_state.sv` (`receipts/pp_params_at_16be6768.txt`).
- At `16be6768`:
  - `protocol_processor_top.sv:81-83` declares `N_AUDIO_UNIT_P`, `N_CLK_DOMAIN_P` and `N_CONTROL_P`, and `:3346-3348` forwards them to the dynamic-state store.
  - `KL_aecp_dyn_state.sv:80-82` declares them. They size `rate_r`, `clksrc_r` and `ident_r` (`:164,172-173,177`), set the per-selector counts (`:193-198`) and drive the reset loops (`:269-276`).
- `integrator.md` did change between the pins (+17/-2, `receipts/pp_integrator_diff.txt`), but only in section 6 (entity-model identity, talker/listener maxima, `identify_index_i`). The cited `<a id="integration-parameters"></a>` is at `:48` at both pins, and the three inventory rows at `:68-70` are byte-identical (`receipts/pp_integrator_anchor_and_params.txt`, `receipts/pp_integrator_headings.txt`).
- The citation is therefore accurate at the candidate pin, so it is not a finding. Its SHA no longer equals the gitlink, which is recorded as SUGGESTION C1.

### (3) Does the composed RTL elaborate and bind the three counts?

Yes, verified by elaboration, not only by text inspection.

- **Elaboration probe** (`elab_probe.py`, `receipts/binding_mutants.txt`, mutant `none`):
  - Verilator 5.050 `--json-only` elaborates `milan_datapath` on the candidate. It uses the repository lint gate's own source list and include order, with 0 `%Error` lines.
  - It then reads the elaborated `KL_aecp_dyn_state` constants. At the shipping `endstation_arty_current` shape they are `1/1/1`.
  - With a synthetic copy of that header carrying AUDIO_UNIT=2, CLOCK_DOMAIN=3, CONTROL=4, they are **`2/3/4`**. Distinct generated constants reach the matching processor parameters through both hops.
- **Mutants** (`binding_mutants.sh`, in place, restored after each):
  - swap CLOCK_DOMAIN/CONTROL at `u_pp`;
  - drop `N_CONTROL_P` at `u_pp`;
  - literal `1` for `N_AUDIO_UNIT_P` at `u_pp`;
  - swap AUDIO_UNIT/CONTROL at `pp_shadow`.
  
  Each mutant still elaborates cleanly at the shipping shape, which shows equal shipping counts cannot expose it. Each is killed twice: by the elaboration probe (synthetic values `2/4/3`, `2/3/1`, `1/3/4`, `4/3/2`) and by `check_entity_shape.py` (named `[FAIL] ... derives from ...` rows).
- **Gates on the candidate:**
  - `check_entity_shape.py` passes 166/0. Per configuration, `AEM_N_{AUDIO_UNIT,CLKDOM,CONTROL}_C == census` and `generated ROM {kind} descriptors`, for all five configurations (`receipts/entity_shape.txt`).
  - `check_entity_shape.py --self-test` passes 219/0, including the distinct 2/3/4 census, literal, zero-census, unbound and swap arms at both hops (`receipts/entity_shape_selftest.txt`).
  - The self-test includes the "configs/generated copy is current" checks, so the committed five-configuration headers still match what the builder emits on the candidate. That is the five-configuration identity.
- **RTL lint ratchet** with the pinned Verilator: `LINT GATE: PASS (90 violation(s) <= ratchet 90; 17 waived, 0 justified lint_off)` (`receipts/lint_rtl_check.txt`).

### (4) Do #396 or #397 interact with the unit-count binding?

No.

- I searched every predecessor-changed text path for the PR's paths and symbols (`receipts/predecessor_interaction_grep.txt`). The matches are all:
  - prose naming `KL_pp_shadow`/`milan_datapath` in saved-state and testing documents, none of which describes the `u_pp` parameter map;
  - pin notes (`docs/reference/SUBMODULES.md:25,57`, `docs/design/SAVED_STATE_MATERIALIZATION.md:232`, consistent with the `16be6768` gitlink);
  - one invocation of `check_entity_shape.py --self-test` in `docs/findings/397_SERVICE_BUDGET.md:389`, which the candidate passes.
- #396/#397 touch no RTL, builder, configuration or shape-gate file.
- Their registries and inventories pass on the candidate:
  - `ci_events.py --check` OK, 1655 items, including the `.github/workflows/docs.yml:449` entity-shape step; `--selftest` PASS, 2206 arms (`receipts/ci_events_*.txt`);
  - `measure_test_evidence.py --check` PASS (`receipts/measure_test_evidence_check.txt`);
  - `check_hygiene.py` rc 0 and `check_py_idiom.py` rc 0 (`receipts/check_hygiene.txt`, `receipts/check_py_idiom.txt`);
  - `check_submodule_docs.py` OK, 4 exact gitlinks (`receipts/check_submodule_docs.txt`).
- `syn/yosys/rom_digests.tsv` (#580) keys processor ROM hex by pin. #571 changes no ROM image, only one `localparam` line per generated header.

## 3. Findings

```text
[R357] SUGGESTION Docs — docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:52,70 — C1: processor inventory link pinned to 870ff88a while the composed gitlink is 16be6768
Requirement/evidence: the [integration-parameters] definition (:70) links integrator.md at 870ff88a. On the candidate the processor gitlink is 16be6768 (docs/reference/SUBMODULES.md:25), and the same page's F7 row (:280) names 16be6768 as the adopted pin. The cited anchor (integrator.md:48) and the three rows (:68-70) are byte-identical at both pins (receipts/pp_integrator_anchor_and_params.txt), so the link is accurate. Only its SHA is behind.
Impact: none on correctness. A reader sees a third processor revision on the page with no label saying why.
Required change: optional. Repin the link to 16be6768f710e79450aace277abacd6c2c3336e5, or leave it. This is a Docs-only follow-up, not a merge condition.
Verification: gen_toc.py --verify-anchors and docs_check.py stay rc 0; the anchor resolves at the new pin.
```

Prior public findings on PR #597 were read after this round's own pass. The candidate is byte-identical to `f8a52f91` on every file those findings cite, and page lines `:49-70` are unchanged by the merge. All are SUGGESTIONs and are **retained unchanged**:

- R356 SUGGESTION Docs, page `:62-63,70` (forward-referenced abbreviations, mid-page link definition): retained.
- R356 SUGGESTION Docs/RTL, `hdl/milan/KL_pp_shadow.sv:227-239` (group comment): retained.
- R357-1 S1 Docs, page `:49,61,66` (clause precision): retained. The composed page adds #580's 5.3.3.8 citation elsewhere without changing this.
- R357-1 S2 Tests, `tb/verilator/nvm_cosim/cosim_top.sv:193` (literal `N_CONTROL_P (1)`): retained. It predates the train, and the train does not touch it.
- R357-1 S3 RTL/Docs, `hdl/milan/KL_pp_shadow.sv:227-239`: retained.

No BLOCKER, MAJOR or MINOR finding is open from any round.

## 4. Per-lens results

```text
[R357] PASS Conformance — docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:49-70 at b16e9dad; protocol-processor@16be6768 hdl/top/protocol_processor_top.sv:81-83,3346-3348, hdl/aecp/KL_aecp_dyn_state.sv:80-82,164-198, docs/guides/integrator.md:48,68-70 — issue #571 acceptance 1-3 and assignment scope rechecked against the new processor pin; every #571 processor claim holds there (processor .sv byte-identical to 870ff88a); five-config census/ROM/header identity 166/0 on the candidate.
[R357] PASS RTL — hdl/milan/milan_datapath.sv:7426-7429, hdl/milan/KL_pp_shadow.sv:236-239,1059-1062 elaborated with protocol-processor@16be6768 — clean milan_datapath elaboration; KL_aecp_dyn_state constants 1/1/1 shipping and 2/3/4 synthetic; lint ratchet 90<=90; no predecessor touches hdl/.
[R357] PASS Robustness — entity_shape_selftest zero-census and literal arms (receipts/entity_shape_selftest.txt), protocol-processor@16be6768 hdl/aecp/KL_aecp_dyn_state.sv:154-158 width clamps — composition changes no builder, config or parent RTL input; processor handling of each count is byte-identical to the reviewed pin; zero-count reachability rests on unchanged builder code.
[R357] PASS Tests — scripts/check_entity_shape.py:171-176,372-402,413,558,576; scripts/entity_shape_selftest.py:598-664; .github/workflows/docs.yml:449 via ci_events.py — gate 166/0 and self-test 219/0 on the candidate; 4 reviewer mutants each killed by the gate and by an independent elaboration probe; ci_events inventory and measure_test_evidence ratchet pass with the predecessors' changes present.
[R357] PASS Docs — docs/reference/PP_DESCRIPTOR_OWNERSHIP.md (whole composed page) — both hunks preserved verbatim; no contradiction between #571's unit-count text and #580's pin/F5/F7 text; TOC, anchors, doc paths, docs_check, em-dash (both bases), doc style all rc 0; one SUGGESTION (C1).
```

## 5. Completion ledger (reviewer-owned)

| Lens | Status | Composition touches scope? | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|---|
| Conformance | CLEAN | Yes. The processor pin under the cited contract moved. | Page `:49-70`; processor `integrator.md:48,68-70`, `protocol_processor_top.sv:81-83,3346-3348`, `KL_aecp_dyn_state.sv:80-82,164-198` at `16be6768`; `receipts/entity_shape.txt` | R357-2 | b16e9dadb5a7c6c5cd38852faea9a5c4fdbbd5f5 |
| RTL | CLEAN | Yes. The binding now elaborates against processor `16be6768`. | `milan_datapath.sv:7426-7429`, `KL_pp_shadow.sv:236-239,1059-1062`; `receipts/binding_mutants.txt`, `receipts/lint_rtl_check.txt`, `receipts/pp_params_at_16be6768.txt` | R357-2 | b16e9dadb5a7c6c5cd38852faea9a5c4fdbbd5f5 |
| Robustness | CLEAN | Only through the pin, which leaves every processor `.sv` byte-identical. Source-level depth is covered by R356-1 and R357-1 at `f8a52f91`. | Self-test zero-census/literal arms; `KL_aecp_dyn_state.sv:154-158`; `receipts/rtl_path_identity.txt` | R357-2 (re-applied); source R356-1, R357-1 | b16e9dadb5a7c6c5cd38852faea9a5c4fdbbd5f5 |
| Tests | CLEAN | Yes. The gates now run beside the predecessors' inventories. | `check_entity_shape.py`, `entity_shape_selftest.py`, `ci_events.py`, `measure_test_evidence.py`; `receipts/binding_mutants.txt` | R357-2 | b16e9dadb5a7c6c5cd38852faea9a5c4fdbbd5f5 |
| Docs | CLEAN (SUGGESTION C1 plus retained SUGGESTIONs) | Yes. This is the only file both lanes edited. | Composed `PP_DESCRIPTOR_OWNERSHIP.md`; `receipts/page_hunk_preservation.txt`, `gen_toc_*.txt`, `em_dash_*.txt`, `docs_check_venv.txt`, `doc_paths.txt`, `doc_style.txt` | R357-2 | b16e9dadb5a7c6c5cd38852faea9a5c4fdbbd5f5 |

Source-level coverage at `f8a52f919bd309960046330a5af127b56731cb27` is carried by R356-1 and R357-1. It remains valid for every lens because the candidate is byte-identical to that head on all of the PR's own paths. This round re-applied every lens at the candidate for the composition delta.

## 6. Real limits

- **Verilator.** The designated pinned Verilator path was absent. A substitute wrapper reporting `Verilator 5.050 2026-07-01 rev v5.050` was used read-only, with its identity and sha256 recorded (`receipts/verilator_identity.txt`).
- **Elaboration shapes.** The elaboration covers `milan_datapath` at the shipping `endstation_arty_current` header plus one synthetic 2/3/4 header. The 1x1 and 8x8 `KL_pp_shadow` statistics identity comes from the source evidence at `870ff88a`. It carries over because every processor `.sv`/`.svh` is byte-identical at `16be6768`; it was not re-measured here.
- **Not run:** the full builder banks (either compiler mode), PP/gPTP/Yosys banks, `test_declarations.py`, `check_nvm_capture.py`, and any Docker, `act` or hardware run. This follows the assignment.
- **Physical calibration.** NOT RUN. Field skips are not hardware proof.
- **Markdown renderer.** The pinned renderer (cmarkgfm 2025.10.22, html5lib 1.1, hash-locked from `tools/markdown/requirements.txt`) was installed in a disposable venv under `scratch/`. System `python3` lacked it (`receipts/venv_freeze.txt`).
- **Hosted CI.** No hosted run exists for `b16e9dad`, which is not pushed. At the source head `f8a52f91`, several jobs had completed successfully when inspected, Verilator shards 1, 2 and 4 of 5 were still in progress, and Physical gPTP was skipped (`receipts/hosted_checks.txt`). Hosted/act acceptance is the manager's.
- **Public evidence read.** From `review-evidence/571-r1`: `REVIEW-READY.md`, `completed-gates.json`, `endstation_ax7101_8x8-elaboration.txt` and `OMITTED.txt`, plus the issue and PR comments. The remaining public files were not needed for the composition delta.
- **Manager bank receipts.** No bank receipt for this candidate was public when this report was written.

## 7. Pending manager duties

- Build and validate the final current-dev candidate at the merge turn. Live dev may move past `2a2a7bb6`, and predecessor order may change.
- Own hosted and `act` acceptance on the pushed candidate. That includes the exact-head `rtl-fast`, `verilator-suites` and `yosys-portability` contexts, and the source-head Verilator shards still in progress at inspection.
- Publish the candidate bank receipts.
- Optionally triage SUGGESTION C1 and the retained SUGGESTIONs. None blocks merge.
- Obtain explicit maintainer merge authorization, then run post-merge containment and close issue #571.

## 8. Restore proof

After all probes, the clone is back at the exact head (`receipts/restore_integrity.txt`):

- `HEAD b16e9dad`, tree `5c28ef68`;
- 0 index-vs-HEAD entries and 0 worktree-vs-index entries (bytes and modes);
- 0 untracked files;
- index tree equals HEAD tree;
- the blob-hash list of every worktree file equals HEAD's (sha256 `a8ebd239...` on both sides);
- gitlinks `external efeb541a`, `gptp-processor 5dce647a`, `protocol-processor 16be6768`, `third_party/verilog-axis 48ff7a7e`, each checked out clean.

R357-2 FINISHED
