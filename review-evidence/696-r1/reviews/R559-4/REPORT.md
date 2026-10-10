[R559] POSITIVE - exact head 30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f

# R559-4 - issue #696 / PR #706 - external independent review, delta round

- **Head:** `30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f`, tree `8dbd9df1994c92dfcc25d30c7f18cb6827e56a30`. Reviewed in a detached clean clone.
- **Source base:** `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`.
- **Delta:** `b9b38961..30073ee9` is one manager commit. It changes `tb/verilator/maap/integration.mk` only, +9/-2 (`receipts/delta-b9b38961-30073ee9.diff`). Since `f909d6c4`, nothing outside that file has changed.
- **Question:** does the commit fix the hosted GNU make 4.3 failure (R558-3-F1 = R559-3-F1)? Does it act on the empty-list guard suggestion (R558-3-S1 / R559-3-S1)?
- **Earlier rounds:** R558-1/2/3 and R559-1/2/3 stand for every artifact this commit does not touch.

## Verdict in one paragraph

The commit fixes the hosted failure, and I verified the fix by mechanism, by A/B and on the hosted runner.

- **Mechanism.** Both parse-time captures now run as `$(shell MAKEFLAGS= $(MAKE) -s --no-print-directory ...)`, so the nested make inherits no flag. I reproduced the hosted defect locally on the pre-fix `integration.mk`, under GNU make 4.3: an inherited print-directory flag together with an unusable jobserver gives `A.mk:13: *** datapath source list names non-files: make:.  Stop.`, rc 2. That is the hosted error shape. The head file passes in the same context (`receipts/jobserver-ab.log`, `receipts/jobserver-ab-prefix-error.log`). Under 4.4.1 neither file fails, so a 4.4.1 host cannot show the defect.
- **Hosted.** rtl-full run 38034648698 at this exact head concluded `success`. Verilator shard 1/5 passed, and so did `verilator-suites`. Its `suite-logs-1` `maap.log` reads `KL_maap: 172 checks, 0 failures` and `== maap mutants: checks: 52   failures: 0 ==`. All four datapath rows are `[ok]` with their named rejections. The tested merge ref is `1ab24ec3` = `554e61d2` + this head.
- **Local make 4.3 runs.** The full maap suite ran under GNU make 4.3 with inherited `MAKEFLAGS=w`: unit 172/0, mutants 52/0, rc 0. R558-3's two make 4.3 scripts are clean in all four contexts, and the integration build exits rc 0.
- **Empty-list guard.** The new guard refuses an empty or blank list with its own message.
- **Job bound.** The explicit `VERILATOR_JOBS=$(VERILATOR_JOBS)` reaches `print-dp-vflags`. Without it, `integration.mk`'s own default of 2 would collapse to `-j 0`.
- **No other change to the build.** The derived source list and flag set are byte-identical to the pre-fix ones.

No BLOCKER, MAJOR, MINOR or RESIDUE is raised. Two SUGGESTIONs are retained from earlier rounds.

## Reconstruction (public state only)

1. AGENTS.md (sections 3 and 5-8), CONTRIBUTING.md (by reference) and docs/README.md.
2. Issue #696, read for its frozen acceptance 1-4 and the manager rulings, as indexed in the issue thread. This delta reopens none of them.
3. The interface the delta relies on: `tb/verilator/milan_dp/Makefile:647-664` (`print-srcs`, `print-dp-vflags`, which echoes `GPTP_OFF_VFLAGS` with `-j $(VERILATOR_JOBS)`, default `?= 0` at `:32`).
4. The sibling consumers named by the new comment: `tb/verilator/milan_dp_mclk/Makefile:46-73`, `tb/verilator/milan_dp_render/Makefile:86-91` and `tb/verilator/pp_shadow/Makefile:107`.
5. The suite chain: `scripts/run_all_suites.sh:394` (`make -C <suite>`), `tb/verilator/maap/Makefile:27-29` and `tb/verilator/maap/mutants.py:152-168` (a plain `make -j8 -s -C ... integration-build ... VERILATOR_JOBS=<env or 0>`).
6. The diff and history (`git log f909d6c4..HEAD`: two manager commits, both to this one file).
7. Hosted evidence, first at the prior head (run 38027027728, `suite-logs-1` `maap.log` lines 343-375: four `non-files: make[2]:` refusals) and then at this head.
8. Prior public findings, read only after my own pass over the diff and my own probes (table below).

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE at this head.

### R559-4-S1 - SUGGESTION - Robustness, Tests - `tb/verilator/maap/integration.mk:19-21` - the non-file guard still admits a directory entry (retains the directory half of R558-3-S1 / R559-3-S1)

- **Evidence:** `$(wildcard)` matches directories. In a disposable tree, a `print-srcs` that names `adir`, `real.sv adir` or `../milan_dp` passes the guard under make 4.3 and under 4.4.1. Parsing ends normally and the run stops only at the recipe's first line (`receipts/dir-entry-probe.log`). The empty and blank cases now stop at `integration.mk:17: *** datapath source list is empty.` (`receipts/flags-guard-probe.log`).
- **Impact:** none on verdicts. A directory in the list fails at elaboration, and `mutants.py:165-168` counts a compile failure as escaped, so this cannot produce a false pass. The cost is a less direct diagnostic.
- **Optional outcome:** refuse directory entries at the guard, with its own message.
- **Verification:** the three directory cases in `scripts/dir_entry_probe.sh` stop at the guard.

### R559-4-S2 - SUGGESTION - Tests - `tb/verilator/maap/mutants.py` - no in-suite arm reproduces the hosted make 4.3 shape (retains R558-3-S2)

- **Evidence:** the hosted defect needs a make 4.3 that sees an inherited print-directory flag and an unusable jobserver (`receipts/jobserver-ab.log`). On a 4.4.1 host, the inherited-`MAKEFLAGS=w` suite run cannot show it.
- **Impact:** a local 4.4.1 run cannot catch a regression of this fix. The hosted shard exercises the real shape on every rtl-full run, and it is now green.
- **Optional outcome:** a regression row that builds `integration-build` under an inherited `w` plus an unusable `--jobserver-auth`, which is meaningful on a make 4.3 host.

## Prior public findings, resolved or retained at this head

| Finding | State at `30073ee9` | Basis |
|---|---|---|
| R558-3-F1 (BLOCKER) = R559-3-F1 (BLOCKER), hosted make 4.3 capture pollution | **Resolved** | The hosted shard 1/5 `maap.log` at this head reads 172/0 and 52/0, with the four datapath rows `[ok]` (`receipts/hosted-shard1-maap-excerpt.log`), and `verilator-suites` passed (`receipts/hosted-status.tsv`). Locally, the pre-fix file fails and the head passes in the defect's exact context (`receipts/jobserver-ab.log`). |
| R558-3-S1 / R559-3-S1 (SUGGESTION), the guard accepts an empty list and directories | **Empty half resolved; directory half retained** as R559-4-S1 | `receipts/flags-guard-probe.log` (empty and blank lists refused); `receipts/dir-entry-probe.log` (directories still admitted) |
| R558-3-S2 (SUGGESTION), no hosted-shape arm in the suite | **Retained** as R559-4-S2 | unchanged `mutants.py` |
| R558-1-F1 (MINOR, Docs) and R559-1 F1-F3 (MINOR, Tests/Docs) | Resolved at `f909d6c4` (R558-2 and R559-2 POSITIVE). Still resolved, since nothing outside `integration.mk` has changed since then. | `git diff --stat f909d6c4..30073ee9` |
| R558-2-R1 / R559-2-R1 (RESIDUE, `docs/design/MARK_II_AREA_PLAN.md:66-67`) | Unchanged. Carried by the manager on the residue checklist, and not re-opened here. | the file is untouched since `f909d6c4` |
| R558-1-S1 (SUGGESTION) | Unchanged, optional | the file is untouched |

## Lens results (artifact-specific)

```text
[R559] PASS Conformance - tb/verilator/maap/integration.mk:12-25 at 30073ee9; hosted suite-logs-1 maap.log:246,343-350 (merge ref 1ab24ec3) - the issue #696 datapath acceptance evidence (M4 clean, M4 reset-time sampling, M5 link return, M3 clock seed) now builds and runs on the hosted toolchain; each mutant is killed by its named check, and the unit harness grades 172/0. No protocol behaviour changed (the delta touches no hdl/ file).
[R559] PASS RTL - receipts/derive-equal.log; git diff b9b38961..30073ee9 - no RTL is changed. The integration build elaborates the same 114-file source list and the same 39-word flag set as before (sha256 identical, prefix vs head), so the datapath that the M3/M4/M5 rows exercise is unchanged. Only the inherited-flag path to that list changed.
[R559] PASS Robustness - receipts/flags-guard-probe.log, receipts/jobserver-ab.log, receipts/chain-ab.log, receipts/make43-probe.log - the captures are now independent of inherited MAKEFLAGS: w, -j8, w+j8, -n, and w plus an unusable jobserver, under make 4.3 and 4.4.1. An empty list, a blank list, a missing file, a leaked "make[1]:" word, a failed source derivation and a failed flag derivation each stop at their own $(error). A directory entry is admitted but fails later (R559-4-S1, SUGGESTION).
[R559] PASS Tests - receipts/suite43.log (+ .rc), receipts/make43-build.log, receipts/make43-head-integration.log, receipts/make43-remedy-run.log, receipts/hosted-shard1-maap-excerpt.log - the full maap suite under make 4.3 with inherited MAKEFLAGS=w gives unit 172/0 and mutants 52/0, rc 0. The integration build under make 4.3 exits rc 0 and runs at 3 checks / 0 failures. Hosted shard 1/5 gives 172/0 and 52/0, and verilator-suites passed. The A/B controls show that each probe can fail: the pre-fix file fails under make 4.3 with an unusable jobserver and under an inherited -n, and removing the explicit job pass-through drops the default bound from 2 to 0 (receipts/chain-ab-echo.log, prefix rows).
[R559] PASS Docs - tb/verilator/maap/integration.mk:8-11; docs/testing/TESTING.md:592 - the new comment's claims are checked: the make 4.3 leak matches the hosted log and the local A/B; milan_dp_mclk, milan_dp_render and pp_shadow use the same MAKEFLAGS= form; the job bound is passed explicitly. No authoritative document describes the derivation mechanism, so none needed an update.
```

### Job bound (manager's question)

- **Explicit pass-through.** `print-dp-vflags` receives the bound. With `VERILATOR_JOBS` set on the parent command line (5), in the environment (7) or through the suite target chain (3), the derived flag set carries that `-j` value under both makes (`receipts/flags-guard-probe.log`, "bound" rows).
- **No bound given.** The flag set carries `integration.mk`'s own default, `-j 2`. The pre-fix file gives `-j 0` here (`receipts/chain-ab-echo.log`).
- **Make 4.3 integration build at `VERILATOR_JOBS=8`.** The build reports `on 8 threads` (`receipts/make43-head-integration.log`).
- **The mutation campaign.** `mutants.py:163` always passes `VERILATOR_JOBS=<env or '0'>` on the command line. When the environment does not set it, the campaign's bound is therefore its own default of 0, which the delta does not change. That is the campaign's existing design, not a loss caused by the cleared flags.

## Reviewer-owned completion ledger (this round)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | integration.mk:12-25; hosted maap.log 172/0 and 52/0 with the datapath rows; issue #696 acceptance (earlier rounds stand for untouched artifacts) | R559-4 | 30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f |
| RTL | CLEAN | delta diff (no hdl); derive-equal (identical source list and flags, prefix vs head) | R559-4 | 30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f |
| Robustness | CLEAN (S1 is a SUGGESTION) | guard fault injection under both makes; inherited-flag A/B (w, -j8, -n, unusable jobserver) | R559-4 | 30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f |
| Tests | CLEAN (S2 is a SUGGESTION) | make 4.3 full suite (172/0, 52/0); R558-3's make 4.3 probe and build scripts; hosted shard 1/5 and verilator-suites | R559-4 | 30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f |
| Docs | CLEAN | integration.mk:8-11 comment against the siblings and the hosted log; TESTING.md maap row | R559-4 | 30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f |

## Executed evidence (all in this packet)

- **`scripts/make43_probe.sh` and `scripts/make43_build.sh`:** R558-3's scripts, byte-identical (sha256 `988d0630...` and `2a0f6d7f...`), run with GNU make 4.3.
  - All three probe variants report `SRCS-WORDS=114 NONFILE=[]` in the plain, w, j8 and w+j8 contexts, rc 0.
  - The head integration build exits rc 0. The "remedy" arm's substitution no longer matches at this head, so it rebuilds the head file: rc 0, `MAAP integration: 3 checks, 0 failures`.
- **`scripts/suite43.sh`:** the full suite (`make all`) under make 4.3 with `MAKEFLAGS=w` and the pinned Verilator 5.050, giving `receipts/suite43.log` (172/0, 52/0) and `.rc` 0.
- **`scripts/flags_guard_probe.sh`:** the captures and the job bound in four contexts, under both makes, plus guard fault injection in a disposable tree.
- **`scripts/jobserver_ab.sh`:** the pre-fix file against the head file, with an inherited print-directory flag and an unusable jobserver. This is the hosted defect's exact mechanism.
- **`scripts/chain_ab.sh` and `scripts/chain_ab_echo.sh`:** the run_all_suites -> mutants -> integration.mk chain, dry and real (`VERILATOR=echo`), using untracked sibling copies of the suite directory that are removed afterwards.
- **`scripts/chain_py.sh`:** the same chain with the python layer.
- **`scripts/dir_entry_probe.sh`:** directory entries in the source list.
- **`scripts/derive_equal.sh`:** the derived source list and flag set, prefix against head.
- **`scripts/hosted_check.sh`:** read-only queries of run 38034648698 and its `suite-logs-1` artifact (zip sha256 `e7d78b6a...`).
- **`receipts/restore-check.log`:** the clone is at HEAD and tree. The porcelain status is empty, with no untracked or new ignored files. Index (mode, blob, path) equals the HEAD tree, the worktree matches the index, and the gitlinks are `gptp-processor 5dce647a`, `protocol-processor 2ad2f845`.

## Real limits

- **The make 4.3 binary used locally is an upstream build, not the runner's distribution build.** It reproduces the defect only when the unusable jobserver is supplied directly (`jobserver-ab`). Through the natural local chain, the pre-fix file passes (`chain-ab-echo`, `chain-py`), because the jobserver stays usable there. The hosted shard at this head is therefore the authoritative proof that the real runner shape is fixed, and it is green.
- **Hosted provenance.** The hosted run tests the merge ref `1ab24ec3` = `554e61d2` + head. That base is neither the source base `6aa25dec` nor the live dev `e8454e27` named by the manager.
- **Scope of this round.** It is a delta review. It ran only the maap suite and the targeted probes, with no parent, PP, gPTP, Yosys or builder bank. No manager source bank exists at this head, and none is claimed or inferred.
- **No hardware.** Physical calibration was NOT RUN. The skipped "Physical gPTP (nightly and manual)" context is a skip, not hardware proof.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `6aa25dec`, live dev `e8454e27`), with builder and native banks, at the merge turn, and link the receipts on the PR.
- Own hosted and act acceptance for this head and for the candidate.
- Carry R558-2-R1 / R559-2-R1 (RESIDUE) on the residue checklist.
- R559-4-S1 and R559-4-S2 are optional.
- A merge needs explicit maintainer authorization and the full completion bar, including the second positive review for this head.

R559-4 FINISHED
