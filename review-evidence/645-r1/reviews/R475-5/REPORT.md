[R475] POSITIVE - exact head 17c39e57f450c3e99d073b7589172a2af9c2f8e7

External independent composition review R475-5 of issue #645 (with its included #647 work) and PR #672, merge-train candidate.

The candidate is `17c39e57f450c3e99d073b7589172a2af9c2f8e7`, tree `47e1e22d511016d3772c33419afc84ca88930f55`. Its parents are live dev `6aa25dec977c6ad78bf4ff6275de47fb81d0c246` and PR head `85db353400c6bf3965d279a9f5b5d47e08a0d1ed`, over merge base `99e4eb6c14462aafa84bb1ac597fd241abc1a240`.

This round judges the composition only. The PR's source verdicts are separate. At this candidate, all five lenses are CLEAN for the composed tree and no new finding is raised. One prior wording RESIDUE and three prior SUGGESTIONs are retained unchanged. They are carried below with candidate locators.

The verdict and ledger were drafted before any prior review report was read. Prior findings were read afterwards and are dispositioned in "Prior public findings".

## Reconstruction

The scope was rebuilt in this order:

- AGENTS.md and CONTRIBUTING.md, in particular section 2.1 step 7, candidate-merge validation;
- docs/README.md;
- issue #645's frozen acceptance and the manager rulings on the issue (stage, round-2, span, timing, T1 and round-2e rulings);
- `docs/design/AREA_BUDGET.md` (the resource gate and its re-baseline and merge-bank rules) and `docs/integration/BUILDING.md` section 5;
- `git diff 6aa25dec..17c39e57`, `git diff 99e4eb6c..85db3534`, `git diff 99e4eb6c..6aa25dec` and history;
- the author's round-2e public evidence under `review-evidence/645-r1/author-r2e/round2e/` at `00f489b18c63d9cf7e617ddb9e0437902062d416`: `resource-summary.json`, `area-ooc/comparison.json` and `prepare.py`, `logs/render-default.log` and `physical/milan_dp_gptp.log`;
- the review-ready comment 6056511818.

Since #645's last dev merge (`99e4eb6c`), dev gained three PRs:

- PR #694 (#654, SoC CPU option refusals);
- PR #695 (#686, fabric MAAP Annex B, its fifth resource re-record and comment refreshes in `milan_datapath.sv`);
- PR #690 (F4, SRP firmware, the lwSRP submodule and the act_ci manifest).

## Composition facts (receipts/01, 02, 05)

- **The merge is automatic and exact.** `git merge-tree --write-tree 6aa25dec 85db3534` reproduces tree `47e1e22d` with no conflict, so the candidate merge commit carries no hand resolution.
- **Path partition:**
  - 38 PR-side paths and 83 dev-side paths changed since the merge base.
  - 33 PR-only and 78 dev-only paths hold exactly their side's blob in the candidate.
  - The five paths changed on both sides are `hdl/milan/milan_datapath.sv`, `sw/builder/test_builder.py`, `scripts/measure_test_evidence_readers.py`, `docs/testing/TESTING.md` and `tb/verilator/milan_dp/README.md`. That matches the manager's list.
- **Both sides survive in each of the five both-sides paths.** For each one, `git patch-id --verbatim` of the PR-side delta (base to PR) equals that of dev to candidate. The dev-side delta (base to dev) equals that of PR to candidate. No RTL hunk, test registration, evidence-reader disposition or document row was lost.
- **RTL independence.**
  - Dev's change to `milan_datapath.sv` is 19 changed lines, all `//!` comments, at `hdl/milan/milan_datapath.sv:264-284`. They cover the KL_maap area figure and the four-PROBE claim-walk wording. It adds one net line.
  - The PR's datapath hunks are the settle recentre: `:1219-1223`, `:1312-1314` (`.lb_recentre_i ({LB_STREAMS_C{settle_recentre_p_r}})`), `:6019-6025`, `:6566-6653`, and the render pulse at `:6664-6667`.
  - No PR-added RTL line names MAAP, admission or SRP signals.
  - `KL_maap.sv` in the candidate is dev's blob `6adb624a`, with an unchanged module port list. `KL_chan_map_capture.sv` is the PR's blob `58539a09`.
- **The glue copied into the follow_ring harness is unchanged.** `tb/verilator/follow_ring/dp_glue.py` was run over the PR-head and candidate datapath texts. The non-comment lines are byte-identical: 190 lines, sha256 `99e78387...`. Only the provenance comment line offsets move by +1 (receipts/04).
- **No newly stale line citation.** Neither side adds a line citing any of the five both-sides files by line number. Every moved citation in the tree predates the merge base and is byte-identical in both parents (receipts/09).

## Resource position (manager question)

**Arithmetic only.** No vendor-tool measurement of this candidate exists, and none was run in this round. The scripts are in receipts/06 and receipts/03.

- **Own-area OOC +113 LUT / +78 FF carries over unchanged.** The author's `prepare.py` regenerates all six OOC inputs from the candidate: `cmc_base/head.sv`, `piece_base/new.svh` and `settle_base/new.sv`. Every one is byte-identical, by sha256, to the published `area-ooc/comparison.json` inputs. #686 touches none of them.
- **The candidate's recorded baseline is #686's fifth re-record.** For route-1x1 that is 50,391 LUT / 54,263 FF / 15,788 slices, WNS +0.241 ns, WHS +0.029 ns, with inputs at `e519e31f`. The gate's own `judge()` gives:
  - **#645's published route-1x1 figures** (49,913 / 54,309 / 15,754, WNS +0.057, WHS +0.024) **pass against it:** LUT -478, FF +46, slices -34, WNS -0.184 against the 0.25 fall limit, floor +0.030 met.
  - **A linear estimate of the composition** (#686 record plus #645's delta from F) is 50,347 / 54,298 / 15,808, WNS +0.174. That passes as well: LUT -44, FF +35, slices +20.
- **Area is predicted to pass with wide margin. Timing is not predictable from published figures.**
  - The only measured WNS that includes #645 is +0.057 ns, only 0.027 ns above the floor.
  - The composed image (#645 plus #686's re-mapped KL_maap plus #693's capture change) has never been placed, and placement is noise-dominated (`BUILDING.md:80`).
- **Answer: yes, the candidate's route-1x1 needs a fresh measurement before merge.**
  - `AREA_BUDGET.md:244` puts the measurement and `check` in the manager's merge bank for every PR that changes RTL. `:248` says the trigger is the merge result's delta from the record.
  - `AREA_BUDGET.md:194-195` says a merge that moves the shipping image records its own re-baseline on its merge result.
  - The candidate's record (`syn/ooc/pp_resource_baseline.json:451,919,1377`, "RTL inputs at e519e31f") describes neither #693's nor #645's RTL.
  - This is a pending manager duty under a documented rule, not a defect the composition introduces. Neither PR's source tree carried its own re-record, and the merge bank rule exists to catch exactly this.

## Gates and suites run on the candidate

All of these ran on a byte-identical copy of the candidate, with the pinned simulator release 5.050 (the CI pin). Receipts are under `receipts/runs/`.

- **Source and documentation gates: 43 of 43 pass** (receipts/08). They include:
  - `check_em_dash.py --base 6aa25dec`: 0 findings over 301 added lines in 9 pages;
  - `check_em_dash.py --base 85db3534`: 0 findings over 741 added lines in 18 pages, and `--selftest` 339/339;
  - `gen_toc.py --check` (140 pages), `--verify-anchors` (416 links) and `--selftest` (1501/1501);
  - `docs_check.py` (0 findings in 200 pages);
  - `ci_events.py --check` (1741 contract items over 4 workflows and `CI_WORKFLOWS.md`) and `--selftest`;
  - `measure_test_evidence.py --check` ("0 <= 0 unexplained DUT-source readers") and `--selftest`;
  - `docs/traceability/gen_module_matrix.py --check` (77 modules, up to date);
  - `pp_resource_gate.py check-baseline` (3 endpoints) and `--selftest`;
  - `lint_rtl.py --check` (90 <= ratchet 90), `pp_srcs.py --check`, `check_rtl_source_lists.py` and `check_port_contracts.py`;
  - `check_wire_accountability.py` (42 checks), `check_feature_status.py`, `check_solution_docs.py` and the idiom and hygiene ratchets.

  The six Markdown-renderer gates first refused with exit 2 under the system interpreter, because the pinned renderer was not installed. They passed when rerun under a private environment holding the hash-pinned renderer (`tools/markdown/requirements.txt`). The refusals are kept in `receipts/runs/static-env-refused/`.
- **Builder.** `test_baremetal_profile_contract` passes. This is gate 1b, which reads the composed datapath text, including the PR's "settle recentre withheld from the LOOP queues" control at `sw/builder/test_builder.py:13087,15933`. Dev's `test_soc_option_refusals` passes as well, with 52 constructor cases, 18 CLI cases and 9 killed controls. Both ran alone, not as a bank (`runs/builder_focus.*`).
- **follow_ring.**
  - `make run`: b8 and pullin 18 checks, 0 failures; small pulls 10/10; settle control PASS at 6.25, 25, 50 and 100 MHz.
  - `make mutants`: 12/12 controls caught, each by its named check.
- **chmap_capture** `run netcheck`: 785 behavioral and 20 netlist checks, 0 failures.
- **milan_dp_render** (default target), the shipping-shape datapath with KL_maap:
  - tdm8render 272 checks, tdm8render-multi 71 checks, leg defects 5/5;
  - run output byte-identical to the author's source run (receipts/07).
- **Physical-rate gPTP leg** (`milan_dp_gptp`, main `ax1x1gptp` run):
  - 143 checks, 0 failures;
  - both wire recentres at output PDUs 9822 and 95985, declared and observed -5, with dup and skip counters unchanged;
  - simulation stdout byte-identical to the author's source run (receipts/10).
- **Dev's `crflic` leg** (milan_dp: MAAP claim, CRF licence, with #686's harness on the composed datapath): 417 checks, 0 failures.

## Lens results

[R475] PASS Conformance - `hdl/milan/milan_datapath.sv:6566-6667` with `hdl/ieee1722/maap/KL_maap.sv` (blob 6adb624a); `runs/follow_ring_run.log`, `runs/render_default.log`, `runs/gptp_physical.log`, `runs/crflic.log` - checked that the composed tree still meets #645's ruled settle-recentre law (one recentre per transient, ring centred, no post-settle slip, declared -5 wire steps) and that #686's Annex B engine still claims and licenses CRF on the composed datapath. The PR's behaviour reproduces byte-identically on the render and physical legs, and crflic passes 417/417. The bench-repeat criterion is not a composition matter and remains pending.

[R475] PASS RTL - `hdl/milan/milan_datapath.sv:264-284` (dev, comment-only) against `:1219-1314,6019-6025,6566-6667` (PR); receipts/05 - checked that the dev-side delta is 19 comment lines and 0 RTL, that the PR's added RTL references no MAAP, admission or SRP net, and that the KL_maap port list is unchanged. Elaboration is clean in five composed builds (tdm8r, tdm8r-multi, ax1x1gptp, crflic, follow_ring wrap), and `lint_rtl.py --check` is at ratchet (90 <= 90).

[R475] PASS Robustness - `runs/follow_ring_mutants.log` (12/12), `runs/render_default.log` (leg defects 5/5), `sw/builder/test_builder.py:13087,15933` (gate 1b mutant table, PASS), `runs/chmap_capture.log` (785+20) - checked that the PR's negative controls (overshoot, single-drop, held-dup, starved-held-dup, early, W1, render-only and the six settle-controller defects) still fail their named checks on the composed sources, and that dev's SoC option refusal controls (9 killed) still bite.

[R475] PASS Tests - `sw/builder/test_builder.py:11392,13087,28754,29063`; `scripts/measure_test_evidence_readers.py:72,92,98`; `docs/testing/TESTING.md:514,522`; receipts/02 and 08 - checked that both sides' test registrations survive. `test_soc_option_refusals` is first in the `__main__` tuple and the PR's gate-1b pins and control are present. Both reader dispositions are present, and `measure_test_evidence.py --check` finds 0 unexplained readers. The module matrix is current, `ci_events` passes `--check` and `--selftest`, and each side's own suite passes on the candidate.

[R475] PASS Docs - `docs/testing/TESTING.md:200-202,514,522,528-530`; `tb/verilator/milan_dp/README.md:214-233,258-275` (PR) and `:492,998` (dev); receipts/09 - checked that both sides' rows and paragraphs survive in table order. The added-line em-dash gate is clean against both parents, the TOC check and anchors pass, and `docs_check`, doc-style, feature-status and solution-docs pass. No newly stale line citation exists. No PR text quotes an area or timing figure that #686's re-record changed.

## Findings

No new finding at this head.

## Prior public findings

Each prior finding on PR #672 was checked against this candidate. Every PR-side artifact named below is byte-identical to the PR head `85db3534`, except where a locator moved by dev's +1 datapath line.

| ID | Severity; lenses | Disposition at `17c39e57` |
|---|---|---|
| R475-1-F1, R474-1-F1, R474-1-F2 | MAJOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED, unchanged by the composition. Settle recentre RTL and capture crossbar are byte-identical to the resolved source. The follow_ring legs, the 12 controls and the physical wire checks pass here. |
| R474-1-F3 / R475-1-F3 | BLOCKER / MINOR; Conformance, Tests, Docs | RESOLVED. `gen_module_matrix.py --check` is up to date on the candidate. |
| R475-1-F2 / R474-1-F4 | MINOR; Docs | RESOLVED. `MEDIA_CLOCK_FOLLOWING.md` is identical to the PR head. |
| R474-2-F1 (from R474-1-S1) | MINOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED. `KL_chan_map_capture.sv` is the PR blob, and HELD-DUP and STARVED-HELD-DUP are caught here. |
| R474-2-R1, R474-2-R2, R475-2-R1, R474-3-R1, R474-3-R2 | RESIDUE; Docs | RESOLVED, unchanged. `TESTING.md:514` lists the twelve controls. |
| R475-2-R2 | RESIDUE; Docs | RETAINED, see below. |
| R474-2-S1, R474-2-S2, R474-2-S3 / R474-1-S2 | SUGGESTION; Tests (S2 also Docs) | RETAINED, see below. |

### Retained items for the manager's checklist

- **R475-2-R2; RESIDUE; Docs.**
  - **Artifact:** `docs/design/MEDIA_CLOCK_FOLLOWING.md:1085-1086`, against `hdl/milan/milan_datapath.sv:6534-6565` at this candidate (6533 at the PR head).
  - **Evidence:** the parenthetical naming the preserved #386 recentre says `g_settle_recentre`. That block is `g_src_recentre`; `g_settle_recentre` is #645's new block at `:6615-6653`.
  - **Impact:** a wrong navigation label only.
  - **Exact fix:** replace that parenthetical's `g_settle_recentre` with `g_src_recentre`.
- **R474-2-S1; SUGGESTION; Tests.** The quiet-band floor is not pinned to the shipped constant. Artifacts: `tb/verilator/follow_ring/settle_control.py` and `quiet_distributions.py` (unchanged), and the band comment at `hdl/milan/milan_datapath.sv:6587` (6586 at the PR head).
- **R474-2-S2; SUGGESTION; Tests, Docs.** There is no standing shipping-clock quiet or latency evidence. `MEDIA_CLOCK_FOLLOWING.md` and `tb/verilator/follow_ring/Makefile` are unchanged.
- **R474-2-S3 / R474-1-S2; SUGGESTION; Tests.** The physical leg can pass with zero decisions. `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:1101` is unchanged. This run made two decisions.

## Ledger (reviewer-owned)

All five lenses are touched by the composition: the five both-sides paths span RTL, tests and documentation. Each lens was therefore applied directly at the candidate rather than delegated.

For the 33 PR-only paths, whose candidate blobs equal the PR head, the source coverage remains:

- R475-4 POSITIVE at `85db353400c6bf3965d279a9f5b5d47e08a0d1ed` (issue comment 6060183780), all five lenses CLEAN;
- R474-3 POSITIVE (6041843633) and R475-3 POSITIVE (6041707628) at the ancestor `2525eae9567865a8bc741901914bdf5a1caf2c26`.

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_datapath.sv:6566-6667`, `KL_maap.sv` (dev blob), follow_ring / render / physical gPTP / crflic runs, issue #645 rulings | R475-5 | 17c39e57f450c3e99d073b7589172a2af9c2f8e7 |
| RTL | CLEAN | `milan_datapath.sv:264-284` vs PR hunks, KL_maap ports, five composed elaborations, lint ratchet, glue identity | R475-5 | 17c39e57f450c3e99d073b7589172a2af9c2f8e7 |
| Robustness | CLEAN | follow_ring 12/12 controls, render leg defects 5/5, gate-1b mutant table, SoC option controls, capture 785+20 | R475-5 | 17c39e57f450c3e99d073b7589172a2af9c2f8e7 |
| Tests | CLEAN | `test_builder.py`, `measure_test_evidence_readers.py`, `TESTING.md` rows, evidence ratchet, module matrix, ci_events, both sides' suites | R475-5 | 17c39e57f450c3e99d073b7589172a2af9c2f8e7 |
| Docs | CLEAN | `TESTING.md`, `milan_dp/README.md`, em-dash vs both parents, TOC and anchors, docs_check, citation shift, AREA_BUDGET rules | R475-5 | 17c39e57f450c3e99d073b7589172a2af9c2f8e7 |

Open in any lens: none.

## Real limits

- **No vendor-tool run.** No route, standalone synthesis, timing sweep or IOB check was run on the candidate. Every resource and timing statement above is arithmetic on published figures.
- **The candidate has no hosted evidence.** `17c39e57` is not on the hosted repository; the commits endpoint returns 422. At the PR head, `rtl-fast`, `docs-check`, `docs-check-no-git`, `elaborate`, `wire-accountability`, `yosys-elaboration` and Yosys shards 0-3 had succeeded. Verilator shards 0, 1, 2 and 4 were still in progress and physical gPTP was skipped at query time (receipts/03). The manager owns hosted and act acceptance.
- **Not rerun on the candidate.**
  - The physical leg's harness controls, `verify_abort.py` and `verify_recentres.py`. Each re-runs the full physical simulation, and the job was stopped after the main leg.
  - The arrival campaign (128) and pull-in campaign (32).
  - `tdm8render-pullin`, `tdm8render-law-boundary` and `tdm8render-mutants`.
  - The full builder, native, firmware, behave and Yosys banks.
- **Limited exercise of the dev-side additions.** The lwSRP submodule is not initialised in this clone, and F4's firmware suites were not run. The PR touches no firmware, CSR or SoC source.
- **No hardware proof.** Physical calibration was NOT RUN. Field skips and simulated physical-model checks are not hardware proof. Issue #645's bench-repeat acceptance criterion remains open.
- **Shared host.** The host was shared with other heavy jobs throughout. That affects wall time only.

## Pending manager duties

1. **Resource and timing measurement on this merge result.** Run the merge-bank resource measurement and `check` (route-1x1 and ooc-1x1, `AREA_BUDGET.md:244-251`), and record this merge's re-baseline per `AREA_BUDGET.md:194-195`. The record now in the tree names #686's inputs (`e519e31f`). It covers neither #693's nor #645's RTL. The route WNS floor is the binding risk: +0.057 ns measured at the PR head, 0.027 ns of margin.
2. **Shipping timing sweep.** Decide whether the `BUILDING.md` section 5 sweep (best of three directives at least +0.030 ns setup, 0 hold, full IOB check) is rerun on the merge result. The round-2e source sweep did not include #686's KL_maap change.
3. **Merge-turn banks.** Run the current-dev candidate builder and native banks, and link their receipts on the PR.
4. **Hosted contexts.** Confirm exact-head hosted contexts for the merge candidate (`rtl-fast`, `verilator-suites`, `yosys-portability`).
5. **R474-4 at `85db3534`.** It was started (6059457382) but had published no verdict when this report was written. Under AGENTS.md section 7, no review round may remain in flight at merge.
6. **Residue checklist.** Carry R475-2-R2 to the residue checklist, and keep the three SUGGESTIONs.
7. **Post-merge containment.** After merge, run `check_merge_containment.py` and `check_merge_review_integrity.py`.
8. **Bench repeat.** Issue #645's bench repeat remains outstanding.

## Receipts

`MANIFEST.sha256` lists every published receipt and script. Host paths were replaced by placeholders, as described in `receipts/00_path_substitutions.txt`.

- `receipts/01_merge_identity.txt` - parents, merge base, merge-tree reproduction, path partition.
- `receipts/02_overlap_side_retention.txt` - per-path side retention and patch-ids.
- `receipts/03_hosted_status.txt` - hosted lookups.
- `receipts/04_dp_glue_identity.txt` - follow_ring glue extraction, PR head vs candidate.
- `receipts/05_rtl_composition.txt` - RTL delta classification and blob identities.
- `receipts/06_resource_arithmetic.txt` - the gate's `judge()` on published figures and on the linear estimate.
- `receipts/07_render_vs_source.txt` and `receipts/10_physical_gptp_vs_source.txt` - output identity against the source runs.
- `receipts/08_static_gates_summary.txt` - 43 gates.
- `receipts/09_citation_shift.txt` - line-citation movement.
- `receipts/11_clone_integrity.txt` - exact-head bytes, modes, index and gitlinks after the round.
- `receipts/runs/` - each job's `.cmd`, `.log` and `.rc`.
- `scripts/` - `run_job.sh`, `static_gates.sh`, `static_gates.txt`, `md_gates.txt`, `builder_focus.py`, `resource_arith.py` and `cite_shift.py`.

R475-5 FINISHED
