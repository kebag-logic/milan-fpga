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

Ready for review: every gate rounds 3 and 4 touch was run at the head. Under #818's floor both split images pass on their best directive, and the ROM banking is unchanged since the routed head. The harness's known lines are the base's — head `1a1e6665` — `919-phy-link` -> `dev-soft-core`

## Linked Issue / roles

Closes #919
Relates to #665

Executor: `[A785]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

The split's control firmware now polls the PHY after boot, as the release firmware does. It publishes the resolved link, speed and duplex to `milan_mac_link_status` (REQ-MAC-03). It also carries #840's 1000BASE-T-only advertisement on that path, as the #919 scope addition asks. Before this the split published nothing, so the word kept its reset value, link up, and no consumer of the datapath's effective link saw a link change (#665 rehearsal finding A).

| Piece | What |
|---|---|
| `sw/firmware/ctrl/plat/ctrl_plat_phy.{h,c}` (new) | The release's `phy_link_tick`, resumable one Clause-22 frame a call. With no PHY found, one address is probed a frame; a miss publishes link down and the next address follows at once, with no blocking scan. With the PHY found: BMSR; a loss it latched while the link was published up is published first; then a second BMSR for the current state; then BMCR (forced mode), the 1000BASE-T pair where the extended status offers it, then registers 4 and 5. The release's registers, order and words. |
| The advertisement (#840) | The release's PHY init, through the same frame helpers (a write drives all 64 bits, IEEE 802.3 22.2.4.5). It runs only on a PHY with 1000BASE-T full duplex ability; a 10/100 PHY is never written. Register 9 keeps its MASTER-SLAVE bits and advertises 1000BASE-T full duplex only. Register 4 drops 10/100, 100BASE-T4 and reserved bit 14, keeping pause and selector. Register 0 then enables and restarts autonegotiation, with reset and isolate clear. It runs after the poll's first BMSR read, before the current state is resolved, so a link formed before the restart is never published. It runs at boot and again after every link loss (a published link going down), and registers 4 and 9 are read back until they hold it. Where the advertisement is owed, a poll takes six reads (15, 4, 9, 0, then 4 and 9 back) and three writes (9, 4, 0), each a frame of 64 bit periods; the restart's write is left out where the PHY still held the advertisement. |
| The restart rule | Negotiation restarts after every write that repaired the advertisement, so the abilities in force are the ones written (IEEE 802.3 28.2.4.1.3). At boot it restarts whatever the PHY held, as the release's init does. A PHY that still held the advertisement is written and not restarted, so a restart's own latched loss never restarts again. A write the PHY dropped therefore leaves the advertisement unverified, and the next poll writes it again and restarts again, until it reads back. The release writes once at boot; the read-back and the pass after every loss are #919's acceptance. |
| THE OUTCOME | The restart's own write is never read back, because its bit clears itself (IEEE 802.3 22.2.4.1.7). A restart the PHY dropped therefore leaves the negotiation before it in force while registers 4 and 9 read back, so the restart is verified by what it negotiates. A negotiation complete (BMSR bit 5) on a link up that shares no 1000BASE-T mode in registers 9 and 10, while the advertisement is verified, is that earlier negotiation. Its link resolves from 4 and 5, which share no mode below 1000 Mb/s, so it is published down; the next poll owes the advertisement again with its restart taken whatever the PHY holds, and the restarts are counted (`renegotiations`). A poll that restarted negotiation resolves from a BMSR read after the restart, never the one before it, so the check restarts at most once a poll and never during a negotiation. A forced mode is published as the release publishes it. |
| THE STEP (`ctrl_loop.h`) | `ctrl_plat_phy_store_step` is the platform's THE STEP client. The store's owed step comes first, unchanged. A PHY frame runs only in a call whose store took no step of a save, with `CTRL_PLAT_PHY_STEP_US` of the pass's share left. |
| The pace, the half period | A poll every `CTRL_PLAT_PHY_POLL_US` = `MILAN_NVM_HEARTBEAT_MS * 1000 / 2`, 125 ms: the release's `PHY_POLL_NS`. MDC's half period is at least 200 ns (22.2.2.13, 22.3.4). |
| Cost | Measured on the platform image on the split CPU (split boot simulation), reads and writes alike: at most 14,537 CPU cycles at 1x1/1if (145.37 us) and 14,545 at 8x8/1if (145.45 us). The stated `CTRL_PLAT_PHY_STEP_US` stays 155 us (the most measured + 5 %, rounded up to 5 us). |
| Paths | Armed past the CSR identity check; the ready loop through THE STEP; a refused stage on each console turn (#70). A SoC with no MDIO rows arms nothing. |
| Bus map | `ctrl_plat_gen.py map` emits `milan_mac_phy_mdio_w`/`_r` and `milan_mac_link_status`, all three or none. |
| Memory ledger | Under the owner's rule of 2026-11-15 ([#923's ruling](https://github.com/kebag-logic/milan-fpga/issues/923#issuecomment-6906679024)), a measured overflow raises its entry and names the debt. The platform's 8x8/2if entry went 60.0, then 60.5 (#895), and is now 61.0 (this lane, #840), refused at 61.5: ROM debt 5.0 RAMB36 owed to S14. A new product entry ledgers the platform's 8x8/1if image, a shipping image, at 56.5 (debt half a tile). The product SoC build (`milan_soc.add_ctrl_memory`) and `ctrl_plat_image.py` plan it there by the image's symbols (`ctrl_memory.product_point`). Every other image stays refused past 56. `plan` itself is unchanged. |
| Sync | One `--no-ff` merge of dev-soft-core `70f4056f` (8670bfb0), six conflicts, both sides kept. |

**Tests of the advertisement** (`sw/firmware/ctrl/test/test_plat_phy.cpp`, on the pin-level peer `phy_peer.hpp`):
- P11: the boot's writes, each property by its own name from start values in opposite states.
- P12: a 10/100 PHY never written.
- P13: written and read back after every loss, with no restart where the PHY held it.
- P14: a PHY that lost the advertisement behind a loss is written and restarted once, whether it lost both registers, register 4 alone or register 9 alone.
- P15: a dropped write to register 4, then to register 9, is written again and negotiation restarted on each try, until it reads back, and then not again.
- P16: an unacknowledged read writes nothing.
- P17: the peer latches the abilities in force at each restart. With register 4's writes dropped through a try, at boot and after a loss, and a partner offering 100BASE-TX full duplex alone, ten periods later the advertisement in force is 1000BASE-T only, the partner has no link, the repair's own restart did it (THE OUTCOME owed none), and no restart follows.
- P18 (THE OUTCOME): the peer loses the boot's restart write, so its earlier 100 Mb/s negotiation stays in force while 4 and 9 read back. The poll publishes it down and the next poll restarts once, counted; after recovery there is no link at 100. Lost three times, the write is restarted once a poll, each counted, until one takes. There is no restart while a negotiation is incomplete, none for a negotiation at 1000BASE-T, and none on a PHY the advertisement is not for.

The control campaign plants 94 platform defects, 53 of them the PHY's and 27 the advertisement's. Among them are:
- #840's "100BASE-TX left advertised";
- the restart marked taken before the read-back verifies (caught by P15, and by P17 through the outcome it leaves to THE OUTCOME);
- the after-loss decision reading register 4, or register 9, as held when the PHY lost it alone (caught by P14 on its own words);
- THE OUTCOME's seven: unchecked, owing the advertisement without its restart, uncounted, its count wrapping, judging a link at 1000BASE-T, judging a PHY the advertisement is not for, and resolving from the BMSR read before a restart.

**Where the link edge goes on the split** (unchanged RTL): `milan_mac_link_status.link_up` -> `MultiReg` -> `i_link_up` -> `eff_link_w` (`milan_datapath.sv`; `LINK_CTRL[0]` resets 1) ->
- AVB_INTERFACE LINK_UP / LINK_DOWN (`ctr_linkup_r`/`ctr_linkdn_r`), read by the split's GET_COUNTERS;
- their GET_COUNTERS notification: the counter change -> mailbox COUNTERS_CHANGED -> `ctrl_app_aecp.c` -> AECP's unsolicited GET_COUNTERS;
- the gPTP plane's `port_enabled_i`, whose toggle ends the Pdelay_Req cease (Milan v1.2 4.2.6.2.5) and re-evaluates asCapable;
- the mailbox's LINK level and event (`o_ctl_link_up`) -> ADP, MAAP and SRP.

**Images.**
- The release image is byte-identical at base (`70f4056f`) and head, both configs: `bios.bin`, its disassembly and the ELF with debug sections stripped. Nothing the release image reads has changed since that comparison. dev-soft-core's release firmware does not carry #840; it is unchanged here.
- The split platform images, with the base `70f4056f` in parentheses:

| Point | Platform `rom` / `sram` need, B | Platform RAMB36 | `ctrl_plat`, B | Against its limit |
|---|---|---|---|---|
| 1x1, one interface (shipping) | 119,500 (117,488) / 56,288 (56,224) | 43.5 (43.0) | 17,600 (17,536) | within 56 |
| 1x1, two interfaces | 121,084 (119,072) / 58,464 (58,400) | 44.5 (44.0) | 19,136 (19,072) | within 56 |
| 8x8, one interface (shipping) | 132,204 (130,200) / 97,392 (97,328) | 56.5 (56.0) | 18,240 (18,240) | its product entry's 56.5, S14 debt; 916 B of `rom` left |
| 8x8, two interfaces | 133,772 (131,752) / 114,352 (114,224) | 61.0 (60.5) | 20,416 (20,352) | its entry's 61.0, S14 debt; 1,396 B left |

Growth by file, from the link maps, the same at every point:
- `ctrl_plat_phy.o` +1,939 B: the poll's 1,354 and the advertisement's 585, 64 of them THE OUTCOME;
- `ctrl_plat.o` +60 to +68 B;
- `ctrl_plat_main.o` +12 B.

No other object grows. Round 3's restart rule took 8 B off `ctrl_plat_phy.o` and THE OUTCOME adds 64. Every image keeps its RAMB36 count, its `ctrl_plat` size (the outcome's counter takes the struct's padding) and its ROM banks.

**Area.** The RTL is unchanged; the split images' gateware changes only in their CPU memories.
- 1x1/1if: a fifth ROM bank of 512 words.
- 8x8/1if: a 512-word bank past the 128 KiB one.

Placed at the routed head (`c805f699`, whose ROM banks are this head's), the device's block RAM is 82 of 135 tiles at 1x1/1if (64 RAMB36 / 36 RAMB18) and 92.5 at 8x8/1if (76 / 33). Other resources:

| | 1x1/1if (EPPO / ETO / ASL) | 8x8/1if (EPPO / ETO / ASL) |
|---|---|---|
| LUT | 31,314 / 31,308 / 31,309 | 42,659 / 42,736 / 42,744 |
| FF | 42,120 | 50,755 / 50,767 / 50,768 |
| DSP | 9 | 9 |

**Timing** (S9's recipe at `c805f699`, re-routed then because the ROM banking changed). The floor is #818's: a route set passes when the best of the recipe's three directives meets +0.030 ns setup and 0 ns hold at every signoff corner. Every image's ROM and SRAM banks are unchanged since that head (rounds 3 and 4 move each image by -8 and then +64 B within its banks), so no route was repeated. No seeds or extra directives were run here.
- 1x1/1if passes on all three directives: ExtraPostPlacementOpt +0.414 / +0.015, ExtraTimingOpt +0.176 / +0.032 and AltSpreadLogic_high +0.090 / +0.036.
- 8x8/1if passes on ExtraPostPlacementOpt (+0.189 / +0.031). ExtraTimingOpt (+0.005 / +0.036) and AltSpreadLogic_high (+0.002 / +0.036) miss setup on the mailbox event path (`KL_mbx/u_evt/amap_cnt_r` -> `/R`), #927's family, recorded for #927.

## Authoritative references

- #919, its scope addition (issuecomment-6907491954) and the STOP ruling (issuecomment-6907583837); #840; #927 (timing, issuecomment-6908876362); #923's BRAM ruling (issuecomment-6906679024); #665 rehearsal report (finding A / 12).
- The release's `phy_link_tick` (`sw/firmware/milan_baremetal/milan_baremetal.c`) and, on `dev`, #840's `phy_advertise_gigabit_only` with its host test (`sw/firmware/nvm_hosttest/phy_host.c`, whose per-property grading P11 mirrors).
- IEEE 802.3-2022 22.2.2.13 (MDC timing), 22.2.4 (BMCR, BMSR, PHYID, ANAR/ANLPAR), 22.2.4.1.7 (restart), 22.2.4.2.13 (BMSR latched-low link), 22.2.4.4.3 (extended status), 22.2.4.5 (frame format), 22.3.4 (MDIO output delay), 28.2.4.1.3, Table 28B-1, Table 28-2, Table 40-3, 40.5.1.1.
- Milan v1.2 4.2.6.2.5; IEEE 1722.1-2021 7.4.42 and Table 7-158 (GET_COUNTERS, LINK_UP/LINK_DOWN).
- REQUIREMENTS.md REQ-MAC-03; `docs/reference/REGISTER_MAP.md` MAC_STATUS; `sw/firmware/ctrl/loop/ctrl_loop.h`; `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3 and 5.

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
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir /tmp/pl --self-test
python3 sw/litex/test_ctrl_memory.py
```

Expected result: every command exits 0. The boot simulation's PHY lines show:
- the probe and a poll every 125 ms;
- `[0, 13]` after the latched loss, `[0, 0]` after the loss and `[13]` after the return;
- seven advertisement writes: the boot's 9 0x0200, 4 0x0001 and 0 0x1200, then 9 and 4 after each loss, each group read back;
- every frame within 155 us and MDC within IEEE 802.3 22.2.2.13.

Evidence at `1a1e6665`, each on a fresh clean clone:

| Gate | Result |
|---|---|
| Workflow jobs `rtl-fast`, `elaborate`, `docs`, step by step | rc 0: 89 steps rc 0, 159 not run with a stated reason, 0 bad. The not-run steps are the hosted-only steps, plus 29 steps of jobs these rounds do not touch (RTL lint, Yosys, BDD, CDC, census; the AECP and SRP campaigns), each rc 0 at `afa3ea19` |
| Control mutant campaign (`firmware-control-mutants`) | 769 of 769 caught. Among them are the platform's 94: the PHY's 53, and within those the advertisement's 27, with THE OUTCOME's seven |
| Firmware suites (`firmware-unit`) | `test_ctrl_firmware: PASS`, every arm |
| Firmware coverage ratchet | `ctrl_plat_phy.c` 178/178 lines, 164/164 branches, its row ratcheted there; PASS on 40 files |
| Split boot simulation, 1x1/1if and 8x8/1if | rc 0; 59 frames, 10 publications, the longest 145.37 and 145.45 us against 155; the advertisement's seven writes as above |
| Split boot simulation self-test | rc 0: 6 of 6 native controls, 6 of 6 plants caught (`phy-unadvertised` among them), 8 of 8 placement controls |
| Platform ledger self-test | rc 0 at every point; 8 of 8 controls |
| Memory test (`test_ctrl_memory.py`) | PASS, 0 failures |
| The reviews' own probes | R852-1's retry probe: the last restart on `0001`, no link to a 100BASE-TX-only partner. R851-1's `retry_probe.sh`: 21 of 21. R851-1's `mutants.sh`: with the three anchors this head renamed, m3, m3b and m8 are caught; m6 is its equivalent mutant |
| Release image | Byte-identical, both configs, at `c805f699`; nothing it reads has changed since |
| S9 routes | Not repeated: every image's ROM and SRAM banks are round 2's. See Timing (#818's floor) |
| CPU service budget harness | Its images at this head are byte-identical to round 2's and the base's at both shapes, so its verdict is the base's. 1x1/1if rc 0: 96 groups, 0 refusals, 0 of 130,341 passes over the 2 ms share, 7 misses = the `backlog-owed` held-egress rows. 8x8/1if: 95 groups, 0 refusals, 0 of 270,769 passes over the share, the same 7 rows, and exit 1 on 11 stated-cost lines, the base's (#920 issuecomment-6908928237). The PHY's cost there is THE STEP's, measured by the boot simulation |
| Native suite sweep (`verilator-suites`, 4 shards) | Not re-run: these rounds change no RTL and no Verilator testbench source. At `afa3ea19`: 65 of 65 suites, 2,713,040 checks, 0 failures |

## Known limitations / out of scope

- **Timing.** Under #818's floor both split images pass, 1x1/1if on all three directives and 8x8/1if on ExtraPostPlacementOpt. 8x8/1if's other two directives miss setup on the mailbox event path, in unchanged logic; that is #927's family, and #927's own acceptance needs all three directives at every ROM banking.
- **The block RAM debt is S14's.** 8x8/1if plans 56.5 RAMB36 (half a tile) and 8x8/2if plans 61.0 (5.0 RAMB36), each ledgered under the owner's rule. A parallel implementation of the same product-entry mechanism is in #923's lane (PR #931), and the sync will reconcile the two.
- **The harness's known lines are the base's.** Its image composes no platform and is byte-identical to the base's. Its seven `backlog-owed` held-egress rows are the base's already-ruled rows. Its 8x8/1if stated-cost lines are the base's too: the base keys the statements on the interface count, so 8x8/1if is held to 1x1/1if's figures. #920 records the same at this base (issuecomment-6908928237), each line within #914's own 8x8/1if statements.
- **The PHY's frames wait for a save.** Under input that never leaves a pass empty, with a save in flight, the frames wait for the save; the store's steps come first.
- **A repair costs one renegotiation.** After a loss where the PHY no longer holds the advertisement, or after a write it dropped, negotiation restarts once the write is repeated, and the link returns when the PHY renegotiates. A PHY that never takes the writes is restarted on every try and so holds no link, which is #840's outcome for a PHY that cannot advertise 1000BASE-T alone.
- **The release firmware has the same gap, and it is not changed here.** Its PHY init (`phy_advertise_gigabit_only` on `dev`) writes register 0's restart once and cannot read it back (22.2.4.1.7). So a restart write the PHY drops leaves the release's earlier negotiation in force, which can be a 100 Mb/s link the MAC is silent on. The split's poll closes this by THE OUTCOME; the release is a known release limitation.
- **A forced mode is the release's.** THE OUTCOME judges a completed autonegotiation. A PHY in a forced mode (BMCR's autonegotiation enable clear) is published in that mode, as the release publishes it; the advertisement's restart write enables autonegotiation.
- **The bench acceptance is the gating run's.** That is #919's tap link-flap and gPTP resume within 5 s.

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
