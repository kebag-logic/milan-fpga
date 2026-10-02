# HANDOFF: lane P2, round 2b (merge only), executor [A506]

**Status: REVIEW READY.** Both items are done in order, and every gate below is rc 0 at the head.

- Assignment: processor #15 comment 5959104191 (two items, in order). TAKEN: #15 comment 5959112223. REVIEW READY: #15 comment 5960259376.
- Branch `p2-nvm-port-robustness`. Start head `c26b14b316f14abdbe1080f2649f7df83bce061a` (round 2, REVIEW READY 5959067531).
- Main merged: `631eeb342ca1e3fa80e734077a56a943aee76ff1` (PR #142, P141; it contains #139's merge `2ebd4fe8`, this lane's base).
- **Round-2b head: `c0715410418b47ffaccf5feed55b71617fcfaf82`.** It is the merge commit, with parents `c26b14b3` and `631eeb34`. Local only: this lane does not push.
- Every `file:line` below is at the round-2b head unless it names another revision.

| Commit | Subject | Item |
|---|---|---|
| `c0715410` | Merge main 631eeb34 (#142) into the NVM port lane, keeping both sides: 09 §8.2's D3C row and its dispatch-campaign sentence beside the lane's pointer to §8.5, which keeps its number | 1 |

STOP conditions: none met.
- No port, parameter, register or RTL change.
- `git diff c26b14b3 c0715410 -- hdl` is main's comment in `hdl/aecp/ucode/gen_ucode.py` alone. The ucode ROM is byte-identical at both heads: 26,624 bytes, sha256 `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8`.
- `hdl/packet_engine`, `hdl/nvm` and `hdl/top` equal `c26b14b3`.
- No parent file was touched beyond the scratch copy.

## Findings

None. Round 2b answers no review: it is the merge alone. So there is no change per finding and no check that newly fails without one.

## Item 1: the merge

`git merge --no-ff 631eeb34`, one commit, `c0715410`. No rebase and no other merge.

**What main brought** (`git diff 2ebd4fe8 631eeb34`, 14 files): P141's SET/GET_CLOCK_SOURCE work. That is `tb/pp_top` section D3C (`d3_phases.hpp`, `sim_main.cpp`, `pp_top_wrap.sv`), its six mutants (`d3_mutants.py`, `aecp_dispatch_mutants.py` and two new `sclks-*` patches, plus a refreshed `lk-prefix-zero-body.patch`), a comment in `hdl/aecp/ucode/gen_ucode.py`, the `tb/pp_top` README, and the docs: L6 (07), REQ-AEM-013 and REQ-MDL-005 (00), 06 §6.4's SET_CLOCK_SOURCE row, and 09 §8.2.

**Overlap with this lane:** two files, 07 and 09. Main touches no file under `hdl/nvm`, `hdl/packet_engine`, `hdl/top`, `tb/nvm_port` or `tb/acmp_nvm`.

| File | Merge | Result, and the contract it serves |
|---|---|---|
| `docs/architecture/07_memory_maps.md` | auto-merged, disjoint hunks | Main's L6 row is at `:135`. The lane's restore-table rows and drain paragraph are at `:639`, `:649-657` and `:701` (DEADLINE beside DEVICE; the drain answered by the port's deadline). Both sides' contracts stand unchanged. |
| `docs/architecture/09_verification.md` | one conflict, §8.2's closing paragraph (`:208-215`) | Both sides kept. Main's D3C row (`:206`) and its 87-control count; main's sentence that the two SET_CLOCK_SOURCE range-check controls run from `aecp_dispatch_mutants.py`'s `d3` target (`:211-212`). The lane's tail stays (`:212-215`): the top's device model grades the walks' deadlines, and "the port's own deadline, resets and handshake models are §8.5's". Main's side still carried the base's "#18, #19, #21 are not closed by this evidence" sentence, re-wrapped and otherwise unchanged. The lane had deliberately replaced it, because this PR closes those issues, so the pointer stays. |

Checks on the result (`git diff --cached` before the commit):
- Every file only main changed equals `631eeb34`: `tb/pp_top`, `hdl/aecp`, 00, 06.
- Every file only the lane changed equals `c26b14b3`: `hdl/packet_engine`, `hdl/top`, `tb/nvm_port`, `tb/acmp_nvm`, 01, 02, 08, the integrator guide, diagram 21.
- `git diff --check` is clean.
- `git grep` for the dropped sentence's phrases ("not closed by this", "no handshake-misbehaving", "no reset mid-commit") finds nothing.

**Section number.** This lane's section stays **09 §8.5**. Main's 09 ends at §8.4, so main does not use 8.5. Lane C8 (PR #144) also adds an §8.5; per the assignment, whichever lane merges second renumbers, so nothing is renumbered here for C8.

**Citations the merge moves.** The merge shifts 09 by +2 lines from `:206` on: §8.3 moves from `:215` to `:217`, and §8.5 from `:293` to `:295`. 07, 06 and 00 keep their line counts. The audit:
- `git grep` for every `file:line` and `file#Lnnn` citation in the tree (patches excluded) finds 14. They point into `KL_pp_nvm_port.sv`, `KL_aecp_nvm_writer.sv`, `protocol_processor_top.sv`, `KL_pp_shadow.sv`, `KL_pp_maap.sv`, `KL_pp_acmp_listener.sv` and `09_verification.md:56`. Main changed none of those files. `09:56` sits above main's hunk, with its text unchanged.
- PR-BODY.md's 14 citations name those files, plus `tb/nvm_port/sim_main.cpp`, `KL_acmp_nvm_shadow.sv`, `KL_aecp_resp_buf.sv` and `KL_aecp_desc_store.sv`. Main changed none of them.
- Main's new text cites no line in a file this lane changed.
- No heading changed on either side, so every anchor resolves. `check-links.py` gives 1,045 links OK, round 2's figure.
- So no citation needed a fix.

The compliance review's persistence rows (REQ-ACMP-021, REQ-AEM-011/013/015, REQ-NOT-005, REQ-PER-001..003) were read at the head. Main changed REQ-AEM-013's finding cell (D3C1 to D3C4). This lane changes no row, and the merge needs none.

## Per item: device models, mutations and RTL

- **Item 1:** no device model, mutation or RTL change. The `tb/nvm_port` models and every mutation row re-measured equal to round 2 (the figures gate, below): pristine, half-page, page-buffered NOR, lazy erase, lazy + page-buffered, coincident and unsolicited at 343 PASS, 0 FAIL each; short read 265/78 and silent 115/228. D18-D26 and D26/coincident at 1, 1, 1, 1, 2, 0, 3, 7, 0 and 5.
- **Item 2:** measurement only.

## Item 2: re-measure, at `c0715410`

Pinned Verilator 5.050 (`$VALIDATION_TOOLS/pinned-verilator-5.050`). Every processor command ran on a `git archive` export of the head under `$VALIDATION_STORAGE/ppP2-a506/`. The exception is the figures gate, which ran in the lane tree; the tree was clean afterwards, ignored files included. Logs and rc files are in `$VALIDATION_STORAGE/ppP2-a506/{gates,pgates,logs}`; none is in this directory.

**Suites and gates, all rc 0:**

| Command | rc | Result |
|---|---:|---|
| `git apply --check`, every `*.patch` in the tree, at the tree root (as every driver applies them) | 0 | 207 of 207: `tb/srp_top` 73, `tb/pp_top/mutations` 42, `tb/pp_top/aecp_dispatch_mutations` 37, `tb/adp_engine` 28, `tb/maap` 27 |
| `./scripts/run_suites.sh` | 0 | UPC map gate (61 constants, 89 entry points), M9 opcode gate (30, selftest 9 of 9). 33 suites, 1,019,705 checks, 0 failing; 1,042 s. Each suite's tally equals round 2's except `pp_top`: 9,168 = 9,151 + main's 17 D3C checks. `nvm_port` 686 = 343 + 343; `acmp_nvm` 388 |
| `make -C tb/nvm_port figures` | 0 | 88 builds: 1 baseline, 2 `make run`, 12 arms, 59 mutations and probes, 9 models, 5 matrix. Baseline 343/343; `make run` [(343, 343, 0), (343, 343, 0), (686, 686, 0)]. All 87 measured rows agree; one waiver (2 illustrative phrasings); 593 s |
| CI docs job one by one: `check-links.py`, `check-matrix.py`, `check-integrator-params.py`, `render-wavedrom.py --check`, `make stale`; then `make check` and `gen_matrix.py --check` | 0 each | 41 mermaid + 18 WaveDrom; links 1,045; REQ 115 rows, 17 GAP; module matrix 94 rows, 0 untested; parameters 28 = 28 = 28 |
| `./scripts/lint_hdl.sh` | 0 | 41 modules, LINT OK |

**Mutation campaigns.** Each re-ran because a file it reads changed in the merge: it builds `tb/pp_top`, where main changed `d3_phases.hpp`, `sim_main.cpp` and `pp_top_wrap.sv`, and the generated ucode from `gen_ucode.py`. Some drivers are also files main changed.

| Campaign | rc | Result | Time |
|---|---:|---|---:|
| `make -C tb/pp_top aecp-mutants` | 0 | 5 controls PASS, 55 of 55 KILLED; every arm's `failures=` equals round 2's | 1,113 s |
| `make -C tb/pp_top aecp-dispatch-mutants` | 0 | 4 controls PASS, 37 of 37 KILLED. Against round 2, new are only main's `d3` control and `sclks-bound-three` (11) and `sclks-bound-inclusive` (6), as P141 records | 1,104 s |
| `python3 tb/pp_top/d3_mutants.py --jobs 3` | 0 | goldens PASS (`tb/acmp_nvm`, `pp_top`, `rx_validator`); **87 of 87 KILLED** by their named checks. All 75 `tb/pp_top` failing counts equal the README table. The 12 `tb/acmp_nvm` and 2 `rx_validator` rows equal round 2's. The moves against round 2 are exactly P141's: `TRG_clks` 5 to 10, `RPL_clks` 3 to 5, `rule_ignored` 3 to 7, `unframed_reads_as_device_error` 38 to 42, `done_without_d3` 42 to 45; new `clks_row_two_bits` 10, `clks_restore_count_narrowed` 2, `clks_restore_index_narrowed` 4, `clks_restore_bound_inclusive` 4 | 2,388 s |
| `make -C tb/maap mutants` | 0 | 3 controls, 29 of 29 KILLED; each arm equals round 2's | 291 s |
| `make -C tb/adp_engine mutants` | 0 | 2 controls, 30 of 30 KILLED; each arm equals round 2's | 470 s |
| `python3 tb/pp_top/acmp_mutants.py --jobs 2` | 0 | 19 of 19 KILLED, 3 goldens PASS. Each failing count equals its README (`tb/pp_top` 14, `tb/acmp_listener` 4, `tb/rx_validator` M6 27 FAILs) | 286 s |
| `python3 tb/pp_top/notify_mutants.py --jobs 2` | 0 | 40 of 40 KILLED, goldens PASS; each failing count equals the `tb/pp_top` README | 495 s |
| `python3 tb/pp_top/gsi_mutants.py` | 0 | 20 detected by named checks; golden and restored PASS | 1,037 s |
| `python3 tb/pp_top/name_wr_mutant.py` | 0 | `decode` killed; golden and restored PASS | 43 s |
| `./syn/yosys/run.sh` (it runs `gen_ucode.py`) | 0 | 36 tops OK and the Xilinx memory-map check (`KL_aecp_engine`), as in round 2 | 135 s |

**Not re-run: no file they read changed in the merge.**
- `make -C tb/srp_top mutants` (round 2: 78 of 78).
- `tb/acmp_talker/retry_mutants.py`: it copies `hdl`, `tb/acmp_talker` and `tb/common`, and its build never runs `gen_ucode.py`.
- `tb/srp_admission/mutants.py`.
- `tb/desc_mem_guard/mutate.py`: it builds `KL_aecp_desc_store.sv` and `KL_aecp_desc_mem_guard.sv`.

None builds `tb/pp_top` or runs the ucode generator.

**Parent consumer set (16)** at milan-fpga dev `cdf49d1a`. The scratch copy is `$VALIDATION_STORAGE/ppP2-a506/parent`, built by `mkparent.sh` (round 2's, re-pointed):
- a `git archive` of the trusted checkout, 984 index entries;
- gptp-processor `5dce647a` and verilog-axis `48ff7a7e`, made repositories at their pins;
- the processor gitlink at `c0715410`;
- `parent-adoption-c4c6-ea3fb388.patch` then `parent-adoption-p2-cdf49d1a.patch`, each `git apply --check` clean, then committed;
- the porcelain empty before the gates and after them;
- the trusted checkout unmodified (clean, HEAD `cdf49d1a`).

All rc 0:

| # | Command | rc | Result (vs round 2) | Time |
|---:|---|---:|---|---:|
| 1 | `check_cpp_idiom.py` | 0 | log identical: build without warnings 0 <= 0, long function 0 <= 0 | 1 s |
| 2 | `check_py_idiom.py` | 0 | 294 modules, 188,346 lines (round 2 188,315; +31 are main's); 9 <= 9, 10 <= 10 | 4 s |
| 3 | `check_rtl_source_lists.py` | 0 | identical: 107 files, 4 of 4 lists; 36/42 tops, 6 recorded | 1 s |
| 4 | `pp_srcs.py --check --selftest` | 0 | pass | 0 s |
| 5 | `check_port_contracts.py` | 0 | identical: processor 1,757 ports, undocumented 111 <= 111 | 3 s |
| 6 | `measure_naming.py --check` | 0 | identical | 1 s |
| 7 | `measure_test_evidence.py --check` | 0 | identical | 6 s |
| 8 | `docs_check.py` | 0 | identical: 0 findings over 185 md + 956 files | 5 s |
| 9 | `xvlog_gate.py --check` | 0 | 4 findings == ratchet, the same four; only the pin line differs (`c0715410`) | 162 s |
| 10 | `sw/builder/test_builder.py` | 0 | all gates pass except gate 11, not run (needs a local build tree, as before) | 1,531 s |
| 11 | `lint_rtl.py --check` | 0 | 90 <= 90 | 26 s |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 606, 606, 646, 311 checks, 0 failures (identical) | 323 s |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | pass | 1 s |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 of 315 | 47 s |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | 9 benches RESULT: PASS; 4 mutant arms caught, the same 4 | 1,763 s |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | 65 + 152 checks, 0 failures; 5 of 5 leg-defect arms | 331 s |

Peak anonymous memory of this service over the concurrent runs: 8.3 GB (cap 12 GB).

## Parent-visible list

1. **Nothing the parent instantiates changed.** The port, arbiter and top sources equal round 2's. No port or parameter changed. `KL_pp_shadow` needs no edit, and the port-contract count is unchanged (1,757).
2. **Both patches unchanged:**
   - `parent-adoption-p2-cdf49d1a.patch`: sha256 `3dda850924ffe4150aa33703ac82c0784035e3387070b7c9b5fc537a7467d08b`, 9,728 bytes.
   - `parent-adoption-c4c6-ea3fb388.patch`: sha256 `67bcd69852e5d090abc635e8dd66e5159667847ebf83d85aba9599d7cff7bd7c`, 2,687 bytes.

   Both are byte-equal to round 2's, and both apply cleanly at `cdf49d1a`.
3. **Processor documents the parent reads** are unchanged by the merge: 02 §8 (`sec-02-nvm-deadline`), F08.1, the integrator guide's `NVM_MEM_TMO_CYC_P` row, 09 §8.5. 09 §8.5 keeps its number, and the renumbering against C8 falls to whichever merges second.

## Out-of-context cost

Unchanged, and not re-run: its only input, `hdl/packet_engine/KL_pp_nvm_port.sv`, is byte-identical to round 2's (sha256 `20525cbd5ed14436fc725cf525c89567e43cabd5b43299703dea5db0404efbf2`). Round 2's figures, sv2v v0.0.13 then Yosys 0.66 `synth_xilinx -family xc7 -flatten`, against main's 197 LUT, 118 FF, 14 CARRY4:

| Configuration | LUT | FF | CARRY4 | vs main |
|---|---:|---:|---:|---|
| the default, 100,000,000 | 245 | 148 | 21 | +48 LUT, +30 FF, +7 CARRY4 |
| the smallest legal value, 1 | 248 | 122 | 14 | +51 LUT, +4 FF |

## Scratch, not in this directory

All under `$VALIDATION_STORAGE/ppP2-a506/`:
- `gates/` (run.sh, export.sh, docs.sh, logs, rc files);
- `pgates/` (run.sh, light.sh, heavy.sh, logs);
- `logs/` (the figures log, the memory log);
- `parent/` and `src/`;
- `c-*` (the campaign exports and outputs);
- `rom/` (the two ucode builds);
- `mkparent.sh`, `chainX.sh`, `chainY.sh`, `figures.sh`, `memmon.sh`.

The lane tree stayed clean, ignored files included.
