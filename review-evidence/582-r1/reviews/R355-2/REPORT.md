[R355] POSITIVE - exact head 77998f14b16bf7605956332d0f0ac8af0cecab5a

Round R355-2, external independent re-review of PR #596 for issue #582.
Head `77998f14b16bf7605956332d0f0ac8af0cecab5a`, tree `8efca551799d1ef09c09e6194720bc6fb25b840a`.
The delta under review is `3baff441..77998f14`: two commits, nine files. The whole change from source base `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5` was also re-read.

All five lenses were applied at this head, and all five are CLEAN.

- Every one of my round-1 findings is resolved at this head: F1 BLOCKER and F2-F5 MINOR.
- R354-1 F1 and F2 are resolved, and so are R354-1 S1 and S2.
- I rerun my round-1 mutants at this head: S1-S4 and B3 are now KILLED, and so are the probe-36 ROM mutant and the dropped `--clk-hz` mutant. All eight controls pass.
- No CLI default changed, and the five configurations are byte-identical to the base.
- The findings open at this head are SUGGESTIONs only, and they do not affect coverage.

## Scope reconstructed

I read the sources in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.md.
3. The body of issue #582.
4. The [A10] scope comments on #582 (5853404680 and 5855343934) and the round-1 assignment and decisions (5857543940).
5. The round-2 assignment, 5858125516. It lists required items 1-6, puts R354-1 S3 groups 4/5 out of scope (#495 at merge), and says docs only with no default change for item 5.
6. The [A374] TAKEN and REVIEW READY comments.
7. The authority documents:
   - BAREMETAL_FIRMWARE.md "Build contract";
   - `tb/verilator/nvm_capture_cpu/recipe.py` (`CPU_HZ`);
   - the CI_WORKFLOWS.md gate-read policy;
   - README-parameters.md "Product profile";
   - ENDSTATION_BUILDER.md rows 5a and 34.
8. The diffs `3baff441..77998f14` and `9e9954e9..77998f14`, commit by commit.
9. The public evidence tree `e0c591ff/review-evidence/582-r1`. It holds the round-1 author evidence at `3baff441` only. I found no round-2 evidence tree in it, so this head's evidence is my own receipts plus the [A374] REVIEW READY comment.
10. The exact-head hosted check runs.

I read prior public findings only after the verdict and ledger were fixed (see "Prior public review findings").

## Required items (round-2 assignment), verified at this head

1. **The tap page is registered as gate-read. Met.**
   - `scripts/ci_scope.py:54-59` adds `docs/AAF_LATENCY_TAPS.md` to `GATE_READ_DOCS`, and `:264-265` adds its classification case.
   - `docs/testing/CI_WORKFLOWS.md:56-63` says "Four pages" and names the reader. `:74` adds a reader-table row.
   - Receipt `10_ci_scope_head.log`:
     - `--selftest` returns rc 0 with `selftest: PASS`;
     - the PR's file list classifies `true`;
     - a docs-only edit of the tap page classifies `true` (relevant), while a plain docs page classifies `false`.
   - The registration is bound by the self-test. Mutant CI1 drops it from `GATE_READ_DOCS` and fails with 2 failures. Mutant CI2 drops its case and fails with 1 failure. Both are KILLED (`30_mutants.log`).
   - Exact-head hosted `changes`, `full-ci-gate` and `rtl-fast` now succeed (`51_hosted_checks.txt`). At `3baff441` they failed.
2. **The ROM follows the configured Milan clock. Met.**
   - `sw/builder/test_clock_contract.py:75-101` (`test_gptp_rom_clock`) does the following for each of the five configurations:
     - it builds the configuration and regenerates the ROM with the gPTP generator, passing the normalized `milan_clk_hz`;
     - it requires byte equality between the two;
     - it requires that both the no-`--clk-hz` ROM and the `sys_clk_hz` ROM differ from it.
   - The test is wired into the builder bank at `test_builder.py:27559-27566`, which `docs-check` and `elaborate` both run.
   - These mutants are KILLED (`30_mutants.log`):
     - R1, the probe-36 mutant, which feeds `sys_clk_hz`;
     - R2, which drops `--clk-hz` (the R354-1 F2 mutant);
     - R3, which feeds the board-default system clock.
   - I reran probe 36 (`36_rom_clock_replay.log`). The mutant ROM still differs from the correct ROM in 7 of 1024 words and still passes gate 1b's remaining assertions. The new test is what now kills it.
3. **SoC product argv, `--no-milan` and builder `flashboot: none`. Met.**
   - SoC side:
     - `test_clock_contract.py:129-132` substitutes ±1 Hz, 80 MHz and 100 MHz into `emit_soc_argv` of every tracked configuration.
     - `:143-147` covers `--no-milan` at the contract clock through either option (accepted), and at each divergent value through either option (refused).
   - Builder side: `:47-51` proves that `flashboot: none` loads, and `:60-63` refuses every bad clock with `flashboot: none`.
   - My mutants S1-S4 and B3 are all KILLED, and so are S5, S6 and the new S8. Controls C0-C7 all pass.
   - `31_soc_behaviour_head.log`: 75 cases, 0 unexpected. The base gives 45 unexpected, because the base accepts divergent clocks.
   - `33_builder_cli_head.log`: 12 cases, 0 unexpected. The base gives 7 unexpected.
4. **The fixed clock is stated by reference. Met.**
   - `sw/builder/README-parameters.md:58` has a `board.constraints.milan_clk_hz` row: "`CPU_HZ` in recipe.py; Fixed Milan and bare-metal CPU clock; divergent values refuse".
   - `docs/ENDSTATION_BUILDER.md:967` (row 5a) and `:1014` (row 34) each add "The Milan clock is fixed to `CPU_HZ` in recipe.py; divergent values refuse".
   - None of the three restates the number: a grep for 50 MHz spellings finds no hit in either file. `recipe.py:5` holds the only definition.
   - `check_doc_paths` resolves both links (`40_doc_static_gates.log`).
5. **Usage block and clock help, docs only. Met, and no default changed.**
   - `sw/litex/milan_soc.py:7-23` now opens with the required `--milan-clk-freq <CPU_HZ>`, or `--sys-clk-freq <CPU_HZ>` without a Milan domain. It names `recipe.py`, requires `--entity-gen-dir` for Milan builds, and scopes `--no-milan` to a CLI smoke path.
   - The `--sys-clk-freq` help (`:3391-3394`) and the `--milan-clk-freq` help (`:3401-3405`) match the guard at `:3704-3707`, which checks `(milan or sys) != CPU_HZ` with no `--no-milan` exemption.
   - The `--entity-gen-dir` help (`:3494-3499`) matches `_builder_out` (`:3294-3310`).
   - `31_soc_behaviour_head.log`: every documented usage is refused as written with the named `baremetal clock:` message, and is accepted once the header's required option is added.
   - `37_cli_defaults.log` compares an AST of all 54 `add_argument` calls at base and head. There are 0 non-help keyword differences. Only the help of `--sys-clk-freq`, `--milan-clk-freq` and `--entity-gen-dir` changed. `--sys-clk-freq` stays `default=100e6`, and `--milan-clk-freq` stays `default=None`.
   - Mutants D2 and D3 plant a changed default. `check_solution_docs.py` kills both.
6. **The readers use the normalized configuration. Met.**
   - `test_pp_mem_bridge.py:389-398` (`configured_clock_pairs`) now reads `eb.load_config(path)["constraints"]`. Its fixture (`:400-427`) proves both the loader call order and the board default when `sys_clk_hz` is omitted.
   - `test_clock_contract.py:161-168` (`_assert_sweep_clocks`) reads `eb.load_config(config)`. `test_extra_sweep_clocks` adds an omitted-`sys_clk_hz` case.
   - Mutants N1 and N2 revert each reader to raw YAML, and both are KILLED. So is W4, where the sweep prints the board default.

**Second commit `77998f14` ("Preserve the system clock mutation after adding CLI help"). It does not weaken a test.**
- It changes only the anchor strings of the `system clock default` arm in `scripts/check_solution_docs.py:791-797`, because the head's multi-line `add_argument` no longer contains `type=float)`.
- The arm still plants `default=80e6` into the same call and still expects "system clock default differs". The gate reads the default by AST, so the reader is unchanged.
- Evidence:
  - The self-test has 43 mutation controls at both base and head (`38_solution_docs_arms.log`).
  - Mutant D1 reverts to the old anchor, and the self-test fails with "missing fixture for system clock default". So the commit was necessary, and the arm is live.
  - Mutant D2, a real default change, is caught by the gate.
- This file was not named by the assignment, but the edit is a forced consequence of item 5's help text.

**Unchanged constraints.**
- Base to head changes nothing under `configs/`, `tb/`, `hdl/` or `sw/firmware/`, and no gitlink or `.gitmodules` (`22_scope_and_history.log`).
- The builder CLI produces byte-identical complete output trees at base and head for all five configurations, 10 files each. The per-configuration tree digests equal my round-1 digests (`20_artifact_identity.log`).
- In-tree `--write-fragment --write-rtl` regeneration is identical between the base and head copies (`21_fragment_identity.log`).
  - Only the 13 PR files differ; the script's echo line still says "eight" from round 1.
  - In both copies the regenerated per-board fragments and `adp_shape_defaults.svh` differ from the tracked copies in the same way. That is last-writer order, and it is the same at base and head.
- `check_nvm_capture.py` returns rc 0 (`11_focused_gates_clone.log`).
- Both new commits have one-line messages with no trailers, and `git diff --check 3baff441..HEAD` returns rc 0.

## Findings

No BLOCKER, MAJOR or MINOR finding is open at this head.

### Suggestions (do not affect coverage)

- **SG5 - SUGGESTION - Docs - `docs/testing/CI_WORKFLOWS.md:56-63` vs `:67-75`: the new reader-table row can be read as filing the tap page as documentation only.**
  - The prose lists the page among the four relevant pages, and `GATE_READ_DOCS` makes it relevant.
  - The table is introduced as the readers whose page "stays documentation only when" `docs-check` runs the same check, and the new row answers "yes".
  - Every fact in the row is true, the classifier behaviour is correct and conservative, and my own round-1 F1 asked for the row.
  - A clause saying the page is nonetheless relevant, because `test_clock_contract.py` is not in `DOCS_JOB_PY`, would remove the ambiguity.
- **SG6 - SUGGESTION - Tests - `sw/builder/test_clock_contract.py:125-132`: the product argv tested is `emit_soc_argv` without `--entity-gen-dir`.**
  - Every real launch adds `--entity-gen-dir` (`build.sh:376`, `deploy.sh:125`, `sweep.sh:116`). My new mutant S9 exempts `--entity-gen-dir` from the guard, and it SURVIVES (`30_mutants.log`).
  - It is not a round-1 mutant or a required item, and the narrowing it models is contrived.
  - Appending the configuration's `--entity-gen-dir` to the product cases would close it.
- **SG7 - SUGGESTION - Tests, Robustness - `sw/builder/test_clock_contract.py:94-96`: the ROM test fails on a builder-accepted shape where `sys_clk_hz == milan_clk_hz`.**
  - `39_rom_test_equal_clocks.log`: the builder accepts the 1x1 at 50/50 MHz, and the test then fails with "ROM clock control is insensitive". The system-clock control equals the correct ROM by construction in that case.
  - No tracked configuration has equal clocks, and the failure is loud.
  - Skipping that control when the two clocks are equal, or using a fixed off-contract control clock, would avoid a misleading failure on a future shape.
- **SG8 - SUGGESTION, pre-existing, follow-up Issue suggested - Robustness - `sw/litex/sweep_extra.sh:48`: the launched command has no `--entity-gen-dir`.**
  - The refreshed `--entity-gen-dir` help (`milan_soc.py:3494-3499`) and `_builder_out` (`:3300-3303`) make the flag required for the Milan path, so a real `sweep_extra.sh` launch would stop with "pass --entity-gen-dir".
  - The base script also lacks the flag. This PR only derived its clocks, so the defect is outside #582's scope.
- **Retained from R355-1, unchanged at this head:**
  - **SG1:** mutants B5 and S7 (a literal mirror in place of the import) SURVIVE. A regular `tb` package on `PYTHONPATH` still replaces the contract clock (`34_env_shadow.log`).
  - **SG2:** mutant P1 (the precedence loop drops the configured pairs) still SURVIVES.
  - **SG3:** restatements remain. Groups 4/5 are out of scope, to #495 at merge.
  - **SG4:** `sweep_extra.sh` argument-order fragility.
  - B6 is a deliberately over-fitted mutant, is recorded, and is not a finding.

## Gates and probes I ran (receipts listed in MANIFEST.sha256)

- **Focused gates on the clone** (`11_focused_gates_clone.log`), all rc 0:
  - `test_clock_contract.py --soc`: 50 named refusals, 5 ROMs, sweep, tap and SoC checks;
  - `test_declarations.py`;
  - `check_nvm_capture.py`;
  - `test_pp_mem_bridge.py`: 113/113, which also runs the SoC contract test and the clock-pair fixture.
- **Documentation and static gates** (`40_doc_static_gates.log`, `41_renderer_gates.log`):
  - Every gate the assignment names returns rc 0:
    - `ci_scope.py --selftest`;
    - `check_baremetal_only.py --check` and `--selftest`;
    - `check_entity_shape.py --self-test`;
    - `check_deploy_shape.py --self-test`;
    - `check_em_dash.py --selftest` (339 arms) and `--base 9e9954e9` (49 added lines in 5 pages);
    - `docs_check.py` and its `--selftest`;
    - `check_doc_style`, `check_doc_paths` and `check_solution_docs`, including its self-test;
    - hygiene and idiom checks;
    - the TOC and anchor checks;
    - `git diff --check` base..head.
  - Four checks returned rc 2 on the first pass because that interpreter lacks the pinned Markdown renderer. All four returned rc 0 under a disposable interpreter built with `--require-hashes` from `tools/markdown/requirements.txt`.
- **Workflow static checks:** 23 of 23 returned rc 0 (`42_workflow_static.log`), including `ci_events.py --check` and `--selftest`, and `ci_litex_env.py`.
- **Mutation:** 39 entries, consisting of 8 controls, all passing, and 31 mutants (`30_mutants.log`).
  - 26 mutants are KILLED: B1-B4, S1-S6, S8, W1-W4, P2, R1-R3, N1, N2, CI1, CI2 and D1-D3.
  - 5 SURVIVE: B5, S7 and P1 are retained suggestions SG1 and SG2; B6 is over-fitted by design; S9 is SG6.
- **Behaviour probes:**
  - SoC: 75 cases at head and base (`31_*`).
  - Sweep: 15 dry-run cases (`32_sweep_extra.log`).
  - Builder CLI: 12 cases at head and base (`33_*`).
  - Environment shadow (`34_*`), ROM replay (`36_*`), CLI defaults (`37_*`), self-test arm count (`38_*`) and the equal-clock ROM test (`39_*`).

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #582 acceptance 1-4 and the [A10] assignments 5857543940 and 5858125516, items 1-6; `endstation_builder.py:4296-4299,5699-5704`; `milan_soc.py:3704-3707`; `recipe.py:5`; `sweep_extra.sh:9-21`; `test_clock_contract.py:75-101,120-148`; receipts 10, 20, 21, 22, 31, 32, 33, 37 | R355-2 | 77998f14b16bf7605956332d0f0ac8af0cecab5a |
| RTL | CLEAN | No HDL, bench or gitlink change (`22_scope_and_history.log`). The new `--milan-clk-freq` help ("separate Milan and CPU domain") was checked against the guard and the round-1 domain rules (`_CRG` `if milan_clk_freq`, Vexii `with_cpu_clk = bool(milan_clk_freq)`, `milan_cd`), which are unchanged. The ROM generator's clock input (`gen_gptp_ucode.py:432-450`) was checked against the test's byte comparison. | R355-2 | 77998f14b16bf7605956332d0f0ac8af0cecab5a |
| Robustness | CLEAN (SG7 and SG8 are suggestions) | ±1 Hz, 0, 80 MHz and 100 MHz on the product argv of all five configurations; `--no-milan` through each option; implicit system clock; `flashboot: none`; omitted `sys_clk_hz` in both readers and the sweep; wrong, missing, empty and absolute `SWEEP_CFG`; equal system and Milan clocks; `PYTHONPATH` shadow. Receipts 31, 32, 33, 34, 39 | R355-2 | 77998f14b16bf7605956332d0f0ac8af0cecab5a |
| Tests | CLEAN (SG6 and SG7 are suggestions) | `test_clock_contract.py` (whole file); `test_pp_mem_bridge.py:389-427,948-951`; `test_builder.py:17119-17124,27559-27566`; `ci_scope.py:47-59,255-266,310-470`; `check_solution_docs.py:763-805,940-975`; receipts 30 (8 controls and 31 mutants), 11, 36, 38, 40, 42 | R355-2 | 77998f14b16bf7605956332d0f0ac8af0cecab5a |
| Docs | CLEAN (SG5 is a suggestion) | `CI_WORKFLOWS.md:43-90`; `README-parameters.md:47-61`; `ENDSTATION_BUILDER.md:967,1014`; `milan_soc.py:1-30,3388-3405,3494-3499`; `ci_scope.py` docstring and comments at `:1-80`; BAREMETAL_FIRMWARE.md and AAF_LATENCY_TAPS.md unchanged since round 1, re-read at `:19-70` and `:11-31`; receipts 40, 41, 42, 37 | R355-2 | 77998f14b16bf7605956332d0f0ac8af0cecab5a |

## Prior public review findings on this PR

I read these only after the verdict and ledger above were written. The only prior public review rounds are R354-1 (5858016029) and my own R355-1 (5858120015). R354-2 had published only its start notice when I read the thread.

- **Manager bank r1 (5857952562), gate 6 `ci_scope.py --selftest`:** **resolved**. It passes at this head (receipts 10, 40, 42), and hosted `changes` and `rtl-fast` succeed.
- **R355-1 F1 BLOCKER (Tests, Docs), the gate-read page not registered:** **resolved** by item 1 above, including the CI_WORKFLOWS.md prose and table. SG5 records a residual wording ambiguity as a suggestion.
- **R355-1 F2 MINOR (Tests), the guard-narrowing mutants:** **resolved**. S1-S4 and B3 are KILLED, and controls C0-C3 pass.
- **R355-1 F3 MINOR (Tests), ROM clock binding:** **resolved**. The probe-36 mutant (R1) is KILLED by `test_gptp_rom_clock`, which runs in the builder bank.
- **R355-1 F4 MINOR (Docs), the parameter reference:** **resolved** by item 4.
- **R355-1 F5 MINOR (Docs), usage block and clock help:** **resolved** by item 5, with no default changed.
- **R355-1 SG1-SG4:** **retained** as suggestions, unchanged. See above.
- **R354-1 F1 BLOCKER (Tests, Docs):** the same defect as my F1. **Resolved.**
- **R354-1 F2 MINOR (Tests), `--clk-hz` not proven:** **resolved**. Its mutant is my R2, and R2 is KILLED.
- **R354-1 S1 SUGGESTION, raw-YAML clock reads:** **resolved** by item 6. Mutants N1 and N2 are KILLED.
- **R354-1 S2 SUGGESTION, usage block and `--entity-gen-dir` note:** **resolved** by item 5. SG8 records the related pre-existing `sweep_extra.sh` omission.
- **R354-1 S3 SUGGESTION, remaining restatements:** **retained**. Groups 4/5 are out of scope by the assignment and go to #495 at merge. This agrees with my SG3.

## Limits

- **Where things ran.**
  - The focused gates, the documentation, static and workflow checks, and the `ci_scope` probe ran on the review clone.
  - Every mutant, behaviour probe and base comparison ran on disposable exports under `scratch/`. Each export was given a private local git snapshot in the copy and each submodule, because the SoC path runs `git ls-files` (`01_prepare_copies.sh`).
  - The submodule trees of the copies equal the clone's (protocol-processor tree `7e6d16f3…`).
- **Banks not run.** As assigned, I did not run the full builder bank (either compiler mode), the parent, PP, gPTP, Yosys or native banks, `act`, or any hardware step. `test_gptp_rom_clock` was run on its own and through `test_clock_contract.py`, not through the full `test_builder.py`.
- **Scoped Verilator was not used.** No RTL, HDL or bench changed, so its identity was not checked.
- **Hosted evidence** was inspected read-only (`50_hosted_checks_initial.txt`, `51_hosted_checks.txt` at 19:22 UTC).
  - Succeeded: `changes`, `full-ci-gate`, `rtl-fast`, `bdd-conformance`, `docs-check-no-git`, `wire-accountability`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3, and Verilator shards 0 and 3.
  - Still in progress: `docs-check`, `elaborate`, and Verilator shards 1, 2 and 4.
  - Skipped: "Physical gPTP (nightly and manual)". A skipped context is not evidence either way.
- **Hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Clone restore.**
  - One ignored byproduct, `sw/builder/out/`, was created at 21:18 during this round's gate run and removed. Bytecode writing was disabled throughout.
  - Final state (`05_clone_identity_final.txt`):
    - head, tree and index tree are `77998f14`/`8efca551`;
    - the `ls-files -s` digest is unchanged from `00_clone_identity_before.txt`;
    - the four gitlinks are unchanged, and the three checked-out submodules are clean at their gitlinks;
    - `git status --ignored` is empty.
  - The work copy equals the head export after all probes.

## Pending manager duties

- Hosted and `act` acceptance at this head. `docs-check`, `elaborate` and Verilator shards 1, 2 and 4 were still running at my last inspection.
- The full builder bank in both compiler modes, and the native banks, at this head. The brief reports them passed, but the public evidence tree I could read holds round-1 material only.
- The final current-dev candidate build and its validation (source base `9e9954e9`, live dev `6d5ebd73`).
- The internal review verdict (R354-2) and the completion ledger acceptance.
- Follow-up Issues the maintainers want: SG8, the `sweep_extra.sh` launch without `--entity-gen-dir`; SG1, the import-by-path guard; and #495 for S3 groups 4/5.

R355-2 FINISHED
