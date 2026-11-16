# #919 round 1 — [A785] handoff (kept current)

Lane: 919-phy-link, base origin/dev-soft-core 659d7687. Issue #919 (part of #665), rehearsal finding 12 / A.
TAKEN: #919 issuecomment-6899687849. Head 55769f09 (commits 437b2bd4, 927d8044, ec5bd171, c4cacb0c,
63fcf730, bdd44f96, 1bdbd2a8, 895681e5, 55769f09 on 659d7687). Nothing pushed; the manager pushes and opens the PR
(PR-BODY.md). Since bdd44f96: 1bdbd2a8 the boot grader's return bounded by the release's 250 ms publication bound
(run.py, README); 895681e5 comments only (ctrl_plat_phy.{h,c} THE BIT); 55769f09 plat/README's defect counts
(67, the PHY's 26).

## Status

- [x] base verified (659d7687), submodules initialised
- [x] TAKEN posted
- [x] step 1 report (below)
- [x] step 2 implementation
- [x] step 3 tests (26/26 platboot at 1 and 2 interfaces, 10 plat, 5 platmap; 26 PHY/map defects planted, all caught)
- [ ] step 4 gates (table below): 1x1/1if routes meet on all three directives; **8x8/1if misses the timing floor
  on all three** (EPPO setup +0.011, ETO and ASL hold +0.014, every corner otherwise clean, 0 failing endpoints)
- [x] STOP posted on #919 (issuecomment-6905511089, text comments/STOP.md), the brief's "a timing miss after the
  three directives"; the sweep not started after it (no new long gate after a stop); of the gates already
  running, the two mutant jobs and the 1x1 harness finished; the 8x8/1if harness was stopped ungraded (see its row).
  No REVIEW READY in this round.

**STOP, 2026-11-16 03:07.** The 8x8/1if split image misses WNS/WHS >= +0.030 ns on each of S9's three directives.
The 8x8/1if export is identical to the base's but for the ROM's contents (route/base-vs-head-8x8-netlist.txt), and
the paths are not this lane's: EPPO's setup is the `KL_mbx_cdc/u_edit/rq_r` -> `milan_datapath/amap_edit_oclaim_*`
clock-enable cone (40 levels; #810's EPPO at 8x8 was +0.001 on the same family), ETO's and ASL's hold is one
register-to-register path inside `milan_datapath` (`g_aaf_meter.aaf_clock_meter/s2_ts_r_reg[6]` ->
`grp_ts0_r_reg[6]`, 0 levels, 0.268 ns clock skew). Not resolved here: seeds, a fourth directive, or a constraint
are the owner's (or S14's) call, not this lane's.

## Step 1 report (written before any change, at 659d7687)

**The release's poll** (`milan_baremetal.c:939-1115`): `phy_link_tick` every `PHY_POLL_NS = NVM_HEARTBEAT_NS / 2`
(125 ms: `MILAN_NVM_HEARTBEAT_MS` 250 from `scripts/nvm_shape.py` WRITER_TIMING_MS), ridden on the BIOS dispatch
and idle hooks (`nvm_heartbeat_tick`), armed only past the CSR identity check (`phy_live`, #70). A poll is up to
9 Clause-22 reads, all in one call: unfound, reg 2 at one address per opportunity (no scan; a miss advances the
address, publishes 0 and re-arms at once); found, BMSR; a latched loss with link published up publishes 0 first;
a second BMSR when not published up; then `phy_resolved_status` (BMCR; forced mode; AN done; ext status 15,
1000T 9/10; 4/5) and the publication. Each bit `phy_mdio_bit`: 3 CSR writes, 1 read, 2 x `cdelay(32)`.
Release cost measured on its harness (docs/findings/397_SERVICE_BUDGET.md "PHY poll derivation"): one
transaction 0.12455 ms, a complete poll 0.650 ms (1x1).

**MDIO access cost on the split CPU (estimated before, then measured in the split boot simulation):** a frame
is 65 bit periods (32 preamble + 14 command + 2 turnaround + 16 data, then the release write). Measured: with the
release's bit sequence and a 20-turn volatile spin a half (one cycle a turn assumed), 98,791 CPU cycles a frame
(988 us: a turn is ~27 cycles, the console-blocks plant's 0.27 us a turn); each CSR access ~110 cycles. Final:
two writes and one read a bit (the falling edge folded into the next bit's write) and a timed one-turn half
period: 14,537 cycles (145.37 us) at 1x1/1if, 14,512 at 8x8/1if. A steady 1000FD poll is 5 frames, a
link-change poll 6, a probe miss 1: a whole poll does not fit beside THE SHARE's heaviest passes, and any frame
beside an input lengthens it.

**Where a poll fits:** not as a loop poll (every pass, so beside every record: the rows charge every ordinary
pass at the polls' base, `rows_grade.demand` 'passes'). THE STEP's class does: its work runs only in a pass
that took no input (`ctrl_loop.c` work == 0), admitted against the pass's deadline, and the rows charge THE
STEP as `floor(W / (10 (CTRL_LOOP_STEP_AGE + 1))) + 1` steps at `CTRL_LOOP_STEP_PASS_US`, a count fixed by the age
limit and not by how often a client owes. THE STEP has one client; the platform binds a composite one.

**Every consumer the release's link edge reached, and its split path** (all through the datapath's
`eff_link_w = i_link_up & cfg_sw_link & (cfg_linkg_dis | linkg_est_w)`, `milan_datapath.sv:3351`; `i_link_up` is
`milan_mac_link_status.link_up` through `MultiReg`, `milan_soc.py:1985-2014`; `LINK_CTRL[0]` resets 1 and no
firmware writes it): unchanged RTL in both placements.
- AVB_INTERFACE LINK_UP / LINK_DOWN: `ctr_linkup_r` / `ctr_linkdn_r` on each edge of `eff_link_w`
  (`milan_datapath.sv:4033-4059`); the split's GET_COUNTERS reads them through the face's CTR window
  (`aecp_face.c:225`).
- The link-edge GET_COUNTERS notifications: the same edge sets the AVB_INTERFACE pending bit (`ctr_avb_dirty_w`)
  -> `pp_ctr_evt_*` -> `o_ctl_ctr_chg_*` (`:10073`) -> mailbox COUNTERS_CHANGED -> `ctrl_app_aecp.c` face_event ->
  `ctrl_app_aecp_changed(..., 8u)` -> AECP's unsolicited GET_COUNTERS (MBX_CTRCHG_HOLDOFF_MS 1 s).
- gPTP link-up (Pdelay_Req cease ended, Milan v1.2 4.2.6.2.5; asCapable re-evaluated): the fabric gPTP plane's
  `port_enabled_i (eff_link_w)` (`:9129`), the release's RTL (gptp-processor `KL_gptp_engine.sv:113`).
- ADP / MAAP / SRP: `o_ctl_link_up = eff_link_w` (`:10081`) -> mailbox LINK level and event -> `adp_link_change`,
  `maap_mbx`, `srp_mbx`.
- MAC speed: `link_status.speed` -> `o_mac_is_1g` (REQ-MAC-03), the lwSRP 750 Mb/s admission gate.

## Design (as built)

- `sw/firmware/ctrl/plat/ctrl_plat_phy.{h,c}`: the release's poll, resumable, one Clause-22 frame a call
  (802.3 22.2.2.13: MDC has no maximum high/low time). Same registers, same order, both of each pair read
  before either is judged, same words (13, 5, 11, 3, 9, 1, forced modes, 0).
- Placement, THE STEP: `ctrl_plat_phy_store_step` (ctrl_plat_phy.c:221) is the platform's THE STEP client: the
  store's owed step first, unchanged; the PHY's frame only where the store took no step of a save (phase
  CAPTURE..VERIFY before the call and steps moved), with `CTRL_PLAT_PHY_STEP_US` (155) of room. No pass carries a
  save step and a frame. Owed while a frame is due, so under input that never leaves a pass empty its frames ride
  the age limit, one per aged step whose store step is idle (the store's tick owes a step every cs, so the idle
  store step precedes it).
- Pace: `CTRL_PLAT_PHY_POLL_US = MILAN_NVM_HEARTBEAT_MS * 1000 / 2` = 125 ms, the release's PHY_POLL_NS derivation.
- Half period >= 200 ns (22.2.2.13 160/160/400; 22.3.4 300 ns output delay before the sample):
  `ceil(CONFIG_CLOCK_FREQUENCY / 5 MHz)` turns (one cycle a turn), or one turn where a 1024-turn run timed at arm
  on the flash port's us clock exceeds 205 us (a turn >= 205/1024 us). Boot sim: MDC high >= 930 ns, low >=
  1120 ns, period >= 2260 ns.
- Stated cost `CTRL_PLAT_PHY_STEP_US` 155 = 145.37 us + 5 %, rounded up to 5 us; under a fifth of a store
  read-back step (0.77 ms), so a step call with a frame is lighter than one with a save's flash step, which the
  CPU budget harness measures in every class THE STEP enters. Harness fixture NOT changed (it composes no
  platform; adding the PHY would also move the fixture's ROM ledgers).
- Paths: armed past the CSR identity check (ctrl_plat.c:254); the ready loop through THE STEP (:280); a refused
  stage polls on each console turn (:304), as the release on every path past its identity check (#70).
- Map: `ctrl_plat_gen.py map` emits the three PHY rows (all or none; none -> 0, the poll arms nothing; partial
  refused). `CONFIG_CLOCK_FREQUENCY` from generated/soc.h (the split CPU is on sys).

## Changes (file:line — reason)

- `sw/firmware/ctrl/plat/ctrl_plat_phy.h` (new): THE POLL / THE PACE / THE STEP / THE BIT; bus struct; register
  and field constants; `CTRL_PLAT_PHY_POLL_US` :135; `CTRL_PLAT_PHY_STEP_US` :143 with its measurement.
- `sw/firmware/ctrl/plat/ctrl_plat_phy.c` (new): `arm` :28 (calibration :43), `bit` :49, `frame` :64 (shift
  register of the 64 bits), `take` :107 (the release's decisions per stage), `due` :190, `step` :195,
  `store_step` :221.
- `sw/firmware/ctrl/plat/ctrl_plat.c:254` arm past identity; `:280` composite bound as THE STEP; `:304` refused
  stage polls. `ctrl_plat.h:38` THE PHY, `:99` env bus, `:132` state. `ctrl_plat_main.c` env from the map.
- `sw/firmware/ctrl/plat/ctrl_plat_gen.py:57,148-153` PHY rows. `sw/firmware/ctrl/test/ctrl_plat_csr.csv` rows.
- `sw/firmware/ctrl/loop/ctrl_loop.h` THE STEP comment names the PHY frames (comment only).
- `sw/firmware/ctrl/test/ctrl_plat_image.py` links and requires the PHY; `plat_arms.py` PHY in platboot/platrv32,
  new `platmap` arm :201; `ctrl_mutants.py` arms dict `platmap`; `tb/verilator/milan_dp/twin_fw.py` PHY source
  (the twin's env has no MDIO: unarmed, behaviour unchanged).
- Tests: `phy_peer.hpp` (pin-level peer), `plat_bus.hpp` (peer hook), `test_plat_phy.cpp` P1-P10,
  `test_plat_boot.cpp` B11, B12, L1-L4 with a datapath-link model (edge counting, LINK event, COUNTERS_CHANGED,
  CTR window answers, port-enable trace).
- Boot sim: `boot_soc.py:78` PhyBoundary (milan_mac_phy_mdio_w/_r, link_status, MultiReg), `sim_main.cpp:60` Phy
  peer at address 1 and `phy_script` :259, `run.py:355-...` phy_constants / grade_phy / phy_rows, 2 plants.
- Ledger: `sw/litex/ctrl_memory.py` platform-8x8-two-interfaces 60.0 -> 60.5 (its cap), ctrl_plat 20,288 ->
  20,352, S14 debt 4.5; `ctrl_memory_ledger.py` PLAT_1X1_2 19,072, PLAT_8X8_2 20,352, cases at 60.5/61.0;
  `test_ctrl_memory.py` words.
- Coverage ratchet: ctrl_plat.c 136/136 42/42; ctrl_plat_phy.c 122/122 107/107 (only these two rows changed).
- Docs: plat/README.md (The PHY), ctrl_split_boot/README.md, SPLIT_CONTROL_MEMORY.md (section 3 ledger, section
  5 "With the PHY poll"), REGISTER_MAP.md.
- sw/firmware/ctrl/plat/README.md:139-140 (55769f09): the campaign's count 63 -> 67 and "the PHY's 22" -> 26 (the
  poll's 22, the link counters' notification, the bus map's 3), as `plat_mutants.mutants()` plants them (8 CSR,
  16 console, 17 boot, 26 PHY). The base's README said 40 against the base's 41, so that count was one short
  before this lane too.

## New checks (planted mutant — failing words)

Control campaign, `plat_mutants.py` (26 new, 1 re-anchored; arm platboot1 unless noted):

| Mutant | Named test — words |
|---|---|
| plat-phy-never-armed (no poll) | Phy.L1 — "L1 the ready loop publishes the PHY's link" |
| plat-phy-loss-not-latched | PlatPhy.P3 — "P3 a loss that recovered between two polls publishes link down, then link up"; Phy.L2 |
| plat-phy-edge-not-counted (whole poll in one call) | Phy.L2 — "L2 a loss that recovered between two polls moves LINK_DOWN and LINK_UP by one each"; P7 |
| plat-phy-cease-not-ended (second BMSR read dropped) | Phy.L4 — "L4 the first poll after the link's return publishes it up"; P3 |
| plat-link-counter-change-dropped (ctrl_app_aecp.c) | Phy.L3 — "L3 each link edge sends one unsolicited GET_COUNTERS" |
| plat-map-phy-rows-ignored (platmap) | PlatMap.M1 — "M1 the PHY's three rows give their addresses" |
| plat-map-partial-accepted (platmap) | PlatMap.M3 — "M3 some but not all of the PHY's rows are refused" |
| plat-map-absent-refused (platmap) | PlatMap.M2 — "M2 a SoC with no MDIO gives 0 for each" |
| plat-phy-unguarded | Phy.B11 — "B11 a foreign window's MDIO pins are never touched" |
| plat-phy-refused-stage-unpolled | Phy.B11 — "B11 a stage refused past the identity check keeps publishing the link" |
| plat-phy-beside-a-save-step | Phy.B12 — "B12 a call whose store takes a step of its save carries no PHY frame" |
| plat-phy-store-owed-dropped | Phy.B12 — "B12 the client owes a step while the store owes one" |
| plat-phy-after-an-idle-step-refused | Phy.B12 — "B12 a call whose store step is an idle one carries one PHY frame" |
| plat-phy-probe-scans | PlatPhy.P1 — "P1 one address an opportunity, no scan in one call" |
| plat-phy-late-sample | PlatPhy.P1 — "P1 the PHY found at its address publishes its link" |
| plat-phy-unpaced | PlatPhy.P2 — "P2 no poll before CTRL_PLAT_PHY_POLL_US"; Phy.L1 "L1 a poll a period" |
| plat-phy-wrap-unsafe | PlatPhy.P10 — "P10 a clock that went back makes a poll due at once" |
| plat-phy-common-mode-misread | PlatPhy.P4 — "P4 the highest common mode of 4 and 5" |
| plat-phy-fault-ignored | PlatPhy.P4 — "P4 a master-slave configuration fault is link down" |
| plat-phy-ack-ignored | PlatPhy.P5 — "P5 a NAKed register is link down" |
| plat-phy-turnaround-driven | PlatPhy.P6 — "P6 every frame a Clause-22 read, driven then released" |
| plat-phy-no-deadline | PlatPhy.P7 — "P7 a frame is taken only with CTRL_PLAT_PHY_STEP_US left" |
| plat-phy-not-owed | PlatPhy.P8 — "P8 a probe that missed owes the next" |
| plat-phy-half-period-short | PlatPhy.P9 — "P9 the half period at 100 MHz: 200 ns, 20 turns" |
| plat-phy-timed-run-ignored | PlatPhy.P9 — "P9 a run of 277 us: one turn holds 200 ns" |
| plat-phy-timed-resolution-ignored | PlatPhy.P9 — "P9 a run of 205 us bounds a turn under 200 ns" |
| plat-store-step-unbound (re-anchored on the composite binding) | Boot.B10 — unchanged words |

Local runs: 18/23 first (4 refused by -Werror, an unused name each; 1 caught by an earlier P3 check), fixed;
then 5/5, 3/3 (map), 2/2 (store-owed, ack): all 26 + 1 caught. The full campaign runs in the firmware-control-mutants
job (gate table).

Boot simulation plants (`run.py` PLANTS, `--self-test`): phy-unpublished (the final publication removed) and
phy-loss-not-latched, each must be a PHY finding in a completed run.

## Gate table

| Gate | Command | Head | rc | Receipt |
|---|---|---|---|---|
| Workflow jobs rtl-fast, elaborate, docs (every job; firmware units, coverage ratchet, firmware-verilator, the AECP, SRP and control mutant campaigns, elaborate gates, docs gates) | run_wf.py per job, fresh clone each (elaborate jobs and firmware-boundary with the host's LiteX venv, WF_VENV; see workflows/README.md for the two discarded gates-1 attempts) | 55769f09 | 0 (verify_wf.py: 118 steps rc 0, 130 not run with a reason, 0 bad) | workflows/verify-55769f09.md, workflows/logs/ |
| Control mutant campaign | firmware-control-mutants ci_step_9 | 55769f09 | 0 | 742 of 742 caught (the platform's 67 among them), workflows/logs/rtl-fast__firmware-control-mutants__ci_step_9.log |
| S9 route 1x1/1if ExtraPostPlacementOpt (integrated) | rt/tools/route_one.sh via vivado-slot.sh | 895681e5 (inputs = 55769f09) | 0 | route/1x1-ExtraPostPlacementOpt/ (WNS +0.390, WHS +0.058 worst corners) |
| S9 route 1x1/1if ExtraTimingOpt | rt/tools/route_directive.sh via vivado-slot.sh | 895681e5 (inputs = 55769f09) | 0 | route/1x1-ExtraTimingOpt/ (WNS +0.177, WHS +0.036) |
| Split boot simulation self-test (controls and plants, phy-unpublished and phy-loss-not-latched caught) | run.py --self-test | 55769f09 | 0 | boot/self-test-1x1-55769f09.txt |
| S9 route 1x1/1if AltSpreadLogic_high | rt/tools/route_directive.sh via vivado-slot.sh | 895681e5 (inputs = 55769f09) | 0 | route/1x1-AltSpreadLogic_high/ (WNS +0.113, WHS +0.036) |
| S9 route 8x8/1if ExtraPostPlacementOpt (integrated) | rt/tools/route_one8.sh via vivado-slot.sh | 895681e5 (inputs = 55769f09) | 0; signoff.py 1 | route/8x8-ExtraPostPlacementOpt/ (WNS **+0.011**, WHS +0.034: setup under the floor) |
| S9 route 8x8/1if ExtraTimingOpt | rt/tools/route_directive8.sh | 895681e5 (inputs = 55769f09) | 0; signoff.py 1 | route/8x8-ExtraTimingOpt/ (WNS +0.171, WHS **+0.014**: hold under the floor) |
| S9 route 8x8/1if AltSpreadLogic_high | rt/tools/route_directive8.sh | 895681e5 (inputs = 55769f09) | 0; signoff.py 1 | route/8x8-AltSpreadLogic_high/ (WNS +0.215, WHS **+0.014**: hold under the floor) |
| 8x8/1if timing verdict | best of three against WNS and WHS >= +0.030 at every corner | 895681e5 | **MISS: STOP** | route/8x8-timing-miss.txt |
| Base vs head split image export, 1x1/1if and 8x8/1if (area delta) | route_image.sh / route_image8.sh on a base clone, diff of the netlists | 659d7687 vs 895681e5 | diff as stated | route/base-vs-head-{1x1,8x8}-netlist.txt |
| CPU service budget harness 1x1/1if | ctrl_service_budget/run.py --point 1x1 --record-budget-findings --record-share-findings | ec5bd171 (image = base's and head's, budget/image-identity-base-ec5bd171-head.txt) | 0 | budget/1x1/: 96 groups graded, 0 refusals, 0 of 140,032 work passes over the 2.000 ms share; **7 probe instances (4 of 92 paths) MISS ceiling, all in `backlog-owed`** (the owed-frame response and the ACMP commands behind it, 61.6 to 63.4 ms against 20 ms) — the base's own (see below) |
| CPU service budget harness 8x8/1if | --point 8x8-1if | ec5bd171 (image = base's, `607d2104...`) | **stopped, ungraded** at 68 of 96 groups | budget/8x8-1if/run-stopped.log. Stopped by me after the STOP: it can only reproduce the base's verdict, and the host ran at load 230 on 128 CPUs (its simulations at ~35 % of a CPU), so it would have taken 10 h or more. A next round that needs it reruns it, or cites a base run at 659d7687 (same image, same testbench) |
| Split boot simulation 1x1/1if | tb/verilator/ctrl_split_boot/run.py | 55769f09 | 0 | boot/boot-1x1-55769f09.txt (figures = bdd44f96's) |
| Split boot simulation 8x8/1if | run.py --shape endstation_ax7101_8x8 | 55769f09 | 0 | boot/boot-8x8-55769f09.txt |
| Platform ledger, every point | plat_ledger.py | 55769f09 | 0 | boot/plat-ledger-55769f09.txt |
| Release image byte-identical, 1x1 and 8x8 | scripts/release_image.sh at base and head, compare | 659d7687 vs 63fcf730; nothing the release build reads changed after it | identical | release-image/COMPARE.txt, release-image/LATER-COMMITS.txt |
| Native suite sweep (verilator-suites shards) | native-shards.py, 4 shards | — | **not run** (STOP: no new long gate after a stop) | — |

## ROM and area

| Point | Platform rom / sram, B (base) | RAMB36 (base) | ctrl_plat (base) |
|---|---|---|---|
| 1x1/1if | 117,516 (116,072) / 56,224 (56,224) | 43.0 (42.5) | 17,536 (17,536) |
| 1x1/2if | 118,828 (117,384) / 58,400 (58,336) | 44.0 (43.5) | 19,072 (19,008) |
| 8x8/1if | 131,068 (129,624) / 97,328 (97,264) | 56.0 (56.0), 4 B of rom spare | 18,176 |
| 8x8/2if | 132,372 (130,920) / 114,288 (114,160) | 60.5 (60.0), ledger raised (S14 debt 4.5) | 20,352 (20,288) |

Area. The RTL is unchanged; the split image's gateware changes only by the image's ROM. The base's (659d7687)
and the head's exports (S9 recipe, no Vivado) differ, apart from paths, dates and LiteX's comment tree:
- 1x1/1if: `rom_bank3` 512 -> 1,024 words x 32 (one RAMB18 -> one RAMB36, +0.5 tile, the ledger's 42.5 -> 43.0)
  and its decode compare (`bus_adr[15:9] == 56` -> `[15:10] == 28`, the hole from 0x7200 -> 0x7400 words);
- 8x8/1if: nothing but the ROM's contents (one 32,768-word bank at both).
Placed at the head, 1x1/1if (EPPO / ETO / ASL): LUT 31,344 / 31,382 / 31,340, LUTRAM 1,120 / 1,119 / 1,119,
FF 42,120 / 42,119 / 42,119, Slice 13,423 / 14,037 / 14,014, BRAM 81 tiles (63 RAMB36 / 36 RAMB18), DSP 9,
CARRY4 2,399. Against #810's route (084cf7a8, the nearest routed tree): LUT +89 / +167 / +130, FF +30 / +29 / +28,
BRAM 78.5 -> 81; #810's export had three ROM banks and a different sram banking (the base's own image growth,
#894/#904, between 084cf7a8 and 659d7687), so that route is a reference, not the base.

## The CPU budget harness and this change

The harness's fixture composes no platform, so the PHY poll is not in its image. Its firmware image at ec5bd171 is
byte-identical to the base's at both points (1x1 `e6a821cb...`, 8x8/1if `607d2104...`, each relinked from the base's
own `ctrl_srp_image.py` with the harness build's flash map and archives), and its testbench and RTL are the base's
(`git diff 659d7687 55769f09 -- tb/verilator/ctrl_service_budget tb/verilator/fw_service_budget hdl` empty). So
its verdict is the base's. The 1x1 run's seven `backlog-owed` ceiling misses are the base's; the base's harness
README already tables the owed-frame row and the ACMP commands behind it over the ceiling ("a response with 7
frames owed ahead of it ... over ceiling"). The poll's own cost is placed by its stated cost in THE STEP's class
(`CTRL_PLAT_PHY_STEP_US` 155 us = 145.37 us measured on the platform image + 5 %, rounded up to 5 us), measured in
the split boot simulation, where every frame is within it. Not a STOP of its own (the poll's pacing is not in that
image, and the round is already stopped); for the owner with the timing decision: "every row within its bound" is
not met by the base's own harness at 1x1.

## Scratch left for the timing decision

About 1.0 GB is left in scratch, and none of my units are running. `rt/route/` and `rt/route8/` hold each directive's
routed checkpoint and signoff reports, and the 1x1 and 8x8/1if synthesis checkpoints
(`*/gateware/alinx_ax7101_synth.dcp`). `rt/repo` is the clone they read the RTL from (895681e5). `rt/route-base/` and
`rt/route8-base/` hold the base's exports. Their sha256 values are in receipts/route/*/artifacts.txt. A seed or
directive run from the synthesis checkpoint needs no re-export. The harness build directories, the boot runs and
the other clones are removed; each is reproducible from the commands in receipts/scripts.

## Open risks / questions

- 8x8/1if has 4 B of ROM before 56.5, which the product SoC build refuses (it names no ledgered point): any
  later growth of the platform image at that point needs S14's ROM work or a ruling.
- Under input that never leaves a pass empty WITH a save in flight, the PHY's frames wait for the save
  (the store's steps come first); without a save, one frame per aged step (30 ms), a 1000FD poll 150 ms.
- The datapath consumers are modelled in the host test (edge counter, LINK event, counter change, port
  enable); the RTL itself is unchanged and is tested by its own suites (gptp-processor engine tests,
  milan_dp counters). The bench acceptance (#919: tap link flap, gPTP resume within 5 s) is the gating run's.
