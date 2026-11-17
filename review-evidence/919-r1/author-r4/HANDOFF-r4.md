# #919 round 4 — [A785] handoff (kept current)

Lane: 919-phy-link, PR #933 (base dev-soft-core). Round 3's head da8a8b84 (its REVIEW READY was posted on #919 as
issuecomment-6932294892 before this round was assigned; the manager publishes rounds 3 and 4 together). Round 4
starts on da8a8b84 before any review. Nothing pushed by me.

Round 4 scope (manager):
- Close the disclosed gap: a dropped register-0 restart write cannot be read back (IEEE 802.3 22.2.4.1.7), so a
  verified advertisement can leave the old negotiation active. Verify the restart by its outcome: once
  autonegotiation completes (register 1 bit 5) or the link comes up, check the resolved result (register 10's
  1000BASE-T status, the resolved speed). Below 1000BASE-T with the advertisement verified 1000BASE-T only: restart
  again, paced like the poll, counted.
- The pin-level peer's negotiation latch: a dropped register-0 write leaves the old abilities in force. The case:
  a 100BASE-TX-only partner, the register-0 write dropped once: no link at 100 after recovery, one extra restart;
  a plant (the outcome check skipped) caught by name.
- The release firmware has the same gap: noted in the PR body as a known release limitation, not changed.
- The coverage ratchet row for ctrl_plat_phy.c rewritten to the final head's measurement.
- The PHY frame within 155 us; the gates on a clean clone; the images (route again only if the ROM banking changes;
  the floor is #818's, +0.030 ns setup and 0 ns hold).
- ONE REVIEW READY on #919 covering rounds 3 and 4; round4/HANDOFF-r4.md and round4/PR-BODY.md.

## Status

- [x] the outcome check, the peer's latch, P18, the plants: 8beada76
- [x] the count's saturation graded and planted (coverage's one missing branch): 33041d64
- [x] figures restated, the ratchet row at 178/178 and 164/164: 1a1e6665
- [x] gates at 1a1e6665 (table below)
- [x] REVIEW READY for rounds 3 and 4 posted on #919 (issuecomment-6934522568, text comments/REVIEW-READY.md); nothing pushed

Head 1a1e6665: 8beada76, 33041d64, 1a1e6665 on da8a8b84. No RTL, mailbox contract, CPU budget bound or release
firmware changed (receipts/head/files-changed.txt).

## Changes (file:line — reason)

THE OUTCOME (8beada76):
- `sw/firmware/ctrl/plat/ctrl_plat_phy.c:246-265` (GIG_PEER): a completed negotiation on a link up that shares no
  1000BASE-T mode in registers 9 and 10, while the advertisement is verified (`adv == 0`), owes the advertisement
  again with its restart taken whatever the PHY holds, at the next poll, and is counted (`renegotiations`,
  saturating). The poll continues to registers 4 and 5 as the release does; with register 4 verified they share no
  mode, so the word is link down. The check is reached only through BMCR's autonegotiation-complete branch, so it
  never judges a negotiation in progress.
- `ctrl_plat_phy.c:233-238` (ADV_RESTART): a poll that took the restart resumes at the second BMSR read, so it
  resolves from a BMSR read after the restart. Without it, a repair on a link published up resolved the stale
  pre-restart BMSR, and THE OUTCOME owed a needless restart (found by P17's new oracle, below).
- `ctrl_plat_phy.c:202-209, 273-276`: a 10/100 PHY is `CTRL_PLAT_PHY_ADV_NONE`, not 0, so `adv == 0` means
  verified; the owed test reads the OWED bit. `:38`, `:228-229`, `:234`: the boot flag renamed
  `CTRL_PLAT_PHY_ADV_RENEGOTIATE` (the boot's restart and THE OUTCOME's).
- `sw/firmware/ctrl/plat/ctrl_plat_phy.h:53-67` THE OUTCOME; `:192-197` the flags; `:250` the counter, in the
  struct's padding (struct size unchanged on RV32 and the host: `ctrl_plat` unchanged at every point).
- `sw/firmware/ctrl/test/phy_peer.hpp:18-26,64,159-162,182`: `drop_restarts`, the next restart writes lost whole
  (register 0, the restart count, the abilities in force and the link stay the last negotiation's); a negotiation
  sets BMSR's autonegotiation complete.
- `sw/firmware/ctrl/test/test_plat_phy.cpp:720-843` P18 (three tests); `:672-673` P17 requires the repair's own
  restart (THE OUTCOME owing none); header list `:52-58`.
- `sw/firmware/ctrl/test/plat_mutants.py:312-326` anchors (the rename, the HELD line's break, the early-restart
  plant's flag moved to 0x8 off the new NONE bit), `:358-369` the boot and MII plants' anchors given context,
  `:392` the early-restart plant's needle, `:401-419` THE OUTCOME's plants.
- `tb/verilator/ctrl_split_boot/run.py:133-135`: the `phy-unadvertised` plant's anchor (renamed flag, context line).
- `sw/firmware/ctrl/plat/README.md:93` THE OUTCOME; `:138` tests; `:142-143` the plants.

The saturation (33041d64): `test_plat_phy.cpp:806-815` the count started at 0xfffe saturates at 0xffff; plant
`plat-phy-outcome-count-wraps`. Coverage at 8beada76 was 178/178 lines and 163/164 branches (the guard's false
branch), refused by the ratchet (receipts/measure/fw-coverage-check-8beada76-refused.log).

Figures (1a1e6665), measured at 8beada76 on a clean clone (receipts/measure/):
- `sw/firmware/gtest/coverage.ratchet:30` ctrl_plat_phy.c 178/178, 164/164 (measured at 33041d64).
- `sw/firmware/ctrl/plat/README.md:127,129`, `docs/design/SPLIT_CONTROL_MEMORY.md:147-148,399-409`,
  `sw/litex/ctrl_memory.py:285,292`: rom +64 B at every point; tiles, banks and ctrl_plat unchanged.
- `tb/verilator/ctrl_split_boot/README.md:97-103`: the boot's figures. The frame's cost is unchanged (145.37 and
  145.45 us), so `ctrl_plat_phy.h`'s statement and `CTRL_PLAT_PHY_STEP_US` (155) stand.

## New checks (planted defect — failing words)

| Defect | Caught by — words |
|---|---|
| plat-phy-outcome-unchecked (the manager's plant: the outcome check skipped) | P18TheRestartIsVerifiedByItsOutcome — "P18 no link at 100 after recovery"; also P18OneRestartAPollUntilOneTakes — "P18 one restart a poll, paced like the poll" |
| plat-phy-outcome-not-renegotiated (owed without its restart) | P18TheRestart... — "P18 one extra restart"; also the paced test |
| plat-phy-outcome-uncounted | P18TheRestart... — "P18 the outcome's restart is counted" |
| plat-phy-outcome-count-wraps | P18OneRestartAPollUntilOneTakes — "P18 the count saturates at 0xffff" |
| plat-phy-outcome-at-gigabit (judging a 1000BASE-T link) | P18OnlyAMissingGigabitLinkOwesARestart — "P18 a negotiation at 1000BASE-T owes no restart" |
| plat-phy-outcome-on-unadvertised (judging a PHY the advertisement is not for) | P18OnlyAMissing... — "P18 a PHY the advertisement is not for owes no restart" |
| plat-phy-resolved-before-restart (the poll resolving the pre-restart BMSR) | P17 — "P17 the repair restarts negotiation itself" |
| (re-needled) plat-phy-restarted-before-verified | P17 — "P17 the repair restarts negotiation itself"; also P15 as before. THE OUTCOME now also recovers this round-3 defect, so P17's end state alone no longer fails; its new oracle (no outcome restart owed) does |

Local PHY subset at 33041d64's tree: 54 of 54 caught (receipts/measure/phy-plant-subset-33041d64-tree.log).

The reviews' own probes at 1a1e6665 (receipts/probes/):
- R852-1's retry probe: rc 0, fault `advertised-at-last-restart=0001 active-Mbps=0 restarts=2`; control `restarts=1`.
- R851-1's retry_probe.sh: rc 0, 21 of 21, `advertised-at-last-restart=0001 restarts=2 adv-owed=0`.
- R851-1's mutants.sh: m3, m3b and m8 refused (their anchors name `CTRL_PLAT_PHY_ADV_BOOT` and the old owed test);
  an executor's copy with those three anchors renamed (diff in the receipt): all caught but m6, the review's
  equivalent mutant.

## Gate table

| Gate | Command | Head | rc | Receipt |
|---|---|---|---|---|
| Workflow jobs rtl-fast, elaborate, docs | run_wf.py per job, fresh clone each; verify_wf.py with the job reasons | 1a1e6665 | 0 | workflows/verify-1a1e6665.md: 89 steps rc 0, 159 not run with a reason (29 of them jobs these rounds do not touch, each rc 0 at afa3ea19), 0 bad |
| Firmware suites | firmware-unit (test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4, ctrl_nvm) | 1a1e6665 | 0 | workflows/logs/rtl-fast__firmware-unit__ci_step_10.log: test_ctrl_firmware: PASS |
| Coverage ratchet | fw_coverage.py --selftest, --check | 1a1e6665 (and 33041d64; 8beada76 refused 163/164) | 0 | ci_step_12.log: ctrl_plat_phy.c 178/178 164/164, PASS (40 files) |
| Control campaign | firmware-control-mutants | 1a1e6665 | 0 | ci_step_9.log: mutants: 769 of 769 caught |
| Boundary, Verilator builders | firmware-boundary, firmware-verilator | 1a1e6665 | 0 | workflows/logs |
| Elaborate | elaborate-gates-0, elaborate-gates-1, elaborate (product LiteX venv) | 1a1e6665 | 0 | workflows/logs |
| Docs | docs.yml's six jobs (the idiom gates among them: docs-gates-0 gate_38, gate_39) | 1a1e6665 | 0 | workflows/logs |
| Split boot simulation 1x1/1if, 8x8/1if | run.py | 1a1e6665 (and 8beada76) | 0, 0 | boot/: 145.37 and 145.45 us at most |
| Split boot self-test | run.py --self-test | 1a1e6665 | 0 | boot/boot-self-test-1a1e6665.log: 6/6 native, 6/6 plants, 8/8 placement |
| Platform ledger self-test | plat_ledger.py --self-test | 1a1e6665 (and 8beada76) | 0 | boot/plat-ledger-self-test-1a1e6665.log |
| Memory test | sw/litex/test_ctrl_memory.py | 1a1e6665 | 0 | boot/test-ctrl-memory-1a1e6665.log |
| R852-1's retry probe, control | its retry_probe.py, scratch copy | 1a1e6665 | 0, 0 | probes/ |
| R851-1's retry_probe.sh, mutants.sh (and renamed copy) | scratch copies | 1a1e6665 | 0; m3, m3b, m8 caught with renamed anchors | probes/ |
| Harness image identity | harness_identity.sh, both shapes | 1a1e6665 | identical | budget/ |
| ROM banking | plat_ledger's plans, da8a8b84 vs 8beada76; images 8beada76 = 1a1e6665 | 1a1e6665 | unchanged | measure/rom-banking.txt: no route |
| Release image | not rebuilt: no input changed since c805f699 | 1a1e6665 | n/a | head/files-changed.txt |
| Native sweep | not re-run: no RTL or Verilator testbench source changed | (afa3ea19: 65 of 65) | n/a | round 2 |

Units: the docs, firmware and campaign batches and the boot unit on the session's own four 8-CPU slices; the
measurement units and the two elaborate batches on ranges cpu_ranges.py picked. The picker returned one range three
times while the measurement units started, so three of them shared 48-55 (only my own jobs slowed); the elaborate
batches were started only once a fresh pick differed. No background loop starts anything; every unit of mine has
ended (listed at the end).

## ROM

Platform images at 1a1e6665 (= 8beada76's bytes) against da8a8b84, `rom` B, banks, tiles (receipts/measure/):
- 1x1/1if 119,500 (119,436), banks [64K, 32K, 16K, 4K, 2K] (same), 43.5, 1,332 B left in its banks
- 1x1/2if 121,084 (121,020), banks [64K, 32K, 16K, 8K] (same), 44.5, 1,796 B left
- 8x8/1if 132,204 (132,140), banks [128K, 2K] (same), 56.5, product entry, 916 B left
- 8x8/2if 133,772 (133,708), banks [128K, 4K] (same), 61.0, its entry, 1,396 B left
By file: ctrl_plat_phy.o 1,875 -> 1,939 B; nothing else. The banks are round 2's routed ones, so no route.
Timing under #818's floor (best of three directives meets +0.030 ns setup and 0 ns hold at every corner), round 2's
routes at c805f699: 1x1/1if passes on all three (EPPO +0.414/+0.015, ETO +0.176/+0.032, ASL +0.090/+0.036);
8x8/1if passes on EPPO (+0.189/+0.031); its ETO (+0.005) and ASL (+0.002) miss setup on the mailbox event path,
#927's family. Round 2's and round 3's texts applied +0.030 to hold as well; round 4 restates by #818.

## Open risks / questions

- A forced mode (BMCR's autonegotiation enable clear) is published as the release publishes it; THE OUTCOME judges
  a completed autonegotiation. A PHY left forced before boot whose register-0 write is lost stays in that mode.
- A PHY that downshifts below 1000 Mb/s against a gigabit-only advertisement (a vendor feature on two-pair
  cabling) is restarted once a poll and holds no link; #840 wants no link other than 1000BASE-T.
- The release firmware's same gap is a known release limitation (PR body); not changed.
- R851-1's mutants.sh no longer places m3, m3b and m8 at this head (renamed anchors); the adapted copy is in the
  receipt, and the campaign's own plants cover m3 and m3b by name.
