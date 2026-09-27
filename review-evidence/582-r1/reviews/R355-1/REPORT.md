[R355] NEGATIVE - exact head 3baff4411fd70aaccb066662628ff0b0a7d7c05d

Round R355-1, external independent review of PR #596 for issue #582.
Head `3baff4411fd70aaccb066662628ff0b0a7d7c05d`, tree `ce000a55f0ce2cfdb6e63959bf70a4f579426a77`, one commit on source base `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5`.
All five lenses were applied. The verdict is NEGATIVE because of one BLOCKER and four MINOR findings.

- **BLOCKER F1.** The PR breaks the repository's CI scope classifier self-test. `scripts/ci_scope.py --selftest` returns rc 1 at the head and rc 0 at the base. As a result, the hosted `changes`, `rtl-fast`, `elaborate` and `full-ci-gate` contexts failed on the exact head.
- **MINOR F2 and F3.** Refusal and ROM-clock mutants survive the tests.
- **MINOR F4 and F5.** Two documents still describe the pre-refusal contract.

The substance of the change is correct:

- Both tools refuse every divergent bare-metal clock I planted, and the base accepts the same clocks.
- The five configurations produce byte-identical artifacts to the base.
- The capture receipt is unchanged.
- The tap-page table matches the configurations.

## Scope reconstructed

I read the sources in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.md.
3. The body of issue #582.
4. The [A10] comments on #582:
   - 5853404680, the dated-history note for AAF_LATENCY_TAPS.md;
   - 5855343934, the scala_args message;
   - 5857543940, the assignment and decisions.
5. The [A370] TAKEN and REVIEW READY comments.
6. The body of PR #596.
7. BAREMETAL_FIRMWARE.md "Build contract", AAF_LATENCY_TAPS.md, CI_WORKFLOWS.md "gate-read" policy, README-parameters.md "Product profile" and ENDSTATION_BUILDER.md rows 5a and 34.
8. The full diff `9e9954e9..3baff441`, which touches 8 files, and its history. It is one commit with a one-line message and no trailers.
9. The public evidence tree `e0c591ff/review-evidence/582-r1`: identity, gates, mutations, clock-contract and capture logs.
10. The exact-head hosted check runs.

## Findings

### F1 - BLOCKER - Tests, Docs - `sw/builder/test_clock_contract.py:155`, `scripts/ci_scope.py:54-58` (`GATE_READ_DOCS`), `docs/testing/CI_WORKFLOWS.md:56-75` - the new gate reads a docs page that the CI scope classifier does not know about

**Authority and evidence.** CI_WORKFLOWS.md sets the #444 rule for gate-read pages: a page read by Python in a classifier-gated root is relevant unless the reader is registered. `scripts/ci_scope.py --selftest` derives that set and refuses any difference.

- The new `test_tap_clock_docs` reads `docs/AAF_LATENCY_TAPS.md`.
- The reader is not registered as a gate-read page. It is also not listed in `DOCS_JOB_PY` or in the policy table as a docs-check reader.
- Receipt `receipts/50_ci_scope_head.log`: at the head, `FAIL gate-read page docs/AAF_LATENCY_TAPS.md (named at sw/builder/test_clock_contract.py:155) is relevant`, `selftest: 1 FAILURE(S)`, rc 1.
- Receipt `receipts/50_ci_scope_base_selftest.log`: the same self-test on a base export gives `selftest: PASS`, rc 0.
- Receipt `receipts/50_hosted_checks.txt`: the exact-head hosted runs are on merge `f09d5ef`, which is 3baff441 merged into live dev 2a2a7bb6.
  - `changes`, `elaborate` and `full-ci-gate` each fail on this same self-test line.
  - `rtl-fast` fails because `CHANGES_RESULT: failure`.
  - `verilator-suites` and `yosys-portability` fail on "no shard evidence", which follows from the skipped shards.
- The author's and manager's published gate lists do not include this self-test.

**Impact.**
- The required `rtl-fast` verdict (AGENTS section 7) cannot pass at this head, and the RTL-relevant hosted gates cannot produce evidence.
- The classifier contract is broken: `echo docs/AAF_LATENCY_TAPS.md | scripts/ci_scope.py` prints `false`, so a docs-only edit is filed as documentation.
- `docs-check` does still run `test_builder.py`, which now calls the tap check. That partly contains the practical coverage gap, but the registration and the policy table do not say so.

**Required outcome.**
- `scripts/ci_scope.py --selftest` passes at the head.
- A docs-only edit of the tap page is still graded by a job that runs the tap-table check.
- The CI_WORKFLOWS.md reader table and prose name the new reader, as the policy requires.

**Verification.**
- `python3 scripts/ci_scope.py --selftest` rc 0.
- Exact-head hosted `changes` and `rtl-fast` succeed.
- `scripts/ci_events.py --check` stays rc 0.

### F2 - MINOR - Tests - `sw/builder/test_clock_contract.py:64-106` (SoC refusal cases), `:36-60` (builder refusal cases) - refusal tests leave realistic guard narrowings alive

**Authority and evidence.** The AGENTS Tests lens says that each new test can fail for the defect it claims to detect, and that real integration wiring is tested where practical.

- The SoC refusal cases use only a minimal argv, such as `["--milan-clk-freq", bad]`. The configured product argv is tested only as a positive.
- Receipt `receipts/30_mutants.log` runs my own mutants, with identity-replacement controls C0-C3 all passing. These survive:
  - S1: the SoC guard exempts `--no-milan`.
  - S2: the SoC guard exempts `--full`, which is the product argv.
  - S3: the SoC guard exempts `--board arty`.
  - S4: the SoC guard exempts `--with-spiflash`.
  - B3: the builder guard applies only when `flashboot == "baremetal"`, while `flashboot: none` is an accepted bare-metal value.
- The head code itself is correct.
  - Receipt `receipts/31_soc_behaviour_head.log`: the head refuses all 45 divergent product-argv cases (75 cases, 0 unexpected); the base accepts all 75.
  - Receipt `receipts/33_builder_cli_head.log`: the head refuses `flashboot: none` at 100 MHz.
- The #565 regression this issue exists for, the 8x8 product argv at 100 MHz, is therefore not protected at the SoC entry point.

**Impact.** A later edit that narrows either refusal to non-product inputs would pass every gate. That reopens the #565 failure mode at the SoC, which is the last check before Vivado for `build.sh`, `sweep.sh`, `sweep_extra.sh` and `deploy.sh`.

**Required outcome.**
- The SoC refusal test exercises the configured product argv of each tracked configuration, and the documented `--no-milan` path, at divergent clocks.
- The builder refusal covers the accepted `flashboot: none` variant.
- Together these must kill S1-S4 and B3.

**Verification.** Rerun `scripts/30_mutants.py`. S1-S4 and B3 must be KILLED, and the controls must still pass.

### F3 - MINOR - Tests - `sw/builder/test_builder.py:17106-17123`, `sw/builder/endstation_builder.py:5703` - the config-to-gPTP-ROM clock binding lost its only kill test

**Authority and evidence.** The AGENTS Tests lens says that positive, negative and boundary behaviour is covered and that real integration wiring is tested where practical.

- The removed 80 MHz ROM variant was the only arm that proved `gptp_ucode.hex` follows the Milan clock passed as `--clk-hz`.
- At the head, the ROM assertions that remain are `test_builder.py:2998-3006` and `:17106-17118`: the ROM exists, has 1024 words, and changes with the MAC and priority1. The engine-pin gate at `:25088-25140` does not read the clock.
- Receipt `receipts/36_rom_clock_replay.log`: I planted a mutant that feeds `sys_clk_hz` (100 MHz on the AX shapes) to `--clk-hz`.
  - The mutant's ROM differs from the correct 50 MHz ROM in 7 of 1024 words.
  - It passes every one of those remaining assertions.
- The assignment required the variant to be converted to a refusal, and that is correct. What was lost is the binding coverage, not the variant itself.

**Impact.** A builder that generates the fabric gPTP microcode for the wrong clock would ship with the gates green, and the gPTP time arithmetic would be off by the clock ratio on silicon.

**Required outcome.** An executable check proves that the builder's ROM follows the contract or configured Milan clock and kills the probe-36 mutant. The test design is the author's choice.

**Verification.** The probe-36 mutant is killed by a bank test.

**Limit.** Under the mutant, I replayed the assertions rather than running the whole `test_baremetal_profile_contract`. That function exceeds this session's 600 s per-command ceiling. See Limits.

### F4 - MINOR - Docs - `sw/builder/README-parameters.md:47-60` ("Product profile"), named by `docs/ENDSTATION_BUILDER.md:1014` (row 34) - the accepted-values table omits the new clock refusal

**Authority and evidence.**
- The AGENTS Docs lens says that changed contracts are reflected in authoritative docs.
- ENDSTATION_BUILDER.md row 34 says the accepted product-profile values are in README-parameters.md#product-profile.
- That table lists the CPU, XLEN, cpu_count, full, scala_args, l2_bytes and flashboot, and ends "Unknown values and keys are rejected".
- The builder now also rejects any `board.constraints.milan_clk_hz` other than the contract clock (`endstation_builder.py:4296-4299`). Neither the table nor row 34 or row 5a (`milan_clk_hz`) says so.
- BAREMETAL_FIRMWARE.md was updated, but the builder's own parameter reference was not.

**Impact.** A reader who configures from the parameter reference cannot see that the Milan clock is fixed. They meet the refusal only at build time.

**Required outcome.** The parameter reference states the accepted Milan clock by reference to its single definition, without restating the number.

**Verification.** Read the page, and the docs gates stay rc 0.

### F5 - MINOR - Docs - `sw/litex/milan_soc.py:7-14` (usage block), `:3382`, `:3389-3393` (clock help) - documented invocations now exit 2

**Authority and evidence.**
- The AGENTS Docs lens says that changed contracts are reflected in authoritative docs.
- Receipt `receipts/31_soc_behaviour_base.log` and `_head.log` cover the five usages the header documents: `./milan_soc.py`, `--full`, `--with-mac`, `--no-milan` ("bring-up smoke; self-contained") and the bare-metal flashboot line.
  - At the base, all five reach the platform.
  - At the head, all five exit 2 with `baremetal clock:`, because the `--sys-clk-freq` default is 100e6 and `--milan-clk-freq` defaults to none.
- The `--milan-clk-freq` help still describes an optional "slower clock domain (Hz, e.g. 50e6)".
- The refusal itself is required by the decision. The text around it now documents rejected commands.

**Impact.** The tool's own usage block and help mislead anyone doing bring-up. The documented smoke test fails on first use.

**Required outcome.** The usage block and the clock help describe invocations the tool accepts, or state the contract-clock requirement.

**Verification.** Rerun `scripts/31_soc_behaviour.py`: each documented usage is accepted as written, or the text names the required clock.

### Suggestions (do not affect coverage)

- **SG1 (Robustness, Tests): the one-source property has no executable guard.**
  - Mutants B5 and S7 replace the import with a literal `50_000_000`, and both survive (`receipts/30_mutants.log`).
  - The import `tb.verilator.nvm_capture_cpu.recipe` resolves through a namespace package. A regular `tb` package anywhere on `sys.path` replaces the contract clock (`receipts/34_env_shadow.log`: under such a PYTHONPATH the shipped 1x1 is refused with "must be 100000000 Hz"). The capture gate imports the same file by directory, so the two readers can diverge.
  - Clock-named environment variables have no effect.
  - Consider importing by file path, and a check that the refusal follows `recipe.CPU_HZ`.
- **SG2 (Tests): the configured pairs are not guarded inside the precedence loop.**
  - Mutant P1 drops the configured pairs from the `test_precedence` loop and survives.
  - The head log does show all five configured pairs graded, 113/113.
- **SG3 (Docs, Tests): remaining restatements of the clock value.** None of these is read by either refusal.
  - `tb/verilator/milan_dp/Makefile:413` (`AX_GPTP_HZ = 50000000`, the AX 1x1 physical-rate bench). This is the only one not cross-checked against the configuration or the contract. A follow-up Issue is suggested.
  - `sw/litex/sweep.sh:47-48` default tables. The generated fragment overrides them, and gate 9 and `check_sweep_shape.py` gate them.
  - `scripts/check_solution_docs.py:62`, an independent oracle.
  - `sw/builder/test_builder.py:17097`, a print string.
  - Dated measurement records, correctly labelled: BAREMETAL_FIRMWARE.md:1991/2017, SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1596/1772, nvm_capture_cpu/README.md:44-48.
- **SG4 (Robustness): `sweep_extra.sh` is fragile about argument order and environment.**
  - `--dry-run` is honoured only as the third argument. `sweep_extra.sh ax7101 --dry-run` takes it as the tag and launches.
  - `clock_options` runs before the virtualenv PATH export. `sweep.sh` sets up its environment first.
- **Observation, pre-existing.** `int(_req(...))` truncates `milan_clk_hz: 50000000.9` to the contract clock, and the build is accepted (`receipts/33_builder_cli_head.log`). The effective and emitted clock equals the contract, so this is not a bypass.

## Evidence per verification item from the assignment

1. **Refusals: met.**
   - The builder refuses 100/80 MHz, ±1 Hz, 25 MHz, `flashboot: none` and milan=sys cases by name ("baremetal clock: ... (docs/integration/BAREMETAL_FIRMWARE.md build contract)"), with no output and no fragment written (`33_builder_cli_head.log`). The base builds all of them rc 0 (`33_builder_cli_base.log`).
   - The SoC refuses:
     - divergent `--milan-clk-freq` on every product argv;
     - the implicit system fallback, which removes `--milan-clk-freq` and uses sys 100e6 or 83.333e6;
     - the disabled domain (`--milan-clk-freq 0`);
     - `--no-milan` at 100e6;
     - duplicate-override-last.

     It accepts the configured argv and sys = 50e6 with no Milan domain (`31_soc_behaviour_head.log`, 75/75).
   - `MilanSoC(...)` is constructed only from `main()`. The capture harness subclasses it for its labelled 100 MHz comparison arm and is not a product path.
   - No environment variable is read by either tool. See SG1 for PYTHONPATH.
2. **80 MHz variant: met.** It is now refused (`test_builder.py:17106-17123`, and `test_clock_contract.py` bad list). The Scala message "no scala_args overrides" matches its check `soc["scala_args"]` truthy, and a non-cache override is refused. The SoC message was already "no --scala-args overrides". F3 records the coverage side effect.
3. **Clock pairs: met.**
   - `configured_clock_pairs()` reads all five YAMLs, and the head log grades 5 configured and 2 labelled historical pairs.
   - The sweep dry-run defaults are arty_4x4 → 83333000/50000000 and 1x1 → 100000000/50000000.
   - SWEEP_CFG works for every configuration, relative and absolute paths, and an empty value.
   - A wrong board, a missing configuration or a 100 MHz variant is refused (`32_sweep_extra.log`).
   - The Arty configurations build (`20_artifact_identity.log`).
4. **Tap page: met.**
   - The present-tense text divides by the configuration's `milan_clk_hz`. The table equals the configurations: 20 ns/cycle, with the 8x8 pruned, and is checked.
   - The 2026-07-26 section keeps "100 MHz (10 ns/cycle)" and all values. The diff only adds the historical label.
   - `axis_clk` equals the Milan domain whenever `--milan-clk-freq` is set (`milan_soc.py:2766`).
   - Tap-tool audit: no tool converts tap cycles to time. `KL_lat_history_ring` is not instantiated, and `nvm_host.c` `NS_PER_CYCLE` models the 100 MHz system timer, not taps.
5. **BAREMETAL_FIRMWARE.md: met.** It states that both tools enforce the clock, names the single definition, and describes the system-clock fallback. The "not checked by either tool" text is gone, and grep finds it nowhere in the tree.
6. **Identity: met.**
   - The builder CLI on base and head gives byte-identical complete output trees for all five configurations, 10 files each (`20_artifact_identity.log`).
   - In-tree `--write-fragment --write-rtl` regeneration is identical between base and head copies (`21_fragment_identity.log`).
   - My results agree with the author's published per-artifact digests, which hash an equal set.
   - `check_nvm_capture.py` rc 0. The recipe and receipt are untouched, and no path under `hdl/`, `sw/firmware/`, `tb/`, `configs/` or the submodules changed.

## Gates I ran (receipts listed in MANIFEST.sha256)

- **Focused gates on the clone:** `test_clock_contract.py --soc`, `test_declarations.py`, `check_nvm_capture.py` and `test_pp_mem_bridge.py` (113/113) all returned rc 0 (`10_focused_gates_clone.log`). The first attempt, with an interpreter lacking migen and a copy without submodule git metadata, is kept as `10_focused_gates_head.log` and records only environment failures.
- **Documentation gates:** 12 of 15 returned rc 0 on the first pass. The three that need the Markdown renderer returned rc 0 with a disposable hash-pinned renderer (`40_doc_static_gates.log`, `41_renderer_gates.log`).
- **Other workflow checks:** 21 of 23 returned rc 0 (`42_workflow_static.log`).
  - `ci_scope.py --selftest` returned rc 1. This is F1.
  - `ci_litex_env.py` returned rc 1 because that interpreter has no LiteX pythondata. This is an environment failure, not the PR.
- **Whitespace and shell syntax:** `git diff --check 9e9954e9 HEAD` rc 0; `bash -n sw/litex/sweep_extra.sh` rc 0.
- **Mutants:** 18 mutants plus 4 controls, and all 4 controls pass (`30_mutants.log`). 9 mutants were killed: B1, B2, B4, S5, S6, W1-W3 and P2. 9 survived: B3, B5, B6, S1-S4, S7 and P1. B6 is a deliberately over-fitted band mutant built around the sampled test points. It is recorded, and it is not a finding.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #582 acceptance 1-4, [A10] 5853404680/5855343934/5857543940; `endstation_builder.py:66-72,4293-4305`; `milan_soc.py:59-64,3686-3697`; `sweep_extra.sh`; `test_pp_mem_bridge.py:383-418`; `AAF_LATENCY_TAPS.md:14-31,141-146`; `BAREMETAL_FIRMWARE.md:29-70`; receipts 20, 21, 31, 32, 33, 10 | R355-1 | 3baff4411fd70aaccb066662628ff0b0a7d7c05d |
| RTL | CLEAN | No HDL in the diff (`git diff --name-only`). Checked the guard's effective-clock semantics against `_CRG` (`milan_soc.py:242-255`, `if milan_clk_freq`), the Vexii `with_cpu_clk = bool(milan_clk_freq)` (`:2569`), `milan_cd` (`:2766`) and `milan_clk_hz=int(milan_clk_freq or sys_clk_freq)` (`:2949`). The tap `axis_clk` claim was checked against the same `milan_cd` rule. No CDC primitive changed. | R355-1 | 3baff4411fd70aaccb066662628ff0b0a7d7c05d |
| Robustness | CLEAN | Boundaries ±1 Hz, 0, -1, nan, inf, float and string clocks, omitted key, duplicate override, `--no-milan`, disabled domain, implicit sys, `flashboot: none`, missing or empty or absolute or wrong-board SWEEP_CFG, other working directory, clock-named environment variables, PYTHONPATH shadow (SG1): receipts 31, 32, 33, 34 | R355-1 | 3baff4411fd70aaccb066662628ff0b0a7d7c05d |
| Tests | UNCLEAN (F1, F2, F3) | `test_clock_contract.py` (whole file), `test_builder.py:2990-3006,17080-17155,25088-25140,27555-27567`, `test_pp_mem_bridge.py:383-520,928-934`, `scripts/ci_scope.py:1-80,280-330`; receipts 30, 36, 50, 42, 10 | R355-1 | 3baff4411fd70aaccb066662628ff0b0a7d7c05d |
| Docs | UNCLEAN (F1, F4, F5) | `BAREMETAL_FIRMWARE.md:19-70,1985-2020`, `AAF_LATENCY_TAPS.md:1-48,125-175`, `LATENCY_HISTORY_RING.md:92-104`, `CI_WORKFLOWS.md:50-92`, `README-parameters.md:47-60`, `ENDSTATION_BUILDER.md:967,1014`, `milan_soc.py:1-21,3382-3393`; receipts 40, 41, 31 | R355-1 | 3baff4411fd70aaccb066662628ff0b0a7d7c05d |

## Prior public review findings on this PR

I read these only after the verdict and ledger above were written. When this round started, no findings existed. Two items were published during the round. I resolve or retain each one at this head as follows.

- **Manager bank comment 5857952562: builder bank 47/48, gate 6 `ci_scope.py --selftest`.**
  - I had already derived the same failure on my own, from the exact-head hosted logs and local head and base runs (receipts 50).
  - It is **retained** as my F1, because a bank note is not a lens finding and the ledger must carry it.
  - F1 adds the CI_WORKFLOWS.md reader-table part.
  - The assignment brief said the source builder bank passed at this head. That comment corrects it to 47/48.
- **Internal round R354-1, NEGATIVE, comment 5858016029.**
  - **F1 BLOCKER** (gate-read page not registered): **retained**. It is the same defect as my F1, with the same lens attribution: Tests and Docs.
  - **F2 MINOR** (the configured clock no longer proven to reach the gPTP ROM): **retained**. It is the same defect as my F3, where my probe uses a different mutant (`sys_clk_hz` forwarded, 7 of 1024 words differ).
  - **S2 SUGGESTION** (the `milan_soc.py` usage block): **retained at a higher severity** as my F5, MINOR, Docs.
    - I checked that the documented usages reach the platform at the base and exit 2 at the head (`31_soc_behaviour_*.log`).
    - The Docs lens requires changed contracts to be reflected, and the tool's own usage block and `--milan-clk-freq` help now document refused commands. That is why I rate it MINOR.
    - Their note about `--entity-gen-dir` concerns later, unchanged steps. It is not re-examined here.
  - **S1 SUGGESTION** (raw-YAML clock reads raise `KeyError` on a configuration that omits the optional `sys_clk_hz`): **retained as a suggestion**. I did not reproduce it on my own, and it fails loudly, not wrongly.
  - **S3 SUGGESTION** (remaining restatements): **retained**. It agrees with my SG3, including `tb/verilator/milan_dp/Makefile:413` as the one mirror that is not cross-checked.
  - My F2 (surviving guard-narrowing mutants), F4 (the README-parameters product-profile table) and SG1, SG2 and SG4 are **additional to R354-1**.

At this head, no prior finding is resolved: every prior item above is retained.

## Limits

- **Clean-clone runs.** The focused gates, documentation gates, static checks, `ci_scope.py` and `check_nvm_capture.py` ran on the review clone. Every mutation, the builder CLI and SoC behaviour probes, and the base comparisons ran on disposable exports under `scratch/`, each with private copies of the submodule git metadata.
- **Banks not run.** I did not run the full builder bank (either compiler mode), the parent, PP, gPTP or Yosys banks, `act`, or any hardware step, as the assignment requires.
- **F3 replay.** F3's survival is shown by replaying the head's ROM assertions under the mutant. The full `test_baremetal_profile_contract` exceeds the 600 s per-command ceiling. One attempt was cut off; its copy was restored and verified by blob hash, and nothing from it is used.
- **Scoped Verilator.** It was not used, because no RTL, HDL or bench changed. Its identity was therefore not checked.
- **Hosted evidence.** It was inspected read-only. `docs-check` was in progress at first inspection and had succeeded by the final inspection (`51_hosted_checks_final.txt`). `docs-check-no-git`, `bdd-conformance` and `wire-accountability` had also succeeded. Skipped contexts (`verilator-lint`, `yosys-elaboration`, shard matrices, physical gPTP) are not evidence either way.
- **Hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Clone restore.**
  - Byproducts of the gate runs were removed from the clone: ignored `__pycache__/` directories and `sw/builder/out/`, all created during this round.
  - Final state (`05_clone_identity_final.txt`):
    - head, tree and index tree equal `3baff441`/`ce000a55`;
    - the `ls-files -s` digest is unchanged;
    - the four gitlinks are unchanged, and the three checked-out submodules sit at their gitlinks, clean;
    - `git status --ignored` is empty.
- **Redaction.** One receipt had its home-directory path redacted to `$HOME`.

## Pending manager duties

- Hosted and `act` acceptance on the next head. The current exact-head `rtl-fast` is red because of F1.
- The final current-dev candidate build: source base 9e9954e9, live dev 2a2a7bb6.
- The internal review verdict and ledger.
- Filing any follow-up Issue the maintainers want for SG3 (`milan_dp/Makefile` `AX_GPTP_HZ`).
- Re-review of the corrected head, covering Tests and Docs, plus any lens whose scope the fix touches.

R355-1 FINISHED
