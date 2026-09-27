[R351] NEGATIVE - exact head 55079500483970ee244f12fa4c94401783f3df6f

# R351-1 external independent review: issue #587 / PR #589

- Head under review: `55079500483970ee244f12fa4c94401783f3df6f`, tree `791dba22b442a3c5bc43223a1cd74f4200ffdf82`, one commit on dev `63fe4fb0164d798d44a6476001dc8b887cdd4609`.
- Role: [R351], external independent reviewer, cleared context, isolated detached clone.
- Round: R351-1. Lenses applied: Conformance, RTL, Robustness, Tests, Docs (all five).
- Verdict: NEGATIVE, because one MINOR finding is open under Docs.

The measurement is correct. Both integrated 8x8 syntheses reproduce exactly at the configuration-derived 50 MHz: 68,047 LUT, -1.708 ns WNS, -89 LUT versus 100 MHz. Conformance, RTL, Robustness and Tests are covered clean.

The open MINOR (R351-F1, which retains the public [R350] F1) concerns one committed evidence value. The input manifest's normalized-Verilog digest cannot be produced by the manifest's own stated normalization rule. It reproduces only after inserting the executor's private checkout path.

My independent pass, recorded before I read any other review (`receipts/independent_verdict_before_prior_findings.txt`), found the same defect but rated it SUGGESTION. Section 7 explains why I retain it at MINOR.

## 1. Reconstruction

I reconstructed the task from public state only, in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.md.
3. Issue #587: the body (frozen acceptance 1-3), the [A10] assignment 5855348441 and the [A360] TAKEN / REVIEW READY comments.
4. The recipe `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, `syn/ooc/pp_baseline*.py`, `configs/endstation_ax7101_8x8.yaml`, `hdl/milan/KL_pp_shadow.sv` and `hdl/milan/KL_nvm_backend.sv`.
5. The diff `63fe4fb0..55079500` and commit metadata.
6. The manager-published packet `review-evidence/587-r1` at `f847f343` (MANIFEST.json, author gate receipts, HANDOFF.md, ARTIFACTS.tsv).
7. The hosted check runs at the exact head.

Frozen acceptance (issue #587):
1. Re-run integrated 8x8 synthesis and the attribution variant with the #231 recipe at dev after #565, at the declared 50 MHz.
2. The page states both measurements with their clocks; the 100 MHz figures stay as labelled history; the #229 reference comment is updated.
3. Report whether the 8x8 LUT total changed and by how much, and the WNS at 50 MHz.

Per the assignment, the #229 reference comment is manager-owned after merge. The executor's pre-review edit of that comment is not part of this PR and is not reviewed here.

The diff touches exactly three files, all documentation or evidence:
- `docs/findings/PP_SHADOW_BASELINE.md` (M, +188/-33)
- `docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json` (A, 100644)
- `docs/findings/PP_SHADOW_BASELINE_50MHZ_RANKING.tsv` (A, 100644)

There is no RTL, configuration, tooling or gitlink change. The commit is one line with no body and no trailers (CONTRIBUTING 2.2).

## 2. Independent reproduction (reviewer-executed)

I rebuilt a private environment in the reviewer scratch directory (never published):
- the pinned SDK, installed fresh and verified by `scripts/ci_rv32_sdk.py` (archive sha256 `d42680e9...`, GCC 14.3.0);
- private copies of the LiteX packages at the manifest's recorded dependency revisions;
- the repository patches 0002 and 0004 applied, which reproduce the host's patched state exactly. The VexiiRiscv netlist is the host's cached one; its hash equals the manifest's.

Vivado 2026.1, SW build 6511674. Each long step exceeded the session's per-command limit, so it ran as a detached, memory-capped (48 GiB) transient user unit that I polled in the foreground until it exited. Nothing was left running.

| Check | Executor claim / manifest | Reviewer result at this head | Receipt |
|---|---|---|---|
| Clock source | launcher derives `--milan-clk-freq 50e6` from the configuration | preview emits `50e6` from `soc_params.json`, regenerated from `configs/endstation_ax7101_8x8.yaml:56` (`milan_clk_hz: 50000000`). A disposable mutation to `100000000` makes the same preview emit `100e6`; the YAML was restored byte-exact | `receipts/head_ax8x8_dry_run.log`, `receipts/probe_clock_100e6_dry_run.log` |
| Recipe identity | same #231 recipe | generated `alinx_ax7101.tcl` and `baseline_integrated.tcl` are byte-identical to the manifest hashes after substituting the executor's published checkout and build roots. XDC is raw-identical | `receipts/generated_identity.out` |
| Inputs | 127 source and 6 image hashes | all repository, processor, gPTP, AXIS and CPU-package sources, and all 6 images, match. The only raw differences are the 3 root-bearing generated files above. Images rehash clean after synthesis | `receipts/compare_inputs_default.out`, `receipts/compare_inputs_post_synthesis.out`, `receipts/post_synthesis_rehash.out` |
| Default 8x8 synthesis | 68,047 LUT, 70,744 FF, 80/29 RAMB, 11 DSP, 3,913 CARRY4, WNS -1.708 ns | identical, rc 0, zero `Synth 8-4445` diagnostics. The 10 MB primitive census and the scope-timing TSV are sha256-identical to the executor's artifacts | `receipts/compare_measurements.out` |
| Default timing detail | 20.000 ns Milan clock; worst path `u_notify/ctr_pend_r_reg[3]/C` to `u_event_router/sel_r_reg[3]/D`, 43 levels; 46 in / 86 out without I/O delay; 0 unclocked / unconstrained | identical | `receipts/default_timing_and_elaboration_excerpt.txt` |
| Elaborated clock-derived parameters | `CLK_HZ_P=50000000`, `TIM_DIV_US_P=50`, `TIM_DIV_MS_P=1000` | identical. `TIM_DIV_US_P` is derived from `CLK_HZ_P` in RTL (`hdl/milan/KL_pp_shadow.sv:198`), not restated | same excerpt |
| Attribution 8x8 synthesis (extra, beyond the required minimum) | whole 69,923 LUT, WNS -1.700; wrapper 28,955 LUT | identical, rc 0. The only Tcl difference from the default is `read_xdc baseline_boundary.xdc`; 118 `read_verilog` in both. Census and scope timing are sha256-identical to the executor's artifacts | `receipts/compare_measurements.out`, `receipts/attribution_export_identity.out` |
| Rankings | 82-row TSV | `pp_baseline_rank.py` on my default and attribution reports reproduces both 41-row blocks exactly. Internal check: children plus reconciliation equal the total in every column, storage/DSP reconciliation is zero, ranks are correct, and totals equal the manifest metrics | `receipts/ranking_default_compare.out`, `receipts/ranking_attribution_compare.out`, `receipts/check_ranking.out` |
| Public boundary/load probes | manifest boundary rows and load histograms | unchanged probes (sha256 `45debf29...`, `a1a9097c...` at `e21bc530`) on both of my checkpoints, rc 0. All six outputs are sha256-identical to the executor's artifacts | `receipts/probes_default_compare.out`, `receipts/probes_attribution_compare.out` |
| Delta and WNS arithmetic | -89 LUT, -91 FF, -3 CARRY4, +9.623 ns; attribution -534 / -9 / -3 DSP / -35 / +9.146 | recomputed from the manifest and the historical #231 figures: correct. Capacity excess 68,047 - 63,400 = 4,647: correct | this report |
| Historical figures | 100 MHz 8x8 kept as history; 1x1 unchanged | all 60 base numeric table rows survive unchanged at head; no removed prose number is lost | `receipts/check_history_numbers.out` |
| Historical comparability | processor HDL identical; only `CLK_HZ_P` and `TIM_DIV_US_P` differ; the gPTP image changes | the `hdl` trees at `990f965` and `0922e43` are the same tree object `d8879608`. Wrapper parameter values differ only in those two (the ROM parameters differ in record form, not value). Firmware and both processor ROM hashes equal the historical ones; the gPTP image differs. Between `7eb3b0d` and `63fe4fb0` the only synthesis-relevant input change is the configuration clock (plus that pin move) | this report |
| Normalized-Verilog digest | `3d371f2d...` under "Replace each absolute build root with `$BUILD`; strip block and line comments" | the rule as written gives `1f7c01e2...` for both of my exports: equal to each other, but not the committed value. `3d371f2d...` appears only when the executor's private checkout path is inserted | `receipts/normalization_rule_as_written.out`, `receipts/generated_identity.out` |

## 3. Gates (reviewer-run at this head, foreground, rc recorded)

All rc 0:
- `pp_baseline.py --selftest`
- `pp_baseline_mutants.py`: control passes, every removal fails
- `pp_baseline_reports_selftest.py`
- `docs_check.py`, in Git mode and in `GIT_DIR=/dev/null` mode (0 findings over 901 text files)
- `check_em_dash.py --base 63fe4fb0` (339/339 arms)
- `check_doc_style.py`
- `gen_toc.py --check` and `--verify-anchors` (179 anchors)
- `check_doc_paths.py` (848 paths)
- `git diff --check 63fe4fb0 HEAD`
- the repository gates the assignment named for committed JSON receipts: `pp_srcs.py --check`, `check_baremetal_only.py --check` (0 findings over 899 tracked files, which include the new JSON and TSV), `check_baremetal_only.py --selftest` and `check_entity_shape.py` (113 checks, 0 failures)

The em-dash and contents gates ran with the locked Markdown renderer installed from `tools/markdown/requirements.txt`, with hashes, into a private scratch environment.

Receipts: `receipts/gates_docs_baseline.rc`, `receipts/gates_repo.rc`, `receipts/gate_*.out`.

Hosted snapshot at the exact head (2026-09-27T13:18Z): 21 check runs completed success. `Physical gPTP (nightly and manual)` was skipped; a skipped context is not hardware proof. The manager owns hosted and act acceptance. Receipt: `receipts/hosted_check_runs.tsv`.

## 4. Findings

```text
[R351] MINOR Docs - docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json:29-32 - R351-F1 (retains public [R350] F1): normalized-Verilog digest is not reproducible from its stated normalization
Requirement/evidence:
  - export_comparison records normalized_verilog_sha256 3d371f2d... under the rule "Replace each absolute build
    root with $BUILD; strip block and line comments from generated Verilog".
  - The generated top embeds the absolute checkout root three times (gPTP image, listener ROM and microcode paths).
  - Applying that rule to both reviewer exports gives 1f7c01e2..., equal to each other. The committed 3d371f2d...
    appears only when the executor's private checkout path, published only in the REVIEW READY comment, is written
    into the text before hashing (receipts/normalization_rule_as_written.out).
  - The manifest's roots map records labels, not that path.
  - AGENTS.md section 2 requires a cold reviewer to reconstruct from GitHub and the repository, and the assignment
    asks that the committed JSON be reproducible.
Impact: A cold reviewer who follows the committed rule obtains a different digest. They could wrongly conclude that the
  generated RTL differs, or be unable to confirm the value. The underlying claims are true and independently reproduced:
  the two 50 MHz exports are equal, and every measured figure matches. No remeasurement is needed.
Required change: The manifest's digest and its stated normalization must agree from any checkout path. For example,
  normalize the checkout root as well and recompute the value, or state the root dependence explicitly (redacted), or
  drop the digest and keep the equality with its rule. The page wording that the normalized RTL matches can stay.
Verification: Apply the committed rule to a fresh export in an arbitrary checkout (or rerun
  scripts/compare_inputs.py and the normalization in receipts/normalization_rule_as_written.out) and obtain the committed
  digest. All docs gates stay rc 0.
```

```text
[R351] SUGGESTION Docs - docs/findings/PP_SHADOW_BASELINE.md:32, :48 - R351-S1 (overlaps public [R350] F2): Provenance tables describe only the #231 run
Requirement/evidence: The Provenance processor row (990f965) and the product-configuration table (8x8 row "historical #231",
  timer 100 MHz) are not labelled as the original run's inputs. The rerun's pin 0922e43 and 50 MHz binding appear only at
  lines 139-150. Some nearby historical 8x8 prose (standalone BRAM and critical path, original ranking link, 8x8
  load-stem prose) carries its clock only through the adjacent labelled tables.
Impact: A reader of Provenance alone could attribute 990f965 to the 50 MHz figures. No figure is mislabelled.
Suggested change: Label the Provenance table as the original #231 inputs, or add a 50 MHz 8x8 row and the current pin.
  Optionally, tag the remaining historical 8x8 prose "historical (#231) 100 MHz".
Verification: Read the Provenance section against the manifest's submodules and wrapper_parameters.
```

```text
[R351] SUGGESTION Docs - docs/design/AREA_BUDGET.md:9 - R351-S2: pointer names only issue #231
Requirement/evidence: "The protocol processor baseline records issue #231." The page now also records the #587 50 MHz rerun.
Impact: Discoverability only; the statement remains true.
Suggested change: Optionally mention the 50 MHz rerun.
Verification: Read the line.
```

## 5. Clean-lens results (same format as findings, with evidence)

```text
[R351] PASS Conformance - issue #587 acceptance 1-3; docs/findings/PP_SHADOW_BASELINE.md:111-253; receipts/compare_measurements.out, receipts/head_ax8x8_dry_run.log, receipts/probe_clock_100e6_dry_run.log
  Item 1: the reviewer re-ran the recipe's ax8x8 export and synthesis endpoint at this head. The clock is the
  configuration's declared 50 MHz (launcher-derived, mutation-confirmed), and the recipe bytes, tool build and inputs
  are the recorded ones. Both variants reproduce exactly.
  Item 2: every 50 MHz and 100 MHz 8x8 table figure carries its clock, and the 1x1 figures are numerically unchanged.
  The #229 comment is a manager duty after merge, per the assignment.
  Item 3: -89 LUTs and WNS -1.708 ns are stated at lines 119-132 and are correct.
[R351] PASS RTL - git diff 63fe4fb0..55079500 (no hdl/, configs/, syn/, sw/ or gitlink change); hdl/milan/KL_pp_shadow.sv:184-199; hdl/milan/KL_nvm_backend.sv:603; receipts/default_timing_and_elaboration_excerpt.txt
  There is no RTL change. The clock-derived wrapper parameters bind CLK_HZ_P=50000000, TIM_DIV_US_P=50 (derived in
  RTL) and TIM_DIV_MS_P=1000. The Milan clock (clkout1) is constrained at 20.000 ns. The reported worst path, logic
  depth and I/O-delay gaps match the reviewer's report. The CLK_HZ_P-derived NVM millisecond divider accounts for the
  NVM DSP change the page reports.
[R351] PASS Robustness - receipts/probe_clock_100e6_dry_run.log, receipts/post_synthesis_rehash.out, receipts/gate_pp_baseline_selftest.out, receipts/gate_pp_baseline_mutants.out, receipts/default_timing_and_elaboration_excerpt.txt, receipts/restore_verification.out
  The configuration-to-launcher clock path responds to a mutated declaration, so the clock is not a restated literal.
  Missing-ROM diagnostics are promoted to errors and absent in both runs. Images rehash clean after synthesis. The
  helper's refusal self-test and enforcement-removal mutants pass. The measurement is deterministic across an
  independent environment on a loaded shared host: identical census, scope timing and probe outputs.
[R351] PASS Tests - receipts/ranking_default_compare.out, receipts/ranking_attribution_compare.out, receipts/check_ranking.out, receipts/probes_default_compare.out, receipts/probes_attribution_compare.out, receipts/gates_docs_baseline.rc, receipts/gates_repo.rc
  The committed ranking and probe evidence regenerate bit-for-bit from the reviewer's own checkpoints, using the
  maintained parser and the unchanged public probes. The ranking is internally consistent with the manifest. The
  baseline self-tests and mutants pass. The repository gates that a sibling lane's JSON receipts tripped pass with the
  new receipts tracked. This measurement-only scope needs no test change. R351-F1 concerns a documentation evidence
  record that no test asserts, so it is not filed under Tests.
```

Docs is not covered clean in this round: R351-F1 (MINOR) is open under it. Docs was applied to the full page at head, both committed receipts, the history-number check (`receipts/check_history_numbers.out`), every 50 MHz page figure against the manifest (row by row, including deltas), the docs, em-dash, style, contents, anchor and path gates, and the `AREA_BUDGET.md` cross-reference. The committed receipts contain no private paths.

## 6. Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #587 acceptance and assignment; PP_SHADOW_BASELINE.md:111-253; reviewer default and attribution synthesis; launcher preview and clock-mutation probe | R351-1 | 55079500483970ee244f12fa4c94401783f3df6f |
| RTL | CLEAN | diff (no RTL/config/gitlink change); KL_pp_shadow.sv:184-199; KL_nvm_backend.sv:603; reviewer baseline.log parameters; reviewer baseline_timing.rpt | R351-1 | 55079500483970ee244f12fa4c94401783f3df6f |
| Robustness | CLEAN | clock-mutation probe; post-synthesis rehash; `Synth 8-4445` scan; baseline self-test and mutants; cross-environment determinism | R351-1 | 55079500483970ee244f12fa4c94401783f3df6f |
| Tests | CLEAN | ranking regeneration (both variants); ranking consistency check; six probe outputs; baseline and repository gates | R351-1 | 55079500483970ee244f12fa4c94401783f3df6f |
| Docs | UNCLEAN (R351-F1 MINOR open) | full page at head; PP_SHADOW_BASELINE_50MHZ_INPUTS.json:29-32; PP_SHADOW_BASELINE_50MHZ_RANKING.tsv; history-number check; docs gates; AREA_BUDGET.md:9 | R351-1 | 55079500483970ee244f12fa4c94401783f3df6f |

## 7. Prior public review findings (read after my independent pass)

I wrote my independent verdict and ledger first; the pre-read record is in `receipts/independent_verdict_before_prior_findings.txt`. Only then did I read the PR and issue comments. PR #589 carries the [R350] NEGATIVE review at this head (comment 5856181980), which was posted during this round. I resolve or retain its findings as follows:

- **[R350] F1, MINOR Docs (normalized-Verilog digest): RETAINED at MINOR as R351-F1.**
  - My independent pass found the same defect. The pre-read record lists it as a SUGGESTION under Docs and Tests.
  - I re-verified the specific claim with my own two exports: the rule as written gives `1f7c01e2...`, and the committed value needs the executor's private path (`receipts/normalization_rule_as_written.out`).
  - I retain MINOR rather than SUGGESTION for two reasons. First, the defect is a committed evidence value that its own stated method does not reproduce. Second, the assignment explicitly asks whether the committed JSON is reproducible. That makes a fix worthwhile, not optional, although it is non-blocking for the measurement itself. AGENTS.md section 7 also warns against using a lower severity to bank a lens.
  - I narrow the lens attribution to Docs: no test asserts the digest.
- **[R350] F2, SUGGESTION Docs (untagged historical 8x8 figures): RETAINED as SUGGESTION**, merged into R351-S1. I agree that each figure is recoverable from the adjacent labelled tables.

No other review findings exist on PR #589 or issue #587 at this head.

## 8. Real limits

- I reproduced the executed recipe, not an independent re-derivation of it. The VexiiRiscv netlist came from the host's cached netlist (hash-matched to the manifest), not a fresh generator build. The #231 recipe itself was accepted in #231 and is out of scope.
- I did not rerun the standalone OOC, Yosys, 1x1 or placement parts of the recipe. They are out of scope, and the page does not change their figures.
- All results are synthesis estimates. The setup WNS is negative and the synthesis-stage hold estimate is also negative (WHS -0.761 ns before placement; the page makes no hold claim). There is no placement, routing, board-interface signoff, bitstream or hardware result, and physical calibration was NOT RUN. The 50 MHz design still exceeds device LUT capacity by 4,647.
- The generated-file hash comparison relied on the executor's checkout and build roots published in the issue and in the handoff.
- Hosted evidence is a snapshot, not an acceptance. The manager's source-bank receipts were not in the published packet at `f847f343`, so I did not inspect them.
- As assigned, this reviewer did not run the full source, builder, native, parent, PP, gPTP or Yosys banks.

## 9. Pending manager duties

- Route R351-F1 (same as [R350] F1) to the executor. At the corrected head, Docs must be re-covered. The other four lenses stay covered at `55079500` only if the new commit touches nothing in their scope. A manifest-only edit would leave Conformance, RTL, Robustness and Tests covered, but a reviewer must confirm that.
- Update the #229 reference comment after merge (acceptance 2, manager-owned per the assignment).
- Hosted and act acceptance at the exact head, including exact-head `verilator-suites` and `yosys-portability` evidence (AGENTS.md section 7).
- Final current-dev candidate merge validation, post-merge containment, closing the issue and moving the card.
- Publish this packet.

## 10. Clone restoration

The disposable probe edits were reverted and the three recipe symlinks removed. Bytecode caches the gates created were deleted. At the end of the round:
- the worktree and index both equal HEAD `55079500`, and the index tree is `791dba22`;
- all 925 tracked non-gitlink blobs re-hash to the index with zero mismatches, and their modes all match;
- the gitlinks are protocol-processor `0922e434`, gptp-processor `5dce647a` and verilog-axis `48ff7a7e`, and all three submodules are clean;
- no shared LiteX checkout or environment was modified.

Receipt: `receipts/restore_verification.out`.

R351-1 FINISHED
