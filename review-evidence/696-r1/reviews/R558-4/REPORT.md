[R558] POSITIVE - exact head 30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f

Round R558-4, internal cleared-context review of issue #696 / PR #706. Exact head `30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f`, tree `8dbd9df1994c92dfcc25d30c7f18cb6827e56a30`.

This is a delta review from `b9b38961` to `30073ee9`. The delta is one manager commit to `tb/verilator/maap/integration.mk` (+9/-2). It answers R558-3-F1 = R559-3-F1 (BLOCKER, the hosted GNU Make 4.3 leak) and R558-3-S1 (SUGGESTION, empty-list guard).

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open. All five lenses are clean at this head.

- The two derivations now clear inherited flags. The hosted datapath arm builds and kills its mutants: shard 1/5 reports `== maap mutants: checks: 52   failures: 0 ==`, and `verilator-suites` is green.
- Under GNU Make 4.3 with `MAKEFLAGS=w`, the local suite gives unit 172/0 and campaign 52/0.
- A control reproduces the hosted failure shape. The b9b38961 capture form leaks under it and is refused; the head form is clean.
- The job bound reaches `print-dp-vflags`.

One RESIDUE (PR body wording) and two optional SUGGESTIONs are recorded.

## Reconstruction

- Read in order: `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`, then the body of issue #696 (frozen acceptance 1-4; acceptance 2 is the datapath-level M4 check that `integration.mk` builds).
- Next: `git diff 6aa25dec..30073ee9` scope, `git diff b9b38961..30073ee9`, and `git diff --stat f909d6c4..30073ee9`. The last touches only `integration.mk` (`receipts/diff_since_f909d6c4.txt`).
- Then the `print-srcs` / `print-dp-vflags` authority in `tb/verilator/milan_dp/Makefile:32,83-101,648-664` and the callers `tb/verilator/maap/Makefile:11,27-29` and `mutants.py:151-166,199-226`.
- Then hosted runs at this head and at `b9b38961`.
- Prior public findings were read only after the independent pass below.

## The delta

`integration.mk:12` and `:22` now run `$(shell MAKEFLAGS= $(MAKE) -s --no-print-directory -C ../milan_dp ...)`. `:22` also passes `VERILATOR_JOBS=$(VERILATOR_JOBS)`. The new `:16-18` refuses an empty list. The non-file guard (`:19-21`) and the `.SHELLSTATUS` guards (`:13-15`, `:23-25`) are unchanged.

| Check | Result | Receipt |
|---|---|---|
| Hosted, exact head | Run 38034648698 (`pull_request`, headSha `30073ee9`, merge ref `1ab24ec3` = `30073ee9` + dev `554e61d2`): Verilator shards 0-4/5 success, `verilator-suites` success ("every worker succeeded at 1ab24ec3"), `yosys-portability` success, Yosys shards success. rtl-fast, docs, elaborate success. Physical gPTP skipped (a skipped context, not executed). In suite-logs-1 `maap.log`: `KL_maap: 172 checks, 0 failures`, `== maap mutants: checks: 52   failures: 0 ==`, and the four datapath rows `m4_datapath_clean rc=0`, `m4_reset_time_sampling`, `m5_datapath_ignores_link`, `m3_datapath_ignores_clock` all `[ok]` | `receipts/hosted_checks_30073ee9.txt`, `hosted_30073ee9_run38034648698_suite-logs-1_maap.log`, `..._TARGET_SHA`, `hosted_merge_ref.txt` |
| Hosted, prior head (failure shape) | Run 38027027728 at `b9b38961`: `make[2]: warning: jobserver unavailable` then `datapath source list names non-files: make[2]:`. The four datapath rows ESCAPED | `receipts/hosted_b9b38961_run38027027728_suite-logs-1_maap_excerpt.log` |
| R558-3 parse probe, GNU Make 4.3 | All four contexts (plain, w, -j8, w+-j8) give rc 0, 114 words, no non-file. The same holds under 4.4.1. At this head the script's "sibling" sed is a no-op, so its three variants are the head file and the head minus the guard | `scripts/make43_probe.sh`, `receipts/make43_probe.log`, `make441_probe.log` |
| R558-3 build script, GNU Make 4.3 | Head `integration-build`, invoked as `mutants.py` invokes it under `MAKEFLAGS=w`: rc 0. Second build rc 0, run `MAAP integration: 3 checks, 0 failures` | `scripts/make43_build.sh`, `receipts/make43_build.summary`, `make43-*.log` |
| Full maap suite, GNU Make 4.3, `MAKEFLAGS=w`, `make -C <suite>` | Suite rc 0; unit 172/0; campaign 52/0 including the four datapath rows | `scripts/suite43.sh`, `receipts/suite43.summary`, `suite43.log` (home path redacted to `<home>`) |
| Leak control, GNU Make 4.3 | With the hosted shape (`MAKEFLAGS='w -j8 --jobserver-auth=97,98'`, an advertised but closed jobserver), the b9b38961 capture form fails `names non-files: make:` (rc 2) and the head form is clean (rc 0, 114 words). `w` alone and an unavailable jobserver alone do not leak. GNU Make 4.4.1 does not leak in any of the three | `scripts/leak_control.sh`, `receipts/leak_control.log` |
| Hosted shape, real build and run, GNU Make 4.3 | `integration-build` under that MAKEFLAGS: `jobserver unavailable` warning once, rc 0. `maap_integration`: 3 checks, 0 failures | `scripts/hosted_shape_build.sh`, `receipts/hosted_shape.summary`, `hosted-shape-*.log` |
| Full hosted chain, build stubbed | `make -C <suite>` → python → `make -j8 -s -C <suite> integration-build` → `-f integration.mk` → `$(shell)`, under auto-w and `MAKEFLAGS=w`, GNU Make 4.3 and 4.4.1: rc 0, 114 `.sv`/`.v` words on the flag line, `--build -j 5` | `scripts/chain_probe.sh`, `receipts/chain_probe.log` |
| Job bound reaches print-dp-vflags | GNU Make 4.3 with `VERILATOR_JOBS=5` on the outer line: head gives `--build -j 5` in plain and w+j8 contexts. A copy without the explicit pass gives `--build -j 0`. Without the variable the head gives `-j 2` (`integration.mk:5`) | `scripts/guard_probe.sh`, `receipts/guard_probe_make43.log` (and `_make441.log`) |
| Content unchanged | Under `MAKEFLAGS=w`, the head's `DP_SRCS` and `DP_FLAGS` match the datapath suite's own `print-srcs` and `print-dp-vflags VERILATOR_JOBS=5` byte for byte (114 words; 39 words, quoting kept), on GNU Make 4.3 and 4.4.1 | `scripts/equality_probe.sh`, `receipts/equality_probe.log` |
| Guard power | Fake derivation suites, GNU Make 4.3 and 4.4.1, plain and w+j8: an empty list stops with `datapath source list is empty`; a directory line and a non-file word stop with `names non-files`; a failing derivation stops with `derivation failed`. A directory entry is still accepted | `receipts/guard_probe_make4*.log`, `directory_entry_probe.log` |

Tools: GNU Make 4.3 at the briefed path, sha256 `d4f77b74…3598`. Its digest differs from the binary R558-3 recorded, so it is a different 4.3 build. Also GNU Make 4.4.1 and pinned Verilator `5.050 2026-07-01 rev v5.050`, identity checked (`receipts/tool_identity.txt`).

## Findings

### R558-4-R1 - RESIDUE - Docs - PR #706 body, "Status" and "How to get into the same state" - the stated head is two commits stale
- **Evidence:** the body says "review ready at `f909d6c4…`" and `git rev-parse HEAD   # f909d6c460344527f102f24b8e7a77f09959e755`. Its review-round table ends at round 2. The branch tip is `30073ee9`, which adds `b9b38961` and `30073ee9` (both `integration.mk` only). A cold reviewer who follows the recipe gets a mismatching hash.
- **Impact:** the fix is wording only. No figure, count, command, measurement or verdict in the body changes, because 172 / 3 / 52 rows hold at this head.
- **Exact fix:**
  - Replace both `f909d6c460344527f102f24b8e7a77f09959e755` occurrences with `30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f`.
  - Add a round-3 row: "R558-3-F1 / R559-3-F1 (Conformance, Robustness, Tests): the two datapath derivations clear inherited make flags and pass the job bound explicitly; an empty list is refused | `b9b38961`, `30073ee9`".
- **Verification:** read the PR body.

### R558-4-S1 - SUGGESTION - Robustness, Tests - `tb/verilator/maap/integration.mk:19-21` - a directory entry still passes the non-file guard
`$(wildcard)` matches directories (`receipts/directory_entry_probe.log`). An empty list is now refused. A directory in the list would still fail loudly at Verilator elaboration, not silently. This is optional and carries over the directory half of R558-3-S1.

### R558-4-S2 - SUGGESTION - Docs - `tb/verilator/maap/integration.mk:8-10` - the comment could name the trigger exactly
The comment says the leak happens "under an inherited w flag inside a recursive -j parent". On GNU Make 4.3 the leak needs both an inherited `w` and a jobserver advertised to the capture but unavailable there. The hosted log shows the `jobserver unavailable` warning. With a working jobserver (w+j8 locally) the old form does not leak (`receipts/leak_control.log`, `make43_probe.log`). Naming the jobserver condition is optional. The fix is right for either reading.

### Observation (no finding)
- **Job bound defaults:** `integration.mk:5` (`VERILATOR_JOBS ?= 2`) is now live. A direct `make integration-build` with no bound builds the datapath with `-j 2`, where it used to get the datapath suite's `-j 0`. `mutants.py:166` always passes `VERILATOR_JOBS` (default `0`), so the campaign and hosted behaviour are unchanged. The bound only affects compile parallelism.
- **Other cleared overrides:** clearing MAKEFLAGS also drops the other command-line overrides. Callers pass `MAAP_RTL`, `MDIR` / `DP_MDIR` and `VERILATOR`, and none of these feeds the two print targets (`milan_dp/Makefile:83-101,648-664`). The byte-identical equality probe confirms this.

## Prior public findings at this head

| Finding | Status at `30073ee9` | Evidence |
|---|---|---|
| R558-3-F1 = R559-3-F1 (BLOCKER; Conformance, Robustness, Tests) | **Resolved** | Hosted shard 1/5 52/0 with the four datapath rows `[ok]`, and `verilator-suites` green at this head. GNU Make 4.3 suite 52/0. The leak control kills the old form and the head form passes |
| R558-3-S1 / R559-3-S1 (SUGGESTION) | Partly applied (empty list refused); directory half retained as R558-4-S1, optional | `guard_probe_make4*.log`, `directory_entry_probe.log` |
| R558-3-S2 (SUGGESTION, no in-suite hosted-shape arm) | Retained, optional | `mutants.py` unchanged |
| R558-1-F1, R559-1-F1, R559-1-F2, R559-1-F3 (MINOR) | Still resolved | `docs/`, `sim_main.cpp`, `sim_integration.cpp`, `mutants.py` unchanged since `f909d6c4`. Hosted and local unit 172/0 |
| R558-2-R1 / R559-2-R1 (RESIDUE, `MARK_II_AREA_PLAN.md:66-67`) | Retained on the residue checklist | File unchanged |
| R558-1-S1 applied; R559-1-S1..S4 (SUGGESTION) | Retained, optional | - |

## Lens results

- [R558] PASS Conformance - `tb/verilator/maap/integration.mk:12-25` at `30073ee9`; issue #696 acceptance 2; hosted run 38034648698 suite-logs-1 `maap.log:343-350` - Under the hosted runner's make, the datapath-level M4 check and the M3/M5 datapath kills are built and graded again: 4/4 `[ok]`, 52/0. Locally under GNU Make 4.3 the same holds (`suite43.log:343-350`). The derived source list and flags equal the datapath suite's authority byte for byte, so the check still elaborates the shipping integration.
- [R558] PASS RTL - `receipts/diff_since_f909d6c4.txt` (no `hdl/`, gitlink or recipe change since `f909d6c4`); `integration.mk:32-36` (unchanged parameter set); `receipts/equality_probe.log` - No RTL changed. The elaboration flags reaching Verilator equal `print-dp-vflags` (GPTP_OFF_VFLAGS) exactly, with only the `-j` compile bound caller-set. The model parameters are unchanged.
- [R558] PASS Robustness - `integration.mk:12-25`; `receipts/leak_control.log`, `guard_probe_make43.log`, `guard_probe_make441.log`, `hosted_shape.summary`, `chain_probe.log` - Caller flags no longer reach the captures:
  - w, jobserver-unavailable, -j8, auto-w and the full chain are all clean on GNU Make 4.3 and 4.4.1.
  - Empty, directory-line, non-file and failing derivations each stop with a named error.
  - The job bound survives the cleared flags.
  - The open directory case is optional (S1).
- [R558] PASS Tests - `tb/verilator/maap/{integration.mk,mutants.py,Makefile}`; `receipts/suite43.log` (172/0, 52/0, GNU Make 4.3, `MAKEFLAGS=w`); `make43_build.summary`; `make43_probe.log`; hosted `maap.log` 52/0 at this head - The campaign's four integration rows are the regression for this defect. They failed hosted at `b9b38961` (excerpt receipt) and pass at this head. My control shows the old form fails under the hosted shape, so the evidence can tell the fix from the defect.
- [R558] PASS Docs - `integration.mk:8-11` checked against `milan_dp_mclk/Makefile:62,70`, `milan_dp_render/Makefile:86,91`, `pp_shadow/Makefile:107` (all use `MAKEFLAGS=`, as claimed); `docs/testing/TESTING.md:397,592` (no mechanism or count claim affected); commit `30073ee9` message (one line, no trailer, `CONTRIBUTING.md`); PR #706 body - Only wording residue: R558-4-R1 (stale head in the PR body) and optional S2.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `integration.mk`; issue #696 acceptance 2; hosted suite-logs-1 `maap.log`; local GNU Make 4.3 suite; equality probe | R558-4 | 30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f |
| RTL | CLEAN | diff since `f909d6c4` (no RTL); `integration.mk:32-36`; flag/source equality with `milan_dp` print targets | R558-4 | 30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f |
| Robustness | CLEAN (S1 optional) | captures and guards under GNU Make 4.3 / 4.4.1 parse probes, leak control, full chain, hosted-shape build and run | R558-4 | 30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f |
| Tests | CLEAN | GNU Make 4.3 suite 172/0 and 52/0; R558-3 probe and build scripts; old-form control; hosted shard 1/5 52/0 | R558-4 | 30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f |
| Docs | CLEAN (RESIDUE R558-4-R1, R558-2-R1 / R559-2-R1) | `integration.mk:8-11`, sibling Makefiles, `TESTING.md:397,592`, commit message, PR body | R558-4 | 30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f |

The lenses for the unchanged rest of the lane stand as covered at `f909d6c4` by R558-2 / R559-2. `30073ee9` descends from `f909d6c4`, and the only file changed since is `integration.mk`, which this round re-covered under all five lenses.

## Real limits

- **No manager source bank at this head.** I neither claim nor infer one. Source-head execution evidence here is my own focused runs plus the hosted exact-head contexts.
- **Merge base of the hosted run:** it validated the merge ref `1ab24ec3` (`30073ee9` into dev `554e61d2`). That is neither the source base `6aa25dec` nor the live dev `e8454e27`.
- **Make binary:** the GNU Make 4.3 used is the briefed local build (sha256 `d4f77b74…`), not the hosted runner's binary. With it, the hosted leak reproduces only once an advertised jobserver is unavailable, which I synthesised with closed descriptors. The hosted green run is the authority for the runner itself.
- **Not run:** full parent, PP, gPTP, Yosys, builder and documentation banks, coverage, differential, firmware and field banks. Their inputs are unchanged since `f909d6c4`; hosted docs and Yosys contexts are green at this head.
- **Hardware:** physical calibration NOT RUN. Field skips are not hardware proof. The Physical gPTP context was skipped, not executed.
- **Restore:** after the probes the clone is at exact head bytes. The index digest is identical to baseline, there are no untracked or ignored files, the worktree and index match HEAD, the five gitlinks match HEAD, and the submodule worktrees are clean (`receipts/restore_check.txt`).

## Pending manager duties

- Build and validate the current-dev merge candidate (builder and native banks) against live dev `e8454e27`, and link its receipts.
- Own hosted and local-replica acceptance at the exact head.
- Carry RESIDUE R558-4-R1 and R558-2-R1 / R559-2-R1 to the residue checklist. S1, S2 and R558-3-S2 are optional.
- Obtain the external positive review at this head before merge. Acceptance 4 (bench interop) remains the post-merge bench lane.

R558-4 FINISHED
