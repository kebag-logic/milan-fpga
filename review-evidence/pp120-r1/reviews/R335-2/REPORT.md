[R335] POSITIVE - exact head 83c84b19e09d397ed2eb6f5ace337686ce0ef86b

# R335-2 external independent review: processor issue #120 / PR #121, round 3 (delta)

- Exact head `83c84b19e09d397ed2eb6f5ace337686ce0ef86b`, tree `7e6d16f3b5dfd3c4f1a0bc9ddb872f1156a1aea9` (verified, `receipts/90-clone-integrity.txt`).
- Delta judged: `a9b7874d..83c84b19` (one commit on `a9b7874d`). Round 1 of this reviewer covered `a9b7874d` in full, against source base `0922e43408f891fc0b84a84691df86b4fd0f1c0d`.
- Scope sources: issue #120 body (frozen acceptance), the maintainer comments on the issue (acceptance-3 correction 5845334300, round-2 scope 5845451831, round-3 scope 5846001897), PR #121 body, the donor `README.md`, `docs/` and `tb/pp_top/README.md`, the parent port parser (`scripts/check_port_contracts.py` and `scripts/sv_ports.py` at parent `7eb3b0d4`), and the public evidence at `kebag-logic/milan-fpga@356583ef6ba0d99eec2b7a8d006664a47497d8bc/review-evidence/pp120-r1`. The donor repository has no `AGENTS.md` or `CONTRIBUTING.md`. The parent's `CONTRIBUTING.md` port rule is taken from the gate's own docstring.
- Tool: Verilator 5.050. The assigned pinned path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. A substitute shim with the identical exec line to the host's `372-manager-r2` pinned shim reports `Verilator 5.050 2026-07-01 rev v5.050`. Binary hashes are in `receipts/00-tool-identity.txt`. g++ 16.2.1, Python 3.14.7.

## What the delta does

`git diff --name-status a9b7874d 83c84b19` touches two files, both harness-only (`receipts/30-delta-scope.txt`):

1. `tb/pp_top/pp_top_wrap.sv:312-332`. The two new harness outputs (`aecp_name_wr_o`, `dbg_name_live_we_o`) and their own `//!` contracts now sit before the existing effect-strobe bundle, followed by a blank line. The bundle's `//!` run (lines 321-328) again sits directly above its four declarations (`dbg_dyn_writes_o`, `aecp_nvm_stb_o`, `aecp_nvm_mark_o`, `dbg_notify_enq_o`, lines 329-332). No port was renamed, resized or re-typed, and no instance connection or assign changed.
2. `tb/pp_top/sim_main.cpp:9744`. `static void run_name_writes(H& h)` became `[[maybe_unused]] static void run_name_writes(H& h)`. The default-build call at `:9782` (`if (!gsi_only) run_name_writes(h);`) is retained. The fixture build (`#ifdef PP_TOP_SRP_DOM_DEF_VID`, `:9772`) still runs section DV alone. The attribute is standard C++17, and the Makefile builds with `-std=c++17`.

The `hdl/`, `syn/`, `docs/` and `scripts/` tree ids are identical at `a9b7874d` and `83c84b19` (`receipts/30-delta-scope.txt`), so production RTL, the documentation and the donor gate scripts are byte-for-byte unchanged in this round. `git diff --check` is clean for the delta and for the whole PR. Nothing outside `tb/pp_top` references `pp_top_wrap`, so the port reorder cannot change any positional binding.

## Verification performed (reviewer-executed, this head)

| # | Check | Result | Receipt |
|---|---|---|---|
| 1 | Parent parser `check_port_contracts.scan_ports` (parent `7eb3b0d4`) on `tb/pp_top/pp_top_wrap.sv` | base 209/**162**, round 2 211/165, **head 211/162** undocumented. All six effect/name ports are documented at head; at round 2, three bundle ports were undocumented. Top, engine, store and `desc_mem_guard/wrap.sv` counts are unchanged from round 2. | `receipts/20-scan-ports.txt`, `scripts/20-scan-ports.py` |
| 2 | `make -C tb/pp_top run` (both builds) at head, from a pristine `git archive` export | rc 0. Default 7731/0, fixture 20/0, canonical `7751 checks: 7751 PASS, 0 FAIL`. The `NW: 85 checks, 0 failures` line appears in the default build. **0 C++ compiler warnings** across both builds. | `receipts/10-pp_top-head/` |
| 3 | Same at `a9b7874d` (round 2) | rc 0, same tallies. **1 C++ warning**: `sim_main.cpp:9744:13: 'void run_name_writes(H&)' defined but not used [-Wunused-function]`, in the fixture build. | `receipts/10-pp_top-a9b7874d/` |
| 4 | Head vs round 2: simulation stdout | Default, fixture and `--name-writes-only` simulation output is **byte-identical**. The Verilator `%Warning` set (63, `-Wno-fatal`, PINMISSING/PINCONNECTEMPTY harness-intent) is identical with line numbers stripped, and equals the base set. | `receipts/11-compare-a9b7874d-vs-head.txt`, `receipts/11-compare-base-vs-head.txt` |
| 5 | `make -C tb/pp_top name-writes` at head | rc 0, `NW: 85 checks, 0 failures` | `receipts/10-pp_top-head/name-writes.log` |
| 6 | Shipped `tb/pp_top/name_wr_mutant.py` at head | golden PASS; command-decode mutant builds, completes and fails the required `NW EIGHT`, `NW LOCKED` and `NW ABORT` pulse-count checks (34 failures in total); restored PASS; rc 0. All three builds are warning-free. | `receipts/40-shipped-mutant*` |
| 7 | Donor gates in a scratch clone at head: `scripts/lint_hdl.sh`, `make check`, `gen_matrix.py --check`, `fixture-guards-test` (the fixture guards also ran inside #2) | all rc 0 | `receipts/60-donor-gates/` |
| 8 | Parent consumer commands at parent `7eb3b0d4` + processor gitlink staged at `83c84b19` + a reviewer-reconstructed consumer patch (open `.aecp_name_wr_o()` with a rationale comment in `KL_pp_shadow.sv`; a `name_wr_mutant.py` DUT-reader disposition in `measure_test_evidence.py`) | **11 of 12 executed, all rc 0**: 01 C++ idiom, 02 Py idiom, 03 xvlog (4 == ratchet), 04 RTL source lists, 05 pp_srcs, 07 pp_shadow (3 × 402/0), 08 port contracts (protocol-processor 111 <= 111), 09 naming, 10 test evidence (0 unexplained readers, 3 <= 3 wall-clock files), 11 docs_check, 12 lint_rtl (90 <= 90). **06 `sw/builder/test_builder.py` did not complete**: it was stopped at the 585 s cap of this session's foreground limit (rc 124, no verdict). See Limits. | `receipts/50-consumer/`, `receipts/50-parent-consumer.patch`, `receipts/51-builder-delta-relevance.txt` |
| 9 | Robustness probe: delete the default-build `run_name_writes(h)` call in a disposable copy | `make name-writes` rc 0 with `0 checks, 0 failures` and 0 compiler warnings. The shipped `name_wr_mutant.py` refuses (golden "missing required verdict", rc 1). See S1. | `receipts/70-drop-call-probe/`, `scripts/70-drop-call-probe.sh` |
| 10 | Hosted checks at the exact head | push run 36241197950 and pull_request run 36241199616, workflow `hdl`: `suites`, `docs-gates` and `portability` all **executed** and succeeded, with no skipped context. Hosted `pp_top` 7751/0; hosted suite total 1,014,722 checks, 0 failing. | `receipts/80-hosted-checks.txt` |
| 11 | Public evidence integrity (`author-r3`) | 53 entries in the top `MANIFEST.json` match their published hashes. The 7 `MANIFEST.sha256` mismatches are exactly the `path_redacted` entries. `head.txt` = exact head. The author's gates and 12 consumer commands report rc 0. | `receipts/81-public-evidence.txt` |
| 12 | Review clone restored | HEAD/tree exact; porcelain status (with ignored) empty; index mode+blob identical to the HEAD tree (248 entries); worktree blob hashes equal HEAD blobs; no gitlinks in the donor. | `receipts/90-clone-integrity.txt` |

## Findings

No open BLOCKER, MAJOR or MINOR finding.

### S1 - SUGGESTION - Robustness, Tests
- **Where:** `tb/pp_top/sim_main.cpp:9744` (`[[maybe_unused]]`) together with `tb/pp_top/Makefile:61-62` (`name-writes` target).
- **Evidence:** in a disposable copy with the `:9782` call deleted, `make name-writes` returns 0 and prints `[build default, ...] 0 checks, 0 failures` with no compiler warning (`receipts/70-drop-call-probe/summary.txt`). Before this round, the same deletion would at least have produced a non-fatal `-Wunused-function` in the default build. With the attribute, a dropped call is silent at compile time and the focused target passes vacuously. The shipped mutation script does catch it (its golden arm requires the `NW:` line and refuses), so the risk is limited to someone relying on the focused target alone. The vacuous focused target was already present in round 2; the attribute only removes the last compile-time hint.
- **Impact:** low. The acceptance bar for round 3 ("warning-free in both builds, scenario still running in the default build") is met.
- **Suggested outcome (processor residue, not required for this PR):** either guard the definition with `#ifndef PP_TOP_SRP_DOM_DEF_VID` instead of `[[maybe_unused]]` (the default build keeps the diagnostic, and the fixture build stays warning-free), or make `name-writes` refuse a run without a nonzero `NW:` tally.
- **Verification:** rerun `scripts/70-drop-call-probe.sh`. The focused target should then fail or warn.

## Prior public findings at this head

- **R335-1 F1** (this reviewer, round 1, MINOR; `run_name_writes` unused in the `PP_TOP_SRP_DOM_DEF_VID` fixture build, which added a `-Wunused-function` warning): **CLOSED**. At `a9b7874d` the fixture build emits exactly that warning (`receipts/10-pp_top-a9b7874d/summary.txt`). At head, both builds emit 0 C++ warnings (`receipts/10-pp_top-head/summary.txt`), the default build still runs `NW: 85 checks, 0 failures`, and the simulation output is byte-identical to round 2 (`receipts/11-compare-a9b7874d-vs-head.txt`).
- **R334-1 F1** (other reviewer, round 1, MINOR; the harness effect-port `//!` bundle was detached by the two new ports, and the parent parser reported 165 against 162): **CLOSED**. The parent parser reports 162 undocumented for `pp_top_wrap.sv` at head, equal to base, and all four bundle ports plus both new ports are documented (`receipts/20-scan-ports.txt`).
- Round-1 SUGGESTIONs (R335-1 S1 store unit-suite pin and S2 §8.1 combinational note; R334-1 S1 store unit-suite pin, S2 README "independently" wording and S3 §8.1 combinational note) were routed by the maintainer to the processor residue (issue comment 5846001897). The delta does not touch `docs/`, `tb/desc_store` or `tb/pp_top/README.md`, so they stand as residue suggestions. They are non-blocking and are not re-litigated here.
- Maintainer round-2 parent-gate items (issue comment 5845451831; 1 long C++ function, 2 undocumented Python functions, 3 port contracts, 4 wall-clock dependence) remain **resolved** at this head. Parent consumer commands 01, 02, 08 (processor 111 <= 111) and 10 (0 unexplained readers, 3 <= 3 wall-clock files) return 0 (`receipts/50-consumer/`), and the harness side of item 3 is now also clean (R334-1 F1 above).

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #120 acceptance 1-3 and the maintainer corrections/round scopes; round-3 items 1 and 2 met exactly (162 undocumented, both builds warning-free, scenario in the default build); `hdl/` tree id unchanged, so there is no behaviour change and the NVM mark timing is untouched; consumer bar 11/12 executed green, with the 12th covered under Limits | R335-2 (delta) on top of R335-1 (full at `a9b7874d`) | `83c84b19e09d397ed2eb6f5ace337686ce0ef86b` |
| RTL | CLEAN | Delta has no production RTL (`hdl/` and `syn/` tree ids identical to round 2); harness `pp_top_wrap.sv` reorder is declaration-only with no binding change; identical Verilator warning set; `lint_hdl.sh` 0; parent xvlog 4 == ratchet; parent `lint_rtl` 90 <= 90; pp_shadow elaborates with the open port | R335-2 + R335-1 | `83c84b19e09d397ed2eb6f5ace337686ce0ef86b` |
| Robustness | CLEAN (S1 suggestion only) | Warning-freedom in both builds; dropped-call probe; shipped-mutant refusal of a vacuous golden; parent port and test-evidence ratchets; hosted executed jobs | R335-2 + R335-1 | `83c84b19e09d397ed2eb6f5ace337686ce0ef86b` |
| Tests | CLEAN (S1 suggestion only) | `pp_top` both builds 7731 + 20 = 7751/0; NW 85/0 in the default and focused runs; simulation stdout byte-identical to round 2; shipped decode mutant killed on the required checks, with golden and restored passing; fixture guards; pp_shadow 3 × 402/0 | R335-2 + R335-1 | `83c84b19e09d397ed2eb6f5ace337686ce0ef86b` |
| Docs | CLEAN | `//!` contracts in `pp_top_wrap.sv:312-332` (parent parser); `tb/pp_top/README.md` NW section still accurate (unchanged; its reproduction commands were rerun); `docs/` tree unchanged; `make check` 0; parent `docs_check` 0; parent naming ratchet 0 | R335-2 + R335-1 | `83c84b19e09d397ed2eb6f5ace337686ce0ef86b` |

## Real limits

- **Parent command 06 (`sw/builder/test_builder.py`) was not completed by this reviewer.** The author's run took 688 s, which exceeds this session's 10-minute foreground limit, and the run stopped at 585 s with no verdict (rc 124). Mitigation, not proof: the builder reads only processor `hdl/` and `docs/` paths (`receipts/51-builder-delta-relevance.txt`), and both trees are byte-identical between `a9b7874d` and `83c84b19`. The author's published round-3 run reports rc 0 at this head, with one calibration arm NOT RUN for a missing implementation report. The manager's bank at this head is stated to pass.
- The consumer patch is a **reviewer reconstruction**. The manager-supplied patch bytes (sha256 `1de2a73a…`) are not public. The reconstruction matches the published diffstat (2 files, +2/+3) and intent, but its exact wording may differ. The merge-turn candidate must use the manager's patch or the real #502 connection.
- Only the suites the delta can affect were rerun (`tb/pp_top`, plus lint and docs gates). The full donor `run_suites.sh` bank, Yosys and area runs were not rerun here, as assigned. Their inputs outside `tb/pp_top` are unchanged, and the hosted suite total at this head is 1,014,722/0.
- The manager's full source static/builder and native banks were not located as a separate directory in the named public evidence tree, which holds the author-r3 packet. They are taken as stated in the assignment.
- Physical calibration was NOT RUN. Field skips are not hardware proof. No hardware was used.

## Pending manager duties

- Build and validate the final current-dev candidate at the merge turn (source base `0922e434`, live dev `7eb3b0d4`) with the manager's consumer patch, including the full builder command 06.
- Own hosted and act acceptance.
- Route S1 to the processor residue if desired.
- Publish this report and the files listed in `MANIFEST.sha256`.

## Receipts and scripts (listed in MANIFEST.sha256)

- `scripts/10-pp_top-builds.sh`: pristine-export build and run of both `pp_top` builds plus `name-writes` at one revision. The only deviation from the committed recipe is Verilator `-j 8` instead of `-j 0`, to respect the job budget.
- `scripts/11-compare.py`: compares warnings and simulation output between two such runs.
- `scripts/20-scan-ports.py`: the parent's `scan_ports`/`declarations` over PR-touched files at base, round 2 and head.
- `scripts/50-parent-consumer.sh`: the 12 consumer argument vectors in the scratch parent.
- `scripts/70-drop-call-probe.sh`: the S1 probe.
- `receipts/00`-`90`: raw logs and summaries as cited above. `receipts/50-consumer/06.log` is empty, because the builder's buffered stdout was lost when the 585 s cap stopped it.
- Scratch trees (exports, the parent copy, builds) are under `scratch/` and are not published.

R335-2 FINISHED
