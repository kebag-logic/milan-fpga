[R754] POSITIVE - exact head 79fdea05ef54e2c99a0aa6efeadaa0f509076e92

Round R754-4. External cleared-context review of kebag-logic/milan-fpga PR #825 (#797 lane R1). Tree `0a92dabeca98bfc973dc43e67a3819ef804f892e`. Delta `e90284bd..79fdea05`: five commits, docs and scripts only (`REGISTER_MAP.md`, `register_descriptions.json`, `register_fields.py`, `register_page.py`, `register_sv.py`, new `register_read_sweep.py`). No RTL, firmware, SoC or submodule file moved in the delta. Source base `1e80128f`. Live dev `503bc97c` is the manager's merge-turn candidate and is not validated here.

No MINOR, MAJOR or BLOCKER is open. Both prior findings are resolved at their cause. Every one of the 17 read tables holds as printed on the shipping build and on a 2x2 build. The sweep that proves this reads the clauses the way the page prints them, and it catches every wrong row I planted. I record two suggestions. Three earlier residue items are still open and are carried to the residue checklist.

## Findings

No MINOR, MAJOR or BLOCKER.

### S1 - SUGGESTION - Robustness, Tests - `scripts/register_sv.py:390`, `:867` - the new selection read cannot see the loop step

- **Evidence:** `for_statement` throws away the loop's step (`while self.take() != ")": pass`, `:390`). `selection()` (`:867`, new in `dbe2b143`) checks the start (0), the bound (`v < N`) and the pick (`x == v`). Its docstring describes `v++`, but it cannot check the step.
  - Probe `gen_step2` changed `milan_csr.sv:2447` to `s += 2`.
  - `--write` left `REGISTER_MAP.md` byte-identical (`receipts/probes/gen_step2.page.diff.rc` = 0).
  - `--check` then reports fresh and `--selftest` gives 61/61 (`gen_step2.check.log`, `gen_step2.selftest.log`).
  - Against that RTL, the 2x2 sweep reports 96 `RENDER_STAT` disagreements at listener index 1 (`sweep_step2_rtl.log`). So the "holds at any `N_LISTENERS_P`" property depends on a form that the reader neither refuses nor reads.
  - The older unroll path has the same cause, since it always steps by +1 (`:841-842`).
  - Control `gen_le` (`s <= N`) does change the page (`gen_le.page.diff`), so the shape test works where it can see.
- **Why not MINOR:** every statement at this head is true. The loop is unit-step. The selection read is exact for it on the shipping, 2x2 and wider builds, because `x < N_LISTENERS_P` with `STRM_SEL[8]` at 0 is exactly `win_in_range_w` (`milan_csr.sv:1109-1110`). Reaching the hole takes a deliberate RTL edit. That is the same class the previous R754 round recorded as S4.
- **Suggested outcome:** the parser keeps the step and refuses anything except `v++`, `v += 1` and `v = v + 1`, on both the selection path and the unroll path. Add one selftest control: the step-2 mutant exits 2.

### S2 - SUGGESTION - Tests - `scripts/register_read_sweep.py:55-56`

- The "2x2" build includes `configs/generated/endstation_arty_4x4` and overrides the stream counts with `-G`.
- This is harmless, because the comment at `:54` says the window decode reads none of those headers.
- A shape header whose name matches the build would remove the question.

## Focus results

### (1) R753-3 F1: `STRMW_SRP` index 0 by the value of `STRM_SEL[9]`

- The RTL is `strm_mux = ((strm_idx_r == 0) && !srp_idx0_ls_w) ? i_lwsrp_status : (srp_fresh_r ? {16'd0, i_srp_ctx_rd_stat} : 0)` (`milan_csr.sv:2574-2576`), with `srp_idx0_ls_w = strm_lsn0_r && (SRP_LSN0_ROW_P != 0)` (`:2528`). It has no direction term.
- At the page's `SRP_LSN0_ROW_P` = 2 (`REGISTER_MAP.md:249`), and on every datapath build (`SRP_LSN0_ROW_C` >= 1 at `milan_datapath.sv:1891`), the wire equals `STRM_SEL[9]`. So:
  - row `REGISTER_MAP.md:3638`, "index 0 and `STRM_SEL[9]` is 0", gives `i_lwsrp_status`;
  - row `:3639`, "`STRM_SEL[9]` is 1 and a poll answered", gives the status;
  - row `:3640`, "index not 0 and a poll answered", gives the status.
- All three are exact, at `SEL` `0x300` and everywhere else. The field row at `:3634` uses the finding's wording.
- `STRM_SEL[9]` is write-only and reads 0 (`REGISTER_MAP.md:3396`, `milan_csr.sv:2535`). The sweep keeps the last value written, and checks after each step that `STRM_SEL` reads back `sel & 0x10F` (`register_read_sweep.py:328`).
- Sweep at head: `STRMW_SRP` has 0 disagreements on both builds (`receipts/sweep_head.log`).
- Plant A, the `[9]` row without its poll clause, gives 48 disagreements on shipping and 96 on 2x2 (`receipts/probes/sweep_plant_rows.log`).
- **Resolved.**

### (2) R754-3 F1: `RENDER_STAT` holds at any `N_LISTENERS_P`

- **RTL:** `for s < N_LISTENERS_P: if (!strm_dir_r && 32'(strm_idx_r) == s) live_mux = i_render_status[s*32 +: 32]` (`milan_csr.sv:2445-2451`).
- **`selection()`** (`register_sv.py:867`) rewrites that loop as `!strm_dir_r && x < N_LISTENERS_P`, with value `i_render_status[x*32 +: 32]`.
  - This is sound for a unit-step loop from 0. At most one pass assigns, and it is the pass where `v == x`. The other conjuncts are substituted with `v := x`.
  - The rewrite refuses (falls back to unrolling) when the pick is not `x == v`, when `x` mentions `v`, when there is an `else`, or when there is more than one pick.
- **`named()`** (`register_page.py:788`) prints `idx < N_LISTENERS_P` beside `!dir` as `win_in_range_w`, which is `dir ? idx < N_TALKERS_P : idx < N_LISTENERS_P` (`milan_csr.sv:1109`). That arm is the one the choice literal selects. The choice stays in the row. The substitution is an identity, given the literal that it keeps.
- **`register_fields.py:242`** names `x[i*w +: w]` as `x`'s word. The `RENDER_STATUS` field row is unchanged, and the page diff touches only the read row.
- The row "the selected stream exists and `STRM_SEL[8]` selects a listener" (`REGISTER_MAP.md:3974`) is the finding's text. It equals the decode at every `N_LISTENERS_P`, so it is not a fold to the shipping build.
- Sweep at head: 0 disagreements on both builds. Plant B, the previous row, gives 96 on 2x2 and 0 on shipping, which is the shape-only signature.
- My generator mutant `gen_le` changes the page. The step caveat is S1.
- **Resolved.**

### (3) The class: the sweep reads each clause as printed

- **The tables:** `read_tables` collects every `| When | A read returns |` table under its register heading, strides included. Both builds print 17 tables and 24,007 reads. A table that is printed but not swept refuses.
- **The clauses:** `holds()` splits a row on " and ", and a clause missing from `CLAUSE` (`register_read_sweep.py:77`) refuses with exit 2. Plant D, the old SRP wording, refused (`receipts/probes/sweep_plant_clause.log`). So did the head's sweep run on the `e90284bd` page (`sweep_e90284bd.log`).
- **How each clause is read:** each `CLAUSE` entry reads what the harness did or read back:
  - selection: what was written, checked by a readback;
  - `exists`: computed from the build's counts, not from `win_in_range_w`;
  - `snap`: `STRM_SNAP[0]`, read through the bus before and after the reads;
  - `srppoll`: a poll answer that came last, after the selection and after any `STRMW_CTRL` write;
  - `cmvalid`: `CHMAP_SNAP[1]`, read through `0x910` just before `0x914`.
- **What the harness sets inside the block:** it deposits only the counter kinds and the shadow words. The clause that reads them names the recorded kind. As documented, it reads `mac_wire_w` only for the value cell that names that wire.
- **The report:** every disagreement is printed with its state, and every table gets read and disagreement counts plus per-row hit counts. The two-row match conflict and the no-row case are both reported. The report is complete.
- **Reproduced:** the `fd12faf9` sweep on the `e90284bd` page gives exactly the PR's table (`receipts/probes/sweep_fd12_on_e90284bd.log`):

| Table | Shipping | 2x2 |
|---|---|---|
| `STRMW_SRP` | 60 | 108 |
| `STRMW_SID_LO` | 0 | 24 |
| `STRMW_SID_HI` | 0 | 24 |
| `RENDER_STAT` | 0 | 96 |
| `CHMAP_LOOP` | 4 | 4 |
| **Total** | **64** | **256** |

- **Plant C:** swapping the `CHMAP_LOOP` values gives 7 disagreements on each build.

### (4) The two rows the sweep found

- **SRP-served word:**
  - `srp_fresh_r` is set only by a read-type grant. It is cleared by a write-type grant (`milan_csr.sv:3113-3115`), by `srp_prov_w` (`:3120-3128`), by any `STRM_SEL` write (`sel_wr_w`) and by `i_srp_ctx_stolen`. That input is tied to 0 in `milan_datapath.sv:3010`.
  - `srp_prov_w` (`:3091-3093`) is a `STRMW_CTRL` write that is in range, at an index other than 0 or with the `[9]` row. Every `STRMW_CTRL` write that does not clear the flag happens in a state where no row's value depends on the flag: out of range, or index 0 without `[9]`.
  - A poll cannot be answered ahead of a pending write, because `o_srp_ctx_we = srp_wr_pend_r` (`:3137`).
  - So "the SRP table answered a poll since the last `STRM_SEL`/`STRMW_CTRL` write" is true as printed, at `REGISTER_MAP.md:3462`, `:3483` and `:3639-3640`.
  - The analogous ACMP clause is still exact: `acmp_fresh_r` is cleared only by reset and `sel_wr_w` (`milan_csr.sv:3154-3170`).
- **`CHMAP_LOOP`** (`REGISTER_MAP.md:4269-4270`):
  - `chmap_loop_rd_w = cmrd_valid_r ? ... : 32'hDEADDEAD` (`milan_csr.sv:1308`), and `CHMAP_SNAP[1]` is `cmrd_valid_r` (`:1286`).
  - A re-arm clears it (`:2773`). A timeout leaves it 0 (`:2791-2794`).
  - The harness reads never, answered, re-armed, timed out, answered, armed-unanswered and timed out. That gives 2 valid reads and 5 poison reads, and 0 disagreements.
- **Both true.**

### (5) Generator-fresh, and no other row changed

- `--check` is fresh (203 registers, 34 modules, 240 files) and `--selftest` gives 61/61 (`receipts/gen_check.log`, `gen_selftest.log`). `memory_map.gen.py --check` and `check_doc_style.py` give rc 0.
- `git diff e90284bd..79fdea05 -- docs/reference/REGISTER_MAP.md` is exactly the 9 rows named in the PR's Round 4 table. No SVG, diagram or other page moved.
- The removed `cmrd_valid_r` phrase is now printed from the register field. No other condition used it: `--check` would refuse an unworded condition.

## Prior findings at this head

| Finding | Status | Evidence |
|---|---|---|
| R753-3 F1 `STRMW_SRP` / `STRM_SEL[9]` | Resolved | Focus (1); the exact required wording; sweep 0; plant A |
| R754-3 F1 `RENDER_STAT` any `N_LISTENERS_P` | Resolved | Focus (2); the exact proposed row; 2x2 sweep 0; plant B |
| R753-3 RES1 (PR body "no `or`") | Resolved | The phrase is gone from the PR body |
| R754-3 R3 (PR body 12-of-17 scope) | Resolved | The Round 3 cell now says "A sweep of 12 of the 17 tables" and states Round 4's extension |
| R754-3 R2 (`[9]` condition words) | Superseded | Replaced by R753-3 F1's wording, which is true at the page's `SRP_LSN0_ROW_P` |
| R753-3 RES2 (`REGISTER_MAP.md:4503`, "a CPU write in the same cycle clears it") | Open RESIDUE, carried | Unchanged at head; its exact fix is in R753-3 |
| R753-3 RES3 (`CSR_REGISTER_NOTES.md:974`) | Open RESIDUE, carried | Unchanged at head |
| R754-3 R1 (`CSR_REGISTER_NOTES.md:78`, "every RW word still stores") | Open RESIDUE, carried | Unchanged at head |
| R753-3 S1 to S4, R754-3 S1 to S5, earlier carried suggestions | Not taken, optional | The PR body says so. R753-3 S1 is now superseded by R754-3 F1's fix |

## Residue

None new in the delta. The delta's source comments carry no bench lane labels, lane names, review rounds or reviewer IDs. They carry only `#797`. The five commits are one line each, with no trailers, and `git diff --check` is clean.

## Lens results

```text
[R754] PASS Conformance - REGISTER_MAP.md:3462,3483,3634-3640,3974,4269-4270 against milan_csr.sv:1109,1286,1308,2445-2451,2528,2535-2576,2773,3086-3137 - every changed row and clause is true as printed on shipping and 2x2; the R753-3 F1 and R754-3 F1 required outcomes are met
[R754] PASS RTL - git diff e90284bd..79fdea05 (no hdl/ path); milan_csr.sv:1109,2445-2451,2528,3113-3137 - no RTL change; the generator's reading of the selection loop, srp_idx0_ls_w and the freshness flops matches the decode
[R754] PASS Robustness - register_sv.py:867 selection(), register_page.py:788 named(), register_read_sweep.py holds()/read_tables() - unknown clause refuses (plant D rc 2), unswept table refuses, fallback to unrolling on a non-matching shape (gen_le control); the step gap is S1 (latent, needs an RTL edit)
[R754] PASS Tests - receipts/sweep_head.log, probes/sweep_plant_rows.log, probes/sweep_fd12_on_e90284bd.log - sweep 0/0 at head; plants A, B, C are caught; the 64/256 baseline is reproduced; selftest 61/61; the author's sweep controls and generator mutants (author-r4 receipts) agree
[R754] PASS Docs - PR #825 body Round 4 table, REGISTER_MAP.md diff, register_descriptions.json diff - the counts reproduce, the page is generator-fresh, only the named rows changed, no stale wording elsewhere (grep of *.md, *.json, *.py outside docs/history)
```

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Changed rows at `REGISTER_MAP.md:3462`, `:3483`, `:3634-3640`, `:3974`, `:4269-4270` against `milan_csr.sv` decode lines; sweep logs on both builds | R754-4 | `79fdea05ef54e2c99a0aa6efeadaa0f509076e92` |
| RTL | CLEAN | Delta file list (no RTL); `milan_csr.sv` selection loop, window range, SRP and ACMP freshness, channel-map readback | R754-4 | `79fdea05ef54e2c99a0aa6efeadaa0f509076e92` |
| Robustness | CLEAN | `register_sv.py` `selection` and `for_statement`; `register_page.py` `named`; `register_fields.py:242`; sweep refusal paths; mutants `gen_step2` and `gen_le` | R754-4 | `79fdea05ef54e2c99a0aa6efeadaa0f509076e92` |
| Tests | CLEAN | `register_read_sweep.py` at head and at `fd12faf9`; plants A to D; `--selftest`; author-r4 `controls.tsv` and `generator_mutants.tsv` | R754-4 | `79fdea05ef54e2c99a0aa6efeadaa0f509076e92` |
| Docs | CLEAN | PR body Round 4; page and descriptions diff; `--check`; doc style; stale-wording grep | R754-4 | `79fdea05ef54e2c99a0aa6efeadaa0f509076e92` |

Code outside the delta keeps its R754-3 lens verdict. The delta changes only what the read tables state and how the generator reads one loop form.

## Real limits

- Source-head execution only, in this clone. I ran:
  - generator `--check` and `--selftest`;
  - `memory_map.gen.py --check`;
  - `check_doc_style.py`;
  - the sweep, at head and on planted pages;
  - two generator mutants, and the `fd12faf9` sweep on the `e90284bd` page.
- The simulator was the scoped Verilator 5.050 (`receipts/verilator_version.txt`). The interpreter carries the pinned wavedrom 2.0.3.post3. Scripts: `run_gates.sh`, `run_probes.sh`, `run_fd12_sweep.sh`.
- I did not run:
  - the other docs-workflow steps (`docs_check.py`, `check_doc_paths.py`, `gen_toc.py`, `check_em_dash.py`, `ci_events.py`, behave). The author's round-4 runner receipts at `ca9452e9` show rc 0 for those, and I spot-checked them;
  - any manager source bank, builder bank or native bank;
  - hosted or act workflows;
  - Yosys;
  - hardware.
- No physical calibration was run, and field skips are not hardware proof.
- I swept 2x2 and the shipping build only. Wider shapes (4x4, 8x8) are covered by argument (focus (2)), not by simulation.
- After the probes, the clone is byte-identical: clean status, same index digest, and gitlinks equal to the checked-out submodule commits (`receipts/clone_state_after.txt`). All probe trees are under `scratch/`.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `1e80128f`, live dev `503bc97c`) and publish its receipts on the PR.
- Own hosted and act acceptance for the exact head, including exact-head `rtl-fast`, plus `verilator-suites` and `yosys-portability` where they apply.
- Carry R753-3 RES2, R753-3 RES3 and R754-3 R1 to the residue checklist.
- Merge only on explicit maintainer authorization.

R754-4 FINISHED
