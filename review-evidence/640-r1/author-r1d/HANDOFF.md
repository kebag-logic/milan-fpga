# [A540] #640 stage 1: Mark II area plan -- HANDOFF

Current status: Round 1c REVIEW READY at `39258a1486897127288f82fbb1b86333febf6f00`.
The Round 1c section below owns current estimates and validation.
Round 1b supplies unchanged source measurements; its prior estimates are superseded.
Earlier sections are retained as Round 1 history and do not define the current ledger or unresolved decisions.

## Round 1 historical handoff

Round 1 status: DONE (STOP posted 5990726992). Measurement and plan only; no RTL, configuration, register-map or parameter change.

- Lane: #640 stage 1, executor [A540], reviewers [R492] internal, [R493] external.
- Assignment followed: #640 comment 5988586965 (the lane comment naming [A540]). The pointer handed to this session,
  #658 comment 5988328859, is the #658 lane for [A539]; noted in TAKEN 5988601365.
- Branch `640-mark2-plan` from dev `e617275074e370cec342af99b929e2588fc8d43f`, two one-line commits, not pushed:
  - `8d3be7343126b6e23ea2f0fe1e202802dfe753bd` Plan Mark II's way to NFR-RES-01 ... (#640)
  - `06f5e7e55be79f9184854d9c84a72f98ab0527cb` Start the Mark II ledger from the second pin adoption's measured route ... (#640)
- Committed: `docs/design/MARK_II_AREA_PLAN.md` (new, 629 lines). No measurement script: `syn/resmap/route_map.tcl` +
  `resmap_map.py` (#649) and the #234 recipe and gate cover the measurement; the plan documents the scratch-record step
  that lets them map a head the gate's record does not describe.
- Worktree clean after the run (recipe symlinks unlinked). Scratch `$VALIDATION_STORAGE/640-a540/` (413 MB kept as evidence:
  `meas/`, `route-map/`, `cpu/`, gate logs; the SDK install and standards text were removed).

## Baseline (source checkpoints)

Integrated route of the shipping `endstation_ax7101_1x1_tdm8` image at `e6172750`, #234 recipe unchanged, Vivado 2026.1
build 6511674, `xc7a100t-fgg484-2`, 50 MHz datapath. No routed checkpoint of this tree existed on the host (only
processor-lane scratch parents and the in-flight #661 adoption), so it was routed fresh.

| Source | Path (scratch) | SHA-256 | Bytes |
|---|---|---|---:|
| Routed checkpoint | `meas/ax7101/gateware/alinx_ax7101_route.dcp` | `ac7a716819091b492b23efc8996b4bc93f13bc9866cf8f3cc9110e2d43c37658` | 110,137,721 |
| Route log | `meas/ax7101/gateware/baseline.log` | `16cbfa00cca1f514a45ac477b3ab60ee95acb86c99344031f592456a815fc4d7` | 816,503 |
| Image manifest | `meas/ax7101/gateware/baseline_images.json` | `1fab9d504ab04761ea25637cf3f254687309e20b564a4b975c1385492b4daff6` | - |
| Standalone 1x1 checkpoint | `meas/ax7101-ooc/baseline_synth.dcp` | `c7a692f9132feda2035e256046afcddc9a9d284c4fc5242c71a15d752f08978d` | 9,407,818 |
| Standalone log | `meas/ax7101-ooc/baseline.log` | sha256 first 16 `96910f8fcb64bf1c` | 248,489 |
| Route map (175 blocks, every tie held) | `route-map/out/rows_all.tsv`, `map.json` | - | - |

| Endpoint | LUT | LUTRAM | FF | Slice | RAMB36 | RAMB18 | DSP | WNS / WHS ns |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Route, gate record (dev `54643724`) | 50,767 | - | 59,634 | 15,832 | 79 | 27 | 14 | +0.193 / +0.024 |
| Route, this head `e6172750` | 50,702 | 2,228 | 59,677 | 15,828 | 79 | 27 | 14 | +0.244 / +0.036 |
| Standalone 1x1, this head (= gate record) | 24,332 | 1,242 | 25,345 | - | 21 | 3 | 8 | estimate only |
| Route, second pin (#661 REVIEW READY 5990292142, head `42f65447`) | 50,318 | - | 54,214 | 15,789 | 74 | - | - | +0.108 / +0.036 |

- Gate `check --endpoint route-1x1`: rc 0 (LUT -65, FF +43, slices -4; route complete, 106,639/106,639 nets).
  `check --endpoint ooc-1x1`: rc 0, no movement. All four signoff corners meet the build gate.
- Critical path `u_pp/u_rx_validator/hdr_ctlr_eid_r_reg[11]` -> `u_pp/u_tx_arbiter`, 39 levels, 19.443 ns, 73 % routing.
- Top-level split at this head: processor wrapper 24,051 (47.4 %), gPTP plane 4,999, CSR 2,907, the rest of the
  datapath 10,181, SoC side 8,564 (LiteX top 4,833, control hart 3,522).
- #661's measured image is 358 LUT above the three area lanes' additive projection (49,960); the plan starts from 50,318.

## Inventory (plan section "Inventory")

46 hierarchies above 500 routed LUT at this head; every one is in the plan with function and clause, construction, and
the standard-set versus implementation-chosen part. Largest: AECP 7,451 (dispatch cone 1,798, micro-coded engine 1,720,
saved-state writer 1,405, dynamic state 1,265 routed / 152 standalone, descriptor store 974); notification 3,118
(16 x 128-bit registry in flops, 16 parallel compares); SRP 4,219 (encoder 1,320, glue and timer FIFOs 862, FSMs
612 + 419); gPTP plane 4,999 (its micro-coded engine 2,083); CSR 2,907; ACMP listener 1,414 (already one executor over
records); timer service 884; dispatch 775; binding store 790; originator 721; ACMP talker 689. Clause numbers checked
against the IEEE 1722.1-2021, 1722-2016, 802.1Q-2018 and Milan v1.2 texts (1722-2016 clause 5 corrected to clause 4).

## Levers (saving central and range in routed LUT; basis; risk; verification)

| Lever | Saving | Basis | Risk | Verification cost |
|---|---|---|---|---|
| L1a shared micro-coded sequencer for ADP, ACMP, originator, notification, AECP dispatch/dyn state, both record managers | 4,700 (2,800-6,400) | standalone rows of the displaced blocks with second-pin changes, shares 0.4-0.7, engine cost 1,068 OOC / 1,608-1,720 measured, processor record scenario C and its silicon substitution (-3,459 synth); no prototype | high | every processor suite and campaign at its count, transaction-level equivalence, consumer set of 17, pp_shadow, nvm_cosim, milan_dp, NVM capture, bench suite |
| L1b SRP onto the sequencer | 1,300 (700-1,700) | standalone SRP rows, shares 0.3-0.7 | medium-high | SRP suites/campaigns, pp_top, bench SRP items |
| L2 slow path to the RISC-V | 5,500-6,500 (four named functions); up to ~15,000 whole plane | standalone rows as upper bound less mailbox | very high; blocked by REQUIREMENTS s.1, NFR-SCOUT-02/03, ownership rule | suites replaced by firmware tests: counts not holdable |
| L3 block RAM for tables outside L1 | 800 (500-1,200) | routed LUTRAM per block, #639's measured exchange, processor record precedent | medium | per-array lockstep, owning suites |
| L4 widths from the entity model | 200 (100-400) | #649 measured per-unit sensitivities | low | owning suites |
| L5 remaining #233 items | 30-100 | measured (u_vlan 138 routed; #649 sweep) | low | SRP, dispatch, notify suites |
| L6 diagnostics off in shipping build | 700 (650-750) | routed latency taps 672, trace ring 37, probes ~12 | low; product decision | builder bank, shape gates, milan_dp both ways, CSR bench |
| L7 SRP shared evaluator only | 450 (300-600) | #638/#234 per-context marginals 212/227, #230's 200/210 | medium | SRP suites/campaigns |
| L8 CSR read path | 600 (400-1,000) | routed 2,907; #649 OOC fit; no prototype | medium | CSR bench, tcam_csr, milan_dp, firmware host tests |
| L9 datapath per-stream contexts in RAM | 600 (400-900) | routed blocks; #649 per-stream marginals | medium | avtp_rxmon, tkdiag, chmap_capture, render_setpoint, milan_dp |
| L10a gPTP tables | 500 (300-700) | routed rows (464 LUTRAM in the engine) | medium | gPTP processor suites, gptp_* parent suites |
| L10b one engine for gPTP and AECP | 1,200 (900-1,500) | smaller engine's routed 1,720 less arbitration | high | as L10a plus turnaround proof |
| L11a on-chip main memory (drop DDR3) | 1,600 (1,200-2,000) | #649 census: 823 + 873 LUT cells, 2,599 FF | high; needs #70 staging resize and memory-map change | firmware host tests, nvm_cosim, nvm_capture_cpu, bench boot |
| L11b smaller cacheless RV32I core | 1,700 (1,300-2,200) | MEASURED here, OOC AreaOptimized_high: VexiiRiscv netlist 3,066 LUT / 5,017 FF / 4.5 tiles (about 600 LUT DMA bridges), VexRiscv Min 843 / 791 / 1, PicoRV32 minimal 1,051 / 549 / 0; 300-600 kept for LiteX interconnect | high | check_nvm_capture (8x8 <= 24.5 ms), boot, firmware tests |
| L12 excluded prunes | - | RX filter (REQ-MAC-02 MUST), loopback (AEM), MAAP, servo/meter, CRF, render, controllers < 16 | - | - |

No lever has a protocol-visible wire effect; L1 and L7 change internal latency (decision D3).

## Lane sequence (central, from #661's measured 50,318)

| Lane | Weeks | Levers | Repository | Own target | Image after |
|---|---|---|---|---:|---:|
| M0 | before 1 | #661 (at review) | parent | - | 50,318 |
| M1 | 1-2 | L6 | parent (+ processor trace-ring parameter) | -700 | 49,618 |
| M2 | 1-4 | L3 | processor, gPTP processor, parent | -800 | 48,818 |
| M3 | 1-8 | L1a + L4 + L5, three sub-lanes | processor | -4,950 | 43,868 |
| M4 | 3-8 | L1b (or L7) | processor | -1,300 | 42,568 |
| M5 | 2-6 | L8 | parent | -600 | 41,968 |
| M6 | 2-6 | L9 | parent | -600 | 41,368 |
| M7 | 3-6 | L10a | gPTP processor, parent | -500 | 40,868 |
| M8 | 2-8 | L11a + L11b | parent SoC, firmware | -3,300 | 37,568 |
| M10 | 6-9 | L10b | gPTP processor, processor | -1,200 | 36,368 |
| M9 | 9-10 | adoptions, route, closure, gate re-record | parent | to <= 38,040 | - |

Result: 37,568 at central without M10 (472 under the limit, 1.2 %); 36,368 with M10 (228 above the 36,140 target).
No priced sequence reaches the 5 % margin at central estimates; without the SoC lane M8 the image stays near 40,900.
Decisions D1-D9 are listed in the plan (equivalence bar, diagnostics, internal timing, on-chip memory, control core,
engine sharing, the re-baseline rule versus the assignment's "re-record only at the target", the margin, the RISC-V
direction). Follow-up noted, not edited: AREA_BUDGET.md line 138 still says "after Instrument verification".

## Gates (at head `06f5e7e5`, base `e6172750`; all foreground, no pipes; pinned Markdown venv whose lock hash matches)

| Gate | rc | Command |
|---|---:|---|
| docs_check | 0 | `python3 scripts/docs_check.py` |
| docs_check_nogit | 0 | `env GIT_DIR=/dev/null python3 scripts/docs_check.py` |
| feature_status | 0 | `python3 scripts/check_feature_status.py` |
| feature_status_self | 0 | `python3 scripts/check_feature_status.py --self-test` |
| em_dash | 0 | `python3 scripts/check_em_dash.py --base e617275074e370cec342af99b929e2588fc8d43f` |
| em_dash_self | 0 | `python3 scripts/check_em_dash.py --selftest` |
| doc_style | 0 | `python3 scripts/check_doc_style.py` |
| doc_style_self | 0 | `python3 scripts/check_doc_style.py --selftest` |
| gptp_docs | 0 | `python3 scripts/check_gptp_docs.py` |
| gptp_docs_self | 0 | `python3 scripts/check_gptp_docs.py --selftest` |
| doc_map | 0 | `python3 docs/DOC_MAP.gen.py --check` |
| doc_map_self | 0 | `python3 docs/DOC_MAP.gen.py --selftest` |
| timesync_chain | 0 | `python3 docs/diagrams/timesync_chain.gen.py --check` |
| timesync_chain_self | 0 | `python3 docs/diagrams/timesync_chain.gen.py --selftest` |
| solution_docs | 0 | `python3 scripts/check_solution_docs.py` |
| solution_docs_self | 0 | `python3 scripts/check_solution_docs.py --selftest` |
| submodule_diagram | 0 | `python3 docs/diagrams/submodule_boundaries.gen.py --check` |
| submodule_diagram_self | 0 | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` |
| submodule_docs | 0 | `python3 scripts/check_submodule_docs.py` |
| submodule_docs_self | 0 | `python3 scripts/check_submodule_docs.py --selftest` |
| diagram_pngs | 0 | `python3 scripts/check_diagram_pngs.py` |
| diagram_pngs_self | 0 | `python3 scripts/check_diagram_pngs.py --selftest` |
| module_matrix | 0 | `python3 docs/traceability/gen_module_matrix.py --check` |
| baremetal | 0 | `python3 scripts/check_baremetal_only.py --check` |
| baremetal_self | 0 | `python3 scripts/check_baremetal_only.py --selftest` |
| doc_paths | 0 | `python3 scripts/check_doc_paths.py` |
| archive | 0 | `python3 scripts/check_archive.py` |
| archive_self | 0 | `python3 scripts/check_archive.py --selftest` |
| toc_self | 0 | `python3 scripts/gen_toc.py --selftest` |
| toc_anchors | 0 | `python3 scripts/gen_toc.py --verify-anchors` |
| toc_check | 0 | `python3 scripts/gen_toc.py --check` |
| todo_ownership | 0 | `python3 scripts/check_todo_ownership.py` |
| hygiene | 0 | `python3 scripts/check_hygiene.py --check` |
| diff_check_base | 0 | `git diff --check e617275074e370cec342af99b929e2588fc8d43f HEAD` |
| diff_check_tree | 0 | `git diff --check` |

35 of 35 rc 0 (logs in `$VALIDATION_STORAGE/640-a540/gates-r2/`; the same 35 were rc 0 at `8d3be734` too, `gates-8d3be734/`).
em-dash judged 617 added lines in 1 page at the first commit; doc paths resolved 926 citations; docs_check 0 findings
with and without git. Not run, because the commit touches no file they read: Verilator suites, Yosys, builder bank,
NVM gates, idiom ratchets other than hygiene/TODO.

## Run receipts

| Run | rc | Duration | Log sha256 (16) | Bytes |
|---|---:|---|---|---:|
| Export `milan_soc.py` without `--build` | 0 | ~2 min | `437f11cf5ddd1ce4` | 60,087 |
| Route 1x1 (lock 08:40:51-09:33:19, waited 75 min) | 0 | 52.5 min | `16cbfa00cca1f514` | 816,503 |
| Standalone 1x1, 20 ns (lock 09:41:44-10:02:46) | 0 | 21.0 min | `96910f8fcb64bf1c` | 248,489 |
| Route map `route_map.tcl` (10:03:34) | 0 | 0.5 min | `0881e5e4dcd735f2` | 6,929 |
| `resmap_map.py map` tie | 0 | - | `2e789a95f2c5064e` | 107 |
| Gate route-1x1 vs record | 0 | - | `b82def0b753d4fd6` | 1,051 |
| Gate ooc-1x1 vs record | 0 | - | `b2469c8f91130e4b` | 371 |
| Core pricing VexiiRiscv / VexRiscv Min / PicoRV32 (10:06:30-10:09:38) | 0/0/0 | ~1 min each | `f933a1b83daf101d` / `75ee4a4f8a55d345` / `fdbb010a293c3750` | 103,103 / 32,238 / 36,210 |

The service unit reached its 12 GB cap during the route's parallel synthesis (memory.events max 32,716, oom 0,
oom_kill 0). Only the echoed `Synth 8-4445` severity command matches in the route and standalone logs.

## Open questions for the manager

1. D1-D9 in the plan, D7 (gate re-baseline rule during Mark II) and D8 (margin) first.
2. The plan uses #661's REVIEW READY figures (head `42f65447`, not merged); if #661's reviewed head moves the route,
   the ledger's start moves with it.
3. AREA_BUDGET.md's "after Instrument verification" wording is stale since the owner's 2026-10-05 correction.

## Log

- 07:20 start; remote and HEAD confirmed.
- 07:27 TAKEN posted: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5988601365
- No routed checkpoint matching `e6172750` exists on the host. Dev moved since the gate record (dev `54643724`):
  `KL_crf_rx.sv` (#653, functional, outside the wrapper), `KL_nvm_backend.sv` (localparam only), `milan_datapath.sv`
  (comment only), builder (generation-time refusal). So a fresh route and 1x1 OOC were run per the recipe.
- Export at `e6172750` rc 0 (scratch `$VALIDATION_STORAGE/640-a540/meas`, own verified SDK install). Measurement chain
  `$VALIDATION_STORAGE/640-a540/chain.sh` queued on `$VIVADO_LOCK` at 07:25 (another lane's route held it).
- Normative constraints found while reading (they shape the levers): REQUIREMENTS section 1 (fabric owns MAAP and
  1722.1 processing), NFR-SCOUT-01/02/03 (one cacheless RV32I hart; protocol control keeps its fabric owner; no
  packet deadline on firmware latency), ARCHITECTURE_HW_SW_SPLIT section 1, REQ-MAC-02 (RX filter is a MUST),
  FR-CTRL-03 (16 controllers). `talker_diag` is Milan Table 5.4 counters, not diagnostics.
- Conflict to publish: AREA_BUDGET's rule "a merge that moves the shipping image records its own re-baseline" vs the
  assignment's "resource gate re-recorded only in the lane that reaches the target" (decision D7 in the plan).
- #661 has published no measured delta yet (only TAKEN 5986101343); the plan projects from the three area lanes'
  own route deltas (#232 -763, #230 -429, #639 -282 against one base route of 51,434) and labels it a projection.
- No new measurement script: `syn/resmap/route_map.tcl` + `resmap_map.py` (#649) and the #234 recipe/gate cover the
  measurement; the plan documents the scratch-record step needed to map a head the gate record does not describe.
- 08:40:51 the route took the lock (other lane's route had held it since 07:13); synthesis done 08:52; placement 08:54.
  The service unit sat at its 12 GB cap during parallel synthesis (memory.events max climbing, oom 0); nothing else
  heavy was run beside it.
- Follow-up queued (`follow.sh`): scratch-baseline record of this route, `route_map.tcl` (#649) under the lock,
  `resmap_map.py map`, then a CPU-core pricing run (VexiiRiscv shipping netlist, VexRiscv Min, PicoRV32 minimal)
  under one hold of the lock, to give L11b a measured basis.
- AREA_BUDGET.md line 138 still says the redesign comes "after Instrument verification"; the owner's 2026-10-05
  correction (#640 comment 5988555968) puts Mark II before P3. Not edited here (out of scope); noted in the plan.
- 09:33 route rc 0 (lock 08:40:51 to 09:33:19, 52.5 min). Route at `e6172750`: LUT 50,702 / FF 59,677 / slices 15,828 /
  RAMB36 79 / RAMB18 27 / DSP 14; WNS +0.244 (slow corners), WHS +0.036 (fast corners); 106,639 of 106,639 routable
  nets fully routed, 0 with routing errors; only the echoed `Synth 8-4445` severity line in the log.
  `pp_resource_gate.py check ... --endpoint route-1x1` against the record (dev `54643724`): rc 0, PASS; LUT -65,
  FF +43, slices -4; wrapper +147 LUT with no wrapper source change (optimization movement).
  Critical path `u_pp/u_rx_validator/hdr_ctlr_eid_r_reg[11]` -> `u_pp/u_tx_arbiter/FSM_onehot_arb_st_r_reg[0]/CE`,
  39 levels, 19.443 ns, 73 % routing.
  `baseline.log` sha256 16cbfa00cca1f514a45ac477b3ab60ee95acb86c99344031f592456a815fc4d7, 816,503 bytes;
  `alinx_ax7101_route.dcp` sha256 ac7a716819091b492b23efc8996b4bc93f13bc9866cf8f3cc9110e2d43c37658, 110,137,721 bytes;
  `baseline_images.json` sha256 1fab9d504ab04761ea25637cf3f254687309e20b564a4b975c1385492b4daff6.
- 10:02 standalone rc 0 (= record). 10:04 route map tied (175 blocks). 10:09 core pricing rc 0 x3.
- 10:13 commit `8d3be734`; 35/35 gates rc 0. 10:14 #661 REVIEW READY (07:47) found with measured route 50,318:
  ledger re-based on it; 10:20 commit `06f5e7e5`; 35/35 gates rc 0.
- 10:23 STOP posted: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5990726992 (head `06f5e7e5`).

## Round 1b historical handoff

Status: REVIEW READY. Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6080904058.
Executor [A540]; reviewers [R492] internal and [R493] external.
Head: `c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970` on `640-mark2-plan`.
Confirmed origin `https://github.com/kebag-logic/milan-fpga.git` and starting head `06f5e7e55be79f9184854d9c84a72f98ab0527cb`.
The tracked worktree is clean. No push or PR action was performed.
The manager publishes the branch and opens review. Independent review is still required.

### Completed steps and commits

| Step | Commit | Result |
|---|---|---|
| 1 | `a959b7879ed05a24c89bf71424e02c3049042463` | Conflict-free merge, ordered parents `06f5e7e55be79f9184854d9c84a72f98ab0527cb` and `5603c353137e90c1fa95429f6d00ef7a2298d9ee` |
| 2 | `37e4cea8a60925421aea2d8d37f961cafc66c481` | Every linked decision folded in, including later placement overrides |
| 3 | `d53ea40ac16e66245dadd19fea4e192e3ab4edb8` | Three recorded endpoints, split removal/debit estimate and recalculated ledger |
| 4 | `85e6f34989edb2011ec98240ae7a3396bd1b337a` | Lane scope, dependencies, order and validation; M3/M10 have zero default credit |
| 5 | `780fdcffe975bf6df3be7e75a56e5760418143b7` | AREA_BUDGET aligned; unchanged gate policy and M9 re-record rule |
| Wording correction | `c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970` | Current mailbox wording; residual wrapper attribution explicitly uncredited |

Relative to assigned dev, only `docs/design/MARK_II_AREA_PLAN.md` and `docs/design/AREA_BUDGET.md` change.
All new commit subjects are one line, with no body or trailers.
No additional measurement script was needed: the committed recipe, baseline reader and resource gate supply this stage's evidence.
No RTL, port, parameter, register map, resource record or gate implementation changed.
No new Vivado run, hardware access or bench activity took place.

### Decisions and requirements

The plan cites and applies #640 comments 5990755268, 5991591637, 5991605450, 5991626132,
5991695093, 5991737927, 5991745829 and 5993114362, plus #664 approval 6015500032.
D1 keeps PDU/port equivalence and all test counts; D2 retains diagnostics; D3 requires deterministic service
bounds with normative margin; D4 approves on-chip main memory; D5 permits a smaller cacheless RV32I only
with capture and boot proof; D6 plans sharing where fabric AECP remains; D7 retains the last gate record
until M9; D8 sets a one-percent planning margin; the later split decisions supersede the initial D9 exclusion.
F0-F5 moves ADP, ACMP, MAAP, SRP, AECP and saved-state handling before P3, after suite and bench qualification.
Unqualified functions retain their fabric owner. The hard-core port remains milestone 13.
The 10 ms project service budget does not replace any normative wire deadline.

### Recorded baseline and source checkpoint

Source: [`pp_resource_baseline.json`](../../syn/ooc/pp_resource_baseline.json), all three `record` objects.
Each `measured` note identifies `a5ca6e5110d515bf5f894f87b94f9bf6f6836bbb`.
That is #645/#647's measured merge of dev `6aa25dec`.
It uses processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`.
Dev `5603c353137e90c1fa95429f6d00ef7a2298d9ee` carries those records unchanged.
This names the stored baseline, not a measurement of `5603c353`.
No new Vivado measurement was made for Round 1b.

| Endpoint | LUT | FF | Slice | RAMB36 | RAMB18 | BRAM tiles | DSP | WNS / WHS ns |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `route-1x1` | 50,267 | 54,413 | 15,779 | 74 | 27 | 87.5 | 14 | +0.299 / +0.031 |
| `ooc-1x1` | 23,179 | 19,779 | -- | 16 | 3 | 17.5 | 8 | -3.562 / +0.159 |
| `ooc-8x8` | 30,135 | 27,380 | -- | 21 | 5 | 23.5 | 8 | -2.278 / +0.159 |

The resource records omit LUTRAM; it is not zero.
The historical inventory below retains its separately measured LUTRAM column.
Standalone timing has unconstrained I/O and proves no integrated fit.
The 8x8 row is a scaling reference, not shipping acceptance.
The route leaves 71 slices and 47.5 physical BRAM tiles.
The 121.5-tile policy ceiling leaves 34 tiles of usable allowance.

[The source receipt](../findings/234_PP_SHADOW_AREA_BASELINE.md#re-baseline-of-2026-10-08-issues-645-and-647)
records the completed route and all four signoff corners.
Its source checkpoint is `alinx_ax7101_route.dcp` from that measurement.
The route log SHA-256 is
`94c0471debaa23a0fd20d9050298173facb997735ffa8bbf451f68cbd82de0ac`
(829,160 bytes).
The record's input SHA-256 values bind the measurement inputs:

| Endpoint | Input SHA-256 |
|---|---|
| `route-1x1` | `95a6cc95786fa743da28e2aa603d3a6af08200c86bf4bb7c452aeba7ec072c4c` |
| `ooc-1x1` | `2dd522bd12b3480a8817cf2bb3dd969ac7be6f3d80be70d13fe32ce5576011a5` |
| `ooc-8x8` | `5604984543f875b19f344900a8b183adf81281c02ba42517ff894502f7a07f0c` |

The recipe uses Vivado 2026.1 build 6511674, `xc7a100t-fgg484-2`.
Directives: `AreaOptimized_high`, `ExploreArea`, `ExtraPostPlacementOpt`, `AggressiveExplore`.
It uses the default seed, one synthesis worker, 32 general threads.
The standalone wrapper clock is 20 ns.
The historical route below predates this synthesis-worker recipe identity.
Its deltas therefore inform planning, not a comparable gate verdict.

The checkpoint is identified by the committed source receipt, not copied or reopened in this round.
Its digest and size are not supplied by that receipt; the input digest and route-log digest above are not
checkpoint digests. The Round 1 checkpoint in the historical section is a different measurement.

### Current inventory

These are the current record's source-scope references.
The routed hierarchy is rebuilt and can absorb neighbouring logic.
Use standalone scopes to estimate removable source functionality.
Parent rows include descendants; never add both to a saving.
The [historical inventory](#inventory) supplies functions, clauses and construction.

| Scope relative to wrapper | Route LUT | OOC 1x1 LUT | OOC 8x8 LUT | Split disposition |
|---|---:|---:|---:|---|
| `wrapper` | 23,345 | 23,179 | 30,135 | Replaced after every control function qualifies |
| `u_pp` | 22,794 | 22,517 | 28,938 | Control functions move; retained fabric interfaces are reconnected |
| `u_pp/u_aecp` | 8,084 | 6,150 | 7,298 | F5; includes the following five children |
| `u_pp/u_aecp/u_d3` | 1,781 | 1,703 | 2,297 | F1/F5 saved-state ownership |
| `u_pp/u_aecp/u_dyn` | 1,440 | 134 | 497 | F5; fabric media state stays authoritative |
| `u_pp/u_aecp/u_store` | 979 | 1,026 | 1,119 | F5 validated image and names |
| `u_pp/u_aecp/u_ucpu` | 1,727 | 1,553 | 1,651 | F5; no second M10 credit |
| `u_pp/u_aecp/u_resp` | 345 | 432 | 416 | F5 response serving |
| `u_pp/u_notify` | 2,259 | 2,125 | 2,114 | F5 registry, notification and counter serving |
| `u_pp/u_srp` | 3,682 | 3,868 | 7,312 | F4; media admission enforcement remains in fabric |
| `u_pp/u_srp/u_encoder` | 1,358 | 1,479 | 1,466 | Included in SRP |
| `u_pp/u_srp/u_decoder` | 579 | 588 | 922 | Included in SRP |
| `u_pp/u_listener` | 1,451 | 1,560 | 1,681 | F3 ACMP listener |
| `u_pp/u_talker` | 641 | 823 | 1,472 | F3 ACMP talker |
| `u_pp/u_adp` | 385 | 523 | 696 | F0/F3 advertisement and discovery |
| `u_pp/u_originator` | 687 | 697 | 682 | F3/F5 originated transactions |
| `u_pp/u_nvm_shadow` | 792 | 808 | 780 | F1/F3 binding persistence |
| `u_pp/u_nvm_port` | 513 | 526 | 524 | F1 store and flash service |
| `u_nvm` | 486 | 581 | 1,116 | F1 replaces container backend |
| `u_pp/u_timer` | 882 | 906 | 1,631 | Hard deadlines remain fabric events; no saving credited |
| `u_pp/u_dispatch` | 665 | 887 | 908 | Replaced routing; no separate credit |
| `u_pp/u_trace` | 31 | 37 | 28 | Equivalent diagnostics retained; no credit |

The #232 registry, #230 SRP storage and #639 rings/listener changes
are already included; their savings cannot be subtracted again.
#686 also changed MAAP, before #645/#647 refreshed the record.

The full original hierarchy inventory, functions and clause references remain in the committed plan's
historical inventory. The current table supersedes its processor counts; non-processor lever bases that
still use the original route are explicitly estimates from that older inventory.

### Levers: saving basis, risk and verification cost

All values below are LUT estimates for the shipping 1x1 image, except explicitly measured bases.

| Lever | Credit and basis | Risk | Verification cost |
|---|---|---|---|
| L1 shared evaluator | Default 0; M3 retained-AECP opportunity 2,600, derived from current notification/D3/dynamic/dispatch scopes less replacement engine cost; ACMP/ADP replaced by F0-F5 | High: service bounds and state ordering | Full processor and consumer bank, differential PDUs/port transactions, reviewed cycle retargeting |
| L2 firmware placement | 14,000 (11,500-16,000); 17,678 disjoint wrapper source LUTs plus parent MAAP 429, less measured mailbox 3,102 and estimated integration 1,000; +/-1,500 mapping allowance | Highest: F5 integration, deterministic service, memory and qualification | F2-F5 suites and bench, malformed/stall/reset cases, all-stream/counter traffic, sustained churn, integrated route |
| L3 storage | M2 200 (100-400); retained SoC arrays only, excluding removed processor and M6/M7 tables | Medium: RAM inference and primitive growth | Per-array lockstep, generated SoC checks, real build and resource gate |
| L4 right-sized widths | Included in M3 retained-AECP estimate; default 0 and no separate saving | Medium: truncation, invalid IDs and shapes | Boundary/invalid values at 1x1 and 8x8, complete transaction bank |
| L5 transaction serialization | Included in M3 retained-AECP estimate; default 0 and no separate saving | High: notification/D3 ordering and latency | Repeated/concurrent commands, persistence, reset/backpressure, deterministic deadline proof |
| L6 diagnostics | 0: D2 rejects the original 700-LUT prune | Diagnostics must survive placement changes | Equivalent visibility and counter tests in each supported placement |
| L7 SRP evaluator | 0 extra: F4 replaces M4 and the earlier 450-LUT opportunity | Medium: serialization and timers | Both-shape SRP campaigns, event stalls, MRP deadlines and protocol bench |
| L8 CSR read path | M5 600 (400-1,000); historical 2,907-LUT mux and #649 model | Medium: coherent snapshots and AXI-Lite latency | CSR, tcam_csr, milan_dp, host firmware tests, map checks and boot readback |
| L9 media contexts | M6 600 (400-900); retained monitor/counter/channel-map/set-point inventory and per-stream marginals | Medium: concurrent updates | avtp_rxmon, tkdiag, chmap_capture, render_setpoint, milan_dp, GET_COUNTERS, reset/wrap |
| L10 gPTP | M7 500 (300-700), historical 464 LUTRAM basis; M10 default 0, retained-AECP sharing 1,200 (900-1,500) only if M3 leaves its engine | Medium for tables, high for sharing | gPTP suites, plane/shadow/timestamps, CDC, #117 bench; M10 adds arbitration/turnaround proof |
| L11 SoC | M8a 1,600 (1,200-2,000), historical DDR controller/PHY 823+873; M8b 1,700 (1,300-2,200), measured isolated cores 3,066/843/1,051 with bridge/storage allowance | High: capacity and CPU service | Firmware host, nvm_cosim, nvm_capture_cpu, capture <=24.5 ms at 8x8, builder/deploy, target hooks, boot/persistence bench |
| L12 functional prunes | 0; protocol features, 16 controllers, RX filter, media-clock, CRF and rendering remain | Removing required function cannot satisfy the target | Existing full protocol and media acceptance remains mandatory |

The split credits only 6.5 released BRAM tiles and debits the mailbox's six. Its net 0.5 does not establish
F5 storage capacity. M8 must account for image, firmware stack, contexts and staging within 121.5 tiles.
M3 and M10 cannot save an AECP engine already removed by F5; if M3 consumes it in a fabric build, M10 is repriced.
The other 5,501 standalone wrapper LUTs receive no removal credit and are not a guaranteed reserve.

### Cumulative estimate

Each row assumes every preceding row has landed and qualified.
Ranges describe all-low or all-high savings, not statistical confidence.

| Order | Lane | Saving | Central image | Conservative image | Optimistic image |
|---:|---|---:|---:|---:|---:|
| 0 | Recorded baseline | -- | 50,267 | 50,267 | 50,267 |
| 1 | F0-F5, complete qualified flip / L2 | 14,000 | 36,267 | 38,767 | 34,267 |
| 2 | M2 | 200 | 36,067 | 38,667 | 33,867 |
| 3 | M5 | 600 | 35,467 | 38,267 | 32,867 |
| 4 | M6 | 600 | 34,867 | 37,867 | 31,967 |
| 5 | M7 | 500 | 34,367 | 37,567 | 31,267 |
| 6 | M8a | 1,600 | 32,767 | 36,367 | 29,267 |
| 7 | M8b, conditional | 1,700 | 31,067 | 35,067 | 27,067 |
| 8 | M3 and M10 | 0 | 31,067 | 35,067 | 27,067 |
| 9 | M9 | No assumed saving | Measure | Measure | Measure |

Central headroom is 6,973 LUTs below 38,040, or 18.33 percent.
The conservative estimate leaves 2,973, or 7.82 percent.
Both exceed D8's 1 percent planning margin.
Without M8b, the conservative image is 36,367 and still clears it.
Without the split, these retained-fabric levers reach only 45,067 centrally.
A partial flip must subtract only its measured disjoint contribution.
F5 qualification is therefore essential to this default ledger.
Timing cannot be inferred from these LUT calculations.

### Lane sequence and closure

All parent lanes start from the third adoption, processor `2ad2f845`.
The earlier #661 dependency is satisfied on dev `5603c353`.
Weeks count from 2026-10-12; 2026-12-15 is week 10.
This is a schedule estimate, conditional on split qualification.
Each implementation needs its own settled public scope and review.
Independent lanes may proceed concurrently in isolated worktrees.
Measurements queue serially; no Vivado overlaps another heavy build.

| Order / window | Lane | Scope and files | Dependency | Estimated default saving | Required evidence and risk |
|---|---|---|---|---:|---|
| 0, complete | M0 | Adopted processor pin and current three-endpoint record | #661, #682, #686, #645/#647 present at assigned dev | Already in 50,267 | Reuse committed record; do not subtract old lane deltas |
| 1, weeks 1-6 | F0-F5 / L2 | `sw/firmware/ctrl/`, `sw/firmware/ctrl_nvm/`, mailbox contract and parent integration; complete F5 and connect the datapath | Approved #664 text; F0-F4 foundations present; F2-F5 suites and bench before default flip | 14,000 (11,500-16,000) | Highest risk: exact ownership, full service/wire bounds, all streams/counters and soak; no full credit for a partial flip |
| 2, weeks 1-4 | M2 | SoC FIFO/table storage in `sw/litex/milan_soc.py`; exclude processor, media and gPTP arrays | Adopted pin; settled split interface allocation; measure final split for default credit | 200 (100-400) | RAM inference and per-array lockstep; primitive growth still judged by gate |
| 3, weeks 2-6 | M5 | Existing read mux and snapshots in `hdl/common/csr/milan_csr.sv` | Adopted pin; preserve both placement faces | 600 (400-1,000) | CSR coherence, AXI-Lite timing and firmware readback |
| 4, weeks 2-6 | M6 | AVTP counter contexts, channel-map capture and render set-point under `hdl/ieee1722/` | Adopted pin; fabric media ownership fixed by #664 | 600 (400-900) | Update/read/reset hazards, GET_COUNTERS and full datapath |
| 5, weeks 3-6 | M7 | gPTP engine state tables and parent shadow wrapper | Adopted pin; gPTP remains fabric; excludes M2 arrays | 500 (300-700) | gPTP suites, CDC/timestamps and turnaround |
| 6, weeks 2-8 | M8a/M8b | SoC memory/core selection, firmware layout and #70/F1 staging | D4 approved; D5 conditional; measure linked F5 storage and split service before accepting core | 3,300 (2,500-4,200) | Memory capacity, boot, 8x8 capture <= 24.5 ms, SRP churn; revert core if bounds fail |
| 7, decision at week 4; weeks 4-8 | M3 | Retained fabric AECP dispatch, notification, D3 and entity widths in processor | D1/D3 approved; ACMP/ADP portion replaced; schedule residual only for a selected fabric-AECP image | **0**; fabric-only opportunity 2,600 (1,500-3,600) | PDU/port equivalence and complete processor/consumer bank; no F5 overlap |
| 8, weeks 6-9 | M10 | One gPTP/AECP engine across processor integration | D6 planned; requires fabric AECP remaining and M3 preserving a separate removable engine | **0**; fabric-only opportunity 1,200 (900-1,500) | Sharing turnaround proof; removed AECP cannot be saved twice |
| 9, weeks 9-10 | M9 | Final pin adoption, integrated route, timing closure and resource-gate re-record; budget/ledger update | Selected F2-F5 functions qualified, actual M-lane deltas known, required review complete | No assumed saving | <= 38,040 LUT with timing; aim <= 37,659; all suites/campaigns and physical acceptance |

M1 is dropped by D2; M4 is replaced by F4.
M3/M10's listed order is for any retained fabric-AECP work.
It does not make them blockers for a fully qualified split.
Their zero default contribution follows from F5's ownership change.
The manager assigns those implementation lanes against their chosen placement.

At week 4, replace estimates with available routed lane deltas.
The original checkpoint was M3's first sub-lane route.
The split decision makes its equivalent the first integrated split route.
If neither exists, report the measurement as missing, not a pass.
Reprice M3/M10 against actual remaining fabric ownership at that checkpoint.
A missed split deadline or service bound blocks the default ledger.
Retain the qualified fabric function and publish the residual area gap.
Never change acceptance or omit functions to force the LUT target.

Each lane records its own route and both standalone references.
Standalone 1x1/8x8 continue to guard the supported all-fabric option.
A fully split route has no `KL_pp_shadow` scope.
The current recipe expects exactly one wrapper and cannot measure that shape.
M9 therefore needs reviewed split-aware measurement coverage before re-recording.
Keep the existing all-fabric endpoints as independent references.
Add a named split shipping endpoint with comparable whole-image metrics.
This is a future tooling obligation; no gate/schema changes occur here.

Intermediate lanes publish measured deltas and compare with the last record. Zero primitive-growth tolerances
still apply: a RAM conversion that trips them requires explicit disposition, not a threshold change or a claimed pass.
M9 alone re-records once the target and timing are met. The current wrapper-only recipe needs reviewed split-aware
coverage before it can measure a fully split image; all-fabric standalone references remain independent.

### Gate table at the committed head

Head: `c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970`. **48/48 commands returned 0.**
Every command ran without a shell pipe. Independent checks used separate log and rc files and a foreground
wait; the submodule documentation build used `make -j16`. No heavy build ran.
The Markdown environment matches `tools/markdown/requirements.txt`; Python writes of bytecode were disabled
for the final campaign. The exported Verilator was `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`;
no Verilator invocation was needed for these documentation-only changes.

| Gate | Command | rc |
|---|---|---:|
| docs_check | `rtk proxy python3 scripts/docs_check.py` | 0 |
| docs_self | `rtk proxy python3 scripts/docs_check.py --selftest` | 0 |
| feature_status | `rtk proxy python3 scripts/check_feature_status.py` | 0 |
| feature_self | `rtk proxy python3 scripts/check_feature_status.py --self-test` | 0 |
| em_dash | `rtk proxy python3 scripts/check_em_dash.py --base 5603c353137e90c1fa95429f6d00ef7a2298d9ee` | 0 |
| em_dash_self | `rtk proxy python3 scripts/check_em_dash.py --selftest` | 0 |
| doc_style | `rtk proxy python3 scripts/check_doc_style.py` | 0 |
| doc_style_self | `rtk proxy python3 scripts/check_doc_style.py --selftest` | 0 |
| gptp_docs | `rtk proxy python3 scripts/check_gptp_docs.py --with-submodule` | 0 |
| gptp_docs_self | `rtk proxy python3 scripts/check_gptp_docs.py --selftest` | 0 |
| doc_map | `rtk proxy python3 docs/DOC_MAP.gen.py --check` | 0 |
| doc_map_self | `rtk proxy python3 docs/DOC_MAP.gen.py --selftest` | 0 |
| timesync | `rtk proxy python3 docs/diagrams/timesync_chain.gen.py --check` | 0 |
| timesync_self | `rtk proxy python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 |
| solution | `rtk proxy python3 scripts/check_solution_docs.py` | 0 |
| solution_self | `rtk proxy python3 scripts/check_solution_docs.py --selftest` | 0 |
| submodule_diagram | `rtk proxy python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 |
| submodule_diagram_self | `rtk proxy python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 |
| submodule_docs | `rtk proxy python3 scripts/check_submodule_docs.py` | 0 |
| submodule_docs_self | `rtk proxy python3 scripts/check_submodule_docs.py --selftest` | 0 |
| diagram_pngs | `rtk proxy python3 scripts/check_diagram_pngs.py` | 0 |
| diagram_pngs_self | `rtk proxy python3 scripts/check_diagram_pngs.py --selftest` | 0 |
| module_matrix | `rtk proxy python3 docs/traceability/gen_module_matrix.py --check` | 0 |
| baremetal | `rtk proxy python3 scripts/check_baremetal_only.py --check` | 0 |
| baremetal_self | `rtk proxy python3 scripts/check_baremetal_only.py --selftest` | 0 |
| doc_paths | `rtk proxy python3 scripts/check_doc_paths.py` | 0 |
| archive | `rtk proxy python3 scripts/check_archive.py` | 0 |
| archive_self | `rtk proxy python3 scripts/check_archive.py --selftest` | 0 |
| toc_self | `rtk proxy python3 scripts/gen_toc.py --selftest` | 0 |
| toc_anchors | `rtk proxy python3 scripts/gen_toc.py --verify-anchors` | 0 |
| toc_check | `rtk proxy python3 scripts/gen_toc.py --check` | 0 |
| todo | `rtk proxy python3 scripts/check_todo_ownership.py` | 0 |
| hygiene | `rtk proxy python3 scripts/check_hygiene.py --check` | 0 |
| wire | `rtk proxy python3 scripts/check_wire_accountability.py --self-test` | 0 |
| resource_baseline | `rtk proxy python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 |
| resource_self | `rtk proxy python3 syn/ooc/pp_resource_gate.py --selftest` | 0 |
| resource_mutants | `rtk proxy python3 syn/ooc/pp_resource_gate_mutants.py` | 0 |
| ci_scope | `rtk proxy python3 scripts/ci_scope.py --selftest` | 0 |
| ci_events | `rtk proxy python3 scripts/ci_events.py --check` | 0 |
| wavedrom_self | `rtk proxy python3 scripts/gen_wavedrom.py --selftest` | 0 |
| wavedrom_axis | `rtk proxy python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 |
| wavedrom_cdc | `rtk proxy python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 |
| wavedrom_gptp | `rtk proxy python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 |
| pp_sources | `rtk proxy python3 scripts/pp_srcs.py --check --selftest` | 0 |
| docs_nogit | `rtk proxy env GIT_DIR=/dev/null python3 scripts/docs_check.py` | 0 |
| gptp_make | `rtk proxy make -j16 -C gptp-processor docs` | 0 |
| diff_base | `rtk proxy git diff --check 5603c353137e90c1fa95429f6d00ef7a2298d9ee HEAD` | 0 |
| diff_tree | `rtk proxy git diff --check` | 0 |

The resource self-test passes 260 arms and 500 generated cases. Its mutation control passes and all 174
mutants fail as expected; the overall mutation-driver exit status is 0.
The first pass at `780fdcffe` had one bare-metal wording failure; the correction used the current contract's
mailbox terminology. The full 48-command final campaign passed at the head above; no test was weakened.
An additional arithmetic check verified the three recorded endpoint values, disjoint 17,678-LUT/6.5-tile
source subtotal, all cumulative rows and the resource-record byte identity against assigned dev.

Logs and rc files: `$VALIDATION_STORAGE/640-a540/round1b/gates-final/`.
`ROUND1B-GATE-RECEIPTS.txt` in this output directory records full SHA-256 and size for every log, rc and result file.
RTL suites, Yosys and new routed builds are outside this documentation-only change; no changed source or build input
requires them here. Hosted CI, future integration fit, bench qualification and independent reviews are not claimed.

### Remaining qualification and publication

- The complete split's 14,000-LUT saving is an estimate, not an integrated measurement.
- F5, memory capacity, deterministic target service and F2-F5 bench qualification remain implementation work.
- The smaller core remains conditional and is reverted if capture, boot or split-load bounds fail.
- The manager publishes the branch and opens review. The executor supplies no review verdict or completion ledger.
- Public REVIEW READY comment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081236580.

Final containment: generated Python caches removed; tracked and ignored worktree status clean.
/data has 61,008,318,464 free bytes, above the 30 GB floor. Output files are each below 200 KB.
No push, PR action, merge to dev or further implementation is performed by this handoff.

## Round 1c

Public readiness receipt: [A540 REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081871164).

Status: REVIEW READY. Head: `39258a1486897127288f82fbb1b86333febf6f00`.
Start: `c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970`.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081534590
Reviews: PR #698 comments 6081481326 (R492-1) and 6081524243 (R493-1).
Executor: [A540]. Reviewers: [R492] internal and [R493] external.
Origin and PR #698 matched the starting branch/head. No push or PR change.

### Findings and commits

| Assignment / review | Outcome | Commit |
|---|---|---|
| Step 1, R492-1-F1 | M0s owner, two steps, dependencies and D7 ordering mirrored | `da590e495` |
| Step 2, R492-1-F2 | Correct units, unowned remainder, explicit repricing and ledger | `72ee30833` |
| Step 3, R492-1-F3 | Inclusive no-split, partial-flip assumptions, both bars and residual gaps | `72a215f17` |
| Step 4, R492-1-R1/R2/R3/R4; R493-1-R1/R2 | Shortened prose, M3 basis table, linked authorities, historical tense and blank-line fix | `30b539ad8` |
| Step 5, R492-1-S1/S2 | Exact core reproduction command and surviving M2 FIFO scope | `cee00f59f` |
| Final wording check | Three new sentences shortened | `39258a148` |

The Round 1c assignment and both reviews are addressed in documentation.
M0s belongs to the manager's resource bench. Its first route selects F0-F4 with fabric AECP; its second follows F5's merge. Both precede week 4 and the default flip. D7 compares M0s figures with the last accepted record; later lanes also show their matching-placement delta. Missing integration or measurement is a missed checkpoint, not a pass.

M8a now credits 1,000 LUTs (400-1,500). The 823 controller and 873 PHY figures count pre-packing cells. The 3,231 anonymous cells receive no credit. Explicit 50/75/100 percent packing assumptions, less 400/250/100 LUT replacement costs, produce the rounded cases. These assumptions need routed validation.

Full split finishes at 31,667 LUTs centrally, 35,867 conservatively and 27,567 optimistically. All clear 38,040 and 37,659 arithmetically. Without M8b, conservative full split is 37,167.
No split including M3/M10 reaches 41,867 centrally; every priced case misses both bars.
Partial split with F5 unqualified reaches 37,957 centrally: 83 below the requirement, 298 above the planning-margin bar. Conservative partial is 43,557; optimistic partial is 32,557. Without M8b, central partial is 39,657. The manager must qualify F5 or commission additional redesign against the published gaps.

M2 names the retained MAC packet/CDC and CSR AW/W/B/AR/R FIFOs. DDR3, core/protocol-memory bridges, mailbox rings and media/gPTP tables receive no overlapping M2 credit. Already mapped block RAM supplies no second saving.
The L11b section contains source sizes and digests, all Tcl inputs/options, and the serial lock-held reproduction command. Shell syntax passes, and all three command traces equal the retained originals under a Tcl recording harness. No synthesis was executed.

Commit history:

```text
da590e4951b8b82a953729a69c534903279cbfde Schedule M0s measurements before the split flip and week-four checkpoint (#640)
72ee30833d726e013bfad6e9bb0056599a4ad48c Reprice on-chip memory from the pre-packing cell census (#640)
72a215f17ce2bc802bbe7ed291e7e47dafb79091 Price no-split and partial-flip outcomes against both LUT bars (#640)
30b539ad8e2b994ee0a5fb1f2fa07ada2b6bcb20 Shorten current area prose and link its authorities (#640)
cee00f59f934973277d1e346c412468f7fbe1ef4 Document core pricing reproduction and retained M2 FIFO scope (#640)
39258a1486897127288f82fbb1b86333febf6f00 Keep reproduction and retained-scope prose within the sentence limit (#640)
```

### Baseline and source checkpoint

Stored measurement source: `a5ca6e5110d515bf5f894f87b94f9bf6f6836bbb`.
Assigned dev `5603c353137e90c1fa95429f6d00ef7a2298d9ee` carries that record.
Source checkpoint: `alinx_ax7101_route.dcp` from the #645/#647 measurement.
The #234 findings source receipt records route-log SHA-256
`94c0471debaa23a0fd20d9050298173facb997735ffa8bbf451f68cbd82de0ac`, 829,160 bytes.
It is not a fresh measurement of this documentation head.
The three input digests and full source-recipe identity remain in Round 1b above.
The resource JSON and policy are unchanged, byte-checked against the starting head.

| Endpoint | LUT | FF | Slice | RAMB36 / RAMB18 | BRAM tiles | DSP | WNS / WHS ns |
|---|---:|---:|---:|---|---:|---:|---|
| route-1x1 | 50,267 | 54,413 | 15,779 | 74 / 27 | 87.5 | 14 | +0.299 / +0.031 |
| ooc-1x1 | 23,179 | 19,779 | -- | 16 / 3 | 17.5 | 8 | -3.562 / +0.159 |
| ooc-8x8 | 30,135 | 27,380 | -- | 21 / 5 | 23.5 | 8 | -2.278 / +0.159 |

### Inventory


These are the current record's source-scope references.
The routed hierarchy is rebuilt and can absorb neighbouring logic.
Use standalone scopes to estimate removable source functionality.
Parent rows include descendants; never add both to a saving.
The [historical inventory](#inventory) supplies functions, clauses and construction.

| Scope relative to wrapper | Route LUT | OOC 1x1 LUT | OOC 8x8 LUT | Split disposition |
|---|---:|---:|---:|---|
| `wrapper` | 23,345 | 23,179 | 30,135 | Replaced after every control function qualifies |
| `u_pp` | 22,794 | 22,517 | 28,938 | Control functions move; retained fabric interfaces are reconnected |
| `u_pp/u_aecp` | 8,084 | 6,150 | 7,298 | F5; includes the following five children |
| `u_pp/u_aecp/u_d3` | 1,781 | 1,703 | 2,297 | F1/F5 saved-state ownership |
| `u_pp/u_aecp/u_dyn` | 1,440 | 134 | 497 | F5; fabric media state stays authoritative |
| `u_pp/u_aecp/u_store` | 979 | 1,026 | 1,119 | F5 validated image and names |
| `u_pp/u_aecp/u_ucpu` | 1,727 | 1,553 | 1,651 | F5; no second M10 credit |
| `u_pp/u_aecp/u_resp` | 345 | 432 | 416 | F5 response serving |
| `u_pp/u_notify` | 2,259 | 2,125 | 2,114 | F5 registry, notification and counter serving |
| `u_pp/u_srp` | 3,682 | 3,868 | 7,312 | F4; media admission enforcement remains in fabric |
| `u_pp/u_srp/u_encoder` | 1,358 | 1,479 | 1,466 | Included in SRP |
| `u_pp/u_srp/u_decoder` | 579 | 588 | 922 | Included in SRP |
| `u_pp/u_listener` | 1,451 | 1,560 | 1,681 | F3 ACMP listener |
| `u_pp/u_talker` | 641 | 823 | 1,472 | F3 ACMP talker |
| `u_pp/u_adp` | 385 | 523 | 696 | F0/F3 advertisement and discovery |
| `u_pp/u_originator` | 687 | 697 | 682 | F3/F5 originated transactions |
| `u_pp/u_nvm_shadow` | 792 | 808 | 780 | F1/F3 binding persistence |
| `u_pp/u_nvm_port` | 513 | 526 | 524 | F1 store and flash service |
| `u_nvm` | 486 | 581 | 1,116 | F1 replaces container backend |
| `u_pp/u_timer` | 882 | 906 | 1,631 | Hard deadlines remain fabric events; no saving credited |
| `u_pp/u_dispatch` | 665 | 887 | 908 | Replaced routing; no separate credit |
| `u_pp/u_trace` | 31 | 37 | 28 | Equivalent diagnostics retained; no credit |

The [#232](https://github.com/kebag-logic/milan-fpga/issues/232) registry, [#230](https://github.com/kebag-logic/milan-fpga/issues/230) SRP storage and [#639](https://github.com/kebag-logic/milan-fpga/issues/639) rings/listener changes
are already included; their savings cannot be subtracted again.
[#686](https://github.com/kebag-logic/milan-fpga/issues/686) also changed MAAP, before [#645](https://github.com/kebag-logic/milan-fpga/issues/645)/[#647](https://github.com/kebag-logic/milan-fpga/issues/647) refreshed the record.

### Levers and verification costs


| Lane | Default saving, central (range) | Basis and overlap exclusion |
|---|---:|---|
| M2 / L3 | 200 (100-400) | Retained MAC and CSR FIFOs listed in L3; excludes DDR3, CPU/protocol-memory bridges and M6/M7 tables |
| M3 / L1a, L4, L5 | 0 | AECP/notification residual applies only where fabric AECP remains; ACMP/ADP work is replaced by F0-F5 |
| M5 / L8 | 600 (400-1,000) | Historical 2,907-LUT CSR read path; optimize existing status mux only, not split-interface growth |
| M6 / L9 | 600 (400-900) | Historical monitor, counter, channel-map and set-point contexts; retained media functions |
| M7 / L10a | 500 (300-700) | Historical gPTP plane tables; no overlap with M2 or M10 |
| M8a / L11a | 1,000 (400-1,500) | 1,696 named pre-packing cells, explicit packing/replacement assumptions in L11; 3,231 anonymous cells receive no credit |
| M8b / L11b | 1,700 (1,300-2,200) | Core OOC comparison in L11; conditional on capture, boot and split service under load |
| M10 / L10b | 0 | F5 removes fabric AECP's engine; sharing it cannot save twice |

M3 remains a priced fabric-AECP lane.
Its estimate is 2,600 LUTs (1,500-3,600).
Its basis uses these shares:

| Scope | LUT basis | Share |
|---|---:|---:|
| Notification | 2,125 | 60 percent |
| D3 and dynamic state | 1,703 + 134 | 70 percent |
| AECP own logic | 1,302 | 50 percent |
| AECP dispatch queue | 421 | 40 percent |
That displaces about 3,380 LUTs.
Engine and arbitration overhead costs about 1,000 LUTs.
Residual width work adds approximately 200 LUTs.
That brings the saving near 2,600.
This is a prototype target for retained fabric AECP only.
M10 remains planned there at 1,200 LUTs (900-1,500).
The routed AECP engine bounds sharing: 1,727 LUTs.
M3 must preserve that engine for M10 to remove.
If M3 consumes it, reprice M10 to zero.
Neither lane receives credit in the default-split total.

| Lever | Risk and verification cost |
|---|---|
| L2/F0-F5 | High: ownership, service under load, storage. F0/F1 tests, F2-F5 differential suites, target execution, streams/counters/soak qualification and M0s routes |
| L3/M2 | Medium: MAC/CSR buffering, reset and RAM inference. Per-array lockstep, owning suites, both shapes and post-D4 route |
| L1/L4/L5/M3 | High: retained-AECP sequencing. Processor suites/campaigns at counts, PDU/transaction equivalence, parent consumers and capture bounds |
| L8/M5 | Medium: coherent snapshots and read latency. CSR, tcam_csr, milan_dp, firmware readback |
| L9/M6 | Medium: update/read/reset hazards. avtp_rxmon, tkdiag, chmap_capture, render_setpoint and milan_dp |
| L10a/M7 | Medium: gPTP state/turnaround. Processor suites, gptp_plane, gptp_shadow, gptp_txts, milan_dp_gptp and timestamp/CDC checks |
| L11a/M8a | High: unmeasured packing and memory capacity. Linked firmware/storage census, builder/deploy, memory/boot/persistence tests and routed delta |
| L11b/M8b | High: conditional capture/service bounds. nvm_capture_cpu, 8x8 capture <=24.5 ms, boot, split service under load; revert if missed |
| L10b/M10 | High: sharing turnaround. Preserve separate AECP engine through M3; combined protocol/gPTP arbitration and deadline proof |
| L6/M1, L7/M4, L12 | No default saving: diagnostics retained, F4 replaces M4, required surfaces remain. No pruning credit |

### Scenario ledger


All scenarios retain required function, diagnostics and D7 policy.
Each assumes its credited levers qualify independently, including conditional M8b.
M3 must preserve a separate AECP engine for M10.
Their combined central credit is 3,800 LUTs.
The range is 2,400-5,100.
They receive no credit in the complete split.

**No split:** apply M2/M5/M6/M7/M8a/M8b first.
Those levers alone leave 45,667 LUTs centrally.
Adding M3 and M10 gives **41,867 LUTs**.
No F-lane removal or mailbox replacement is counted here.

**Partial flip:** F0-F4 qualify; F5 remains unqualified.
AECP, notification, originator and their NVM path remain in fabric.
That retains 10,095 LUTs from the full-split basis:
`6,150 + 2,125 + 697 + 542 + 581 = 10,095`.
F1/F3 owns moved binding persistence; fabric retains AECP persistence.
Each field still has one owner; integration must prove arbitration.
The ACMP binding store's 808-LUT removal is conditional on this.

The disjoint removal basis is **8,012 LUTs**:
`523 + 1,561 + 823 + 808 + 3,868 + 429 = 8,012`.
Debit the complete 3,102-LUT mailbox.
Do not assume fewer rings.
Use the complete split's integration and mapping allowances unchanged.
Retained shared timers, pools and dispatch receive no removal credit.

| Partial split case | Calculation | Estimated split saving |
|---|---|---:|
| Conservative | `8,012 - 3,102 - 2,000 - 1,500` | 1,410 |
| Central | `8,012 - 3,102 - 1,000` | 3,910 |
| Optimistic | `8,012 - 3,102 - 500 + 1,500` | 5,910 |

The remaining lanes are M2/M5/M6/M7/M8a/M8b.
Their central saving totals 4,600 LUTs.
Conservative savings total 2,900; optimistic savings total 6,700.
The partial scenario also credits M3/M10's retained-AECP work.
Thus: `50,267 - 3,910 - 4,600 - 3,800 = 37,957`.
Neither this arithmetic nor its range establishes measured savings.
M0s must verify retained ownership, integration cost and timing.

Positive headroom meets the stated LUT bar; negative headroom misses.
The two bars remain distinct; timing qualification remains mandatory.

| Placement | Case | Estimated image LUT | Headroom to 38,040 | Headroom to 37,659 |
|---|---|---:|---:|---:|
| Full split | Conservative | 35,867 | +2,173 | +1,792 |
| Full split | Central | 31,667 | +6,373 | +5,992 |
| Full split | Optimistic | 27,567 | +10,473 | +10,092 |
| No split, including M3/M10 | Conservative | 44,967 | -6,927 | -7,308 |
| No split, including M3/M10 | Central | 41,867 | -3,827 | -4,208 |
| No split, including M3/M10 | Optimistic | 38,467 | -427 | -808 |
| Partial, F5 unqualified | Conservative | 43,557 | -5,517 | -5,898 |
| Partial, F5 unqualified | Central | 37,957 | +83 | -298 |
| Partial, F5 unqualified | Optimistic | 32,557 | +5,483 | +5,102 |

The full split clears both bars in all three estimates.
The no-split cases all miss both bars, including M3/M10.
Partial central clears 38,040 but misses 37,659.
Its conservative case misses both; its optimistic case clears both.
Without M8b, partial central rises to 39,657.
It misses both bars.

No-split needs 3,827 further LUTs centrally for [NFR-RES-01](../reference/FR_NFR.md#35-resource-reliability-and-the-rest).
D8 requires 4,208 further LUTs.
Conservative gaps are tabled above.
The partial central case needs 298 further LUTs for D8.
Its conservative case needs 5,898 to clear both bars.
Qualifying F5 supplies the priced route to the full-split scenario.
When switching scenarios, remove M3/M10 credit to avoid overlap.
If F5 cannot qualify, the manager must commission additional redesign.
The week-4 ruling names its measured target and revised schedule.
No additional lever has earned credit in these fallback totals.
A D8 margin exception alone cannot cure an [NFR-RES-01](../reference/FR_NFR.md#35-resource-reliability-and-the-rest) miss.
It also needs an explicit ruling; no exception is assumed.

### Lane sequence


All parent lanes start from the third adoption, processor `2ad2f845`.
The earlier [#661](https://github.com/kebag-logic/milan-fpga/issues/661) dependency is satisfied on dev `5603c353`.
Weeks count from 2026-10-12; 2026-12-15 is week 10.
This is a schedule estimate, conditional on split qualification.
Each implementation needs its own settled public scope and review.
Independent lanes may proceed concurrently in isolated worktrees.
Measurements queue serially; no Vivado overlaps another heavy build.

| Order / window | Lane | Scope and files | Dependency | Estimated default saving | Required evidence and risk |
|---|---|---|---|---:|---|
| 0, complete | M0 | Adopted processor pin and current three-endpoint record | [#661](https://github.com/kebag-logic/milan-fpga/issues/661), [#682](https://github.com/kebag-logic/milan-fpga/issues/682), [#686](https://github.com/kebag-logic/milan-fpga/issues/686), [#645](https://github.com/kebag-logic/milan-fpga/issues/645)/[#647](https://github.com/kebag-logic/milan-fpga/issues/647) present at assigned dev | Already in 50,267 | Reuse committed record; do not subtract old lane deltas |
| 0s, now through week 3 | M0s | Manager resource bench: split-aware recipe and gate coverage, then two selected-placement routes | First: integrated F0-F4 with fabric AECP; second: F5 merged; both before week 4 and default flip | No assumed saving | Reviewed measurement support; whole-image metrics, timing and D7 comparison; preserve all-fabric references |
| 1, weeks 1-6 | F0-F5 / L2 | [`sw/firmware/ctrl/`](../../sw/firmware/ctrl/), [`sw/firmware/ctrl_nvm/`](../../sw/firmware/ctrl_nvm/), mailbox contract and parent integration; complete F5 and connect the datapath | Approved [#664](https://github.com/kebag-logic/milan-fpga/issues/664) text; F0-F4 foundations present; both M0s measurements and F2-F5 suites/bench before default flip | 14,000 (11,500-16,000) | Highest risk: exact ownership, full service/wire bounds, all streams/counters and soak; no full credit for a partial flip |
| 2, weeks 1-4 | M2 | MAC packet/CDC and CSR AW/W/B/AR/R FIFOs listed in [L3](#l3-ram-friendly-retained-tables); [SoC wiring](../../sw/litex/milan_soc.py) | Adopted pin; confirm post-D4 FIFO survival; settled split interface allocation; measure final split | 200 (100-400) | RAM inference and per-array lockstep; primitive growth still judged by gate |
| 3, weeks 2-6 | M5 | Existing read mux and snapshots in [`hdl/common/csr/milan_csr.sv`](../../hdl/common/csr/milan_csr.sv) | Adopted pin; preserve both placement faces | 600 (400-1,000) | CSR coherence, AXI-Lite timing and firmware readback |
| 4, weeks 2-6 | M6 | AVTP counter contexts, channel-map capture and render set-point under [`hdl/ieee1722/`](../../hdl/ieee1722/) | Adopted pin; fabric media ownership fixed by [#664](https://github.com/kebag-logic/milan-fpga/issues/664) | 600 (400-900) | Update/read/reset hazards, GET_COUNTERS and full datapath |
| 5, weeks 3-6 | M7 | gPTP engine state tables and parent shadow wrapper | Adopted pin; gPTP remains fabric; excludes M2 arrays | 500 (300-700) | gPTP suites, CDC/timestamps and turnaround |
| 6, weeks 2-8 | M8a/M8b | SoC memory/core selection, firmware layout and [#70](https://github.com/kebag-logic/milan-fpga/issues/70)/F1 staging | D4 approved; D5 conditional; measure linked F5 storage and split service before accepting core | 2,700 (1,700-3,700) | Memory capacity, boot, 8x8 capture <= 24.5 ms, SRP churn; revert core if bounds fail |
| 7, decision at week 4; weeks 4-8 | M3 | Retained fabric AECP dispatch, notification, D3 and entity widths in processor | D1/D3 approved; ACMP/ADP portion replaced; schedule residual only for a selected fabric-AECP image | **0**; fabric-only opportunity 2,600 (1,500-3,600) | PDU/port equivalence and complete processor/consumer bank; no F5 overlap |
| 8, weeks 6-9 | M10 | One gPTP/AECP engine across processor integration | D6 planned; requires fabric AECP remaining and M3 preserving a separate removable engine | **0**; fabric-only opportunity 1,200 (900-1,500) | Sharing turnaround proof; removed AECP cannot be saved twice |
| 9, weeks 9-10 | M9 | Final pin adoption, integrated route, timing closure and resource-gate re-record; budget/ledger update | M0s coverage accepted; selected F2-F5 functions qualified; actual M-lane deltas known; required review complete | No assumed saving | <= 38,040 LUT with timing; aim <= 37,659; all suites/campaigns and physical acceptance |

M1 is dropped by D2; M4 is replaced by F4.
M3/M10's listed order is for any retained fabric-AECP work.
They do not block a fully qualified split.
Their zero default contribution follows from F5's ownership change.
The manager assigns those implementation lanes against their chosen placement.

The [Round 1c decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081534590) schedules M0s before the flip.
The manager's resource bench owns its tooling and measurements.
[The split program](https://github.com/kebag-logic/milan-fpga/issues/665) lands behind build switches, defaulting to all-fabric.
M0s selects split placement explicitly; shipping defaults remain unchanged.

M0s runs two steps, both before the week-4 checkpoint:

1. Now: prepare reviewed split-aware measurement support and its controls.
   Route integrated F0-F4 with AECP still in fabric.
   Firmware presence alone does not satisfy the integration prerequisite.
2. After F5 merges: route the complete selected split.
   Finish this measurement before week 4 and any default flip.

The schedule therefore requires F5 integration by week 3.
Qualification may continue through week 6; measurement precedes qualification.
A delayed F5 merge makes M0s's second measurement late.
Report that missed checkpoint explicitly; do not claim full-split evidence.
The planned default flip waits for both measurements and qualification.

At week 4, replace estimates with M0s's routed figures.
Reprice M3/M10 against the measured remaining fabric ownership.
A missed service bound retains the affected function in fabric.
Publish that placement's residual area gap and revised schedule.
Never omit functions or change acceptance to force the target.

D7 uses M0s figures for each selected-placement comparison.
Compare whole-image resources against the last accepted gate record.
Later lanes also publish their delta from matching M0s placement.
This separates integration cost from subsequent lane savings.
Missing or incomparable measurements cannot produce a pass.
Intermediate measurements enter this ledger; only M9 re-records acceptance.

The current [recipe](../../syn/ooc/pp_baseline.py) expects exactly one wrapper.
The complete split removes that wrapper.
M0s must therefore deliver reviewed split-aware recipe and gate coverage.
It precedes both split routes, the checkpoint and default flip.
Name each measured placement and retain comparable whole-image metrics.
Preserve tool/flow identities, route completion, primitive counts and timing.
Retain the all-fabric shipping endpoint and standalone 1x1/8x8 references.
Later lanes record selected routes and both standalone references.
M9 consumes M0s coverage for final qualification and re-recording.
No gate, schema or policy implementation changes occur here.

### Gates at the committed head

48/48 documentation and applicable resource-policy commands returned 0.
All ran with separate logs and rc files; eight concurrent lightweight workers.
Every child was waited for by its foreground driver. No shell pipes.
Pinned Markdown environment and Verilator 5.050 were exported.
Submodule top-level paths were verified before running gates.

| Gate | Command | rc |
|---|---|---:|
| docs_check | `rtk proxy python3 scripts/docs_check.py` | 0 |
| docs_self | `rtk proxy python3 scripts/docs_check.py --selftest` | 0 |
| feature_status | `rtk proxy python3 scripts/check_feature_status.py` | 0 |
| feature_self | `rtk proxy python3 scripts/check_feature_status.py --self-test` | 0 |
| em_dash | `rtk proxy python3 scripts/check_em_dash.py --base 5603c353137e90c1fa95429f6d00ef7a2298d9ee` | 0 |
| em_dash_self | `rtk proxy python3 scripts/check_em_dash.py --selftest` | 0 |
| doc_style | `rtk proxy python3 scripts/check_doc_style.py` | 0 |
| doc_style_self | `rtk proxy python3 scripts/check_doc_style.py --selftest` | 0 |
| gptp_docs | `rtk proxy python3 scripts/check_gptp_docs.py --with-submodule` | 0 |
| gptp_docs_self | `rtk proxy python3 scripts/check_gptp_docs.py --selftest` | 0 |
| doc_map | `rtk proxy python3 docs/DOC_MAP.gen.py --check` | 0 |
| doc_map_self | `rtk proxy python3 docs/DOC_MAP.gen.py --selftest` | 0 |
| timesync | `rtk proxy python3 docs/diagrams/timesync_chain.gen.py --check` | 0 |
| timesync_self | `rtk proxy python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 |
| solution | `rtk proxy python3 scripts/check_solution_docs.py` | 0 |
| solution_self | `rtk proxy python3 scripts/check_solution_docs.py --selftest` | 0 |
| submodule_diagram | `rtk proxy python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 |
| submodule_diagram_self | `rtk proxy python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 |
| submodule_docs | `rtk proxy python3 scripts/check_submodule_docs.py` | 0 |
| submodule_docs_self | `rtk proxy python3 scripts/check_submodule_docs.py --selftest` | 0 |
| diagram_pngs | `rtk proxy python3 scripts/check_diagram_pngs.py` | 0 |
| diagram_pngs_self | `rtk proxy python3 scripts/check_diagram_pngs.py --selftest` | 0 |
| module_matrix | `rtk proxy python3 docs/traceability/gen_module_matrix.py --check` | 0 |
| baremetal | `rtk proxy python3 scripts/check_baremetal_only.py --check` | 0 |
| baremetal_self | `rtk proxy python3 scripts/check_baremetal_only.py --selftest` | 0 |
| doc_paths | `rtk proxy python3 scripts/check_doc_paths.py` | 0 |
| archive | `rtk proxy python3 scripts/check_archive.py` | 0 |
| archive_self | `rtk proxy python3 scripts/check_archive.py --selftest` | 0 |
| toc_self | `rtk proxy python3 scripts/gen_toc.py --selftest` | 0 |
| toc_anchors | `rtk proxy python3 scripts/gen_toc.py --verify-anchors` | 0 |
| toc_check | `rtk proxy python3 scripts/gen_toc.py --check` | 0 |
| todo | `rtk proxy python3 scripts/check_todo_ownership.py` | 0 |
| hygiene | `rtk proxy python3 scripts/check_hygiene.py --check` | 0 |
| wire | `rtk proxy python3 scripts/check_wire_accountability.py --self-test` | 0 |
| resource_baseline | `rtk proxy python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 |
| resource_self | `rtk proxy python3 syn/ooc/pp_resource_gate.py --selftest` | 0 |
| resource_mutants | `rtk proxy python3 syn/ooc/pp_resource_gate_mutants.py` | 0 |
| ci_scope | `rtk proxy python3 scripts/ci_scope.py --selftest` | 0 |
| ci_events | `rtk proxy python3 scripts/ci_events.py --check` | 0 |
| wavedrom_self | `rtk proxy python3 scripts/gen_wavedrom.py --selftest` | 0 |
| wavedrom_axis | `rtk proxy python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 |
| wavedrom_cdc | `rtk proxy python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 |
| wavedrom_gptp | `rtk proxy python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 |
| pp_sources | `rtk proxy python3 scripts/pp_srcs.py --check --selftest` | 0 |
| docs_nogit | `rtk proxy env GIT_DIR=/dev/null python3 scripts/docs_check.py` | 0 |
| gptp_make | `rtk proxy make -j16 -C gptp-processor docs` | 0 |
| diff_base | `rtk proxy git diff --check 5603c353137e90c1fa95429f6d00ef7a2298d9ee HEAD` | 0 |
| diff_tree | `rtk proxy git diff --check` | 0 |

Additional checks:

| Check | Result |
|---|---|
| Adapted reviewer `recompute_ledger.py .` | 174 checks, 0 failures; M8a assumptions and dependent expected values updated |
| `verify_round1c.py .` | 54 scenario cells, M8a arithmetic, partial gross, core fallback, named FIFOs, issue links and unchanged resource JSON pass |
| Reproduction command | All shell blocks pass `bash -n`; three recorded Tcl command traces equal the retained original recipes |

The original reviewer script and adaptation diff are retained.
These are author checks, not independent review verdicts.
First campaign: 48/48 at `cee00f59f`; final campaign: 48/48 at this head.
Final logs: `$VALIDATION_STORAGE/640-a540/round1c/gates-39258a148/`.
Receipt digests: `ROUND1C-GATE-RECEIPTS.txt` beside this handoff.

### Residue and handoff boundaries

`RESIDUE-495.md` identifies remaining presentation observations for the manager.
Carry them to #495 at merge; this lane has no posting authorization there.
Prior long historical/existing prose remains, with no changed measurement claim.
R492-1-R3/R4 are corrected; R1/R2 and R493-1-R1/R2 are addressed at changed passages.
The residual analyzer observations are screening results, not new correctness findings.

No RTL, parameter, port, register-map, gate implementation or resource-record changes.
No synthesis, hardware, bench or flashing action. No push, rebase or amend.
Both reviewers must assess the corrected head; their old verdicts do not approve it.
The manager retains publication, hosted/replica acceptance and merge-candidate duties.
Full-split integration, F5 capacity, service timing and physical qualification remain unproved.
No final hardware acceptance or merge authorization is claimed.


## Round 1d

Status: REVIEW READY at `7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783`.
Starting head: `39258a1486897127288f82fbb1b86333febf6f00`.
Branch: `640-mark2-plan`; origin: `https://github.com/kebag-logic/milan-fpga.git`.
PR #698 was confirmed open on this branch at the starting head.
No push or PR change was performed. The worktree is clean.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081895732
Owner decision: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081706413
F5 preflight: https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081556432
F5 ruling: https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081705916

| Step | Commit | Result |
|---|---|---|
| 1, firmware memory | `9b6a04e10499b060eb25dc7c3d489e03c177c566` | Decision, measured preflight, disjoint memory ledger, expansion priorities and checkpoint duties in both documents |
| 2, arithmetic | `7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783` | Recomputed RAM and LUT ledgers; documented the equation and the unchanged LUT estimates |

Only `docs/design/MARK_II_AREA_PLAN.md` and `docs/design/AREA_BUDGET.md` changed.
New commits only. No RTL, port, register-map, parameter, resource record or gate change.
No new Vivado run, hardware access or physical acceptance claim.
The latest assignment supersedes the initial STOP-only publication rule.
It asks for REVIEW READY on #640, without another TAKEN.

### Baseline, source checkpoint and current inventory

Source: [`pp_resource_baseline.json`](../../syn/ooc/pp_resource_baseline.json), all three `record` objects.
Each `measured` note identifies `a5ca6e5110d515bf5f894f87b94f9bf6f6836bbb`.
That is [#645](https://github.com/kebag-logic/milan-fpga/issues/645)/[#647](https://github.com/kebag-logic/milan-fpga/issues/647)'s measured merge of dev `6aa25dec`.
It uses processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`.
Dev `5603c353137e90c1fa95429f6d00ef7a2298d9ee` carries those records unchanged.
This names the stored baseline, not a measurement of `5603c353`.
No new Vivado measurement was made for Rounds 1b-1d.

| Endpoint | LUT | FF | Slice | RAMB36 | RAMB18 | BRAM tiles | DSP | WNS / WHS ns |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `route-1x1` | 50,267 | 54,413 | 15,779 | 74 | 27 | 87.5 | 14 | +0.299 / +0.031 |
| `ooc-1x1` | 23,179 | 19,779 | -- | 16 | 3 | 17.5 | 8 | -3.562 / +0.159 |
| `ooc-8x8` | 30,135 | 27,380 | -- | 21 | 5 | 23.5 | 8 | -2.278 / +0.159 |

The resource records omit LUTRAM; it is not zero.
The historical inventory below retains its separately measured LUTRAM column.
Standalone timing has unconstrained I/O and proves no integrated fit.
The 8x8 row is a scaling reference, not shipping acceptance.
The route leaves 71 slices and 47.5 physical BRAM tiles.
The 121.5-tile policy ceiling leaves 34 tiles of usable allowance.

[The source receipt](../findings/234_PP_SHADOW_AREA_BASELINE.md#re-baseline-of-2026-10-08-issues-645-and-647)
records the completed route and all four signoff corners.
Its source checkpoint is `alinx_ax7101_route.dcp` from that measurement.
The route log SHA-256 is
`94c0471debaa23a0fd20d9050298173facb997735ffa8bbf451f68cbd82de0ac`
(829,160 bytes).
The record's input SHA-256 values bind the measurement inputs:

| Endpoint | Input SHA-256 |
|---|---|
| `route-1x1` | `95a6cc95786fa743da28e2aa603d3a6af08200c86bf4bb7c452aeba7ec072c4c` |
| `ooc-1x1` | `2dd522bd12b3480a8817cf2bb3dd969ac7be6f3d80be70d13fe32ce5576011a5` |
| `ooc-8x8` | `5604984543f875b19f344900a8b183adf81281c02ba42517ff894502f7a07f0c` |

The recipe uses Vivado 2026.1 build 6511674, `xc7a100t-fgg484-2`.
Directives: `AreaOptimized_high`, `ExploreArea`, `ExtraPostPlacementOpt`, `AggressiveExplore`.
It uses the default seed, one synthesis worker, 32 general threads.
The standalone wrapper clock is 20 ns.
The historical route below predates this synthesis-worker recipe identity.
Its deltas therefore inform planning, not a comparable gate verdict.

### Current processor inventory

These are the current record's source-scope references.
The routed hierarchy is rebuilt and can absorb neighbouring logic.
Use standalone scopes to estimate removable source functionality.
Parent rows include descendants; never add both to a saving.
The [historical inventory](#inventory) supplies functions, clauses and construction.

| Scope relative to wrapper | Route LUT | OOC 1x1 LUT | OOC 8x8 LUT | Split disposition |
|---|---:|---:|---:|---|
| `wrapper` | 23,345 | 23,179 | 30,135 | Replaced after every control function qualifies |
| `u_pp` | 22,794 | 22,517 | 28,938 | Control functions move; retained fabric interfaces are reconnected |
| `u_pp/u_aecp` | 8,084 | 6,150 | 7,298 | F5; includes the following five children |
| `u_pp/u_aecp/u_d3` | 1,781 | 1,703 | 2,297 | F1/F5 saved-state ownership |
| `u_pp/u_aecp/u_dyn` | 1,440 | 134 | 497 | F5; fabric media state stays authoritative |
| `u_pp/u_aecp/u_store` | 979 | 1,026 | 1,119 | F5 validated image and names |
| `u_pp/u_aecp/u_ucpu` | 1,727 | 1,553 | 1,651 | F5; no second M10 credit |
| `u_pp/u_aecp/u_resp` | 345 | 432 | 416 | F5 response serving |
| `u_pp/u_notify` | 2,259 | 2,125 | 2,114 | F5 registry, notification and counter serving |
| `u_pp/u_srp` | 3,682 | 3,868 | 7,312 | F4; media admission enforcement remains in fabric |
| `u_pp/u_srp/u_encoder` | 1,358 | 1,479 | 1,466 | Included in SRP |
| `u_pp/u_srp/u_decoder` | 579 | 588 | 922 | Included in SRP |
| `u_pp/u_listener` | 1,451 | 1,560 | 1,681 | F3 ACMP listener |
| `u_pp/u_talker` | 641 | 823 | 1,472 | F3 ACMP talker |
| `u_pp/u_adp` | 385 | 523 | 696 | F0/F3 advertisement and discovery |
| `u_pp/u_originator` | 687 | 697 | 682 | F3/F5 originated transactions |
| `u_pp/u_nvm_shadow` | 792 | 808 | 780 | F1/F3 binding persistence |
| `u_pp/u_nvm_port` | 513 | 526 | 524 | F1 store and flash service |
| `u_nvm` | 486 | 581 | 1,116 | F1 replaces container backend |
| `u_pp/u_timer` | 882 | 906 | 1,631 | Hard deadlines remain fabric events; no saving credited |
| `u_pp/u_dispatch` | 665 | 887 | 908 | Replaced routing; no separate credit |
| `u_pp/u_trace` | 31 | 37 | 28 | Equivalent diagnostics retained; no credit |

The [#232](https://github.com/kebag-logic/milan-fpga/issues/232) registry, [#230](https://github.com/kebag-logic/milan-fpga/issues/230) SRP storage and [#639](https://github.com/kebag-logic/milan-fpga/issues/639) rings/listener changes
are already included; their savings cannot be subtracted again.
[#686](https://github.com/kebag-logic/milan-fpga/issues/686) also changed MAAP, before [#645](https://github.com/kebag-logic/milan-fpga/issues/645)/[#647](https://github.com/kebag-logic/milan-fpga/issues/647) refreshed the record.

### Current levers, bases, risks and verification costs

The historical function/clause inventory remains in the earlier handoff and plan.
The following current levers preserve its source references.

The [ledger](#ledger) owns the current numerical estimates.
Historical measurements support estimates; none proves a redesigned image fits.
Every lane measures its actual delta before adopting a saving.
All implemented paths must preserve wire semantics and normative ordering.
D1/D3 permit bounded internal latency changes with reviewed equivalence evidence.

### L1 Shared sequencing in retained fabric control

ACMP/ADP sequencing and SRP L1b are superseded by F0-F5.
M3 retains only the AECP/notification/record-manager residual for fabric AECP.
Its estimate is 2,600 LUTs (1,500-3,600), zero in the default image.
The ledger derives it from current standalone scopes, less engine overhead.

**Risk: high.** Shared sequencing changes contention and internal latency.
Each response path needs a deterministic bound under maximum fan-out.
**Verification:** processor suites and campaigns at their recorded counts;
PDU/port-transaction differential checks; parent consumers, `pp_shadow`,
`nvm_cosim`, `milan_dp`, capture bounds and bench compliance.
Cycle-pinned tests are retargeted under review, never removed.
The interface index remains in all contexts.

### L2 Default control split

F0-F5 transfers ADP, ACMP, MAAP, SRP and AECP control ownership.
F1 supplies flash validation, boot apply and transactional write-back.
The [split contract](../ARCHITECTURE_HW_SW_SPLIT.md) keeps one owner per function.
The [mailbox contract](MAILBOX_SPLIT.md) provides filtered packet mailboxes and events.
The earlier CSR-only interface proposal is superseded.

**Saving:** estimated 14,000 LUTs, range 11,500-16,000.
The ledger shows disjoint removal references and all cost allowances.
The measured mailbox skeleton costs 3,102 LUTs and six BRAM tiles.
F0-F4 code is present at the assigned dev revision.
Presence does not establish integrated, bench-qualified operation.
The [SoC wiring](../../sw/litex/milan_soc.py) holds the mailbox datapath idle.
[`milan_datapath.sv`](../../hdl/milan/milan_datapath.sv) still instantiates `KL_pp_shadow` unconditionally.
Consequently, enabling `--ctrl-mailbox` alone saves no processor logic.

**What leaves after qualification:** the selected protocol engines, their
private tables, notification and descriptor serving, and fabric NVM serialization.
The complete flip removes `KL_pp_shadow` from the default build.
Equivalent settings, counters, diagnostics and media controls must remain accessible.
Framing, timestamps, ingress filtering, hard-deadline event timers, gPTP,
AVTP/AAF/CRF, media admission and physical audio stay in fabric.
A software protocol owner must not become a software media path.

**Risk: high.** Target service time, ring backlog, flash interference,
firmware capacity and F5 qualification remain implementation obligations.
The [owner's memory decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081706413) replaces the earlier approximately 128 KB budget.
F5's limit is now 224 KB, including AECP.
Budget about 50 RAMB36 tiles for firmware.
The [memory ledger](#firmware-and-block-ram-ledger) includes the measured preflight and packing risk.
Measure linked code, data, stack, static pools and saved-state staging.
The current ROM parameter does not establish Mark II capacity.

**Verification:** F0 mailbox tests on both adapters, filter mutation campaigns,
F1 store tests, F2-F5 unit and differential protocol suites,
RV32 execution and the [service hooks](../reference/FR_NFR.md#342-control-service-test-hooks).
Prove 10 ms project service under bounded ingress, SRP churn,
full rings, all recipients, flash activity and delayed events.
Prove wire deadlines separately; mailbox commit is insufficient evidence.
Retain all-fabric suites and compare reused stimuli at unchanged counts.
Bench acceptance covers every stream, counters and audio soak.
Unqualified functions remain all-fabric until their acceptance passes.

### L3 RAM-friendly retained tables

M2 covers retained SoC FIFOs, identified below after D4.
**Saving:** 200 LUTs (100-400), reduced from the original 800.
The old inventory included processor tables removed by L2.
gPTP belongs to M7; media context tables belong to M6.
The historical RAM census motivates this target.
[#639](https://github.com/kebag-logic/milan-fpga/issues/639) illustrates storage tradeoffs, not these FIFOs' measured savings.
Budget up to two extra tiles, subject to measured primitive counts.

[The SoC wiring](../../sw/litex/milan_soc.py) names the surviving scope:

| Retained object | Purpose after D4 | M2 treatment |
|---|---|---|
| `MilanMAC.tx_sf` payload and parameter FIFOs | Gapless complete-frame transmission | Already synchronous block-RAM storage; no credit for its earlier conversion |
| `MilanMAC.mac_tx_cdc`, `MilanMAC.mac_rx_cdc` | MAC/datapath crossings at distinct clocks | Inspect residual storage and control; retain buffering and paired reset |
| `milan_axil_cdc` AW/W/B/AR/R FIFOs | CPU-to-datapath CSR crossing at distinct clocks | Inspect shallow storage and control; preserve AXI-Lite ordering and coherent snapshots |

D4 removes DDR3, not the MAC or CSR crossings.
The estimate is an aggregate target for this surviving scope.
It is not a measured per-FIFO saving.
Preserve widths, depths, throughput, reset behavior and clock-domain contracts.
The implemented conversion and its LUT saving still need proof.
Already inferred block RAM supplies no second conversion credit.

Exclude LiteDRAM bank-machine, command, read and write queues.
Exclude `memory_port_cdc*` and CPU-internal bridge FIFOs under M8.
Exclude `descmem_*`, `respmem_*` and `nvmmem_*` crossings under L2/M8.
Their retained-AECP variants remain those lanes' responsibility.
Mailbox rings belong to L2.
Media/gPTP tables belong to M6/M7.
Reconcile the actual post-D4 export before assigning any M2 saving.

**Risk: medium.** Same-cycle reads may prevent block RAM inference.
**Verification:** per-array lockstep and negative controls, owning suites,
both shapes, primitive mapping and integrated route.
Read latency changes require D3's deterministic bounds.

### L4 Entity-derived widths

Wire IDs, addresses, sequence numbers and counters retain standard widths.
Only implementation indices can narrow from the generated entity shape.
The historical 200-LUT estimate is included in M3's residual.
It receives zero default-split credit.
[#233](https://github.com/kebag-logic/milan-fpga/issues/233) already found shipping stream geometry fully derived.

**Risk: low. Verification:** boundary indices, all supported shapes,
refusals and owning suites; unchanged wire bytes.

### L5 Remaining specialization items

VLAN reference widths, descriptor lines and queue depths need measurement.
The original 30-100 LUT estimate remains reference material only.
SRP's work leaves with F4; AECP residue belongs to M3.
Neither adds another default-split credit.
Depth reductions require burst/backpressure evidence and protocol capacity.
GET_DYNAMIC_INFO still requires its 524-byte response capacity.

**Risk: low to medium. Verification:** owning SRP, notification,
dispatch and AECP suites, including worst-case backlog.

### L6 Diagnostics retained

D2 rejects diagnostic pruning from the shipping image.
The earlier 700-LUT opportunity is dropped, with zero saving.
Latency taps, probe information and equivalent control diagnostics remain.
Milan counter producers were never optional diagnostic prunes.
The split's integration allowance includes retained control observability.

**Verification:** diagnostic readback, counter coherence and builder presence checks.
No implementation lane is opened to disable them.

### L7 SRP shared evaluator

F4 replaces M4 and L1b/L7 in the default plan.
The historical 450-LUT estimate is not an additional saving.
A supported fabric SRP implementation may revisit it separately.

**Risk: medium.** Serialized event handling changes internal latency.
**Verification:** SRP suites/campaigns at both shapes, event stalls,
MRP timers and bench protocol checks under D3.

### L8 CSR read path

M5 restructures the existing live-status read mux and snapshots.
**Saving:** 600 LUTs (400-1,000), from the historical 2,907-LUT block
and [#649](https://github.com/kebag-logic/milan-fpga/issues/649)'s 2,893 fixed plus 211-per-stream OOC model.
New split-interface logic is charged to L2, not saved again here.

**Risk: medium.** Snapshot coherence and AXI-Lite latency must hold.
**Verification:** CSR, `tcam_csr`, `milan_dp`, firmware host tests,
register-map checks and boot readback in both placements.
Register addresses, widths and reset values remain unchanged by M5.

### L9 Media context tables

M6 owns listener/talker counters, channel-map capture and render set-point.
**Saving:** 600 LUTs (400-900), from the historical routed inventory
and [#649](https://github.com/kebag-logic/milan-fpga/issues/649)'s per-stream OOC marginals of 208, 317 and 205.
These datapath functions remain fabric-owned in the split.

**Risk: medium.** Read-modify-write hazards can break coherent counters.
**Verification:** `avtp_rxmon`, `tkdiag`, `chmap_capture`, `render_setpoint`,
`milan_dp`, GET_COUNTERS, wrap/reset and concurrent update cases.
No M2 table credit overlaps these arrays.

### L10 Fabric gPTP

M7 moves eligible gPTP tables into block RAM or narrows indices.
**Saving:** 500 LUTs (300-700), based on 464 historical LUTRAM LUTs.
Dual-read operand files remain where required.
M10 shares gPTP and AECP execution only in retained-fabric AECP builds.
Its estimated 1,200 LUTs (900-1,500) has zero default-image credit.
F5 already removes the AECP engine in the split.

**Risk:** medium for tables; high for shared execution and turnaround.
**Verification:** gPTP processor suites, `gptp_plane`, `gptp_shadow`,
`gptp_txts`, `milan_dp_gptp`, timestamp/CDC checks and [#117](https://github.com/kebag-logic/milan-fpga/issues/117) bench evidence.
M10 additionally proves arbitration and worst-case gPTP turnaround.
Audio and gPTP deadlines remain independent of firmware service.

### L11 The SoC side

D4 approves on-chip main memory instead of DDR3.
M8a sizes [#70](https://github.com/kebag-logic/milan-fpga/issues/70)/F1 staging to the selected shape's container.
**Saving:** 1,000 LUTs (400-1,500), repriced in Round 1c.
The [historical census](../findings/649_RESOURCE_MAP_AND_SENSITIVITY.md#the-soc-tops-own-logic) reports pre-packing LUT cells.
Its controller has 823; its PHY has 873.
The 1,696 cells do not identify packed LUT sites.
Another 3,231 anonymous LUT cells have no assigned owner.
Their DDR share is unknown and receives zero credit.

The estimate uses explicit packing and replacement assumptions:

| Case | Named cells retained as LUT sites | Replacement debit, LUT | Net calculation | Rounded saving |
|---|---:|---:|---|---:|
| Conservative | 50 percent | 400 | `1,696 * 0.50 - 400 = 448` | 400 |
| Central | 75 percent | 250 | `1,696 * 0.75 - 250 = 1,022` | 1,000 |
| Optimistic | 100 percent | 100 | `1,696 - 100 = 1,596` | 1,500 |

Each result rounds down to the preceding hundred LUTs.
The packing shares bracket paired and unpaired named cells.
Replacement allowances cover on-chip decode, arbitration and storage control.
These are planning assumptions, not measured conversion ratios or bounds.
Shared sites or larger replacement logic can erase that saving.
Anonymous DDR logic could instead increase the measured saving.
M8a must replace these assumptions with a routed delta.
M0s and M9 retain independent primitive and memory-capacity checks.
M8a replaces the existing CPU memory allocation within the 50-tile budget.
It must reconcile that reuse against the [memory ledger](#firmware-and-block-ram-ledger).
The lane owns its memory-map migration and both placement contracts.

D5 conditionally approves a smaller cacheless RV32I control hart.
**Saving:** 1,700 LUTs (1,300-2,200).
This includes 300-600 retained bridge LUTs.
The original same-part `AreaOptimized_high` OOC pricing was:

| Core/netlist | LUT | FF | BRAM tiles |
|---|---:|---:|---:|
| Shipping VexiiRiscv netlist, including bus bridges | 3,066 | 5,017 | 4.5 |
| VexRiscv Min | 843 | 791 | 1 |
| PicoRV32 minimal | 1,051 | 549 | 0 |

These are isolated netlists, not integrated replacement measurements.
**Risk: high.** CPU service and on-chip capacity can invalidate estimates.
Prove 8x8 capture <= 24.5 ms with [`check_nvm_capture.py`](../../scripts/check_nvm_capture.py).
Keep boot timing and recheck service under filtered SRP churn.
A smaller core failing those conditions is reverted.

**Verification:** firmware host tests, `nvm_cosim` and `nvm_capture_cpu`.
Also run builder/deploy gates and target service hooks.
Repeat bench boot and persistence checks.
The all-fabric option still needs its response and staging memory.
Neither 8x8 nor F5 memory fit is established.

### L12 Functional prunes excluded

RX filtering, loopback, media-clock servo, CRF and rendering remain.
Milan's 16-controller minimum remains in either placement.
MAAP's protocol remains required; F2 relocates its implementation.
No protocol surface is removed to achieve area savings.

### Round 1d memory ledger and expansion order

The [owner decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081706413) allocates about 50 RAMB36 tiles to firmware.
The [F5 ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081705916) sets its linked-image limit at 224 KB, AECP included.
This supersedes the approximately 128 KB figure.
The device still reserves 13.5 of its 135 tiles.
The usable ceiling remains 121.5 tiles.

The [F5 sizing preflight](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081556432) used dev `5603c353`.
It linked existing protocol code with the F1 store retained.
It contained neither AECP nor its descriptor image.

| Preflight shape | Linked span, bytes | Status |
|---|---:|---|
| Shipping 1x1, one interface | 94,688 | Size fixture; AECP absent |
| Largest supported shape, two interfaces | 147,360 | Size fixture; AECP absent |

The largest fixture has 56,948 text and 3,458 rodata bytes.
Data is zero; BSS is 78,744 bytes, including static pools.
Its stack reservation is 8,192 bytes.
Those sections total 147,342 bytes; link alignment adds 18.
Do not add the pools to BSS again.
These are measured link spans, not an irreducible minimum.
They establish neither F5 completion nor mapped RAMB36 counts.

The 50-tile figure uses approximately 4.5 KB per RAMB36.
That is raw capacity; mapping can expose less usable storage.
For example, 224 KiB needs 56 tiles at 4 KiB usable each.
That example is a packing check, not a new F5 threshold.
M8a must report actual usable bytes and allocated primitives.

This ledger first withholds the wrapper's remaining 11 tiles.
It credits only the same removed scopes as L2's LUT basis.
RAMB18 counts as half a tile; deltas carry their signs.
The firmware row replaces CPU memory, so replacement storage counts once.

| Item | RAMB36 delta | RAMB18 delta | Tile delta | Image tiles after |
|---|---:|---:|---:|---:|
| Recorded route at `a5ca6e51` | 74 | 27 | 87.5 | 87.5 |
| L2 credited removals: AECP and SRP storage | -6 | -1 | -6.5 | 81 |
| Measured mailbox replacement | +1 | +10 | +6 | 87 |
| M8a reuse of existing BIOS ROM and SRAM, estimate | -18 | -1 | -18.5 | 68.5 |
| Total firmware allocation, including reused CPU memory | +50 | 0 | +50 | 118.5 |
| M2 maximum additional allocation | +2 | 0 | +2 | 120.5 |
| Conditional release of remaining wrapper storage | -10 | -2 | -11 | 109.5 |

The base and wrapper counts come from the [route record](../../syn/ooc/pp_resource_baseline.json).
The [mailbox measurement](MAILBOX_SPLIT.md#measured-area) supplies its debit.
The reuse estimate comes from the [earlier SoC census](../findings/649_RESOURCE_MAP_AND_SENSITIVITY.md#the-soc-tops-own-logic).
That census reports BIOS ROM/SRAM at 18 RAMB36 and one RAMB18.
It is historical attribution, not a new census of `a5ca6e51`.
M8a must confirm the reusable count at its actual checkpoint.
Any retained boot memory outside the firmware allocation adds a debit.
The allocation must also contain stack, pools and shape-sized saved-state staging.
Any descriptor image or alignment space outside it adds a debit.
No separate smaller-core RAM saving is credited.

Arithmetic in tiles: `87.5 - 6.5 + 6 - 18.5 + 50 + 2 = 120.5`.
The conditional release subtracts eleven once, giving 109.5.
These memory entries grant no additional LUT saving.
The LUT estimates remain 31,667 central and 27,567-35,867 across the range.
They depend on fitting the credited RAM conversions within the ledger.

Before the conditional release, the estimate leaves one tile below 121.5.
After it, 109.5 tiles leaves twelve below that ceiling.
Both leave the separate 13.5-tile reserve untouched.
Neither number proves integrated fit.
Unpriced M6/M7 RAM conversions and integration buffers consume that allowance.
Each lane must debit them before accepting its LUT saving.
Without the estimated CPU-memory reuse, those totals become 139 and 128.
Both exceed the ceiling; reuse is a prerequisite, not free headroom.

**What gives way above 50 firmware tiles:** the remaining wrapper storage.
These disjoint scopes are outside the six AECP tiles and SRP half-tile:

| Released fabric scope, relative to wrapper | RAMB36 | RAMB18 | Tiles |
|---|---:|---:|---:|
| `u_pp/g_rx_pool[0,1,2,4,5].u_rx_slots`, five separate pools | 5 | 0 | 5 |
| `u_pp/u_mrp_strip` | 1 | 0 | 1 |
| `u_pp/u_tx_slots` | 1 | 0 | 1 |
| `u_pp/u_timer` | 1 | 0 | 1 |
| `u_pp/u_trace` | 1 | 0 | 1 |
| `u_pp/u_rx_validator` | 0 | 1 | 0.5 |
| `ctl_fifo` | 1 | 1 | 1.5 |
| Total | 10 | 2 | 11 |

Full-split integration must remove these stores before claiming their capacity.
Debit every replacement event, queue or diagnostic store separately.
Equivalent observability remains required by D2.
The measured mailbox already supplies its own queues and timers.
Do not credit its storage or these released stores twice.
At 56 firmware tiles, the conditional total becomes 115.5 tiles.
It leaves six below the ceiling, before other unpriced debits.
Beyond that allowance, defer M2's two-tile MAC/CSR FIFO conversion first.
Keep its existing storage and reprice the associated LUT saving.
Defer new M6/M7 block-RAM conversions next, with the same repricing.
No media buffer, diagnostic function or protocol capacity is pruned.
If these trades still exceed 121.5, the manager must commission further redesign.

Partial placement retains AECP's six tiles and any still-used wrapper stores.
With the same 50-tile hold, the pre-release estimate becomes 126.5.
That is five tiles over the ceiling, before extra fabric-AECP staging.
M0s must substitute measured firmware use and actual retained storage.
A partial route cannot borrow the full split's reclamation credits.
The all-fabric option needs its own complete memory reconciliation.

**Checkpoint evidence:** both M0s routes, the default flip and M9 report this ledger.
Record linked text, rodata, data, BSS, stack and static pools.
Count pools once; report alignment, descriptor images and staging separately.
Cover shipping and largest supported shapes, at one and two interfaces.
Report allocated RAMB36/RAMB18, usable bytes and unused firmware capacity.
Name the five largest BSS consumers and a reduction option each.
F5 implements no reductions outside AECP's own footprint.
Publish whole-image LUT, FF, RAMB36/RAMB18 and timing at each routed checkpoint.
Reconcile removals, replacement debits and actual firmware allocation against 121.5.
The default flip requires firmware resident in block RAM and the reserve intact.
Missing measurements or an exceeded ceiling cannot qualify the flip.

### Current lane sequence

All parent lanes start from the third adoption, processor `2ad2f845`.
The earlier [#661](https://github.com/kebag-logic/milan-fpga/issues/661) dependency is satisfied on dev `5603c353`.
Weeks count from 2026-10-12; 2026-12-15 is week 10.
This is a schedule estimate, conditional on split qualification.
Each implementation needs its own settled public scope and review.
Independent lanes may proceed concurrently in isolated worktrees.
Measurements queue serially; no Vivado overlaps another heavy build.

| Order / window | Lane | Scope and files | Dependency | Estimated default saving | Required evidence and risk |
|---|---|---|---|---:|---|
| 0, complete | M0 | Adopted processor pin and current three-endpoint record | [#661](https://github.com/kebag-logic/milan-fpga/issues/661), [#682](https://github.com/kebag-logic/milan-fpga/issues/682), [#686](https://github.com/kebag-logic/milan-fpga/issues/686), [#645](https://github.com/kebag-logic/milan-fpga/issues/645)/[#647](https://github.com/kebag-logic/milan-fpga/issues/647) present at assigned dev | Already in 50,267 | Reuse committed record; do not subtract old lane deltas |
| 0s, now through week 3 | M0s | Manager resource bench: split-aware recipe and gate coverage, then two selected-placement routes | First: integrated F0-F4 with fabric AECP; second: F5 merged; both before week 4 and default flip | No assumed saving | Reviewed measurement support; whole-image metrics, memory-ledger reconciliation, timing and D7 comparison; preserve all-fabric references |
| 1, weeks 1-6 | F0-F5 / L2 | [`sw/firmware/ctrl/`](../../sw/firmware/ctrl/), [`sw/firmware/ctrl_nvm/`](../../sw/firmware/ctrl_nvm/), mailbox contract and parent integration; complete F5 and connect the datapath | Approved [#664](https://github.com/kebag-logic/milan-fpga/issues/664) text; F0-F4 foundations present; both M0s measurements, firmware in block RAM within the ledger, and F2-F5 suites/bench before default flip | 14,000 (11,500-16,000) | Highest risk: exact ownership, full service/wire bounds, all streams/counters and soak; no full credit for a partial flip |
| 2, weeks 1-4 | M2 | MAC packet/CDC and CSR AW/W/B/AR/R FIFOs listed in [L3](#l3-ram-friendly-retained-tables); [SoC wiring](../../sw/litex/milan_soc.py) | Adopted pin; confirm post-D4 FIFO survival; settled split interface allocation; measure final split | 200 (100-400) | RAM inference and per-array lockstep; primitive growth still judged by gate |
| 3, weeks 2-6 | M5 | Existing read mux and snapshots in [`hdl/common/csr/milan_csr.sv`](../../hdl/common/csr/milan_csr.sv) | Adopted pin; preserve both placement faces | 600 (400-1,000) | CSR coherence, AXI-Lite timing and firmware readback |
| 4, weeks 2-6 | M6 | AVTP counter contexts, channel-map capture and render set-point under [`hdl/ieee1722/`](../../hdl/ieee1722/) | Adopted pin; fabric media ownership fixed by [#664](https://github.com/kebag-logic/milan-fpga/issues/664) | 600 (400-900) | Update/read/reset hazards, GET_COUNTERS and full datapath |
| 5, weeks 3-6 | M7 | gPTP engine state tables and parent shadow wrapper | Adopted pin; gPTP remains fabric; excludes M2 arrays | 500 (300-700) | gPTP suites, CDC/timestamps and turnaround |
| 6, weeks 2-8 | M8a/M8b | SoC memory/core selection, firmware layout and [#70](https://github.com/kebag-logic/milan-fpga/issues/70)/F1 staging | D4 approved; D5 conditional; reconcile 50-tile firmware allocation and measured linked storage; prove split service before accepting core | 2,700 (1,700-3,700) | Memory capacity, boot, 8x8 capture <= 24.5 ms, SRP churn; revert core if bounds fail |
| 7, decision at week 4; weeks 4-8 | M3 | Retained fabric AECP dispatch, notification, D3 and entity widths in processor | D1/D3 approved; ACMP/ADP portion replaced; schedule residual only for a selected fabric-AECP image | **0**; fabric-only opportunity 2,600 (1,500-3,600) | PDU/port equivalence and complete processor/consumer bank; no F5 overlap |
| 8, weeks 6-9 | M10 | One gPTP/AECP engine across processor integration | D6 planned; requires fabric AECP remaining and M3 preserving a separate removable engine | **0**; fabric-only opportunity 1,200 (900-1,500) | Sharing turnaround proof; removed AECP cannot be saved twice |
| 9, weeks 9-10 | M9 | Final pin adoption, integrated route, timing closure and resource-gate re-record; budget/ledger update | M0s coverage accepted; selected F2-F5 functions qualified; actual M-lane deltas known; required review complete | No assumed saving | <= 38,040 LUT with timing; aim <= 37,659; all suites/campaigns and physical acceptance |

M1 is dropped by D2; M4 is replaced by F4.
M3/M10's listed order is for any retained fabric-AECP work.
They do not block a fully qualified split.
Their zero default contribution follows from F5's ownership change.
The manager assigns those implementation lanes against their chosen placement.

The [Round 1c decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081534590) schedules M0s before the flip.
The manager's resource bench owns its tooling and measurements.
[The split program](https://github.com/kebag-logic/milan-fpga/issues/665) lands behind build switches, defaulting to all-fabric.
M0s selects split placement explicitly; shipping defaults remain unchanged.

M0s runs two steps, both before the week-4 checkpoint:

1. Now: prepare reviewed split-aware measurement support and its controls.
   Route integrated F0-F4 with AECP still in fabric.
   Firmware presence alone does not satisfy the integration prerequisite.
2. After F5 merges: route the complete selected split.
   Finish this measurement before week 4 and any default flip.

The schedule therefore requires F5 integration by week 3.
Qualification may continue through week 6; measurement precedes qualification.
A delayed F5 merge makes M0s's second measurement late.
Report that missed checkpoint explicitly; do not claim full-split evidence.
The planned default flip waits for both measurements and qualification.
Both M0s routes reconcile RAMB36 use against the [memory ledger](#firmware-and-block-ram-ledger).
The flip reports its own routed LUT, FF and RAMB36 use.
Its firmware resides in block RAM, with the 10 percent reserve intact.

At week 4, replace estimates with M0s's routed figures.
Reprice M3/M10 against the measured remaining fabric ownership.
A missed service bound retains the affected function in fabric.
Publish that placement's residual area gap and revised schedule.
Never omit functions or change acceptance to force the target.

D7 uses M0s figures for each selected-placement comparison.
Compare whole-image resources against the last accepted gate record.
Later lanes also publish their delta from matching M0s placement.
This separates integration cost from subsequent lane savings.
Missing or incomparable measurements cannot produce a pass.
Intermediate measurements enter this ledger; only M9 re-records acceptance.

The current [recipe](../../syn/ooc/pp_baseline.py) expects exactly one wrapper.
The complete split removes that wrapper.
M0s must therefore deliver reviewed split-aware recipe and gate coverage.
It precedes both split routes, the checkpoint and default flip.
Name each measured placement and retain comparable whole-image metrics.
Preserve tool/flow identities, route completion, primitive counts and timing.
Retain the all-fabric shipping endpoint and standalone 1x1/8x8 references.
Later lanes record selected routes and both standalone references.
M9 consumes M0s coverage for final qualification and re-recording.
No gate, schema or policy implementation changes occur here.

### Gates on the committed head

Head: `7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783`. Full campaign: **51/51 commands returned 0**.
Commands ran concurrently with eight workers, separate logs and rc files, no pipes.
The foreground driver waited for every child process before exiting 0.
`make` used `-j16`. The driver exported the pinned Verilator path.
The pinned Markdown interpreter was `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3`.
All three required submodule toplevels were verified before the gates.
The comparison base is `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
It equals `git merge-base origin/dev HEAD` in this worktree.
`EVIDENCE` in the table denotes this output directory.

| Gate | Command | rc |
|---|---|---:|
| docs_check | `rtk proxy python3 scripts/docs_check.py` | 0 |
| docs_self | `rtk proxy python3 scripts/docs_check.py --selftest` | 0 |
| feature_status | `rtk proxy python3 scripts/check_feature_status.py` | 0 |
| feature_self | `rtk proxy python3 scripts/check_feature_status.py --self-test` | 0 |
| em_dash | `rtk proxy python3 scripts/check_em_dash.py --base 5603c353137e90c1fa95429f6d00ef7a2298d9ee` | 0 |
| em_dash_self | `rtk proxy python3 scripts/check_em_dash.py --selftest` | 0 |
| doc_style | `rtk proxy python3 scripts/check_doc_style.py` | 0 |
| doc_style_self | `rtk proxy python3 scripts/check_doc_style.py --selftest` | 0 |
| gptp_docs | `rtk proxy python3 scripts/check_gptp_docs.py --with-submodule` | 0 |
| gptp_docs_self | `rtk proxy python3 scripts/check_gptp_docs.py --selftest` | 0 |
| doc_map | `rtk proxy python3 docs/DOC_MAP.gen.py --check` | 0 |
| doc_map_self | `rtk proxy python3 docs/DOC_MAP.gen.py --selftest` | 0 |
| timesync | `rtk proxy python3 docs/diagrams/timesync_chain.gen.py --check` | 0 |
| timesync_self | `rtk proxy python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 |
| solution | `rtk proxy python3 scripts/check_solution_docs.py` | 0 |
| solution_self | `rtk proxy python3 scripts/check_solution_docs.py --selftest` | 0 |
| submodule_diagram | `rtk proxy python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 |
| submodule_diagram_self | `rtk proxy python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 |
| submodule_docs | `rtk proxy python3 scripts/check_submodule_docs.py` | 0 |
| submodule_docs_self | `rtk proxy python3 scripts/check_submodule_docs.py --selftest` | 0 |
| diagram_pngs | `rtk proxy python3 scripts/check_diagram_pngs.py` | 0 |
| diagram_pngs_self | `rtk proxy python3 scripts/check_diagram_pngs.py --selftest` | 0 |
| module_matrix | `rtk proxy python3 docs/traceability/gen_module_matrix.py --check` | 0 |
| baremetal | `rtk proxy python3 scripts/check_baremetal_only.py --check` | 0 |
| baremetal_self | `rtk proxy python3 scripts/check_baremetal_only.py --selftest` | 0 |
| doc_paths | `rtk proxy python3 scripts/check_doc_paths.py` | 0 |
| archive | `rtk proxy python3 scripts/check_archive.py` | 0 |
| archive_self | `rtk proxy python3 scripts/check_archive.py --selftest` | 0 |
| toc_self | `rtk proxy python3 scripts/gen_toc.py --selftest` | 0 |
| toc_anchors | `rtk proxy python3 scripts/gen_toc.py --verify-anchors` | 0 |
| toc_check | `rtk proxy python3 scripts/gen_toc.py --check` | 0 |
| todo | `rtk proxy python3 scripts/check_todo_ownership.py` | 0 |
| hygiene | `rtk proxy python3 scripts/check_hygiene.py --check` | 0 |
| wire | `rtk proxy python3 scripts/check_wire_accountability.py --self-test` | 0 |
| resource_baseline | `rtk proxy python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 |
| resource_self | `rtk proxy python3 syn/ooc/pp_resource_gate.py --selftest` | 0 |
| resource_mutants | `rtk proxy python3 syn/ooc/pp_resource_gate_mutants.py` | 0 |
| ci_scope | `rtk proxy python3 scripts/ci_scope.py --selftest` | 0 |
| ci_events | `rtk proxy python3 scripts/ci_events.py --check` | 0 |
| wavedrom_self | `rtk proxy python3 scripts/gen_wavedrom.py --selftest` | 0 |
| wavedrom_axis | `rtk proxy python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 |
| wavedrom_cdc | `rtk proxy python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 |
| wavedrom_gptp | `rtk proxy python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 |
| pp_sources | `rtk proxy python3 scripts/pp_srcs.py --check --selftest` | 0 |
| docs_nogit | `rtk proxy env GIT_DIR=/dev/null python3 scripts/docs_check.py` | 0 |
| gptp_make | `rtk proxy make -j16 -C gptp-processor docs` | 0 |
| diff_base | `rtk proxy git diff --check 5603c353137e90c1fa95429f6d00ef7a2298d9ee HEAD` | 0 |
| diff_tree | `rtk proxy git diff --check` | 0 |
| recompute_ledger | `rtk proxy python3 "$EVIDENCE/recompute_ledger.py" .` | 0 |
| verify_round1c | `rtk proxy python3 "$EVIDENCE/verify_round1c.py" .` | 0 |
| verify_round1d | `rtk proxy python3 "$EVIDENCE/verify_round1d.py" .` | 0 |

The resource self-test passed 260 arms and 500 generated cases.
The mutant campaign passed its control and rejected all 174 mutants.
The preserved LUT checker passes 174 checks.
The Round 1c recomputation passes 54 scenario cells and the conditional cases.
The Round 1d recomputation passes 80 memory table cells.
It verifies the disjoint wrapper partition, historical CPU-memory reuse,
preflight spans, packing, partial placement, reserve and unchanged resource record.
The first memory-check attempt exposed a generator-consumption bug in the checker.
Its summation now materializes the input before reading both primitive columns.
No document value or expected result changed to obtain that pass.
All three checkers returned 0 in the final campaign.

Logs: `$VALIDATION_STORAGE/640-a540/round1d/gates-7387bb6f6/`.
Exact commands, log sizes and SHA-256 digests: `ROUND1D-GATE-RECEIPTS.txt`.
The three final arithmetic logs and their scripts are retained in this packet.
No toolchain, virtual environment, package or tree export was added here.
Every output file is below 200,000 bytes.
No heavy build ran; no new build artifact requires cleanup.

### Remaining implementation obligations

The 18.5-tile CPU-memory reuse is estimated from the historical census.
The eleven additional wrapper tiles require actual removal and replacement debits.
F5 link spans exclude AECP and do not establish target memory mapping.
The 56-tile packing example illustrates why primitive measurement remains required.
Partial placement cannot use full-split reclamation credits.
M0s, M8a, the default flip and M9 must replace these assumptions with measured allocations.
Any RAM trade must reprice its LUT effect before acceptance.
The reserve, resource tolerances and NFR-RES-01 remain unchanged.
Independent review, publication, hosted acceptance and hardware qualification remain outstanding.
