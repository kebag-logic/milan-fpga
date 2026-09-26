[R333] NEGATIVE - exact head 0a506fa8f0032d21e9614a617b75b0a57dc5f2e4

# R333-2 external review: issue #231 / PR #572

Reviewer: [R333], external independent reviewer, round R333-2.
Head `0a506fa8f0032d21e9614a617b75b0a57dc5f2e4`, tree `925498fa6e15c7fc53705810a42cff4278b0b336`.
Delta reviewed: `af6d19c5..0a506fa8`, one commit, 11 files, +1,142 / -43. No `hdl/`, donor
or gitlink change (`git diff --stat 7eb3b0d4..0a506fa8` lists no RTL path). Round R333-1 covered
`af6d19c5` in full; this round judges the delta and re-covers every lens at this head.

Context reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #231 (assignment
5844867171, round-two decision 5846064333, review-ready 5846494955), PR #572 body, the #229
reference comment 5845524962, the delta and the public evidence packet
`review-evidence/231-r1` at `bc7fdb29` (`author-r2/`). The verdict, findings and ledger below
were written before any other reviewer's report was read.

## Verdict

NEGATIVE, on two narrowed MINOR residuals. The substance of round 1's MAJOR is fixed: an
attribution-only integrated run that preserves the wrapper boundary reproduces exactly from a
clean checkout. The boundary probe now attributes no datapath-driven logic to `u_dyn`, and the
remaining wrapper feed-through traces to wrapper RTL. The complete ranking and the hierarchical
mapping reconciliation also reproduce byte for byte.

Two items remain open:

- **F1 residual.** The #229 epic reference, which is the acceptance criterion's link from #229,
  still publishes the default-flow wrapper and AECP rows as consumption and links the superseded
  page.
- **F4 residual.** Five enforcement points that the page and recipe claim can still be removed
  with the self-test green. One of them lets a truncated firmware ROM through.

## What was reproduced (clean checkout, exact head)

Disposable clean clone at `0a506fa8` with the three public submodules at their gitlinks. The
LiteX series was verified applied, the SDK was installed fresh from the pinned archive and
verified, and the recipe was followed (`scripts/export.sh`). The only deviation is 4 Vivado
threads instead of 32. Receipts are under `receipts/`.

| Measurement | Page | Reproduced | Match |
|---|---|---|---|
| Attribution 1x1 synthesis, whole / wrapper LUT | 52,210 / 22,314 | 52,210 / 22,314 | exact |
| Attribution 1x1 wrapper FF / RAMB36 / RAMB18 / DSP / CARRY4 / internal WNS | 24,535 / 21 / 3 / 5 / 1,415 / -1.201 | same | exact (`receipts/attr-1x1-synth/`) |
| Attribution 1x1 AECP / `u_dyn` LUT | 4,678 / 111 | 4,678 / 111 | exact |
| Attribution 8x8 synthesis, whole / wrapper LUT | 70,206 / 29,489 | 70,206 / 29,489 | exact |
| Attribution 8x8 wrapper FF / RAMB36 / RAMB18 / DSP / CARRY4 / internal WNS | 32,991 / 26 / 5 / 8 / 1,809 / -10.846 | same | exact; the 3 extra DSPs are in `u_nvm` (1,131 LUT, 4 DSP) |
| Attribution 8x8 scoped table (`PP_SHADOW_BASELINE.md:152-160`) | all 7 rows | same, including every internal WNS | exact (`receipts/attr-8x8-synth/baseline_scope_timing.tsv`) |
| `KEEP_HIERARCHY` on `milan_datapath/pp_shadow` in both checkpoints | TRUE | TRUE | `keep_attr_*.txt` |
| Boundary probe, 10 rows (`PP_SHADOW_BASELINE.md:198-209`, attribution column) | e.g. 8x8 `u_dyn` 607 / 0 / 0; wrapper 32,833 / 519 / 467 | same, all 10 rows | exact (`boundary_attr_*.tsv`) |
| `u_dyn` external-load histogram, both shapes | empty | empty (0 lines) | exact |
| Ranking TSV, `attribution-synth-1x1`, `attribution-synth-8x8`, `ooc-1x1` | 41 rows each | `pp_baseline_rank.py` on the reproduced reports | byte-identical |
| Ranking TSV, `default-synth-1x1`, `default-synth-8x8`, `ooc-1x1`, `ooc-8x8` | 41 rows each | round-1 reproduced reports (filtered) | all 31 comparable rows per endpoint equal; the 8 absent are instances that filter drops |
| Standalone 1x1: LUT / FF, census sha256 | 22,350 / 24,533 | same; `edfd86ab...` equals round 1 | exact |
| Yosys flattened 1x1 | 41,258 / 5,972 / 47,230 / 23,041 / 15 / 4 / 5 / 1,813 | same | exact |
| Yosys hierarchical 1x1 raw logic LUTs | 48,915 | 48,915 from the parser; Yosys's own `stat` LUT1-6 sum is also 48,915 | exact |
| Mapping TSV, 1x1 (every row) | `PP_SHADOW_BASELINE_MAPPING.tsv` | `receipts/mapping-1x1/mapping.tsv` | byte-identical, including `g_rx_pool[3]` 92 / 0 |
| Input images, both shapes | manifest sha256 | all 12 in the manifest, unchanged after the runs | yes |
| `Synth 8-4445` diagnostics, both attribution logs | zero | zero (the one hit is the echoed `set_msg_config`) | yes |

The default-flow whole-design totals (`PP_SHADOW_BASELINE.md:67-73`) are unchanged from
`af6d19c5`. The delta only moves the default wrapper-name rows out of that table into the
labelled default/attribution comparison (`:189-193`), and `:238-239` marks the placement-table
wrapper counts as not ownership.

## Checks against the round-two assignment (issue 231 comment 5846064333)

1. **Boundary preserved, and the probe is clean.** The helper writes
   `set_property KEEP_HIERARCHY TRUE [get_cells milan_datapath/pp_shadow]` and reads it before
   `synth_design` (`syn/ooc/pp_baseline.py:193-198`). The run log parses it with no
   unmatched-object warning (`boundary_constraint_log_lines.txt`), and the checkpoint property is
   TRUE.
   - **`u_dyn`.** 1x1 has 144 LUT cells and 8x8 has 607, with zero external-only loads and an
     empty histogram at both shapes. Round 1 found 763 and 5,922 cells with external-only loads.
   - **SRP.** The remaining SRP cells with an external input and only external loads number 96 at
     1x1 and 432 at 8x8. `probe_boundary/feedthrough.tcl` shows every one runs from
     `station_mac_i`/`cfg_stream_id_i` to `srp_src_fail_bridge_o` (`feed_srp_attr_*.tsv`). That
     is 48 bits per talker stream, the RTL
     `msrp_fail_bridge_o[s] = (tk_decl_state_o[s] == 2'd2) ? {16'd0, own_mac_i} : 64'd0`
     (`protocol-processor/hdl/srp/KL_srp_talker_fsm.sv:805-806`). This is genuine wrapper
     feed-through, not relocated datapath logic.
   - **Wrapper.** Its other external loads go to datapath CSR muxes and CDC counters, which are
     wrapper outputs (`loads_wrapper_attr_*.tsv`).
   - **Page.** It states the difference (`:75-81`, `:180-219`), and the PR body carries the
     qualification.
2. **Ranking complete.** The threshold is zero, and own-logic, reconciliation and total rows are
   present. `probe_boundary/children.tcl` lists the netlist's direct hierarchical children of the
   wrapper (3) and of `u_pp` (32) in the attribution 1x1 checkpoint. Every one is ranked, and no
   ranked row is missing from the netlist (`children_attr_1x1_synth.tsv`). The timing tables are
   labelled subsets (`:120`).
3. **Mapping explanation evidence-backed.** This takes the decision's first option, an
   equivalent-geometry run that is not flattened. It reproduces at 1x1, and the independent Yosys
   `stat` agrees. The flattening residual (-7,657 / -4,498) is kept global, not assigned.
   `probe_mapping/flat_scope.py` supports that choice: net names attribute only 2,803 of the
   41,258 flattened LUTs (`flat_scope_1x1.tsv`), so no per-module split of the flattened netlist
   is measurable by name. The page limits the claim accordingly: "SRP dominates the
   hierarchy-preserved logic difference" (`:334`).
4. **Self-test mutants.** All ten maintained mutants fail, and hosted `yosys-elaboration` ran them
   at this head (`receipts/hosted_yosys_elaboration_job_108409593143_excerpt.txt`). Round 1's five
   mutants are all killed now. Twelve further removals survive, five of them claimed enforcement
   (F4 residual).
5. **`check_doc_paths` on a clean checkout.** It passes on the review clone with no
   `sw/builder/out`: "848 cited paths all resolve, 1 allowlisted". It also passes on a
   `git archive` export of the head (`receipts/doc_paths_clean_export.txt`). The allowlisted
   entry is pre-existing. The citation now names `sw/builder/out/`, which `.gitignore:32` matches, so the
   gate's build-artifact rule accepts it. `docs_check.py`, `check_py_idiom.py`,
   `ci_events.py --check` and `git diff --check 7eb3b0d4 0a506fa8` all return rc 0.
6. **Measurement only.** No RTL change.

## Findings

### F1 (residual) - MINOR - Conformance, Docs

Location: issue #229 comment 5845524962 (`[A328] BASELINE REFERENCE`), last updated
2026-09-26T10:35:11Z, before round 1.

Title: the #229 baseline reference still presents default-flow wrapper and AECP rows as
consumption and links the superseded page.

Evidence: F1's required outcome in round 1 was "The PR and issue summaries must carry the same
qualification." The PR body and #231 now do. The #229 comment is the artifact through which the
acceptance criterion's "baseline page linked from #229" is met. It still carries:

- the rows "Vivado shipping 1x1 route, wrapper | 22,441" and "Vivado integrated 8x8 synthesis,
  wrapper | 37,809", with no qualification;
- the sentence "integrated 8x8 AECP is 15,199 LUTs";
- links to `af6d19c5`, whose page carries the misattribution this round fixed.

The measurement defect itself is closed at this head (see the checks above). The severity is
re-assessed from MAJOR to MINOR because what remains is a public summary, not the committed
measurement.

Impact: the epic's readers, who choose the optimization tickets, still see 37,809 wrapper LUTs and
a 15,199-LUT AECP at 8x8. The attribution figures are 29,489 and 5,025.

Required outcome: the #229 reference points at the corrected baseline (this head or the merged
page) and states or links the default-versus-attribution distinction. Alternatively, it is
superseded by a new reference comment that does.

Verification: read the #229 thread for a reference to the corrected page with that qualification.

### F4 (residual) - MINOR - Tests

Location: `syn/ooc/pp_baseline.py:162`, `:174-175`, `:143-144`, `:180-181`, guarded by
`:289-381`. Claims at `docs/findings/PP_SHADOW_BASELINE.md:279-285` ("rejects missing, short,
malformed and ambiguous inputs") and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:380` ("checks
complete control-ROM and generated-ROM geometry").

Title: claimed geometry and ambiguity refusals can still be removed with the self-test green.

Evidence: `probe_selftest/mutate2.py` (`mutation_results.txt`). Round 1's five mutants are all
killed now. These claimed-enforcement mutants survive:

- dropping the generated-ROM depth check (`int(words)` to `None`);
- dropping the generated-ROM width check;
- dropping the parameter-ROM width check (`package_number(text, width)` to `None`);
- disabling the ambiguous image or geometry-source refusal (`:174`);
- disabling the single-declaration check in `package_number` (`:143`).

`probe_selftest/truncated_rom.py` on a real 1x1 export with the firmware ROM one word short gives
"pristine: refused: wrong image depth ... 12938 != 12939" and "mutant: ACCEPTED truncated firmware
ROM" (`truncated_rom_results.txt`). The synthetic export only mutates parameter-ROM depth, never
the generated ROM's depth or width. The round-two assignment (item 4) requires a failing mutant
for "any other enforcement line it claims".

Seven lesser guards also survive: the integrated-directory guard, both attribution-endpoint
guards, the `-hierarchical_min_primitive_count 0` flag, wrapper-parameter set equality, the
duplicate-parameter refusal and the single-synth-command check. They are listed for completeness.

Impact: a truncated firmware ROM gives a plausible wrong area with no `Synth 8-4445`, which is the
#246 family. The only guard against it can be deleted with CI green.

Required outcome: the self-test fails when any of the five claimed checks above is removed. For
example, add generated-ROM short and wrong-width cases, a parameter-ROM wrong-width case, and
duplicate-declaration cases to the synthetic export, with a maintained mutant for each.

Verification: `probe_selftest/mutate2.py` reports those five mutants killed, and
`pp_baseline_mutants.py` includes them.

### Suggestions (do not affect coverage)

- **S3 (Robustness).** The attribution script does not verify that its constraint took effect.
  If the wrapper instance is renamed, the unmatched `get_cells` is only a warning, and the run
  silently produces default-flow numbers under the attribution label. A post-synthesis
  `if {[get_property KEEP_HIERARCHY [get_cells milan_datapath/pp_shadow]] ne "TRUE"} {error ...}`
  would close that.
- **S4 (Docs).** `PP_SHADOW_BASELINE.md:216` says "The routed attribution checkpoint is probed
  separately as well" but publishes no result. The public handoff has it (143 / 0 / 0 / 0); the
  page could state it.
- **S5 (Docs).** The PR body ends "The local commit is unpushed ... this prepared body has not
  been applied to the PR". That is no longer true at the published head.
- **S6 (Tests).** `probe_selftest/mutate_reports.py` (`mutation_reports_results.txt`): the report
  self-test kills 4 of 9 mutants. These five survive:
  - FF rank computed in LUT order, although the page claims independent ranks;
  - duplicate-row refusal removed;
  - missing-parent refusal removed;
  - within-module primitive multiplicity collapsed;
  - residual row's Yosys column zeroed.

  The published TSVs were verified independently, so this affects only future edits.
- **S1** (round 1, still optional). The recipe's "Rehash `baseline_images.json` inputs after each
  run" still gives no command.

## Lens results

- **Conformance: UNCLEAN** (F1 residual). The assignment's items 1, 2, 3 and 5 are met with
  reproduced evidence (above). The default totals stay the fit baseline, and the attribution run
  is separate and labelled (`:75-87`, `:117-118`, `:189-193`). There is no RTL change.
- **RTL: CLEAN.**
  - Artifacts: `KEEP_HIERARCHY` TRUE in both reproduced checkpoints, and the boundary probe clean
    for `u_dyn` at both shapes.
  - The SRP feed-through traced to `KL_srp_talker_fsm.sv:805-806` through wrapper ports
    `station_mac_i` / `srp_src_fail_bridge_o` (`KL_pp_shadow.sv:647`).
  - The 8x8 DSP change located in `u_nvm` (reproduced 1,131 LUT / 4 DSP).
  - The diff contains no `hdl/` path.
  - Resource effects of the integrated boundary are now attributed correctly on the page.
- **Robustness: CLEAN.** Artifacts:
  - `syn/ooc/pp_baseline.py:185-236`: the attribution branch refuses a standalone endpoint at both
    CLI and `prepare()`, and the directory guard now runs before any write;
  - `truncated_rom_results.txt` (the pristine helper refuses a short real ROM);
  - the image rehash after both runs;
  - zero `Synth 8-4445`;
  - the clean clone showing only the recipe symlink as untracked.

  S3 is optional.
- **Tests: UNCLEAN** (F4 residual). The ten maintained mutants and round 1's five are killed. The
  report self-test passes and hosted CI runs all three self-test entry points at this head.
- **Docs: UNCLEAN** (F1 residual). The page, recipe, TSVs and PR body were checked against the
  reproduced figures. `check_doc_paths.py`, `docs_check.py` and `check_py_idiom.py` return rc 0.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 residual, MINOR) | `docs/findings/PP_SHADOW_BASELINE.md`, the two TSVs, the recipe, issue #231 5846064333, #229 comment 5845524962, PR body; `receipts/attr-1x1-synth`, `attr-8x8-synth`, `ooc-1x1`, `mapping-1x1`, `ax7101-yosys` | R333-2 | 0a506fa8f0032d21e9614a617b75b0a57dc5f2e4 |
| RTL | CLEAN | `keep_attr_*.txt`, `boundary_attr_*.tsv`, `loads_*_attr_*.tsv`, `feed_srp_attr_*.tsv`, `children_attr_1x1_synth.tsv`; `protocol-processor/hdl/srp/KL_srp_talker_fsm.sv:805-806`; `hdl/milan/KL_pp_shadow.sv:647`; `git diff --stat 7eb3b0d4..0a506fa8` | R333-2 | 0a506fa8f0032d21e9614a617b75b0a57dc5f2e4 |
| Robustness | CLEAN | `syn/ooc/pp_baseline.py:185-236,384-409`; `probe_selftest/truncated_rom_results.txt`; `receipts/attr-*/baseline_images.json` rehash; `synth_8_4445_*`; `receipts/environment.txt` | R333-2 | 0a506fa8f0032d21e9614a617b75b0a57dc5f2e4 |
| Tests | UNCLEAN (F4 residual, MINOR) | `syn/ooc/pp_baseline.py:239-381`, `pp_baseline_mutants.py`, `pp_baseline_reports_selftest.py`; `probe_selftest/mutation_results.txt`, `mutation_reports_results.txt`; hosted `yosys-elaboration` job 108409593143 excerpt | R333-2 | 0a506fa8f0032d21e9614a617b75b0a57dc5f2e4 |
| Docs | UNCLEAN (F1 residual, MINOR) | the page, recipe and TSVs against the reproduced receipts; #229 comment 5845524962; PR body; `check_doc_paths.py` / `docs_check.py` / `check_py_idiom.py` rc 0 on the clean review clone | R333-2 | 0a506fa8f0032d21e9614a617b75b0a57dc5f2e4 |

## Prior public review findings on this PR

This section was written after the verdict, findings and ledger above. It was completed at about
2026-09-26T14:20Z, after reading PR comment 5846062021 ([R332] round 1). No review round had
published on this head before this one.

Round R333-1 findings (PR comment 5846062510):

| Finding | Status at `0a506fa8` | Evidence |
|---|---|---|
| R333-1 F1 MAJOR, integrated rows misattribute datapath logic | **Measurement closed; residual RETAINED as MINOR** (F1 residual above) | Attribution run reproduced, `KEEP_HIERARCHY` TRUE, `u_dyn` external-only loads 5,922 to 0 at 8x8, the page qualified, the PR and #231 summaries qualified. The #229 reference is unchanged. |
| R333-1 F2 MINOR, Yosys difference not explained | **CLOSED** | The hierarchical run and the per-scope reconciliation reproduce byte for byte at 1x1 (`receipts/mapping-1x1/mapping.tsv`). The Yosys `stat` sum agrees. The residual is kept global, and the net-name probe shows no finer split is measurable. |
| R333-1 F3 MINOR, a-priori subset tables | **CLOSED** | The complete zero-threshold ranking is committed. Three endpoints were reproduced byte for byte, four more agree on every comparable row, the netlist children check is complete, and the subset tables are labelled (`:120`). |
| R333-1 F4 MINOR, self-test does not guard enforcement | **Original four mutants closed (killed); residual RETAINED** (F4 residual above) | `probe_selftest/mutation_results.txt` rows R1-*: all killed. Five claimed-enforcement mutants still survive. |
| R333-1 S1, S2 (suggestions) | Both still apply (optional). For S2, the author-r2 handoff names an executed-script hash record that is not in the public packet. | Not coverage-relevant. |

Round R332-1 findings (PR comment 5846062021):

| Finding | Status at `0a506fa8` | Evidence |
|---|---|---|
| R332-1 F1 MINOR, `check_doc_paths` fails on a clean checkout | **CLOSED** | Following the finding's own verification (a `git archive` export of the head, `git init && git add -A`, no `sw/builder/out`), the gate reports "848 cited paths all resolve" at rc 0 (`receipts/doc_paths_clean_export.txt`). The review clone gives the same. The citation now reads `sw/builder/out/` (`PP_SHADOW_BASELINE_RECIPE.md:44`), which `.gitignore:32` matches. |
| R332-1 F2 MINOR, hierarchy tables are a fixed subset | **CLOSED** | Same evidence as R333-1 F3. Every direct child of `u_pp` and of the wrapper is ranked at all eight endpoints with `@reconciliation` and `@total` rows. The timer growth (+758) is now stated (`PP_SHADOW_BASELINE.md:220`). |
| R332-1 F3 MINOR, self-test cannot fail when #246 guard removed | **CLOSED as specified** | Its four mutants map to maintained mutants "ROM error promotion", "readmemh inventory equality", "empty SRAM requirement" and "outside repository guard", all killed locally and in hosted `yosys-elaboration`. The required ordering assertion (promotion before `synth_design` in each emitted script) is at `pp_baseline.py:334-337`. The wider claimed-enforcement gap is carried by this round's F4 residual. |
| R332-1 S1-S3 (suggestions) | S3 is answered by the attribution run (`u_dyn` 574 at 8x8 with the boundary kept). S1 and S2 remain optional. | Not coverage-relevant. |

Reading these findings changed no verdict, finding or ledger row above.

## Limits

- The attribution 1x1 route (20,655 LUT, +0.041 / +0.015 ns) was not reproduced; it is checked
  only against the public handoff and the ranking TSV. The attribution syntheses were reproduced.
- The 8x8 standalone run, the 8x8 Yosys runs (flattened and hierarchical) and the 8x8 mapping rows
  were not rerun this round. They are checked by arithmetic: the 8x8 TSV rows sum to the page's
  totals.
- The runs used 4 Vivado threads, not 32. Every reproduced figure matched exactly.
- The boundary probe classifies by cell location. With the wrapper kept, reverse relocation
  cannot occur across that boundary, but sibling attribution inside the wrapper remains rebuilt,
  as the page states.
- No hardware, bitstream, act or Docker run was produced. Physical calibration was NOT RUN.
  Hosted evidence was only read: the exact-head jobs executed, and the physical gPTP context was
  skipped.

## Pending manager duties

- Hosted and act acceptance at the final head. The current-dev candidate build at the merge turn
  (source base `7eb3b0d4`, live dev `462b714f`).
- Publication of this packet (REPORT.md plus the files in MANIFEST.sha256).
- The #229 reference update (F1 residual) is a GitHub write the manager or executor must make.
- Re-review of any corrected head, which must re-cover Conformance, Tests and Docs.

R333-2 FINISHED
