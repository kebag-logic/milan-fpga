# HANDOFF: lane M7 for #640, fabric gPTP plane tables (plan L10a)

Executor [A587]. Reviewers [R592] (internal) and [R593] (external).
Branch `640-m7` from dev `e8454e27`, head `9d42762c555118e3ea86665bf7d8c6ef673698d3`. Local only; not pushed.
The gPTP processor submodule carries a local branch `640-m7` at `18dd997b2459699e41e5ce9bceca1181e41fa5fe` (from `5dce647a`).
Push that submodule branch before the parent: the parent's gitlink names it.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6097272538
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6097298086
REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6100339945

## Status

REVIEW READY at `9d42762c`. Every gate listed below returned 0.
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

Existing suites that cover the plane, at heads whose RTL and tests equal the final head: `gptp_shadow` 309/309 with 9/9 controls; `gptp_txts` 85/85 with 6/6; `gptp_plane` 29/29; `milan_dp` 12,065 checks (legacy, N=4 and N=8 legs); `milan_dp_gptp` (physical) 197; `tsn_fuzz` with the pinned generator: gPTP field campaign 677 pass, 0 fail, committed artifact fresh, AAF 164 pass; the gPTP processor's `make tb` (micro-CPU 768, parser 268, engine 1,613 x3, 40/40 engine mutants, gaskets, tsngen and the Arty bench).

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
