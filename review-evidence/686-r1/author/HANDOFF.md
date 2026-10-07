# [A565] HANDOFF: issue #686 (fabric MAAP engine vs IEEE 1722-2016 Annex B)

Status: REVIEW READY at `c7b69cd0fb2bdf980546ab413b3b82198267cbd8`. Every gate rc 0: maap suite and campaign, every datapath suite that instantiates `KL_maap`, the crflic campaign, ctrl + differential, lint, parser ratchet, docs and code-quality gates, Yosys OOC/portability, the shipping route (meets setup and hold floors), the standalone endpoints, the resource gate x3 and the re-record. No STOP condition: area within budget, route met, no register-map/filter/mailbox change, nothing outside scope. Not pushed (push and PR are outside this session's authority).

- Lane: branch `686-maap-annexb` from dev `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`
- Remote: `https://github.com/kebag-logic/milan-fpga.git` (confirmed)
- Assignment: issue #686 comment 6043036997. TAKEN: comment 6043296747. REVIEW READY: comment 6046944192 (head `c7b69cd0`).
- Authority: IEEE 1722-2016 Annex B (cited by clause; no text copied). Table B.7 was read from the rendered PDF page as well as the text extraction.
- Commits (one-line, no trailers, configured identity):
  - `a8364df1c` Conform KL_maap to IEEE 1722-2016 Annex B on the #686 items and grade each against its clause
  - `c6f5357a5` Document the Annex B contract of KL_maap and the deviations outside #686
  - `70297b2b4` Classify the maap mutation campaign as a DUT-source reader for the test-evidence ratchet
  - `7b2896568` Probe the crflic leg's Run B opening while KL_maap still probes, not after its ANNOUNCE
  - `c7b69cd0f` Re-record the resource gate's three endpoints after the KL_maap Annex B change, every tolerance, floor and ceiling unchanged

## Decisions made in public (TAKEN)

- Item 3 includes Table B.7 note b's conflict predicate. It is one predicate for PROBE, DEFEND and ANNOUNCE reception, so it became half-open (adjacent ranges no longer conflict, an empty range never conflicts) for all three.
- Item 3 includes the whole rAnnounce! row: compare_MAC (note d) in DEFEND, unconditional yield in PROBE.
- Out of the four items and NOT changed (recorded in MAAP_FABRIC.md and to be listed in REVIEW READY for a follow-up decision): compare_MAC in rProbe!/PROBE and rDefend!/DEFEND; the DEFEND requested_* echo (B.3.6.6); the generate_address generator/seed (B.3.6.1); no PortOperational! input (B.3.5.9); a PROBE parsed while a frame is on the wire is not defended.

## Changes (file:line at `7b2896568`)

| Item / purpose | Clause | file:line | Change |
|---|---|---|---|
| 1 cdl | B.2.1 | `hdl/ieee1722/maap/KL_maap.sv:114`, `:234` | `CDL_C` = 16 in every frame (was 28) |
| 1 DEFEND destination | B.2.1 | `KL_maap.sv:227-228`, `:320-324`, `:372` | RX captures the source MAC (bytes 6..11); DEFEND latches it into `tx_dst_r` and sends to it; PROBE/ANNOUNCE stay multicast |
| 2 probe timer | B.3.3 Table B.8, B.3.4.2 | `KL_maap.sv:120-124`, `:161` | draw 518 + lfsr[5:0] ms (was 500 + lfsr[6:0]) |
| 2 announce timer | B.3.3 Table B.8, B.3.4.1 | `KL_maap.sv:125`, `:162` | draw 30488 + lfsr[9:0] ms (was 3000 + lfsr[10:0]) |
| 3 range per message type | B.2.5-B.2.8, Table B.7 note b | `KL_maap.sv:164-190`, `:330-337` | one capture set: requested_* for PROBE/ANNOUNCE, conflict_* for DEFEND (same lanes, beat chosen by type) |
| 3 conflict predicate | Table B.7 note b | `KL_maap.sv:192-199` | half-open 17-bit overlap, zero counts never conflict |
| 3 DEFEND overlap | B.2.7, B.2.8 | `KL_maap.sv:200-203` | max/min overlap from the shared range |
| 3 compare_MAC | B.3.6.4, Table B.7 note d | `KL_maap.sv:205-210`, `:257-261` | octet-reversed compare; rAnnounce! in ANNOUNCE (DEFEND) re-addresses only when this station is not the lower |
| 4 four PROBEs | Table B.7, Table B.8 | `KL_maap.sv:118-119`, `:355`, `:365`, `:388-396` | `PROBE_SENDS_C` = 4 (ReserveAddress! sProbe + 3 retransmissions) |
| 4 first PROBE at once | Table B.7 ReserveAddress! | `KL_maap.sv:356` (Begin!), `:366` (Restart!) | timer loaded 0 |
| 4 ANNOUNCE at once | Table B.7 probeCount! | `KL_maap.sv:388-391` | ANNOUNCE state with timer 0 after the 4th PROBE |
| frame integrity | B.3.6.5-B.3.6.7 | `KL_maap.sv:213-220`, `:237`, `:373`, `:381` | `tx_off_r` latched at every send; a Restart! cannot rewrite a frame on the wire |
| one decision per cycle | Table B.7 / B.3.2 sequential execution | `KL_maap.sv:253-264`, `:345-399` | priority disable > Restart! > sDefend > timer send |
| banner | -- | `KL_maap.sv:6-49` | Annex B contract and remaining deviations |
| harness | all items | `tb/verilator/maap/sim_main.cpp` | re-pointed to the clauses (table below) |
| campaign | all items | `tb/verilator/maap/mutants.py` (new) | 22 planted defects + clean control |
| suite target | -- | `tb/verilator/maap/Makefile` | `all: run mutants`; `MAAP_RTL`, `MDIR`, `VERILATOR_JOBS` overrides |
| differential | items 1-4 | `sw/firmware/ctrl/test/test_maap_differential.cpp:112-206`, `:208-237` | #686 deltas become equalities; parent graded on Annex B |
| differential controls | -- | `sw/firmware/ctrl/test/maap_differential.py:4`, `:55-64` | test renamed `ProbeTimingAndCount`; parent bound 581, count 5 controls |
| consumer timing | -- | `tb/verilator/milan_dp/sim_crf_licence.cpp:39`, `:832-854`, `:868-870` | probe while the claim is in flight; ANNOUNCE check and offset read move to phase A |
| evidence ratchet | -- | `scripts/measure_test_evidence_readers.py:72-76` | disposition for the new DUT-source reader |
| resource baseline | -- | `syn/ooc/pp_resource_baseline.json` (records of `route-1x1`, `ooc-1x1`, `ooc-8x8`; `measured` notes at `:450`, `:917`, `:1374`) | written by `pp_resource_gate.py record --write` from this lane's recipe run; every tolerance, floor and ceiling unchanged |
| area budget | -- | `docs/design/AREA_BUDGET.md:102-104`, `:114-126`, `:132-137`, `:165`, `:198-199` | names the #686 record as the gate's record; headroom table, slice/critical-path lines, allocation figures and fall-limit sentence follow it; the third re-baseline's delta |
| findings | -- | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:5`, `docs/findings/README.md:25` | the 2026-10-05 D record is no longer called the current record |
| docs | -- | `docs/design/MAAP_FABRIC.md:36`, `:42-135`, `:138-139`, `:171-177` | Annex B contract, cells table, remaining deviations, history, TB bullet |
| requirement trace | FR-MAAP-01 | `docs/reference/FR_NFR.md:167` | ledger row names the conformed clauses and links the deviations |
| docs | -- | `docs/testing/TESTING.md:519`, `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:3-5`, `sw/firmware/ctrl/maap/README.md:165-187`, `tb/verilator/milan_dp/README.md:455`, `:961-962`, `tb/verilator/pp_shadow/README.md:363` | wording follows the new contract |

## Tests and the planted defect each catches

Harness `tb/verilator/maap/sim_main.cpp` (120 checks). Campaign `tb/verilator/maap/mutants.py` (22 mutants, each must exit 1 with its named `[FAIL]`).

| Item | Named check (sim_main.cpp line) | Planted defect (mutants.py name) |
|---|---|---|
| 1 | `B.2.1 cdl 16 (Begin! PROBE 1)` (:223) | `cdl_28` |
| 1 | `B.2.1 DEFEND DA = PROBE source (above)` (:309) | `defend_to_multicast` |
| 1 | `B.2.1 DEFEND DA latched at send` (:343) | `defend_destination_not_latched` (reads the live RX register) |
| 1 | `B.2.1 PROBE DA multicast (Begin! 1)` (:225) | `every_frame_to_the_prober` |
| 1 (B.2.8) | `B.2.8 conflict_count = overlap (below)` (:317) | `overlap_count_to_our_end` |
| 2 | `B.3.4.2 probe T < 600 ms (campaign)` (:506) | `probe_draw_7_bits` |
| 2 | `B.3.4.2 probe T > 500 ms (campaign)` (:505) | `probe_base_500` |
| 2 | `B.3.4.1 announce T > 30 s` (:295) | `announce_base_3s` |
| 2 | `B.3.4.1 announce T < 32 s` (:296) | `announce_draw_11_bits` |
| 2 | `B.3.4.1 announce T randomized` (:298) | `announce_not_randomized` |
| 3 | `B.2.7 ANNOUNCE conflict_* is not its range` (:375) | `announce_judged_on_conflict_fields` (the old behaviour) |
| 3 | `note b adjacent above: no conflict` (:378) | `inclusive_range_end` |
| 3 | `note b adjacent below: no conflict` (:381) | `inclusive_range_start` |
| 3 | `note b empty range: no conflict` (:384) | `empty_range_conflicts` |
| 3 | `T.B7 note d: lower MAC keeps range` (:372) | `no_compare_mac` |
| 3 | `T.B7 rAnnounce!/PROBE: no compare_MAC` (:404) | `compare_mac_while_probing` |
| 3 | `T.B7 rAnnounce!/DEFEND: re-address` (:390) | `compare_mac_unreversed` |
| 3/4 | `frame on the wire keeps its offset` (:421) | `restart_rewrites_the_frame_on_the_wire` |
| 4 | `T.B7 Begin!: four PROBEs before ANNOUNCE` (:251) | `three_probes` |
| 4 | `T.B7 Begin!: first PROBE at once` (:249) | `first_probe_after_a_timer` |
| 4 | `T.B7 Restart!: first PROBE at once` (:396) | `restart_probe_after_a_timer` |
| 4 | `T.B7 probeCount!: ANNOUNCE at once (Begin!)` (:253) | `announce_after_a_timer` |

The campaign refuses to run unless every item 1-4 has a mutant, and every anchor must occur exactly once. A build failure or abnormal exit never counts as a kill. First campaign run caught 22/23 rows: `announce_draw_11_bits` escaped its named check because the wait budget equalled the bound, so the over-long interval timed out instead of being measured. Budgets were widened past the bounds (`sim_main.cpp:33-36`); the rerun caught 23/23.

Differential (`maap_differential.py --self-test`): 12 positive cases; 16/16 controls caught (core wire, release, nine Table B.7 cells, 1/500/600 ms probe defects, parent bound 581 -> 499, parent count 5 -> 4).

crflic leg (`make -C tb/verilator/milan_dp crflic-mutants`): pending in the chain (see gate table).

## Coverage table

| Item | Clause | Graded by | Defects caught |
|---|---|---|---|
| 1 | B.2.1 | golden frames (B.2/Figure B.1) for every PROBE/ANNOUNCE of two walks; cdl in PROBE, ANNOUNCE, DEFEND; DEFEND DA from two probers and under backpressure; multicast after a DEFEND; differential raw-frame equality with the core | 5 |
| 2 | B.3.3/B.3.4 | 456 probe intervals over 150 walks (517.2..581.0 ms observed, both ends of the draw reached); 24 announcement intervals (30.53..31.50 s observed); differential parent intervals over 1024 phases (517.2..581.1 ms) | 5 |
| 3 | B.3.2/Table B.7 | every conflict cell in both states, note b edges (adjacent above/below, empty, one shared address), compare_MAC both ways with octet-reversal sensitive MACs, conflict fields ignored for ANNOUNCE | 8 |
| 4 | Table B.7 | first PROBE latency at Begin!, Restart! and the seeded Begin!; 4 PROBEs then ANNOUNCE at once in 152 walks | 4 |

Line coverage (`make -C tb/verilator/maap coverage`): `KL_maap.sv` 100.0 % (167/167), gate 95 %: PASS.

## Gate table

| Gate | Command | rc | Result |
|---|---|---|---|
| maap suite | `make -C tb/verilator/maap` | 0 | 120 checks 0 failures; mutants 23/23 (tally 143 checks) |
| maap coverage | `make -C tb/verilator/maap coverage` | 0 | 100.0 % (167/167) |
| milan_dp | `make -C tb/verilator/milan_dp` | 0 | 12,065 checks, 0 failures, 1,985 s (first run rc 2 on the crflic leg, fixed in `7b2896568`) |
| pp_shadow | `make -C tb/verilator/pp_shadow` | 0 | 2,184 checks, 0 failures |
| capture_coherence | `make -C tb/verilator/capture_coherence` | 0 | 21,194 checks, 0 failures |
| milan_dp_mclk | `make -C tb/verilator/milan_dp_mclk` | 0 | 168 checks, 0 failures |
| milan_dp_render | `make -C tb/verilator/milan_dp_render` | 0 | 334 checks, 0 failures |
| suite tally | `scripts/suite_tally.py` over the six logs | 0 | 36,088 checks, 0 in-suite failures |
| crflic campaign | `make -C tb/verilator/milan_dp crflic-mutants` | 0 | obj_crflic leg 417 checks, 0 failures; campaign 7/7 (control passes, 6 mutants caught), 747 s |
| ctrl suite | `test_ctrl_firmware.py --require-rv32` (verified SDK) | 0 | PASS |
| differential | `maap_differential.py` / `--self-test` | 0 / 0 | 12/12; 16/16 controls |
| lint ratchet | `scripts/lint_rtl.py --check` | 0 | 90 <= 90; maap 1 <= 1 (pre-existing `rx_msg_r` truncation) |
| parser ratchet | `scripts/xvlog_gate.py --check` (Vivado 2026.1 xvlog, under the lock) | 0 | PASS: 81 hdl/ + 52 pinned files; 0 hdl/ findings; 2 pre-existing pinned-processor findings == ratchet; 218 s |
| Yosys OOC | `syn/yosys/ooc.sh KL_maap` | 0 | 474 LUT / 278 FF / 59 CARRY4 (dev 637 / 268 / 74) |
| Yosys portability | `syn/yosys/run.sh --top KL_maap` | 0 | PASS, 1,949 cells; tied-input and tap-purity PASS |
| test evidence | `measure_test_evidence.py --check` / `--selftest` | 0 / 0 | 0 unexplained readers (`--check` re-run 0 at `c7b69cd0`) |
| docs | docs_check, check_em_dash (base e21c1ca0) + selftest, gen_toc check/anchors, doc_style, doc_paths, module_matrix, feature_status, DOC_MAP, solution/submodule docs | all 0 | at `7b2896568` and again at `c7b69cd0` (after the area-budget and findings edits) |
| code quality | naming, port_contracts, fail_fast, todo_ownership, hygiene, sv/cpp/py idiom, rtl_source_lists, pp_srcs, `git diff --check e21c1ca0 HEAD` | all 0 | at `7b2896568` and again at `c7b69cd0` |
| shipping route | recipe "Integrated measurements", 1x1 `endstation_ax7101_1x1_tdm8`, `place_design -directive ExtraPostPlacementOpt`, Vivado 2026.1 | 0 | 1,891 s. WNS +0.317 ns (floor +0.03), TNS 0; WHS +0.036 ns (floor 0), THS 0; WPWS +0.264 ns; 100,981/100,981 routable nets routed, 0 routing errors. 50,088 LUT / 54,188 FF / 15,843 slices / 74 RAMB36 / 27 RAMB18 / 14 DSP |
| standalone endpoints | recipe "Standalone measurements": 1x1 with `--integrated-clock`; 8x8 RTL elaboration then standalone | 0 | 2,548 s. ooc-1x1 23,178 LUT / 19,776 FF / 16 / 3 / 8; ooc-8x8 29,853 / 27,370 / 21 / 5 / 8 (both identical to the previous record) |
| resource gate | `pp_resource_gate.py check <dir> --endpoint` route-1x1 / ooc-1x1 / ooc-8x8 against the 2026-10-05 record | 0 / 0 / 0 | PASS x3 (route: LUT -230, FF -26, SLICE +54 of +80, WNS +0.209, WHS 0) |
| resource record | `record --write` x3, then `check-baseline`, then `check` x3 against the new record | 0 x3, 0, 0 x3 | baseline PASS: 3 endpoints; rechecks PASS |
| gate self-tests | `pp_resource_gate.py --selftest`, `pp_resource_gate_mutants.py` | 0 / 0 | 260 arms + 500 generated cases PASS; control passes, all 174 mutants fail |

Head each gate saw: milan_dp (20:35-21:08) and the crflic campaign ran at `7b2896568`. The other Verilator suites, ctrl, lint, Yosys and the first docs pass ran at `70297b2b4`. From `70297b2b4` to `c7b69cd0`, only `tb/verilator/milan_dp/{sim_crf_licence.cpp,README.md}` (built only by `tb/verilator/milan_dp/Makefile`), the resource JSON and three docs change. The route, standalone endpoints and parser ratchet read the tree at `7b2896568`, whose RTL is that of `c7b69cd0`. The docs/code-quality pass and `check-baseline` re-ran at `c7b69cd0`.

## Area

Yosys OOC (`syn/yosys/ooc.sh KL_maap`, the repository's OOC measurement): dev 637 LUT / 268 FF; branch 474 LUT / 278 FF. Delta -163 LUT / +10 FF, within +40 / +40. One shared range register and one comparator set replace the two 48-bit range captures and two inclusive predicates; the source MAC, DEFEND destination and frame offset latches add FFs.

Vivado in context (shipping route hierarchy, `milan_datapath/g_maap.maap_engine`): branch 435 LUT / 279 FF. Dev's figure is 479 LUT / 267 FF in `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:223` (dev `241f9184`; `KL_maap.sv` is unchanged from 2026-08-25 to `e21c1ca0`). Delta -44 LUT / +12 FF, within +40 / +40.

Image against the 2026-10-05 record (which spans dev `506d91db`..`e21c1ca0` as well as this change): -230 LUT, -26 FF, +54 slices (tolerance +80), WNS +0.108 -> +0.317 ns. Slice headroom is now 7 of 15,850 (was 61): a packing effect, with LUTs and FFs both lower. The worst setup path moved to the CPU's DMA bridge (21 logic levels).

Evidence (scratch, not copied here; sha256, bytes):

| Artifact | sha256 | bytes |
|---|---|---|
| route `baseline.log` | `94ea82713519d3c2c4abf02212a7baa32e2f920531196f2d85f56e6de0726d90` | 977,052 |
| route `baseline_timing.rpt` | `0267fd270778a8d537ec9f558a7baeda0afd8e184097baaf759e0f0ec2f256b7` | 1,277,551 |
| route `baseline_utilization.rpt` | `3002be04511894c51ade488389aa533e0867a9b111815e93d0513aa9f34dfd2d` | 13,319 |
| route `alinx_ax7101_route_status.rpt` | `d7846c034fbf8b962f2695ef7ef90c0ce5eb1b048c90ae5fc7888854f5c6d1b8` | 651 |
| route `baseline_hierarchy.rpt` | `57c9f897433b75feeca45219af4c2b22160d7f9e090d6cb7dc25e562eaa0daed` | 46,405 |
| ooc-1x1 `baseline.log` | `60794406ac1d2208b44e3caa022ef162f850647a921ee5081758da89a0106540` | 312,103 |
| ooc-1x1 `baseline_utilization.rpt` | `ef16c058577ba7f86bfd6a4fcf05ba11d9c92e423aba6ff0ffae545076a58cff` | 9,297 |
| ooc-8x8 `baseline.log` | `19aef6f97537e0af187bc673f093d75d7d33ba7f163dffab731306c913c16951` | 315,788 |
| ooc-8x8 `baseline_utilization.rpt` | `a2bb4512f3f5c2dc80985441e2c52af34c46340b7d97404fdd44db3dd0447b2f` | 9,297 |
| xvlog gate log | `4bf5acfc38c97c5c8e3f36282fb007db13bf83e7cc4a98f097edd9881a7732d3` | 1,025 |

## Incidents (process handling, no evidence affected)

- The first `crflic-mutants` start inherited no `VERILATOR` (an `export` placed before one `&` job applied only to that job) and began re-Verilating `obj_crflic` with the system 5.052 while the full milan_dp rerun started. Both were stopped, `obj_crflic` was deleted, and milan_dp was rerun from scratch with the pinned 5.050; every suite log records 5.050.
- A later chain was believed dead because this host rewrites `ps` output through a filter, so `ps | grep` showed nothing. Its script file was then overwritten while bash was still reading it, which started a second campaign in the same directory. Both process groups were terminated (their temp dirs cleaned by the driver's handler), `obj_crflic` was deleted again, and one chain was restarted from a read-only copy (`chain-run2.sh`). No route or standalone Vivado step had started. Process checks now use `/proc` and `pgrep -a`.
- The first shipping route (lock acquired 21:44:20) was OOM-killed at 21:48 with the whole session when Vivado's parallel synthesis took the 12 GB unit to its cap. No report was written. The run's directory was discarded and a fresh one rebuilt from the 19:58 export (the RTL is unchanged since: `7b2896568` touches only the crflic testbench and a README), and the route restarted at 21:50:50 under a 20 GB unit with a unit-scoped memory guard (`chain-mem3.log`).
- Memory on the restarted route: synthesis runs seven parallel worker processes beside the main Vivado (about 2.2 GB each). The unit peaked at 18.44 GB memory.current / 17.43 GB anonymous at 21:59:05 (samples 21:58:50 17.76 GB, 21:59:20 14.05 GB), about 1.4 GB over the 17 GB target for under 45 s; the first guard's stop threshold (18 GiB anonymous) was not reached. The guard was then tightened (5 s polling, page-cache reclaim above 16 GB, stop this unit's Vivado above 17 GB anonymous); synthesis finished at 22:00 and the unit fell to 6.5 GB for implementation. The guard never fired. A first pattern-based stop of the old logger also ended two idle tool shells in this unit; the chain and Vivado were unaffected (checked through `cgroup.procs`).

## Resources and hygiene

- Toolchains, the verified RV32 SDK copy, exports, logs and checkpoints stay in scratch; nothing over 200 KB here.
- Memory: the Verilator suites stayed under 9 GB (max about 4.1 GB in the 12 GB unit). The Vivado steps ran in the 20 GB unit one at a time under the lock: route synthesis peaked at 18.44 GB current / 17.43 GB anonymous for under 45 s (see Incidents), the 8x8 standalone at 16.18 GB / 14.53 GB, implementation at about 7 GB.
- The recipe's temporary symlinks (`sw/builder/out`, `configs/generated/{ltn_rom,ucode}.hex`) were removed after the last Vivado step, before the last commit; `git status` is clean at `c7b69cd0`.
