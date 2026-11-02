[R753] NEGATIVE - exact head e90284bd0896067eba6f10b3e5b0e534c9b0e017

Round R753-3, internal cleared-context review of kebag-logic/milan-fpga PR #825 (#797 lane R1), tree `ba8551a2254c49763c632a5f695d87922a2b0706`, delta `96bfa851..e90284bd`. Live dev `1f29f189` is merged, with one merge base. The delta moves no RTL, firmware, SoC or submodule file.

**Why NEGATIVE:** one open MINOR, F1. The round fixed the `STRM_SEL[9]` row, but the `STRMW_SRP` field row and two `STRMW_SRP` read-table rows still call the bit "the listener row" with no direction. At `SEL` `0x300` they print `LWSRP_STATUS`, and the simulated read returns 0. Everything else the round was asked to judge holds.

My verdict and ledger were recorded before I read any prior report (`receipts/own_verdict_before_prior_findings.md`). This report adds the prior-finding resolutions, and they changed neither.

## Findings

### F1 - MINOR - Conformance, Docs, Tests - `STRMW_SRP` still says `STRM_SEL[9]` selects "the listener row", so its rows are false as printed on the talker side

- **Where:**
  - `docs/reference/REGISTER_MAP.md:3634`, from `scripts/register_descriptions.json:3406`
  - `docs/reference/REGISTER_MAP.md:3638-3639`, from the wording of `srp_idx0_ls_w` at `scripts/register_descriptions.json:4093`
- **Authority:** #797 acceptance: no current document contains a statement the code contradicts. Round-3 focus (2): rows are true as printed. R754-2 F5.
- **Evidence:**
  - `hdl/common/csr/milan_csr.sv:2528` has no direction term in `srp_idx0_ls_w`, and `:2574-2576` uses it for this read.
  - `REGISTER_MAP.md:3396`, new this round, says that with `[8]` at 1 and `[3:0]` at 0 the bit moves `STRMW_SRP` "to the talker row". So at `SEL` `0x300` bit 9 does not select the listener row.
  - Line 3634 then says: index 0, unless bit 9 selects the listener row, is the live `LWSRP_STATUS` word. Line 3638 says the same as a read row, with "`STRM_SEL[9]` does not select the listener row at index 0".
  - The read at `0x85C` is 0 with `i_lwsrp_status` at `0x33333333`, on both builds (`receipts/sweep/ship_directed.txt`, `x2_directed.txt`).
  - Counted with that clause read as line 3396 defines it: 48 disagreements on the shipping build, all at `SEL` `0x300` (`receipts/sweep/ship_reader.txt`). With the clause read as the flop: 0 (`ship_flag.txt`).
- **Why Tests:** the published row-truth evidence, `read_table_compare.py`, maps this clause to the flop in its `CLAUSE` table. So "each row read as printed" holds the generator's meaning, not the printed one. The selftest arm checks form only and cannot see this.
- **Why not RTL or Robustness:** the RTL is unchanged and matches the new `STRM_LSN0` row. The defect is the statement.
- **Why not RESIDUE:** it predicts a different read value in a reachable state.
- **Impact:** a talker-side read with bit 9 left set is the exact case R754-2 F5 named. A programmer using this table expects `LWSRP_STATUS` and gets 0.
- **Required outcome:** the three rows state the condition by the bit's value. This wording works, and it is true on the shipping build, where `SRP_LSN0_ROW_P` is 2:
  - `condition_words.srp_idx0_ls_w`: `["`STRM_SEL[9]` is 1", "`STRM_SEL[9]` is 0"]`
  - `STRMW_SRP` field text: "Index 0 with `STRM_SEL[9]` at 0: the live `LWSRP_STATUS` word. Other rows are the attribute-row port, which is never granted, so they read 0."
- **Verification:** `--check` fresh after `--write`. Rerun `scripts/compare_sweep.py`, with the new clause in its table, on a log from `scripts/build_and_run.sh`: 0 disagreements at `SEL` `0x300` on the shipping build.

## Focus results

### (1) Page statements against the cited lines

| Statement | Page | Checked against | Result |
|---|---|---|---|
| `MAC_STATUS` published on each path reaching `nvm_boot()`; nothing writes it after an identity mismatch | `:516`, `:518`; notes `:164`, `:198` | `milan_baremetal.c:950-953`, `:1099-1102`, `:1671`. The only exits of `nvm_boot()` install the idle hook first (`:1676`, `:1812`). `milan_init` returns at `:1901-1902`, before `nvm_boot()`. The only writes are `:1064`, `:1073`, `:1080`, inside `phy_link_tick`. The shipping export has the MDIO CSR, so the `#ifdef` arm is live | Matches |
| `PP_NVM_STAT[6:0]` strobes, `[1:0]` read 0, identity in `[31:16]` | `:4458`, `:4473-4479` | `KL_nvm_backend.sv:455-462`, and `:593-599` by bit count. `CAP_ID_W_P` defaults to 16 and the datapath does not override it. `:638`, `:682` for the heartbeat | Matches |
| `ADP_CMD` strobes self-clear, read 0, reach no logic | `:1412-1413` | `milan_csr.sv:1654`, `:1799-1802`; `milan_datapath.sv:2780-2781`. Simulated: reads 0 after a write, strobe high one cycle per write | Matches |
| `STRM_SEL[9]` | `:3396`; notes `:974` | `milan_csr.sv:2528`, `:2574-2576`, `:3087-3090`, read bit at `:2535`. Simulated `SEL` `0x100` reads the alias, `0x300` reads 0, a read returns bit 9 as 0. On the shipping build the talker row is row 0, the legacy talker-0 row (`milan_datapath.sv:1888`) | This row matches. Its neighbours do not: F1 |
| Entity enable bits | `:96`, `:1168`, `:1191`, `:4344`; notes `:86`, `:348`, `:1229` | `protocol_processor_top.sv:2027`, `:2922`; `milan_datapath.sv:9586`; `KL_aecp_nvm_writer.sv:857`, `:874-877` (COMPLETE and DEFAULTS set done, the closed arm sets closed); `milan_baremetal.c:1846-1849` | Matches |
| REBOOT hold on `milan_mac_phy_crg_reset` | `:561`, `:4503` | `milan_soc.py:2115-2132`, `:2163`; `KL_reboot_ctrl.sv:271`, `:293`, `:320` (only reset clears the level); `REBOOT_RESET.md:163-164`. CPU-write precedence read from the local LiteX `CSRStorage` source, where the write arm is in the submodule and so follows the parent's statement. Not elaborated | Matches; wording in RES2 |
| `CHMAP_LOOP[31:28]` and `[26]` | `:4258`, `:4260` | `milan_csr.sv:1295-1311`; `0xDEADDEAD` has `[31:28]` = `Dh` and `[26]` = 1 | Matches |

### (2) Read-table sweep

My own harness (`scripts/gen_sweep.py`) and my own parse of the page (`scripts/compare_sweep.py`) cover all 17 tables.

- **State swept:** `[9]`, `[8]`, index 0, 1, 2, 3, 15, ACMP answered, SRP answered, snapshot running, channel-map readback, and three counter kinds. That is 960 states and 24,960 reads per build, with 0 reads dropped for moved state.
- **How state is set:** ACMP and SRP state comes from the real grant ports. A snapshot comes from a real start. On a selection whose snapshot ends at once, I deposit the busy flop, so talker index 0 is also read with a snapshot running. Kinds, shadow words and the readback flag are deposited.

| Page | Shipping 1x1 | 2x2 |
|---|---|---|
| Head, clause read as the flop | 0 disagreements | 96, all `RENDER_STAT` at listener index 1 |
| Head, clause read as line 3396 defines it | 48, all `STRMW_SRP` at `SEL` `0x300` (F1) | 144: those 48 and the 96 above |
| `96bfa851` page, control | 4,656 | 4,608 |

- **Rows with no hits:** the 2x2 build hits every row. On the shipping build, 6 rows have 0 hits, all above index 0, which that build does not have. They are vacuously true, and the handoff says so.
- **The form rule holds:** no `When` cell has `or`, a repeated term or a contradiction.
- **What the five tables were left out of:** the author's simulation sweep only. `STRMW_STATE`, `STRMW_CNTn`, `STRMW_PDUS`, `RENDER_STAT` and `CHMAP_LOOP` are absent from `words[]` in `gen_read_table_sim.py`, and `read_table_compare.py` prints them as "not swept". The selftest's form check does read them.
- **The five under my sweep:** all five are clean on the shipping build, and four are clean on 2x2. `RENDER_STAT` is the exception, see S1. "No `or`" also does not describe it: its row on the previous page held one (RES1).

### (3) Refusals and arm, undone

Each plant ran in its own scratch copy, regenerated so freshness cannot mask it (`receipts/mutants/mutants.tsv`). The baseline copy gives `--check` rc 0 and `--selftest` 61/61.

| Plant | Result |
|---|---|
| U1: reserved refusal off | `--selftest` rc 1, its control fails (rc 1, want 2) |
| D1: reserved `[1:0]` row back in the data | `--check` rc 2, "leaves the block" |
| U2: table refusal off | `--selftest` rc 1, its control fails (rc 1, want 2) |
| D2: table note in the data | `--check` rc 2, "holds a Markdown table" |
| U3: exact undo of `read_value_table` to `96bfa851` | `--selftest` rc 1, the arm fails |
| U4: no merge; U5: negated spellings apart; U7: exclusive compare off | `--selftest` rc 1, the arm fails |
| U6: view priority reversed | Survives, and is equivalent: the page is byte-identical, because `flatten` gives mutually exclusive paths |
| X1, X2, X3: "any other case" row dropped, its value wrong, later terms dropped | Survive: see S2 |

All three things the round was asked to prove fail when undone. The author's published mutant receipts agree on the shared plants.

## Residue

- **RES1:** the PR body and handoff say "Five tables with no `or` in them were outside the sweep". `RENDER_STAT`'s row on the previous page held an `or`. Exact fix: "Five tables were outside the sweep: `STRMW_STATE`, `STRMW_CNTn`, `STRMW_PDUS`, `RENDER_STAT` and `CHMAP_LOOP`."
- **RES2:** `REGISTER_MAP.md:4503` says "a CPU write in the same cycle clears it". A write of 1 does not clear it, and `milan_soc.py:2123` says "can clear". Exact fix: "a CPU write of 0 in the same cycle clears it for that cycle only".
- **RES3:** `CSR_REGISTER_NOTES.md:974` opens with "1 = the window serves sink 0's dedicated lwSRP row", unconditional, and then limits it. Exact fix: delete that clause and put "(`SRP_LSN0_ROW_C = L+T-1`)" after "sink 0's dedicated row".

## Suggestions

- **S1:** `RENDER_STAT`'s table is true only at `N_LISTENERS_P` = 1. The generator folds the loop at `milan_csr.sv:2447`, so on a 2x2 build listener index 1 reads the render word while the table says 0 (`receipts/sweep/x2_flag.txt`). I do not count this as a wrong statement, because the page states the shipping parameters and the module note at `:3942` is correct. Printing "`STRM_SEL[3:0]` is below `N_LISTENERS_P`" would make the table hold on every shape. The 2x2 talker row has the same shape limit: `srp_sel_row_w` gives row `L-1`, which is listener `L-1`'s row there.
- **S2:** the arm checks the form of rows, not their values. X1 to X3 regenerate a page with a missing or wrong row and still print 61/61. Only `READ_SHAPES` tests values, through `read_rows`, and `read_value_table`'s row assembly has no check. A small expected-rows control on one real register would kill all three.
- **S3:** `read_rows` has a third new refusal, more than 12 conditions. It fires (`receipts/probes/refusal_reach.txt`), but no control holds it.
- **S4:** `note_prose` guards notes only. A table in `page.intro` passes `--write` with rc 0 (`refusal_reach.txt`). `mechanism_blocks` and `register_section` print their text without the guard in the same way. R754-2 R5 asked only about notes, so this is outside what was asked.

## Prior findings at this head

| Finding | Status | Evidence |
|---|---|---|
| R753-2 F1, R754-2 F1 `MAC_STATUS` | Resolved | Table (1); both notes lines changed |
| R753-2 F2, R754-2 F6 entity enable | Resolved | Table (1); page and all three notes lines changed |
| R753-2 F3, R754-2 F7 REBOOT hold | Resolved | Table (1); row links `REBOOT_RESET.md`; RES2 is wording |
| R753-2 F4, R754-2 F4 read-condition grouping | Resolved at its cause | Sweep (2), selftest arm, U3. The remaining false rows come from a clause's wording, not from grouping, and are F1 |
| R753-2 F5, R754-2 F3 `ADP_CMD` | Resolved | The required text, simulated |
| R754-2 F2 `PP_NVM_STAT[1:0]` | Resolved | Table (1); each strobe in its own row; SVG and JSON regenerated; U1, D1 |
| R754-2 F5 `STRM_SEL[9]` | Resolved for the notes and the `STRM_LSN0` row. Its consequence for `STRMW_SRP` is retained as F1 | Table (1), F1 |
| R753-2 R1 to R3, R754-2 R1 to R5 | Resolved | Five stops at the named lines; `MAC_STATUS` rows; `CHMAP_LOOP` rows; line 68; note refusal (U2, D2) |
| R753-2 S1 to S3, R754-2 S1 to S5 | Not taken, optional | PR body says so. They do not affect coverage |
| Round-1 findings | Keep their round-2 closure | `scripts/register_sv.py`, `register_decode.py`, `register_fields.py` and `register_rtl.py` are outside the delta; `--check` and 61/61 reproduced |

Neither prior round raised F1, and my own R753-2 closed its round-1 `STRMW_SRP` finding on that row. The contradiction became plain only once line 3396 stated the talker case.

## Lens results

```text
[R753] PASS RTL - hdl/common/csr/milan_csr.sv:1654,1799-1802,2528,2574-2576,3087-3090; hdl/milan/KL_nvm_backend.sv:455-462,593-599; KL_reboot_ctrl.sv:271-320; protocol_processor_top.sv:2027,2922 - no RTL in the delta (git diff 1f29f189 HEAD has no hdl path, gitlinks unchanged); each cited line read and the module simulated on two builds; the contracts stand
[R753] PASS Robustness - scripts/register_page.py read_rows, impossible, note_prose, field_text; receipts/sweep/*_state_coverage.txt, receipts/mutants/mutants.tsv, receipts/probes/refusal_reach.txt - out-of-range index, snapshot during every selection, each freshness state, both refusals on undo and on data, the 13-condition refusal; S3 and S4 are optional
[R753] UNCLEAN Conformance - F1; every other statement in table (1) matches its cited line
[R753] UNCLEAN Tests - F1 on the row-truth evidence; the arm and both refusal controls each fail when undone (U1 to U5, U7, D1, D2)
[R753] UNCLEAN Docs - F1; docs_check 0 findings, check_doc_style rc 0, check_doc_paths rc 0, memory-map --check rc 0, git diff --check rc 0; no bench label, round, reviewer ID or comment ID in a new source comment
```

## Completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Page rows and notes in table (1), against the cited RTL, firmware and SoC lines | R753-3 | `e90284bd0896067eba6f10b3e5b0e534c9b0e017` |
| RTL | CLEAN | `milan_csr.sv`, `KL_nvm_backend.sv`, `KL_reboot_ctrl.sv`, `protocol_processor_top.sv`, `milan_datapath.sv`; two simulated builds; no RTL in the delta | R753-3 | `e90284bd0896067eba6f10b3e5b0e534c9b0e017` |
| Robustness | CLEAN | `register_page.py` new paths, refusal plants, sweep state coverage | R753-3 | `e90284bd0896067eba6f10b3e5b0e534c9b0e017` |
| Tests | UNCLEAN (F1) | `register_selftest.py`, 12 plants, author's sweep tools and receipts | R753-3 | `e90284bd0896067eba6f10b3e5b0e534c9b0e017` |
| Docs | UNCLEAN (F1) | `REGISTER_MAP.md`, `CSR_REGISTER_NOTES.md`, generated `pp` diagrams, PR body, doc gates | R753-3 | `e90284bd0896067eba6f10b3e5b0e534c9b0e017` |

## Real limits

- **Simulation scope:** the sweep is `milan_csr` alone, with inputs at constants and no engines. On the shipping datapath `srp_ctx_gnt_w` is tied 0 (`milan_datapath.sv:8720`), so states with the SRP table answered exist only in this harness.
- **Weak oracle:** the `CHMAP_LOOP` "fields above" check tests `[26]` set and `[31:28]` clear, not each field.
- **Read, not run:** the firmware, SoC and processor statements. The LiteX precedence was read, not elaborated. Physical calibration NOT RUN, and no hardware.
- **Gates not rerun:** `gen_toc.py --check`, `--verify-anchors` and `check_em_dash.py` exit 2 here because the pinned Markdown renderer is not installed (`receipts/gates/`). I rely on the author's published receipts for them.
- **Evidence provenance:** the evidence commit `ffb9c2b6` is unsigned by GitHub's verdict, so I checked hashes instead: 13 author files I fetched match `MANIFEST.json`, 0 mismatched. I spot-checked and did not rerun the author's whole gate table.
- **Local package:** the pinned `wavedrom` went into a disposable environment under `scratch/`.
- **Clone state:** the clone is at exact head. Index equals tree `ba8551a2`, the work tree equals the index, and the gitlinks are in `receipts/probes/gitlinks.txt`. No probe edited it.

## Pending manager duties

Hosted and act acceptance; the current-dev candidate banks at the merge turn against live dev `1f29f189`; the residue checklist (RES1 to RES3); and a re-review of the F1 fix. The lane conflict with PR #815 stands as the PR states.

R753-3 FINISHED
