[R354] NEGATIVE - exact head 3baff4411fd70aaccb066662628ff0b0a7d7c05d

# R354-1: internal independent review of PR #596 (issue #582)

- Role: internal independent reviewer, cleared context, own detached clone.
- Head under review: `3baff4411fd70aaccb066662628ff0b0a7d7c05d`, tree `ce000a55f0ce2cfdb6e63959bf70a4f579426a77`.
- Source base: `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5`. One commit.
- Diff: `docs/AAF_LATENCY_TAPS.md`, `docs/integration/BAREMETAL_FIRMWARE.md`, `sw/builder/endstation_builder.py`, `sw/builder/test_builder.py`, new `sw/builder/test_clock_contract.py`, `sw/litex/milan_soc.py`, `sw/litex/sweep_extra.sh`, `sw/litex/test_pp_mem_bridge.py`.
- No change under `hdl/`, `tb/`, `sw/firmware/`, `configs/`, or to any gitlink.
- Scope was reconstructed from:
  - AGENTS.md, CONTRIBUTING.md and docs/README;
  - the issue #582 body (acceptance 1-4);
  - the scope comments on #582: the dated-history note 5853404680, the scala_args note 5855343934 and the assignment 5857543940;
  - BAREMETAL_FIRMWARE.md build contract, CI_WORKFLOWS.md, the diff, and public evidence.
- Lenses applied this round: Conformance, RTL, Robustness, Tests, Docs.

The implementation itself is sound:
- both refusals hold against every bypass I tried;
- 20 of the 20 kill-mutants aimed at the new checks die;
- the five configurations are byte-identical to the base;
- the capture receipt is unchanged.

The verdict is NEGATIVE for two reasons:
- **F1:** the new test makes a docs page gate-read without registering it. That fails the change classifier's selftest, and the selftest makes every required hosted context at this exact head red, `rtl-fast` included.
- **F2:** converting the 80 MHz ROM variant into a refusal removed the only check that the configured clock reaches the gPTP ROM generator.

## Findings

### F1 - BLOCKER - Tests, Docs - `sw/builder/test_clock_contract.py:155` + `scripts/ci_scope.py:54-58` + `docs/testing/CI_WORKFLOWS.md:68-70` - new gate-read page not registered with the change classifier

- **Authority and evidence:**
  - `CI_WORKFLOWS.md:61-66` says `scripts/ci_scope.py --selftest` derives the gate-read page list from gated code under `tests/ tb/ syn/ sw/ hdl/ avdecc/`. It refuses a `GATE_READ_DOCS` table that differs.
  - `test_clock_contract.py` sits under `sw/` and is not in `DOCS_JOB_PY`. It reads `docs/AAF_LATENCY_TAPS.md` (line 155), but `GATE_READ_DOCS` was not changed.
  - Reproduced locally at the head: `python3 scripts/ci_scope.py --selftest` gives rc 1, `FAIL gate-read page docs/AAF_LATENCY_TAPS.md (named at sw/builder/test_clock_contract.py:155) is relevant`.
  - The same command on the source base extraction passes (`receipts/ci_scope_selftest_head.log`, `receipts/ci_scope_selftest_base_vs_head.log`).
  - Hosted at the exact head, the classify step fails with that same line (`receipts/hosted_exact_head.log`):
    - `rtl-fast` run 36334607821;
    - `elaborate` run 36334607811;
    - `rtl-full`/`full-ci-gate` run 36334607868.
  - As a result, `changes`, `rtl-fast`, `elaborate`, `full-ci-gate`, `verilator-suites` and `yosys-portability` are all `fail`. Only `docs` passed.
  - The CI_WORKFLOWS.md reader table still says `test_builder.py` reads "six pages under `docs/`". Through its new import of `test_tap_clock_docs` it now reads one more.
- **Impact:**
  - AGENTS section 7 requires a successful `rtl-fast` at the current head. This head cannot get one, and no exhaustive gate runs on it.
  - The PR and handoff report "all assigned gates rc 0", but this repository selftest fails.
  - A docs-only edit to the tap table is today checked only because `docs-check` runs `test_builder.py`. That dependency is not recorded where the policy says readers must be recorded.
- **Required outcome:**
  - `scripts/ci_scope.py --selftest` passes at the new head, with the page's classification decided and recorded.
  - Either the page is registered as gate-read, or the reader is placed where the classifier's contract admits it.
  - The CI_WORKFLOWS.md reader table states the new page read truthfully.
- **Verification:** `python3 scripts/ci_scope.py --selftest` rc 0 locally. The hosted classify step passes, and `rtl-fast`, `elaborate` and `full-ci-gate` reach real verdicts on the corrected head.

### F2 - MINOR - Tests - `sw/builder/test_builder.py:17106-17124` (removed "fabric clock" variant) vs `sw/builder/endstation_builder.py:5699-5703` - configured clock no longer proven to reach the gPTP ROM

- **Authority and evidence:**
  - At the base, gate 1b asserted that the gPTP ROM changes with each of its three YAML-owned inputs: station MAC, priority1 and fabric clock (80 MHz variant).
  - The PR removed the clock variant because it is now refused, and added no replacement.
  - The generator's own default is `--clk-hz 100_000_000` (`gptp-processor/hdl/ucode/gen_gptp_ucode.py:2110`), which is not the 50 MHz contract.
  - Mutant: delete `"--clk-hz", str(cfg["constraints"]["milan_clk_hz"])` from the builder.
    - The shipping-AX ROM changes from `78c8418a…` (the value the capture receipt records) to `21e846a7…`.
    - The mutant SURVIVES a replica of every gate-1b ROM assertion at the head (M21).
    - It survives `test_clock_contract.py` (M21b).
    - It survives `scripts/check_nvm_capture.py` (M21c).
  - The same mutant applied to the base builder is KILLED by the removed variant: the 80 MHz ROM equals the base ROM (`receipts/base_variant_kill.log`).
  - Test grep: the only readers of `gptp_ucode` in the builder tests are gate 1b and an existence assert at `test_builder.py:17202`.
- **Impact:** if the clock stops being forwarded, the product ROM silently gets servo gains for 100 MHz on a 50 MHz plane, and every gate stays green. The acceptance-1 reconciliation turned a detecting test into a refusal test without keeping the property the old test guarded.
- **Required outcome:** an executable check that the configured Milan clock reaches the ROM generator, which fails when `--clk-hz` is dropped or mis-wired, at the contract clock.
- **Verification:** `scripts/mutants.py <repo> <python> M21-rom-clock-not-forwarded` (with the new check as its test) reports KILLED.

### S1 - SUGGESTION - Robustness, Tests - `sw/litex/test_pp_mem_bridge.py:386-394`, `sw/builder/test_clock_contract.py:45,117-122,159` - raw-YAML clock reads

- The builder treats `board.constraints.sys_clk_hz` as optional, defaulting it from the board (`endstation_builder.py:3794`).
- A valid configuration without it builds (100 MHz on ax7101), and `sweep_extra.sh` derives it through `load_config`.
- `configured_clock_pairs()` raises `KeyError: 'sys_clk_hz'` on it (`receipts/bypass_probe.log`), and so would `_assert_sweep_clocks`. This fails loudly, not wrongly, so it is optional.
- Reading the normalised configuration would make the derivation match the builder's.

### S2 - SUGGESTION - Docs - `sw/litex/milan_soc.py:7-14` - usage block

- Every usage example in the module header now exits 2 with the new `baremetal clock` refusal (`receipts/probe_soc_header_examples.log`), because the SoC defaults are `--sys-clk-freq 100e6` and no Milan clock.
- These examples were already partly stale: Milan-datapath elaborations need `--entity-gen-dir` (`milan_soc.py:3293-3296`).
- Optional refresh.

### S3 - SUGGESTION - Conformance, Docs - remaining restatements outside the named consumers

The literal survey covered `sw/ tb/ docs/ scripts/ configs/`. The named consumers (builder refusal, SoC refusal, capture recipe, BAREMETAL_FIRMWARE.md build contract) now derive from `recipe.CPU_HZ`. What remains falls into five groups:

1. Checked declarations: the five configs' `milan_clk_hz`, held to equality by the builder.
2. Generated or byte-gated copies: `sweep.sh:47-48` and `configs/generated/sweep_opts_*.sh`, gate 9 and `check_sweep_shape.py`.
3. Dated measurement records, correctly labelled:
   - `AAF_LATENCY_TAPS.md:141-146` (100 MHz);
   - `BAREMETAL_FIRMWARE.md:1986-1994`;
   - `measurements.json`.
4. Simulation model parameters that hand-copy the AX 1x1 configured clock: `tb/verilator/milan_dp/Makefile:413` `AX_GPTP_HZ = 50000000` and `sim_ax1x1gptp.cpp:57`. These are outside #582's named scope. A follow-up Issue could derive them.
5. Present-tense prose: `BAREMETAL_FIRMWARE.md:2017` "run at 50 MHz" (rationale) and the `test_builder.py:17100` print text.

None of these contradicts the one-source decision for the named consumers.

## Acceptance and focus items

1. **Refusals.** Both tools refuse a divergent bare-metal clock with a named error that cites the build contract.
   - Builder: `endstation_builder.py:4296-4299` raises `ConfigError("baremetal clock: … (docs/integration/BAREMETAL_FIRMWARE.md build contract)")` inside `load_config`, before any artifact. The test asserts that no output is written.
   - SoC: `milan_soc.py:3693-3696` calls `ap.error` (rc 2) before the platform is built.
   - The SoC effective-clock expression `milan_clk_freq or sys_clk_freq` matches `_CRG` (`:242`), the CPU binding `with_cpu_clk = bool(milan_clk_freq)` (`:2569`), `milan_cd` (`:2766`), the datapath `MILAN_CLK_FREQ_HZ` (`:2949`) and the watchdog (`:3009-3010`).
   - These paths were probed, beyond the PR's own table, and none bypasses the refusal (`receipts/bypass_probe.log`):
     - SoC: `=` form, repeated options (last wins), build.sh EXTRA appended after the shipping argv, a disabled domain at 100 MHz, `-0`, `--no-milan` at 100 MHz and sub-hertz values;
     - builder: string, float, bool and int-normalised values.
   - Neither tool reads the environment (0 `environ`/`getenv` hits) and the builder CLI has no clock override.
   - The one-source import is `tb.verilator.nvm_capture_cpu.recipe.CPU_HZ`, imported by both tools. The recipe is unchanged because the receipt hashes it: `measurements.json` `harness_sha256["recipe.py"]` still matches, and `check_nvm_capture.py` rc 0.
2. **80 MHz variant and scala_args.**
   - The 80 MHz variant is now refused for every configuration (`test_clock_contract.py:49`).
   - The scala_args message "no scala_args overrides" matches the non-empty check at `:4302`. A non-cache override is refused (`:59-61`).
   - The replacement lost ROM-clock coverage (F2).
3. **Clock pairs.**
   - `test_pp_mem_bridge.py` precedence uses the configured pairs: all five, with arty at 83.333/50 and AX at 100/50. The two historical AX pairs are kept as labelled stress controls.
   - `sweep_extra.sh` derives clocks through `load_config`:
     - defaults are arty `endstation_arty_4x4` and ax7101 `endstation_ax7101_1x1_tdm8`;
     - `SWEEP_CFG` overrides;
     - a board mismatch, a missing configuration and an invalid clock all fail, verified by the PR's tests and my M12-M15 kills.
   - The Arty configurations build (#583): 58 of 58 generated files are identical.
4. **AAF_LATENCY_TAPS.md.**
   - The present-tense line uses `milan_clk_hz`, backed by a per-configuration table checked by `test_tap_clock_docs`. The 8x8 row is correctly `pruned`.
   - The 2026-07-26 section is labelled historical and "**100 MHz** (10 ns/cycle)". Its values are unchanged; the diff only adds two lines.
   - The tap-tool audit holds:
     - `sw/trace/milan_trace.yaml:444-446` keeps `min/last/max_cyc` in cycles;
     - no firmware or script tap reader exists;
     - `KL_lat_history_ring` takes `latency_ns` as an input and has no instantiated adapter.
5. **BAREMETAL_FIRMWARE.md.** The page states that both tools enforce the clock (`:38-49`), and the "not checked by either tool" text is gone (0 hits).
6. **Artifact identity.** The five configurations are byte-identical between base and head across 58 generated files, 5 gPTP ROMs included (`receipts/artifact_identity.log`). The capture receipt is unchanged. There is no firmware, RTL, configuration or gitlink change.

## Kill-tests (my own mutants, `scripts/mutants.py`, `receipts/mutants.log`, `receipts/mutants_m21c.log`)

20 of 20 mutants aimed at the new checks are KILLED:

- **Builder guard:** removed, ceiling-only, floor-only, and unnamed message.
- **Scala message:** narrowed.
- **SoC guard:** removed, ignoring the system-clock fallback, ceiling-only, and system-only.
- **SoC message:** unnamed.
- **Recipe clock:** changed to 100 MHz. This flows to both tools and refuses every configuration.
- **Sweep:** hard-coded pair, swallowed configuration failure, board check removed, `SWEEP_CFG` ignored.
- **Clock pairs:** swapped, truncated, and copied.
- **Tap table:** the old 10 ns value, and an unpruned 8x8.

3 of 3 variants of the ROM-clock mutant SURVIVE (F2).

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #582 acceptance 1-4 and comments 5853404680, 5855343934, 5857543940; `endstation_builder.py:66-71,4296-4303`; `milan_soc.py:59-64,3686-3696`; `test_builder.py:17106-17124`; `receipts/bypass_probe.log`, `artifact_identity.log`, `baseline_check_nvm_capture.log`; literal survey (S3) | R354-1 | 3baff4411fd70aaccb066662628ff0b0a7d7c05d |
| RTL | CLEAN | Diff empty for `hdl/ tb/ sw/firmware/ configs/` and gitlinks (`receipts/restore_verification.log`); SoC clock-domain consequences at `milan_soc.py:242,2569,2766,2949,3009-3010` against the guard at `:3693`; the disabled-domain and `--no-milan` probes | R354-1 | 3baff4411fd70aaccb066662628ff0b0a7d7c05d |
| Robustness | CLEAN (S1 optional) | `sweep_extra.sh` (whole file); `receipts/bypass_probe.log`; mutants M12-M15; the omitted-`sys_clk_hz` probe; SoC and builder value forms | R354-1 | 3baff4411fd70aaccb066662628ff0b0a7d7c05d |
| Tests | UNCLEAN (F1 BLOCKER, F2 MINOR) | `test_clock_contract.py` (whole file); `test_pp_mem_bridge.py:383-418,484,928-934`; `test_builder.py:17106-17124,27555-27566`; `scripts/ci_scope.py:48-72,309-320`; `receipts/mutants.log`, `mutants_m21c.log`, `base_variant_kill.log`, `ci_scope_selftest_*.log`, `baseline_*.log`, `hosted_exact_head.log` | R354-1 | 3baff4411fd70aaccb066662628ff0b0a7d7c05d |
| Docs | UNCLEAN (F1 BLOCKER) | `BAREMETAL_FIRMWARE.md:19-68,1984-2019`; `AAF_LATENCY_TAPS.md:11-31,139-146`; `CI_WORKFLOWS.md:55-85`; `milan_soc.py:1-21`; `receipts/focused_static.log`, `focused_static_md.log` (doc style, doc paths, em-dash vs base, TOC check, anchors, docs_check, py/sh idiom, bare-metal-only, solution docs, hygiene, `git diff --check` base..head: all rc 0) | R354-1 | 3baff4411fd70aaccb066662628ff0b0a7d7c05d |

## Prior public review findings

I checked after the verdict and ledger above were written. PR #596 has no reviews, no review comments and no prior findings, so nothing needs resolving or retaining.

- The other reviewer's round had not published when I checked.
- One manager evidence comment exists: 5857952562, "Manager bank r1 at `3baff441`: builder 47/48". It reports the same `ci_scope.py --selftest` failure as a known bank result.
  - That comment is not a review finding.
  - I derived F1 on my own from the exact-head hosted logs and a local rerun before reading it.
  - F1 stays as a reviewer finding so the lens ledger carries it. It adds the stale CI_WORKFLOWS.md reader-table part.
  - The assignment brief said the source builder bank passed at this head. That comment corrects it to 47/48.

## Real limits

- **Not run:** the full builder, parent, PP, gPTP, Yosys and native banks, as assigned.
  - Gate 1b was run once as a single function at the head, rc 0 (`receipts/baseline_gate1b.log`).
  - The F2 replica reproduces only gate 1b's ROM assertions.
- **Verilator not used.** The scoped Verilator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. No RTL changed, so no Verilator run was needed.
- **Host environment.**
  - LiteX-dependent probes used the host LiteX environment.
  - The Markdown-renderer gates used the existing pinned docs environment; nothing was installed.
  - `shellcheck` is unavailable, and `check_sh_idiom.py` passed.
- **Not proven here.** Physical calibration was NOT RUN. No hardware or timing-closure claim is made, and field skips are not hardware proof.
- **Hosted evidence.** It was inspected read-only. The `docs` workflow succeeded, and the classifier-gated workflows failed at classification (F1), so no Verilator or Yosys shard ran.
- **Artifact comparison setup.** Base and head were extracted with `git archive` plus identical submodule contents. Fragments were regenerated in the same per-board order in both trees.

## Pending manager duties

- Hosted and local-replica acceptance at the corrected head, once F1 is fixed.
- The final current-dev candidate build: source base 9e9954e9, live dev 2a2a7bb6.
- Re-review of the F1 and F2 fixes at the new head, with every lens re-covered where the fix touches its scope.

R354-1 FINISHED
