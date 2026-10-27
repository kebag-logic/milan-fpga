# [A688b] HANDOFF: PR #92 round 2 (R719-1 F1/F2/F3/R1, R720-1 F1/F2)

Status: REVIEW READY at `4d8fb9024c7ed4ce4b6e70912721c3cfb03e729e`. Every repository gate is rc 0 at this head. With the regenerated parent companion change, every parent consumer gate is rc 0, including both milan_dp gPTP legs, both idiom gates and tsn_fuzz `ptp`. The companion change is not committed upstream from this lane, so the PR body does not use closing keywords.

- Repository: Mister-M-alt/FPGA-gPTP, branch `89-90-91-srto-pdelay` (local only, not pushed)
- Base: `55680bff3b287b9a7b0c759f51471fa617c17335` (main)
- Round-1 head: `d27a1654285614ded5093cb58f58bceed551fdae`
- Round-2 head: `4d8fb9024c7ed4ce4b6e70912721c3cfb03e729e`
- Round-2 commits (one-line subjects, no body, no trailers):
  - `dd37df8` Mark the port on every sync receipt timeout, age only with gmPresent, and keep both Sync watches across mastership (#89)
  - `91d26df` Move the receipt-rule controls to their own module and plant a failing control for each new receipt check
  - `4d8fb90` Document master-role ageing, the kept Follow_Up watch and the gmPresent condition, and name sync-ok in the handover bullet
- Issue #90: TAKEN at comment 6442878190; `[A688b] REVIEW READY 4d8fb9024c7ed4ce4b6e70912721c3cfb03e729e` at comment 6448529102.
- No top-level port, parameter or register-map change, and no RTL file change. The parser and the engine top are untouched.

## What round 2 changes (IEEE 802.1AS-2011 with Cor1 and Cor2)

### R719-1 F1: an expiry found in the master role is not forgotten

- 10.3.11, Figure 10-13 (Cor1): CURRENT goes to AGED whenever `currentTime >= syncReceiptTimeoutTime && gmPresent`. Figure 10-4 (Cor1) moves syncReceiptTimeoutTime on a received Sync only. So the role the port held when the time passed does not matter.
- Every slot-4 expiry now writes the aged mark (`S_SRTO = SRTO_PASSED_C`), whatever role it finds. Round 1 recorded the role and treated only the slave value as aged.
- BECOME no longer stops the Sync receipt watch (slot 4). Mastership won by an Announce lapse (or by our own vector winning) therefore still ages the port when Sync stops.
- The no-oscillation rule of the round-1 assignment now holds for "one pair, then Sync dies again": that pair restarts the watch, its expiry marks the port again, and the next Announce is aged at once. Automatic recovery is unchanged: the first usable pair clears the mark.

### R719-1 F2: a pending Sync keeps its 125 ms Follow_Up watch across BECOME

- BECOME no longer stops slot 5. A Sync parked before the takeover is voided by its own followUpReceiptTimeout (11.2.13 MDSyncReceive; Milan v1.2 Table 4.2: 125 ms), so a later Follow_Up pairs with nothing in the master role.
- A Follow_Up inside the 125 ms that lands after the takeover is still a usable pair, heard as master. That matches 802.1AS-2011: the pair completes inside followUpReceiptTimeout and refreshes syncReceiptTimeoutTime.

### R720-1 F1: ageing honours gmPresent exactly

- gmPresent is TRUE only while the priority1 of the gmPriorityVector's rootSystemIdentity is below 255 (802.1AS-2011 10.2.3.13; 10.3.12.1.4 g, restated by Cor1).
- Expiry: an elected peer is aged (BECGATE, then BECOME) only when its grandmaster's priority1 is below 255. A slave of a priority1 255 grandmaster stays elected.
- Announce on an aged port: it is aged at once only when its grandmaster's priority1 is below 255, which is exactly when gmPresent would be TRUE with it elected. A priority1 255 grandmaster competes as usual. An aged Announce now goes to BECGATE, which leaves a master as it is and makes a slave of a priority1 255 grandmaster master at once, as 10.3.11 does.
- One compare decides both: `SRTO_PASSED_C = 0xFF << 16`. A vector's {priority1, clockClass, clockAccuracy}, bits 63:40 as S_BESTPV and BTCA hold it, compares below it exactly when its priority1 is below 255. The cell is zero when not aged.
- The published flags bit 0 keeps its #82 meaning (a peer is elected, or thisClock is grandmaster-capable). Only the ageing decision changed.

### R719-1 R1 and R720-1 F2 (residue, applied as written)

- `docs/TEST_DEVELOPER.md:132` now reads "- Clears sync-ok on every handover to a peer." (option 1 of both findings; the line keeps its place).

### R719-1 F3: parent companion patch

- Regenerated from the scratch parent snapshot; see "Parent companion change" below.

## Changes (file:line at `4d8fb902`)

`hdl/ucode/gen_gptp_ucode.py`
- `:10`, `:20`: module notes for the round-2 rules.
- `:419` `S_SRTO = 46`: now holds `SRTO_PASSED_C` or zero, with its invariant.
- `:504` `SRTO_PASSED_C = 0xFF << 16`: the gmPresent threshold and the aged mark.
- `:868` `prog_rx_sync`: the asCapable gate branches out on the clear bit (4 words instead of `e_flag_gate`'s 5), the word the receipt rules spend. Behaviour unchanged.
- `:891` `prog_rx_followup` docstring: a master's pair also clears the aged mark.
- `:1092`..`:1101` `prog_rx_announce`: the aged-mark gate moved after the qualification and the raw publication, compares the Announce's {priority1, clockClass, clockAccuracy} with `S_SRTO`, and branches to BECGATE. Round 1's role compare is gone.
- `:1885` `prog_become`: the slot-4 and slot-5 disarms are removed, with the reason.
- `:2138`..`:2169` `prog_leg_srto`: writes the mark on every expiry, then BECGATE only for an elected peer with gmPresent (branch-free: the presence bit less one, OR-ed into the elected vector's bits 63:40, compared with `SRTO_PASSED_C`).
- The four tracked images are regenerated with each Makefile's arguments.

ROM: shipping 1,021 of 1,024 words (round 1: 1,018; main: 1,015), three free; seeded regression images 1,022. SRTO +5, the Announce gate +1, BECOME -2, the Sync gate -1.

`tb/verilator/engine/sim_main.cpp`: 1,805 shipping checks (round 1: 1,799) and 57 in the priority1 255 pass (round 1: 53).
- `:190`, `:197` header entries for phases 40 and 41.
- `:4006` phase 21: phase 19's queued receipt timeout now leaves the port aged, so the grandmaster's Announce before Sync elects nothing (new check `:4008`), its Sync is heard as master, and the next Announce re-adopts it.
- `:5354` phase 36: one Announce inside D's Sync watch, so the asCapable gate alone is what refuses it (once the watch runs out the aged mark refuses D too).
- `:5612` `return_to_gms`, `:5624` `outlive_mastership_with_the_sync_watch`, `:5645` `park_a_sync_across_the_takeover`.
- `:5682` phase 40 `age_the_port_whatever_role_the_timeout_finds` (shipping passes, run at `:399` before the whole-run grades).
- `:5718` phase 41 `age_only_while_a_grandmaster_is_present` (priority1 255 pass, run at `:307`).
- The anchors both reviewer probes plant at are unchanged, so both run unchanged.

`tb/verilator/engine/mutants.py` (836 lines) and new `tb/verilator/engine/receipt_mutants.py` (285 lines): the #89-#91 controls moved to their own data module, keeping the arm under the parent's 1,000-line module ratchet. 98 controls (round 1: 91).
- New: `:68` only an expiry that ages a slave marks the port; `:97` sync receipt ageing ignores gmPresent; `:128` an aged port refuses a priority1 255 grandmaster; `:135` an aged Announce is dropped rather than aged; `:145` mastership stops the Sync receipt watch; `:151` mastership stops the Follow_Up watch; `:156` mastership voids the parked Sync.
- Repaired for the new code: `:26` a queued receipt timeout ages a master; `:42` a sync receipt timeout only clears sync-ok; `:112` an aged port takes Announces (and it now also names a phase-41 check); `:173` a master hears no Sync (word-neutral: the Follow_Up role gate admits the slave alone; it now also names a phase-40 check); `mutants.py:506` a queued receipt timeout clears a master's sync-ok (word-neutral; its two words come from the priority1 read, an incidental defect only the priority1 255 pass sees).

Docs:
- `docs/INTEGRATION.md:603`..`:637`: the watch belongs to the port; master-role expiry; the kept Follow_Up watch; gmPresent.
- `docs/HDL_DEVELOPER.md:194`..`:212`: the receipt state.
- `docs/TEST_DEVELOPER.md:125`..`:132`: suite responsibilities; the handover bullet.
- `docs/MANAGER.md:103`, `:107`, `:117`: ROM 1,021, three free, `FUTO@254`.
- `docs/SOURCE_EVIDENCE.md:31` slew anchor `#L984`; `:39`, `:40` two requirement rows.

## New checks, their controls and failing words

Every round-2 check is failed by at least one planted control, through the arm's own named verdict. Both tables are generated from `receipts/repo-gates-head/04b-engine-mutants.log` (`receipts/coverage/coverage-map.md`, `receipts/coverage/mutant-table.md`).

| New check | Controls that fail it |
|---|---|
| #89 takeover: the queued receipt timeout leaves the port aged | only an expiry that ages a slave marks the port |
| #89 a lone pair heard as master: a later Announce elects nothing | only an expiry that ages a slave marks the port |
| #89 a lone pair heard as master: an Announce inside its watch elects the grandmaster | a master hears no Sync |
| #89 Announce lapse: a sync receipt timeout after mastership ages the next Announce | only an expiry that ages a slave marks the port; mastership stops the Sync receipt watch |
| #89 parked Sync: a Follow_Up 200 ms after it pairs with nothing | mastership stops the Follow_Up watch |
| #89 parked Sync: a Follow_Up 60 ms after it, after the takeover, is heard | mastership voids the parked Sync |
| p1 255 #89 gmPresent: a priority1 1 Announce on the aged port elects nothing | an aged port takes Announces |
| p1 255 #89 gmPresent: the aged port elects a priority1 255 grandmaster | an aged port refuses a priority1 255 grandmaster |
| p1 255 #89 gmPresent: a priority1 255 grandmaster without Sync stays elected | sync receipt ageing ignores gmPresent |
| p1 255 #89 gmPresent: a priority1 1 Announce on the aged port makes this plane master | an aged Announce is dropped rather than aged |
| #82 Pdelay loss: Announces from the incapable port elect nothing (stimulus changed) | an incapable receipt timeout keeps the elected peer; an incapable port's Announces still compete |

| Control (new or repaired) | Verdict | Failing words (named checks, as printed) |
|---|---|---|
| only an expiry that ages a slave marks the port (the round-1 rule) | caught | #89 takeover: the queued receipt timeout leaves the port aged<br>#89 a lone pair heard as master: a later Announce elects nothing<br>#89 Announce lapse: a sync receipt timeout after mastership ages the next Announce |
| sync receipt ageing ignores gmPresent | caught | p1 255 #89 gmPresent: a priority1 255 grandmaster without Sync stays elected |
| an aged port refuses a priority1 255 grandmaster | caught | p1 255 #89 gmPresent: the aged port elects a priority1 255 grandmaster |
| an aged Announce is dropped rather than aged | caught | p1 255 #89 gmPresent: a priority1 1 Announce on the aged port makes this plane master |
| mastership stops the Sync receipt watch (round 1's BECOME) | caught | #89 Announce lapse: a sync receipt timeout after mastership ages the next Announce |
| mastership stops the Follow_Up watch (round 1's BECOME) | caught | #89 parked Sync: a Follow_Up 200 ms after it pairs with nothing |
| mastership voids the parked Sync | caught | #89 parked Sync: a Follow_Up 60 ms after it, after the takeover, is heard |
| a queued receipt timeout ages a master (repaired) | caught | #89 takeover: the queued receipt timeout ages nothing |
| a sync receipt timeout only clears sync-ok (repaired; main's leg) | caught | #89 Sync stops: the plane takes mastership<br>#89 never usable: the grandmaster is aged<br>#89 no Follow_Up / Follow_Up after the next Sync / Follow_Up with the next sequenceId: the plane takes mastership within syncReceiptTimeout and one BMCA pass |
| an aged port takes Announces (repaired) | caught | the five "#89 …: the aged port stays master while Announces continue" checks<br>p1 255 #89 gmPresent: a priority1 1 Announce on the aged port elects nothing |
| a master hears no Sync (repaired, word-neutral) | caught | #89 first grandmaster / Sync stops / no Follow_Up: the next Announce elects the grandmaster<br>#89 a lone pair heard as master: an Announce inside its watch elects the grandmaster |
| a queued receipt timeout clears a master's sync-ok (repaired, word-neutral) | caught | #84 takeover: a queued receipt timeout keeps sync-ok<br>#84 every master cycle publishes sync-ok |
| a receipt timeout unlocks the servo | caught | (plain verdict: "the servo stays locked across a Sync receipt timeout") |
| an incapable port's Announces still compete | caught | #82 Pdelay loss: Announces from the incapable port elect nothing |

Two packing notes. "a master hears no Sync" and "a queued receipt timeout clears a master's sync-ok" were made word-neutral, because the three free ROM words sit in one-word gaps and their round-1 forms no longer pack. One phase-36 control ("an incapable port's Announces still compete") survived the first parallel run, because the new mark also refuses those Announces once D's watch runs out. Phase 36 now sends one Announce inside the watch, and the control is caught.

## Reviewer probes (run unchanged at `4d8fb902`)

Script hashes match each reviewer's MANIFEST (`receipts/probes/PROBES.txt`). The reviewers' own logs at `d27a1654` are under `receipts/probes-before/` for comparison.

| Probe | At `d27a1654` (reviewer) | At `4d8fb902` |
|---|---|---|
| R719-1 `probe_reaging.sh`, late rounds 1-3 | `elected_by_announce=1` in 3 of 3, `grandmaster changes=2` | `elected_by_announce=0 commits_naming_gm=0` in 3 of 3, `grandmaster changes=0` |
| R719-1, control round (Announce 124 ms after the pair) | re-elects | re-elects (`elected_by_announce=1`) |
| R719-1, `PROBE parked` (Follow_Up 200 ms after a Sync parked 339 ms after the pair) | `elected_by_next_announce=1 commits_naming_gm=1` | `elected_by_next_announce=0 commits_naming_gm=0` |
| R720-1 `p255_probe.py` (priority1 255 peer, 6 s of Announces, no Sync) | elected, then aged within 1 s (`flags=e`) | slave of the peer throughout (`flags=5`, gm `0x…0101`); the pass's 57 checks pass |
| R720-1 `reviewer_probes.py` via its `par_mutants.py` | 7 of 9 caught | R1, R2, R4, R8, R9 caught; R3 and R7 patterns absent (that round-1 code was rewritten); R5 survives (the equivalent mutant R720-1 identified); R6 still refused by the ROM |

- In round 2 of the R719 probe, `retakeovers=1` with `grandmaster changes=0` is a completed Pdelay exchange's commit while master (PDPAIR commits every exchange), not a takeover.
- R3 adapted to the new leg (the timeout records no mark), through the same driver: caught (`receipts/probes/r3-adapted.log`). R7's target, the role-coded mark, no longer exists; its gate is covered by "an aged port takes Announces", "an aged port refuses a priority1 255 grandmaster" and "an aged Announce is dropped rather than aged".

## Parent companion change (regenerated; verified, not committed upstream)

`receipts/parent-companion-test.patch`, sha256 `b53944d52a51323b267b0a91dbfd6bd1aeaabcacf26d31b246b19318d56a1b7a` (round 1: `1651cb5a…`). It is `git diff 97aab1d0 <snapshot>` without the gitlink, and it applies to a clean milan-fpga dev `97aab1d0`. Eight files:

- Round-1 test hunks, unchanged: `tb/verilator/milan_dp/sim_gptp.cpp`, `tb/verilator/milan_dp/sim_ax1x1gptp.cpp`, `tb/verilator/gptp_plane/sim_phc_step.cpp`, `tb/verilator/gptp_plane/phc_step.py`.
- `tb/verilator/tsn_fuzz/fuzz_ptp_timing.py` (new): the campaign's BTCA rejection probes adopt a master that sends no Sync, so the sync receipt timeout ages the port. Its later Announce-only adoptions ("12-hop legal better vector still adopts" and the sync section's GMID) therefore hear one usable pair as master first. The edit is check-neutral (677 checks), so the committed `TEST_RESULTS.md` stays current.
  - Measured: at base (gitlink `55680bff`) 677/0 without and with the edit, so this part can land first. At the round-1 head `d27a1654` without it, 675/2 (the same two checks), so round 1 already needed it. At this head with it, 677/0 and the artifact freshness check passes.
- R719-1 F3, parent docs:
  - `docs/design/GPTP_PLANE.md:130` "The fifth unanswered request after it clears asCapable." and `:134` "The fourth unanswered request after it clears asCapable."
  - `docs/testing/TESTING.md:186` "Five missed Pdelay intervals, …" and `:187` "The scenario spans 17.992742740 simulated seconds over 899637137 cycles." That is the patched run's own figure: `simulated_duration_seconds=17.992742740 cycles=899637137` in `receipts/consumer-head/final-b/01.log`, the same in the exploratory run and in round 1's patched run.
  - `tb/verilator/milan_dp/README.md`, which restates the same scenario: `:198` fifth unanswered interval; the Sync loss row (the expiry makes this station grandmaster); the Peer loss row (five intervals, around 9.2 s, the sixth unanswered request, 6.05 s deadline, certain `tu` after the holdover); `:335` five missed intervals; `:337` the same scenario figure.
- Not changed: `tb/verilator/milan_dp/README.md:347` "The physical harness contributes 137 checks." This was already stale at base (the base run reports 155 physical checks; this head with the patch reports 151, round 1's patched figure). Recorded for the bump, not edited, because it is not a count this change introduced.

Snapshot used for every consumer gate: local commit `b42a52a2743443b2ddf39095481fc8be3ad7d758` on milan-fpga dev `97aab1d0`, gptp-processor gitlink `4d8fb902`, never pushed. Every unit ran in its own fresh clone of that commit.

## Base and head repository gate records

Each gate ran unpiped, on its own, through the lane's recorder, with its own log and result row. Gates 01-11 ran in the lane checkout and gate 12 (`make`) in a fresh clone of the lane at the same commit, so the two could run at once. Base records are this lane's round-1 records at the same base and with the same commands (`receipts/repo-gates-base/`).

### Repository gates, head `4d8fb902`

| Gate | Command | rc | Seconds | HEAD unchanged |
|---|---|---:|---:|---|
| 01-contract | `make contract` | 0 | 0.0 | True |
| 02-ucpu | `make -C tb/verilator/ucpu` | 0 | 6.0 | True |
| 03-parser | `make -C tb/verilator/parser` | 0 | 60.3 | True |
| 04a-engine-run | `make -C tb/verilator/engine run` | 0 | 196.3 | True |
| 04b-engine-mutants | `make -C tb/verilator/engine mutants` | 0 | 6723.1 | True |
| 05-gaskets | `make -C tb/verilator/gaskets` | 0 | 38.8 | True |
| 06-tsngen | `make -C tb/tsngen` | 0 | 41.2 | True |
| 07-bench-test | `make -C bench/arty test` | 0 | 5.0 | True |
| 08-lint | `make lint` | 0 | 0.3 | True |
| 09-docs | `make docs` | 0 | 0.8 | True |
| 10-diagrams-check | `make diagrams-check` | 0 | 0.2 | True |
| 11-ooc-selftest | `python3 syn/ooc/check_ooc_clock.py --selftest` | 0 | 0.1 | True |
| 12-make-all | `make` | 0 | 7076.4 | True |

### Repository gates, base `55680bff` (round 1)

| Gate | Command | rc | Seconds | HEAD unchanged |
|---|---|---:|---:|---|
| 01-contract | `make contract` | 0 | 0.0 | True |
| 02-ucpu | `make -C tb/verilator/ucpu` | 0 | 5.1 | True |
| 03-parser | `make -C tb/verilator/parser` | 0 | 56.8 | True |
| 04a-engine-run | `make -C tb/verilator/engine run` | 0 | 130.1 | True |
| 04b-engine-mutants | `make -C tb/verilator/engine mutants` | 0 | 3775.8 | True |
| 05-gaskets | `make -C tb/verilator/gaskets` | 0 | 35.0 | True |
| 06-tsngen | `make -C tb/tsngen` | 0 | 38.5 | True |
| 07-bench-test | `make -C bench/arty test` | 0 | 5.0 | True |
| 08-lint | `make lint` | 0 | 0.3 | True |
| 09-docs | `make docs` | 0 | 0.8 | True |
| 10-diagrams-check | `make diagrams-check` | 0 | 0.2 | True |
| 11-ooc-selftest | `python3 syn/ooc/check_ooc_clock.py --selftest` | 0 | 0.1 | True |
| 12-make-all | `make` | 0 | 4035.1 | True |

Engine suite at head: 1,805 checks in the shipping pass and in each seeded pass, 57 in the priority1 255 pass; the arm 99/99 (control plus 98 controls). microCPU 768, parser 337 plus 9 mutants, gaskets 81 plus 5, tsngen 288 plus 4. At base: 1,703 and 53; the arm 73/73.

## Consumer gate table (scratch milan-fpga dev `97aab1d0`)

### Head: snapshot `b42a52a2` (gitlink `4d8fb902` and the companion change)

Template list (the manager's `parent-consumer.json`, unchanged commands and environment) split over three fresh clones of the snapshot, each run by the manager's recorded-gates runner in its own unit: A = template commands 1-13 and 15, B = command 14, C = tsn_fuzz `ptp` with the CI-pinned field-campaign generator (`deca300c`).

| Unit | # | Gate | rc | Seconds |
|---|---:|---|---:|---|
| A | 1 | `python3 scripts/check_cpp_idiom.py` | 0 | 3.756 |
| A | 2 | `python3 scripts/check_py_idiom.py` | 0 | 7.15 |
| A | 3 | `python3 scripts/xvlog_gate.py --check` | 0 | 166.784 |
| A | 4 | `python3 scripts/check_rtl_source_lists.py` | 0 | 2.1 |
| A | 5 | `python3 sw/builder/test_builder.py` | 0 | 1474.687 |
| A | 6 | `make -C tb/verilator/gptp_shadow -j8` | 0 | 253.936 |
| A | 7 | `python3 scripts/check_port_contracts.py` | 0 | 3.161 |
| A | 8 | `python3 scripts/measure_naming.py --check` | 0 | 0.556 |
| A | 9 | `python3 scripts/measure_test_evidence.py --check` | 0 | 9.583 |
| A | 10 | `python3 scripts/docs_check.py` | 0 | 7.35 |
| A | 11 | `python3 scripts/lint_rtl.py --check` | 0 | 24.964 |
| A | 12 | `make -C tb/verilator/milan_dp gptp` | 0 | 172.051 |
| A | 13 | `make -C tb/verilator/milan_dp gptp-lat` | 0 | 164.975 |
| A | 14 | `make -C tb/verilator/milan_dp_gm_steps` | 0 | 747.819 |
| A | | run complete | 0 | |
| B | 1 | `make -C tb/verilator/milan_dp_gptp` | 0 | 5301.627 |
| B | | run complete | 0 | |
| C | 1 | `make -C tb/verilator/tsn_fuzz ptp` | 0 | 41.496 |
| C | | run complete | 0 | |

- milan_dp `gptp` 185/185 and `gptp-lat` 185/185. milan_dp_gptp: physical scenario 151 checks, 0 failures, `simulated_duration_seconds=17.992742740 cycles=899637137`; setup abort 6, no-TX 20, no-Pdelay 14, recentre 14, all 0 failures. gm_steps: gmstep 196 checks, 0 failures, and its wrapper 6/6. tsn_fuzz `ptp`: 677 pass, 0 fail, artifact freshness 1/1.
- After the runs the A and B clones are clean. The C clone holds the campaign's own rewrite of `TEST_RESULTS.md`, whose only change is its timestamp (`receipts/consumer-head/final-c-test-results-rewrite.diff`).

### Base: dev `97aab1d0` with gitlink `55680bff` (round 1, `receipts/consumer-base/`)

| # | Gate | rc | Seconds |
|---:|---|---:|---:|
| 1 | `TMPDIR=<scratch>/tmp python3 scripts/check_cpp_idiom.py` | 0 | 4.033 |
| 2 | `TMPDIR=<scratch>/tmp python3 scripts/check_py_idiom.py` | 0 | 7.792 |
| 3 | `TMPDIR=<scratch>/tmp python3 scripts/xvlog_gate.py --check` | 0 | 166.197 |
| 4 | `TMPDIR=<scratch>/tmp python3 scripts/check_rtl_source_lists.py` | 0 | 3.365 |
| 5 | `TMPDIR=<scratch>/tmp python3 sw/builder/test_builder.py` | 0 | 1368.1 |
| 6 | `TMPDIR=<scratch>/tmp make -C tb/verilator/gptp_shadow -j8` | 0 | 258.043 |
| 7 | `TMPDIR=<scratch>/tmp python3 scripts/check_port_contracts.py` | 0 | 3.309 |
| 8 | `TMPDIR=<scratch>/tmp python3 scripts/measure_naming.py --check` | 0 | 0.585 |
| 9 | `TMPDIR=<scratch>/tmp python3 scripts/measure_test_evidence.py --check` | 0 | 9.203 |
| 10 | `TMPDIR=<scratch>/tmp python3 scripts/docs_check.py` | 0 | 8.208 |
| 11 | `TMPDIR=<scratch>/tmp python3 scripts/lint_rtl.py --check` | 0 | 13.302 |
| 12 | `TMPDIR=<scratch>/tmp make -C tb/verilator/milan_dp gptp` | 0 | 156.614 |
| 13 | `TMPDIR=<scratch>/tmp make -C tb/verilator/milan_dp gptp-lat` | 0 | 143.411 |
| 14 | `TMPDIR=<scratch>/tmp make -C tb/verilator/milan_dp_gptp` | 0 | 5126.488 |
| 15 | `TMPDIR=<scratch>/tmp make -C tb/verilator/milan_dp_gm_steps` | 0 | 595.762 |

Run complete: exit 0. tsn_fuzz `ptp` at base, this round: 677/0 rc 0 (`receipts/parent-explore/tsn_fuzz-ptp-base-unedited.log`).

### Exploratory parent runs (before the final snapshot)

- milan_dp `gptp` 185/185 and `gptp_plane` rc 0 (29/29, phc_step 62 checks, its campaign 8/8) at gitlink `4d8fb902` with the round-1 companion hunks.
- milan_dp_gptp rc 0 on an exploratory snapshot with the same tests; it measured the scenario figure the docs now carry.
- tsn_fuzz `ptp`: 675/2 at this head without the campaign edit, 677/0 with it; base and round-1 results as listed above.

## Residuals and follow-ups

Parent follow-ups owed by the gitlink bump (none made here; the parent is never committed upstream from this lane):
- The companion change above (sha256 `b53944d5…`). Its tsn_fuzz and milan_dp `sim_gptp.cpp` parts also pass on the current gitlink, so they can land first.
- `scripts/check_gptp_docs.py --with-submodule` (parent docs workflow, not on the consumer list) requires the donor deep links in `docs/design/GPTP_PLANE.md`, `docs/design/TIME_SYNC.md` and `docs/guides/gptp/*.md` to name the gitlink. Every bump updates them.
- `tb/verilator/milan_dp/README.md:347` "137 checks" was already stale at base (see the companion section).

Not done, recorded:
- R720-1 F3 (suggestion): a two-responder shape where the second responder also sends its own Follow_Up. Not in the round-2 assignment, and a control restricting the reset to one source still does not fit the ROM (R720-1's R6 probe is refused again).
- R719-1 S2: Figure 11-8 also sends WAITING_FOR_PDELAY_RESP to RESET on a Pdelay_Resp with a wrong sequenceId or another port's requestingPortIdentity. Outside #91; worth its own issue.
- R719-1 S3: a reflected own-clock Sync/Follow_Up counts as usable Sync while master and clears the mark (no IEEE 1588-2008 9.5.2.2 own-port filter on Sync receipt). Only a forwarding loop produces one; worth its own issue.
- Published flags bit 0 keeps its #82 meaning: it is set while any peer is elected, a priority1 255 grandmaster included. The ageing decision now uses gmPresent exactly. Changing the published bit is a publication change, not this lane's.
- The per-port mark follows 802.1AS-2011: after a sync receipt timeout, any Announce with gmPresent is aged until a usable Sync is heard, a different grandmaster's included. Adoption of a non-aged port still starts the watch (the 802.1AS-2020 SUPERIOR_MASTER_PORT value before the first Sync), as in round 1.

## Environment and process notes

- No vendor synthesis tool on this host: `make ooc` ran as its self-test only, and the parent's `xvlog_gate.py --check` takes its documented skip. No RTL changed.
- CPU booking: `cpu_ranges.py pick` found no free range. Long runs ran as this lane's own sub-units on its own range (80-95), pinned to sub-ranges, with MemoryMax 4-8 GB each. The parent units ran with `PYTHON_CPU_COUNT=8` and `VERILATOR_JOBS=8`, which change parallelism only. Temporary files went to the lane scratch, never to RAM.
- Every repository gate, probe and parent gate ran unpiped, each with its own log and rc.
- Local snapshots: the parent snapshots are local commits in scratch clones, never pushed.

## Receipts

`receipts/INDEX.md` lists every file present, with size and SHA-256 prefix. Host paths are replaced by placeholders such as `<scratch>`, `<lane>`, `<lane-clone>`, `<parent-final>` and `<management>`.
- `repo-gates-head/`, `repo-gates-base/` (round 1): gate logs and result rows.
- `consumer-head/final-a|b|c/`: the runner's per-command logs, `results.json` and `complete.json`, with the three specs; `consumer-base/` (round 1).
- `probes/`, `probes-before/`: the reviewer probes at this head, and the reviewers' own logs at `d27a1654`.
- `parent-explore/`: the exploratory parent runs and the tsn_fuzz base and round-1 comparison.
- `coverage/`: the check-to-control map and the control table, generated from the arm's log.
- `parent-companion-test.patch` and its `.sha256`; `scripts/`: the lane's runner and helper scripts.
