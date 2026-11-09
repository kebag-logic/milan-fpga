[R801] POSITIVE - exact head 84f6d6ad77d51d678f8efdf26b45aae011a42001

# R801-2 independent review: processor issue #216 / PR #218, round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #218 (closes #216; parent issues kebag-logic/milan-fpga#860 and #857).
- Exact head `84f6d6ad77d51d678f8efdf26b45aae011a42001`, tree `3582db8c1c23012840dcbcf2cfd1a1e91f560119`. Source base `044cb25f`. Previously reviewed head `60094a268c0df46703a3bee08c94118153634fd9`.
- Delta `60094a2..84f6d6a`: four commits (`b655100`, `b5f9e53`, `ceb6a98`, `84f6d6a`), 28 files, +583 / -70. The HDL part is `hdl/srp/KL_srp_vlan.sv` (+36 / -8) and `hdl/srp/KL_srp_top.sv` (+11). The rest is tests, arms and docs.
- Reconstructed in this order, in a cleared context:
  - the repository README and `docs/README.md` (the tree has no AGENTS.md or CONTRIBUTING.md);
  - the issue body (frozen acceptance) and all five issue comments, including the manager's round 2 ruling (issuecomment-6740735425);
  - the PR body and the review-start comment;
  - IEEE 802.1Q-2018 Tables 10-3 and 10-4 and 10.7.6.3, and Milan v1.2 4.3.2, as cited;
  - `git diff 044cb25f..84f6d6a` with its history, read for the delta `60094a2..84f6d6a` in full;
  - then the public evidence. The tree named in the brief, kebag-logic/milan-fpga `8844ce1c` `review-evidence/pp216-r1`, holds round 1 only. The round 2 receipts are its successor on the same branch, `pp216-review-evidence` at `6ef09f9d` (`author-r2/`).
- I read the prior review findings (R801-1 issuecomment-6740368085, R802-1 issuecomment-6740725581) only after my own pass over the delta. Each is resolved below.
- **Verdict: POSITIVE.**
  - Every ruling item is met at its cause, and every round 1 finding of both reviews is resolved.
  - The processor gates I ran at the head pass (below).
  - The findings of this round are SUGGESTIONs only. No MINOR, MAJOR, BLOCKER or RESIDUE is open.

## Findings

### R801-2-S1 - SUGGESTION - Tests

- **Where:** `tb/srp_top/mutants.py:489`, `:491`, `:493`. The three AP8 arms expect the substring `'AP8:'`. The AP8 setup check's message also starts `AP8: setup:` (`tb/srp_top/sim_main.cpp:4103-4105`).
- **Evidence:**
  - An arm that broke only the setup (no JoinIn before the bounce) would count as killing the link property.
  - At this head each of the three arms fails the property rows, never the setup:
    - `vlan-link-keeps-registrar`: both rows (`receipts/probe-arm-vlan-link-keeps-registrar-app.log`; it sends `New@3801 New@4001 JoinIn@5001`);
    - `vlan-link-no-begin`: the restart row (`receipts/probe-arm-vlan-link-no-begin-app.log`);
    - `top-vlan-link-unwired`: both rows (the author's `camp-srp/selected-out/top-vlan-link-unwired.log`).
  - So no result changes.
  - The campaign's own logs cannot show this. A label graded on two suites keeps one receipt name, and the encoder run overwrites the `srp_top` log (`mutants.py` `trial` docstring). That is why I ran the two shared arms on the `applicant` group alone.
- **Suggested outcome:** expect `'AP8: VID 2'`, the words both property rows start with, so that a plant must fail the property to count as a kill.

### R801-2-S2 - SUGGESTION - Conformance, Robustness, Docs

- **Where:** `hdl/srp/KL_srp_vlan.sv:478` (`vid_sent_o = active_r & sent_r`); `sent_r` is not cleared at LINK_UP. `docs/architecture/10_srp_engine.md:532` says "A link change does not reset the talker's streaming licence (below)". The section below (§6.2 "Join before the stream", `:549-592`) does not mention a link change.
- **Behaviour:**
  - After a link bounce the talker's streaming licence stays open for the VID.
  - The VID's declaration on the restored link has not yet left: its first New goes out within one T-MRP-JOIN of LINK_UP (AP8).
  - Milan v1.2 4.3.2: a Talker "shall join the relevant VLAN via MVRP prior to sending any Stream frames".
- **Why only a suggestion:**
  - The licence also needs a Listener registration at the talker, and LINK_DOWN flushes it. In the author's report-only probe, `tk_reg(0)` goes from 1 to 0 during the link-down period (`receipts/stream-link-bounce/probe.log`).
  - A Ready from the new partner needs our Talker Advertise registered there first. In practice it follows the VID's New, which rides the first MVRP tx! after LINK_UP.
  - Before this PR the VID had no restart at all, so the window was not wider than before.
  - The HANDOFF lists it as unchanged on purpose.
- **Suggested outcome:** one of these.
  - Clear `sent_r` at LINK_UP, so that the licence waits for the New on the new link.
  - Or replace "(below)" with the argument: "A link change does not reset the talker's streaming licence: the licence also needs a Listener registration, which LINK_DOWN flushes, and a new partner's Ready follows its registration of the Talker Advertise."

### Observations (no action)

- **A message the encoder has already taken from a walk that LINK_UP interrupts still leaves in that walk's MRPDU.**
  - Only the message the walk still holds is withdrawn (`KL_srp_vlan.sv:452-454`, `:474`).
  - 10 §6.2 discloses this (`:530-531`).
  - A message decided after LINK_DOWN reads the Registrar MT, so it is never a JoinIn. At worst the new partner sees one extra JoinMt or New before the restarted ladder.
- **A last user's leave on the LINK_UP clock itself** gives VN, then Lv! (LA), so one Lv goes to the new partner. That follows the documented order (the link change comes before the clock's MAD request) and Table 10-3, and it is harmless.
- **LINK_UP in Begin! then New!:** the restart takes Begin! then New!, so the new partner gets New, New, then the Join, as the ruling directs. A Join! re-declaration (VO + Join! = VP) is the other reading of Table 10-3. The ruling decided between them, so I do not re-open it.

## Prior findings at this head

| Finding | Severity there | State at `84f6d6a` | Evidence |
|---|---|---|---|
| R801-1-F01 (= R802-1 F2): `tb/srp_encoder/README.md` row records 7 FAIL where the arm fails 8 | MINOR | **RESOLVED** | `tb/srp_encoder/README.md:277` reads `8 FAIL — V10, W4, W5 (two), B1 (four)`, the ruling's exact text. The author's head campaign and mine both measure `vlan-rejoin-of-leaving-allocates ... failures=8` |
| R801-1-F02 (= R802-1 R1): §6.5 copies "10 to 15 s" outside F08.1 | RESIDUE | **RESOLVED** | `10_srp_engine.md:1150` reads "every `T-MRP-LEAVEALL` ([F08.1](08_timing.md#fig-08-constants)) from Begin!", R802-1 R1's exact fix with the in-repo link (anchor at `08_timing.md:11`) |
| R801-1-F03 (= R802-1 S3): a VID a peer registered before the first local join is first answered JoinMt | SUGGESTION | **RESOLVED** as the ruling's item 5 directs | GAP-18 [Minor] in `docs/00_MILAN_COMPLIANCE_REVIEW.md:369-382`, with the ruling's basis (note 11 covers the Applicant only; a Table 10-4 Registrar would read IN). Its F00.2 row is at `:598`, REQ-SRP-006 lists it (`:541`), and 10 §6.2 cites it (`:505-509`) |
| R802-1 F1: the VID Registrar keeps IN across LINK_DOWN / LINK_UP | MAJOR | **RESOLVED** | Ruling item 1, below |
| R802-1 S1: no check tells VP from AP on note 4 and txLA! | SUGGESTION | **RESOLVED** | DA6, DA7, VR12, VR13 and three arms; ruling item 3, below |
| R802-1 S2: `N_VIDS_P > ENC_DEPTH_P` would stall the MVRP round | SUGGESTION | **RESOLVED** | `g_vids_fit`; ruling item 3, below |

## Ruling items (issuecomment-6740735425), judged at their cause

1. **The VID Registrar and Applicants at a link change: MET.**
   - **Wiring.** `KL_srp_vlan` has `link_up_i` (`:75`). `KL_srp_top` wires it to the engine's `link_up_i` (`:476`), the same net the Domain (`:399`) and the listener FSMs (`:670`) take.
   - **Registrar.** `link_ev_w` (either edge, `:187`) takes every VID Registrar to MT (`:279-280`). It comes last in the Registrar's update, so it wins over the clock's received value, rLA! and txLA!. That is 802.1Q-2018 Table 10-4: Flush! and Begin! go to MT, here as LINK_DOWN and LINK_UP.
   - **Applicant.** `link_rise_w` is Begin! on every Applicant (VO). Each entry with users then takes New! (VN), before the clock's MAD request or tx! moves it (`:289-290`, then `one_st_w` and `wmsg_w` read `app_ev_w`). That is Table 10-3's Begin! and New! rows.
   - **Effect on sJ.** sJ then reads the Registrar MT, so it is JoinMt (10.7.6.3).
   - **Entries with no user.** An entry with no user is VO with nothing owed, so the next walk discards it (`:433`, note 11).
   - **A message held across LINK_UP.** A message the walk holds at LINK_UP is withdrawn (`:452-454`, `:474`), and the entry re-evaluates restarted.
   - **Reset.** `link_q_r` resets to 0, as the Domain's does. A link already up at reset is a LINK_UP on the first clock, with nothing allocated, so it is harmless.
   - **The check.** AP8 (`tb/srp_top/sim_main.cpp:4092-4124`) sets up the Registrar IN (the peer's JoinIn, VID 2 sent JoinIn), then 30 ms down and up. It then requires no JoinIn after the bounce, and New, New, JoinMt on consecutive tx!, the first within 240 ms of LINK_UP. That is the ruling's check.
   - **Arms killing AP8 by name.** `vlan-link-keeps-registrar` fails both AP8 rows and `vlan-link-no-begin` fails the restart row (my receipts). `top-vlan-link-unwired` fails both (the author's selected log, and my campaign's KILLED line).
   - **Encoder rows.** VR14 to VR18 hold each edge apart and are killed by four more arms.
   - **My probes p1, p3, p4, p8** are each killed by a VR row and not by AP8, which is expected:
     - p1: LINK_DOWN no longer flushes;
     - p3: LINK_UP no longer clears the Registrar;
     - p4: the withdrawal keeps its valid;
     - p8: Begin! keyed on `alloc_r` instead of `active_r`.
     - p1 and p3 leave AP8 passing because the bounce has both edges and either one suffices; VR14 and VR15 tell them apart.
   - **Docs.** 10 §6.2 "A link change" (`:515-536`) and F10.3's three link edges (`:485-487`) match the code.
2. **The stream Applicants across a link bounce, report only: MET.**
   - **The probe is sound.** The author's disposable `streamlink` group (published patch and log) declares a Talker and a Listener with a registering peer, bounces the link for 30 ms, and prints each value's messages after LINK_UP, with and without a peer re-declaration.
   - **What it shows.** The Talker Advertise is not declared New again: its first message after LINK_UP is the JoinMt of the next periodic!, 872 ms later. The Listener Ready is withdrawn and declared again once the peer's Advertise registers.
   - **Filed.** That is filed as #220 (open, created 2026-11-09T18:07Z) with this evidence.
   - **Nothing in the stream path changed.** The delta's HDL is only `KL_srp_vlan.sv` and `KL_srp_top.sv` (the guard and the one port connection). `KL_srp_talker_fsm.sv`, `KL_srp_listener_fsm.sv`, `srp_pkg.sv`, `KL_srp_domain.sv`, `KL_srp_encoder.sv` and `KL_srp_decoder.sv` are untouched (`git diff --stat 60094a2..84f6d6a -- hdl`).
   - **Suites.** `tb/srp_stream_fsms` passes 1512/1512 at the head, the same count as round 1.
3. **The README count, the VP/AP checks, the N_VIDS guard, the gap register entry: MET.**
   - **README count.** See F01 above.
   - **VP/AP checks.** DA6/VR12 (note 4: a peer LeaveAll riding its JoinIn leaves VP alone, so JoinIn goes out on two tx!) and DA7/VR13 (txLA! from VP sends s and goes AA, so Mt, then one JoinMt) are in `tb/srp_encoder/sim_main.cpp:1507-1547` and `:1975-2004`.
     - Their arms `vp-rjoinin-ignores-note4`, `vp-txla-stays-vp` and `vp-txla-sends-sj` plant the same edits as R802-1's three surviving probes.
     - The published `r802-probes` receipts show each probe failing at the head with `1659 checks: 1657 PASS, 2 FAIL`, and the link-bounce probe passing (`New@3801 New@4001 JoinMt@4201`).
   - **N_VIDS guard.** `g_vids_fit` (`KL_srp_top.sv:267-275`) refuses `N_VIDS_P > ENC_DEPTH_P`.
     - It is the right bound. The encoder's MVRP table is `mvrp_ram_r [0:DEPTH_P-1]` (`KL_srp_encoder.sv:327`), with `DEPTH_P` wired from `ENC_DEPTH_P` (`KL_srp_top.sv:791`). A walk pushes at most one message per VID, and pushes wait while a drain runs.
     - I ran the guard bench on Verilator 5.050 and Yosys: 13 is refused at `KL_srp_top.sv:273` by both, and 12 elaborates. `make` is 160/160 and `--only KL_srp_top.g_vids_fit --frontend yosys` is 34/34.
     - All five planted arms are killed (`elab guard mutants: 5 of 5 killed`).
     - The defaults (4, 12) and the processor top (no override) pass.
   - **Gap register entry.** GAP-18, see F03 above.
4. **The seven pre-existing `tb/srp_top/README.md` arm counts: NOT REQUIRED by the ruling.**
   - The ruling's item 2 names one count only, the encoder row of F01.
   - Its "Done means" list names gates, campaigns, the scratch parent and the twin. It does not name these rows.
   - Both round 1 reviews found them stale already at the base, and in rows this PR did not add or change. R801-1 classed them as out of scope and a manager follow-up.
   - The author's comparator shows they are unchanged at `60094a2` and at this head (`camp-srp/cmp-counts.txt`: 19 rows differ, all pre-existing). The PR body discloses them.
   - No follow-up issue exists yet (a manager duty, below).
5. **Area: MET.**
   - 10 §5.1 (`:339-347`) states the VID link change as 49 LUT and 1 FF of `KL_srp_vlan` alone (594 to 643 LUT, 147 to 148 FF). In `KL_srp_top` it is -1 LUT at 2x2 and +89 at 8x8, inside the flow's noise, with no FF.
   - These equal the author's yosys receipts: `area-60094a2-out/SUMMARY.md` and `area-84f6d6a-out/SUMMARY.md`. The `vlan.stat` LUT1 to LUT6 sum is 643, with 148 FDRE.
   - The PR body's table carries the same figures.
   - The 2x2 FF count staying at 5,447 is consistent with the new `link_q_r` merging with the Domain's identical register of the same net.
   - I did not re-run synthesis (see limits).
6. **The 40 scratch-parent consumer gates and the twin's three owed rows: MET on the published receipts.** I did not re-run them; that is not allowed here.
   - `parent-84f6d6a/` has 40 `.rc` files, all 0.
   - The pin record shows protocol-processor at `84f6d6ad77d5…` on dev `ac0a01e3`, with two local commits (the pin, then the ROM digests re-recorded through the recorder).
   - `twin-84f6d6a/twin-compare.txt` reports the three owed rows `fabric-mvrp-leave-all`, `fabric-domain-one-new` and `fabric-vid2-join-in`, each "the defect has gone". The run's rc 2 comes from those three DIFF lines only.
   - `entity-available-index` (#217), `split-talker-failed` and `stream-output-0-notices` still hold as OWED.
7. **`tools/proc-shards.py` and the ten-minute pause: NEITHER COULD CHANGE A RESULT.**
   - **What the stand-in changes.** `proc-shard.sh` runs the repository's own `scripts/run_suites.sh` text. It changes only the suite list of its one loop, guarded to match that loop exactly once or exit 99.
     - So each shard runs the uPC-map and M9 checks, each suite's `make`, the PASS/FAIL/UNREADABLE verdicts and the exit status unchanged.
     - The partition is suite index mod 4. The four `assignment.txt` files together list the 36 suites, and the head has 36 `tb/*/Makefile` directories.
   - **What the merge checks.** `merge-shards.py` takes the expected suites from the head's own glob. It requires each one PASS in exactly one shard, no FAIL or UNREADABLE line, every shard rc 0 and each shard's closing `0 failing` line. Its `MERGE OK` and the merged per-suite counts are in `sweep/`.
   - **Other run conditions.** `MAKEFLAGS=-j4` changes build parallelism only.
   - **The pause.** The SIGSTOP/SIGCONT of the maap, adp_engine, aecp_cmds and elab_guards campaign chain cannot matter. Every budget in those drivers and benches is a clock-cycle budget (for example `aecp_cmds` `TRIAL_BUDGET = 40000` clocks). None is a wall-clock budget: none of `timeout`, `time.time`, `monotonic`, `chrono` or `alarm` appears in their drivers or in `tb/common`'s Python.
   - **Cross-check.** The per-suite counts I measured independently equal the merged record: srp_top 8706, srp_encoder 1659, srp_stream_fsms 1512, elab_guards 160.

## Lens verdicts and evidence

- **Conformance: CLEAN.**
  - **Link change.** Table 10-4 Flush!/Begin! to MT and Table 10-3 Begin! (VO) then New! (VN) are implemented as ruled, on every entry, with the link change winning its clock. 10.7.6.3 holds across a bounce (AP8, VR14 to VR16).
  - **VP rows.** The VP rows (note 4, txLA! from VP) now each have a distinguishing check.
  - **Gap register.** GAP-18 records the pre-join registration with its clause basis.
  - **Timers.** No timer value, draw range or F08.1 row moved (`docs/architecture/08_timing.md` is untouched).
  - **Licence.** S2 is a suggestion on the streaming licence.
- **RTL: CLEAN.**
  - **Read.** I read the full HDL delta: the edge detect and its reset; the Registrar priority (link last); the Applicant override before the MAD request and tx!; and the W_PUSH withdrawal (valid masked combinationally on the LINK_UP clock, re-entry to W_EVAL at the same index, `queued_r` not set for the withdrawn message).
  - **LINK_UP during an operation.** I traced LINK_UP during V_SCAN, during V_APPLY (a New! on a found inactive entry, a New! on a free entry, a last user's Lv!), during W_EVAL with txLA!, and during W_PUSH at the last index. Each leaves a consistent state.
  - **Guard.** The guard's generate block is named and elaborates away at the defaults.
  - **Lint.** `bash scripts/lint_hdl.sh` gives 41 modules `LINT OK` on Verilator 5.050.
  - **Ports.** The top port list is unchanged (`hdl/top` untouched).
- **Robustness: CLEAN.**
  - **Exercised.** A received value on the link clock (VR16); a link bounce with the Lv owed and no user (VR17); LINK_UP while the walk holds a message, and on the clock the walk evaluates it (VR18); a link already up at reset; `N_VIDS_P` above the encoder depth (refused at elaboration).
  - **Interrupted walk.** The interrupted-walk case is disclosed (Observations).
  - **Suites.** `tb/srp_top` 8706/8706, `tb/srp_encoder` 1659/1659, `tb/srp_stream_fsms` 1512/1512.
- **Tests: CLEAN.**
  - **Rows read.** AP8, DA6, DA7 and VR12 to VR18, each with its own words and setup.
  - **Arms.** I read the ten new arms and the four re-expressed arms. My full campaign gives `365 checks: 365 PASS, 0 FAIL` and `assertion coverage: 185/185; missing=[]`. All 342 arm results (label, rc, failure count, verdict) and every control are identical to the author's head receipt (`receipts/cmp-campaign-vs-author.txt`, 0 differing).
  - **Probes.** My four probes are each killed. The two shared AP8 arms were run on the `applicant` group alone, so their AP8 rows are visible.
  - **Suggestion.** S1 tightens the AP8 expectation.
- **Docs: CLEAN.**
  - **Prose against code.** 10 §5.1, §6.1 (DA6, DA7), §6.2 and F10.3 (the link change, GAP-18), §6.5 (F02 fixed); 00 GAP-18, its F00.2 row and REQ-SRP-006; 09 §8.15 (three rows).
  - **README totals.** The READMEs of `tb/srp_top` (8706, AP8, coverage AP1 to AP8), `tb/srp_encoder` (1659) and `tb/elab_guards` (32 guards, 96/160 checks, 165 arms) match my runs.
  - **README counts.** Every arm count in a row the delta added or changed equals the campaign. I checked the `tb/srp_encoder` README's 13 re-measured and 9 new rows and the `tb/srp_top` README's 2 re-measured and 3 new rows against the head campaign.
  - **Gates.** `make check` rc 0; `gen_matrix.py --check` `matrix: OK (94 rows, 0 untested)`; `git diff --check 044cb25f 84f6d6a` empty.
  - **Suggestion.** S2's docs wording is a suggestion.
- **Comment rule.** I scanned the delta's added lines under `hdl/`, `tb/`, `scripts/` and `syn/`. The only ID-like tokens are issue numbers (#214, #216), clause and table IDs, and test-row IDs (B1, VR*, DA*). No bench lane label, lane name, review round, reviewer ID or issue-comment ID appears. No new instance.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_srp_vlan.sv:75,177-188,226-303,339-345,430-474` against Table 10-4 (Flush!, Begin!), Table 10-3 (Begin!, New!, note 11) and 10.7.6.3; `KL_srp_top.sv:267-275,476`; stream path untouched (`git diff --stat 60094a2..84f6d6a -- hdl`); the stream probe and #220; GAP-18 basis; timers unchanged; S2 suggestion. Code the delta does not touch keeps R801-1's verdict | R801-2 (delta), R801-1 (rest) | 84f6d6ad77d51d678f8efdf26b45aae011a42001 |
| RTL | CLEAN | the full HDL delta (edge detect, reset, Registrar priority, Applicant override order, W_PUSH withdrawal, guard); LINK_UP during each FSM state; lint 41 `LINT OK` (Verilator 5.050) | R801-2 (delta), R801-1 (rest) | 84f6d6ad77d51d678f8efdf26b45aae011a42001 |
| Robustness | CLEAN | VR16 to VR18 and AP8 scenarios; reset with the link up; guard at 12/13; the interrupted walk (disclosed); suites srp_top 8706/8706, srp_encoder 1659/1659, srp_stream_fsms 1512/1512 | R801-2 (delta), R801-1 (rest) | 84f6d6ad77d51d678f8efdf26b45aae011a42001 |
| Tests | CLEAN | AP8, DA6, DA7, VR12 to VR18 source; 10 new and 4 re-expressed arm patches; full SRP campaign 365/365, coverage 185/185, all 342 arm results identical to the author's head receipt; two shared AP8 arms on `applicant` alone; four reviewer probes killed; elab guard bench 160/160 and its 5 new arms killed; S1 suggestion | R801-2 | 84f6d6ad77d51d678f8efdf26b45aae011a42001 |
| Docs | CLEAN | 10 §5.1, §6.1, §6.2/F10.3, §6.5; 00 GAP-18, F00.2, REQ-SRP-006; 09 §8.15; READMEs of `tb/srp_top`, `tb/srp_encoder`, `tb/elab_guards` against the campaign; `make check` rc 0; matrix OK; `git diff --check` empty; comment rule; S2 suggestion | R801-2 | 84f6d6ad77d51d678f8efdf26b45aae011a42001 |

## Gates and probes I ran at the exact head

Each gate ran in its own disposable `--shared` clone of the head. I used Verilator 5.050, verified with `verilator --version`: `Verilator 5.050 2026-07-01 rev v5.050`, through the scoped wrapper put first on PATH. Python is 3.14.9 on the host; CI uses 3.12.3. The receipts are under `receipts/`, each with `.cmd`, `.log`, `.rc`, `.start` and `.end`.

| Gate | rc | Result |
|---|---|---|
| `make check` | 0 | every docs, AECP-command, ids and figures gate OK |
| `python3 scripts/gen_matrix.py --check` | 0 | `matrix: OK (94 rows, 0 untested)` |
| `bash scripts/lint_hdl.sh` | 0 | 41 modules `LINT OK` |
| `git diff --check 044cb25f 84f6d6a` | 0 | empty |
| `make -C tb/srp_top -j2` | 0 | `8706 checks: 8706 PASS, 0 FAIL` (the FIFO-arm shapes first) |
| `make -C tb/srp_encoder -j4` | 0 | `1659 checks: 1659 PASS, 0 FAIL` |
| `make -C tb/srp_stream_fsms -j4` | 0 | `1512 checks: 1512 PASS, 0 FAIL` |
| `python3 -B tb/elab_guards/guards.py --jobs 2` (Verilator and the local Yosys) | 0 | `elab guards: 160 checks: 160 PASS, 0 FAIL` |
| `guards.py --frontend yosys --only KL_srp_top.g_vids_fit` | 0 | `34 checks: 34 PASS, 0 FAIL` (13 refused at `KL_srp_top.sv:273`, 12 elaborates) |
| `tb/elab_guards/mutants.py --only` the five `g_vids_fit` arms | 0 | `elab guard mutants: 5 of 5 killed` |
| `python3 -B tb/srp_top/mutants.py --jobs 5` | 0 | `365 checks: 365 PASS, 0 FAIL`; `assertion coverage: 185/185; missing=[]`; every arm KILLED; 342 of 342 arm lines identical to the author's receipt (67 min wall) |
| reviewer probes p1, p3, p4, p8 on `tb/srp_encoder` (p1, p3 also on `applicant`) | 2 each on the encoder | p1 fails VR14 and VR16; p3 fails VR15 and VR16; p4 fails VR18 (withdraw); p8 fails VR17. p1 and p3 pass `applicant` 21/21 |
| in-tree arms `vlan-link-keeps-registrar`, `vlan-link-no-begin` on `applicant` alone | 2 each | the first fails both AP8 rows; the second fails the restart row, 20/21 |

**Published evidence check.** `scripts/verify_manifest.py` was run over kebag-logic/milan-fpga `6ef09f9d` `review-evidence/pp216-r1`. All 1310 `MANIFEST.json` entries match their `published_sha256`, with 0 missing and 0 unlisted. Of these, 521 are under `author-r2/`, 9 of them path-redacted (`receipts/evidence-manifest-check.txt`).

**Clone integrity** (`scripts/clone_integrity.sh`, `receipts/clone-integrity.txt`). After every probe the reviewed clone is at HEAD `84f6d6a…` with tree `3582db8c…`. `git status --porcelain --ignored` is empty, and the index entries (mode, blob, path) are identical to `ls-tree -r HEAD`. There are zero gitlinks, because this repository has no submodules. Every probe ran on copies under the packet's `scratch/`.

**Hosted evidence at the exact head** (`receipts/hosted-checks-at-head.tsv`, read 20:01Z; observation only).
- The `hdl` workflow's push run 42671237160 completed `failure` with zero jobs, so it started no job.
- The pull_request run 42671247024 lists only `suites`, `in_progress` since 18:08Z. There is no `docs-gates` or `portability` job in it.
- The delta does not touch `.github/` (the workflow at the head has all three jobs). So this is not attributable to the change, but there is no hosted docs or portability result at this head. The manager owns hosted and act acceptance.

## Real limits

- **Banks not re-run.** I did not run the full `scripts/run_suites.sh` sweep, `syn/yosys/run.sh`, the area flow, `check-req-tags.py` with executed evidence, `tb/pp_top`, or the AECP, MAAP, ADP and aecp_cmds campaigns. Full banks are not allowed here, and the HDL outside `hdl/srp` is untouched. For those I rely on the author's published, manifest-checked receipts (the sweep's merged record and per-suite counts, `pp_top 11066`, `req-tags ... OK`, the area summaries).
- **Parent and twin not re-run.** I did not re-run the parent consumer gates or the twin; that is not allowed. Items 6 and 7 are judged on the published receipts.
- **Local tool versions.** The local sv2v is v0.0.13, and CI pins v0.0.12. The guard results agree with the author's CI-pinned run (`proc/elab_guards.*`: 96/96 with Yosys alone). The bench README notes the `error` arm reads differently under 0.0.13. All five arms were killed here.
- **Specification text.** I had no specification PDFs. Table 10-3, 10-4 and 10.7.5 cells and sub-clause numbers were checked against the clause structure and the author's `STANDARDS.txt` quotations, not the printed text.
- **Not a merge-candidate review.** This is a source-head review. The current-dev merge candidate (source base `044cb25f` against live dev `123f57a922bf07476cd69f91867f3b6f07080804`) is not covered, and no manager source bank ran at this head. Physical calibration was NOT RUN, and skipped field contexts are not hardware proof.
- **Path redaction.** The published logs are path-redacted copies: the local home and packet paths are replaced by placeholders. The unredacted originals stay in the unpublished scratch.

## Pending manager duties

- At the merge turn, build and validate the current-dev merge candidate (builder and native banks) and link its receipts.
- Own hosted and act acceptance. At 20:01Z the push run had started no job and the pull_request run had only `suites` in progress, with no `docs-gates` or `portability` job.
- Open the follow-up for the seven pre-existing stale `tb/srp_top/README.md` arm counts (ruling item 4; none filed yet).
- Track #220, the stream Applicants at LINK_UP.
- On the parent side, delete the three owed twin rows when this head is adopted.
- Optionally carry S1 and S2 to the author.

R801-2 FINISHED
