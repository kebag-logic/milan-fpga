# #919 round 3 — [A785] handoff (kept current)

Lane: 919-phy-link, PR #933 (base dev-soft-core). Round 2 head afa3ea19 (pushed by the manager; packets archived
review-evidence/919-r1, archive c129707b). Round 3 answers two NEGATIVE reviews of afa3ea19: the external R852-1
(PR #933 issuecomment-6929889363) and the internal R851-1 (PR #933 issuecomment-6930496445), added to this round by
the manager. Nothing pushed by me.

Round 3 scope (manager), fix exactly:
- R852-F1 = R851-F1 (MAJOR): the restart flag set before verification lets a repaired advertisement stay inactive.
  Restart after every repaired write, at boot and after every loss; a negotiation latch in phy_peer.hpp; the
  reviewer's case (register-4 writes dropped on the first poll, a 100BASE-TX-only partner, ten more periods: no
  link, the active advertisement 1000BASE-T only); a plant (the flag set before verification) caught by name; the
  frame cost within its stated 155 us.
- R852-F2 = R851-F4 (MINOR): "six reads and three writes", "64 bit periods", the conditional restart omission kept.
- R852-R1 = R851-R1 (RESIDUE): no workflow references in the new source comments.
- R851-F2 (MINOR, Tests): the after-loss restart graded with register 4 lost alone and register 9 lost alone, each
  one restart; the reviewer's m3 and m3b as plants, caught by name.
- R851-F3 (MINOR, Docs): the fit page's section 3 states one history for the platform 8x8/2if entry.
Gates: firmware units, the control campaign, fw_coverage --check (100 % for ctrl_plat_phy.c), the boot simulation,
docs jobs, the PHY's figures at 1x1/1if and 8x8/1if; route again only if the ROM banking changes.

## Status

- [x] F1: 319afb3d
- [x] R852-F2 / R851-F4 and R852-R1 / R851-R1: 319afb3d (header, README), c79f1c76 (ctrl_memory.py)
- [x] R851-F2: 5c2682a4
- [x] R851-F3: c79f1c76
- [x] figures restated at the measured head: da8a8b84
- [x] gates at da8a8b84 (table below)
- [x] REVIEW READY posted on #919 (issuecomment-6932294892, text comments/REVIEW-READY.md); nothing pushed

Head da8a8b84: 319afb3d, 5c2682a4, c79f1c76, da8a8b84 on afa3ea19. No RTL, no mailbox contract, no CPU budget bound
changed (`git diff --name-only afa3ea19 da8a8b84`: nine files, receipts/head/files-changed.txt).

## Changes (file:line — reason)

F1, the restart rule (319afb3d):
- `sw/firmware/ctrl/plat/ctrl_plat_phy.c:223-233`: `ADV_SET_LOCAL` skips the restart only where the PHY still held
  the advertisement as read before the writes, and never at boot; `ADV_RESTART` clears only the boot flag. The
  `RESTARTED` flag is gone, so a repair of a dropped write always restarts. `:234-240` (`ADV_CHECK_GIG`) unchanged:
  verified on read-back, else still owed, and the next poll writes and restarts again.
  Reason: IEEE 802.3 28.2.4.1.3 (a changed advertisement takes effect by renegotiation); #840 (no 100 Mb/s link).
  The no-loop property holds by the pre-write read: a restart's own latched loss finds the advertisement held.
- `sw/firmware/ctrl/plat/ctrl_plat_phy.h:43-51` THE ADVERTISEMENT restated (restart after every repairing write,
  at boot always, no restart where held, a PHY that never takes a write restarted at each try); `:62-64` THE STEP
  (six reads 15, 4, 9, 0, 4, 9 and three writes 9, 4, 0, 64 bit periods, the restart's write omitted where held:
  R852-F2); `:178-179` the flags, OWED and BOOT only.
- `sw/firmware/ctrl/test/phy_peer.hpp:62-63,159,166-174`: the negotiation latch. With `negotiates`, a restart
  latches registers 4 and 9 as the abilities in force (`active_anar`, `active_gctrl`) and resolves the link
  against the partner's registers 5 and 10 (1000BASE-T by 40.5.1.1's shift, else the best common 10/100 mode),
  so the registers and the negotiation are separate.
- `sw/firmware/ctrl/test/test_plat_phy.cpp:586-620` P15 restated: each try writes and restarts again, until the
  read-back holds, then neither. `:658-707` P17 new (the reviewers' case), at boot and after a loss.
- `sw/firmware/ctrl/test/plat_mutants.py:313-318` REPAIR / RESTARTED_EARLY; `:379` the plant
  `plat-phy-restarted-before-verified` replaces `plat-phy-restart-each-poll` (whose rule was the defect).
- `sw/firmware/ctrl/plat/README.md:92-94,137,141-142`: the rule, THE STEP's counts, the tests and the plants.

R851-F2 (5c2682a4):
- `sw/firmware/ctrl/test/test_plat_phy.cpp:550-584` P14 loops over both registers lost, register 4 alone and
  register 9 alone behind a latched loss, each three writes with the restart last and one restart, then a poll
  with no write and no restart.
- `sw/firmware/ctrl/test/plat_mutants.py:370-377` the review's m3 and m3b as plants:
  `plat-phy-lost-local-not-restarted`, `plat-phy-lost-gig-not-restarted`.
- `sw/firmware/ctrl/plat/README.md:137,141-142`: 87 defects, the PHY's 46, the advertisement's 20.

R851-F3 and R1 (c79f1c76):
- `docs/design/SPLIT_CONTROL_MEMORY.md:142-147`: the round-1 sentence ("It is 60.5 ... since the split's PHY poll
  ... refused at 61.0") removed; `:146` restated: the fixture holds 59.0 (refused at 59.5), the platform held #895's
  60.5 (refused at 61.0) until the PHY poll's merge; `:147` 61.0 since the PHY poll, refused at 61.5. One history:
  60.0 (`:142`), 60.5 by #895 (`:145`), 61.0 by #919/#840 (`:147`). Reread against `ctrl_memory.LEDGERED`
  (`sw/litex/ctrl_memory.py:273` 61.0 and `:288` 56.5) and section 5 (`:276`, `:282`, `:402`): they agree.
- `sw/litex/ctrl_memory.py:237-238,255`: the comment's issue-comment ID and lane name replaced by the decision and
  issue (R1). The entries' reason strings were left as data (R851-R1 lets the manager carry them).

Figures (da8a8b84), measured at c79f1c76 on a clean clone (receipts/measure/):
- `ctrl_plat_phy.h:191-192`, `tb/verilator/ctrl_split_boot/README.md:97-103`: the frame's cost and the boot's
  figures at this head; `CTRL_PLAT_PHY_STEP_US` stays 155 (145.45 us x 1.05 = 152.7, up to 155).
- `sw/firmware/ctrl/plat/README.md:127,129`, `docs/design/SPLIT_CONTROL_MEMORY.md:147-148,399-409`,
  `sw/litex/ctrl_memory.py:285,292`: rom 8 B less at every point; RAMB36 and ctrl_plat unchanged.

## New checks (planted defect — failing words)

| Defect | Caught by — words |
|---|---|
| plat-phy-restarted-before-verified (the round-2 rule: the restart marked taken at the restart, before the read-back) | PlatPhy.P17 — "P17 the active advertisement is 1000BASE-T only"; also P15 — "P15 and negotiation restarts after every repaired write" |
| plat-phy-lost-local-not-restarted (R851's m3) | PlatPhy.P14 — "P14 a PHY that lost the advertisement is written and restarted once, register 4 alone" |
| plat-phy-lost-gig-not-restarted (R851's m3b) | PlatPhy.P14 — "P14 a PHY that lost the advertisement is written and restarted once, register 9 alone" |
| (kept) plat-phy-reset-phy-not-restarted | PlatPhy.P14 — "P14 a PHY that lost the advertisement is written and restarted" (both registers, the first case) |
| (removed) plat-phy-restart-each-poll | its rule, one restart a time owed, was the defect F1 names |

The reviewers' own probes at da8a8b84, run from copies under scratch (receipts/probes/):
- R852's retry probe: rc 0; fault case `register4=0001 advertised-at-last-restart=0001 active-Mbps=0 restarts=2`;
  control `restarts=1`.
- R851's retry_probe.sh: rc 0, 18 of 18; `register4=0001 advertised-at-last-restart=0001 restarts=2 adv-owed=0`.
- R851's mutants.sh: m1, m2, m3, m3b, m4, m5, m7, m8 caught (m3 and m3b by P14 on the words above); m6 survives,
  the review's equivalent mutant (-1 reads as all ones).

## Gate table

| Gate | Command | Head | rc | Receipt |
|---|---|---|---|---|
| Workflow jobs rtl-fast, elaborate, docs | run_wf.py per job, fresh clone each; verify_wf.py with round 3's job reasons | da8a8b84 | 0 | workflows/verify-da8a8b84.md: 89 steps rc 0, 159 not run with a reason (29 of them jobs this round does not touch, each rc 0 at afa3ea19), 0 bad |
| Firmware suites | firmware-unit's test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4, ctrl_nvm | da8a8b84 | 0 | workflows/logs/rtl-fast__firmware-unit__ci_step_10.log: test_ctrl_firmware: PASS |
| Coverage ratchet | fw_coverage.py --selftest, --check | da8a8b84 (and c79f1c76) | 0 | ci_step_12.log: ctrl_plat_phy.c 172/172 158/158, PASS (40 files); measure/fw-coverage-check-c79f1c76.log |
| Control campaign | firmware-control-mutants | da8a8b84 | 0 | ci_step_9.log: mutants: 762 of 762 caught; the four restart plants on their words |
| Boundary, Verilator builders | firmware-boundary, firmware-verilator | da8a8b84 | 0 | workflows/logs |
| Elaborate | elaborate-gates-0, elaborate-gates-1, elaborate (product LiteX venv) | da8a8b84 | 0 | workflows/logs |
| Docs | docs.yml's six jobs | da8a8b84 | 0 | workflows/logs; docs-check-no-git's runner traceback after its steps is the job's own git strip (workflows/README.md) |
| Split boot simulation 1x1/1if | run.py | da8a8b84 (and c79f1c76) | 0 | boot/boot-1x1-da8a8b84.log: 59 frames, longest 14,537 cycles, 145.37 us |
| Split boot simulation 8x8/1if | run.py --shape endstation_ax7101_8x8 | da8a8b84 (and c79f1c76) | 0 | boot/boot-8x8-da8a8b84.log: longest 14,545 cycles, 145.45 us |
| Split boot self-test | run.py --self-test | da8a8b84 | 0 | boot/boot-self-test-da8a8b84.log: 6/6 native, 6/6 plants, 8/8 placement |
| Platform ledger self-test | plat_ledger.py --self-test | da8a8b84 (and c79f1c76) | 0 | boot/plat-ledger-self-test-da8a8b84.log: 4 points PASS, 8/8 controls |
| Memory test | sw/litex/test_ctrl_memory.py | da8a8b84 | 0 | boot/test-ctrl-memory-da8a8b84.log: 0 failures |
| R852-1's retry probe and control | its retry_probe.py, from a scratch copy | da8a8b84 | 0, 0 | probes/r852-*.log |
| R851-1's retry_probe.sh, mutants.sh | from scratch copies | da8a8b84 | 0; m3, m3b caught | probes/r851-*.txt/.log |
| CPU budget harness image identity | harness_identity.sh (ctrl_srp_image.py, both shapes) | da8a8b84 | identical | budget/harness-image-identity-da8a8b84.txt; budget/README.md: round 2's verdict stands |
| ROM banking | plat_ledger's plans, afa3ea19 vs da8a8b84 | da8a8b84 | unchanged | measure/rom-banking.txt: no route; owed to #927 |
| Release image | not rebuilt: its inputs have no diff from c805f699 (round 2, identical) | da8a8b84 | n/a | head/files-changed.txt |
| Native suite sweep | not re-run: no RTL or Verilator testbench source changed | (afa3ea19: 65 of 65) | n/a | round 2 |
| Idiom gates | scripts/check_cpp_idiom.py, check_py_idiom.py (locally before the commits, then in docs-gates-0) | da8a8b84 | 0 | workflows/logs/docs__docs-gates-0__gate_38.log, gate_39.log |

Runs used the session's own four 8-CPU slices (no range was bookable). Two queued launchers, which I believed
had exited, started a duplicate PHY subset into the same output, a redundant one on the lane, and the coverage
check on a booked range (40-47). The two redundant units were stopped by name after their commands were listed.
The subset's result was discarded (the campaign at da8a8b84 supersedes it); the coverage run, alone in its output,
is the c79f1c76 receipt.

## ROM

Platform images at da8a8b84 (afa3ea19), `rom` B, ROM banks, RAMB36 (receipts/measure/rom-banking.txt):
- 1x1/1if 119,436 (119,444), banks [64K, 32K, 16K, 4K, 2K] (same), 43.5
- 1x1/2if 121,020 (121,028), banks [64K, 32K, 16K, 8K] (same), 44.5
- 8x8/1if 132,140 (132,148), banks [128K, 2K] (same), 56.5, product entry, 980 B left
- 8x8/2if 133,708 (133,716), banks [128K, 4K] (same), 61.0, its entry, 1,460 B left
The banks are round 2's at every point, so the gateware the routes at c805f699 placed is this head's in structure;
no route was repeated, and timing stays recorded as owed to #927 with round 2's figures.
By file (receipts/measure/rom-per-file.txt): ctrl_plat_phy.o 1,883 -> 1,875 B; nothing else changed.

## Open risks / questions

- The restart's own write (register 0) is not read back: its restart bit clears itself (22.2.4.1.7), so a dropped
  restart write is not seen and the advertisement then reads back while the PHY keeps its earlier negotiation. The
  release's init has the same property. Not changed here (fix exactly); disclosed in the PR body. A new issue if
  wanted.
- A PHY that never takes the writes is restarted every poll (125 ms) and so never links; #840 wants no link other
  than 1000BASE-T. Stated in the header and the PR body.
- `sw/firmware/gtest/coverage.ratchet:30` records ctrl_plat_phy.c at 173/173 and 160/160 (round 2); this head
  measures 172/172 and 158/158, both 100 %. The check holds fractions ("fell below the recorded"), so it passes;
  the row was not rewritten (that would move the head after the gates, and `--write` rewrites other lanes' rows).
- #923's lane (PR #931) implements the same product-entry mechanism; the train reconciles the two (R851-1 (4)).
