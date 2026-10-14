# HANDOFF: lane M7 for #640, fabric gPTP plane tables (plan L10a)

Executor [A587]. Reviewers [R592] (internal) and [R593] (external).
Branch `640-m7` from dev `e8454e27`.
Round 1 head `9d42762c555118e3ea86665bf7d8c6ef673698d3`, pushed as PR #713.
Round 2 head `2cc2ba0b8b08010df5ee12c1fc228851fa9a8444`: four new commits on top, local only, not pushed.
Round 3 head `354f781828d8b4d73037129f297b072320a10f9c`: four new commits on `2cc2ba0b`, local only, not pushed. The donor is unchanged.
Historical Round 1 donor: the gPTP processor submodule branch `640-m7` was at `18dd997b2459699e41e5ce9bceca1181e41fa5fe` (from `5dce647a`), pushed as donor PR FPGA-gPTP #78. Round 2 adds no donor commit; the gitlink is unchanged.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6097272538
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6097298086
REVIEW READY (round 1): https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6100339945
Round 2 assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6100980189
REVIEW READY (round 2): https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6103827621
Round 3 assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6104116064
REVIEW READY (round 3): https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6104542951

## Status

Round 5: REVIEW READY at parent `4c5d70b50230fbd5da347852d39daf7f23b3df0b`; donor `e4869fd0c42889b2ac806587cc5c78afb1c33461` unchanged. See [Round 5](#round-5) for the current scope and evidence. Prior sections retain historical results.

Historical Round 4 continuation: REVIEW READY under owner ruling 6162175442. Parent `412e3f6c8c402bce63e94c291d2782b5579aaa1d`; donor `e4869fd0c42889b2ac806587cc5c78afb1c33461`. Both repositories are clean and local only. All assigned continuation checks pass, including all 26 table controls and 33 donor engine mutants. See the final continuation results and receipts below.

Round 3: REVIEW READY at `354f7818`, see the [Round 3](#round-3) section at the end.
Round 2: see the [Round 2](#round-2) section. Sections 1 to 10 are the round-1 record at `9d42762c`, except the F5 label in section 4.

Round 1: REVIEW READY at `9d42762c`. Every gate listed below returned 0.
Integrated route through the M0s recipe: gate `check` PASS against `route-1x1`, all endpoints met, route complete, no exception added.
Measured saving: the gPTP plane is 107-253 LUTs smaller, below the plan's 500 (300-700); 1,149 plane FFs and one block-RAM tile are freed.
The gate record is not re-recorded (D7: only M9 re-records).

## 1. Measured starting point (dev `e8454e27`)

The base route of dev `e8454e27` equals the `route-1x1` record in every gated figure.
Its routed census gives `g_gptp_plane.u_gptp_shadow` 5,107 LUT (508 LUTRAM), 5,899 FF, 3 RAMB36 + 3 RAMB18, 4 DSP.
That route is lane M2's base route of the same commit (read only; receipts in section 10).

| Table | Module | Shape | Primitives at dev | LUT sites |
|---|---|---|---|---:|
| `bank_r` (message bank) | `KL_gptp_engine` | 64 x 64 | 21 RAM64M + 1 RAM64X1D | 86 |
| `scratch_r` | `KL_gptp_engine` | 64 x 64 | 64 RAM64X1S | 64 |
| `ann_ctx_r` | `KL_gptp_engine` | 32 x 64 | 11 RAM32M | 44 |
| `evq_pd_ctx_r` | `KL_gptp_engine` | 4 x 144 | 24 RAM32M | 96 |
| `evq_r` | `KL_gptp_engine` | 4 x 40 | 4 RAM32M + 2 RAM32X1D | 20 |
| `rf_r` | `KL_gptp_ucpu` | 16 x 64, three reads | 33 RAM32M | 132 |
| `slot_r` | `KL_gptp_tx_slot` | 128 x 8 | 6 RAM64M | 24 |
| `tsf_r` | `KL_gptp_shadow` | 32 x 64 | 11 RAM32M | 44 |
| `led_type_r`, `led_seq_r`, `led_tag_r` | `KL_gptp_txret` | 8 x 21 | flip-flops, LUT read muxes | - |
| `res_*` | `KL_gptp_txret` | 8 x 89 | flip-flops, LUT read muxes (111 MUXF7 in the ledger) | - |
| `deadline_r` | `KL_gptp_timer` | 8 x 32 | flip-flops, LUT read mux | - |
| `rx_fifo` storage | `axis_fifo` in the shadow | 256 x 74 | RAMB36 + RAMB18 | - |
| `tx_fifo` storage | `axis_fifo` in the shadow | 256 x 73 | RAMB36 + RAMB18 | - |

The historical 464 LUTRAM sites are the engine's; the plane's are 508 (the shadow's `tsf_r` adds 44).

## 2. What was eligible, and why

The gate holds RAMB36 and RAMB18 at zero growth, so a table can move into block RAM only onto a freed tile.

- The two plane FIFOs carry 74 and 73 bits; 72 fit one RAMB36. Their consumers read `tkeep` only as a lane. The RX serializer stops after the highest enabled lane. The TX gearbox only builds enables from lane 0. A three-bit lane (RX) and a four-bit count (TX; count 0 is the all-clear `tkeep` of an empty FIFO) free one RAMB18 each.
- The message bank then moved onto those two RAMB18 and was routed (route #1, `ba350298`). The state port's read register cannot be the block RAM's latch for every read, so the bank's data must merge with it. That merge fans out into three micro-CPU consumers (write-back, copy lane, descriptor base). Placed, the engine level grew by 165 logic LUTs for 86 LUTRAM sites freed. It was reverted (`861e8f80`); the two RAMB18 stay freed.
- The egress ledger fields, the result queue and the timer deadlines are flip-flop tables written at one index and read combinationally at one other. No reader samples an entry not written since reset: the ledger is read only while it holds an entry, the engine takes a result only on an accepted beat, and the sweep reads a deadline only for an armed slot. They move to distributed RAM with the same read latency.
- Not eligible: `rf_r` (three reads in one cycle for `OP_SET_MASKED`), `ann_ctx_r` (written in the same cycle as the bank), `evq_pd_ctx_r` (144 bits read whole at pop), `evq_r` (read combinationally for dispatch), `scratch_r` (state-port read: the same merge as the bank), `led_live_r` (a barrier clears every entry in one cycle), `ann_pub_tail_r` and the publication banks (read in parallel).
- Index narrowing gains nothing: every LUTRAM table is already at its primitive's depth granularity, and the bank's unused words (13-15, 24-31) are inside one 32-word half.

## 3. Changes (file:line at `9d42762c`)

RTL, parent:
- `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:233-244`: lane field widths (`LANE_W_C`, `CNT_W_C`) and the FIFO depths in beats.
- `KL_gptp_shadow.sv:269`: elaboration refusal of a lane count outside 1..8 (`g_refuse_lanes`).
- `KL_gptp_shadow.sv:319`: `rx_top_lane`, the highest enabled lane of the tap beat.
- `KL_gptp_shadow.sv:432,440`: `rx_fifo` without `tkeep`, `tuser` = {lane, bad}, depth in beats.
- `KL_gptp_shadow.sv:573,597`: the serializer stores the lane (`ser_top_r`) instead of eight enables.
- `KL_gptp_shadow.sv:797,819`: the gearbox keeps the beat's lane count (`st_cnt_r`); `gb_keep_r` is gone.
- `KL_gptp_shadow.sv:835,843,879-883`: `tx_fifo` carries the count in `tuser`; `tx_tkeep_o` is decoded from it.
- `hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv:339-353`: ledger fields and result queue as distributed RAM, and the ledger's one named read port (`led_head_*_w`).
- `KL_gptp_txret.sv:540,590,597`: the tag check and both outcome terms read that port.
- `KL_gptp_txret.sv:636-643,669`: `ledger_ram` takes the allocation write outside reset; `led_live_r` stays a register.
- `KL_gptp_txret.sv:699`: `result_ram` takes the resolution write outside reset.

RTL, gPTP processor submodule (`5dce647a..18dd997b`):
- `hdl/common/KL_gptp_timer.sv:80,89-95,107`: deadlines in distributed RAM, written by `deadline_ram`, read by the sweep through `delta_w` as before.
- `docs/MANAGER.md`: the engine's measured snapshot from its own `make ooc` (4,748 LUT, 3,396 registers, 1.5 BRAM, 4 DSP, +2.249 ns; micro-CPU repeats 1,643/733).
- History: `f61b90c6` moved the bank to block RAM, `4f9fb19b` moved two evidence anchors, `861e8f80` reverts both. The engine RTL equals `5dce647a`.

Tests and their anchors:
- New suite `tb/verilator/gptp_tables/` (Makefile, wrapper, harness, `mutants.py`, README, `.gitignore`).
- `tb/verilator/gptp_shadow/mutants.py:75`: the `no_tag_check` anchor follows the ledger's read port.
- `scripts/check_gptp_docs.py:182`: the pinned `res_ok_w` token follows the same port.

Generated and pin follow-up (through their generators): `docs/diagrams/submodule_boundaries.*`, `docs/diagrams/timesync_chain.*`, `docs/diagrams/PNG_MANIFEST.json`, `syn/yosys/rom_digests.tsv` (rows for `8b8d0beb`, `861e8f80`, `18dd997b`, all the unchanged image digest `c496ed8a`), `docs/traceability/MODULE_MATRIX.md` and three `README-tests.md`.
Docs: the donor links in eight pages; `docs/testing/TESTING.md` (suite row and the two submodule-reader lists); `docs/design/MARK_II_AREA_PLAN.md` (L10 line, "M7 intermediate measurement", block-RAM ledger lines); `docs/design/AREA_BUDGET.md` (M7 note, freed tile).

## 4. Tests and the planted defect each catches

`tb/verilator/gptp_tables` runs the real plane inside the `gptp_shadow` slice bench (engine, ledger, launch observer, link guard, PHC).
Beside it, each changed table is kept in its old storage form, written by the old RTL's conditions from untouched signals.
It is compared every cycle with what the table's consumer receives (`gptp_tables_wrap.sv`):

| Table | Reference | Compared (wrapper line) | Named check (`sim_main.cpp`) |
|---|---|---|---|
| Tap FIFO | `axis_fifo` with eight `tkeep` bits (`:184`) | ready, valid, overflow/bad/good; data, last, lane while valid (`:222`) | `rx_fifo lockstep` (`:451`) |
| Transmit FIFO | old gearbox enables (`:236`) into the eight-bit FIFO (`:266`) | ready, valid, last, data, `tkeep`, every cycle (`:300`) | `tx_fifo lockstep` (`:452`) |
| Ledger fields | reset-cleared registers (`:330`) | the read port at the head while non-empty (`:363`) | `ledger lockstep` (`:453`) |
| Result queue | reset-cleared registers (`:330`) | the result face while valid (`:372`) | `results lockstep` (`:454`) |
| Timer deadlines | reset-cleared registers (`:383`) | `delta_w` for an armed sweep slot (`:402`) | `timer lockstep` (`:455`) |

Stimulus: 29.1 M cycles from a fixed seed. A peer answers the engine's Pdelay requests and is a better master (Announce, Sync, Follow_Up), except in the stall phase, where the engine becomes grandmaster.
Around it runs a mix of every type, malformed, foreign, runt and oversize frames, and corrupted `tkeep`. There are FIFO-overflowing bursts, long TX stalls, held launch records and two warm resets in traffic.
Coverage checks (`:458-477`) make each zero informative: every RX lane delivered, 33,528 overflow drops, 256 beats deep; TX lane counts 2/4/8, 27 beats queued; every ledger and result entry was the head, 3 ledger entries outstanding; timer slots 0-5.
Result at the head: 21/21 checks.

Planted defects (`mutants.py:54-139`), each in private copies of the inputs, each required to fail its own table's named check; 15/15 caught:

| Control | Defect | Caught by |
|---|---|---|
| `rx_fifo_wrong_depth` | depth halved | `rx_fifo lockstep` |
| `rx_fifo_wrong_read_latency` | `RAM_PIPELINE` 2 | `rx_fifo lockstep` |
| `rx_fifo_lane_alias` | lanes 4-7 alias 0-3 | `rx_fifo lockstep` |
| `tx_fifo_wrong_depth` | 16 of 256 beats | `tx_fifo lockstep` |
| `tx_fifo_wrong_read_latency` | `RAM_PIPELINE` 2 | `tx_fifo lockstep` |
| `tx_fifo_count_alias` | three-bit count: 8 aliases 0 | `tx_fifo lockstep` |
| `ledger_wrong_depth` | one entry short | `ledger lockstep` |
| `ledger_wrong_read_latency` | registered head port | `ledger lockstep` |
| `ledger_index_alias` | head MSB dropped | `ledger lockstep` |
| `results_wrong_depth` | one entry short | `results lockstep` |
| `results_wrong_read_latency` | registered result face | `results lockstep` |
| `results_index_alias` | head MSB dropped | `results lockstep` |
| `timer_wrong_depth` | half the slots | `timer lockstep` |
| `timer_wrong_read_latency` | registered sweep read | `timer lockstep` |
| `timer_index_alias` | slots 4-7 alias 0-3 | `timer lockstep` |

Supplementary, not committed (scratch): a differential build of the same harness with the reference models removed hashes every plane-visible value each cycle. Covered: lane outputs, publication, PHC controls, the micro-CPU's state-port read data, the engine byte faces, ingress timestamps at the serializer and the result face. Over 29,100,030 cycles the dev `e8454e27` RTL and this lane's RTL give the same hash, `5de6fe9546553c22`.

Existing suites that cover the plane, at heads whose RTL and tests equal the final head: `gptp_shadow` 309/309 with 9/9 controls; `gptp_txts` 85/85 with 6/6; `gptp_plane` 29/29; `milan_dp` 12,065 checks (legacy, N=4 and N=8 legs); `milan_dp_gptp` (physical) 197; `tsn_fuzz` with the pinned generator: gPTP field campaign 677 pass, 0 fail, committed artifact fresh, AAF 164 pass; the gPTP processor's `make tb` (micro-CPU 768, parser 268, engine 1,613 x3, 40/40 donor mutants (engine 33, gaskets 4, tsngen 3), and the Arty bench).

## 5. Primitive mapping before and after (routed census, cell names)

| Table | Before | After |
|---|---|---|
| Tap FIFO | 1 RAMB36 + 1 RAMB18 | 1 RAMB36 (SDP 72, READ_FIRST) |
| Transmit FIFO | 1 RAMB36 + 1 RAMB18 | 1 RAMB36 |
| Ledger `led_type_r` / `led_seq_r` / `led_tag_r` | 168 FF + read muxes | 1 RAM32M / 3 RAM32M / 1 RAM32X1D |
| Result queue `res_ns_r` / `seq` / `type` / `ok` / `gen` | 712 FF + read muxes | 11 / 3 / 1 RAM32M, 1 RAM32X1D, 1 RAM32M |
| Timer `deadline_r` | 256 FF + read mux | 5 RAM32M + 2 RAM32X1D |
| Message bank (unchanged) | 21 RAM64M + 1 RAM64X1D | 21 RAM64M + 1 RAM64X1D |

Plane cells: LUT cells 5,780 -> 5,388, MUXF7 168 -> 57, RAMB18 3 -> 1; FF -1,149 (ledger -880, timer -256, wrapper -16).
Vivado names the ledger's RAM cells `milan_datapath/u_txret/...`, so the hierarchy report files 84 LUTRAM sites under the datapath's own level.

Out of context (scratch, the plane alone, AreaOptimized_high + opt_design ExploreArea, 20 ns):

| Variant | Plane LUT | LUTRAM | FF | RAMB36 / RAMB18 |
|---|---:|---:|---:|---:|
| dev `e8454e27` | 5,134 | 510 | 6,132 | 3 / 3 |
| FIFO lane fields only | 5,134 | 510 | 6,116 | 3 / 1 |
| + bank in block RAM (mux form) | 5,073 | 424 | 6,117 | 3 / 3 |
| + ledger, results, deadlines | 4,979 | 532 | 4,984 | 3 / 3 |
| + bank output as OR | 4,925 | 532 | 4,985 | 3 / 3 |
| Final (bank in LUTRAM) | 5,027 | 618 | 4,983 | 3 / 1 |

Per-module figures move by up to 80 LUTs in unchanged modules between these runs (the parser by 68, the engine's own level by 80), so only totals are compared.

## 6. Resource and route before and after (M0s recipe)

Recipe: `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` "Integrated measurements", `--single-thread-synthesis`, Vivado 2026.1, one route at a time under the host lock.
Each candidate is a clean clone with the four submodules initialised at their gitlinks. Its `baseline_integrated.tcl` and XDC equal the base's apart from checkout paths, so no exception was added.

| Measurement | LUT | FF | Slices | RAMB36 / RAMB18 | DSP | WNS / WHS, ns | Route |
|---|---:|---:|---:|---:|---:|---|---|
| Record `route-1x1` / base `e8454e27` | 50,267 | 54,413 | 15,779 | 74 / 27 | 14 | +0.299 / +0.031 | complete |
| Route #1, bank in block RAM, `ba350298` | 50,339 | 53,156 | 15,775 | 74 / 27 | 14 | +0.091 / +0.014 | complete |
| Route #2, final RTL, `49e1ce48` | 49,898 | 53,220 | 15,773 | 74 / 25 | 14 | +0.122 / +0.019 | complete |

Route #2: gate `check` PASS (LUT -369, FF -1,193, slices -6, RAMB18 -2, WNS fall 0.177 <= 0.25, WHS fall 0.012). All 100,073 routable nets routed, 0 routing errors. No negative-slack path in any of the four signoff corners. Worst setup path: SoC write buffer (`milansoc_write_w_buffer_level0_reg` -> `storage_13_dat1_reg`), not the plane.
Route #2's head `49e1ce48` differs from the final head only in docs; its RTL equals `9c7ad7f4`, where the sweep ran.

Attribution (route #2 against base):

| Scope | Routed LUT | Post-synthesis LUT | Out of context |
|---|---:|---:|---:|
| gPTP plane | -229 | -253 | -107 |
| Untouched processor wrapper | -414 | -449 | - |
| Rest of the image | +274 | +358 | - |

The untouched wrapper moves more than the plane, so the image delta is mapping movement, not a reproducible saving.
The plane figures (107-253) are below the plan's 500 (300-700).
Reason: the LUTRAM tables were already at their primitives' density. The only block-RAM target that fits the zero-growth tile budget (the bank) costs more in its output merge than it saves.
Firmware block-RAM ledger: one tile freed (87.5 -> 86.5 tiles), recorded in the plan; the ledger table keeps the record until M9.

## 7. Gate table

Interpreters: `$PY312` hosted-equivalent CPython 3.12.3; `$MDPY` the pinned Markdown environment; `$HOSTPY` the host CPython (PyYAML); `$LITEX_PYTHON` the LiteX environment; `$VERILATOR_DIR` the pinned Verilator 5.050; `$BASE` = `e8454e2751d05b02ee8e5a571857589ab358ab86`.
Each command ran from the lane root at `9d42762c`, with its own log and status file. None was piped.

| Gate | Command | rc |
|---|---|---:|
| py_idiom | `$PY312 scripts/check_py_idiom.py` | 0 |
| py_idiom_self | `$PY312 scripts/check_py_idiom.py --selftest` | 0 |
| sh_idiom | `$PY312 scripts/check_sh_idiom.py` | 0 |
| sh_idiom_self | `$PY312 scripts/check_sh_idiom.py --selftest` | 0 |
| cpp_idiom | `$PY312 scripts/check_cpp_idiom.py` | 0 |
| cpp_idiom_self | `$PY312 scripts/check_cpp_idiom.py --selftest` | 0 |
| sv_idiom | `$PY312 scripts/check_sv_idiom.py` | 0 |
| sv_idiom_self | `$PY312 scripts/check_sv_idiom.py --selftest` | 0 |
| naming | `$PY312 scripts/measure_naming.py --check` | 0 |
| naming_self | `$PY312 scripts/measure_naming.py --selftest` | 0 |
| fail_fast | `$PY312 scripts/measure_fail_fast.py --check` | 0 |
| fail_fast_self | `$PY312 scripts/measure_fail_fast.py --selftest` | 0 |
| test_evidence | `$PY312 scripts/measure_test_evidence.py --check` | 0 |
| test_evidence_self | `$PY312 scripts/measure_test_evidence.py --selftest` | 0 |
| hygiene | `$PY312 scripts/check_hygiene.py --check` | 0 |
| hygiene_self | `$PY312 scripts/check_hygiene.py --selftest` | 0 |
| todo | `$PY312 scripts/check_todo_ownership.py` | 0 |
| todo_self | `$PY312 scripts/check_todo_ownership.py --selftest` | 0 |
| control_flow_self | `$PY312 scripts/measure_control_flow.py --selftest` | 0 |
| cohesion_self | `$PY312 scripts/measure_cohesion.py --selftest` | 0 |
| docs_check | `$MDPY scripts/docs_check.py` | 0 |
| docs_nogit | `env GIT_DIR=/dev/null $MDPY scripts/docs_check.py` | 0 |
| docs_self | `$MDPY scripts/docs_check.py --selftest` | 0 |
| em_dash | `$MDPY scripts/check_em_dash.py --base $BASE` | 0 |
| em_dash_self | `$MDPY scripts/check_em_dash.py --selftest` | 0 |
| doc_style | `$MDPY scripts/check_doc_style.py` | 0 |
| doc_style_self | `$MDPY scripts/check_doc_style.py --selftest` | 0 |
| toc_self | `$MDPY scripts/gen_toc.py --selftest` | 0 |
| toc_anchors | `$MDPY scripts/gen_toc.py --verify-anchors` | 0 |
| toc_check | `$MDPY scripts/gen_toc.py --check` | 0 |
| doc_paths | `$MDPY scripts/check_doc_paths.py` | 0 |
| doc_map | `$MDPY docs/DOC_MAP.gen.py --check` | 0 |
| doc_map_self | `$MDPY docs/DOC_MAP.gen.py --selftest` | 0 |
| feature_status | `$MDPY scripts/check_feature_status.py` | 0 |
| feature_status_self | `$MDPY scripts/check_feature_status.py --self-test` | 0 |
| archive | `$MDPY scripts/check_archive.py` | 0 |
| archive_self | `$MDPY scripts/check_archive.py --selftest` | 0 |
| solution | `$MDPY scripts/check_solution_docs.py` | 0 |
| solution_self | `$MDPY scripts/check_solution_docs.py --selftest` | 0 |
| module_matrix | `$MDPY docs/traceability/gen_module_matrix.py --check` | 0 |
| gptp_docs | `$MDPY scripts/check_gptp_docs.py` | 0 |
| gptp_docs_sub | `$MDPY scripts/check_gptp_docs.py --with-submodule` | 0 |
| gptp_docs_self | `$MDPY scripts/check_gptp_docs.py --selftest` | 0 |
| submodule_docs | `$MDPY scripts/check_submodule_docs.py` | 0 |
| submodule_docs_self | `$MDPY scripts/check_submodule_docs.py --selftest` | 0 |
| submodule_diagram | `$MDPY docs/diagrams/submodule_boundaries.gen.py --check` | 0 |
| submodule_diagram_self | `$MDPY docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 |
| timesync | `$MDPY docs/diagrams/timesync_chain.gen.py --check` | 0 |
| timesync_self | `$MDPY docs/diagrams/timesync_chain.gen.py --selftest` | 0 |
| diagram_pngs | `$MDPY scripts/check_diagram_pngs.py` | 0 |
| diagram_pngs_self | `$MDPY scripts/check_diagram_pngs.py --selftest` | 0 |
| soc_sources | `$PY312 scripts/check_soc_sources.py` | 0 |
| soc_sources_self | `$PY312 scripts/check_soc_sources.py --selftest` | 0 |
| port_contracts | `$PY312 scripts/check_port_contracts.py` | 0 |
| port_contracts_self | `$PY312 scripts/check_port_contracts.py --selftest` | 0 |
| rtl_source_lists | `$PY312 scripts/check_rtl_source_lists.py` | 0 |
| rtl_source_lists_self | `$PY312 scripts/check_rtl_source_lists.py --selftest` | 0 |
| pp_srcs | `$PY312 scripts/pp_srcs.py --check --selftest` | 0 |
| tied_inputs | `bash scripts/check_tied_inputs.sh` | 0 |
| sweep_shape | `$HOSTPY scripts/check_sweep_shape.py` | 0 |
| ci_scope_self | `$PY312 scripts/ci_scope.py --selftest` | 0 |
| ci_events | `$HOSTPY scripts/ci_events.py --check` | 0 |
| wire | `$HOSTPY scripts/check_wire_accountability.py --self-test` | 0 |
| baremetal | `$HOSTPY scripts/check_baremetal_only.py --check` | 0 |
| baremetal_self | `$HOSTPY scripts/check_baremetal_only.py --selftest` | 0 |
| resource_self | `$PY312 syn/ooc/pp_resource_gate.py --selftest` | 0 |
| resource_baseline | `$PY312 syn/ooc/pp_resource_gate.py check-baseline` | 0 |
| dp_srcs_self | `$PY312 syn/ooc/dp_srcs.py --selftest` | 0 |
| dp_srcs_datapath | `$PY312 syn/ooc/dp_srcs.py --top milan_datapath` | 0 |
| ooc_tcl_self | `$PY312 syn/ooc/ooc_tcl_selftest.py` | 0 |
| pp_baseline_self | `$PY312 syn/ooc/pp_baseline.py --selftest` | 0 |
| genmac_check | `$LITEX_PYTHON sw/litex/gen_mac_tx_model.py --check` | 0 |
| lint | `env PATH=$VERILATOR_DIR:$PATH $PY312 scripts/lint_rtl.py --check --self-test` | 0 |
| gp_contract | `env PATH=$VERILATOR_DIR:$PATH make -C gptp-processor contract` | 0 |
| gp_lint | `env PATH=$VERILATOR_DIR:$PATH make -C gptp-processor lint` | 0 |
| gp_docs | `env PATH=$VERILATOR_DIR:$PATH make -C gptp-processor docs` | 0 |
| diff_base | `git diff --check $BASE HEAD` | 0 |
| diff_tree | `git diff --check` | 0 |
| route_gate_base | `$PY312 syn/ooc/pp_resource_gate.py check $VALIDATION_STORAGE/640m2-a586/meas-base/ax7101/gateware --endpoint route-1x1` | 0 |
| route_gate_m7 | `$PY312 syn/ooc/pp_resource_gate.py check $VALIDATION_STORAGE/640m7-a587/meas-cand3/ax7101/gateware --endpoint route-1x1` | 0 |

Run separately, each with its own log and status file:

| Gate | Command | Head | Result |
|---|---|---|---|
| sweep shard 0/2 | `scripts/run_all_suites.sh $OUT --shard 0/2` | `9c7ad7f4` | rc 0: 61/61 suites, 2,173,804 checks, 0 failures |
| sweep shard 1/2 | `scripts/run_all_suites.sh $OUT --shard 1/2` | `9c7ad7f4` | rc 0: `milan_dp`, 12,065 checks |
| physical gPTP | `scripts/run_all_suites.sh $OUT --physical-gptp` | `74e7e6d5` | rc 0: `milan_dp_gptp`, 197 checks |
| tsn_fuzz, pinned generator | `TSN_GEN_ROOT=$TSNGEN make -C tb/verilator/tsn_fuzz` | `74e7e6d5` | rc 0: gPTP 677/0, AAF 164/0, both artifacts fresh |
| Yosys portability | `syn/yosys/run.sh` | `9c7ad7f4` | rc 0: 58 tops pass, tied-input and tap-purity gates pass |
| xvlog | `python3 scripts/xvlog_gate.py --check` and `--selftest` | `49e1ce48` | rc 0 / rc 0: 0 findings |
| gPTP processor benches | `make -C gptp-processor tb` | `49e1ce48` | rc 0 |
| builder, both shapes | `$LITEX_PYTHON sw/builder/test_builder.py --require-elaboration --require-rv32` | `9d42762c` | rc 0; gate 11 not run (Arty calibration report absent on this host) |
| route gate, base and M7 | in the table above | - | rc 0 / rc 0 |

`9c7ad7f4..9d42762c` and `74e7e6d5..9d42762c` change only Markdown, generated diagrams, one ROM digest row and the gitlink. The submodule moves `861e8f80..18dd997b`, `docs/MANAGER.md` only. No file a suite builds changed.
Lint: 90 violations against the ratchet of 90. The sweep ran with VERILATOR_JOBS=2, the pinned Verilator and the LiteX interpreter for `gptp_txts`.

## 8. Pre-existing defect observed (not changed by this lane)

`KL_gptp_shadow` pops `tx_fifo` on `tx_tready_i` (the instance's `.m_axis_tready`), while the departure fence holds `tx_tvalid_o` low (`fn_S != FN_OPEN`).
A frame admitted while the fence holds then leaves the FIFO with no departure counted.
Its ledger entry never resolves, the response claim never clears, and the engine's event queue wedges behind the next Pdelay_Req.
`gptp_tables` reaches it after its second warm reset, because its lane ready does not wait for valid. At the end of that run the dev `e8454e27` RTL shows the head event Pdelay_Req and a valid response claim. It also shows one ledger entry, zero departures, an empty FIFO and an open fence.
The shipping merge arbiter raises its ready for this source only while it is valid or locked to it, so the routed image may not reach it.
The run hashes identically on the dev RTL and on this lane's RTL. It needs a separate issue; this lane does not change it.

## 9. Open risks and decisions

- Decision offered, not implemented: the two freed RAMB18 could hold `tsf_r` (the ingress timestamp ring) with a read-ahead address, saving at most its 44 LUTRAM sites. Its debug output would lag one cycle after a push into an empty ring. The tile is left to the firmware block-RAM ledger instead.
- The saving is below the plan's range. The cumulative ledger tables keep the 500-LUT planning figure until the week-4 re-measure.
- Gate record: not re-recorded (D7). The gate reports "re-baseline recommended" for FF and RAMB18; that is M9's step.
- The submodule branch must be pushed before the parent; until then hosted CI cannot fetch `18dd997b`.
- `syn/yosys/rom_digests.tsv` keeps a row for the intermediate pins `8b8d0beb` and `861e8f80`; the generator retains rows and the digest is the shipped one.

## 10. Receipts (scratch; not in the output directory)

| File | Bytes | sha256 (first 16) |
|---|---:|---|
| `640m2-a586/meas-base/ax7101/gateware/baseline_hierarchy.rpt` | 46405 | `03c7fdc6705a8563` |
| `640m2-a586/meas-base/ax7101/gateware/baseline_cells.tsv` | 8301796 | `44dab163382b8444` |
| `640m2-a586/meas-base/ax7101/gateware/baseline_utilization.rpt` | 13319 | `971d7d2bafd532fd` |
| `640m7-a587/meas-cand/ax7101/gateware/baseline_utilization.rpt` | 13319 | `523fb281211b4686` |
| `640m7-a587/meas-cand/ax7101/gateware/baseline_cells.tsv` | 8142121 | `fad96741d7ca7388` |
| `640m7-a587/meas-cand3/ax7101/gateware/baseline_utilization.rpt` | 13319 | `565dd46cd929b387` |
| `640m7-a587/meas-cand3/ax7101/gateware/baseline_hierarchy.rpt` | 46405 | `dca8a9fbe8133ee9` |
| `640m7-a587/meas-cand3/ax7101/gateware/baseline_cells.tsv` | 8185293 | `5dcc1453fc99a56f` |
| `640m7-a587/meas-cand3/ax7101/gateware/baseline_timing.rpt` | 1250444 | `9f650e750a76bf74` |
| `640m7-a587/meas-cand3/ax7101/gateware/alinx_ax7101_route_status.rpt` | 651 | `82bf1486d54b0a43` |
| `640m7-a587/gate-route-final.log` | 1247 | `768d4e71b4ebba27` |
| `640m7-a587/gate-route1.log` | 1198 | `26cb16f82cec9421` |
| `640m7-a587/sweep/shard0.out` | 1993 | `d4e3b08730448b7f` |
| `640m7-a587/sweep/shard1.out` | 246 | `a8a145e5b5baf42d` |
| `640m7-a587/sweep/physical.out` | 249 | `10c4c1f8c55b8e89` |
| `640m7-a587/sweep/tsn.log` | 9711 | `bbc65e4f6e288fc3` |
| `640m7-a587/gates/gp_tb.log` | 27089 | `f7905047c10cc666` |
| `640m7-a587/yosys/out.log` | 6182 | `4886c0edff6cff8b` |
| `640m7-a587/session/xvlog.log` | 721 | `496c392d2c4592de` |
| `640m7-a587/gates/builder.log` | 102794 | `e416fd516d423d38` |
| `640m7-a587/ooc/v-base/out/opt_hier.rpt` | 3057 | `223ade4b775019bb` |
| `640m7-a587/ooc/v5-final/out/opt_hier.rpt` | 2805 | `55540fb3f12af1ab` |
| `640m7-a587/session/gp/syn/ooc/work/engine_util.rpt` | 9168 | `f262097515f96efd` |
| `640m7-a587/tables-mutants2.log` | 1071 | `0bf38149e17b5251` |
| `640m7-a587/sweep/logs0/gptp_tables.log` | 3440 | `fa6b85807068b0ee` |

## Round 2

Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6100980189
It answers R592-1 (NEGATIVE, one MINOR: F1) and R593-1 (POSITIVE).
Starting heads: parent `9d42762c` (PR #713), donor `18dd997b` (FPGA-gPTP #78).
Final heads: parent `2cc2ba0b8b08010df5ee12c1fc228851fa9a8444`, donor `18dd997b2459699e41e5ce9bceca1181e41fa5fe` (unchanged).
New commits only; no rebase, amend or merge commit.

Session note: the first round-2 session was cut by an external usage limit at 21:06 after it committed `84910cb4`. Its mutation campaign was cancelled (signal 15, no verdict), and every result below was re-run in this session.

### R2.1 Item 4: #621 merge state

| Checked | origin/dev | PR #707 (#621) | donor main | FPGA-gPTP #77 | Result |
|---|---|---|---|---|---|
| start, 21:35 | `f88df731` | open, head `83239549` not in dev | `5dce647a` | open, head `7dda9c3b` not in main | not applicable |
| finish, 2026-10-11 02:36 | `ac2c5e77` | open, head `f5d0fb0e` not in dev | `5dce647a` | open, head `7dda9c3b` not in main | not applicable |

No merge was made, so the round-1 route figures stand as measured: they were measured at `9d42762c` (route #2 at `49e1ce48`, whose RTL equals it).
`9d42762c..2cc2ba0b` changes no compiled RTL; see the proof in R2.5.

### R2.2 Commits

| Commit | Items |
|---|---|
| `84910cb4` | 1 (F1 fill, named depth coverage, write-index control, per-table claim); 2 (F4 decode check, S-01, S-02) |
| `d46d386f` | 3 (F2 = R-02 comments; F3 = R-01 plan sentence) |
| `270fcbf5` | the suite Makefile's description of its controls |
| `2cc2ba0b` | the `TESTING.md` suite row |

F5 is a label in this hand-off (section 4) and in the round-1 REVIEW READY comment, which is not edited. Corrected text: "40/40 donor mutants (engine 33, gaskets 4, tsngen 3)". The split was counted from round 1's own donor `make tb` log: 33, 4 and 3 "mutant caught" lines in the engine, gaskets and tsngen campaigns.

### R2.3 Changes (file:line at `2cc2ba0b`)

Item 1, R592-1-F1:
- `tb/verilator/gptp_tables/gptp_tables_wrap.sv:171-189` (`result_slow`): a test-only slow engine. While `res_slow_i` is high, the result face's valid (to the engine) and ready (to the queue) are both forced low, so nothing transfers on either side and results wait in the queue. No result is fabricated: each is the queue's own, offered later.
- `sim_main.cpp:121`: a 3,000,000-cycle slow phase after the stall phase. `:424` drives it. `:432-443` (`slow_engine`) holds the face off for 500-20,000 cycles, then frees it for 200-3,000.
- `sim_main.cpp:535`: named coverage `results coverage: two or more results outstanding` (`res_maxn_o >= 2`). `gptp_tables_wrap.sv:111,492-495`: a printed count of results written while one waits.
- `mutants.py:140`: control `results_write_index`, R592-1's form (`res_ns_r[res_tail_w]` -> `res_ns_r[res_head_r]`), which must fail `results lockstep`.
- The claim is narrowed per table at `sim_main.cpp:10-24` and in the README table at `README.md:26-32`. Each table is written, read and reset in traffic at every index its use reaches. How full each gets is stated with the reason it gets no fuller: `rx_fifo` full; `tx_fifo` 27 of 256 beats; ledger 3 of 8; results 3 of 8 in the slow phase only; timer slots 0-5 of 8.

Item 2:
- R592-1-F4: `gptp_tables_wrap.sv:191-197` (`decode_force`) forces the transmit FIFO's lane count. `sim_main.cpp:110,445-462` (`decode_check`) drives each count 0 to 8 with the plane in reset and requires `tx_tkeep_o` = lanes 0 to count-1 (the old gearbox's mask; count 0 is a never-written word). Checks at `:513` (`tx_fifo decode`) and `:522` (coverage 0x1FF). `mutants.py:88`: control `tx_fifo_decode_odd_counts`.
- `waivers.vlt:9-11`, listed first in `Makefile:28`: the forces read as a second driver to Verilator. The `MULTIDRIVEN` waiver is scoped to `KL_gptp_shadow.sv` and to the three forced nets, not to the rule.
- R593-1-S-01: `README.md:56-60` states the tag column is one-valued for every reachable entry. `gptp_tables_wrap.sv:106,484` collect the tag values compared as a set, and the run prints `tags 0x2`.
- R593-1-S-02: `README.md:61-67` notes the post-reset wedge (#714). It states that coverage is graded over the whole run, and that per-segment coverage follows the fix of #714.

Item 3 (the reviewers' exact texts):
- R592-1-F2 = R593-1-R-02: `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:238-242,258-261,878-880`, with R592-1-F2's three replacement texts.
- R592-1-F3 = R593-1-R-01: `docs/design/MARK_II_AREA_PLAN.md:690-691`, R592-1-F3's text, one sentence per line as the page is written.

Doc follow-up: `tb/verilator/gptp_tables/Makefile:57-61` and `docs/testing/TESTING.md:601` name the slow phase, the decode check and the two added controls.

### R2.4 Tests and the planted defect each catches

`make -C tb/verilator/gptp_tables` at `270fcbf5`: 24/24 checks over 32,100,038 cycles, then 17/17 controls, each caught by its own named check, rc 0 (8 min 17 s at host load about 110; the sweep allows 1,800 s).
The sweep's reader (`scripts/suite_tally.py --verdict`) reads that log as 24 checks, 0 failures.
Coverage lines: `tx_fifo decode: counts 0x1ff driven, 0 decoded wrong`; `ledger: ... tags 0x2, 3 deep`; `results: 11377 compared, heads 0xff, 3 deep, 110 written behind a waiting result`.

The two controls added this round:

| Control | Planted defect | Caught by |
|---|---|---|
| `results_write_index` | the result queue's timestamp written at the head, not the tail | `results lockstep` |
| `tx_fifo_decode_odd_counts` | odd lane counts decode one lane short | `tx_fifo decode` |

The other 15 are unchanged and were each caught again by their own check.

Supplementary, scratch, not committed (`slow_probe.py`, private copies, at `2cc2ba0b`):

| Variant | Results depth | Outcome |
|---|---:|---|
| slow phase replaced by mixed traffic of the same length | 1 | 23/24: only `results coverage: two or more results outstanding` fails |
| the same, plus `results_write_index` | 1 | 23/24: the same single failure; `results lockstep` stays clean |

So the new coverage check can fail, and the slow phase is what exposes the write-index defect, as R592-1 found.
Per phase (the earlier session's boundary print of this stimulus; same totals as the committed run): the results queue is 1 deep through the stall phase and 3 after the slow phase. Results keep being compared after both warm resets (5,497 -> 9,690 and 9,690 -> 11,377), so at this seed the plane does not reach #714.

### R2.5 Gates (round 2)

Static: the 76 commands of section 7 other than the four Verilator ones ran from the lane root at `2cc2ba0b`, each with its own log and status file: all rc 0.

| Gate | Command | Head | Result |
|---|---|---|---|
| lint | `env PATH=$VERILATOR_DIR:$PATH $PY312 scripts/lint_rtl.py --check --self-test` | `2cc2ba0b` | rc 0, 90 violations against a ratchet of 90 |
| gp_contract | `env PATH=$VERILATOR_DIR:$PATH make -C gptp-processor contract` | `2cc2ba0b` | rc 0 |
| gp_lint | `env PATH=$VERILATOR_DIR:$PATH make -C gptp-processor lint` | `2cc2ba0b` | rc 0 |
| gp_docs | `env PATH=$VERILATOR_DIR:$PATH make -C gptp-processor docs` | `2cc2ba0b` | rc 0 |
| gptp_tables | `make -C tb/verilator/gptp_tables` | `270fcbf5` | rc 0: 24/24, 17/17 controls |
| gptp_shadow | `make -C tb/verilator/gptp_shadow` | `2cc2ba0b` | rc 0: 309/309, 9/9 controls (second attempt; see below) |
| gptp_txts | `MILAN_LITEX_PYTHON=$LITEX_PYTHON make -C tb/verilator/gptp_txts` | `2cc2ba0b` | rc 0: 85/85, 6/6 controls |
| gptp_plane | `make -C tb/verilator/gptp_plane` | `2cc2ba0b` | rc 0: 29/29 |
| xvlog | `python3 scripts/xvlog_gate.py --check` and `--selftest`, under the host Vivado lock | `2cc2ba0b` | rc 0 / rc 0: 0 findings (81 files under `hdl/`, 52 under the pinned processors) |
| make 4.3 | `MAKEFLAGS=w make -C tb/verilator/gptp_tables print-inputs`, and `-n mutants` | `270fcbf5` tree | rc 0 / rc 0 |

`270fcbf5..2cc2ba0b` changes only `docs/testing/TESTING.md`.
The first `gptp_shadow` attempt returned rc 2 before reaching the suite. Its mutant-lifecycle self-test (`test_mutant_lifecycle.py`, case `accept-git-stderr`) hit its 12-second subprocess wait, at host load about 110 with the campaign and the static gates running beside it. Run alone it passed; nothing it exercises changed this round.

Comment-only proof: `verilator -E -P` of `KL_gptp_shadow.sv` at `9d42762c` and at `2cc2ba0b` gives byte-identical output (25,863 bytes, sha256 `77feef0eb388fbbf...`).
No other file under `hdl/` and no gitlink changed in `9d42762c..2cc2ba0b`.
Not re-run, for that reason: the full sweep, `milan_dp`, `milan_dp_gptp`, `tsn_fuzz`, Yosys portability, the builder and the donor's `make tb`. Round 1 ran them at heads whose compiled RTL equals this head (section 7). The route is not repeated (D7).

### R2.6 Finish

All four round-2 items are done, and every gate above returned rc 0 at the head named.
The xvlog gate waited about five hours for the shared Vivado lock (queued 21:42, acquired 02:33).
#621 had not merged at finish, so item 4 did not apply and no merge commit was made.
Both heads at finish: parent `2cc2ba0b8b08010df5ee12c1fc228851fa9a8444`, donor `18dd997b2459699e41e5ce9bceca1181e41fa5fe`. Neither is pushed by this round.

### R2.7 Receipts (scratch; not in the output directory)

| File | Bytes | sha256 (first 16) |
|---|---:|---|
| `640m7-a587/r2/camp/mutants.log` | 8012 | `bfbe0e6229451dc6` |
| `640m7-a587/r2/suites2/gptp_shadow.log` | 21992 | `960132652d823c83` |
| `640m7-a587/r2/suites/gptp_shadow.log` (first attempt) | 3102 | `ed1cf37c3fd48276` |
| `640m7-a587/r2/suites/gptp_txts.log` | 9499 | `c11c865ed9bf3e09` |
| `640m7-a587/r2/suites/gptp_plane.log` | 1594 | `6307139af3908b23` |
| `640m7-a587/r2/probe/probe.log` | 450 | `8eeb32badea73f87` |
| `640m7-a587/r2/logs/segments.log` | 3193 | `5b4431cee8ba40e7` |
| `640m7-a587/r2/ppcmp/old.pp`, `new.pp` | 25863 each | `77feef0eb388fbbf` both |
| `640m7-a587/r2/gates/final_vl/lint.log` | 14888 | `4384e935dd6dc19c` |
| `640m7-a587/r2/xvlog/xvlog.log` | 721 | `496c392d2c4592de` |
| `640m7-a587/r2/xvlog/xvlog-self.log` | 170 | `ed6b967261542515` |

## Round 3

Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6104116064
It answers R593-2 (NEGATIVE, one MINOR: F1; R-01; S-01) and R592-2 (POSITIVE; RES1; S1 optional).
Starting heads: parent `2cc2ba0b` (PR #713), donor `18dd997b` (FPGA-gPTP #78).
New commits only; no rebase or amend.

### R3.1 #621 merge state

| Checked | origin/dev | PR #707 (#621) | FPGA-gPTP #77 | Result |
|---|---|---|---|---|
| start, 2026-10-11 03:17 | `ac2c5e77` | open, head `2cf985f3`, not merged | open, head `7dda9c3b`, not merged | not applicable |
| finish, 2026-10-11 04:15 | `ac2c5e77` | open, head `2cf985f3`, not merged | open, head `7dda9c3b`, not merged | not applicable |

No merge was made. The route figures stand as measured at `9d42762c` (route #2 at `49e1ce48`, whose RTL equals it).
`2cc2ba0b..354f7818` changes no file under `hdl/` and no gitlink (`git diff 2cc2ba0b..354f7818 -- hdl gptp-processor protocol-processor third_party external` is empty).

### R3.2 Commits

| Commit | Items |
|---|---|
| `a8a1c117` | 1 (value census, one named check per column, declaration list, README table, stuck-column and list controls); 2 (S-01) |
| `a9eab29a` | 1 (the `TESTING.md` suite row) |
| `70c697bf` | 1 (the table generator moved to `scripts/`; see R3.6) |
| `354f7818` | the README's `make` line names the table check |

Item 3 is PR-BODY.md only: R593-2-R-01 (`git switch --detach origin/640-m7`) and R592-2-RES1 ("Marked ready for review; merge waits for both reviews to be positive."), each with the reviewer's exact text.
R592-2-S1 is optional and not taken: the README states the ledger reaches 3 of 8 entries, and filling it would need a new directed phase.

### R3.3 Changes (file:line at `354f7818`)

Item 1, R593-2-F1, ruled for every converted table:
- `tb/verilator/gptp_tables/gptp_tables_wrap.sv:117-135`: census outputs, one per column, and one compare strobe per table.
- `gptp_tables_wrap.sv:466-495`: each column as the plane gives it to its consumer, under its lockstep's compare gate. Tap FIFO lane while the reference offers a beat (the lockstep's data gate). Transmit FIFO lane count while a beat is offered (the lockstep compares every cycle, but a consumer takes the count only from an offered beat). Ledger type, sequence and tag at the head port while the ledger holds an entry. The result face's five columns while a result is offered. The swept slot's deadline while it is armed, rebuilt as `delta_w + ms_now_r`.
- `tb/verilator/gptp_tables/sim_main.cpp:121-141`: `Column` (the distinct values seen) and `Declared` (one list row).
- `sim_main.cpp:206-216`: the 11 censused columns. `:239` reads them before each active edge, the edge the wrapper's counters sample on (`census()`, `:261`).
- `sim_main.cpp:612-623`: the grading. `values: the declaration list is read and well formed`; one `<table> values: <column>` check per column (`grade_column`, `:628`); `values: declarations that name no censused column`. A column passes when it held two or more values and is not declared, or exactly its declared value.
- `sim_main.cpp:655`: the list reader. `#` lines are comments; the header must be the five field names; a value must be `0x` hex.
- `tb/verilator/gptp_tables/one_valued.tsv:13-16`: the list: `ledger` `tag` 0x1 (covered by none), `results` `ok` 0x1 (`gptp_shadow`), `results` `gen` 0x1 (none, no consumer past the engine's masked claim compare). Each row carries its reason.
- `scripts/gen_one_valued_table.py`: writes the README's table between `<!-- one-valued-columns:start -->` and `:end`; `--check` changes nothing and exits 1 if the table is stale.
- `tb/verilator/gptp_tables/Makefile:49,53,57,70,79`: the list is passed to the harness and named in `print-inputs`; `limits` runs the generator's `--check`; `all` is `limits mutants`.
- `tb/verilator/gptp_tables/README.md:55-74`: the limits section, with the generated table. `:83-93`: the new controls.
- `tb/verilator/gptp_tables/mutants.py:53-68`: list path and check names. `:174-214`: nine controls (R3.4).
- The round-2 tag set (`led_tags_o` and the `tags 0x2` print) is removed: the census line for the same column replaces it.

`ok` and `gen` are declared as R593-2 describes, not reached. A generation other than 1 needs a barrier. A barrier closes the departure fence, and in this bench the lane ready does not wait for valid, which is the path of the open #714.

Item 2, R593-2-S-01: `tx_fifo coverage: decode driven with counts 0 to 8` is dropped. `sim_main.cpp:530` keeps the enables the plane presented for each count, and `:567` prints them. `tx_fifo decode` and its control are unchanged.

Doc: `docs/testing/TESTING.md:601`, the suite row.

### R3.4 Tests and the planted defect each catches

`make -C tb/verilator/gptp_tables` from a clean suite directory at `354f7818`: the table is current, then 36/36 checks over 32,100,038 cycles, then 26/26 controls, each caught by its own named check, rc 0 (7 min 51 s). The run at `70c697bf` gives byte-identical result and control lines.
`scripts/suite_tally.py` reads the log as 36 checks, 0 failures; `--verdict` returns 0.

Census lines at `354f7818`:

```text
rx_fifo values: lane: 8 distinct: 0x0 0x1 0x2 0x3 0x4 0x5 0x6 0x7
tx_fifo values: count: 3 distinct: 0x2 0x4 0x8
ledger values: type: 6 distinct: 0x0 0x2 0x3 0x8 0xa 0xb
ledger values: seq: 5168 distinct, 0x0 to 0xff05
ledger values: tag: 1 distinct: 0x1, declared 0x1
results values: ns: 10525 distinct, 0x4d24 to 0x2ff19706
results values: seq: 5167 distinct, 0x0 to 0xff05
results values: type: 6 distinct: 0x0 0x2 0x3 0x8 0xa 0xb
results values: ok: 1 distinct: 0x1, declared 0x1
results values: gen: 1 distinct: 0x1, declared 0x1
timer values: deadline: 1525 distinct, 0x4b0 to 0x34ec
```

The decode line: `tx_fifo decode: counts 0 to 8 presented enables 00 01 03 07 0f 1f 3f 7f ff, 0 decoded wrong`.

The nine controls added this round:

| Control | Planted defect | Caught by |
|---|---|---|
| `rx_fifo_lane_stuck` | the tap FIFO's lane field written as 7 | `rx_fifo values: lane` |
| `tx_fifo_count_stuck` | the gearbox count written as 8 | `tx_fifo values: count` |
| `ledger_type_stuck` | the ledger's type written as 0 | `ledger values: type` |
| `results_seq_stuck` | the result's sequence written as 0 | `results values: seq` |
| `timer_deadline_stuck` | every deadline written as 5,000 ms | `timer values: deadline` |
| `declaration_missing` | the tag row made a comment: the real, unchanged tag column is one-valued and undeclared | `ledger values: tag` |
| `declaration_wrong_value` | the tag declared as 0x0 | `ledger values: tag` |
| `declaration_many_valued` | the ledger's type declared one-valued (0x2) | `ledger values: type` |
| `declaration_stray` | the `gen` row renamed `generation` | `values: declarations that name no censused column` |

`declaration_missing` is the R593-2 class directly: the RTL is untouched, every lockstep stays clean, and only the census sees the undeclared one-valued column.
The other 17 controls are unchanged and were each caught again by their own check.

### R3.5 The declared columns, probed (scratch, private copies, not committed)

| Probe | `gptp_tables` (at `70c697bf`) | `gptp_shadow` (at `2cc2ba0b`; its inputs are unchanged since) |
|---|---|---|
| none | 36/36 | 309/309 |
| `res_ok_r` written as 1 | 36/36, `results values: ok: 1 distinct: 0x1, declared 0x1` | 305/309: `echo: the plane is sealed`, `phc: every capture at a non-nominal step is an explicit loss`, `phc: not one of them was published as a measurement` (twice) |
| `res_gen_r` written as 1 | 36/36, `results values: gen: 1 distinct: 0x1, declared 0x1` | 309/309 |

So the `ok` row's "covered by `gptp_shadow`" and the `gen` row's "none" are measured here. R593-2 found the same, and also `gen` stuck at 1 surviving `gptp_txts` 85/85; `gptp_txts` was not re-probed this round.
The `gen` reason rests on `KL_gptp_engine.sv:513-519` (the generation at event bits 27:24) and `gen_gptp_ucode.py:370-376` (above `TXQ_MASK_C`). The only consumer of `txts_gen_o` in `hdl/` is the engine port.

### R3.6 Gates (round 3)

Static: the 78 commands of `r2/gates/list.tsv` (section 7's list, the route gates excluded) ran from the lane root at `354f7818`, each with its own log and status file: all rc 0. Lint: 90 violations against a ratchet of 90.

| Gate | Command | Head | Result |
|---|---|---|---|
| gptp_tables | `make -C tb/verilator/gptp_tables clean`, then `make -C tb/verilator/gptp_tables` | `354f7818` | rc 0: table current, 36/36, 26/26 controls |
| tally | `python3 scripts/suite_tally.py <dir holding gptp_tables.log>` and `--verdict` | `354f7818` log | rc 0: 36 checks, 0 failures / rc 0 |
| make 4.3 | `MAKEFLAGS=w make -C tb/verilator/gptp_tables print-inputs`, `-n all`, `limits` | `70c697bf` (the Makefile is unchanged since) | rc 0 / rc 0 / rc 0 |
| ci_scope_self | `$PY312 scripts/ci_scope.py --selftest` | `a9eab29a`, then `70c697bf`, then `354f7818` | rc 1, then rc 0, then rc 0 (in the 78) |

The first `ci_scope.py --selftest` failed one arm: `gate-read page README.md (named at tb/verilator/gptp_tables/one_valued.py:29) is relevant`. The generator was then under the suite directory, and the selftest resolves its `README.md` literal to the top-level README.md, a documentation-only page. The page it really reads is the suite README under `tb/`, which is never documentation-only. `70c697bf` moves the generator to `scripts/`, which the scan does not cover, and its docstring states why. `ci_scope.py` is unchanged.
Observation for the manager, not acted on: the scan's suffix rule matches the top-level README.md for any literal that ends in `/README.md`, so no Python, Makefile or shell under `tb/` can name a suite README by any literal spelling. That would be its own issue.

Not re-run, because round 3 changes no RTL, no gitlink and no input of any other suite: the full sweep, `gptp_shadow`, `gptp_txts`, `gptp_plane`, `milan_dp`, `milan_dp_gptp`, `tsn_fuzz`, Yosys portability, xvlog, the builder and the donor's `make tb`. The route is not repeated (D7).
The mutation driver imports `tb/verilator/gptp_shadow/private_inputs.py` and `scripts/owned_process.py`, both unchanged.

### R3.7 Finish

All three round-3 items are done, and every gate above returned rc 0 at the head named.
#621 had not merged at the start or the finish, so round 2's item 4 did not apply and no merge commit was made.
Both heads at finish: parent `354f781828d8b4d73037129f297b072320a10f9c`, donor `18dd997b2459699e41e5ce9bceca1181e41fa5fe` (unchanged). Neither is pushed by this round.
REVIEW READY posted: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6104542951

### R3.8 Receipts (scratch; not in the output directory)

| File | Bytes | sha256 (first 16) |
|---|---:|---|
| `640m7-a587/r3/final2/camp/suite.log` (`354f7818`) | 9684 | `478180ce725630cc` |
| `640m7-a587/r3/final/camp/suite.log` (`70c697bf`) | 9684 | `b67dc3161674f49d` |
| `640m7-a587/r3/camp/suite.log` (`a9eab29a`) | 4956 | `657019b7f4e0da2e` |
| `640m7-a587/r3/final/tally.out` | 149 | `9088556663d70c78` |
| `640m7-a587/r3/probe/gptp_shadow.baseline.log` | 2914 | `72f40693b53bbd5a` |
| `640m7-a587/r3/probe/gptp_shadow.results_ok_stuck1.log` | 3086 | `d1f7d0644d41e12a` |
| `640m7-a587/r3/probe/gptp_shadow.results_gen_stuck1.log` | 2663 | `07510e92e49bca1a` |
| `640m7-a587/r3/probe/tables_probe.log` | 271 | `d79e0118cae81492` |
| `640m7-a587/r3/probe/gptp_tables.results_ok_stuck1.log` | 1534 | `a0eaef6d8641c87b` |
| `640m7-a587/r3/probe/gptp_tables.results_gen_stuck1.log` | 1532 | `04bb91bb6a4f7d57` |
| `640m7-a587/r3/gates/full/ci_scope_self.log` (`a9eab29a`, rc 1) | 6982 | `5b244fb9bf5f9b8c` |
| `640m7-a587/r3/gates/ci_scope_fix.log` | 6877 | `1eb60568978729e2` |
| `640m7-a587/r3/final2/gates/lint.log` | 14888 | `4384e935dd6dc19c` |
| `640m7-a587/r3/final/make43/print-inputs.log` | 1113 | `6e5bab65938768f0` |
| `640m7-a587/r3/final/make43/n-all.log` | 1587 | `83a09749af05bb89` |
| `640m7-a587/r3/final/make43/limits.log` | 253 | `895e6a6cc7671084` |

## Round 4 initial STOP record

**STOP.** The incoming donor causes two mandatory parent quality gates to fail.
The assignment says "Nothing else changes" and the task requires all affected
gates to return zero. No source fix, exception or budget increase was made.
The integration role needs to assign the donor corrections before this lane
can complete its parent merge and the remaining mutation campaign.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6161607579

### R4.1 Exact local state

| Artifact | State |
|---|---|
| Parent branch | `640-m7` |
| Parent HEAD | `354f781828d8b4d73037129f297b072320a10f9c`; unchanged from Round 3 |
| Parent MERGE_HEAD | `fa8209889411e8ca95757174c981f720dbcd95a2` |
| Resolved parent index tree | `3112cc103cfa17756ee0b5ede78aa0bdc9a46627` |
| Donor branch and HEAD | `640-m7`, `6b5a4282586a3851117674891d1955253e3de452`; clean |
| Donor merge parents | `18dd997b2459699e41e5ce9bceca1181e41fa5fe`, `61d486e9dfbff80739d7ce8cbac587b6f011648d` |
| Parent index gitlink | `6b5a4282586a3851117674891d1955253e3de452` |

The donor merge is committed. The parent merge is fully resolved and staged,
including generated records, but deliberately **not committed** because its
verification step did not pass. There are no unresolved index entries and no
unstaged tracked changes. Preserve the staged merge for the next authorized
step. Neither repository was pushed. No existing public comment was edited.

The starting parent and donor heads matched the assignment. Parent origin was
verified as `https://github.com/kebag-logic/milan-fpga.git`; original lane commit
`2ad1528b` has parent `e8454e2751d05b02ee8e5a571857589ab358ab86`.
The donor root and origin were verified before donor Git operations.
The donor merge contains `18dd997b`, `7dda9c3b` and `61d486e9`.

### R4.2 Changes and conflict resolutions

Line references below describe donor `6b5a4282` and the staged parent tree,
not the still-old parent HEAD. No M7 RTL, test implementation or declaration
was manually changed in this round.

| File:line or artifact | Resolution / generated change |
|---|---|
| `gptp-processor/docs/MANAGER.md:29`, `:72` | Sole donor conflict: keep the complete upstream constrained/unconstrained table and its PR #76 comparison, then retain the M7 table and its separate comparison. Identify the M7 measurement as the old unconstrained flow at `18dd997b`. All incoming ownership/risk prose remains. |
| `gptp-processor` gitlink | Resolve to the new donor merge, preserving both required ancestries. |
| `docs/design/GPTP_PLANE.md:32`; `docs/design/TIME_SYNC.md:115`; `docs/reference/SUBMODULES.md:24`; `docs/traceability/ieee8021as.md:53` | Keep dev's merged prose and update exact donor references to `6b5a4282`. |
| `docs/guides/gptp/MANAGER.md:23`; `HDL_DEVELOPER.md:33`; `SYSTEM_INTEGRATOR.md:61`; `TEST_DEVELOPER.md:30` | The other four pin-only conflicts retain dev prose and use the merged donor. |
| `docs/design/AREA_BUDGET.md:201`, `:206`, `:282` | Retain both M2 and M7 measurement notes; retain dev's current firmware-memory arithmetic and M7's freed-tile note. |
| `docs/design/MARK_II_AREA_PLAN.md:679`, `:710`, `:894` | Retain complete separate M2 and M7 sections. Preserve dev's current ledger arithmetic. Explicitly bind the M7 baseline comparison to historical dev `e8454e27`, because #696 replaced the live resource record. |
| `docs/diagrams/submodule_boundaries.drawio:1`, `.svg:1`, `.png`; `docs/diagrams/timesync_chain.drawio:1`, `.svg:1`, `.png`; `docs/diagrams/PNG_MANIFEST.json` | Regenerate both diagrams through their generators, retaining the incoming six-submodule inventory and new pin. Both PNGs were visually checked. Manifest retains unrelated dev entries. |
| `syn/yosys/rom_digests.tsv:32` | Generator appends the new donor row. The default image digest is `a435fba6167238268fa9074dd4645dd03380e56ff1eeea273fd3fc2fcecab9fd`, matching the #621 row at `7dda9c3b`; older rows are retained by the generator. |

The parent merge also imports dev's upstream changes without new lane edits.
The `third_party/lwSRP` and `third_party/tsn-c-stack` checkouts were initialized
at the incoming pins. All six documented gitlinks pass the consistency gate.
The M7 shadow/ledger RTL and table suite inputs equal the starting lane.
Against donor `61d486e9`, the donor merge differs only in the existing timer
RAM conversion and the retained M7 measurement subsection.

Generated-record commands, run from the parent root:

```sh
python3 docs/diagrams/submodule_boundaries.gen.py
python3 docs/diagrams/timesync_chain.gen.py
bash syn/yosys/ooc.sh --record-rom-digests
```

Each returned zero. This ROM-content record is separate from the resource
acceptance record, which was not re-recorded.

### R4.3 STOP evidence

| Gate | Result | Exact imported source |
|---|---|---|
| `python3 scripts/check_py_idiom.py` | rc 1: long function 10 > 9; undocumented public function 1 > 0 | `gptp-processor/syn/ooc/check_ooc_clock.py:269`: `selftest` is 120 lines; `:370`: nested `findings` has no docstring |
| `python3 scripts/check_cpp_idiom.py` | rc 1: multi-declarator declaration 4 > 0 | `gptp-processor/tb/verilator/parser/sim_main.cpp:275`, `:1343`, `:1421`, `:1491` |

Both files are byte-identical to incoming donor `61d486e9`; these are not
merge-resolution edits. The parser source at dev's donor `7dda9c3b` has zero
multi-declarator findings under the same checker, versus four at `61d486e9`.
The OOC clock checker did not exist at `7dda9c3b`.
The exact sites and hashes are in `r4/stop-provenance.log`.

An additional inherited documentation mismatch remains:
`gptp-processor/docs/MANAGER.md:103` says 1,008 real ROM words and `:111` says
`FUTO@13`. The merged generator reports 1,016 real words and `FUTO@249`.
The paragraph is unchanged from incoming main. It was recorded here rather
than silently changed under the merge-only assignment. The donor docs gate
passes but does not detect this numerical mismatch.

### R4.4 Gate table and defects checked

Environment: pinned Verilator 5.050, CPython 3.12.3 and GNU make 4.3 with
`MAKEFLAGS=w`. Simulation builds used `make -j8`, `VERILATOR_JOBS=2`; a scratch
launcher caps donor hard-coded build parallelism at two. At most two builds
ran concurrently. No Vivado run or full suite sweep ran this round. Observed
service memory remained below 9 GB.

The following evidence applies to the staged source tree or committed donor
identified above. Successful commands are plain shell without a launcher
prefix. Receipt names refer to `r4/` in scratch.

| Command / receipt | rc / result | Defect or regression checked |
|---|---|---|
| `make -j8 -C tb/verilator/gptp_tables run limits` / `gptp-tables-run` | 0; 36/36 | Five storage locksteps, FIFO depth/read timing, head indices, all 11 consumer-column censuses and declaration consistency. All RX lanes; results reach depth 2 with 111 writes behind a waiting result; no lockstep failure. |
| `python3 scripts/gen_one_valued_table.py --check` / `one-valued` | 0 | Stale README declaration table. |
| `make -C tb/verilator/gptp_tables print-inputs`; `make -C tb/verilator/gptp_tables limits` / `make43-inputs`, `make43-limits` | 0 each, GNU make 4.3 and `MAKEFLAGS=w` | Input manifest and README checks continue to work with directory chatter. No Makefile was edited. |
| `make -j8 -C tb/verilator/gptp_plane run` / `gptp-plane-run` | 0; 29/29 | Integrated publication, time-validity and PHC behavior. No fresh planted arm in this command. |
| `make -j8 -C tb/verilator/gptp_plane phc-step` / `gptp-phc-step` | 0; clean 62/62, campaign 8/8 | Stale rate window, crossing exchange, failure to rearm, absent liveness and incorrect credit on step. Two passing controls plus six defect arms; the two liveness arms are identical text, hence five distinct defects. |
| `make -j8 -C tb/verilator/gptp_shadow run` / `gptp-shadow-run` | 0; 309/309 | Shadow integration regressions. Its separate mutation campaign was not repeated. |
| `python3 scripts/ci_scope.py --selftest` / `ci-scope` | 0 | Incorrect docs/RTL classification, stale-base scope, lost history result and hosted/replay disagreement. |
| `python3 -I scripts/act_ci.py --selftest` / `act-self` | 0, inside disposable container only | Wrong pins/base, changed trust manifest, unsafe runner inputs, failed cleanup and replay boundary faults. No candidate host orchestration. |
| `python3 scripts/ci_events.py --check` / `ci-events` | 0; 2,174 contract items | Workflow event/trigger contract drift. |
| `make -C gptp-processor contract lint docs` / `donor-static` | 0 | PHC contract and RTL lint; 9 diagram assets; 11 current/17 historical pages; 20 exact source anchors. Diagram/docs/source self-tests catch changed diagrams, stale documentation and incorrect source anchors (10/10/7 arms). |
| `python3 gptp-processor/syn/ooc/check_ooc_clock.py` and `--selftest` / `donor-clock`, `donor-clock-self` | 0 each; 30 arms | Missing/wrong/late clock, absent synthesis clock evidence, wrong clock source, unclocked registers and critical warnings. Its Python style still fails the parent gate. |
| Donor microCPU target, first leg of `make -j8 -C gptp-processor tb` / `donor-tb` | leg passes 768/768 | Instruction and state-port behavior. Aggregate command later returned 2; see below. |
| Donor parser target, same invocation / `donor-tb` | leg passes 337/337 and 8/8 mutants | Frame rejection, error on each byte, post-error writes and contamination of the next accepted frame. |
| Donor engine target, same invocation / `donor-tb` | leg passes 1,613/1,613 at each of three seeds and 33/33 mutants | Protocol/servo pairing, publication, timeout and transmit-result faults named in the donor campaign. |
| Donor gaskets target, same invocation / `donor-tb` | leg passes 81/81 and 4/4 mutants | Byte transport/gasket faults. |
| `make -j8 -C gptp-processor/tb/tsngen` / `donor-tsngen` | 0; 288/288 and 3/3 mutants | Zeroed received sequence ID, discarded grandmaster identity and transmit EOF one byte early. |
| `make -j8 -C gptp-processor/bench/arty test` / `donor-arty` | 0 | Simulated RX/TX tag transport; no board or bench access. |
| `python3 syn/ooc/pp_resource_gate.py check-baseline` / `resource-baseline` | 0; three endpoints | Malformed/inconsistent acceptance baseline, not a new area measurement. |
| `python3 scripts/check_doc_style.py` / `doc-style` | 0; 22 current documents | Documentation style regressions. |
| Python/C++ idiom gates / `py-idiom`, `cpp-idiom` | **1 each; STOP** | Findings listed above; no budget changed. |

The table stimulus now reports `ledger.tag`, `results.ok` and `results.gen`
as the same single declared value 1. The timer has 680 distinct deadlines.
Other counts differ from historical Round 3 because the upstream microcode
changed; the acceptance criterion is at least two queued results, not exactly
three. No declaration or acceptance criterion was changed to obtain the pass.

All six donor `tb` constituent targets passed, but the initial aggregate
`make tb` itself returned **2** when tsngen encountered missing PyYAML in the
initial interpreter. The failed leg and final Arty leg were then run to zero
in the prepared 3.12 environment. The four already-green legs were not repeated.
This is constituent-target evidence, not an aggregate rc-0 receipt.

The M7 mutation driver did **not** produce a Round 4 verdict. The supplied
3.12 build lacks the pidfd functions the driver requires. Native Python has
them, but correctly refuses the uncommitted dependency gitlink (rc 2).
The parent merge remains uncommitted due the real quality failures, so the
26-arm campaign remains outstanding. Historical Round 3 controls still appear
in that section, explicitly tied to its old head. The ordinary census and
README/declaration checks above did pass the merged tree.

Initial isolated-Python/absent-PyYAML and unresolved-gitlink probes were not
passing verdicts. The corrected CI self-test invocations passed; the two
remaining quality failures are source findings, not environment failures.

Additional parent static gates below ran on the resolved pin; all rows marked
zero have actual rc-0 receipts. Fixture self-tests were run where listed.

| Command | rc | Receipt |
|---|---:|---|
| `python3 scripts/docs_check.py` | 0 | `docs.log` |
| `env GIT_DIR=/dev/null python3 scripts/docs_check.py` | 0 | `docs-nogit.log` |
| `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | `gptp-docs.log` |
| `python3 scripts/check_gptp_docs.py --selftest` | 0 | `gptp-docs-self.log` |
| `python3 scripts/check_submodule_docs.py` | 0 | `submodule-docs.log` |
| `python3 scripts/check_submodule_docs.py --selftest` | 0 | `submodule-docs-self.log` |
| `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | `submodule-diagram.log` |
| `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | `submodule-diagram-self.log` |
| `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | `timesync-diagram.log` |
| `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | `timesync-diagram-self.log` |
| `python3 scripts/check_diagram_pngs.py` | 0 | `pngs.log` |
| `python3 scripts/check_diagram_pngs.py --selftest` | 0 | `pngs-self.log` |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `module-matrix.log` |
| `python3 scripts/check_doc_paths.py` | 0 | `doc-paths.log` |
| `python3 scripts/gen_toc.py --check` | 0 | `toc.log` |
| `python3 scripts/gen_toc.py --selftest` | 0 | `toc-self.log` |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | `toc-anchors.log` |
| `python3 scripts/check_feature_status.py` | 0 | `feature-status.log` |
| `python3 scripts/check_py_idiom.py` | 1 | `py-idiom.log` |
| `python3 scripts/check_cpp_idiom.py` | 1 | `cpp-idiom.log` |
| `python3 scripts/check_sv_idiom.py` | 0 | `sv-idiom.log` |
| `python3 scripts/check_sh_idiom.py` | 0 | `sh-idiom.log` |
| `python3 scripts/check_hygiene.py --check` | 0 | `hygiene.log` |
| `python3 scripts/measure_naming.py --check` | 0 | `naming.log` |
| `python3 scripts/measure_fail_fast.py --check` | 0 | `fail-fast.log` |
| `python3 scripts/measure_test_evidence.py --check` | 0 | `evidence.log` |
| `python3 scripts/check_port_contracts.py` | 0 | `ports.log` |
| `python3 scripts/check_rtl_source_lists.py` | 0 | `source-lists.log` |
| `python3 scripts/lint_rtl.py --check` | 0 | `lint.log` |

Pin checks cover six exact gitlinks and eight current gPTP pages. Diagram checks
cover decoded pixels and wrong-raster controls; the PNG campaign passes 28
controls. Module matrix: 77 modules, zero untested, seven controls. TOC: 1,501
self-test arms and 496 valid cross-page anchors. No quality ratchet was loosened.
The passing CI scripts/workflows and census declaration inputs were hashed;
all ten recorded inputs still match their passing invocations.

For the workflow self-test, the command above ran in a disposable container:
network disabled, source read-only, no credentials or Docker socket, all
capabilities dropped, no new privileges, 2 GB memory and four CPUs, with disk
scratch. Its CPython is 3.12.3. No hosted CI or full local replay was started
because the heads were not pushed and this is STOP evidence.

### R4.5 Primitive, resource and route applicability

Sections 5 and 6 retain the historical before/after census and M0s recipe
receipts. The timer mapping was 256 FF plus a read mux -> 5 RAM32M + 2 RAM32X1D;
the two FIFO conversions freed two RAMB18. The historical M0s route changed
LUT 50,267 -> 49,898; FF 54,413 -> 53,220; RAMB36/RAMB18 74/27 -> 74/25;
WNS +0.299 -> +0.122 ns; WHS +0.031 -> +0.019 ns. It passed the then-recorded
route gate, not the current merged tree's physical acceptance.

The donor imports `hdl/wire/KL_gptp_rx_parser.sv` error-state logic and changes
`hdl/ucode/gen_gptp_ucode.py` plus four images for #621. These can change
standalone engine and integrated plane resources/timing. The OOC scripts now
read the clock before synthesis (#70), unlike the old unconstrained snapshot.
Parent dev imports M5 CSR logic, M6 media contexts, M2 retained MAC/CSR storage,
packet counters and SoC/firmware inputs, which can change whole-image M0s
resources/timing. Therefore old numerical measurements do not qualify the
staged parent or new donor head. No measurement was rerun after this STOP;
no new area credit or acceptance re-record is claimed. D7 leaves acceptance
re-recording to M9. A later continuation must address applicability explicitly.

### R4.6 Receipts and next authorized step

Scratch receipts are under `$VALIDATION_STORAGE/640m7-a587/r4/`. They stay outside
the output directory. Sizes and complete SHA-256 digests follow. The output
contains Markdown only; no installed packages, toolchains, tree exports or
large log files were copied into it.

| Receipt | Bytes | SHA-256 |
|---|---:|---|
| `act-self.log` | 59168 | `6a28c53acbded43c63ca0ec57eb4fb5f58c1f0826a0a6d8a8bd539d364f6debe` |
| `ci-events.log` | 167 | `cbf7f2bb4fa19ca31b60e6e86d022a8f00176c252a015526d8ef299bd1933eb1` |
| `ci-scope.log` | 15329 | `be3ebff4df64fbd38d8a614ddb3be3ff889801c4531ac3a81747f7ae1185c010` |
| `cpp-idiom-list.log` | 220 | `913825091a6bf1f2d986ae5176ce56818e54f3bbc3c30f6193ac6a5cf896b1ad` |
| `cpp-idiom.log` | 133 | `a9d036222c8b7cabdfff022696286ce415728e909e3a87fb807055eb31a10e12` |
| `doc-paths.log` | 85 | `7033b54b2784b7b8d9f1fc7da5b907a49ef6b6572f7579790e4ec9d6f48572ed` |
| `doc-style.log` | 47 | `1491d3f6bec03b920cf58f5fb28e6abff4a9d433a758bc0fe5d2db77bf4f53cd` |
| `docs-nogit.log` | 196 | `08a0ebc92d5f7c34c1af5243f7bc58aa869502fbc0eaf6e6e873add0ac7c820d` |
| `docs.log` | 128 | `afd69244ae6e7091eb4b64694f7d41e43df44ce57725a896bb48a551fdfd2584` |
| `donor-arty.log` | 5041 | `192588704bf206c42b057e1eab8f3f9d34a303c80b38984a55d9375349fe3d84` |
| `donor-clock-self.log` | 41 | `99a0559caf79c40591b86d49bde93bcdd98a53230af48cbaa02cf09ee27ece09` |
| `donor-clock.log` | 68 | `95d7509d88fb0432367164d91a04052eea11195787c8cd4b986997967557c02f` |
| `donor-rom.log` | 296 | `096cd71d0b654495a5c9ddd97b0e91567dcfc8df9464ee9832d96ad511745e5c` |
| `donor-static.log` | 4270 | `9952220737bab66e7193481a4ea88053455f06c34f700226caba19a7e5fb7246` |
| `donor-tb.log` | 38731 | `59ba61deda6383547ee9322b5972f664e36651179d808943bb04a1eb3b59c5d5` |
| `donor-tsngen.log` | 1877 | `59c7abe36fba88cbbe46f805b37166199df9fbf88b67c23125a1e18c292f48ff` |
| `evidence.log` | 18788 | `99be30210e18d0af8473388a5625b5174bbb7dc01f0809a9618917c2a8ac89b7` |
| `fail-fast.log` | 5967 | `88736e013ea360ab7771ca768e0227032b26f748c1f24c20f1a260b788a67d8b` |
| `feature-status.log` | 29 | `802f5eeb2f0aa147169f3ddb9c64d4369ca92ab380455195403f2e8ae02490d0` |
| `final-state.log` | 680 | `c0c3443a4d8d07403ae7748f4642b4486115ef91fed17deff48bacad8d51d5b8` |
| `gen-submodule.log` | 134 | `d27511608a6f9eb40f2755a8c3a947dc700330b7ab3fde979b5c0349eaa5edc5` |
| `gen-timesync.log` | 72 | `2a83a8d01c4205742800386c03425154e1c3fc5e857dae69654e9c9efa850d48` |
| `gptp-docs-self.log` | 46 | `200332e4eddfd8a6338d8a4dbe27d2f513de92f951a1aa1f6b25882182bc290e` |
| `gptp-docs.log` | 66 | `7ca87a8501c54854805f1cf90d49b2a8ff6353a1049fd21cf0631569f5024e41` |
| `gptp-phc-step.log` | 1907 | `7cb6fb858cf4868ee1db86d9dadef61fcba88dc3027d22ffdb202c278aae0942` |
| `gptp-plane-run.log` | 11581 | `ee15abef4b13b00a6a2a6faf7f4a88803c2e6900801f7f9e3029f7b97bcdea2d` |
| `gptp-shadow-run.log` | 9102 | `2a60385b26f382392bdad5283cae390bf2fa66b3acde15bb6156aeaad906f5e4` |
| `gptp-tables-mutants.log` | 55 | `d0acbe5775c13cf9014378375919a3e8aedabd8ff4f802a8b944b7664c407c1f` |
| `gptp-tables-run.log` | 8146 | `73055e8f56514192a1c67ed9e2035cdfe822214fcc9d1d337aa2ff053a13e391` |
| `hygiene.log` | 2000 | `16c9e549e4e17018801eaa9d34610a7939b4f6c87fcc7fc51e8a6fc838afe660` |
| `lint.log` | 14186 | `f7765c8f0fb403026f5eba51c6e99b88abd23c1fba7a10b0b9ebd3fa9feec214` |
| `make43-inputs.log` | 1113 | `6e5bab65938768f013ed4195a68b2f8af5fd7a83dcfd7c03df85237a2abfe63b` |
| `make43-limits.log` | 253 | `895e6a6cc7671084b922d6b570d791d64857fd3c37e640e4aa5694f312ff1cdd` |
| `module-matrix.log` | 118 | `4e782e68ed5c09299d5d990702b634a2358aa1d5cbc2fd822374561e249c2687` |
| `naming.log` | 36490 | `8db123cd4a9ebdcc6a488529e53b67d91b48a7c2b4e8d577d9ea17ec0b724965` |
| `one-valued.log` | 43 | `b1818889beca5d5a8dea520e8fd1c0b9b2cb350cf97740418713fd9e2a3a12a8` |
| `pngs-self.log` | 59 | `918e8cc85a2a2b0d45eeb3f0c7b006824c81e2ed404a535eded095b09d875dc5` |
| `pngs.log` | 66 | `05e0fcfa26a97494e8983dcfca3ad89cdaf91e390acbfb9dbdfb6f614cba4e51` |
| `ports.log` | 421 | `cd9f24fbfd71df64a01d448c13e8aee85846692cbc781f4f45e8eecc7f950bf6` |
| `py-idiom-list.log` | 1273 | `2d4da88a541d22260d54235d509c16112e55ac812339b4d317bc683410221150` |
| `py-idiom.log` | 250 | `e67ee4daf8e2a54d14c8c6fc9fc59aa15887aee0e6047a4b4d88371d7556d1fc` |
| `resource-baseline.log` | 27 | `2114d909e60add091220b415987d4409a611d70c9e84f1bb9e0ae12d6a2f14a0` |
| `rom-digests.log` | 198 | `2b72feda1e2a99d4d8cb43a0ac258f1b894e26ade05b25c83c839c451087b342` |
| `sh-idiom.log` | 235 | `7ace602f03fa0e411862de119cff9d337583f1f2170d920dff65a0e0f39ee6d9` |
| `source-lists.log` | 153 | `ed979d7e26c3cd7a6f14364c11994089b77632424d04252613eeed458ebc8a95` |
| `static-summary.log` | 6946 | `e4276cbb350ba7b4b9bc9920d7fdb0771b26d9d7f0b39d874ae73eb33b442d2b` |
| `stop-provenance.log` | 1257 | `56f200227bfcf901fd339365e36ac64b89dba9420f9ee290b3185a3ae3097037` |
| `submodule-diagram-self.log` | 60 | `51bca8fb66fd6f0acc480e3364f74fd7a4874946b191468bfbe20ad159cca889` |
| `submodule-diagram.log` | 54 | `4f2d621c17d265a6e2851eaa978fe81af61cf6bbf152cce8ab90ba77b4f91e18` |
| `submodule-docs-self.log` | 66 | `54dbecff3ad17dc651e86c7b313ef57fa96baf89fb40f0fb90af4bbb8ddc802b` |
| `submodule-docs.log` | 47 | `c4bbf250ee33a3cc538cbbf1028e693c8acc058adc782d1f1feef249cd2faa0b` |
| `sv-idiom.log` | 218 | `aed2873a1909e4a41b3e6dee6dc5aaab993bbf1ef41f556062a5b377a6a8b167` |
| `timesync-diagram-self.log` | 61 | `7c7ad79fa685d29607abf71e3a99d98855fd7ffa1ba5fbf7de23bfb41a33c8fa` |
| `timesync-diagram.log` | 60 | `51058c96a481bf763246394b619601227bdec11b6b11ddcaa1d6f57593d2f1f4` |
| `toc-anchors.log` | 64 | `9d9e538fb10cc7787bf9f74abf5a385ad07c4336858a66a6b03ad7311245e459` |
| `toc-self.log` | 38 | `d7fd5f6ebcdd25e6cf93b623b0fba00cfa32d19c812ce34eb6b8d8b352ac9b32` |
| `toc.log` | 94 | `69f1c8a46304a5e42bd93366b34a8efb1e6aea995f10a25f83cedbdab720a5cf` |
| `gptp-default.hex` | 13312 | `a435fba6167238268fa9074dd4645dd03380e56ff1eeea273fd3fc2fcecab9fd` |

Generated raster receipts (files remain in the repository, not the output directory):

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `docs/diagrams/submodule_boundaries.png` | 438587 | `bf27abec86beff56d61dbfa74ac4e059998b37479d2db089bca900d09a89ff56` |
| `docs/diagrams/timesync_chain.png` | 314713 | `97ded3483620010b55f52e4a7eb2227c623d20e75e64cd4dd234f7e86352c79b` |

Required continuation: assign donor style corrections without raising ratchets,
resolve the stale ROM paragraph, then rerun the affected donor/parent gates.
When the merge step passes, commit the parent merge using the configured
identity and a one-line subject, run the 26-arm table campaign on that committed
gitlink, and obtain fresh independent review. Do not treat the staged tree as
an approved head or the old reviews as review of this merge. Publication and
any physical remeasurement require the task's next authorized step.

Public STOP receipt: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6162158855

## Round 4 continuation

Ruling: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6162175442

Starting parent `354f781828d8b4d73037129f297b072320a10f9c`, staged merge source
`fa8209889411e8ca95757174c981f720dbcd95a2`; starting donor
`6b5a4282586a3851117674891d1955253e3de452`, clean. Origin and original
`e8454e27` ancestry verified. Preserve the existing parent merge.

Authorized steps: split the donor clock self-test and document its nested
fixture evaluator; split four C++ declarations; correct the ROM budget and
FUTO location. Compare the 30 clock controls and 337 parser checks before
and after. Pass the parent Python/C++ gates without exceptions or budget
changes. Commit the donor correction and update the parent pin and generated
records, then commit the parent merge. Run the 26 table controls and all
parent gates recorded for Round 4.

No new physical measurement is required by this ruling. Every area/timing
number in sections 1, 5 and 6 belongs to its recorded historical revision.
The daily issue #640 measurement records the integrated effect the day after
the merge. No new physical acceptance is claimed.

Changes so far: `gptp-processor/syn/ooc/check_ooc_clock.py:269` separates
fixture definitions (`selftest_arms`, 95 lines) from execution (`selftest`,
30 lines at :366); `:376` documents `findings`. All 29 defect fixtures,
required findings and four clean fixtures compare equal, and production
function syntax trees match. The 30-control outputs also match.

`gptp-processor/tb/verilator/parser/sim_main.cpp:275`, `:1344`, `:1424`,
`:1496` split the four declarations with unchanged initializers. Its 337-check
output matches byte-for-byte (2,049 bytes, SHA-256
`f521be7f25439184b14991a9667aabeb05d84a3b98f27df2b6dbe2ea2e8e556c`).
`gptp-processor/docs/MANAGER.md:103`, `:105`, `:111`, `:113` now report
1,016/1,024 words (99.2%), eight free, SERVO in the prefix, FUTO@249 outside it.
The generator confirms those values and the unchanged default image digest.

Parent Python/C++ gates and their 54/75 self-tests pass without any budget
change. Donor contract/lint/docs pass. A first donor documentation invocation
caught one overlong sentence; the revised two sentences pass. The first
isolated workflow self-test could not find sudo in its container image; the
prepared CPython 3.12.3 image passes. Both attempts remain in scratch receipts.
CI scope and event-contract checks pass. All 35 parent static checks pass on
resolved tree `3a0b668761728b2e9fcc328f71f67f885ef3d11e`. The 36-check table
census and 29-check plane run pass. The original staged merge tree
`3112cc103cfa17756ee0b5ede78aa0bdc9a46627` is preserved except for the new
donor gitlink and its eight documentation pointers, generated diagrams and
ROM digest row (17 paths total).

Donor correction commit: `e4869fd0c42889b2ac806587cc5c78afb1c33461`.
Parent merge commit: `412e3f6c8c402bce63e94c291d2782b5579aaa1d`, parents
`354f781828d8b4d73037129f297b072320a10f9c` and
`fa8209889411e8ca95757174c981f720dbcd95a2`, tree
`3a0b668761728b2e9fcc328f71f67f885ef3d11e`.
Both repositories are clean. Neither was pushed. Existing commits were
preserved, with no rebase or amend.

The donor aggregate was deliberately interrupted after 415.9 seconds because
the full engine campaign would exceed the foreground command window. It has
no passing aggregate verdict. Its microCPU (768), parser (337 plus eight
mutants) and three engine simulation seeds (1,613 each) completed. All 33
engine mutation entries are being rerun in five disjoint batches of seven,
seven, seven, seven and five, each retaining the original positive control.
The driver source and verdict logic are unchanged. Remaining donor targets
will run separately. The PHC-step campaign passes all eight arms (62 clean checks); the shadow
run passes 309 checks. The 26 table controls all pass at the committed parent
in ranges 7/7/7/5, with no failed named checks. Remaining donor batches and
small constituent targets are still running.

Final heads, complete results and receipt hashes appear below. Progress notes in this section describe the sequence; the final results supersede their pending states.

### Continuation campaign scheduling

The per-command foreground window is shorter than the complete donor engine
campaign. The first aggregate was interrupted with no aggregate PASS claim.
The unmodified donor engine driver runs disjoint original index ranges
[0,7), [7,14), [14,21), [21,28), [28,33), each with its own original clean
control. Batch 0 passes eight checks (seven defects plus the clean control).
Driver SHA-256: `078d176b829cd21ed7f31339624a6b3d52db9fd113b68b7994a990217527e3d1`.

The table driver's committed-pin verification now accepts parent `412e3f6c8`.
It runs ranges [0,7), [7,14), [14,21), [21,26) under the same window. Its
input copier, simulator commands and named-failure verdict are unchanged.
Driver SHA-256: `c2e7cab57e000a73805190aa960d5277ef745c282ae9924220e91198a0c6594d`.
The native interpreter provides the pidfd support this driver requires.
Each batch uses no more than two compiler workers; no more than two simulation
builds run concurrently. All scratch and receipts stay on disk outside the tree.

The em-dash gate passes at the committed parent against dev `fa820988`,
including 339 planted controls. An attempted ROM check flag was refused as an
unknown top; the supported ROM-record command then passed and left the ledger
byte-identical to the committed record. This is not resource re-recording.

### Continuation parent static gate table

All rows below returned zero on tree `3a0b668761728b2e9fcc328f71f67f885ef3d11e`,
which is the committed parent merge tree. Logs and status files use the receipt
names below in `r4-resume/` under the existing scratch root.

| Command | rc | Receipt |
|---|---:|---|
| `python3 scripts/docs_check.py` | 0 | `docs.log` |
| `env GIT_DIR=/dev/null python3 scripts/docs_check.py` | 0 | `docs-nogit.log` |
| `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | `gptp-docs.log` |
| `python3 scripts/check_gptp_docs.py --selftest` | 0 | `gptp-docs-self.log` |
| `python3 scripts/check_submodule_docs.py` | 0 | `submodule-docs.log` |
| `python3 scripts/check_submodule_docs.py --selftest` | 0 | `submodule-docs-self.log` |
| `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | `submodule-diagram.log` |
| `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | `submodule-diagram-self.log` |
| `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | `timesync-diagram.log` |
| `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | `timesync-diagram-self.log` |
| `python3 scripts/check_diagram_pngs.py` | 0 | `pngs.log` |
| `python3 scripts/check_diagram_pngs.py --selftest` | 0 | `pngs-self.log` |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `module-matrix.log` |
| `python3 scripts/check_doc_paths.py` | 0 | `doc-paths.log` |
| `python3 scripts/gen_toc.py --check` | 0 | `toc.log` |
| `python3 scripts/gen_toc.py --selftest` | 0 | `toc-self.log` |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | `toc-anchors.log` |
| `python3 scripts/check_feature_status.py` | 0 | `feature-status.log` |
| `python3 scripts/check_py_idiom.py` | 0 | `py-idiom.log` |
| `python3 scripts/check_cpp_idiom.py` | 0 | `cpp-idiom.log` |
| `python3 scripts/check_sv_idiom.py` | 0 | `sv-idiom.log` |
| `python3 scripts/check_sh_idiom.py` | 0 | `sh-idiom.log` |
| `python3 scripts/check_hygiene.py --check` | 0 | `hygiene.log` |
| `python3 scripts/measure_naming.py --check` | 0 | `naming.log` |
| `python3 scripts/measure_fail_fast.py --check` | 0 | `fail-fast.log` |
| `python3 scripts/measure_test_evidence.py --check` | 0 | `evidence.log` |
| `python3 scripts/check_port_contracts.py` | 0 | `ports.log` |
| `python3 scripts/check_rtl_source_lists.py` | 0 | `source-lists.log` |
| `python3 scripts/lint_rtl.py --check` | 0 | `lint.log` |
| `python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 | `resource-baseline.log` |
| `python3 scripts/check_doc_style.py` | 0 | `doc-style.log` |
| `python3 scripts/gen_one_valued_table.py --check` | 0 | `one-valued.log` |
| `make -C tb/verilator/gptp_tables print-inputs` | 0 | `make43-inputs.log` |
| `make -C tb/verilator/gptp_tables limits` | 0 | `make43-limits.log` |
| `python3 syn/ooc/pp_resource_gate.py --selftest` | 0 | `resource-self.log` |

### Table campaign completion

At parent `412e3f6c8c402bce63e94c291d2782b5579aaa1d` and donor
`e4869fd0c42889b2ac806587cc5c78afb1c33461`, all four table batches returned zero:
7 controls in 122.7 s, 7 in 130.1 s, 7 in 122.7 s and 5 in 72.1 s.
Together they run every original index 0 through 25 exactly once. Every defect
failed the table's own named check. This is current-head evidence, replacing
the prior uncommitted-pin refusal, with no change to any test or declaration.
The clean run remains 36/36, including the eleven consumer-column censuses.

### Reproducing the bounded batches

Use the pinned build environment and disk-backed `TMPDIR`, with `MAKEFLAGS=w`
and `VERILATOR_JOBS=2`. These are runtime selections of the existing mutation
lists, not repository edits. From the parent root, the following command runs
one table batch; run it separately for `BATCH=0`, `1`, `2`, `3`. Use the native
interpreter with pidfd support. Each invocation returns the original driver's
exit status and verifies committed input bytes before creating private copies.

```sh
BATCH=0 python3 - <<'PYRUN'
import importlib.util
import os
from pathlib import Path
import sys

source = Path("tb/verilator/gptp_tables/mutants.py").resolve()
spec = importlib.util.spec_from_file_location("table_controls", source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert len(module.MUTATIONS) == 26
batch = int(os.environ["BATCH"])
assert 0 <= batch < 4
module.MUTATIONS = module.MUTATIONS[batch * 7:(batch + 1) * 7]
sys.exit(module.main())
PYRUN
```

For the donor's original 33 entries, run the same command separately with
`source = Path("gptp-processor/tb/verilator/engine/mutants.py").resolve()`,
expected length 33 and `0 <= batch < 5`, for batches 0 through 4. That driver
also runs its original positive control in each batch. The scratch launchers
add only source digests and index-range reporting. They are retained as
`r4-resume/table_chunk.py` and `r4-resume/donor_engine_chunk.py`; the final
audit checks every batch's digest, indices, entry names, verdict and exit code.
No mutation, assertion, acceptance criterion or source anchor was changed.

### Final continuation results

REVIEW READY at parent `412e3f6c8c402bce63e94c291d2782b5579aaa1d` and donor
`e4869fd0c42889b2ac806587cc5c78afb1c33461`. The parent is the authorized merge
of dev `fa820988` into `354f7818`. Its tree equals the gated resolved tree.
The donor correction is on top of the preserved `6b5a4282` merge. No existing
commit was rewritten. Both repositories are clean, with no push or PR edit.

The 35-row static gate table above is all rc 0. The following simulation and
contract results complete the continuation; all completed constituent targets
pass. The interrupted `make tb` aggregate is not represented as rc 0.

| Check | Result | Defect sensitivity / limitation |
|---|---|---|
| Clock checker before/after | 30/30 each; identical output, fixtures and required findings | Missing, wrong or late clock; wrong port/period; absent synthesis evidence; unclocked registers; critical warnings. Production function syntax trees unchanged. |
| Parser before/after | 337/337 each; identical complete simulator output | Error flags on first, interior and final bytes, writes after rejection and stale words in the next accepted frame. All eight original parser mutants caught. |
| Python/C++ idiom gates and controls | rc 0; 54/54 and 75/75 self-tests | Detect the imported long/undocumented function and four multi-declarator declarations. Long-function debt returns to 9; undocumented and multi-declarator findings return to zero. No budget or exception changed. |
| Table clean run | 36/36 | Five storage locksteps, explicit decode and all eleven column censuses. Result queue reaches depth two and 111 writes behind a waiting result. |
| Table mutation batches | 26/26, all batch rc 0 | Wrong depths/latencies/indices, wrong result write index, odd-count decode, undeclared stuck columns and incorrect declaration lists. Each fails its own named check. |
| Plane run | 29/29 | Publication, PHC and wire flags; positive regression, not a new planted campaign. |
| PHC-step campaign | 62 clean checks; 8/8 arms, rc 0 | Two passing controls and six defect arms (five distinct defects): stale rate window, crossed exchange, absent rearm/liveness and unearned credit. |
| Shadow run | 309/309, rc 0 | Integrated shadow regression; its separate mutation campaign was not repeated. |
| Donor microCPU | 768/768, completed constituent | Instruction and state-port regression; no new planted campaign in this target. |
| Donor engine simulations | 1,613/1,613 at each of three seeds | Protocol and servo behavior, high request/Sync counters. Completed before the aggregate interruption. |
| Donor engine mutation batches | 33/33 defects plus five clean controls; all rc 0 | Pair/result retention, ready/credit, loss handling, reset, step/slew thresholds and trim/integrator limits. The original driver requires named runtime failures for its slew arms and its original failed-harness verdict for the other arms. |
| Donor gasket suite | 81/81; 4/4 mutants, rc 0 | Truncated FIFO level, frozen RX/TX SFD toggles and missing end-of-frame. |
| Donor traffic-generator suite | 288/288; 3/3 mutants, rc 0 | Zeroed sequence ID, discarded grandmaster identity and early TX end-of-frame. |
| Simulated board-wrapper target | rc 0 | Two done toggles retain their tags; simulation only. |
| CI scope / events / isolated workflow self-test | rc 0 each; events 2,174 items | Scope/history classification, replay boundary and workflow event drift. Offline workflow test uses read-only source, no network/credentials/socket and CPython 3.12.3. |
| Pins, diagrams, ROM records and resource policy | rc 0 | Six exact gitlinks, eight gPTP pages, generated source-bound rasters and unchanged default ROM digest. Resource policy checks three endpoints; no new physical measurement. |
| Final batch audit | rc 0 | Exact original source digests, every index/name once, expected verdicts and rc 0 in every batch; no omission or duplicate. |

Final parent pin changes are at `docs/design/GPTP_PLANE.md:32`,
`docs/design/TIME_SYNC.md:115`, `docs/reference/SUBMODULES.md:24`,
`docs/traceability/ieee8021as.md:53`, and `docs/guides/gptp/`
`MANAGER.md:23`, `HDL_DEVELOPER.md:33`, `SYSTEM_INTEGRATOR.md:61`,
`TEST_DEVELOPER.md:30`. The generated diagrams and PNG manifest carry
`e4869fd0`; `syn/yosys/rom_digests.tsv:61` records its unchanged image digest.
The gitlink plus these documentation/generated paths are the only 17 changes
from the preserved staged merge. No resumed parent RTL or test source changed.

The historical primitive and M0s resource/route tables in sections 5 and 6
remain tied to their listed revisions in the `e8454e27` lineage. No new area
credit, route verdict or resource acceptance re-record is claimed. The ruling
assigns the merged-effect measurement to the daily #640 work after merging.
Independent reviews must cover these new heads; old positives do not transfer.
The full hosted/candidate-merge bar and post-merge containment remain later work.

The pinned compiler and make were unchanged. CPython 3.12.3 ran the usual
checks; native CPython 3.14.7 ran the table driver for pidfd support. Every
foreground gate invocation stayed under ten minutes. At most two simulation
builds ran concurrently, each capped at two compiler workers. The service's
reported peak was 8,463,949,824 bytes, below 9 GB. No vendor run or
physical access occurred.

### Additional exact commands

Commands below use the same environment as the static table. The workflow
self-test runs only inside the disposable container. `$SCRATCH` denotes the
external disk-backed evidence directory. No gate output was piped.

| Command | rc | Receipt |
|---|---:|---|
| `python3 gptp-processor/syn/ooc/check_ooc_clock.py --selftest` | 0 | `donor-before-clock.log` |
| `python3 gptp-processor/syn/ooc/check_ooc_clock.py --selftest` | 0 | `donor-after-clock.log` |
| `python3 gptp-processor/syn/ooc/check_ooc_clock.py` | 0 | `donor-clock.log` |
| `make -j8 -C gptp-processor/tb/verilator/parser run` | 0 | `donor-before-parser.log` |
| `make -j8 -C gptp-processor/tb/verilator/parser run` | 0 | `donor-after-parser.log` |
| `make -C gptp-processor contract lint docs` | 0 | `donor-static-fixed.log` |
| `python3 gptp-processor/hdl/ucode/gen_gptp_ucode.py -o "$SCRATCH/gptp-default.hex"` | 0 | `donor-rom.log` |
| `python3 scripts/check_py_idiom.py --selftest` | 0 | `py-idiom-self.log` |
| `python3 scripts/check_cpp_idiom.py --selftest` | 0 | `cpp-idiom-self.log` |
| `python3 scripts/ci_scope.py --selftest` | 0 | `ci-scope.log` |
| `python3 scripts/ci_events.py --check` | 0 | `ci-events.log` |
| `python3 -I scripts/act_ci.py --selftest` | 0 | `act-self-prepared.log` |
| `make -j8 -C tb/verilator/gptp_tables run limits` | 0 | `gptp-tables-run.log` |
| `make -j8 -C tb/verilator/gptp_plane run` | 0 | `gptp-plane-run.log` |
| `make -j8 -C tb/verilator/gptp_plane phc-step` | 0 | `gptp-phc-step.log` |
| `make -j8 -C tb/verilator/gptp_shadow run` | 0 | `gptp-shadow-run.log` |
| `bash syn/yosys/ooc.sh --record-rom-digests` | 0 | `rom-digests-record.log` |
| `python3 scripts/check_em_dash.py --base fa8209889411e8ca95757174c981f720dbcd95a2` | 0 | `em-dash.log` |
| `make -j8 -C gptp-processor/tb/verilator/gaskets` | 0 | `donor-gaskets.log` |
| `make -j8 -C gptp-processor/tb/tsngen` | 0 | `donor-tsngen.log` |
| `make -j8 -C gptp-processor/bench/arty test` | 0 | `donor-arty.log` |

Batch commands are reproduced above. Original failed attempts are preserved:
`donor-static` returned 2 for one sentence-length violation, then
`donor-static-fixed` passed; `act-self` returned 1 for a missing executable
in the first isolated image, then `act-self-prepared` passed; `rom-digests`
returned 2 for an unsupported option, then the supported generator command
passed without a ledger delta; `donor-tb` was interrupted after 415.9 seconds
and returned -2. All its completed constituents and every remaining target
now have passing evidence. None of those attempts is hidden or called a PASS.

### Continuation receipts

Scratch root: `$VALIDATION_STORAGE/640m7-a587/r4-resume/`. No receipt below was copied
to the output directory. Files over 200 KB remain outside it.

| Receipt | Bytes | SHA-256 |
|---|---:|---|
| `act-self-prepared.log` | 59168 | `6a28c53acbded43c63ca0ec57eb4fb5f58c1f0826a0a6d8a8bd539d364f6debe` |
| `act-self.log` | 18538 | `16d1d5c9beda06145bf44bc82e40e2bf33b0b673c1679199c9205ed7921206d5` |
| `additional-commands.json` | 1547 | `f3cd5b4446b032545980907e7cc3689e477dbddcfd66090deea91b7523be818f` |
| `before-after.log` | 170 | `9acfffc22ea54354ac9dc3d5d0250e60285457464a7df44d78b9ea5175d6e7df` |
| `campaign-audit.log` | 185 | `4f19513f696ec26fdcac668935f8e492c74254f3375d062d595892f7b20ef435` |
| `campaign_audit.py` | 2007 | `ab206920d63ca19efc7fe8819abce43d3f5da87c6d85cb345ade03af86db9734` |
| `ci-events.log` | 167 | `cbf7f2bb4fa19ca31b60e6e86d022a8f00176c252a015526d8ef299bd1933eb1` |
| `ci-scope.log` | 15329 | `be3ebff4df64fbd38d8a614ddb3be3ff889801c4531ac3a81747f7ae1185c010` |
| `clock-equivalence.log` | 114 | `71a824133bc57f6d55071644653d80066c79d8bc7b237d1d5de9b96ae94264b3` |
| `cpp-idiom-self.log` | 3593 | `7fd74c4ebf8b2f0a9812a20518981f63c8350a34c535bcde2c7fa6c58fbec2b9` |
| `cpp-idiom.log` | 316 | `7c773521653f1e4211a0bb3d719c5d2939de5ef85a8e22d4e83d3280de97c09c` |
| `doc-paths.log` | 85 | `7033b54b2784b7b8d9f1fc7da5b907a49ef6b6572f7579790e4ec9d6f48572ed` |
| `doc-style.log` | 47 | `1491d3f6bec03b920cf58f5fb28e6abff4a9d433a758bc0fe5d2db77bf4f53cd` |
| `docs-nogit.log` | 196 | `08a0ebc92d5f7c34c1af5243f7bc58aa869502fbc0eaf6e6e873add0ac7c820d` |
| `docs.log` | 128 | `afd69244ae6e7091eb4b64694f7d41e43df44ce57725a896bb48a551fdfd2584` |
| `donor-after-clock.log` | 41 | `99a0559caf79c40591b86d49bde93bcdd98a53230af48cbaa02cf09ee27ece09` |
| `donor-after-parser.log` | 4164 | `8b30ccc07db74c520df1ccd99031a01f7c778b719af8a3a716096e31e55cc15c` |
| `donor-arty.log` | 1064 | `4a79ec13b0b9ead7757c44d36f5030f864c1927b693f31fb164e77ad9b410745` |
| `donor-before-clock.log` | 41 | `99a0559caf79c40591b86d49bde93bcdd98a53230af48cbaa02cf09ee27ece09` |
| `donor-before-parser.log` | 3215 | `bdaca5979478959da8a1cce3e0bda3e5d9274404d90e762ea10b35ce519d24ae` |
| `donor-clock.log` | 68 | `95d7509d88fb0432367164d91a04052eea11195787c8cd4b986997967557c02f` |
| `donor-engine-0.log` | 1620 | `2604981321c078d91405adc884f58e2db7065336258f472355bb26bc394a9ae1` |
| `donor-engine-1.log` | 1195 | `3b698a40c76e15e54b7ff4215a3549374b222988c0d8849f6d1f7cb35a5f9f06` |
| `donor-engine-2.log` | 1171 | `f576ea6fd2f61cda020c44a831df6b79b68e824eb6898f3924d87433d6dec6e5` |
| `donor-engine-3.log` | 1063 | `b43b70fca6652082cd049776d69a8ed25708e6465b3dde3a12c061c8d9d9e6ef` |
| `donor-engine-4.log` | 841 | `e2e5420ae19ead00148e8989263746eb33ac52958bd9c70948a1baee2c281b4e` |
| `donor-gaskets.log` | 1876 | `4c9caf476954f74a3c807650a6e95ab98fd46a12c6e62ed7c394f02e5e0d333a` |
| `donor-rom.log` | 303 | `1dee52966fa53d4e5447bc1fe5a2d49a0db5c1d7e1640d1e5a01f612aa0b939f` |
| `donor-static-fixed.log` | 4270 | `ca3432bc23ce6e86ce8fd366aff86e1e55c866362dd73df62ab040e138f6f6eb` |
| `donor-static.log` | 2127 | `823d49fd17e888119f61f8aeff72de372f21dc3ff2356800252d35ea995cee3f` |
| `donor-tb.log` | 10362 | `483a5ad3ded85cdb8c2eb50b0ee5c8a24e819aa96dc11fa24099e4633f45a1ba` |
| `donor-tsngen.log` | 1877 | `c31c0e191ea69dbf2ed9ad1e66af577ff8b8ce0e094923226eababc15585bc7f` |
| `donor_engine_chunk.py` | 794 | `e5d25b85fb57204a3a48e43e54ce69d7b61cd7ad2896821460dbb9420566bd06` |
| `em-dash.log` | 141 | `a8a3f603a691dc4590c987b99d2a057236e3337b0fd283fba10241f8777a6829` |
| `evidence.log` | 18788 | `99be30210e18d0af8473388a5625b5174bbb7dc01f0809a9618917c2a8ac89b7` |
| `fail-fast.log` | 5967 | `88736e013ea360ab7771ca768e0227032b26f748c1f24c20f1a260b788a67d8b` |
| `feature-status.log` | 29 | `802f5eeb2f0aa147169f3ddb9c64d4369ca92ab380455195403f2e8ae02490d0` |
| `final-state.log` | 784 | `56022346517b5933678ecc1ce695b6434c3c0b088e162c5de2e43fb5992e15a9` |
| `gptp-default.hex` | 13312 | `a435fba6167238268fa9074dd4645dd03380e56ff1eeea273fd3fc2fcecab9fd` |
| `gptp-docs-self.log` | 46 | `200332e4eddfd8a6338d8a4dbe27d2f513de92f951a1aa1f6b25882182bc290e` |
| `gptp-docs.log` | 66 | `7ca87a8501c54854805f1cf90d49b2a8ff6353a1049fd21cf0631569f5024e41` |
| `gptp-phc-step.log` | 1907 | `7cb6fb858cf4868ee1db86d9dadef61fcba88dc3027d22ffdb202c278aae0942` |
| `gptp-plane-run.log` | 1668 | `0fbc2f1205b9e6fad8d0919c86918bd1aae080a72ac2495af2de8bd4524c5416` |
| `gptp-shadow-run.log` | 2330 | `cf57f1f963452630137af4a1abdfbd395f9fee549415b9d8294936ebaed3b8c9` |
| `gptp-tables-mutants-0.log` | 577 | `4c73a0626cc20e26d1ce9b4ed0a30b700816c2b02a0322e95c3de46e519ac1ed` |
| `gptp-tables-mutants-1.log` | 569 | `d91c9a5050bef623d3b23451b4aa88d4730a646a0efc4b791ce978d7cc20ca09` |
| `gptp-tables-mutants-2.log` | 567 | `e4b478436759a883133e3404a7a10361e4488a2acf2796b98cd91c02e888c5b3` |
| `gptp-tables-mutants-3.log` | 501 | `4315fa567286e3f823d97bde81bd59af951bf68f2c77f5b0999c5265762d4aef` |
| `gptp-tables-run.log` | 3430 | `8692b7580909a3ecdeecd66c4594b649d57cb95a13bcdafc52a44acc727b6448` |
| `hygiene.log` | 2000 | `16c9e549e4e17018801eaa9d34610a7939b4f6c87fcc7fc51e8a6fc838afe660` |
| `lint.log` | 14186 | `f7765c8f0fb403026f5eba51c6e99b88abd23c1fba7a10b0b9ebd3fa9feec214` |
| `make43-inputs.log` | 1113 | `6e5bab65938768f013ed4195a68b2f8af5fd7a83dcfd7c03df85237a2abfe63b` |
| `make43-limits.log` | 253 | `895e6a6cc7671084b922d6b570d791d64857fd3c37e640e4aa5694f312ff1cdd` |
| `module-matrix.log` | 118 | `4e782e68ed5c09299d5d990702b634a2358aa1d5cbc2fd822374561e249c2687` |
| `naming.log` | 36490 | `8db123cd4a9ebdcc6a488529e53b67d91b48a7c2b4e8d577d9ea17ec0b724965` |
| `one-valued.log` | 43 | `b1818889beca5d5a8dea520e8fd1c0b9b2cb350cf97740418713fd9e2a3a12a8` |
| `passing-inputs.json` | 944 | `12ae6d135790c1d2a37cdeca73bbb00b5ebefb49598e87f72df57fd1b341fd30` |
| `pngs-self.log` | 59 | `918e8cc85a2a2b0d45eeb3f0c7b006824c81e2ed404a535eded095b09d875dc5` |
| `pngs.log` | 66 | `05e0fcfa26a97494e8983dcfca3ad89cdaf91e390acbfb9dbdfb6f614cba4e51` |
| `ports.log` | 421 | `cd9f24fbfd71df64a01d448c13e8aee85846692cbc781f4f45e8eecc7f950bf6` |
| `py-idiom-self.log` | 2531 | `d7413b83955948950d15e364a901be97cf05148dad38e97be07b2d63eb46406d` |
| `py-idiom.log` | 461 | `4a29b174d272f40260506cf2d18a92fe21b4b97e645f30dab78616a6568be035` |
| `repin.log` | 404 | `d65416942e69b6e953c42aa708c0a0c27a060a7c8475f32bb9823f784366552d` |
| `resource-baseline.log` | 27 | `2114d909e60add091220b415987d4409a611d70c9e84f1bb9e0ae12d6a2f14a0` |
| `resource-self.log` | 36595 | `768e343f39de02e68d68aa0a6da0d45bda263cfdea9c5bbb13cb4e037eb80ec7` |
| `rom-digests-record.log` | 198 | `baddd8a42481b7ac6ce7a5c1dc7a31807055e408b20d73cea1003ee70eb34579` |
| `rom-digests.log` | 82 | `855a4eb4d24e91c8643416e11b80671aff75e021a7adf6124e614ffd8724a8dd` |
| `sh-idiom.log` | 235 | `7ace602f03fa0e411862de119cff9d337583f1f2170d920dff65a0e0f39ee6d9` |
| `source-lists.log` | 153 | `ed979d7e26c3cd7a6f14364c11994089b77632424d04252613eeed458ebc8a95` |
| `state-proof.log` | 415 | `f3352082dfe3adb12482954dafc7c3ce1fad7f5d301333b8237f80bc2594b94f` |
| `static-gates.json` | 3001 | `098892238d99c4ad93561b910b08c9051bc00aa782bdff64bbeaa70f4016eeea` |
| `submodule-diagram-self.log` | 60 | `51bca8fb66fd6f0acc480e3364f74fd7a4874946b191468bfbe20ad159cca889` |
| `submodule-diagram.log` | 54 | `4f2d621c17d265a6e2851eaa978fe81af61cf6bbf152cce8ab90ba77b4f91e18` |
| `submodule-docs-self.log` | 66 | `54dbecff3ad17dc651e86c7b313ef57fa96baf89fb40f0fb90af4bbb8ddc802b` |
| `submodule-docs.log` | 47 | `c4bbf250ee33a3cc538cbbf1028e693c8acc058adc782d1f1feef249cd2faa0b` |
| `sv-idiom.log` | 218 | `aed2873a1909e4a41b3e6dee6dc5aaab993bbf1ef41f556062a5b377a6a8b167` |
| `table_chunk.py` | 746 | `15b416c1dc628e9699d6ecc85267f2ee2d5c0e1cb6adc7063b51d61f334e356b` |
| `timesync-diagram-self.log` | 61 | `7c7ad79fa685d29607abf71e3a99d98855fd7ffa1ba5fbf7de23bfb41a33c8fa` |
| `timesync-diagram.log` | 60 | `51058c96a481bf763246394b619601227bdec11b6b11ddcaa1d6f57593d2f1f4` |
| `toc-anchors.log` | 64 | `9d9e538fb10cc7787bf9f74abf5a385ad07c4336858a66a6b03ad7311245e459` |
| `toc-self.log` | 38 | `d7fd5f6ebcdd25e6cf93b623b0fba00cfa32d19c812ce34eb6b8d8b352ac9b32` |
| `toc.log` | 94 | `69f1c8a46304a5e42bd93366b34a8efb1e6aea995f10a25f83cedbdab720a5cf` |

Generated raster receipts (retained in the repository):

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `docs/diagrams/submodule_boundaries.png` | 438329 | `cec6255edea7b7d3d2dc7377f6d7217e6b6c1c6814dfbc4db26dd7cb30d32734` |
| `docs/diagrams/timesync_chain.png` | 314514 | `63bbccf71eaa015227b0976935db9d5b486e7e049ffbfb69a892f7c6c399e577` |

Public REVIEW READY receipt: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6162686301

## Round 5

REVIEW READY under issue #640 comment 6163132636.
Parent: `4c5d70b50230fbd5da347852d39daf7f23b3df0b`. Donor: `e4869fd0c42889b2ac806587cc5c78afb1c33461` (unchanged).
The parent origin is the assigned HTTPS repository; the branch is `640-m7`.
Its merge base with the original base is `e8454e2751d05b02ee8e5a571857589ab358ab86`.
Both tracked trees and indexes are clean. No push occurred.
The donor root and origin were verified before donor Git inspection.

### Changes and disposition

| Change | File and line | Result |
|---|---|---|
| Provisional suite duration | `scripts/suite_shards.py:161,201` | `gptp_tables` is recorded at the required 1800 seconds and declared provisional |
| Added worker and overhead | `scripts/suite_shards.py:207,846` | Prior maximum overhead 115 seconds inserted before the dedicated worker; its landmark moves to 5 |
| Workflow capacity and evidence | `.github/workflows/rtl.yml:161,227,426` | Six workers, `milan_dp` alone on 5/6, aggregate requires six matching records |
| Contract and negative fixtures | `scripts/ci_events.py:1959,1974,2237,5261,5367,6144,6544` | Ownership, counts, dropped-worker and omitted-last-worker controls follow the six-worker shape |
| Current scheduler documentation | `docs/testing/TESTING.md:518`; `docs/testing/CI_WORKFLOWS.md:347,356,2684` | Current counts and examples match; historical five-worker measurements stay dated |
| Measured reach | `tb/verilator/gptp_tables/README.md:29,31`; `tb/verilator/gptp_tables/sim_main.cpp:15,20` | TX 25/256; results 2/8; thresholds and stimulus unchanged |

Step 1 commit: `fb4d30b1a491d2dddc5c98cf7d725c19f92841db`.
Step 2 commit: `90f75192f5771ad873eba45a391ba764da91af57`.
Step 3 commit: `4c5d70b50230fbd5da347852d39daf7f23b3df0b` advances the remaining stale-denominator fixture
at `scripts/ci_events.py:5402`, as the new-worker procedure requires.
The final CI contract/self-test and Python idiom gate pass again.
All three are new one-line commits with the configured identity.

R592-4-F1 and R593-4-F1 are implemented for re-review.
R593-4-F2 now agrees with fresh execution.
R592-4-S1 was optional: the inert historical ROM row is retained.
Earlier residues and suggestions remain assigned as the reviews describe.
No donor commit, RTL change, register change or budget exception was added.

### Timing and ownership

The untouched starting selector reproduces the missing-duration refusal (rc 1).
Adding only the mandated provisional duration reproduces the capacity refusal
(rc 1): workers 0..3 predict 4629, 4628, 4630 and 4730 seconds,
above the 4320-second bound. These are expected negative controls.

After adding the worker, predicted seconds are
`3746, 3746, 3746, 3747, 3747, 2877`.
The 120-minute timeout and 60 percent bound are unchanged.
All 63 default suites have complete, disjoint ownership.
`gptp_tables` appears exactly once, on 0/6; `milan_dp` is alone on 5/6.
The specialized owners remain `tsn_fuzz` on 1/6 and `chmap_capture` on 3/6.
The serial list remains the full lexical inventory.

Local measured components: clean build plus baseline 21.803 seconds;
stock 26-control campaign 402.903 seconds; limits check 0.032 seconds.
Their sum is 424.738 seconds. This is a sum of separate local executions,
not a hosted suite window or one end-to-end default-target measurement.
The committed provisional 1800 seconds comes from `suite_timeout`, as required.
After a successful published run, step 3 of the selector's procedure must
replace the suite duration and new-worker overhead with hosted measurements.
No publication or hosted execution was authorized here.

### Gate table

All final gates below returned zero. Gates ran directly with logs redirected,
without verdict pipelines. The simulation uses the pinned 5.050 compiler;
the fresh baseline uses GNU make 4.3, `MAKEFLAGS=w` with `-j8`, and
`VERILATOR_JOBS=2`. Static Python gates use CPython 3.12.3 with the existing
scratch environment's dependencies. Process-ownership tests use native Python
because the supplied 3.12.3 build lacks pidfd support.

| Gate / plain command | Result | Defect detected or evidence limit |
|---|---|---|
| `python3 scripts/suite_shards.py --selftest` | PASS | Missing/retired/zero durations, wrong provisional timeout, overload, wrong worker count, moved specialized owners, overlapping or incomplete ownership |
| `python3 scripts/ci_events.py --check` | 2175 items, PASS | Workflow/contract drift, including wrong worker count or aggregate record count |
| `python3 scripts/ci_events.py --selftest` | 3096 arms, PASS | Dropped sixth worker, stale denominator, stale `--expect`, widened dedicated ownership and tally/result loops omitting the last worker |
| `python3 scripts/ci_scope.py --selftest` | PASS | Scope/history changes that would skip required execution |
| `scripts/run_all_suites.sh --shard I/6 --list` for I=0..5, plus `--list` | PASS | Independent counter comparison detects missing, duplicated or renamed suites; specialized and dedicated owners asserted |
| Serial `run_preflight_gates` | 8/8 gates, PASS, 105.601 seconds | Exact function bodies loaded from the current driver; only its final `main` invocation omitted; no full sweep claimed |
| `make -j8 -C tb/verilator/gptp_tables run` | 36/36 twice | Consumer mismatch, missing activity/index/reset/depth coverage, wrong decode, incorrect one-valued declarations; actual run used verified input copies in scratch |
| `python3 tb/verilator/gptp_tables/mutants.py` | 26/26, PASS | Every original planted defect fails its named check, listed below |
| `python3 scripts/gen_one_valued_table.py` and `--check` | Both PASS | Stale generated one-valued table; generation made no change; reach table is handwritten |
| `python3 scripts/check_py_idiom.py` | PASS | Python ratchet violations, with unchanged budgets |
| `python3 scripts/check_cpp_idiom.py` | PASS | C++ ratchet violations, with unchanged budgets |
| `python3 scripts/docs_check.py` | PASS | Public hygiene and routing; 23 scrub and four routing controls |
| `GIT_DIR=/dev/null python3 scripts/docs_check.py` | PASS | Filesystem fallback; 22 scrub and four routing controls; Git inventory-parity arm explicitly skipped |
| `python3 scripts/check_em_dash.py --base 412e3f6c` | PASS | All 21 added Markdown lines, three pages; 339 planted controls |
| `python3 scripts/check_doc_style.py` | PASS | Documentation style gate; no new planted control |
| `python3 scripts/check_doc_paths.py` | PASS | 985 paths and ten line anchors; no new planted control |
| `python3 scripts/gen_toc.py --check` | PASS | Stale generated contents; no headings changed |
| `python3 scripts/check_hygiene.py --check` | PASS | Whitespace/encoding ratchets; unchanged budgets |
| `python3 scripts/measure_naming.py --check` | PASS | Unrecorded boundary naming findings; unchanged budget |
| `python3 scripts/measure_fail_fast.py --check` | PASS | Masked verdicts and discarded statuses; unchanged budget |
| `python3 scripts/measure_test_evidence.py --check` | PASS | Evidence ratchets and 63-suite scheduling contract; unchanged budgets |
| Final source/evidence audit | PASS | Exactly seven changed paths, 24 tested input files match final bytes, non-comment harness lines and runtime output identical, all controls present |
| `git diff --check` and tracked status checks | PASS | Whitespace defects or unintended tracked changes |

The serial preflight executes these unchanged gate commands:

```sh
python3 scripts/test_suite_cancellation.py
python3 scripts/suite_tally.py --selftest
python3 scripts/suite_shards.py --selftest
python3 scripts/check_merge_containment.py --selftest
python3 scripts/check_results_fresh.py --self-test
bash syn/yosys/check_list_hermetic.sh
python3 scripts/xvlog_gate.py --selftest
python3 scripts/check_merge_review_integrity.py --selftest
```

Their controls respectively detect cancellation/orphan/timeout failures,
false or unreadable tallies, scheduler omissions, false containment,
stale/unverifiable evidence (18 controls), non-hermetic top discovery,
use-before-declaration and replacement-reference populations, and invalid
review/closure claims (86 controls). These checks provide no actual merge,
review approval, full-suite or hardware verdict.

### Table defect controls

The campaign copied the original committed inputs before the documentation edit.
Only two whole-line C++ comments changed afterward. Its executable source,
26 mutation definitions, wrapper, declarations and RTL match the final head.
The repeated baseline's runtime output is byte-identical and all 24 declared
inputs in its scratch build match the final source. It reaches TX depth 25,
ledger depth 3 and result depth 2, with 111 writes behind a waiting result.

| Planted defect | Named check that failed |
|---|---|
| `rx_fifo_wrong_depth` | `rx_fifo lockstep` |
| `rx_fifo_wrong_read_latency` | `rx_fifo lockstep` |
| `rx_fifo_lane_alias` | `rx_fifo lockstep` |
| `tx_fifo_wrong_depth` | `tx_fifo lockstep` |
| `tx_fifo_wrong_read_latency` | `tx_fifo lockstep` |
| `tx_fifo_count_alias` | `tx_fifo lockstep` |
| `tx_fifo_decode_odd_counts` | `tx_fifo decode` |
| `ledger_wrong_depth` | `ledger lockstep` |
| `ledger_wrong_read_latency` | `ledger lockstep` |
| `ledger_index_alias` | `ledger lockstep` |
| `results_wrong_depth` | `results lockstep` |
| `results_wrong_read_latency` | `results lockstep` |
| `results_index_alias` | `results lockstep` |
| `results_write_index` | `results lockstep` |
| `timer_wrong_depth` | `timer lockstep` |
| `timer_wrong_read_latency` | `timer lockstep` |
| `timer_index_alias` | `timer lockstep` |
| `rx_fifo_lane_stuck` | `rx_fifo values: lane` |
| `tx_fifo_count_stuck` | `tx_fifo values: count` |
| `ledger_type_stuck` | `ledger values: type` |
| `results_seq_stuck` | `results values: seq` |
| `timer_deadline_stuck` | `timer values: deadline` |
| `declaration_missing` | `ledger values: tag` |
| `declaration_wrong_value` | `ledger values: tag` |
| `declaration_many_valued` | `ledger values: type` |
| `declaration_stray` | `values: declarations that name no censused column` |

### Primitive, resource and route evidence

Round 5 changes no synthesized input. No new synthesis, route, hardware or
bench measurement was run. The following are historical M0s results from
base `e8454e27` to routed M7 `49e1ce48`; they do not qualify the merged tree.

| Storage | Historical before | Historical after |
|---|---|---|
| Tap and TX frame FIFO, each 256 beats | Each RAMB36 + RAMB18 | Each one RAMB36 |
| Ledger 8 x 21 | 168 FF plus mux | 4 RAM32M + 1 RAM32X1D |
| Results 8 x 89 | 712 FF plus mux | 16 RAM32M + 1 RAM32X1D |
| Timer 8 x 32 | 256 FF plus mux | 5 RAM32M + 2 RAM32X1D |

| M0s integrated metric | Base | M7 |
|---|---:|---:|
| LUT | 50267 | 49898 |
| FF | 54413 | 53220 |
| Slices | 15779 | 15773 |
| RAMB36 / RAMB18 | 74 / 27 | 74 / 25 |
| WNS / WHS, ns | +0.299 / +0.031 | +0.122 / +0.019 |

The historical resource gate passed the then-current record, every endpoint
met timing, and the route was complete. The isolated plane saving remains
107-253 LUTs, below the estimated 500 (300-700), plus 1149 FFs and one tile.
No re-record occurred; D7 reserves that for M9. The owner requires the daily
area measurement after merge to capture the integrated effect.

### Execution limits and attempts

No Makefile changed. Builds and mutation copies stayed in disk scratch.
At most two simulation builds overlapped; no route ran beside them.
The service's observed peak was 1629097984 bytes, below 9 GB.
No source or generated artifact was added to the repository by validation.
Pre-existing ignored build products were left in place.

Two initial CI-contract invocations lacked PyYAML in bare CPython 3.12.3
(rc 2). Both pass with the existing scratch 3.12.3 environment.
An initial final-audit helper mistakenly compared generated build metadata
with pre-existing ignored products (rc 1). Restricting that helper to the
Makefile's declared input inventory produced the passing 24-file audit.
The initial pre-commit em-dash call saw zero committed changes and supplies
no evidence for these edits; the final call grades all 21 changed lines.
Expected selector refusals above are negative controls, not final gates.

No full parent/donor suite bank, synthesis bank, builder bank, physical
calibration, hosted workflow or local workflow replica was rerun this round.
The Round 5 assignment requires the scheduler/preflight and focused evidence.
Prior bank and area evidence retains its original revision and limits.
Corrected-head reviews, hosted duration refresh, required contexts,
current-dev candidate validation, donor-before-parent merge ordering,
explicit merge authorization, containment and daily area measurement remain.

### Round 5 receipts

Receipts remain in disk scratch under `640m7-a587/round5`; the output
contains only these descriptions. No build tree or installed dependency
was copied here. Sizes and SHA-256 below identify the original bytes.

| Receipt | Bytes | SHA-256 |
|---|---:|---|
| `baseline-final.log` | 4454 | `b92e4ab692282c953bf7c2ac94d4ac1a0f9f920aaa84c89fb44beda7d4dedb60` |
| `baseline-time.txt` | 59 | `e20e2ad140231eebbd71c102bd63184928775906d84669dde47e0f46b2549fcf` |
| `baseline.log` | 8293 | `e273f41f2e1582519c993cfc96edefbf408b1f1584f9a466e60cb33e4c9bfa1f` |
| `ci-events-final.log` | 167 | `1d6cd17ae0e330d2f2cd96ed2860848271e3b99f2e7c13c6e5e9583312518a0b` |
| `ci-events-ready.log` | 167 | `1d6cd17ae0e330d2f2cd96ed2860848271e3b99f2e7c13c6e5e9583312518a0b` |
| `ci-events-self-ready.log` | 201887 | `23d55e96ea018ba2ed2844516b4e82ca9aaa54fe8f783a562fdeafc992bab9bb` |
| `ci-events-self.log` | 112 | `66ff829cdfd77c5b5c714c54610e3918d9a542b9f6c0840266c46fa44e8892cb` |
| `ci-events.log` | 94 | `2766cc70ea74e5ea60a7f629477f34efc6d435842c046a083296293bb021a962` |
| `ci-scope.log` | 15329 | `be3ebff4df64fbd38d8a614ddb3be3ff889801c4531ac3a81747f7ae1185c010` |
| `cpp-idiom.log` | 316 | `7c773521653f1e4211a0bb3d719c5d2939de5ef85a8e22d4e83d3280de97c09c` |
| `doc-paths.log` | 85 | `7033b54b2784b7b8d9f1fc7da5b907a49ef6b6572f7579790e4ec9d6f48572ed` |
| `doc-style.log` | 47 | `1491d3f6bec03b920cf58f5fb28e6abff4a9d433a758bc0fe5d2db77bf4f53cd` |
| `docs-final.log` | 128 | `afd69244ae6e7091eb4b64694f7d41e43df44ce57725a896bb48a551fdfd2584` |
| `docs-nogit.log` | 196 | `08a0ebc92d5f7c34c1af5243f7bc58aa869502fbc0eaf6e6e873add0ac7c820d` |
| `docs.log` | 128 | `afd69244ae6e7091eb4b64694f7d41e43df44ce57725a896bb48a551fdfd2584` |
| `em-dash-final.log` | 139 | `25026be3ac4e76b2044f583bc25420aca8e1536342b6db600d06aff902dcd0c5` |
| `em-dash-step1.log` | 139 | `499b28e50e304c1a1f5dbe4c242484262f2eceaf8c84cb244c5614300475a49a` |
| `em-dash.log` | 138 | `6c36e0bf54c4caa048d8e132fb3ae187843d98dc9b748a1941f1789c1a6af042` |
| `evidence.log` | 18788 | `99be30210e18d0af8473388a5625b5174bbb7dc01f0809a9618917c2a8ac89b7` |
| `fail-fast.log` | 5967 | `88736e013ea360ab7771ca768e0227032b26f748c1f24c20f1a260b788a67d8b` |
| `final-proof-inputs.log` | 424 | `c3ac2d83f7881d9dd209fccd86f3d186929c5763c9a5803c94801fbdfea67e9c` |
| `final-proof.log` | 318 | `dae4a047326279160bd74a65298b73803b3b0226acc013b60a5d90eb063cb096` |
| `hygiene.log` | 2000 | `16c9e549e4e17018801eaa9d34610a7939b4f6c87fcc7fc51e8a6fc838afe660` |
| `naming.log` | 36490 | `8db123cd4a9ebdcc6a488529e53b67d91b48a7c2b4e8d577d9ea17ec0b724965` |
| `one-valued-check.log` | 43 | `b1818889beca5d5a8dea520e8fd1c0b9b2cb350cf97740418713fd9e2a3a12a8` |
| `one-valued-generate.log` | 43 | `b1818889beca5d5a8dea520e8fd1c0b9b2cb350cf97740418713fd9e2a3a12a8` |
| `py-idiom.log` | 461 | `5187a715364d5aeea694f08e745481a5fa8c94b3f3bda617c5fa8c8d71fd06a0` |
| `selection.log` | 913 | `ecc4133ce31b5e3701871db092ce7f98320b345a4bf1304d1ca236c08c5d1323` |
| `selector-before.log` | 1732 | `349b189b9179d1502768a5c4d84ba367af6ce303ed142e1a171ccb6995a14637` |
| `selector-five-workers.log` | 1753 | `9d02dbb8378b274e0db9d057f90be550b60f78e4dd5c23b8ce33abd8697a9fa5` |
| `selector.log` | 3184 | `7696d9aec29bfc337cbba3dc0c1f82e6140a1f8985586273aac1f4c53883591f` |
| `serial-preflight/preflight/check_list_hermetic.log` | 277 | `6bedc0b16eb78f3099a4f37ee48e6745df697975e72195519f2a6811a7cc40aa` |
| `serial-preflight/preflight/check_merge_containment.log` | 77199 | `928072db281e8ccdfe8af91318c5720a1bf179b7f6d028443fd30026c7dcd1f3` |
| `serial-preflight/preflight/check_merge_review_integrity.log` | 67 | `a51886ca2968afa03f52241d7e26856732f00f97e96735f9ea2cde040244a88d` |
| `serial-preflight/preflight/check_results_fresh.log` | 1220 | `dd66248c3a2e15863eaa46890be77b0198b251c3ee9fdcd86094f461055b0ae9` |
| `serial-preflight/preflight/suite_shards.log` | 3184 | `7696d9aec29bfc337cbba3dc0c1f82e6140a1f8985586273aac1f4c53883591f` |
| `serial-preflight/preflight/suite_tally.log` | 6164 | `055407e98670d2dd43e727273c951699f7c69d3327239a558b1bfe7057b2f675` |
| `serial-preflight/preflight/test_suite_cancellation.log` | 5972 | `3909d229caecfad058a3765f220d5ed1f657ef074bf7f5751399c59439ae49a0` |
| `serial-preflight/preflight/xvlog_gate.log` | 170 | `ed6b96726154251583cf2076cefb9526af04c7093efd8de974e86e7c3a6dc9f8` |
| `serial-preflight.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `table-controls.log` | 1605 | `73e1764e29ca80cb07ddf247f64e38ef9cf6f0f515b336d86e96ef8082f6821e` |
| `toc.log` | 94 | `69f1c8a46304a5e42bd93366b34a8efb1e6aea995f10a25f83cedbdab720a5cf` |
| `worker-0.txt` | 94 | `9d361068a9efd45a26cefda098da522c2b98d98c7db8ac9dc472684e3b464c41` |
| `worker-1.txt` | 141 | `e210e4aa3100669c85d375ac4a9fe2ec6a68de5092e06516f53d6c0b96eb75c6` |
| `worker-2.txt` | 131 | `5398c14596ac65ccc038e62bf149e2c4bf0329d60d29577e210f756502df80e8` |
| `worker-3.txt` | 150 | `bbb3db1c4a4ddeb6467413dcfaa2e66c46f840676af9507750f41d6946d598fb` |
| `worker-4.txt` | 135 | `993287c41baefb3f33f414ea7cc17b0cbaa4164871192b4d485f436da7f3bf2c` |
| `worker-5.txt` | 9 | `4612796f87e8211c362dda12da45090a4d300000b8804bc2975ad3dda3928c9e` |

Final fixture and head-audit receipts:

| Receipt | Bytes | SHA-256 |
|---|---:|---|
| `ci-events-final-fixtures.log` | 167 | `1d6cd17ae0e330d2f2cd96ed2860848271e3b99f2e7c13c6e5e9583312518a0b` |
| `ci-events-self-final.log` | 201887 | `23d55e96ea018ba2ed2844516b4e82ca9aaa54fe8f783a562fdeafc992bab9bb` |
| `py-idiom-final.log` | 461 | `5187a715364d5aeea694f08e745481a5fa8c94b3f3bda617c5fa8c8d71fd06a0` |
| `final-head-proof.log` | 424 | `c3ac2d83f7881d9dd209fccd86f3d186929c5763c9a5803c94801fbdfea67e9c` |
