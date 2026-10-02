# [A497] Round 2b handoff: lane P141 (processor issue #141, PR #142)

Status: **REVIEW READY** at the merge commit **`a90ca735844a3e7a5bdfd2d1baeba24c95608992`** (issue #141 comment 5956727692); items 1-3 done; PR-BODY.md updated ("Round 2b"). The manager pushes; nothing was pushed from here. One parent gate function is left to the manager's bank (see "Open").

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #142, issue #141 (the processor part of milan-fpga #629).
- Branch `pp141-clock-sources`. Start head `76b09ff058c6b95750c5a36d8befe67b77e0e079` (round 2, REVIEW READY, pushed). Nothing amended, nothing rebased, nothing pushed.
- Assignment: issue #141 comment 5950735422. TAKEN: issue #141 comment 5950742103.
- Confirmed at the start: origin `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git`, HEAD `76b09ff0`, tree clean (`git status --ignored` empty).
- Fetched `origin main` = `2ebd4fe8d31e88c44559e934bd624e1c50515ad5` (merge of PR #139, lane C6). Merge base with the lane: `03c842a7`.
- Simulator: `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator` (5.050) through a scratch wrapper `$VALIDATION_STORAGE/pp141-a497/bin/verilator`, first on PATH, which rewrites the Makefiles' `-j 0` to `-j ${PP141_VJOBS:-8}`. The host's `/usr/bin/verilator` is 5.052 and was never used.
- Scratch root `$VALIDATION_STORAGE/pp141-a497/` (outside every repository): `scripts/`, `logs/`, `exports/`.

## 1. Merge (item 1)

Merge commit **`a90ca735844a3e7a5bdfd2d1baeba24c95608992`**, `git merge --no-ff 2ebd4fe8` (first parent `76b09ff0`, second `2ebd4fe8`), tree `877a0f78e3b6f15c1159899c10d7ba5e3ca3c836`. One-line subject, no body, no trailer:

> Merge main 2ebd4fe8 (#139) into the clock-source lane, keeping both sides: pp_top's five builds (default, fixture, identify, line, timebase) with section D3C in the default build beside ID0, NP, ST and RN, 09 §8.2's D3C row beside §8.4, and C6's µprograms at 464 and 480 clear of E_SCLKS at 1184

No text conflict. The merge changes no line beyond the two sides: `git diff 03c842a7 76b09ff0` and `git diff 2ebd4fe8 a90ca735` have the same stable patch-id, and so do `git diff 03c842a7 2ebd4fe8` and `git diff 76b09ff0 a90ca735`. So every lane hunk and every C6 hunk is carried exactly once.

The seven files both sides changed, and how each was combined (all by git's three-way merge, each side's hunks in disjoint regions):

| File | Lane side (`03c842a7..76b09ff0`) | C6 side (`03c842a7..2ebd4fe8`) | Combined |
|---|---|---|---|
| `hdl/aecp/ucode/gen_ucode.py` | the E_SCLKS range-check comment (one line longer, comment only) | `E_IDNOTIF = 464`, `E_SINFOUNS = 480` and their two programs (+60 lines) | both; ROM byte-identical to main's (section 2) |
| `tb/pp_top/sim_main.cpp` | `D3ClockSourcePhase` run at the end of section D3 (+1) | five builds; `identify_button_i = 0`; `--identify-only`, `--notify-only`; `notify_phases.hpp` | both; D3C runs in the default build's D3 (and `--d3-only`); ID0, NP, ST, RN run after HZ |
| `tb/pp_top/pp_top_wrap.sv` | `aecp_clk_src_index_o` output, connected to the top's export | `identify_button_i`, `EN_IDENTIFY_NOTIF_P` under `PP_TOP_EN_IDENT`, `dbg_ident_gap_*` taps, builds renumbered | both |
| `tb/pp_top/README.md` | section D3C; the D3 table's four rows and five raised counts; the dispatch table's two `d3` arms | five builds; lane C6's sections ID, ID0, NP, ST, RN; `notify_mutants.py` record (40) | both |
| `docs/architecture/06_aecp_engine.md` | 06 §6.4 SET_CLOCK_SOURCE row (§7.2.32, Table 7-141) | §7 identify and notification text | both |
| `docs/architecture/09_verification.md` | §8.2 D3C row; 83 -> 87; the dispatch `d3` sentence | §8.3 "fifth build"; new §8.4 | both |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md` | REQ-AEM-013 cell; REQ-MDL-005 | GAP-06/GAP-17 landed text; REQ-AEM-026, REQ-NOT-001/002; register rows | both |

`tb/pp_top`'s builds are numbered the same everywhere after the merge: default 1, fixture 2 (DV), identify 3 (ID), line 4 (AX), timebase 5 (TB). Checked by a grep for build ordinals and counts over the bench (`sim_main.cpp`, `pp_top_wrap.sv`, `Makefile`, `notify_phases.hpp`), the README, 06/08/09, and the drivers (`aecp_mutants.py` "the fifth build", `notify_mutants.py` "the third build"). The lane's own text names no build ordinal ("the whole default build" only), so nothing needed renumbering.

## 2. ROM map check (item 1)

Every ROM regenerated from its generator, each revision in its own `git archive` export of `hdl/` (`scripts/rom_regen.sh`, log `rom_regen.log`):

| Output | Bytes | `03c842a7` = `76b09ff0` (lane) | `2ebd4fe8` (main) = `a90ca735` (merge) |
|---|---:|---|---|
| `ucode.hex` (`gen_ucode.py`) | 26,624 | `3559d0a64b51062a4dc47744ead112a0cc839f389bb2d16ba0133b03baf4b053` | `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8` |
| `ltn_rom.hex` (`gen_ltn_rom.py`) | 6,138 | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | the same |
| `image.bin` (`gen_desc_image.py`, `example_milan_8.json`) | 1,880 | `20356f5967e45a9eafcf8a63c5c933dca75fccb5d6bbc16941dc91dc2483b62c` | the same |

The merge's ROMs are byte-identical to main's: the lane adds no microcode.

Word map beyond text (`scripts/rom_map.py` runs the generator in memory with `place()` recording each program's start and length; `scripts/rom_overlap.py`, log `rom_overlap.log`):

| Program | Words at main and at the merge |
|---|---|
| `E_COPYT` | 448..455 |
| `E_IDNOTIF` (C6) | 464..469 (6) |
| `E_SINFOUNS` (C6) | 480..500 (21) |
| `E_SCLKSRF` | 1144..1150 (7) |
| `E_SCLKS` | 1184..1209 (26) |

89 programs and 1,107 of 2,048 words at both main and the merge; the program map and every ROM word are identical. No SET_CLOCK_SOURCE word lies in 456..511. `place()`'s overlap assert passed at both.

The lane's E_SCLKS changes are its two dispatch arms. Every committed patch on `gen_ucode.py` (22: 20 dispatch, 2 in `mutations/`) was planted in a fresh copy of each export and its ROM diffed against the unmutated one (`scripts/rom_patch_check.py`, log `rom_patch_check.log`). For all 22 the changed words, with their old and new values, are identical at `76b09ff0` and at the merge, and none is in C6's two programs. `sclks-bound-three` changes word 1196 and `sclks-bound-inclusive` word 1197, both in E_SCLKS. `lk-prefix-zero-body` changes 98 words in 1144..1991, the same 98 at both revisions.

`scripts/check_upc_map.py` at the merge: PASS, 61 engine constants and 89 entry points agree (59 and 87 at `76b09ff0`). `scripts/check_m9_opcodes.py`: PASS, 30 opcodes.

## 3. git apply --check table (item 2)

`git apply --check -v` of every committed campaign patch, each against a pristine `git archive` export of the same revision, outside any repository (`scripts/apply_check.sh`):

| Revision | Patches | Refused | At an offset | On `gen_ucode.py` | Log (sha256/16, bytes) |
|---|---:|---:|---:|---|---|
| `76b09ff0` (lane) | 207 | 0 | 179 | 22 apply; both `sclks-*` exact | `939ee81204113b9f`, 20,936 |
| `2ebd4fe8` (main) | 205 | 0 | 182 | 20 apply | `debfbbeb72201631`, 20,782 |
| **`a90ca735` (merge)** | **207** | **0** | 184 | **22 apply**; both `sclks-*` at offset 25 | `f381c4609990ceea`, 21,000 |

Per directory at the merge: `tb/pp_top/aecp_dispatch_mutations` 37 (37 at an offset), `tb/pp_top/mutations` 42 (42), `tb/srp_top/mutations` 73 (56), `tb/maap/mutations` 27 (21), `tb/adp_engine/mutations` 28 (28); none refused. The offset-25 lines on the two `sclks-*` patches are C6's +6 (entry points) and +19 (E_IDNOTIF) lines above E_SCLKS; the per-patch ROM diff above shows each still plants the same word. They were left as they are (merge only; `git apply` places them by context, as it does 184 of the 207).

The text-edit drivers (`d3_mutants.py`, `notify_mutants.py`, `acmp_mutants.py`, `gsi_mutants.py`, `name_wr_mutant.py`, `retry_mutants.py`, `srp_admission/mutants.py`, `desc_mem_guard/mutate.py`) check their own anchors when they plant; their re-runs below cover them.

## 4. Changed-file-to-campaign map

The merge changes two sets of files: against the lane head, C6's 31 (non-doc: `hdl/aecp/KL_aecp_engine.sv`, `KL_aecp_notify.sv`, `ucode/gen_ucode.py`, `hdl/common/pp_pkg.sv`, `hdl/top/protocol_processor_top.sv`, `tb/aecp_notify/{Makefile,sim_main.cpp}`, `tb/originator/sim_main.cpp`, `tb/pp_top/{Makefile,aecp_mutants.py,notify_mutants.py,notify_phases.hpp,pp_top_wrap.sv,sim_main.cpp}`, `tb/ucpu/sim_main.cpp`); against main, the lane's 14 (non-doc: the `gen_ucode.py` comment, `tb/pp_top/{aecp_dispatch_mutants.py,d3_mutants.py,d3_phases.hpp,pp_top_wrap.sv,sim_main.cpp}` and three dispatch patches). Which suite reads a changed `hdl/` file was taken from the suite Makefiles' source lists: `pp_pkg.sv` feeds 19 suites (acmp_listener, acmp_nvm, acmp_talker, adp_engine, aecp_notify, ca_originator, dispatch, maap, originator, pp_top, rx_validator, scoreboard, srp_decoder, srp_encoder, srp_stream_fsms, srp_top, timer_map, timer_service, tx_arbiter); the engine and the top feed `pp_top`; `KL_aecp_notify.sv` feeds `aecp_notify` and `pp_top`; `gen_ucode.py` feeds `pp_top` and `ucpu`.

| Campaign | Builds and runs | Changed inputs it reads | Re-run |
|---|---|---|---|
| `aecp_dispatch_mutants.py` (37) | pp_top `aecp-dispatch`, `aecp-line`, `line-guards`, `d3` | bench (`sim_main.cpp`, wrap, both phase headers, Makefile), engine, top, notify, `pp_pkg`, `gen_ucode.py`; its driver and patches | yes |
| `aecp_mutants.py` (55) | pp_top `deadline`, `d3`, `budget`, `hazards`; ucpu `run` | the pp_top bench and RTL; `tb/ucpu/sim_main.cpp`; its driver | yes |
| `d3_mutants.py` (87) | pp_top `--d3-only`; acmp_nvm; rx_validator | the pp_top bench and RTL; `pp_pkg` (all three); its driver | yes |
| `notify_mutants.py` (40) | pp_top identify build, `--identify-only`, `--notify-only`; originator; aecp_notify `identify` | the pp_top bench (now with D3C), all C6 files | yes |
| `acmp_mutants.py` (19) | acmp_listener; rx_validator; pp_top `--acmp-only` | `pp_pkg`; the pp_top bench and RTL | yes |
| `gsi_mutants.py` (20), `name_wr_mutant.py` (1) | pp_top `--gsi-internal-only`, `--name-writes-only` | the pp_top bench and RTL | yes |
| `tb/maap` `mutants` (32) | maap; rx_validator; pp_top `maap-internal` | `pp_pkg`; the pp_top bench and RTL | yes |
| `tb/adp_engine` `mutants` (32) | adp_engine; pp_top `adp-config` | `pp_pkg`; the pp_top bench and RTL | yes |
| `tb/srp_top` `mutants` (90) | srp_top; srp_stream_fsms; srp_encoder | `pp_pkg` (against the lane head only) | yes |
| `acmp_talker/retry_mutants.py` (70) | acmp_talker | `pp_pkg` (against the lane head only) | yes |
| `srp_admission/mutants.py` (12) | srp_admission; srp_top | `pp_pkg` via srp_top (against the lane head only) | yes |
| `desc_mem_guard/mutate.py` | desc_mem_guard | none | yes (cheap) |
| `tb/nvm_port` `figures` | nvm_port | none | yes (a CI step) |

So every campaign was re-run at the merge, whole where it fits in one foreground command, otherwise in chunks that partition its arms (below).

## 5. Suites (item 2)

All at the merge `a90ca735`, from a `git archive` export (`exports/run-a90ca735`), with Verilator 5.050 and every build held to eight jobs:

| Command | rc | Result | Against round 2 (`76b09ff0`) |
|---|---:|---|---|
| `./scripts/run_suites.sh`, whole (523 s, after a per-suite warm build) | 0 | 33 suites, **1,019,127 checks, 0 failing**; its µPC map gate 61/89 and M9 gates 9/9 and 30 | 1,018,860 |
| `tb/pp_top` (`make`, in the sweep and alone) | 0 | **9,168**: default 8,696, fixture 20, identify 178, line 218, timebase 56; section D3 150 | 8,918 (default 8,624, fixture 20, line 218, timebase 56); the default build gains C6's ID0 3, NP 47, ST 18, RN 4 (+72) and the identify build is new (+178) |
| `./scripts/lint_hdl.sh` | 0 | 41 modules LINT OK | 41 |

## 6. Campaigns (item 2)

Each chunk re-runs the positive control (or golden) of every target or suite it uses. Each failing count was compared with its README record by script (`scripts/compare_readme.py` and inline comparers; logs `compare_*.txt`).

| Campaign | How it ran (arms per foreground command) | Controls | Arms | Against the README record |
|---|---|---|---|---|
| `aecp_dispatch_mutants.py` | `--only` chunks of 5, 15, 17 (92, 245, 463 s) | `aecp-dispatch` x3, `aecp-line`, `line-guards`, `d3`: PASS | **37 of 37 KILLED** | 37 of 37 rows equal (`tb/pp_top/README.md:1071-1107`): `lk-prefix-zero-body` 7, `sclks-bound-three` 11, `sclks-bound-inclusive` 6 |
| `aecp_mutants.py` | `--only` chunks of 14, 20, 21 (319, 322, 242 s) | pp_top `d3`, `deadline` x2, `budget`, `hazards` x2; ucpu `run` x2: PASS | **55 of 55 KILLED** | 55 of 55 equal (`:1002-1048`, shorthand rows such as `` `hz-map-as-ro`, `-talker` `` expanded); "5 controls PASS and 55 arms KILLED" holds |
| `d3_mutants.py` (`--jobs 4`, 2 Verilator jobs each) | `--only` chunks of 10 (`--jobs 2`), 12, 14, 14, 14, 12, 11 | goldens PASS in every chunk | **87 of 87 KILLED** | 75 of 75 `tb/pp_top` rows (`:913-987`, the five D3C-raised counts and the four D3C rows included), 11 of 11 `tb/acmp_nvm` rows (`tb/acmp_nvm/README.md:377-387`), `tb/rx_validator` M4 4; every count also equals its log's own tally |
| `notify_mutants.py` (`--jobs 4`) | `--only` chunks of 10, 15, 15 (157, 278, 158 s) | goldens PASS | **40 of 40 KILLED** | 40 of 40 rows equal (`:1983-2022`) |
| `acmp_mutants.py` (`--jobs 4`) | whole (202 s) | 3 goldens PASS | **19 of 19 KILLED** | 15 pp_top "N of 43" rows, 4 `tb/acmp_listener` rows, `tb/rx_validator` M6 27: all equal |
| `gsi_mutants.py` | no `--only`, whole run 595 s+ (stopped at the bound after the golden and 12 variants, all detected); then three slices of 7, 7, 6 by `scripts/gsi_slice.py`, which runs the driver's own `mutations()` and `check_variant()` with its CPU pin, golden first and restored last in each | golden and restored PASS in each slice | **20 of 20 detected** | the README records "20 detected", no per-variant count |
| `name_wr_mutant.py` | whole (44 s) | golden, restored PASS | decode **KILLED** (NW EIGHT, LOCKED, ABORT) | as recorded |
| `make -C tb/maap mutants` | whole (284 s) | 3 PASS | 29 entries KILLED, **32 of 32** | 29 of 29 "N FAIL of M" equal (`tb/maap/README.md:237-265`) |
| `make -C tb/adp_engine mutants` | whole (443 s) | 2 PASS | 30 KILLED, **32 of 32** | 30 of 30 rows equal (`tb/adp_engine/README.md:172-201`) |
| `tb/srp_top/mutants.py` | `--only` chunks of 11, 11, 11, 13, 9, 9, 9 labels (368, 335, 232, 532, 301, 413, 136 s) | 11 distinct, all PASS | 73 labels, **78 entries KILLED**; assertion coverage rebuilt from the KILLED arms' tags: **65/65**; the whole run's **90 of 90** | 78 of 78 entries equal each label's latest README record: the round tables, superseded where the README's own prose re-measures (`tb/srp_top/README.md:375-379`, `:408-413`); `peer-restarts-timer` is retired there (`:374`) |
| `acmp_talker/retry_mutants.py` | whole (406 s) | baseline, restored rc 0 | **62 KILLED, 7 equivalence, 1 performance** | 70 of 70 rows equal (`tb/acmp_talker/README.md:225-294`) |
| `srp_admission/mutants.py` | no `--only`, whole run stopped at the bound (595 s) after its control and 5 entries, all PASS; then three slices by `scripts/srp_admission_slice.py` (the driver's own `MUTANTS`, `SUITES`, `build_tree`, `run_suite`, `judge`): control + one mutant each (386, 400, 409 s) | control PASS in all 3 suites, in each slice | 3 mutants x 3 suites, all their named failures: **12 of 12** | as recorded |
| `desc_mem_guard/mutate.py` | whole (5 s) | | hold-deleted mutant **detected** | as recorded |
| `make -C tb/nvm_port figures` | whole (259 s), in the export with `GIT_DIR` set to the lane's repository (it reads two pinned revisions with `git show`; nothing is written there) | | "all measured figures agree with the tree" | |

No arm was lost: each driver's arm list (read from the driver, `scripts/listarms.py`) was partitioned exactly by its chunks, and every chunk ended rc 0.

Other gates at the merge (CI's docs and portability jobs and the generator checks), all rc 0:

| Command | Result |
|---|---|
| `check-links.py`, `check-matrix.py`, `check-integrator-params.py`, `render-wavedrom.py --check`, `make stale` (lane checkout) | 1,035 links; 115 REQ rows, 17 GAP findings; top 27, guide 27, diagram 27 parameters (C6's `EN_IDENTIFY_NOTIF_P` is the 27th); 18 wavedrom blocks; not stale |
| `make check` (lane checkout, 29 s) | 41 mermaid + 18 wavedrom blocks, the figures above, 94 module rows, 0 untested. It bootstrapped `.venv-wavedrom/` (ignored), removed afterwards |
| `python3 scripts/gen_matrix.py --check` | 94 rows, 0 untested |
| `scripts/check_upc_map.py`; `check_m9_opcodes.py --selftest` and plain | 61 constants, 89 entry points; 9 of 9; 30 opcodes |
| `./syn/yosys/run.sh` (sv2v 0.0.13, Yosys 0.66), in the export | 36 tops YOSYS OK, the Xilinx map OK (91 s) |
| `git diff --check` against `76b09ff0`, `2ebd4fe8` and `03c842a7`; `git diff-tree --cc --check HEAD` | clean |

## 7. Parent consumer gates (item 3), milan-fpga dev `cdf49d1a`, gitlink at `a90ca735`

Scratch parent `$VALIDATION_STORAGE/pp141-a497/parent`:

- A `git archive` of the read-only trusted checkout at `cdf49d1a28527562888f0a903de51b6b15b1244f`. HEAD and index were set to that commit (fetched from the trusted checkout, then `git reset`): 984 index entries, tree `904f30790afd22115a4f627da7f48d1604d6b1b8`, working tree clean against it.
- `gptp-processor` `5dce647a` and `third_party/verilog-axis` `48ff7a7e` cloned from their recorded URLs (the trusted checkout carries no submodule contents). `protocol-processor` is a scratch clone of this branch (`--no-hardlinks`) checked out at `a90ca735`, with the gitlink staged there. The three are registered and absorbed into `.git/modules`; `git submodule status` shows a blank prefix for each. `external` is recorded and uninitialised, as in the trusted checkout.
- `parent-adoption-c4c6-ea3fb388.patch` (2,687 bytes, sha256 `67bcd69852e5d090abc635e8dd66e5159667847ebf83d85aba9599d7cff7bd7c`) applied with `git apply` (its `--check` clean, no offsets). The working-tree diff has the patch's own patch-id. It binds `EN_IDENTIFY_NOTIF_P (1'b0)` and `identify_button_i (1'b0)` in `hdl/milan/KL_pp_shadow.sv`, and adds the `acmp_mutants.py` and `notify_mutants.py` dispositions in `scripts/measure_test_evidence.py`. Apart from the gitlink it is the only change; `scripts/test_evidence.budget` is untouched.
- The trusted checkout was not modified: HEAD `cdf49d1a`, and its one ignored entry, `scripts/__pycache__/`, dates from 07:35, before this session.

Each gate ran alone, in the foreground. Verilator 5.050 through the wrapper; `xvlog` (Vivado 2026.1, found by the gate itself) never ran beside a Verilator build of this lane. Note: a check just before gate 3 showed another session's CI replay running Verilator shards on this host (not this lane's processes); nothing of this lane ran beside `xvlog`.

| # | Gate | rc | Result | Log (sha256/16, bytes) |
|---:|---|---:|---|---|
| 1 | `check_cpp_idiom.py` | 0 | every ratchet held | `0819e65b083515c0`, 315 |
| 2 | `check_py_idiom.py` | 0 | every ratchet held (too many parameters 7 <= 7) | `a0301dea70613aed`, 461 |
| 3 | `xvlog_gate.py --check` | 0 | 4 findings == ratchet (0 `hdl/`, 4 pinned processors); "pinned at: protocol-processor@a90ca735; gptp-processor@5dce647a"; 144 s, alone | `5be94b4a37d36ee6`, 1,320 |
| 4 | `check_rtl_source_lists.py` | 0 | 107 files, 4 of 4 lists; processor 36/42 tops, 6 recorded | `b8372555c3e35c33`, 390 |
| 5 | `pp_srcs.py --check --selftest` | 0 | | `fad5e1b9dd5f465b`, 955 |
| 6 | `sw/builder/test_builder.py` | see note | **99 of 100 gate functions rc 0; gate 12 not completed** (manager's bank re-runs it whole) | below |
| 7 | `make -C tb/verilator/pp_shadow -j8` (Verilator 1 job each) | 0 | 606, 606, 646, 311 checks, 0 failures (253 s) | `e9d02d541b78c3ad`, 264,341 |
| 8 | `check_port_contracts.py` | 0 | processor 111 <= 111 undocumented (1,757 processor ports); lowerable by 3 | `4c480cfd56977f70`, 536 |
| 9 | `measure_naming.py --check` | 0 | 96 recorded | `264ee07e802a4ea0`, 36,704 |
| 10 | `measure_test_evidence.py --check` | 0 | 72 <= 77, 10 <= 10, **0 <= 0 unexplained DUT-source readers**, 3 <= 3; byte-identical output after all the builds | `b8fcdff852cf5f6b`, 12,577 (both) |
| 11 | `docs_check.py` | 0 | 0 findings (185 md + 956 text files) | `8181a29ba6868d4e`, 127 |
| 12 | `make -C tb/verilator/nvm_cosim lint` | 0 | | `e1a20ef6a43943d2`, 29,864 |
| 13 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 of 315 | `520d47b8d67e1f60`, 394 |
| 14 | `make -C tb/verilator/milan_dp -j8` | 0 per part | every leg PASS (below); `render_mutants.py` 6/6; `gmstep_mutants.py` 6/6 | below |
| 15 | `make -C tb/verilator/milan_dp_render -j8 VERILATOR_JOBS=4` | 0 | both legs RESULT PASS (65, 152 checks); leg defects 5/5; one whole run (345 s) | `5d81db9b59764532`, 170,067 |
| 16 | `lint_rtl.py --check` | 0 | 90 <= 90 | `75be251ed2de9739`, 14,186 |

Note on 6. One whole run reached the bound (595 s, rc 124; `parent-test_builder-whole.log`). `test_builder.py` has no gate selection, so `scripts/test_builder_slice.py` compiles the script's own source and runs it as `__main__` from the parent root, with only its gate tuple cut to a slice in memory (`test_builder_gates.txt` lists the 100):

- gates 0-11: rc 0, 21 s, ALL GATES PASS (`0200f383597610de`, 9,741);
- gates 13-99: rc 0, 165 s, 87 functions, "ALL GATES PASS EXCEPT 1 NOT RUN": the calibration gate, whose mf48 board build tree is not on this host, as in rounds 1 and 2 (`6b1f959523b383d0`, 41,982). Its two "FAIL" lines are the planted disabled-writer control being caught;
- gate 12, `test_baremetal_profile_contract` (gate 1b), alone: rc 124 at 590 s, twice. The unbuffered run printed 4 sub-gate lines, each PASS (product configs and refusal arms, compiler identity, boot-unit asm forms, identity storage), as in round 2 (`2d9cd1a912b209fe`, 578). It is one sequential function and cannot be split without editing the parent. **It is left to the manager's bank, which re-runs `test_builder.py` whole (assignment item 3).**

Note on 14. One `make` is longer than one foreground command. It ran as:

1. `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=1`: built all 14 binaries; the three prerequisite simulations passed (`gptp` 182/0, `gptplat` 182/0, `gmstep` 104/0, RESULT PASS); the pool's first legs passed (`sim` 235/0, `notify` 382/0); the bound came inside `crflic` (595 s; `42bd7c9f9c8b2a0a`, 1,128,982 bytes).
2. The recipe's own `python3 sim_pool.py --jobs="2"` command, its arguments taken from `make -n run` (`milan_dp_pool_cmd.txt`), in three groups, each rc 0: A `sim` 235/0, `notify` 382/0, `crflic` 416/0, `nxn` 1,845/0, `nxndv` 1,847/0 (60 s); B1 `nxn8` 3,525/0, `nxn4c` 1,845/0, `nolpf` 235/0 (39 s); B2 `prune` 33/0, `ax1x1` 232/0, `aclk` 191/0 (570 s).
3. `python3 render_mutants.py`: 6 of 6 (425 s); `python3 gmstep_mutants.py`: 6 of 6 (318 s), from `tb/verilator/milan_dp`, each build held to 8 jobs.

## 8. Parent-visible list

- **Nothing parent-visible from this lane: no STOP.** At the merge, `hdl/` differs from main's only in the `gen_ucode.py` comment (no non-comment line), `hdl/top/protocol_processor_top.sv` is byte-identical to main's, and every ROM is byte-identical to main's (`ucode.hex` `518b900c…`).
- **What the merge brings is main's C6, which main already carries.** Against the lane head, the top gains `parameter bit EN_IDENTIFY_NOTIF_P = 1'b0` and `input wire identify_button_i`. The combined C4 + C6 parent patch binds both to `1'b0` in `KL_pp_shadow`. `check-integrator-params.py` counts 27 overridable parameters (26 at the lane head). `check_port_contracts.py` holds processor 111 <= 111 with the patch.
- **Registry and budget:** the patch's two disposition lines (`acmp_mutants.py` from #137, `notify_mutants.py` from C6) hold `measure_test_evidence.py --check` at 0 <= 0 unexplained readers. No budget change. This lane adds no new reader: `d3_mutants.py` and `aecp_dispatch_mutants.py` keep their round-1 dispositions.
- **Processor totals at the merge:** `tb/pp_top` 9,168 (default 8,696, fixture 20, identify 178, line 218, timebase 56); section D3 150; sweep 1,019,127. No parent file at `cdf49d1a` quotes them.
- **The parent's pin line** would read `protocol-processor@a90ca735` (gate 3).
- Round 1's list otherwise stands: names for adoption D3C1 to D3C4; the parent's own L6 (`docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:89`) still cites 7.4.23.1; `aecp_clk_src_index_o` unchanged.

## 9. PR-BODY.md

Round 2's body (29,330 bytes, equal to the round-2 packet's) with only additions (`diff` shows 0 removed lines): the commit table gains `a90ca73`, and a "Round 2b" section is appended (items 1-3, the parent-visible list, and a line-reference map: C6 moved the body's `76b09ff` cites of `gen_ucode.py` by +25, `KL_aecp_engine.sv:1563` to `:1579`, REQ-AEM-013 `:382` to `:406`, REQ-MDL-005 `:425` to `:449`, 06 §6.4 `:462` to `:465`; L6 `:135`, `KL_aecp_dyn_state.sv:186` and `KL_aecp_nvm_writer.sv:502` are unchanged). First line `[A490]` and "Closes #141" kept; 41,690 characters; no absolute paths, no attribution footer.

## Open

- Parent gate 6, `test_baremetal_profile_contract` (one of 100 functions): not completed inside one foreground command; the manager's bank re-runs `test_builder.py` whole.
- Not taken (merge only): R430-1 S1/S2 and R431-1 S1/S2; refreshing the two `sclks-*` hunk headers to the merge's line numbers (they apply at offset 25 and plant the same words).

## Scratch and hygiene

- Scratch root `$VALIDATION_STORAGE/pp141-a497/` (outside every repository and this directory): `bin/verilator` (the job-capping wrapper), `scripts/` (`rom_map.py`, `rom_regen.sh`, `rom_overlap.py`, `rom_patch_check.py`, `apply_check.sh`, `listarms.py`, `chunk.sh`, `compare_readme.py`, `suite_group.sh`, `gsi_slice.py`, `srp_admission_slice.py`, `test_builder_slice.py`), `chunks/` (each driver's arm list), `logs/`, `out/` (campaign outputs), `exports/` (`run-a90ca735`, `apply-*`, `rom/*`), `parent/` (the scratch parent, 4.0 GB), `tmp/` (driver temp trees; three are left by the runs stopped at the bound).
- Processor logs (sha256/16, bytes): `run_suites.log` `7c51e16dc35eee2d` 1,746; `lint_hdl.log` `9a3703ba1ec6767b` 1,056; `suite-pp_top-cold.log` `3636d1a4b01ce63c` 150,615; `compare_dispatch.txt` `fe8720b100593ba6`; `compare_aecp.txt` `5a39e59d45a7ee1e`; `compare_d3_pp_top.txt` `786cba454e63904e`; `compare_d3_acmp_nvm.txt` `2758f4a910c357c6`; `compare_notify.txt` `d7a7be5e974d478d`; `compare_acmp.txt` `981a32bf45031bca`; `compare_maap.txt` `a4e940ae4098abd6`; `compare_adp.txt` `622d373b7c5c3c09`; `compare_srp.txt` `a471dc20f6a345e3`; `srp_summary.txt` `57c3c98d5fa5f97f`; `compare_retry.txt` `d02b6aab95b6402e`; `nvm_port_figures.log` `5838b1559fc5afd9` 3,647; `yosys.log` `8a2b6975c0faf1b7` 25,840; `make_check.log` `9320efb7c5dfc54a`; `docs_gates.log` `7ce36e42b460c417`.
- The lane tree is clean (`git status --porcelain --ignored` empty). `make check` bootstrapped `.venv-wavedrom/` (ignored) in it; that was removed after checking it was created in this session. Every other run used the export or the scratch parent. `nvm_port figures` read history through `GIT_DIR` and wrote nothing in the lane.
- Nothing in this directory is over 200 KB, and it holds no toolchains, virtualenvs or tree exports.
