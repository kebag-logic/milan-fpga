[R332] NEGATIVE - exact head af6d19c553ad8c445a80528344baf2273b41ad46

Round R332-1, internal cleared-context review of PR #572 for issue #231 (parent epic #229).
Head `af6d19c553ad8c445a80528344baf2273b41ad46`, tree `abdc83b490114b217f40951173d637cbe2ba7dcf`, source base `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.
All five lenses were applied. Three MINOR findings remain open, so Conformance, Tests and Docs are unclean. RTL and Robustness are clean.

The measurements themselves hold up. Every figure I reproduced matched the page to the digit:

- both standalone OOC products;
- the shipping 1x1 integrated place-and-route;
- the integrated 8x8 synthesis;
- both Yosys mappings.

The open findings concern a documentation gate that fails on a clean checkout, the completeness of the hierarchy tables, and a self-test that cannot detect removal of the #246 guard.

## Reconstruction

- Authorities read: AGENTS.md, CONTRIBUTING.md, docs/README.md, docs/development/CODE_QUALITY.md (Rule 12).
- Issue #231 body and its frozen acceptance criteria.
- The scope decision in issue comment 5844867171: integrated means the placed-and-routed wrapper inside the shipping 1x1 AX7101 build, plus integrated synthesis only for 8x8. The historical substitution delta stays as quoted history.
- Epic #229, workstream 1.
- The corrected historical evidence in issue comment 5411378865.
- The diff `7eb3b0d4..af6d19c5`: one commit and 5 files. No `hdl/` change and no gitlink change.
- The public evidence tree at `63cd047a`, `review-evidence/231-r1`, and the author's [A328] REVIEW READY comment.
- Prior review findings on this PR: none exist. At review start the only PR comments were the two review-start notices, and the PR had no review objects or line comments. Nothing needed to be resolved or retained.

## What was reproduced (clean checkout, recipe as committed)

I made a fresh clone at the head with the three pinned submodules. The SDK was extracted from the pinned archive and verified by `scripts/ci_rv32_sdk.py`. Vivado was 2026.1 build 6511674 and Yosys was 0.66 (`86f2ddebc-dirty`), the same identities as the author's.

I executed the recipe verbatim, with these exceptions:

- only the maxThreads line differs: 4 threads for the integrated scripts and 2 for OOC, against the recipe's 32 (diffs recorded);
- the two placement-directive comparisons were not rerun.

Every Vivado and Yosys run returned rc 0 with zero `Synth 8-4445` diagnostics (`receipts/reproduced/run-status.txt`).

| Measurement | Reproduced | Page / published report |
|---|---|---|
| Export images (6 per shape) | sha256 equal to `PP_SHADOW_BASELINE_INPUTS.json` for all 12 records | identical |
| Wrapper parameters, 1x1 and 8x8 | 20/20 equal (paths repo-relative) (`receipts/params-compare.txt`) | identical |
| Source set | 118 `read_verilog` in identical order and options, integrated vs OOC. The 3 CPU-core sources hash equal to the published record. Only the generated `.v`, which embeds absolute paths, differs (`receipts/source-hashes-compare.txt`) | consistent |
| Vivado OOC 1x1 | 22,350 LUT / 24,533 FF / 21+3 BRAM / 5 DSP / 1,415 CARRY4 / WNS -6.180 ns, same worst path. Hierarchy and utilization reports have 0 diff lines. The primitive census sha256 `edfd86ab...` equals the omitted-file record | identical |
| Vivado OOC 8x8 | 28,992 / 32,984 / 26+5 / 5 / 1,775 / -10.987 ns. Census sha256 `17f32ee5...` equals the record | identical |
| Integrated 1x1 synthesis | hierarchical report identical except the date line | identical |
| Integrated 1x1 shipping route | 48,618 LUT, WNS +0.013 ns, WHS +0.014 ns, 0 failing setup, hold or pulse-width endpoints, 102,740/102,740 nets routed, IOB check identical, 46/87 missing I/O delays. Census sha256 `ee11fb0d...` equals the record | identical |
| Integrated 8x8 synthesis | 68,136 LUT (107.47 %), WNS -11.331 ns. Hierarchical and flat reports have 0 diff lines | identical |
| Yosys 1x1 / 8x8 | 41,258/5,972/47,230/23,041/15/4/5/1,813 and 65,724/6,136/71,860/32,615/16/4/7/2,108 | identical |

Other checks:

- All 28 hierarchical table rows (LUT, FF, RAMB36, RAMB18, DSP, internal WNS) match the published reports (`receipts/page-tables-vs-public-reports.txt`).
- The CARRY4 columns for OOC 1x1, OOC 8x8 and the shipping route match my censuses.
- The mapping reconciliation arithmetic (24,880 and 42,868) is exact.
- Yosys attribution confirms the three memory-mapping rows:
  - `u_notify/rows_r` is 1,024 RAM32M, against 2,048 FFs in Vivado;
  - listener `rec_ram_r` is 52 RAM32M;
  - timer `slot_ram_r` is 14 RAM64M.
- The BRAM tile table holds, including `g_rx_pool[3]` being absent in both flows.
- The extra 8x8 DSPs are the RATE and CLKS record-offset multipliers; the BIND multiplier appears at both shapes.
- The sv2v output is byte-identical across shapes, so all geometry reaches Yosys through the 18 `chparam` values.
- The historical figures (eff99a9c: 56,779 to 55,466 LUT, 109 to 135 BRAM tiles, 5,079 flops) match `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:329,465,466,483`. The corrected pin pair (38,879 at b3507ddd against 34,215 at 04b55dad) matches comment 5411378865. The page presents both under "Historical comparison" as not current.
- Both protocol-processor ROMs match `syn/yosys/rom_digests.tsv:30-31` for pin 990f965.

## Findings

### F1 - MINOR - Docs, Tests - `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:41` - The doc-path gate fails on a clean checkout of this head

- **Authority and evidence:**
  - The recipe cites `` `sw/builder/out` `` with no trailing slash.
  - The `.gitignore` entry is directory-only (`sw/builder/out/`), so `git check-ignore` does not excuse the path when the directory is absent.
  - `scripts/check_doc_paths.py` then reports `MISSING sw/builder/out` and exits 1. Its `ignored()` docstring says a gate that "changes verdict between two checkouts of the same commit is worse than no gate".
  - Reproduced from a `git archive` export of the head: rc 1. With the directory created the gate passes. With the trailing-slash spelling it passes with the directory absent (`receipts/doc-paths-clean-export.txt`, `receipts/gate-check_doc_paths.log`).
  - The hosted `docs-check` passed only because its "End-station builder gates" step creates the directory before the "Doc cited-path gate" step runs (`receipts/hosted-docs-check-doc-paths.txt`).
  - The author's `gates/doc-paths.log` rc 0 came from a tree that already contained the directory. The recipe's own precondition ("a clean checkout with no existing `sw/builder/out`") therefore guarantees this gate fails.
- **Impact:** a required documentation gate is red for anyone who validates a clean checkout or follows the recipe. The hosted green depends on step ordering.
- **Required outcome:** the citation resolves, or is excused, on a clean checkout, so `check_doc_paths.py` exits 0 whether or not a builder has run.
- **Verification:** export the fixed head, `git init && git add -A`, run `python3 scripts/check_doc_paths.py` without `sw/builder/out`, and expect rc 0.

### F2 - MINOR - Conformance, Docs - `docs/findings/PP_SHADOW_BASELINE.md:93-160` (fixed list `syn/ooc/pp_baseline.py:51`) - The hierarchy tables are a fixed subset that omits larger consumers than the ones listed

- **Authority and evidence:**
  - Issue #231 acceptance says "Reports identify the dominant resource consumers by hierarchy". Epic #229 workstream 1 says "Record per-module LUT, FF, RAMB18, RAMB36, DSP, carry, and timing figures".
  - The page calls itself the reference for the remaining tickets, and the #229 comment says it "records complete hierarchy resources".
  - Each of the four tables lists only `u_pp`, five children and `u_nvm`, with no remainder row. Reproduced direct-child rankings (`receipts/u_pp-direct-children-ranked.txt`):
    - OOC 1x1: `u_dispatch` is 879 LUT and the listed `u_talker` is 860.
    - OOC 8x8: `u_timer` is 1,452 against `u_talker` at 1,354. `u_timer` growth (694 to 1,452, +758) is the second-largest standalone scaling term, and it goes unmentioned.
    - Integrated 8x8: `u_timer` is 1,460 against `u_talker` at 848.
    - Shipping route: `u_originator` (743) and `u_nvm_shadow` (732) both exceed `u_talker` (716).
  - The listed children cover 14,522 of 21,762 `u_pp` LUTs at OOC 1x1 (66.7 %).
  - The complete `baseline_hierarchy.rpt` files exist only in the uncommitted review-evidence tree, and the page does not reference them.
  - Workstream 3 targets several of the omitted blocks: timer deadlines, dispatch queues, originator, trace and TX slots.
- **Impact:** follow-up optimization tickets have no committed baseline figure for several blocks they target. The table ordering implies a dominance ranking that the reports contradict.
- **Required outcome:** the committed baseline records per-module figures for every direct child of `u_pp`, or for every child above a stated threshold plus a remainder row, in each measured flow. Alternatively it binds a durable, committed complete hierarchy. The page's completeness claims must match what is recorded.
- **Verification:** compare the page rows against `baseline_hierarchy.rpt` direct children for all four flows. No omitted child may exceed a listed one, and listed plus remainder must equal the parent.

### F3 - MINOR - Tests - `syn/ooc/pp_baseline.py:231-277` - The self-test cannot fail when the #246 guard or the other enforcement lines are removed

- **Authority and evidence:**
  - AGENTS.md section 6, Tests lens: "Each new test can fail for the defect it claims to detect". Issue #231 requires every ROM input to be proven present with zero `Synth 8-4445`.
  - The self-test exercises only `image_record`, `parameters` and `wrapper_parameters`. It never runs `inventory()`, `prepare()` or `main()`.
  - Each of these single-line mutants still prints "9 refusals PASS" at rc 0 (`receipts/selftest-mutations.txt`):
    - removing the promotion `prefix += ROM_ERROR` (line 188);
    - disabling the `$readmemh` inventory equality (lines 161-163);
    - accepting a non-empty SRAM image (line 158);
    - disabling the outside-repository guard (lines 297-299).
  - The guards themselves work when present. My probes show Vivado returns rc 1 on a missing image only with the promotion, and rc 0 without it (`receipts/probe-synth-8-4445.txt`). All 10 image and inventory mutations are refused (`receipts/probe-helper-image-checks.txt`).
  - Only the executed guards are proven. No executable check keeps them in place, and no gate runs `--selftest` (it appears only in the recipe).
- **Impact:** a later edit can silently reopen the #246 missing-ROM trap. The failure mode is a plausible rc 0 utilization that is thousands of LUT low.
- **Required outcome:** the self-test drives `inventory()` and `prepare()` on a synthetic export. It asserts the promotion precedes `synth_design` in both emitted scripts, and that missing LiteX init files, non-empty SRAM images and in-repository output are refused. Each mutant above must make it fail.
- **Verification:** apply the four mutants in `receipts/selftest-mutations.txt` and expect a non-zero self-test for each. The unmodified self-test must still pass.

### Suggestions (do not affect coverage)

- **S1 - SUGGESTION - Robustness - `syn/ooc/pp_baseline.py:183-226`.** Nothing binds `--integrated-log` to the export it is paired with. The 1x1 export with the 8x8 log yields rc 0 and a script with 1x1 includes and `N_STREAM_IN_P=9` (`receipts/probe-mixed-shape.txt`). The recipe pairs them correctly, so this is operator error only. Consider checking that the log's wrapper source path or include set matches the export.
- **S2 - SUGGESTION - Robustness - `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:262`.** The post-run image rehash is a manual step. A file that shrinks between preparation and the Vivado read raises no `Synth 8-4445`, because the file still exists. Consider automating the rehash against `baseline_images.json`.
- **S3 - SUGGESTION - Docs - `docs/findings/PP_SHADOW_BASELINE.md:154-160`.** The integrated-vs-standalone AECP gap is recorded but not explained: `u_dyn` goes from 574 to 6,915 LUT at 8x8, and from 111 to 1,296 at 1x1 route vs OOC, with equal FFs and BRAM. It is the largest single integrated consumer. A follow-up issue to root-cause it would keep the baseline from being used additively.

## Clean lenses

- [R332] PASS RTL - `git diff --stat 7eb3b0d4..af6d19c5`; `hdl/milan/KL_pp_shadow.sv:180-245`; generated `baseline_ooc.tcl` and `clock.xdc`; 8x8 `alinx_ax7101.tcl` include order; `protocol-processor/hdl/aecp/KL_aecp_notify.sv:274`; `syn/ooc/pp_baseline.py:36-68` - Checked the following:
  - No RTL or gitlink change.
  - The wrapper has one clock, `clk_i`, which is the only constrained port, loaded before synthesis at 10 ns.
  - All 20 wrapper parameters, including 16-bit `SRP_DOM_DEF_VID_P` and 32-bit base addresses, pass as generics equal to the integrated elaboration for both shapes.
  - The part is `xc7a100t-fgg484-2` for both flows.
  - `SYNTHESIS` is implicit in Vivado and explicit in Yosys.
  - The 8x8 build resolves `gen/adp_shape_defaults.svh` from `configs/generated/endstation_ax7101_8x8`, because it is first in `include_dirs` (9/9 contexts confirmed in the log). The launcher's tracked-header refusal is previewed only, as the recipe states.
  - Scoped-timing semantics (both endpoints inside the instance) match the page's labels.
  - The notify `ram_style="distributed"` attribute on 128x16 rows explains the Vivado 2,048-FF versus Yosys RAM32M mapping as stated.
- [R332] PASS Robustness - `syn/ooc/pp_baseline.py:71-180,297-301`; `receipts/probe-helper-image-checks.txt`; `receipts/probe-synth-8-4445.txt`; `receipts/clean-clone-after-recipe.txt` - Checked the following:
  - Short, long, narrow, non-hex, missing and empty ROMs are refused.
  - A missing LiteX init, a short identifier memory, a non-empty SRAM and a duplicated image parameter are refused.
  - Output inside the repository is refused, and nothing is created.
  - The promoted `Synth 8-4445` stops Vivado (rc 1, script not completed).
  - An ambiguous or foreign parameter block is refused (self-test).
  - After the full recipe and its cleanup, the clean clone has no tracked, untracked or ignored residue beyond `__pycache__`. Tracked content equals HEAD.
  - Only S1 and S2 (suggestions) remain.

## Lens coverage for unclean lenses

- **Conformance:** applied against each #231 acceptance criterion and the 5844867171 decision, using the reproductions above.
  - Clean-checkout reproduction of both OOC products: met, exact.
  - Standalone, integrated, Vivado and Yosys labelling: met.
  - Part, constraint, parameters, defines and source set: met.
  - Integrated 1x1 route plus 8x8 synthesis only: met.
  - Historical figures quoted with provenance and not presented as current: met.
  - Linked from #229: met (comment 5845524962).
  - Dominant consumers by hierarchy and per-module figures: F2.
- **Tests:** applied to `pp_baseline.py --selftest` by mutation (F3). Focused gates rerun at the head:
  - pass: py-idiom, docs_check, em-dash, TOC, doc style, pp_srcs --check, self-test;
  - fail: doc paths (F1).
  - Hosted exact-head contexts: every executed job succeeded, and `Physical gPTP` was skipped (not hardware evidence).
- **Docs:** applied to all four changed pages. Every numeric claim was checked against reproduced or published reports. The privacy scrub passes (`docs_check`: 0 findings) and the page contains no bench-identifying text. Findings: F1, F2 (and S3).

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | issue #231 AC + 5844867171; epic #229 WS1/WS3; PP_SHADOW_BASELINE.md; INPUTS.json; reproduced OOC, route, 8x8 synthesis and Yosys runs | R332-1 | af6d19c553ad8c445a80528344baf2273b41ad46 |
| RTL | CLEAN | diff stat (no hdl/gitlink); KL_pp_shadow.sv parameters and clock; generated OOC/integrated Tcl; 8x8 include resolution; KL_aecp_notify.sv:274; SCOPE_TIMING Tcl | R332-1 | af6d19c553ad8c445a80528344baf2273b41ad46 |
| Robustness | CLEAN | pp_baseline.py refusal paths under 10 mutations; Vivado 8-4445 promotion probe; in-repo output guard; mixed-shape probe (S1); recipe cleanup residue | R332-1 | af6d19c553ad8c445a80528344baf2273b41ad46 |
| Tests | UNCLEAN (F1, F3) | pp_baseline.py self-test under 4 mutants; focused gates at head; hosted exact-head check runs | R332-1 | af6d19c553ad8c445a80528344baf2273b41ad46 |
| Docs | UNCLEAN (F1, F2) | PP_SHADOW_BASELINE.md, PP_SHADOW_BASELINE_RECIPE.md, INPUTS.json, AREA_BUDGET.md:9-11; history page lines 329/465/466/483; doc gates | R332-1 | af6d19c553ad8c445a80528344baf2273b41ad46 |

## Real limits

- The two comparison placements (`AltSpreadLogic_high`, `ExtraTimingOpt`) were not rerun. Their page rows were checked only against the published reports: whole and wrapper LUT, route status, IOB check and scoped timing. Their full timing reports are omitted from the public packet.
- My runs capped Vivado at 4 or 2 threads instead of the recipe's 32. All compared outputs were nevertheless identical.
- The LiteX environment was the host's existing one, used read-only. Its patch series was not re-derived. The Yosys package is the host install and is not pinned, as the page states.
- No full parent, PP, gPTP, Yosys or builder bank was run, and no act or hardware run. Physical calibration was NOT RUN, and field skips are not hardware proof.
- The integrated-vs-standalone AECP difference was not root-caused (S3).

## Pending manager duties

- Answer F1-F3 and then re-review the corrected head. This round does not approve later fixes.
- Obtain the external review (R333) and assemble the completion ledger at the merge candidate.
- Build and validate the candidate merge result at the merge turn. Base 7eb3b0d4 is the live dev tip, so the head tree is the candidate tree if dev has not moved.
- Run the act-first local replica and accept the hosted contexts on the final head.
- Merge only with maintainer authorization, then run post-merge containment.

Receipts and portable scripts are listed in `MANIFEST.sha256`. Paths in receipts are written relative to `$PACKET`, `$REVIEW_CLONE` and `$HOME`.

R332-1 FINISHED
