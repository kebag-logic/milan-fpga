[R245] NEGATIVE - exact head 5874895eb817ed41c0f8be4eb427ad3315c29844

R245-1 is the first full cleared-context internal source review of issue #517 / PR #524. One MAJOR finding remains: stdout backpressure can prevent INT/TERM cancellation from terminating and reaping simulations. All five lenses were applied to both implementation commits; the finding affects each for the reasons below. This is a source verdict, not a merge authorization.

Reviewed tree: `45a2a9b2b108a932db49d9ec595ff4b3f18a2b3e`. Actual implementation base: `483a133ed08867ea0d300d2b4a027b5b48a4282f`. Original implementation/benchmark commit: `7ab1c8d0ad073fbc1977c455dea89b7b318d4e52`. The [public assignment](https://github.com/kebag-logic/milan-fpga/pull/524#issuecomment-5783078964), issue/PR metadata and public comments are preserved in `assignment.json`, `issue.json` and `pr.json`. No earlier reviewer verdict or numbered reviewer finding exists in those captured PR reviews/comments; earlier author/manager failures are explicitly disposed of below.

[R245] MAJOR Conformance, RTL, Robustness, Tests, Docs - tb/verilator/milan_dp/sim_pool.py:303,316,335,340 - F1: blocked output replay prevents cancellation cleanup

**Authority/evidence.** The frozen [issue contract](https://github.com/kebag-logic/milan-fpga/issues/517) requires cancellation to terminate and reap owned children/process groups and retain attributable partial logs. The architecture/backpressure and robustness lenses explicitly cover stalls and cancellation. The runner blocks INT/TERM while inside `Pool.run`, consumes them at `sigwait`, and synchronously calls `shutil.copyfileobj`/`flush` before returning to that wait. See [replay and event loop](https://github.com/kebag-logic/milan-fpga/blob/5874895eb817ed41c0f8be4eb427ad3315c29844/tb/verilator/milan_dp/sim_pool.py#L295). When stdout is a full pipe, it cannot reach `stop` while a consumer refuses to drain.

Independent reproduction uses two real executable fixtures: the first completes with 262 KiB of output; the second emits partial output and owns a descendant in a separate session. The probe waits for the kernel-observable `anon_pipe_write` state, then sends INT or TERM. After the signal, the runner remains in that state with the signal pending in `ShdPnd`; both owned PID descriptors report no exit event. The same result occurs through the exact, byte-identical Makefile and runner, with the recipe's two-child default, after inert compiler/prerequisite fixtures. The Makefile probe sends the signal to make's process group, not merely to an imported helper.

[Direct receipts](output-backpressure-v2/results.json) and [real-Makefile receipts](make-backpressure/results.json) retain both signals, argv, process identities, pending-signal snapshots, captures and exit outcomes. `check_backpressure.py` exits **1** for each set. Releasing the same pipe is the positive control: the pending signal is handled, the runner/make ends by the original signal, and both PID descriptors then report `POLLHUP` (event mask 17), proving reaping. No process was left running by the review.

**Impact.** A caller using a stalled stdout consumer can leave make/runner cancellation waiting indefinitely for output progress, with an ordinary leg and its descendant still running. The normal sweep's regular-file capture avoids this particular condition; its successful evidence is not contradicted. The runner and README impose no regular-file-only output contract. The observed defect is delayed cancellation while the parent remains blocked; the probe does not claim that the parent exited first or that SIGKILL cleanup is possible.

**Required outcome.** Cancellation must terminate and reap owned simulations without depending on further stdout consumption. Keep complete/partial per-leg captures attributable on disk and preserve deterministic replay when output is available. Add a regression exercising cancellation during blocked replay through the real recipe. Do not waive this as #523 or merely change the issue's frozen acceptance.

**Verification.** With the consumer still blocked, both INT and TERM must result in terminated/reaped owned processes and bounded runner shutdown; subsequent draining must not be necessary to trigger cleanup. Preserve the existing ordered-output, failure, group-exclusion and frame-output controls. Re-review the corrected exact head across affected lenses.

**Lens attribution.** Conformance: the cancellation contract fails. RTL/architecture: the host runner's synchronous replay blocks its signal-service path; this is an orchestration architecture finding, not an HDL defect. Robustness: output backpressure defeats interruption with descendants. Tests: `test_sim_pool.py:258-264` deliberately sends runner stdout to regular files, and its interruption arms at `:697` never interrupt a blocked replay; all 17 arms pass with F1 present. Docs: README `:28-33` and runner docstring `:35-48` promise interrupt cleanup without disclosing or satisfying the output dependency. These are overlapping consequences of one defect, not five independent findings.

The first diagnostic attempt exited 1 at its setup guard because it required the exact wait-channel spelling `pipe_write`; this host reports `anon_pipe_write`. It produced no cancellation verdict. `output-backpressure/setup-failure.txt` retains that setup event; the corrected portable probe uses substring matching and separate v2 receipts. No failed receipt was relabelled as a pass.

The public task was reconstructed from AGENTS, CONTRIBUTING sections 2/3, `docs/README.md`, REQ-VER-01/02/04, the verification developer guide, architecture/submodule authorities, the issue and linked decisions, and then the complete diff/history and executable evidence. Product ownership and interface/reset/CDC rules remain those in `REQUIREMENTS.md`, `docs/overview/ARCHITECTURE.md:43-119` and `docs/reference/SUBMODULES.md:19-100`. No production RTL, firmware, processor pin, clock, reset or wire contract changed. The changed host scheduling architecture was still reviewed under RTL rather than declaring the entire lens inapplicable.

The [shared-header decision](https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5780545051) replaces the erroneous read-only-input premise: all five `sim_nxn` executables share one exclusive, ordered group, while other ordinary legs may overlap within two slots. `sim_nxn.cpp:255-260,398-420` selects existing configs and generator argv; `sw/builder/endstation_builder.py:5632-5671` still writes their repository-relative shape headers. Three 4-stream legs share the 4x4 header. Notification and 8-stream legs write their respective headers. Private images remain unique via `mkdtemp` at `sim_nxn.cpp:356-368`. The other three selected harness source files contain no file-writing operations; the resolved model/source set and generator bytes are unchanged. Frame writes remain at `sim_nxn.cpp:2837-2844`; environment presence, including empty, selects one-worker execution for the entire ordinary set before launch.

The original command/model inventory was derived from base Makefile executable lines, independently of the new runner/test inventory. All commands below have **no arguments**, retain the suite working directory, and execute once on success. Build parameters, source lists, seeds, windows, timers and assertions are unchanged. Evidence: `source-scope-proof.json`, `blackbox/*/ledger.jsonl`, original per-leg captures, and the corrected manager's real `milan_dp.log`.

| Legacy order / executable | Harness and model distinction | Exclusive | Real checks |
|---|---|---|---:|
| `obj_dir/Vmilan_dp_sim` | `sim_main.cpp`, baseline 1-stream Arty option-OFF | No | 230 |
| `obj_notify/Vmilan_dp_notify` | `sim_nxn.cpp`, 1-stream TDM8, timed notifications, existing compressed PP timers | Yes | 135 |
| `obj_nxn/Vmilan_dp_nxn` | `sim_nxn.cpp`, 4 streams, default 2 wire channels | Yes | 1633 |
| `obj_nxndv/Vmilan_dp_nxndv` | `sim_nxn.cpp`, divergent input-row rate, 4 streams | Yes | 1635 |
| `obj_nxn8/Vmilan_dp_nxn8` | `sim_nxn.cpp`, 8 streams, loopback and fixed sequence | Yes | 3061 |
| `obj_nxn4c/Vmilan_dp_nxn4c` | `sim_nxn.cpp`, 4 streams, 4 channels, TDM8/I2S blend | Yes | 1633 |
| `obj_nolpf/Vmilan_dp_nolpf` | `sim_main.cpp`, LPF pruned | No | 230 |
| `obj_prune/Vmilan_dp_prune` | `sim_prune.cpp`, six tier-1 blocks pruned | No | 33 |
| `obj_ax1x1/Vmilan_dp_ax1x1` | `sim_main.cpp`, AX 1x1 TDM8 option-OFF | No | 227 |
| `obj_aclk/Vmilan_dp_aclk` | `sim_aclk.cpp`, same AX shape at true 391/1591 ratio | No | 139 |

The ordinary subtotal is 8956. Real gPTP prerequisites and render controls bring the total to 9324, zero failures, 13 tally records. `Makefile:352-447` retains all ten builds before the pool and render after successful pool completion. `source-scope-proof.json` proves every Makefile byte outside the two intended scheduling additions identical to base, and the only C++ delta is its corrected comment. The source list derivation, prerequisite recipes and `render_mutants.py` are byte-identical. The six original render checks and all 23 phase/event/status semantics match across the four original runs and corrected source, including both positive modes and all four named mutation failures. No telemetry adds tests. Unchanged `scripts/run_all_suites.sh`, `suite_tally.py`, `suite_shards.py` and `.github/workflows/rtl.yml` preserve suite ownership, deadlines and failure interpretation under #444/#445.

Independent verification, with raw receipts:

| Examination | Result | Artifacts |
|---|---|---|
| Existing runner arms | 17/17, exit 0; these do not cover F1 | `focused/runner.stdout`, `focused/receipts.json` |
| Existing phase observation | 24/24, exit 0 | `focused/phase.stdout` |
| Tally selftest | exit 0 | `focused/tally-selftest.stdout` |
| Policy actual inventory / selftest | zero findings across 827 files; 601 arms, exit 0 | `focused/policy-check.stdout`, `focused/policy-selftest.stdout` |
| Real Makefile black boxes | 15 controls accepted: default/one-worker, complete large binary output, group order/overlap, frame set/empty, child fail/crash/missing, INT/TERM descendants, invalid workers with inherited `MAKEFLAGS=-j8` | `blackbox/results.json` and per-case captures/ledgers |
| Runner/wiring defect controls | All six rejected: removed Makefile exclusivity, third slot, empty-variable truthiness, discarded output, masked failure, unreaped adopted children | `blackbox/results.json` |
| Independent policy CLI fixtures | 264 expected outcomes across 20 real literals; five broadened-mask mutants detected | `policy-probes/results.json` |
| Blocked-output INT/TERM, direct and Makefile | Cancellation acceptance FAIL; draining controls pass | `backpressure-acceptance-receipts.json`, `make-backpressure/acceptance.stdout` |

The black boxes execute an unchanged Makefile with inert compiler/model fixtures, retained real build argv, and generated prerequisites explicitly marked old only in the disposable fixture. They are wiring/fault evidence, not new RTL runs. All fixture work was bounded to eight make/build jobs. No repeated full parent, PP, gPTP, Yosys or builder bank was run. The allowed Verilator wrapper, underlying driver and binary hashes were matched to public identities before `--version`; `tool-identity.json` records 5.050. No reviewer model build was necessary to establish F1 or the unchanged model workload.

The bounded [host-tool correction](https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5781783857) is otherwise sound. #259's host-development non-goal does not permit a retired target product. `check_baremetal_only.py:264-305` adds exactly three term-mask and two runtime-mask entries, pinned to path and surrounding literal context. Only allowed tokens are removed; other classes still inspect the line. Independent CLI fixtures use actual source lines identified by the original public failure, not strings generated from regexes. They accept legitimate home contexts and reject wrong-file, same-line, unrelated-line, protected-product, longer-token and altered-path copies, plus T/R/S/H/K/O additions. The mixed refusal line remains covered under both T and R. An AST comparison removes only those five entries, two new fixture helpers and their registration and then exactly matches the old checker: inventory discovery, every pre-existing policy class, product/path restrictions and prior selftests remain intact. All 13 `.budget` files match base; no ratchet grew.

Every original policy failure is resolved at this head; the following table covers all 21 findings on 20 distinct lines. These were public checker findings, not severity-labelled independent reviewer findings.

| Original artifact | Original classes | Exact-head disposition |
|---|---|---|
| `tb/verilator/milan_dp/README.md:33` | T | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/sim_pool.py:35` | T | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/sim_pool.py:81` | T | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/sim_pool.py:87` | T | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/sim_pool.py:88` | T | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/sim_pool.py:103` | R | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/test_sim_pool.py:45` | T | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/test_sim_pool.py:46` | R | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/test_sim_pool.py:107` | R | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/test_sim_pool.py:109` | R | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/test_sim_pool.py:113` | R | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/test_sim_pool.py:124` | R | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/test_sim_pool.py:169` | R | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/test_sim_pool.py:282` | R | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/test_sim_pool.py:284` | R | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/test_sim_pool.py:288` | R | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/test_sim_pool.py:344` | R | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/test_sim_pool.py:412` | R | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/test_sim_pool.py:908` | R | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |
| `tb/verilator/milan_dp/test_sim_pool.py:909` | T, R | Resolved by exact context mask; real literal accepted and transplanted/appended variants refused. |

Other earlier public items are explicitly resolved or retained:

| Earlier item | Disposition at reviewed head |
|---|---|
| A176 shared-header decision blocker and inaccurate comment | Decision recorded; exact five-leg Makefile group and ordered scheduler verified; comment corrected, generator argv/writes preserved. |
| A176 preliminary integration arm failed on the unintegrated base | Resolved: new Makefile handoff is present, existing integration arm and independent executed-recipe controls pass. No preliminary result is treated as final acceptance. |
| Original 21-finding full-bank failure | Resolved only by the scoped policy correction and fresh exact-head bank; original failed/partial evidence remains failed/partial. |
| Preliminary mask swallowed the prefix of `Linuxptp` | Resolved by the token boundary at checker `:265`; literal longer-token probe refuses it. Reintroducing that mask defect is detected independently. |
| #523 pre-existing outer-sweep/gPTP mutation interruption issue | Retained under its separate public issue. This review neither claims it fixed nor invokes it to excuse F1 in the new runner. |

The full-suite benchmarks remain attributed to **7ab1c8d0ad073fbc1977c455dea89b7b318d4e52**, never relabelled as measurements made at the correction head. Git object comparison proves these five artifact bytes unchanged:

| Artifact under `tb/verilator/milan_dp` | Same blob at both heads |
|---|---|
| `Makefile` | `5266b593f66f15e6b0d2bc00cfc1e9713e254da8` |
| `sim_pool.py` | `761ec858c7ad23abb81d215122de3c5d260e653e` |
| `test_sim_pool.py` | `ab93e2c5bfa37474320b1f40fd7cb71cc45e7704` |
| `sim_nxn.cpp` | `5866a1b5beef2c268495e759755f6192526229d6` |
| `README.md` | `d5b6cb89e9bee722b611490e99cf483d324e9705` |

`public-evidence-review.json` independently recomputes totals, checks exact per-leg bytes in the full logs, compares input/executable identities and before/after committed header bytes, and reads all four raw process-sample streams. All ten ordinary captures are byte-identical across every benchmark and the corrected manager run. The sample streams observe each original argv once and the stated bounds; sampled maxima are observations rather than mathematical concurrency proofs, which the held-process controls supply separately.

| Temperature | Sequential seconds | Pooled seconds | Observed gain |
|---|---:|---:|---:|
| Cold | 1136.415 | 1099.401 | 3.257% |
| Warm | 987.247 | 943.330 | 4.448% |

One pair per temperature used the same host, pinned tool, eight-CPU affinity and 12 GiB memory limit. Cold means suite build artifacts were removed, not filesystem cache eviction. Warm retains same-mode build artifacts but reruns simulations and mutants. Full time includes unchanged builds/prerequisites/render; no build acceleration or hosted speedup follows from these figures. Sampled ordinary/group peaks are 1/1 sequential and 2/1 pooled. Cold aggregate RSS peaks were 2686736/2720648 KiB, warm 2573764/2550360 KiB; pooled ordinary RSS peaks were 10900/10928 KiB. Sampling is not an exact simultaneous memory peak; `wait4`'s single-process peaks are separately recorded. The small observed gains satisfy the local measured comparison, with no statistical repeatability or universal-percentage claim.

The manager's public corrected-source receipts bind all **50 static/builder command exits and five native command exits to 0** at `5874895eb817ed41c0f8be4eb427ad3315c29844` and base `483a133ed08867ea0d300d2b4a027b5b48a4282f`. I inspected the exact ledgers and raw native/static logs, and independently re-tallied the real milan_dp log. The parent sweep reports 55 passed suites, 2118264 checks and four explicit field/freshness skips. PP reports 14903 checks, no failing; native gPTP and uncached Yosys commands finish; Behave reports 316 scenarios and 1515 steps passed. Builder gate 11 is explicitly **NOT RUN**. These are source validation records, not hardware proof and not final current-dev candidate validation.

Hosted dedicated-worker comparison remains manager pending. No Actions/run/check API, `gh run`, `gh pr checks`, or `statusCheckRollup` was inspected. Trusted act, exact-head hosted contexts, external R246 Opus, final current-dev candidate validation, authorized merge and containment remain outstanding manager/reviewer duties; external availability is not a waiver. The existing 1999-second hosted baseline is public context only, not a local-to-hosted ratio. F1 independently prevents a clean source verdict regardless of that pending integration work.

Reviewer-owned completion ledger, applying the named lenses to the exact source head:

| Lens | Applying round / result | Exact head |
|---|---|---|
| Conformance | R245-1, applied; UNCLEAN (F1) | `5874895eb817ed41c0f8be4eb427ad3315c29844` |
| RTL | R245-1, applied; UNCLEAN (F1) | `5874895eb817ed41c0f8be4eb427ad3315c29844` |
| Robustness | R245-1, applied; UNCLEAN (F1) | `5874895eb817ed41c0f8be4eb427ad3315c29844` |
| Tests | R245-1, applied; UNCLEAN (F1) | `5874895eb817ed41c0f8be4eb427ad3315c29844` |
| Docs | R245-1, applied; UNCLEAN (F1) | `5874895eb817ed41c0f8be4eb427ad3315c29844` |

No clean covering round is banked here while F1 remains open. Artifact coverage was independent: Conformance examined the frozen issue/decisions, REQ-VER-01/02/04, Makefile `:352-447`, runner `:143-173,311-406` and public real outputs; RTL examined unchanged HDL/interfaces/source/config identities, generator writes `:5632-5671`, and runner state/signal/replay architecture; Robustness exercised actual process failures, crashes, absent executables, worker bounds, whole-set serialization, descendants and blocked output; Tests examined all 17 runner arms, all 24 phase arms, policy controls and independent executable fault probes against actual wiring; Docs compared README `:15-45`, source contracts, public frozen decisions, head attribution, complete/partial evidence and all limitations above. Unchanged production wire/reset/CDC internals are proved outside this diff by `full-diff.txt` and `source-scope-proof.json`; that does not excuse the changed host architecture from review.

Final integrity: `initial-integrity.json` and `final-integrity.json` independently hash every tracked blob from bytes, verify regular-file/symlink kinds and executable modes, compare the entire stage-0 index to the commit tree, reject hidden index flags, disable Git replacement objects, and verify registered submodule roots/pins/bytes. All 853 parent files and 539 files in the three required submodules match; tracked status is empty. Pins remain `third_party/verilog-axis` = `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, `protocol-processor` = `424c688fa2205b934a7689a58f2aa766420f2326`, and `gptp-processor` = `c1b617435824929a790739ea8585c3fe1a328cc0`. The unconsumed `external` gitlink is unchanged and was not validated as an initialized checkout.

`COMMANDS.md` supplies portable reproduction. Public downloads retain Git-blob and SHA-256 receipts; raw captures and per-command exits accompany the independent scripts. No source fix, source commit/push, public comment/metadata mutation, author contact, other agent, edit to another source checkout, Docker/act, candidate act_ci execution/selftest, shared installation, privilege operation or hardware action occurred. This report contains conclusions and reproducible evidence, not private reasoning.

R245-1 FINISHED
