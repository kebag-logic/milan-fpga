[R357] POSITIVE - exact head f8a52f919bd309960046330a5af127b56731cb27

# R357-1: external independent review of PR #597 (issue #571)

- Reviewer role: external independent reviewer, cleared context, round R357-1.
- Head reviewed: `f8a52f919bd309960046330a5af127b56731cb27`. Its tree is `f707dc8a91bbb708cd07c895bc2d744cdb6e8d83`. It has one commit on base `2a2a7bb655e528edc3087c88033cd3a47546feb4`.
- Scope: bind the processor's `N_AUDIO_UNIT_P`, `N_CLK_DOMAIN_P` and `N_CONTROL_P` at `u_pp` from the builder-generated entity-model counts.
- Authorities read:
  - AGENTS.md and CONTRIBUTING.md.
  - The #571 issue body (acceptance 1-3).
  - Assignment comment 5857833068 (decision: bind, no refusal) and the correction comment 5858103665 (`docs/spec-refs.md` is not a repository file).
  - The processor integrator guide section 2 at pin `870ff88a` (`protocol-processor/docs/guides/integrator.md:48-70`).
  - `KL_aecp_dyn_state.sv:154-198`.
  - The full base..head diff.
  - The public evidence tree `review-evidence/571-r1` at `ab3d66a7`.
- Prior public findings on PR #597: none existed when this review ran. The only PR comments are the two review-start notices. No PR reviews or inline comments exist. So there is nothing to retain or resolve.

## Verdict summary

All five lenses were applied at the exact head and none has an open BLOCKER, MAJOR or MINOR finding. I record three SUGGESTIONs. They are optional and do not affect coverage.

The seven assigned verification points all hold on reviewer-run evidence:

1. **Same census, no literal at any hop.** The three counts come from `overlay["descriptor_counts"]` in the pass that also emits `AEM_N_AUDIO_UNIT_C` and `AEM_N_CLKDOM_C` (`sw/builder/endstation_builder.py:2779-2790`). The census is constructed in `_overlay_document` (`:5153-5160`). `AEM_N_CONTROL_C` equals the number of CONTROL descriptors the model actually assembles: the new gate arm compares the census with the generated descriptor directory (`scripts/check_entity_shape.py:575-576`). A reviewer mutant that makes `aem_assemble` emit a second CONTROL is rejected on all five configs. The census value itself is a construction constant (`"CONTROL": 1`), like AUDIO_UNIT and CLOCK_DOMAIN before it. From the census to `u_pp` no hop carries a literal.
2. **Both hops bind symbolically.** `milan_datapath.sv:7426-7429` passes `AEM_N_AUDIO_UNIT_C`, `AEM_N_CLKDOM_C` and `AEM_N_CONTROL_C`. `KL_pp_shadow.sv:1059-1062` binds `u_pp` from `N_AUDIO_UNIT_P`, `N_CLK_DOM_P` and `N_CONTROL_P`. The parent keeps the name `N_CLK_DOM_P` (`KL_pp_shadow.sv:237`). I checked this functionally with Verilator 5.050, not only by regex:
   - I set the per-config header that the datapath includes to AUDIO_UNIT=2, CLOCK_DOMAIN=3, CONTROL=4 in a disposable copy.
   - At head, the elaborated `KL_aecp_dyn_state` inside `u_pp` carries exactly 2/3/4 (not swapped).
   - At base it carries 1/1/1 while the wrapper carries 2/3 (`receipts/elab/propagation_hop0.txt`).
   - The same holds with `KL_pp_shadow` as top (`receipts/elab/propagation.txt`).
3. **Zero is unreachable.** `_overlay_document` sets `"AUDIO_UNIT": 1`, `"CLOCK_DOMAIN": 1` and `"CONTROL": 1` unconditionally. `aem_assemble._entity_descriptors` appends AUDIO_UNIT, CLOCK_DOMAIN and CONTROL (IDENTIFY) unconditionally (`avdecc/aem_assemble.py:210,235,237`). I ran ten hand-edited variants of the AX 1x1 configuration (`receipts/probe_zero_counts.txt`):
   - Some add top-level `descriptor_counts: {..: 0}`, `controls: []`, `audio_units: []`, `clock_domains: []`, `entity.controls: []` or `entity.identify: false`. The loader accepts them and still yields census = header = directory = 1.
   - Some set `names.control_identify` to null or to an empty string, or add `names.controls`. The loader refuses them with a named `ConfigError`.
   - If a zero were ever bound, the processor refuses to elaborate. `KL_aecp_dyn_state.sv:164/172/177` reports "Size of range is '[0]'" for each of the three counts (`receipts/elab/zero_count_processor.txt`). The new gate arm also rejects a zero census.
4. **The two-hop checks fail as claimed.** 24 reviewer-written mutants, separate from the author's 24, were all killed with the named parameter or symbol in the rejection (`receipts/probe_binding_mutants.txt`). They cover:
   - unbound, literal (`1`, `32'd1`), wrong generated constant, masking expression, one-sided and two-sided swaps, a binding present only in a comment, a duplicate binding, a local alias, and a binding moved to `u_nvm`, at both hops;
   - header line removed, set to zero, set to two, and duplicated.

   I also ran six on-disk mutants through the real gate entry (`receipts/mutants/emitter_mutants_summary.txt`):
   - An RTL literal at hop 0 and an unbound parameter at hop 1 fail the plain gate.
   - A census of zero and two emitted CONTROL descriptors fail the plain gate.
   - An emitter that cross-wires CONTROL from AUDIO_UNIT, or emits a literal 1, passes the plain gate because every shipping count is 1. The `--self-test` run kills it through the distinct 2/3/4 census. CI runs `--self-test` on every pull request (`.github/workflows/docs.yml:448-449`, no path filter).
5. **Five-configuration identity.** Both base and head trees were rebuilt from scratch, 14 artifacts per config, including the packed AEM image and its map (`receipts/artifact_compare.txt`):
   - 65 artifacts are byte-identical.
   - The 5 per-config headers differ by exactly one added line, `localparam int AEM_N_CONTROL_C    = 1;`.
   - Every config keeps counts 1/1/1.
   - Verilator 5.050 `KL_pp_shadow` elaboration at AX 1x1 and 8x8 generates C++ that is byte-identical between base and head once the tree path is normalized (`receipts/elab/cpp_compare.txt`: 16 and 19 files, 0 differ).
   - Statistics differ only in the pre-parameterization Link column, which records the one new parameter declaration and three new pins. PreOrder, Scoped, WroteAll and WroteFast are identical (`receipts/elab/stats_compare.txt`).
6. **Tracked headers are builder output.** Rebuilding every config at head rewrote all five `configs/generated/*/gen/adp_shape_defaults.svh`. It also rewrote `hdl/common/gen/adp_shape_defaults.svh` through `--write-rtl` for its `Source :` owner, AX 1x1. `git status` stayed clean afterwards and each tracked file equals the regenerated one (`receipts/regen_git_status.txt`).
7. **The ownership-page text is accurate** (`docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:49-70`):
   - The table's generated, parent and processor names match the RTL.
   - The link target `#integration-parameters` exists as an explicit anchor at the pinned processor commit (`integrator.md:48`). Its rows 68-70 define the three consumers.
   - The `A.`/`B.` abbreviations resolve through the page's own source table (`:98-100`).
   - The claims about construction, refusal and self-test match the evidence above. SUGGESTION S1 covers clause precision.

No processor source file changed and no gitlink changed (`receipts/diff_raw_base_head.txt`: 12 files, no `160000` entries, no `protocol-processor/` path).

## Findings

**S1 - SUGGESTION - Docs - `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:49,61,66` - three precision nits in the new paragraph**
- Authority/evidence:
  - Line 61 says "Milan v1.2 Section 5.3.3 requires these descriptor classes." The same page's rule matrix cites Milan 5.3.2 for cardinalities (L1, `:84`) and 5.3.3.10 for IDENTIFY (L8, `:91`). The processor compliance table does the same: REQ-MDL-001 is 5.3.2 and includes CLOCK_DOMAIN ≥1, and REQ-MDL-009 is 5.3.3.10 (`protocol-processor/docs/00_MILAN_COMPLIANCE_REVIEW.md:402,410`). The assignment prescribed the 5.3.3 citation and the manager accepted it, so this is recorded as precision only.
  - Line 66 says the gate checks "descriptor bytes". It actually counts generated descriptor-directory entries by type (`scripts/check_entity_shape.py:514-525,575-576`).
  - Line 49 says "that same descriptor census", but the preceding paragraph does not name a census.
- Impact: a reader who traces the clause lands on per-descriptor subclauses instead of the cardinality clause. The zero-unreachable claim does not rest on the citation, so its correctness is unaffected.
- Optional outcome: cite 5.3.2 alongside 5.3.3.10, say "descriptor directory counts", and name the census explicitly.
- Verification: re-read the page. The docs gates stay green.

**S2 - SUGGESTION - Tests - `tb/verilator/nvm_cosim/cosim_top.sv:193` - the co-simulation dynamic-state store still binds `N_CONTROL_P (1)` as a literal**
- Evidence: the harness derives AUDIO_UNIT and CLOCK_DOMAIN from the census (`tb/verilator/nvm_cosim/run_cases.py:128-131`). CONTROL now has a generated constant too, but the harness does not use it. This predates the PR and is outside #571's `u_pp` scope.
- Impact: none at today's counts. If a model ever carried more than one CONTROL, the harness would diverge from the product without anything flagging it.
- Optional outcome: a follow-up Issue, if the maintainer wants harness parity.
- Verification: the co-simulation elaborates at the census count.

**S3 - SUGGESTION - RTL, Docs - `hdl/milan/KL_pp_shadow.sv:227-239` - parameter-block comment is now partly stale**
- Evidence: the block heading says "saved-state record allocation shape". `N_CONTROL_P` now sits under it, but CONTROL does not size saved-state records: `KL_nvm_backend` takes no CONTROL count (`KL_pp_shadow.sv:974-985`). `N_AUDIO_UNIT_P` and `N_CLK_DOM_P` now also size the processor's dynamic state. The `u_pp` comment at `:1059` and the new parameter comment at `:238` say so. The block heading does not.
- Impact: readability only.
- Optional outcome: widen the heading, for example "saved-state allocation and processor dynamic-state rows".
- Verification: comment-only change. The lint ratchet stays at 90.

## Per-lens results (clean-lens evidence)

```text
[R357] PASS Conformance - issue #571 acceptance 1-3 + assignment 5857833068 vs sw/builder/endstation_builder.py:2779-2790,5153-5160, hdl/milan/milan_datapath.sv:7424-7429, hdl/milan/KL_pp_shadow.sv:236-239,1059-1062, protocol-processor/docs/guides/integrator.md:68-70 - bind (not refuse) chosen and recorded; all three counts from the one descriptor_counts pass with no literal at either hop; N_CLK_DOM_P name kept; decision/zero-count rationale recorded in issue and page; 65/70 artifacts byte-identical and 5 headers +1 line (receipts/artifact_compare.txt); gitlinks and processor sources unchanged (receipts/diff_raw_base_head.txt)
[R357] PASS RTL - hdl/milan/KL_pp_shadow.sv:236-239,1054-1069, hdl/milan/milan_datapath.sv:7393-7430, protocol-processor/hdl/aecp/KL_aecp_dyn_state.sv:154-198 - int->int unsigned parameter plumbing, no width/sign loss (elaborated 32'sh -> 32'h values); distinct 2/3/4 counts reach KL_aecp_dyn_state unswapped through both hops at head and not at base (receipts/elab/propagation.txt, receipts/elab/propagation_hop0.txt); generated C++ at AX 1x1/8x8 byte-identical base vs head (receipts/elab/cpp_compare.txt); lint ratchet PASS 90<=90 with Verilator 5.050 (receipts/lint_rtl_check_head.log); no clock/reset/CDC/FSM change
[R357] PASS Robustness - sw/builder/endstation_builder.py:5099-5160, avdecc/aem_assemble.py:198-242, scripts/check_entity_shape.py:395-402 - ten hand-written config variants cannot reach a zero or altered count (accepted ones keep census=header=directory=1, name removals refused by ConfigError) (receipts/probe_zero_counts.txt); a forced zero in any of the three fails processor elaboration at KL_aecp_dyn_state.sv:164/172/177 (receipts/elab/zero_count_processor.txt) and the gate's nonzero arm; every harness header generator uses builder emission or tracked copies, so no stale fixture lacks AEM_N_CONTROL_C
[R357] PASS Tests - scripts/check_entity_shape.py:170-175,372-402,413,558,575-576 and scripts/entity_shape_selftest.py:598-649,664 - 24 independent reviewer mutants (both hops: unbound, literal, wrong constant, expression, swaps, comment-only, duplicate, alias, moved-to-u_nvm; header removal/zero/two/duplicate) all killed with the named parameter (receipts/probe_binding_mutants.txt); 6 on-disk gate-entry mutants killed, emitter cross-wire/literal killed by --self-test as CI runs it (receipts/mutants/); gate --self-test 219 checks 0 failures; test_declarations rc 0 (receipts/entity_shape_selftest_head.log, receipts/test_declarations_head.log)
[R357] PASS Docs - docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:49-70, hdl/milan/KL_pp_shadow.sv:238,1059, hdl/milan/milan_datapath.sv:7428, PR #597 body, public evidence tree review-evidence/571-r1 - table names match RTL; pinned integrator anchor exists (integrator.md:48); abbreviations resolve (page :98-100); no other parent doc lists these as unbound; docs_check, check_doc_paths, gen_toc --check, check_doc_style, check_em_dash --base, check_py_idiom, check_feature_status, check_nvm_capture all rc 0 and git diff --check clean (receipts/focused_gates_head.txt); only SUGGESTIONs S1/S3 open
```

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #571 acceptance, assignment + correction comments, builder census/header emitter, datapath and shadow bindings, integrator guide section 2 at `870ff88a`, five-config artifact comparison, raw diff | R357-1 | `f8a52f919bd309960046330a5af127b56731cb27` |
| RTL | CLEAN | `KL_pp_shadow.sv` parameter block and `u_pp` map, `milan_datapath.sv` `pp_shadow` map, `KL_aecp_dyn_state.sv` sizing, Verilator 5.050 elaborations (identity, propagation, zero), lint ratchet | R357-1 | `f8a52f919bd309960046330a5af127b56731cb27` |
| Robustness | CLEAN | `_overlay_document`, `_entity_descriptors`, `_load_names`, ten hand-edited config variants, forced-zero elaborations, harness header generators | R357-1 | `f8a52f919bd309960046330a5af127b56731cb27` |
| Tests | CLEAN | `check_entity_shape.py` new arms, `entity_shape_selftest.py::_prove_unit_counts`, 24 in-memory + 6 on-disk reviewer mutants, gate self-test run, `test_declarations.py`, CI trigger for the gate | R357-1 | `f8a52f919bd309960046330a5af127b56731cb27` |
| Docs | CLEAN | `PP_DESCRIPTOR_OWNERSHIP.md:49-70`, RTL comments at the bindings, PR body, public evidence tree, docs/style gates | R357-1 | `f8a52f919bd309960046330a5af127b56731cb27` |

S1, S2 and S3 are SUGGESTIONs, so none of them leaves any lens unclean.

## Real limits

- **Verilator substitute.** The assigned Verilator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` did not exist when this review ran. I used a reviewer-local wrapper around the same Verilator 5.050 install that the other pinned-tool-bin wrappers execute; binary sha256 values are in `receipts/verilator_identity.txt`. The author's own elaboration used 5.052. My identity result is at 5.050.
- **Elaboration identity is Verilator-only.** It covers `KL_pp_shadow`. I did not run a Yosys cell or stat comparison, a full-datapath statistics comparison, or any synthesis or timing.
- **Milan clause not checked against the spec text.** No copy of the Milan v1.2 specification is in the repository. The clause point in S1 rests on the repository's own secondary citations.
- **Banks and hosted runs not executed by me.** I did not run the full builder bank, the parent/processor/gPTP/Yosys banks, act or the host replica. I ran only focused gates and probes.
- **Hosted checks were still running.** In my read-only snapshot of exact-head check runs (`receipts/hosted_check_runs.txt`):
  - Completed successfully: rtl-fast, verilator-lint, Yosys shards 0-3, yosys-elaboration, Verilator shards 0 and 3, wire-accountability, bdd-conformance and full-ci-gate.
  - Still in progress: docs-check, elaborate, and Verilator shards 1, 2 and 4.
  - Skipped (not executed): Physical gPTP.
- **No hardware.** Physical calibration was NOT RUN. Field and physical skips are not hardware proof.
- **Probe scope.** The zero-count probe used hand-edited variants of one base configuration, AX 1x1. The loader silently ignores unknown top-level keys; this predates the PR and no count path reads those keys.
- **Public author evidence consulted.** I read the public author evidence tree for its elaboration method. Every conclusion above rests on reviewer-run receipts.
- **Clone integrity.** The review clone was never modified. Afterwards, HEAD, tree, index tree, index modes and blobs, and all four gitlinks match the exact head. The submodule worktrees are clean (`receipts/clone_integrity.txt`). All probes ran in disposable copies under `scratch/`.

## Pending manager duties

- Accept the exact-head hosted gates once they finish: docs-check, elaborate, and Verilator shards 1, 2 and 4 were in progress at my snapshot. Also run and accept the act replica.
- Obtain the internal review. A positive from it is also required.
- Build and validate the final candidate merge on live `dev`. The source base and live dev were both `2a2a7bb6` at assignment. #580 also edits `PP_DESCRIPTOR_OWNERSHIP.md` and moves the processor pin, so the merge order must be re-checked.
- Obtain maintainer merge authorization, then do post-merge containment, and close #571 and move it to Done.
- Optionally decide whether S2 becomes a follow-up Issue.

R357-1 FINISHED
