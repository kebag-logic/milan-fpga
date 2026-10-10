[R559] NEGATIVE - exact head b9b389611304850ea435b2056887568afe5e6bf4

External independent review, round R559-3, issue #696 / PR #706. This is a delta review of `f909d6c4..b9b38961`, which is one commit to `tb/verilator/maap/integration.mk`. Tree `d2c5eb6e64ec20bb8291ac2aa00e105a137c7b9b`.

## Verdict in one paragraph

The commit does not fix the hosted failure it answers. At this exact head, hosted Verilator shard 1/5 fails again: run 38027027728, job 114140492769, merge ref `98be85e7` = live dev `554e61d2` + this head. The `maap` suite reports `checks: 52   failures: 4`, the same four datapath mutants as at `f909d6c4`. The new guard now refuses the list loudly with `integration.mk:13: *** datapath source list names non-files: make[2]:.`, which fails closed. But the datapath arm of the campaign still never builds on the hosted runner.

I reproduced this locally at the exact head with the runner's own GNU make (Ubuntu `make 4.3-4.1build2`): same four refusals, same 52/4 tally. I also isolated the mechanism in a seven-line case. The polluting text is not the print-directory banner that `--no-print-directory` controls. Under GNU make 4.3, a nested make that inherits a print-directory flag and an unusable jobserver (from the mutant driver's `make -j8`) prints `Entering directory '<dir before -C>'` / `Leaving directory` while it emits its "jobserver unavailable" warning, and `--no-print-directory` does not suppress that. The prescribed validation (`MAKEFLAGS=w make -C tb/verilator/maap`) passes, but only under GNU make 4.4.1, which does not have this path. It therefore cannot reproduce the hosted condition.

One BLOCKER (R559-3-F1). The verdict is NEGATIVE.

## Reconstruction (public state only)

- Read AGENTS.md (sections 3, 5-8), the issue #696 body and its frozen acceptance 1-4, the PR #706 conversation, and the round-start comment 6094139505. I read prior review comments only after my own pass over the diff.
- Delta: `git diff f909d6c46..b9b389611` changes only `tb/verilator/maap/integration.mk`, +5/-2:
  - `--no-print-directory` is added to both `$(shell $(MAKE) ...)` captures, at `integration.mk:8` and `:15`.
  - A guard is added at `integration.mk:12-14` that refuses any word of `DP_SRCS` that `$(wildcard)` does not return.
  - The commit subject is one line with no trailers. Its parent is `f909d6c4`.
- The mutant driver is `tb/verilator/maap/mutants.py:151-226`. It runs `make -j8 -s -C <maap> integration-build` for four datapath cases (`m4_datapath_clean`, `m4_reset_time_sampling`, `m5_datapath_ignores_link`, `m3_datapath_ignores_clock`), and a compile failure counts as ESCAPED. `Makefile:29` recurses with `$(MAKE) -f integration.mk build`. The hosted runner calls `make -C tb/verilator/maap` from `scripts/run_all_suites.sh:394`, with stdout to a log.
- The tooling identity check (`receipts/directory_entry_fails_closed.txt`) shows Verilator 5.050 rev v5.050, the scoped pinned build. The local host make is GNU Make 4.4.1. The runner-equivalent make is GNU Make 4.3, Ubuntu package `4.3-4.1build2`, sha256 in `receipts/make43_identity.txt`. It was copied from a container layer already on the host into scratch and was not installed.

## What I executed

| Run | Result | Receipt |
|---|---|---|
| Hosted condition as prescribed, make 4.4.1: `MAKEFLAGS=w make -C tb/verilator/maap` | unit `KL_maap: 172 checks, 0 failures`; mutants `checks: 52 failures: 0`; rc 0; 4 datapath cases `[ok]` | `receipts/w2.log`, `w2.rc` |
| Plain `make -C tb/verilator/maap`, make 4.4.1 | 172/0; 52/0; rc 0 | `receipts/plain2.log`, `plain2.rc` |
| **Exact head, runner-equivalent make 4.3, `make -C tb/verilator/maap` with stdout to a file (as `run_all_suites.sh`)** | unit 172/0; **mutants `checks: 52 failures: 4`**, rc 2; all four datapath cases `integration.mk:13: *** ... non-files: make[2]:` | `receipts/m43.log`, `m43.rc` |
| Hosted shard 1/5 at this head (artifact `suite-logs-1`) | `FAIL maap`, `in-suite failures: 4`; the same four `non-files: make[2]:` refusals | `receipts/hosted_b9b38961_shard1_maap.log`, `_summary.txt`, `_TARGET_SHA` |
| Hosted shard 1/5 at `f909d6c4`, for comparison | Verilator given `Entering`, `directory`, `'/…/tb/verilator/maap'`, `Leaving`, `'/…/tb/verilator/milan_dp'` as sources | `receipts/hosted_f909d6c4_shard1_maap.log` |
| Chain emulation, make 4.3 (`make -C` → python → `make -j8 -s -C … integration-build` → `$(MAKE) -f integration.mk`) | rc 2, `non-files: make[2]:`. A disposable widened error showed the first list word is `make[2]: Entering directory '<…>/tb/verilator/maap'`, the directory BEFORE `-C` | `receipts/chain43.log`, `scripts/chain43.sh` |
| Minimal mechanism, no repository files | make 4.3 with `MAKEFLAGS='w -j8 --jobserver-auth=97,98'` captures `make: Entering directory '<dir>' payload make: Leaving directory '<dir>/sub'` despite `--no-print-directory`. `w` alone, or the jobserver alone: clean. With `MAKEFLAGS=` cleared on the nested call: clean. make 4.4.1: clean in every row | `receipts/minimal_jobserver_leak.txt`, `minimal_banner_leak.txt`, `scripts/minimal_*.sh` |
| Disposable probe (restored): `MAKEFLAGS=` prefixed on both captures, the sibling idiom of `pp_shadow/Makefile:107`, `milan_dp_mclk/Makefile:62,70`, `milan_dp_render/Makefile:86,91` | make 4.3 chain `integration-build rc=0`; `MAAP integration: 3 checks, 0 failures` | `receipts/chain43_makeflags_probe.log`, `makeflags_probe.diff` |
| f909d6c4 `integration.mk` under `MAKEFLAGS=w`, make 4.4.1 (negative control) and head (control) | f909: rc 2, `%Error: Cannot find file containing module: 'make[2]:'` …; head: build rc 0, harness 3/0 | `receipts/f909ctl.*`, `headctl*.{log,rc}` |
| Guard probes, parse time, make 4.4.1 | Fires on make chatter (`make[1]:`), a non-file word, a glob word, and a command-line `DP_SRCS=` override. The status check still fires on a failing nested make. It does **not** fire on a directory word or an empty list | `receipts/guard_probes.txt`, `scripts/guard_probes.sh` |
| Directory word reaching Verilator | `%Error: Cannot find file containing module: '../milan_dp'`, rc 1 (fails closed) | `receipts/directory_entry_fails_closed.txt` |
| Tree scan: 128 tracked make files, parent and submodules | 9 `$(shell … make …)` captures, all with `--no-print-directory`; no continuation-split capture | `receipts/nested_make_scan.txt`, `scripts/scan_nested_make.sh` |
| Inherited-flag side effects | `make -n -C maap integration-build`: rc 2, `non-files: echo`. `make -pqrR` of `integration.mk`: rc 2, which is pre-existing and the same for `capture_coherence/Makefile`. `integration.mk` does not name `adp_shape_defaults.svh`, so the shape inventory does not read it | `receipts/flag_leak_probe.txt` |
| Hosted contexts at this head | `rtl-fast`, `elaborate`, `docs` success. `rtl-full` failure: Verilator shard 1/5 failure; shards 0, 2, 3, 4 and Yosys 0-3 success; `verilator-suites` failure; `yosys-portability` success; Physical gPTP skipped (not executed). The merge ref differs from the head in 42 files, none under `tb/verilator/maap`, `tb/verilator/milan_dp`, `run_all_suites.sh` or `rtl.yml` | `receipts/hosted_contexts.txt`, `merge_ref_delta.txt` |

A first local attempt lost its `/tmp/maap-mutants-*` work directories mid-campaign in both concurrent runs at once. This was an external cleanup on the shared host, not this change: the unit harness had already passed 172/0. The receipts are `receipts/{w,plain}.attempt1_tmp_removed.log`. All later runs used private TMPDIRs under scratch.

## Findings

### R559-3-F1 - BLOCKER - Tests, Robustness, Conformance - `tb/verilator/maap/integration.mk:8`, `:15` (with `:12-14`) - the derived source list is still polluted on the hosted toolchain; the datapath mutant arm never builds

- **Authority/evidence:**
  - AGENTS.md section 7 requires exact-head `verilator-suites` evidence; at this head it is a failure.
  - Issue #696 acceptance 1 requires planted defects caught by suite checks.
  - Acceptance 2 requires a datapath-level check showing that different MACs draw different intervals. In the suite, that check runs only as the campaign's `m4_datapath_clean` case.
  - Hosted shard 1/5 at `b9b38961` reports `maap mutants: checks: 52 failures: 4`, with all four datapath cases refused at `integration.mk:13` naming `make[2]:`. The exact-head make 4.3 reproduction and the minimal case show the cause. Under GNU make 4.3, a nested make inheriting a print-directory flag plus an unusable jobserver writes `Entering/Leaving directory` to stdout around its jobserver warning, and `--no-print-directory` does not suppress it.
  - The commit's validation used make 4.4.1, which never takes that path. So `MAKEFLAGS=w make -C tb/verilator/maap` passing locally (`receipts/w2.log`) does not show that the hosted condition is fixed.
- **Impact:** the campaign is the only place the real-datapath harness runs, so the required hosted gate cannot show M3, M4 or M5 being killed at datapath level, or the acceptance-2 datapath check passing. `verilator-suites` is red at the exact head, and every later PR head that keeps this derivation will fail the same way. The guard makes the failure explicit, which is an improvement over `f909d6c4`, but it does not let the campaign run.
- **Required outcome:** the datapath arm builds and passes under the hosted invocation chain on GNU make 4.3: `run_all_suites.sh` → `make -C tb/verilator/maap` → `mutants.py` `make -j8 -s -C … integration-build` → `$(MAKE) -f integration.mk`. The derived source and flag lists must not depend on flags inherited from the caller. For reference only, not as a prescribed design: clearing inherited flags on the nested call, as `pp_shadow`, `milan_dp_mclk` and `milan_dp_render` already do, passed this chain in a disposable probe (`receipts/chain43_makeflags_probe.log`).
- **Verification:**
  1. Hosted Verilator shard 1/5 reports `PASS maap`, and `verilator-suites` succeeds at the new exact head.
  2. Locally at that head, a GNU make 4.3 run of `make -C tb/verilator/maap` with stdout to a file gives 172/0 and 52/0, with all four datapath cases `[ok]`.
  3. `scripts/minimal_jobserver_leak.sh`-style evidence, or the act replica, shows the inherited-jobserver case is covered. A regression check that runs under make 4.3 with `w` plus an inherited jobserver would keep this from returning.

### R559-3-S1 - SUGGESTION - Robustness - `tb/verilator/maap/integration.mk:12-14` - the guard admits directories and an empty list

The commit subject says it refuses "non-file entries", but `$(wildcard)` also returns directories. A directory word (`../milan_dp`) passes the guard (115 words), and so does an empty derived list (0 words); see `receipts/guard_probes.txt`. Both still fail closed later: Verilator rejects a directory (`receipts/directory_entry_fails_closed.txt`), and an empty list cannot elaborate `milan_datapath`. So this changes no outcome, only the diagnostic. Optional: also refuse directories and an empty list, so the refusal names the problem at derivation time.

### Observation for the manager, not a finding against this PR

`tb/verilator/capture_coherence/Makefile:101,105` uses the same `--no-print-directory`-only capture. Its hosted runs pass today. If its parse-time captures ever run under an inherited print-directory flag plus a `-j` jobserver on make 4.3, it is exposed to the same mechanism. AGENTS section 4 routes this to a separate public Issue if the manager judges it worth tracking.

## Prior public findings: resolved or retained at this head

Since `f909d6c4` only `integration.mk` changed, so the state recorded at `f909d6c4` carries forward for every other file.

- R558-1-F1 (MINOR, Docs): resolved; `docs/design/MAAP_FABRIC.md` is unchanged since `f909d6c4`.
- R559-1-F1 (MINOR, Tests): resolved; `sim_main.cpp` and `sim_integration.cpp` are unchanged.
- R559-1-F2 (MINOR, Docs): resolved; `MARK_II_AREA_PLAN.md` is unchanged.
- R559-1-F3 (MINOR, Docs, Tests): resolved; the files are unchanged.
- R558-2-R1 and R559-2-R1 (RESIDUE, `MARK_II_AREA_PLAN.md:66-67`): retained as residue, unchanged.
- R558-1-S1: applied. R559-1-S1 to S4: retained as optional.
- R559-2's `Tests` coverage at `f909d6c4` no longer holds: `integration.mk` is in that lens's scope and changed. It is re-covered here and found UNCLEAN.

## Lens results with evidence

- `[R559] BLOCKER Conformance - issue #696 acceptance 1-2; tb/verilator/maap/mutants.py:200-226 (only invocation of the datapath harness); receipts/hosted_b9b38961_shard1_maap.log - the datapath-level acceptance evidence does not execute in the required hosted gate (R559-3-F1)`
- `[R559] PASS RTL - git diff f909d6c46..b9b389611 (no file under hdl/, no submodule gitlink changed: protocol-processor 2ad2f845, gptp-processor 5dce647a, verilog-axis 48ff7a7e unchanged) - the RTL scope is byte-identical to f909d6c4, where R559-2 covered it clean; the headctl datapath build at this head elaborates and passes 3/0`
- `[R559] BLOCKER Robustness - tb/verilator/maap/integration.mk:8,15 under GNU make 4.3 with inherited w and jobserver; receipts/m43.log, minimal_jobserver_leak.txt - derivation depends on caller flags (R559-3-F1); guard edge cases are SUGGESTION R559-3-S1`
- `[R559] BLOCKER Tests - tb/verilator/maap/{integration.mk,mutants.py,Makefile}; receipts/m43.log, hosted_b9b38961_shard1_maap.log, w2.log, plain2.log - the campaign fails 52/4 on the runner toolchain; the prescribed reproduction cannot show the hosted condition (R559-3-F1)`
- `[R559] PASS Docs - delta touches no document; PR #706 body (no claim about this commit); docs/testing/TESTING.md:592 maap row (no count or mechanism claim); integration.mk:3 header - nothing to update for this delta; RESIDUE R558-2-R1/R559-2-R1 retained`

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue #696 acceptance 1-2, `mutants.py:151-226`, hosted shard 1/5 maap log, make 4.3 run | R559-3 | `b9b389611304850ea435b2056887568afe5e6bf4` |
| RTL | CLEAN | delta diff (no RTL or gitlink change); RTL as covered at `f909d6c4` by R559-2; head datapath build 3/0 | R559-3 (delta); R559-2 for the unchanged RTL at ancestor `f909d6c460344527f102f24b8e7a77f09959e755` | `b9b389611304850ea435b2056887568afe5e6bf4` |
| Robustness | UNCLEAN (F1) | `integration.mk:8-18`, guard probes, make 4.3 chain and minimal cases, flag-leak probe | R559-3 | `b9b389611304850ea435b2056887568afe5e6bf4` |
| Tests | UNCLEAN (F1) | `integration.mk`, `mutants.py`, `Makefile`; make 4.4.1 w/plain campaigns; make 4.3 campaign; hosted shard 1/5 at this head and at `f909d6c4`; negative control | R559-3 | `b9b389611304850ea435b2056887568afe5e6bf4` |
| Docs | CLEAN (RESIDUE R558-2-R1 / R559-2-R1 only) | delta, PR body, `TESTING.md:592`, `integration.mk:3` | R559-3 | `b9b389611304850ea435b2056887568afe5e6bf4` |

## Real limits

- I did not run the act replica (not allowed in this round). The make 4.3 used here is the runner-equivalent Ubuntu package taken from a local image layer, not the hosted runner itself. The run log does not print the runner's make version. The match rests on the Ubuntu 24.04 image and on an identical failure signature.
- No manager source bank exists at this head, and none is claimed. The current-dev merge candidate was not built by me. The hosted shard ran the PR merge ref `98be85e7`, which does not differ from the head on the failing path.
- I did not inspect any other `rtl-full` shard's logs beyond their conclusions. Physical gPTP was skipped and is not evidence. Physical calibration was NOT RUN, and field skips are not hardware proof.
- I did not determine the make 4.3 internals beyond the observed behaviour and the minimal case.

## Pending manager duties

- Route R559-3-F1 back to the author lane. Re-review is required at the corrected head, with hosted shard 1/5 and `verilator-suites` green there.
- Run the act replica at the next head. Its Ubuntu image should exercise the make 4.3 path that make 4.4.1 hosts do not.
- Carry RESIDUE R558-2-R1 / R559-2-R1 on the residue checklist.
- Decide whether the `capture_coherence` exposure note merits its own Issue.
- Build and validate the current-dev merge candidate at the merge turn.

## Receipts and reproduction

The receipts are in `receipts/` and the scripts in `scripts/`, all listed in `MANIFEST.sha256`. Host-specific prefixes are replaced by `<scratch>`, `<probe>` and `<verilator-root>`. The hosted `maap.log` copies are verbatim. Every probe edit was made in disposable copies under scratch. The review clone was verified after the probes:

- `HEAD` = `b9b389611304850ea435b2056887568afe5e6bf4`
- tree and index tree = `d2c5eb6e64ec20bb8291ac2aa00e105a137c7b9b`
- 0 porcelain lines, and the worktree equals `HEAD` in bytes and modes
- the `integration.mk` blob is `727a038d…` in both
- the gitlinks are unchanged

See `receipts/clone_integrity.txt`.

R559-3 FINISHED
