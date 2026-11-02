# [A711c] R1 register reference (#797): handoff, round 3

Status: REVIEW READY at the head below. Every docs-workflow step that can run here is rc 0 on a clean clone of the head. Local branch; the manager pushes.

- Branch `797-r1-regref`. Head `e90284bd0896067eba6f10b3e5b0e534c9b0e017`, tree `ba8551a2254c49763c632a5f695d87922a2b0706` (`receipts/gates/HEAD.txt`).
- Base: dev `1f29f189279f9fc0132f4918e47342b87d22f33a`, still the dev tip when this was written, one merge base. Nothing was merged or rebased this round.
- Origin verified: `https://github.com/kebag-logic/milan-fpga.git`. Round 1 branched from dev `1e80128f`, which is an ancestor of the head.
- Submodules at their pins, unchanged. `protocol-processor` was verified as its own top level and its origin as the processor repository before any read.
- Receipts: `receipts/INDEX.md`, generated from the files present, with host paths replaced. Tools: `tools/`.
- Round 2's handoff, `../797-a711b/HANDOFF.md`, still describes everything this round did not touch.

## Assignment as read

Round 3, statement fixes only. Both reviews of `96bfa851` were NEGATIVE with MINOR findings on what the page states: R753-2 and R754-2 on PR #825. Fix every finding and residue, with file:line and a verification line. Move no more text to other pages, add no new gate, add no new diagram, and do not search beyond the reviewers' findings. No RTL changed.

TAKEN: issuecomment-6566866800 (`taken_posted.md`). REVIEW READY: issuecomment-6567675725 (`review_ready_posted.md`).

## Round 3: commits

Each is one finding group, one subject line, no body, no trailer. The page and diagrams are regenerated in each commit, so `--check` is fresh at every commit.

| Commit | Subject | Findings |
|---|---|---|
| `5887ae88` | Print each read-table row as one conjunction true as printed, drop rows no state reaches, and hold it with a selftest arm | R753 F4, R754 F4 |
| `2d1771f5` | State that firmware publishes MAC_STATUS on every boot path reaching nvm_boot(), not only while the writer runs | R753 F1, R754 F1 |
| `89b0ecdd` | State that either enable bit requests the entity enable, and that the fabric holds it until the restore releases it | R753 F2, R754 F6 |
| `361833a9` | State the AECP REBOOT's hold on milan_mac_phy_crg_reset in its row and in PHY_RESET's | R753 F3, R754 F7 |
| `72f8e1ce` | State that the inert ADP_CMD strobes self-clear and read 0 | R753 F5, R754 F3 |
| `b2df755e` | Name each PP_NVM_STAT strobe in the row of its own bit, and refuse reserved bits on a word whose write leaves the block | R754 F2 |
| `763e7055` | State that STRM_SEL[9] also moves STRMW_SRP off the LWSRP_STATUS alias on the talker side at index 0 | R754 F5 |
| `9a1d1547` | End carried fragments with a stop, reword the MAC_STATUS rows, state what the CHMAP_LOOP poison sets, and drop the RW store claim | R753 R1 to R3, R754 R1 to R4 |
| `e90284bd` | Refuse a description note that holds a Markdown table, with a control | R754 R5 |

## Round 3: findings, each with its fix and its check

Line numbers are at the head. `P` is `docs/reference/REGISTER_MAP.md`, `J` is `scripts/register_descriptions.json`, `N` is `docs/design/CSR_REGISTER_NOTES.md`, and `G` is `scripts/register_page.py`.

### Read conditions lose their grouping: R753 F4, R754 F4

- **Cause:** `Wording.condition` joined nested `&&` and `||` with no grouping, and each table row joined that to the rest of its path.
- **Fix:** `G:230` `read_rows` turns a table's conditions into variables, walks every assignment and gives each read value its shortest conjunctions (`G:208`). A term and its negation are one variable (`G:167`). One signal cannot equal two values at once (`G:197`). `G:772` prints one conjunction per row, and the constant taking the most rows becomes "any other case" (`G:784`). A row no state reaches is dropped: `STRMW_DMAC_LO` listed `i_lctx_rd_data` under a condition that could never hold.
- **Selftest arm:** `scripts/register_selftest.py:303` `read_table_control`. Two read decodes must give exactly their listed rows, and every When cell of a regenerated page must have no `or`, repeated term or contradiction.
- **The page at this head:** 17 tables, 52 rows, 0 with `or`. At `96bfa851` the same tables had 71 rows, 24 with `or`. The `STRMW_CTRL` table (`P:3437`) now reads as R753 F4 asked.
- **Verification, simulation:** `sim/read_table_compare_2x2.txt` and `sim/read_table_compare_ship.txt`. `tools/gen_read_table_sim.py` sweeps selection, snapshot and table-answered state over `milan_csr` with distinct constants on each input. `tools/read_table_compare.py` reads each printed row as written, with `and` binding tighter than `or`. Both logs: 1,152 reads, 0 disagreements. The 2x2 build hits every row of the 12 swept tables; the shipping 1x1 build does not reach 6 of them, each a row above index 0, which that build does not have.
- **Verification, the probe can fail:** the same compare on the page at `96bfa851` exits 1 with 360 disagreements (`sim/read_table_compare_old_page_control.txt`).
- **Verification, the arm can fail:** `mutants/read_table_mutants.tsv`. `no_grouping`, `no_merge`, `polarity_inverted` and `exclusive_compare_off` each regenerate the page and then fail `--selftest`, naming this arm.
- **Not in that sweep:** `STRMW_STATE`, `STRMW_CNTn`, `STRMW_PDUS`, `RENDER_STAT` and `CHMAP_LOOP` (five tables, eleven rows; the compare's "not swept" lines). Their rows carry no `or` either. Both reviewers' harnesses, rerun below, read those words at the reset selection and in their directed cases, not at every row.

### `MAC_STATUS` publication: R753 F1, R754 F1

- **Fix:** `J:1268` and `P:516`, `P:518`: firmware publishes on each boot path reaching `nvm_boot()`, and after a CSR identity mismatch nothing writes it. `N:164` and `N:198` say the same.
- **Verification:** read against `milan_baremetal.c:950-953`, `:1092-1094`, `:1099-1102`, `:1671`, `:1676` (`statements/mac_status_sources.txt`). `--check` fresh in `gates/docs-gates-0__gate_50.log`.

### Entity enable is a request: R753 F2, R754 F6

- **Fix:** `P:96` carries the exact wording R753 and R754 gave (`J:20`). `P:1168` (`J:296`). `P:1191` (`J:1690`) and `P:4344` (`J:3866`) name the release at COMPLETE or DEFAULTS and the CLOSED case. The two module purposes read "Entity enable request". `N:86`, `N:348`, `N:1229` follow.
- **Verification:** read against `protocol_processor_top.sv:2027`, `milan_datapath.sv:9586`, `milan_baremetal.c:1846-1849` (`statements/entity_enable_sources.txt`). `check_doc_style.py` rc 0 in `gates/docs-gates-0__gate_9.log`.

### REBOOT hold: R753 F3, R754 F7

- **Fix:** `P:4503` (`J:1059`) states that an AECP REBOOT sets the storage and holds it, that the hold only rises, and that a CPU write in the same cycle clears it for that cycle only. It links `docs/design/REBOOT_RESET.md`. `P:561` (`J:1298`) adds that a REBOOT also sets that storage.
- **Verification:** read against `milan_soc.py:2115-2123`, `:2132`, `REBOOT_RESET.md:163-164` (`statements/reboot_hold_sources.txt`). `docs_check.py` reports 0 findings, link health included, in `gates/docs-gates-0__gate_7.log`.

### `ADP_CMD`: R753 F5, R754 F3

- **Fix:** `P:1412`, `P:1413` (`J:1869`, `J:1870`), the exact text both reports gave.
- **Verification:** `statements/adp_cmd_sources.txt`: `milan_csr.sv:1799-1802`, `milan_datapath.sv:2780-2781`, and the oracle line for 0x640 reading `w1=00000000 w0=00000000`.

### `PP_NVM_STAT` strobes: R754 F2

- **Fix:** `J:4052`, `J:4057` replace the reserved `[1:0]` with `COMMIT_ACK` and `HEARTBEAT` (`P:4478`, `P:4479`). `[6:2]` each name their strobe in their own row (`P:4473` to `P:4477`). `P:4458` points at them. `docs/diagrams/regmap/pp/PP_NVM_STAT.svg` is regenerated.
- **Control:** `G:348` refuses a reserved writable field on a word whose write leaves the block. Selftest control "reserved bits on a word whose write leaves the block".
- **Verification:** `statements/pp_nvm_stat_sources.txt`: `milan_csr.sv:2200-2204`, `:2282`, `KL_nvm_backend.sv:455-461`, `:462` (the identity in `[31:16]`), `:593-599`, `milan_baremetal.c:1112`, `:1457`. `sim/r754_compare_page.txt` shows the same `RW-NOT-STORED` measurement under the new names. Mutant `reserved_on_strobe_word` fails `--selftest`.

### `STRM_SEL[9]`: R754 F5

- **Fix:** `N:974` carries R754's exact sentences. `P:3396` (`J:3293`) states the same in its own words.
- **Verification:** `statements/strm_sel_sources.txt`: `milan_csr.sv:2528`, `:2574-2576`, `:3086-3090`; `sim/r754_sim_directed.txt` reads `0xFFFFFFFF` at `SEL` `0x100` and `0x00000000` at `SEL` `0x300`. The sweep's `STRMW_SRP` rows agree.

### Residue

| Item | Fix | Verification |
|---|---|---|
| R753 R1, R754 R1 | Stops at `J:1306`, `:1578`, `:1579`, `:2617`, `:3910`; `P:625`, `:994`, `:995`, `:2360`, `:4403` | Read at those lines |
| R753 R2, R754 R2 | Exact text at `J:1260` to `:1262`; `P:506` to `:508` | Read at those lines |
| R753 R3, R754 R3 | Exact text at `J:3840`, `J:3842`; `P:4258`, `P:4260` | `statements/chmap_loop_sources.txt`, `milan_csr.sv:1307-1309` |
| R754 R4 | Exact text at `J:6`; `P:68` | Read at that line |
| R754 R5 | `G:584` `note_prose` refuses a table delimiter row in any note's prose | Selftest control "prose wrapped in a Markdown table inside a note"; mutant `table_in_note` fails `--selftest` |

### Suggestions not taken

S1 to S3 of both reports and S4, S5 of R754 are optional by their severity, and the assignment asks for findings and residue. S1 and S2 would also change diagrams this round may not add to. They remain open for the area lanes.

## Findings count per area

| Area | R753-2 | R754-2 | Distinct | Fixed |
|---|---|---|---:|---:|
| Read conditions (generator) | 1 (F4) | 1 (F4) | 1 | 1 |
| Statements about the merged tree | 3 (F1 to F3) | 3 (F1, F6, F7) | 3 | 3 |
| Rows false against the RTL | 1 (F5) | 3 (F2, F3, F5) | 3 | 3 |
| Residue | 3 | 5 | 5 | 5 |
| Suggestions | 3 | 5 | 5 | 0 taken |

## Generator and freshness gate

Unchanged in shape; round 2's section stands. Step "Register reference freshness gate" of `.github/workflows/docs.yml`, `id: gate_50`.

- **Planted stale-page mutants:** the selftest now has 61 controls through the workflow's own `--check` entry (`gates/docs-gates-0__gate_50.log`). A flop change with a matching ROM change exits 1 naming the page. A field rename exits 2 while its description names the old field. New this round: reserved bits on a strobe word, a Markdown table in a note, and the read-table arm.
- **No new gate.** The new refusals and controls live inside the existing generator and its selftest.
- **Generator mutants:** `mutants/read_table_mutants.tsv`, 6 mutants, 0 survivors. Each regenerates the page first, so freshness cannot be what kills it.
- **Both reviewers' plants, rerun at this head:** `plants/r753_plant_probes.txt` 45 plants, 0 misses. `plants/r754_mutants.tsv` 39 rows: rc 2 on 24, rc 1 on 14, rc 0 on the comment-only control.

## The simulations, rerun

- `sim/r753_oracle_compare.txt`: 203 registers, 499 fields, 0 undocumented addresses with a nonzero observation. Against round 2 the only change is `[1:0] RESERVED` becoming `[1:1] COMMIT_ACK` and `[0:0] HEARTBEAT`, one more row of the same class.
- `sim/r754_compare_page.txt`: 203 registers, 257 words, 8,224 bit checks. Against round 2 the same two rows are renamed, and nothing else differs.
- `export/soc_from_check.txt`: `--check --soc-from` against round 2's export, rc 0. The SoC extract did not change this round.
- `behave/counters_contract_milan.txt`, rc 0, and `plants/r753_row_audit.txt`, `plants/r753_note_as_paragraph.txt`, `plants/memory_map_plants.txt`, each rc 0.

## Dropped statements

`receipts/survival.txt`: 1,610 fragments, 1,546 present verbatim, 64 missing. Round 2 listed 56, and its table in `../797-a711b/HANDOFF.md` covers them. The 8 new ones are the sentences this round corrected, on the evidence above:

| Fragment | Why |
|---|---|
| Six entity-enable sentences on the old page ("either bit enables the entity", "either bit starts the plane", and the like) | Contradicted: `protocol_processor_top.sv:2027`. Rewritten as a request |
| "There is exactly one control plane now ... for either bit to start." | Reworded: "to request" |
| `speed (0=10,1=100,2=1000)` | R2's exact rewording |

## Open risks and decisions

1. **ETH_GUARD.** The page states the code. The gating and the RTL comments stay open and out of this PR.
2. **The design notes hold about 31,000 words of carried prose,** sampled by both reviewers. This round fixed only the sentences they named.
3. **Mermaid is parsed, not rendered,** by both reviewers. A reader should open the PR's rendered page once.
4. **The read-table sweep is `milan_csr` alone,** with inputs held at constants and no engines. The five unswept tables have no `or` to misread.
5. **`shortest_terms` may print overlapping rows for one value:** `STRMW_SRP` has two rows returning `{16'd0, i_srp_ctx_rd_stat}`, and both can hold at once. Each is true as printed and they return the same value, so the compare accepts it.
6. **The statements about firmware, the SoC and the processor were read, not simulated.** `statements/` holds the cited lines.
7. **Lane conflict with PR #815** stands: both add a docs-check step, and D0's inventory must list the design notes.

## Gate table

Method as round 2: each step of the head's `.github/workflows/docs.yml` ran as its job runs it, read from the workflow by `../797-a711b/tools/run_docs_workflow.py`, one `bash -e` script per step, output to a file, never piped. The clone is a fresh one of the head with the four submodules the jobs fetch, each at its pin. Logs and rc files: `receipts/gates/`.

| Job | Step id | Name | rc | Last line |
|---|---|---|---:|---|
| wire-accountability | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| wire-accountability | ci_step_3 | Fetch the engine authority the builder derives from | 0 |  |
| wire-accountability | ci_step_4 | Advertised-vs-emitted gate (green since 2026-07-28, item 0 | 0 | RESULT: PASS |
| docs-check-no-git | ci_step_2 | Set CPU-derived job budgets | 0 |  |
| docs-check-no-git | ci_step_3 | Strip git metadata, then run the docs gate | 0 | feature_status: 0 finding(s) |
| docs-gates-0 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| docs-gates-0 | gate_1 | Build the validated HDL reference | 0 | Wrote: <runner-temp>/milan-hdl-reference/index. |
| docs-gates-0 | gate_7 | Link health, wording, dead-reference and local-info gate | 0 | docs_check: 0 finding(s) across 213 md files + 1687 scrubbed text files, scrub self-test 2 |
| docs-gates-0 | gate_8 | Added-line em-dash gate | 0 | check_em_dash: 0 finding(s) over 5769 added line(s) in 7 changed Markdown page(s), 0 mirro |
| docs-gates-0 | gate_9 | Concise audience documentation gate | 0 | gPTP documentation selftest: OK (30 controls) |
| docs-gates-0 | gate_10 | Audience diagram no-drift gate | 0 | time-sync diagram selftest: OK (source, status, XML, raster) |
| docs-gates-0 | gate_11 | Product solution source-fact gate | 0 | solution documentation selftest: OK (45 mutation controls) |
| docs-gates-0 | gate_12 | Verified submodule documentation gate | 0 | submodule documentation selftest: OK (table and diagram controls) |
| docs-gates-0 | gate_13 | HDL timing diagram no-drift gate | 0 | WaveDrom current: docs/diagrams/wd_gptp_pdelay.json |
| docs-gates-0 | gate_14 | Published diagram PNG gate | 0 | diagram PNG selftest: OK (6 rasters, 28 mutation controls) |
| docs-gates-0 | gate_15 | Milan feature-status consistency gate | 0 | feature_status: 0 finding(s) |
| docs-gates-0 | gate_16 | Traceability matrix no-drift gate | 0 | traceability matrix up to date (80 modules, 0 untested <= ratchet 0, 0 archived) |
| docs-gates-0 | ci_step_21 | Fetch the builder source dependencies | 0 |  |
| docs-gates-0 | gate_18 | Imported gPTP documentation gate | 0 | source evidence selftest: PASS (7 arms) |
| docs-gates-0 | gate_19 | Code-quality measurement self-tests | 0 | 18 checks: 18 PASS, 0 FAIL |
| docs-gates-0 | gate_21 | Bare-metal scope gate | 0 | baremetal-only selftest: PASS (867 arm(s)) |
| docs-gates-0 | ci_step_28 | Install and verify the pinned RV32 SDK | 0 | SDK cache hit: verified |
| docs-gates-0 | gate_24 | Compiler-absent firmware controls | 0 | GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations |
| docs-gates-0 | gate_26 | NVM record-space gate | 0 | 0 finding(s) across 5 config(s): the inventory's (group, index) key set is exactly the set |
| docs-gates-0 | gate_27 | Capture measurement census and clock gate | 0 | PASS: capture census, clocks, both timing arms and receipt agree |
| docs-gates-0 | gate_28 | Saved-state writer gate | 0 | saved-state writer gate: OK across 5 shape(s), and every planted defect reddened |
| docs-gates-0 | gate_29 | SoC source-list gate (Vivado would fail 40 min in without  | 0 | iob_pack_selftest: 22 arms, 21 mutants, 0 failure(s) |
| docs-gates-0 | gate_30 | RTL source-list drift gate | 0 | 50 checks: 50 PASS, 0 FAIL |
| docs-gates-0 | gate_31 | Boundary-unit naming ratchet | 0 | 66 checks: 66 PASS, 0 FAIL |
| docs-gates-0 | gate_32 | Port contract gate | 0 | 82 checks: 82 PASS, 0 FAIL |
| docs-gates-0 | gate_33 | Fail-fast ratchet | 0 | 106 checks: 106 PASS, 0 FAIL |
| docs-gates-0 | gate_34 | TODO ownership gate | 0 | 45 checks: 45 PASS, 0 FAIL |
| docs-gates-0 | gate_35 | Test-evidence ratchet | 0 | 105 checks: 105 PASS, 0 FAIL |
| docs-gates-0 | gate_36 | Mechanical hygiene ratchet | 0 | 35 checks: 35 PASS, 0 FAIL |
| docs-gates-0 | gate_37 | SystemVerilog idiom gate | 0 | 55 checks: 55 PASS, 0 FAIL |
| docs-gates-0 | gate_38 | C and C++ idiom gate | 0 | 75 checks: 75 PASS, 0 FAIL |
| docs-gates-0 | gate_39 | Python idiom gate | 0 | 54 checks: 54 PASS, 0 FAIL |
| docs-gates-0 | gate_40 | Shell idiom gate | 0 | 48 checks: 48 PASS, 0 FAIL |
| docs-gates-0 | gate_43 | Doc cited-path gate | 0 | doc path gate: OK (1091 cited paths all resolve, 2 allowlisted; 10 line anchor(s) within t |
| docs-gates-0 | gate_44 | Archive integrity gate | 0 | archive selftest: OK (24 controls) |
| docs-gates-0 | gate_45 | Per-page contents gate | 0 | TOC gate: OK (151 page(s) carry an annotated contents list, 18 below the 3-section thresho |
| docs-gates-0 | gate_46 | AEM store generator self-test | 0 | gen_aem_store self-test: PASS |
| docs-gates-0 | gate_47 | Sweep/build shape gate | 0 |   [self-test] OK: 1 drift(s) reported |
| docs-gates-0 | gate_48 | Deploy shape gate | 0 |   [selftest] OK: 1 drift(s) reported |
| docs-gates-0 | gate_49 | Entity shape gate | 0 | RESULT: PASS |
| docs-gates-0 | gate_50 | Register reference freshness gate | 0 | memory map diagram: fresh |
| docs-gates-0 | ci_step_53 | Fetch inventory dependencies | 0 |  |
| docs-gates-0 | gate_51 | CI scheduling and evidence controls | 0 | manifest comparison controls: PASS |
| docs-gates-1 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| docs-gates-1 | ci_step_9 | Fetch the builder source dependencies | 0 |  |
| docs-gates-1 | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | SDK cache hit: verified |
| docs-gates-1 | gate_25_0 | End-station builder gates, leg 0 of 2 | 0 | ALL GATES PASS |
| docs-gates-2 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| docs-gates-2 | ci_step_9 | Fetch the builder source dependencies | 0 |  |
| docs-gates-2 | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | SDK cache hit: verified |
| docs-gates-2 | gate_25_1 | End-station builder gates, leg 1 of 2 | 0 | ALL GATES PASS EXCEPT 16 NOT RUN |
| docs-gates-2 | gate_41 | CI event and SHA contract gate | 0 | selftest: PASS (2207 contract items, 5271 arms) |
| docs-gates-2 | gate_42 | Local act runner contract gate | 0 | selftest: PASS |

58 steps ran, 0 not rc 0, 38 not run.

Not run: wire-accountability: Record actual job execution; docs-check-no-git: Retain checkout identity before removing metadata; docs-check-no-git: Record actual job execution; docs-gates-0: Install the python gate dependencies; docs-gates-0: Install the pinned Markdown renderer; docs-gates-0: Resolve exact package downloads 6; docs-gates-0: Install diagram gate dependencies; docs-gates-0: Install the pinned sv2v release; docs-gates-0: Record executed gate outcomes; docs-gates-0: Record actual job execution; docs-gates-1: Install the python gate dependencies; docs-gates-1: Install the pinned Markdown renderer; docs-gates-1: Resolve exact package downloads 4; docs-gates-1: Install diagram gate dependencies; docs-gates-1: Install the pinned sv2v release; docs-gates-1: Record executed gate outcomes; docs-gates-1: Record actual job execution; docs-gates-2: Install the python gate dependencies; docs-gates-2: Install the pinned Markdown renderer; docs-gates-2: Resolve exact package downloads 4; docs-gates-2: Install diagram gate dependencies; docs-gates-2: Install the pinned sv2v release; docs-gates-2: Record executed gate outcomes; docs-gates-2: Record actual job execution; docs-check: Set CPU-derived job budgets; docs-check: Install the pinned evidence reader; docs-check: Require every gate exactly once; docs-check: Record actual job execution; ci-manifest: Set CPU-derived job budgets; ci-manifest: Fetch inventory dependencies; ci-manifest: Install the pinned evidence reader; ci-manifest: Collect actual runtime evidence; ci-fail-fast: Set CPU-derived job budgets; ci-fail-fast: Observe the first failed job; ci-fail-fast: Cancel this run and sibling workflows; ci-fail-fast: Record actual job execution; ci-cancel-tail: Set CPU-derived job budgets; ci-cancel-tail: Cancel confirmed terminal failures.

Reasons for the steps not run, as round 2:

- **`Record ...`, `Retain checkout identity`:** GitHub run evidence only.
- **`Install ...`, `Resolve exact package downloads`:** apt, sudo or pip. The host and venv already hold these tools. The runner also drops the `python3 -m pip install` lines inside gate steps and leaves their other commands intact.
- **Jobs `docs-check`, `ci-manifest`, `ci-fail-fast`, `ci-cancel-tail`:** they verify uploaded CI receipts or cancel runs, so they run only on GitHub.

Builder leg 1 reports `ALL GATES PASS EXCEPT 16 NOT RUN` with rc 0 (`gates/docs-gates-2__gate_25_1.log`), as in round 2. `docs-gates-2__gate_41.log` is over the size limit: its digest, size and tail are in `gates/docs-gates-2__gate_41.log.tail`.

Also on this head:

| Check | rc | Receipt |
|---|---:|---|
| `git diff --check 1f29f189 HEAD` | 0 | `gates/lane__diff_check.rc` |
| `git merge-base --all origin/dev HEAD`: one base, `1f29f189` | 0 | `gates/lane__merge_base.txt` |
| `gen_register_reference.py --selftest`, standalone: 61/61 | 0 | `gates/lane__selftest.log` |
| `gen_register_reference.py --check`, standalone | 0 | `gates/lane__check.log` |
| Clone status after the run: 0 lines | 0 | `gates/lane__clone_status_after.txt` |
| `gen_register_reference.py --check --soc-from <export>` | 0 | `export/soc_from_check.txt` |
| `behave features/counters_contract_milan.feature` | 0 | `behave/counters_contract_milan.txt` |
| Read-table sweep, 2x2 and shipping builds | 0 | `sim/read_table_compare_*.rc` |
| The same compare on the page at `96bfa851`: the control, which must fail | 1 | `sim/read_table_compare_old_page_control.rc` |
| Generator mutants: 6 of 6 killed | 0 | `mutants/read_table_mutants.rc` |
| Both reviewers' simulations and plants, rerun | 0 | `sim/`, `plants/` |

Not run: the Verilator sweep, Yosys and the full behave suite (documentation lane, no RTL changed). No hardware, no Vivado.
