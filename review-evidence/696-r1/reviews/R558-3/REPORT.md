[R558] NEGATIVE - exact head b9b389611304850ea435b2056887568afe5e6bf4

# R558-3 - issue #696 / PR #706 - internal independent review, delta round

- **Head:** `b9b389611304850ea435b2056887568afe5e6bf4`, tree `d2c5eb6e64ec20bb8291ac2aa00e105a137c7b9b`, reviewed in a detached clean clone.
- **Delta:** `f909d6c4..b9b38961` is one commit, `b9b38961`, by the manager. It changes one file, `tb/verilator/maap/integration.mk`, by +5/-2. Nothing changed in `hdl`, `syn`, `sw`, `scripts`, `.github`, `docs`, `configs` or the submodule gitlinks (`receipts/delta-f909d6c4-b9b38961.diff`).
- **Question:** does the commit answer the hosted failure at `f909d6c4`, and is the shard green at this head?
  - The failure was rtl-full run 38021886237, job "Verilator shard 1/5". There, `maap` failed with 4 in-suite failures.
- **Earlier rounds:** R558-1, R558-2, R559-1 and R559-2 stand for every artifact that this commit does not touch.
- **Reading order:** I reconstructed the task from AGENTS.md, CONTRIBUTING.md and the issue (body, frozen acceptance 1-4, and the manager rulings), then the diff and history. I read the published evidence and the hosted logs and artifacts next. I read the prior public findings on this PR only after I had written my own provisional verdict and ledger.

## 1. Verdict

**NEGATIVE.** The commit does not fix the hosted failure, so I raise one BLOCKER, R558-3-F1, under Conformance, Robustness and Tests.

- **Hosted result.** Verilator shard 1/5 at this exact head fails again: rtl-full run 38027027728, job 114140492769. `maap` reports the same 4 in-suite failures, and the `verilator-suites` gate is red.
  - This time the new guard is what stops the build: `integration.mk:13: *** datapath source list names non-files: make[2]:.  Stop.`
  - The four real-datapath rows are therefore still counted as escaped.
  - Issue acceptance 2 depends on those rows.
- **Cause.** `--no-print-directory` does not stop the nested make from writing directory lines under GNU Make 4.3, the hosted runner's make, when the capture runs inside a `-j8` recursive parent with `w` inherited. That parent is the shape `mutants.py` creates.
- **Reproduction.** I reproduced it locally with a GNU Make 4.3 binary.
  - The head stops at the guard.
  - A copy whose captures also clear `MAKEFLAGS=`, as `pp_shadow`, `milan_dp_mclk` and `milan_dp_render` already do, builds and passes `MAAP integration: 3 checks, 0 failures`.
- **Why the local campaigns passed.** The reproduction requested for this round, `MAKEFLAGS=w make -C tb/verilator/maap`, passes on the host's GNU Make 4.4.1 (172/0 and 52/0). That make does not show the defect, so this reproduction is necessary but not faithful.
- **What does work.** The guard works as intended: it turned silent list pollution into a named parse stop. That part of the commit is sound.

## 2. What the commit does, and what I checked

`integration.mk:8` and `:15` now pass `--no-print-directory` to both nested captures (`print-srcs` and `print-dp-vflags`).
`:11-13` add a parse-time guard. It stops with `datapath source list names non-files: <first word>` when any word of `DP_SRCS` is not matched by `$(wildcard)`.

| Check | Result | Receipt |
|---|---|---|
| **Hosted Verilator shard 1/5 at this head** | **failure.** 22 of 23 suites pass. `maap` FAILS with `checks: 197745 in-suite failures: 4`. In the maap log, `KL_maap: 172 checks, 0 failures`, then four times `make[2]: warning: jobserver unavailable ...` followed by `integration.mk:13: *** datapath source list names non-files: make[2]:.  Stop.` and `[ESCAPED] <row>: compilation failed`, ending `== maap mutants: checks: 52 failures: 4 ==`. The `verilator-suites` gate is failure. | `receipts/hosted-shard1-summary.log`, `receipts/hosted-b9b38961-shard1-maap-excerpt.log` (artifact `suite-logs-1`, id 11662447870), `receipts/hosted-status.tsv` |
| Other hosted contexts at this head | rtl-fast, docs, docs-check-no-git and elaborate: success. rtl-full: Verilator shards 0/2/3/4, Yosys shards 0-3, yosys-portability and full-ci-gate: success. Physical gPTP: skipped, which is not proof. | `receipts/hosted-status.tsv` |
| Hosted failure at `f909d6c4` (the target of this commit) | The same four rows failed to compile. Verilator reported `Cannot find file containing module: 'Entering'`, `'directory'`, `'Leaving'`, and both the maap and milan_dp runner directories. The campaign gave `52 failures: 4`. | `receipts/hosted-f909d6c4-shard1-maap-excerpt.log` |
| **GNU Make 4.3, parse-only derivation** | The binary is the hosted runner's version, sha256 `d78b8f1d099fbcfb6f2f49ab87223b9b68fb3956642f92d6ec6de812e8afa965`, staged in scratch. The head file is clean plain, under `w` and under `-j8`. Under `w` with a `-j8` recursive parent it stops at the guard (`non-files: make[1]:`). With the guard removed, the captured list has 122 words: `make[1]: Entering directory '.../maap'` and `make[1]: Leaving directory '.../milan_dp'` arrive despite `--no-print-directory`. The sibling `MAKEFLAGS=` form is clean in all four contexts. Under GNU Make 4.4.1, all variants are clean in all four contexts. | `receipts/make43-probe.log` |
| **GNU Make 4.3, real builds** | The head's own `integration-build` target, invoked as `mutants.py` invokes it (`make -j8 -s -C <suite> integration-build`) under `MAKEFLAGS=w`, gives rc 2 at the guard. The disposable remedy copy, with `MAKEFLAGS=` added to both captures and run from a `-j8` parent under `w`, gives build rc 0 and run rc 0 with `MAAP integration: 3 checks, 0 failures`. | `receipts/make43-build.log`, `make43-head-integration.log`, `make43-remedy-integration.log`, `make43-remedy-run.log` |
| `MAKEFLAGS=w make -C tb/verilator/maap`, GNU Make 4.4.1, pinned Verilator 5.050 | `KL_maap: 172 checks, 0 failures` and `== maap mutants: checks: 52 failures: 0 ==`, make rc 0. This is not a faithful reproduction of the hosted make: see above. | `receipts/campaign-makeflags-w.log`, `.rc` |
| Plain `make -C tb/verilator/maap`, GNU Make 4.4.1 | Same figures: 172/0 and 52/0, rc 0. | `receipts/campaign-plain.log`, `.rc` |
| Pre-fix vs head file, GNU Make 4.4.1, under `w` | **Pre-fix `f909d6c4` file:** build rc 2 with the hosted error class (`'make[1]:'`, `'Entering'`, `'directory'`, ...). **Head file:** build rc 0, run 3/0. So under 4.4.1 the flag is sufficient; under 4.3 in the jobserver context it is not. | `receipts/ab-prefix-f909.log`, `ab-head-b9b3.log`, `.rc` |
| Guard behaviour (GNU Make 4.4.1, parse-only) | The guard fires on `make[1]:` once the flag is removed under `w`. It also fires on an injected non-file word, an unexpanded glob and a command-line `DP_SRCS=not_a_file`. An existing directory and an empty list pass it (S1), but both fail at elaboration (Verilator exit 1). | `receipts/derive-probe.log`, `receipts/dir-empty-probe.log` |
| Other makefiles capturing nested make output | There are 9 `$(shell ... $(MAKE) ...)` captures in tracked `Makefile`/`.mk` files, and all 9 pass `--no-print-directory`. There are none in the submodules, and no `!=` or backtick captures. Of those 9, only `maap/integration.mk` (2) and `capture_coherence` (2) do not also clear `MAKEFLAGS=`. `capture_coherence` passes hosted shard 1/5 at this head; its campaign runs its builds under its own `BUILD_MAKEFLAGS`. | `receipts/nested-capture-census.log` |
| `w` propagation, GNU Make 4.4.1 | A plain top-level `make -C` does not put `w` into a recipe's `MAKEFLAGS`. | `receipts/makeflags-propagation.log` |
| Restore | Clean status, including ignored files. Index tree = head tree `d2c5eb6e`. `integration.mk` blob `727a038d` and mode 644 match the head. The three gitlinks equal their clean checkouts. Rechecked after the last probe. | `receipts/restore-check.log` |

## 3. Findings

### R558-3-F1 - BLOCKER - Conformance, Robustness, Tests - `tb/verilator/maap/integration.mk:8`, `:15` - the nested captures still collect directory lines on the hosted make; shard 1/5 fails at this head

- **Authority:**
  - Issue #696 acceptance 2 asks for a datapath-level check showing that the MAC changes the intervals, with planted defects. Its rows are `m4_datapath_clean`, `m4_reset_time_sampling`, `m5_datapath_ignores_link` and `m3_datapath_ignores_clock`.
  - AGENTS.md section 7 requires exact-head `verilator-suites` evidence on an RTL/tooling PR head.
  - This commit's stated purpose is to answer hosted run 38021886237.
- **Evidence:**
  - Hosted job 114140492769 at `b9b38961` concluded failure: `maap` has 4 in-suite failures. All four integration rows stop at `integration.mk:13 ... non-files: make[2]:` (`receipts/hosted-b9b38961-shard1-maap-excerpt.log`).
  - GNU Make 4.3 reproduces it only under inherited `w` together with a `-j8` recursive parent. There, the `$(shell)` child cannot use the jobserver and warns. Its stdout still carries `make[1]: Entering directory '<start dir>'` and `make[1]: Leaving directory '<-C dir>'`, although `--no-print-directory` is on its command line (`receipts/make43-probe.log`).
  - The same file passes under GNU Make 4.4.1 in every context, which is why the local campaigns pass.
  - Clearing the inherited flags for the capture removes the pollution under 4.3 and the integration builds and passes (`receipts/make43-build.log`). That is the pattern `pp_shadow/Makefile:107`, `milan_dp_mclk/Makefile:62,70` and `milan_dp_render/Makefile:86,91` already use; `milan_dp_mclk/Makefile:44-54` records why.
- **Impact:**
  - The mandatory hosted `verilator-suites` gate is red at this head.
  - The acceptance-2 datapath check and the M5/M3 datapath plants cannot be graded on the hosted runner. Locally they pass only because the local make differs.
  - The failure is loud, not a false pass: the guard names it.
- **Required outcome:** under the hosted runner's GNU Make 4.3, the derived source list and flag list carry only the datapath suite's own output. This must hold when the capture runs inside the recursive `-j` parent that `mutants.py` creates, with `w` inherited.
  - One way to get there is the sibling suites' `MAKEFLAGS=` prefix on both captures.
  - If inherited flags are cleared, decide how the job bound that `mutants.py` passes as `VERILATOR_JOBS=` reaches `print-dp-vflags`. Today it travels in `MAKEFLAGS`.
  - Keep the guard.
- **Verification:**
  - Hosted Verilator shard 1/5 and `verilator-suites` green at the corrected exact head, with `== maap mutants: checks: 52 failures: 0 ==` in the `suite-logs-1` maap log.
  - Locally, `scripts/make43_probe.sh` and `scripts/make43_build.sh` from this packet, with a GNU Make 4.3 binary: the head variant is clean in all four contexts, and the head `integration-build` gives rc 0.
  - A cold reviewer re-applies Conformance, Robustness and Tests at that head.

### R558-3-S1 - SUGGESTION - Robustness, Tests - `tb/verilator/maap/integration.mk:11-13` - the guard tests existence, not "file", and accepts an empty list

- **Evidence:** `$(wildcard)` matches directories. An injected `../milan_dp` passes, and so does an empty list (`receipts/derive-probe.log` §4).
  - The commit subject says "refuse non-file entries".
  - Both cases still fail at elaboration (`receipts/dir-empty-probe.log`, Verilator exit 1), and `mutants.py:165-168` counts a compile failure as escaped. So neither can produce a false pass.
- **Optional outcome:** refuse a directory entry and an empty list with the guard's own message.
- **Verification:** the §4 probes stop at the guard.

### R558-3-S2 - SUGGESTION - Tests - `tb/verilator/maap/mutants.py` - no in-suite arm builds the integration in the hosted shape

- **Evidence:** `capture_coherence/mutants.py` has an inherited-`MAKEFLAGS=w` arm. The maap campaign has none.
  - F1 also shows that `MAKEFLAGS=w` alone, on GNU Make 4.4.1, does not reproduce the hosted defect.
- **Optional outcome:** a regression row that builds the integration from a `-j` recursive parent with `w` inherited.
  - It is useful mainly on a GNU Make 4.3 host. The hosted shard already exercises that shape on every rtl-full run.

## 4. Prior public findings on this PR, resolved or retained at this head

| Finding | State at `b9b38961` | Basis |
|---|---|---|
| R558-1-F1 (MINOR, Docs) | Resolved at `f909d6c4` (R558-2, R559-2); still resolved | `docs/` is unchanged since `f909d6c4` |
| R559-1-F1 (MINOR, Tests) | Resolved; still resolved | The unit M5 loss/return check passes and `m5_restart_on_link_loss` is killed in both local campaigns. The hosted unit harness gives `172 checks, 0 failures` |
| R559-1-F2 (MINOR, Docs) | Resolved; still resolved | `docs/` unchanged |
| R559-1-F3 (MINOR, Docs, Tests) | Resolved; still resolved | `docs/` and `sim_main.cpp` unchanged |
| R558-2-R1, R559-2-R1 (RESIDUE, Docs, `MARK_II_AREA_PLAN.md:66-67` etc.) | Retained, wording only, on the manager's residue checklist | The file is unchanged |
| R558-1-S1 (SUGGESTION) | Applied at `f909d6c4` | — |
| R559-1-S1..S4 (SUGGESTION) | Retained, optional; no lens effect | — |

## 5. Lens results

- [R558] UNCLEAN Conformance - R558-3-F1 open.
  - Examined: `tb/verilator/maap/integration.mk` at `b9b38961`; issue #696 acceptance 2; the four datapath rows in `receipts/hosted-b9b38961-shard1-maap-excerpt.log`, `campaign-*.log` and `make43-build.log`.
  - Acceptance 2's datapath check passes locally under GNU Make 4.4.1, but it cannot build on the mandatory hosted runner at this head.
  - No other clause-bearing artifact changed. Acceptance 1 and 3 stand from earlier rounds. Acceptance 4 is the post-merge bench lane.
- [R558] PASS RTL - `git diff f909d6c4 b9b38961 -- hdl syn configs` (empty); `receipts/derive-probe.log` §1; `receipts/make43-probe.log`.
  - No RTL byte changed.
  - When the capture is clean, the elaborated set equals the datapath suite's list: 114 words, every one an existing file. The flag set is unchanged at 39 words.
  - The mutant `subst` reaches the build, which the three locally killed datapath plants show.
  - F1 is a build-derivation defect. It changes no RTL contract, so I do not record it under RTL.
- [R558] UNCLEAN Robustness - R558-3-F1 open.
  - Examined: `integration.mk:8-17`; `receipts/derive-probe.log` §1-6; `receipts/make43-probe.log` (4 contexts × 3 variants × 2 make versions); `receipts/dir-empty-probe.log`.
  - The captures are not robust to the inherited-flag and jobserver context of the hosted make.
  - The guard does convert that into a named stop.
- [R558] UNCLEAN Tests - R558-3-F1 open.
  - Examined: `tb/verilator/maap/mutants.py:151-237`; local campaigns `receipts/campaign-makeflags-w.log` and `campaign-plain.log` (52/0 each); the hosted maap logs at `f909d6c4` and at this head (52/4 each); `receipts/make43-build.log`.
  - The suite's own gate fails on the hosted runner at this head.
- [R558] PASS Docs - `docs/testing/TESTING.md:392-405`; `tb/verilator/maap/integration.mk:3`; commit `b9b38961` message.
  - The delta changes no documented contract, and the header comment is still true.
  - TESTING.md's submodule-census paragraph predates this PR, and already omits other `print-srcs` consumers. It is not a delta defect.
  - The commit is one line with no trailer (`CONTRIBUTING.md:402`). Its "refuse non-file entries" overstates the guard for directories (S1); a commit message is immutable history, so this is noted only.

## 6. Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R558-3-F1) | `integration.mk`; acceptance 2; the four datapath rows in the hosted, local and GNU Make 4.3 runs | R558-3 | b9b389611304850ea435b2056887568afe5e6bf4 |
| RTL | CLEAN | empty `hdl`/`syn`/`configs` delta; derived 114-word source set and 39-word flag set | R558-3 | b9b389611304850ea435b2056887568afe5e6bf4 |
| Robustness | UNCLEAN (R558-3-F1) | captures and guard under 11 GNU Make 4.4.1 parse probes and 12 GNU Make 4.3 parse probes; head/remedy builds under 4.3 | R558-3 | b9b389611304850ea435b2056887568afe5e6bf4 |
| Tests | UNCLEAN (R558-3-F1) | two local 52-row campaigns (52/0), unit harness 172/0, pre-fix/head A/B, hosted maap logs at `f909d6c4` and this head (52/4) | R558-3 | b9b389611304850ea435b2056887568afe5e6bf4 |
| Docs | CLEAN | TESTING.md census, integration.mk header, commit message; `docs/` unchanged since `f909d6c4` | R558-3 | b9b389611304850ea435b2056887568afe5e6bf4 |

- For RTL and Docs, every other artifact in scope is unchanged since `f909d6c4`, where R558-2 and R559-2 covered them clean. `f909d6c4` is an ancestor of this head.
- Conformance, Robustness and Tests must be covered again at the head that fixes F1.

## 7. Real limits

- I ran the maap suite only. No parent, PP, gPTP, Yosys, builder, firmware, docs or field bank was run in this round. Nothing outside `tb/verilator/maap/integration.mk` changed.
- There are no author receipts at this exact head; the commit is the manager's. No manager source bank ran at this head, and I claim none.
- The GNU Make 4.3 binary used for reproduction came from a local container image layer (sha256 above). Its behaviour matches the hosted log, but it is not the runner's binary.
- The remedy copy is a disposable probe that shows one way to meet the required outcome. I did not edit or commit anything to the branch.
- I ran no Docker or act replica. The current-dev merge candidate (dev `554e61d2`) was not built.
- Physical calibration was NOT RUN. Field skips are not hardware proof. Acceptance 4 (bench interop) is outside this round.
- Published campaign logs have the local simulator install prefix replaced by `<pinned-verilator-install>`. The result lines are byte-identical to the raw logs.

## 8. Pending manager duties

- Route R558-3-F1 to a fix at a new head. Then obtain hosted Verilator shard 1/5 and `verilator-suites` green at that exact head, and a re-review covering Conformance, Robustness and Tests.
- Own hosted acceptance. At this head, rtl-fast, docs and elaborate are success; rtl-full and `verilator-suites` are failure, from shard 1/5 only.
- Build and validate the current-dev merge candidate (source base `6aa25dec`, live dev `554e61d2`) at the merge turn, with receipts linked on the PR.
- Carry RESIDUE R558-2-R1 and R559-2-R1 to the residue checklist. S1 and S2 are optional.
- Merge requires two independent positive reviews at the merge head, the full CONTRIBUTING bar and explicit maintainer authorization.

R558-3 FINISHED
