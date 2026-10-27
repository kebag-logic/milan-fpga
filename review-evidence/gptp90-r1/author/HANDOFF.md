# [A688] HANDOFF: #89, #90, #91 (sync receipt ageing, fifth lost response, duplicate response reset)

Status: REVIEW READY for this repository (every repository gate rc 0 at base and head). The parent consumer gates at head need a companion parent test change. It is prepared and verified below, but this lane may not commit it. So the PR body does not use the "Closes" keywords.

- Repository: Mister-M-alt/FPGA-gPTP, branch `89-90-91-srto-pdelay` (local only, not pushed)
- Base: `55680bff3b287b9a7b0c759f51471fa617c17335` (main)
- Head: `d27a1654285614ded5093cb58f58bceed551fdae`
- Commits (one-line subjects, no body, no trailers):
  - `a9f511a` Age the port on sync receipt timeout, clear asCapable at the fifth lost response, and reset the exchange on a duplicate Pdelay_Resp (#89, #90, #91)
  - `4112c55` Document sync receipt ageing, the fifth-loss rule and the duplicate-response reset
  - `14418db` Plant a failing mutant for every new receipt-rule check and keep the lost-arm mutants word-neutral
  - `72c5615` State the request leg's 56-word size after the branch-free loss count
  - `d27a165` Keep the engine mutation arm under the module length ratchet
- Issue #90: TAKEN at comment 6434826116; `[A688] REVIEW READY d27a1654285614ded5093cb58f58bceed551fdae` at comment 6440565653.
- No top-level port, parameter or register-map change, and no RTL file change. Only these change: `hdl/ucode/gen_gptp_ucode.py` and its four regenerated images, the engine harness and its mutation arm, and the docs.

## What the change does (IEEE 802.1AS-2011 with Cor1 and Cor2, the edition Milan v1.2 profiles)

- #89, 10.3.11 / Figure 10-13 (Cor1): CURRENT goes to AGED on `currentTime >= syncReceiptTimeoutTime && gmPresent`. Timer slot 4 is 375 ms (3 x 125 ms, 10.6.3.1; Milan v1.2 Table 4.2: 375 ms, 337.5..562.5 ms).
  - It now ages an asCapable slave of an elected peer through BECOME, exactly as announce receipt timeout does.
  - Every usable Sync/Follow_Up pair restarts it, and so does the adoption of a new grandmaster. A parent refresh restarts nothing.
  - A grandmaster that never sends usable Sync is therefore aged too.
- #89, no oscillation and automatic recovery: Cor1 strikes `sourcePortIdentity == gmPriority.sourcePortIdentity` from Figure 10-4. So any Sync an asCapable port takes refreshes syncReceiptTimeoutTime, whatever the port's role.
  - An aged port keeps a mark: scratch 46 holds the slave role the timeout found.
  - While the mark stands, every Announce is dropped, because it would be aged again at once. The plane stays grandmaster while Sync stays broken.
  - A master still pairs that peer's Sync and Follow_Up, steering and publishing nothing. The first usable pair clears the mark and restarts the watch, and the peer's next Announce re-elects it, once.
  - An asCapable rise also clears the mark, and every reset forces one, so no mark outlives a reset.
- #90, 11.2.15.3 / Figure 11-8 RESET: `if (lostResponses <= allowedLostResponses) lostResponses += 1; else asCapable = FALSE;`, with allowedLostResponses = 3 (11.5.3). Four consecutive losses keep asCapable and the fifth clears it. Both loss shapes count: no response, and a response without its Follow_Up.
- #91, Figure 11-8 WAITING_FOR_PDELAY_RESP_FOLLOW_UP: a second Pdelay_Resp with the outstanding sequenceId goes to RESET, from either responder.
  - The arm is now `S_RSPSEQ += sequenceId | RSP_ARMED_C`. From zero it arms.
  - Once armed or reset, the value is at least 2 x RSP_ARMED_C, which no Follow_Up can pair with, and it stays nonzero. So a third response cannot re-arm; RESET leaves only on the interval timer (Cor2).
  - The interval then counts as a lost response at the next beat.

## Changes (file:line at head)

`hdl/ucode/gen_gptp_ucode.py`
- `:7` module notes for #89/#90/#91; `:139` the multiple-responder note (the LAST-responder rule is retired); `:192` v6 note on the Sync source cell.
- `:409` `S_SYNCSRC = 45` (own cell; slot 6 stays the master's Sync sequence); `:413` `S_SRTO = 46` (the aged mark) with its invariant.
- `:488` `LOST_CLEARS_AT_C = LOST_N_C + 2`; `:557` `ROLE_MASK_C`, `ROLE_SLAVE_C`, `ROLE_MASTER_C` (replace `SYNCOK_BY_AMGM_C`).
- `:843` `prog_rx_sync` records Sync on any asCapable port.
- `:867` `prog_rx_followup`: a branch-free role gate (slave or master); at `:912` a master's pair goes to SRWATCH.
- `:997` `prog_leg_svrate` ends in SRWATCH; `:1015` new `prog_leg_srwatch` (consume, restart slot 4, stop slot 5, clear the mark).
- `:1041` `prog_rx_announce`: an aged port drops every Announce.
- `:1230` `_pdresp_arm_the_pairing`: one test for completed or frozen, then the RESET sum (`:1271`).
- `:1524` the init leg writes `S_PDGOT = 1` (S_PDGOT left the zero list), so its own first request is never judged.
- `:1622` `_tmr_pdelay_request`: branch-free lost count, compare at `:1643`.
- `:1769` BTCA adoption: the redundant `S_SYNCSRC` clear is dropped; `:1780` adoption arms slot 4.
- `:2073` PDPAIR good verdict: the redundant `S_PDLOST = 0` is dropped (the beat is its only reader); `:2088` an asCapable rise clears `S_SRTO`.
- `:2112` `prog_leg_srto` records the role and runs BECOME only for the slave role; `:2268` SRWATCH in `LEG_FNS`.
- Regenerated images match the generator at head byte for byte, each with its Makefile's arguments:
  - `syn/ooc/work/gptp_ucode.hex` and `tb/verilator/ucpu/gptp_ucode.hex`: defaults.
  - `tb/tsngen/gptp_ucode.hex`: `--clk-hz 2000000`.
  - `tb/verilator/engine/gptp_ucode.hex`: `--clk-hz 2000000 --cease-ms 3000`.

ROM: shipping uses 1,018 of 1,024 words (base 1,015), leaving six free; the seeded regression images use 1,019. The words came from inside the touched legs:
- the branch-free loss count with the init `S_PDGOT` change: -5;
- the PDPAIR and BTCA redundant writes: -1 each;
- the shorter SRTO leg: -1;
- the OR-combined completed/frozen test, which pays for the RESET sum: net 0.

`tb/verilator/engine/sim_main.cpp`: 1,799 shipping checks at head, 1,703 at base. Each seeded pass matches; the priority1 255 pass stays at 53.
- `:508` `pd_reqs_sent`; `:872` `PD_NOFU`/`PD_DUP3` (duplicate and no-Follow_Up exchanges no longer feed the delay model); `:977` `wait_requests`.
- `:2987` the post-adoption window is now two Sync slots, plus a "still slave inside the Sync receipt watch" check.
- `:3345` phase 12, `age_the_grandmaster_at_the_sync_receipt_timeout`: Announce continues; the takeover lands within 375 ms and one BMCA pass of the last usable pair, names thisClock, and carries sync-ok as master.
- `:3376` `hear_a_pair_as_master` and `:3394` `reelect_after_the_sync_receipt_timeout`.
- Phases adapted to the new rule (a receipt timeout now makes the plane master; the grandmaster's Sync is heard, then its Announce re-elects it):
  - 12b `:3435`, 15 `:3600`, 18d `:3870`, 21b `:4028`;
  - 19 `:3927`: the queued timeout ages nothing and keeps sync-ok;
  - the slew contract at `:5718`, `:5801` and `:5868`.
- `:4142` phase 25, `clear_ascapable_at_the_fifth_lost_response`, in four shapes: no response, no Follow_Up, a duplicated response, three responses. One loss and four losses keep asCapable; the fifth clears it; duplicated exchanges complete nothing.
- `:4310` phase 27: same-identity duplicates keep requests going (not a storm).
- `:5399`..`:5504` new phase 39, `age_a_grandmaster_whose_sync_fails`, run at `:385` before the whole-run graders (header `:181`):
  - a never-usable grandmaster is aged within 375 ms of its adoption;
  - then Sync stops, loses its Follow_Up, gets it after the next Sync, or names the next sequenceId, each with Announce continuing. Each time: the takeover lands within the window, no unusable pair is consumed, 3 s of Announces cause no re-election, the recovered Sync is heard as master without steering, the grandmaster is re-elected once, and usable Sync keeps it elected;
  - Sync every 250 ms keeps the plane deferring, and a Follow_Up 60 ms after its Sync is used.

`tb/verilator/engine/mutants.py`: 91 mutants at head, 72 at base; 995 lines, under the parent's 1,000-line module ratchet.
- `:892` named verdicts now also enforce `#89 `, `#90 ` and `#91 `.
- Five stale patterns were repaired (`:188`, `:265`, `:440`, `:502`) and one was repurposed (`:508`).
- Two lost-arm mutants were made word-neutral (`:168`, `:177`): the Follow_Up handler's three new words filled TXLOST's gap.
- The docstring note on the lapse hook's asCapable term is updated for #89.

Docs:
- `docs/INTEGRATION.md`: locked-servo events, the slew table row, departure rules, and a new "Lost Pdelay responses" section.
- `docs/HDL_DEVELOPER.md`: a new "Microcode receipt state" section.
- `docs/TEST_DEVELOPER.md`: suite responsibilities.
- `docs/MANAGER.md`: the ROM budget and `FUTO@190`.
- `docs/SOURCE_EVIDENCE.md`: four requirement rows; the slew policy anchor moved to `#L964`.

## New checks, their mutants and failing words

The head arm (`receipts/repo-gates-head/04b-engine-mutants.log`) catches all 91 mutants: 92 checks with the positive control, rc 0. The table lists each new or repaired mutant and the named checks the arm printed as failing.

| Mutant | Verdict | Failing words (named checks, as printed) |
|---|---|---|
| a sync receipt timeout only clears sync-ok | caught | #89 Sync stops: the plane takes mastership<br>#89 never usable: the grandmaster is aged<br>#89 no Follow_Up: the plane takes mastership within syncReceiptTimeout and one BMCA pass<br>#89 Follow_Up after the next Sync: the plane takes mastership within syncReceiptTimeout and one BMCA pass<br>#89 Follow_Up with the next sequenceId: the plane takes mastership within syncReceiptTimeout and one BMCA pass |
| adoption leaves the Sync receipt watch off | caught | #89 never usable: the grandmaster is aged<br>#89 never usable: within syncReceiptTimeout of its adoption |
| an aged port takes Announces | caught | #89 never usable: the aged port stays master while Announces continue<br>#89 Sync stops: the aged port stays master while Announces continue<br>#89 no Follow_Up: the aged port stays master while Announces continue<br>#89 Follow_Up after the next Sync: the aged port stays master while Announces continue<br>#89 Follow_Up with the next sequenceId: the aged port stays master while Announces continue |
| a master steers on its aged peer's Sync | caught | #89 first grandmaster: Sync recovery is heard as master and steers nothing<br>#89 Sync stops: Sync recovery is heard as master and steers nothing<br>#89 no Follow_Up: Sync recovery is heard as master and steers nothing |
| a master hears no Sync | caught | #89 first grandmaster: the next Announce elects the grandmaster<br>#89 Sync stops: the next Announce elects the grandmaster<br>#89 no Follow_Up: the next Announce elects the grandmaster |
| a queued receipt timeout ages a master | caught | #89 takeover: the queued receipt timeout ages nothing |
| the Sync receipt watch is 100 ms | caught | #89 Sync stops: within syncReceiptTimeout and one BMCA pass<br>#89 first grandmaster: usable Sync keeps it elected<br>#89 Sync every 250 ms keeps the plane deferring |
| the Sync receipt watch is 500 ms | caught | #89 Sync stops: within syncReceiptTimeout and one BMCA pass<br>#89 no Follow_Up: the plane takes mastership within syncReceiptTimeout and one BMCA pass<br>#89 Follow_Up with the next sequenceId: the plane takes mastership within syncReceiptTimeout and one BMCA pass |
| a parent refresh expires the Sync watch | caught | #89 Sync stops: the Announce leaves the grandmaster elected |
| the adoption watch is 100 ms | caught | #89 never usable: within syncReceiptTimeout of its adoption<br>still slave inside the Sync receipt watch |
| a Follow_Up pairs whatever its sequenceId | caught | #89 Follow_Up after the next Sync: no unusable pair is consumed<br>#89 Follow_Up with the next sequenceId: no unusable pair is consumed |
| the Follow_Up watch is 50 ms | caught | #89 a Follow_Up 60 ms after its Sync is used |
| the tracking band is empty | caught | slew: second return pair stays inactive |
| lost responses clear asCapable at the first | caught | #90 no response: one loss keeps asCapable<br>#90 no follow-up: one loss keeps asCapable<br>#91 duplicated response: one loss keeps asCapable<br>#91 three responses: one loss keeps asCapable |
| lost responses clear asCapable at the fourth | caught | #90 no response: four losses keep asCapable<br>#90 no follow-up: four losses keep asCapable<br>#91 duplicated response: four losses keep asCapable<br>#91 three responses: four losses keep asCapable |
| lost responses clear asCapable at the sixth | caught | #90 no response: the fifth loss clears asCapable<br>#90 no follow-up: the fifth loss clears asCapable<br>#91 duplicated response: the fifth loss clears asCapable<br>#91 three responses: the fifth loss clears asCapable |
| the fifth loss stops the requests | caught | #90 no response: request 6 goes out<br>#90 no follow-up: runs from a capable plane<br>#90 no follow-up: runs from a completed exchange |
| a second response re-arms the pairing | caught | #91 duplicated response: the fifth loss clears asCapable<br>#91 duplicated response: no exchange completes<br>#91 three responses: the fifth loss clears asCapable<br>#91 three responses: no exchange completes |
| a third response re-arms the reset exchange | caught | #91 three responses: the fifth loss clears asCapable<br>#91 three responses: no exchange completes |
| same-identity duplicates are a storm | caught | #91 duplicates are not a storm: requests keep going out |
| a later response re-arms the frozen pair | caught | (any check) |
| a receipt timeout unlocks the servo | caught | (any check) |
| an incapable port's Announces still compete | caught | #82 Pdelay loss: Announces from the incapable port elect nothing |
| a queued receipt timeout clears a master's sync-ok | caught | #84 takeover: a queued receipt timeout keeps sync-ok<br>#84 every master cycle publishes sync-ok |
| lost Sync cancels the requester exchange | caught | (any check) |
| lost response cancels the requester exchange | caught | (any check) |

Coverage: every one of the 106 new or changed checks is failed by at least one planted mutant. 59 generator mutants were run against the head harness; none was refused, none survived. The map from each check to every mutant that fails it is `receipts/coverage/coverage-map.md`, generated from `receipts/coverage/coverage.json`.

## Base and head repository gate records

### Repository gates, base `55680bff`

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

Checkout HEAD for every row: `55680bff3b287b9a7b0c759f51471fa617c17335`

### Repository gates, head

| Gate | Command | rc | Seconds | HEAD unchanged |
|---|---|---:|---:|---|
| 01-contract | `make contract` | 0 | 0.0 | True |
| 02-ucpu | `make -C tb/verilator/ucpu` | 0 | 5.1 | True |
| 03-parser | `make -C tb/verilator/parser` | 0 | 52.2 | True |
| 04a-engine-run | `make -C tb/verilator/engine run` | 0 | 184.2 | True |
| 04b-engine-mutants | `make -C tb/verilator/engine mutants` | 0 | 6112.2 | True |
| 05-gaskets | `make -C tb/verilator/gaskets` | 0 | 35.0 | True |
| 06-tsngen | `make -C tb/tsngen` | 0 | 40.7 | True |
| 07-bench-test | `make -C bench/arty test` | 0 | 5.0 | True |
| 08-lint | `make lint` | 0 | 0.3 | True |
| 09-docs | `make docs` | 0 | 0.8 | True |
| 10-diagrams-check | `make diagrams-check` | 0 | 0.2 | True |
| 11-ooc-selftest | `python3 syn/ooc/check_ooc_clock.py --selftest` | 0 | 0.1 | True |
| 12-make-all | `make` | 0 | 6210.1 | True |

Checkout HEAD for every row: `d27a1654285614ded5093cb58f58bceed551fdae`

Engine suite tallies at head: 1,799 checks in the shipping pass and in each seeded pass, 53 in the priority1 255 pass; the arm 92/92. At base: 1,703 and 53; the arm 73/73.

## Parent companion test change (verified, not committed upstream)

`receipts/parent-companion-test.patch` applies to milan-fpga dev `97aab1d0`. It touches five files.

`tb/verilator/milan_dp/sim_gptp.cpp` (consumer gates 12 and 13):
- The PathTrace phases keep an Announce-only peer elected for longer than syncReceiptTimeout, which #89 now ages. The patch sends one Sync pair before each long wait.
- The full-queue drop arm passed at base only because a stale queue entry dispatched the Announce handler's long BTCA path. With #89 that entry is a short handler. The arm now holds a Pdelay_Resp at the MAC so dispatch pops nothing.
- Verified at head: `milan_dp gptp` 185/185 and `gptp-lat` 185/185. At base `gptp` is also 185/185, so this part can land before the bump.

`tb/verilator/milan_dp/sim_ax1x1gptp.cpp` (consumer gate 14), the loss arm:
- The 375 ms Sync timeout now makes the station grandmaster, so tu is set with the role synchronised (`0x3`). The holdover is timed from the real takeover.
- The asCapable deadline gains one second for the fifth missed response, and the count becomes five unanswered intervals.
- Head result: rc 0 in 5,065 s, physical scenario 151 checks with 0 failures (4 fewer than the unpatched 155: the "before this station is grandmaster" audio window no longer exists), and every sub-arm passes; simulated length 17.99 s against 16.99 s at base. The dated measurement records in the parent's `tb/verilator/milan_dp/README.md` are left as they are.

`tb/verilator/gptp_plane/sim_phc_step.cpp` and `phc_step.py` (not on the consumer list):
- Windows gain one second for the fifth loss; the expected counts become 5 and 4.
- Verified at head: the suite, its phc_step mutant arms included, rc 0.
- This part is gitlink-specific and must land with the bump.

`docs/testing/TESTING.md`: "Five missed Pdelay intervals". The scenario length quoted there grows by about a second; take the new figure from the run.

## Consumer gate table (scratch milan-fpga dev 97aab1d0)

Head result: 12 of 15 gates rc 0. Gates 12, 13 and 14 return 2, every failing check a parent expectation of the pre-#89/#90 behaviour (root causes in the companion section). gm_steps passes.
- `milan_dp gptp` and `gptp-lat`: 18 failing checks each (PathTrace phases with an Announce-only peer past syncReceiptTimeout; the stale-entry drop arm).
- `milan_dp_gptp`: 2 failing checks (`375 ms Sync timeout clears sync and asserts tu` got 0x3 exp 0x1; `loss clears asCapable` at the old fourth-loss deadline).
- Base result: all 15 gates rc 0, run complete with exit 0.

### Consumer gates at head, run A (gates 1-10; unit stopped by its own 8 GB cap at gate 11)

Parent snapshot HEAD `56229cc91fd7c1e624ff701b88a25ef17b21d4df`, base `97aab1d0f28bd753a3e11df6278d5cac54f964dd`.

| # | Gate | rc | Seconds |
|---:|---|---:|---:|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | 1.807 |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | 5.059 |
| 3 | `python3 scripts/xvlog_gate.py --check` | 0 | 159.182 |
| 4 | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.817 |
| 5 | `python3 sw/builder/test_builder.py` | 0 | 1501.815 |
| 6 | `make -C tb/verilator/gptp_shadow -j8` | 0 | 231.188 |
| 7 | `python3 scripts/check_port_contracts.py` | 0 | 2.898 |
| 8 | `python3 scripts/measure_naming.py --check` | 0 | 0.495 |
| 9 | `python3 scripts/measure_test_evidence.py --check` | 0 | 8.903 |
| 10 | `python3 scripts/docs_check.py` | 0 | 7.625 |

Run did not write complete.json (see notes).

### Consumer gates at head, run B (gates 11-15)

Parent snapshot HEAD `56229cc91fd7c1e624ff701b88a25ef17b21d4df`, base `97aab1d0f28bd753a3e11df6278d5cac54f964dd`.

| # | Gate | rc | Seconds |
|---:|---|---:|---:|
| 11 | `python3 scripts/lint_rtl.py --check` | 0 | 12.669 |
| 12 | `make -C tb/verilator/milan_dp gptp` | 2 | 149.304 |
| 13 | `make -C tb/verilator/milan_dp gptp-lat` | 2 | 148.043 |
| 14 | `make -C tb/verilator/milan_dp_gptp` | 2 | 3919.749 |
| 15 | `make -C tb/verilator/milan_dp_gm_steps` | 0 | 653.676 |

Run complete: exit 1.

### Consumer gates at base

Parent snapshot HEAD `97aab1d0f28bd753a3e11df6278d5cac54f964dd`, base `97aab1d0f28bd753a3e11df6278d5cac54f964dd`.

| # | Gate | rc | Seconds |
|---:|---|---:|---:|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | 4.033 |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | 7.792 |
| 3 | `python3 scripts/xvlog_gate.py --check` | 0 | 166.197 |
| 4 | `python3 scripts/check_rtl_source_lists.py` | 0 | 3.365 |
| 5 | `python3 sw/builder/test_builder.py` | 0 | 1368.1 |
| 6 | `make -C tb/verilator/gptp_shadow -j8` | 0 | 258.043 |
| 7 | `python3 scripts/check_port_contracts.py` | 0 | 3.309 |
| 8 | `python3 scripts/measure_naming.py --check` | 0 | 0.585 |
| 9 | `python3 scripts/measure_test_evidence.py --check` | 0 | 9.203 |
| 10 | `python3 scripts/docs_check.py` | 0 | 8.208 |
| 11 | `python3 scripts/lint_rtl.py --check` | 0 | 13.302 |
| 12 | `make -C tb/verilator/milan_dp gptp` | 0 | 156.614 |
| 13 | `make -C tb/verilator/milan_dp gptp-lat` | 0 | 143.411 |
| 14 | `make -C tb/verilator/milan_dp_gptp` | 0 | 5126.488 |
| 15 | `make -C tb/verilator/milan_dp_gm_steps` | 0 | 595.762 |

Run complete: exit 0.

Extras, run at head after the list (not on the consumer list): `make -C tb/verilator/gptp_plane` rc 2; `make -C tb/verilator/gptp_txts` rc 0; `make -C tb/verilator/gptp_tables` rc 0; `python3 scripts/check_gptp_docs.py --with-submodule` rc 1; `make -C gptp-processor docs` rc 0. gptp_plane fails on the fifth-loss expectations (4 checks: the liveness and unanswered windows and counts, and the missing-peer window) and passes with the companion change; the docs-pin check reports the expected gitlink pin findings.

## Residuals and follow-ups

Parent follow-ups owed by the gitlink bump (none made here: the parent is never committed upstream from this lane):
- The companion test change above.
- `scripts/check_gptp_docs.py --with-submodule` (parent docs workflow, not on the consumer list) requires every donor deep link in `docs/design/GPTP_PLANE.md`, `docs/design/TIME_SYNC.md` and `docs/guides/gptp/*.md` to name the gitlink. It passes at base and reports pin findings at any other gitlink, so every bump updates those links. Nothing in them is wrong about this change's behavior.

Out-of-scope observations, recorded and not changed (the assignment confines this lane to its three issues):
- **Wrong-sequence response.** Figure 11-8 also sends WAITING_FOR_PDELAY_RESP to RESET on a Pdelay_Resp with a wrong sequenceId or another port's requestingPortIdentity. The engine ignores such a response, so an interval that later receives a correct pair completes instead of counting a loss. Worth its own issue.
- **gmPresent approximation.** The ageing condition uses the engine's published gmPresent (a peer is elected, or thisClock is grandmaster-capable). So a priority1 255 peer elected by a priority1 255 plane is aged on Sync loss, where 802.1AS-2011 10.2.3.13 gmPresent would be FALSE (no grandmaster-capable system present). This is the engine's existing approximation (#82).
- **Reflected Sync.** A reflected Sync and Follow_Up carrying this plane's own clockIdentity would count as usable Sync while master and clear the aged mark. Sync receipt has never filtered own-clock frames (IEEE 1588-2008 9.5.2.2), and only a forwarding loop produces one.
- **Per-port mark.** The aged mark is per port, as 802.1AS-2011 defines syncReceiptTimeoutTime. After a sync receipt timeout, a different grandmaster's Announce is also aged until a usable Sync is heard.
  - 802.1AS-2020 Figure 10-14 restarts the timer at SUPERIOR_MASTER_PORT instead. That re-elects for 375 ms per Announce while Sync stays broken, which is the oscillation the assignment rules out.
  - The 2011 reading is the one implemented. Adoption of a non-aged port still starts the watch, which is the 2020 clarification of the value before the first Sync.

Environment and process notes:
- **No Vivado on this host.** `make ooc` was run only as its self-test, and the parent's `xvlog_gate.py --check` takes its documented skip. No RTL changed; the ROM content changes, not its size or interface.
- **CPU booking.** `cpu_ranges.py pick` found no free range at any launch. The long runs ran as this lane's own sub-units on its own range (80-95), with MemoryMax 4-10 GB each. Every gate command ran unpiped, with its own log and result row.
- **Consumer run A.** It was stopped at gate 11 (`lint_rtl.py --check`) by its own 8 GB cap. That gate and milan_dp default to the host's 128 CPUs, not the unit's 16.
  - Run B re-ran gates 11-15 on the same snapshot with `PYTHON_CPU_COUNT=16` and `VERILATOR_JOBS=8`, which change parallelism only.
  - The base run used the same environment.
- **Local snapshots.** The parent snapshots are local commits in scratch clones (`97aab1d0` plus the gitlink at head), never pushed.

## Receipts

`receipts/INDEX.md` lists every file present, with size and SHA-256 prefix. Host paths are replaced by placeholders such as `<scratch>`, `<lane>` and `<parent-head>`.
