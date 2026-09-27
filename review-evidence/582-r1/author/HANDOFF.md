# [A370] Issue #582 handoff

Status: local implementation and assigned validation complete; ready for independent review; no review verdict.
Branch: `582-baremetal-clock`
Base: `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5`
Assignment: https://github.com/kebag-logic/milan-fpga/issues/582#issuecomment-5857543940
Roles: author [A370], internal reviewer [R354], external reviewer [R355].

## Scope and stop condition

Enforce the shared bare-metal clock in both entry points, derive clock tests and sweep inputs from tracked configurations, correct current tap timing while preserving dated measurements, and align the scala_args refusal. No firmware, RTL, submodule, or tracked configuration edits are planned. Stop if a tracked configuration would be refused. All five tracked configurations build successfully and retain their generated artifact identities. The STOP condition was not triggered.

## Change list

- `sw/builder/endstation_builder.py:71`: import the recipe's existing `CPU_HZ` as the single contract clock.
- `sw/builder/endstation_builder.py:4296`: reject divergent bare-metal clocks by name before artifact writes; `:4303` states that every Scala override is refused.
- `sw/litex/milan_soc.py:64` and `:3693`: import the same constant and check the effective CLI clock before platform construction, including the system-clock fallback.
- `sw/builder/test_builder.py:17120` and `:27558`: retire the accepted 80 MHz ROM variant and run the clock/refusal, sweep, and documentation controls in the full bank.
- `sw/builder/test_clock_contract.py:36`: tracked positives and 25 owning clock refusals, plus system ordering and non-cache Scala refusals, with no output on failure.
- `sw/builder/test_clock_contract.py:85`: actual SoC CLI checks under a pre-platform sentinel; `:125` checks the real extra-sweep preview; `:153` derives documentation rows from configurations.
- `sw/litex/test_pp_mem_bridge.py:386`: read all configured clock pairs; `:397` proves pair/domain preservation with independent fixture clocks; `:415` labels historical pairs; `:487` runs precedence over configured and historical pairs.
- `sw/litex/sweep_extra.sh:9` and `:32`: load configuration-owned clocks, refuse a mismatched board or invalid/missing configuration, and expose a preview that launches nothing.
- `docs/integration/BAREMETAL_FIRMWARE.md:43`: document enforcement and the single clock authority.
- `docs/AAF_LATENCY_TAPS.md:14` and `:141`: checked per-shape conversion table and explicit historical measurement provenance.

The recipe remains byte-identical: the capture receipt hashes it. Using its existing constant as authority avoids changing measurement provenance. This decision is public in the takeover comment: https://github.com/kebag-logic/milan-fpga/issues/582#issuecomment-5857569754

## Refusal, test, and mutant table

| Refusal or behavior | Test | Mutant | Result |
|---|---|---|---|
| Bare-metal 100/80 MHz and adjacent clocks | `test_baremetal_clock_contract` | Delete builder guard | Killed, rc 1: accepted invalid clock |
| Slower clocks also violate equality | `test_baremetal_clock_contract` | Replace equality by ceiling | Killed, rc 1: accepted invalid clock |
| All Scala overrides refused | `test_baremetal_clock_contract` | Restore cache/prefetch-only message | Killed, rc 1: wrong owning diagnostic |
| SoC clock refusal before platform | `test_soc_clock_contract` | Delete SoC guard | Killed, rc 1: clock accepted before platform |
| SoC slower adjacent clock | `test_soc_clock_contract` | Replace equality by ceiling | Killed, rc 1: clock accepted before platform |
| Implicit system-clock fallback | `test_soc_clock_contract` | Substitute contract constant for fallback | Killed, rc 1: clock accepted before platform |
| Extra sweep Milan clock follows config | `test_extra_sweep_clocks` | Restore 100 MHz literal | Killed, rc 1: argv clock mismatch |
| Extra sweep system clock follows config | `test_extra_sweep_clocks` | Copy 100 MHz literal | Killed, rc 1: argv clock mismatch |
| Precedence pair preserves domains | `test_configured_clock_pairs` | Swap sys/Milan fields | Killed, rc 1: fixture mismatch |
| Precedence pair follows declarations | `test_configured_clock_pairs` | Copy Milan clock literal | Killed, rc 1: fixture mismatch |
| Current tap conversion follows shape | `test_tap_clock_docs` | Restore 10 ns/cycle on AX 1x1 | Killed, rc 1: documentation table mismatch |

The campaign itself returned rc 0. `mutations.py` restores each source in `finally`, uses isolated bytecode caches, and requires each negative result to contain its owning diagnostic. No firmware, RTL, configuration, or submodule source is mutated by this campaign. The restored focused suite passed. `mutations.log` records every result.

Positive controls cover all five tracked configurations, the SoC's explicit and implicit contract clocks, zero disabling the separate domain, both sweep defaults, all five shape overrides, and a changed system clock with a spaced configuration path. Negative controls also cover NaN/infinity, clock ordering, board mismatch and missing configuration. Historical watchdog clock pairs remain labelled non-product stress controls.

## Five-configuration SHA-256 identity

All five configurations build, and every named generated artifact matches the base byte-for-byte. No tracked generated file or configuration changed. The STOP condition was not triggered.

The digest is SHA-256 over compact sorted JSON mapping each builder artifact role to SHA-256 of its file bytes. Per-artifact hashes are in `baseline-sha256.json` and `final-sha256.json`; `identity.py` reproduces the comparison from the worktree. There are 61 named artifact entries across the five shapes.

| Configuration | Entries | Base and final SHA-256 | Comparison |
|---|---:|---|---|
| `endstation_arty_4x4` | 12 | `f1a8ba03c1e639a0e6628d664efadc5d71f5ea45e7aa5398d44c93a8cf92b3f0` | identical |
| `endstation_arty_8ch` | 12 | `e31a65d95263cc96f308d9b29d83e53c0425a25a110728120741fe41e671f7fc` | identical |
| `endstation_arty_current` | 13 | `12f3fcedf8b24a32862d00e4a42e2107b8ad2b115606fcbfcf74c77a59b0427f` | identical |
| `endstation_ax7101_1x1_tdm8` | 12 | `deeee0e1261257049a0e4b69349d86c6f6ff52cc63c097f9f77d388b4b1050c4` | identical |
| `endstation_ax7101_8x8` | 12 | `6f8ce8711b3d995df08874ede226159efb4cd566cd7d47002896d1eb881e7732` | identical |

## Gate table

All commands use physical worktree `$LANES/582-baremetal-clock` as their working directory and run in the foreground, without pipelines. Logs and generated builds are outside this output directory until bounded evidence logs are copied here. The existing SoC environment supplies hardware-description dependencies; documentation checks use `/tmp/582-a370-docs`, with `tools/markdown/requirements.txt` installed using `--require-hashes` and PyYAML installed there. No environment or installed package is stored in this output directory.

The compiler-absent wrapper runs the same complete bank and hides exactly the three RV32 census selectors. Host probes remain real; compiler-dependent stand-downs are explicitly recorded. The RV32-required run covers those instruments. The existing gate 11 placed-resource calibration cannot run without its historical hardware report; this assignment authorizes no hardware work, and the bank records that arm as NOT RUN while returning rc 0.

| Gate | Command | Return code | Evidence |
|---|---|---|---|
| Builder, RV32 required | `timeout 7200 $WORKSPACE_HOME/litex-milan/venv/bin/python3 sw/builder/test_builder.py --require-rv32` | 0 | Full bank passed; existing gate 11 hardware-report calibration NOT RUN (report absent) |
| Builder, compiler absent | `timeout 7200 $WORKSPACE_HOME/litex-milan/venv/bin/python3 -u builder-absent.py` from the worktree | 0 | Full bank passed; gate 1b intentional compiler stand-down and gate 11 absent hardware report are NOT RUN |
| Declarations | `python3 sw/builder/test_declarations.py` | 0 | 26 refusal arms; 3 header mutations per configuration; 9 binding/reset mutations |
| Capture | `python3 scripts/check_nvm_capture.py` | 0 | Census, clocks, both timing arms and receipt agree; 7 negative controls detected |
| Memory bridge | `timeout 600 $WORKSPACE_HOME/litex-milan/venv/bin/python3 sw/litex/test_pp_mem_bridge.py` | 0 | 113/113 checks plus SoC clock controls |
| Documentation | See `docs-gates.py` and `docs-results.json` | 0 | 31 commands passed; added-line check repeated on final head: 40 added lines, 2 pages, 339/339 arms |
| Diff whitespace | `git diff --check` and `git diff --check 9e9954e96bf55181edb9949ae94c9abd4ab6aaf5 HEAD` | 0 | Clean |
| Focused contract | `timeout 300 $WORKSPACE_HOME/litex-milan/venv/bin/python3 sw/builder/test_clock_contract.py --soc` | 0 | `clock-contract.log` |
| Mutation campaign | `timeout 1800 $WORKSPACE_HOME/litex-milan/venv/bin/python3 -u mutations.py` from the worktree | 0 | 11/11 killed; `mutations.log` |
| Artifact identity | `timeout 300 python3 identity.py` from the worktree | 0 | 61 named entries identical; `identity.log` |

## Tap conversion audit

`git grep -n -i -E '(ltap|latency.tap|tap.cycles|ns.per.cycle)'` over tracked Python, shell, C and C++ sources found no tap-cycle-to-time conversion tool. `sw/trace/milan_trace.yaml:437` declares `min_cyc`, `last_cyc` and `max_cyc`; `sw/trace/ctf_read.py` reads those fields without conversion. The `NS_PER_CYCLE` in the NVM host test models a different clock and is outside tap conversion. Firmware and RTL were not edited.

## Final state

Head: `3baff4411fd70aaccb066662628ff0b0a7d7c05d`.
Commit subject: `Enforce the bare-metal clock contract and derive configured clock pairs`.
The commit has no body or trailers. The worktree is clean, with no changes to configurations, generated files, firmware, RTL, submodule pins or the capture recipe/receipt.
Public review-ready evidence: `REVIEW-READY.md`. The final posting command records its URL in `review-ready-url.txt`.
No push, pull request, merge, hardware operation, or review was performed. Assigned independent reviewers retain responsibility for the review verdicts. Final action: append the prepared review-ready comment and stop.
