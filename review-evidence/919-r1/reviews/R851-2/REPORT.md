[R851] POSITIVE - exact head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84

Internal independent review R851-2 of issue #919 / PR #933. Tree `6a9d88680c7222514a0186e8ba8351e62b2d3514`. This is a delta review of rounds 3 and 4, from round 2's head `afa3ea19` to `1a1e6665`. It covers the code at the commits `319afb3d`, `5c2682a4`, `8beada76` and `33041d64`, and the figures at `c79f1c76`, `da8a8b84` and `1a1e6665`.

All five lenses were applied at this head. No BLOCKER, MAJOR or MINOR is open. Every prior finding is resolved at its cause. Two wording-only RESIDUE items and some optional suggestions are recorded below.

## Contents

- Identity and independence
- Findings at this head (RESIDUE, SUGGESTION)
- Prior public findings: resolved or retained
- The focus items, checked
- What this round executed
- Reviewer-owned completion ledger
- Limits
- Pending manager duties
- Packet

## Identity and independence

- **Role:** internal, cleared-context reviewer. The executor and reviewer are as published on #919. This round approves nothing of its own.
- **Order of reconstruction:**
  1. AGENTS.md and CONTRIBUTING.md.
  2. The #919 body and its comments: TAKEN, STOP, the scope addition (#840 1000BASE-T-only, issuecomment-6907491954), the timing ruling, and the three REVIEW READY comments.
  3. IEEE 802.3 clauses 22, 28 and 40 as the code cites them.
  4. `git diff afa3ea19..1a1e6665` and its history.
  5. The author packets `author-r3` and `author-r4` from evidence archive `d8bc5057`.
- **Prior findings:** the two prior public reviews (R851-1 issuecomment-6930496445, R852-1 issuecomment-6929889363) were fetched only after this round's own pass over the diff, its campaign and its probes.
- **Not read:** no private author material, no lane scratchpad, nothing under the management tree, no other reviewer's report of this round, and not the archive's `reviews/` directory.
- **No changes made:** no source was changed and nothing was written to GitHub.

## Findings at this head

### R851-2-R1 - RESIDUE - Docs - THE OUTCOME's prose says every completed sub-gigabit link is a dropped restart; a PHY that links below 1000 Mb/s on its own is restarted at each such link, and that is not stated

- **Artifacts:**
  - `sw/firmware/ctrl/plat/ctrl_plat_phy.h:56-58`: "...while the advertisement is verified, is that earlier negotiation."
  - `sw/firmware/ctrl/plat/README.md:93`: the same sentence.
  - The PR body, "Known limitations": it covers "a PHY that never takes the writes" but not this case.
- **Evidence:** the check at `ctrl_plat_phy.c:257-262` cannot tell a dropped restart from a PHY that completes a link below 1000 Mb/s while the gigabit-only advertisement is in force. That happens with a PHY that downshifts, or with parallel detection of a partner that does not autonegotiate, where the PHY implements it so.
  - This round's probe `RvProbeParallelDetectLoopTimed` (`receipts/reviewer_probes_summary.txt`) models a restart that drops the link and a sub-gigabit link back about 1 s later.
  - Result: 90 polls (11.25 s), `restarts=9 renegotiations=9`, nothing below 1000 Mb/s published, final word 0. That is one counted restart per sub-gigabit link-up, paced by the poll, without end.
  - The untimed variant gives exactly one restart a poll (20 in 20). That confirms the header's "at most once a poll".
  - The author's round-4 REVIEW READY discloses the downshift case as an open risk. The authoritative docs and the PR body do not.
- **Why RESIDUE:** the behaviour is consistent with #840's stated outcome, no link for a partner or PHY without 1000BASE-T. It also tears down the PHY-level 100 Mb/s link "the MAC is silent on", which #840 exists to prevent. So no code, test or figure change is required. The defect is that the prose misdescribes what the check judges.
- **Exact fix:**
  - At `ctrl_plat_phy.h:58` and `README.md:93`, replace "is that earlier negotiation" with "is taken for that earlier negotiation; a PHY that itself links below 1000 Mb/s against the advertisement in force (a downshift, or parallel detection of a partner that does not autonegotiate) is judged the same way: restarted once each such link completes, counted, and never published up".
  - Add the same sentence as a bullet under the PR body's "Known limitations".
- **Effect:** none on any lens or on the verdict.

### R851-2-R2 - RESIDUE - Docs - "a link the PHY formed before the restart is never published" does not hold when register 4's write and the restart are both lost

- **Artifacts:**
  - `sw/firmware/ctrl/plat/ctrl_plat_phy.h:38-40`: "(so a link the PHY formed before the restart is never published)".
  - `sw/firmware/ctrl/plat/README.md:92`: the same claim.
- **Evidence:** in probe `RvProbeBothLostAtBoot`, a 100 Mb/s link is in force before boot, and the boot loses both register 4's write and the restart. The boot poll publishes `11` (100 Mb/s full duplex, up). The next poll repairs and restarts, publishes `0`, and the link never returns at 100.
  - So the earlier link is published for one poll period (125 ms), only under a double MDIO write loss.
  - The release would publish it until the next physical loss. With either loss alone, nothing below 1000 is published: P18's `below_gigabit` checks pass, and so do the probes `RvProbeRepairThenRestartLost` and `RvProbeSlowRestart`.
  - This sentence predates the delta. Round 4's THE OUTCOME is what now carries the single-loss half of the claim, so it is recorded here.
- **Exact fix:** at both places, append "unless the PHY also lost the advertisement's own write, when the earlier link is published until the next poll repairs it".
- **Effect:** none on any lens or on the verdict.

### Suggestions (optional; they affect no lens)

- **S1 - Robustness - `ctrl_plat_phy.c:257-262`.** If the restart per sub-gigabit link in R851-2-R1 is not wanted, two changes would separate a dropped restart from a PHY that links below 1000 Mb/s on its own:
  - Read ANER (register 6) bit 0, "link partner autonegotiation able", which is clear after parallel detection.
  - Bound THE OUTCOME to one restart per loss. A second sub-gigabit completion after the outcome's own restart is then not a dropped write.
  - Either costs one read frame. The manager may instead record the paced, counted restart as accepted. This round sees no harm to the Milan function: no link is published either way.
- **S2 - RTL - `ctrl_plat_phy.c:117-124`.** `publish()` sets `adv = CTRL_PLAT_PHY_ADV_OWED` on a loss and so drops a pending `CTRL_PLAT_PHY_ADV_RENEGOTIATE`. That only happens when THE OUTCOME fires in a poll whose final word is a loss, which a conformant PHY cannot produce, because a speed change latches a loss first. Even then the effect is one poll's delay and a second count. `phy->adv |= CTRL_PLAT_PHY_ADV_OWED` would keep the bit, and the `NONE` path re-reads ability either way.
- **S3 - Robustness - `ctrl_plat_phy.h:250`.** `renegotiations` is not exposed by the console or any status word. A bench or field reader therefore cannot see the restarts in R851-2-R1. Adding it to `milan_status` would make the count usable.
- **S4 - Tests - `test_plat_phy.cpp:681-694`.** The pin-level peer negotiates the moment the restart is written. So P17's boot poll publishes the dropped write's 100 Mb/s link for one period: this round's probe `RvProbeRepairThenRestartLost` sees one publication below 1000 at boot. A real PHY needs well over a poll period to negotiate. A comment there, or a peer delay option, would stop a later reader taking that publication for intended behaviour.
- **Retained from R851-1:** S1 (the spin's `CYCLES_HALF` fallback is not bounded by `CTRL_PLAT_PHY_STEP_US`), S2 (a split export without the PHY rows arms nothing, silently) and S3 (the store-step wording of ruling 6899740728 item 4). The code they name is unchanged by the delta, and they stay optional.

## Prior public findings: resolved or retained

| Prior finding | Status at 1a1e6665 | Evidence |
|---|---|---|
| R851-F1 = R852-F1, MAJOR: a repaired advertisement is not renegotiated | **Resolved** | See below the table. |
| R851-F2, MINOR: after-loss restart graded only with both registers lost | **Resolved** | See below the table. |
| R851-F3, MINOR: the fit page's section 3 gave two histories | **Resolved** | `SPLIT_CONTROL_MEMORY.md:142` 60.0, `:145` 60.5 by #895, `:146` "held #895's cap, 60.5, refused at 61.0, until the PHY poll's merge", `:147` 61.0 by #919/#840, refused at 61.5. The round-1 sentence is gone. This agrees with `ctrl_memory.py` LEDGERED (61.0, 56.5) and section 5 (`:276`, `:282`, `:402`). |
| R851-F4 = R852-F2, MINOR: frame and work counts | **Resolved** | `ctrl_plat_phy.h:75-81` and `README.md:94` now say six reads (15, 4, 9, 0, 4, 9), three writes (9, 4, 0) and 64 bit periods (`CTRL_PLAT_PHY_FRAME_BITS`). Recounted against the stage enum `ctrl_plat_phy.h:229-237`. No "65 bit" or "seven reads" remains in any tracked doc or source of the lane. |
| R851-R1 = R852-R1, RESIDUE: comment labels | **Resolved in comments** | `ctrl_memory.py:237` now reads "(`product_point`, #919 and #923)", and `:255` reads "until the hybrid XIP work (#665 decision D3)". The entries' reason strings (`:283-295`) still carry an issue-comment ID. They are data in the base's pattern, as R851-1 recorded, and go to the residue checklist. No label appears in any added line of the delta's code, tests or scripts (searched `^+` lines for lane, reviewer, round and issue-comment patterns). |

**R851-F1 = R852-F1** is resolved by four pieces of evidence:
- The code: `ctrl_plat_phy.c:228-237`. Any write that finds registers 4 and 9 not gigabit-only restarts. `RENEGOTIATE` is cleared only by the restart write. The old `RESTARTED` flag is gone.
- The tests: P17 (`test_plat_phy.cpp:681-716`), whose peer latches the abilities in force at each restart, and P15 (`:593-627`), which requires one restart per repaired try.
- This round's harder variant, `RvProbeRepairThenRestartLost`: register 4 is dropped at boot, then the repair's own restart is lost too. Result: `restarts=2 renegotiations=2 active=0 anar=0001 adv=0 word=0`, so the advertisement in force is gigabit-only and there is no link at 100.
- The author's runs of both reviews' retry probes: `author-r4/receipts/probes/`, 21 of 21, `advertised-at-last-restart=0001`.

**R851-F2** is resolved by P14's three cases (`test_plat_phy.cpp:567-589`: both registers, register 4 alone, register 9 alone). This round's campaign catches the plants `plat-phy-lost-local-not-restarted` and `plat-phy-lost-gig-not-restarted` by "P14 ... register 4 alone" and "... register 9 alone" (`receipts/phy_arms_and_plants.log`). Those are R851-1's m3 and m3b. The author's renamed-anchor copy of R851-1's `mutants.sh` catches m3, m3b and m8, with m6 still the equivalent mutant (`author-r4/receipts/probes/r851-mutants-1a1e6665.txt`).

## The focus items, checked

1. **F1, the restart after every repair.** Covered in the table above.
   - The pin-level peer (`phy_peer.hpp:156-183`) keeps the abilities in force (`active_anar`, `active_gctrl`, `active_speed`) apart from the registers.
   - The reviewer's case (register 4 dropped on the first poll, a 100BASE-TX-only partner) ends with no link. The plant `plat-phy-restarted-before-verified` is caught by P17's and P15's words.
2. **Round 4, THE OUTCOME** (`ctrl_plat_phy.c:233-238` and `:255-262`; header `:51-67`). 22.2.4.1.7 is correctly cited for the self-clearing restart bit, and 40.5.1.1 for register 9's bits 9:8 against register 10's 11:10 (`<< 2`).
   - The check fires only when all of these hold:
     - negotiation is complete (BMSR bit 5) and the link is up;
     - autonegotiation is enabled;
     - the extended status shows 1000BASE-T ability;
     - registers 9 and 10 share no 1000BASE-T mode;
     - the advertisement is verified (`adv == 0`).
   - The link is then resolved from registers 4 and 5, which share nothing below 1000 Mb/s, so it is published down, and the next poll restarts, counted, with the count saturating at 0xffff.
   - The P18 tests pass. `plat-phy-outcome-unchecked` is caught by "P18 no link at 100 after recovery" (in the `also` list) and first fails on "P18 the outcome's restart is counted". All seven outcome plants are caught by name.
   - **Restart loop against a partner without 1000BASE-T:**
     - An autonegotiating 100-only partner gives no link up, so no outcome fires and there is no loop. P18 shows "none follows", and the probe `RvProbeSlowRestart` shows one extra restart at most, then none.
     - A PHY that links below 1000 Mb/s on its own (a downshift, or parallel detection) gets one paced, counted restart per such link and nothing published (R851-2-R1, S1).
   - **A link left up at 100:** none after recovery in any probe. The double-loss case publishes one poll period's worth (R851-2-R2).
   - **Forced mode:** a PHY in forced 100 Mb/s whose restart write is lost is published at 100, `word=11`, with no restart (`RvProbeForcedModeRestartLost`). That is the stated KNOWN item, not a finding.
3. **F2.** See the table above.
4. **F3, F4 and R1.** See the table above.
5. **Figures:**
   - **Frame cost:** at most 14,537 CPU cycles (145.37 us) at 1x1/1if and 14,545 (145.45 us) at 8x8/1if, against 155 us. Read from `author-r4/receipts/boot/boot-{1x1,8x8}-1a1e6665.log:25`. 145.45 x 1.05 = 152.7, so 155 holds.
   - **ROM:** 119,500 / 121,084 / 132,204 / 133,772 B at 43.5 / 44.5 / 56.5 / 61.0 RAMB36.
     - That is +64 B against round 3 and +56 B against round 2, all in `ctrl_plat_phy.o` (1,875 to 1,939 B).
     - The banks, tiles and `ctrl_plat` are unchanged (`measure/rom-banking.txt`, `measure/rom-per-file.txt`).
     - 916 B are left at 8x8/1if and 1,396 B at 8x8/2if. Rechecked: 133,120 - 132,204 and 135,168 - 133,772.
     - The page figures (`SPLIT_CONTROL_MEMORY.md:147-148`, `:399-409`) agree: 652 B past 60.5 and 1,132 B past 56.0.
   - **The counter:** `renegotiations` takes the struct's existing padding after six one-byte fields (`ctrl_plat_phy.h:244-251`), so there is no size change.
   - **CPU budget harness images:** byte-identical to round 2's and the base's at both shapes (`budget/harness-image-identity-1a1e6665.txt`: `10684d74...` and `2cf4e51a...`, porcelain 0).
   - **Ratchet:** `coverage.ratchet:30` reads 178/178 and 164/164, which this round measured independently.
6. **Gates:**
   - **Workflow steps:** 89 rc files, all 0, all logs headed `1a1e6665`. Verified by `receipts/author_r4_index_verify.txt`.
   - **Archive integrity:** every r3 and r4 file matches the archive's `MANIFEST.json` published sha256 (477 rows, 0 mismatches). The four logs whose bytes differ from the author INDEX are recorded there as path-redacted, with original hashes equal to the INDEX's (`receipts/archive_manifest_verify.txt`).
   - **Control campaign:** 769 of 769 (`rtl-fast__firmware-control-mutants__ci_step_9`).
   - **Firmware unit and coverage:** `test_ctrl_firmware: PASS` and `firmware coverage: PASS (40 files)`.
   - **Boot simulation:** PASS at both shapes (`boot/`). Its self-test catches 6/6 plants, the renamed-anchor `phy-unadvertised` among them. The ledger self-test passes four points.

## What this round executed

All runs used disposable copies under the packet's scratch; `receipts/commands.txt` lists each command.

- **Unit arms:** the PHY and boot unit arms (`platboot`) at one and two interfaces: 36 of 36 tests each, PASS.
- **Plant campaign:** the control campaign restricted to the 49 `plat-phy-*` plants: **49 of 49 caught by their named test and words**, rc 0 (`receipts/phy_arms_and_plants.log`).
- **Coverage check:** `fw_coverage.py --check` on a pristine copy, rc 0. It gives `ctrl_plat_phy.c 178/178 164/164` and `firmware coverage: PASS (40 files)` (`receipts/fw_coverage_check.log`).
- **Probes:** six reviewer probes, in `scripts/reviewer_probes.cpp` and inserted by `scripts/probe.sh`. With them the `platboot` arms ran 42 of 42 at both shapes, rc 0 (`receipts/reviewer_probes.log`, `receipts/reviewer_probes_summary.txt`):

| Probe | Result |
|---|---|
| `RvProbeParallelDetectLoop` | `restarts=20` in 20 polls, `below_gig=0` |
| `RvProbeParallelDetectLoopTimed` | `restarts=9` in 90 polls, `below_gig=0`, word 0 |
| `RvProbeSlowRestart` | 1 extra restart, then none; no link at 100 |
| `RvProbeRepairThenRestartLost` | recovers; anar 0001, active 0, word 0 |
| `RvProbeBothLostAtBoot` | boot publishes `11` once, then `0` thereafter |
| `RvProbeForcedModeRestartLost` | `word=11`, no restart (KNOWN) |

- **Evidence checks:** the archive `d8bc5057` was fetched into a separate bare repository and checked against its `MANIFEST.json` and the author INDEX (`scripts/verify_index.py`, `scripts/verify_manifest.py`).
- **Clone integrity:** the review clone is unchanged: index and tree agree, porcelain shows 0 lines, and the gitlinks are as at start (`receipts/clone_integrity.txt`).

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `ctrl_plat_phy.c:117-285` against IEEE 802.3 22.2.4.1.7 (self-clearing restart), 28.2.4.1.3 (a changed advertisement renegotiated), 40.5.1.1 (registers 9/10), 22.2.4.5 (64-bit frame); the #840 scope addition 6907491954 (written and verified at boot and after every loss); P17/P18 outcomes; `RvProbeRepairThenRestartLost` | R851-2 | 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| RTL | CLEAN | firmware FSM `ctrl_plat_phy.c:129-285` (adv bit states OWED/RENEGOTIATE/NONE, `resume = CURRENT` after a restart, saturating `uint16_t` counter, `(uint8_t)~` mask), struct layout `ctrl_plat_phy.h:240-258` (padding, no size change), stage enum `:217-238`; `git diff afa3ea19..1a1e6665 -- hdl sw/firmware/ctrl/mbx tb/verilator/ctrl_service_budget tb/verilator/fw_service_budget sw/firmware/milan_baremetal` empty; S2 optional | R851-2 | 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| Robustness | CLEAN | dropped register-4 write, dropped restart once and three times, both lost, slow restart, sub-gigabit link on its own (untimed and timed), forced mode, count saturation, 10/100 and 1000-half-only PHYs: P13-P18 and the six probes in `receipts/reviewer_probes_summary.txt`; R2 and S1/S3 recorded | R851-2 | 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| Tests | CLEAN | `test_plat_phy.cpp:557-842` (P14 three cases, P15, P17, P18 three tests), `phy_peer.hpp:15-27,61-69,156-183`, `plat_mutants.py:309-419`; this round's 49 of 49 PHY plants by name, coverage 178/178 lines and 164/164 branches (`receipts/fw_coverage_check.log`), `coverage.ratchet:30`; author receipt 769 of 769; S4 optional | R851-2 | 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| Docs | CLEAN (R1, R2 residue) | `ctrl_plat_phy.h:28-81`, `plat/README.md:92-94`, `SPLIT_CONTROL_MEMORY.md:136-149,276-282,395-409`, `ctrl_split_boot/README.md:95-104` against `author-r4/receipts/boot/*.log`, `ctrl_memory.py:234-295`, `tb/verilator/ctrl_split_boot/run.py:133-135`, PR body (known limitations), REVIEW READY issuecomment-6934522568 | R851-2 | 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |

All five lenses are covered clean at the exact head. That is one internal positive. CONTRIBUTING.md still requires the external review's own positive at this head.

## Limits

- **Boot simulation:** not run by this round. This host has no RV32 cross-compiler. Its figures rest on the author's receipts at `1a1e6665`, which were checked for head, index and manifest integrity and spot-checked against `ctrl_split_boot/README.md:97-103`.
- **Workflow jobs and full control campaign:** the 89 workflow steps and the full 769-plant campaign were not re-run. This round verified their receipts and re-ran only the PHY plants, the PHY and boot unit arms, and the coverage check.
- **Hosted runs:** hosted exact-head CI was not inspected. The manager owns hosted and act acceptance.
- **No manager source bank** runs at this head, and none is claimed or inferred.
- **Physical evidence:** physical calibration was NOT RUN, and field skips are not hardware proof. The bench acceptance (tap link-flap, gPTP resume within 5 s) is the gating run's.
- **The probes' PHY:** the probes model a PHY that links below 1000 Mb/s on its own, and a slow restart, by setting peer registers between polls. They are not a model of any specific PHY's downshift or parallel-detection timing.
- **KNOWN items, not assessed as findings:** the timing floor (#818's, best of three; #665 issuecomment-6930885185), the release firmware's same restart gap, and a PHY in forced mode before boot.

## Pending manager duties

- Carry R851-2-R1 and R851-2-R2, with their exact fixes, and the remaining ledger reason strings of R851-R1/R852-R1 (`ctrl_memory.py:283-295`), to the residue checklist.
- Optionally record whether the paced, counted restart for each sub-gigabit link a PHY forms on its own (R851-2-R1, S1) is accepted as is.
- Validate the current-dev merge candidate (source base `659d7687`, live dev `6b66f66d`) with the builder and native banks at the merge turn, and link those receipts.
- Hosted exact-head acceptance, the external review's verdict at this head, and the gating run's bench features.

## Packet

`REPORT.md`, `scripts/` (`run_phy.py`, `probe.sh`, `reviewer_probes.cpp`, `verify_index.py`, `verify_manifest.py`) and `receipts/`. Every published file is listed in `MANIFEST.sha256`. Host paths are written as `<packet>`, `<clone>` and `<home>`.

R851-2 FINISHED
