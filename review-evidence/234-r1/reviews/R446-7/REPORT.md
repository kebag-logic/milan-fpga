[R446] NEGATIVE - exact head 9b28c04bf7f23824b25f479b6584c4e5c8c4f334

# R446-7: composition review of issue #234 / PR #638, merge-train candidate

- Role: independent composition reviewer, cleared context.
- Candidate: `9b28c04bf7f23824b25f479b6584c4e5c8c4f334`, tree `04a0c948d8fabb836c64ac4c50271c3a8bc16c89`.
- Parents: live dev `546437243e87eb5a78783a9e3cd5d1badcc3423e`, PR head `d5f56313dc5a5c2716211356f99796664dc843dd`.
- Source reviews of the PR head, both POSITIVE at `d5f56313`: R446-6 (issue comment 5972052581) and R447-7 (issue comment 5972176095).
- Scope: what the composed tree adds beyond the two reviewed sources. It is not a new source review.

## Verdict

NEGATIVE. The text merge is clean and every hosted-equivalent gate I ran is green on the candidate. The composition has one semantic defect (F1, MAJOR).

The PR records the resource gate's route baseline at dev `1269cdaf`. Since then, dev has merged PR #634, which changes the shipping image's inputs. PR #634's own published measurement of that image already exceeds the recorded baseline by more than the LUT and FF tolerances. If the candidate's gate is fed those published figures, it returns exit 1. So the baseline the composed tree lands with already fails dev's current image, before any further change.

## Reconstruction

- Authorities read: AGENTS.md (sections 5 to 8), docs/README.md, and the issue #234 body.
- Public scope comments read on #234:
  - 5966260488: the lane, with base dev `1269cdaf` and pin `631eeb34`.
  - 5967852698: the manager's rulings (b), (c), (e), (a) and the gate policy.
  - 5967924270: the owner's decision. NFR-RES-01 stays at 60 %; "Until then: the #638 resource gate holds every resource at its recorded value."
- Requirement: NFR-RES-01 (`docs/reference/FR_NFR.md:318`). Dev's changes to FR_NFR.md do not touch it.
- Interface authorities: `docs/design/AREA_BUDGET.md` (the policy table and where the gate runs) and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.
- Merge identity: `git merge-tree --write-tree 546437243 d5f56313d` gives `04a0c948d8fabb836c64ac4c50271c3a8bc16c89`, which is the candidate's tree. The candidate is therefore the plain merge, with nothing hand-edited (`receipts/composition_identity.txt`, `receipts/candidate_identity.txt`).
- Dev delta since the PR's base `1269cdaf`, first-parent:
  - `bbf704ec`: PR #634, AAF and CRF media-clock following, lane M2. It is RTL, configuration, AEM, builder and test benches, 121 files in all.
  - `54643724`: PR #644, docs only. It changes `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and `docs/findings/README.md`.
  - #635 is not a PR. It is the processor pin `631eeb34`, already inside `1269cdaf`.
- The gitlinks are identical in both parents and the candidate: `protocol-processor` `631eeb34`, `gptp-processor` `5dce647a` and `external` `efeb541a`.

## Overlap and interaction inventory

| Shared surface | PR #638 | Dev since `1269cdaf` | Composition result |
|---|---|---|---|
| `docs/findings/README.md` (the only file both sides change) | adds the `PP_SHADOW_BASELINE.md` and `234_PP_SHADOW_AREA_BASELINE.md` rows | #644 rewrites the `629_...` row in place | clean: 19 rows, no duplicates, both parents' orders kept, the union of both row sets, and every link target present (`receipts/composition_checks.txt` part 1) |
| CI workflow and contract: `.github/workflows/rtl-fast.yml`, `scripts/ci_events.py`, `scripts/ci_scope.py`, `docs/testing/CI_WORKFLOWS.md` | changed | untouched | `ci_events.py --check` OK (1655 items) and `--selftest` rc 0. `ci_scope.py --selftest` rc 0. The candidate-vs-dev change set classifies as `true`, so the gate step runs |
| The gate's hosted inputs: `syn/ooc/*`, `docs/design/AREA_BUDGET.md`, the recipe | changed | untouched | the gate's self-test, mutants (174 of 174 killed) and `check-baseline` (3 endpoints) pass on the candidate, as does the whole rtl-fast step "Prove the OOC read sets come from run.sh" (`receipts/gates/`) |
| `syn/yosys/run.sh` and `ooc.sh`: `dp_srcs.py` asks `run.sh --emit` | untouched | #634 adds `KL_aaf_clock_meter.sv` to the `milan_datapath` row and an OOC top | `dp_srcs.py --top milan_datapath` rc 0 with 114 lines, the meter included, and `--top KL_pp_shadow` rc 0 |
| **The gate's measured inputs**: the shipping route (`sw/litex/build.sh ax7101` and every source, header, generic and image it reads) and the standalone `KL_pp_shadow` at the shipping generics | the baseline is recorded at dev `1269cdaf` | #634 changes `hdl/milan/milan_datapath.sv`, adds `KL_aaf_clock_meter.sv` (one instance at the 1x1 shipping shape, `AEM_N_AAF_CLKSRC_C = 1`), changes the CRF servo, NCO and grid align, `milan_soc.py`, `aem_rom.json`, and the shipping shape header (`AEM_NAME_ENTRIES_C` 38 to 39, passed to the processor as `DESC_NAME_ENTRIES_P` at `hdl/milan/milan_datapath.sv:7681`; `AEM_N_CLKSRC_C` 2 to 3) | **F1** |
| Docs gates over the composed tree | | | all green (below) |

## Gates run on the candidate

Every gate ran on a disposable shared clone of the review clone, detached at `9b28c04b` with the submodules at their gitlinks. The no-git runs used a `git archive` extraction of the same tree. The commands are in `scripts/composition_gates.sh`; each has a log and an rc file under `receipts/gates/`. The renderer-dependent gates were re-run under `receipts/gates_venv/`, with the repository's pinned renderer (`tools/markdown/requirements.txt`, hash-locked) installed in a scratch virtual environment.

| Gate | rc | Result |
|---|---:|---|
| `docs_check.py` (git) | 0 | 0 findings, 187 md files and 975 scrubbed text files |
| `docs_check.py` (no git) | 0 | 0 findings, with inventory parity skipped as designed |
| `check_feature_status.py` (no git) | 0 | |
| `gen_toc.py --check` | 0 | 129 pages |
| `gen_toc.py --verify-anchors` | 0 | 315 cross-page fragment links |
| `gen_toc.py --selftest` | 0 | |
| `check_doc_paths.py` | 0 | 900 cited paths resolve |
| `check_em_dash.py --base 54643724` | 0 | 0 findings over 614 added lines, arms 339 of 339 |
| `docs/DOC_MAP.gen.py --check` | 0 | |
| `check_doc_style.py`, `check_archive.py` | 0 | |
| `ci_events.py --check` and `--selftest` | 0 | |
| `ci_scope.py --selftest` | 0 | |
| `pp_resource_gate.py --selftest`, `pp_resource_gate_mutants.py`, `pp_resource_gate.py check-baseline` | 0 | |
| `dp_srcs.py --selftest`, `ooc_tcl_selftest.py`, `pp_baseline.py --selftest`, `pp_baseline_mutants.py`, `pp_baseline_reports_selftest.py` | 0 | the rest of the rtl-fast OOC step |
| `dp_srcs.py --top milan_datapath` and `--top KL_pp_shadow` | 0 | |

The first pass of the four renderer-dependent gates gave rc 2 (`receipts/gates/*.log`). The cause was that the renderer was not installed on this host, not a defect in the tree.

## Findings

### F1: MAJOR. The resource gate's recorded baseline already fails the composed tree's shipping image

- **Lenses:** Conformance, RTL, Robustness, Docs.
- **Where:** `syn/ooc/pp_resource_baseline.json` (`endpoints.route-1x1`: `"measured": "dev 1269cdaf, processor 631eeb34, issue #234"`; figures LUT 50128, FF 59006, SLICE 15815, WNS 0.063).
  - `docs/design/AREA_BUDGET.md:13`: "measures the current head".
  - `docs/design/AREA_BUDGET.md:107-118`: "does not meet it today", the 1269cdaf table, "35 slices left".
  - `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:347`: "35 left".
  - `docs/findings/README.md:23` and `:24`: "the current head's figures", and "The resource gate holds every resource at its recorded value".
- **Authority and evidence:**
  - The owner's decision (#234 comment 5967924270): "the #638 resource gate holds every resource at its recorded value."
  - #234 acceptance: "CI rejects material LUT, FF, BRAM, DSP, or timing regressions."
  - Ruling 5967852698: route tolerances of +500 LUT and +600 FF.
  - PR #634's public body records the shipping image at its merge. It was rebuilt at `c1288648` through `sw/litex/build.sh ax7101`, with Vivado 2026.1. The figures are LUT 50,767, FF 59,634, slices 15,832, WNS +0.193 and WHS +0.024. The meter alone, placed, is 483 LUT and 630 FF.
  - `c1288648` is dev `1269cdaf` merged into lane M2. Between it and the merged #634 head, no file under `hdl/`, `sw/litex/`, `configs/`, `avdecc/` or `syn/` changes, and #644 is docs only. So that image's inputs are the candidate's shipping inputs. PR #638 changes no build input.
  - Against the recorded route this is +639 LUT and +628 FF (`receipts/composition_checks.txt` part 2).
  - Feeding exactly these figures to the candidate's own `judge()` gives "LUT REGRESSION: grew by more than 500", "FF REGRESSION: grew by more than 600", "RESULT: MATERIAL REGRESSION" and exit status 1 (`scripts/judge_probe.py`, `receipts/judge_probe.txt`). The probe keeps the recorded identity and holds the unpublished BRAM, DSP and carry figures at their recorded values, so it can only be lenient.
  - My own Yosys run reproduces the meter's out-of-context cost on the candidate: 574 LUT (16 LUTRAM) and 636 FF (`receipts/yosys_ooc_aaf_clock_meter.log`). The meter's FFs alone exceed the route's +600 FF tolerance.
  - The standalone endpoints' inputs also changed, through the processor's `DESC_NAME_ENTRIES_P` 38 to 39 and the AEM ROM. I did not measure whether their figures moved.
- **Impact:**
  - Neither source has this defect alone. At its base, the PR's baseline described dev's image; dev alone has no gate. Composed, the gate lands with a baseline that dev's current shipping image already exceeds.
  - By the PR's own placement rule (AREA_BUDGET "Where the gate runs"), #638 changes no RTL, pin or recipe, so its merge bank runs no Vivado comparison and nothing catches the drift at merge.
  - The first later PR that does change RTL is judged against `1269cdaf`. It is then charged #634's +639 LUT and +628 FF: either a false exit 1, or #634's growth silently consumes that PR's tolerance or enters its re-baseline unreviewed.
  - That contradicts "holds every resource at its recorded value" and the issue's fourth criterion in the composed tree.
  - The docs' "current head" and "today" figures (LUT 79.07 %, 35 slices free, WNS +0.063) no longer describe the tree they ship in: #634 measured 80.07 %, 18 slices free and +0.193 ns.
- **Required outcome:** before merge, the baseline the composed tree carries must describe the composed tree's shipping image, or be explicitly and publicly accepted as not doing so. Either of these satisfies it:
  - (a) Re-measure `route-1x1`, `ooc-1x1` and `ooc-8x8` on the merge-train tree under the recipe and record them with `record --write` as a reviewed re-baseline, so that #634's growth is recorded as #634's. Then update or re-date the "current head" and "today" figures in AREA_BUDGET.md, the #234 findings page and the index rows.
  - (b) A recorded owner or manager decision that this merge accepts the `1269cdaf` baseline as predating #634, with #634's measured growth named. That decision must state how the first RTL-changing merge bank avoids charging that growth to the next PR. The docs must then stop calling the `1269cdaf` figures the current head.
- **Verification:**
  - For (a): `pp_resource_gate.py check <candidate route dir> --endpoint route-1x1` exits 0 on the composed tree, and `check-baseline` stays green.
  - For (b): the decision is linked from AREA_BUDGET.md, and `judge_probe.py` or a real `check` on the post-merge dev image is shown handled as the decision states.
  - In both cases, the docs gates listed above are re-run on the new candidate.

No other finding. No RESIDUE or SUGGESTION from this round.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #234 acceptance 4; owner decision 5967924270; ruling 5967852698; `syn/ooc/pp_resource_baseline.json` `route-1x1`; `syn/ooc/pp_resource_gate.py:310-354` `judge()`; PR #634's body figures; `receipts/judge_probe.txt` | R446-7 | `9b28c04bf7f23824b25f479b6584c4e5c8c4f334` |
| RTL | UNCLEAN (F1) | the composition touches this lens's resource and timing scope through the RTL #634 brought in: `hdl/ieee1722/crf/KL_aaf_clock_meter.sv` (Yosys 574 LUT and 636 FF, `receipts/yosys_ooc_aaf_clock_meter.log`); `hdl/milan/milan_datapath.sv:7681` (`DESC_NAME_ENTRIES_P`); `configs/generated/endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh` lines 31, 54 and 69 against `1269cdaf`. The PR itself changes no RTL file. | R446-7 | `9b28c04bf7f23824b25f479b6584c4e5c8c4f334` |
| Robustness | UNCLEAN (F1) | the gate's behavior under a predecessor's merge (ordering and configuration-dependent): `judge()` on the composed tree's published image figures returns exit 1 with no change of the next PR's own; `docs/design/AREA_BUDGET.md` "Where the gate runs" (no Vivado run at a non-RTL merge) | R446-7 | `9b28c04bf7f23824b25f479b6584c4e5c8c4f334` |
| Tests | CLEAN | `receipts/gates/`: `pp_resource_gate.py --selftest`, `pp_resource_gate_mutants.py` (174 of 174 killed, control passes), `check-baseline`, `dp_srcs.py --selftest`, `ooc_tcl_selftest.py`, `pp_baseline.py --selftest`, `pp_baseline_mutants.py`, `pp_baseline_reports_selftest.py`, `ci_scope.py --selftest`, `ci_events.py --selftest`, `gen_toc.py --selftest`, all rc 0 on the candidate. No PR test reads a file dev changed; `dp_srcs.py --top milan_datapath` resolves dev's new `run.sh` row. The tests' own design is covered by the source reviews R446-6 and R447-7 at `d5f56313`. | R446-7 (composition); R446-6, R447-7 (source) | `9b28c04bf7f23824b25f479b6584c4e5c8c4f334`; source `d5f56313dc5a5c2716211356f99796664dc843dd` |
| Docs | UNCLEAN (F1) | `docs/findings/README.md` composition clean (`receipts/composition_checks.txt` part 1); docs gates all rc 0 (`receipts/gates_venv/`, `receipts/gates/`); but `docs/design/AREA_BUDGET.md:13,107-118`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:347` and `docs/findings/README.md:23-24` state the `1269cdaf` figures as the current head or today, which the composed tree's dev side no longer matches (F1) | R446-7 | `9b28c04bf7f23824b25f479b6584c4e5c8c4f334` |

## Real limits

- I ran no Vivado. F1's route figures for the composed image are PR #634's published measurement, not my own. Its inputs match the candidate's shipping inputs, as shown above. Vivado's run-to-run variation is not bounded here, but the margins exceed the tolerances by 139 LUT and 28 FF.
- I did not measure the standalone endpoints `ooc-1x1` and `ooc-8x8` on the candidate. Their inputs changed; whether their figures did is unknown.
- I ran no hosted workflow, `act`, full bank, Yosys portability bank or builder bank. The rtl-fast "Elaborate the integration-heavy tops" step and `ooc_selftest.py` were not run, because the PR changes no elaborated source and no `ooc.sh`.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- The docs gates needed the pinned renderer, which I installed in a scratch virtual environment. The host has none.

## Review clone restored

I made no edit in the review clone. All probes ran in a disposable shared clone under `scratch/`. At the end, the review clone's HEAD, tree, index tree and worktree all equal `9b28c04b` and tree `04a0c948`. Its status is empty, and the submodules sit at the required gitlinks with no changes (`receipts/review_clone_integrity.txt`).

## Pending manager duties

- Resolve F1 by (a) or (b) before merge, then rebuild the merge-train candidate and send it for re-review.
- Hosted and act acceptance of the exact candidate, including the protected `rtl-fast`, `verilator-suites` and `yosys-portability` contexts.
- The final current-dev candidate at the merge turn, if dev moves again.
- Carry the retained RESIDUE R446-5 R1 (below) to the residue checklist.

## Prior findings at this head

I wrote this section after the verdict, findings and ledger above. Before writing those, I read no other reviewer's report.

The merge leaves every file the PR changes byte-identical to the PR head `d5f56313`, except `docs/findings/README.md`. In that file the only difference is dev's #644 rewrite of the `629_...` row (`git diff --stat d5f56313d 9b28c04bf -- <PR files>`: 1 file, 1 line). So no prior source finding can have moved in the composition. The states below are the latest source reviews' states, carried forward on that byte identity.

| Prior finding | State at `9b28c04b` | Evidence |
|---|---|---|
| All BLOCKER, MAJOR and MINOR findings of R446-1 to R446-6 and R447-1 to R447-6, the last being R447-6 F1 (MINOR Docs, PR body) | **Remain resolved** | They were resolved at `d5f56313` per R446-6 (5972052581) and R447-7 (5972176095). The gate code, tests and docs are byte-identical here, and the gate's self-test, mutants and `check-baseline` rerun green on the candidate (`receipts/gates/`). |
| R446-6 R1 and R447-6 R1 (RESIDUE, PR body) | **Remain resolved** | Per R447-7, the PR body was edited at `d5f56313`. |
| R446-5 R1 (RESIDUE Docs, PR body): the Round 5 row says "run by `strict()` on every JSON the gate reads" | **Retained** as RESIDUE | The live PR body still contains the phrase once. The exact fix stands as R446-5 gave it: "run by `strict()` on every JSON that `check`, `record` and `check-baseline` read". |
| R447-7 S1 to S3, R446-6 S1 and R446-5 S1 (SUGGESTION) | **Retained**, optional | The code is unchanged. |
| The prior reviews' pending duty: "validate the final current-dev candidate at the merge turn (live dev `bbf704ec`)" and "run the Vivado comparison in the merge bank" | **Open; this round's F1 is what that duty finds** | The prior rounds name the duty without judging it. F1 judges it, using PR #634's published image. |

R446-7 FINISHED
