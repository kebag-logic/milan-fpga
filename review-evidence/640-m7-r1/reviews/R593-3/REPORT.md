[R593] POSITIVE - exact head 354f781828d8b4d73037129f297b072320a10f9c

# R593-3: external review of PR #713 (issue #640, Mark II lane M7, plan L10a), round 3

- Head `354f781828d8b4d73037129f297b072320a10f9c`, tree `27d0094ad4a11b5d2fe55091b6ae93d9f1f70237`. Source base: dev `e8454e2751d05b02ee8e5a571857589ab358ab86`, 20 parent commits. Round 3 adds `a8a1c117`, `a9eab29a`, `70c697bf` and `354f7818` on `2cc2ba0b`.
- Gitlinks at the head:
  - `gptp-processor` `18dd997b2459699e41e5ce9bceca1181e41fa5fe`. The donor diff `5dce647a..18dd997b` touches only `hdl/common/KL_gptp_timer.sv` and `docs/MANAGER.md`, and `18dd997b` is on the donor's published `origin/640-m7`.
  - `protocol-processor` `2ad2f845` and `third_party/verilog-axis` `48ff7a7e`. `external` and `third_party/lwSRP` are unchanged.
- All five lenses were applied: Conformance, RTL, Robustness, Tests and Docs. **All five are clean. No BLOCKER, MAJOR or MINOR is open.**
- Open, non-blocking items:
  - one RESIDUE, R593-3-R-01, a stale count in a Makefile comment;
  - one new SUGGESTION, R593-3-S-01;
  - two retained prior SUGGESTIONs, R592-2-S1 (optional) and R593-1-S-03 (pre-existing, routed to #495).
- The product RTL preserves behaviour as far as simulation can show. On the `gptp_shadow` stimulus (record faults, barriers, link-guard episodes, PHC loads, observer resets), the dev-base plane and the head plane produce byte-identical per-cycle change traces of every plane-visible output (3,612 change records; same sha256). `gptp_shadow`, `gptp_plane` and `gptp_txts` print identical output at the base and at the head.
- Every prior public finding that needed a change is resolved at this head. That includes R593-2-F1, the MINOR that made round 2 NEGATIVE.

## Reconstruction

Sources, read in this order:
1. `AGENTS.md`, `CONTRIBUTING.md` (by reference from AGENTS.md) and `docs/README.md`.
2. The issue #640 body: owner decision, NFR-RES-01 at 60 %, and the acceptance (routed image at most 38,040 LUT with timing met, function unchanged at the same counts, gate re-recorded in the change that reaches the target).
3. The issue's manager and author comments for this lane:
   - assignment 6097272538 and TAKEN 6097298086;
   - REVIEW READY round 1, 6100339945;
   - the round-2 assignment 6100980189 and the round-3 assignment 6104116064;
   - REVIEW READY round 3, 6104542951.
4. The decisions they cite: D1, D3, D7 and D8 (5990755268), and the firmware block-RAM decision (6081706413).
5. The PR #713 body.
6. The interface authorities: `third_party/verilog-axis/rtl/axis_fifo.v` (ADDR_WIDTH rule, user-field layout, bad-frame test, `MARK_WHEN_FULL` default), and the engine's result face and event word (`gptp-processor/hdl/top/KL_gptp_engine.sv:349-350,478-519`, `hdl/ucode/gen_gptp_ucode.py:360-376`).
7. Then `git diff e8454e27..354f7818` with its history, and the donor diff.
8. Public evidence: `3e0f36b8:review-evidence/640-m7-r1` (`MANIFEST.json`, `author/HANDOFF.md`, `author/PR-BODY.md`).

The prior public reviews on this PR (R593-1, R592-1, R593-2, R592-2) were read only after this round's own pass over the diff and its first probe wave.

**Frozen scope**, from assignment 6097272538 with rounds 2 and 3:
- Move eligible fabric gPTP plane tables into block RAM, or narrow their indices, measuring first. Keep the dual-read operand files; M10 is out of scope.
- Target about 500 LUT (300-700), reported honestly.
- Block RAM may grow only within the firmware ledger. A read-latency change needs deterministic bounds.
- No change to gPTP behaviour, its register map or its timestamp path.
- Proof required:
  - the named suites in both shapes;
  - per-table lockstep with planted wrong-depth, wrong-read-latency and index-alias defects, each failing a named check;
  - the integrated route and resource gate through the M0s recipe, with every endpoint passing and WNS at or above the floor with no exception;
  - no re-record before M9 (D7).
- Round 2: fill the result queue, with named coverage and a write-index control. Add the TX lane decode check for counts 0 to 8. State the tag limit and #714.
- Round 3: census every column of every converted table. Declare one-valued columns in one machine-readable list, and generate or check the README from it. A stuck undeclared column must fail. Drop the tautological decode check. Apply residues R593-2-R-01 and R592-2-RES1.

The PR says "Relates to #640", not "Closes". It does not claim the issue-level 38,040-LUT acceptance, which belongs to the whole redesign.

## Independent executions at this head

All runs used Verilator 5.050 (`receipts/verilator_identity.txt`): the pinned wrapper first on `PATH`, `VERILATOR_JOBS=2`.
- Suites ran in the review clone. Differentials and probes ran in disposable `git archive` exports of base and head under `scratch/`, with submodules exported at their gitlinks.
- The clone was restored and verified afterwards (`receipts/clone_integrity.txt`: INTEGRITY PASS).

| What | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/gptp_tables` (limits check, suite, `mutants.py`) | rc 0. Limits table current. **36/36 checks** over 32,100,038 cycles. rx 44,199 good / 33,354 overflow / 12,751 bad, all eight lanes, 256 beats deep. tx 10,530 frames, 27 beats deep. Decode `00 01 03 07 0f 1f 3f 7f ff`, 0 wrong. Ledger 3 deep, heads 0xff. Results 3 deep, heads 0xff, 110 written behind a waiting result. Timer slots 0x3f. Census: 11 columns; `tag`, `ok`, `gen` one-valued 0x1 and declared. **26/26 controls caught, each by its own named check** | `A_tables_all.log` |
| `make -C tb/verilator/gptp_shadow` | rc 0; 309/309, mutant lifecycle PASS, 9/9 controls | `B_shadow_all.log` |
| `make -C tb/verilator/gptp_txts`, with `MILAN_LITEX_PYTHON=true` | rc 0; 85/85, 6/6 controls. The stale-chain regeneration check was bypassed: no LiteX environment here, and the converted chain is not in the diff | `C_txts_all.log` |
| `make -C tb/verilator/gptp_plane` | rc 0; 29/29 | `E_plane.log` |
| `make -C gptp-processor contract tb lint`, then `docs` | All rc 0. The engine passes 1613/1613 in each seeded variant, and all 40 donor controls are caught. Parser, gaskets, tsngen and Arty bench pass. Donor lint and docs pass, with 20 exact source-evidence anchors | `D_gp_contract_tb_lint.log`, `I_gp_docs.log` |
| `scripts/lint_rtl.py --check` | rc 0; 90 <= ratchet 90 | `F_lint.log` |
| Differential, per-cycle trace (`scripts/add_trace.py`): the `gptp_shadow` bench at base (`e8454e27` + donor `5dce647a`) and at head | **IDENTICAL**: 3,612 change records each, sha256 `57403e63...bec90` for both. Traced: lane outputs including raw `tkeep`; all publication outputs; the debug counters; the txts state, torn, stall and PHC-loss counters; the PHC adjust; recovery counts; the engine's accepted result fields, on the accepted beat only | `differential_summary.txt`, `trace/*.gz`, `T_trace_*` |
| Base vs head summary output, `gptp_shadow` / `gptp_plane` / `gptp_txts` | identical (309, 29, 85 checks) | `G_diff_*`, `differential_summary.txt` |
| Eight reviewer probes in private copies (`scripts/plant.py`), plus an unplanted control | Control 36/36. **All 8 caught by the expected check** (`receipts/probes_summary.tsv`): <br>- ledger tag written 0, by `ledger lockstep`; <br>- ledger type and seq written at the head, by `ledger lockstep`; <br>- RX lane = lowest enabled lane, by `rx_fifo lockstep`; <br>- RX bad-frame mask widened over the lane bits, by `rx_fifo lockstep`; <br>- TX decode `<=`, by `tx_fifo decode` and `tx_fifo lockstep`; <br>- timer deadline written at slot^1, by `timer lockstep`; <br>- result gen written 0, by `results lockstep` and `results values: gen`; <br>- result ok written 1, by `gptp_shadow` 305/309. That confirms `one_valued.tsv`'s covered-by claim for `ok` | `PR_*.log`, `probes_summary.tsv` |
| `tsn_fuzz` (scratch head) | rc 0, but **build and self-tests only**. Both field campaigns SKIPPED (generator absent), so this is not plane evidence | `H_tsn_fuzz.log` |
| 23 documentation and source gates the diff touches (`scripts/doc_gates.sh`) | All rc 0. They include: <br>- `docs_check`, `check_em_dash --base`, doc style, TOC check and anchors, doc paths, doc map; <br>- module matrix, `check_gptp_docs --with-submodule`, submodule docs and diagram, time-sync diagram, diagram PNGs; <br>- RTL source lists, `ci_scope --selftest`, test evidence, the py, cpp and sv idiom ratchets, hygiene; <br>- `pp_resource_gate check-baseline`, `gen_one_valued_table --check`, `git diff --check` base..head | `docgates/*` |
| RTL since the measured and swept heads | `git diff 49e1ce48..354f7818 -- hdl gptp-processor third_party syn/ooc sw` and `9c7ad7f4..354f7818` change comments only, plus a docs-only gitlink move (`861e8f80` to `18dd997b`: `docs/MANAGER.md`). So the round-1 route and sweep apply to this head's compiled RTL | (commands in this row) |
| Commit format | 20 parent and 5 donor commits, each one line, no merges | (command: `git log --format=%B`) |
| Hosted runs at the exact head | none: 0 check runs, 0 workflow runs, status pending with 0 statuses. GitHub reports the PR `CONFLICTING` | `hosted_at_head.txt`, `pr713_metadata.json` |
| Trial merge with live dev `ac2c5e77` (disposable clone, `git merge-tree`) | Content conflicts in `docs/design/AREA_BUDGET.md` and `docs/design/MARK_II_AREA_PLAN.md`. `docs/testing/TESTING.md` auto-merges | `merge_tree_head_vs_dev_ac2c5e77.txt` |

## Findings

### R593-3-R-01: RESIDUE (Tests, Docs). The suite Makefile's comment undercounts the declaration-list controls

- **Location:** `tb/verilator/gptp_tables/Makefile:62-63`.
- **Evidence:** the comment says "and two wrong declaration lists". `mutants.py` carries four list controls: `declaration_missing`, `declaration_wrong_value`, `declaration_many_valued` and `declaration_stray` (`mutants.py:197-214`). Its docstring (`:17`), the README (`:89`) and the TESTING.md row (`:601`) all say four.
- **Impact:** wording in a comment only. No test, control, count, verdict or generated artifact changes.
- **Exact fix:** in `tb/verilator/gptp_tables/Makefile:62`, replace `and two wrong declaration` with `and four wrong declaration`.
- **Verification:** the comment matches `python3 tb/verilator/gptp_tables/mutants.py --list`, which shows four `one_valued.tsv` rows.

### R593-3-S-01: SUGGESTION (Docs). The donor's new engine figures lost their evidence link

- **Location:** `gptp-processor` `docs/MANAGER.md:35-56` at `18dd997b`.
- **Evidence:** the page states the new engine figures (4,748 LUT, 3,396 registers, WNS +2.249 ns). The paragraph's previous link to its measurement reports was removed, and no link replaces it. The figures agree with the published round-1 hand-off ("Donor: -105 LUT, -256 FF"). They are donor-owned and outside this repository's gates.
- **Suggested outcome:** in the donor PR (FPGA-gPTP #78) or later, link the page to the published M7 evidence for those figures.

### Retained prior items, both SUGGESTION

- **R592-2-S1 (Tests), optional.** The ledger's full-table write guard (`n_led_r != TXTS_CAP_N_P`) is never exercised, because the ledger reaches 3 of 8. The round-3 assignment made it optional, and the README states the reach.
- **R593-1-S-03 (Robustness), pre-existing.** The lane guard `KL_gptp_shadow.sv:271` admits widths the classifier and gearbox cannot serve. The manager routes it to #495 at merge, and the PR body says so.

## Prior public review findings at this head

| Prior item | Status at this head | Basis |
|---|---|---|
| R593-2-F1 MINOR (Tests, Docs): result `ok` and `gen` one-valued and undisclosed | **Resolved** | Census of all 11 columns (`gptp_tables_wrap.sv:467-495`, `sim_main.cpp:259-277,613-650`). One named check per column. One list, `one_valued.tsv`, declares `tag`, `ok`, `gen` with value, reason and covering suite. The README table is generated from it (`scripts/gen_one_valued_table.py --check` rc 0, and the first step of `make`). My run prints `ok` and `gen` as 1 distinct and declared. My `res_gen_stuck0` probe fails `results values: gen`. My `res_ok_stuck1` probe fails `gptp_shadow` (305/309), as the list states. Five stuck-column and four list controls are caught by name |
| R593-2-R-01 RESIDUE: PR-body checkout command | **Resolved** | The body reads `git switch --detach origin/640-m7` |
| R593-2-S-01 SUGGESTION: tautological decode coverage | **Resolved** | The check is gone. The run prints the enables the plane presented (`sim_main.cpp:567-569`); `tx_fifo decode` and its control remain |
| R592-2-RES1 RESIDUE: PR body called the PR a draft | **Resolved** | The body says "Marked ready for review; merge waits for both reviews to be positive." The PR is not a draft (`pr713_metadata.json`) |
| R592-2-S1 SUGGESTION (optional) | **Retained** | Not taken, as permitted |
| R592-1-F1 MINOR, F2, F3, F4, F5 | **Resolved** (as R593-2 and R592-2 found), unchanged since | The slow-engine phase and `results_write_index` (caught in my run); the comments at `KL_gptp_shadow.sv:236-242,258-261,877-879`; the plan sentence; the decode check; the hand-off label |
| R593-1-R-01, R-02, S-01, S-02 | **Resolved**, unchanged since | The plan sentence, the shadow comments, the tag limit (now in the generated table), the #714 note (`README.md`, coverage paragraph) |
| R593-1-S-03 SUGGESTION | **Retained**, pre-existing | Routed to #495 at merge |

## Lens results

```text
[R593] PASS Conformance - assignment 6097272538, rounds 6100980189 and 6104116064 vs hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:230-276,316-326,423-475,567-611,777-890; KL_gptp_txret.sv:328-360,530-600,630-740; gptp-processor hdl/common/KL_gptp_timer.sv:73-130; docs/design/MARK_II_AREA_PLAN.md:557-560,672-718,849-853; docs/design/AREA_BUDGET.md:194-201,264-268; PR #713 body; author HANDOFF.md sections 1-6 at 3e0f36b8 - five tables changed storage form; none narrowed; rf_r and the other dual- or parallel-read tables untouched, each with a stated reason. Widths, depths and read latency unchanged: both FIFOs keep ADDR_WIDTH = $clog2(BYTES/KEEP_W_C) because axis_fifo.v:137 takes DEPTH in beats with KEEP_ENABLE=0; every converted table keeps one write and a combinational read at the same address. No port list, register map, wire or timestamp-path file in the diff. Function: per-cycle differential trace base == head; gptp_shadow/gptp_plane/gptp_txts identical counts at base and head. Block RAM freed (RAMB18 27 to 25), never added. The route was measured at 49e1ce48, whose compiled RTL equals this head (comment-only diff). Its figures re-derive: -369 = -229 - 414 + 274; WNS fall 0.177 <= 0.25. D7 is respected (no record --write). The below-range saving (plane 107-253 against 300-700) is stated as not met in the plan, the budget, the PR and the issue, as the assignment's "report honestly" requires. Accepting it is a pending manager decision, listed below. Round-3 items 1-3 are met; the #621 merge item does not apply (PR #707 still open).
[R593] PASS RTL - KL_gptp_shadow.sv:244-276,316-326,430-475,567-611,777-890; KL_gptp_txret.sv:339-357,537-541,587-599,630-707,733-740; KL_gptp_timer.sv:76-125; third_party/verilog-axis/rtl/axis_fifo.v:137,164,180-185,227,292,459; KL_gptp_engine.sv:349-350,478-519 - the RX highest-lane encoder is the base serializer's rule moved ahead of the FIFO. The TX count decode equals the base gearbox mask, because gb_keep_r only ever held lanes 0..idx-1 and CNT_W_C'(gb_idx_r)+1 <= 8 fits 4 bits. tuser bit 0 alone judges a bad frame (mask/value 1; the test at axis_fifo.v:292 is bitwise on the mask), and MARK_WHEN_FULL=0 means the stored lane is never overwritten (:227). ledger_ram, result_ram and deadline_ram take the base write conditions, with rst_n gating standing in for the base reset branch. Every read of an un-reset word is guarded: by have_entry_w for tag_ok_w and resolve_w, by txts_valid_o with an accept-only engine consumer, or by armed_r. The new g_refuse_lanes guard refuses lane counts outside 1..8. Single clock domain, no CDC primitive touched. Lint ratchet 90 <= 90; donor lint rc 0.
[R593] PASS Robustness - receipts A_tables_all.log, T_trace_{base,head}_shadow + differential_summary.txt, PR_rx_bad_mask_wide.log, PR_rx_lowest_lane.log, PR_led_write_at_head.log - malformed, runt, oversize, foreign-EtherType and wrong-version frames, corrupted tkeep, 33,354 overflow and 12,751 bad drops, 12.1 M stalled TX cycles, held launch records, the slow-engine phase and two warm resets in traffic all run in lockstep with zero mismatches. The gptp_shadow differential adds record faults, barriers, link-guard episodes, PHC loads and observer resets, and is byte-identical at base and head. A bad-frame mask that leaked onto the lane bits is caught. Configuration: the guard refuses more than 8 lanes; TXTS_CAP_N_P keeps explicit modular pointers. The pre-existing fence/tx_fifo wedge is #714 (open): dev and head behave identically there, and the README defers per-segment coverage to its fix.
[R593] PASS Tests - tb/verilator/gptp_tables/{gptp_tables_wrap.sv,sim_main.cpp,mutants.py,one_valued.tsv,README.md,Makefile,waivers.vlt}; scripts/gen_one_valued_table.py; receipts A_tables_all.log (36/36, 26/26), probes_summary.tsv (8/8 by the expected check, control green), B_shadow_all.log, C_txts_all.log, E_plane.log, D_gp_contract_tb_lint.log - every oracle is the PREVIOUS storage form, written from untouched signals: an axis_fifo with KEEP_ENABLE=1 and eight tkeep bits, the old gearbox enables, and reset-cleared register arrays. Comparisons are gated by the consumers' real sampling conditions. Coverage thresholds are graded by name, and each threshold sits below the reach the run prints. The census grades every converted column: one-valued columns must be declared with their exact value, and stray declarations fail. The two declared, unreached columns are justified: ok is caught by gptp_shadow (my probe), and gen has no consumer past TXQ_MASK_C (gen_gptp_ucode.py:369-376; no other reader in hdl/). The test-only forces fabricate nothing, and their lint waiver is scoped to three nets. The suite is in run_all_suites.sh --list. R593-3-R-01 is RESIDUE only.
[R593] PASS Docs - docs/design/MARK_II_AREA_PLAN.md:560,672-718,849-853; docs/design/AREA_BUDGET.md:197-200,267-268; docs/testing/TESTING.md:150,409-410,601; tb/verilator/gptp_tables/README.md; regenerated MODULE_MATRIX.md and three README-tests.md; eight donor pin-link pages at 18dd997b; syn/yosys/rom_digests.tsv; KL_gptp_shadow.sv comments; receipts docgates/* (23 gates rc 0), I_gp_docs.log - every figure checked: FIFO words 74 and 73 bits before, 69 after; primitives 4+1, 16+1 and 5+2 for 21, 89 and 32 bits; routed deltas; firmware tiles 87.5 to 86.5; the README reach table matches my run (27 beats, 3 and 3 deep, slots 0x3f). No authoritative page keeps a stale storage statement (searched GPTP_PLANE.md and the gPTP guides). The limits table is generated from the graded list. R593-3-R-01 (Makefile comment) is RESIDUE; R593-3-S-01 (donor page link) is a SUGGESTION.
```

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment and round-2/3 rulings; shadow, txret and donor timer RTL; plan and budget M7 sections; PR body; HANDOFF sections 1-6; differential and suite-equality receipts | R593-3 | `354f781828d8b4d73037129f297b072320a10f9c` |
| RTL | CLEAN | `KL_gptp_shadow.sv`, `KL_gptp_txret.sv`, `KL_gptp_timer.sv` (donor `18dd997b`), `axis_fifo.v`, engine result face; lint ratchet and donor lint | R593-3 | `354f781828d8b4d73037129f297b072320a10f9c` |
| Robustness | CLEAN | `gptp_tables` run (malformed input, overflow, stalls, warm resets), `gptp_shadow` differential trace (faults, barriers, resets), bad-mask, lane and write-index probes; guard and pointer arithmetic | R593-3 | `354f781828d8b4d73037129f297b072320a10f9c` |
| Tests | CLEAN (R-01 RESIDUE carried) | `tb/verilator/gptp_tables/*`, `scripts/gen_one_valued_table.py`; 36/36 and 26/26; eight probes plus control; neighbouring suites and donor `tb` | R593-3 | `354f781828d8b4d73037129f297b072320a10f9c` |
| Docs | CLEAN (R-01 RESIDUE, S-01 SUGGESTION carried) | Plan, budget, TESTING.md, suite README and list, generated matrix, donor pin links, ROM digests, source comments; 23 doc gates and donor `docs` | R593-3 | `354f781828d8b4d73037129f297b072320a10f9c` |

Coverage holds only for this head. The merge candidate must change `docs/design/AREA_BUDGET.md` and `docs/design/MARK_II_AREA_PLAN.md` to resolve the dev conflicts. That re-opens Docs and Conformance for the resolved text, which this round has not seen.

## Real limits of this round

- **Physical calibration NOT RUN.** No hardware, bench or field evidence was produced or inferred. The `tsn_fuzz` field campaigns were skipped (generator absent) and are not evidence.
- **No manager source bank runs at this head**, and none is claimed or inferred. This round's source-head execution is listed above. The author's published gate receipts (round 1 at `9d42762c`, round 3 at `354f7818`) are the other source-head evidence.
- **Not run by this round**, relying on the author's round-1 receipts at RTL-identical commits:
  - the full suite sweep (61/61) and `milan_dp` both legs (N=4, N=8);
  - `milan_dp_gptp` (physical), the timestamp and CDC suites (`ptp_ts`, `ptp_sync`, `ptp`, `cdc`, `clkvalid`), Yosys portability, the xvlog gate and the builder.
  - The changed modules are elaborated by `gptp_shadow`, `gptp_tables`, `gptp_txts`, `milan_dp`, `tsn_fuzz` and the engine suites. Of these, this round ran all but `milan_dp` and the `tsn_fuzz` campaigns.
- **The Vivado route, OOC mapping and primitive census were not reproduced.** The resource figures are the author's route #2 at `49e1ce48`, and this round only re-derived their arithmetic. `gptp_txts` ran with its LiteX stale-chain check bypassed.
- The base/head equality covers the `gptp_shadow`, `gptp_plane` and `gptp_txts` stimuli. No equivalence proof was attempted.

## Pending manager duties

- **Decide the below-range saving.** The lane's target was about 500 LUT (300-700); it measured 107-253 for the plane, with 1,149 FF and one block-RAM tile freed. Also decide the `tsf_r` block-RAM option the plan leaves open.
- **Build and validate the current-dev merge candidate** (source base `e8454e27`, live dev `ac2c5e77`) with the builder and native banks, and link the receipts:
  - resolve the content conflicts in `AREA_BUDGET.md` and `MARK_II_AREA_PLAN.md`;
  - fold in the #621 donor merge (PR #707 and FPGA-gPTP #77) if it lands first;
  - publish the donor branch (`18dd997b`, FPGA-gPTP #78) before the parent.
- **Own hosted and act acceptance.** No hosted run exists at this exact head (0 check runs, 0 workflow runs; the PR is `CONFLICTING`). The exact-head `verilator-suites` and `yosys-portability` evidence that AGENTS.md section 7 requires does not exist yet.
- **Carry the open items.** R593-3-R-01 goes to the residue checklist. R593-1-S-03 goes to #495 at merge. #714 stays open as filed.

## Packet

- `scripts/`:
  - `job.sh`, the detached job runner;
  - `plant.py`, the eight probes;
  - `add_trace.py`, the differential trace;
  - `doc_gates.sh`;
  - `clone_integrity.sh`.
- `receipts/` holds every log and rc file named above. The publishable files are listed in `MANIFEST.sha256`; `scratch/` is not published.

R593-3 FINISHED
