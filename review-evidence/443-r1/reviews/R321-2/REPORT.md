[R321] POSITIVE - exact head 5beebb7c7edd908d08be34e52286c9eee441f5b3

# R321-2: external delta review of PR #561 (issue #443)

- Exact head `5beebb7c7edd908d08be34e52286c9eee441f5b3`, tree `f1210ce331ebf00f39187ca02021f85d66b4ee2c`. Its parent is round 1's head `c9bbb03cc3d4da9c6ee28996b91addbb081efa7e`. Source base `0755923d983218ca6ca9db6891a558cbe6425b8d`.
- The executor is [A301]. Scope comes from the round-2 assignment (issue comment 5826779078), items 1-5. That assignment also records the VERSION decision.
- The delta touches 10 files: +110/-17. No file under `hdl/`, `configs/`, `syn/` or any submodule changed. The `hdl` tree hash is `d4284df5` at both heads (`receipts/delta-scope.txt`).
- The raw delta's sha256 is `ce765acb...99b4`. It equals the `delta_sha256` in the executor's public `validation-head.json`.
- Round 1's ledger stands for everything outside this delta. I still re-applied all five lenses at this head. For RTL, the check is that the RTL is byte-identical to round 1's head and that the unchanged RTL reproduces under the new benches.

## Verdict summary

All five of my round-1 MINOR findings are closed in the tree, and so are the three MINOR findings of the concurrent round-1 review (R320-1). I reproduced each closure with an executable check or by reading the artifact, and none was moved to another Issue.

- The delta adds no new defect.
- One optional suggestion (S1) is recorded. It does not affect coverage.
- All five lenses are CLEAN at this head.

## Round-1 findings: status at this head

| Finding | Status | Evidence at `5beebb7c` |
|---|---|---|
| R321-1 F1 (Tests, Docs): CSR bench asserts `0x8DC` unmapped | **CLOSED** | The stale check is gone. `sim_main.cpp:1224-1225` now checks the neighbours `0x8E0` and `0x8F4`. `sim_main.cpp:1429-1449` grades the word with a driven `i_render_status`: tie reads zero, reset word `0x100`, all fields `0xA5C30216`, write ignored, talker and out-of-range zero, full-width rails `0xFFFF0100`. The reset tie is explicit (`:325`). All three N=1 executables pass 380/380 (`receipts/csr-bench-all.log`). Dropping the `RENDER_STAT` read-window term fails `RENDER_STAT driven prefill reset word` (`receipts/probe-csr-bench.jsonl`, `drop_read_window@main`). |
| R321-1 F2 (Tests): `STRM_SEL[9]` not graded | **CLOSED** | My round-1 mutant `csr_row_select_as_window_aclk`, re-run unchanged, is now **CAUGHT** at `RENDER-CSR: bit 9 preserves talker rejection` (got 65550, expected 0). The check is at `sim_aclk.cpp:404-405`. The campaign also plants the mutant itself (`render_csr_controls.py:62-65`) and requires that named failure, 4/4 (`receipts/render-csr-controls.log`). `sim_win.cpp:700-718` grades bit 9 with nonzero listener indices at `N_LISTENERS_P=4`. It catches the window mutant and a stricter variant that keeps direction but forces listener 0 (`lsn0_keep_dir@win`). |
| R321-1 F3 (Tests, Docs): campaign missing from TESTING.md | **CLOSED** | `TESTING.md:265` names the target, its command, and who must run it: the owners of `render_status_w`, the connections in `milan_datapath.sv`, the decode and selection in `milan_csr.sv`, the taps in `KL_render_setpoint.sv`, `sim_aclk.cpp` and the campaign itself. |
| R321-1 F4 (Conformance, Docs): no VERSION bump or recorded deferral | **CLOSED** | The recorded decision is assignment item 4 (5826779078). `CHANGELOG.md:31-39` has an Unreleased entry naming `RENDER_STAT` at `0x8DC`. It says VERSION stays `0x0002_0060`, that the release step owns the minor bump, and that this follows the `GPTP_DROPE[31:16]` precedent (`CHANGELOG.md:133-135`). `REGISTER_MAP.md:1945-1948` repeats the deferral, and says VERSION alone cannot identify the addition before the bump. `milan_csr.sv:196` still holds `0x0002_0060`, as decided. |
| R321-1 F5 (Docs): no `0x8DC` group-index row | **CLOSED** | `REGISTER_MAP.md:242` has the row: `RENDER_STAT`, RO live, selected listener plus global rails, structural zero without the stage, "VERSION minor remains `0x0060`". The note matches F4's decision. `gen_toc --check` and `--verify-anchors` pass. |
| R320-1 F1 (Tests, Docs, Conformance): same stale bench contract | **CLOSED** | See R321-1 F1. Its required nonzero index on a multi-listener elaboration is met by `sim_win` (all four indices, 115/115). Aliasing every index to listener 0 fails `RENDER_STAT selected NxN listener word` (`alias_listener0@win`). |
| R320-1 F2 (Conformance, RTL, Docs): VERSION | **CLOSED** by route (b) | The manager decision is recorded in 5826779078 and linked from both the 0x8DC section and the CHANGELOG. The section now states the identification limit instead of implying one. |
| R320-1 F3 (Docs): group index | **CLOSED** | See R321-1 F5. |
| R321-1 S1, S2; R320-1 S3, S4 (optional) | taken | S1 and S3: `REGISTER_MAP.md:1957-1961` covers the reset assumption and the shared-selector snapshot and coordination caveat. S2: the PR body calls the datapath decrease "unattributed" and says it makes "no physical area or timing claim". S4: the PR body discloses the TDM frame-pin wording change. |

## Findings

No open BLOCKER, MAJOR or MINOR finding.

### S1 SUGGESTION (Tests): the new neighbour reads cannot see a RENDER_STAT alias

- **Where:** `tb/verilator/csr/sim_main.cpp:1224-1225`. Both reads run in `reserved_inert_csr_gap()`, while `i_render_status` is still tied to zero. `render_status_word()` drives the input only later (`:1429`).
- **Evidence:** I planted a mutant that decodes `0x8E0` as a second copy of `RENDER_STAT`: an extra case label plus a read-window term. It **survives** 380/380 (`receipts/probe-csr-bench.jsonl`, `neighbour_alias@main`).
- **Why only a suggestion:** The labels are true at this head. The checks still catch a neighbour that aliases any other non-zero source. The assignment asked only that the neighbour checks be kept, and the decode is an exact case match.
- **Optional outcome:** Repeat the two neighbour reads inside `render_status_word()` while the input is driven non-zero. The `neighbour_alias@main` mutant would then fail by name.

## Independent evidence (reviewer-run, this head)

| Check | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/csr` (five executables) | rc 0: 380/380, 380/380, 115/115, 38/38, 380/380. It matches the executor's published counts | `receipts/csr-bench-all.{log,rc}` |
| `make -C tb/verilator/milan_dp render-csr-controls` | rc 0, campaign 4/4. Clean 63/63. Wrong-fill caught (got 256, expected 262). Bit-9 window mutant caught (got 65550, expected 0). Absent stage 32/32 | `receipts/render-csr-controls.{log,rc}` |
| `make -C tb/verilator/milan_dp aclk` (default leg) | rc 0, 189/189, with 46 `RENDER-CSR` lines including both bit-9 checks | `receipts/aclk-default.{log,rc}` |
| Round-1 probes, script byte-identical (sha256 `baca481a...6c1a`) | Both clean controls PASS: aclk 63/63, multi 64/64. Rails from underruns, prefill/converged swap, direction ignored, bit 9 zeroes, read window dropped, and listener-0 alias are all CAUGHT by name. `csr_row_select_as_window_aclk` is now CAUGHT; it SURVIVED in round 1. `..._multi` still SURVIVES, because that bench is unchanged and the aclk and `sim_win` legs now grade the semantic | `receipts/probe-mutants.jsonl`, `receipts/probe-row-select.jsonl`, `receipts/probes/probe-*.log` |
| Round-2 CSR-bench probes (`scripts/probe_csr_bench.py`) | Clean `main` 380/380 and `win` 115/115. **CAUGHT by name:** `window_sem@win`, `lsn0_keep_dir@win`, `ignore_direction@{main,win}`, `alias_listener0@win`, `drop_read_window@{main,win}`, `rails_truncated@{main,win}`. **Survived, and why:** `window_sem@main`, `alias_listener0@main` and `lsn0_keep_dir@aclk` survive by construction, because a single-listener shape cannot tell those selections apart and the 4-listener bench catches each one. `neighbour_alias@main` survives (S1) | `receipts/probe-csr-bench.jsonl`, `receipts/probe-csr-bench-aclk.jsonl`, `receipts/probes/probe2-*.log` |
| Docs gates | rc 0: `gen_toc --check`, `--verify-anchors`, `--selftest`; `docs_check` in git and no-git modes; doc style; doc paths; em dash against the base | `receipts/docs-*.log`, `receipts/gates.rc` |
| Static gates | rc 0: `lint_rtl --check`; SV, C++ and Python idiom; port contracts; RTL source lists; `measure_test_evidence --check` and `--selftest`; `git diff --check` against the base and against round 1 | `receipts/static-*.log`, `receipts/gates.rc` |
| Hosted checks at this head (read 05:11:47Z) | 17 success, 1 skipped (`Physical gPTP (nightly and manual)`), 2 in progress (`Verilator shard 1/5`, `4/5`). Not accepted here | `receipts/hosted-check-runs.tsv` |

The Verilator 5.050 build was the pinned wrapper, with its identity checked (`receipts/tool-identity.txt`). All builds and probes ran in disposable copies under `scratch/`. `scripts/reproduce.sh` re-runs everything above from a clean exact-head clone.

## Lens results at this head

- [R321] PASS Conformance — `CHANGELOG.md:31-39`, `REGISTER_MAP.md:242,1945-1961`, `milan_csr.sv:196`, assignment 5826779078 — Items 1-5 of the round-2 assignment are each met. VERSION stays `0x0002_0060` exactly as decided. The deferral wording matches the cited `GPTP_DROPE` precedent. Acceptance items 1-5 and the item-4 decision, which I verified in round 1, sit on byte-identical RTL (`receipts/delta-scope.txt`). No STREAM_INTERRUPTED wiring was added.
- [R321] PASS RTL — `hdl` tree `d4284df5` identical at `c9bbb03c` and `5beebb7c`; `milan_csr.sv:2389-2395,2561`; `tb/verilator/milan_dp/Makefile:108,196` — No RTL changed. The new `CSR_SRC ?=` defaults to the same path, so every default elaboration is unchanged: the clean controls pass and the default aclk leg passes 189/189. `lint_rtl --check`, port contracts and source-list checks pass. Round 1's synthesis counts carry over unchanged, because the RTL and `syn/` are byte-identical.
- [R321] PASS Robustness — `sim_main.cpp:1429-1449`, `sim_win.cpp:700-718`, `sim_aclk.cpp:401-412` — The new checks read zero for talker selections, for bit 9 combined with a talker, and for out-of-range indices 1 (N=1) and 4 (N=4). Writes are ignored at both shapes. Full-width saturated rails `0xFFFF` pass through. The input is restored to the absent-source tie. Reset, backpressure, flush and absent-stage paths re-pass at this head (controls 63/63 and 32/32, aclk 189/189).
- [R321] PASS Tests — `receipts/probe-mutants.jsonl`, `receipts/probe-row-select.jsonl`, `receipts/probe-csr-bench*.jsonl`, `render_csr_controls.py:55-92`, `measure_test_evidence.py:614-618` — Each new check fails for the defect it names. Of 21 mutant runs, 16 are caught by name. Three survive only on a single-listener shape that cannot distinguish them, and the 4-listener bench catches each one. One multi-leg run survives because that bench is unchanged, and other legs grade the semantic. One is S1. The campaign fails closed on anchor drift and build failure. Its evidence disposition is accurate: it mutates source and derives no expected value from it.
- [R321] PASS Docs — `REGISTER_MAP.md:242,1945-1961`, `CHANGELOG.md:11,31-39`, `TESTING.md:265`, `milan_dp/README.md:806-815`, `render_csr_controls.py:1-14` — The group row, the deferral, the shared-selector caveat, the campaign ownership and the control table all match the code. The README's "Three extra elaborations" equals the three cases in the campaign. All docs gates pass.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | assignment 5826779078 items 1-5; `CHANGELOG.md:31-39,133-135`; `REGISTER_MAP.md:242,1945-1961,2271`; `milan_csr.sv:196`; issue decisions 5789749713 and 5826779078; round-1 acceptance on identical RTL | R321-2 | `5beebb7c7edd908d08be34e52286c9eee441f5b3` |
| RTL | CLEAN | `hdl` tree identity at both heads; `milan_csr.sv:196,437,922,1583,1764,2389-2395,2561`; `milan_dp/Makefile:108,196`; lint, port-contract and source-list gates; clean and default elaborations | R321-2 | `5beebb7c7edd908d08be34e52286c9eee441f5b3` |
| Robustness | CLEAN | `sim_main.cpp:325,1429-1449`; `sim_win.cpp:700-718`; `sim_aclk.cpp:401-412`; controls (clean and absent stage); the default aclk leg; the probe receipts | R321-2 | `5beebb7c7edd908d08be34e52286c9eee441f5b3` |
| Tests | CLEAN (S1 optional) | `sim_main.cpp:1221-1225,1429-1449,1499`; `sim_win.cpp:700-718,743`; `sim_aclk.cpp:401-412`; `render_csr_controls.py`; `milan_dp/Makefile:108,196`; `measure_test_evidence.py:614-618`; 21 mutant runs plus 4 clean controls | R321-2 | `5beebb7c7edd908d08be34e52286c9eee441f5b3` |
| Docs | CLEAN | `REGISTER_MAP.md:242,1945-1961,1522`; `CHANGELOG.md:11,31-39`; `TESTING.md:258-268`; `milan_dp/README.md:793-815`; PR #561 body; the docs gate receipts | R321-2 | `5beebb7c7edd908d08be34e52286c9eee441f5b3` |

## Real limits

- **Banks not run.** I did not run the full parent, PP, gPTP, Yosys or builder banks, or the `milan_dp_render` suite. For those I rely on the manager's statement and the executor's public logs.
  - Round-1 synthesis counts are not re-run. The RTL and `syn/` are byte-identical to `c9bbb03c`, where I reproduced them exactly.
  - The two-listener leg ran only as round-1 probes (clean 64/64).
- **Shapes exercised.** The `RENDER_STAT` checks covered the N=1 CSR and aclk shapes, the 4x4 CSR window shape, and the two-listener TDM8 shape. No 8x8 elaboration read the word.
- **Hardware.** Physical calibration was NOT RUN. No hardware was touched, and no field or skip result is hardware proof. Builder gate 11 is NOT RUN, per the executor.
- **Hosted checks.** Two Verilator shards were still in progress when I read the check runs. Hosted and act acceptance belong to the manager.
- **Clone integrity.** This clone was never edited. After the probes it is still at the exact head: 885 tracked blobs hash equal to the index, with no mode mismatch, and the index hash, staged listing and four gitlinks are unchanged (`receipts/integrity-{before,after}.txt`). The pinned tool's host install prefix is redacted in three logs (`receipts/REDACTIONS.txt`).
- **Disk.** The shared disk filled once during probing. The affected run aborted before building and was rerun in full. Only its successful rerun is recorded.

## Pending manager duties

- Hosted and act acceptance at this exact head, including `Verilator shard 1/5` and `4/5`.
- The concurrent internal delta review R320-2. This round is one of the two required positive reviews.
- The candidate-merge build on current dev `c533b4818df8b3f581df76aa0d1c6d5f55d20449`, its validation, and post-merge containment.
- At merge time, confirm that the Unreleased CHANGELOG entry survives any concurrent Unreleased entries without conflict.

R321-2 FINISHED
