[A785]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**Blocked (STOP on #919): the 8x8/1if split image misses the timing floor on all three directives**, an owner decision. Everything else that ran is green: the workflow jobs, the boot simulation, the ledger, the release image and 1x1/1if timing. The native suite sweep has not run. Head `55769f09` — `919-phy-link` -> `dev-soft-core`

## Linked Issue / roles

Closes #919
Relates to #665

Executor: `[A785]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

The split's control firmware now polls the PHY after boot, as the release firmware does, and publishes the resolved link, speed and duplex to `milan_mac_link_status` (REQ-MAC-03). Before this the split published nothing, so the word kept its reset value, link up, and no consumer of the datapath's effective link saw a link change (#665 rehearsal finding A).

| Piece | What |
|---|---|
| `sw/firmware/ctrl/plat/ctrl_plat_phy.{h,c}` (new) | The release's `phy_link_tick`, resumable one Clause-22 frame a call: no PHY found, one address probed a frame (a miss published link down, the next address at once, no blocking scan); found, BMSR, a loss it latched while the link was published up published first, then a second BMSR for the current state; BMCR (forced mode), then the 1000BASE-T pair where the extended status offers it, then 4/5. The release's registers, order and words. |
| THE STEP (`ctrl_loop.h`) | `ctrl_plat_phy_store_step` is the platform's THE STEP client: the store's owed step first, unchanged, and a PHY frame only in a call whose store took no step of a save, with `CTRL_PLAT_PHY_STEP_US` of the pass's share left. No frame stands beside an input, no pass carries a save step and a frame, and the store's own worst cases stand. While a frame is due the client owes a step, so under input that never leaves a pass empty frames ride THE STEP's age limit. |
| The pace | A poll every `CTRL_PLAT_PHY_POLL_US` = `MILAN_NVM_HEARTBEAT_MS * 1000 / 2`, 125 ms: the release's `PHY_POLL_NS` by its own derivation. |
| The half period | At least 200 ns (IEEE 802.3 22.2.2.13 and 22.3.4): `ceil(CONFIG_CLOCK_FREQUENCY / 5 MHz)` spin turns, or one turn where a 1,024-turn run timed at arm shows one turn alone holds 200 ns (on the split CPU a turn is about 27 cycles). |
| Cost | Measured on the platform image on the split CPU (split boot simulation): a frame 14,537 CPU cycles at 1x1/1if, 145.37 us; stated `CTRL_PLAT_PHY_STEP_US` = 155 us (measurement + 5 %, rounded up to 5 us). |
| Paths | Armed past the CSR identity check (a foreign window's MDIO pins untouched); the ready loop through THE STEP; a refused stage on each console turn (the release's #70). A SoC with no MDIO rows arms nothing. |
| Bus map | `ctrl_plat_gen.py map` emits `milan_mac_phy_mdio_w`/`_r` and `milan_mac_link_status`, all three or none (none = 0), partial refused. |
| Memory ledger | The platform's 8x8/2if entry 60.0 -> 60.5 (the owner's cap; S14 debt 4.5 RAMB36), `struct ctrl_plat` sizes re-measured. |

**Where the link edge goes on the split** (unchanged RTL, both placements): `milan_mac_link_status.link_up` -> `MultiReg` -> `i_link_up` -> `eff_link_w` (`milan_datapath.sv:3351`; `LINK_CTRL[0]` resets 1) ->
- AVB_INTERFACE LINK_UP / LINK_DOWN (`ctr_linkup_r`/`ctr_linkdn_r`, `:4033-4059`), read by the split's GET_COUNTERS through the face's CTR window;
- their GET_COUNTERS notification: the AVB_INTERFACE counter change (`ctr_avb_dirty_w`) -> mailbox COUNTERS_CHANGED -> `ctrl_app_aecp.c` -> AECP's unsolicited GET_COUNTERS;
- the gPTP plane's `port_enabled_i` (`:9129`), whose toggle ends the Pdelay_Req cease (Milan v1.2 4.2.6.2.5) and re-evaluates asCapable;
- the mailbox's LINK level and event (`o_ctl_link_up`, `:10081`) -> ADP, MAAP and SRP.

**Images.** The release image is byte-identical. At base and head, both shapes, `bios.bin` and its disassembly are equal, and so is the ELF with debug sections stripped. The release build reads no file this PR changes. The split platform images change at every point:

| Point | Platform `rom` / `sram` need, B (base) | Platform RAMB36 (base) | `ctrl_plat`, B (base) |
|---|---|---|---|
| 1x1, one interface (shipping) | 117,516 (116,072) / 56,224 (56,224) | 43.0 (42.5) | 17,536 (17,536) |
| 1x1, two interfaces | 118,828 (117,384) / 58,400 (58,336) | 44.0 (43.5) | 19,072 (19,008) |
| 8x8, one interface | 131,068 (129,624) / 97,328 (97,264) | 56.0 (56.0); 4 B of `rom` before 56.5 | 18,176 (18,176) |
| 8x8, two interfaces | 132,372 (130,920) / 114,288 (114,160) | 60.5 (60.0): the entry is raised to the owner's cap; the 4.5 RAMB36 is S14 debt | 20,352 (20,288) |

**Area.** The RTL is unchanged. The base's and the head's split exports differ, apart from paths and dates, only in the ROM:
- 1x1/1if: `rom_bank3` goes from 512 to 1,024 words, one RAMB18 to one RAMB36 (+0.5 tile), and its decode compare changes with it.
- 8x8/1if: only the ROM's contents differ.

Placed at the head, 1x1/1if (ExtraPostPlacementOpt / ExtraTimingOpt / AltSpreadLogic_high):

| | ExtraPostPlacementOpt | ExtraTimingOpt | AltSpreadLogic_high |
|---|---:|---:|---:|
| LUT | 31,344 | 31,382 | 31,340 |
| FF | 42,120 | 42,119 | 42,119 |
| BRAM | 81 tiles (63 RAMB36 / 36 RAMB18) | same | same |
| DSP | 9 | 9 | 9 |

8x8/1if: LUT 42,607 / 42,604 / 42,596, FF 50,722 / 50,724 / 50,723, BRAM 92.5 tiles (76 / 33), DSP 9.

**Timing** (S9's recipe; the floor is WNS and WHS >= +0.030 ns at every corner):
- 1x1/1if meets on all three directives. The best is ExtraPostPlacementOpt at +0.390 / +0.058; ExtraTimingOpt gives +0.177 / +0.036 and AltSpreadLogic_high +0.113 / +0.036.
- 8x8/1if misses on all three. ExtraPostPlacementOpt is +0.011 / +0.034 (setup). ExtraTimingOpt is +0.171 / +0.014 and AltSpreadLogic_high +0.215 / +0.014 (hold).
- The 8x8/1if paths are in unchanged logic, on a netlist identical to the base's except for the ROM's contents. The setup path is the `KL_mbx_cdc/u_edit/rq_r` -> `milan_datapath/amap_edit_oclaim_*` clock-enable cone. The hold path is one register pair in `milan_datapath` (`g_aaf_meter.aaf_clock_meter/s2_ts_r[6]` -> `grp_ts0_r[6]`).
- This is the open decision on #919.

## Authoritative references

- #919; #665 rehearsal report (finding A / 12).
- `sw/firmware/milan_baremetal/milan_baremetal.c` `phy_link_tick` and `sw/firmware/nvm_hosttest/test_phy_firmware.py` (the release's behaviour and its host tests).
- IEEE 802.3 22.2.2.13 (MDC timing), 22.2.4 (BMCR, BMSR, PHYID, ANAR/ANLPAR), 22.2.4.2.13 (BMSR latched-low link status), 22.3.4 (MDIO output delay), 40.5.1.1 (1000BASE-T control/status).
- Milan v1.2 4.2.6.2.5 (the Pdelay_Req cease ended by a link toggle); IEEE 1722.1-2021 7.4.42 and Table 7-158 (GET_COUNTERS, LINK_UP/LINK_DOWN).
- REQUIREMENTS.md REQ-MAC-03; `docs/reference/REGISTER_MAP.md` MAC_STATUS.
- `sw/firmware/ctrl/loop/ctrl_loop.h` (THE SHARE, THE STEP), `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3 and 5.

## How to get into the same state

```sh
git fetch origin && git checkout 919-phy-link
git submodule update --init third_party/tsn-c-stack third_party/lwSRP protocol-processor gptp-processor third_party/verilog-axis
```

## How to validate

```sh
python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py                      # every arm; platboot1/2, platmap among them
python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --self-test --shard 1/4   # the control campaign (and 0, 2, 3)
python3 sw/firmware/gtest/fw_coverage.py --check
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/b1                # PHY grade at 1x1/1if
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/b8 --shape endstation_ax7101_8x8
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/bs --self-test
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir /tmp/pl
python3 sw/litex/test_ctrl_memory.py
```

Expected result: every command exits 0; the boot simulation's PHY lines show the probe, a poll every 125 ms, `[0, 13]` after the latched loss, `[0, 0]` after the loss, `[13]` after the return, every frame within 155 us and MDC within IEEE 802.3 22.2.2.13.

Evidence at `55769f09`, each on a fresh clean clone:

| Gate | Result |
|---|---|
| Workflow jobs `rtl-fast`, `elaborate`, `docs`, step by step | rc 0: 118 steps rc 0, 130 hosted-only steps not run with a stated reason, 0 bad |
| Control mutant campaign (`firmware-control-mutants`) | 742 of 742 caught, the platform's 67 among them (the PHY's 26) |
| Firmware coverage ratchet | `ctrl_plat_phy.c` 122/122 lines, 107/107 branches; `ctrl_plat.c` 136/136, 42/42 |
| Split boot simulation, 1x1/1if and 8x8/1if | rc 0. PHY: 34 frames, the longest 14,537 CPU cycles (145.37 us) against 155 us; polls 125.055 to 125.493 ms apart; the latched loss published `[0, 13]`, the loss `[0, 0]`, the return `[13]` 126.2 ms after it; MDC at least 930 ns high, 1,120 ns low |
| Split boot simulation self-test | rc 0. The PHY's plants `phy-unpublished` and `phy-loss-not-latched` are each a PHY finding |
| Platform ledger, every point | rc 0, the table above |
| Release image | byte-identical, both shapes |
| S9 route, 1x1/1if | meets on all three directives (best +0.390 / +0.058) |
| S9 route, 8x8/1if | **misses** on all three (see Timing); STOP on #919 |
| CPU service budget harness, 1x1/1if and 8x8/1if | Run at `ec5bd171`. Its image is byte-identical to the base's at both points (the fixture composes no platform), and its testbench and RTL are unchanged, so its verdict is the base's. 1x1/1if: 96 groups, 0 work passes over the 2 ms share, and 7 `backlog-owed` probe instances over their ceiling, which the base's harness README already tables. 8x8/1if: stopped ungraded after the STOP (68 of 96 groups; its image is the base's) |
| Native suite sweep (`verilator-suites`) | not run (STOP) |

## Known limitations / out of scope

- **Open decision (STOP on #919):** the 8x8/1if split image misses WNS/WHS >= +0.030 ns on each of S9's three directives. The netlist is identical to the base's but for the ROM's contents, and the paths are in unchanged logic (see Timing). Whether that is accepted, or what further run is wanted, is the owner's call.
- The 8x8/1if platform image has 4 B of `rom` before 56.5 RAMB36, which the product SoC build refuses (it names no ledgered point): further growth there needs S14's ROM work or a ruling.
- Under input that never leaves a pass empty and with a save in flight, the PHY's frames wait for the save (the store's steps come first); without a save, one frame per aged step.
- The datapath's consumers are unchanged RTL tested by their own suites; the host tests model them as the RTL builds them. The bench acceptance of #919 (the tap link-flap feature and gPTP resume within 5 s) belongs to the gating run.
- The CPU budget harness's fixture composes no platform, so it does not run the poll; the frame's cost is measured in the split boot simulation on the platform image and placed in THE STEP's class by its stated cost.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
