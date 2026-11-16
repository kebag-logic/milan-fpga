# #919 round 2 — [A785] handoff (kept current)

Lane: 919-phy-link. Round 1 head 55769f09 on dev-soft-core 659d7687 (round1/HANDOFF-r1.md). Round 1 posted
STOP (issuecomment-6905511089, 8x8/1if timing). Nothing pushed; the manager pushes and opens the PR.

Round 2 scope (manager, #919 issuecomment-6907583837 ruling, issuecomment-6907491954 scope addition, resume brief):
1. Both split images' routes recorded as "misses at the base, owed to #927" with the figures; no seeds, no extra
   directives; route again only if the gateware changes after the merge; record what a round-2 route gives,
   owed to #927.
2. The seven backlog-owed held-egress rows: the base's already-ruled rows, recorded as such, not a stop.
3. #840's 1000BASE-T-only advertisement on the split PHY path through this lane's MDIO helpers, as the release
   firmware applies it: written and verified at boot and after every link loss; host test; planted defect caught
   by name; release image byte-identical.
4. One --no-ff merge of origin/dev-soft-core 70f4056f onto 55769f09, conflicts resolved keeping both sides.
5. CPU budget harness 1x1/1if and 8x8/1if at the final head (8x8/1if as parallel part units on booked CPUs, must
   complete); remaining gates on a clean clone; the 4-shard sweep. Owner's BRAM rule with no STOP (#923
   issuecomment-6906679024): a measured overflow raises the entry and names the debt.

## Status

- [x] merge 70f4056f: 8670bfb0 (parents 55769f09, 70f4056f), six conflicts, both sides kept
- [x] #840 advertisement on the split: fcceb603
- [x] boot simulation grades it: 8b742277
- [x] ledger at the measured images (owner's rule, no STOP): c805f699
- [x] tests P11-P16, 18 planted defects (85 platform, PHY 44), coverage ctrl_plat_phy.c 173/173 160/160
- [x] afa3ea19: the boot simulation's native stand-in prints the advertisement (its six native controls were WRONG
  at c805f699: the stand-in printed no PHYW lines), the header's frame-cost provenance and the boot README's figures
- [x] gates at afa3ea19 (table below)
- [x] REVIEW READY posted on #919 (issuecomment-6929222018, text comments/REVIEW-READY.md); nothing pushed

Head afa3ea19: 8670bfb0 (merge), fcceb603, 8b742277, c805f699, afa3ea19 on 55769f09. c805f699 -> afa3ea19 changes
tb/verilator/ctrl_split_boot/run.py (the stand-in), its README, and a comment in ctrl_plat_phy.h; the harness and the
routes ran at c805f699, their inputs unchanged (route images relinked at afa3ea19: identical; the harness reads none
of the three files).

**Power cycle, 2026-11-16 15:40 CET** (host shutdown and memory upgrade; every unit killed). Units with a recorded
rc kept their results: the workflow jobs, the boot simulations, the ledger, the release images, the six routes, the
harness builds, 1x1 part 0 (rc 0) and 8x8/1if part 0 (rc 1: the base's stated-cost lines). The units without one were
treated as cut: 1x1 part 1, 8x8/1if parts 1 and 2 (part 3 had not started), and the four sweep shards. Their outputs
were removed: 68 result files of those parts' groups (scripts/clean_parts.py), sweep2/ and its four shard clones.
They were re-run: the 117 remaining groups as parts B0-B4 (8x8/1if) and B0-B1 (1x1) on booked ranges as they free,
then a regrade over every group; the sweep at afa3ea19 again.

**Host crash, 2026-11-16 18:46 CET** (hard reset, rebooted 19:06). Kept, rc recorded: 8x8/1if part B1 (rc 0, 14
groups). Cut, no rc: 8x8/1if B0, B2, B3, B4 and 1x1 B0, B1 (no part had graded: no group JSON). Their 186 group
files were removed and the 103 groups re-run as parts C0-C6 (8x8/1if, each on a booked range) and C0-C3 (1x1, two
booked, two on the session pool). The sweep (finished 17:45) and its receipts were checked byte for byte against the
scratch sources: intact.

**Host shutdown, 2026-11-16 19:39 CET** (maintenance; back 19:43). Every C part was cut with no rc (none had
graded). Their 191 group files were removed and the same eleven parts re-run at once: 8x8/1if C0-C2 on three
booked ranges, C3-C6 beside them on those ranges at 3 jobs, 1x1 C0-C3 on the session pool at 4 jobs. The files written
after 19:00 (this handoff, comments/REVIEW-READY.md, sweep/large-logs.sha256) were checked whole.

## Changes (file:line — reason)

Merge 8670bfb0 (one --no-ff of dev-soft-core 70f4056f onto 55769f09). Six conflicts, each resolved keeping both sides:
- `sw/firmware/ctrl/plat/ctrl_plat.c:274`: upstream's `AECP_ENTITY_NAME_RUNS` call, with this lane's THE STEP comment.
- `sw/firmware/gtest/coverage.ratchet`: ctrl_plat.c remeasured (136/136, 42/42) in the commit after.
- `sw/litex/ctrl_memory.py` and `ctrl_memory_ledger.py`: both sides' 60.5 histories in one text, and upstream's
  PLAT_8X8_1 18,240; the measured sizes and entries are in c805f699.
- `sw/firmware/ctrl/plat/README.md` and `docs/design/SPLIT_CONTROL_MEMORY.md`: upstream's figures kept, this lane's
  PHY sentences added after them.
The merged tree passed every platform arm (plat, platboot1/2, platmap, platrv32) before the commit.

#840 on the split (fcceb603):
- `sw/firmware/ctrl/plat/ctrl_plat_phy.h:28` THE ADVERTISEMENT: the design and its reasons; `:172` the owed flags
  (OWED, BOOT, RESTARTED); `:205` nine stages after STATUS; struct fields adv, resume, gig, control.
- `sw/firmware/ctrl/plat/ctrl_plat_phy.c:38` owed at arm, with BOOT (restart whatever the PHY holds, as the release's
  init); `:109` gigabit_only (no 10/100, 1000 FD, not HD); `:117` publish(): a published link going down owes it
  again; `:145` a write frame drives all 64 bits (22.2.4.5); `:202-255` the stages: the ability read (a PHY without
  1000BASE-T FD is never written), 4, 9, 0 read, no write after a NAK, 9 then 4 written as the release writes them,
  0 restart at most once a time it is owed (boot always; after a loss only if the PHY no longer held it), 4 and 9
  read back (verified, else owed again); `:258` diverted to after the first BMSR read, before the current state.
  Reason for the restart rule: a restart latches a loss of its own; restarting after every loss would loop.
  The release's init writes once (dev's phy_advertise_gigabit_only); the read-back and the post-loss pass are #919's
  acceptance (issuecomment-6907491954).
- `sw/firmware/ctrl/test/phy_peer.hpp:142` the host peer takes Clause-22 writes, counts restarts, can ignore a
  register's writes and can latch a loss on restart.
- `sw/firmware/ctrl/test/test_plat_phy.cpp`: P3, P4, P5, P6, P7 updated for the advertisement's frames and writes;
  P11-P16 new (below).
- `sw/firmware/ctrl/test/test_plat_boot.cpp`: the composed tests' first window 5 -> 10 ms (kFirstPollMs: the boot's
  advertisement adds nine frames, one a step).
- `sw/firmware/ctrl/test/plat_mutants.py`: two anchors moved by the refactor re-anchored (loss-not-latched,
  turnaround-driven); 18 new defects.
- `sw/firmware/gtest/coverage.ratchet`: ctrl_plat.c 136/136 42/42, ctrl_plat_phy.c 173/173 160/160. A `--write`
  also raised four rows of files this lane does not touch (aecp_commands.c, aecp_face.c, aecp_maps.c, srp_mbx.c, all
  at 100 %); those were restored to upstream's values: upstream's ratchet is stale for them (observation, not this
  lane's).

Boot simulation (8b742277): `tb/verilator/ctrl_split_boot/sim_main.cpp:133` the peer takes writes (PHYW lines);
`run.py:385` advertisement(): the boot's 9 0x0200, 4 0x0001, 0 0x1200, then 9 and 4 after each of the two losses,
no other write, each group read back; `run.py:133` plant phy-unadvertised; the two older plants re-anchored.

Ledger (c805f699), the owner's rule of 2026-11-15 as #923's ruling applies it (issuecomment-6906679024):
- `sw/litex/ctrl_memory.py:288` product entry `platform-8x8-one-interface` at 56.5 (ctrl_plat 18,240), the
  two-interface platform entry 60.5 -> 61.0 (ctrl_plat 20,416); `:299` product_point(); `Ledgered.product`.
- `sw/litex/milan_soc.py:3345` add_ctrl_memory plans by product_point; `ctrl_plat_image.py:201` likewise without
  --ledgered-point; `plan()` itself unchanged, so every measurement keeps its meaning.
- `sw/litex/ctrl_memory_ledger.py`, `test_ctrl_memory.py`: the cases, facts (product_facts), 13 planted ledgers,
  4 product mutants; the image writer reaches 62.0 (three tiles shifted, was two, reaching 61.0).
- `tb/verilator/ctrl_split_boot/plat_ledger.py`: 8x8-if1 names its product entry; controls budget-under-a-point
  moved to 1x1-if2, override-unlinked renamed, product-override-not-taken added (8 of 8).
- Docs: SPLIT_CONTROL_MEMORY.md sections 3 and 5, plat/README.md.

## New checks (planted mutant — failing words)

| Defect | Caught by — words |
|---|---|
| plat-phy-100base-tx-advertised (#840's named) | PlatPhy.P11 — "P11 no 100BASE-TX advertised" |
| plat-phy-10base-t-advertised | P11 — "P11 no 10BASE-T advertised" |
| plat-phy-reserved-kept | P11 — "P11 reserved bit 14 cleared" |
| plat-phy-half-duplex-advertised | P11 — "P11 no 1000BASE-T half duplex advertised" |
| plat-phy-master-slave-dropped | P11 — "P11 MASTER-SLAVE kept" |
| plat-phy-test-mode-kept | P11 — "P11 the test mode cleared" |
| plat-phy-not-restarted | P11 — "P11 autonegotiation restarted" |
| plat-phy-reset-kept | P11 — "P11 reset cleared" |
| plat-phy-boot-restart-dropped | P11 — "P11 the boot restarts negotiation whatever the PHY holds" |
| plat-phy-write-released | P6 — "P6 every frame a Clause-22 read or write, driven as 22.2.4.5 drives it" |
| plat-phy-mii-written | P12 — "P12 a PHY without BMSR's extended capability is never written" |
| plat-phy-10-100-written | P12 — "P12 a PHY without 1000BASE-T full duplex ability is never written" |
| plat-phy-advertised-once | P13 — "P13 after a link loss the advertisement is written again" |
| plat-phy-restart-every-loss | P13 — "P13 a loss with the advertisement held restarts nothing" |
| plat-phy-reset-phy-not-restarted | P14 — "P14 a PHY that lost the advertisement is written and restarted" |
| plat-phy-restart-each-poll | P15 — "P15 and restarts negotiation once, not each poll" |
| plat-phy-advertisement-unverified | P15 — "P15 an advertisement that does not read back is written again each poll" |
| plat-phy-written-before-read | P16 — "P16 no write before its read" |
| (re-anchored) plat-phy-loss-not-latched, plat-phy-turnaround-driven | P3 / P6, as before |
| boot plant phy-unadvertised | split boot self-test: a PHY finding |
| memory: no product point / every entry a product / by its staging buffer alone / SoC build plans none | test_ctrl_memory checks arm, each by a product fact |

Local campaign on the PHY subset: 44 of 45 caught at first (restart-every-loss escaped: P13's write-count ASSERT
aborted before its restart check), the check moved ahead of the ASSERT, both P13 defects then caught. The full
campaign runs in the firmware-control-mutants job (gate table).

## Gate table

| Gate | Command | Head | rc | Receipt |
|---|---|---|---|---|
| Split boot simulation 1x1/1if | run.py | afa3ea19 (c805f699 identical figures) | 0 | boot/boot-1x1-afa3ea19.txt |
| Split boot simulation 8x8/1if | run.py --shape endstation_ax7101_8x8 | afa3ea19 | 0 | boot/boot-8x8-afa3ea19.txt |
| Split boot self-test (6 native controls, 6 plants incl. phy-unadvertised, placement controls) | run.py --self-test | afa3ea19 | 0 | boot/boot-self-test-afa3ea19.txt (c805f699's WRONG run kept) |
| Platform ledger self-test (4 points, 8 controls) | plat_ledger.py --self-test | afa3ea19 | 0 | boot/plat-ledger-self-test-afa3ea19.txt |
| Release image byte-identical, both configs | release_image.sh, base 70f4056f vs head | c805f699 (nothing it reads changed after) | identical | release-image/COMPARE.txt |
| Control mutant campaign | firmware-control-mutants | afa3ea19 | 0 | 760 of 760 caught |
| S9 route 1x1/1if EPPO (integrated) | rt2/tools | c805f699 (image identical at afa3ea19) | 0; signoff 1 | WNS +0.414, WHS **+0.015** (TDM render FIFO crossing, #927's) |
| S9 route 1x1/1if ETO | rt2/tools | c805f699 | 0; signoff 0 | WNS +0.176, WHS +0.032: meets |
| S9 route 1x1/1if ASL | rt2/tools | c805f699 | 0; signoff 0 | WNS +0.090, WHS +0.036: meets |
| S9 route 8x8/1if EPPO (integrated) | rt2/tools | c805f699 (image identical at afa3ea19) | 0; signoff 0 | WNS +0.189, WHS +0.031: meets |
| S9 route 8x8/1if ETO | rt2/tools | c805f699 | 0; signoff 1 | WNS **+0.005** (KL_mbx/u_evt amap_cnt_r -> /R, the mailbox path #927 names), WHS +0.036 |
| S9 route 8x8/1if ASL | rt2/tools | c805f699 | 0; signoff 1 | WNS **+0.002** (KL_mbx/u_evt amap_cnt_r -> tick_cnt_r /R), WHS +0.036 |
| Timing verdict | recorded, owed to #927 (ruling issuecomment-6907583837, #927 issuecomment-6908876362) | | | 1x1/1if meets on ETO and ASL, misses hold on EPPO (TDM render FIFO crossing); 8x8/1if meets on EPPO, misses setup on ETO and ASL (mailbox event path). No seeds, no extra directives. |
| Workflow jobs rtl-fast, elaborate, docs | run_wf.py per job, fresh clone each | afa3ea19 | 0 (118 rc 0, 130 not run with a reason, 0 bad) | workflows/verify-afa3ea19.md; census rerun twice for sv2v's 900 s limit under load (workflows/README.md) |
| AECP and SRP mutant campaigns | firmware-aecp-mutants, firmware-srp-mutants | afa3ea19 | 0 | test_ctrl_firmware: PASS each |
| CPU service budget harness 1x1/1if | run.py parts on booked ranges (C2, C3 on the pool), then --regrade over every group | c805f699 (inputs = afa3ea19's; image = base 70f4056f's) | 0 | budget/1x1/: 96 groups, 0 refusals, 0 of 130,341 passes over the share, 7 misses = the backlog-owed held-egress rows (base, ruled) |
| CPU service budget harness 8x8/1if | run.py as parallel parts, each on a booked range or beside one, then --regrade | c805f699 (same) | 1 (the base's) | budget/8x8-1if/: 95 groups, 0 refusals, 0 of 270,769 passes over the share, the same 7 backlog-owed rows; 11 STATED lines, the base's (1x1-keyed statements; #920 issuecomment-6908928237) |
| Native suite sweep, 4 shards (verilator-suites) | native-shards.py, the session pool's four 8-CPU slices (no range was bookable; no route ran beside it) | afa3ea19 | 0 each | sweep/: 65 of 65 suites, 2,713,040 checks, 0 failures (15/17/17/16 suites; 6,308 / 5,811 / 6,011 / 4,844 s) |

## ROM and area

Platform images, head (base 70f4056f), `rom` / `sram` B, RAMB36, `ctrl_plat` B (receipts/boot/plat-ledger-*):
- 1x1/1if 119,444 (117,488) / 56,288 (56,224), 43.5 (43.0), 17,600 (17,536)
- 1x1/2if 121,028 (119,072) / 58,464 (58,400), 44.5 (44.0), 19,136 (19,072)
- 8x8/1if 132,148 (130,200) / 97,392 (97,328), 56.5 (56.0): its product entry, S14 debt half a tile, 972 B left
- 8x8/2if 133,716 (131,752) / 114,352 (114,224), 61.0 (60.5): its entry raised, S14 debt 5.0 RAMB36, 1,452 B left
Growth by file at every point (receipts/boot/rom-per-file-base-70f4056f-head.txt): ctrl_plat_phy.o +1,883 B
(round 2's advertisement 529 of it), ctrl_plat.o +60..68, ctrl_plat_main.o +12; nothing else.

Device (placed, receipts/route/*/utilization_place-table.txt): 1x1/1if 82 of 135 block RAM tiles (64 RAMB36 / 36
RAMB18), LUT 31,308-31,314, FF 42,120; 8x8/1if 92.5 tiles (76 / 33), LUT 42,659-42,744, FF 50,755-50,768; DSP 9.
The gateware changes from round 1 only in the CPU memories' banking (route/route-inputs-c805f699-afa3ea19.txt).

## Open risks / questions

- #923's lane implements the same product-entry mechanism (its option A); the sync reconciles the two.
- Timing at both shapes is #927's (recorded above); no seeds or extra directives here.
- The harness's 8x8/1if exit 1 and the seven held-egress rows are the base's (identity receipt).
- Observation for a new issue (not this lane's): upstream's coverage.ratchet rows for aecp_commands.c, aecp_face.c,
  aecp_maps.c and srp_mbx.c record fewer lines and branches than the tree measures (all 100 %); left as upstream's.
- A restart after a loss where the PHY lost the advertisement costs one renegotiation.
