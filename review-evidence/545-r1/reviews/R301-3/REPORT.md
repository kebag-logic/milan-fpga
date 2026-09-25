[R301] NEGATIVE - exact head b376f6113b388929fe82e883d400e5361319b966

Round R301-3. I am the external reviewer, with a cleared context. This is the merge-dev delta review of PR #563 / issue #545.

- Head: `b376f6113b388929fe82e883d400e5361319b966`, tree `659205c787ef36b51185790d0579dfbcd6705682`.
- Parents: lane `92ad1687d84ff077f872719b4f1df601f82064d2` and dev `864b36f5e9450ef64f75ca3f0d68c44330e447d7`. The merge base is `5b73d3f47dfed519eb988c13d6beb1db664ef1e0`.
- Delta judged: `b94f53cc..b376f611`. That is the round-3 content (`b94f53cc..92ad1687`) plus the merge resolutions.

**Summary.** The merge itself is clean:

- Hand resolutions are confined to the six assigned files.
- Every other path is exactly one parent's blob or the automatic merge.
- The regenerated diagram set reproduces byte for byte.
- The ROM ledger matches the merged pin pair.
- No product behaviour changes beyond the union of the two parents.
- Every requested suite, campaign and documentation gate passes at this head.

The round-3 content holds up. The re-armed U15 kills both counting variants and a further re-base variant that I planted myself.

One new MINOR remains open under Docs. It is a present-tense control count in the `milan_dp` suite README that the lane made false. It predates the merge, and my own R301-2 Docs pass missed it. The Docs lens is therefore unclean and the verdict is NEGATIVE.

## Findings

### F1 MINOR - Docs - `tb/verilator/milan_dp/README.md:590-592` - the suite README says `make gmstep-mutants` runs "all eleven" controls; the target runs fourteen

- **Authority:** AGENTS.md section 6, Docs lens: changed contracts are reflected in the docs, and no stale statements remain. The executable inventory is authoritative.
- **Evidence at this head:**
  - `README.md:576-588` tabulates eleven controls. Then `:590-592` reads: "Each control costs one elaboration of the datapath, so the sweep carries the three the acceptance names and the explicit `make gmstep-mutants` target runs all eleven".
  - `tb/verilator/milan_dp/gmstep_mutants.py` has 14 `Control(...)` entries: the eleven #387 controls plus the three #545 "policy level" controls. `main()` selects all of them under `--all`.
  - `docs/testing/TESTING.md:268` says "twelve gmstep controls and two option-off controls" (14), and so does the campaign I ran here: 16 checks = 14 controls + 2 positive legs (`receipts/milan_dp_gmstep_mutants_all.log`).
  - The lane's own addendum at `README.md:989-996` says the three slew controls "also belong to `make gmstep-mutants`". The page therefore contradicts itself.
  - The lane introduced the drift at `fc8a719f`, when it added the three controls without touching this sentence. The count "all eleven" is unchanged at `5b73d3f4`, `b94f53cc`, `92ad1687` and `864b36f5`. The merge carried it forward unchanged.
  - The dated measurement lines `:615` and `:859` ("2026-09-24 ... all eleven") are historical records and are not the finding.
- **Impact:** a later reviewer or executor reading the suite page is told the explicit campaign is the eleven tabulated #387 controls. That under-states what the target proves and what it costs to run. It is the same class of inventory drift that R300-1 F3 required fixing in TESTING.md. The authoritative TESTING.md row and the executable inventory are correct, so nothing in the product or the gates is affected.
- **Required outcome:** the README's present-tense statement of what `make gmstep-mutants` runs matches the executable inventory: fourteen controls, the three #545 controls included. For example, add the three rows to the table or state the total. Dated historical measurements may stay as dated records.
- **Verification:** count the `Control(` entries in `gmstep_mutants.py` against the README statement and TESTING.md:268, then rerun the doc gates (`docs_check.py` both modes, `gen_toc.py --check`, `check_em_dash.py --base <dev>`).

### S1 SUGGESTION - Docs - `scripts/measure_test_evidence.py:597-601` - the `slew_mutants.py` disposition names six defect classes for eight defects

I observed this independently. It is the same point as R300-3 S2 and is retained under that ID; see the prior-findings table below. It is non-blocking.

## What was examined and run

Every command ran in the foreground on this head, with Verilator 5.050, the CI pin, from the scoped wrapper (`verilator --version`: `Verilator 5.050 2026-07-01 rev v5.050`). Each receipt records the head, the tool identity, the command, the full output, the exit code and the wall clock.

| Check | Result | Receipt |
|---|---|---|
| Merge provenance vs both parents and base | 25 lane-only, 21 dev-only and 13 both-changed paths; 0 injected, 0 unexpected | `receipts/merge_provenance.log` |
| `git show --remerge-diff b376f611` | Hand resolutions only in CHANGELOG.md, PNG_MANIFEST.json, submodule_boundaries.drawio/.png, SUBMODULES.md, TESTING.md | reviewed; summary below |
| Lane patch identity across the merge, for auto-merged both-changed files | Preserved for `milan_datapath.sv`, `rom_digests.tsv`, REGISTER_MAP, CI_WORKFLOWS, `milan_dp/README.md`, the SVG. `measure_test_evidence.py` has identical added content with shifted context | `receipts/lane_patch_ids.txt` |
| Gitlinks at head | gptp-processor `5dce647a…`, protocol-processor `990f9652…`, verilog-axis `48ff7a7e…`, external `efeb541a…` | `receipts/final_state.log` |
| ROM digests regenerated with the ooc.sh generators at the merged pins | `ltn_rom.hex` and `ucode.hex` @990f9652, `gptp_ucode.hex` @5dce647a: all MATCH the ledger. Ledger rows are in `LC_ALL=C` order, which is the recorder's output order | `receipts/rom_digests.log` |
| Submodule diagram regenerated from scratch (write mode, sources deleted first) in a disposable clone | drawio, SVG, PNG, PNG_MANIFEST.json all byte-identical to HEAD blobs | `receipts/diagram_regen.log` |
| `submodule_boundaries.gen.py --check` / `--selftest`; `check_diagram_pngs.py`; `check_submodule_docs.py` | rc 0 / 0 / 0 / 0 | `receipts/submodule_diagram_check.log`, `submodule_diagram_selftest.log`, `check_diagram_pngs.log`, `check_submodule_docs.log` |
| `mmcm_servo` default target, in its four recipe stages (`receipts/mmcm_servo_default_recipe.txt`) | unit 100/0, rails 8/0, step 113/0, slew 90/0; 35.5 + 26.3 + 343.8 + 343.8 s | `receipts/mmcm_servo_{1_unit,2_rails,3_step,4_slew}.log` |
| `slew-mutants` (the campaign's own tables and `run_case`, in parallel) | 10/10: both clean controls pass, and all 8 defects fail their named checks. The 3 U15 streak variants fail `[U15] four fresh guard trips precede re-base` | `receipts/mmcm_servo_slew_mutants.log` |
| Reviewer probe: slew discard also re-bases the window (`win_valid_r <= 0`) | KILLED: U15 fails, and S2/S4 fail in the slew suite | `receipts/probe_slew_rebase.log` |
| `milan_dp` gmstep leg (`make gmstep`) | 58/0, RESULT: PASS | `receipts/milan_dp_gmstep.log` |
| `gmstep-mutants` (the campaign's own `CONTROLS` and `run_control`, in parallel) | 16/16: 2 positive legs + 14 controls, each caught on its named check | `receipts/milan_dp_gmstep_mutants_all.log` |
| `docs_check.py` with Git / with no Git (extracted tree) | 0 findings / 0 findings (only inventory parity skipped); `check_feature_status` 0 | `receipts/docs_check_git.log`, `docs_check_git_venv.log`, `docs_check_nogit.log` |
| `gen_toc.py --verify-anchors` / `--check` (pinned renderer, private venv) | 174 anchors reproduced / TOC OK | `receipts/gen_toc_verify_anchors.log`, `gen_toc_check.log` |
| `check_em_dash.py --base 864b36f5…` | 0 findings over 154 added lines, arms 339/339 | `receipts/check_em_dash_base.log` |
| `check_doc_style`, `check_doc_paths`, `measure_test_evidence --check`, `git diff --check 864b36f5..b376f611` | all rc 0 | `receipts/check_doc_style.log`, `check_doc_paths.log`, `measure_test_evidence.log`, `diff_check.log` |
| Hosted `mmcm_servo` basis (CI_WORKFLOWS.md:159) | b94f53cc sample: job 108001867446 = 1159.06 s, which matches the documented 1159.1 s / 640.9 s / 35.6%. Exact head: job 108072309878 (merge 318515b of this head) = 1065.29 s of 1800 s | `receipts/hosted_mmcm_servo_windows.txt`, `hosted_job_*_excerpt.log`, `hosted_job_108001867446.json` |
| Clone restored | head, tree and index tree exact; no diff; `status --ignored` empty; submodules at their gitlinks and clean | `receipts/final_state.log` |

Four compile receipts contained host tool-install include paths: `mmcm_servo_1_unit`, `_2_rails`, `_3_step` and `milan_dp_gmstep`. Those paths are redacted to `<TOOL_ROOT>`. `scripts/run_step.sh` takes the pinned tool directory from `TOOLBIN`. No other receipt bytes were edited.

The first attempts at `gen_toc` and `check_em_dash` ran without the pinned renderer installed and exited 2 ("cannot read Markdown"). Their receipts were overwritten by the successful reruns, which used a private venv built from `tools/markdown/requirements.txt`. The system-Python `docs_check_git.log` run needs no renderer.

A note on the two campaigns. Run serially, they exceed the session's foreground limit. The parallel drivers, `scripts/slew_mutants_parallel.py` and `scripts/gmstep_mutants_parallel.py`, import the scripts' own mutant tables and their verdict functions unchanged. Only the scheduling differs: clean controls first, then at most 8 concurrent arms. The `make slew-mutants` and `make gmstep-mutants` targets themselves were not invoked serially.

### Merge-resolution review (remerge-diff)

- **CHANGELOG.md:** both Contents bullets and both sections are kept. The #545 section is first, then #508, separated by a blank line. `gen_toc --check` and `--verify-anchors` pass.
- **SUBMODULES.md:** the pin table carries gPTP `5dce647a…` (from the lane) and processor `990f9652…` (from dev). The lane's `5dce647a` guide links and its slew paragraph come through the automatic merge. No `e5dcea6e` or `09f9bf38` remains outside dated history.
- **TESTING.md:** dev's #508 `gsi-mutants` row, the lane's updated `gmstep-mutants` row (fourteen controls, with the round-3 triggers) and the `slew-mutants` row are all present. Dev's superseded "nine controls" row is correctly dropped.
- **Diagram set:** the drawio carries `pin 990f96526bb8` and `pin 5dce647ab5a0`. The PNG, the SVG (automatically merged as text) and the manifest all regenerate identically. So the resolution is the generator's output, not a hand merge.
- **Auto-merged `milan_datapath.sv`:** the lane's slew hunks (`:1455-1462`, `slew_rate_alignment`, the servo `.phc_slew_active_i`, the plane `.phc_slew_active_o`, the absent-engine tie-off) and dev's GET_STREAM_INFO hunks are disjoint. Neither reads the other's nets.

### Round-3 content (`b94f53cc..92ad1687`)

- **U15 (`sim_main.cpp:555-581`)** is now armed with one guard trip. Its three states:
  - Correct RTL: the streak goes 1 → 0 at the slew discard, and four fresh trips follow at gaps of 32, 32, 32 and 33.
  - Streak reset removed: the streak stays at 1, so the third fresh trip re-bases.
  - The increment or guard-trip variants: the streak goes 1 → 3, so the first fresh trip re-bases.

  Each violates the graded gap pattern, and all three were killed here. I planted a fourth variant, a direct re-base on each slew discard. U15 and slew-suite S2/S4 kill it.
- **Budget basis.** The `CI_WORKFLOWS.md` `mmcm_servo` row arithmetic is correct: 1800 − 1159.1 = 640.9, which is 35.6%. The run and job links resolve to a successful shard at `b94f53cc`. The window matches the job log to 0.1 s. The Makefile header labels its 952.797 s as the round-2 local figure and points to the hosted basis.
- **Triggers.** The `gmstep-mutants` trigger list now names `KL_gptp_shadow.sv` (`phc_adj_o` and the slew pass-through) and the `gptp-processor` pin.
- **Counts.** TESTING.md's "eight defects and two positive controls" matches `slew_mutants.py` (5 + 3 defects).
- **No RTL change** in round 3: `git diff b94f53cc..92ad1687 -- hdl` is empty.

## Prior public findings on PR #563, resolved or retained at this head

I read these only after my own pass and a draft verdict and ledger were written.

| ID | Severity | Status at `b376f611` | Evidence at this head |
|---|---|---|---|
| R300-1 F1 / R301-1 F1 (default servo target overruns budget) | MAJOR | Resolved | Mutants are behind `slew-mutants`. The default target keeps 100/8/113/90. Exact-head hosted window is 1065.3 s of 1800 s (job 108072309878) |
| R300-1 F2 / R301-1 F2 (coincident step+slew dedupe untested) | MINOR | Resolved | `[S5] coincident step+slew window counted once` passes. `step_dedupe_removed` is killed on it |
| R300-1 F3 (TESTING index/campaign stale) | MINOR | Resolved | TESTING.md:267-269,485 match the executable inventories. The README sentence in F1 above is a separate artifact that it did not cover |
| R301-1 F3 / R300-1 S1 (connected tail oracle copied the RTL) | MINOR / SUGGESTION | Resolved | The gmstep leg grades against the measured PHC advance. `the policy level misses an extra addend stage` is caught |
| R301-1 S1 (slew streak reset uncontracted) | SUGGESTION | Resolved | Stated in the servo header and TIME_SYNC. Pinned by U15 and three controls |
| R300-2 F4 (U15 blind to counting variants) | MINOR | Resolved | Both counting variants and the removal are killed by U15 (`receipts/mmcm_servo_slew_mutants.log`) |
| R300-2 F5 (1800 s basis contradicted hosted) | MINOR | Resolved | The `mmcm_servo` row (CI_WORKFLOWS.md:159) has its hosted basis, checked against the job log |
| R301-2 S-A (tail oracle one-sided) | SUGGESTION | Retained, open | `sim_gmstep.cpp` is unchanged since `b94f53cc`. The manager routed it to #495. It is the conservative direction |
| R301-2 S-B (record the hosted window) | SUGGESTION | Resolved | CI_WORKFLOWS row and Makefile pointer |
| R301-2 S-C (shadow latch and pin as gmstep triggers) | SUGGESTION | Resolved | TESTING.md:268 |
| R300-3 S1 (U15 blind to a level-gated streak reset on sub-window slews) | SUGGESTION | Retained, open | `sim_main.cpp` and the servo RTL are unchanged by the merge. I did not re-derive the survivor |
| R300-3 S2 (disposition lists six classes for eight defects) | SUGGESTION | Retained, open | `measure_test_evidence.py:597-601` is unchanged. This is S1 above |

**Self-correction.** My R301-2 round banked Docs clean at `b94f53cc`, citing `milan_dp/README.md:895-899`. The "all eleven" sentence (F1) was already present there and I did not catch it. That R301-2 Docs coverage is superseded by this round.

## Lens results

```text
[R301] PASS Conformance - issue #545 acceptance 1-3; assignments 5830332403 items 1-3 and 5831902801 items 1-3; SUBMODULES.md:24-25; syn/yosys/rom_digests.tsv:20,30-31 vs receipts/rom_digests.log; receipts/merge_provenance.log; remerge-diff of b376f611 - merge keeps gPTP 5dce647a and processor 990f9652, both stated; ROM ledger reproduced; no content outside the union of both parents; exact-head hosted shards green so far (receipts/hosted_checkruns_b376f611_final.txt)
[R301] PASS RTL - hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:470-500,589-620,650-721 (unchanged since b94f53cc); hdl/milan/milan_datapath.sv lane hunks (:1455-1462, slew_rate_alignment, servo/plane ports, tie-off) vs dev GET_STREAM_INFO hunks at b376f611 - disjoint and non-interacting; empty hdl diff in round 3; the only gitlink change from dev is the processor's
[R301] PASS Robustness - sim_main.cpp:555-581 (U15 one-trip arming); receipts/probe_slew_rebase.log (unplanned re-base variant killed); receipts/mmcm_servo_4_slew.log (short, shared-boundary, prolonged, reset, saturation and coincident-step cases, 90/0) at b376f611
[R301] PASS Tests - slew_mutants.py 10/10 (receipts/mmcm_servo_slew_mutants.log); gmstep_mutants.py 16/16 (receipts/milan_dp_gmstep_mutants_all.log); gmstep leg 58/0; servo default 100/8/113/90 at b376f611; every control fails its named check
[R301] MINOR Docs - tb/verilator/milan_dp/README.md:590-592 - F1; everything else under Docs checked clean: CHANGELOG, SUBMODULES and TESTING resolutions; CI_WORKFLOWS row vs job logs; diagram set regenerated byte-identical; docs_check in both modes; gen_toc --check and --verify-anchors; em-dash vs dev base; doc style and paths
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #545 acceptance and the three assignment/decision comments; the pin pair in the gitlinks, SUBMODULES and the diagram; the ROM ledger regenerated; merge provenance; remerge-diff | R301-3 | `b376f6113b388929fe82e883d400e5361319b966` |
| RTL | CLEAN | servo slew, streak and tally logic; datapath slew wiring vs the auto-merged dev GET_STREAM_INFO hunks; round-3 hdl diff empty | R301-3 | `b376f6113b388929fe82e883d400e5361319b966` |
| Robustness | CLEAN (retained R300-3 S1 and R301-2 S-A suggestions only) | U15 arming; slew-suite boundary, reset, saturation and prolonged cases; reviewer re-base probe | R301-3 | `b376f6113b388929fe82e883d400e5361319b966` |
| Tests | CLEAN (suggestions only) | servo default, 4 stages; slew campaign 10/10; gmstep leg 58/0; gmstep campaign 16/16; reviewer probe | R301-3 | `b376f6113b388929fe82e883d400e5361319b966` |
| Docs | UNCLEAN (F1 MINOR open; S1 = R300-3 S2 suggestion) | CHANGELOG, SUBMODULES, TESTING, CI_WORKFLOWS, milan_dp README, servo Makefile header, measure_test_evidence dispositions, diagram set and manifest, all doc gates in both modes | R301-3 | `b376f6113b388929fe82e883d400e5361319b966` |

The Docs lens clears when a round at a head that fixes F1 re-applies Docs. A README-only fix touches no other lens's scope. Under AGENTS.md section 7, a documentation-only commit therefore leaves this round's Conformance, RTL, Robustness and Tests coverage standing, provided nothing else in their scope changes.

## Limits

- **Campaigns run through parallel drivers.** The serial make targets `slew-mutants` and `gmstep-mutants` were not invoked. Their tables and verdict logic ran unchanged through the parallel drivers, and the `gmstep` prerequisite was run first.
- **Servo default run in stages.** The `mmcm_servo` default ran as its four recipe stages, one per foreground step, on an unconstrained host. It was not timed on two CPUs.
- **Not run by me.** The full `milan_dp` sweep, `crf_rx`, `gptp_shadow`, the builder, behave, the static HDL, C++ and Python gates, the area/OOC recipe, and all parent, processor, gPTP and Yosys banks. Those are outside this delta's assignment or disallowed. I relied on the manager's and the executor's public receipts for them, and did not re-verify them.
- **Hosted state.** Hosted exact-head checks were read, not accepted. At 2026-09-25T13:12Z, 18 contexts were success. Verilator shard 4/5 was in progress. The nightly physical gPTP job was skipped, which is not hardware evidence. The `verilator-suites` and `yosys-portability` aggregates were not yet present in the check-run list.
- **No hardware.** No physical calibration and no bench run. Builder gate 11's board-report calibration arm is NOT RUN, as the executor also states.

## Pending manager duties

- Route F1 to a fix at a new head, then re-review Docs at that head.
- Accept the hosted/act evidence at the final head, including `verilator-suites`, `yosys-portability` and the in-progress shard 4/5.
- Build and validate the current-dev candidate merge (source base `864b36f5`) at the merge turn.
- Post-merge containment.
- Keep the retained suggestions (R301-2 S-A → #495; R300-3 S1 and S2) tracked as the manager decides.

R301-3 FINISHED
