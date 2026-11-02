[R753] NEGATIVE - exact head 79fdea05ef54e2c99a0aa6efeadaa0f509076e92

Round R753-4 is the internal cleared-context review of kebag-logic/milan-fpga PR #825 (#797 lane R1). It covers tree `0a92dabeca98bfc973dc43e67a3819ef804f892e` and the round-4 delta `e90284bd..79fdea05` (5 commits, in `docs/reference/REGISTER_MAP.md` and in `scripts/` only). The source base is `1e80128f`. Live dev `1f29f189` is merged, with one merge base. Across this round's delta, `git diff --stat e90284bd..HEAD` touches no `hdl/`, `sw/`, `syn/`, `configs/` or gitlink path.

**Why NEGATIVE:** one MINOR is open, F1. One of the two rows the sweep found is the SRP-served clause, and it is still weaker than what the RTL tests. The page says the word is served when "the SRP table answered a poll since the last `STRM_SEL`/`STRMW_CTRL` write". The RTL also drops the word to 0 in two cases:
- a provisioning write is answered after that poll answer;
- another master takes one beat of the table.

The block-level probe reads 0 in four states where the printed clause holds. The sweep never builds those states, and its harness defines `srppoll` as "the latest answer is a poll", not by the printed words. Everything else the round was asked to prove holds:
- R753-3 F1 is resolved;
- R754-3 F1 is resolved, and the generator change is exact, not a shipping-only fold;
- `CHMAP_LOOP` is exact;
- the sweep's per-table report reproduces to the count;
- the page is fresh, and no other row changed.

My verdict and ledger were written before I read any prior-round report (`receipts/own_verdict_before_prior_findings.md`). Reading those reports changed neither.

## Findings

### F1 - MINOR - Conformance, Robustness, Tests, Docs - the SRP-served clause omits two cases that zero the word

- **Where:**
  - The clause is printed at `docs/reference/REGISTER_MAP.md:3462` (`STRMW_SID_LO`), `:3483` (`STRMW_SID_HI`), and `:3639` and `:3640` (`STRMW_SRP`).
  - It is worded at `scripts/register_descriptions.json:4086-4087` (`srp_fresh_r`).
  - The sweep reads it at `scripts/register_read_sweep.py:88-91`, with its harness definition at `:300-308`.
- **Authority:**
  - #797 acceptance: no document marked current contains a statement the code contradicts.
  - This round's focus (4): the rows the sweep found are true against the RTL.
  - Focus (3): each clause is read as the page prints it.
- **RTL:** `hdl/common/csr/milan_csr.sv:3108-3133`.
  - `srp_fresh_r` is set by a grant whose command was a poll (`:3112-3117`).
  - It is cleared by a grant whose command was a write (`:3113-3115`), by a `STRM_SEL` write (`:3119`), by a provisioning `STRMW_CTRL` write (`:3120-3128`) and by `i_srp_ctx_stolen` (`:3132`). The port comment at `:624-630` says the window "reads 0 ... until its continuous poll refills it".
  - Two of those clears are missing from the printed clause: a write answer that arrives after a later poll answer, and a stolen beat.
- **Probe:** `probe_srp_poll_clause.py`, receipt `receipts/probe_srp_poll_clause.log`, rc 0. It runs the 2x2 build at talker index 1.
  - **Case A:** an engine grants on consecutive cycles around a provisioning `STRMW_CTRL` write, within the port contract the sweep's own `answer_srp` uses. With the grant at ticks 1-2, 0-2 or 1-3 from the write, a poll is answered after the write fires, and then the write itself is answered. Once the engine idles, `STRMW_SRP` reads `0x00000000` and `STRMW_SID_LO` reads `0x00000000`. In these states the printed rows say `{16'd0, i_srp_ctx_rd_stat}` (`0x00004444`) and `i_srp_ctx_rd_sid[31:0]` (`0x66666666`).
  - **Case B:** a poll is answered, with no write since. `STRMW_SRP` reads `0x00004444`. After one `i_srp_ctx_stolen` beat it reads `0x00000000`, and `STRMW_SID_LO` also reads 0. The clause still holds as printed.
- **Why the sweep reports 0:** its harness comment at `register_read_sweep.py:301-302` defines `srppoll` as "a poll answer is the latest answer, after the selection and after any STRMW_CTRL write". That is the RTL's meaning, not the page's words. The harness drives poll-only, write-only and write-then-poll sequences. It never drives poll-then-write or a stolen beat, so no state separates the two meanings. This is the class the round set out to remove: a clause read by its implementation-side meaning rather than by its words.
- **Shipping scope:**
  - The shipping datapath ties `srp_ctx_gnt_w` to 0 (`hdl/milan/milan_datapath.sv:8720`) and `i_srp_ctx_stolen` to 0 (`:3010`). On the shipping SoC no read differs, and the clause is never true there.
  - The read tables state the block decode in terms of its inputs. The round's evidence, the 2x2 sweep, is block-level, so the rows are claimed exact at block level.
- **The other half of the clause is fine:** "`STRMW_CTRL` write" is broader than the RTL's provisioning-only clear (`srp_prov_w`, `milan_csr.sv:3091-3093`). That is harmless: every CTRL write that does not provision is at a selection whose read does not use `srp_fresh_r` (index 0 with `STRM_SEL[9]` at 0, or out of range). It needs no change.
- **Why not RESIDUE:** it is a read-table clause claim that predicts a different read value in a reachable block-level state.
- **Why not RTL:** the RTL matches its own port comment. The defect is the statement and the evidence for it.
- **Impact:**
  - Someone integrating the block with a live SRP engine, or reading the table as the block's contract, expects the row's value. Within a few cycles of a provisioning write, or after another master's beat, they get 0.
  - The REVIEW READY says the found rows "now state what the RTL tests", and PR body Round 4 row `f7f6ea7d` makes the same claim. Neither is yet true for this clause.
- **Required outcome:**
  - The `srp_fresh_r` pair states every case that clears the word. One wording that matches `:3108-3133`: "the SRP table's latest answer to the window was a poll, after the last `STRM_SEL`/`STRMW_CTRL` write, and no other master has used the table since", with its negation.
  - The sweep reads that clause from states that separate it from the weaker reading: a poll answered and then a write answered, and a stolen beat after a poll answer.
- **Verification:**
  - `--check` is fresh after `--write`.
  - The extended sweep gives 0 disagreements on both builds.
  - The four marked states in `receipts/probe_srp_poll_clause.log` agree with the new rows.
  - The old wording, planted back, makes the extended sweep exit 1.

### Suggestions (optional, no effect on coverage)

- **S1 - Robustness - `scripts/register_sv.py:378-392`, `:830-849`, `:867`:**
  - `for_statement` discards the step text (`while self.take() != ")"`). Both the unroller and the new `selection()` therefore assume `v++`, and a loop stepping by 2 would be read wrongly instead of refused.
  - This predates the delta, and every loop in `milan_csr.sv` steps by 1 (`:1589`, `:1692`, `:1981`, `:2106`, `:2447`, `:2932-2983`). `selection()` widens what relies on it.
  - Refusing any step other than `v++`, `v += 1` or `v = v + 1` would keep the "outside the subset is a refusal" contract true.
- **S2 - Tests - `scripts/register_read_sweep.py:431-433`:**
  - The sweep refuses an unswept table, but not a row that neither build reaches.
  - Today every row is reached on 2x2. The 6 rows at 0 hits on the shipping build are all talker index 1 and above, which are vacuous there (`receipts/sweep_head.log`).
  - A refusal for a row with 0 hits on both builds would keep "every row is read" true as the tables change.
- **S3 - Docs - `REGISTER_MAP.md:3638-3639`, `:3396`:**
  - "`STRM_SEL[9]` is 1" names a write-only bit, and the field row says "A read returns 0", so a reader could take the clause as a read-back.
  - "the last `STRM_SEL` write set bit 9" cannot be read that way.
  - The current text is R753-3 F1's own required wording and is correct as the field row defines the bit, so this is optional.
- **S4 - Tests - `scripts/register_selftest.py`:**
  - No selftest control holds `selection()`, `named()` or the word-index branch at `register_fields.py:240-243`.
  - Today the committed page holds them through `--check`: each undo fails it (`receipts/mutants_generator_delta.txt`).
  - A small arm would hold the refusal side independently of the page: a loop with an `else`, or with two `x == v` terms, that must not be read as one selection.

### Residue

None new in the delta. No new source comment carries a lane label, review round, reviewer ID or comment ID. A grep of the added lines `e90284bd..HEAD` finds none, and finds no em-dash. Prior-round residue that is retained is listed below.

## Focus results

| Check | Result | Evidence |
|---|---|---|
| (1) R753-3 F1: `STRMW_SRP` index-0 rows by the value of `STRM_SEL[9]` | **Resolved.** The page carries the finding's exact wording: the field text at `:3634` and `srp_idx0_ls_w` at `register_descriptions.json:4093-4095`. Against `milan_csr.sv:2528` and `:2570-2576` at `SRP_LSN0_ROW_P` = 2 (page `:249`), `[9]` = 1 takes the poll path in either direction | `receipts/spot_reads_head.txt`. `SEL` `0x300` reads 0 with no answer, `0x4444` after a poll and 0 after a write answer only. `SEL` `0x100` reads the alias `0x33333333`. The same holds on both builds |
| (2) R754-3 F1: `RENDER_STAT` holds at any `N_LISTENERS_P` | **Resolved, exact.** The RTL is `for (s = 0; s < N; s++) if (!dir && idx == s) mux = word s` (`milan_csr.sv:2445-2451`). `selection()` reads it as `if (!dir && idx < N) mux = word idx`. Start 0, a `<` bound and exactly one `x == v` term free of `v` make at most one pass assign, so the two are equal for a step-1 loop (S1). `named()` maps `idx < N_LISTENERS_P` with `dir` = 0 to the listener arm of `win_in_range_w` (`:1109-1110`), and keeps the direction term. The word-index branch names `i_render_status[idx*32 +: 32]` as the 32-bit word, so the field table is unchanged | The row at `:3974` is the finding's wording. On 2x2, listener 1 reads `0x70000001` (`spot_reads_head.txt`). The mutants (`mutants_generator_delta.txt`, `mutant_m1.page.diff`, `mutant_m2.page.diff`): with `selection()` undone, `--check` exits 1 and the row reverts to the shipping fold "... is 0". With `named()` undone, it exits 1 and prints "is below `N_LISTENERS_P`". With the word branch undone, it exits 2 (refusal). Not a shipping-only fold |
| (3) The class: sweep over 17 tables on both builds, reading each clause as printed | **Holds except F1.** All 17 tables, 24,007 reads per build. The clauses are read from what the harness did or read back: `STRM_SEL` read back is checked, `STRM_SNAP[0]` is read and `CHMAP_SNAP[1]` is read. "Exists" comes from the page's build parameters, which is how the page defines it. Unknown clauses, values, `fields above` and unswept tables refuse. The per-table report gives reads, disagreements and hits per row | I reran the sweep at the head: 0 and 0 (`receipts/sweep_head.log`, rc 0). I ran the `fd12faf9` sweep on the `e90284bd` page: 64 on shipping and 256 on 2x2, matching the author's per-table table exactly. Shipping: `STRMW_SRP` 60, `CHMAP_LOOP` 4. 2x2: `STRMW_SRP` 108, `RENDER_STAT` 96, `STRMW_SID_LO` and `STRMW_SID_HI` 24 each, `CHMAP_LOOP` 4 (`receipts/sweep_fd12_on_e90284bd_page.log`). The author's eight controls hash-match the manifest (`receipts/author_r4_controls.tsv`). The exception is the `srppoll` reading (F1) |
| (4a) The SRP-served word after a provisioning write | **Improved, not yet exact (F1).** The write-answer case named in the commit is now right. The poll-then-write and stolen-beat cases are not | `receipts/probe_srp_poll_clause.log` |
| (4b) `CHMAP_LOOP` by `CHMAP_SNAP[1]` | **Exact.** `chmap_snap_rd_w[1]` is `cmrd_valid_r` (`milan_csr.sv:1286`), and `chmap_loop_rd_w` is `cmrd_valid_r ? fields : poison` (`:1308-1319`). A re-arm clears it (`:2773`), a timeout leaves it 0 (`:2791-2794`) and an answer sets it (`:2789`). The wording comes from the generator's field naming once the hand phrase was removed (`register_page.py:125-131`) | The 7 reads per build cover never, answered, re-armed in flight, timed out, answered, in flight and timed out. Two read the fields; five read `0xDEADDEAD` with `cmdone` = 1 on four of them, which the old clause would have called the fields (`spot_reads_head.txt`) |
| (5) Generator-fresh; no other row changed | **Holds.** `--check` rc 0, "fresh (203 registers, 34 modules, 240 files)". `--selftest` rc 0, 61/61. Memory-map `--check` rc 0. The page diff `e90284bd..HEAD` is 9 lines, all of them the rows named above. `git diff --check e90284bd HEAD` is clean | `receipts/gen_check.log`, `gen_selftest.log`, `memmap_check.log` |

## Prior findings at this head

| Finding | Status | Evidence |
|---|---|---|
| R753-3 F1 `STRMW_SRP` "listener row" | Resolved | Focus (1) |
| R754-3 F1 `RENDER_STAT` index 0 only | Resolved | Focus (2) |
| R753-3 S1 `RENDER_STAT` at 2x2 | Resolved by the R754-3 F1 fix | Focus (2) |
| R753-3 S2 to S4, R754-3 S1 to S5 | Not taken, optional (PR body Round 4) | No effect on coverage |
| R753-3 RES1, R754-3 R3 (PR body sweep scope) | Resolved | PR body Round 3 row now says "A sweep of 12 of the 17 tables"; the "no `or`" sentence is gone |
| R754-3 R2 (`STRM_SEL[9]` clause wording) | Resolved | Superseded by the R753-3 F1 wording. The page states `SRP_LSN0_ROW_P` = 2 at `:249` |
| R753-3 RES2 (`REGISTER_MAP.md:4503`, "a CPU write in the same cycle clears it") | Retained, RESIDUE | The text is unchanged. Exact fix as given in R753-3 |
| R753-3 RES3 (`CSR_REGISTER_NOTES.md:974`, the unconditional opening clause) | Retained, RESIDUE | The file is unchanged in the delta. Exact fix as given in R753-3 |
| R754-3 R1 (`CSR_REGISTER_NOTES.md:78`, "every RW word still stores") | Retained, RESIDUE | The file is unchanged in the delta. Exact fix as given in R754-3 |
| Earlier rounds' findings | Keep their prior closure | The delta changes none of what they depended on, apart from the rows judged above |

## Lens results

```text
[R753] UNCLEAN Conformance - docs/reference/REGISTER_MAP.md:3462,3483,3639,3640 against hdl/common/csr/milan_csr.sv:3108-3133 - F1; the other changed rows (:3634,:3638,:3974,:4269-4270) match milan_csr.sv:2528,2570-2576,2445-2451,1286,1308-1319,2765-2795
[R753] PASS RTL - hdl/common/csr/milan_csr.sv:1109-1110,1286,1308-1319,2445-2451,2528,2543-2576,2765-2795,3086-3137; hdl/milan/milan_datapath.sv:3009-3010,8720 - no RTL in the delta (git diff --stat e90284bd..HEAD: docs and scripts only; gitlinks equal HEAD, receipts/clone_state.txt); every decode the changed rows cite was read and simulated on two builds; the generator's loop reading equals the RTL loop for its step-1 form
[R753] UNCLEAN Robustness - receipts/probe_srp_poll_clause.log - F1 (poll/write ordering and stolen-beat paths); the out-of-range, snapshot-running, re-arm and timeout paths of the changed tables agree (sweep_head.log, spot_reads_head.txt); S1 is optional
[R753] UNCLEAN Tests - scripts/register_read_sweep.py:88-91,300-308 - F1 (srppoll is read by the RTL meaning, not the printed words; no separating state); the rest of the sweep reproduces to the count on both builds and against the e90284bd page; generator mutants m1-m3 each fail --check (mutants_generator_delta.txt); S2 and S4 are optional
[R753] UNCLEAN Docs - docs/reference/REGISTER_MAP.md:3462,3483,3639,3640; scripts/register_descriptions.json:4086-4087; PR body Round 4 row f7f6ea7d - F1; --check fresh, page diff limited to the 9 named rows, git diff --check clean, no lane, round, reviewer or comment ID in the delta, retained residue listed
```

## Completion ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | The 9 changed page rows against the cited `milan_csr.sv` lines; the probe | R753-4 | `79fdea05ef54e2c99a0aa6efeadaa0f509076e92` |
| RTL | CLEAN | `milan_csr.sv` decodes and flops behind each changed row; `milan_datapath.sv` SRP port ties; no RTL in the delta; 2 simulated builds | R753-4 | `79fdea05ef54e2c99a0aa6efeadaa0f509076e92` |
| Robustness | UNCLEAN (F1) | SRP grant ordering and stolen-beat probe; out-of-range, snapshot, `CHMAP` re-arm and timeout paths; generator loop subset (S1) | R753-4 | `79fdea05ef54e2c99a0aa6efeadaa0f509076e92` |
| Tests | UNCLEAN (F1) | `register_read_sweep.py` (rerun on both builds, and the `fd12faf9` copy on the `e90284bd` page); author controls; 3 generator mutants; `--selftest` 61/61 | R753-4 | `79fdea05ef54e2c99a0aa6efeadaa0f509076e92` |
| Docs | UNCLEAN (F1) | `REGISTER_MAP.md` delta, `register_descriptions.json` delta, PR body and REVIEW READY text, `--check`, memory-map `--check`, `git diff --check` | R753-4 | `79fdea05ef54e2c99a0aa6efeadaa0f509076e92` |

## Real limits

- **Block-level only:** the sweep and my probe elaborate `milan_csr` alone. On the shipping datapath the SRP grant and the steal input are tied 0, so F1 has no shipping-SoC read. The probe's engine timing follows the block's port contract (`srp_cmd_was_wr_r` records the command one cycle before its grant). No real SRP engine is wired to this port in any build.
- **Not rerun here:** the full docs-workflow table (58 steps), TOC and anchor checks, the doc style and path gates, Verilator suites, Yosys, and any parent, PP, gPTP or builder bank. For the docs steps I rely on the author's receipts. I verified 6 of them by sha256 against the published `MANIFEST.json` (sha256 `c6a5a4b2...`, `receipts/author_evidence_hash_check.txt`): all match. I verified hashes, not a signature.
- **Hosted:** a snapshot at this head (`receipts/hosted_checks_snapshot.tsv`) shows `changes`, `docs-check-no-git` and `full-ci-gate` succeeded, `Physical gPTP` skipped, and most jobs queued or in progress. A skipped context is not execution. Hosted and act acceptance belong to the manager.
- **Hardware:** physical calibration NOT RUN. No hardware, and no field evidence.
- **Local packages:** the pinned `wavedrom` 2.0.3.post3 is in a disposable environment under `scratch/`. Verilator is the scoped 5.050 (`receipts/clone_state.txt`).
- **Clone state:** the clone is at the exact head. The index equals tree `0a92dabe`, the work tree equals the index, nothing is untracked or ignored, and the six gitlinks equal HEAD (`receipts/clone_state.txt`). The probes ran in copies or wrote only under the packet.

## Pending manager duties

- Re-review the F1 fix at its new head.
- Hosted and act acceptance at the exact head.
- Build the current-dev merge candidate at the merge turn (source base `1e80128f`, live dev `503bc97cd4f24ad07596c17e7188f2024617972d`).
- Carry the residue checklist: R753-3 RES2 and RES3, R754-3 R1.

R753-4 FINISHED
