# #464 author handoff: A167

Written 2026-09-22 by [A167], the isolated implementation author. The companion files are PR-BODY.md (the proposed PR description) and REVIEW-READY.md (the text posted publicly as [A167] REVIEW READY). `receipts/` holds every transcript and the scripts that reproduce them; see `receipts/README.md`.

## Identity

| Item | Value |
|---|---|
| Issue | kebag-logic/milan-fpga#464, "[Tooling] avdecc/gen_aem_store.py --self-test exits 1 on dev and no workflow runs it"; Project status `In progress` (set by the manager) |
| Roles | executor A167; reviewers R235 (internal, cleared-context Opus) and R236 (external, cleared-context Codex); manager A10 |
| Checkout / branch | `$CANDIDATE`, `464-aem-store-selftest` (linked to #464 by `gh issue develop`; upstream `origin/464-aem-store-selftest` is still at the base) |
| Base | `ec34fcdee0ca9ffa63564a9af8ad70a3a618de29`, tree `2ec2d2e9931d250dacb945643cf3a444ec0e9a91`; live `origin/dev` at the start and again at 13:07 CEST |
| Head | `1576f0893ae9781074fffb105f5384fe774ff11e`, tree `b16ce21a92e8c80f209486d8a5d848f6e47359aa`; directly descends from the base, so the head tree is the candidate merge tree while `dev` stays at `ec34fcde` |
| Commit 1 | `4fc5a19db751a2d6c136d7300f5de5876435a002` (tree `a243c82831f5dea8c7aac05c33d0fa8f30393d13`): "Repair the AEM store self-test for the one-map model: its own two-map fixture, cause-checked refusals, deviations exact at AUDIO_MAP[0]" |
| Commit 2 | `1576f0893ae9781074fffb105f5384fe774ff11e`: "Run the AEM store self-test as a docs-check step and pin it: canonical record, step-count arms, policy and running-tests pages" |
| Commit form | one line each, no body, no trailers; author `hackerman-kl` |
| Lane state | tracked and index clean, 0 hidden index flags, no untracked or ignored files. Nothing pushed, no PR opened |
| Public record | TAKEN: https://github.com/kebag-logic/milan-fpga/issues/464#issuecomment-5775075742 ; REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/464#issuecomment-5775408351 |

## Changed files, base to head

| File | Mode | Base blob | Head blob | +/- |
|---|---|---|---|---|
| `.github/workflows/docs.yml` | 100644 | `f5a45401` | `6495a125` | +9/-0 |
| `avdecc/aem_maps.py` | 100644 | `ca7b4733` | `25636b2d` | +6/-1 |
| `avdecc/gen_aem_store.py` | 100644 | `eaa4265b` | `aa884381` | +112/-33 |
| `docs/testing/CI_WORKFLOWS.md` | 100644 | `89c221da` | `2823156c` | +10/-0 |
| `docs/testing/RUNNING_TESTS.md` | 100644 | `2d623c5c` | `38a276cc` | +1/-0 |
| `scripts/ci_events.py` | 100755 | `b90ae46b` | `b6cc7689` | +9/-5 |

No mode changes, renames, submodule or gitlink changes. All added lines are ASCII.

## Causes (acceptance 1)

Each cause was measured at the base (`receipts/baseline_original_arms.txt`, `history_da71309c.txt` and `interpreter_matrix.txt`):

1. First failure: `_selftest_map_bounds`' `global_index` assigns `audio_maps[1]` and raises IndexError. da71309c (2026-08-17) made the builtin Stream Port Input dynamic (Milan v1.2 5.3.3.9) and renumbered the one remaining static map to AUDIO_MAP[0]. The self-test passes at the parent b7d0bbcd and fails at da71309c.
2. Same cause, further arms: the OUTPUT duplicate refusal and the OUTPUT cluster_offset accept also raise IndexError. The INPUT duplicate vector is refused by the OUTPUT rule, and the CRF-sink vector by the stream_index bound, so neither refusal was exercised. `KNOWN_MAP_DEVIATIONS` names AUDIO_MAP[1], while the deployed model carries the same six deviations at AUDIO_MAP[0].
3. Python 3.12, the hosted docs-check interpreter, fails earlier still with `NameError: Callable`: an annotation without its import since 25f543b9. Python 3.14's deferred annotations hide it.

None of these is a generator behaviour defect. The two-level directory and Base-format sections passed for their own causes at the base and are unchanged.

## What changed

- `_map_fixture()`: builtin_spec() with the map-bounding geometry declared explicitly. STREAM_INPUT 0 is AAF (FORMATS) and STREAM_INPUT 1 is the CRF sink; STREAM_OUTPUT 0 is 2-channel AAF. AUDIO_MAP[0] serves static STREAM_PORT_INPUT[0] (8 clusters from 0), and AUDIO_MAP[1] serves static STREAM_PORT_OUTPUT[0] (8 clusters from 8). Default cluster names are used. Each call returns fresh objects.
- `_selftest_map_bounds()`: two positive controls, the deployed `builtin_spec()` and the fixture. The 9 refusal vectors each mutate a fresh fixture and must raise ValueError carrying that bound's refusal text; a refusal carrying other text is a FAIL. The accept vector is unchanged in meaning. The 62-mapping vector is now `[[0, c, c % 8, 0] for c in range(63)]` on the output map, so Table 7-32 is the only refusing bound it breaks. The function is 95 lines, under the Rule 12 limit of 100.
- `_selftest_map_deviations()`: the deployed model's deviation arm is split out and now checks both directions (no new deviation, and no recorded deviation the model does not carry). The empty-allowlist arm is kept.
- Also in `avdecc/gen_aem_store.py`: `from collections.abc import Callable` (the sibling modules' idiom); the docstring's model counts are corrected (CLOCK_SOURCE x2 since #389, AUDIO_MAP x1 since da71309c); and a note records that docs-check runs the self-test.
- `avdecc/aem_maps.py`: the `KNOWN_MAP_DEVIATIONS` string moves from `AUDIO_MAP[1]` to `AUDIO_MAP[0]`, with a comment giving da71309c as the reason. The set keeps the same 6 members, mappings, stream and format. The self-test is its only reader, and no emitter reads SMAP DEVIATIONS.
- The docs-check step 41 is `AEM store generator self-test`, running `python3 avdecc/gen_aem_store.py --self-test`. It sits after `Per-page contents gate` and before the three shape gates, so the #407 swap and rename arms at steps 38/39 keep their indices.
- `scripts/ci_events.py`: the step's `CARRIER_STEP_LISTS` entry, plus five fragments in `_carrier_step_list_arms` changed from 43 to 44 steps (found 42 to found 43). This is the same commit as the workflow edit, as CI_WORKFLOWS.md item 11 requires.
- Docs: CI_WORKFLOWS.md gets a paragraph after the shape-gate paragraph (short sentences, no em dash); RUNNING_TESTS.md section 1 gets the local command.
- Arm census: the base self-test defines 19 arms but crashes after the first. The head defines and passes 20: the same 19 plus the fixture-acceptance control. No arm removed, no allowlist widened, no validator weakened.

## Commands and results

Unless stated otherwise, each ran in the lane at the committed head with Python 3.14.7.

| Command | Result |
|---|---|
| `python3 -B avdecc/gen_aem_store.py --self-test` | exit 0, PASS, 20 ok / 0 FAIL; identical transcript on Python 3.12.13 |
| same at base `ec34fcde` | exit 1: IndexError (3.14), NameError `Callable` (3.12) |
| `receipts/mutate_selftest.py <checkout> 1576f089 [py]` | 28/28 met on 3.14 and on 3.12 |
| `receipts/gen_outputs.sh` base and head, then `cmp` of the manifests | identical: 83 files |
| `python3 -B scripts/ci_events.py --check` | OK, 1513 items (base 1505) |
| `python3 -B scripts/ci_events.py --selftest` | PASS, 1150 arms (base 1144); vacuity stub fails all 1051 (base 1046) |
| `docs_check.py`; `check_doc_paths.py`; `gen_toc.py --check`, `--verify-anchors`, `--selftest` | pass (0 findings; 824 paths; 105 pages; 144 anchors; 279/279) |
| `check_em_dash.py --base ec34fcde`; `--selftest` | 0 findings over 11 added lines in 2 pages; 34/34 |
| `check_feature_status.py` (+`--self-test`); `check_doc_style.py` (+`--selftest`); `check_archive.py` | pass |
| `check_py_idiom.py` (+`--selftest`); `check_sh_idiom.py`; `check_hygiene.py --check` (+`--selftest`) | pass, every ratchet unchanged (long function 9 <= 9) |
| `check_todo_ownership.py`; `measure_fail_fast.py --check`; `measure_test_evidence.py --check` | pass at the head (`gates_ratchets_head.txt`); their "can be lowered" notes are pre-existing slack, and no finding involves `avdecc/` |
| `gen_module_matrix.py --check`; `check_baremetal_only.py --check`; `check_solution_docs.py`; `check_submodule_docs.py`; `check_gptp_docs.py` | pass |
| `python3 -B sw/builder/test_builder.py` | exit 0, ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 calibration: needs a local Vivado placement report); AEM gates 3, 10 and 16 pass; 7m12s |
| `check_entity_shape.py --self-test` | 136 checks, 0 failures |
| `check_sweep_shape.py --self-test`; `check_deploy_shape.py --self-test`; `check_wire_accountability.py --self-test`; `check_nvm_record_space.py` (+`--self-test`) | pass |
| `python3 -B scripts/lint_rtl.py --check` | PASS, 90 <= ratchet 90 (Verilator 5.052) |
| `python3 -B scripts/xvlog_gate.py --check` | PASS, 4 findings == ratchet (all in the pinned protocol-processor, 0 in `hdl/`); analysed 72 `hdl/` and 48 processor files with a local Vivado 2026.1 xvlog |
| `git diff --check ec34fcde HEAD` | clean |

Compilation caps: `MAKEFLAGS=-j8` was set for the builder run. No Verilator or Yosys suite was compiled.

## Acceptance mapping

| #464 acceptance | Status | Evidence |
|---|---|---|
| 1. Failing assertion named with its cause | met | TAKEN comment; receipts `baseline_original_arms.txt`, `history_da71309c.txt`, `interpreter_matrix.txt` |
| 2. `--self-test` exits 0 on dev, or removed with a reason | met (kept) | `selftest_head_py314.txt`, `selftest_head_py312.txt`; `final_head_gates.txt` |
| 3. docs-check step runs it and `ci_events.py` recognises it | met locally | step 41 in `docs.yml`; `CARRIER_STEP_LISTS` record; `--check` 1513 items and `--selftest` step-41 arms caught. The hosted run needs the maintainer push of the workflow hunk |

Readiness-decision constraints: the fixture geometry is explicit per property; the deployed-model positive control is kept separate; refusal coverage is preserved; no allowlist is widened (the reverse exactness check and receipt M12 prove it); product image bytes are identical.

## Shipping byte comparison

Method (`receipts/gen_outputs.sh`): `git archive <rev>`, with the three pinned public submodules copied in (never symlinked, `.git` dropped, gitlink equality checked). For each of the five tracked configs (`arty_4x4`, `arty_8ch`, `arty_current`, `ax7101_1x1_tdm8`, `ax7101_8x8`) it records the builder's own `load_config`, `emit_aem_overlay` and `_entity_model_image` (`aem_desc.bin`, `aem_desc.json`, `aem_desc.map`, `aem_overlay.json`). It also runs the full builder CLI per config, and the store CLI's default target, builtin `--out-dir` and per-overlay `--out-dir`. It then hashes everything generated.

Result: `manifest_base.sha256` and `manifest_head.sha256` are identical, 83 files. The `aem_desc.bin` SHA-256 values:

| Config | aem_desc.bin sha256 |
|---|---|
| arty_4x4 | `1b288e13ccbf03410c593a53bc22f4a68e3d289eef8a7f907e63bc98a51415ff` |
| arty_8ch | `2b5c008cf3a2ff1eca11ef5e24c5a2e391e97f25435854430e563758de516b9b` |
| arty_current | `ac833c3ccde42a2d9a78b517d660b9f7da03c4b3d31227aa65dcaf9e8def6192` |
| ax7101_1x1_tdm8 | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| ax7101_8x8 | `193bf18736d23256c1b25d9af1bddb0721d95780fb36a14cf5f91476aff1a2d4` |

## Pre-existing finding, out of scope, not changed

The tracked `avdecc/aem_rom.json` does not equal its own regeneration at `ec34fcde` (`receipts/preexisting_aem_rom_json_drift.txt`, reproduced by `decode_aem_rom_drift.py`). It differs at 4 ROM offsets: 118-119, ENTITY firmware_version "2.87.0" against "2.96.0" (VERSION 0x0002_0060); 1117, the AVB_INTERFACE port_number low byte, 0 against 1 (#462); 1467, the CONTROL IDENTIFY reset_time low byte, 3 against 0 (#463). No gate reads the tracked file, and neither does `avdecc/milan_controller.py`; test_builder reads `--out-dir` copies. The drift is identical at the head. Regenerating it would be an unrelated model-artifact change, so it is left for the manager to route as a new Issue if wanted.

## Missing gates, not run by this author

- act replicas: the manager owns them. The candidate's `scripts/act_ci.py` was not executed in any form.
- Hosted contexts (`rtl-fast`, `docs-check`, `wire-accountability`, `docs-check-no-git`, `elaborate`, `verilator-suites`, `yosys-portability`): nothing was pushed.
- The full local bar: `scripts/run_all_suites.sh`, `syn/yosys/run.sh`, behave, both processor suites and donor sweeps. Out of scope for this author, and no RTL changed.
- `ci_events.py --check`/`--selftest` under Python 3.12: that interpreter has no PyYAML here, and installs were out of scope. The self-test itself is stdlib-only and was run under 3.12.
- test_builder gate 11 (calibration) reports NOT RUN, which is environment-dependent and pre-existing.
- Candidate merge validation and post-merge containment: the manager's. As of 13:07 CEST, `dev` equals the base, so the head tree is the candidate tree.

## Risks and open questions

- The fixture's static STREAM_PORT_INPUT map is non-shipping; Milan v1.2 5.3.3.9 keeps a PAAD-AE's inputs dynamic. It is needed because the generator still applies the IEEE 1722.1-2021 7.2.19 INPUT rule and the CRF-sink bound to any static input map a spec or overlay declares.
- The cause oracles bind the vectors to the refusal text in `avdecc/aem_maps.py`. A reworded refusal fails the self-test until its fragment is updated; this is fail-closed.
- Importing the generator builds the deployed model (`aem_assemble._M`), so a refused deployed model fails at import before the positive-control arm prints. The run still exits 1 (receipt M14d).
- The `.github/workflows/docs.yml` hunk needs a push with workflow scope, per the Issue text.

## For the manager

1. Push `464-aem-store-selftest` at `1576f089` with workflow scope. Then open the PR against `dev` with `PR-BODY.md`, and post the self-test evidence as a PR comment (CONTRIBUTING 2.1 step 4).
2. Run the trusted act replica from a clean live-`dev` worktree, and the hosted, native full and candidate bars.
3. Start R235 and R236 cold from the Issue, the PR and this public record.
4. Route the `avdecc/aem_rom.json` drift finding if a follow-up Issue is wanted.
