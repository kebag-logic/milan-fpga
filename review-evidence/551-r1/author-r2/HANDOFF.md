[A260] Round 2 handoff for PR #553 / issue #551

## Status

Local implementation committed and every assigned gate passed. Ready for independent re-review of this round; F1 remains dependent on the processor pin.
No push, PR edit or merge was performed. No other checkout, sub-agent or
hardware was used. Commands run in the foreground; no detached jobs.

- Branch: `551-licence-real-grant`
- Starting head: `0bf22c93546fcc70fffdb8428bde331fa2fc8f05`
- Final implementation head: `babb8925030612e47c687b1fda1a1ce614988721`
- Commit: `Pin licence contract tests and document pending stale-grant fix`
- Commit has one subject line, no body and no trailers.
- Validation base: `59b816708852472da6ed4576386c30ebd5f8f839`
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/551#issuecomment-5816014072
- Review-ready issue comment: https://github.com/kebag-logic/milan-fpga/issues/551#issuecomment-5816587279

F1's defect remains open. A refused re-declaration whose TSpec differs from
that source's previous one can still see about one round of licence because
the first-round grant uses the previous slope. This round implements the
assigned documentation corrections and reproducer, not the processor fix.
Processor #112 must merge and be adopted by a parent pin before issue #551
can close. No reviewer coverage or approval is claimed here.

## Finding responses and changed artifacts

| Finding | Implementation | Evidence / remaining dependency |
|---|---|---|
| Both F2 | `tests/features/milan_streaming_licence.feature:87` and `tests/steps/milan_streaming_licence_steps.py:175` pin ACTIVE AND the per-source grant, exact slices and no other logic | Full behaviour suite passes. ACTIVE-only and raw-grant-only each fail the actual scenario; clean controls pass before and after. Await independent re-review. |
| R296 F4 / R297 F3 | `docs/traceability/ieee8021q.md:98` restores Q-9/Q-10 module mapping, processor status, deleted 75% test caveat and 34.3/34.4 rationale | Q-9 claims only oversized refusal with the same TSpec preloaded; it expressly does not prove the 75% boundary. |
| Both F3 | Regenerated `docs/traceability/MODULE_MATRIX.md:160` and `hdl/milan/README-tests.md:15` | `KL_pp_shadow` again lists 34.3 and 34.4; generator check rc 0. |
| R297 F4 / R296 F4 | Corrected declaration, CRF status and admission-block comments in `hdl/milan/milan_datapath.sv`, parent interface at `hdl/milan/KL_pp_shadow.sv:627`, ieee8021q interface/MRP-4, compliance matrix row 179, and suite index row 27 | Both touched RTL modules have identical non-comment tokens to the starting head; see `rtl_comments_only.txt`. |
| Both F1, text and fixture only | Residual in FR_NFR:225, REGISTER_MAP:1119, EGRESS_QUEUE_MAP:92, ieee8021q, compliance matrix, CHANGELOG:47, suite README:420 and RTL/fixture comments | Processor #112 and its parent pin remain pending. Claims of unconditional closure removed. |
| Both F1, latency | Suite README and RTL/CHANGELOG distinguish 0--2 warm cycles from the reviewed 4-cycle changed-TSpec start | The 4-cycle CRF phase-0 measurement is attributed to R296-1, not re-measured this round. Re-measure both histories after the processor fix. |
| Both F1, unwarmed case | `sim_crf_licence.cpp:1080` adds `[I]`, selected by `--unwarmed-refusal` | Default explicitly skips it by name with EXPECTED-FAIL processor #112. Explicit run preserves assertions and returns 1. |

The manager's generator-only commit had repaired freshness but lost the
module citation. This round repairs the source rows and regenerates both
outputs; it does not retire that ownership.

## Fixture evidence

Default `crflic`: 253 checks, zero failures, rc 0.
Warm added latency remains AAF phase 0/1 = 2/1 cycles and CRF = 0/1.

Explicit unwarmed arm: 339 total checks, 28 failures, rc 1, EXPECTED-FAIL.
It adds four cases: both sources at both phases of the two-source round.
Each first preloads an admissible 224-byte TSpec, withdraws and confirms
the grant cleared, then stages a refused 20,000-byte TSpec. Listener Ready
arrives through the real MAC decoder at the measured time. No admission
verdict, registrar, optimistic state or licence is forced.

All four cases fail the same seven assertions: no first-round grant rise,
no licence rise, no STREAM_START, no STREAM_STOP, and preservation of
MEDIA_RESET/TIMESTAMP_UNCERTAIN/FRAMES_TX (17/29/43 become zero).
All four no-PDU checks pass for this schedule. A possible PDU is still a
residual exposure, not an observed emitted PDU in this run.

Reproduce after building the default leg:

```sh
cd tb/verilator/milan_dp
./obj_crflic/Vmilan_dp_crflic --unwarmed-refusal
```

After pinning processor #112, make I unconditional and remove its
EXPECTED-FAIL/skip labels. Require the same no-pulse, counter-preservation
and no-PDU assertions to pass. First declaration after reset and other
geometries are outside this arm's executed coverage.

## Required gates

All commands use repository root unless the cwd column says otherwise.
No gate output was piped. `gates.jsonl` records commands, rc and duration;
individual raw logs have the names below. The locked Markdown dependencies
were installed outside this output directory. No SDK, toolchain or virtual
environment is stored here. `versions.txt` records the versions used.

| Gate / command | cwd | rc | Log |
|---|---|---|---|
| `behave --no-capture -f plain` | `tests` | 0; 344 scenarios, 1739 steps | `behave.log` |
| `make -C tb/verilator/milan_dp crflic VERILATOR_JOBS=8` | root | 0; 253/0 | `crflic.log` |
| `make -C tb/verilator/milan_dp crflic-mutants VERILATOR_JOBS=8` | root | 0; 7/7, all six mutants caught | `crflic_mutants.log` |
| `make -C tb/verilator/milan_dp VERILATOR_JOBS=8` | root | 0; all 13 legs plus render campaign 6/6 | `milan_dp_default.log` |
| `python3 scripts/docs_check.py` | root | 0 | `docs_git.log` |
| `env GIT_DIR=<absent-path> python3 scripts/docs_check.py` | root | 0; filesystem walk | `docs_no_git.log` |
| `python3 scripts/check_em_dash.py --base 59b816708852472da6ed4576386c30ebd5f8f839` | root | 0; 339/339 arms | `em_dash.log` |
| `python3 scripts/check_doc_style.py` | root | 0 | `doc_style.log` |
| `python3 scripts/gen_toc.py --check` | root | 0 | `gen_toc.log` |
| `python3 scripts/check_doc_paths.py` | root | 0 | `doc_paths.log` |
| `python3 docs/traceability/gen_module_matrix.py --check` | root | 0; clause cell restored | `module_matrix.log` |
| `python3 scripts/xvlog_gate.py --check` | root | 0; 0 first-party / 4 unchanged processor findings | `xvlog.log` |
| `python3 scripts/check_rtl_source_lists.py` | root | 0 | `rtl_source_lists.log` |
| `python3 scripts/check_py_idiom.py` | root | 0 | `py_idiom.log` |
| `python3 scripts/check_cpp_idiom.py` | root | 0 | `cpp_idiom.log` |
| `git diff --check` | root | 0 | `working_diff_check.log` |
| `git diff --check 0bf22c93546fcc70fffdb8428bde331fa2fc8f05 HEAD` | root | 0; also checks committed round delta | `diff_check.log` |

Filesystem docs mode skips only its Git inventory-parity control, explicitly.
Syntax analysis ran; it was not a missing-tool skip.

## Local rtl-fast equivalents and mutation sensitivity

| Check | rc / result | Evidence |
|---|---|---|
| `python3 scripts/ci_scope.py --selftest` and actual changed-file classification | 0; RTL scope true | `ci_scope.log`, `changed-files.txt`, `ci_scope_result.log` |
| `python3 scripts/lint_rtl.py --check --self-test` | 0; 90 findings at unchanged ratchet | `lint.log` |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 | `pp_srcs.log` |
| Full behaviour suite | 0 | `behave.log` |
| `syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow` | 0; 3/3 tops | `yosys_elaboration.log` |
| Additional `python3 scripts/check_sv_idiom.py` | 0 | `sv_idiom.log` |
| Actual BDD scenario, clean before/after | both 0 | `bdd_clean_before.log`, `bdd_clean_after.log` |
| ACTIVE-only BDD mutant | 1, named composition assertion | `bdd_active_only.log` |
| Raw-grant-only BDD mutant | 1, named composition assertion | `bdd_raw_grant_only.log` |
| `bdd_mutants.py <repository> <evidence-directory>` | 0; both caught and exact RTL bytes restored | `bdd_mutants.log`, `bdd_mutants.py` |
| Explicit unwarmed arm | 1, EXPECTED-FAIL; not an acceptance pass | `unwarmed_expected_fail.log` |

The mutation driver temporarily rewrites only the actual gate assignment,
runs the unchanged scenario, checks its assertion failure and restores the
original bytes in `finally`. It ran with no concurrent RTL readers/builds.

The local fast checks do not publish or replace hosted required contexts.
No pushed head exists for this round. Hosted acceptance and the supported
local workflow replica remain for the authorised publication turn. Full
parent/processor banks, exhaustive portability and candidate-merge gates
are not claimed by this scoped round.

## Handoff and remaining work

`PR-BODY.md` is a full replacement body starting with [A260]. It retains
`Closes #551`, as requested, with an explicit dependency/merge block.
That remains accurate if PR #553 waits for the processor pin before merge.
If this partial state were to merge earlier, `Relates to #551` would be the
accurate relationship and the issue must remain open; no early merge is
proposed here.

The [A260] REVIEW READY comment was posted with the exact local head.
The manager owns publication, independent re-review and processor-pin
adoption. F1 is not resolved by moving its ownership or documenting it.

The last amendment changes only the README dependency wording: awaiting the processor pin. All behavioral/test/RTL blobs are unchanged from the head used to start the simulations. Both documentation inventory modes, TOC, em-dash and generated-matrix checks were rerun afterwards and pass.

Final audit: clean worktree; expected branch/head; one-line commit without trailers; unchanged processor gitlinks; comment-only RTL delta. All assigned gates return 0. The explicit unwarmed arm remains rc 1 with 28 expected failures, and is not counted as a gate pass. See `final-state.txt` and `MANIFEST.sha256`.
