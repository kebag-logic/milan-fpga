# Issue 502 handoff

[A338] Local implementation committed. All requested gate commands returned exit 0.

Head: `87e263fd1d71b1a7a04a2e9c9339220f35e4348f`.
Base: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.
Branch: `502-pending-live-write`.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/502#issuecomment-5846418959
Takeover: https://github.com/kebag-logic/milan-fpga/issues/502#issuecomment-5846425135
Executor: [A338]. Reviewers: [R328] internal, [R329] external.

## Scope and acceptance

| Assignment item | Result | Evidence |
|---|---|---|
| 1. Pin and generated adoption artifacts | Complete | Processor 870ff88a; regenerated ROM ledger, diagram, pin documentation and changelog |
| 2. Live-write pending and real K10/K12 | Complete | Accepting pulse reaches the backend beside sticky history; clean real-command tests pass |
| 2. Controls and late-mark mutant | Complete | Name unchanged, map zero-record/duplicate/static refusal, reset and capture ACK; mutant fails K10 and K12 |
| 3. Permanent consumer adaptation | Complete | Named aecp_name_wr_o connection; processor mutation reader disposition retained |
| 4. Capture and area | Complete | Firmware unchanged; capture gate passes; same-pin OOC delta below |

The original K10/K12 evidence was read from `a21b165a`,
under `design-evidence/500-materialization`, in read-only temporary files.
The new harness uses the real processor and shipping parent map owners.
It does not reuse the design evidence's modeled command timing.

## Changes

| File:line | Change |
|---|---|
| `protocol-processor (gitlink)` | Adopt 870ff88a, including the accepted name-write export. |
| `hdl/milan/KL_pp_shadow.sv:921` | Clock/reset contract; accepted pulses plus sticky history drive pending. |
| `hdl/milan/KL_pp_shadow.sv:1080` | Connect aecp_name_wr_o; retain the later command marks. |
| `tb/verilator/pp_shadow/sim_main.cpp:266` | Read-only observer samples every accepting edge and published status. |
| `tb/verilator/pp_shadow/sim_main.cpp:1249` | Independent image and control-face baseline; real name and map commands. |
| `tb/verilator/pp_shadow/sim_main.cpp:1385` | K10/K12, unchanged/refused/repeat/reset controls and accepted capture ACK. |
| `tb/verilator/pp_shadow/pending_probes.vlt:4` | Expose only read-only acceptance/status probes. |
| `tb/verilator/pp_shadow/fixtures/pending.yaml:3` | Validated fixture with dynamic output mapping. |
| `tb/verilator/pp_shadow/Makefile:163` | Default dynamic-output leg and explicit pending-mutant target. |
| `tb/verilator/pp_shadow/pending_mutant.py:35` | Clean control and isolated late-mark mutant; both named failures required. |
| `tb/verilator/pp_shadow/README.md:50` | Reproduction, oracle, controls and measurement limits. |
| `scripts/measure_test_evidence.py:596` | Keep the processor name-write mutant disposition; classify the parent mutant. |
| `syn/yosys/rom_digests.tsv:25` | Repository-generated ledger entries keyed by the adopted pin. |
| `docs/reference/SUBMODULES.md:25` | Pin and exported-event integration notes. |
| `docs/diagrams/submodule_boundaries.svg:1` | Regenerated pin diagram. |
| `docs/diagrams/submodule_boundaries.drawio:1` | Regenerated editable pin diagram. |
| `docs/diagrams/submodule_boundaries.png (binary)` | Regenerated rendered pin diagram. |
| `docs/diagrams/PNG_MANIFEST.json:1` | Regenerated diagram digest metadata. |
| `docs/design/SAVED_STATE_MATERIALIZATION.md:221` | Distinguish the standalone reporting fix from proposed D3 materialization. |
| `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:954` | Pending edge, source, clear and conservative duplicate-map rules. |
| `CHANGELOG.md:34` | Pin and live-write pending correction. |

## Behavioral evidence

| Case | First live-write cycle | Later group-mark cycle | Clean result | Late-mark mutant |
|---|---:|---:|---|---|
| K10, eight changed name lanes | 12965 | 14846 | Zero durable cycles after acceptance | 1881 falsely durable cycles |
| K12, input map | 12558 | 12573 | Zero durable cycles after acceptance | 15 falsely durable cycles |
| K12, output map | 12559 | 12574 | Zero durable cycles after acceptance | 15 falsely durable cycles |

The counters restart at each armed case, not at power-on.
Evidence: `pp-shadow.log`, `pending-mutant-verified.log`.
The default shadow suite passes 520 + 520 + 520 + 159 checks.
The mutation control passes 159 checks; the mutant's named failures are required.
GET_NAME and GET_AUDIO_MAP confirm values through the real command path.
The control-face baseline is explicitly asserted durable before each case.
ARM, ATTEST and ACK must be accepted, and pending must survive that ACK.
Reset/load must return both pending publications to zero.

The backend samples the pulse on the same clock edge as the live write.
Only its sticky history would add an incorrect one-cycle delay.
The map face holds phase 5 across two cycles; the parent accepts once.
Duplicate records conservatively raise pending even without another mark.
Marks remain command-completion events, and are not record-write events.

No name or map record materializer is introduced.
The harness models descriptor/response memory and the control-face writer.
It does not prove flash persistence or boot restoration for these groups.
Pending remains sticky until reset, including after snapshot acknowledgement.

## Area and capture

Recipe: `syn/yosys/ooc.sh KL_pp_shadow`.
Both measurements use processor `870ff88a`, wrapper defaults and the same tools.
The baseline uses the unchanged base shadow with the adopted processor pin.
This isolates the parent glue delta; it is not an old-pin/new-pin comparison.
`area.json` records the before/after source hashes.
`versions.json` records the tool versions.

| Resource | Before | After | Delta |
|---|---:|---:|---:|
| LUT | 60855 | 60766 | -89 |
| LUTRAM | 6136 | 6136 | 0 |
| LUT total | 66991 | 66902 | -89 |
| FF | 30187 | 30187 | 0 |
| RAMB36 | 15 | 15 | 0 |
| RAMB18 | 4 | 4 | 0 |
| DSP | 6 | 6 | 0 |
| CARRY4 | 2104 | 2104 | 0 |

This is synthesis area, not placed timing or a hardware result.
The firmware source and generated firmware contract are unchanged.
`check_nvm_capture.py` passes; no new capture measurement is required.

## Completed default sweep

| Chunk | Suites | Checks | Exit |
|---|---:|---:|---:|
| 0/6 | 16 | 227846 | 0 |
| 1/6 | 5 | 212684 | 0 |
| 2/6 | 13 | 2756 | 0 |
| 3/6 | 6 | 1652280 | 0 |
| 4/6 | 14 | 18278 | 0 |
| 5/6 | 1 | 11206 | 0 |
| Total | 55 | 2125050 | 0 |

The chunks contain 55 distinct suites, with no overlap or omission.
`sweep-results.json` records their names and counts. `source-state.json`
records the clean parent and processor heads and the measured shadow hash.

Declared skipped checks contribute zero to the reported total:

- tsn_fuzz: AAF/AVTP field campaign (tsn-gen absent; set TSN_GEN_ROOT to enable)
- tsn_fuzz: hdl/ieee1722/avtp/doc/TEST_RESULTS.md freshness not checked (AAF/AVTP field campaign (tsn-gen absent; set TSN_GEN_ROOT to enable))
- tsn_fuzz: gPTP/802.1AS field campaign (tsn-gen absent; set TSN_GEN_ROOT to enable)
- tsn_fuzz: hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md freshness not checked (gPTP/802.1AS field campaign (tsn-gen absent; set TSN_GEN_ROOT to enable))

## Final gate table

Only the following invocations count toward the completed local validation.
Earlier failures and cancelled attempts remain in the history below.
Builder exit 0 does not claim its explicitly unrun arms: the SDK run lacks
the board calibration report; the absent run additionally lacks RV32 census
coverage. The SDK run supplies that RV32 coverage and records 855 compiler
invocations through the requested pinned compiler.

The completed sweep chunk 0 excludes the optional AAF/AVTP and gPTP field
campaigns and their freshness checks because `tsn-gen` is absent. Those
declared skips contribute zero to the check total.

| Gate | Command | Exit | Evidence |
|---|---|---:|---|
| pp-shadow | `make -C tb/verilator/pp_shadow` | 0 | `pp-shadow.log` |
| pending-mutant-verified | `make -C tb/verilator/pp_shadow pending-mutant` | 0 | `pending-mutant-verified.log` |
| nvm-cosim | `make -C tb/verilator/nvm_cosim` | 0 | `nvm-cosim.log` |
| nvm-backend | `make -C tb/verilator/nvm_backend` | 0 | `nvm-backend.log` |
| sweep-clean-0 | `env SUITE_TIMEOUT=10800 scripts/run_all_suites.sh $MANAGEMENT/2026-09-23/502-a338/sweep-clean-0 --shard 0/6` | 0 | `sweep-clean-0.log` |
| sweep-clean-1 | `env SUITE_TIMEOUT=10800 scripts/run_all_suites.sh $MANAGEMENT/2026-09-23/502-a338/sweep-clean-1 --shard 1/6` | 0 | `sweep-clean-1.log` |
| sweep-clean-2 | `env SUITE_TIMEOUT=10800 scripts/run_all_suites.sh $MANAGEMENT/2026-09-23/502-a338/sweep-clean-2 --shard 2/6` | 0 | `sweep-clean-2.log` |
| sweep-clean-3 | `env SUITE_TIMEOUT=10800 scripts/run_all_suites.sh $MANAGEMENT/2026-09-23/502-a338/sweep-clean-3 --shard 3/6` | 0 | `sweep-clean-3.log` |
| sweep-clean-4 | `env SUITE_TIMEOUT=10800 scripts/run_all_suites.sh $MANAGEMENT/2026-09-23/502-a338/sweep-clean-4 --shard 4/6` | 0 | `sweep-clean-4.log` |
| sweep-clean-5 | `env SUITE_TIMEOUT=10800 scripts/run_all_suites.sh $MANAGEMENT/2026-09-23/502-a338/sweep-clean-5 --shard 5/6` | 0 | `sweep-clean-5.log` |
| ooc-before | `env OOC_TMP=/tmp/502-ooc-before syn/yosys/ooc.sh KL_pp_shadow` | 0 | `ooc-before.log` |
| ooc-after | `env OOC_TMP=/tmp/502-ooc-after syn/yosys/ooc.sh KL_pp_shadow` | 0 | `ooc-after.log` |
| builder-sdk-verified | `env PYTHONUNBUFFERED=1 /tmp/502-python/bin/python3 /tmp/502-builder-sdk.py` | 0 | `builder-sdk-verified.log` |
| builder-absent | `/tmp/502-python/bin/python3 /tmp/502-builder-absent.py` | 0 | `builder-absent.log` |
| nvm-firmware-selftest | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | `nvm-firmware-selftest.log` |
| nvm-capture | `python3 scripts/check_nvm_capture.py` | 0 | `nvm-capture.log` |
| baremetal | `python3 scripts/check_baremetal_only.py --check` | 0 | `baremetal.log` |
| docs-final | `/tmp/502-python/bin/python3 -B scripts/docs_check.py` | 0 | `docs-final.log` |
| docs-no-git-verified | `/tmp/502-python/bin/python3 -B scripts/docs_check.py` | 0 | `docs-no-git-verified.log` |
| ci-events | `python3 scripts/ci_events.py --check` | 0 | `ci-events.log` |
| ci-events-selftest | `python3 scripts/ci_events.py --selftest` | 0 | `ci-events-selftest.log` |
| em-dash-final | `/tmp/502-python/bin/python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | 0 | `em-dash-final.log` |
| doc-style | `python3 scripts/check_doc_style.py` | 0 | `doc-style.log` |
| toc-final | `/tmp/502-python/bin/python3 scripts/gen_toc.py --check` | 0 | `toc-final.log` |
| anchors | `python3 scripts/gen_toc.py --verify-anchors` | 0 | `anchors.log` |
| doc-paths | `python3 scripts/check_doc_paths.py` | 0 | `doc-paths.log` |
| module-matrix | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `module-matrix.log` |
| xvlog | `python3 scripts/xvlog_gate.py --check` | 0 | `xvlog.log` |
| rtl-source-lists | `python3 scripts/check_rtl_source_lists.py` | 0 | `rtl-source-lists.log` |
| sv-idiom | `python3 scripts/check_sv_idiom.py` | 0 | `sv-idiom.log` |
| rtl-lint | `python3 scripts/lint_rtl.py --check` | 0 | `rtl-lint.log` |
| cpp-idiom | `python3 scripts/check_cpp_idiom.py` | 0 | `cpp-idiom.log` |
| py-idiom-final | `/tmp/502-python/bin/python3 scripts/check_py_idiom.py` | 0 | `py-idiom-final.log` |
| port-contracts | `python3 scripts/check_port_contracts.py` | 0 | `port-contracts.log` |
| naming | `python3 scripts/measure_naming.py --check` | 0 | `naming.log` |
| test-evidence-final | `/tmp/502-python/bin/python3 scripts/measure_test_evidence.py --check` | 0 | `test-evidence-final.log` |
| behave | `/tmp/502-python/bin/python3 -m behave --no-capture -f plain` | 0 | `behave.log` |
| diff-check-final | `git diff --check` | 0 | `diff-check-final.log` |
| diff-check-commit | `git diff --check 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a HEAD` | 0 | `diff-check-commit.log` |
| submodule-docs | `/tmp/502-python/bin/python3 scripts/check_submodule_docs.py` | 0 | `submodule-docs.log` |
| diagram-check | `/tmp/502-python/bin/python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | `diagram-check.log` |

## Invocation history

Every invocation and exit is recorded in `gates.jsonl`.
The table below includes development failures and their later passing reruns.
Commands ran in the foreground, with logs redirected directly, never piped.
Most commands run from the candidate worktree.
Behave runs from `tests`; the no-Git gate runs in a tracked-file export.

| Gate | Command | Exit | Seconds | Log |
|---|---|---:|---:|---|
| ooc-before | `env OOC_TMP=/tmp/502-ooc-before syn/yosys/ooc.sh KL_pp_shadow` | 0 | 182.2 | `ooc-before.log` |
| pending-first | `make -C tb/verilator/pp_shadow run-base SIM_ARGS=--pending-only` | 2 | 9.43 | `pending-first.log` |
| pending-second | `make -C tb/verilator/pp_shadow run-base SIM_ARGS=--pending-only` | 2 | 6.73 | `pending-second.log` |
| pending-third | `make -C tb/verilator/pp_shadow run-pending` | 0 | 12.24 | `pending-third.log` |
| ooc-after | `env OOC_TMP=/tmp/502-ooc-after syn/yosys/ooc.sh KL_pp_shadow` | 0 | 185.64 | `ooc-after.log` |
| pending-mutant | `make -C tb/verilator/pp_shadow pending-mutant` | 2 | 16.9 | `pending-mutant.log` |
| pending-mutant-final | `make -C tb/verilator/pp_shadow pending-mutant` | 0 | 25.37 | `pending-mutant-final.log` |
| nvm-cosim | `make -C tb/verilator/nvm_cosim` | 0 | 396.64 | `nvm-cosim.log` |
| behave | `/tmp/502-python/bin/python3 -m behave --no-capture -f plain` | 0 | 1.17 | `behave.log` |
| nvm-firmware-selftest | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | 39.32 | `nvm-firmware-selftest.log` |
| nvm-capture | `python3 scripts/check_nvm_capture.py` | 0 | 0.72 | `nvm-capture.log` |
| nvm-backend | `make -C tb/verilator/nvm_backend` | 0 | 32.75 | `nvm-backend.log` |
| baremetal | `python3 scripts/check_baremetal_only.py --check` | 0 | 14.85 | `baremetal.log` |
| docs | `python3 -B scripts/docs_check.py` | 0 | 4.18 | `docs.log` |
| ci-events | `python3 scripts/ci_events.py --check` | 0 | 0.21 | `ci-events.log` |
| pp-shadow | `make -C tb/verilator/pp_shadow` | 0 | 61.31 | `pp-shadow.log` |
| ci-events-selftest | `python3 scripts/ci_events.py --selftest` | 0 | 14.79 | `ci-events-selftest.log` |
| em-dash | `python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | 0 | 3.07 | `em-dash.log` |
| doc-style | `python3 scripts/check_doc_style.py` | 0 | 0.07 | `doc-style.log` |
| toc | `python3 scripts/gen_toc.py --check` | 0 | 2.42 | `toc.log` |
| anchors | `python3 scripts/gen_toc.py --verify-anchors` | 0 | 1.57 | `anchors.log` |
| doc-paths | `python3 scripts/check_doc_paths.py` | 0 | 0.06 | `doc-paths.log` |
| module-matrix | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | 0.97 | `module-matrix.log` |
| docs-no-git | `/tmp/502-python/bin/python3 -B scripts/docs_check.py` | 1 | 4.22 | `docs-no-git.log` |
| pending-mutant-evidence | `make -C tb/verilator/pp_shadow pending-mutant` | 0 | 25.08 | `pending-mutant-evidence.log` |
| docs-no-git-final | `/tmp/502-python/bin/python3 -B scripts/docs_check.py` | 0 | 4.07 | `docs-no-git-final.log` |
| xvlog | `python3 scripts/xvlog_gate.py --check` | 0 | 138.33 | `xvlog.log` |
| rtl-source-lists | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.37 | `rtl-source-lists.log` |
| sv-idiom | `python3 scripts/check_sv_idiom.py` | 0 | 0.41 | `sv-idiom.log` |
| rtl-lint | `python3 scripts/lint_rtl.py --check` | 0 | 6.47 | `rtl-lint.log` |
| cpp-idiom | `python3 scripts/check_cpp_idiom.py` | 0 | 1.22 | `cpp-idiom.log` |
| py-idiom | `python3 scripts/check_py_idiom.py` | 1 | 3.22 | `py-idiom.log` |
| port-contracts | `python3 scripts/check_port_contracts.py` | 0 | 2.32 | `port-contracts.log` |
| naming | `python3 scripts/measure_naming.py --check` | 0 | 0.46 | `naming.log` |
| test-evidence | `python3 scripts/measure_test_evidence.py --check` | 1 | 5.32 | `test-evidence.log` |
| diff-check | `git diff --check` | 0 | 0.03 | `diff-check.log` |
| submodule-docs | `/tmp/502-python/bin/python3 scripts/check_submodule_docs.py` | 0 | 0.51 | `submodule-docs.log` |
| diagram-check | `/tmp/502-python/bin/python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | 0.41 | `diagram-check.log` |
| py-idiom-final | `/tmp/502-python/bin/python3 scripts/check_py_idiom.py` | 0 | 3.17 | `py-idiom-final.log` |
| test-evidence-final | `/tmp/502-python/bin/python3 scripts/measure_test_evidence.py --check` | 0 | 5.27 | `test-evidence-final.log` |
| pending-mutant-verified | `make -C tb/verilator/pp_shadow pending-mutant` | 0 | 34.51 | `pending-mutant-verified.log` |
| em-dash-head | `/tmp/502-python/bin/python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | 0 | 2.97 | `em-dash-head.log` |
| docs-head | `/tmp/502-python/bin/python3 -B scripts/docs_check.py` | 0 | 4.22 | `docs-head.log` |
| docs-no-git-head | `/tmp/502-python/bin/python3 -B scripts/docs_check.py` | 0 | 4.17 | `docs-no-git-head.log` |
| toc-final | `/tmp/502-python/bin/python3 scripts/gen_toc.py --check` | 0 | 2.52 | `toc-final.log` |
| em-dash-final | `/tmp/502-python/bin/python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | 0 | 3.07 | `em-dash-final.log` |
| docs-final | `/tmp/502-python/bin/python3 -B scripts/docs_check.py` | 0 | 4.22 | `docs-final.log` |
| docs-no-git-verified | `/tmp/502-python/bin/python3 -B scripts/docs_check.py` | 0 | 4.28 | `docs-no-git-verified.log` |
| builder-sdk | `/tmp/502-python/bin/python3 /tmp/502-builder-sdk.py` | 1 | 726.9 | `builder-sdk.log` |
| builder-no-compiler | `/tmp/502-python/bin/python3 sw/builder/test_builder.py` | 1 | 728.16 | `builder-no-compiler.log` |
| sweep-5 | `env SUITE_TIMEOUT=10800 scripts/run_all_suites.sh $MANAGEMENT/2026-09-23/502-a338/sweep-5 --shard 5/6` | 143 | 757.33 | `sweep-5.log` |
| builder-absent | `/tmp/502-python/bin/python3 /tmp/502-builder-absent.py` | 0 | 555.2 | `builder-absent.log` |
| builder-sdk-verified | `env PYTHONUNBUFFERED=1 /tmp/502-python/bin/python3 /tmp/502-builder-sdk.py` | 0 | 760.38 | `builder-sdk-verified.log` |
| sweep-clean-5 | `env SUITE_TIMEOUT=10800 scripts/run_all_suites.sh $MANAGEMENT/2026-09-23/502-a338/sweep-clean-5 --shard 5/6` | 0 | 1480.59 | `sweep-clean-5.log` |
| sweep-clean-0 | `env SUITE_TIMEOUT=10800 scripts/run_all_suites.sh $MANAGEMENT/2026-09-23/502-a338/sweep-clean-0 --shard 0/6` | 0 | 969.78 | `sweep-clean-0.log` |
| sweep-clean-1 | `env SUITE_TIMEOUT=10800 scripts/run_all_suites.sh $MANAGEMENT/2026-09-23/502-a338/sweep-clean-1 --shard 1/6` | 0 | 179.41 | `sweep-clean-1.log` |
| sweep-clean-2 | `env SUITE_TIMEOUT=10800 scripts/run_all_suites.sh $MANAGEMENT/2026-09-23/502-a338/sweep-clean-2 --shard 2/6` | 0 | 1173.61 | `sweep-clean-2.log` |
| sweep-clean-3 | `env SUITE_TIMEOUT=10800 scripts/run_all_suites.sh $MANAGEMENT/2026-09-23/502-a338/sweep-clean-3 --shard 3/6` | 0 | 335.34 | `sweep-clean-3.log` |
| sweep-clean-4 | `env SUITE_TIMEOUT=10800 scripts/run_all_suites.sh $MANAGEMENT/2026-09-23/502-a338/sweep-clean-4 --shard 4/6` | 0 | 1474.58 | `sweep-clean-4.log` |
| diff-check-commit | `git diff --check 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a HEAD` | 0 | 0.02 | `diff-check-commit.log` |
| diff-check-final | `git diff --check` | 0 | 0.03 | `diff-check-final.log` |

## Reproduction details

- `run-gate.py` writes command, exit, elapsed time and the unfiltered log.
- `sweep-clean.py` runs all six accepted default-sweep chunks sequentially.
  `sweep.py` records the discarded initial attempt.
- `fast-gates.py` records the remaining command suite.
- `builder-sdk.py` verifies the pinned SDK read-only, then maps only the
  test's absolute compiler selector to that SDK, following the supplied recipe.
- `builder-sdk-argv.jsonl` records every mapped compiler invocation and exit.
- `builder-absent.py` runs the full unmodified builder test with all three
  RV32 candidates explicitly hidden; host tools remain available.
- The initial two builder runs collided on temporary in-tree fixtures and
  were discarded. The default invocation also found installed RV32 tools;
  its historical `builder-no-compiler` label does not establish absence.
  The compiler-absent and pinned-SDK reruns run serially.
- Markdown gates use the hash-locked renderer from `tools/markdown/requirements.txt`.
  Its environment is temporary and outside this output directory.
- The no-Git mode contains the candidate's tracked files and empty gitlink
  directories, matching CI's checkout without submodule population.

Development corrections retained in the command record:

| Earlier result | Correction and final evidence |
|---|---|
| Initial pending build refused | Corrected the harness's instance path |
| Initial fixture checks failed | Used a valid named ENTITY descriptor and enabled dynamic output maps in a separate fixture |
| Initial mutant build refused | Preserved the copied shadow's relative path for existing scoped warnings |
| Python idiom failed | Added public annotations and documentation; py-idiom-final passes |
| Test-evidence ratchet failed | Removed the redundant inner process timeout; DUT waits remain cycle-bounded and the outer run retains its generous limit |
| Initial no-Git export missed directory links | Preserved empty gitlink directories; docs-no-git-head passes |

## Remaining work and limits

The compiler-absent rerun passed with exit 0. It explicitly excludes the
RV32 census and the unavailable board calibration report. The pinned-SDK
rerun passed with exit 0, covering the RV32 census. Its only unrun arm is
the unavailable board calibration report.

The initial concurrent builder runs and overlapping sweep are discarded.
The sweep was cancelled; shard 5 recorded exit 143. The scheduler briefly
started shard 0 before cancellation; its empty log has no completed verdict.
Both serial builder modes and all six clean sweep chunks passed.
The author handoff is complete; the local head is ready for independent review.
Independent review and hosted required contexts have not run for this local head.
No push, PR creation/edit, merge, hardware operation, other checkout or donor edit
was performed. The processor checkout is at its staged gitlink and clean.
The separate #567 integration round remains with the maintainer.
