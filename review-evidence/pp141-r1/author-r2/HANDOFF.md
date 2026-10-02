# HANDOFF: lane P141, round 2 ([A495])

Status: **REVIEW READY** at `76b09ff058c6b95750c5a36d8befe67b77e0e079`, with one parent gate arm not completed (see
"Open"). The manager pushes. Nothing was pushed from here.

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #142, issue #141 (the processor part of milan-fpga #629)
- Branch `pp141-clock-sources`. Round-2 base `4a40b1798e463d09aafd74632408003229bcc673`; new commit `76b09ff0` (one, one-line subject, no body or trailer); nothing amended.
- Assignment: issue #141 comment 5947144104. TAKEN: issue #141 comment 5947149935. REVIEW READY: issue #141 comment 5950696185.
- Reviews answered: R430-1 POSITIVE (PR #142 comment 5946693777); R431-1 NEGATIVE, F1 MAJOR (the dispatch campaign aborts at `4a40b17`).
- Remote and HEAD were confirmed at the start: origin `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git`, HEAD `4a40b179`.
- Simulator: `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator` (5.050), through a scratch wrapper (`$VALIDATION_STORAGE/pp141-a495/bin/verilator`) that rewrites `-j 0` to `-j ${PP141_VJOBS:-8}`.
- Every command ran in the foreground, one heavy build at a time; `xvlog` never ran beside a Verilator build.

## Open

- Parent gate 6, `sw/builder/test_builder.py`: 99 of its 100 gate functions pass at this head. `test_baremetal_profile_contract` (gate 1b, one function of about 14,800 lines) did not finish inside one foreground command (10 minutes), and it cannot be split without editing the parent. It reads no processor file. Round 1 ran the whole script at `39fd019`, rc 0. **It needs one whole run at `76b09ff0`, in the manager's consumer bank.**
- Not taken under "No other change": R430-1 S1/S2 and R431-1 S1/S2 (suggestions).

## Item 1: refresh (`76b09ff0`)

| Patch | Change | Planted defect |
|---|---|---|
| `tb/pp_top/aecp_dispatch_mutations/lk-prefix-zero-body.patch:98-99` | hunk `@@ -1427,31 +1417,25 @@`: its two leading context lines replaced one for one by `4a40b17`'s re-wrapped lines (`hdl/aecp/ucode/gen_ucode.py:1637-1638`), so its line counts stand | unchanged: its 151 `-`/`+` lines equal `39fd019`'s |
| `tb/pp_top/aecp_dispatch_mutations/sclks-bound-three.patch:3` | hunk header `-1658,7 +1658,7` to `-1659,7 +1659,7` | unchanged (2 lines) |
| `tb/pp_top/aecp_dispatch_mutations/sclks-bound-inclusive.patch:3` | hunk header `-1659,8 +1659,8` to `-1660,8 +1660,8` | unchanged (4 lines) |

Proof (`scripts/defect_identity.sh`, log `defect_identity.log`): each old patch planted at `39fd019` and its
refreshed form planted at `76b09ff0` generate a byte-identical `ucode.hex`, and each differs from the unmutated ROM.
`lk-prefix-zero-body`'s other hunks keep the base's offsets (1-2 at 9; 3-4 at 209; 5-9 now 210, 209 before the
one-line re-wrap). The base itself applies those hunks at offsets, and 179 of its 205 patches apply at some offset,
so they were left as they are.

## Item 2: apply checks and campaign re-runs

Files this PR changes (`03c842a7..76b09ff0`, 14): `docs/00_MILAN_COMPLIANCE_REVIEW.md`,
`docs/architecture/06_aecp_engine.md`, `07_memory_maps.md`, `09_verification.md`, `hdl/aecp/ucode/gen_ucode.py`,
`tb/pp_top/README.md`, `aecp_dispatch_mutants.py`, `aecp_dispatch_mutations/{sclks-bound-inclusive,sclks-bound-three,lk-prefix-zero-body}.patch`,
`d3_mutants.py`, `d3_phases.hpp`, `pp_top_wrap.sv` and `sim_main.cpp`.

Campaign inventory (every patch directory and every mutation driver in the tree):

| Campaign | Mechanism | Edits on a changed file |
|---|---|---|
| `tb/pp_top` `aecp-dispatch-mutants` (`aecp_dispatch_mutations/`, 37) | `git apply` | 20 patches on `gen_ucode.py` |
| `tb/pp_top` `aecp-mutants` (`mutations/`, 42 patches, 55 arms) | `git apply` | 2 on `gen_ucode.py` (`dlkill-always-misbehaving`, `mvu-silent`) |
| `tb/srp_top` (73), `tb/maap` (27), `tb/adp_engine` (28) `mutations/` | `git apply` | none |
| `d3_mutants.py`, `acmp_mutants.py`, `gsi_mutants.py`, `name_wr_mutant.py`, `acmp_talker/retry_mutants.py`, `srp_admission/mutants.py`, `desc_mem_guard/mutate.py` | exact-text edits | none (they edit `.sv` files and `tb/acmp_talker/sim_main.cpp`, none of them changed) |

No patch touches `06_aecp_engine.md` or any other changed file but `gen_ucode.py`. No prose file cites `gen_ucode.py`
by line number.

`git apply --check -v` of every patch, each against a pristine `git archive` export of the same revision
(`scripts/apply_check.sh`):

| Revision | Patches | Refused | At an offset | The 22 on `gen_ucode.py` |
|---|---:|---:|---:|---|
| `03c842a7` (base) | 205 | 0 | 179 | 20 OK |
| `39fd019` | 207 | 0 | 179 | 22 OK; both `sclks-*` exact |
| `4a40b17` | 207 | **1**: `lk-prefix-zero-body`, hunk 5, `gen_ucode.py:1427` | 180 | 21 OK; both `sclks-*` at offset 1 |
| **`76b09ff0`** | 207 | **0** | 179 | **22 OK**; both `sclks-*` exact |

Campaign re-runs at `76b09ff0` (export `run-76b09ff0`). A whole run of either campaign is longer than one
foreground command may run (dispatch about 13 minutes), so each ran as `--only` chunks that partition its arm list
exactly. Each chunk re-runs the positive control of every target it uses. `scripts/compare_readme.py` compared
every measured failing count with the README's table.

| Campaign | Chunks (arms) | Controls | Arms | vs `tb/pp_top/README.md` |
|---|---|---|---|---|
| `aecp_dispatch_mutants.py` | 7, 13, 15, 2 | `aecp-dispatch` x3, `aecp-line`, `line-guards`, `d3`: all PASS | **37 of 37 KILLED** | 37 rows, 0 disagreements (`:1069-1107`) |
| `aecp_mutants.py` | 7, 15, 16, 17 | pp_top `deadline` x2, `d3`, `budget`, `hazards` x2, ucpu `run`: all PASS | **55 of 55 KILLED** | 55 arms, 0 disagreements (`:1000-1048`); "5 controls PASS and 55 arms KILLED" (`:998`) holds |

The three refreshed arms: `lk-prefix-zero-body` 7 (`:1085`), `sclks-bound-three` 11 (`:1106`) and
`sclks-bound-inclusive` 6 (`:1107`), each with its named check failing. They ran twice: once in a targeted chunk
first, and once in the partition.

## Item 3: PR body

`PR-BODY.md` is round 1's body (equal to the live PR #142 body apart from a trailing newline), with:

- the commit table gaining `76b09ff`;
- the "No file cites `gen_ucode.py` by line number" sentence corrected: the committed patches carry line numbers and context;
- the re-measure statement under "Validation" corrected: a comment change re-runs every campaign with a patch on the changed file, and the round-1 tables are marked as `39fd019`'s;
- a "Round 2" section added: items 1-4, validation at `76b09ff0`, the parent gates and the round-2 parent-visible list.

Every `gen_ucode.py` line reference in the body was re-checked at `76b09ff0` (`gen_ucode.py` is unchanged since
`4a40b17`): `:1629-1638` (the range-check comment), `:1637-1638`, `:1649-1686` (E_SCLKS, `place(` to `])`, with
E_SCLKSRF at `:1678`) and `:1663-1664` (`CHECK_ARG ... REL_LT`). The design's cites, `:1414` and `:1410-1440`, are
against the pin `b2db3a97` and hold there.

## Item 4: hosted `suites`

Every step of `.github/workflows/hdl.yml` was reproduced locally at `76b09ff0` (table below). The manager pushes
after REVIEW READY.

## Docs changes of the PR (round 1, unchanged in round 2)

| Site | Change | Clause |
|---|---|---|
| `docs/architecture/07_memory_maps.md:135` (L6) | §5.3.3.6's set stated as a minimum; one INPUT_STREAM source per AAF input beside the CRF input's; order INTERNAL 0, CRF 1, AAF input k at 2 + k (milan-fpga D1); identity list of any length up to 216 | Milan v1.2 §5.3.3.6; IEEE 1722.1-2021 §7.2.9.2/Table 7-17, §7.2.32/Table 7-61, Table 7-141, §7.4.23.1 |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:425` (REQ-MDL-005) | the same minimum, allowance and order; BAD_ARGUMENTS credited to IEEE 1722.1-2021 §7.2.32 and Table 7-141, not to Milan §5.4.2.15/.16 | Milan v1.2 §5.3.3.6; IEEE 1722.1-2021 §7.2.32, Table 7-141 |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:382` (REQ-AEM-013) | finding cell names D3C1 to D3C4 beside D3S1/D3R1 | Milan v1.2 §5.4.2.15/.16 |
| `docs/architecture/06_aecp_engine.md:462` (06 §6.4) | membership credited to IEEE 1722.1-2021 §7.2.32; BAD_ARGUMENTS to Table 7-141; the current index to §7.4.23.1 | same |
| `hdl/aecp/ucode/gen_ucode.py:1629-1638` (E_SCLKS comment) | the same credits; comment only, every ROM byte-identical | same |
| `docs/architecture/09_verification.md:206-214` (§8.2) | D3C row; 87 D3 controls; the two dispatch arms | n/a |

## Tests and their failing mutants (round 1, re-measured where noted)

| Test (`tb/pp_top/d3_phases.hpp`, section D3C) | Grades | Failing mutant(s) |
|---|---|---|
| D3C1 (`:2821-2871`) | SET_CLOCK_SOURCE(9) over ten sources: SUCCESS byte-exact, one unsolicited response, one write/mark/enqueue, GET, row and export read 9 | `sclks-bound-three` (dispatch, 11 failing, **re-run at `76b09ff0`**); `clks_row_two_bits` (D3, 10) |
| D3C2 | SET_CLOCK_SOURCE(10): BAD_ARGUMENTS carrying 9; nothing stored, marked, enqueued or sent; nothing pending for two windows | `sclks-bound-inclusive` (dispatch, 6, **re-run at `76b09ff0`**) |
| D3C3 | the D3S1/D3R1 pair for AAF index 9 (REQ-AEM-013): one ERASE and WRITE of record 0x0A; restore applied | `clks_restore_count_narrowed` (D3, 2); `clks_row_two_bits` (D3, 10) |
| D3C4 | the saved 9 refused over a 9-source and a 3-source image | `clks_restore_index_narrowed` (D3, 4); `clks_restore_bound_inclusive` (D3, 4) |

The `d3_mutants.py` controls (`tb/pp_top/README.md:984-987`) were last run at `4a40b17` in R431-1 (87/87, every
count equal to the README) and at `39fd019` in round 1.

## Gates: processor, at `76b09ff0`

Everything ran from `git archive` exports of `76b09ff0` (`run-76b09ff0`, then `suites-76b09ff0`), except the docs
gates and `nvm_port figures`, which read git history and ran in the lane checkout. All rc 0.

| Command (workflow step) | Result |
|---|---|
| `./scripts/lint_hdl.sh` | 41 modules LINT OK |
| `./scripts/run_suites.sh` | 33 suites, 1,018,860 checks, 0 failing (572 s, run whole after a per-suite cold build; `tb/pp_top` 8,918) |
| `make -C tb/srp_top mutants` | 7 `--only` chunks over the 73 labels: 78 entries KILLED, 11 controls PASS, assertion coverage 65/65 (`srp_summary.txt`): the whole run's 90 of 90 |
| `make -C tb/maap mutants` | 32 of 32, one run (287 s) |
| `make -C tb/adp_engine mutants` | 32 of 32, one run (411 s) |
| `make -C tb/pp_top aecp-mutants` | 55 of 55 KILLED, 5 controls PASS (item 2) |
| `make -C tb/pp_top aecp-dispatch-mutants` | 37 of 37 KILLED, 4 controls PASS (item 2) |
| `python3 scripts/gen_matrix.py --check` | 94 rows, 0 untested |
| `make -C tb/nvm_port figures` | all measured figures agree with the tree, one run |
| docs-gates: `check-links.py`, `check-matrix.py`, `check-integrator-params.py`, `render-wavedrom.py --check`, `make stale`; and `make check` | 1,017 links; 115 REQ, 17 GAP; 26 parameters; 18 wavedrom; 41 mermaid; not stale |
| portability: `./syn/yosys/run.sh` (sv2v 0.0.13, Yosys 0.66) | 36 tops YOSYS OK; the Xilinx map OK |
| `scripts/check_upc_map.py`; `check_m9_opcodes.py --selftest` and plain | 59 constants / 87 entry points; 30 opcodes |
| `git diff --check 03c842a7 HEAD`, `git diff --check 4a40b17 HEAD` | clean |

Not re-run at `76b09ff0`: `d3_mutants.py` (87/87 at `4a40b17` in R431-1, and at `39fd019` in round 1),
`acmp_mutants.py`, `gsi_mutants.py`, `name_wr_mutant.py`, `acmp_talker/retry_mutants.py`,
`srp_admission/mutants.py` and `desc_mem_guard/mutate.py` (round 1, `39fd019`). The assignment's rule re-runs only
campaigns with a patch on a changed file, and none of these reads a byte that changed. `39fd019..76b09ff0` changes
five files: the `gen_ucode.py` comment (every ROM byte-identical), 06 §6.4's row, and the three dispatch patches,
which only `aecp_dispatch_mutants.py` reads.

## Gates: parent consumer set, milan-fpga dev `cdf49d1a`, gitlink at `76b09ff0`

Scratch parent `$VALIDATION_STORAGE/pp141-a495/parent`:

- A `git archive` of the read-only trusted checkout at `cdf49d1a28527562888f0a903de51b6b15b1244f`, with HEAD and index set to that commit (fetched read-only from the trusted checkout). 984 index entries, tree `904f3079`, working tree clean against it.
- `gptp-processor` `5dce647a` and `third_party/verilog-axis` `48ff7a7e` cloned from their recorded URLs, because the trusted checkout carries no submodule contents.
- `protocol-processor` a scratch clone of this branch checked out at `76b09ff0`, with the gitlink staged there. All three registered (`git submodule init`) and absorbed into `.git/modules`; `git submodule status` shows a blank prefix for each.
- `external` recorded and uninitialised, as in the trusted checkout.
- #137's `acmp_mutants.py` disposition line applied with `git apply`: PR #137 body, round 2 item 2, +4 lines in `DUT_READER_DISPOSITIONS` of `scripts/measure_test_evidence.py`, after the `d3_mutants.py` entry. Scratch patch sha256 `ee7d55466bbcc40fb78d644aa83751b5d91d6c5ffbd0dca0b38eb243012fe4e6`. Apart from the gitlink it is the only change; `scripts/test_evidence.budget` is untouched.
- The trusted checkout was not modified: HEAD is `cdf49d1a`. Its one ignored entry, `scripts/__pycache__/`, dates from 07:35, before this session.

Verilator jobs: under `make -j8`, each Verilator build was held to one job (`PP141_VJOBS=1`, plus `VERILATOR_JOBS=1`
for `milan_dp`), and to four for `milan_dp_render`'s two parallel legs. `nvm_cosim` used its own default of 8.

| # | Gate | rc | Result |
|---:|---|---:|---|
| 1 | `check_cpp_idiom.py` | 0 | every ratchet held |
| 2 | `check_py_idiom.py` | 0 | every ratchet held (too many parameters 7 <= 7) |
| 3 | `xvlog_gate.py --check` | 0 | 4 findings == ratchet (0 `hdl/`, 4 pinned processors), pinned at `protocol-processor@76b09ff0`; 145 s, alone |
| 4 | `check_rtl_source_lists.py` | 0 | 107 files, 4 of 4 lists; processor 36/42 tops, 6 recorded |
| 5 | `pp_srcs.py --check --selftest` | 0 | |
| 6 | `sw/builder/test_builder.py` | see note | 99 of 100 gate functions rc 0; **gate 1b not completed** |
| 7 | `make -C tb/verilator/pp_shadow -j8` | 0 | 606, 606, 646, 311 checks, 0 failures |
| 8 | `check_port_contracts.py` | 0 | processor 111 <= 111 undocumented; lowerable by 3 |
| 9 | `measure_naming.py --check` | 0 | 96 recorded |
| 10 | `measure_test_evidence.py --check` | 0 | 72 <= 77, 10 <= 10, 0 <= 0 unexplained readers, 3 <= 3; the same after the builds |
| 11 | `docs_check.py` | 0 | 0 findings (185 md + 956 text files) |
| 12 | `make -C tb/verilator/nvm_cosim lint` | 0 | |
| 13 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 of 315 |
| 14 | `make -C tb/verilator/milan_dp -j8` | 0 per part | every RESULT PASS (9); `render_mutants.py` 6/6; `gmstep_mutants.py` 6/6 (see note) |
| 15 | `make -C tb/verilator/milan_dp_render -j8` | 0 | both legs RESULT PASS (65, 152 checks); leg defects 5/5; one run (341 s) |
| 16 | `lint_rtl.py --check` | 0 | 90 <= 90 |

Note on 6. `test_builder.py` has no gate selection. A scratch runner (`scripts/test_builder_slice.py`) read the
gate tuple from the script's own `__main__` block (100 functions) and mirrored that block's imports. It ran the
functions in order, in fresh processes, starting no new function after a time budget. Gates 0-11 and 13-99 passed.
The only SKIP is the calibration gate, whose mf48 build tree is not on this host, as in round 1. Gate 12,
`test_baremetal_profile_contract`, compiles each of many firmware mutations with the RV32 compiler. It printed 4 of
its 28 sub-gate lines, each PASS, in 570 s, then reached the bound. One run of the whole script also reached the
bound (590 s, rc 124). Gate 12 reads no processor file: its processor mentions are message strings.

Note on 14. One `make` is longer than one foreground command: 14 builds, three prerequisite simulations, 11 pool
simulations at the `sim_pool.py` ceiling of `--jobs=2` (#517), then two mutation campaigns. It ran in parts:

1. Run 1 (`make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=1`) built all 14 binaries and stopped at the bound inside the pool.
2. Run 2, the same command, re-ran the pool and passed eight of its simulations before the bound cut `aclk`.
3. Run 3, the same command plus `SIM_JOBS=8`, re-ran every Verilator command as up to date and passed the three prerequisite simulations (`gptp` 182/0, `gptplat` 182/0, `gmstep` 104 RESULT PASS). It then stopped, rc 2, because `sim_pool.py` refuses `--jobs=8`; no pool simulation started.
4. The recipe's own `sim_pool.py --jobs="2"` command, with its exact arguments, ran in two halves: A (`sim`, `notify`, `crflic`, `nxn`, `nxndv`) rc 0 in 59 s, and B (`nxn8`, `nxn4c`, `nolpf`, `prune`, `ax1x1`, `aclk`) rc 0 in 541 s.
5. `render_mutants.py` (6/6, 573 s) and `gmstep_mutants.py` (6/6, 524 s) ran from `tb/verilator/milan_dp`.

## Parent-visible list

- **No change from round 2.** `76b09ff0` touches three test patches under `tb/pp_top/aecp_dispatch_mutations/`. The parent neither builds nor reads them.
- Round 1's list stands:
  - No interface or behaviour change: the only `hdl/` change is the `gen_ucode.py` comment, and every ROM is byte-identical.
  - No new parent registry entry and no budget change. `measure_test_evidence.py --check` holds 0 <= 0 with #137's line alone; that line is still owed by the pin bump.
  - Processor totals: `tb/pp_top` 8,918, D3 150, sweep 1,018,860 (re-measured: `run_suites.sh` at `76b09ff0`).
  - Names for adoption: D3C1 to D3C4. The parent's own L6 (`docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:89`) still cites 7.4.23.1.
  - The top's `aecp_clk_src_index_o` is unchanged.
- The parent set ran with the gitlink at `76b09ff0` (above).

## Scratch, receipts and hygiene

Scratch root `$VALIDATION_STORAGE/pp141-a495/` (outside the tree and this directory): `scripts/` (`apply_check.sh`,
`defect_identity.sh`, `chunk.sh`, `srp_chunk.sh`, `suite_group.sh`, `compare_readme.py`, `test_builder_slice.py`),
`chunks/` (the `--only` partitions), `logs/`, the exports and the scratch parent. Key logs (sha256 prefix, bytes):

| Log | sha256 (16) | Bytes |
|---|---|---:|
| `apply_check_4a40b179.log` | `ecddde05cef7f575` | 21,205 |
| `apply_check_76b09ff0.log` | `72073190676063e7` | 21,174 |
| `defect_identity.log` | `13a3e59f46cb42ac` | 749 |
| `dispatch-d1.log`, `-d23`, `-d456`, `-d7` | `5653f370…`, `e32f3147…`, `51462512…`, `0ee93fd6…` | 7,284; 9,963; 8,533; 2,243 |
| `compare_dispatch.txt` | `9559c4e8c9c67ece` | 2,121 |
| `aecp-a1.log`, `-a234`, `-a56`, `-a78` | `64e3e878…`, `e39125b4…`, `da03c4cd…`, `20f817b7…` | 5,968; 9,179; 36,020; 19,446 |
| `compare_aecp.txt` | `571c92bc40df5e53` | 3,197 |
| `run_suites.log` | `ebe473543a2f74d3` | 1,746 |
| `srp_summary.txt` | `d5c9f8a0ba5ee0cf` | 154 |
| `parent-xvlog_gate.log` | `99d0a494af5cb30f` | 1,320 |
| `parent-test_builder-s0.log`, `-s13.log` | `9c145c2d761052ba`, `9ecaf3cd0f20a866` | 10,506; 43,900 |
| `parent-pp_shadow.log` | `d7e15e60896aae72` | 264,465 |
| `parent-milan_dp-simA.log`, `-simB.log` | `54713c8f3335f3d2`, `5a56c18391b7a76e` | 410,082; 521,040 |
| `parent-milan_dp_render-1.log` | `64de089fbff956fa` | 170,129 |

Hygiene:

- The lane tree is clean (`git status --ignored` empty). Three generated entries were removed from it: `tb/pp_top/__pycache__/` (an import of the drivers to list their arms), `.venv-wavedrom/` (`make check`'s bootstrap) and `tb/nvm_port/__pycache__/` (`nvm_port figures`).
- One slip, after all campaign chunks had finished: an empty `git init` was run by mistake in the scratch export `run-76b09ff0`. Its removal was declined, so later runs used a fresh export, `suites-76b09ff0`. No result depends on that export after the slip.
- Nothing in this directory is over 200 KB, and it holds no toolchains, virtualenvs or tree exports.
