# [A570] Issue #696 handoff

## Status: REVIEW READY

Published and read back identical: https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6092935897 (text in `REVIEW-READY-COMMENT.md`).

Head `030eb98a12685a2ca41cf8d785bb0eb69dc32a98`, branch `696-maap-annexb`, local only (no push, no PR).
Clean tree; fourteen first-parent commits over dev `6aa25dec`, the merge of dev `8b61b709` among them.
Ruling applied: https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6089712293 (option b, no floor exception),
on top of rulings 6080332335, 6079463350, 6079087547, 6076940309 and the assignment 6076750392.
The previous STOP (route floor) is https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6089695284 (text in `STOP-COMMENT.md`).

What this resume did, in order:

1. Merged dev `8b61b70902f3ebf118e56967277e2686731081bd` (`origin/dev` at fetch, the merge of #699) as merge commit `0df48637`. No rebase.
   No conflict; submodule pins unchanged. The lane's diff over dev is identical to its diff over `6aa25dec`, hunk headers aside.
2. Reran the full local bar at the merged head `0df48637`: parent sweep without any lock, parser, portability, lint, behaviour,
   the documentation set, the focused MAAP checks, the firmware bank and the pinned field campaigns. Every gate rc 0 (table below).
3. Re-measured `route-1x1`, `ooc-1x1` and `ooc-8x8` at `0df48637` through the recipe in one exclusive-lock job. All three gate checks exit 0.
4. Recorded all three through `pp_resource_gate.py record --write` and committed the record alone (`e6f00121`); `check-baseline` exits 0.
5. Updated the two documents that restate the gate's record (`030eb98a`) and reran the documentation set at that head: 94/94 rc 0.
6. Measured the MAAP block with its ceiling instrument at dev and at the merged head: within the ceiling.

No register-map, filter, mailbox, submodule-pin or policy change. No tolerance, floor or ceiling changed.

## Merged-head measurement

| Endpoint | Figures at `0df48637` | Against the #645/#647 record (dev) | Gate |
|---|---|---|---|
| `route-1x1` | LUT 50,230; FF 54,308; slice 15,823 (27 free); RAMB36 74; RAMB18 27; DSP 14; CARRY4 3,397; WNS +0.114 ns; WHS +0.036 ns; 101,344/101,344 nets routed, 0 errors; IOB packing 22 ports OK | LUT -37, FF -105, slice +44, WNS -0.185 ns, WHS +0.005 ns | `check` exit 0 |
| `ooc-1x1` | LUT 23,179; FF 19,779; RAMB36 16; RAMB18 3; DSP 8 | every figure equal | `check` exit 0 |
| `ooc-8x8` | LUT 30,135; FF 27,380; RAMB36 21; RAMB18 5; DSP 8 | every figure equal | `check` exit 0 |

The record's WNS +0.299 ns made the 0.25 ns fall limit bind first (at least +0.049 ns needed); +0.114 ns meets it and the +0.030 ns floor.
Route corners: Slow 0C/85C WNS +0.114 / WHS +0.102 ns; Fast 0C/85C WNS +1.518 / WHS +0.036 ns.

Worst setup path: `milansoc_crg_clkout0` (10 ns), slack +0.114 ns, 16 logic levels, data path 9.574 ns (logic 2.279, routing 7.295).
It runs from `milansoc_sdram_zqcs_timer_count1_reg[1]` to `milansoc_sdram_bankmachine1_level_reg[0]`, inside the soft CPU's SDRAM controller.
Receipt: `merge-receipts/route-queries/worst_path.rpt` and `worst10.rpt`.

MAAP in the routed checkpoint (same lock hold, `merge-receipts/route-queries/queries.log`):
`g_maap.maap_engine` 425 LUT / 339 FF (339 sequential cells).
The worst setup path into it keeps +4.037 ns (18 levels, from the PHC `ts_counter/acc_reg[31]` to `offset_r_reg[12]`).
The worst path out of it keeps +6.719 ns, and the worst hold into it +0.135 ns.

Slack history of `route-1x1` (all the same recipe identity F):

| Image | WNS ns | WHS ns | Critical path |
|---|---:|---:|---|
| F (#682) | +0.124 | +0.031 | AXI-Lite-to-Wishbone bridge to SPI-flash PHY counter, 18 levels |
| #686 record | +0.241 | +0.029 | - |
| #645/#647 record (dev `6aa25dec`) | +0.299 | +0.031 | `milansoc_write_w_buffer_level0_reg[1]` to `storage_13_dat1_reg[14]`, 14 levels |
| Lane head `39571196` (not recorded, previous STOP) | +0.029 | +0.015 | soft CPU DMA write bridge `downW_header_reg[3]` to `pendings_valids_reg[0]`, 19 levels |
| Merge `0df48637` (recorded) | +0.114 | +0.036 | SDRAM controller `zqcs_timer_count1_reg[1]` to `bankmachine1_level_reg[0]`, 16 levels |

Both worst paths in this lane lie outside `KL_maap` and `milan_datapath`; placement variation in unchanged soft-CPU logic explains the spread.

### MAAP resources against the ceiling

Instrument: unchanged `syn/ooc/milan_datapath_ooc.tcl`, one synthesis and general thread, under the exclusive lock (`merge-receipts/maap-ooc-*`).
Ceiling (ruling 6079087547): +60 LUT / +60 FF at `g_maap.maap_engine` over the `6aa25dec` base of 439 / 280.

| Tree | `g_maap.maap_engine` LUT | FF | vs base `6aa25dec` | vs dev `8b61b709` | Within ceiling |
|---|---:|---:|---:|---:|---|
| Base `6aa25dec` (historical) | 439 | 280 | 0 / 0 | - | - |
| Dev `8b61b709` (no lane change) | 443 | 280 | +4 / 0 | 0 / 0 | - |
| Lane head `39571196` (historical, M3 committed) | 441 | 340 | +2 / +60 | - | yes |
| Merge `0df48637` | 445 | 340 | +6 / +60 | +2 / +60 | yes: 445 <= 499, 340 <= 340 |

The FF allowance is fully used, as before the merge. Dev's datapath edits alone move the block by +4 LUT.
Zero `Synth 8-4445` diagnostics in both runs; input hashes equal before and after.

## Changes in this resume

| Commit | Artifact | Change |
|---|---|---|
| `0df48637` | merge of dev `8b61b709` | Merge commit; one-line subject; no conflict. The lane's MAAP hunks at `hdl/milan/milan_datapath.sv:267`, `:7171` and `:7172` are intact |
| `e6f00121` | `syn/ooc/pp_resource_baseline.json:5`, `:470`, `:928` | `record --write` replaced the three records (figures and input digests) |
| `e6f00121` | `syn/ooc/pp_resource_baseline.json:451`, `:919`, `:1377` | `measured` notes name merge input `0df48637`, dev `8b61b709` and the passed comparison; identities, tolerances, floors and ceilings unchanged |
| `030eb98a` | `docs/design/AREA_BUDGET.md:13`, `:108` | Current record named as #696's merge of dev `8b61b709` |
| `030eb98a` | `docs/design/AREA_BUDGET.md:122`-`:127`, `:130`-`:134` | Headroom table ("the gate's record"), binding slice margin, critical path and preceding image |
| `030eb98a` | `docs/design/AREA_BUDGET.md:143`, `:148` | Datapath and wrapper LUTs and the NFR-RES-01 arithmetic at the new record |
| `030eb98a` | `docs/design/AREA_BUDGET.md:383` | Which WNS limit binds at the new record (the floor, after a 0.084 ns fall) |
| `030eb98a` | `docs/design/AREA_BUDGET.md:436`-`:438` | Seventh re-baseline: deltas against #645 and the routed `KL_maap` |
| `030eb98a` | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:6`, `:16`, `:32`-`:104` | Current-record pointer, generated contents entry (description hand-written) and the new re-baseline section |

## Merged-head gate table

WORK denotes disk-backed scratch. Commands are unpiped; each rc is the command's own.
Heads: `M` = merge `0df48637`; `F` = final `030eb98a` (adds only the record JSON and two documents to `M`).
Verilator builds used the pinned 5.050 through a two-slot build semaphore; never more than two compilations at once.

| Gate | Exact command | Head | Result |
|---|---|---|---|
| Parent sweep | `bash scripts/run_all_suites.sh "$WORK/parent-suites-logs"` (clean worktree, no flock) | M | rc 0; 61/61 suites, 2,185,905 checks, 0 failures, 0 timeouts; four declared field-campaign skips; 8,862 s |
| Pinned field campaigns | `TSN_GEN_ROOT="$FIELD_GENERATOR" make -j8 -C tb/verilator/tsn_fuzz` (generator at the `rtl.yml` pin, clean) | M | rc 0; AAF 164 and gPTP 677 pass, both freshness checks pass; the two generated pages differ only in their timestamp line (diff kept, scratch tree restored) |
| Parser | `python3 scripts/xvlog_gate.py --check` (exclusive lock) | M | rc 0; 81 + 52 sources, 0 findings |
| Portability | `bash syn/yosys/run.sh --results "$WORK/portability-results"` | M | rc 0; 58/58 tops, tied-input and tap-purity gates pass |
| Lint | `python3 scripts/lint_rtl.py --check --self-test --jobs 2` | M | rc 0; 90 <= 90 |
| Behaviour | `behave --no-capture -f plain` (in `tests`) | M | rc 0; 14 features, 404 scenarios, 1,968 steps |
| MAAP unit | `make -j8 -C tb/verilator/maap run MDIR="$WORK/unit-build"` | M | rc 0; 171 checks, 0 failures |
| MAAP datapath | `make -j8 -C tb/verilator/maap integration-build DP_MDIR="$WORK/integration-build"`, then the built binary | M | rc 0; 3 checks, 0 failures |
| MAAP campaign | `python3 tb/verilator/maap/mutants.py` | M | rc 0; 51 rows: 49 defects caught (rc 1, named check), 2 clean controls |
| MAAP coverage | `make -j8 -C tb/verilator/maap coverage COV_MDIR="$WORK/coverage-build"` | M | rc 0; `KL_maap.sv` 215/215 lines, 95 % gate |
| Differential | `python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep "$WORK/differential"` | M | rc 0; 12/12 cases; 17/17 defects; clean sweep 5,173..5,810 cycles; MAC-ignoring 5,220..5,710, rejected at the highest-draw check |
| Firmware bank | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 2` | M | rc 0; host, RV32 and campaigns; general campaign 471/471 |
| Documentation set | 94 commands: every `docs.yml` docs-check, wire-accountability and no-git command, plus `pp_srcs --check --selftest`, the `syn/ooc` and `syn/yosys` self-tests and mutants, and `check-baseline` | M and F | rc 0 at both heads, tree clean; em-dash base `8b61b709` |
| Shipping exports | Recipe previews, emitted arguments without `--build`, helper with `--single-thread-synthesis` | M | every step rc 0; 122 / 119 inputs byte-identical to the lane; 6 / 6 images match |
| `route-1x1` | `baseline_integrated.tcl`, then `pp_resource_gate.py check ... --endpoint route-1x1` | M | Vivado rc 0 (50.2 min); check rc 0 |
| `ooc-1x1` | `baseline_ooc.tcl` with `--integrated-clock`, then `check ... --endpoint ooc-1x1` | M | Vivado rc 0 (22.3 min); check rc 0 |
| `ooc-8x8` | RTL elaboration for parameters, `baseline_ooc.tcl` with `--integrated-clock`, then `check ... --endpoint ooc-8x8` | M | Vivado rc 0 (1.2 + 43.0 min); check rc 0 |
| Input stability | Measurement-input digests before and after the job | M | equal: 1x1 `a6574248...`, 8x8 `e05f6bd1...` |
| Record | `record ... --write` for the three endpoints, `check` after each, `check-baseline` | M -> F | all rc 0; committed alone as `e6f00121` |
| MAAP ceiling | `syn/ooc/milan_datapath_ooc.tcl`, one thread, exclusive lock | dev and M | rc 0; 443/280 at dev; 445/340 at M |
| Whitespace and tree | `git diff --check 8b61b709 HEAD`; `git status --short` | F | clean |
| Hosted checks / local workflow replica | exact pushed PR head | - | NOT RUN: no push or PR in this assignment |
| Processor banks | protocol-processor `scripts/run_suites.sh`; gptp-processor `make -j8 tb` | - | Not rerun: pins and processor sources unchanged; last run at `963ad3b8e` passed (1,028,250 checks; gPTP bank) |
| Bench | Acceptance 4 | - | NOT RUN; separate post-merge lane |

The focused bank wrapper exited 1 only because the field campaign rewrote the timestamp lines of its two generated pages;
every one of its eleven commands returned 0 (`merge-receipts/focus-merged/`, `field-generated-diff.log`).
Vivado ran alone: the go file released the measurement job only after the sweep and the focused bank had ended.
Measurement lock hold 02:12-04:12; MAAP-ceiling hold 04:17-04:34. Largest Vivado peak 8,026 MB; no out-of-memory event.

## Acceptance coverage

| Acceptance | Status at `030eb98a` |
|---|---|
| 1. Each item conformed with a suite check and planted defect, or justified by clause | MET: M1, M2, M4, M5, M7 conformed; M8 discard conformed (counting withdrawn by ruling, documented); M6 and M3 conformed with explicit, clause-cited limits in `MAAP_FABRIC.md` (one-response capacity; pool-fold bias) |
| 2. M4 fixed in RTL first, datapath check with two MACs | MET (`39bf3d5f`); real-datapath check and reset-time defect pass at M |
| 3. OOC area and one shipping route within budget; records re-recorded through the recipe | MET: MAAP +6 / +60 against base (ceiling +60 / +60); route and both standalone endpoints pass the gate at the merge result and are recorded (`e6f00121`) |
| 4. Bench interop unchanged | NOT RUN; separate post-merge bench lane (assignment item 6) |

| Item | Clause | Status |
|---|---|---|
| M4 | B.3.4 NOTE; B.3.6.1 | Implemented first; datapath check and planted defect pass; consumer differential corrected and passing |
| M2 | B.3.6.6 | Implemented; check and planted defects pass |
| M7 | B.4; Table B.9 | Implemented; boundary checks and planted defects pass |
| M8 | B.2 | Discard implemented and tested; counting withdrawn by ruling and documented |
| M1 | Table B.7 note d; B.3.6.4 | Implemented; both-cell checks and planted defects pass |
| M5 | B.3.5.9; Table B.7 | Implemented; unit and real-datapath checks and defects pass |
| M6 | Table B.7; B.3.6.6 | Shared buffer retained; finite capacity explicitly documented |
| M3 | B.3.6.1 | 32-bit period, MAC-plus-clock seed; six planted defects pass; pool bias documented |

## Implementation summary

The fabric allocator samples the programmed MAC at first enable, echoes the PROBE requested range in DEFEND,
rejects supplied ranges outside the dynamic pool and discards truncated PDUs without protocol effects.
It applies the remaining MAC comparisons and re-probes on link return.
One shared buffer retains a response while PROBE or ANNOUNCE drains.
A 32-bit generator of period 2^32 - 1 is seeded at first enable from the low 32 bits of MAC plus the existing PHC,
and continues across Release/Begin retries.
The buffer holds one pending or transmitting DEFEND; further PROBEs while occupied remain unsupported, including during DEFEND.
Full Table B.7 conformance is not claimed. B.3.6.6 defines the response action; B.3.6.3 defines probe-count decrement.

## Commits and changes before this resume

Line numbers are at the current head. Only `milan_datapath.sv` moved, by dev's merged lines.

| Commit | Artifact | Change |
|---|---|---|
| `39bf3d5f` | `hdl/ieee1722/maap/KL_maap.sv:352` | M4: sample the programmed MAC on first enable |
| `39bf3d5f` | `tb/verilator/maap/sim_integration.cpp:18` | Different programmed MACs draw different intervals through real CSRs |
| `39bf3d5f` | `tb/verilator/maap/integration.mk:8` | Derive real datapath sources and generate images |
| `74692746` | `hdl/ieee1722/maap/KL_maap.sv:408` | M2: echo requested start and all sixteen count bits |
| `74692746` | `hdl/ieee1722/maap/KL_maap.sv:300` | M7: reject supplied ranges outside the dynamic pool |
| `74692746` | `hdl/ieee1722/maap/KL_maap.sv:193` | M8: require every PDU byte and complete final beat |
| `74692746` | `tb/verilator/maap/Makefile:17` | External build directories and unpiped coverage execution |
| `19cc4eec` | `hdl/ieee1722/maap/KL_maap.sv:285` | M1: both remaining MAC-ordering cells |
| `19cc4eec` | `hdl/ieee1722/maap/KL_maap.sv:433` | M5: operational rising event revokes and re-probes |
| `19cc4eec` | `hdl/milan/milan_datapath.sv:7171` | Drive operational input from existing effective link |
| `19cc4eec` | `tb/verilator/maap/sim_integration.cpp:39` | Link-return datapath check |
| `832ee972` | `tb/verilator/maap/sim_main.cpp:462` | M6: deferred response, intact current frame and exact-once checks |
| `832ee972` | `tb/verilator/maap/sim_main.cpp:707` | Pending-response cancellation on reset/release/restart/link return |
| `bc89c6c1` | `tb/verilator/maap/sim_main.cpp:78` | Missing frames fail checks instead of crashing the harness |
| `bb1940966` | `hdl/ieee1722/maap/KL_maap.sv:218` | Share pending and transmitting DEFEND storage |
| `bb1940966` | `hdl/ieee1722/maap/KL_maap.sv:242` | Separate own-range snapshots preserve PROBE/ANNOUNCE while storing a response |
| `bb1940966` | `hdl/ieee1722/maap/KL_maap.sv:296` | Prevent overwriting pending or active response data |
| `bb1940966` | `tb/verilator/maap/sim_main.cpp:394` | Active DEFEND integrity at stalls after 0, 2, 4 and 7 beats |
| `bb1940966` | `tb/verilator/maap/sim_main.cpp:483` | A later conflicting PROBE cannot replace the first pending response |
| `bb1940966` | `tb/verilator/maap/mutants.py:39` | Two occupied-buffer defects; refresh existing mutation anchors |
| `bb1940966` | `docs/design/MAAP_FABRIC.md:145` | Explicit shared-buffer capacity and precise clause citation |
| `313b20b34` | `sw/firmware/ctrl/test/test_maap_differential.cpp:176` | Program 1,024 MAC identities before first enable; preserve every bound and draw assertion |
| `313b20b34` | `sw/firmware/ctrl/test/maap_differential.py:18` | Permit the self-test to substitute one copied RTL source |
| `313b20b34` | `sw/firmware/ctrl/test/maap_differential.py:65` | Plant a MAC-ignoring generator and require its named highest-draw failure |
| `963ad3b8e` | `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:5` | MAC ordering, first-enable seeding, bounded supplied ranges and operational input |
| `963ad3b8e` | `sw/firmware/ctrl/maap/README.md:189` | Programmed-MAC sweep and named negative control |
| `c1bc77f4` | `docs/design/MAAP_FABRIC.md:153` | Measured shared-buffer area; M6 retained under the ceiling |
| `a872917ca` | `hdl/ieee1722/maap/KL_maap.sv:141` | M3: 32-bit maximal recurrence, MAC-plus-clock seed, nonzero fallback, explicit low-bit pool draw |
| `a872917ca` | `hdl/milan/milan_datapath.sv:7172` | Existing synchronous PHC supplies the seed input |
| `a872917ca` | `tb/verilator/maap/Makefile:18` | Unit harness can clock selected generator states |
| `a872917ca` | `tb/verilator/maap/sim_main.cpp:50` | Fixture MAC preserves overlap-test margins under direct-sum seeding |
| `a872917ca` | `tb/verilator/maap/sim_main.cpp:856` | Transition-map order, zero/carry/wrap seed cases, Release/Begin continuity |
| `a872917ca` | `tb/verilator/maap/sim_integration.cpp:147` | Same MAC at two PHC times changes probe intervals |
| `a872917ca` | `tb/verilator/maap/mutants.py:39`, `:224` | Five generator/seed defects; missing clock contribution fails the datapath check |
| `a872917ca` | `sw/firmware/ctrl/test/test_maap_differential.cpp:72`; `maap_differential.py:65` | Explicit zero clock in the isolated sweep; MAC-ignoring defect uses the new seed expression |
| `a872917ca` | `docs/design/MAAP_FABRIC.md:97`; `KL_maap.md:28`; `sw/firmware/ctrl/maap/README.md:190` | Period/seed contract, cost, live-clock integration, retained pool bias |
| `395711960` | `hdl/milan/milan_datapath.sv:267` | Area comment points to the measured contract |

## Tests and planted defects

All existing clause checks remain; no threshold was loosened. A detected defect requires a successful build, process status 1 and its named failure.
Compiler failures and abnormal exits never count as detections. Every row below ran again at the merged head (campaign rc 0, 51 rows).

| Item | Named check | Planted defect | Result at M |
|---|---|---|---|
| M3 | M3 B.3.6.1 generator period is 2^32-1 | `m3_short_period` | Caught, rc 1 |
| M3 | M3 B.3.6.1 generator period is 2^32-1 | `m3_trap_outside_basis` | Caught, rc 1 |
| M3 | M3 B.3.6.1 first enable seeds MAC plus clock | `m3_ignores_clock` | Caught, rc 1 |
| M3 | M3 B.3.6.1 first enable seeds MAC plus clock | `m3_xors_clock` | Caught, rc 1 |
| M3 | M3 Release/Begin retains the generator sequence | `m3_reseeds_after_release` | Caught, rc 1 |
| M3 | M3 datapath: real-time clock changes probe intervals | `m3_datapath_ignores_clock` | Caught, rc 1 |
| M6 | M6 occupied response buffer preserves active DEFEND | `m6_overwrite_active_response` | Caught, rc 1 |
| M6 | M6 pending response preserves prober and requested range | `m6_replace_pending_response` | Caught, rc 1 |
| M6 | M6 pending response cancelled with allocation | `m6_pending_survives_release` | Caught, rc 1 |
| M6 | M6 busy PROBE gets DEFEND after wire is free | `m6_drop_busy_probe` | Caught, rc 1 |
| M6 | M6 pending response preserves prober and requested range | `m6_pending_source_not_saved` | Caught, rc 1 |
| M5 | M5 B.3.5.9 link return revokes and reprobes | `m5_ignore_link_return` | Caught, rc 1 |
| M5 | M5 B.3.5.9 link return restarts PROBE | `m5_level_restarts` | Caught, rc 1 |
| M5 | Link return starts four fresh PROBEs through the datapath | `m5_datapath_ignores_link` | Caught, rc 1 |
| M1 | M1 rProbe/PROBE lower MAC keeps range | `m1_probe_no_compare` | Caught, rc 1 |
| M1 | M1 rDefend/DEFEND lower MAC keeps range | `m1_defend_no_compare` | Caught, rc 1 |
| M8 | M8 B.2 truncated PROBE-state input has no effect | `m8_early_last_accepted` | Caught, rc 1 |
| M8 | M8 B.2 truncated DEFEND-state input has no effect | `m8_missing_bytes_accepted` | Caught, rc 1 |
| M7 | M7 Table B.9 invalid supplied range refused | `m7_accept_invalid_seed` | Caught, rc 1 |
| M7 | M7 Table B.9 valid supplied boundary retained | `m7_reject_valid_boundary` | Caught, rc 1 |
| M2 | M2 B.3.6.6 requested start echoes PROBE | `m2_own_requested_start` | Caught, rc 1 |
| M2 | M2 B.3.6.6 requested count echoes all 16 bits | `m2_own_requested_count` | Caught, rc 1 |
| M4 | Programmed MAC changes probe intervals through real CSRs | `m4_reset_time_sampling` | Caught, rc 1 |
| 1 | B.2.1 cdl 16 (Begin! PROBE 1) | `cdl_28` | Caught, rc 1 |
| 1 | B.2.1 DEFEND DA = PROBE source (above) | `defend_to_multicast` | Caught, rc 1 |
| 1 | B.2.1 DEFEND DA latched at send | `defend_destination_not_latched` | Caught, rc 1 |
| 1 | B.2.1 PROBE DA multicast (Begin! 1) | `every_frame_to_the_prober` | Caught, rc 1 |
| 2 | B.3.4.2 probe T < 600 ms (campaign) | `probe_draw_7_bits` | Caught, rc 1 |
| 2 | B.3.4.2 probe T > 500 ms (campaign) | `probe_base_500` | Caught, rc 1 |
| 2 | B.3.4.1 announce T > 30 s | `announce_base_3s` | Caught, rc 1 |
| 2 | B.3.4.1 announce T < 32 s | `announce_draw_11_bits` | Caught, rc 1 |
| 2 | B.3.4.1 announce T randomized | `announce_not_randomized` | Caught, rc 1 |
| 2 | B.3.4.2 probe T randomized (zero-seed MAC) | `zero_seed_freezes_the_probe_draw` | Caught, rc 1 |
| 2 | B.3.4.1 announce T randomized (zero-seed MAC) | `zero_seed_freezes_the_announce_draw` | Caught, rc 1 |
| 3 | B.2.7 ANNOUNCE conflict_* is not its range | `announce_judged_on_conflict_fields` | Caught, rc 1 |
| 3 | note b adjacent above: no conflict | `inclusive_range_end` | Caught, rc 1 |
| 3 | note b adjacent below: no conflict | `inclusive_range_start` | Caught, rc 1 |
| 3 | note b empty range: no conflict | `empty_range_conflicts` | Caught, rc 1 |
| 3 | T.B7 note d: lower MAC keeps range | `no_compare_mac` | Caught, rc 1 |
| 3 | T.B7 rAnnounce!/PROBE: no compare_MAC | `compare_mac_while_probing` | Caught, rc 1 |
| 3 | T.B7 rAnnounce!/DEFEND: re-address | `compare_mac_unreversed` | Caught, rc 1 |
| 4 | T.B7 Begin!: four PROBEs before ANNOUNCE | `three_probes` | Caught, rc 1 |
| 4 | T.B7 Begin!: first PROBE at once | `first_probe_after_a_timer` | Caught, rc 1 |
| 4 | T.B7 Restart!: first PROBE at once | `restart_probe_after_a_timer` | Caught, rc 1 |
| 4 | T.B7 probeCount!: ANNOUNCE at once (Begin!) | `announce_after_a_timer` | Caught, rc 1 |
| 0 | frame on the wire keeps its offset | `restart_rewrites_the_frame_on_the_wire` | Caught, rc 1 |
| 0 | B.2.8 conflict_count = overlap (below) | `overlap_count_to_our_end` | Caught, rc 1 |
| 0 | PROBE mid-frame: frame on the wire byte-identical | `defend_rewrites_the_frame_on_the_wire` | Caught, rc 1 |
| 0 | note b: this station's empty range never conflicts | `own_empty_range_conflicts` | Caught, rc 1 |
| control | unit harness unmodified | `clean` | rc 0 |
| control | datapath harness unmodified | `m4_datapath_clean` | rc 0 |

M8 compares malformed input with cycle-matched idle RX: lengths 1..41 and missing bytes 0..41, all three types, in PROBE and DEFEND states.

| Differential check | Planted defect | Result at M |
|---|---|---|
| Golden probe/announce wire | `wire`: control-data length 28 | Caught |
| Release and retry | `release`: remain in DEFEND | Caught |
| Nine Table B.7 cells | `maap-table-b7-0/1/2/6/7/8/12/13/14` | All nine caught |
| Strict probe timing | `probe-1ms`, `probe-500ms`, `probe-600ms` | All three caught |
| Fabric draw bound | `parent-probe-bound`: expected maximum 499 ms | Caught |
| Fabric probe count | `parent-probe-count`: expect four total frames | Caught |
| Highest draw across 1,024 programmed identities | `parent-ignores-mac`: constant seed | Caught at the named coverage assertion |

## Area attribution (assignment item 5)

Instrument: `syn/ooc/milan_datapath_ooc.tcl`, Arty 1x1 geometry, one synthesis and general thread.

| Cumulative item | Clause | MAAP LUT | MAAP FF | LUT vs base | FF vs base |
|---|---|---:|---:|---:|---:|
| base `6aa25dec` | Baseline | 439 | 280 | +0 | +0 |
| M4 | B.3.4 NOTE; B.3.6.1 | 460 | 281 | +21 | +1 |
| M2 | B.3.6.6 | 473 | 297 | +34 | +17 |
| M7 | B.4; Table B.9 | 483 | 297 | +44 | +17 |
| M8 | B.2, amended ruling | 498 | 298 | +59 | +18 |
| M1 | Table B.7 note d; B.3.6.4 | 491 | 298 | +52 | +18 |
| M5 | B.3.5.9; Table B.7 | 456 | 299 | +17 | +19 |
| M6 original, replaced | Table B.7; B.3.6.6 | 518 | 380 | +79 | +100 |
| M6 shared, from M5 | Table B.7; B.3.6.6 | 457 | 324 | +18 | +44 |
| M3, after shared M6 | B.3.6.1 | 441 | 340 | +2 | +60 |
| Merge `0df48637` | all, on dev `8b61b709` | 445 | 340 | +6 | +60 |

The first rows are historical recipe results (`fresh-receipts/area/`, `final-receipts/area/`); the last row is this resume's.

## Independent review coverage

| Lens | Covering round | Head |
|---|---|---|
| Conformance | Pending independent review | None |
| RTL | Pending independent review | None |
| Robustness | Pending independent review | None |
| Tests | Pending independent review | None |
| Docs | Pending independent review | None |

This is author evidence, not a review verdict. No merge readiness or physical acceptance is claimed.

## Receipts and resume boundary

- `merge-receipts/`: this resume's bounded, path-redacted receipts (681 files) with `PROVENANCE*.json` (raw and published digests).
  `SCRATCH-ARTIFACTS.json` lists the 34 artifacts over 200 KB (logs, timing reports, checkpoints) by size and digest; they stay in scratch.
  The executed bank scripts are included (`parent_bank.py`, `docs_bank.py`, `focus_bank.py`, `vivado_bank.py`, `maap_ooc_bank.py`, `record_merge.py`).
- `route-stop-receipts/`, `final-receipts/`, `consumer-resume-receipts/`, `resume-receipts/`, `fresh-receipts/`: earlier sessions, unchanged.
- `STOP-COMMENT.md` (route-floor STOP) and `STOP-COMMENT-6080309288.md` (documentation-scope STOP) are historical.
- `PR-BODY.md` is the unpublished PR body (`Closes #696`).
- Scratch worktrees (validation, parent sweep, gate trees at M and F, dev) are detached and outside the lane; the lane tree is clean.
- No push, PR creation or edit, merge, rebase, amend or history rewrite; no hardware access. No job remains running.
- Reviewers named by the ruling: [R558] internal, [R559] external.
